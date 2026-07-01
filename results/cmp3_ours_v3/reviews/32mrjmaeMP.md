Now I have sufficient calibration. Let me finalize the review.

**Bracket:** Based on calibration, the initial bracket is [6.0, 7.0]. The τJp paper (avg 6.00) is the most directly comparable — it has similar evaluation scope but requires data, has less theoretical depth, and lacks language experiments. The current paper addresses several weaknesses of τJp while having its own weakness (no error bars). The Partial Linearization paper (avg 7.00) is a clean, well-scoped paper but narrower in contribution. I narrow to **6.5** — clearly above the τJp baseline due to stronger theory, broader evaluation, and practical advantages, but not at the 7.0 level due to the missing statistical significance reporting.

## Summary

This paper proposes TAK (Task Arithmetic with KFAC regularization), a method for weight disentanglement in task arithmetic that avoids requiring external task data during regularization. The key insight is that representation drift regularization — which normally needs per-task data — simplifies under linearization to a quadratic form involving the Jacobian Gram matrix, which is identified as a generalized Gauss-Newton (GGN) matrix. The paper leverages Kronecker-Factored Approximate Curvature (KFAC) to make this tractable and introduces an O(1) aggregation scheme that merges per-task KFAC factors. Experiments across vision (CLIP ViT-B/32, B/16, L/14) and language (T5-base) benchmarks show TAK achieves competitive performance with data-dependent methods while being data-efficient.

## Strengths

1. **Clean conceptual derivation (Sec. 3.1–3.2).** The paper clearly derives that representation drift regularization under linearization reduces to a quadratic form of the Jacobian Gram matrix, then identifies this as a special case of the generalized Gauss-Newton matrix. This connection to well-studied curvature approximation techniques is a crisp and well-explained theoretical contribution that grounds the entire work.

2. **Practical O(1) aggregation scheme (Eq. 8, Table 3).** The Kronecker-accumulation heuristic that merges per-task KFAC factors into a single Kronecker product achieves *constant* storage and computation costs in the number of tasks, with negligible performance loss (~0.0–0.6 points) compared to the O(T) idealized multi-task formulation. This is a genuinely useful engineering contribution.

3. **Strong empirical showing in task negation (Table 2).** TAK achieves substantially lower target accuracy (better forgetting) while maintaining or improving control task preservation compared to baselines including τJp. On ViT-B/32: TAK achieves 3.4 target accuracy vs. τJp's 6.7, with control accuracy 62.4 vs. 60.8 — a decisive result in a practically important setting.

4. **Robustness to α scaling coefficient (Fig. 4a).** The paper demonstrates that TAK maintains stable accuracy across α ∈ [0, 2], eliminating the need for held-out tuning of this hyperparameter. This is a practical advantage over methods like τJp that are more sensitive to coefficient choice.

5. **Thorough efficiency analysis (Figs. 6, 7, 8).** The paper systematically examines KFAC estimation cost (4 minutes for all 8 Vision tasks), memory footprint, compression strategies (87% reduction via block-based compression with ~1 point drop), and scheduling regularization every N steps. This is more extensive than typical method papers and builds confidence in deployability.

## Weaknesses

### Fatal
None.

### Major

1. **No statistical significance reporting.** All tables and figures report single numbers without variance estimates, confidence intervals, or multiple seeds. This is a significant evidential gap because:
   - Differences between TAK and τJp in Table 1 are often 0.3–0.5 percentage points (e.g., ViT-B/16: 88.3 vs. 88.6 abs. accuracy), which is indistinguishable from noise with a single run.
   - In Table 3, the "accumulated" method (TAK) slightly *exceeds* the "idealized" multi-task method on ViT-B/16 (88.3 vs. 88.1) and T5-base (78.7 vs. 78.5). If the accumulated method approximates the idealized one, systematic outperformance suggests these numbers are within the noise floor.
   - Task negation results in Table 2 (e.g., TAK at 3.4 vs. τJp at 4.7 on ViT-B/32) show larger gaps that are likely meaningful, but without error bars the reader cannot assess significance.
   - The paper mentions "variance across seeds" once (line 318) but only in the context of MC sampling for KFAC estimation, not for the main experimental results.

   This weakness is **major** because it undermines the precision of comparative claims against baselines. However, it does *not* invalidate the core contribution — the theoretical derivation, the O(1) aggregation scheme, and the general finding that curvature regularization helps weight disentanglement are supported even without error bars.

### Minor

1. **"Dataless" framing is somewhat overclaimed.** The paper calls TAK "dataless" throughout (title, abstract, conclusions), but KFAC estimation requires 128 examples per task to estimate input/output covariances (line 302, 318). While the paper is transparent about this data use and the key advantage is avoiding access to *full training data* of other tasks at regularization time, the "dataless" label is technically too strong. A framing like "data-efficient" or "data-free at regularization time" would be more precise without diminishing the contribution.

2. **Non-linear regime justification relies on an unexamined premise.** The paper applies KFAC regularization in the non-linear regime paired with attention-only fine-tuning, justified by the claim that attention-only fine-tuning induces "approximately linear fine-tuning dynamics in Transformers" (line 227). While Jin et al. (2025) is cited for showing attention-only FT induces kernel-like behavior, the specific link to linear dynamics sufficient for the regularization to be theoretically exact is asserted rather than demonstrated. The paper appropriately hedges ("our regularization is not theoretically exact in the non-linear regime," line 227), but the non-linear results rest on a plausible but unsubstantiated premise. This does not affect the linearized regime results, which are the paper's primary contribution.

3. **No quantitative OOD detection metric despite relevant data.** Figure 5 shows that TAK produces clean separation between in-distribution and out-of-distribution Jacobian norms, and the paper notes this "suggests a natural use of our method for out-of-distribution detection" (line 298). However, no AUROC or standard OOD metric is computed from the already-available data. Computing this would directly strengthen the paper's claims about task localization.

### Trivial
None.

## Nice-to-Haves
- **Quantitative OOD detection evaluation:** Computing AUROC or similar metrics from the Jacobian-norm distributions in Fig. 5 would directly support the claimed applicability to OOD detection without any additional experiments.
- **Direct weight disentanglement metric:** Including the weight disentanglement metric from Ortiz-Jimenez et al. (2023) would provide more direct evidence for the paper's central claim about improved disentanglement.
- **Pipeline with post-hoc merging methods:** Testing TAK + TIES or TAK + ISO as a pipeline could show additional practical value, though the complementarity is already acknowledged.

## Removed Points
- **"Missing comparison with more recent data-free merging methods"** — The paper compares with TaLoS (the only directly comparable dataless method) and explains that TIES/TSV/ISO are complementary post-hoc approaches rather than competitors. Removed because the comparison set is appropriate for the paper's framing.
- **"Limited architectural scope"** (missing ResNet/LLaMA experiments) — This is scope creep; the paper covers CLIP ViT at three scales and T5-base, which is a reasonable scope for a method paper at this venue. Removed.
- **"Fig. 1 heatmaps hard to interpret"** — This is a minor presentation point about parser artifacts; the paper describes the figure in text. Removed as a formatting nitpick.
- **"Language results weaker than vision"** — The paper acknowledges this (line 231: "textual domains may still benefit from even more accurate curvature estimation"). Weaker results on one modality are not a flaw. Removed.
- **"TAK has slightly higher memory than τJp"** — The paper reports this transparently (12.9 vs 12.3 GB, line 304) and explains it's due to KFAC factors. This is an observation, not a weakness. Removed.

## Novel Insights
None beyond the paper's own contributions.

## Suggestions
- **Add 3–5 seed runs with reported standard deviations for all main results** (Tables 1, 2, 3). This is the single highest-impact improvement: it would let readers assess whether the observed differences between TAK and baselines are meaningful, and would resolve the ambiguity in Table 3 where the "approximate" method occasionally outranks the "idealized" one.
- **Reframe "dataless" claims** to acknowledge the 128-example KFAC estimation upfront while emphasizing the key advantage: avoiding access to full training data of other tasks during regularization.
- **Either strengthen the non-linear justification** (e.g., measure the norm of the second-order Taylor term during attention-only fine-tuning to quantify linearity) or explicitly frame the non-linear results as exploratory.

## Score and Decision

**Calibration Anchors (all rounds):**

| Paper Path | Avg Score | Round | Comparison |
|---|---|---|---|
| τJp Weight Disentanglement (1VwWi6zbxs) | 6.00 | R1/R2 | Direct competitor; requires data, narrower eval, weaker theory. Current paper is stronger across multiple dimensions. |
| Attention-Only FT (dj0TktJcVI) | 6.25 | R1/R2 | Similar area; well-executed but narrower contribution. Current paper has more theoretical depth. |
| Submodule Linearity (irPcM6X5FV) | 6.00 | R1/R2 | Task arithmetic in LLMs; clean execution. Comparable quality. |
| Partial Linearization (iynRvVVAmH) | 7.00 | R2 | PEFT-focused; very clean. Current paper is comparable but with different strengths. |
| Task Arithmetic Trust Region (q3ztjJRQuJ) | 5.75 | R1 | Training-free merging; rejected. Current paper is clearly stronger. |
| Online Weight Approximation (HCCkCjClO0) | 3.00 | R1 | Continual learning with weak results. Not comparable. |
| Multi-Concept Editing (UHDSE86qiG) | 4.50 | R1 | Task arithmetic editing; rejected. Not directly comparable. |

**Bracket:** Round 1 bracket was [6.0, 7.0]. After inspecting the τJp (6.00), Attention-Only FT (6.25), and Partial Linearization (7.00) anchors in detail, the current paper sits above the τJp paper due to stronger theory, broader evaluation (vision + language), and practical advantages (dataless, O(1) aggregation, α-robustness, thorough efficiency analysis). It does not reach the polish of the 7.00 Partial Linearization paper primarily due to the missing statistical significance reporting. **Final score: 6.5.**

MY FINAL SCORE: <score>6.5</score>
MY FINAL DECISION: <decision>Accept</decision>