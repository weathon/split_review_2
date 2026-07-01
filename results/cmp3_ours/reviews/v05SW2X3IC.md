Now I have a solid calibration base. Let me write the final review.

## Summary

This paper develops a learnable three-channel (one common + two private) neural codec inspired by the Gray-Wyner network from information theory. The authors extend lossless common-information bounds to the lossy setting (Theorem 1), derive a practical Lagrangian optimization with a single tradeoff hyperparameter β (Theorem 2, Eq. 12), and design a "split and match" architecture (Eq. 13–14) to encourage common/private channel separation. Experiments on synthetic data, colored MNIST, Cityscapes, and COCO compare the proposed architecture against Joint (single-channel), Independent (two-channel), and two encoder-topology baselines.

## Strengths

1. **Clean theory-to-practice bridge.** Theorem 2 and the Lagrangian formulation (Eq. 12) with a single hyperparameter β that cleanly interpolates between transmit-rate-optimal (β=1) and receive-rate-optimal (β=2) operation is a principled derivation grounded in the Gray-Wyner framework. The connection between β and the contour of the achievable region (Section 3.2) is well explained.

2. **Thoughtful architecture design.** The "split and match" mechanism (Eq. 13–14), where two separate analysis transforms each produce a candidate common half and the common representation is only active where both halves agree, coupled with the auxiliary loss (Eq. 15), is a clever inductive bias for inducing channel separation without hard architectural constraints.

3. **Theoretical bounds for lossy common information.** Theorem 1 extends Wyner's lossless bounds to the lossy setting, connecting interaction information with Gács-Körner and Wyner common information. This provides useful framing for the paper's approach and motivates the transmit-receive tradeoff exploration.

## Weaknesses

### Major

1. **The central disentanglement claim is not directly validated by the experiments.** The paper claims the method "disentangles shared information from task-specific details" (abstract), but the experiments provide only indirect evidence. The comparisons are fundamentally capacity-imbalanced: the 3-channel proposed system is compared against Joint (1 channel) and Independent (2 channels), so outperforming these baselines on their respective metrics is expected. No baseline controls for total channel count without enforcing common/private structure. The synthetic experiment compares encoder topologies (Separated, Combined) that are naive alternatives, but does not isolate whether the *separation of content across channels* itself provides benefit. The paper never directly measures what each channel actually encodes (e.g., mutual information between channel content and task targets, or visualization of common-channel activations). Without such analysis, the reader cannot assess whether the architecture achieves genuine common/private separation or simply learns a 3-channel codec that happens to allocate information asymmetrically.

2. **Headline BD-rate number is presented without clarifying context.** The conclusion states "a BD-rate advantage of -81.58% in transmit rate, against single-task codecs" (line 275). This figure is computed against the Independent baseline (2 private channels, no common channel). Comparing a 3-channel system against a 2-channel system inflates the reported improvement. When compared against the Joint method (the single-channel baseline), the proposed method has *positive* BD-rates in Figure 5 (23.32% and 13.16% for transmit rate in Cityscapes and COCO respectively), meaning it is strictly *worse* on transmit rate. The paper acknowledges this in the caption but the abstract and conclusion do not make the baseline clear, leaving the misleading impression that the proposed method achieves large improvements across the board.

3. **No ablation of the critical auxiliary matching loss (γ) or analysis of the matching mechanism.** The core mechanism for inducing common/private separation is the matching-based combination in Eq. 14, driven by a γ-scaled MSE loss (Eq. 15). The paper notes that γ can cause degenerate behavior (lines 181–182) and simply states γ=1 was used. There is no ablation showing sensitivity to γ, no quantification of what fraction of elements actually match in the trained model, and no evidence that the matching mechanism achieves its intended effect rather than being dominated by other loss terms. This is a critical gap since the entire architecture depends on this mechanism working correctly.

### Minor

4. **No error bars, confidence intervals, or significance statements for any experiment.** Given that some differences between methods are small (e.g., Proposed(Transmit) vs. Joint in Figure 5), the absence of any measure of variability makes it impossible to assess whether the reported improvements are statistically meaningful.

5. **The colored MNIST experiment demonstrates rate adaptation to task correlation but does not test representation disentanglement.** It shows the method can adjust common-channel rate across PMFs with different mutual information—a necessary property—but all methods achieve near-perfect accuracy, so the comparison reduces to rate differences that follow the expected ordering. This is a weak test of whether the method genuinely separates common from private *content* in the representations.

6. **The Markov conditions in Eq. 1 are presented as core assumptions but then said to be "effectively removed" by the architecture (line 167).** This framing is confusing: if the architecture removes the need for these conditions, presenting them as foundational assumptions misleads the reader about their role in the theoretical development.

### Trivial

None.

## Nice-to-Haves

- A capacity-matched 3-channel baseline that does not enforce common/private separation would substantially strengthen the evaluation of whether the separation mechanism itself adds value.
- Direct analysis of channel content (e.g., mutual information between each channel's representation and each task's target, or visualization of common-channel activations) would provide direct evidence for the disentanglement claim.
- An ablation of γ across a range of values (e.g., 0.1, 0.5, 1, 2, 10) and quantification of the fraction of matching elements would validate the matching mechanism.
- Reporting results across multiple random seeds with error bars would improve confidence.
- The relationship between the Markov conditions (Eq. 1) and their removal by the architecture should be clarified.

## Removed Points

These points are flagged to be removed; treat them with caution.

1. **"No comparison to representation learning approaches (CCA, contrastive learning, variational information bottleneck)"** — The paper explicitly scopes itself as a source coding / compression contribution, not a representation learning paper. The related work section (lines 39–49) discusses why these approaches are not directly comparable (unsupervised, no natural compression mechanism). Criticizing their absence is scope creep. **Removed per soft rules (scope creep).**

2. **"The paper does not state how many independent runs are performed"** — This is covered by weakness #4 (no error bars). The lack of error bars is already listed as a minor weakness. **Merged into weakness #4.**

3. **"Training procedure details relegated to appendix"** — This is standard practice for conference papers and the paper explicitly references Appendix D. The harsh critic acknowledges this is standard. **Removed per soft rules (standard practice).**

4. **"Missing related works"** — Cannot be confirmed without external sources; the paper's related work section covers Gray-Wyner theory, learnable image coding, and coding for humans and machines. **Removed per hard rules.**

5. **"The rates produced by these methods are used to compute empirical estimates... BD-rates are computed with respect to the method with no assigned score"** (from harsh critic's section-by-section notes about Figure 3) — This is an observation, not a weakness. **Removed as not a weakness.**

6. **Strengths removed:** "Theoretical grounding of the lossy Gray-Wyner framework" — kept but reframed as strength #3. The strength about "practical optimization objective" is kept as strength #1. The strength about "architecture design" is kept as strength #2. Generic praise about the introduction and previous work sections is removed as not specific enough.

## Novel Insights

None beyond the paper's own contributions. The core insight—that the Gray-Wyner framework can be operationalized as a learnable codec via a β-parameterized Lagrangian balancing transmit and receive rates—is already the paper's own contribution. The reviews do not surface any unexpected interpretation of the results or identify a deeper pattern the paper itself missed. The main critical insight from the reviews is that the experimental validation would need direct evidence of channel-content disentanglement (e.g., MI measurements between channels and task targets) to fully substantiate the paper's central claim, but this is a call for stronger evidence, not a new discovery about the method.

## Suggestions

1. **Directly validate disentanglement.** On the synthetic dataset (where ground-truth structure is known), measure the mutual information between each channel's content (Y₀, Y₁, Y₂) and each task's target (Z₁, Z₂). This would directly test whether the common channel carries shared information and private channels carry task-specific information. For real datasets, visualize common-channel activations or compute channel-task MI estimates.

2. **Add a capacity-controlled baseline.** Train a 3-channel codec that does not enforce common/private separation (all channels can carry any information, decoders can use any subset). If the proposed method beats this on transmit and/or receive rate, then the separation mechanism itself provides benefit beyond having three channels.

3. **Ablate γ and quantify matching.** Run experiments with γ ∈ {0.01, 0.1, 0.5, 1, 2, 10} and report the fraction of common-channel elements that actually match under Eq. 14. Report whether matching rates change with β.

4. **Clarify the BD-rate baseline.** State explicitly in the abstract and conclusion which baseline the -81.58% figure is computed against (Independent), and contextualize it by also reporting that the method is 13–23% worse than Joint on transmit rate.

5. **Report error bars.** Run each experiment with at least 3 random seeds and report mean ± std for rate-distortion curves.

## Score and Decision

**Bracketing (Round 1):** The most topically similar anchor is "Which Tasks Should Be Compressed Together?" (avg 5.33, accepted with mixed reviews). Papers in the 3–4 range are generally rejected with significant flaws, while papers at 5.5–6.5 typically have stronger experimental validation. My initial bracket is 3.5–5.5.

**Narrowing:** The paper has a genuine theoretical contribution (Theorem 1–2, clean Lagrangian derivation) that is stronger than the typical 3–4 rejected paper in this space. However, its experimental validation is weaker than the Taskonomy compression paper (5.33), which at least provided thorough comparisons on a large-scale benchmark (Taskonomy dataset) with multiple baselines. The Shared-AE paper (5.50) and the Disentangled SSL paper (6.25) both directly measure whether their models achieve shared/private separation—exactly what this paper does not do. Compared to these accepted papers, the experimental gap is clear and significant.

**Final score:** 4.5. The theoretical contribution and architecture design are real contributions that place this paper above a straight reject (3). However, the experimental validation is materially insufficient to support the central claims as stated, and the missing ablation of the key architectural mechanism raises questions about whether the architecture is functioning as intended. With strengthened experiments—particularly direct validation of disentanglement and a capacity-controlled baseline—this could become a solid paper.

**Anchors considered:**
- `/home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/x33vSZUg0A.md` (5.33, Round 1–3): Multi-task compression baseline; has stronger experimental scale but weaker theory.
- `/home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/yVGGtsOgc7.md` (5.80, Round 1): Disentangled representations via multi-task learning; stronger experimental validation of disentanglement.
- `/home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/zXCnIyX9MG.md` (5.50, Round 3): Shared-AE for shared/private feature identification; directly validates separation.
- `/home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/3n4RY25UWP.md` (6.25, Round 3): Disentangled SSL with information-theoretic criterion; rigorous analysis of disentanglement.
- `/home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/aQ7qYnY2nF.md` (4.00, Round 2): Task-aware video compression; rejected, weaker theory.
- `/home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/LnKDcqOfgy.md` (5.00, Round 2): Rate-distortion model quantization; less relevant domain.
- `/home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/6j0GH40mFt.md` (3.40, Round 2): LIC with attention; rejected, pure compression without theory.
- `/home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/S3zKrEQpRr.md` (3.00, Round 1): GNNs as communication channels; tangential.

MY FINAL SCORE: <score>4.5</score>
MY FINAL DECISION: <decision>Reject</decision>