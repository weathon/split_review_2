## Summary
# Final Review Report

## Summary

This paper proposes GenCoGS, a 3D Gaussian Splatting (3DGS) based method for few-shot novel view synthesis (NVS) that addresses the problem of incomplete scene representation under sparse training views. The key idea is to use generative completion in two stages: (1) **GCGI** — a point cloud completion strategy that generates complementary 3D points via a Transformer-based generator and filters outliers using a kd-tree-based mask, providing denser initialization for Gaussians; and (2) **GCGO** — a pseudo-view completion strategy that uses a perturbed camera trajectory with an image-to-video (I2V) diffusion model to synthesize pseudo views covering unobserved regions, with a generative consistency loss to mitigate hallucination.

Experiments on LLFF, DTU, and Shiny datasets under 3/6/9-view settings show consistent improvements over existing 3DGS-based few-shot NVS methods, with gains of up to 2.40 dB PSNR on DTU 3-view compared to the second-best 3DGS baseline. The method integrates two complementary completion strategies whose individual contributions are validated through ablation studies.

**Overall assessment:** The paper addresses a well-motivated problem (scene completion under sparse views) and proposes a technically reasonable combination of generative components. However, several issues reduce confidence: missing statistical variance reporting, incomplete specification of the diffusion model component, a mathematical inconsistency in Eq (7), and overclaimed contribution statements. The novelty is partially overlapping with diffusion-guided 3DGS/NVS methods (e.g., ViewCrafter, CAT3D, ReconFusion); the main differentiator is the dual focus on both initialization and optimization completion. A major revision with strengthened experimental rigor and more precise claims is required before acceptance.

## Strengths
1. **Well-motivated problem formulation.** The paper correctly identifies that existing 3DGS-based few-shot NVS methods are fundamentally limited by their reliance on observed information only, and that scene completion (both at initialization and optimization stages) is a key missing capability. The decomposition into initialization completion (point cloud) and optimization completion (pseudo views) is logical and comprehensive.

2. **Effective generate-and-filter paradigm for point clouds.** The GCGI strategy's two-stage design — generating complementary points via a Transformer-based CPG module, then filtering outliers via a kd-tree-based CPF module — is a practical and principled approach to handling generative hallucination in point cloud completion. The ablation results (Table 6) confirm that both modules contribute positively, and the robustness test with degraded input (1/4 sampling) demonstrates strong generalization.

3. **Strong empirical results across multiple benchmarks.** On all three datasets (LLFF, DTU, Shiny) and under all tested few-shot settings (3/6/9 views), GenCoGS consistently outperforms existing 3DGS-based methods by non-trivial margins (e.g., 2.40 dB PSNR on DTU 3-view). The qualitative visualizations (Figures 5, 6, 7) show visibly cleaner reconstructions with reduced floating artifacts, supporting the claimed improvement in scene completion.

4. **Acknowledgment of the hallucination-exploration trade-off.** The paper honestly identifies and discusses the "see-saw effect" between generative model hallucination and unobserved region exploration (Section 4.3), which is a genuine challenge for diffusion-guided NVS. This self-awareness is scientifically valuable even though the analysis could be deepened.

5. **Comprehensive ablation studies.** Tables 4-6 provide a clear decomposition of the contribution of each component (GCGI, GCGO, CPG, CPF, perturbed trajectory, consistency loss), allowing reviewers to assess the marginal value of each design choice. The ablation on degraded input quality (1/4 sampling) is particularly informative.

## Weaknesses
### W1 (Major) — Missing statistical rigor in all experimental results
All quantitative results (Tables 1–6) are reported as single-run point estimates without variance, confidence intervals, or significance tests. Given that the improvement margins are sometimes small (e.g., PSNR +0.47 dB on LLFF 9-view; SSIM +0.003 on LLFF 9-view), readers cannot assess whether these gains are statistically reliable. The paper's central claim of "superiority" requires evidence that the improvements are consistent across random seeds rather than driven by a favorable training run. **Impact:** This is the most critical weakness because it undermines the reliability of all quantitative conclusions. **Action:** Report mean ± std over ≥3 seeds and add a paired significance test against the strongest baseline.

### W2 (Major) — I2V diffusion model specification is critically incomplete
The GCGO strategy relies on an I2V diffusion model (Eq 10) but the manuscript provides insufficient implementation details: the exact pretrained model variant is not named, it is unclear whether fine-tuning is performed, key sampling hyperparameters (steps, guidance scale, seed) are omitted, and the frequency of diffusion inference during optimization (every iteration vs. periodic) is not specified. The paper defers to an Appendix that is not available in the current submission. **Impact:** This prevents reproducibility and independent verification of a core component. **Action:** Add a dedicated implementation subsection specifying model identity, fine-tuning status, sampling parameters, and compute cost.

### W3 (Major) — Overclaimed contribution statements
The three bullet-point contributions (Introduction) are vague and use promotional language ("first time," "inspired by human imagination"). The "first time" claim for point cloud completion in Gaussian initialization is not adequately scoped — prior work on point cloud completion for 3D reconstruction (e.g., PCN, point cloud transformers) exists, and the paper does not clearly delineate what is novel beyond using an existing CPG module design (DGCNN + Transformer + FoldingNet). **Impact:** Without precise, verifiable contribution claims, the paper may be perceived as an engineering combination of existing components. **Action:** Replace "first time" with specific technical differentiation; describe concrete technical challenges overcome (e.g., how kd-tree filtering handles the few-shot hallucination problem specifically).

### W4 (Major) — The see-saw effect is insufficiently analyzed
While the paper honestly acknowledges the trade-off between hallucination and exploration in GCGO, the analysis is limited to one qualitative comparison (Figure 8 with A=2.0 vs A=3.0). Without a quantitative parameter sweep, the claimed "balanced trade-off" at A=2.0 is not empirically justified. Furthermore, the paper does not discuss boundary conditions under which GCGO's generative completion becomes unreliable. **Impact:** The core benefit of GCGO may be limited to specific scene types where the diffusion model hallucinates minimally, which is not disclosed. **Action:** Add a quantitative sweep of A and f in the appendix, and discuss when the see-saw effect is prohibitive.

### W5 (Major) — GCGO alone shows no LPIPS improvement
In Table 4, the "+GCGO" row shows LPIPS = 0.184 (identical to baseline), while "+GCGI" alone achieves LPIPS = 0.168. This means GCGO alone provides no perceptual quality benefit; the full method's LPIPS improvement (0.164) is primarily driven by GCGI. This non-monotonic behavior is not discussed, which is misleading. **Impact:** Overstates GCGO's contribution to perceptual quality. **Action:** Add a discussion explicitly acknowledging this finding; hypothesize why GCGO alone does not improve LPIPS.

### W6 (Major) — Novelty verification is unresolved (deferred)
Due to the Retrieval-Disabled Mode in this review run, external literature verification could not be performed. The paper's novelty claims relative to ViewCrafter, CAT3D, ReconFusion, and other diffusion-guided NVS methods cannot be independently assessed. The paper's key differentiator — dual focus on initialization *and* optimization completion — appears incremental rather than paradigmatic, but this cannot be confirmed without systematic literature comparison. **Impact:** Novelty judgment is deferred; the authors should proactively discuss the differences from the most closely related diffusion-guided 3DGS methods in more detail. **Action:** In revision, add a dedicated comparison table showing side-by-side qualitative and quantitative differences with ViewCrafter, CAT3D, ReconFusion, and IPSM across multiple dimensions (initialization strategy, trajectory design, hallucination mitigation, computational cost).

### W7 (Minor) — Mathematical inconsistency in Eq (7)
The formula for $\mu(\mathbf{P}_0)$ sums $\sum_{i=1}^{n-1}$ but uses denominator $n(n-1)$, creating an index range mismatch. This suggests the formula was not carefully verified. **Action:** Correct to $\sum_{i=1}^n$ for consistency, or reformulate as the standard mean pairwise distance.

### W8 (Minor) — Missing limitation discussion
The conclusion does not discuss failure cases, computational overhead of the diffusion model, or generalization boundaries. **Action:** Add a dedicated limitations paragraph covering when the method fails, computational cost, and dataset scope.

## Score
**Final Score: 6/10**

**Rationale:** The paper presents a well-motivated approach to an important problem (few-shot NVS) with reasonable technical design and consistent empirical improvements across three benchmarks. The two-stage completion strategy (GCGI + GCGO) is logically structured and the ablation studies provide useful validation.

However, the score is constrained by the following factors, prioritized by severity:

1. **Missing statistical variance (W1):** All results lack error bars and significance tests. Given that several improvements are small (e.g., +0.003 SSIM on LLFF 9-view), the claimed "superiority" cannot be verified as statistically reliable. This directly impacts the validity of the paper's core claim.

2. **Incomplete specification of a core component (W2):** The I2V diffusion model, central to GCGO, is critically under-described, preventing reproducibility. This is a serious methodological gap.

3. **Overclaimed contributions (W3):** The bullet-point contributions use "first time" language without clear technical differentiation, and the paper's novelty relative to existing diffusion-guided NVS methods is not convincingly demonstrated.

4. **Novelty cannot be fully assessed (W6):** Due to the retrieval-disabled review mode, external literature verification was not possible. The paper's differentiation from ViewCrafter, CAT3D, ReconFusion, and similar methods requires careful manual assessment by authors and reviewers.

A score of 6/10 reflects a methodologically solid paper with promising results, but with critical gaps in statistical rigor and reproducibility that need to be addressed before the claims can be fully trusted. With a major revision addressing W1–W6, the paper has the potential to become a strong contribution to the few-shot NVS literature.