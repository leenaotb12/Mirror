# Decisions

## Translation
Kept `Helsinki-NLP/opus-mt-ar-en` because it is the completed project's actual translation model. A larger model would change reproducibility.

## Entity extraction
Combined CAMeL Arabic NER with explicit Arabic date/time regex rules and spaCy `en_core_web_sm` for English.

## Alignment
Kept entity-level translation + Jaccard/SequenceMatcher similarity, type compatibility, threshold `0.35`, and greedy one-to-one matching. The supplied project lists `awesome-align` and `simalign` as alternatives.

## Measured extension
Added automated submission/artifact validation. This is an engineering/reproducibility extension; it is **not** presented as an accuracy improvement.
