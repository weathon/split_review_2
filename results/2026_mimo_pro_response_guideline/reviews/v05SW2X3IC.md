Now I have enough calibration data. Let me finalize my assessment and write the complete review.

Based on my calibration:

**Round 1 bracket: 5.5-7.5** — The paper clearly surpasses weak papers in the 3.5-5.5 range (e.g., "Real Time Macro-Block Rate Control" at 4.0, "Which Tasks Should Be Compressed Together" at 5.33) and sits in the range of accepted compression papers like "Language Modeling Is Compression" (6.0) and "Approaching Rate-Distortion Limits" (7.20).

**Round 2 narrowing: 6.0-7.0** — The paper has stronger theoretical novelty than the 6.0 papers but the theory-practice gap places it below the 7.20 paper. Final score: **6.5**.

---

## Summary

This paper proposes a learnable three-channel codec inspired by the Gray-Wyner Network, separating common from task-specific information across multi-task vision settings. The core contributions include: (1) bounds relating Wyner's and Gács-Körner lossy common information via interaction information (Theorem 1); (2) a reformulation of the Gray-Wyner objective for deterministic function families (Theorem 2); (3) a Lagrangian objective with parameter β controlling the transmit-receive rate tradeoff; and (4) a "Shared" architecture using a mask-based mechanism for the common channel. Experiments span a synthetic dataset, colored MNIST edge cases, and two real CV task pairs (segmentation+depth on Cityscapes, detection+keypoint on COCO).

## Strengths

- **Novel theoretical framework (Theorem 1, Eqs. 6–7):** The extension of Wyner's (1975) lossless bound to the lossy setting, showing interaction information as a sandwich between Gács-Körner and Wyner's lossy common information, is a genuine information-theoretic contribution. The discussion of separability and the ergodic decomposition argument (Eq. 8, lines 109–113) is particularly insightful for motivating why approximate methods are necessary.

- **Principled optimization objective derived from theory (Theorem 2, Eq. 12):** The β-parameterized Lagrangian directly derives from the Gray-Wyner objective (Eq. 9), with β=1 targeting transmit rate, β=2 targeting receive rate, and β=3/2 balancing both. This is more principled than ad-hoc multi-task codec objectives, and the empirical validation confirms β=3/2 is a reasonable operating point (Figures 3c, 3d).

- **Comprehensive and well-designed experimental evaluation:** Four experimental settings — synthetic (Section 4.1), colored MNIST edge cases with Dependent/Independent/Mixture PMFs (Section 4.2), Cityscapes (Section 4.3), and COCO (Section 4.3) — demonstrate the method adapts correctly to varying dependency structures. The synthetic experiments comparing Shared vs. Separated vs. Combined architectures (Figure 3b) provide clean ablation evidence, and the colored MNIST edge-case design is clever.

- **Consistent rate savings on real CV tasks (Figure 5):** The method achieves BD-rate advantages over Independent of 120.37% (Cityscapes) and 64.20% (COCO) in transmit rate, while operating near Joint performance (23.32% and 13.16% BD-rate relative to Joint).

- **Transparent treatment of limitations:** The paper honestly acknowledges that lossy common information is often unattainable (separability discussion, Section 3.1), that GK common information is zero for Gaussian sources, and that the mask mechanism is sensitive to γ (line 181). This intellectual honesty strengthens the paper.

## Weaknesses

### Fatal

None.

### Major

- **Theory-practice gap regarding Markov conditions:** The theoretical framework (Sections 2.1–3.2) is built on the Markov conditions Z₂ ↔ X₂ ↔ X₁ and Z₁ ↔ X₁ ↔ X₂ (Eq. 1), which assume each task depends only on its corresponding source. These conditions define the Gray-Wyner region and the meaning of common information measures C and K. However, the implementation explicitly removes these conditions — line 167 states: "Because each branch of the proposed architecture has access to both sources X₁ and X₂... This effectively removes the requirement for the conditions in 1," and line 191 further collapses to (X₁, X₂) = X. The paper does not discuss what theoretical guarantees remain under this relaxation. Does β still control the transmit-receive tradeoff? Do the bounds in Theorem 1 still serve as meaningful approximations? The paper claims the method is "grounded on the proposed objective function" (line 160) while its implementation violates the assumptions under which that objective was derived. The paper should explicitly discuss what the optimization objective means when the Markov conditions are relaxed and whether the common channel still isolates common information in the theoretical sense.

### Minor

- **Misleading "six vision benchmarks" in abstract:** The abstract claims "six vision benchmarks," but there are four experimental settings (synthetic, colored MNIST, Cityscapes, COCO) covering six individual tasks. The synthetic dataset is not a "vision benchmark." This overstates the experimental scope and should be corrected.

- **Non-standard BD-rate aggregation in conclusion:** The conclusion states "BD-rate advantage of -81.58% in transmit rate, against single-task codecs." This averages BD-rate differences across experiments with different reference methods: MNIST BD-rates are relative to the proposed method (Figure 4), while Cityscapes/COCO BD-rates are relative to Joint (Figure 5). While the individual results are convincing on their own, this aggregated figure uses a non-standard methodology. The paper should either explain the computation or replace it with per-experiment comparisons.

- **Limited exploration of mask mechanism alternatives:** The mask in Eq. 14 zeros out mismatched elements entirely. The paper acknowledges sensitivity to γ (line 181: "Small values of γ might result in elements of Y₀⁽¹⁾ and Y₀⁽²⁾ never matching") and mitigates by fixing γ=1 and tuning β. No alternatives are explored, which limits confidence in the architecture's robustness across different settings.

### Trivial

None.

## Nice-to-Haves

- Provide a direct comparison of the proposed method's common channel rate against empirical mutual information for the real CV tasks (as done for synthetic in Figure 3a), to let readers assess whether the method isolates common information.
- Report standard deviations or confidence intervals, especially given sensitivity to γ and β.
- Brief discussion of computational overhead (parameters, FLOPs, training time) compared to Independent and Joint baselines.

## Removed Points

These points are flagged to be removed, treat them with caution.

- **Harsh critic's concern about "missing standard deviations"**: Valid but a nice-to-have, not a core flaw — rate-distortion papers typically do not report confidence intervals for BD-rate.
- **Strength finder's claim about pre-trained task models as a distinguishing strength**: This is a reasonable design choice noted in the paper (Section 4.3) but is standard practice in coding-for-machines work and not a unique contribution of this paper.
- **Strength finder's claim about the masking mechanism being a "novel architectural contribution"**: While creative (Eq. 14), the mask mechanism is an implementation detail; the paper's core contribution is the theoretical framework. The mechanism's sensitivity to γ (acknowledged by the authors) limits its strength as a standalone contribution.

## Novel Insights

The paper's most novel insight is connecting the gap between Wyner's and Gács-Körner lossy common information (quantified by interaction information in Theorem 1) to the practical need for a tunable β parameter. This bridges a 50-year-old information-theoretic concept with modern learnable compression. The observation that lossy common information is even harder to achieve than its lossless counterpart — due to the additional requirement of separability from "excess common information" not useful for rate-distortion (lines 109–113) — is a genuine conceptual contribution that clarifies why approximate approaches are necessary and motivates the transmit-receive tradeoff exploration.

## Suggestions

- Add a dedicated paragraph explicitly discussing what theoretical guarantees (if any) remain when the Markov conditions are relaxed, and whether β retains its interpretability in this regime. Even a brief acknowledgment that the theory serves as motivation/approximation rather than formal guarantee would strengthen the paper significantly.
- Replace the aggregated -81.58% figure with per-experiment BD-rate comparisons, which are more transparent.
- Correct "six vision benchmarks" to accurately describe the experimental scope.

## Calibration Anchors

| Path | Avg Score | Round | Comparison |
|------|-----------|-------|------------|
| gwZ90hFSL2.md | 1.00 | R1 | Off-topic paper on Chinese NLP; irrelevant |
| Uj0h13lVrR.md | 1.00 | R1 | GFlowNets paper with fatal flaws; far below ours |
| gIrVoQEDQv.md | 3.40 | R1 | NCA compression, limited novelty; below ours |
| aQ7qYnY2nF.md | 4.00 | R1 | RL rate control, limited novelty; below ours |
| x33vSZUg0A.md | 5.33 | R1 | Multi-task compression with task grouping; comparable topic but weaker theory and presentation; below ours |
| LnKDcqOfgy.md | 5.00 | R1 | Rate-distortion model quantization; less novel |
| Piod76RSrx.md | 5.50 | R2 | Slicing MI generalization bounds; comparable theory depth |
| jznbgiynus.md | 6.00 | R1 | Language Modeling Is Compression; solid but different scope; comparable |
| bsnRUkVn63.md | 6.00 | R1 | Test-time adaptation for LIC; incremental; comparable |
| mRw9BuNO9i.md | 6.00 | R2 | Cross-platform video codec; different focus |
| UvpuGrd6ey.md | 6.25 | R2 | DNNs and compositionality; theory paper |
| vkakKdznFS.md | 6.33 | R2 | TextSeg; different topic |
| foKwWau15m.md | 6.00 | R1 | CMC-Bench; benchmark paper with less novelty |
| VkWbxFrCC8.md | 6.67 | R2 | RECOMBINER; incremental improvement; comparable |
| Tv36j85SqR.md | 7.20 | R1 | Lattice Transform Coding; strong theory+experiments, comparable depth; above ours |
| CxXGvKRDnL.md | 8.00 | R1 | Progressive compression with diffusion; strong paper; above ours |

**Round 1 bracket: 5.5–7.5.** The paper is clearly above the 5.33 multi-task compression paper and comparable to 6.0–6.67 compression papers, but below the 7.20 lattice transform coding paper which has comparable theoretical novelty without the theory-practice gap.

**Round 2 narrowing: 6.0–7.0.** The paper has stronger theoretical novelty than uniform-6 papers but the Markov condition gap places it below the 7.20 paper.

**Final score: 6.5.** A solid contribution with genuine theoretical novelty and comprehensive experiments, tempered by the acknowledged but under-discussed theory-practice gap.

MY FINAL SCORE: <score>6.5</score>
MY FINAL DECISION: <decision>Accept</decision>