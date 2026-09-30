# Evaluation Report

## Available measurements
- Input preparation: 78 sentences / 1,208 words.
- Supplied HTML: 96 rows / 18 unique aligned IDs / 49 entity-word spans.

## Quality metrics
Precision, recall, F1, BLEU/COMET, and human agreement are not reported because no gold annotations/reference evaluation set was supplied.

## Suggested slices
PERSON, LOC/GPE, ORG, DATE/TIME, MISC, and multiword entities.

## Observed limitations
The supplied HTML contains noisy source examples and translation mismatches. Similarity alignment can fail when translation is non-literal or entity surface forms differ.

## Evaluation gap
A small manually annotated test set with Arabic spans, English spans, entity types, and gold alignments is the next required step for defensible quality metrics.
