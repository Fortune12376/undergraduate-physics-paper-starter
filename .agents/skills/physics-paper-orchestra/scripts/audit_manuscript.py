#!/usr/bin/env python3
"""Audit active LaTeX citations, BibTeX publications and manuscript coverage."""
import argparse
import json
import math
import re
from pathlib import Path


IGNORED = re.compile(
    r"\\verb\*?([^a-zA-Z\s]).*?\1|"
    r"\\begin\{(comment|verbatim\*?|lstlisting|minted)\}.*?\\end\{\2\}|"
    r"(?<!\\)((?:\\\\)*)%[^\n]*",
    re.DOTALL,
)
TOKEN = re.compile(
    r"\\\\|\\(?P<cite>(?:cite|citep|citet|citealp|citealt|citeauthor|citeyear|"
    r"citeyearpar|citenum|Cite|Citep|Citet|Citealp|Citealt|Citeauthor|"
    r"onlinecite|nocite))\*?(?![a-zA-Z])"
    r"(?:\s*\[(?:[^\[\]{}]|\{[^{}]*\}|\[[^\[\]]*\])*\]){0,2}\s*\{(?P<keys>[^{}]*)\}"
    r"|\\(?P<include>input|include)\s*(?:\{(?P<path>[^{}]+)\}|(?P<bare>[^\s\\{}]+))"
    r"|\\bibliography\s*\{[^{}]*\}|\\appendix(?:es)?\b"
    r"|\\(?P<env>begin|end)\s*\{(?P<name>[^{}]+)\}"
)
CONDITIONAL = re.compile(
    r"\\\\|\\(if[a-zA-Z]*|else|fi)(?![a-zA-Z])"
)
BIB_ENTRY = re.compile(r"@([a-zA-Z]+)\s*([{(])\s*([^,\s})]+)\s*,")
IDENTIFIER = re.compile(
    r'(?:^|,)\s*(doi|eprint|archiveprefix|isbn|pmid)\s*=\s*'
    r'(?:\{([^{}]*)\}|"([^"]*)"|([^\s,}]+))', re.IGNORECASE
)
PAGE_LABEL = re.compile(
    r"\\newlabel\{citation-coverage:last-scientific-page\}\{\{[^{}]*\}\{([1-9]\d*)\}"
)


def active_text(text):
    text = IGNORED.sub(lambda match: match.group(3) or "", text)
    # Handle literal TeX branches while preserving other conditionals for TeX.
    parts, branches, start = [], [], 0
    for match in CONDITIONAL.finditer(text):
        flag = match[1]
        if flag is None:
            continue
        if all(branch is not False for branch in branches):
            parts.append(text[start:match.start()])
        if flag.startswith("if"):
            branches.append({"iffalse": False, "iftrue": True}.get(flag))
        elif branches and flag == "else" and branches[-1] is not None:
            branches[-1] = not branches[-1]
        elif branches and flag == "fi":
            branches.pop()
        start = match.end()
    if all(branch is not False for branch in branches):
        parts.append(text[start:])
    return "".join(parts)


def manuscript_tokens(path, root, issues, sources, ancestors=()):
    path = path.resolve()
    if path in ancestors:
        issues.append(f"Recursive TeX inclusion: {path.name}")
        return
    if not path.is_file():
        issues.append(f"Missing TeX source: {path.name}")
        return
    sources.add(path)
    for match in TOKEN.finditer(active_text(path.read_text(encoding="utf-8"))):
        if not match["include"]:
            yield match
            continue
        filename = Path((match["path"] or match["bare"]).strip())
        if not filename.suffix:
            filename = filename.with_suffix(".tex")
        target = root / filename
        if not target.is_file():
            target = path.parent / filename
        yield from manuscript_tokens(target, root, issues, sources, (*ancestors, path))


def manuscript(path, issues, sources):
    cited, scientific, included = set(), set(), set()
    # A wrapper without a document environment is also accepted by the audit.
    tokens = list(manuscript_tokens(path, path.resolve().parent, issues, sources))
    has_document = any(t["env"] == "begin" and t["name"] == "document" for t in tokens)
    active, appendix = not has_document, False
    stack = []
    for token in tokens:
        if token["env"] == "begin":
            stack.append(token["name"])
            if token["name"] == "document":
                active = True
        elif token["env"] == "end":
            if not stack or stack.pop() != token["name"]:
                issues.append(f"Mismatched environment: {token['name']}")
            if token["name"] == "document":
                break
        elif active and token[0].startswith(r"\appendix"):
            appendix = True
        elif active and token["keys"] is not None:
            keys = {key.strip() for key in token["keys"].split(",") if key.strip()}
            if token["cite"] == "nocite":
                included.update(keys)
            else:
                cited.update(keys)
                if not appendix and "thebibliography" not in stack:
                    scientific.update(keys)
    if stack:
        issues.append(f"Unclosed environments: {stack}")
    return cited, scientific, included


def bibliography(paths, issues):
    by_key, by_identifier = {}, {}
    for path in paths:
        if not path.is_file():
            issues.append(f"Missing bibliography: {path.name}")
            continue
        text = path.read_text(encoding="utf-8")
        matches = list(BIB_ENTRY.finditer(text))
        for index, match in enumerate(matches):
            kind, _, key = match.groups()
            if kind.lower() in {"string", "preamble", "comment"}:
                continue
            if key in by_key:
                issues.append(f"Repeated bibliography key: {key}")
                continue
            end = matches[index + 1].start() if index + 1 < len(matches) else len(text)
            fields = {
                field.lower(): (braced or quoted or bare or "").strip().lower()
                for field, braced, quoted, bare in IDENTIFIER.findall(text[match.end()-1:end])
            }
            doi = re.sub(r"^(?:https?://(?:dx\.)?doi\.org/|doi:\s*)", "", fields.get("doi", ""))
            isbn = re.sub(r"[-\s]", "", fields.get("isbn", ""))
            arxiv = fields.get("eprint", "") if fields.get("archiveprefix") == "arxiv" else ""
            identifiers = {
                "doi": doi if re.fullmatch(r"10\.\d{4,9}/\S+", doi) else "",
                "isbn": isbn if re.fullmatch(r"(?:\d{9}[\dx]|\d{13})", isbn) else "",
                "pmid": fields.get("pmid", "") if fields.get("pmid", "").isdigit() else "",
                "arxiv": re.sub(r"v\d+$", "", arxiv),
            }
            by_key[key] = key
            for kind, value in identifiers.items():
                if value:
                    by_identifier.setdefault((kind, value), []).append(key)
    for keys in by_identifier.values():
        roots = set()
        for key in keys:
            while by_key[key] != key:
                key = by_key[key]
            roots.add(key)
        root = min(roots)
        for key in roots:
            by_key[key] = root
    for key in by_key:
        root = key
        while by_key[root] != root:
            root = by_key[root]
        by_key[key] = root
    return by_key


def scientific_pages(tex, inspected_pages, sources):
    if inspected_pages is not None:
        return inspected_pages, "compiled PDF inspection"
    aux = tex.with_suffix(".aux")
    pdf = tex.with_suffix(".pdf")
    if aux.is_file() and pdf.is_file() and all(
        min(aux.stat().st_mtime_ns, pdf.stat().st_mtime_ns) >= source.stat().st_mtime_ns
        for source in sources if source.is_file()
    ):
        labels = PAGE_LABEL.findall(aux.read_text(encoding="utf-8", errors="replace"))
        if len(labels) == 1:
            return int(labels[0]), "compiled AUX page label"
    return None, None


def audit(tex, bib, *, pages=None, config=None):
    tex = Path(tex)
    bibs = [Path(bib)] if isinstance(bib, (str, Path)) else list(map(Path, bib))
    config = config or {}
    issues = []
    sources = set(bibs)
    cited, scientific, included = manuscript(tex, issues, sources)
    publications = bibliography(bibs, issues)
    defined = set(publications)
    missing = sorted((cited | (included - {"*"})) - defined)
    unique = {publications[key] for key in scientific & defined}
    groups = {}
    for key, publication in publications.items():
        groups.setdefault(publication, []).append(key)

    minimum = config.get("minimum_per_page", 3)
    target = config.get("target_per_page", [5, 8])
    if (not isinstance(target, list) or len(target) != 2
            or not all(type(value) in (int, float) and math.isfinite(value)
                       for value in [minimum, *target])
            or not 0 < minimum <= target[0] <= target[1]):
        raise ValueError("Expected positive, ordered minimum and two target densities")
    exception = config.get("approved_density_exception")
    if exception is not None:
        if not isinstance(exception, dict) or not all(
            isinstance(exception.get(field), str) and exception[field].strip()
            for field in ("approved_by", "reason", "approval_record")
        ):
            raise ValueError("Density exception requires approved_by, reason and approval_record")

    page_count, source = scientific_pages(tex, pages, sources)
    if page_count is not None and (type(page_count) is not int or page_count < 1):
        raise ValueError("Scientific page count must be a positive integer")
    report = {"scientific_pages": page_count, "unique_cited_publications": len(unique)}
    status = "INCOMPLETE"
    if page_count:
        density = len(unique) / page_count
        report.update(
            page_count_source=source, citation_density=round(density, 4),
            minimum_publications=math.ceil(minimum * page_count),
            target_publications=[math.ceil(value * page_count) for value in target],
        )
        if density < minimum:
            status = "WARNING" if exception else "FAIL"
            if exception:
                report["approved_density_exception"] = exception
        else:
            status = "PASS" if density >= target[0] else "WARNING"

    exclusions = config.get("reference_exclusions", {})
    if not isinstance(exclusions, dict) or not all(
        isinstance(reason, str) and reason.strip() for reason in exclusions.values()
    ):
        raise ValueError("Reference exclusions must map citation keys to scientific reasons")
    documented, unexplained = {}, {}
    for field in ("author_supplied", "recommended"):
        keys = config.get(field, [])
        if not isinstance(keys, list) or not all(isinstance(key, str) and key.strip() for key in keys):
            raise ValueError(f"{field} must be a list of citation keys")
        absent = sorted(key for key in set(keys) - scientific if publications.get(key) not in unique)
        documented.update({key: exclusions[key] for key in absent if key in exclusions})
        omission = [key for key in absent if key not in exclusions]
        if omission:
            unexplained[f"missing_{field}_references"] = omission
    if unexplained and status == "PASS":
        status = "WARNING"
    diagnostics = {
        **unexplained,
        "documented_reference_exclusions": documented,
        "missing_bib_entries": missing,
        "unused_bib_entries": sorted(defined - cited),
        "duplicate_publications": sorted(sorted(keys) for keys in groups.values() if len(keys) > 1),
        "structural_issues": issues,
    }
    report.update({key: value for key, value in diagnostics.items() if value})
    report["citation_coverage"] = "FAIL" if missing or issues else status
    report["passed"] = report["citation_coverage"] in {"PASS", "WARNING"}
    return report


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("tex", type=Path)
    parser.add_argument("bib", nargs="+", type=Path)
    parser.add_argument("--scientific-pages", type=int, help="Count from inspection of the current PDF")
    parser.add_argument("--citation-config", type=Path, help="Defaults to citation-coverage.json beside TeX")
    args = parser.parse_args()
    path = args.citation_config or args.tex.with_name("citation-coverage.json")
    try:
        config = json.loads(path.read_text(encoding="utf-8")) if path.exists() or args.citation_config else {}
        if not isinstance(config, dict):
            raise ValueError("Citation configuration must be an object")
        report = audit(args.tex, args.bib, pages=args.scientific_pages, config=config)
    except (ValueError, OSError) as error:
        parser.error(str(error))
    print(json.dumps(report, indent=2))
    return 0 if report["passed"] else 2 if report["citation_coverage"] == "INCOMPLETE" else 1


if __name__ == "__main__":
    raise SystemExit(main())
