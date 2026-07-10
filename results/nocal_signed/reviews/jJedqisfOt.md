Now I'll write the final consolidated review.

## Summary

This paper proposes two modifications to Spiking Self-Attention (SSA) in SNN-based Transformers: LRF-SSA, which adds local receptive fields via dilated depthwise convolutions parallel to the global SSA computation, and LRF-Dyn, which reformulates the attention computation through recurrent neuronal dynamics to avoid explicit storage of attention matrices. The methods are evaluated across three Spiking Transformer backbones (Spikformer, QKFormer, SDT-V3) on ImageNet-1K and ADE20K segmentation, showing consistent but modest accuracy improvements (0.44–1.24%) while claiming reduced memory.

## Strengths

- **Well-motivated problem.** The paper identifies two genuine limitations of Spiking Transformers (the performance gap from SSA's loss of locality when softmax is removed, and the memory overhead of storing attention matrices) and supports the locality hypothesis with empirical evidence (Fig. 2, showing VSA vs SSA attention distributions). This analysis provides a concrete basis for the proposed approach.

- **Clean experiment design.** The method is evaluated across three distinct Spiking Transformer backbones (Spikformer, QKFormer, SDT-V3) on ImageNet-1K and on ADE20K segmentation. Consistent positive accuracy gains (+0.44% to +1.24% on ImageNet) across architectures provide substantially stronger evidence than a single-baseline improvement would. The ablation on CIFAR-100 (Table 3) further supports that the LRF module contributes to the gains.

- **Theoretical grounding attempt.** Theorems 1 and 2 provide a formal framework connecting the proposed architecture to lower-entropy, more localized attention distributions — a step beyond purely empirical method papers in this area.

## Weaknesses

### Major

- **Unsubstantiated memory reduction claim.** The paper claims a 49.4% memory reduction under Spikformer-8-512 (line 259) as a single sentence with no supporting measurements — no absolute memory numbers (MB/GB), no breakdown of where the savings come from, and no comparison of total model memory vs. attention-matrix-only memory. The "SR" column in Table 1 reports theoretical complexity classes (O(d²) vs O(kd)), but this is not a substitute for empirical memory measurements. Since memory reduction is one of the paper's two central claims, this lack of empirical support is a significant omission.

- **Causal reformulation introduced without justification for vision tasks.** LRF-Dyn (Eq. 11) changes the attention from bidirectional (summing over all tokens j=1..N in Eq. 8) to causal (summing over j=1..n-1). For image data, the 1D token ordering is arbitrary, and there is no motivation for preventing later tokens from attending to earlier ones. The paper mentions causal inference in passing (line 142) but never discusses the trade-offs or justifies why this architectural shift is acceptable for image classification. While Table 3 shows LRF-Dyn recovers most of the performance gap (77.78% vs Causd SSA's 74.30%, both w/o LRF), Table 1 nevertheless compares LRF-Dyn against bidirectional baselines without acknowledging this architectural difference.

- **LRF-Dyn formulation is underspecified with notation inconsistencies.** Several issues prevent a clear understanding of what LRF-Dyn actually computes: (a) Eq. 13 shows a tridiagonal matrix with dual labeling (𝒜 labeled as 𝒞 via underbrace) and inconsistent dimensionality (𝒜 is stated as ∈ ℝ^d on line 152 but the matrix shown is of size n×n); (b) Fourier transforms appear without motivation in Eq. 15, and the convolution kernel 𝒦(t) is defined as "Γ C Σ_{m=1}^{n-m} 𝒜," which is syntactically malformed (upper bound depends on m); (c) the relationship between k (number of dendrites, set to 8), d (feature dimension), and N (token count) is never clarified.

- **Disconnect between theoretical framing and implementation.** Theorem 1 characterizes LRF-SSA as interpolating attention weights (α = (1−λ)·VSA + λ·r), but Eq. 8 implements SSA plus a separate convolutional path on V (additive outputs, not interpolated weights). The theorems as stated describe a different computational mechanism than what is actually implemented.

### Minor

- **Number of simulation timesteps T not reported for ImageNet experiments.** T is reported for segmentation (Table 2, T=4) but omitted for the main ImageNet-1K classification results (Table 1). Since SNN performance is sensitive to T, this omission impairs reproducibility.

- **"Causd SSA" baseline incompletely specified.** The ablation (Table 3) compares LRF-Dyn against a "Causd SSA" model (74.30% w/o LRF) but does not specify whether this is Eq. 7 with a causal mask or Eq. 11 without the full neuronal dynamics formulation. The paper only labels it as "causal SSA model" (line 265).

### Trivial

None.

## Nice-to-Haves

- Provide actual memory measurements (peak GPU memory in MB) for at least one configuration with a breakdown by component.
- Acknowledge the causal shift explicitly as a design choice and discuss its trade-offs (information flow limitations, sequential processing latency).
- Add a controlled ImageNet ablation that separates the contribution of LRF (locality) from the contribution of the recurrent formulation, similar to the CIFAR-100 ablation in Table 3.
- Clarify the relationship between k, d, and N in LRF-Dyn.

## Removed Points

These points from the input review were removed:

1. **Claim that memory savings come "largely from the causal shift, not from neuronal dynamics"** — REMOVED because the paper's own data (Table 3: LRF-Dyn w/o LRF 77.78% vs Causd SSA 74.30%) shows the neuronal dynamics contribute substantially beyond mere causal masking.
2. **Ambiguity about N² vs d² baseline** — REMOVED because the paper explicitly mentions both versions and explains the O(d²) origin (lines 20, 100).
3. **Request for ANN attention baselines (Performer, Nyströmformer)** — REMOVED as scope creep; the paper is about SNN-specific methods.
4. **Missing variance/statistical significance** — REMOVED because single-run reports are standard practice in this subfield for large-scale ImageNet experiments.
5. **Biological motivation not operationalized** — REMOVED because the multi-dendrite formulation is clearly inspired by the biological concepts mentioned.
6. **Formatting nitpicks** — REMOVED per formatting artifact rules.

## Novel Insights

The most interesting observation from the reviews is the disconnect between what the paper claims theoretically (interpolated attention weights with controlled entropy) and what it actually implements (additive convolutional bypass + global SSA). The empirical success of LRF-Dyn despite (or perhaps because of) this gap suggests that the locality benefits may come primarily from the convolutional pathway rather than from modifying the attention distribution itself. This raises the question of whether simpler architectural additions (e.g., a ConvNeXt-style convolutional stem) could achieve similar gains with less complexity.

## Suggestions

1. Provide absolute memory measurements (GPU memory in MB) to support the 49.4% reduction claim.
2. Either motivate the causal restriction for vision tasks or remove it and present LRF-Dyn as a bidirectional recurrent method.
3. Resolve the notation issues in Section 5.2: fix inconsistent dimensionality, clarify the summation in the kernel definition, explain the role of Fourier transforms.
4. Report T for ImageNet experiments and fully specify the Causd SSA baseline.
5. Add an ImageNet-scale ablation that isolates the LRF contribution from the recurrent formulation contribution.

## Score and Decision

**Score: 5.0**

**Decision: Reject**

The paper identifies a real problem and presents consistent empirical improvements across multiple backbones, which is genuine evidence of progress. However, the paper's central memory-efficiency claim is supported only by a theoretical complexity class and an unverifiable single percentage — no actual measurements are provided. The LRF-Dyn formulation is underspecified to the point that a reviewer cannot determine exactly what computation is performed. Additionally, the causal reformulation introduces an architectural shift (bidirectional → causal) that is neither motivated for vision tasks nor properly acknowledged when comparing against bidirectional baselines. These issues collectively prevent acceptance in the current form, though a revision with proper supporting measurements, clarified notation, and honest framing of the causal trade-offs could make a genuine contribution.

MY FINAL SCORE: <score>5.0</score>
MY FINAL DECISION: <decision>Reject</decision>