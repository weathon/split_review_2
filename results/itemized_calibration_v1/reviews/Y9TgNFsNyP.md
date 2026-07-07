Now I have sufficient calibration data. Let me write the final consolidated review.

**Round 1 bracket**: 4–6 based on comparison with anchors. The paper has stronger novelty than Uv7bWrIucU (4.20) and KvFk356RpR (4.80), both of which were criticized for limited contribution or flawed threat models. However, the evaluation is less rigorous than xmQuUqSynb (5.75), which was praised for comprehensive experiments. The evaluation gaps (no error bars, narrow G-MIA dynamic range, limited baselines) prevent it from reaching the 5.5–6 range.

**Narrowing**: The closest anchor is iQIQT88prm (5.33) — a machine unlearning paper with novel framework but limited experiments. Our paper has stronger problem novelty (first FF unlearning) but similar evaluation limitations (single forget fraction, no convergence analysis, few baselines). The lack of error bars is a weakness that the 5.33 anchor didn't have, but our ablation study is more thorough. Score placement: 5.0.

---

## Summary

This paper introduces FF-Erase, the first machine unlearning framework designed specifically for Forward-Forward (FF) models. The core idea uses KL-divergence between the model's layer-wise goodness distribution and that of a guidance model (ignorant of the forgetting data) to stabilize unlearning, avoiding the model collapse that naive gradient ascent causes. Two strategies for generating the guidance model are proposed (mini-retrained and fast-distilled). The paper also proposes G-MIA, a goodness-based membership inference attack for unlearning verification. Experiments on CIFAR-10/100, MNIST, and Fashion-MNIST with various FF architectures show 1.9–3.1× speedup over retraining while maintaining comparable effectiveness.

## Strengths

- **Genuinely novel problem and solid motivation.** The paper correctly identifies that FF models' layer-wise independent training and sensitivity to parameter tuning create unique unlearning challenges not present in backpropagation-trained models. This problem is well-articulated in Sections 1 and 3. To my knowledge, this is the first formal treatment of FF unlearning.
- **Principled core design.** The goodness-guided unlearning via KL-divergence to a guidance model is sensible and well-grounded. Rather than directly maximizing loss (which the paper shows causes collapse), pushing the goodness distribution toward a model ignorant of the forgetting data provides a stable optimization target (Section 4.1).
- **Useful ablation study.** The two strategies for generating the guidance model (mini-retrained and fast-distilled) give practical flexibility. The ablation in Table 1 systematically demonstrates how guidance model quality (controlled by data proportion α₁ and epoch proportion α₂) affects the effectiveness–utility–efficiency trade-off, and confirms that a poor guidance model (random initialization, R.G.M.) leads to collapse.
- **Demonstrated efficiency gains.** The 1.9–3.1× speedup over retraining is well-supported by the timing data in Table 1 and Figure 4, and the efficiency analysis in Section 4.3 provides a reasonable analytical model.

## Weaknesses

### Major

1. **No error bars, variance, or significance testing on any metric.** The central effectiveness comparison between FF-Erase and retraining (RE) rests on G-MIA ACC differences of ~0.01–0.03 (e.g., FF-Erase(D): 0.5245 vs RE: 0.532 in Figure 4c; Table 1 values all cluster 0.551–0.577). Every table and figure reports only point estimates with no standard deviations, confidence intervals, or statistical tests. Without variance information, these small numerical differences could be within measurement noise, and it is impossible to assess whether FF-Erase truly achieves effectiveness "comparable" to RE. This is verifiable from Table 1 and Figures 3–5, none of which report any measure of variability.

2. **G-MIA has narrow dynamic range in the unlearning verification setting, limiting its claimed utility.** All G-MIA ACC scores in Table 1 cluster between 0.524 and 0.577 — a range of only ~0.05. Notably, the randomly-initialized guidance model (R.G.M) — which produces a catastrophically collapsed model (Acc_f = 51.18%, Acc_t = 55.53%) — achieves a nearly identical G-MIA ACC (0.553) to the gold-standard retrained model (RE, 0.551). This means G-MIA ACC alone cannot distinguish a collapsed model from a properly retrained one, undermining the paper's claim that G-MIA provides "accurate" and "reliable" verification. While the paper also reports Acc_f and Acc_t (which do distinguish these cases), the G-MIA metric central to the effectiveness evaluation lacks the resolution claimed. (Verifiable from Table 1, last row vs first row.)

### Minor

3. **G-MIA's access model is imprecisely characterized as "black-box."** The paper repeatedly calls G-MIA a "black-box" attack (abstract, Section 1 contributions, Section 2), justified by the statement that "FF models output the goodness vectors from all layers for inference" (Section 3.1). This is technically consistent with the native FF output format. However, since a predictor layer is placed on top of these goodness vectors and is the default in experiments, a typical deployment API would return final class predictions, not layer-wise goodness scores. The required access level sits between standard black-box (final output only) and white-box (full parameters/gradients). The paper should clarify this rather than claiming "strict black-box constraint" (Section 2).

4. **Only one approximate unlearning baseline (gradient ascent) is adapted and tested.** The paper evaluates only GA (with extensive λ exploration) as a representative of existing unlearning methods and argues other BP-based methods would similarly fail due to architectural incompatibilities (Section 1, Appendix A). This principled argument is plausible, but testing at least one additional adapted baseline — e.g., a teacher-student approach (incompetent teacher, Chundawat et al., AAAI 2023, which the paper cites) or an influence-function-based method — would provide stronger empirical support for the claim that existing methods are broadly infeasible for FF models.

5. **Only a single forgetting fraction (20%) is evaluated.** The main unlearning experiment uses 20% of training data as the forgetting set (Section 6.2). Many unlearning studies test a range of fractions (1%, 5%, 10%, 20%, 50%). Testing only one fraction limits understanding of how FF-Erase scales with the forgetting burden and whether it generalizes to smaller forget sets.

6. **Batch processing not specified.** Algorithm 1's FFwd subroutine iterates `for x in D_forget` (line 136), suggesting sample-by-sample processing. The paper should clarify whether mini-batching is supported, as this affects both practical efficiency and optimization dynamics.

### Trivial

7. **Goodness vector notation is confusing.** Equation (1) defines g^l as the L1 norm of h^l (suggesting a scalar), but the text immediately treats g^l as a J-dimensional vector of class-wise scores. The footnote clarifies that h^l is "a vector of vector" with column-wise L1 norm, but this could be stated more clearly in the main text.

## Nice-to-Haves

- Run all experiments with multiple random seeds and report mean ± std for all key metrics (G-MIA ACC/AUC, Acc_f, Acc_t). This is the single most impactful improvement.
- Provide a calibration experiment showing that G-MIA scores correlate with actual forgetting across varying forgetting fractions.
- Test class-stratified forgetting and additional forgetting fractions (e.g., 1%, 5%, 10%).
- Consider adapting one more unlearning method (e.g., incompetent teacher) to FF models.

## Removed Points

These points are flagged to be removed; treat them with caution.

- "G-MIA is not a black-box attack — this is a fundamental mischaracterization" → Downgraded to Minor (point 3). The paper has a reasonable technical justification (FF models natively output goodness vectors as their inference output), so calling it a "fundamental mischaracterization" overstates the issue.
- "G-MIA's discriminative power is very weak" → Merged into Major point 2 (narrow dynamic range). G-MIA ACC of ~0.55 on RE is expected (strong retraining should produce near-random MIA performance). The real concern is the narrow band across all methods, including collapsed models.
- "FF-Erase outperforming RE suggests measurement noise" → This is supporting evidence for the error-bars concern (Major point 1), not a standalone weakness. The paper claims "comparable" not "superior."
- "Efficiency comparison unfair (retraining uses full data/epochs)" → Removed because RE retrains on D_remain (80% of data), which is the correct gold-standard baseline for unlearning.
- "No discussion of D_remain unavailability" → Removed. D_remain is other subjects' data, not the requesting subject's, so it is retained under GDPR.
- "No analysis of forgetting data distribution" → Merged into Nice-to-Haves as a scope extension.
- Various formatting/presentation nitpicks and speculations about appendix content → Removed per filtering rules.

## Novel Insights

None beyond the paper's own contributions. The review confirms that the core novelty — adapting machine unlearning to the FF paradigm via guidance-model-stabilized goodness optimization — is genuine and well-motivated. However, the evaluation is not yet rigorous enough to fully substantiate the effectiveness claims. The central tension is between the paper's genuine novelty and the insufficiently rigorous evaluation.

## Suggestions

1. **Add error bars to all experiments.** Run every configuration with at least 5 random seeds and report mean ± std. This is the most critical improvement because the central claims rest on G-MIA ACC differences of ~0.01–0.03.
2. **Demonstrate G-MIA's validity as a verification tool.** Show that G-MIA ACC/AUC scores correlate with actual forgetting extent across varying forgetting fractions, and discuss the narrow dynamic range honestly.
3. **Clarify G-MIA's access model.** Explicitly state that G-MIA requires layer-wise goodness vectors — distinct from both standard black-box (final output) and white-box (full parameters) access.
4. **Add at least one more adapted baseline** (e.g., teacher-student) to strengthen the claim that BP-based methods broadly fail for FF models.
5. **Test additional forgetting fractions and clarify batch processing** in Algorithm 1.

## Score and Decision

MY FINAL SCORE: 5.0
MY FINAL DECISION: Reject

**Calibration details.** Round 1 bracket: 4–6. Closest anchors: Uv7bWrIucU (4.20, unlearning auditing, weaker novelty than this paper); KvFk356RpR (4.80, unlearning attack, criticized for "lacks std devs" and "threat model flawed," similar evaluation gaps); iQIQT88prm (5.33, game-theoretic unlearning, similar evaluation limitations but without the error-bar gap); xmQuUqSynb (5.75, unlearning + adversarial robustness, stronger experiments). This paper's novelty is above the 4.2–4.8 anchors, but its evaluation gaps (no variance reporting, narrow G-MIA dynamic range) prevent it from reaching the 5.75 level. Score 5.0 reflects genuine merit with insufficiently rigorous evaluation.