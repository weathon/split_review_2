## Summary
This paper conducts the first systematic study of how reasoning data—varying in scale, diversity, and quality—affects 8B LLM performance when introduced at different stages of training (pretraining, SFT, RL). The authors pretrain four 8B models from scratch for 1T tokens each on 512 H100 GPUs, with a controlled 80/20 base-to-reasoning token ratio over the final 400B tokens, using reasoning datasets that range from 1.2M to 269M samples. They find that front-loading reasoning data into pretraining creates durable, compounding gains that SFT cannot replicate, and discover an asymmetric allocation principle: diversity matters most in pretraining while quality matters most in SFT.

## Strengths
- **Impressive experimental scale with clean controlled design**: Four separate 8B models pretrained from scratch for 1T tokens each on 512 H100 GPUs (Section 3.1), with fixed 80/20 base-to-reasoning token ratios over the final 400B tokens (Section 2.3). This provides causal evidence at a scale that studies relying on existing checkpoints cannot achieve.
- **Direct, well-designed test of the "catch-up" hypothesis**: Table 4 tests whether doubling SFT epochs on the baseline can match reasoning-pretrained models. The enhanced baseline (34.01%) still falls short of even the weakest reasoning-pretrained model M_SHQ + SFT_SHQ (37.33%), conclusively addressing a fundamental question.
- **Discovery of latent effects activated by SFT**: Table 4 reveals M_LMQ gains +4.25% over M_LDQ post-SFT despite near-identical pretraining performance (64.07 vs. 64.09 in Table 1), showing high-quality pretraining data instills dormant potential activated only during alignment.
- **Asymmetric allocation principle with direct evidence**: Table 1 shows diversity dominates pretraining (M_LDQ +9.09% over M_SHQ, with +28.4% in math), while Table 5 shows quality dominates SFT (SFT_SHQ ~44.99% vs. SFT_LDQ ~31.54%). This phase-dependent principle is actionable.
- **Demonstration that naive SFT scaling is harmful**: Table 8 shows doubling mixed-quality SFT data degrades math accuracy by -4.92%, while adding only 0.4% more high-quality samples consistently improves results.
- **Compounding advantage tracked across all three stages**: The gap widens from +8.35% after pretraining (Table 1), to +9.3% after SFT (Table 2), to +18.57% after RL (Table 3), with +39.32% on AIME competition math.

## Weaknesses

### Fatal
None

### Major
- **Data repetition confound undermines the diversity-vs-quality interpretation**: All reasoning-augmented pretraining runs use a fixed budget of 80B reasoning tokens (Section 2.3). D_SHQ has only 1.2M samples while D_LMQ has 269.2M samples, meaning D_SHQ must be repeated on the order of 15–30× to fill the budget. The paper acknowledges this ("When a reasoning dataset is small, it is repeated") but never discusses or controls for the confound. The central claim that "scale and diversity of the reasoning data are more critical than its curated quality" (Section 4) could be substantially explained by severe data repetition causing diminishing returns or overfitting on D_SHQ, rather than quality being inherently less important. This makes the diversity-vs-quality comparison in pretraining unresolvable as presented.

- **Incomplete RL evaluation limits strongest claims**: The paper's most dramatic result — a ~19% gap after RL (Table 3) — rests on comparing only M_base and M_LMQ after RL. Given four pretraining variants and three SFT variants each, presenting a single pair after RL makes it impossible to evaluate whether the advantage is monotonic across pretraining data types, whether RL amplifies or shrinks SFT-stage gaps, or whether the specific choice of M_LMQ is justified as representative. The paper's own SFT results (Table 4) show substantial variation across pretraining types, so this matters.

- **Headline numbers in the abstract are selectively chosen**: The "19% average gain" traces to Table 3 (56.66 − 37.92 = 18.74), which compares only the single best reasoning-pretrained model against baseline after RL — not an average across all reasoning-pretrained variants. The more representative SFT-stage average is +9.3% (Table 2). The "+11% gain with diverse corpus" traces to Table 1 (M_LDQ 64.09 − M_base 52.70 = 11.39), which is "any reasoning data vs. none," not diversity per se (the diversity-specific M_LDQ vs. M_SHQ comparison yields +9.09%). The "+15% gain with high quality data" does not cleanly trace to any single table entry (Table 5: M_res + SFT_SHQ 44.99 − M_res + SFT_LDQ 31.54 = 13.45%). Each number selects the most favorable comparison rather than a systematic analysis.

### Minor
- **No variance or uncertainty reporting**: The paper reports Pass@1 averages of 4 or 16 runs (Section 3.2) but never reports standard deviations or confidence intervals. For large effect sizes this may not change conclusions, but for smaller differences (e.g., 64.07 vs. 64.09 in Table 1, or 32.84 vs. 32.99 in Table 8) it is impossible to determine whether differences are meaningful.
- **ALF proxy for reasoning complexity is unvalidated**: D_ALF (7.1M samples) is created by filtering D_LMQ for answer length >4096 tokens on the principle that "longer responses often correspond to more complex CoT reasoning" (Section 2.2). This proxy is never validated — length could correlate with verbosity or template repetition rather than reasoning quality.
- **Non-dominant architecture limits generalizability**: The study uses a hybrid Mamba 2 + attention architecture (Section 2.1), which is not the dominant architecture in the field. The 1.2B Transformer experiment (Table 14 in appendix) is not discussed in the main text, leaving open whether findings transfer to pure transformers.
- **Reasoning ratio ablation only tested with D_LMQ**: Tables 6–7 vary reasoning proportion (10%, 20%, 40%) but only with D_LMQ, and may not generalize to the other datasets.

### Trivial
None

## Nice-to-Haves
- Validate the ALF proxy with a brief quality analysis of D_ALF entries vs. random D_LMQ entries.
- Add a consistent core benchmark evaluated at every stage (pretraining, SFT, RL) to track capability evolution.
- Briefly discuss transferability of findings to pure transformer architectures.

## Removed Points
These points are flagged to be removed, treat them with caution:
- "QA-format reasoning data during pretraining is a significant design choice not discussed" — scope creep; the paper studies when to inject reasoning data, not the optimal format for pretraining corpora.
- Table 8's D_ALF* is "only implicitly defined" — the naming convention and "0.4% more samples" claim make this clear: D_ALF' = D_ALF ∪ D_SHQ. Minor nitpick.
- Table 2's averaging across SFT variants "could mask important variation" — the paper references Table 13 for full breakdowns.
- "Benchmark changes between stages" — reasonable for stage-appropriate evaluation (general capability vs. reasoning-specific).

## Novel Insights
The most genuinely novel finding is the discovery of latent effects from high-quality pretraining data: M_LMQ shows near-identical performance to M_LDQ immediately after pretraining (Table 1: 64.07 vs. 64.09) but reveals a +4.25% advantage after SFT (Table 4: 50.95 vs. 46.70). This suggests that pretraining can instill "dormant" capabilities only activated through alignment — implying that evaluating pretraining data quality requires post-training evaluation, not just base model benchmarks. The asymmetric allocation principle (diversity → pretraining, quality → SFT) is also practically actionable, though its precise magnitude is somewhat undermined by the repetition confound.

## Suggestions
- Report the repetition factor for each dataset and add a discussion acknowledging this confound in the diversity-vs-quality comparison. Alternatively, run a cap-repetition ablation for D_SHQ.
- Complete the RL evaluation by running RL on at least M_SHQ and M_LDQ (with SFT_SHQ + RL) to show whether the pretraining advantage is monotonic.
- For headline numbers in the abstract, add explicit table citations so readers can verify each claim.
- Add standard errors or confidence intervals to key tables.

## Calibration Report

**All anchors retrieved across rounds:**

| Path | Avg Score | Round | Comparison |
|------|-----------|-------|------------|
| 8QTpYC4smR (Systematic Review of LLMs) | 1.00 | R1 | Low-effort survey, not comparable |
| gwZ90hFSL2 (Cross-Lingual Humanoid Robots) | 1.00 | R1 | Irrelevant topic, not comparable |
| 5kMwiMnUip (NEMESIS Jailbreaking) | 1.40 | R1 | Weak jailbreak paper, not comparable |
| nSDOkm0SKo (Financial Markets NN) | 1.00 | R1 | Not comparable |
| bntJK4NyIW (Decentralized Training) | 2.00 | R1 | Rejected, limited contribution |
| qgLyKwXVDs (FreeLM) | 2.00 | R1 | Rejected, limited scope |
| a2rSx6t4EV (EDU-RAG) | 2.33 | R1 | Rejected, narrow benchmark paper |
| SaOxhcDCM3 (Self-Consuming Training Loop) | 3.20 | R1 | Interesting but rejected |
| bppG9srkpR (LokiLM) | 3.60 | R1 | Technical report, rejected |
| cqU91W3LnB (ReBase) | 4.33 | R1 | Limited distillation work |
| OegBJMucyM (Pre-Memorization Accuracy) | 4.25 | R1 | Narrow scope, rejected |
| GtpubstM1D (Advancing Mathematical Reasoning) | 5.71 | R1 | Similar topic but major issues (one reviewer scored 1); under-review paper is clearly stronger |
| EDoD3DgivF (Linear Representations) | 6.00 | R1 | Clean but narrower contribution |
| 1hQKHHUsMx (What Kind of Pretraining Data) | 6.75 | R1 | Interesting interpretability; accepted. Under-review paper has more ambitious scale |
| KIPJKST4gw (At Which Training Stage Does Code Data Help) | 7.25 | R1 | **Most relevant** — same question, accepted. Had smaller scale and token-control issue but cleaner claims |
| 07yvxWDSla (Synthetic Continued Pretraining) | 8.00 | R1 | Cleaner method + theory, above under-review paper |
| f4gF6AIHRy (DiSF) | 8.00 | R1 | Clean pretraining contribution, above |
| vf5aUZT0Fz (DEPT) | 8.00 | R1 | Clean method, above |
| jOmk0uS1hl (Training on Test Task) | 8.00 | R1 | Strong evaluation methodology, above |

**Round 1 bracket: 6.0–7.0.** The paper is clearly stronger than the 5.0–6.0 anchors (which had major methodological issues or very limited scope) but has substantive concerns (repetition confound, selective reporting, incomplete RL) that keep it below the 7.0–8.0 anchors (which had cleaner claims or novel methodology). The most relevant comparison is KIPJKST4gw (7.25), which asks the same question but at smaller scale; the under-review paper has more impressive experiments but more problematic reporting.

**Final calibration: 6.5.** This is a solid empirical study with genuinely ambitious scale and practically useful findings, held back by a significant methodological confound in its central quality-vs-diversity comparison, selective headline reporting, and an incomplete RL evaluation. The directional findings are likely correct, but the quantitative claims need the confound and reporting issues addressed.

MY FINAL SCORE: <score>6.5</score>
MY FINAL DECISION: <decision>Accept</decision>