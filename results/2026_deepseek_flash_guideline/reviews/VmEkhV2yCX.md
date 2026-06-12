Now let me finalize the complete review.

## Summary
This paper presents a large-scale empirical study (8B models pretrained from scratch for 1T tokens) investigating how reasoning data should be allocated between pretraining and supervised fine-tuning (SFT). By systematically varying diversity, quality, and scale of reasoning data across both stages and evaluating through RL, the authors demonstrate that: (1) front-loading reasoning data into pretraining creates durable advantages that compound through post-training; (2) data allocation is asymmetric—diversity/scale matter most in pretraining while quality dominates in SFT; and (3) naive scaling of mixed-quality SFT data provides no benefit.

## Strengths
- **Systematic end-to-end pretraining from scratch with controlled reasoning data injection.** The paper trains 8B models from scratch for 1T tokens with controlled variations of reasoning data diversity, quality, and scale (Section 3.1). Table 1 shows a clean monotonic benefit from diverse reasoning data (M_LDQ at 64.09 vs M_base at 52.70). This is a significantly more controlled and computationally intensive design than existing work focused only on post-training interventions.

- **Asymmetric principle demonstrated via fully crossed experimental design.** The paper varies both pretraining data type (4 base models) and SFT data type (3 SFT corpora), creating 12 trained models. This allows direct comparison of the same dimensions across phases: diversity/scale matters in pretraining (Table 1: M_LDQ 64.09 vs M_SHQ 54.98, +9.09) while quality dominates in SFT (Table 5: M_res+SFT_SHQ 44.99 vs M_res+SFT_LDQ 31.54, +13.45).

- **RL phase evaluation showing the pretraining gap widens after full post-training.** Table 3 provides the paper's single strongest piece of evidence: M_LMQ+SFT_SHQ+RL at 56.66 vs M_base+SFT_SHQ+RL at 37.92, an 18.74 point gap. The largest advantages appear on the hardest benchmarks (AIME24: 45.21 vs 12.29; AIME25: 33.96 vs 16.04), directly demonstrating that early reasoning injection creates compounding advantages that survive and amplify through the entire training pipeline.

## Weaknesses

### Major
- **"Latent effects" claim is confounded with data repetition.** The paper finds M_LMQ (pretrained on D_LDQ∪D_SHQ) and M_LDQ (pretrained on D_LDQ only) perform nearly identically after pretraining (64.07 vs 64.09), but after SFT on D_SHQ, M_LMQ outperforms by +4.25 points (line 215). The paper attributes this to "latent potential" unlocked by SFT. However, M_LMQ already saw D_SHQ during pretraining—a straightforward alternative explanation is a double-exposure/familiarity effect, since the model simply sees identical data twice. The current design cannot distinguish "latent activation" from "the model benefits from seeing the exact same data in both phases." A proper test would require held-out high-quality data in SFT that neither model saw during pretraining.

- **Catch-up test is too weak to support the strong conclusion drawn.** The paper tests whether M_base can catch up by doubling SFT epochs (1→2) on the same 4.8M samples. When this fails to close the gap, the paper claims to have "proved" the catch-up hypothesis false, stating that "SFT cannot compensate for a weak foundation" (line 36, 183, 213). Doubling epochs on a fixed, moderate-sized SFT dataset is a narrow operationalization of "more intensive SFT." This test does not rule out that a larger or more diverse SFT dataset, or different SFT methodologies, could close the gap. The conclusion should be tempered to: "under the tested SFT configuration and data budget, catch-up does not occur"—not that it is impossible in principle.

### Minor
- **"Diversity" advantage in pretraining is confounded with unique sample volume.** The headline claim compares M_LDQ (268M unique samples) with M_SHQ (1.2M unique samples) at equal token budgets (80B tokens each, with D_SHQ repeated). The ~223× difference in unique sample count means the advantage could stem from seeing vastly more unique reasoning patterns rather than from broader domain diversity per se. The paper consistently pairs "scale and diversity" in its claims (e.g., "diversity and scale matter most during pretraining," line 25), which is appropriate, but the abstract and introduction emphasize "diversity" as the operative variable (e.g., "pretraining benefits most from broad diversity in reasoning patterns," line 9). A controlled ablation—subsampling D_LDQ to match D_SHQ's unique count, or scaling D_SHQ to match D_LDQ's unique count—would sharpen the attribution.

- **No variance or uncertainty estimates reported.** Every result is a point estimate, including comparisons where differences are small (e.g., M_LDQ 64.09 vs M_LMQ 64.07 in Table 1; 32.84 vs 32.99 in Table 8). The paper states some evaluations use 4 or 16 runs (line 148) but gives no standard deviations, confidence intervals, or significance tests. This makes it impossible to assess whether finer-grained findings reflect real differences or noise. (The large-gap results in Tables 1, 3, and 5 are likely robust despite this limitation.)

- **"Naive SFT scaling is harmful" is overclaimed.** Table 8 shows that doubling D_LDQ in SFT changes the average from 32.84 to 32.99—essentially flat. The paper highlights a -4.92 drop in math, but science increases (+4.43) and code increases (+1.59). Without error bars, it is unclear whether the math drop reflects meaningful degradation or noise. The defensible conclusion is that naive scaling of mixed-quality SFT data provides no benefit on average and may dilute reasoning-specific signal; the "actively harmful" framing (line 38, 253) is not clearly supported by the presented evidence.

- **Budget constraint (Eq. 2) is a conceptual framing device, not operationalized in comparable units.** The optimization framework imposes B = |D_pt| + |D_sft|, but pretraining uses 80B reasoning tokens while SFT uses 4.8M samples (token count not disclosed). The two quantities are in different units, so the budget constraint is never actually enforced in comparable terms.

### Trivial
None.

## Removed Points
- **Diversity never operationalized beyond domain proportions (Harsh Critic, Section-by-Section):** The critic states diversity is only characterized by domain composition and that within-domain diversity is uncharacterized. Domain composition is a standard and acceptable proxy; this is a generic demand for more analysis, not a specific flaw.
- **D_ALF uses answer length >4096 as a "crude proxy" for complexity (Harsh Critic, Section-by-Section):** Answer length filtering is a commonly used heuristic in the reasoning literature for isolating complex CoT traces. This is a reasonable design choice, not a weakness.
- **Proprietary data prevents independent reproduction (Harsh Critic, Missing Parts):** This is true of most large-scale industry pretraining studies. The critique is valid as a wish for open science but not as a paper weakness—the paper's contributions are scientific, not engineering artifacts. Moved to Nice-to-Haves.
- **Missing overfitting check (Harsh Critic, Missing Parts):** The critic claims the overfitting rebuttal is only weakly supported. However, Table 2 shows reasoning-pretrained models outperform baseline across ALL domains (not just reasoning), which directly contradicts the overfitting concern. The paper's evidence for this claim is actually adequate without the stripped Appendix B.
- **Strength Finder's "latent effect" strength:** The strength finder lists this as a core strength, but I have identified a confound (data repetition) that substantially weakens the clean interpretation. Retained in the strength list above but removed as an unqualified strength.

## Nice-to-Haves
- A small-scale reproduction on open data (e.g., a 1B model on public datasets) would significantly increase reproducibility and community trust.
- Disclose the token count of the 4.8M SFT samples to enable comparison with the pretraining token budget in Eq. 2.
- Reporting within-domain diversity metrics (e.g., problem-type coverage, solution-strategy breadth) beyond domain proportions would strengthen the diversity analysis.

## Novel Insights
The most significant insight from synthesizing the reviews is that the paper has a bifurcated claim structure: the large-gap findings (front-loading matters, diverse/scale data helps pretraining, quality helps SFT) are well-supported by strong experimental evidence, while the nuanced claims (latent effects, definitive catch-up refutation, active SFT harm) either have confounded designs or are overstated relative to the evidence. This asymmetry is itself valuable to flag—the paper's most important contributions are robust and should be preserved, but the secondary claims need to be substantially tempered or redesigned.

## Suggestions
1. **Address the latent effects confound:** Explicitly acknowledge the data-repetition alternative explanation and either soften the claim or run a control experiment using held-out high-quality data in SFT that neither model saw during pretraining.
2. **Add variance estimates** for the key comparisons, particularly the smaller-gap results. Reporting standard deviations or confidence intervals for the 4/16-run evaluations would substantially improve evidentiary quality.
3. **Temper the catch-up and SFT-scaling-harm claims** to match what the evidence supports. The catch-up test shows that doubling epochs on the same data fails—not that SFT categorically cannot compensate. The SFT scaling experiment shows flat average performance with a noisy domain-specific drop—not clear evidence of active harm.
4. **Disentangle the diversity vs. scale confound** in the pretraining comparison: explicitly acknowledge the unique-sample-count confound and either reframe the claim as "diversity and scale together drive pretraining gains" or add a control experiment.

## Score and Decision

**Calibration anchors used:**

| Path | Avg Score | Round | Comparison |
|------|-----------|-------|------------|
| Amuro & Char (8uXkyWFVum) | 4.20 | Round 1 (1.5–3.5) | Similar topic (PT/SFT relationship) but on a single 1B model; our paper is far more ambitious in scale and scope |
| Scaling Relationship (cijO0f8u35) | 5.25 | Round 1 (3.5–5.5) | Scaling laws study on GSM8K only; our paper has broader evaluation and more controlled design |
| Training Mice (eENHKMTOfW) | 6.00 | Round 1 (5.5–7.5) | Empirical study of LLM fine-tuning strategies (3B-7B from existing PT models); similar in being a large empirical study but our paper has more computational investment (PT from scratch) |
| Aioli (sZGZJhaNSe) | 6.25 | Round 1 (5.5–7.5) | Data mixing framework on 160M models; our paper has far larger experiments but also more interpretation issues |
| PolyPythias (bmrYu2Ekdz) | 6.50 | Round 1 (5.5–7.5) | Pretraining stability with 45 runs across 5 model sizes; proper variance reporting but narrower question |
| Synthetic continued pretraining (07yvxWDSla) | 8.00 | Round 1 (7.5–8.5) | Top-tier empirical study with clear claims and strong evidence; our paper does not match this bar due to confounded secondary claims |

**Round 1 bracket:** 5.5–7.5

**Final score determination:** The paper's core experimental design (pretraining from scratch, fully crossed 4×3 design, RL evaluation) is genuinely impressive and the main findings are clearly supported. However, the over-interpretation of several secondary claims (especially the confounded latent-effects finding and the overstated catch-up conclusion) prevents it from reaching the 7+ range. Compared to the calibration anchors, it is clearly stronger than "Training Mice" (6.0) in terms of experimental ambition and scope, but its interpretive weaknesses place it below "PolyPythias" (6.5) which had cleaner claims. A score of 6.0 reflects "borderline accept"—the core contributions are publishable and valuable, but the paper needs revisions to temper its overstated claims.

MY FINAL SCORE: <score>6.0</score>
MY FINAL DECISION: <decision>Accept</decision>