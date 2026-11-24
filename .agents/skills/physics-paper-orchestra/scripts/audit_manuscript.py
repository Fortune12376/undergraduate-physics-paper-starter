#!/usr/bin/env python3
"""Lightweight, deterministic citation and TeX structural check. Not a compiler."""
import argparse, json, re
from pathlib import Path

def without_tex_comments(text):
    return re.sub(r"(?<!\\)((?:\\\\)*)%[^\n]*", r"\1", text)

def audit(tex, bib):
    text = without_tex_comments(Path(tex).read_text(encoding="utf-8"))
    bibtext = Path(bib).read_text(encoding="utf-8") if Path(bib).exists() else ""
    cited = set()
    for m in re.finditer(r"\\(?:cite|citep|citet|citealp|citeauthor)(?:\[[^\]]*\]){0,2}\{([^}]*)\}", text):
        cited.update(x.strip() for x in m.group(1).split(",") if x.strip())
    defined = set(re.findall(r"@\w+\s*\{\s*([^,\s}]+)",bibtext))
    env_start = re.findall(r"\\begin\{([^}]+)\}",text)
    env_end = re.findall(r"\\end\{([^}]+)\}",text)
    stack, errs = [], []
    for match in re.finditer(r"\\(begin|end)\{([^}]+)\}",text):
        op,env = match.groups()
        if op == "begin": stack.append(env)
        elif not stack or stack.pop() != env: errs.append(f"Mismatched environment near {match.start()}: {env}")
    if stack: errs.append(f"Unclosed environments: {stack}")
    missing = sorted(cited-defined)
    report = {"citations":len(cited),"bib_entries":len(defined),"missing_bib_entries":missing,"structural_issues":errs,"passed":not missing and not errs}
    return report

if __name__ == "__main__":
    p=argparse.ArgumentParser()
    p.add_argument("tex")
    p.add_argument("bib")
    a=p.parse_args()
    report=audit(a.tex,a.bib)
    print(json.dumps(report,indent=2))
    raise SystemExit(0 if report["passed"] else 1)
