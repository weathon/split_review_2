## Summary

This paper introduces a learnable Gray-Wyner network for multi-task compression, separating common and private information between two tasks. It provides theoretical bounds on lossy common information (Theorem 1), derives an optimization objective that trades off transmit and receive rates (Theorem 2), and proposes a three-channel codec architecture. Experiments on synthetic data, colored MNIST, Cityscapes, and COCO show that the method reduces redundancy compared to independent coding and can explore the transmit-receive tradeoff.

## Strengths

- **Novel theoretical framing**: The paper bridges classic Gray-Wyner theory with modern learnable codecs, providing new bounds on lossy common information (Theorem 1) and a principled optimization objective (Theorem 2) that explicitly captures the transmit-receive tradeoff. This is a genuine contribution to the information-theoretic understanding of multi-task compression.
- **Well-motivated problem**: The transmit-receive tradeoff is practically important for distributed inference and selective retrieval, and the paper clearly explains why isolating common information is non-trivial in lossy settings.
- **Comprehensive ablation and edge-case experiments**: The synthetic dataset and colored MNIST experiments with controlled mutual information (Dependent, Independent, Mixture PMFs) convincingly demonstrate that the proposed method can adapt to different levels of common information and that the β hyperparameter effectively controls the tradeoff.
- **Practical relevance**: The method achieves substantial BD-rate savings over independent coding on Cityscapes and COCO, showing that the Gray-Wyner approach can yield real compression gains in realistic computer vision tasks.

## Weaknesses

### Major

1. **Missing comparison to existing multi-task codecs**: The paper mentions prior multi-task codec works (Chamain et al., 2021; Feng et al., 2022; Guo et al., 2024) but does not compare against them experimentally. The baselines are only Joint (single common channel, no private channels) and Independent (two separate single-task codecs). The proposed method is essentially a tradeoff between these two extremes; without comparison to other multi-task architectures that also use multiple channels, it is unclear whether the Gray-Wyner design offers additional benefits beyond what simpler multi-task codecs already achieve.

2. **Ad-hoc common channel construction**: The mechanism for combining the two branches into a common representation (Eq. 14) – averaging when elements match, zero otherwise – is heuristic and potentially fragile. The auxiliary loss (Eq. 15) with γ=1 is used to encourage matching, but the paper acknowledges that small γ underutilizes the common channel and large γ causes degenerate distributions. This design choice is not theoretically justified and may limit the method's robustness across different tasks and datasets.

3. **Limited evaluation of the theoretical bounds**: Theorem 1 provides bounds relating Gács-Körner and Wyner common information via interaction information, but the paper does not empirically verify these bounds or use them to analyze the learned representations. The connection between theory and experiments is weak; the paper would be significantly stronger if it showed, for example, that the interaction information of the learned representations falls within the predicted bounds.

### Minor

4. **Clarity of the architecture description**: The architecture overview (Figure 2) and the text describing the entropy models and conditioning are somewhat confusing. It is not immediately clear how the common representation Y0 is used as context for the private entropy models, or how the "mask" block works. The paper would benefit from a more detailed, step-by-step explanation of the data flow.

5. **Pre-trained task models kept fixed**: The task-specific models (DeepLabV3+, Faster R-CNN, etc.) are frozen during codec training. This limits the ability of the codec to adapt representations for the tasks and may not be optimal. The paper does not discuss whether fine-tuning the task models would improve performance or change the tradeoff.

6. **Claim about BD-rate advantage**: The paper states "our codecs achieved, on average, a BD-rate advantage of -81.58% in transmit rate, against single-task codecs." This number is reported without clear definition of "single-task codecs" (presumably Independent) and without error bars or statistical significance. The claim seems overly strong and should be contextualized.

### Trivial

7. The paper uses "receive rate" defined as 2R0 + R1 + R2, which assumes both tasks are received separately. This is a specific operational scenario; the paper could clarify that other definitions are possible.

## Nice-to-Haves

- Compare against other multi-task codec architectures (e.g., Chamain et al., Feng et al., Guo et al.) to demonstrate the advantage of the Gray-Wyner design.
- Empirically verify the bounds from Theorem 1 by computing interaction information of learned representations.
- Provide an ablation on the auxiliary loss weight γ to show robustness.
- Include error bars or confidence intervals on rate-distortion curves.

## Novel Insights

The paper's key insight is that the transmit-receive tradeoff in the Gray-Wyner network can be operationalized in a learnable codec through a single hyperparameter β, and that the common channel rate naturally falls between the two lossy common information measures (Wyner and Gács-Körner) when β is between 1 and 2. The theoretical result that interaction information bounds these measures (Theorem 1) is a useful extension of lossless results to the lossy case, though the paper does not fully exploit it experimentally.

## Suggestions

- Add experimental comparisons to prior multi-task codec methods (e.g., Chamain et al. 2021, Feng et al. 2022) to strengthen the empirical contribution.
- Provide a more detailed explanation of the common channel construction and the role of the auxiliary loss, possibly with an ablation on γ.
- Include an analysis of the learned representations (e.g., mutual information estimates, interaction information) to validate the theoretical bounds.
- Clarify the definition of "single-task codecs" and report BD-rate with confidence intervals.

## Score and Decision

**Score**: 6  
**Decision**: Accept

The paper makes a solid theoretical contribution by extending Gray-Wyner theory to learnable codecs and provides a practical architecture that demonstrably reduces redundancy over independent coding. However, the experimental evaluation lacks comparison to existing multi-task codecs, and the architecture has some ad-hoc elements. The paper is above the ICLR median and brings value to the community, but the weaknesses prevent it from being a strong accept.

MY FINAL SCORE: <score>6</score>  
MY FINAL DECISION: <decision>Accept</decision>