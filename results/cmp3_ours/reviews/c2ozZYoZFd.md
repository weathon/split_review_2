Now let me write the final consolidated review.

**Bracket Analysis:** After comparing with calibration anchors, the plausible range is 5.5–6.5. Papers in this band with similar structure (re-analysis of published claims) include "On the Inadequacy of Similarity-based Privacy Metrics" (6.00, Reject), "Re-evaluating Retrosynthesis Algorithms" (5.50, Reject), "To the Cutoff... and Beyond?" (6.75, Accept), and "Is Memorization Actually Necessary?" (4.40, Reject). The current paper is stronger than the Memorization re-analysis (which had weaker evidential documentation) and comparable to the Privacy Metrics critique. I anchor the final score at **6.0**.

---

## Summary

This paper presents a detailed re-examination of "Turning Up the Heat: MIN-P Sampling for Creative and Coherent LLM Outputs" (Nguyen et al., 2024), a high-profile ICLR 2025 Oral paper. Through four lines of analysis—human evaluations, NLP benchmarks, LLM-as-a-Judge evaluations, and community adoption claims—the authors argue that the original paper's evidence does not support its claims of min-p's superiority. The paper also contributes a Best-of-N hyperparameter analysis methodology for fairly comparing methods with different degrees of hyperparameter tuning, and presents six general lessons for rigorous empirical ML research.

## Strengths

1. **Concrete, well-documented critique.** Each methodological flaw is traced to specific data, code, or public correspondence: the omission of one-third of human evaluation data (Section 2.1), incorrect statistical inference and failure to correct for multiple comparisons (Section 2.2, Table 1), selective reporting in LLM-as-a-Judge scores (Section 4.3), and unsubstantiated GitHub adoption figures that were retracted (Section 5). This specificity gives the critique weight that a generic methodological essay would lack.

2. **Genuine methodological contribution: Best-of-N hyperparameter analysis (Section 3.1).** The idea of subsampling an equal number of hyperparameters across methods and computing maximum achievable performance is simple, principled, and broadly applicable beyond this case study. The 9-model, 31-temperature, 6-hyperparameter sweep (~6000 A100-hours) credibly demonstrates that min-p's advantage vanishes when hyperparameter tuning volume is controlled.

3. **Correct and pedagogically valuable statistical re-analysis.** The demonstration that the original paper's claim of "consistent" superiority collapses under both a Bonferroni correction (1/12 tests significant) and an Intersection-Union Test (largest p = 0.378) is squarely on point. The distinction between "test whether min-p is better on average" (pooled) and "test whether min-p is better across all settings" (IUT) is clearly explained.

4. **Honest about scope.** Section 6 acknowledges that conclusions are based on the evidence re-analyzed and that new evidence could change them. The paper does not overclaim to have proven min-p is bad; it correctly claims that the original paper's evidence does not support its conclusions.

## Weaknesses

### Fatal
None.

### Major

1. **The "blueprint" framing oversells the generality of the contribution.** The paper is titled "A MIN-P BLUEPRINT FOR MORE RIGOROUS SCIENCE," and the abstract/introduction promise "a blueprint for conducting more meticulous science." However, Section 6's six lessons (e.g., "apply statistical tests rigorously," "demand full data transparency," "ensure methodological clarity") are well-established best practices taught in introductory statistics courses and articulated in existing reproducibility guidelines (Pineau et al., 2021; Belz et al., 2021; Biderman et al., 2024—several of which the paper cites). The lessons are valuable *as illustrations* through the case study, but the paper does not advance the *methodological principles themselves* beyond what is already standard knowledge. The one genuinely novel component—the Best-of-N analysis—is one of six lessons, not the whole. This mismatch between the framing (a general blueprint) and the actual contribution (a thorough case study with methodological observations) is the paper's most significant weakness. The paper would be more accurate and harder to fault if framed primarily as a detailed case study, with the lessons offered as observations rather than a novel blueprint.

### Minor

2. **The "incorrect value" claim (Section 2.4) lacks traceable evidence.** The paper states that "the average score of min-p at p=0.05 and temperature T=2 is reported as 7.80, but based on the authors' publicly posted data, we believe the correct numerical value should be 5.80" (line 117). No calculation, data table, or derivation is provided to support this specific accusation. If correct, it is important, but the current documentation is insufficient for independent verification. This should either be fleshed out with a clear calculation trace or presented with appropriate hedging.

3. **The selective reporting accusation (Section 4.3) relies on non-permanently-archived evidence.** The claim that "Table 3(b) reported the higher of two scores for min-p but the lower of two scores for top-p" is based on a "publicly shared Telegram link" from the first author (line 193). While the paper cannot be faulted for the original paper's lack of transparency, this serious accusation rests on evidence that has not been independently archived through standard channels. The paper should either archive this evidence permanently or present the claim as suggestive rather than conclusive.

4. **The LLM-as-a-Judge indirect comparison criticism (Section 4.1) is overstated.** The paper criticizes the original authors for comparing all samplers against a common baseline (basic, τ=1.0) rather than through direct pairwise comparisons, citing non-transitivity of LLM preferences. However, indirect comparison against a fixed baseline is standard practice in evaluation frameworks (Chatbot Arena's Elo ratings, AlpacaEval's baseline). While the non-transitivity concern is theoretically valid, the paper does not explain why min-p specifically would be disadvantaged by it. The force of this criticism relies on a general concern about the evaluation paradigm rather than a specific flaw in this study's design.

5. **The new human evaluation (Section 2.4) involved multiple simultaneous methodological changes.** The paper lists six differences between the original and new study (implementation, participants, hyperparameters, reading time, text, rubric) but does not discuss how these changes confound interpretation. The null result could be attributable to any combination of these changes rather than min-p's lack of advantage. This does not invalidate the finding but should be acknowledged.

6. **Task mismatch between benchmark evaluation and original claims.** The NLP benchmark evaluation (Section 3) uses math/science reasoning tasks (GSM8K, GPQA), while the original paper's contributions emphasized creative writing—a domain where sampling diversity may matter differently. The paper does not address how this mismatch affects the generalizability of its benchmark conclusions.

### Trivial
None.

## Nice-to-Haves
- Discuss how the lessons relate to and extend existing reproducibility frameworks (e.g., ML Reproducibility Checklist).
- Provide the re-analysis code and data in a permanent repository.
- The Best-of-N hyperparameter space (6 values per sampler) is small; while the resampling procedure mitigates this, a larger sweep would strengthen the analysis.

## Removed Points

These points were raised in the input review but removed or merged per the filtering rules:

- **"Pooling focus on high diversity setting is contestable"** — Removed. The paper explicitly justifies this choice with three reasons (min-p's claimed advantage in high diversity, authors' guidance, top-p's poorly chosen low-diversity hyperparameter).
- **"Best-of-N small hyperparameter space"** — Demoted to Nice-to-Haves. The paper addresses this via resampling.
- **"No connection to existing reproducibility checklists"** — Moved to Nice-to-Haves. Scope creep beyond the paper's goals.
- **"No raw data/code alongside manuscript"** — Moved to Nice-to-Haves. The appendix was stripped by the parser; code may already be present.
- **"GitHub adoption claim benefit from direct quotes"** — Removed. Minor presentation nitpick.
- **"Single case study limits generalizability"** — Merged into Major #1 (blueprint framing), as the core issue is the framing mismatch, not the case study design itself.

## Novel Insights

None beyond the paper's own contributions. The input review's most useful observations (framing mismatch, thin evidential claims, confound acknowledgment) are refinements of the paper's own communication rather than novel external insights.

## Suggestions

1. **Retitle and reframe** as a case study rather than a "blueprint." Something like "A Re-examination of Min-P Sampling: Lessons in Methodological Rigor from a High-Visibility Publication" would better match the actual contribution.
2. **Substantiate or soften the two thin evidential claims:** provide a calculation trace for the 7.80 vs. 5.80 discrepancy (Section 2.4), and archive the Telegram-based evidence or present it as suggestive (Section 4.3).
3. **Acknowledge confounds** from simultaneous methodological changes in the new human evaluation (Section 2.4).
4. **Address the task mismatch** between math benchmarks (GSM8K, GPQA) and creative writing claims.

## Score and Decision

**Score: 6.0 | Decision: Borderline Accept**

**Calibration Anchors Used:**

| Paper | Avg Score | Round | Comparison |
|---|---|---|---|
| Is Memorization Actually Necessary for Generalization? | 4.40 | R1 | Weaker than current paper: less specific evidence, more pushback from reviewers |
| On the Inadequacy of Similarity-based Privacy Metrics | 6.00 | R1 | Similar structure (critique paper) but current paper has stronger evidence documentation |
| To the Cutoff... and Beyond? (Data Contamination) | 6.75 | R1 | More novel framing but similar "exposing flaws" contribution; current paper's framing is weaker |
| Re-evaluating Retrosynthesis Algorithms | 5.50 | R2 | Similar re-analysis structure; current paper has richer evidence |
| Reevaluating Theoretical Analysis Methods for Optimization | 5.75 | R2 | Similar "re-evaluation" framing; current paper has more concrete actionable findings |
| Rethinking Graph Classification Benchmarks | 6.00 | R2 | Similar benchmark critique; current paper has more direct societal impact |

**Round 1 bracket:** 5.5–6.5. **Round 2 narrowing:** Anchored against the Privacy Metrics paper (6.00, Reject) and Data Contamination paper (6.75, Accept). The current paper is between these: its core case study is thorough and its Best-of-N methodology is a genuine contribution, but the framing overreach and two insufficiently documented evidential claims prevent it from reaching the acceptance level of the Data Contamination paper. Final score: **6.0**.

MY FINAL SCORE: <score>6.0</score>
MY FINAL DECISION: <decision>Reject</decision>