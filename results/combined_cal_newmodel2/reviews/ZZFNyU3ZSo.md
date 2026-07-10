## Summary

This paper proposes UniMoD, a task-aware token pruning method for unified multimodal transformers that handle both generation and understanding tasks. It first conducts an empirical analysis of unified transformers (attention weight patterns, ARank-based redundancy, task interactions), revealing that token redundancy differs across tasks and layers. Based on these findings, UniMoD employs separate task-specific routers for generation and understanding tasks rather than a single shared router. Applied to Show-o and Emu3, it reduces training FLOPs by 15% and 40% respectively while maintaining comparable performance.

## Strengths

- **Principled motivation grounded in thorough empirical analysis (Sec. 3).** The paper does not just propose a method and run experiments; it first conducts a multi-faceted empirical analysis — attention weight patterns across tasks/layers, ARank-based redundancy measurement across four unified models, competitive token pruning experiments, and task interaction studies. This analysis (Sec. 3.2–3.4) gives a clear rationale for why a single shared router should fail and constitutes a useful characterization of redundancy in unified transformers that is not available in prior work at this level of detail. **[favorability=10.04–12.69]**

- **Core finding about generation-task vulnerability is convincingly demonstrated.** The ablation study (Table 5) shows that naive MoD collapses generation quality (GenEval drops from 0.62 to 0.15, a 76% relative decline), while UniMoD recovers it to 0.61. The "w/o task-aware router" variant (single shared router at ARank-selected layers) also severely degrades generation (GenEval = 0.50 vs. 0.61). This convincingly demonstrates that generation tasks are far more sensitive to token pruning in unified transformers and that task-specific routing is necessary to protect them — this is the paper's most important actionable result. **[favorability=8.30–11.89]**

- **Meaningful efficiency gains on Emu3.** A 40% FLOPs reduction on an 8.5B model while maintaining comparable performance across most benchmarks (Table 3) is a practically significant result. The explanation (Emu3 uses 4096 image tokens vs. Show-o's 1024, creating more redundancy to exploit) is coherent. **[favorability=7.97–11.94]**

## Weaknesses

### Fatal
None.

### Major
None.

### Minor

- **Mismatched baselines in the main results table (Table 3).** The EarlyExit and Interleaved Layer Skipping baselines reduce FLOPs by 50% (from 51.1 to 25.6 TFLOPs for Show-o), while UniMoD reduces by only 15% (to 43.3). These are mismatched compute budgets, making head-to-head comparison less informative — the baselines are much more aggressive and predictably perform worse. The ablation table (Table 5) partially addresses this by including "Basic MoD" and "w/o task-aware router" at FLOPs similar to UniMoD, but these should appear in the main table. **[favorability=3.31]**

- **Method description does not fully bridge the gap from ARank analysis to implementation choices (Sec. 4.1 vs. Sec. 5.1).** The "Layer switch module" describes a principled three-step procedure using ARank to select layers and determine pruning ratios. However, the specific implementation numbers — scaling MMU capacity from 1 down to 0.2, pruning 20% of T2I tokens, using 80% pruning in the last 16 layers for Emu3 (line 209) — are stated without showing how the ARank normalization maps to these precise values. While "last 12 layers" in a 24-layer Show-o is consistent with "the half of layers with the lowest ARank values" (since ARank decreases in later layers per Fig. 3a), the pruning ratios appear heuristic. The connection between the described procedure and the actual implementation should be made explicit. **[favorability=5.41]**

- **Emu3 results are on a custom setup that limits external validation.** As the paper states (line 242), "Our full Emu3 results differ from the original paper because we use alternative training datasets, as the official code and data are not publicly available." Both the Emu3 baseline and UniMoD rows in Table 3 use this custom setup (LLaVA-v1.5-mix-665K for MMU, Show-o's T2I data for generation), so the absolute numbers (e.g., MME=881.3, GQA=46.0 for the baseline) cannot be compared against published Emu3 results. The paper is transparent about this, but it means the reader has no independent reference point for the quality of the results. **[favorability=2.70]**

- **The ablation (Table 5) shows the task-aware router's marginal benefit is concentrated on generation tasks, which is not explicitly discussed.** The "w/o task-aware router" variant (single router at ARank-selected layers) performs competitively on understanding tasks (MME: 1052 vs. 1093.7; GQA: 54.4 vs. 54.5; POPE: 80.2 vs. 80.3; VQAv2: 65.5 vs. 66.2) at lower FLOPs (40.8 vs. 43.3). The task-aware router's main marginal improvement is on generation (GenEval: 0.50 vs. 0.61). The paper treats both tasks symmetrically in the framing; acknowledging that ARank-based layer selection drives most understanding-task gains would be more precise. **[favorability=6.46]**

- **The Shared MoD layer type is described in the architecture (Sec. 4.1) but never separately evaluated.** It is unclear when this layer type is used versus the task-specific MoD layers, and whether it provides any benefit in practice. **[favorability=5.07]**

- **No confidence intervals or statistical significance reported for any benchmark results.** Given that several comparisons are very close (e.g., Show-o GenEval: 0.62 baseline vs. 0.61 UniMoD; Emu3 GQA: 46.0 vs. 45.2), it is impossible to assess whether these differences are meaningful or within noise. Multi-seed runs or other measures of variance would strengthen the evaluation. **[favorability=2.63]**

### Trivial
None.

## Nice-to-Haves
- Move the ablation variants (Basic MoD, w/o task-aware router) from Table 5 into the main results table (Table 3) for a more informative comparison.
- Derive the pruning ratios explicitly from the ARank normalization formula, or clearly state which ratios were manually tuned and why.
- Report one-time setup costs (ARank pre-computation on 50 samples per task).
- Compare against MoMa on shared understanding benchmarks if feasible.
- Evaluate the Shared MoD layer type in the ablation.

## Removed Points
These points are flagged to be removed, treat them with caution:

1. **"15% FLOPs reduction for Show-o is marginal"** — Removed as a subjective framing nitpick. The paper accurately reports a 15% reduction for Show-o and 40% for Emu3. A 15% training FLOPs reduction on a 1.4B model during fine-tuning is not negligible, and the paper's framing ("efficient training") is reasonable.
2. **"MoE does not reduce training costs" criticism** — Removed as factually incorrect. The paper's characterization of MoE training costs is standard in the literature.
3. **"Basic MoD may be undertuned"** — Removed as speculative and unsupported; the paper explicitly states all ablations maintain the same pruning rate.
4. **MoMa comparison demand** — Removed because the paper already acknowledges MoMa in related work and explains why direct comparison is infeasible (MoMa lacks generation benchmarks and most understanding benchmarks).
5. **"First work" claim about novelty relative to MoMa** — Removed because the paper already addresses this in related work (lines 67–68) by noting MoMa's limitations.

## Novel Insights
None beyond the paper's own contributions. The most useful observations from the review process concern experimental framing and presentation choices (mismatched baselines, method-practice transparency, asymmetric benefits across tasks), not novel conceptual insights about the method itself.

## Suggestions
1. Revise the main results table (Table 3) to include properly matched-budget baselines — at minimum the "Basic MoD" and "w/o task-aware router" ablation variants already reported in Table 5.
2. Clarify the connection between ARank values and the specific pruning ratios/heuristics used in implementation. Either show the derivation or explicitly label which choices are manually tuned.
3. Add a brief discussion noting that the task-aware router's marginal benefit is concentrated on generation tasks, while ARank-based layer selection accounts for most of the understanding-task gains.
4. Report benchmark results with variance (multiple seeds or confidence intervals) for close comparisons.

## Score and Decision

MY FINAL SCORE: <score>6.0</score>
MY FINAL DECISION: <decision>Accept</decision>