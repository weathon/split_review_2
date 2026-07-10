Now I have sufficient calibration data. Let me write the final review.

## Summary

This paper presents a large-scale empirical study investigating when and how reasoning data should be introduced across the LLM training pipeline (pretraining → SFT → RL). By pretraining 8B models from scratch with reasoning datasets differing in diversity, quality, and scale, the authors find that front-loading reasoning data into pretraining creates durable advantages that persist and amplify through post-training. Key findings include an asymmetric principle (diversity matters in pretraining, quality in SFT), a latent effect where high-quality pretraining data shows benefits only after SFT, and evidence that naive SFT scaling can be harmful.

## Strengths

- **The research question is genuinely important and underexplored.** Whether reasoning data should be injected during pretraining or reserved for post-training is a practical question with high stakes given the cost of pretraining. The paper addresses a real gap, as most open work focuses on post-training and proprietary training recipes obscure these design choices. [favorability=13.40]

- **The experimental scope is ambitious.** End-to-end pretraining from scratch at 8B scale with controlled data conditions, followed by SFT and RL, allows a longitudinal perspective that tracks whether early advantages persist, amplify, or wash out — a scope most studies skip. [favorability=12.34]

- **The "latent effect" finding (Table 4) is clean and non-obvious.** The observation that $\mathcal{M}_{\text{LMQ}}$ and $\mathcal{M}_{\text{LDQ}}$ are nearly tied at pretraining (64.07 vs 64.09) but diverge after SFT (50.95 vs 46.70) genuinely suggests that high-quality data in pretraining can encode latent structure that only becomes useful after alignment. This is the paper's most distinctive contribution. [favorability=12.80]

- **The finding about harmful effects of naive SFT scaling (Table 8) is practically useful.** Showing that 2× data of the same mixed quality degrades math performance (-4.92%) while a tiny fraction (0.4%) of high-quality data improves performance contradicts the simple "more data is better" heuristic and provides actionable guidance. [favorability=12.90]

## Weaknesses

### Fatal
None.

### Major

- **The central comparisons for the asymmetric principle claim (diversity in pretraining, quality in SFT) are confounded by dataset size and repetition rate.** In pretraining, token count is controlled but sample uniqueness is not: $\mathcal{D}_{\text{SHQ}}$ (1.2M unique samples) is repeated ~66× while $\mathcal{D}_{\text{LDQ}}$ (268M unique samples) is mostly unique — so the advantage attributed to diversity could partly reflect reduced repetition effects. In SFT, all models are fine-tuned on 4.8M samples: for $\mathcal{D}_{\text{SHQ}}$ this means ~4 epochs, while for $\mathcal{D}_{\text{LDQ}}$ this covers <2% of the data once. The observed differences therefore mix dataset composition, size, and training epochs. The paper acknowledges the repetition (line 93: "When a reasoning dataset is small, it is repeated") but does not discuss this confound or its implications for the "diversity vs. quality" attribution. [favorability=2.30]

- **The "catch-up" experiment is too narrow to support the strong claim that "SFT cannot compensate for a weak foundation."** Only one SFT dataset ($\mathcal{D}_{\text{SHQ}}$) and one intervention (2× epochs) were tested. The paper's broader conclusion (abstract: "proving that SFT cannot compensate for a weak foundation") overstates what the evidence supports, which is more precisely stated in the main text as "cannot be fully replicated by simply scaling the SFT phase" (line 213). [favorability=-0.16]

### Minor

- **No data decontamination analysis is reported.** The training datasets ($\mathcal{D}_{\text{LDQ}}$ from Nemotron-Pretraining-SFT-v1, $\mathcal{D}_{\text{SHQ}}$ from Guha et al. 2025) contain public math and code problems that may overlap with evaluation benchmarks (GSM8K, MATH-500, AIME24/25, HumanEval, MBPP, MMLU). Given precise percentage claims on these benchmarks, the absence of contamination analysis is a gap. [favorability=0.80]

- **No uncertainty estimates.** None of the tables report variance, confidence intervals, or statistical significance. Since each configuration was run once (understandable given the compute cost), it is unclear whether small differences between close configurations (e.g., 64.09 vs 64.07) are meaningful or within noise. The paper treats all differences as significant. [favorability=1.23]

- **The headline "19% average gain" is drawn from a single favorable comparison.** The most heavily advertised number compares $\mathcal{M}_{\text{LMQ}} + \text{SFT}_{\text{SHQ}} + \text{RL}$ (the best configuration) against $\mathcal{M}_{\text{base}} + \text{SFT}_{\text{SHQ}} + \text{RL}$ (the worst), and the RL phase was only run on these two models. The generality of RL-phase conclusions is limited since $\mathcal{M}_{\text{LDQ}}$ and $\mathcal{M}_{\text{SHQ}}$ were not included. [favorability=0.15]

- **Minor notation inconsistency.** Equation 2 uses sample counts ($|\mathcal{D}_{\text{res}}^{\text{PT}}| + |\mathcal{D}_{\text{res}}^{\text{SFT}}|$) as the budget constraint, while the experiments control token count (80B tokens in pretraining, 4.8M samples in SFT). [favorability=2.25]

### Trivial
None.

## Nice-to-Haves

- Disentangle diversity from sample uniqueness by training $\mathcal{M}_{\text{LDQ-subset}}$ on a random 1.2M-sample subset of $\mathcal{D}_{\text{LDQ}}$ with matching repetition.
- Run the RL phase on at least one more model (e.g., $\mathcal{M}_{\text{LDQ}}$) to test whether compounding gains generalize beyond the LMQ configuration.
- Add contamination analysis (e.g., n-gram overlap statistics between training and evaluation sets).
- Reframe the catch-up conclusion to match what was tested more precisely.

## Removed Points

These points are flagged to be removed, treat them with caution:

- **Weakness about the 1.2B model experiment being in the appendix (Table 14):** The parser strips appendix content from all papers; this data exists in the original submission. Removed per rule (missing appendix).
- **Weakness about "first systematic study" claim being contradicted by cited works:** The paper explicitly discusses Cheng et al. 2024, Liang et al. 2025, and Ai et al. 2025 and differentiates its contribution (systematic variation across both phases). The "first" claim is about the specific scope and is defensible.
- **Generic/speculative weaknesses from the harsh critic's section-by-section sweep:** e.g., "the paper treats all differences as significant" (absorbed into the "no uncertainty" point above), "the 19%/11%/15% are not from a clean factorial design" (absorbed into the repetition confound point above), and concerns about the data description lacking factor isolation (same confound issue).
- **Strengths about the problem being "important" or "ambitious" without specific evidence:** These were retained because they are specific and evidenced.
- **The harsh critic's "Strengthening the Paper on Its Own Terms" section:** These are suggestions, not weaknesses, and are moved to Nice-to-Haves.

## Novel Insights

None beyond the paper's own contributions. The reviews confirm the significance of the latent effect and SFT scaling findings while correctly identifying the confound between repetition rate and diversity as the primary limitation.

## Suggestions

1. Disentangle diversity from sample uniqueness by training $\mathcal{M}_{\text{LDQ-subset}}$ on a random 1.2M-sample subset of $\mathcal{D}_{\text{LDQ}}$ matching $\mathcal{D}_{\text{SHQ}}$'s size and repetition pattern.
2. Add contamination analysis — at minimum, report n-gram overlap statistics between training and evaluation sets for the key benchmarks.
3. Run RL on at least one more model (e.g., $\mathcal{M}_{\text{LDQ}}$) to test whether compounding gains generalize.
4. Reframe the catch-up and asymmetric principle conclusions to match the precision of what was actually tested.

## Score and Decision

**Calibration anchors:**

| Path | Avg Score | Round | Itemized | Comparison |
|---|---|---|---|---|
| KIPJKST4gw.md | 7.25 | R1 | Yes | Very similar topic (training stage for code data → reasoning). Weaknesses include confounded token counts, no significance tests — comparable issues but my paper's weaknesses have milder favorability ratings. |
| 1hQKHHUsMx.md | 6.75 | R1 | Yes | About pretraining data's role in reasoning. Weaknesses include narrow scope, no cross-validation. My paper has stronger experimental scale and milder weaknesses. |
| GtpubstM1D.md | 5.71 | R1 | Yes | Math reasoning training stages. More polarized reviews (8,1,3,8,8,6,6) with several very negative weaknesses (-4.07, -2.95). My paper's weaknesses are substantially milder. |
| 3OyaXFQuDl.md | 7.00 | R2 | Yes | Compute-optimal sampling for reasoning. Weaknesses go as low as -3.95 (missing baselines), -1.64. My paper's weaknesses are milder. |
| 5HCnKDeTws.md | 6.75 | R2 | Yes | Scaling laws for finetuning. Weakness favorabilities mostly positive with one at -1.01. Comparable weakness profile to my paper but different topic. |

**Round 1 bracket:** 5.5–7.5, with the most topically similar anchors at 6.75–7.25.  
**Round 2 narrowing:** My paper's weakness favorability profile (lowest at -0.16, all others positive 0.15–2.30) is strictly better than every anchor in the 6.75–7.25 range, which all contain weaknesses scoring below -1.0. Combined with strength favorabilities (12.34–13.40) comparable to the 7.25 anchor, the paper sits at or above the 7.0 mark. The primary limiting factor is the repetition confound (favorability 2.30 — the model rates it as relatively mild), which tempers the strongest claims but does not invalidate the core findings.

**Final score: 7.0** — clear accept. The paper makes a genuine contribution through its large-scale investigation of an important question, with several novel findings (latent effect, SFT scaling harms). The primary weakness (confounded comparisons for the asymmetric principle) is real but does not undermine the paper's core contributions; it should be addressed in revision through additional controls and more precise claims.

MY FINAL SCORE: <score>7.0</score>
MY FINAL DECISION: <decision>Accept</decision>