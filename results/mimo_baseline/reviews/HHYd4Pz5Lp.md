## Summary

This paper introduces DelRec, the first surrogate gradient learning (SGL) method for training axonal or synaptic delays in recurrent spiking neural networks. The approach uses a differentiable triangle interpolation kernel (with annealing width) to handle non-integer delays during training and rounds them to integers at inference, managed through a "scheduling matrix" that pre-computes future recurrent inputs. DelRec achieves new state-of-the-art accuracy on the Spiking Speech Command (82.58%) and Permuted Sequential MNIST (96.21%) benchmarks using only vanilla LIF neurons, and matches SOTA on the saturated Spiking Heidelberg Digits dataset.

## Strengths

- **Fills a genuine gap**: DelRec is the first SGL-based method for learning recurrent delays in SNNs. Prior work on recurrent delays was limited to EventProp (Mészáros et al., 2025), which has scalability issues, or softmax-based discrete selection (Xu et al.). Given that all competitive SNN methods use SGL, this is an important contribution.

- **Strong empirical results with simple neurons**: Achieving SOTA on SSC and PS-MNIST using only vanilla LIF neurons is notable. Many competing methods rely on complex neuron dynamics (AdLIF, multi-compartment, attention), so demonstrating that delays alone can close the gap underscores the importance of the approach.

- **Well-designed ablation study (Section 3.2)**: The systematic comparison across 6 model variants on SHD, varying parameter counts and firing rates, provides clear evidence that (a) delays of any kind substantially outperform vanilla SNNs/RSNNs, (b) recurrent delays outperform feedforward delays under low-parameter regimes, and (c) even random fixed recurrent delays help mitigate training difficulties—nicely illustrating the gradient-bridging effect from Figure 1B.

- **Principled handling of the SHD saturation problem**: The paper correctly identifies that SHD is saturated (accuracies >93% have overlapping Bayesian confidence intervals given the test set size of 2264) and uses proper validation splits with data augmentation, setting a methodological standard for the community.

- **Clear and accessible presentation**: The method is well-motivated through biological plausibility and the theoretical work of Izhikevich. Figures 1 and 2 effectively illustrate the key intuitions and mechanisms.

## Weaknesses

### Fatal
None.

### Major

- **Core interpolation technique is borrowed from prior work**: The differentiable triangle interpolation kernel (Eq. 9) and the σ-annealing strategy are directly taken from DCLS (Hammouamri et al., 2024). The novelty lies in applying this to recurrent connections via the scheduling matrix mechanism. While this is a meaningful architectural contribution, the methodological novelty is somewhat incremental.

- **Missing computational cost analysis**: For a method motivated partly by energy efficiency (SNNs on neuromorphic hardware), the paper provides no comparison of training time, memory overhead, or inference cost between DelRec and vanilla RSNN or feedforward delay methods. The scheduling matrix approach clearly adds memory and computation proportional to the maximum delay, but this tradeoff is not quantified. This is important for practical deployment.

### Minor

- **Single seed for PS-MNIST**: Only one seed is tested for PS-MNIST results (acknowledged by the authors), while SSC uses 3 seeds and SHD uses 10. The margin over the prior SOTA (96.21% vs 95.77%) would benefit from variance estimates.

- **Comparison fairness in Table 1**: Different methods use different architectures, hyperparameters, and training procedures. While excluding complex neuron models is reasonable, the direct comparison of DelRec (recurrent delays only, 82.58%) vs DCLS (feedforward delays only, 80.69%) on SSC conflates the delay type with other architectural/hyperparameter differences. The cleaner comparison in Section 3.2 is only done on the smaller SHD dataset.

- **Axonal delay assumption**: The paper assumes identical delays for all outgoing connections of a neuron (axonal delays), which is a significant simplification. While stated as a design choice and the code reportedly supports synaptic delays, the paper does not evaluate the per-synapse variant for recurrent connections, leaving this as unexplored potential.

### Trivial
- Minor notation inconsistency: Eq. 12 and Eq. 13 reference "supp" and "E" with varying bold/formatting conventions.

## Nice-to-Haves

- A comparison of wall-clock training time and GPU memory usage across methods would strengthen the practical contribution.
- Evaluating synaptic (per-synapse) recurrent delays alongside axonal ones would clarify the tradeoff between expressivity and parameter efficiency.
- Testing DelRec with more complex neuron models (e.g., AdLIF) would support the claim that "even higher performance could be achieved by combining delays with more sophisticated neuron models."

## Novel Insights

The paper makes a genuinely useful observation that recurrent delays can act as temporal skip connections in the computational graph (Figure 1B), potentially alleviating vanishing/exploding gradient problems in RSNNs. The empirical finding that even random fixed recurrent delays substantially improve performance over vanilla RSNNs (Figure 3B) provides concrete evidence for this mechanism. The demonstration that recurrent delays outperform feedforward delays under tight parameter budgets, while feedforward delays can be more energy-efficient at matched performance, reveals a meaningful accuracy-efficiency tradeoff that is relevant for neuromorphic hardware design.

## Suggestions

- Add computational cost tables comparing training time and memory for DelRec vs. vanilla RSNN and DCLS on SSC/PS-MNIST.
- Report PS-MNIST results across multiple seeds with mean±std to strengthen the SOTA claim.
- Consider evaluating per-synapse recurrent delays to assess whether the additional parameters yield meaningful gains.

## Score and Decision

This is a solid method paper that addresses a clear gap (SGL-based recurrent delay learning in SNNs), achieves strong empirical results on important benchmarks, and provides a well-designed ablation study. The core interpolation technique is borrowed from DCLS, which tempers the novelty somewhat, and the missing computational cost analysis is a notable gap. However, the combination of first-mover status for recurrent delays in SGL, convincing SOTA results with simple LIF neurons, and insightful ablation analysis makes this a valuable contribution to the SNN community.

MY FINAL SCORE: <score>7.0</score>
MY FINAL DECISION: <decision>Accept</decision>