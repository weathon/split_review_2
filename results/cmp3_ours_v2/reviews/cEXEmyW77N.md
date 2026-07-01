Now I have a clear calibration picture. Let me produce the final review.

**Round 1 bracket:** [5.0, 6.5] — the paper is clearly stronger than rejected 3-5 range empirical papers and comparable to mixed-outcome 5.5-6.5 range papers. The data split issue and framing imprecision prevent it from reaching the 6.5+ level of accepted papers like GraphEval or the Hallucinations probing paper.

**Narrowing to final score:** 5.5 — solid empirical contribution with one significant methodological gap (data split clarification needed) and several minor issues, sitting at the borderline between reject and accept at ICLR.

Here is my final review:

## Summary

This paper investigates whether LLM-generated bibliographies can be distinguished from human ones using graph structure versus semantic content. Using 10,000 paired citation graphs (ground truth vs GPT-4o/Claude-generated) from SciSciNet with field-matched random baselines, the authors find that structural features alone barely separate LLM from human (~60% accuracy), while title/abstract embeddings sharply increase separability (RF: ~83%, GNN: ~93%). Results are robust across two LLM families, two embedding models, three random baseline constructions, and cross-generator transfer.

## Strengths

- **Large-scale paired dataset.** 10,000 focal papers (~275k references) from SciSciNet with paired ground-truth, LLM-generated, and random graphs. The paired design enables direct structural and semantic comparisons that aggregate-level analyses cannot provide.

- **Well-designed random baseline.** The field-matched permutation baseline (preserving out-degree and field-level distributions, with subfield and temporal variants) cleanly isolates what structural realism means: the random baseline is structurally distinguishable (RF ~0.89-0.92) while the LLM graphs are not (RF ~0.60). This demonstrates that the structural mimicry is real, not a field-matching artifact.

- **Progressive, interpretable modeling strategy.** The paper moves from simple structural descriptors → RF on aggregated embeddings → GNNs, making the source of discriminative signal transparent. The control experiment with i.i.d. noise vectors (accuracy collapses to chance) cleanly rules out the trivial explanation that results are driven by feature dimensionality.

- **Multiple robustness checks.** Findings are replicated across (a) two LLM families (GPT-4o and Claude Sonnet 4.5), (b) two embedding models (OpenAI text-embedding-3-large and SPECTER2), (c) three random baseline constructions, and (d) cross-generator generalization (train GPT-4o, test Claude). Cross-generator transfer is a particularly strong test showing the embedding signal is systematic.

## Weaknesses

### Major

- **Data split procedure for paired GT/GPT graphs is underspecified (potential leakage).** The paper states (line 139) that the stratified split ensures ground-truth and random graphs from the same focal paper stay in the same split. It does *not* state whether the GT and GPT graphs from the same focal paper are also kept together. If a GT graph from focal paper X is in training and the paired GPT graph from X is in test, the model could exploit focal-paper-specific patterns, inflating reported test accuracy. The cross-generator experiment (train GPT, test Claude) partially mitigates this concern — leakage from GPT-specific focal-paper patterns could not help across generators — but the main GT-vs-GPT result needs clarification. The authors should specify whether focal-paper grouping was enforced across all graph types and report accuracy with this grouping enforced if it was not already done.

### Minor

- **The GNN gain over RF (~83% → ~93%) is not analyzed.** The paper attributes this gain to GNNs "learn[ing] jointly from structure and node text" (line 27), but structure alone is at chance (51-58% in Table 3). The gain could arise from (a) message-passing that denoises or smoothes embeddings via structural context (a genuine joint exploitation of structure and semantics through relational inductive bias) or (b) simply higher model capacity from the deep network. An ablation comparing GNN performance against an MLP on per-node embeddings with global pooling would clarify the source of this gain and strengthen the paper's structural-vs-semantic decomposition.

- **"Semantic fingerprint" framing is imprecise.** The abstract and conclusion use "semantic fingerprint" (lines 9, 29, 187) to describe detectable differences in LLM-chosen references. The experiments show that embedding-based classifiers can distinguish LLM from human reference lists — a real and practical finding. However, the paper does not probe *which* semantic dimensions drive separability (acknowledged as future work, line 187), leaving it unclear whether the classifier detects systematic LLM biases in paper selection (e.g., preferring certain venues, recency, methods) or simply captures the fact that different papers were chosen. The claims are not fatally overstated — the core finding (content > structure for detection) holds — but the framing could be more precise about what is being detected.

- **Undirected graph conversion discards potentially informative directional structure.** Citation graphs are directed. The paper converts to undirected to avoid "trivial in/out-degree differences" (line 63). This means direction-aware structural features (in-degree vs out-degree asymmetry, PageRank on the directed graph, temporal direction of citations) are not tested. The claim that "structure alone barely separates GPT from ground truth" should be qualified as "undirected structural features alone..." The temporal analysis (GPT recommends post-focal papers ~6% of the time) partially addresses this concern but does not resolve it.

- **GIN F1 of 47.23% on graph properties (GT vs GPT) is below chance.** This result in Table 3 is not commented on. It could indicate training instability or class imbalance issues in a particular split and warrants explanation.

- **Graph-level edge count assigned as per-node feature.** The paper (line 137) assigns the graph's total number of edges as a node feature — a graph-level constant duplicated across all nodes. This is an unusual design choice without justification or ablation.

### Trivial

- No explicit statistical significance testing is reported for the RF structure-vs-embeddings accuracy gap (~60% vs ~83%). Given the tight standard deviations the difference is clearly significant, but this should be stated.

## Nice-to-Haves

- Ablate GNN message passing vs a simple MLP on per-node embeddings with global pooling to pinpoint the source of the 83%→93% gain.
- Probe which embedding dimensions drive classification (recency, venue prestige, author count, topic dimensions) — the paper already identifies this as future work.
- Discuss practical detection scenarios: the RF on aggregated embeddings (83%) is much more practical than the GNN (which requires building the full citation graph) for real-world deployment.

## Removed Points

These points were raised in the input review but removed with justification:

- **"Table 3 formatting is hard to parse"** — formatting nitpick, removed per hard rules.
- **"GPT vs Random asymmetry (92.75% vs 89.56%) not discussed"** — interesting observation but not a weakness; the paper's claims don't depend on this asymmetry.
- **"Paper does not discuss practical detection scenarios"** — moved to Nice-to-Haves; outside the paper's stated scope.
- **"Overlap vs non-overlap subset analysis"** — this proposed control would not resolve the "what does the classifier learn" question, because a paper's embedding is a property of the paper itself, not of who recommended it; the separability necessarily arises from differences in which papers are selected.
- **Criticism that prior work already established LLM bibliographies differ from human ones** — the paper builds on this prior work (Algaba et al. 2024, 2025) and contributes the structural-vs-semantic decomposition and detection methodology, which the cited prior work did not provide.

## Novel Insights

The reviews surface a genuine methodological gap (data split specification) and several worthwhile ablations, but do not offer a fundamentally new interpretation of the paper's findings beyond what the paper itself provides.

## Suggestions

1. **Clarify the data split procedure.** State explicitly whether GT and GPT graphs from the same focal paper are guaranteed to remain in the same split, and report test accuracy with focal-paper grouping enforced.
2. **Add a GNN-vs-MLP ablation** to clarify the source of the 10pp gain over the RF on embeddings.
3. **Qualify structural claims** as referring to undirected structural features.
4. **Comment on the below-chance GIN F1** on graph-property features (Table 3).
5. **Report statistical significance** for the key structure-vs-embeddings accuracy comparison.

MY FINAL SCORE: <score>5.5</score>
MY FINAL DECISION: <decision>Reject</decision>

### Calibration Anchors Used

| Path | Avg Score | Round | Comparison |
|---|---|---|---|
| /home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/ccxD4mtkTU.md | 4.75 | Narrow | LLM misinformation detection; similar detection topic, less rigorous experimental design |
| /home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/oxEER3kZ9M.md | 4.75 | Narrow | AI-text detection sample complexity; theoretical focus, less empirical |
| /home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/EE75tyB5Ay.md | 5.33 | Narrow | ChatGPT detection generalization; similar approach, less comprehensive controls |
| /home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/dbniI5RyWH.md | 4.50 | Bracket | GNN comparison paper; weaker empirical contribution, rejected for insufficient novelty |
| /home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/BYwdia04ZA.md | 5.00 | Bracket | Embedding similarity metric; rejected for insufficient experiments |
| /home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/KRnsX5Em3W.md | 6.50 | Bracket | LLM hallucination probing; stronger paper with deeper insight into model internals |
| /home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/6NEJ0ReNzr.md | 5.75 | Narrow | Citation generation with planning; mixed reviews, rejected |
| /home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/5RUM1aIdok.md | 6.75 | Narrow | Graph-based LLM evaluation; novel method, strong results, accepted |