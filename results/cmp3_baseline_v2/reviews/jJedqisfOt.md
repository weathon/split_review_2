## Summary

The paper identifies two key limitations of Spiking Transformers: (i) a performance gap relative to ANNs due to the lack of locality bias in Spiking Self-Attention (SSA), and (ii) high memory overhead during inference from storing attention matrices. To address these, the authors propose LRF-Dyn, which augments SSA with local receptive fields (LRF) via dilated convolutions to improve local modeling, and then reformulates attention using neuronal membrane-potential dynamics to eliminate explicit attention matrix storage, reducing memory to O(kd). Experiments on ImageNet classification and ADE20K segmentation show consistent accuracy improvements (0.4–1.24%) over SSA baselines across three spiking transformer architectures (Spikformer, QKFormer, SDT-V3).

## Strengths

- **Clear problem formulation**: The paper convincingly demonstrates, both theoretically and empirically, that SSA suffers from a lack of locality bias (uniform attention distribution) and high memory footprint, which are real bottlenecks for deploying spiking transformers on edge devices.
- **Consistent empirical improvements**: The proposed LRF-SSA and LRF-Dyn achieve positive accuracy gains (0.4–1.24%) across multiple architectures (Spikformer, QKFormer, SDT-V3) on ImageNet, and 1.8–2.7% mIoU gains on ADE20K segmentation, while adding negligible parameters.
- **Memory reduction claim is well-motivated**: The reformulation of attention as a recurrent neuronal process (Eq. 11–12) is a natural way to avoid storing O(d²) attention matrices, and the theoretical storage complexity is reduced from O(d²) to O(kd) with k≪d.

## Weaknesses

### Major

1. **Limited novelty relative to prior linear attention and recurrent formulations**. The core idea of avoiding explicit attention matrix storage by computing attention in a recurrent/causal fashion (e.g., summing KᵀV over tokens and then multiplying by Q) is already known from linear attention methods (Katharopoulos et al., 2020; Shen et al., 2021) and from prior spiking transformers that use similar associative tricks (SDT-V2, SDT-V3). The paper’s main addition is the local receptive field via dilated convolutions, which is a straightforward architectural modification. The “neuronal dynamics” framing does not introduce new computation; it simply reinterprets existing linear-attention operations in biological terms.

2. **Theoretical analysis is insufficiently rigorous**. Theorems 1 and 2 are stated with heavy notational simplifications and rely on assumptions (e.g., exponential decay for VSA, piecewise linear for SSA) that are not justified or validated. The proof is deferred to the appendix (not fully visible), and the main text does not provide enough detail to assess the soundness of the claims. The entropy inequality in Theorem 2 appears to be a direct consequence of the convexity of entropy and the mixing of distributions, which is standard and does not require a theorem. The added value of these theoretical statements is therefore limited.

3. **Practical memory reduction is not empirically validated**. The paper claims “49.4% memory reduction” for Spikformer-8-512, but this number appears only in the text with no supporting table or figure showing actual peak memory usage, latency, or energy consumption. The bubble chart (Fig. 5b) shows accuracy vs. parameters, not memory. Without concrete measurements, the memory advantage remains a theoretical claim. Given that the paper’s second major contribution is memory reduction, this omission weakens the experimental evidence.

### Minor

- The LRF module adds 3×3 dilated depthwise convolutions; the ablation shows that larger kernel sets improve accuracy, but the benefit could partially come from increased model capacity rather than genuine locality. A simple control—adding the same parameter count via extra linear layers to SSA without locality bias—would strengthen the claim.
- The paper only evaluates on classification and segmentation. Many prior spiking transformer papers also test on object detection (e.g., Spikformer, QKFormer). Including a detection benchmark would make the evaluation more comprehensive.
- The writing contains several unclear or ambiguous equations (e.g., Eq. 8 uses “V^{jk}” without definition; Eq. 15 introduces Fourier transforms without explanation of why they are used). The connection between the mechanistic neuron model (Eq. 13) and the actual computation is not explicitly shown.

### Trivial

- Several citations are incomplete (e.g., “Wang et al.” without year or venue in the introduction).

## Nice-to-Haves

- Provide an ablation directly comparing LRF-SSA with a simple baseline that increases the number of parameters in the Q/K/V projections by the same count as the LRF convs, to isolate the effect of locality.
- Report actual peak GPU memory usage (in MB/GB) during inference for at least one model scale.
- Include a runtime measurement (e.g., throughput or latency) to show that the O(Nd²) → O(kd) complexity translates to faster inference.

## Novel Insights

None beyond the paper’s own contributions. The observation that spiking transformers lack locality bias is already partially known from related work on SNN attention mechanisms (e.g., Spike-Driven-V2 discusses softmax removal). The use of a recurrent kernel sum to avoid storing large matrices is also standard in the linear attention literature.

## Suggestions

- **Strengthen the theoretical section**: Either provide more rigorous proofs with clear assumptions or remove the theorems and treat the locality argument as empirical.
- **Provide actual memory measurements**: For at least one model (e.g., Spikformer-8-512), report the peak memory consumption during forward inference for SSA, LRF-SSA, and LRF-Dyn.
- **Control for parameter count**: Add an experiment where the LRF convs are replaced by additional learnable parameters in the QKV projections (with same parameter count) to verify that the performance gain comes from the local inductive bias rather than extra capacity.

## Score and Decision

The paper addresses a relevant problem and demonstrates consistent, albeit modest, improvements across multiple spiking transformer architectures. However, the core technical contributions—adding local convolutions to SSA and reusing a recurrent linear-attention formulation—are incremental and largely known from prior work. The theoretical analysis is weak, and the central claim of memory reduction lacks direct empirical support. These factors limit the paper’s impact and novelty for a top venue like ICLR.

**Score**: 4.5  
**Decision**: Reject  

MY FINAL SCORE: <score>4.5</score>
MY FINAL DECISION: <decision>Reject</decision>