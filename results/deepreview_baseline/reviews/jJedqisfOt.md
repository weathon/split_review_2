## Summary

This paper identifies two key limitations in existing Spiking Transformers: a performance gap due to limited local modeling capability in Spiking Self-Attention (SSA) and high memory overhead from storing large attention matrices. To address these, the authors propose LRF-Dyn, which incorporates Local Receptive Fields (LRF) into SSA to enhance local modeling and then approximates the attention computation through neuronal membrane-potential dynamics to eliminate explicit attention matrix storage. Experiments on ImageNet classification and ADE20K segmentation demonstrate consistent performance improvements across multiple Spiking Transformer architectures while reducing inference-time memory.

## Strengths

- **Clear problem identification with empirical evidence**: The paper provides a well-motivated analysis of two concrete limitations in Spiking Transformers, supported by attention distribution visualizations (Figure 2) showing that SSA produces nearly uniform attention scores compared to VSA's localized patterns, with quantitative entropy measurements (H=0.5637 vs H=0.1777).

- **Consistent improvements across multiple architectures**: The method is evaluated on three different Spiking Transformer backbones (Spikformer, QKFormer, SDT-V3) and shows positive gains in all cases, with improvements ranging from 0.44% to 1.24% on ImageNet-1K while adding minimal parameters (<0.2M).

- **Memory reduction with maintained performance**: LRF-Dyn achieves substantial memory savings (49.4% reduction on Spikformer-8-512) while still improving accuracy over baselines, which is a practical contribution for deployment on resource-constrained devices.

## Weaknesses

### Fatal
None.

### Major

- **Theoretical claims are not well-supported**: The paper presents Theorem 1 and Theorem 2 with claims about attention weight distributions and entropy ordering, but the proofs are relegated to the appendix (which is stripped). The theorems themselves contain unclear notation (e.g., "p_i^{vsa}" is not defined, the relationship between VSA's exponential form and the claimed linear form for SSA is asserted without derivation). The theoretical contribution appears incomplete without accessible proofs.

- **Missing critical experimental details**: The paper does not report actual memory consumption numbers in MB/GB for the proposed methods versus baselines. Figure 5(b) shows a bubble chart but the axes are not clearly labeled with memory values. The claim of "49.4% memory reduction" is mentioned only once without specifying the baseline memory footprint. For a paper whose core contribution is memory reduction, this is a significant omission.

- **The LRF-Dyn formulation is unclear and potentially incomplete**: Equation 12-13 introduce a complex dynamical system with dendritic compartments, but the connection between this formulation and the actual attention computation is not clearly explained. The paper states "n is set as 8" without justification, and the relationship between the decay matrix A, the token processing, and the resulting attention-like behavior is not demonstrated. The Fourier transform formulation in Equation 15 appears abruptly without derivation from the previous equations.

### Minor

- **Limited evaluation scope**: The paper only evaluates on image classification and semantic segmentation. Given that the method claims to address fundamental limitations of SSA, evaluation on object detection or other dense prediction tasks would strengthen the claims.

- **Ablation study is on CIFAR-100 only**: The ablation experiments in Table 3 are conducted on CIFAR-100 rather than ImageNet, making it unclear whether the trends (e.g., increasing kernel count improves accuracy) transfer to larger-scale settings.

- **The biological motivation is superficial**: While the paper invokes biological visual neurons and dendritic computation, the actual method uses standard dilated convolutions and a linear dynamical system. The biological references do not meaningfully constrain or inform the technical design.

### Trivial
- Table 2 has formatting issues: the "SDT-V3 + LRF-SSA" row shows "5.1 + 1.4" parameters but the baseline SDT-V3 shows "5.1 + 1.4" as well, making the parameter comparison unclear.

## Nice-to-Haves

- Report actual memory consumption (in MB) for each configuration to make the memory reduction claim concrete and reproducible.
- Provide a clearer derivation showing how Equation 12-13 implement the attention computation from Equation 11, perhaps with a step-by-step numerical example.
- Include experiments on object detection (e.g., COCO) to demonstrate generality.

## Novel Insights

None beyond the paper's own contributions. The idea of using local convolutions to bias attention toward neighboring regions is a straightforward extension, and the connection to neuronal dynamics for memory reduction follows from known linear attention reformulations. The paper's main value is in applying these ideas specifically to the Spiking Transformer context and demonstrating empirical improvements.

## Suggestions

1. Provide actual memory consumption numbers (in MB) for all compared methods in a dedicated table, not just complexity notation.
2. Include the proofs of Theorem 1 and Theorem 2 in the main paper or provide a clear sketch of the argument.
3. Clarify the relationship between the dynamical system in Equation 12-13 and the attention computation—specifically, how the decay matrix A and the dendritic formulation produce attention-like weighting of tokens.
4. Add experiments on at least one additional task (e.g., object detection) to demonstrate generality.

## Score and Decision

The paper addresses a real problem in Spiking Transformers and provides consistent empirical improvements. However, the theoretical analysis is incomplete, the memory reduction claims lack concrete quantification, and the core methodological contribution (LRF-Dyn) is not clearly explained. The paper is solid but has significant room for improvement in clarity and experimental rigor.

MY FINAL SCORE: 5.0</score>
MY FINAL DECISION: Reject</decision>