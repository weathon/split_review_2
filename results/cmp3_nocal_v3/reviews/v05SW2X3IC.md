## Summary

This paper proposes a learnable three-channel (one common + two private) codec inspired by the Gray-Wyner network from information theory for multi-task compression. It provides theoretical bounds relating two notions of lossy common information (Theorem 1), derives a Lagrangian optimization objective that navigates the transmit/receive rate tradeoff (Theorem 2, Eq. 12), and validates the approach on synthetic data, colored MNIST, Cityscapes (segmentation + depth), and COCO (detection + keypoint).

---

## Strengths

- **The theoretical framing is a genuine contribution.** The paper correctly identifies that the Gray-Wyner network provides a principled way to formalize the transmit/receive rate tradeoff in multi-task compression. Theorem 1 extends known lossless results on common information bounds to the lossy setting, and Theorem 2 bridges the gap between the information-theoretic Gray-Wyner objective and a form trainable with neural entropy models. The connection between the Lagrangian parameter β and the tradeoff operating point (β=1 for transmit, β=2 for receive, β=3/2 for equal weight) is well-motivated from theory.

- **The synthetic and colored MNIST experiments provide clean, controlled validation of the optimization objective.** On the synthetic dataset (Section 4.1, Figure 3a), optimizing for transmit rate yields common-channel rates above empirical mutual information, while optimizing for receive rate yields rates below it—exactly as the theory predicts. The colored MNIST experiments (Section 4.2, Figure 4) with three PMFs (Dependent, Independent, Mixture) show the method adapts to different information structures, including edge cases with zero or full mutual information.

- **The problem is well-motivated and practically relevant.** Separating common from private information in multi-task compression, with the ability to navigate the transmit-receive tradeoff, addresses a real need for distributed inference scenarios where the same source feeds multiple task endpoints.

---

## Weaknesses

### Major

- **The evaluation on real vision tasks does not fully support the claimed "consistently outperforms independent coding."** On Cityscapes, the proposed method at transmit-optimal β achieves BD-rate of +23.32% relative to Joint (needs 23% more bits than Joint) and +143.69% for Independent. The method does outperform Independent at *transmit* rate. However, the paper itself states (line 271) that "the curves for the receive rate are higher than the Independent approach," meaning the method is *worse* than Independent at receive rate. The abstract's claim of "consistently outperform[ing] independent coding" conflates the two rate regimes. The paper never shows a region of the tradeoff where the proposed method is simultaneously better than Joint at transmit rate and better than Independent at receive rate, nor does it quantify how much worse the proposed method is than Joint at transmit rate to justify any receive-rate improvement. The absence of Joint's receive rate (which would be 2× its transmit rate, the worst possible) further obscures the tradeoff picture.

- **The architecture ablations that directly validate the design choices (Shared vs. Separated vs. Combined) are only performed on synthetic data.** Section 4.1 compares three-channel encoder architectures on the small synthetic dataset (H=3.3 bits, linear regression tasks). On the real vision benchmarks (Cityscapes, COCO), the method is only compared against Joint (single channel) and Independent (no common channel), which are architecturally different classes. The reader cannot determine whether the Shared architecture's advantage over Separated/Combined carries over to high-dimensional, nonlinear tasks.

- **No variance or significance reporting across any experiment.** The paper reports no error bars, confidence intervals, or seed-based variability analysis. Given the known training instability of neural codecs, the absence of any stochastic uncertainty quantification is a meaningful gap that makes it difficult to assess whether the reported BD-rate differences are robust.

### Minor

- **Overclaims in the abstract and conclusion.** The abstract claims results "spanning six vision benchmarks." The paper includes: (i) synthetic data (not a vision benchmark), (ii) colored MNIST, (iii) Cityscapes (1 benchmark), (iv) COCO (1 benchmark). This counts at most 2–3 vision benchmarks, not six. The conclusion states "between the three computer vision experiments"—there are two (Cityscapes and COCO); colored MNIST is an image classification edge-case analysis, not a third CV experiment. The -81.58% BD-rate advantage claimed in the conclusion (against "single-task codecs") can be roughly derived from Figure 5's numbers, but the calculation is never explained in the body. These inaccuracies should be corrected.

- **The common-channel matching mechanism (Eq. 14) is a hard non-differentiable operation whose optimization behavior is not analyzed.** The mask operation zeroes out Y₀ elements whenever the two branch representations disagree post-quantization. Exact matches are rare without strong alignment pressure from the auxiliary L2 loss (γ‖Y₀⁽¹⁾−Y₀⁽²⁾‖²). The paper sets γ=1 and uses β as the sole hyperparameter (lines 179–182), but there is no ablation showing how common-channel utilization, separation quality, or overall rate-distortion varies with γ or with alternative matching formulations (e.g., soft attention). The gradient dynamics through this mechanism are not discussed.

- **The Markov conditions (Eq. 1) assumed by the theory are violated by the proposed architecture.** Equation 1 assumes Z₂ ↔ X₂ ↔ X₁ and Z₁ ↔ X₁ ↔ X₂. The paper acknowledges (line 167) that "each branch of the proposed architecture has access to both sources X₁ and X₂ [which] effectively removes the requirement for the conditions in 1." However, Theorem 1 and the theoretical framing of Wyner's and Gács-Körner common information rely on these conditions. The paper does not discuss whether the theory still applies when the architecture violates the assumptions, or what the implications are.

- **The "Accuracy Sum" metric used for BD-rate analysis combines different task metrics (mIoU + inverse depth RMSE) without clear justification.** The interpretability of this composite score is unclear, and the paper does not discuss how the relative weighting of the two task metrics affects the BD-rate numbers.

- **No analysis of common-channel utilization on real tasks.** For Cityscapes and COCO, the paper never reports what fraction of the total rate goes through the common channel at different β values, or whether this aligns with the estimated mutual information between tasks. These numbers would directly test whether the method is actually separating common from private information as intended on real data.

### Trivial

- None beyond the overclaims noted above.

---

## Nice-to-Haves

- Present a single figure with transmit rate on one axis, receive rate on the other, and points for the proposed method at β∈{1, 3/2, 2}, along with Joint (excellent transmit, terrible receive) and Independent (excellent receive, terrible transmit). This would directly visualize whether the method occupies a useful region of the tradeoff.
- Compare against Separated and Combined architectures on at least one real vision benchmark to validate the architectural advantage claimed from synthetic data.
- Ablate the auxiliary loss weight γ and report common-channel usage rates and separation quality.
- Report Joint's receive rate (2× its transmit rate) to show the proposed method's receive-rate advantage over Joint.

---

## Removed Points

These points from the input review were removed with brief justification:
- **"Theoretical contributions do not inform architecture/experiments" (Section 3.1)** — The paper ties Theorem 1 to the motivation for exploring the transmit-receive tradeoff (lines 107–113). While the connection is not tight, the claim that it is "not obviously useful in practice" is a judgment call that overstates the gap.
- **"Section 2 (Previous Work): variational vs entropy models"** — The paper's entropy models minimize negative log-likelihood, which is a different variational bound than MI estimation. The distinction is clear enough in context; this is a presentation preference, not a substantive weakness.
- **"Section 4.3: Fixed pre-trained models limit generality"** — Using fixed decoders is a standard and practical design choice; the results are specific to these architectures, as is true for essentially all learned codec evaluations.
- **"Section 4.1: Synthetic dataset is small"** — The synthetic experiments are explicitly designed as a controlled proof-of-concept, which the paper acknowledges. The size is adequate for that purpose.
- **"Conclusion: practical implications are asserted without evidence"** — The conclusion's mention of storage, retrieval, and routing is a brief forward-looking remark typical of conclusions, not a central claim.

---

## Novel Insights

The harsh review's most valuable observation is that the paper's real-task evaluation shows a pattern the paper itself under-discusses: the proposed method loses to Joint on transmit and loses to Independent on receive, yet the paper's narrative emphasizes outperforming Independent without qualification. This exposes that the evaluation is missing the one comparison that would make the tradeoff visible—a transmit-rate vs. receive-rate scatter plot showing where the method sits relative to the two extremes. The claim about "six vision benchmarks" is a specific, verifiable overcount that can be fixed, but it points to a broader imprecision in how the paper characterizes its own evaluation scope. None of the insights in the review go beyond what the paper self-reports but obfuscates through asymmetric presentation.

---

## Suggestions

1. Tone down the abstract to accurately reflect the experimental scope: specify "two vision benchmarks" or list them explicitly, and qualify the "outperforms independent coding" claim to acknowledge that this holds at transmit-optimal operating points.
2. Visualize the full transmit-receive tradeoff on real tasks (e.g., a 2D plot with transmit rate on one axis and receive rate on the other, showing Joint, Independent, and the proposed method at β=1, 3/2, 2).
3. Report common-channel utilization (fraction of total rate) on Cityscapes and COCO at each β.
4. Include error bars or multiple-seed runs for at least the main experiments.
5. Add an ablation varying the auxiliary loss weight γ to characterize the sensitivity of the common-channel matching mechanism.

---

## Score and Decision

MY FINAL SCORE: <score>5</score>
MY FINAL DECISION: <decision>Reject</decision>