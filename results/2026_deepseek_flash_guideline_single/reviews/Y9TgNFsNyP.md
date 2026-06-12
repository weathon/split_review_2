Now I have all the calibration data I need. Let me produce the final review.

## Summary

This paper proposes FF-Erase, the first machine unlearning framework for Forward-Forward (FF) models, along with G-MIA, a membership inference attack for verifying FF unlearning. The core idea is to use a guidance model (trained on remaining data) to provide stable target goodness distributions, then shift the original model's layer-wise goodness toward the guidance distribution via KL divergence rather than direct gradient ascent. The paper identifies that BP-based unlearning methods fail on FF models due to sensitivity to parameter perturbations and layer-wise independence, and demonstrates that FF-Erase achieves comparable unlearning effectiveness to retraining while being 1.9–3.1× faster.

## Strengths

1. **Genuine problem novelty and well-motivated method design.** No prior work addresses unlearning for FF models. The paper correctly diagnoses why standard gradient-ascent unlearning causes catastrophic collapse in FF models (Section 1, Figure 1) and designs a principled solution: using KL divergence toward a guidance model's goodness distribution (Section 4.1, Equation 5) rather than directly minimizing goodness scores. The design follows naturally from the problem analysis.

2. **Informative ablation study (Table 1).** The systematic variation of α₁ (data proportion) and α₂ (epoch proportion) for both guidance strategies (mini-retrained and fast-distilled) clearly demonstrates the efficiency-performance trade-off. The random-initialization baseline (R.G.M., ~55% accuracy on D_forget vs. 81%+ for trained guidance models) cleanly confirms the necessity of a properly trained guidance model. This is the strongest empirical section in the paper.

3. **Clean demonstration that GA fails on FF models (Section 6.3, Figure 5).** The parameter sweep over λ confirms a binary outcome: GA either causes model collapse (λ ≥ 0.1) or fails to unlearn (λ ≤ 0.01), with the unusable middle ground empty. This substantiates the paper's core motivation and is not a foregone conclusion.

## Weaknesses

### Fatal
None.

### Major
1. **No statistical significance or variance reported for any quantitative result.** Every accuracy, G-MIA score, and timing measurement is reported as a single point with no standard deviation, error bars, confidence intervals, or mention of multiple seeds. This makes it impossible to assess whether reported differences (e.g., the 0.0075 G-MIA gap between FF-Erase(D) and RE in Figure 4c, or the speedup range of 1.9–3.1×) are meaningful or within noise. This is the single most significant weakness in the paper — it undermines all comparative claims.

2. **Core unlearning results presented for only one configuration in the main text.** The paper evaluates on 4 datasets and 3 architectures using 2 FF algorithms, but the detailed unlearning time-vs-accuracy curves (Figure 4) are shown only for VGG13 on CIFAR-10. The paper acknowledges this (Section 6.2: "Due to space limitations, we only show the results of VGG13 models trained on the CIFAR-10 dataset in the main text"), but for a paper introducing a new method, the reader cannot assess generalization from the main body alone.

3. **G-MIA's access level is inconsistently framed.** The paper consistently describes G-MIA as operating "under a strict black-box constraint" (abstract, §1, §2, §5) and categorizes it as a "black-box attack" in Figure 3. However, G-MIA requires per-layer goodness vectors from all layers (Section 5), which is more information than the standard black-box definition in the MIA literature (final prediction only, e.g., Shokri et al. 2017). While FF models natively output per-layer goodness, the paper does not explicitly argue why this should be considered black-box access in the FF context, creating a discrepancy between the claimed and actual access requirements.

### Minor
1. **Several hyperparameters are not reported.** The termination thresholds ε₁ and ε₂ (Algorithm 1), the trade-off parameter λ (Equation 6), and the recovery frequency K are listed as input/parameters but never given concrete values used in experiments. The maximum epochs E is also unspecified. This affects full reproducibility.

2. **Potential tension between forgetting and recovering updates is not analyzed.** The recovering forward step (Equation 6) pushes the model toward its original learned distribution on remaining data, while the forgetting forward step (Equation 5) pushes toward the guidance distribution on forgetting data. For data points near the decision boundary between D_forget and D_remain in feature space, these updates could conflict. The paper does not discuss this.

3. **Only gradient ascent is tested as a representative BP-based baseline.** The paper argues that all BP-based unlearning methods are infeasible for FF models and uses GA as the representative. While the argument that gradient-based calibration methods share the same fundamental challenge is reasonable, testing a structurally different baseline (e.g., a teacher-student approach like BadTeaching) would strengthen the empirical case.

### Trivial
None.

## Nice-to-Haves
- Adding a summary table of cross-configuration unlearning results (all 4 datasets × 3 architectures) in the main text.
- Validating G-MIA against multiple RE runs from different random seeds to show the distribution, then positioning FF-Erase within that distribution.
- More prominently highlighting that the actual unlearning time (excluding guidance model acquisition) is only 10–20% of retraining, which is more impressive than the headline 1.9–3.1× speedup that includes guidance model training.

## Removed Points

These points were raised in the input review but are removed with justification:

- **Self-verification circularity (Critical Issue #2 from Harsh Critic):** The paper compares FF-Erase against retraining from scratch (RE) as an external anchor, not just against its own metric. The close G-MIA scores between FF-Erase and RE are evidence of matching, not circular reasoning. The real issue (lack of error bars to assess whether the 0.0075 gap is meaningful) is already captured as Major #1 above.

- **G-MIA's practical assumptions about synthetic data (Critical Issue #5):** The paper follows the standard MIA assumption that synthetic data with similar distribution to training data is available (Shokri et al. 2017, cited). This is a well-established practice in the MIA literature, not a weakness specific to this paper.

- **Verification framing heuristic (Section 6.2 claim about D_forget accuracy):** The heuristic that unlearned model accuracy on D_forget should resemble original model accuracy on D_test is conceptually reasonable for random splits from the same dataset distribution. The specific objection about D_forget difficulty differing from D_test does not apply here since random splitting produces comparable distributions.

- **Introduction cites only GA:** The paper discusses influence functions and Hessian-based methods in Section 2 and argues they share gradient-based limitations. The method category is adequately represented; adding every variant is not required.

## Novel Insights

None beyond the paper's own contributions. The synthesis of the two reviews confirms that the paper's main strengths (problem novelty, method design, ablation) and weaknesses (missing variance, thin main-text evaluation, G-MIA framing) are all directly evident from the paper itself.

## Suggestions
- Add standard deviation/error bars to all quantitative results by running at least 3 random seeds. This is the single most impactful improvement.
- Report concrete values for ε₁, ε₂, λ, K, and E used in the main experiment.
- Explicitly discuss the access level of G-MIA: either reframe it as gray-box (or "FF-native black-box") and justify why this is still practical, or define a new access category specific to FF models.
- Include a main-text summary table showing unlearning effectiveness (accuracy and G-MIA) across all dataset-model configurations, not just VGG13/CIFAR-10.
- Analyze the potential interaction between forgetting and recovering updates for samples near the decision boundary.

## Score and Decision

**Round 1 bracket:** Based on similarity to anchor papers — the paper is stronger than PPU (3.00) and MASIMU (2.50) but weaker in evidential rigor than accepted papers like Utility & Complexity (6.60) or Jogging Memory (6.75). The plausible range is 4.5–5.5.

**Calibration anchors retrieved:**
| Path | Avg Score | Round | Comparison |
|------|-----------|-------|------------|
| PPU (Xagys9QD3T) | 3.00 | 1 | Weaker evaluation and questionable design choices; our paper is stronger |
| MASIMU (BJfIDS5LsS) | 2.50 | 1 | Missing baselines and poor presentation; our paper is clearly stronger |
| Deep Unlearning (pUOesbrlw4) | 5.25 | 1 | Similar quality — interesting method but evaluation gaps; scores spread 8,3,5,5 |
| Meta-Unlearning Diffusion (okRSNTMdFg) | 4.00 | 1 | Interesting problem but key limitation; our paper has stronger motivation |
| Decoupling Class Label (OHOmpkGiYK) | 5.75 | 2 | Insightful problem framing but mixed scores (6,6,3,8); comparable quality |
| UnCLe (pFjzF7dIgg) | 5.75 | 2 | Novel setup but evaluation concerns (5,5,8,5); comparable quality |
| SPE-Unlearn (drrXhD2r8V) | 5.00 | 2 | Parameter-efficient unlearning; similar evidential issues |
| DeeperForward (kOYnXVQCtA) | 6.25 | 2 | FF method paper, accepted; stronger evaluation than our paper |
| Forward Learning GNN (Abr7dU98ME) | 6.50 | 2 | FF applied to GNNs; stronger evaluation and accepted |

**Round 2 narrowing:** Our paper has a genuine novel contribution (first FF unlearning) with a well-motivated design, placing it above papers with fundamentally flawed methods (PPU, MASIMU). However, the complete absence of variance reporting and the thin main-text evaluation are serious gaps that pull it below accepted papers (DeeperForward, Forward Learning GNN, Utility & Complexity). The closest matches are Deep Unlearning (5.25), Decoupling Class Label (5.75), and UnCLe (5.75) — all rejected papers with interesting contributions but notable evidential issues.

**Final score: 5.0** — The paper identifies a genuinely new problem and proposes a well-reasoned method, but the evidential backbone is substantially weaker than the claims warrant. The lack of any variance/error bars and reliance on a single main-text configuration for core results are fixable but currently limit confidence. This paper is between borderline reject and borderline accept.

**Decision: Reject**

MY FINAL SCORE: <score>5.0</score>
MY FINAL DECISION: <decision>Reject</decision>