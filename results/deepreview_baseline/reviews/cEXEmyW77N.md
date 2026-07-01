## Summary

This paper presents a large-scale empirical study comparing LLM-generated reference lists (GPT-4o, Claude Sonnet 4.5) with human ground truth and field-matched random baselines, using citation graphs built from 10,000 focal papers (~275k references). The authors find that structural graph features (centrality, clustering, degree) alone cannot distinguish LLM from human graphs (~60% RF accuracy), while semantic embeddings (title/abstract from OpenAI text-embedding-3-large, SPECTER) enable much higher separability (RF ~83%, GNNs with embedding node features ~93%). The paper concludes that LLM bibliographies mimic human citation topology but carry detectable semantic fingerprints, so detection and debiasing should target content rather than structure.

## Strengths

- **Large-scale, systematic evaluation.** The study uses 10,000 focal papers and constructs paired ground truth, LLM-generated, and random graphs, providing strong statistical power. Multiple random baselines (field-level, subfield-level, temporally constrained) ensure that the comparison is rigorous.

- **Comprehensive robustness checks.** The pipeline is replicated across two LLM families (GPT-4o, Claude Sonnet 4.5) and two embedding models (OpenAI, SPECTER). Cross-generator generalization experiments and an i.i.d. feature control (Appendix results 15) confirm that the semantic signal is genuine and not an artifact of feature dimensionality.

- **Clear, actionable conclusion.** The paper cleanly separates what structure captures (topology mimicry) from what it misses (semantic drift), and the progressive modeling path from interpretable features to GNNs makes the argument easy to follow. The practical recommendation—focus detection on content signals—is well supported.

## Weaknesses

### Fatal
None.

### Major

1. **Limited novelty relative to prior work.** The core observation that LLM-generated reference lists are structurally similar to human ones while differing semantically has already been established by the same authors' earlier papers (Algaba et al., 2024, 2025) and related work (Mobini et al., 2025). The primary new contribution here is the *detection framework* (RF + GNN) rather than new insights about *how* LLM bibliographies differ. The paper would be strengthened by articulating what is added beyond prior descriptive analyses.

2. **No ablation isolating graph structure from embeddings in GNNs.** The GNNs achieve 93% accuracy using 3072-D node embeddings, while RF on aggregated embeddings reaches 83%. It is unclear whether the GNN's graph message passing contributes anything beyond the embeddings themselves. An ablation using a simple MLP on per-node embeddings (without any graph structure) would clarify whether the additional 10% comes from topology or from using node-level (rather than graph-level) inputs. As presented, the GNN may be functioning primarily as an embedding aggregator.

### Minor

- The semantic analysis is shallow. The paper uses pre-trained embeddings as a black box and does not probe *which* dimensions drive separability (e.g., recency, venue prestige, author overlap, topical drift). The conclusion that detection should target "content signals" remains generic. A more fine-grained analysis (e.g., comparing embedding dimensions, nearest-neighbor topical drift, or recency distributions) would significantly deepen the contribution.

- The random baseline, while rigorous, is an *anti-realistic* baseline: it destroys all latent structure. A more challenging baseline—e.g., sampling references from the same field with matched recency/prestige distributions but no citation structure—would better test the limits of structural separability. The paper shows that structure fails against the easy baseline, but this is already expected.

### Trivial

- The paper uses "mean F1-score" in Tables 1 and 2, but F1 is typically reported as a macro or weighted average in binary settings; the meaning should be clarified.

## Nice-to-Haves

- Conduct the GNN ablation (MLP on node embeddings vs. full GNN) to quantify the contribution of graph structure on top of per-node embeddings.
- Analyze the embedding dimensions or use interpretable semantic features (e.g., average publication year of references, fraction of top-venue papers, self-citation rate) to characterize *what* the semantic classifier learns.
- Test whether the RF/GNN detectors generalize to LLM-generated references produced with retrieval augmentation (i.e., not purely parametric).

## Novel Insights

None beyond the paper's own contributions. The finding that structure-only classifiers fail while embedding-based detectors succeed is well demonstrated but largely confirms expectations from prior work. The systematic detection protocol and the demonstration that GNNs can exploit the semantic signal are the main additions.

## Suggestions

1. Add an ablation comparing GNNs on node embeddings vs. a simple MLP that ignores graph structure to isolate whether message passing provides any benefit beyond aggregated embeddings.
2. Replace or supplement the black-box embedding analysis with interpretable semantic features (e.g., recency, venue prestige, topical cosine distance to focal paper) to identify the specific semantic dimensions where LLM references diverge from human ones.

## Score and Decision

The paper is well-executed, large-scale, and addresses a timely and important question. However, its core findings are incremental over established results, and the semantic analysis lacks depth. The detection protocol is a solid methodological contribution, but not transformative for the ICLR community. A borderline accept is appropriate given thoroughness and reproducibility, balanced by limited novelty.

MY FINAL SCORE: <score>6.0</score>
MY FINAL DECISION: <decision>Accept</decision>