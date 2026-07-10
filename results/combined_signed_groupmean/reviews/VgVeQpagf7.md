## Summary

This paper proposes SPS and SPS+, algorithms for differentially private synthetic image generation using dataset distillation techniques. The method privatizes activation statistics from a public pretrained model via the Gaussian mechanism, then synthesizes images by matching these statistics through KL-divergence minimization. Two key enhancements — multistage clipping and grouped pseudo-classes (GPC) — are introduced to improve performance under strict privacy budgets. SPS+ achieves competitive or slightly superior accuracy to DP-SGD on CIFAR-10/100 while enabling post-processing advantages (ensembling, federated learning, continual learning) that DP-SGD cannot provide.

## Strengths

- **Clear and well-motivated problem framing (Section 1).** The paper convincingly identifies genuine limitations of DP-SGD: coupling of privacy cost to gradient steps, model size, and architectural incompatibilities (ensembles, BatchNorm). The argument for a synthetic-data approach that bypasses these constraints via Rényi DP composition is logically sound and well-supported.

- **The Grouped Pseudo-Classes technique (Section 4.2) is technically novel and non-obvious.** The observation that KL-divergence optimization can tolerate noisy per-class statistics when these are aggregated into pseudo-class groups — and that this works *only* due to the Σ inversion in the KL and eigenvalue clipping — is a genuine algorithmic insight. The honest acknowledgment that "this method does not offer benefits for direct mean estimation" shows the authors understand its mechanism.

- **Compelling demonstration of post-processing flexibility (Sections 5.5, 5.6).** The federated learning (asynchronous, no synchronization constraints) and continual learning (no privacy cost for revisiting data) experiments concretely demonstrate qualitative advantages that DP-SGD cannot replicate. These are not afterthoughts — they are core to the paper's thesis that data-based privacy offers fundamentally different capabilities.

- **First generation-based method to match DP-SGD on image classification (Table 1).** SPS+ with WRN28-10 achieves 95.1% vs DP-SGD 94.8% on CIFAR-10 and 71.0% vs 70.3% on CIFAR-100 at ε=1, making it the first distillation-based approach to reach accuracy parity with gradient-based DP methods on these benchmarks.

## Weaknesses

### Major

- **The abstract and headline comparison conflate two sources of advantage.** The abstract (p. 1) states: *"SPS+ achieves **96.2 / 76.6%** top-1 accuracy, outperforming state-of-the-art DP-SGD results (94.8 / 70.3%)."* The 96.2% is from a **5-model WRN34-10 ensemble**, while the DP-SGD number is a **single WRN28-10 model** (De et al., 2022). This comparison stacks architecture (WRN34-10 vs WRN28-10) and ensembling (5 vs 1) simultaneously. When architectures are matched in Table 1 (SPS+ WRN28-10 vs DP-SGD WRN28-10 at ε=1), the margins shrink to 95.1% vs 94.8% on CIFAR-10 (+0.3pp) and 71.0% vs 70.3% on CIFAR-100 (+0.7pp). The paper does present these fair comparisons in Table 1, but the abstract's headline numbers — which are what most readers will remember — imply a substantially larger accuracy gap. While the paper validly argues that post-processing flexibility (ensembles, larger models) is itself a genuine advantage, the abstract should clearly qualify which comparison is being made. The paper would be stronger if it separated "single-model accuracy parity" from "accuracy gains from post-processing flexibility" upfront.

### Minor

- **Theorem 4.1 (privacy accounting) contains a notational error.** The theorem states ε = Mα/(2δ²), but δ is already used throughout the paper as the approximate-DP parameter (δ=10⁻⁵ in CIFAR experiments, δ=3×10⁻⁶ in Table 2). The noise multiplier in eq. (4) is b₀, not δ. The correct RDP formula for the Gaussian mechanism is ε(α) = Mα/(2b₀²). Substituting δ (≈10⁻⁵) would produce astronomically large ε values inconsistent with the reported experimental results. This is clearly a typo — the surrounding text says "This is a direct result of the M-fold composition of Gaussian Mechanisms under RDP" — but as written it impairs reader confidence. Fixing this is straightforward but necessary.

- **Section 5.4 ("Oversized dataset distillation," Table 3) overstates its findings.** The paper claims "further performance gains is unlocked with oversized distilled datasets," but the data do not support this. At ε=1, accuracy *decreases* monotonically with size (76.6% → 75.9%). At other ε values, changes are within ±0.3–0.5pp and non-monotonic (e.g., ε=8: 81.6 → 81.8 → 82.1 → 81.9). These fluctuations are within noise and do not demonstrate systematic improvement.

- **The noise redistribution clipping bound (Section 3.2.4, p. 5) has a derivation/notation issue.** The formula |v|_max = K_clip√(LD_G^layer) + S|L_C|D_C^layer = K_clip√(2LD_G^layer) does not parse cleanly as written: it sums a term inside a sqrt with a term outside, and the claimed simplification to K_clip√(2LD_G^layer) is not obvious without additional assumptions.

- **The DP-SGD baseline (De et al., 2022) is from ~4 years before the submission date.** The paper claims these represent "state-of-the-art DP-SGD results" but does not verify whether more recent work (improved accounting methods, better fine-tuning recipes) has surpassed these numbers. Updating the baseline set would strengthen the comparison, though this does not invalidate the paper's core contribution.

- **The Grouped Pseudo-Classes description (Section 4.2) is too brief.** The mechanism of how real classes map to pseudo-classes and how labels are assigned to synthetic images after generation is not clearly explained. The formula "each class belongs to PN_{c/p}/C pseudo-classes" requires the reader to already understand the mechanism, which is itself not well-described. A concrete example would significantly improve clarity.

### Trivial

- None beyond the minor issues above.

## Nice-to-Haves

- An ablation study quantifying the contribution of the √S noise redistribution technique (Section 3.2.4) would help establish its importance.
- A brief analysis of how accuracy and compute cost scale with the number of clipping stages M would help practitioners decide on M.
- Reporting generation GPU-hours / wall-clock time in the main text (currently referenced to Appendix F.1) would improve practical usability.

## Removed Points

These points are flagged to be removed; treat them with caution.

1. **CAMELYON17 privacy budgets not matched (Table 2).** *Removed.* The asymmetry favors the author's method (SPS uses ε=8 while baselines use ε=10 or 7.56). Per hard rules: criticisms about unfair comparison when asymmetry favors the baseline, not the author's method.
2. **Computational cost not quantified.** *Removed.* The paper directs readers to Section F.1 (appendix) for discussion. Per hard rules: weaknesses about missing appendix content that was stripped by the parser.
3. **Generic strengths removed** (e.g., "the paper addresses an important problem"). Specific strengths are already captured in the main review.

## Novel Insights

None beyond the paper's own contributions. The reviews surface presentation and framing issues rather than uncovering new technical insights about the method.

## Suggestions

1. Restructure the abstract and introduction to clearly separate "single-model accuracy parity" from "accuracy gains via post-processing flexibility (ensembles, larger models)."
2. Fix the notational error in Theorem 4.1: replace δ with the noise multiplier b₀.
3. Update DP-SGD baselines to include more recent results if available, or explicitly state that De et al. (2022) remains the best published result to the authors' knowledge.
4. Add a concrete example (e.g., CIFAR-100 with C=100, P=200, N_{c/p}=2) to clarify the Grouped Pseudo-Classes mechanism.
5. Tone down the oversized distillation claim in Section 5.4 to reflect the flat/noisy results.
6. Fix the clipping bound formula in Section 3.2.4 for clarity.

## Score and Decision

### Calibration Anchors

| Anchor Path | Avg Score | Round | Itemized | Comparison |
|---|---|---|---|---|
| `ckabXglfiT.md` (Privacy as a Free Lunch) | 4.75 | 1 | Yes | Also DP + dataset distillation, but had a fatal DP flaw (no-noise DP claims). Current paper's DP mechanism is sound by contrast. |
| `TbOcySs6g8.md` (Advancing DP through Synthetic Dataset Alignment) | 2.50 | 1 | Yes | Similar topic, but had fundamental DP accounting errors (-10.00 impact). Current paper has only a typo. |
| `YEhQs8POIo.md` (DP Synthetic Data via Foundation Model APIs) | 6.25 | 1 | Yes | Strong experimental results, minor weaknesses. Current paper has stronger accuracy results but worse presentation. |
| `C8niXBHjfO.md` (Does Training with Synthetic Data Truly Protect Privacy?) | 6.00 | 1 | Yes | Empirical study, no new method. Well-written with clear presentation — a point where current paper falls short. |
| `1NHgmKqOzZ.md` (Data Distillation Can Be Like Vodka) | 6.33 | 2 | Yes | Dataset distillation (non-DP), progressive approach. Minor presentation issues, accepted. Current paper has stronger technical novelty (DP + distillation). |

**Round-1 bracket:** The paper sits above 4.75 (Privacy as a Free Lunch — fatally flawed DP approach) and below 6.25–6.33 (papers with strong results and clean presentation). The core methodology is sound and the results are competitive, placing it in the 5.0–6.0 range.

**Score justification:** The paper's key shared high-magnitude strengths with the 6.0-range anchors (+9.97 for motivation, +9.97 for flexibility demonstrations, +9.95 for competitive results) are comparable. However, the abstract's misleading comparison and the theorem typo are real presentation flaws that the 6.0-range anchors do not share. The oversized-distillation overclaim is a further but smaller presentation issue. These weaknesses pull the score below the clean 6.0+ range. The paper is not fatally flawed (unlike the 4.75 anchor) — its DP mechanism is standard and correct modulo a typo — but the presentation issues are significant enough that they should be fixed before acceptance.

**Final score: 5.5**

MY FINAL SCORE: <score>5.5</score>
MY FINAL DECISION: <decision>Accept</decision>