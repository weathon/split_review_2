I'm unable to use the calibration tool due to a path error, so I'll proceed with my best judgment calibrated against the ICLR scoring scale and my knowledge of the field.

Let me finalize the review with careful attention to the filtering rules.

**Double-checking my filtered weaknesses:**

1. "No direct validation that information is separated across channels" — This is valid. The paper claims separation but only validates aggregate rate-distortion. I verified this by looking at all experimental sections. KEEP as Major.

2. "No error bars" — Valid. I checked the paper (all sections), no variance measures. KEEP as Major.

3. "No comparison against prior multi-task compression methods" — Valid. The paper cites them but doesn't compare. KEEP as Minor.

4. "Interaction information bounds never empirically estimated" — Valid. Theorem 1 is proven but the interaction information is never computed. KEEP as Minor.

5. "Six vision benchmarks" overstatement — Valid. The paper has 4 experimental settings. KEEP as Minor.

Let me also reconsider if I should merge any weaknesses across the harsh critic and the strength finder. The strength finder didn't mention any weaknesses, so no merging needed there.

Let me also consider: Is the missing channel ablation truly a "Major" weakness or should it be "Fatal"? 

For it to be fatal, it would need to "invalidate the paper's core claims." The paper's core claims include:
1. Theoretical bounds (Theorem 1) — standalone mathematical contribution
2. A loss function derived from Gray-Wyner theory (Theorem 2 → Eq. 12) — standalone
3. An architecture that separates information — this is what's partially unvalidated

The first two contributions stand independently of the third. The architecture contribution is partially validated (synthetic + MNIST) but not fully. So the missing experiment doesn't invalidate the entire paper. Hence Major, not Fatal.

Good. Let me write the final review.## Summary

This paper develops a learnable three-channel neural codec (common + two private channels) for multi-task compression, grounded in the Gray-Wyner information-theoretic framework. Its contributions include: (1) extending a lossless bound to the lossy setting that relates Gács–Körner and Wyner's common information via interaction information (Theorem 1); (2) deriving a differentiable Lagrangian objective from the Gray-Wyner variational problem (Theorem 2 → Eq. 12) where a single hyperparameter β controls the transmit–receive rate tradeoff; and (3) an architecture with an element-wise matching mechanism to construct the common representation. Experiments are conducted on synthetic data, colored MNIST, Cityscapes (segmentation+depth), and COCO (detection+keypoint).

## Strengths

- **Theorem 1 establishes concrete bounds relating two lossy common information measures (K and C) through the interaction information I(X₁,X₂;Ẑ₁;Ẑ₂).** This bridges previously disconnected theoretical quantities and grounds the transmit–receive tradeoff in a single three-way information term (Eqs. 6–7).

- **Theorem 2 converts the abstract Gray–Wyner variational problem into an explicit entropy-based form (Eq. 10) that directly yields a differentiable Lagrangian (Eq. 12).** The resulting loss has a clean interpretation: β=1 targets transmit rate, β=2 targets receive rate, β=3/2 targets a balanced tradeoff. This is the paper's most practically useful contribution.

- **The colored MNIST edge-case experiments (Section 4.2, Figure 4) provide controlled validation that the codec responds to ground-truth mutual information structure.** Under the Dependent PMF (full MI), the method places nearly all information on the common channel. Under the Independent PMF (zero MI), it minimizes common-channel usage. This sanity check cannot be run on real benchmarks where true MI is unknown.

- **The synthetic-data experiment (Figure 3a) demonstrates that β directly controls the common-channel rate as predicted by theory:** β=1 yields common-channel rate above empirical mutual information; β=2 yields common-channel rate below it; β=3/2 yields an intermediate value.

- **Pre-trained task models (DeepLabV3+, LRASPP, Faster R-CNN, Keypoint R-CNN) are kept frozen during training**, ensuring that measured BD-rate gains come from the coding architecture rather than co-adaptation of task models to the compressed representation.

## Weaknesses

### Fatal
None.

### Major

1. **No direct validation that information is separated across channels.** The paper's central architectural claim is that the method "separates common information between two tasks" (line 25). The experiments only validate aggregate rate-distortion improvements of the three-channel architecture over simpler alternatives. No experiment isolates what information each channel carries — for example, evaluating task 1 using only Y₀ (without Y₁) or evaluating cross-task performance (task 1 using only Y₂). The evidence therefore supports a weaker claim: three channels with the proposed structure offer better rate-distortion than fewer channels. This is a significant gap between what the paper advertises and what it demonstrates.

2. **No error bars, multiple seeds, or statistical significance for real-vision experiments.** In the Cityscapes and COCO experiments (Figure 5), all methods cluster within ~1% of the uncompressed baseline in task performance. The large BD-rate savings (e.g., –81.58% average transmit-rate advantage claimed in the conclusion) are computed from curve interpolation near a performance ceiling, where small curve-fitting differences can produce large BD-rate values. Without variance estimates, it is impossible to assess whether the proposed method's advantage over Independent coding is reliable or due to optimization noise.

### Minor

3. **No comparison against prior multi-task compression methods.** The paper cites Chamain et al. (2021), Feng et al. (2022), and Guo et al. (2024) but does not compare against them or against coding-for-humans-and-machines baselines (Choi & Bajic 2022, Foroutan et al. 2023). While these works address different formulations, a comparison would help situate the practical gains. Even the "Separated" and "Combined" baselines are internal ablations, not external competitors.

4. **The interaction information bounds from Theorem 1 are never empirically estimated.** The bound relates K and C through I(X₁,X₂;Ẑ₁;Ẑ₂), but this quantity is computed for no experimental setting. Computing it for at least the synthetic data would connect the theory to the experiments.

5. **"Six vision benchmarks" is an overstatement.** The abstract claims evaluation "spanning six vision benchmarks." The experiments cover four settings: synthetic data, colored MNIST, Cityscapes (two tasks), and COCO (two tasks). Counting individual tasks as separate benchmarks inflates the evaluation scope.

### Trivial
- The labeling of PMFs as "Dependent" and "Independent" (which describe the task relationship) overlaps with the method name "Independent" (which means no common channel), creating confusing nomenclature.

## Nice-to-Haves
- Channel ablation at test time (evaluate task 1 using only Y₀, task 2 using only Y₀, cross-task using private channels). This single experiment would directly verify the separation claim.
- Report β=3/2 results for Cityscapes and COCO alongside the β=1 and β=2 curves.
- Ablate the element-wise matching mechanism (Eq. 14) against softer alternatives (e.g., a variational information bottleneck on the common channel).
- Analyze the Mixture PMF failure case more thoroughly — why does the codec struggle when common information is not perfectly separable?

## Removed Points
These points were flagged for removal; they are listed here only for traceability and should be treated with caution.
- "The paper never resolves the tension about complete isolation being unattainable": The paper explicitly acknowledges this at line 19 and frames the transmit–receive tradeoff as the resolution. Not a weakness.
- "Markov condition violation not discussed": Addressed at line 167: "This effectively removes the requirement for the conditions in 1." The reviewer missed this passage.
- "β relationship is straightforward without Gray-Wyner theory": The derivation via Theorem 2 is a genuine contribution; dismissiveness is unwarranted.
- "No analysis of what β values achieve": Figure 3a directly shows the effect of β on common-channel rate for the synthetic experiment.
- "Matching mechanism unanalyzed": The paper discusses γ sensitivity (lines 181–182) and connects the mechanism to Gács–Körner separability.
- Missing appendix content, missing proofs, missing references: Parser artifacts — these sections exist in the original submission.
- Criticisms about the paper not reproducing theoretical optimal rates: The paper acknowledges that empirical rates are higher than theoretical values ("as often seen in practice"), which is standard for learned codecs.

## Novel Insights
None beyond the paper's own contributions.

## Suggestions
1. **Add a channel-ablation experiment**: After training, evaluate each task using only the common channel Y₀ and using only the private channel (Y₁ for task 1, Y₂ for task 2), plus cross-task conditions (task 1 with Y₂ only). This directly tests whether Y₀ carries shared information and Y₁/Y₂ carry task-specific information. This is the single highest-leverage improvement.
2. Report all main results with error bars over at least 3 random seeds.
3. Compute the interaction information I(X₁,X₂;Ẑ₁;Ẑ₂) for the synthetic experiment and compare against the Theorem 1 bounds.
4. Add at least one external baseline (e.g., Choi & Bajic 2022 adapted to two tasks, or a compared method from Chamain et al. 2021) to ground the practical improvements.

## Score and Decision

Based on my assessment: the paper has genuine theoretical contributions (Theorems 1 and 2) and a clean differentiable loss function derived from Gray-Wyner theory, which are valuable. The MNIST edge-case and synthetic-data experiments provide partial evidence that the architecture responds to information structure. However, the major weakness — that the central claim of information separation is not directly validated — prevents the paper from fully delivering on its advertised contribution. The lack of error bars for real-vision results further weakens the empirical support. On the ICLR scale, this places the paper in the borderline range, closer to reject than accept because the experimental gap cuts to the core claim.

MY FINAL SCORE: <score>5.5</score>
MY FINAL DECISION: <decision>Reject</decision>