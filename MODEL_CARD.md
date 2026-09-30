# Model Card

- MT: `Helsinki-NLP/opus-mt-ar-en`
- Arabic NER: `CAMeL-Lab/bert-base-arabic-camelbert-msa-ner`
- English NER: `en_core_web_sm` (Colab log: 3.8.0)
- Alignment: custom entity-level heuristic; threshold 0.35.

Intended use: educational/research prototype for Arabic-English entity-aware bilingual display.

Not intended for high-stakes, authoritative translation, legal/medical decisions, or production-grade accuracy claims.

Limitations: domain mismatch, missed entities, noisy translations, lexical similarity failures, and lack of gold-standard evaluation.
