Now let me compile all the information and write the final review.

## Summary

This paper introduces TbLTA, the first weakly-supervised approach for dense long-term action anticipation (LTA) that trains exclusively from video transcripts (ordered action lists without timing or duration information), entirely eliminating the need for frame-level annotations. The architecture combines temporal alignment to generate pseudo-labels (building on the prior ATBA module), cross-modal attention between video features and transcript embeddings, CTC loss for global transcript supervision, and a CRF-based anticipation decoder. Experiments on Breakfast, 50Salads, and EGTEA show that TbLTA achieves competitive results with fully supervised methods on Breakfast and establishes the first transcript-only baseline for dense LTA.

## Strengths

- **First transcript-only weakly-supervised method for dense LTA.** The paper correctly identifies a genuine gap: prior LTA work has relied exclusively on dense frame-level annotations, and TbLTA is the first to operate purely from ordered action lists without timing or duration. This is a real step toward scalable LTA. (Supported by lines 5-35 and Table 1.)

- **Strong deterministic results on Breakfast dataset.** At Obs 30%, deterministic TbLTA achieves 40.28, 35.76, 31.67, and 28.79 at 10–50% horizons, all beating the best supervised method (ActFusion at 35.79, 31.76, 29.64, 28.78). The average of 29.03 also beats ActFusion's 28.45. For a method using no frame-level labels, this is genuinely impressive and suggests transcript supervision captures procedural structure well on this dataset. (Table 1.)

- **Well-motivated and structured architecture.** The encoder-decoder design (class tokens → temporal alignment for pseudo-labels → cross-modal attention → CTC loss → CRF anticipation decoder) is coherent. Each component addresses a specific challenge of the weak-supervision setting, and the ablation study (Table 4) shows measurable performance drops when components are removed.

## Weaknesses

### Major

- **Ablations are conducted on the stochastic Top1 variant, not the deterministic variant used for the main comparison.** The paper states (line 231): "All ablations are conducted on both Breakfast and 50Salads, and we report results using the Top-1 MoC metric." Table 4 numbers match the TbLTA* – Top1 row from Table 1 (e.g., 37.2 vs. 37.18 on Breakfast at Obs 20%/10%). The deterministic results (the "Ours (TbLTA)" row without *) are the paper's primary contribution claim, but the ablation analysis does not isolate which components drive those specific results. The relative importance of components (e.g., CRF loss for filtering incoherent multi-sample sequences vs. single-pass decoding) could differ between the two settings. Running ablations on the deterministic variant would directly connect the analysis to the main claim.

- **No variance or statistical significance reported across standard dataset splits.** The paper states (line 194) that results are "averaged over four standard splits for Breakfast and five for 50Salads," yet no standard deviations, confidence intervals, or significance tests are provided anywhere. Some ablation differences are small (e.g., ~0.6 points on 50Salads for CTC removal, ~0.8 on Breakfast). Without error bars, it is impossible to assess whether these differences are meaningful or within the noise of the evaluation. Given that standard splits already exist, reporting mean±std across them would be straightforward and would substantially strengthen the paper's evidence.

### Minor

- **Mixed deterministic results across datasets undercut the strength of the central claim.** Deterministic TbLTA is strong on Breakfast (beating all supervised methods at Obs 30%) but substantially below supervised methods on 50Salads (20.92 vs. ActFusion's 28.39 average) and on EGTEA (65.37 vs. Anticipatr's 76.80). The paper acknowledges this (line 227: "Performance on 50Salads paints a complementary picture") but the abstract's phrasing — "a very robust and less costly alternative" — is somewhat overstated given this pattern. The contribution is real but should be framed more precisely around the specific settings where transcript-only supervision works well.

- **The stochastic protocol (Mean/Top1) is not defined in the main paper.** The paper only says (line 223): "We also report the stochastic protocol of Abu Farha & Gall (2019) in the supp. mat." The main text gives no explanation of how Mean and Top1 are computed, how many samples are used, or how they relate to the deterministic results. Since these entries appear in the main results table, the reader should be able to interpret them without consulting the supplement.

- **The EGTEA evaluation is restricted to verb-only prediction with only two baselines (Timeception 2019, Anticipatr 2022b).** The gap is large (65.37 vs. 76.80), but without more contemporary supervised baselines it is unclear how much reflects the inherent limitation of weak supervision vs. architectural factors. Since EGTEA has the most complex label space (106 verb-noun classes), a more thorough evaluation here would be informative.

- **Loss weights (γ₁, γ₂, γ₃ in the loss formulation) and key hyperparameters (learning rate, batch size, number of stochastic samples) are deferred to the supplementary material without summary in the main paper.** While this is common, a brief summary of the key values would help readers assess reproducibility from the main text alone.

### Trivial

None.

## Nice-to-Haves

- Run the ablation study on the deterministic variant (not just the stochastic Top1 variant) to directly support the main contribution claim.
- Report mean ± std across standard dataset splits for all main results and ablations.
- Briefly define the stochastic protocol (Mean, Top1, number of samples) in the main paper text.
- Add more recent baselines to the EGTEA evaluation.

## Removed Points

These points are flagged to be removed, treat them with caution:

1. **Stochastic Top1 presentation is misleading (Issue 1b from harsh critic).** REMOVED: The table clearly separates deterministic (no *) and stochastic (*) rows. The caption states "The highest accuracy under a probabilistic framework is indicated in gray" and notes "* means stochastic protocol." This is standard and a careful reader will see the distinction. The paper also discusses both variants in the text.

2. **Kim et al. (2024) related work concern.** REMOVED: The paper explicitly distinguishes itself from Kim et al. by focusing on *dense* frame-level prediction, not symbolic sequence prediction. The paper says (lines 51-53): "Within this landscape, we focus on the task of dense long-term action anticipation." The claim of being "first weakly-supervised approach for LTA" specifically refers to dense LTA, which is clear from context.

3. **Missing CTC ablation table (Table 3).** REMOVED: The parser strips appendices; this content exists in the original submission.

4. **Qualitative results only show 2 examples.** REMOVED: The paper acknowledges this and says "More qualitative results are provided in the supp. mat." (line 287). These are illustrative, not an exhaustive analysis.

5. **Scope creep about failure analysis and computational cost.** REMOVED: Nice-to-have suggestions, not core weaknesses.

6. **WS-DA comparison limited to one setting.** REMOVED: This is a limitation of WS-DA's reported results, not TbLTA's. The paper fairly reports the comparison where available.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

- Run the ablation study on the **deterministic** variant (TbLTA without *) rather than the stochastic Top1 variant, so the analysis directly supports the primary contribution claim.
- Report **mean ± standard deviation** across the standard dataset splits (4 for Breakfast, 5 for 50Salads) for all main results and ablations.
- Include a brief definition of the stochastic protocol (Mean, Top1, number of samples) in a short paragraph in the main paper, not only in the supplement.
- Report the numerical values of γ₁, γ₂, γ₃ and key training hyperparameters (learning rate, batch size) in the main paper.
- Add more recent supervised baselines to the EGTEA evaluation, or at minimum discuss which contemporary methods could not be compared and why.

## Calibration Report

**All anchors retrieved (across rounds):**

| Path | Avg Score | Round | Itemized | Comparison |
|------|-----------|-------|----------|------------|
| /home/.../5lUdTogEL3.md | 1.00 | R1 (bracket) | No | Person re-identification; irrelevant topic |
| /home/.../u1cQYxRI1H.md | 0.50 | R1 | No | Image harmonization; irrelevant |
| /home/.../gwZ90hFSL2.md | 1.00 | R1 | No | Robotics/NLP; irrelevant |
| /home/.../2HdZPEQUig.md | 3.00 | R1 | No | Object-centric video learning; weakly related |
| /home/.../MI0UiWeqOl.md | 2.33 | R1 | No | Autoregressive modeling; weak similarity |
| /home/.../q1Cv7Hp52y.md | 3.00 | R1 | No | RL + symbolic planning; weak similarity |
| /home/.../dl34rOnbqJ.md | 4.40 | R1 | Yes | Action anticipation (short-term, egocentric); somewhat related but weaker scope |
| /home/.../DE2RMJVjgI.md | 4.25 | R1 | No | Action localization; different task |
| /home/.../1DEHVMDBaO.md | 4.60 | R1 | No | Long-form video ViT; different focus |
| /home/.../Bb21JPnhhr.md | 6.25 | R1 | Yes | **AntGPT**: LTA with LLMs. Closest anchor. Stronger evaluation (SOTA on 3 benchmarks) but weaker novelty (LLM application). TbLTA has stronger novelty but weaker evaluation rigor. |
| /home/.../f3CdjpPkSq.md | 6.50 | R1 | Yes | **Action Sequence Augmentation**: Action anticipation with augmentation. Stronger evaluation but limited novelty. TbLTA has stronger novelty but weaker evaluation. |
| /home/.../d9iHI1eimo.md | 6.00 | R1 | No | 3D tracking; different task |
| /home/.../QQBPWtvtcn.md | 7.67 | R1 | No | View synthesis; different task |
| /home/.../7gUrYE50Rb.md | 8.00 | R1 | No | Embodied QA; different |
| /home/.../agPpmEgf8C.md | 8.00 | R1 | No | RL in brain; different |
| /home/.../GQgPj1H4pO.md | 6.00 | R2 (narrow) | No | Weakly supervised VidSGG; different task |
| /home/.../HEXtydywnE.md | 6.00 | R2 | No | Neuro-symbolic scene graphs; different task |
| /home/.../HnpDHiItd2.md | 6.67 | R2 | Yes | Procedure planning with diffusion; related task, stronger evaluation. |
| /home/.../y80D4IojuY.md | 6.75 | R2 | No | Agent behavior modeling; different |

**Round-1 bracket:** Between 4.40 and 6.50 (bounded by dl34rOnbqJ at 4.40 and f3CdjpPkSq at 6.50). The most topically similar anchors are AntGPT (6.25) and Action Sequence Augmentation (6.50) — both accepted, both with stronger evaluation rigor than TbLTA.

**Round-2 narrowing:** The anchor MTID (6.67) has stronger evaluation (detailed ablation, SOTA on multiple benchmarks) but also weaknesses (limited novelty). TbLTA's novel contribution (first weakly-supervised dense LTA) is stronger than MTID's incremental architecture change, but TbLTA's evaluation is weaker.

**Final placement vs. anchors:** TbLTA shares AntGPT's +9.9x strengths (strong results, well-motivated) but has two high-magnitude weaknesses that AntGPT also had (a -10.00 for no variance; AntGPT had -10.00 for marginal improvement and -9.98 for limited novelty). The key difference: AntGPT's evaluation was more thorough across 3 benchmarks, while TbLTA's convincing results are primarily on one dataset (Breakfast). TbLTA also has the additional -6.05 weakness of ablations on the wrong variant. These place TbLTA below AntGPT (6.25) but above the 4.40 action anticipation paper, which had a weaker contribution.

MY FINAL SCORE: <score>5.0</score>
MY FINAL DECISION: <decision>Reject</decision>