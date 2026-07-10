Now I have all the information needed. Here is my final consolidated review:

---

## Summary

This paper develops a theoretical framework for understanding when data curation (pruning) helps or hurts in high-dimensional binary classification. Using a Gaussian generative model with label shift and a ridge regression estimator, the authors derive exact scaling laws for test error under both label-agnostic and label-aware pruning rules. The central result (Theorem 2) shows that "keep hard" is optimal when the generator is strong (ρ→1) and "keep easy" when the generator is weak (ρ<1), under an excellent pruner. The paper connects these findings to recent LLM reasoning results (LIMO/s1 vs. Sun et al.) and presents experiments on ImageNet.

## Strengths

- **Clean theoretical setup for a timely problem.** The paper defines a mathematically precise framework — high-dimensional binary classification with a Gaussian generative model, a pruning oracle that filters by difficulty/correctness, and a ridge regression estimator — that captures the core tension between "more is more" and "less is more." The choice of label shift (w_g ≠ w_*) as the primary source of generator weakness is natural and connects well to model collapse and synthetic data settings.

- **Theorem 2 is genuinely informative.** The result that "keep hard" is optimal when the generator is strong (ρ → 1) and "keep easy" is optimal when the generator is weak (ρ < 1) — both under an excellent pruner (ρ_* → 1) — provides a clean formal statement of an intuition that has remained heuristic in the LIMO/s1 literature. The phase-transition framing is valuable and isolates the key variable (generator quality ρ) to show how it flips the optimal strategy. This is the paper's strongest single contribution.

- **Reconciliation of LIMO/s1 with Sun et al. (Section 4.2).** The observation that the same LLM can be a strong generator on average AIME questions but a weak generator on hard AIME questions, and that this explains why "less is more" holds in the former case and "more is more" in the latter, is genuinely insightful. The paper is transparent that these results are aggregated from existing literature.

## Weaknesses

### Major

- **ImageNet experimental description is too sparse relative to claims made.** The paper states "we empirically confirm our theoretical predictions on ImageNet" (contribution list) and "We validate these theoretical claims with empirical results on ImageNet" (abstract). However, Section 4.3 devotes only ~15 lines of text (plus figure captions) to the ImageNet experiments. The main text does not specify: the model architecture used (ResNet? ViT?), how multi-class ImageNet labels are converted to the binary classification setting, how "keep easy" and "keep hard" are operationalized on image data (by softmax confidence? logit margin?), the training procedure (optimizer, learning rate, epochs, batch size), the value of d (feature dimension), or error bars. While Appendix B (stripped from the review copy by the parser) likely contains additional details, the main text description is not sufficient to assess these experiments, which the paper itself frames as central empirical support.

- **The synthetic experiments (Section 4.1) compare "keep hard" only against random pruning, not against "keep easy."** Since the core theoretical result (Theorem 2) is about when KH vs. KE is optimal, the experiments should validate this directly. Showing that an informed strategy beats an uninformative random baseline is a much weaker test. The paper also does not report the value of d used in the synthetic experiments (only n=100 and n=5000 are stated), making it unclear whether the experiments operate in the asymptotic regime the theory assumes.

### Minor

- **The model collapse experiment (Section 4.3) is described extremely briefly** — three sentences and a figure caption in the main text. The setup (model architecture, dataset, number of rounds, what "keep hard" criterion is used) is not specified. While Appendix C (stripped) likely contains details, the main text description is insufficient to assess this claim, which is listed as a contribution ("We show analytically that data curation can avert model collapse").

- **The claim of providing "rigorous justification" for LIMO/s1 (contribution list) slightly overstates** what is actually a qualitative consistency check. The LLM discussion (Section 4.2) is presented as interpretation of existing results, which is valuable, but the paper's own framing implies a stronger evidential basis than the paper delivers. The abstract more accurately frames this as a "principled explanation."

- **The squared loss for binary classification (Eqn 2) is standard in the high-dimensional statistics / RMT literature** but is not the loss used in the systems the paper claims to explain (LLMs trained with cross-entropy, ImageNet models trained with softmax cross-entropy). The paper does not discuss whether the results would generalize to other losses. This is noted briefly in the limitations section but deserves more explicit treatment.

### Trivial

None.

## Nice-to-Haves

- The paper would benefit from quantifying the magnitude of the "less is more" benefit (how much better is p < 1 than p = 1 in the optimal regime) rather than only showing it qualitatively.
- A discussion of how the label-aware curation model (Eqn 6) compares to the verifier-based oracles used in LIMO/s1 (which check answer correctness rather than providing sign(x^T w_o) labels) would strengthen the connection to practice.

## Removed Points

These points from the input review are flagged for removal — treat them with caution:

- **"Theorem 1's key components are deferred to the appendix"** — Removed because the paper follows standard practice for theory papers (stating main results with proof sketch in main text, full proof in appendix). The appendix was stripped by the parser; this is not a weakness of the paper's content.
- **"No comparison to existing data curation heuristics"** — Removed because the paper explicitly scopes itself as a theoretical framework ("our goal is not to propose another heuristic curation method, but rather to build a principled theoretical framework"). This demand is outside the paper's stated scope.
- **"Model collapse connection (strength #4)"** — Removed as a strength because the full analytical details are deferred to the appendix and the main text treatment is too thin to be a standalone strength.
- **"The paper uses squared loss without adequate justification (framed as critical issue)"** — Downgraded from "critical issue" to Minor (kept above). Squared loss is standard in this line of theoretical work (Firdoussi et al. 2024, Feng et al. 2025) and enables the closed-form RMT analysis. It is a modeling choice worth discussing, not a fatal flaw.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. Add a synthetic experiment that directly compares KE vs. KH in the two regimes (strong generator and weak generator) to directly validate Theorem 2. This would address the most significant gap in the current empirical validation.
2. Either expand the ImageNet experimental description to include full protocol details in the main text, or honestly scope down the empirical claims to acknowledge that the ImageNet results are preliminary/illustrative.
3. Reframe the LLM contribution from "rigorous justification" to "interpretation consistent with the theory" in the contribution list.

## Score and Decision

**Calibration anchors consulted (all rounds):**

| Path | Avg Human Score | Round | Itemized? | Comparison |
|------|----------------|-------|-----------|------------|
| nSDOkm0SKo.md (Financial market NN) | 1.00 | R1 | No | Unrelated topic; strong reject baseline |
| EOPLy80bBm.md (Disentangling Data Pruning) | 3.00 | R1 | Yes | Similar topic but weaker contribution (survey-oriented, no novel result like Theorem 2). Current paper is stronger. |
| Bk13Qfu8Ru.md (Severing Spurious Correlations) | 3.80* | R1 | No | Data pruning with spurious correlations; different focus |
| 9ccZzuix2D.md (Distilling Knowledge in Pruning) | 5.33 | R1 | No | Empirical KD-based pruning paper |
| I9Dsq0cVo9.md (Maximizing Synthetic Data with RMT) | 5.50 | R2 | Yes | Most similar anchor: RMT theory for synthetic data pruning. Had more severe experimental-detail criticisms (favorability -3.66 vs. current paper's 0.12) but was accepted. Current paper has more novel theory. |
| FT4gAPFsQd.md (How Sparse Can We Prune) | 6.00 | R1 | Yes | Theory paper with phase transitions; had strong experimental validation. Current paper has less complete experiments but more novel theoretical result. |
| 93XT0lKOct.md (Data Pruning by InfoMax) | 6.00 | R1 | Yes | Empirical method paper; different type of contribution |
| fxv0FfmDAg.md (DRoP) | 7.33 | R2 | Yes | Strong empirical + theory paper with comprehensive experiments. Current paper has weaker empirical validation. |
| Fk5IzauJ7F.md (Candidate Label Set Pruning) | 8.00 | R1 | No | Partial-label learning; different subfield |

*\*The avg_score field showed 3.80 but individual scores were 10,5,5,8 (avg 7.00). This likely reflects a display issue; treating with caution.*

**Round 1 bracket:** 5.0–7.0. The paper's novel theoretical contribution places it well above the 3.00 anchor, but its incomplete empirical validation prevents it from reaching the 7.33 anchor level.

**Round 2 narrowing:** Compared to the closest anchor (I9Dsq0cVo9, "Maximizing Synthetic Data with RMT," avg 5.50, accepted), the current paper has a genuinely more novel theoretical contribution (Theorem 2 vs. extending prior work) and its weaknesses carry higher (less harmful) favorability ratings (most near-neutral vs. -3.66 for the anchor's experimental criticism). However, it falls short of the 7.33 anchor (DRoP) which has comprehensive experimental validation.

The favorability model rates the current paper's strengths very high (9.81–12.73) and its weaknesses as mostly near-neutral (0.11–2.14) to very mildly negative (-0.49 to -0.99). This profile is consistent with a paper whose theoretical contribution is genuine but whose empirical execution lags behind its claims.

**Final score: 6.0** — borderline accept. The theoretical contribution (especially Theorem 2) is novel and valuable enough to warrant publication. The primary issues are the gap between the paper's strong empirical claims and the sparse experimental descriptions in the main text, and the missing KH vs. KE comparison in the synthetic experiments. These are addressable in a revision by either providing full experimental details (which likely exist in the stripped appendix) or by scoping down the claims to match what is actually demonstrated.

MY FINAL SCORE: <score>6.0</score>
MY FINAL DECISION: <decision>Accept</decision>