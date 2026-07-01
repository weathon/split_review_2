## Summary

This paper introduces DelRec, a method for learning axonal or synaptic delays in recurrent connections of spiking neural networks (SNNs) using surrogate gradient learning and backpropagation. The method employs differentiable interpolation with a triangle function to handle non-integer delays during training, progressively annealing the spread parameter to converge to integer delays at inference. The authors demonstrate state-of-the-art results on Spiking Speech Commands (SSC) and Permuted Sequential MNIST (PS-MNIST) datasets using simple LIF neurons, and provide ablation studies showing that learned recurrent delays outperform feedforward delays under low-parameter constraints.

## Strengths

- **Novel and well-motivated contribution**: This is the first SGL-based method to train delays in recurrent spiking connections, addressing a gap identified in prior theoretical work. The motivation is clearly grounded in biological plausibility (myelin plasticity) and computational benefits (gradient mitigation, richer dynamics).

- **Strong empirical results**: The method achieves new SOTA on SSC (82.58% with only recurrent delays, 82.19% with both) and PS-MNIST (96.21%) using simple LIF neurons, outperforming methods that rely on more complex neuron models. The results are reported with multiple seeds and standard deviations where appropriate.

- **Thorough ablation and functional study**: The comparative analysis on SHD (Figure 3) systematically isolates the contribution of recurrent delays versus feedforward delays, random delays, and vanilla architectures. The parameter count and firing rate analyses provide meaningful insights about tradeoffs.

- **Clean methodology**: The differentiable interpolation approach with progressive σ annealing is elegant and well-explained. The scheduling matrix formulation with pointer mechanism is practical and computationally efficient.

## Weaknesses

### Major

- **Limited architectural exploration**: All experiments use fully connected architectures with at most 3 hidden layers. The paper does not demonstrate compatibility with convolutional layers or more modern SNN architectures (e.g., ResNet-style, transformer-based). This limits the generality claims.

- **Missing comparison with non-spiking recurrent models**: The paper claims recurrent delays are "critical for temporal processing" but does not compare against standard non-spiking RNNs (LSTM, GRU) or modern alternatives (S4, Mamba) on the same benchmarks. This would contextualize whether the gains are specific to SNNs or reflect general temporal modeling improvements.

- **Incomplete analysis of learned delay distributions**: The paper does not analyze what delays are actually learned (e.g., histograms, whether they cluster at certain values, whether they differ across layers or tasks). This would strengthen the claim that delays are meaningfully optimized rather than just providing additional degrees of freedom.

### Minor

- **SHD dataset concerns**: The authors acknowledge SHD saturation issues but still use it for ablation. The "clean split" methodology (20% validation) differs from many prior works, making direct comparison in Table 2 somewhat inconsistent.

- **Computational cost not reported**: The paper does not discuss training time, memory overhead of the scheduling matrix, or how the method scales with sequence length and layer size. This is relevant for practical adoption.

- **Hyperparameter sensitivity**: The σ annealing schedule and initial σ value are critical but not systematically ablated. The paper uses different σ schedules across datasets without justification.

### Trivial

- The paper states "our method is compatible with any spiking neuron model" but only tests LIF neurons.

## Nice-to-Haves

- Analysis of learned delay values across layers and tasks (e.g., do deeper layers learn longer delays?)
- Comparison with learned skip connections in standard RNNs to isolate the benefit of the spiking mechanism
- Demonstration on a neuromorphic hardware platform with programmable delays
- Ablation of the σ annealing schedule

## Novel Insights

Beyond the paper's own contributions, a genuinely novel insight is that recurrent delays in SNNs serve a dual role: they enhance expressivity through polychronization/coincidence detection while simultaneously improving gradient flow by creating temporal skip connections. This suggests that the gradient mitigation benefit (Figure 1B) may be as important as the representational benefit, which is a perspective not emphasized in prior delay-learning work. The finding that recurrent delays outperform feedforward delays under low-parameter constraints (Figure 3C) is also notable, as it suggests recurrent delays enable more efficient reuse of temporal information when representational capacity is limited.

## Suggestions

- Add experiments with convolutional layers or at least one modern SNN architecture to strengthen generality claims.
- Include a comparison with a simple non-spiking recurrent baseline (e.g., LSTM with comparable parameters) on SSC or PS-MNIST.
- Report training time and memory usage, and discuss scaling behavior.
- Visualize learned delay distributions (e.g., histograms) for at least one experiment.
- Ablate the σ annealing schedule (e.g., linear vs. cosine, different initial σ values).

## Score and Decision

The paper presents a novel, well-motivated method with strong empirical results on standard benchmarks. The ablation studies are thorough and provide meaningful insights. The main limitations are the restricted architectural scope and missing comparisons with non-spiking temporal models, but these do not invalidate the core contribution. The work is likely to be of significant interest to the SNN community and has clear practical implications for neuromorphic computing.

MY FINAL SCORE: <score>8</score>
MY FINAL DECISION: <decision>Accept</decision>