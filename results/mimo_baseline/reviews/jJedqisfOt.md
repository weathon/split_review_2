## Summary
This paper proposes LRF-Dyn, a method for Spiking Transformers that addresses two limitations of Spiking Self-Attention (SSA): (1) poor local modeling capability due to the absence of softmax, and (2) high inference-time memory from storing explicit attention matrices. The method first introduces Local Receptive Fields (LRF) into SSA via dilated convolutions to recover locality bias, then approximates the resulting attention through neuronal charge-fire-reset dynamics to eliminate explicit attention matrix storage, reducing memory complexity from O(d²) to O(kd).

## Strengths
- **Consistent improvements across multiple architectures and tasks.** The method is evaluated by substituting the SSA mechanism in Spikformer, QKFormer, and SDT-V3, demonstrating robust gains (e.g., +1.24% on Spikformer-8-512, +0.48% on QKFormer-512, +0.92% on SDT-V3-S) across ImageNet-1K classification and ADE20K segmentation. This breadth of evaluation across three distinct Spiking Transformer families is commendable.
- **Clear problem identification with empirical support.** The paper provides compelling evidence that SSA produces high-entropy, nearly uniform attention distributions (Fig. 2) compared to VSA, and quantifies the locality mismatch via Manhattan distance statistics (76.68% vs. 20.31% of attention within distance 5). This motivates the proposed LRF module cleanly.
- **Biological plausibility of the approach.** The analogy between multi-dendritic neuron dynamics and the sequential accumulation of attention (Eq. 11–12) is conceptually interesting and provides a novel computational perspective on self-attention in SNNs.
- **Minimal parameter overhead.** LRF-SSA introduces fewer than 0.2M additional parameters (two 3×3 dilated depthwise convolutions), making it a lightweight drop-in enhancement.

## Weaknesses
### Fatal
None.

### Major
- **The causal attention formulation is a significant and under-discussed architectural change.** Equation 11 transforms LRF-SSA from bidirectional to causal (autoregressive) attention by changing the summation to j=1,...,n-1. This fundamentally alters the information flow: each token can only attend to preceding tokens, not future ones. For vision tasks, bidirectional attention is standard and generally superior. The paper never acknowledges this trade-off or discusses why causal attention is acceptable for vision. While LRF-Dyn's results suggest the local receptive field compensates, the paper should explicitly analyze what is lost and why the net effect is still positive.
- **Memory reduction claims lack direct empirical validation.** The paper claims LRF-Dyn reduces inference memory from O(d²) to O(kd), but never reports actual measured memory usage (e.g., peak GPU memory or theoretical byte counts). Figure 5(b) shows a visual bubble chart but without precise numbers or controlled experiments isolating memory savings. Additionally, the Fourier transform operations in Eq. 15 themselves require memory (FFT buffers, complex-valued intermediates), which is not accounted for in the complexity analysis.
- **The dynamics formulation (Eq. 13) is underspecified.** The dendritic matrix A involves a tridiagonal structure with learnable inter-dendritic couplings β and time constants τ, but the paper provides no detail on how these are parameterized, initialized, or trained. The statement "n is set as 8" (number of dendrites) appears without justification or sensitivity analysis. The connection between the biological multi-dendrite model and the actual computational implementation (Eq. 15 with Fourier transforms) is not clearly derived.

### Minor
- **Energy efficiency is claimed but not measured.** The paper repeatedly frames Spiking Transformers as energy-efficient and positions LRF-Dyn for edge deployment, yet reports no energy consumption estimates (e.g., synaptic operations, theoretical energy models). This is a missed opportunity given the paper's motivation.
- **Ablation study is on CIFAR-100 while main results are on ImageNet.** The ablation in Table 3 uses CIFAR-100 with Spikformer, which is a different scale than the main experiments. Ablations on ImageNet would strengthen the analysis.
- **Theorem 2's bound is loose.** The entropy ordering in Eq. 10 shows H(p^lrf-ssa) ≤ H(p^ssa), which is the key claim, but the intermediate bound involving h(α_i) + α_i H(p^ssa) + (1-α_i)H(r_i) is not clearly interpretable or tight. The practical implications of this bound for actual attention distributions are not discussed.

### Trivial
- Some notation inconsistencies (e.g., V_reset in Eq. 3 but not clearly defined, τ used both as time constant and as the number of dendrites in some contexts).

## Nice-to-Haves
- Provide actual measured peak memory consumption during inference for LRF-SSA vs. LRF-Dyn across different sequence lengths and model sizes.
- Include an analysis of the latency implications of the sequential causal computation in LRF-Dyn vs. the parallelizable LRF-SSA.
- Add an ablation on the number of dendrites (k) to show its effect on both accuracy and memory.

## Novel Insights
The paper's most novel insight is the theoretical connection between the charge-fire-reset dynamics of spiking neurons and the causal formulation of linear attention (Eq. 11). By showing that the accumulated KV product ∑k_j^T v_j can be interpreted as a membrane potential that evolves with each new token, and that the local receptive field component maps to presynaptic inputs, the paper provides a principled neuron-level reinterpretation of attention aggregation. This perspective could inspire future work on designing attention mechanisms grounded in neuronal computation models.

## Suggestions
- Add explicit memory measurements (in MB/GB) for LRF-SSA and LRF-Dyn during inference to substantiate the O(kd) vs. O(d²) claim.
- Provide a clear discussion of the bidirectional-to-causal transition, including whether a bidirectional variant of LRF-Dyn is possible and what the performance trade-off would be.
- Include a sensitivity analysis on the number of dendrites k and the decay parameters to help practitioners configure the method.

## Score and Decision

MY FINAL SCORE: 5.0
MY FINAL DECISION: Reject