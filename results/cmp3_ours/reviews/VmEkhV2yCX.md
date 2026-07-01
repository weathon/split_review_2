Now I have sufficient calibration data. Let me write the final review.

## Summary

This paper conducts a large-scale empirical study — pretraining 8B models from scratch for 1 trillion tokens — investigating how reasoning data (varying in scale, diversity, and quality) affects LLM performance when introduced at different training stages (pretraining vs. SFT vs. RL). The central findings are: (1) injecting reasoning data during pretraining creates a durable advantage that post-training alone cannot fully recover (~19% gain); (2) an asymmetric allocation principle where diversity matters most in pretraining while quality dominates in SFT; (3) high-quality pretraining data can exhibit a "latent effect" unlocked by SFT; and (4) naively scaling SFT data with mixed quality can be harmful.

## Strengths

1. **Large-scale, controlled investigation with fixed token budget.** Pretraining 8B models from scratch for 1T tokens across multiple data conditions, with a principled 80B reasoning-token budget held constant across all pretraining variants, is a substantial investment that enables meaningful comparisons. The three-phase pipeline (pretraining → SFT → RL) is well-motivated and seldom studied at this scale.

2. **Actionable, clearly communicated heuristics.** The asymmetric principle (diversity for pretraining, quality for SFT) and the finding that reasoning-rich pretraining creates durable advantages over SFT-only approaches are non-trivial, practically relevant, and clearly laid out.

3. **Striking RL-phase results (Table 3).** The gap between M_base + SFT_SHQ + RL (37.92) and M_LMQ + SFT_SHQ + RL (56.66) is large and directionally consistent with the pretraining story. That the advantage compounds through SFT and RL rather than fading is the paper's strongest empirical claim.

4. **Catch-up control experiment (Table 4).** Doubling SFT epochs for the baseline model and showing it still fails to match reasoning-pretrained models directly addresses the most natural counterargument and cleanly refutes the "catch-up" hypothesis within the constraints tested.

## Weaknesses

### Fatal
None.

### Major

1. **Confounded variables in the "diversity vs. quality" comparison weaken causal attribution.** The paper's central asymmetric principle — diversity matters for pretraining, quality for SFT — is built on comparing datasets D_LDQ (268M samples, Nemotron, 56/17/27% math/code/science) and D_SHQ (1.2M samples, Guha et al., 71/21/8% math/code/science). These differ along multiple confounded axes simultaneously: dataset size (→ repetition rate, with D_SHQ repeated ~67× during pretraining), data source, domain composition, and quality level. When M_LDQ outperforms M_SHQ in pretraining (Table 1), the paper attributes this to "diversity," but competing explanations (D_SHQ's heavy repetition leading to overfitting on a narrow distribution, domain coverage differences) are equally plausible. Likewise, when SFT on D_SHQ outperforms SFT on D_LDQ (Table 5), this is attributed to "quality," but D_SHQ is a completely different dataset from a different source — not a quality-filtered variant of D_LDQ. The paper includes no experiment that varies *only* quality or *only* diversity while holding other factors fixed. This means the "asymmetric principle" is an interpretation of a comparison between two specific datasets, not a causally isolated finding about abstract data properties. (Paper lines 82-87 describing datasets; Tables 1 and 5)

2. **"Latent effect" claim confounded by data overlap between pretraining and SFT.** The paper claims that M_LMQ (pretrained on D_LDQ + D_SHQ) shows a "latent advantage" of +4.25% over M_LDQ (pretrained on D_LDQ alone) post-SFT (Table 4), interpreting this as high-quality pretraining data instilling a capability unlocked only during SFT. However, a simpler explanation exists: M_LMQ saw D_SHQ data during pretraining (repeated to match the 80B token budget), so when SFT uses D_SHQ, M_LMQ benefits from having already been trained on those *exact examples*, potentially multiple times. The paper does not test whether the advantage persists when SFT uses a *different* high-quality dataset not seen during M_LMQ's pretraining, which is necessary to distinguish a genuine latent capability from data-overlap-driven memorization. (Paper lines 215-216; Table 4 — compare M_LMQ + SFT_SHQ at 50.95 vs. M_LDQ + SFT_SHQ at 46.70)

### Minor

3. **No uncertainty quantification.** The paper reports only point estimates from single training runs per condition, with no confidence intervals, standard deviations, or significance tests. While single-run experiments are common at this computational scale, several comparisons involve small margins (e.g., M_LDQ vs. M_LMQ at pretraining: 64.09 vs. 64.07), making it impossible to assess whether observed differences are reliable. A brief acknowledgment of this limitation would be appropriate.

4. **"Front-loading" terminology is somewhat imprecise given the actual schedule.** Reasoning data is introduced only in the final 400B of a 1T-token pretraining schedule (600B of D_base alone, then 400B of 80% D_base + 20% D_res). While the paper's core comparison (reasoning during pretraining vs. only during SFT) is validly tested, the term "front-loading" implies injection at the very beginning of training, which does not match the actual schedule. The supported claim is that *any* reasoning data during pretraining (even late-stage) beats only post-training injection, not that earlier-within-pretraining timing drives the effect. (Paper line 93)

5. **Key experimental details underspecified.** (a) The repetition count for D_SHQ during pretraining (1.2M samples → 80B tokens ≈ 67×) is not stated explicitly, which matters for interpreting the repetition confound. (b) The source and selection procedure for the 4.8M SFT samples is not clearly specified — it is stated as "4.8M reasoning samples from D_res" but D_res includes multiple datasets. (c) The D_ALF dataset filters by answer length >4096 tokens as a quality proxy without validating that longer answers correlate with higher quality reasoning.

### Trivial
None.

## Nice-to-Haves

- **Disentangle confounded variables:** Compare high-diversity vs. low-diversity subsets of the *same* data source (e.g., subsample D_LDQ by domain breadth) and control for repetition rate to isolate whether "diversity" or "lower repetition" drives the pretraining advantage.
- **Test the latent effect with non-overlapping SFT data:** Fine-tune M_LMQ on a high-quality dataset *not* seen during pretraining to distinguish genuine latent capability from data overlap.
- **Include within-pretraining timing ablations:** Compare early vs. late injection of reasoning data within the pretraining phase to directly test the "front-loading" timing interpretation.
- **Expand RL comparisons** to include more conditions (e.g., M_LDQ + SFT_SHQ + RL) to test whether the asymmetric principle extends through RL.

## Removed Points

- **Issue about SFT scores being "suspiciously low":** This is speculative. The evaluation benchmarks (AIME24/25, GPQA, LiveCodeBench) are genuinely hard, and the reported scores are plausible for an 8B model. No evidence that the SFT setup is suboptimal was provided. **Removed as speculative.**
- **Claim that the formalization (Eqs. 1-2) is not "used":** The equations frame the conceptual optimization problem; not every formalization in a paper needs to be quantitatively instantiated. This is a framing observation, not a weakness. **Removed as nitpick.**
- **Concern about pretraining data format (QA pairs vs. raw text):** The paper describes using reasoning-style data during pretraining with standard LM loss, following the established "instruction pretraining" paradigm (Cheng et al. 2024). **Removed — not an omission.**
- **Single architecture concern:** The paper acknowledges this limitation and provides a small-scale replication with a 1.2B Transformer in the appendix. **Removed — already addressed by the paper.**
- **Strength 1 from input review ("ambitious investigation"):** While somewhat generic, it references specific concrete design elements (8B models, 1T tokens, 80B controlled budget). Modified and kept in Strengths above.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

- Reframe the contribution to distinguish more carefully between claims about abstract properties ("diversity," "quality") and claims about specific datasets. The empirical findings about which dataset works better at which training stage are valuable even without full causal isolation.
- Add a control experiment testing M_LMQ + SFT on a *different* high-quality dataset (not seen during pretraining) to properly test the "latent effect" interpretation versus the data-overlap alternative.
- Report confidence intervals or variance estimates where feasible, or at least explicitly acknowledge the single-run limitation.
- Clarify the SFT data source (4.8M samples) and the D_SHQ repetition count in the main text.

---

**Calibration analysis.** I retrieved anchor papers across score bands. Topically similar anchors in the 5.5–7.5 range include:

| Path | Avg Score | Round | Comparison |
|------|-----------|-------|------------|
| `GtpubstM1D.md` — "Advancing Mathematical Reasoning" | 5.71 | R1/R2 | Similar study of CPT vs. SFT for math reasoning, but math-only focus and similar confound issues. Our paper is broader (math, science, code) but has similar causal-attribution weaknesses. Comparable quality. |
| `oqsQbn4XfT.md` — "On the Diversity of Synthetic Data" | 5.80 | R1/R2 | Studies diversity in PT/SFT at smaller scale (350M–1.4B). Our paper is more ambitious but has stronger confound issues. Roughly comparable. |
| `3OyaXFQuDl.md` — "Smaller, Weaker, Yet Better" | 7.00 | R1 | Cleaner causal identification, formal framework. Our paper has less rigorous causal identification but broader scope. Our paper is weaker on rigor. |
| `cijO0f8u35.md` — "Scaling Relationship on Learning Math Reasoning" | 5.25 | R1/R2 | Narrower scope (GSM8K only). Our paper is more comprehensive and stronger overall. |

**Round 1 bracket:** 5.5–7.0. The paper is clearly stronger than the 3.5–5.5 band papers (narrower scope, smaller scale) and clearly weaker than the 7.5+ band papers (cleaner causal claims, better methodology). Within the bracket, the paper sits alongside the 5.71–5.80 papers in terms of overall quality — comparable scale and ambition, similar confound limitations. Its broader scope (math + science + code + instruction following) and clean token-budget control are advantages, but the confound issues (Major weaknesses 1 and 2) are substantial. **Final score: 6.0** — a borderline accept; the paper makes a genuine empirical contribution but overstates its causal claims.

MY FINAL SCORE: <score>6.0</score>
MY FINAL DECISION: <decision>Accept</decision>