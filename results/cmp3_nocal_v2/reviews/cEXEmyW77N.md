## Summary

This paper studies whether LLM-generated bibliographies are distinguishable from human ones by building a paired dataset of ~10,000 citation graphs (ground truth, GPT-4o, and field-matched random) and progressively testing structural features alone (RF ~0.60), aggregated semantic embeddings (RF ~0.83), and node-level embeddings with GNNs (~0.93). The core finding — that LLM bibliographies are structurally realistic but leave detectable semantic fingerprints — is well-supported and non-obvious.

## Strengths

1. **Large-scale paired dataset (Sec. 3).** Using 10,000 focal papers (~275k references) from SciSciNet with LLM-generated references paired to the same focal papers provides statistical power unavailable in prior work on this topic.

2. **Progressive analysis design (Secs. 4→5→6).** The clean decomposition — from interpretable structural features through aggregated embeddings to GNNs — cleanly demonstrates where discriminative signal lives. The finding that structure alone yields ~0.60 accuracy (near chance) while embeddings push to ~0.83 (RF) and ~0.93 (GNN) is the paper's central empirical contribution.

3. **Robustness breadth.** The paper checks across two LLM families (GPT-4o, Claude Sonnet 4.5), two embedding backbones (OpenAI, SPECTER2), three random baselines (field, subfield, temporally constrained), and cross-generator generalization (train on GPT-4o, test on Claude). The i.i.d. embedding control (accuracy collapses to chance when embeddings are replaced with random vectors of the same dimensionality) confirms the gains are semantic, not dimensional.

4. **Honest negative result (Table 1).** The paper explicitly reports that structural features fail (~0.60) rather than searching for inflated numbers, and the null result is correctly interpreted as the main finding about topology.

## Weaknesses

### Fatal
None.

### Major

1. **The 83% → 93% improvement is confounded between feature granularity and GNN architecture.** The RF on embeddings (Table 2) operates on *summed* graph-level embedding vectors — a single 3072-d vector per graph that aggregates all references. The GNNs (Table 3) operate on *node-level* 3072-d vectors, where each reference retains its individual embedding. The GNN therefore has access to much finer-grained semantic information (which specific papers the LLM selected vs. the human) that is lost in graph-level summation. The paper frames GNNs as "learn[ing] jointly from structure and node text" (Sec. 1) and "fus[ing] network structure with semantic representations" (Sec. 2), but the experimental design cannot separate whether the 10-point gap is driven by the GNN's message passing or simply by richer input features. An RF or MLP operating on node-level features pooled via a learned or fixed aggregation (mean, max, attention) would clarify whether the GNN's graph structure processing contributes anything beyond having per-node inputs. This does *not* undermine the paper's core claim (semantics work, structure doesn't — the RF-on-embeddings 83.5% alone supports that), but it means the headline 93% figure is less cleanly interpretable than it appears.

### Minor

2. **Data-splitting procedure does not guarantee that paired ground-truth and GPT graphs from the same focal paper stay in the same split.** The paper states (Sec. 6, Experimental setup) that "if a ground truth focal paper appeared in the train dataset, its respective random graph also appeared in the same split set" but says nothing about ground-truth / GPT pairs. If these paired graphs land in different splits, the GNN — which includes the focal paper's embedding as a node feature — could partially exploit focal-paper identity across splits. This is not fatal (the same focal paper appears with both labels, so there is no systematic label leakage), but it is an uncontrolled confound that the authors should either confirm is avoided or address via a controlled re-run.

3. **The difference in separability between GPT-4o and Claude is not analyzed.** The abstract reports RF separability of ~0.77 for Claude vs. ground truth, compared to ~0.83 for GPT-4o. The paper notes that 779 GPT-generated graphs were removed vs. only 89 Claude graphs (Sec. 3), resulting in different numbers of retained graphs (9,218 vs. 9,908). Whether the lower separability reflects Claude being genuinely more "human-like" or is an artifact of different data quality / matching rates is not discussed. This weakens the "robustness across LLM families" claim.

4. **No analysis of what semantic dimensions drive separability.** The paper shows that embeddings work but does not probe *why* — e.g., whether the signal is concentrated in recency, venue prestige, author team size, or topical specificity. The limitations section (Sec. 8) correctly flags this as future work, but even a simple feature-importance analysis on the RF (which embedding dimensions or projected directions are most predictive) would turn the 93% black-box result into an interpretable finding.

### Trivial

5. **No per-class precision/recall reported.** Accuracy and macro F1 are given, but the paper does not report whether the classifiers are equally good at catching GPT lists vs. avoiding false alarms on human lists.

## Nice-to-Haves

- An RF or simple MLP on per-node embeddings aggregated via mean/max/attention (keeping the same input dimensionality as the GNN) would cleanly decompose the 83% → 93% gap into a feature-granularity effect vs. a message-passing effect.
- A baseline classifying individual reference embeddings (is this reference LLM-generated or not?) and averaging per graph would show whether graph structure adds value beyond per-node semantics.
- Feature importance or projection analysis on the RF embedding classifier to reveal which semantic dimensions drive the separation.

## Removed Points

These points from the input review were filtered out as invalid, non-substantive, or violating the filtering rules:

1. **"Related work is thin / gap is unclear"** — Removed as inaccurate. The paper cites the most directly relevant prior work (Algaba et al., 2024, 2025; Mobini et al., 2025) and clearly positions its contribution as using induced citation graphs for detection, which the cited papers do not.
2. **"GNN test variance implausibly tight"** — Removed as speculative. The paper averages across multiple seeds and 500 hyperparameter configurations per model on a large (~18k graphs) dataset; tight variance is plausible.
3. **"Field-level random baseline too coarse"** — Removed because the paper already includes a subfield-level baseline (292 categories) that yields qualitatively similar results.
4. **"Abstract's 93% claim is overstated"** — Removed because the abstract wording ("GNNs with embedding node features achieve 93% test accuracy") is technically accurate.
5. **"Connection to broader capability frameworks is gestural"** — Removed as a trivial presentation point.
6. **"GNNs learn jointly from structure and text"** — Partially addressed in the Major weakness above; the paper's phrasing is somewhat overclaimed, but this is already captured.
7. **"Missing appendix / proof content"** — Removed by rule (parser strips appendices; they exist in the original submission).

## Novel Insights

The progressive decomposition result — that structural features achieve near-chance accuracy (~0.60) while aggregated embeddings jump to ~0.83 and node-level embeddings push to ~0.93 — is the paper's key contribution. The insight that LLM-generated bibliographies are *topologically* indistinguishable from human ones but *semantically* detectable is not entirely new (prior work found similar patterns at the reference level), but the paper's demonstration at the *graph* level with controlled baselines and at scale provides the cleanest evidence to date. The cross-generator generalization result (training on GPT-4o, testing on Claude achieves ~0.72 RF accuracy) is also non-trivial.

## Suggestions

1. Add a controlled experiment to decompose the 83% → 93% gap: train an RF or MLP on the same node-level embeddings used by the GNN, pooled via a simple aggregation (mean, max, or attention-weighted sum). If this matches the GNN's 93%, then message passing adds little; if it does not, the GNN is genuinely exploiting graph structure.
2. Clarify the data-splitting procedure: confirm whether ground-truth and GPT graphs from the same focal paper are always kept in the same split, or re-run with that constraint enforced.
3. Discuss the GPT-4o vs. Claude separability gap and whether the different graph-removal rates (779 vs. 89) could artifactually affect the comparison.
4. Add a brief feature-importance analysis on the embedding RF to identify which semantic dimensions (recency, venue tier, etc.) drive detection.

## Score and Decision

MY FINAL SCORE: <score>7.0</score>
MY FINAL DECISION: <decision>Accept</decision>