Now let me write the final consolidated review.

## Summary
PI-CCA introduces a geometry-first approach to vision-language continual learning that preserves cross-modal alignment invariants (canonical correlations and subspaces) rather than proxy signals (logits, similarities, weight regularization). A compact CCA certificate is maintained via EMA and matched during adaptation using spectral and subspace-angle losses, with prompt invariance achieved by averaging projectors over perturbations. The method achieves state-of-the-art results among replay-free methods across four VL-CL benchmarks (MTIL, X-TAIL, VLCL, ConStruct-VL).

## Strengths
- **Consistent SOTA across four diverse benchmarks without replay**: Tables 1–2 show PI-CCA achieves best results among replay-free methods on MTIL (76.8 Avg), X-TAIL (68.1 Avg), VLCL retrieval (48.6 I2T R@1, 37.4 T2I R@1), and ConStruct-VL (75.2 FA, 2.7 AF). It even outperforms GIFT (a diffusion-synthetic-replay method) on VLCL retrieval (48.6 vs. 47.3 I2T R@1) while storing zero past data.

- **Thorough component-wise ablation with clear evidence**: Table 3 demonstrates meaningful contribution from each loss component—removing spectral or subspace terms causes 2.2–2.7 p.p. drops, covariance EMA removal causes 2.5–2.8 p.p. drops. The sorted pairing surrogate is near-identical to exact Hungarian (0.1 p.p. difference), justifying the computational shortcut.

- **Practical robustness analyses**: Figure 5 shows narrow IQRs across 20 random task orderings (3 seeds each), Figure 2 demonstrates robustness to certificate capacity hyperparameters via Pareto analysis, and Figure 4 provides quantitative prompt invariance stress testing under both ID and OOD perturbations with clear degradation slope reductions.

- **Well-motivated conceptual contribution with coherent math**: The reframing of forgetting as alignment-geometry drift and the direct targeting of CCA invariants (rather than proxy signals) is principled and practically relevant. The mathematical development—sketched projectors via random orthonormal bases (Eq. 4), permutation-invariant spectral loss (Eq. 8), prompt-averaged projectors (Eq. 5–6)—is coherent and well-structured.

## Weaknesses

### Fatal
None

### Major
- **Missing error bars on Table 1 classification results**: Table 2 (VLCL, ConStruct-VL) reports ± standard deviations across seeds for all methods, but Table 1 (MTIL, X-TAIL) reports none. The margins between PI-CCA and the strongest replay-free baseline are modest: +1.6 p.p. Avg, +1.7 p.p. Last on MTIL; +0.7/+0.7 on X-TAIL. Without variance estimates, it is impossible to determine whether these gaps are statistically meaningful or within noise. Since the "state-of-the-art" claim rests partly on these numbers, the selective reporting of error bars weakens confidence in the headline result.

- **Confounded geometry→performance correlation in Figure 3**: The paper reports near-perfect Pearson/Spearman correlations (r≈1.00, ρ=1.00) between geometry drift and performance drops. However, these are computed by sweeping hyperparameters (certificate size, LoRA rank, learning rate, etc.) that simultaneously affect both geometry drift and downstream performance through independent pathways. For instance, higher LoRA rank yields better adaptation → less forgetting *and* less drift, trivially. The correlation cannot establish that preserving geometry *causes* better retention versus being an epiphenomenon of capacity/flexibility. The paper's claim that "preserving CCA geometry predicts retention rather than being a coincidental regularizer" (§4.3) is not supported by this sweep design. A more convincing test would fix all capacity-related hyperparameters and vary geometry drift independently (e.g., via explicit subspace corruption).

### Minor
- **Unexamined long-horizon EMA certificate dynamics**: The certificate is continuously updated via slow EMA (Eq. 13), meaning the "preserved alignment skeleton" drifts with the model. Over 7–11 tasks this plasticity is beneficial (Table 3: α=0 is worse), but cumulative drift over longer sequences could render the regularization vacuous. The paper does not analyze the certificate's trajectory (e.g., ‖S_v* − S_v^(initial)‖ over tasks) or discuss when the EMA dynamics break down.

- **Backbone specification absent from main text**: The specific CLIP backbone (ViT-B/16? ViT-L/14?) is mentioned only in Appendix §A.2, not in the main paper. This matters for interpreting absolute numbers and assessing fairness of baseline comparisons.

- **Computational overhead vs. baselines unreported**: The method adds SVD computation, covariance EMA maintenance, and optionally M prompt perturbation passes per batch. While Figure 2 shows absolute step time, there is no comparison to baseline efficiency (e.g., C-CLIP, Mod-X), which would inform practical adoption.

### Trivial
None

## Nice-to-Haves
- Report PD (zero-shot performance drop) in the main results tables, not just in the prompt stress test, since preserving zero-shot ability is a central motivation.
- Add a brief discussion of the analogy between the certificate EMA dynamics and known EMA instabilities (e.g., in BYOL/DINO) to position the method within the broader understanding of moving-target regularization.

## Removed Points
These points are flagged to be removed, treat them with caution:
- "Constant memory characterization is imprecise": The paper's usage of "constant memory" is technically correct (constant in tasks/samples), and the practical overhead of streaming covariance EMAs (a few MB) is minor. Removed as a nitpick.

## Novel Insights
The paper's genuinely novel insight is the reframing of VL-CL forgetting as alignment-geometry drift and the demonstration that CCA invariants (canonical correlations and subspaces) can serve as effective preservation targets with compact, sketch-based certificates. This goes beyond incremental improvement—it reconceptualizes what should be preserved during continual adaptation of VLMs. The consistent SOTA results across four diverse benchmarks (classification, retrieval, structured concepts) provide meaningful empirical support, even if the causal mechanism claim is weakened by the confounded sweep design.

## Suggestions
- Add error bars (±std over seeds) to Table 1 for MTIL and X-TAIL, matching the reporting standard already used in Table 2.
- For the geometry→performance correlation, construct at least one test that varies geometry drift independently of capacity (e.g., fix all hyperparameters and apply varying levels of explicit subspace corruption or regularization, then show drift tracks performance).
- Add a simple plot of certificate trajectory over the task sequence (e.g., ‖S_v* − S_v^(initial)‖) to address long-horizon EMA dynamics.
- Specify the backbone in the main experimental setup section.

## Score and Decision

**Calibration anchors retrieved:**
| Path | Avg Score | Round | Comparison |
|------|-----------|-------|------------|
| 5lUdTogEL3 | 1.00 | R1 | Clothing re-ID CL; unrelated, much weaker |
| u1cQYxRI1H | 0.50 | R1 | Diffusion harmonization; off-topic match |
| gwZ90hFSL2 | 1.00 | R1 | Humanoid robots NLP; unrelated |
| P49gSPmrvN | 1.00 | R1 | UMAP text embeddings; unrelated |
| 5kMwiMnUip | 1.40 | R1 | LLM jailbreaking; unrelated |
| JIlIYIHMuv | 2.50 | R1 | LVLM-CL; same domain, much weaker contribution |
| gNoqEdT2wO | 2.33 | R1 | MCIL benchmark; just a benchmark |
| WM5G2NWSYC | 2.00 | R1 | Projected Subnetworks; limited scope |
| HfJxXbXlYJ | 3.00 | R1 | LLM2CLIP; different focus |
| ZaudLwn0Hm | 2.50 | R1 | Prototypical evolution; few-shot, different |
| G9Ea7mlqGO | 3.80 | R1 | CLIP online CL; much simpler method, weaker eval |
| 9aZ2ixiYGd | 5.00 | R1 | Vision-Language Synergy; simpler method, less thorough |
| QYgtZRTv3e | 4.50 | R1 | TIPS prompt CL; less comprehensive |
| rkAqvDnnmO | 5.25 | R1 | SimE; similar topic, less rigorous |
| YGflij9S6x | 4.25 | R1 | Adaptive Contrastive Replay; different focus |
| k9NYnsC4Mq | 5.67 | R2 | Proof; comparable scope, less analysis |
| sb7qHFYwBc | 6.50 | R1/R2 | C-CLIP; directly comparable, PI-CCA outperforms |
| TLADT8Wrhn | 6.25 | R1/R2 | TiC-CLIP; different focus, comparable quality |
| wE1I9IGqeH | 6.00 | R2 | Continual Open-vocabulary CL; interesting but limited |
| 6Mg7pjG7Sw | 6.00 | R2 | CSA; CCA-related, different problem |
| ftGnpZrW7P | 7.00 | R2 | Gramian alignment; multimodal alignment, solid quality |
| Pe3AxLq6Wf | 6.25 | R2 | CoMM; multimodal alignment, moderate |
| aPTGvFqile | 6.29 | R2 | AlignCLIP; CLIP alignment, moderate |
| dOAkHmsjRX | 7.50 | R2 | Budgeted Online CL; stronger theoretical treatment |
| 9bMZ29SPVx | 7.50 | R2 | CLIP data selection; different topic |
| OZVTqoli2N | 7.50 | R2 | Second-Order Compositionality; stronger theory |
| X1OfiRYCLn | 7.50 | R2 | VLB dynamic eval; different focus |

**Round 1 bracket**: 6.5–7.5. PI-CCA clearly outperforms C-CLIP (6.50, same domain, same benchmarks) in scope, analysis depth, and results, placing a lower bound of ~6.5. The analytical weaknesses (confounded correlation, missing error bars on headline results) prevent it from matching the 7.5 papers, which tend to have stronger theoretical grounding or more comprehensive treatment of their claims.

**Final calibration**: PI-CCA sits at **7.0** — above the C-CLIP/TiC-CLIP range (6.25–6.50) due to broader benchmarks, stronger analysis, and a more principled geometric approach, but below 7.5 due to the evidential gaps in the analytical narrative (confounded correlation, selective error bars).

MY FINAL SCORE: <score>7.0</score>
MY FINAL DECISION: <decision>Accept</decision>