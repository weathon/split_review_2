Now I have enough calibration data. Let me write the final review.

**Round 1 bracket:** Based on topically similar anchors, NuSA-CL sits clearly above the 5.0-6.25 range (SimE rejected at 5.25; Spectral Regularization accepted at 6.25; C-CLIP accepted at 6.50) and below the 7.5+ range (papers with broader evaluation). Initial bracket: **6.5-7.5**.

**Round 2 narrowing:** Compared to C-CLIP (6.50, accepted), NuSA-CL has a more novel mechanism, deeper analysis, and more thorough ablations. Compared to Elastic Feature Consolidation (7.00, accepted), NuSA-CL offers comparable thoroughness with a unique spectral dynamics insight. Compared to Budgeted Online CL (7.50), NuSA-CL's weaknesses are slightly more present. Final score: **7.0**.

## Summary
NuSA-CL proposes a memory-free continual learning framework for zero-shot vision-language models (e.g., CLIP) that constrains low-rank weight updates to an approximate null space of the model's current weights, identified via SVD. Only a small intermediate matrix M is trained per task while the null-space basis vectors remain frozen, and the update is merged back into the backbone, maintaining a fixed parameter budget. Experiments on MTIL (full-shot and 5-shot) and CIFAR-100 class-incremental benchmarks demonstrate state-of-the-art performance among storage-free methods with 10× fewer parameters than LoRA, while rivaling storage-based approaches.

## Strengths
- **Novel persistent null-space constraint validated by strong ablation.** Table 4a directly shows that unfreezing the null-space basis vectors U_n, V_n causes Avg. accuracy to drop from 75.08 to 68.12 (~7 points), confirming that the persistent constraint—not just initialization in low-energy directions—is the essential design choice. This cleanly distinguishes NuSA-CL from MiLoRA (initialization-only).
- **Best efficiency-performance tradeoff among storage-free methods.** Table 1 shows NuSA-CL achieves 68.6% Transfer, 75.1% Avg. using only 1.5M parameters and 1.21 GPU-hours, outperforming LoRA (15.7M params, 63.9% Transfer, 70.1% Avg.) by large margins, and rivaling storage-based MoE-Adapters (59.8M params, 76.7% Avg.) with 40× fewer parameters and 3× less compute.
- **Insightful spectral dynamics analysis providing mechanistic understanding.** Figure 2 and Section 6.1 reveal that NuSA-CL progressively increases effective rank across tasks (null-space utilization growing from ~47.4% to ~48.2% for vision encoder), while LoRA and Full-FT exhibit near-static spectral behavior. This "accumulation vs. overwriting" characterization provides genuine mechanistic insight beyond typical CL benchmark reporting.
- **Scalability advantage that grows with sequence length.** Table 3 shows the margin over ZSCL on Last accuracy grows from 0.86% at 10 steps to 4.4% at 50 steps on CIFAR-100, providing direct evidence for long-term viability.
- **Comprehensive ablation study.** Systematic validation covers subspace choice (Tail vs. Top vs. Random, Fig. 3a), update rank (Fig. 3b), persistent constraint and modality (Table 4a), energy cutoff robustness (ρ ∈ [0.80–0.99], Table 4b), and SVD overhead quantification (<1 min initialization, Table 4b).

## Weaknesses

### Fatal
None.

### Major
- **Baseline rank configuration not explicitly stated.** The paper says baselines use "a consistent rank" (§5.1) but never states the explicit value. From the parameter counts (LoRA: 15.7M; NuSA-CL: 1.5M), one can infer rank 128 is used for all methods, and the 10× parameter difference arises naturally from the architectural difference (LoRA learns A, B matrices vs. NuSA-CL learning only M). However, this is an important detail for reproducibility and for readers to properly interpret the efficiency claims. A sentence or configuration table specifying "all PEFT baselines use rank 128" would eliminate ambiguity.

### Minor
- **Single backbone scale limits generalizability.** All experiments use CLIP ViT-B/16. The paper acknowledges this in §6.3 and §7, and provides practical guidance for larger backbones. However, the central claim of being "practical and scalable" would be substantially strengthened by even one experiment on ViT-L or ViT-H, since spectral dynamics (null-space size, effective rank evolution) may differ at larger scales.
- **CIFAR-100 10-step Avg comparison not discussed.** Table 3 shows ZSCL outperforms NuSA-CL on this specific metric (82.15 vs. 80.25), though NuSA-CL wins on Last accuracy (74.51 vs. 73.65) and the gap widens at 50 steps. The paper's focus on Last accuracy is appropriate for CL evaluation, but acknowledging this comparison would strengthen credibility.
- **Theoretical analysis is parameter-space only.** Lemma 1 and Theorem 2 bound Frobenius inner product interference, not function-level forgetting. The paper is honest about this limitation and the bounds provide useful intuition, but the cumulative bound (Eq. 6) does not capture how the null space evolves across tasks—the very phenomenon that makes the empirical results interesting.

### Trivial
None.

## Nice-to-Haves
- A parameter-matched ablation where LoRA is given a rank small enough to match NuSA-CL's 1.5M budget would cleanly isolate whether gains come from the null-space constraint versus the more compact parameterization.
- Tracking which specific null-space directions are activated by specific tasks (e.g., via cosine similarity of learned M matrices across tasks) would illuminate whether different tasks occupy distinct null-space regions or compete for the same directions.
- Per-dataset breakdown analysis in the few-shot setting (Table 2) to understand when the method struggles (e.g., Aircraft at 28.9% Avg).

## Removed Points
These points are flagged to be removed, treat them with caution:
- The harsh critic's "Asymmetric Capacity in Baseline Comparisons" was significantly weakened: the asymmetry is inherent to the method design (LoRA requires A+B matrices while NuSA-CL only trains M), and achieving better performance with 10× fewer parameters is a strength. The underlying issue of missing explicit rank specification was retained as a Major weakness.
- The strength finder's claim that the theoretical bound is a core strength was not kept as a standalone strength, since the paper itself acknowledges the bounds are parameter-space only and provide limited function-level guarantees. The theory contributes to motivation but is not a primary contribution.

## Novel Insights
The spectral dynamics analysis revealing "accumulation vs. overwriting" as the fundamental difference between null-space-constrained and conventional fine-tuning approaches (Figure 2, §6.1) is a genuinely novel empirical finding. The observation that NuSA-CL progressively fills low-energy spectral directions while LoRA/Full-FT remain spectrally inert provides mechanistic understanding that goes beyond the specific method—it explains *why* null-space constraints work for continual learning and could inform future work on VLM adaptation more broadly. The quantitative evidence that available null-space directions (313.58) far exceed the update rank (r_max=128) even after 10 tasks provides practical reassurance about long-term viability.

## Suggestions
- Add an explicit statement or table specifying the rank (128) used for all LoRA-based baselines to improve reproducibility.
- Include at least one experiment on CLIP ViT-L/14 to validate scaling claims.
- Add a brief sentence acknowledging where NuSA-CL falls short (e.g., CIFAR-100 10-step Avg) to strengthen credibility.
- Consider a parameter-matched ablation to isolate the contribution of the null-space constraint versus parameter efficiency.

## Reporting

**All anchor papers retrieved:**

Round 1:
1. `/5lUdTogEL3.md` — avg 1.00 — Lifelong Person Re-ID, clearly off-topic/weak, far below NuSA-CL
2. `/u1cQYxRI1H.md` — avg 0.50 — (mis-sorted), illumination harmonization, not comparable
3. `/gwZ90hFSL2.md` — avg 1.00 — Cross-lingual humanoid robots, not comparable
4. `/P49gSPmrvN.md` — avg 1.00 — Scientific discourse visualization, not comparable
5. `/JIlIYIHMuv.md` — avg 2.50 — LVLM-CL, similar topic but much weaker contribution
6. `/WM5G2NWSYC.md` — avg 2.00 — Projected Subnetworks, similar topic, weak execution
7. `/gNoqEdT2wO.md` — avg 2.33 — MCIL benchmark, limited contribution
8. `/TxIrMD6lAN.md` — avg 3.00 — Task-Specific Adapters, moderate contribution
9. `/G9Ea7mlqGO.md` — avg 3.80 — CLIP Online CL, interesting but limited novelty
10. `/9aZ2ixiYGd.md` — avg 5.00 — Vision-Language Synergy for Rehearsal Free CL, mixed scores
11. `/EKfcngSxwD.md` — avg 4.67 — Task Codebook for VLMs, borderline
12. `/rkAqvDnnmO.md` — avg 5.25 — SimE, similar topic but less principled mechanism
13. `/sb7qHFYwBc.md` — avg 6.50 — C-CLIP, very similar topic, direct comparison
14. `/k9NYnsC4Mq.md` — avg 5.67 — Learning without Forgetting for VLMs
15. `/TLADT8Wrhn.md` — avg 6.25 — TiC-CLIP, benchmarking focus
16. `/wE1I9IGqeH.md` — avg 6.00 — Continual Learning in Open-vocabulary Classification
17. `/uAFHCZRmXk.md` — avg 8.00 — Modality Gap in VLMs, analysis paper, not directly comparable
18. `/3i13Gev2hV.md` — avg 8.00 — Compositional Entailment Learning, different focus
19. `/WyEdX2R4er.md` — avg 8.00 — Visual Data-Type Understanding, different focus
20. `/9Cu8MRmhq2.md` — avg 8.00 — Multi-granularity Correspondence, different focus

Round 2:
21. `/Ll8PmgD0IB.md` — avg 6.00 — Divide and Orthogonalize, similar orthogonalization idea
22. `/Hcb2cgPbMg.md` — avg 6.25 — Spectral Regularization for CL, related spectral approach
23. `/u3dHl287oB.md` — avg 5.67 — Analytical model for forgetting, theoretical
24. `/mz8owj4DXu.md` — avg 6.50 — Scalable Language Model with JARe, similar CL approach
25. `/7D9X2cFnt1.md` — avg 7.00 — Elastic Feature Consolidation, exemplar-free CL
26. `/dOAkHmsjRX.md` — avg 7.50 — Budgeted Online CL
27. `/Nsms7NeU2x.md` — avg 6.75 — Data Contamination, not directly comparable
28. `/b20VK2GnSs.md` — avg 7.00 — Adapting MLLM to Concept Drift
29. `/V6uxd8MEqw.md` — avg 6.50 — MISA prompt-based GCL

**Calibration reasoning:**
- NuSA-CL is clearly above papers in the 3.8-6.25 range (rejected papers like SimE at 5.25; accepted papers with weaker contributions like Spectral Regularization at 6.25 and TiC-CLIP at 6.25).
- NuSA-CL is above C-CLIP (6.50) due to its more principled mechanism, deeper spectral analysis, and more thorough ablations, despite similar single-backbone limitations.
- NuSA-CL is at the level of Elastic Feature Consolidation (7.00), which also has thorough ablations, honest limitations, and a clear contribution to exemplar-free CL.
- NuSA-CL is slightly below 7.50 anchors like Budgeted Online CL, which had fewer significant weaknesses relative to its claims.
- Final score: **7.0**.

MY FINAL SCORE: <score>7.0</score>
MY FINAL DECISION: <decision>Accept</decision>