## Summary

This paper proposes LRF-Dyn for spiking transformers, aiming to address two limitations of Spiking Self-Attention (SSA): lack of local modeling and high memory overhead. The approach has two components: (1) LRF-SSA, which adds dilated depth-wise convolutions in parallel with SSA to strengthen locality, and (2) LRF-Dyn, which reformulates attention via neuronal charge-fire-reset dynamics to eliminate explicit attention matrix storage. Experiments on ImageNet classification and ADE20K segmentation across Spikformer, QKFormer, and SDT-V3 show consistent accuracy improvements.

## Strengths

- **Consistent accuracy improvements across multiple SNN architectures.** Tables 1 and 2 show Top-1 accuracy gains of +0.44% to +1.24% on ImageNet across three architectures (Spikformer, QKFormer, SDT-V3) at comparable parameter counts, with no degradation. The gains are modest but consistent.

- **Identifies a genuine limitation of SSA** — its near-uniform attention distribution — and provides empirical support via histogram analysis (Figure 2: 76.68% of VSA attention at short distances vs. 20.31% for SSA).

- **Evaluates on both classification and segmentation** (ADE20K, Table 2), demonstrating generalization beyond a single task, which is relatively rare in the SNN-transformer literature.

- **The LRF-SSA component (dilated depth-wise convolutions) is simple and plausible**, adding only ~0.2M parameters while giving consistent gains.

## Weaknesses

### Fatal
None.

### Major

1. **The LRF-Dyn mechanism is underspecified to the point of irreproducibility.** Equations 12–15 contain multiple unresolved issues that prevent independent implementation:
   - The dimensional relationship between the matrix A (Eq. 13) and the elementwise multiplication ⊙ in Eq. 12 is inconsistent — a matrix cannot be elementwise-multiplied with a vector without specified broadcasting.
   - The Fourier transform in Eq. 15 is introduced without derivation or connection to the preceding recurrent formulation.
   - The convolution kernel K(t) = ΓC Σ_{m=1}^{n-m} A has nonsensical summation bounds (the upper bound references m itself).
   - The paper states "n is set as 8" (line 156), where n was introduced as the token position index. It is unclear whether n=8 refers to the number of dendrites or tokens, and how 8 relates to N=196 patches on ImageNet.
   - The training procedure is deferred to "Chen et al., 2024" without self-contained specification.

2. **The memory reduction claim (49.4%) is unverifiable.** Line 259 states "Under the Spikformer-8-512 architecture, our method achieves a 1.13% increase in accuracy while simultaneously reducing memory usage by 49.4%," attributed to Figure 5(b). However, Figure 5(b) is a bubble chart of accuracy vs. parameter count — it does not report memory consumption on any axis. No table, figure, or text provides measured memory in MB/GB, no measurement methodology is described, and no comparison of peak or activation memory is given. Since memory reduction is one of the paper's two central claims, this absence is critical.

3. **The memory-complexity analysis conflates different SSA implementations without justification.** Section 4.2 describes SSA using the associative property (KV-first, producing a d×d matrix, O(d²) memory) and labels all baselines as O(d²) in Table 1's "SR" column. However, the original Spikformer SSA (Zhou et al., 2023b) computes QK^T first, producing an N×N attention map — O(N²) memory. For ImageNet-224 with patch size 16, N=196 (N²≈38K) while d=512 (d²≈262K), making d² ≈ 6.8× larger than N². The paper never acknowledges this distinction or justifies why d² is the relevant baseline.

### Minor

4. **The "Causal SSA" baseline in Table 3 is undefined.** The paper compares LRF-Dyn against "Causd SSA" (Table 3, line 273, likely a typo for "Causal SSA") and claims LRF-Dyn outperforms it, but never defines or cites this baseline. The only related mention is "through causal inference" (line 142) in a different context. This makes the ablation comparison uninterpretable.

5. **The theoretical analysis (Theorems 1–2) does not characterize the implemented method.** Theorem 1 models LRF-SSA attention as a convex combination of VSA (softmax) weights and LRF weights: α^{lrf-ssa} = (1-λ)α^{vsa} + λ r_{ij}. However, the actual LRF-SSA (Eq. 8) computes SSA weights (no softmax) plus a convolution term — it never computes or has access to VSA weights. The entropy ordering in Theorem 2 therefore applies to an idealized hybrid distribution, not to the algorithm as implemented.

6. **Parameter-count inconsistency in Table 2.** The LRF-SSA large model is listed as "10.0 + 1.4" M parameters, but Table 1 shows SDT-V3 large base has 18.99M and SDT-V3+LRF-SSA large has 19.25M. The 10.0M figure does not match any configuration in the paper and appears erroneous.

### Trivial

7. The ablation study (Table 3) is on CIFAR-100 (32×32 images) while main results are on ImageNet (224×224). The spatial resolution and token counts differ substantially, so the LRF effect at ImageNet scale is not directly validated by this ablation.

8. The number of timesteps T used for ImageNet experiments is not reported (T is specified for segmentation in Table 2 but absent from Table 1), which is a standard reporting requirement for SNN papers.

## Nice-to-Haves

- Actual peak GPU memory measurements (MB/GB) for baseline and LRF-Dyn at each model scale.
- A self-contained algorithmic description of LRF-Dyn (inputs, recurrent update, output generation).
- Energy consumption analysis, since the abstract describes the method as targeting "energy-efficient Spiking Transformers."
- A clearer distinction between standard SSA (QK^T first, O(N²) memory) and the associative variant (KV first, O(d²) memory).

## Removed Points

The following points from the input review are removed:

- **"No energy measurements"** — Moved to Nice-to-Haves. The paper's stated focus is on memory reduction, not energy measurement. The abstract mentions "energy-efficient" in a broader aspirational context, but the paper does not claim to measure energy consumption.
- **"No FLOPs or MACs comparison"** — Removed. Not a standard requirement for this type of paper; the focus is memory and accuracy.
- **"Standard deviations / confidence intervals not reported"** — Removed. Single-run evaluation is standard practice for large-scale ImageNet benchmarks in the SNN-transformer literature.
- **"Missing related work"** — Removed per policy (no external verification possible).
- **Pure formatting/style nitpicks** — Removed as they reflect parser artifacts, not author errors.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. Provide a clean, self-contained algorithmic description of LRF-Dyn with consistent dimensions and no Fourier transforms unless they are actually used in the forward pass.
2. Report measured memory consumption (MB/GB) rather than a single unverifiable percentage.
3. Clarify the relationship between the O(d²) and O(N²) SSA baselines and justify which is used.
4. Define the Causal SSA baseline in the main text.
5. Correct the parameter-count discrepancy in Table 2.
6. Either revise the theoretical analysis to match the actual computation (analyzing SSA + LRF, not VSA + LRF), or reframe it as conceptual motivation.

## Calibration Anchors

All anchors retrieved via RAG over the deepreview_13k_human database.

| Path | Avg Score | Round | Comparison |
|------|-----------|-------|------------|
| DISTA (mjDROBU93g) | 4.50 | R1 | Similar domain (spiking transformer), but lacked ImageNet eval; our paper has broader empirical scope but worse reproducibility for LRF-Dyn |
| Spike-driven Transformer V2 (1SIBN5Xyw7) | 5.67 | R1 | Incremental but method clear and verified; our paper has comparable breadth but weaker methodological rigor |
| Spiking ViT w/ Saccadic Attention (qzZsz6MuEq) | 6.60 | R1 | Strong analysis, clear method, verifiable claims; our paper is substantially weaker on all three dimensions |
| SPikE-SSM (4ILqqOJFkS) | 3.67 | R1 | Similar underspecification issues; our paper has stronger empirical results but similar methodological problems |
| SGHormerVQ (I0mQlersGk) | 4.75 | R1 | Core technical claim found unsupported; analogous to our unsupported memory claim |
| Spike Accumulation Forwarding (CwAY8b8i97) | 4.00 | R2 | SNN training method, similar clarity issues |
| Feature Overlapping (77plFC53J5) | 3.75 | R2 | SNN analysis paper, less complete than ours |

**Round-1 bracket:** 3.5–5.5. **Round-2 narrowing:** 3.75–4.75. **Final score:** 4.0.

The paper sits alongside DISTA (4.50) and SGHormerVQ (4.75) in the ~4–5 range: it has genuine empirical value (consistent ImageNet gains, segmentation evaluation) that raises it above the ~3.5 papers, but the LRF-Dyn component is underspecified and the memory claims are unverifiable — problems severe enough to prevent acceptance in the current form.

MY FINAL SCORE: <score>4.0</score>
MY FINAL DECISION: <decision>Reject</decision>