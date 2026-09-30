# مِرآة (Mirror) — Arabic–English Entity Alignment

## 1. المشكلة

يهدف مشروع **مِرآة (Mirror)** إلى بناء نموذج أولي لمعالجة نص عربي وترجمته إلى الإنجليزية، ثم استخراج الكيانات المسماة من اللغتين وربط كل كيان عربي بمقابله الإنجليزي.  
يوفر المشروع قارئًا تفاعليًا بصيغة HTML؛ فعند تمرير المؤشر فوق كيان في إحدى اللغتين يظهر الارتباط مع الكيان المقابل في اللغة الأخرى.

## 2. النطاق

يشمل المشروع:

- تجهيز نص عربي من مجموعة **OPUS-100** للزوج `ar-en`.
- تنظيف النص وتقسيمه إلى جمل.
- ترجمة العربية إلى الإنجليزية باستخدام نموذج Helsinki-NLP.
- استخراج الكيانات العربية باستخدام CAMeL BERT، مع قواعد صريحة للتاريخ/الوقت.
- استخراج الكيانات الإنجليزية باستخدام spaCy.
- مواءمة الكيانات بين اللغتين باستخدام تشابه النص، وتوافق نوع الكيان، وعتبة مواءمة مقدارها `0.35`.
- إنتاج صفحة HTML تفاعلية تعرض الجملة العربية وترجمتها الإنجليزية وتربط الكيانات بصريًا.

**خارج النطاق:** لا يقدم المشروع ترجمة مرجعية مضمونة، ولا نظام NER إنتاجيًا، ولا تقييمًا دقيقًا لجودة الترجمة أو المواءمة لعدم توفر مجموعة ذهبية annotated gold set في التجربة المقدمة.

## 3. المعمارية

```text
OPUS-100 (Arabic)
       │
       ▼
تنظيف وتقسيم النص
       │
       ▼
Helsinki-NLP/opus-mt-ar-en
       │
       ├──────────────► النص الإنجليزي
       │
       ▼
استخراج الكيانات العربية ───────► استخراج الكيانات الإنجليزية
       │                                  │
       └──────────────┬───────────────────┘
                      ▼
              مواءمة الكيانات
        (Similarity + Type Compatibility
                 + Threshold 0.35)
                      │
                      ▼
             HTML تفاعلي ثنائي اللغة
```

### النماذج والمكونات

| المكوّن | المستخدم في المشروع |
|---|---|
| الترجمة | `Helsinki-NLP/opus-mt-ar-en` |
| NER العربية | `CAMeL-Lab/bert-base-arabic-camelbert-msa-ner` |
| NER الإنجليزية | `en_core_web_sm` |
| المواءمة | `SequenceMatcher` + Jaccard + توافق نوع الكيان |
| الواجهة | HTML + CSS + JavaScript |

## 4. الحدود

- استخراج الكيانات العربية قد يفوّت بعض الكيانات أو يحدد حدودها بصورة غير دقيقة.
- أخطاء الترجمة قد تؤثر مباشرة في مواءمة الكيانات.
- الاعتماد على التشابه النصي لا يلتقط جميع حالات التكافؤ الدلالي أو إعادة الصياغة.
- قيمة `THRESHOLD=0.35` هي عتبة تجريبية وليست نتيجة ضبط على مجموعة ذهبية.
- لا توجد في المواد المقدمة مجموعة gold annotations تسمح بحساب Precision أو Recall أو F1 للمواءمة.
- أرقام القياس المتاحة في هذا المستودع مأخوذة من artifacts مقدمة في المشروع، وليست ادعاءً لدقة النموذج.

## 5. روابط التشغيل الشخصية

- **GitHub:** `https://github.com/leenaotb12/bayan-nlp-leenaotb12`
- **Google Colab:** `https://colab.research.google.com/drive/1jVzY1LAU6NyPvAIbS08k6rjx3Ihhm3Iv?usp=sharing`
- **Demo / HTML:** `PASTE_YOUR_DEMO_URL_HERE`

> يُستبدل رابطا Colab وDemo بالرابطين الشخصيين الفعليين قبل التسليم. لم يتم اختلاق روابط غير موجودة في المواد المقدمة.

## 6. جدول النتائج والقياسات الفعلية

| القياس | القيمة | ملاحظة |
|---|---:|---|
| عدد الجمل في تجربة تجهيز النص | 78 | من تشغيل تجهيز OPUS-100 |
| عدد الكلمات في تجربة تجهيز النص | 1,208 | توقّف الجمع عند بلوغ 1200 كلمة تقريبًا |
| عدد صفوف جدول HTML في الـartifact المقدم | 96 | من ملف `نموذج ٢.html` |
| عدد معرّفات الكيانات الفريدة في HTML | 18 | `data-eid` |
| عدد امتدادات الكلمات الموسومة بالكيانات | 49 | `[data-eid]` |
| Precision / Recall / F1 | غير متاح | لا توجد gold annotations |
| BLEU / COMET | غير متاح | لم تُبنَ مجموعة مرجعية للتقييم |

**تنبيه منهجي:** قياس `78 جملة / 1,208 كلمة` وقياس `96 صفًا` يعودان إلى artifacts مختلفة من المشروع، لذلك لا أتعامل معهما على أنهما ناتج تشغيل واحد end-to-end.

## 7. خطوات إعادة التشغيل

### على Google Colab

```bash
!pip install -q transformers sentencepiece spacy datasets
!python -m spacy download en_core_web_sm
```

تجهيز البيانات:

```python
import re
from datasets import load_dataset

ds = load_dataset("Helsinki-NLP/opus-100", "ar-en", split="train", streaming=True)

lines, words = [], 0
for ex in ds:
    ar = ex["translation"]["ar"].strip()
    if len(ar.split()) < 6:
        continue
    if not re.search(r"[.!؟?]$", ar):
        ar += "."
    lines.append(ar)
    words += len(ar.split())
    if words >= 1200:
        break

open("input.txt", "w", encoding="utf-8").write("\n".join(lines))
print("عدد الجمل:", len(lines), "| عدد الكلمات:", words)
```

ثم تشغيل البرنامج:

```bash
!python entities_alignment.py input.txt entities_alignment_reader.html
```

والنتيجة هي صفحة HTML تفاعلية يمكن فتحها محليًا أو تنزيلها من Colab.

## 8. رمز البرنامج

الكود الأصلي محفوظ في:

- `notebooks/00.ipynb`
- `src/bayan/alignment.py`
- `src/bayan/pipeline.py`
- `reports/mirror_codes.html`

كما أن `mirror_codes.html` يوضح خلايا Colab وتسلسل خطوات التنفيذ في المشروع الأصلي.

## 9. أكاديمية سدايا

هذا المشروع أُنجز ضمن سياق التعلم والتطبيق في **أكاديمية سدايا (SDAIA Academy)**.

**#SDAIAAcademy**

## 10. المدربة

**المدربة:** `يُضاف اسم المدربة هنا`

> لم يرد اسم المدربة في الملفات المقدمة للمشروع، لذلك لم أضع اسمًا غير موثق.

## 11. المصادر

1. **Helsinki-NLP / OPUS-100** — بيانات الترجمة المستخدمة للزوج العربي–الإنجليزي.
2. **Helsinki-NLP/opus-mt-ar-en** — نموذج الترجمة المستخدم في المشروع.
3. **CAMeL-Lab/bert-base-arabic-camelbert-msa-ner** — نموذج استخراج الكيانات العربية.
4. **spaCy / en_core_web_sm** — نموذج استخراج الكيانات الإنجليزية.
5. مكتبات Python المستخدمة: `transformers`, `torch`, `spacy`, `datasets`, `difflib`, `re`.

## 12. الاعتمادات

- بيانات: OPUS-100 / Helsinki-NLP.
- نماذج المعالجة: Helsinki-NLP، CAMeL-Lab، spaCy.
- بيئة التنفيذ الأصلية: Google Colab.
- صاحبة المشروع: **leenaotb12**.

## 13. ملفات المستودع

```text
bayan-nlp-leenaotb12/
├── README.md
├── STUDENT_PROFILE.md
├── PROGRESS.md
├── DECISIONS.md
├── EVALUATION_REPORT.md
├── BENCHMARKS.md
├── MODEL_CARD.md
├── DATA_CARD.md
├── PRESENTATION.md
├── PROJECT_SUMMARY.json
├── SUBMISSION.yml
├── notebooks/
├── src/bayan/
├── tests/
├── reports/
├── sample_outputs/
└── scripts/
```
