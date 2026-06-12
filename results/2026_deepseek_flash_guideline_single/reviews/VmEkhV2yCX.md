Now let me finalize my review by writing it out completely.

## Summary

This paper systematically studies how reasoning data—varying in scale, diversity, and quality—affects LLM performance when introduced at different stages (pretraining, SFT, RL). The authors pretrain 8B models from scratch for 1T tokens with different reasoning data configurations, then trace effects through SFT (fully crossed 4×3 design) and RL. They claim an asymmetric principle: diversity dominates in pretraining, quality dominates in SFT.

## Strengths

1. **Large-scale, systematic experimental design.** Pretraining 8B models from scratch across multiple data configurations with a fully crossed 4×3 SFT design is genuinely resource-intensive and rare in academic literature. The study provides a structured view of how reasoning data injected at different stages interacts.

2. **The "catch-up" experiment (Table 4) is clean and informative.** Showing that even doubling SFT epochs for $\mathcal{M}_{\text{base}}$ (34.01) does not match $\mathcal{M}_{\text{SHQ}}+\text{SFT}_{\text{SHQ}}$ (37.33) is a concrete, interpretable result that directly addresses an important practical hypothesis.

3. **The asymmetric principle, if confirmed, provides a practically useful heuristic.** The finding that pretraining benefits from broad/diverse data while SFT is quality-dominated gives practitioners a concrete framework for allocation decisions.

4. **The finding about SFT scaling harms (Table 8) is notable.** Showing that naively doubling mixed-quality SFT data degrades math reasoning (-4.92% points) while targeted high-quality additions help is a non-obvious result with direct practical implications.

## Weaknesses

### Major

1. **Headline numbers in the abstract are misleadingly framed.** The abstract states "19% average gain" for front-loading, but this traces to a single RL comparison (Table 3: $\mathcal{M}_{\text{LMQ}}+\text{SFT}_{\text{SHQ}}+\text{RL}$ at 56.66 vs $\mathcal{M}_{\text{base}}+\text{SFT}_{\text{SHQ}}+\text{RL}$ at 37.92 = 18.74 absolute points). It is neither an average (single comparison) nor a percentage gain (it is percentage points). Similarly, "11% average gain" for diversity in pretraining corresponds to a 9.11-point gap (Table 1), and "15% average gain" for quality in SFT corresponds to a 13.45-point gap (Table 5). The abstract's numbers are inconsistently rounded upward and presented as broader averages than the evidence supports. While the underlying results are meaningful, the abstract gives a materially inflated impression.

2. **The diversity-vs-quality comparison in pretraining confounds diversity with dataset size, repetition rate, and source.** $\mathcal{D}_{\text{LDQ}}$ (268M samples, broad distribution) and $\mathcal{D}_{\text{SHQ}}$ (1.2M samples, narrower distribution) differ on at least four confounded dimensions: dataset size (223× difference), domain coverage, quality level, and source provenance. The paper attributes $\mathcal{M}_{\text{LDQ}}$'s superiority to "diversity," but the gap could equally be driven by the sheer scale difference or by memorization artifacts from repeating the small $\mathcal{D}_{\text{SHQ}}$ ~67–223× during pretraining. The paper acknowledges the repetition (line 93) but does not discuss its potential downsides. The central "diversity-over-quality in pretraining" claim is not uniquely supported by the design.

3. **The "latent effect" claim has an unaddressed alternative explanation.** The paper finds $\mathcal{M}_{\text{LMQ}}$ and $\mathcal{M}_{\text{LDQ}}$ have nearly identical pretraining scores (64.07 vs 64.09) but $\mathcal{M}_{\text{LMQ}}$ pulls ahead by 4.25 points after SFT on $\mathcal{D}_{\text{SHQ}}$, attributed to "latent value" of high-quality data. However, $\mathcal{M}_{\text{LMQ}}$'s pretraining mix includes $\mathcal{D}_{\text{SHQ}}$ (since $\mathcal{D}_{\text{LMQ}} = \mathcal{D}_{\text{LDQ}} + \mathcal{D}_{\text{SHQ}}$), so $\mathcal{M}_{\text{LMQ}}$ has already seen the SFT data distribution during pretraining. "Distribution matching" is a simpler explanation for the post-SFT advantage, and the paper does not discuss or control for this.

4. **The RL phase—which the headline 19% number depends on—is a single comparison.** Only two models ($\mathcal{M}_{\text{base}}+\text{SFT}_{\text{SHQ}}+\text{RL}$ and $\mathcal{M}_{\text{LMQ}}+\text{SFT}_{\text{SHQ}}+\text{RL}$) reach the RL phase. While the reported gap is large, the paper's central claim about pipeline-level strategy rests on this single data point. Without RL results for $\mathcal{M}_{\text{SHQ}}$ and $\mathcal{M}_{\text{LDQ}}$, the generality of the RL-stage advantage is unknown.

### Minor

5. **No variance or uncertainty estimates.** All results are single-point estimates with no error bars, confidence intervals, or significance tests. While single-run evaluation is common at this scale, the absence of variance information makes it difficult to assess the reliability of smaller gaps (e.g., Table 6: 80/20 vs 90/10 differs by 0.1 overall; Table 8: $\text{SFT}_{\text{ALF}}$ vs $\text{SFT}_{\text{ALF}}^*$ differs by 0.38).

6. **The budget-constrained formulation (Eq. 2) is not operationalized in the experiments.** The paper formalizes a trade-off as $\mathcal{B} = |\mathcal{D}_{\text{res}}^{\text{PT}}| + |\mathcal{D}_{\text{res}}^{\text{SFT}}|$ but never actually varies allocation of a fixed budget. Instead, the experiments compare different data *sources* at each phase. This gap between the formalism and the experimental design should be acknowledged.

### Trivial

- None that survive filtering.

## Nice-to-Haves

- A controlled experiment holding dataset size fixed (e.g., subsampling $\mathcal{D}_{\text{LDQ}}$ to 1.2M samples for comparison with $\mathcal{D}_{\text{SHQ}}$) would disentangle scale from diversity.
- A "latent effect" control using a different high-quality SFT dataset (not $\mathcal{D}_{\text{SHQ}}$) would distinguish distribution-matching from genuine latent benefits.
- Additional RL comparisons (at least $\mathcal{M}_{\text{LDQ}}+\text{SFT}_{\text{SHQ}}+\text{RL}$ and $\mathcal{M}_{\text{SHQ}}+\text{SFT}_{\text{SHQ}}+\text{RL}$) would substantiate the pipeline-level claims.
- Clarifying all percentage units (pp vs %) and stating which comparisons each headline number comes from would improve transparency.

## Removed Points

- Criticism about "the paper reports M_res as an average of three qualitatively different models" — The paper acknowledges this explicitly (line 102: "representing the average score across"), and many papers report aggregate averages. This is a standard practice.
- Criticisms from the "Section-by-Section Notes" that are speculative or about the paper's scope (e.g., "the paper does not operationalize the budget constraint in experiments" downgraded from section note to minor weakness since it's acknowledged as a gap between formalism and execution).
- "The D_ALF dataset is underexplained" — minor presentational issue that doesn't threaten any core finding.
- The critic's Strengthening section items — moved to Nice-to-Haves since they are constructive suggestions, not flaws.

## Novel Insights

None beyond the paper's own contributions. The harsh critic's primary value is identifying confounds and presentation issues in the paper's argumentation, rather than contributing novel analytical insights.

## Suggestions

1. Revise the abstract to report numbers with clear units (percentage points vs percent) and to state which comparisons they refer to rather than labeling them as "average gains."
2. Add a controlled pretraining experiment that subsamples $\mathcal{D}_{\text{LDQ}}$ to match $\mathcal{D}_{\text{SHQ}}$'s size, or explicitly discuss the scale-diversity confound as a limitation.
3. Address the latent effect confound directly: either run a control SFT with a dataset not present in any pretraining mix, or explicitly acknowledge distribution matching as an alternative.
4. Expand the RL evaluation to cover at least the $\mathcal{M}_{\text{SHQ}}$ and $\mathcal{M}_{\text{LDQ}}$ backbones.
5. Add variance estimates for key comparisons, particularly for AIME and MATH-500 where multiple runs are already performed.

## Score and Decision

Let me calibrate using the human-reviewed anchors.

**Round 1 bracket:** 4.0–6.0, based on comparison to:

| Anchor Paper | Avg Score | Comparison |
|---|---|---|
| "At Which Training Stage Does Code Data Help LLMs Reasoning?" | 7.25 | More tightly controlled, cleaner comparisons, accepted; this paper has more confounds |
| "Advancing Mathematical Reasoning in Language Models" | 5.71 | Similar scale of experiments, similar confound issues; slightly higher due to released model |
| "Amuro and Char: Pre-Training and Fine-Tuning Relationship" | 4.20 | Similar question (pretraining-finetuning interaction) but less experimental rigor; this paper is stronger empirically |
| "How Can Language Models Learn from Mistakes on Grade-School Math Problems" | 6.75 | Cleaner experimental design, clearer claims; stronger paper |
| "What Kind of Pretraining Data Do LLMs Rely on When Doing Reasoning?" | 6.75 | Novel methodology, clean analysis; stronger paper |

The paper sits between the 4.20 (Amuro/Char) and the 5.71–6.75 range — its experimental effort is substantial but the confounds and overclaiming pull it below the cleaner studies.

**Final score:** 5.5 — The paper has real empirical contributions (systematic large-scale study, clean catch-up experiment, useful asymmetry finding) but the evidence is weakened by confounded comparisons and the abstract overstates the headline numbers. The paper would benefit from revision that addresses these issues.

MY FINAL SCORE: <score>5.5</score>
MY FINAL DECISION: <decision>Reject</decision>