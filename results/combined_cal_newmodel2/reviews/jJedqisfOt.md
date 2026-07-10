## Summary

This paper addresses two limitations of Spiking Self-Attention (SSA) in Spiking Transformers: poor local modeling and high memory overhead. It proposes (1) LRF-SSA, which adds dilated depthwise convolutions to SSA to strengthen local attention, and (2) LRF-Dyn, a reformulation that replaces explicit attention-matrix storage with a recurrent state update inspired by neuronal dynamics. Experiments across ImageNet classification (Spikformer, QKFormer, SDT-V3) and ADE20K segmentation show consistent accuracy/mIoU improvements of +0.4% to +2.7%.

## Strengths

- **Clear problem diagnosis with supporting empirical evidence.** Section 4 provides concrete quantitative evidence that SSA produces nearly uniform attention distributions (only 20.31% of mass within Manhattan distance 5 vs. 76.68% for VSA) and higher entropy (H=0.5637 vs. H=0.1777), cleanly isolating the specific problem the method aims to solve. **[favorability=8.99]**

- **Consistent, modest improvements across multiple architectures.** Table 1 shows positive accuracy gains for every architecture tested (Spikformer, QKFormer, SDT-V3) at every scale, with LRF-SSA improvements of +0.44% to +1.24%. The consistency across three different backbone families provides credible evidence that the LRF addition provides genuine benefit. **[favorability=12.04]**

- **Segmentation results are meaningfully larger than classification gains.** The +2.2 to +2.7 mIoU improvements on ADE20K (Table 2) substantially exceed the classification gains, suggesting the local bias is particularly beneficial for dense prediction tasks — a genuine finding worth reporting. **[favorability=10.49]**

## Weaknesses

### Major

- **The LRF-Dyn method description is unclear and internally inconsistent.** The paper presents three different formulations (Eq. 8→Eq. 11→Eq. 12→Eq. 15) without a coherent narrative connecting them. Equation 12 is a simple linear recurrent state update (X_n[t] = A⊙X_{n-1}[t] + Γ·Token_n[t]) with no spiking threshold or reset mechanism, yet the paper claims it "establishes an approximate correspondence between self-attention aggregation and the charge–fire–reset dynamics of spiking neurons." Additionally, Eq. 15 introduces Fourier transforms with no motivation or connection to the preceding dynamics, and the kernel definition "Γ C Σ_{m=1}^{n-m} A" (line 170) contains a nonsensical upper bound (n-m). A reader cannot determine which equations describe the actual implementation, fundamentally undermining reproducibility. **[favorability=-1.52]**

- **The switch from bidirectional to causal attention (Eq. 8→Eq. 11) is not justified for vision tasks.** The paper mentions "causal inference" once (line 142) with no explanation of why a causal formulation (summing from j=1 to n-1 rather than over all N tokens) is appropriate for image applications where attention is universally bidirectional. The cited works (Yang et al., 2023; Zhang et al., 2024b; Shen et al., 2021) are about linear attention mechanisms, not about converting bidirectional to causal attention. **[favorability=-0.80]**

- **The 49.4% memory reduction claim (line 259) is stated without any concrete measurement protocol or raw memory consumption numbers (MB/GB).** Only asymptotic complexity classes (O(d²) vs O(kd) vs O(Nd)) are provided across tables. For a paper whose second stated contribution is memory efficiency, the absence of measured inference memory is a notable omission that prevents verification of a central claim. **[favorability=-0.94]**

### Minor

- **Accuracy numbers are reported as point estimates with no indication of variance or statistical significance across runs.** This makes it difficult to assess whether the reported improvements (many under 1%) are statistically meaningful. **[favorability=0.52]**

- **The attribution of SSA's uniform attention distribution entirely to "the removal of softmax" (Section 4) oversimplifies the differences between VSA and SSA.** SSA also differs in its use of spiking neurons (which binarize activations), its lack of scaling, and its use of 1×1 convolutions rather than learned projections. These additional differences may also contribute to the observed attention distribution mismatch. **[favorability=3.48]**

- **The ablation study (Table 3) does not systematically explore LRF design choices.** The paper uses dilated convolutions with rates 3 and 5 and 3×3 kernels, but does not ablate different kernel sizes, alternative dilation rates, or the number of convolution kernels — only the dilation bound (Ω) is varied. **[favorability=2.64]**

- **Variable "n" is used for both token position and the number of dendrites (line 156: "n is set as 8"), creating confusion.** The paper would benefit from distinct notation. **[favorability=-0.26]**

### Trivial

None.

## Nice-to-Haves

- Add a table with measured memory consumption (in MB) across model configurations to support the claimed 49.4% reduction.
- Provide variance statistics (e.g., mean ± std over 3+ runs) for main results.
- Consider ablating different kernel sizes, dilation rates, and numbers of convolution kernels in the LRF module.
- Either remove the unsubstantiated biological claims about "charge–fire–reset dynamics" or explain how the actual equations map to LIF dynamics.

## Removed Points

These points are flagged to be removed; treat them with caution:

- **The claim that Table 3 results are "not possible" under the described mechanism (Critical Issue #1 in the harsh review):** The reviewer asserts that LRF-Dyn w/o LRF (77.78%) being nearly identical to bidirectional SSA (77.86%) contradicts Eq. 11's causal formulation and that the Causal SSA baseline (74.30%) proves this. However, LRF-Dyn is defined by Eq. 12 (recurrent state update), not Eq. 11. LRF-Dyn w/o LRF is a fundamentally different mechanism from applying a causal mask to standard SSA. The performance difference between LRF-Dyn w/o LRF and Causal SSA is therefore expected and not contradictory. *Reason removed: Factually inaccurate — misattributes LRF-Dyn's mechanism to Eq. 11 when it is defined by Eq. 12.*

- **Missing appendix/proofs references and missing related works:** Removed per guidelines (appendix stripped by parser; reviewer cannot confirm existence of missing related works without external sources). *Reason removed: Hard rule.*

- **Pure formatting/style nitpicks:** Removed per guidelines. *Reason removed: Hard rule.*

- **Missing energy/FLOPs estimates:** While the paper mentions energy efficiency contextually, the core claimed contributions are about performance and memory efficiency. *Reason removed: Scope creep — paper's stated contributions focus on performance and memory, not energy measurement.*

## Novel Insights

The most useful perspective from the reviews is the distinction between the two contributions. The LRF-SSA component (adding local convolutions to SSA) is well-motivated, clearly described, and empirically validated across multiple architectures. The LRF-Dyn component has genuine presentation and justification issues — its mathematical formulation shifts between three incompatible descriptions (causal attention, linear recurrence, Fourier-domain convolution), the biological connection is overstated, and the memory claims lack quantitative backing. However, the LRF-Dyn experimental results are internally consistent and do not contradict the paper's other claims; the problem is with the description, not the results. A substantially revised paper that clarifies the LRF-Dyn mechanism (or drops it to focus on LRF-SSA) and adds measured memory numbers would be significantly stronger.

## Suggestions

1. Substantially revise the LRF-Dyn description: provide a single, self-contained formulation, clearly explain whether the computation is causal or bidirectional, remove or properly motivate the Fourier transform variant, and fix the nonsensical kernel bound in Eq. 15.
2. Add a table with measured memory consumption (in MB) across model configurations to substantiate the claimed 49.4% reduction.
3. Provide variance statistics (e.g., mean ± std over 3+ runs) for all main results.
4. Expand the ablation study to explore different kernel sizes, dilation rates, and numbers of convolution kernels in the LRF module.

## Calibration Anchors

### Round 1 (Bracketing)

| Anchor | Path | Avg Score | Topic Similarity | How It Compares |
|--------|------|-----------|-----------------|-----------------|
| Spiking Vision Transformer with Saccadic Attention | qzZsz6MuEq.md | 6.60 | Very high | Stronger presentation, clearer biological motivation, well-justified method. Current paper has more damaging weaknesses (negatives vs all positives). |
| Spike-driven Transformer V2 | 1SIBN5Xyw7.md | 5.67 | Very high | Clearer presentation, seen as incremental. Current paper has comparable weakness severity but an unclear secondary method. |
| DISTA: Denoising Spiking Transformer | mjDROBU93g.md | 4.50 | High | Novelty weakness at -3.75, lacks ImageNet results. Current paper has ImageNet + segmentation results but more presentation issues. |
| PRF: Parallel Resonate and Fire Neuron | OujTnpmAZG.md | 5.50 | Moderate | Weaknesses at -2.52, -0.99. Current paper has similar weakness patterns. |
| Spatio-Temporal Approximation (SNN Conversion) | XrunSYwoLr.md | 7.00 | Moderate | Strong theoretical guarantees, clear contribution. Current paper has weaker method clarity. |

### Round 2 (Narrowing)

Queries targeting the 4.5–6.5 bracket confirmed that topically similar papers with clarity issues and missing measurements cluster around 4.5–5.7, while cleaner papers with better presentation (SVSA at 6.60) score higher.

### Bracket and Final Score

**Round-1 bracket:** 4.5 (DISTA) to 6.6 (SVSA). The current paper lacks the presentation clarity of SVSA (6.60) and its weaknesses are more damaging (negative favorability vs. all-positive for SVSA). It resembles SDT-V2 (5.67) in weakness severity but has a less clear method section. It is clearly above DISTA (4.50) due to ImageNet and segmentation results, and the core LRF-SSA contribution is demonstrably valid.

**Final score:** 5.0. The paper has a genuinely useful core contribution (LRF-SSA) with consistent experimental support across multiple architectures and tasks. However, the LRF-Dyn description is confusing (three incompatible formulations, overstated biological claims, a nonsensical equation bound) and the memory efficiency claims lack concrete measurements. These presentation issues significantly undermine confidence in the secondary contribution but do not invalidate the primary one.

### Score and Decision

MY FINAL SCORE: <score>5.0</score>
MY FINAL DECISION: <decision>Reject</decision>