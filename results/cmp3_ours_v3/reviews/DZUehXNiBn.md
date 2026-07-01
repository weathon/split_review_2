Here is the final consolidated review:

---

## Summary

VISTA is a model-agnostic, modular framework for causal structure learning that decomposes the global DAG learning problem into Markov Blanket (MB) subgraphs, applies any base learner to each subgraph independently, and aggregates local predictions via a weighted voting scheme followed by a Feedback Arc Set (FAS) acyclicity enforcement. The framework comes with finite-sample error bounds and an asymptotic consistency guarantee, and is evaluated on synthetic data (up to n=300) and the Sachs protein network (11 nodes).

## Strengths

1. **Clean, modular, model-agnostic design.** VISTA cleanly separates MB identification, local learning, weighted voting aggregation, and FAS post-processing. The framework operates purely on edge-level outputs and can wrap any base learner without modifying its internals (Section 3, Pseudocode in Figure 2). This is a genuine practical advantage over fusion methods that are tied to specific algorithms or require solver-based reconciliation.

2. **Proposition 3.1 (coverage guarantee) is a solid foundation.** The observation that every true edge appears in at least two MB subgraphs (the child's and the parent's) is simple but correctly establishes that no true edge is lost in the decomposition *if* MBs are accurately identified. This provides a clean correctness basis for the divide-and-conquer strategy.

3. **Runtime improvements are substantial and well-documented.** Table 3 shows consistent large speedups across multiple base learners: e.g., NOTEARS at n=300 goes from ~12,515s to ~2,137s (~5.9×); SCORE at n=300 is listed as infeasible standalone but runs in ~225s with VISTA; DAG-GNN goes from ~17,714s to ~1,960s. These gains are practically meaningful and stem directly from the parallelizable divide-and-conquer design.

## Weaknesses

### Fatal
None.

### Major

1. **The real-data evaluation is limited to an 11-node graph, which does not substantiate the "large-scale" framing.** The paper presents VISTA as a method for "large-scale causal discovery" (Section 1, line 21; abstract, line 9) and "large-scale DAG learning" (Section 3, line 47), but the only real-data evaluation is on Sachs (11 nodes, 17 edges — Table 4). While the synthetic experiments scale to n=300, a single tiny real-world graph is insufficient evidence that the method works for large-scale real-world applications. Adding at least one real or semi-real dataset with 50+ nodes would directly substantiate the claimed use case.

2. **Accuracy claims are overstated relative to what the strongest baselines show.** The abstract claims "notable improvements in both accuracy" (line 9) and the contribution list states VISTA "consistently improving robustness" (line 29). For the strongest base learner (NOTEARS, Table 1, ER), the improvement is modest: F1 0.76→0.79 (+0.03), SHD 208.80→182.40, while TPR *drops* from 0.74 to 0.68. The more dramatic F1 gains occur for base learners that perform poorly on their own (GraN-DAG: 0.06→0.17; SCORE: 0.14→0.31). The paper should calibrate its accuracy claims to reflect that the benefit is most pronounced for weak base learners and marginal for already-strong ones. The runtime improvements are the stronger and more consistent story.

### Minor

1. **The theoretical guarantees assume independent subgraph votes, which the method's design violates.** Theorem 3.2 models votes as A ~ Binomial(m, p) with independent subgraphs. The paper acknowledges this (line 138: "subgraphs learned from the same dataset can induce correlations among votes, so the bound should be interpreted as a qualitative guide") but provides no adjusted bounds or analysis of how dependence affects the guarantees. Since subgraphs share data (drawn from the same observational dataset) and the base learner's errors are correlated across overlapping subgraphs, the formal bounds (Theorems 3.2–3.5) apply to a cleaner setting than the one the method actually operates in. The theoretical section would benefit from a more precise statement of what it does and does not establish.

2. **The Naive Voting results reveal that the MB decomposition itself introduces substantial spurious edges, but this dynamic is not discussed.** Table 1 shows NV achieves FDR values of 0.86–0.95 across all base learners, and F1 collapses to near-identical values (0.23) for NOTEARS, GOLEM, and DAG-GNN. This pattern suggests the decomposition itself — not just base-learner errors — introduces a massive number of false edges that dominate the NV aggregation. WV then aggressively prunes these (FDR drops to 0.08–0.80, but TPR also generally decreases relative to the baseline). This changes the narrative: WV is doing heavy denoising of decomposition artifacts, not just "calibrating" base-learner outputs. The paper briefly mentions latent confounding (line 114) but does not connect this to the NV failure pattern. A more direct discussion would help readers correctly interpret what VISTA's WV is actually accomplishing.

3. **Comparison against other divide-and-conquer methods (DCILP) is relegated to the appendix.** The paper's contribution is a merging method, and the most natural comparison is against another merging method. While the appendix comparison exists (line 174: "in Appendix F.2, we provide a comparison between VISTA and DCILP"), the main experimental section (4.1) only compares VISTA against standalone full-graph baselines. This answers "does decomposition help?" but not "is VISTA's merging better than other merging approaches?" Including the DCILP comparison in the main text or at minimum referencing it with a summary in the main results section would strengthen the paper.

### Trivial
None.

## Nice-to-Haves

- An ablation quantifying the false-positive burden introduced by MB subgraph decomposition (e.g., for a known graph, count how many spurious edges appear across all MB subgraphs before any voting or thresholding).
- A systematic sensitivity table showing F1/SHD at different (λ, t) pairs across multiple base learners and graph types, beyond the λ-only sweeps in Figure 4.
- Disentangling the runtime analysis into MB identification time, base-learner time per subgraph, and aggregation time.
- A discussion of how MB size scales with graph structure (e.g., in scale-free graphs with high-degree hubs where MBs could be large).

## Removed Points

These points from the input review were removed according to the filtering discipline:

- **"CAM baseline mentioned but no results in tables"** — Removed because experimental details (Appendix F) are stripped by the parser; CAM results may be in the appendix.
- **"MB identification method is underspecified"** — Removed because experimental configuration details would appear in the stripped appendix.
- **"Runtime breakdown not specified"** — Removed as such details are typically in the stripped appendix.
- **"Calibrated claim used but never defined"** — Removed because the paper provides operational meaning through the precision-recall analysis and λ/t parameterization; this is a presentation preference, not a flaw.
- **"Theorem 3.4 bound opaque without derivation"** — Removed because the derivation is in Appendix E.1, which is stripped by the parser.
- **"Acyclicity ordering justification unclear"** — Removed because the paper provides a rationale (line 114: filtering before FAS "can lead to unnecessary precision loss as the remaining cycles must be resolved by removing stronger edges"). The critic's concern is about a design choice, not an error.
- **"No analysis of MB size scaling" and "metrics relationship not discussed"** — These are nice-to-have suggestions, not concrete weaknesses of the presented work.
- **Various other section-by-section notes about phrasing and presentation** — These are style preferences or points addressed in the stripped appendix.

## Novel Insights

The harsh critic's most insightful observation is that the NV results (FDR 0.86–0.95 across all base learners, with F1 collapsing to exactly 0.23 for NOTEARS, GOLEM, and DAG-GNN) reveal that the MB decomposition introduces a massive number of spurious edges into the candidate pool. This means WV is primarily doing aggressive denoising of decomposition artifacts rather than merely "aggregating" or "calibrating" base-learner outputs. The paper's own numbers support this reinterpretation, but the text does not highlight it. This shifts what VISTA is actually doing: not "integrating subgraph evidence" so much as "constructing a large noisy candidate set and then pruning aggressively."

## Suggestions

1. Add at least one real or semi-real dataset with 50+ nodes to substantiate the "large-scale" framing. Without this, the claim remains unsubstantiated.
2. Recalibrate the accuracy claims in the abstract and contribution list to reflect that gains are marginal over already-strong base learners and most pronounced for weak ones. The runtime story is the stronger and more consistent finding.
3. Discuss the NV noise-introduction dynamic more directly — it would help readers understand what VISTA's WV is actually doing and avoid the misleading impression that the decomposition is nearly lossless.
4. Move the DCILP comparison (or a summary of it) into the main text to substantiate the claim that VISTA's merging is better than existing merging approaches, not just better than no merging at all.

---

## Calibration Report

**Retrieved anchors (all from deepreview_13k_calibration):**

| Path | Avg Human Score | Round | Comparison to VISTA |
|------|----------------|-------|---------------------|
| `nSDOkm0SKo.md` (Financial Markets) | 1.00 | Round 1 (high_score=1.5) | Unrelated topic, clear reject — far below VISTA |
| `5lUdTogEL3.md` (Person Re-identification) | 1.00 | Round 1 (high_score=1.5) | Unrelated topic, clear reject — far below VISTA |
| `JzFLBOFMZ2.md` (LLM + CSL) | 3.20 | Round 1 (1.5–3.5) | Similar domain (causal discovery); lower-quality paper with mixed reviewer scores. VISTA has cleaner framing and stronger experiments. |
| `AvXrppAS2o.md` (Outcome prediction + CSL) | 3.00 | Round 1 (1.5–3.5) | Similar domain, weaker technical contribution. VISTA is stronger. |
| `UAkVjK00Wv.md` (Auto-Ensemble large BNs) | 4.75 | Round 1 (3.5–5.5) | Divide-and-conquer BN learning with ensemble idea. Similar quality; VISTA has cleaner modular design and theoretical analysis. |
| `DUfwD5yiN4.md` (Exact Distributed BN Learning) | 5.25 | Round 1 (3.5–5.5) | Directly comparable (distributed structure learning). Similar strengths (clean theory) and weaknesses (limited real-data evaluation, few baselines). VISTA has more baselines and better runtime results. |
| `Lxst78Rrwj.md` (Causal Graph via Distributional Invariance) | 5.00 | Round 1 (3.5–5.5) | Different technical approach but same evaluation setting. Similar quality tier. |
| `Idygh9MX0N.md` (Multi-Agent CSL + LLM) | 3.40 | Round 1 (1.5–3.5) | Weaker paper with mixed reviews. |
| `3n6DYH3cIP.md` (Extendable BN Learning) | 5.60 | Round 1 (5.5–7.5) | **Accepted paper.** Similar scope (scalable structure learning). Strong experiments and theory. VISTA is comparable in quality but has weaker real-data evaluation and more overstated claims. |
| `9UGAUQjibp.md` (Quantized Local Indep. RL) | 5.80 | Round 1 (5.5–7.5) | Different domain but similar quality tier. |
| `mGmx41FTTy.md` (Topological Ordering for DAGs) | 6.33 | Round 1 (5.5–7.5) | Higher-scoring causal discovery paper. Stronger experimental evidence. |
| `xByvdb3DCm.md` (Selection + Interventions) | 8.00 | Round 1 (7.5–8.5) | Clear accept — far above VISTA in theoretical depth and clarity. |

**Round 1 bracket:** [4.5, 6.0] — VISTA is clearly above papers in the 1–4 range (which have serious flaws or limited contributions), comparable to papers in the 4.75–5.60 range, and below papers in the 6+ range (which have stronger evidence or fewer framing issues).

**Final score rationale:** VISTA is most comparable to "Exact Distributed Structure-Learning for Bayesian Networks" (5.25) and "Extendable and Iterative Structure Learning for Bayesian Networks" (5.60, accepted). It sits between them — its experimental scope and runtime results are stronger than the former, but its real-data evaluation gap and overclaiming prevent it from reaching the level of the latter. The core contribution (modular, model-agnostic framework with weighted voting) is solid and practically useful, but the paper's framing outruns its evidence in several ways.

MY FINAL SCORE: <score>5.5</score>
MY FINAL DECISION: <decision>Reject</decision>