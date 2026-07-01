## Summary
This paper introduces CausalNovo, a model-agnostic framework for de novo peptide sequencing that aims to learn causal representations from mass spectra by disentangling true signal fragment ions from spurious noise peaks. The framework is grounded in a Structural Causal Model (SCM) and operationalizes two principles—independence and sufficiency—through causal interventions and information-theoretic objectives. Experiments on three public datasets show consistent improvements over three strong baselines (CasaNovo, AdaNovo, π-HelixNovo) at amino acid, peptide, and PTM levels, with particular robustness under varying noise conditions.

## Strengths
- **Well-motivated problem and clear causal framing**: The paper identifies a genuine limitation of existing de novo sequencing models—their reliance on spurious correlations with noise peaks—and provides empirical evidence (Figure 1) that perturbing noise peaks degrades performance. The SCM formulation (Figure 2A) and the derivation of independence and sufficiency principles from Reichenbach's Common Cause Principle are conceptually sound and provide a principled foundation for the method.
- **Strong and consistent empirical results**: CausalNovo achieves substantial and consistent improvements across three datasets and three baselines, with gains of up to 10% in amino acid precision and even larger relative improvements in peptide and PTM-level metrics. The cross-species validation (Table 3) and generalization across varying Noise Signal Ratios (Figure 4) convincingly demonstrate that the framework improves robustness and generalization, not just in-distribution accuracy.
- **Comprehensive and well-designed experiments**: The paper includes thorough ablation studies (Tables 4, 5), vulnerability analysis (Figures 1, 3), analysis of peak distinguish strategies (Table 6), and attention analysis (Table 7). These experiments collectively support the claim that CausalNovo shifts model reliance toward causal signal peaks and away from spurious noise.

## Weaknesses
### Fatal
None.

### Major
- **The causal intervention relies on ground-truth peptide labels to identify non-causal peaks**: The method uses the theoretical spectrum computed from the ground-truth peptide sequence to distinguish causal from non-causal ions (Equation 4). This is a form of label leakage during training—the model uses information that would not be available in a truly unsupervised or semi-supervised setting. While the authors note this is a well-established approach in database search and prior deep learning work, it fundamentally limits the framework's applicability to settings where ground-truth labels are available (i.e., training data). The paper does not discuss how this reliance might affect the method's practical utility or whether the approach could be adapted to work without such labels.
- **The claimed "model-agnostic" property is overstated**: While CausalNovo can be integrated with different backbone architectures, the framework requires access to the encoder's latent representations and the ability to compute theoretical spectra from labels. The intervention strategy (replace-based perturbation) is also tightly coupled to the specific structure of mass spectrometry data. The paper does not discuss the generality of the framework beyond peptide sequencing or what aspects would transfer to other domains.
- **Training overhead is acknowledged but not adequately addressed**: The paper mentions a ~2.3x increase in training time due to multiple forward passes but provides no analysis of how this scales with model size, dataset size, or whether there are practical mitigations. For a method that is intended to be widely adopted, this is a non-trivial practical concern.

### Minor
- **The paper does not compare against the most recent methods under the same protocol**: The authors acknowledge that recent methods (ContraNovo, RankNovo) use a more realistic training protocol (large-scale external corpora, out-of-distribution evaluation) and state that evaluating under this protocol is future work. However, this limits the strength of the current comparisons, as the baselines are evaluated under a different (potentially easier) setting.
- **The attention analysis (Table 7) is interesting but the interpretation is somewhat ambiguous**: The table shows that CausalNovo attends to more causal peaks, but it does not establish a causal link between attention patterns and correctness. The analysis of corrected cases (Appendix Table 14) is more informative but is relegated to the appendix.

### Trivial
None.

## Nice-to-Haves
- An analysis of how the choice of replacement fraction α affects performance would be useful for practitioners.
- A discussion of whether the framework could be extended to use predicted (rather than ground-truth) theoretical spectra during inference, which would make it applicable in a fully de novo setting.

## Novel Insights
None beyond the paper's own contributions.

## Suggestions
- Discuss the label leakage issue more explicitly and consider whether the framework could be adapted to use predicted labels or a self-supervised approach for identifying non-causal peaks.
- Provide a more detailed analysis of the training overhead and potential mitigations (e.g., whether the intervention can be applied less frequently).
- Evaluate CausalNovo under the more realistic training protocol used by ContraNovo and RankNovo to strengthen the comparison.

## Score and Decision
The paper presents a well-motivated, principled, and empirically strong contribution to a specific application domain. The causal framing is novel for peptide sequencing, and the results convincingly demonstrate improved robustness and generalization. The major weakness regarding label leakage for identifying non-causal peaks is a genuine limitation but does not invalidate the core contribution, as the method is designed for supervised training. The paper is clearly written, the experiments are thorough, and the code is provided. I recommend acceptance.

MY FINAL SCORE: <score>8</score>
MY FINAL DECISION: <decision>Accept</decision>