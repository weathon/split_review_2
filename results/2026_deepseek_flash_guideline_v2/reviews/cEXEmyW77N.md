## Summary

This paper constructs paired citation graphs (ground truth vs. LLM-generated) for 10,000 focal papers from SciSciNet and systematically tests whether LLM reference lists are distinguishable from human ones. Using a progressive design—RF on structural features, RF on aggregated text embeddings, and GNNs with per-node features—it finds that structure alone barely separates GPT from ground truth (~0.60 accuracy) while semantic embeddings sharply improve separability (RF: ~0.83, GNN: ~0.93). Robustness checks include multiple LLM families, multiple embedding backbones, cross-generator generalization, field-matched random baselines, and an i.i.d. noise ablation.

## Strengths

1. **Progressive modeling empirically isolates the locus of discriminability** — The staged analysis (structure-only RF → embedding RF → embedding GNN) cleanly decomposes what each representation contributes, showing that the primary discriminative signal resides in semantics rather than topology. The i.i.d. noise ablation (Appendix 15) rules out high-dimensional artifact as an explanation, and the cross-generator experiment (GPT→Claude, ~0.72 RF) shows the finding generalizes beyond a single model family.

2. **Rigorously controlled random baselines at multiple granularities** — The paper constructs field-level, subfield-level, and temporally constrained random baselines (Section 3), all of which are cleanly separable from both GPT and ground truth (Table 1: ~0.89–0.93 accuracy). These controls go well beyond a single naive baseline and convincingly show that LLM-generated graphs mimic human citation topology rather than being merely "non-random."

3. **Multiple robustness checks that are genuinely informative** — The paper replicates with Claude Sonnet 4.5, uses two embedding backbones (OpenAI and SPECTER2), tests cross-generator generalization, and ablates with i.i.d. random vectors. These checks collectively show the result is not an artifact of a specific model, embedding, or feature dimensionality.

## Weaknesses

### Fatal
None.

### Major
None.

### Minor

1. **The 10-point gap between RF-on-embeddings (83%) and GNN-on-embeddings (93%) is not discussed or explained** — The paper frames its central finding as "the primary signature... lies not in topology but in semantic content" (line 175). However, the RF on *aggregated* embeddings achieves 0.83, while the GNN with *per-node* embeddings plus message passing achieves 0.93. This 10-point gap could arise from (a) per-node features retaining more information than graph-level summation, (b) the actual citation graph structure contributing additional signal beyond what aggregated semantics provides, or (c) the GNN being a more powerful classifier. The paper does not disentangle these. A simple control—permuting graph edges while keeping node embeddings identical—would determine whether the gap reflects genuine structural signal or simply finer-grained feature representation. Without this, the strong "structure vs. semantics" dichotomy in the narrative slightly outruns the evidence.

2. **The "semantic fingerprint" driving separability is not characterized** — The paper recommends that "detection and debiasing should target content signals" (Discussion), but never analyzes what those content signals actually are. The 3072-d embeddings remain a black box: the separation could be driven by recency bias, venue-prestige shifts, topical drift, or LLM-specific linguistic artifacts in generated titles, each with very different implications for debiasing. The paper acknowledges this in Section 8 as future work, which softens the criticism considerably, but the practical recommendation remains unactionable without any decomposition of what the embeddings capture.

### Trivial

- The structural feature set is limited to five hand-picked descriptors (degree/closeness/eigenvector centrality, clustering coefficient, edge count). The paper's claim that "structure alone cannot separate" should be qualified as "these specific structural features cannot separate"—more expressive descriptors (e.g., graphlet degree distributions, Weisfeiler-Lehman features) might capture additional signal. The paper acknowledges this implicitly but the qualification could be clearer.

## Nice-to-Haves

- A third LLM family (e.g., Llama or Gemini) would further strengthen generalization claims, since only OpenAI and Anthropic models are tested.
- Reporting test accuracy averaged over a set of top validation configurations (rather than the single best) would address any concern about optimistic bias in Table 3, though the transparent presentation of full validation distributions in Figure 4 already mitigates this.

## Removed Points

These points were identified by reviewers but removed for the reasons given; treat with caution:

- **"GNN test-set results are cherry-picked from hyperparameter sweeps"** — The paper reports the *full validation distribution* across the entire hyperparameter grid (Figure 4, showing KDEs and boxplots for all 500 configs per model), then selects the best validation config for test reporting (Table 3). For the embedding-based GPT vs. Ground Truth task, the validation distributions are tight around ~0.93 (narrow IQRs), so reporting the best config's test performance does not materially inflate results. The methodology is transparent and standard for this type of evaluation.

- **"Including the graph's total number of edges as a per-node feature is odd"** — The paper explicitly notes this design choice (line 137: "which is a graph level features but here assigned as node feature"). This is a transparent design decision, and since the structure-only GNN results are near-chance anyway, it did not affect conclusions.

- **"The GNN with structural features shows non-trivial variance with some configs above 0.6"** — Figure 4 (top-right panel) shows distributions centered at ~0.5 with some tail variance. The paper's characterization ("clustering around chance level") accurately describes the central tendency; occasional outliers above 0.6 do not change the conclusion that structure alone is unreliable for detection.

- **More detail needed on graph size distribution matching** — The paper briefly states it randomly removes references to match sizes (Section 3). The description is sufficient given that the main comparison uses matched sizes by construction, and the matching follows standard practice.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. **Add a permuted-edge control**: Feed the GNN the same 3072-d embeddings as node features but with randomized graph structure (edge permutation preserving degree sequence). If accuracy drops to ~0.83, genuine structural signal contributes; if it stays at ~0.93, the gap reflects per-node granularity rather than topology. Either outcome resolves the ambiguity in the paper's central interpretation.

2. **Characterize the semantic signal**: Provide a basic probe of what drives the embedding-based separation, e.g., by correlating classifier scores with interpretable covariates (mean publication year, venue prestige, topic-model shifts, title lexical diversity). This would turn the black-box finding into an actionable diagnostic.

3. **Slightly soften the narrative claim** from "detection should target content signals rather than global graph structure" to something like "content signals are the primary and most reliable target, though structure provides supplementary signal when combined with content."

## Score and Decision

**Calibration notes**: The calibration search tool was unavailable due to a path configuration issue, so I could not retrieve human-reviewed anchor papers for direct comparison. I instead rely on a careful reading of the paper's content against the ICLR scoring rubric.

**Reasoning**: This is a well-executed empirical study with a large-scale dataset, a clear experimental design, and unusually thorough robustness checks (multiple LLMs, multiple embedding backbones, cross-generator generalization, stratified random baselines, i.i.d. noise ablation). The core finding—that LLM-generated reference lists are structurally near-indistinguishable from human ones but separable via semantic embeddings—is interesting and practically relevant. The weaknesses are real (the 10-point GNN-vs-RF gap is not explained; the semantic signal is not characterized) but are matters of interpretation and depth rather than flawed methodology, and one of them is already acknowledged as future work. These issues are addressable with additional analysis rather than new data collection. The paper falls below the very strongest ICLR acceptances (which would typically introduce new methods or provide deeper mechanistic understanding) but is a solid empirical contribution to an important and timely problem.

MY FINAL SCORE: <score>6.5</score>
MY FINAL DECISION: <decision>Accept</decision>