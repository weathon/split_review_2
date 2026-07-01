## Summary
This paper proposes a learnable three-channel codec inspired by the Gray-Wyner network from information theory, designed to disentangle shared (common) information from task-specific (private) information across multiple vision tasks. The authors characterize the limits of this approach through lossy common information, derive an optimization objective that balances the transmit-receive rate tradeoff, and empirically demonstrate that their method reduces redundancy and outperforms independent coding on synthetic data, edge-case classification tasks, and two-task scenarios on Cityscapes and COCO.

## Strengths
- **Strong theoretical foundation**: The paper connects classic information theory (Gray-Wyner network, Wyner's and Gács-Körner common information) to a practical learnable codec, providing Theorem 1 (bounds on lossy common information) and Theorem 2 (optimization objective derivation) that ground the method in rigorous theory.
- **Novel and well-motivated problem formulation**: The transmit-receive rate tradeoff is a genuinely useful concept for distributed inference, storage, and selective retrieval. The paper clearly explains why isolating common information is non-trivial and why the tradeoff matters, with practical motivation (e.g., camera transmitting only additional information when a new task is requested).
- **Comprehensive experimental evaluation**: The paper evaluates on synthetic data (with known ground-truth information quantities), edge-case classification (colored MNIST with controlled mutual information), and two realistic computer vision benchmarks (Cityscapes, COCO). The ablation study comparing Shared, Separated, Combined, Joint, and Independent architectures is thorough.
- **Clear architectural design**: The proposed architecture (Figure 2) is well-explained, including the matching mechanism for the common channel (Eq. 14) and the auxiliary loss (Eq. 15). The use of conditional entropy models for private channels conditioned on the common representation is a sensible design choice.

## Weaknesses
### Fatal
None.

### Major
- **Limited practical advantage over Joint coding**: In the Cityscapes and COCO experiments (Figure 5), the proposed method's transmit rate is only 13-23% better than Joint (BD-rate), while the Independent baseline is 77-144% worse. The Joint method (single common channel, no private channels) is a strong baseline that the proposed method only marginally beats. The paper does not adequately discuss scenarios where the added complexity of three channels is justified over a simpler Joint codec.
- **The synthetic experiment (Section 4.1) is not fully convincing**: The synthetic dataset has only 3.3 bits of joint entropy, and the theoretical vs. empirical rate gap is large (Figure 3). The paper attributes this to "often seen in practice" (Bajić, 2025), but this gap undermines the quantitative claims about achieving Wyner's or Gács-Körner common information. The empirical rates are far from the theoretical bounds, making it unclear whether the method truly approaches the information-theoretic limits.
- **Missing comparison to relevant baselines**: The paper compares against Joint, Independent, Separated, and Combined architectures, but does not compare against existing multitask learnable codecs (Chamain et al., 2021; Feng et al., 2022; Guo et al., 2024) that are cited in the related work. Without this comparison, it is unclear whether the proposed method offers advantages over existing approaches.

### Minor
- **The Markov conditions (Eq. 1) are assumed but then effectively removed**: The paper states that the architecture "removes the requirement for the conditions in 1" because both branches have access to both sources. This is a significant departure from the original Gray-Wyner setting, and the implications for the theoretical results (Theorem 1, Theorem 2) are not fully discussed.
- **The choice of β=3/2 as "equally optimizing for both rates" is not fully justified**: The paper states that β=3/2 equally optimizes transmit and receive rates, but the Lagrangian (Eq. 12) has β multiplying only r0, while r1 and r2 have coefficient 1. The relationship between β and the tradeoff is not derived from first principles; it is asserted based on the transmit/receive rate formulas.

### Trivial
- The paper uses "codec" to refer to the entire system, but the entropy models are relatively simple (Ballé et al., 2018) and the coding efficiency is not the main focus. The term "codec" may be slightly misleading for readers expecting state-of-the-art compression performance.

## Nice-to-Haves
- A comparison against the cited multitask codecs (Chamain et al., 2021; Feng et al., 2022; Guo et al., 2024) would strengthen the empirical evaluation.
- An analysis of the common channel's content (e.g., visualization of what information is stored in Y0) would provide intuitive understanding of the method's behavior.
- A discussion of the computational cost (parameters, FLOPs) of the three-channel architecture vs. the Joint and Independent baselines.

## Novel Insights
The paper's key insight is that the transmit-receive tradeoff in the Gray-Wyner network can be operationalized through a learnable codec with a single hyperparameter β, and that the gap between Wyner's and Gács-Körner common information (which is often large in practice, e.g., zero for Gaussian sources) provides a strong motivation for exploring this tradeoff. The theoretical bounds (Theorem 1) connecting interaction information to the two common information measures are a genuinely novel contribution that extends Wyner's lossless result to the lossy setting.

## Suggestions
- Add a comparison against existing multitask learnable codecs to demonstrate the practical advantage of the three-channel architecture.
- Provide a more detailed analysis of the gap between empirical and theoretical rates, and discuss whether the method can be improved to close this gap.
- Clarify the relationship between β and the transmit/receive tradeoff with a derivation or a more precise statement.

## Score and Decision
The paper makes a solid theoretical contribution (Theorem 1, Theorem 2) and proposes a well-motivated architecture. The experimental evaluation is thorough in terms of ablation and edge-case testing, but the practical advantage over the Joint baseline is modest, and the lack of comparison to existing multitask codecs weakens the empirical claims. The paper is clearly written and the ideas are novel, but the impact is somewhat limited by the small performance gains on realistic benchmarks.

MY FINAL SCORE: 6.0<score>6.0</score>
MY FINAL DECISION: Accept<decision>Accept</decision>