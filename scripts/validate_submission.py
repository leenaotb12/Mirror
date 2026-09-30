import json
from pathlib import Path
from bs4 import BeautifulSoup
ROOT=Path(__file__).resolve().parents[1]
required=["README.md","STUDENT_PROFILE.md","PROGRESS.md","DECISIONS.md","EVALUATION_REPORT.md","BENCHMARKS.md","MODEL_CARD.md","DATA_CARD.md","PRESENTATION.md","PROJECT_SUMMARY.json","SUBMISSION.yml","src/bayan","tests","reports","sample_outputs","scripts"]
missing=[p for p in required if not (ROOT/p).exists()]
htmls=list((ROOT/"sample_outputs").glob("*.html")); stats={"missing":missing,"html_files":len(htmls)}
if htmls:
 s=BeautifulSoup(htmls[0].read_text(encoding="utf-8"),"html.parser"); ids=[x.get("data-eid") for x in s.select("[data-eid]")]
 stats.update(html_rows=len(s.select("tbody tr")),entity_word_spans=len(ids),unique_aligned_entity_ids=len(set(ids)))
(ROOT/"reports/submission_validation.json").write_text(json.dumps(stats,ensure_ascii=False,indent=2),encoding="utf-8")
print(json.dumps(stats,ensure_ascii=False,indent=2))
raise SystemExit(1 if missing else 0)
