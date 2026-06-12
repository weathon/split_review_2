## Summary

This paper investigates combining dynamic sparse training (specifically Cannistraci-Hebb Training, CHT) with ANN-to-SNN conversion pipelines, studying how structural connectivity sparsity interacts with the temporal sparsity inherent to SNNs. The authors show that sparse SNNs can achieve comparable or superior accuracy to dense SNNs while reducing theoretical energy consumption by up to 99%, and they discover a novel temporal phenomenon: firing rate saturation consistently precedes accuracy saturation, with sparse networks exhibiting larger time lags than dense networks.

## Strengths

- **Novel intersection of two active research areas**: Combining dynamic sparse training with ANN-to-SNN conversion has not been studied before, and the motivation is clear—structural sparsity and temporal sparsity should be complementary for energy efficiency. This is a genuine gap worth filling.

- **Broad experimental scope**: The paper systematically evaluates across 3 architectures (MLP, VGG-16, ViT-B), 3 datasets (CIFAR-10, CIFAR-100, ImageNet-1K), and 4 conversion methods (QCFS, SNM, AEC, SpikeZIP-TF), providing reasonable evidence for the generality of the main findings.

- **Novel temporal dynamics observation**: The time lag phenomenon—where Model Average Spike Firing Rate (MASFR) saturates before accuracy—is a genuinely new empirical observation, supported by appropriate statistical tests (Wilcoxon signed-rank and Mann-Whitney tests) with very small p-values across diverse experimental settings.

- **Practical pipeline contribution**: The paper demonstrates a concrete, easy-to-implement pipeline (train sparse ANN with CHT → freeze topology → convert to SNN) that yields consistent energy savings.

## Weaknesses

### Fatal

None.

### Major

- **Thin methodological contribution**: The core methodological contribution is simply freezing the sparse topology during conversion—an operationally trivial adaptation of existing conversion methods. There is no new algorithm, loss function, or significant modification to either the sparse training or conversion components. This positions the paper as an empirical study rather than a methods paper, which is fine, but the depth of analysis doesn't fully compensate.

- **Energy savings are largely tautological for high-sparsity cases**: For MLP with 99% sparse linear layers, the reported 99% energy reduction is essentially a direct consequence of the sparsity level rather than an emergent finding. The theoretical energy model (Equation 1) simply counts total spikes, and with ~99% fewer connections, ~99% fewer spike transmissions occur. The more interesting cases (VGG-16 at 50% sparsity, ViT-B at 70%) show proportional but less dramatic savings. Moreover, the authors acknowledge the energy analysis is purely theoretical and assumes future hardware supporting both sparse and event-driven computation simultaneously.

- **Mixed accuracy results on stronger benchmarks**: Table 1 shows that for VGG-16 and ViT-B, sparse SNNs frequently underperform dense SNNs in accuracy (5 out of 8 experiments have negative accuracy improvement). The strongly positive results are concentrated on MLP/CIFAR-10/100, where the dense baselines are weak (63.89% on CIFAR-10). The paper's framing of "8 out of 13 experiments" showing improvement obscures this pattern.

- **Time lag analysis lacks mechanistic depth**: The observation that sparse networks have larger time lags than dense networks is interesting, but the explanation offered is superficial—the qualitative argument about rate decoding doesn't explain why sparsity specifically increases the lag. The connection to the accuracy-energy trade-off remains entirely speculative ("may be a potential cause") with no supporting evidence.

### Minor

- No comparison with other DST methods (e.g., SET, RigL, MEST) to establish whether findings are CHT-specific or general to sparse networks. The STBP comparison mentioned in Appendix D is not discussed in the main text.

- The saturation detection threshold (1% improvement over 10 consecutive time steps) is somewhat arbitrary, with no sensitivity analysis.

- MLP baselines on CIFAR-10 achieve only 63.89% accuracy, making accuracy comparisons on this benchmark less meaningful.

## Nice-to-Haves

- Per-layer firing rate analysis to provide mechanistic insight into the time lag phenomenon rather than relying solely on the model-average metric.
- Comparison with at least one non-CHT sparse training method to demonstrate generality.
- Sensitivity analysis of the saturation detection threshold on the time lag conclusions.
- Measured FLOPs or hardware simulation as a more concrete proxy for energy than the theoretical spike-counting model.

## Novel Insights

The time lag between firing rate saturation and accuracy saturation in converted SNNs is a genuinely novel empirical observation. The statistical evidence is strong (p-values on the order of 10⁻⁴¹ to 10⁻⁸²), and the observation holds across methods and architectures. The additional finding that this lag differs significantly between sparse and dense networks is intriguing and could inspire future theoretical work on how connectivity topology affects temporal information processing in SNNs. However, the mechanistic understanding remains shallow, and the causal connection to the accuracy-energy trade-off is unsubstantiated.

## Suggestions

1. Add at least one comparison with a non-CHT DST method (e.g., RigL or SET) to determine if findings generalize beyond CHT.
2. Investigate the time lag mechanism by analyzing per-layer firing rate dynamics, particularly comparing early vs. late layers in sparse vs. dense networks.
3. Re-examine the accuracy-claimed results for VGG-16 and ViT-B more carefully; the paper's narrative of "close or superior accuracy" doesn't fully hold for these architectures.
4. Provide sensitivity analysis of the saturation detection algorithm parameters.

## Score and Decision

The paper fills a genuine gap at the intersection of sparse training and SNN conversion, with commendable experimental breadth and a novel temporal dynamics observation. However, the methodological contribution is thin (trivial topology freezing), the energy analysis is largely a direct reflection of sparsity levels rather than an emergent finding, and the most interesting result (time lag differences) lacks mechanistic explanation. The accuracy advantages are clear only for the weakest benchmark (MLP/CIFAR). The paper provides value as an empirical exploration but falls short of the depth expected for a strong ICLR contribution.

MY FINAL SCORE: <score>5.0</score>
MY FINAL DECISION: Reject