## Summary

This paper introduces DelRec, the first surrogate gradient learning (SGL) method for training axonal or synaptic delays in recurrent connections of spiking neural networks (SNNs). The method uses a differentiable triangle interpolation with an annealing schedule to handle non-integer delays during training, then rounds to integers at inference. DelRec achieves new state-of-the-art accuracy on the Spiking Speech Commands (SSC) and Permuted Sequential MNIST (PS-MNIST) datasets using only simple Leaky-Integrate-and-Fire (LIF) neurons, and provides ablation studies showing that learned recurrent delays outperform feedforward delays under low-parameter constraints.

## Strengths

- **First SGL-based method for learning recurrent delays in SNNs.** Prior work on recurrent delay learning either used EventProp (exact gradients, limited scalability) or learned a single per-layer delay via softmax selection from a fixed set. DelRec learns per-neuron continuous delays with full gradient-based optimization, offering greater flexibility.
- **Strong empirical results.** DelRec sets new SOTA on SSC (82.58% with only recurrent delays, 82.19% with both recurrent and feedforward delays) and PS-MNIST (96.21%), using simple LIF neurons without normalization or data augmentation. The improvements over prior SOTA are modest but consistent across multiple seeds.
- **Comprehensive ablation study.** The paper systematically compares vanilla SNN, vanilla RSNN, fixed random recurrent delays, learned feedforward delays, learned recurrent delays, and their combination. The study shows that recurrent delays provide the best accuracy under low parameter counts and that they mitigate gradient issues in RSNNs.
- **Method is neuron-model agnostic and implemented in SpikingJelly.** DelRec is compatible with any spiking neuron model fitting the standard discrete-time formalism, and the code is publicly available, facilitating adoption and reproducibility.

## Weaknesses

### Major

- **Novelty claim requires clarification.** The paper states it is "the first SGL-based method to train axonal or synaptic delays in recurrent spiking layers." However, Xu et al. (ASRC-SNN) also learns recurrent delays using backpropagation with a softmax-based differentiable selection. The paper acknowledges this work but does not clearly delineate why DelRec is the "first SGL-based" method. If Xu et al. also uses surrogate gradients (which is standard for SNN backprop), the claim is inaccurate. The authors should explicitly compare the gradient computation mechanisms and justify the novelty.
- **Incremental contribution relative to DCLS.** The core technique (triangle interpolation with annealing sigma) is directly adapted from DCLS (Hammouamri et al., 2024) for feedforward delays. Applying it to recurrent connections is a natural extension, and the paper would benefit from a clearer statement of what is novel beyond the application domain.

### Minor

- **Memory and computational overhead not discussed.** The scheduling matrix \(X^{\text{rec}}\) has dimension \(N \times \dim(\tilde{\mathbb{E}})\), which can be large for long sequences or many neurons. The paper does not analyze the memory footprint or computational cost of the scheduling buffer, especially compared to standard RSNN implementations.
- **Ablation study uses small models; scalability not verified.** The comparative phase uses models with ≤10k parameters. While this is informative for understanding delay benefits under constraints, it is unclear whether the conclusions (e.g., recurrent delays outperform feedforward delays) hold for larger, SOTA-scale models.
- **No analysis of learned delay distributions.** The paper does not examine what delay values are learned, whether they cluster at certain values, or how they relate to task temporal structure. Such analysis could provide insight into why recurrent delays help.

### Trivial

- Figure 1A description is somewhat confusing; the bottom part mentions "pattern generation" but the text describes it as "regular and sustained firing pattern" without clearly explaining the mechanism.
- The naming "DelRec (only Rec. delays)" and "DelRec (Rec. and Ff. delays)" could be streamlined for clarity.

## Nice-to-Haves

- Comparison with non-spiking RNNs that incorporate learned delays (e.g., time-delay neural networks or RNNs with skip connections) to contextualize the benefits of spiking-specific delay learning.
- Hardware simulation or discussion of how DelRec maps to neuromorphic chips with programmable delays (e.g., Loihi).
- Visualization of learned delay values across neurons and layers to interpret what the network discovers.

## Novel Insights

Beyond the paper's own contributions, the key insight is that recurrent delays provide a more parameter-efficient mechanism for temporal processing than feedforward delays, especially when the number of neurons is limited. This suggests that recurrent delays enable better reuse of temporal information through self-sustained activity patterns, and that the gradient-skipping effect of delays (bridging distant time steps) is particularly beneficial in recurrent architectures where vanishing gradients are severe. The finding that combining both delay types does not help in small models but does help in larger ones hints at a trade-off between representational capacity and optimization difficulty.

## Suggestions

1. Clarify the novelty claim by explicitly comparing the gradient computation in DelRec with that in Xu et al. (ASRC-SNN). If Xu et al. uses surrogate gradients, acknowledge it and position DelRec as the first method to learn *per-neuron* continuous recurrent delays with SGL.
2. Add a brief analysis of the memory and time complexity of the scheduling matrix, and discuss practical limits on sequence length or layer size.
3. Include a figure or table showing the distribution of learned delays for the SSC or PS-MNIST experiments to provide interpretability.

## Score and Decision

The paper presents a sound method with strong empirical results and thorough ablation studies. The main weakness is the novelty claim relative to prior work, which needs clarification. The contribution is incremental but valuable: it extends differentiable delay learning to recurrent connections in a principled way and demonstrates clear benefits. I recommend acceptance with the expectation that the novelty claim is properly qualified.

MY FINAL SCORE: <score>6</score>
MY FINAL DECISION: <decision>Accept</decision>