## Summary

This paper identifies two limitations of Spiking Self-Attention (SSA) in Spiking Transformers: weak local modeling capacity and high memory overhead during inference. To address these, the authors propose LRF-SSA, which inserts a local receptive field module (dilated depthwise convolutions) into SSA, and LRF-Dyn, which reformulates the attention computation via a recurrent neural-dynamics approximation to avoid storing explicit attention matrices. Experiments on ImageNet classification and ADE20K segmentation show consistent but modest accuracy improvements across several SSN backbone architectures, along with reduced memory complexity claims.

## Strengths

- **Problem identification is clear and well-motivated** – Figures 1 and 2 convincingly illustrate that SSA lacks the locality and entropy concentration of VSA, and that explicit attention-matrix storage is a practical bottleneck.
- **Consistent experimental gains** – The method improves accuracy on ImageNet (e.g., +1.24% on Spikformer-8-512, +0.48% on QKFormer-10-512) across multiple backbones, with modest parameter overhead.
- **Memory reduction is demonstrated** – The LRF-Dyn variant replaces the O(d²) memory of KV aggregation with O(kd), and a bubble chart (Fig. 5b) claims a 49.4% memory reduction while improving accuracy.
- **Ablation and visualization support the core ideas** – The effective receptive field visualizations (Fig. 5a) and the ablation on CIFAR-100 (Table 3) show that increasing the LRF kernel size correlates with better performance.

## Weaknesses

### Fatal
None.

### Major

1. **The theoretical contributions (Theorems 1 and 2) are not well-supported.**  
   The theorems rely on assumed forms for VSA and SSA attention distributions, and the proofs are relegated to the appendix (which is not accessible in the review). The entropy ordering claim (Eq. 10) appears to follow directly from properties of the convex combination and is essentially a restatement of the construction rather than a non-trivial insight. The paper does not provide rigorous justification that LRF-SSA *provably* recovers the locality of VSA.

2. **The neural-dynamics framing is largely superficial.**  
   The connection between the recurrent formulation in Eq. 12 and biological neuron dynamics is heuristic. The computation is simply a causal cumulative product of K and V (a standard technique in linear attention) augmented with a local convolution branch. Calling this “charge–fire–reset dynamics” adds little explanatory power and may even mislead readers about the biological plausibility of the method. The Fourier transform in Eq. 15 is introduced without motivation or necessity.

3. **Incomplete memory evaluation.**  
   The claim of 49.4% memory reduction is based only on computational complexity (O(d²) → O(kd)) and a single bubble chart. Actual wall‑clock memory consumption (e.g., in MB) for a specific hardware setting is never reported. Without such measurements, it is unclear whether the theoretical reduction translates to a meaningful practical benefit, especially given that the LRF branch itself introduces additional storage for its kernels and intermediate activations.

4. **Limited novelty relative to existing efficient-attention literature.**  
   The core ideas—adding local depthwise convolutions to bias attention and using a recurrent form of linear attention (KV accumulation) to reduce memory—are well known in both the ANN and SNN communities. The paper does not compare against efficient-attention baselines (e.g., Performer, Linear Transformer, or other softmax‑free attention) adapted to SNNs, making it difficult to assess whether the claimed gains are attributable to the specific LRF‑Dyn formulation or simply to standard linear attention tricks.

5. **Evaluation scope is narrow.**  
   Only two tasks are considered: ImageNet classification and ADE20K segmentation. No experiments on object detection, neuromorphic (DVS) datasets, or long‑sequence tasks are provided. This limits the generality of the memory and performance claims.

### Minor

- The notation in Eq. 13 is unclear: the dimensions of \(\mathcal{A}\) do not match a simple decay matrix, and the coupling terms \(\beta\) are not explained.
- The ablation in Table 3 is only on CIFAR‑100 with a small model; more extensive ablations on ImageNet would strengthen the conclusions.
- The paper occasionally uses “memory overhead” and “storage complexity” interchangeably without distinguishing between on‑chip SRAM, off‑chip DRAM, or theoretical flops.

### Trivial

- Figure captions are overly repetitive (the same caption appears multiple times for each figure).

## Nice-to-Haves

- Provide actual peak memory measurements (in MB) for a standard GPU/neuromorphic setup.
- Compare against other efficient‑attention mechanisms (e.g., Performer, Nyströmformer) binarized or adapted for SNNs.
- Include experiments on event‑based (DVS) object classification or detection to showcase the method’s value for edge vision.

## Novel Insights

None beyond the paper’s own contributions.

## Suggestions

- Clarify the theoretical analysis by explicitly stating the assumptions behind Theorems 1–2 and including full proofs in the main paper (or a clearly marked appendix).
- Replace the neural‑dynamics language with a more standard description of the recurrent linear‑attention approximation, and justify why this particular formulation is advantageous over existing alternatives.
- Add a table reporting empirical memory usage (e.g., inference‑time GPU memory) for both the base model and the proposed variants.
- Extend the evaluation to at least one additional task (e.g., object detection on COCO or classification on DVS128 Gesture).

## Score and Decision

The paper addresses a real and practical issue in SNN transformers, and the experiments show consistent but incremental improvements. However, the theoretical framing is weak, the neural‑dynamics motivation seems overstated, the memory evaluation lacks concrete numbers, and the novelty is limited given the mature literature on efficient attention. These shortcomings prevent the paper from making a strong contribution to ICLR.

MY FINAL SCORE: <score>4</score>
MY FINAL DECISION: Reject