import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
checks=[{"check":p,"pass":(ROOT/p).exists()} for p in ["README.md","STUDENT_PROFILE.md","PROGRESS.md","DECISIONS.md","EVALUATION_REPORT.md","BENCHMARKS.md","MODEL_CARD.md","DATA_CARD.md","PRESENTATION.md","PROJECT_SUMMARY.json","SUBMISSION.yml"]]
checks.append({"check":"notebooks 00-08","pass":all((ROOT/"notebooks"/f"{i:02d}.ipynb").exists() for i in range(9))})
out={"checks":checks,"passed":sum(x["pass"] for x in checks),"total":len(checks)}
(ROOT/"reports/preflight.json").write_text(json.dumps(out,ensure_ascii=False,indent=2),encoding="utf-8"); print(json.dumps(out,ensure_ascii=False,indent=2))
