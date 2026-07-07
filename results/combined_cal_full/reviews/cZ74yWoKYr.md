## Summary

This paper formalizes the problem of critical KV cache entry selection for LLM inference from an output perturbation perspective. It derives an upper bound on the attention output perturbation (Theorem 3.3) that includes both attention weights and value states projected through the output matrix — moving beyond heuristic attention-weight-only selection. Based on this bound, it proposes a two-stage greedy selection algorithm (Algorithm 1) that splits the budget between attention-weight-based selection (Stage 1) and a combined metric of attention weights and projected value states (Stage 2). When integrated as a plug-and-play enhancement into three SOTA cache eviction methods (SnapKV, AdaKV, HeadKV), the algorithm consistently reduces compression loss across 3 LLMs (7B–32B), 29 datasets from Ruler and LongBench, and multiple cache budgets (20%–80%).

## Strengths

- **Formal reframing of a heuristic-driven area.** The paper provides Definition 3.1 (minimizing output perturbation) and Theorem 3.3 (an upper bound involving value states and the output projection matrix), giving the cache eviction literature a concrete objective to optimize. This is the first formal treatment of the selection problem rather than relying solely on accumulated attention weights.

- **Consistent and substantial empirical gains across diverse settings.** Across 3 LLMs (7B–32B), 3 cache eviction methods, 29 datasets, multiple cache budgets, and multi-turn QA (SCBench), the method consistently improves over base methods. Gains are often large — e.g., AdaKV at 40% on Ruler: loss drops from 13.9% to 1.8% on Llama-3.1-8B. The 97.8% success rate across 90 long-dependency test cases in LongBench (Section 4.3) is strong evidence of robustness.

- **Minimal computational overhead.** Section 4.6 shows the additional prefill TTFT is only 0.06s (batch 1) or 0.04s per request (batch 4) at 32K context, with decoding latency identical to base methods. The method adds only a linear operation (computing ‖VW^O‖₁ per head), making it practical for deployment.

- **Thorough ablation of the two-stage design.** The α sensitivity analysis (Table 4) shows that setting α=0 (removing the attention-first stage) causes catastrophic degradation on Mistral-7B (score 31.94 vs. 42.85 with α=0.5), validating that Stage 1 serves a real function in ensuring Assumption 3.4, not just a ceremonial role.

- **Perturbation analysis confirms the theoretical motivation.** Section 4.7 provides head-level, layer-level, and budget-level perturbation visualizations showing that the method consistently lowers actual output perturbation (92% of attention heads in Llama-3.1-8B), confirming that the theoretical bound translates to practical gains.

## Weaknesses

### Fatal
None.

### Major
None.

### Minor

- **The algorithm is a greedy heuristic inspired by the bound, not a true optimization of it.** The abstract claims the algorithm "optimizes the worst-case output perturbation" and the text says it "constrains worst-case perturbations" (line 74). However, the authors acknowledge that "directly minimizing the upper bound θ remains non-trivial" (line 124). Algorithm 1 is a two-stage greedy Top-K procedure, not a joint optimization over entries. Stage 2 does directly minimize a stage-conditional upper bound (Theorem 3.5), but the overall algorithm is best described as a derivation-inspired heuristic. The empirical evidence is strong, so this does not invalidate the contribution, but the framing should be more measured (e.g., "a heuristic derived from a worst-case perturbation bound").

- **Stage 1 selects by pure attention weights, partially diluting the "beyond attention weights" narrative.** At α=0.5, half the budget is allocated to entries selected by attention weights alone (Stage 1). The paper repeatedly emphasizes that attention weights alone are insufficient (abstract, Section 3.3, Contribution 1), yet the method *augments* rather than *replaces* attention-weight selection. The two-stage design is justified by Assumption 3.4 (ensuring cumulative attention > 0.5 so the bound remains well-conditioned), but the paper's rhetoric somewhat overstates the departure from prior work.

- **Ambiguity in Algorithm 1 pseudocode.** Line 5 reads "for all K_i, V_i ∈ K, V that A_i ∈ Top_k(𝒜, b')" which references the combined-metric variable 𝒜 rather than the attention-weight variable A. The textual description (lines 126–127) clearly states Stage 1 selects by attention weights, but the pseudocode is inconsistent — it checks whether individual attention-weight values belong to the top-b' of the combined-metric vector, which is semantically unclear. This should be corrected (likely Top_k(A, b') for Stage 1).

### Trivial

- **No variance or confidence intervals reported.** Results appear to be from single runs without error bars. While the method is largely deterministic and this is common practice in the cache eviction literature, the absence of variance estimates makes it difficult to assess whether small improvements (e.g., 0.5-point gains on some LongBench tasks) are meaningful.

- **Notation imprecision in Equation (2).** The attention scaling factor uses √d (model dimension) where the standard scaled dot-product attention uses √d_h (head dimension). Since qK^T's dimensionality is determined by the head dimension d_h, the scaling should be √d_h. This does not affect the paper's theoretical contribution but should be corrected for accuracy.

## Nice-to-Haves

- **Oracle analysis:** For very small budgets (e.g., b ≤ 3), enumerating all subsets to find the truly optimal selection and comparing against Algorithm 1 would quantify how close the greedy heuristic comes to exact optimization on its own terms.

- **Ablation replacing Stage 1 with the combined metric:** An experiment where all b entries are selected by the combined metric alone (no two-stage design) would disentangle whether the two-stage structure is strictly necessary or whether the combined metric suffices when Assumption 3.4 holds naturally. The α=0 case in Table 4 partially addresses this, but α=0 also removes the cumulative-attention guarantee, confounding two effects.

- **Bound tightness:** Reporting the ratio ℒ/θ for a few sample heads would show whether minimizing the upper bound θ actually drives down the actual perturbation ℒ, or whether the bound is too loose to be informative.

## Removed Points

These points are flagged to be removed, treat them with caution:

- **"Reduces loss by more than half" claim not uniformly supported.** The paper says "on average across 29 datasets" and the aggregate data support this claim. Individual cases vary (from ~34% to ~87% reduction), but an average claim does not require uniform support. → Removed as a precision nitpick, not a genuine weakness.

- **Missing comparison with more diverse baselines.** The paper compares with SnapKV, AdaKV, HeadKV, and H2O — the established SOTA cache eviction methods. Asking for KeyFormer or gradient-based methods goes beyond the paper's stated scope and is not standard expectation in this sub-area. → Removed as scope creep.

- **α=0.5 justification relies on Appendix A.** The paper states this is "verified in Appendix A" (line 172). Appendices are stripped by the parser; this is a known artifact, not an author omission. → Removed as per rules.

- **Missing: oracle analysis, disentangling stages, bound tightness quantification.** These are nice-to-have suggestions from the "Strengthening the Paper" section rather than actual weaknesses. → Moved to Nice-to-Haves above.

- **Section 3.2 readability / notation issues.** The harsh critic noted that Section 3.2 "needs to be reformatted" and that equations could be simplified. These are readability preferences, not substantive errors. → Removed as stylistic.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

- Correct the pseudocode in Algorithm 1 line 5 to reference A (attention weights) rather than 𝒜 for Stage 1, to match the textual description.
- Replace "optimizes the worst-case output perturbation" in the abstract with "is derived from a worst-case perturbation bound" or similar phrasing that accurately describes the greedy heuristic nature.
- Add standard deviations or confidence intervals for aggregate benchmark results where feasible.
- Fix the scaling factor in Equation (2) from √d to √d_h for accuracy.

## Calibration

**Round 1 bracket:** 5.5–7.5 (based on topical similarity and score distribution in the calibration corpus).

**Anchors retrieved:**

| Path | Avg Score | Round | Itemized | Comparision |
|------|-----------|-------|----------|-------------|
| lRTDMGYCpy.md (THIS PAPER's own human reviews) | 5.75 | R1 | Yes | Human scores: 5,6,6,6. Their strongest weakness (-7.07: "incremental, claims lack support") is harsher than my assessment; their strongest strength (+4.71: "well-motivated with theoretical guarantees") matches my assessment. My draft has weaker negative items (max -2.57) than the human reviewers (-7.07), but the human reviewers' criticisms include several questionable claims (e.g., "marginal improvement" contradicts the data). |
| 0ZcQhdyI3n.md (LSH-E) | 3.83 | R1 | Yes | Lower-scoring KV cache compression paper. Weaker empirical validation and novelty questions. Our paper's formal framing and stronger experiments justify a higher score. |
| Q5VlpYRxGF.md (KVMerger) | 4.33 | R1 | Yes | KV merging approach with limited baselines and novelty concerns. Our paper has stronger theoretical grounding and more comprehensive evaluation. |
| CkCFoN3j4s.md (Locret) | 5.80 | R1 | Yes | Training-based eviction with strong results but novelty concerns (-8.84 weight). Our paper's training-free, theory-grounded approach is comparable in quality. |
| jZVNmDiU86.md (PyramidKV) | 5.60 | R1 | Yes | Observation-driven budget allocation with novelty concerns (-9.28, -8.64 weights). Similar score range; our paper has stronger theoretical novelty. |
| 4QWPCTLq20.md (IntelLLM) | 3.00 | R1 | No | Lower-scoring, less rigorous evaluation. |
| 2DD4AXOAZ8.md (MixAttention) | 2.00 | R1 | No | Architecture modification, not a cache selection method. |
| vw0NurJ7UX.md (PrefixQuant) | 3.00 | R1 | No | Quantization-focused, different subproblem. |
| pG820nmDvy.md (Huge Context on Tiny GPUs) | 4.67 | R1 | No | Top-k selection method with weaker experiments. |
| tcq7n0m7Ml.md (EMS) | 4.60 | R1 | No | Evict-then-merge approach, less theoretical grounding. |
| HzBfoUdjHt.md (D₂O) | 5.80 | R1 | No | Dynamic eviction, similar scope but less formal. |
| OfjIlbelrT.md (FlexPrefill) | 8.00 | R1 | No | Higher-scoring but on sparse attention prefill, not cache eviction. Different subproblem. |

**Weighted-item comparison:** My draft's strongest positive weights (+5.03, +5.20, +5.40 for empirical strength, efficiency, perturbation analysis) align with the human reviewers' strongest positives for this paper (+4.71, +4.95, +4.38). My weaknesses have weights ranging from +1.13 to -2.57, which are milder than the human reviewers' strongest negatives for this paper (-7.07, -4.57, -3.76). However, the human reviewers' strongest negatives contain assertions I find unsupported (e.g., "incremental contribution" and "marginal improvement" that contradicts the paper's reported data). My assessment places the paper slightly above the human average, consistent with its position among topically similar papers (5.60–5.80 range).

**Final score derivation:** The paper's own human reviews average 5.75 (borderline accept). Compared to topically similar papers (3.83–5.80), it scores at the upper end. My assessment finds the theoretical framing genuinely novel and the empirical evidence unusually strong, with only presentation/framing weaknesses. This justifies a score at the upper end of the bracket — 6.0.

## Score and Decision

MY FINAL SCORE: <score>6.0</score>
MY FINAL DECISION: <decision>Accept</decision>