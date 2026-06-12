## Summary

This paper introduces Long-tailed Test-Time Adaptation (L-TTA), the first method specifically designed for test-time adaptation of Vision-Language Models under long-tailed test distributions. The authors identify two unique failure modes in this setting—text-induced tail erosion and modality-bias amplification—and propose three co-designed components: Synergistic Prototypes (SyPs) with Deterministic and Exclusionary Prototypes to enrich tail class representations, Rebalancing Shortcuts (RSs) with a class re-allocation loss for dynamic adaptation, and Balanced Entropy Minimization (BEM) to counteract head-class bias in standard entropy minimization. Extensive experiments across 15 datasets under various imbalance ratios demonstrate consistent improvements over existing TTA methods in both accuracy and macro-F1.

## Strengths

- **Novel problem formulation**: The paper is the first to systematically study test-time adaptation under long-tailed distributions for VLMs, identifying two specific failure modes (text-induced tail erosion and modality-bias amplification) that are unique to this setting and well-motivated.
- **Comprehensive experimental evaluation**: The method is evaluated across 15 datasets spanning OOD benchmarks, cross-domain benchmarks, and corruption benchmarks under three imbalance ratios (10, 20, 50), with consistent improvements over 12 baselines. The inclusion of macro-F1 alongside accuracy is appropriate for long-tailed evaluation.
- **Theoretical grounding**: The paper provides propositions (Proposition 1 and 2) to justify why standard EM fails under long-tailed TTA and why BEM mitigates this issue, with proofs deferred to the appendix.
- **Efficiency considerations**: The method achieves strong performance while maintaining reasonable computational overhead (1.45h on ImageNet), outperforming heavier methods like RLCF and WATT while being competitive with lightweight approaches.

## Weaknesses

### Fatal
None.

### Major
- **Limited analysis of the long-tailed test distribution construction**: The paper creates long-tailed test sets by random sampling to achieve specific imbalance ratios, but the relationship between this synthetic construction and real-world long-tailed test distributions is not discussed. Real-world test streams may have temporal correlations (e.g., bursts of tail classes) that are not captured by random sampling. The robustness experiment in Table 7 partially addresses this but only varies sampling probability, not temporal structure.
- **Proposition proofs are deferred to appendix**: While the paper states "We defer the proof to Appx. A," the appendix is stripped from the provided content. Without seeing the proofs, it is impossible to verify the theoretical claims (Propositions 1 and 2), which are central to motivating BEM. This is a significant concern for a paper that makes theoretical claims.
- **The Exclusionary Prototype update mechanism (Eq. 5) is computationally intensive**: Updating EPs for all C classes at every step based on each view's prediction distribution scales as O(C × Q) per sample. For datasets with many classes (e.g., ImageNet with 1000 classes), this could be prohibitive, yet the paper does not discuss this scaling behavior or provide complexity analysis beyond the single ImageNet timing.

### Minor
- **Hyperparameter sensitivity**: The method introduces several hyperparameters (λ₁, λ₂, η, K, β, θ, Q) that require tuning. While ablation studies are provided for most, the interaction effects between these parameters are not explored. The paper sets K=0.3 in implementation details but Figure 4c shows K=0.2 yields best performance—this inconsistency is confusing.
- **The affinity function A(x) = λ₁ exp(-λ₂(1-x)) is not well motivated**: The paper cites Gao et al. (2024) but does not explain why this specific exponential scaling is appropriate for combining prototype similarities with text similarities in Eq. 8.
- **Limited discussion of failure cases**: While the paper shows strong average performance, it does not analyze cases where L-TTA underperforms baselines (e.g., on certain datasets or classes), which would provide valuable insights into the method's limitations.

### Trivial
- The paper states "K = 0.3" in implementation details but Figure 4c uses "b" instead of "K" and shows K=0.2 as optimal—this labeling inconsistency should be resolved.

## Nice-to-Haves

- An analysis of how the method performs when the test distribution has temporal structure (e.g., blocks of tail classes followed by head classes) would strengthen the real-world applicability claims.
- A comparison with simply applying existing long-tailed learning techniques (e.g., logit adjustment, balanced softmax) to TTA baselines would help isolate the benefits of the proposed components over straightforward adaptations.
- Visualizations of the learned hyper-class vectors and how they cluster prototypes would provide intuitive understanding of the Rebalancing Shortcuts mechanism.

## Novel Insights

Beyond the paper's own contributions, the key insight is that test-time adaptation under long-tailed distributions introduces unique challenges that cannot be addressed by simply combining existing TTA methods with standard long-tailed learning techniques. The identification of "text-induced tail erosion"—where pre-trained text embeddings carry inherent biases that interact with class frequency—is a genuinely novel observation specific to VLMs. The idea of using "exclusionary prototypes" that store improbable features for all classes (rather than just negative features for the predicted class) is an interesting conceptual shift that leverages the full prediction distribution to enrich tail class representations even when those classes are rarely observed.

## Suggestions

- Clarify the inconsistency between the stated K=0.3 in implementation details and the optimal K=0.2 shown in Figure 4c.
- Provide the proofs for Propositions 1 and 2 in the main text or ensure they are available in the appendix for review.
- Add a discussion of computational scaling with respect to the number of classes, particularly for the EP update mechanism.
- Include an analysis of per-class accuracy improvements to demonstrate that gains are indeed coming from tail classes rather than just overall improvement.

## Score and Decision

The paper addresses a novel and practically important problem, provides a well-designed method with three complementary components, and demonstrates consistent improvements across extensive benchmarks. The main concerns are the deferred theoretical proofs (which cannot be verified from the provided content) and the limited analysis of how the synthetic long-tailed construction relates to real-world scenarios. However, the empirical evidence is strong and the problem formulation is timely. The paper represents a solid contribution to the TTA literature.

MY FINAL SCORE: <score>8</score>
MY FINAL DECISION: <decision>Accept</decision>