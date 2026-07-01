## Summary
The paper introduces DelRec, the first surrogate-gradient-based method for learning axonal (or synaptic) delays in recurrent connections of spiking neural networks. It uses a differentiable interpolation with a progressively narrowing spread to handle continuous delays during training, then rounds to nearest integers for inference. On Spiking Speech Commands and Permuted Sequential MNIST, DelRec with simple LIF neurons achieves new state-of-the-art accuracy, outperforming more complex neuron models. Ablations on the Spiking Heidelberg Digits dataset show that learned recurrent delays provide consistent gains over vanilla RSNNs and competitive performance against feedforward delay learning, especially under low parameter budgets.

## Strengths
- **Novel and well-motivated technique:** Extending continuous delay learning (previously only for feedforward connections) to recurrent connections is a natural and impactful idea, biologically grounded and shown to improve temporal processing. The differentiable interpolation with progressive narrowing of the spread is a clean way to handle non-integer delays while maintaining well-defined gradients.
- **Strong empirical results:** DelRec achieves state-of-the-art on SSC (82.58%) and PS-MNIST (96.21%) using only simple LIF neurons, surpassing methods that rely on more complex intrinsic dynamics. The results are reported with multiple seeds for SSC, and the improvements are convincing.
- **Thorough ablation study:** The paper systematically compares recurrent delays against feedforward delays, fixed random delays, and vanilla RSNNs under varying parameter counts and sparsity constraints, providing clear insights into the relative benefits and trade-offs (e.g., performance vs. firing rate). The analysis of gradient propagation (Figure 1B) is conceptually helpful.
- **Clarity and reproducibility:** The method is clearly described with algorithmic details (Algorithm 1, even if not shown in main text), the code is provided, and hyperparameters are given in the appendix. The authors are transparent about the saturation of SHD and use a clean validation split.

## Weaknesses
### Fatal
None.

### Major
None.

### Minor
- **Claim of being “first” SGL-based method:** The paper states “the first method to train axonal or synaptic delays in recurrent connections using surrogate gradient learning (SGL) and backpropagation.” However, prior work (Xu et al., ASRC-SNN) also trains recurrent delays with backpropagation (presumably using SGL), albeit via a softmax selection over a discrete set rather than continuous interpolation. The distinction should be explicitly clarified to avoid overclaiming; the novelty lies in the **continuous** delay optimization with interpolation.
- **Limited analysis of learned delays:** The functional study focuses on accuracy vs. parameters and firing rate, but does not examine what delay values are actually learned, their distribution across neurons, or how they change during training. Such insights would strengthen the understanding of how recurrent delays improve temporal processing.
- **Single seed for PS-MNIST:** Following prior work, only one seed is reported for PS-MNIST. While acceptable, reporting multiple seeds (as done for SSC) would increase statistical confidence and match the standard set on the other datasets.
- **No discussion of computational/memory overhead:** The scheduling matrix buffer grows with the maximum delay and layer size, and the spread function is evaluated for a range of future time steps. The paper does not quantify the additional memory or compute cost relative to a standard RSNN, which is important for practitioners considering neuromorphic deployment.

### Trivial
- The abbreviation “DelRec” is used both for the method and for configuring “Rec. and Ff. delays” vs. “only Rec. delays” in tables, which could be slightly confusing at first glance. The naming is otherwise fine.

## Nice-to-Haves
- Provide an analysis of learned delay distributions (e.g., histogram over neurons) on one of the tasks.
- Include a runtime/memory comparison between DelRec and a vanilla RSNN of the same size.
- Explore combining DelRec with more sophisticated neuron models (e.g., adaptive LIF) to see if the benefits are additive.

## Novel Insights
None beyond the paper’s own contributions.

## Suggestions
- Reframe the novelty claim to “the first method to learn **continuous** axonal or synaptic delays in recurrent connections with surrogate gradient learning and backpropagation” to accurately differentiate from prior discrete-selection approaches.
- Add a short paragraph or a supplementary figure showing a typical learned delay histogram on SSC or PS-MNIST to give readers intuition about how delays are distributed.
- Include a brief remark on memory consumption: the scheduling matrix is of size N × (max_delay + constant), which is modest for the reported architectures but could be noted for scalability.

## Score and Decision
**Score:** 8

**Decision:** Accept

The paper makes a solid contribution by extending continuous delay learning to recurrent connections in SNNs, achieving state-of-the-art results on two challenging benchmarks with simple neurons. The experiments are thorough and well-controlled, and the ablations convincingly demonstrate the value of learned recurrent delays. The weaknesses are minor and do not undermine the core claims; the “first” claim can be easily adjusted. Overall, the paper offers clear value to the community and meets the bar for acceptance.

MY FINAL SCORE: <score>8</score>  
MY FINAL DECISION: <decision>Accept</decision>