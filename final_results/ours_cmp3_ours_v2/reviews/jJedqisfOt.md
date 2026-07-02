## Summary

This paper identifies two limitations of Spiking Self-Attention (SSA) in Spiking Transformers — lack of locality bias and high memory overhead — and proposes LRF-Dyn to address both. The method first augments SSA with dilated depthwise convolutions (LRF-SSA) to inject locality, then reformulates the computation through a recurrent "neuronal dynamics" framework to avoid storing attention matrices. Experiments on ImageNet-1k and ADE20K show consistent accuracy improvements (0.41–1.24%) and a claimed 49.4% memory reduction.

## Strengths

- **Well-motivated problem analysis (Section 4.1, Figure 2):** The paper provides a concrete empirical demonstration that SSA (without softmax) produces a nearly uniform attention distribution (H=0.5637) while VSA concentrates 76.68% of attention at short Manhattan distances (H=0.1777). This diagnosis — that SSA's uniform attention scores harm local modeling — is genuinely informative and not, to my knowledge, made explicitly in prior Spiking Transformer papers.

- **Consistent accuracy gains across multiple architectures and tasks:** Table 1 reports positive gains on all six configurations (3 architectures × 2 sizes), and the segmentation results in Table 2 show larger improvements (2.0–2.6 mIoU points), suggesting the method is not merely exploiting noise. The improvements are especially meaningful on smaller models (e.g., +1.24% on Spikformer-8-512).

## Weaknesses

### Major

- **The method is presented through multiple formulations that are not clearly connected, and the notation shifts meaning across equations.** Eq. 8 defines LRF-SSA as global linear attention plus local convolution. Eq. 11 introduces a causal summation (j=1 to n-1) that fundamentally changes the operation from bidirectional to autoregressive — but the paper does not justify this change for image classification, where tokens have no natural sequential order. Eq. 12–13 then describes a recurrent dynamical system over "dendrites" (with n=8, not the token dimension), while Eq. 15 jumps to a Fourier-domain convolution without explaining how it relates to the preceding formulations. The paper states these are all the same method, but the core computation is obscured. This makes the contribution difficult to understand and reproduce from the description as written.

- **The ablation reveals a critical unexplained discrepancy (Table 3, Section 6.3).** "Causal SSA" (without LRF) achieves only 74.30% on CIFAR-100, while standard SSA achieves 77.86% — a 3.56% gap caused by switching to the causal formulation. Since LRF-Dyn is derived from this causal formulation, the fact that it recovers to 77.78% (w/o LRF) without explanation raises serious questions about what is actually driving performance. The paper neither acknowledges nor discusses this gap. This undermines confidence in the experimental design.

- **The central memory-reduction claim (49.4% reduction, line 259) is not supported by raw memory numbers.** No MB values, no peak activation memory comparisons, no table of memory consumption across model scales — just a single percentage in prose, referenced to a figure that only shows a bubble chart. For a paper whose second main contribution is memory reduction, this level of evidence is insufficient. Additionally, the paper claims "energy-efficient" solutions but provides no energy measurements, no MAC/AC operation counts (standard for SNN papers), and no latency/throughput numbers. The added dilated depthwise convolutions introduce operations that may offset any savings, and this is never examined.

### Minor

- **The "theorems" (Section 5.1) are not valid mathematical theorems.** Theorem 1 claims α_{ij}^{vsa} ∝ exp(−βΔ) as a general property, but softmax attention weights only decay exponentially with spatial distance under unstated assumptions about query/key distributions that are neither specified nor justified. Theorem 2 uses undefined notation (h(α_i) in Eq. 10) and asserts an entropy ordering without clarifying its assumptions. The paper would benefit from presenting these as empirical observations or analytical claims rather than theorems.

- **The memory cost of O(d²) for d=512 is described as "substantial" (Section 4.2) without contextualizing it against the total model memory footprint.** A 512×512 matrix is ~1 MB at single precision. For a 12-layer transformer with T=4 timesteps, that's ~48 MB — comparable to the model weights (29–66 MB). While the neuromorphic context may justify concern, the framing overstates the problem without comparison.

### Trivial

- Table 2's formatting makes it ambiguous whether the baseline for the "+2.6" gain is the SDT-V3 row (33.6) or a different value. The information is present but could be clearer.

## Nice-to-Haves

- A table reporting peak inference memory (in MB) for SSA vs. LRF-SSA vs. LRF-Dyn at multiple model scales, including the T timestep dimension, would substantiate the central memory-reduction claim.
- MAC/AC operation counts or a brief energy analysis would strengthen the "energy-efficient" framing, especially given the added convolutions.
- Separating the effect of causal masking from the effect of LRF convolutions in the ablation would clarify what each component contributes.
- Error bars or multi-run statistics would help calibrate how much of the smaller gains (0.41–0.48%) is attributable to the method vs. run-to-run variance.

## Removed Points

The following points from the input review were removed after verification against the paper:

- "Theoretical proofs relegated to the appendix" — The appendix is stripped by the parser; it exists in the original submission.
- "Missing related work on non-SNN efficient attention methods" — Not permitted to flag missing references.
- "LIF neuron equations have unclear causal structure" — The equations are standard LIF; the concern is a superficial presentation nitpick.
- "No statistical significance/variance on ImageNet" — Single-run reporting is standard for ImageNet benchmarks at this scale; weakened to a nice-to-have.
- "Parameter increases should be acknowledged" — The paper's claim of "almost no additional parameters" is reasonable given increases of 0.03–0.19M out of 5–66M total.
- Several speculative/framing criticisms that lacked specific anchoring to paper content.

## Novel Insights

The most valuable observations from the review are: (1) the connection between the unexplained "Causal SSA" gap (3.56% in Table 3) and the causal formulation in Eq. 11 — this concretely identifies a structural experimental flaw that the paper fails to discuss, and (2) the point that the multiple formulations (Eq. 8 → Eq. 11 → Eq. 12–13 → Eq. 15) are insufficiently connected, making it unclear what computation the experiments actually use. These are genuine insights beyond the paper's own contributions.

## Suggestions

1. **Unify the method description:** pick one coherent formulation for the computation actually used in experiments, and clearly explain how each equation relates to that core computation. Commit to whether the method is causal or bidirectional, and justify the choice for image tasks.
2. **Report actual memory numbers** (in MB) for all methods and model scales in a proper table. Also report MAC/AC operation counts.
3. **Acknowledge and explain the Causal SSA gap** in the ablation. Separate the effect of causal masking from the effect of LRF convolutions.
4. **Rephrase the "theorems"** as empirical observations or analytical claims with stated assumptions.

## Calibration Report

**Round 1 bracket:** 3.5–5.0 (between "reject" and "borderline reject").

**Anchor papers retrieved:**

| Paper | Avg Score | Round | Comparison |
|-------|-----------|-------|------------|
| Spike-TransCNN (event-based detection) | 3.50 | narrow | Rejected. Similar SNN hybrid architecture but weaker experiments (no ImageNet). Paper under review has better experimental breadth but similar method clarity issues. |
| DISTA (spatiotemporal attention) | 4.50 | narrow | Rejected. Similar unsubstantiated energy/memory claims and novelty concerns, but the paper under review has stronger experiments (ImageNet across architectures vs. CIFAR only). |
| Spike Accumulation Forwarding (SNN training) | 4.00 | narrow | Rejected. About a different SNN subproblem, but comparable score band. |
| Spiking Hybrid Attentive Mechanism | 5.00 | narrow | Rejected (controversial: scores 6,8,1,5). Similar SNN+attention paper but with weaker ablation. |
| Spike-driven Transformer V2 | 5.67 | bracket | Accepted. More incremental contribution but clearer presentation and strong ImageNet results (80.0%). Paper under review has weaker clarity but comparable experiments. |
| Spiking ViT with Saccadic Attention | 6.60 | bracket | Accepted. Very similar topic (improving spiking transformer attention). Clearer method, better-supported claims. Outperforms paper under review in presentation and evidence quality. |

The paper under review has real strengths (well-motivated problem analysis, consistent gains across architectures) but suffers from three major weaknesses: the method is specified through insufficiently connected formulations, the main memory-reduction claim lacks supporting quantitative evidence, and the ablation reveals a critical unexplained 3.56% gap. The combination of these issues places it below the accepted anchors (5.67–6.60) and in the borderline-reject range (3.5–5.0).

MY FINAL SCORE: <score>4.0</score>
MY FINAL DECISION: <decision>Reject</decision>