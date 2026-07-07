Here is my final consolidated review.

---

## Summary

PELICAN proposes a two-stage adaptive tutoring framework: first, collaborative cognitive diagnosis uses a successor-first strategy with an expert-assistant-verifier pipeline to assess the student's knowledge state; second, a dual-system (fast/slow thinking) approach selects teaching strategies from a strategy pool, with slow thinking activating a simulated teaching tree when the student faces persistent difficulties. Evaluations are conducted on the Gaokao dataset (184 questions). The paper includes both simulated experiments (LLM tutor + LLM simulated student) and a human evaluation with 169 high school students.

## Strengths

- **Well-motivated two-stage architecture.** The framework design — first diagnosing the student's cognitive state via a successor-first method that leverages knowledge hierarchies, then adapting tutoring accordingly — follows sound pedagogical principles and is clearly described (Section 3.2). The expert-assistant-verifier pipeline for question accuracy is a reasonable engineering contribution.

- **Real human evaluation is valuable and rare.** The deployment with 169 students and 1335 tutoring reports (Section 4.6, Table 6), with documented ethical safeguards including informed consent from parents/guardians, is a genuine strength that sets this work apart from papers that evaluate only in simulation.

- **Strategy distribution analysis provides useful internal validation.** Figure 4 shows that the system uses more analogies for low-cognition students and more questioning for high-cognition students, which is consistent with intuitive pedagogical expectations.

## Weaknesses

### Fatal
None.

### Major

- **Abstract claims (+18.7%, +22.4%) are unsupported by any reported data.** These numbers appear only in the abstract (line 9). They do not appear in any table, and the paper does not specify which baseline or metric they refer to. In the closest available data: Table 2's "Inspiration" (the only proxy for critical thinking) shows PELICAN at 4.21 vs Free-Prompt at 2.42 — a ~74% relative difference, not 18.7%. In Table 6 (human eval), PELICAN's success rate (86.8%) vs the best baseline (86.5%) is a 0.3 percentage point difference, not 22.4%. These abstract claims cannot be verified from the presented evidence and are likely overstated or incorrectly computed.

- **Numerical inconsistency between Table 2 and Table 3.** PELICAN's own reported performance differs dramatically between the main results (Table 2) and the ablation study (Table 3): R_coverage drops from 72.36 to 54.84 (a 32% relative difference), and F_frequency drops from 72.06 to 61.47. The paper provides no explanation for this discrepancy. Without knowing whether the experimental conditions changed (different problems, different student configurations, different evaluation protocols), a reader cannot determine which set of numbers reflects the system's true performance or whether the ablation comparisons are valid against the main results.

- **Primary experiments use an LLM-simulated student without adequate acknowledgment of limitations.** The main experiments (Tables 1–5) involve an LLM tutor interacting with a simulated student whose knowledge state is initialized (line 336: "we initialize three different cognitive levels for the students"). This evaluates how well GPT-4o prompts a GPT-based simulated student, not real educational effectiveness. The paper never explicitly acknowledges this as a limitation, nor does it clearly distinguish between simulated and human evaluation results when presenting findings. The human evaluation (Table 6) partially mitigates this concern, but the simulated experiments produce the more dramatic numbers and the paper relies on them for its central claims.

### Minor

- **GPT-based self-evaluation on subjective dimensions is unvalidated.** The "Inspiration" dimension in the GPT-based evaluation (Table 2) is used to support claims about critical thinking. This is GPT-4o evaluating outputs from the same model family on a subjective pedagogical quality. The paper provides no validation that these scores correlate with human judgments, no inter-annotator agreement, and no operational definition of critical thinking in the tutoring context.

- **Human evaluation improvements are very small.** In Table 6, PELICAN's success rate (86.8%) is only marginally above Stepwise (86.5%) and Free-Prompt (85.2%). The paper claims results "exhibit strong consistency" with GPT-based evaluation but provides no correlation coefficients or agreement statistics to quantify this claim.

- **Student response categorization is not validated.** The method relies on classifying student responses into five categories (Section 3.3.1), but the paper does not explain or evaluate how reliably the LLM performs this classification.

- **Slow-thinking threshold M=1 makes fast thinking vestigial.** Slow thinking activates after just one dialogue round on a subtask (line 278), meaning the expensive simulated-tree search runs almost immediately. This design choice, which effectively eliminates the fast-thinking phase for most interactions, deserves justification.

- **Limited dataset and no failure analysis.** The Gaokao dataset contains only 184 questions (line 266), which limits generalizability. The paper also does not discuss any failure modes or cases where PELICAN performs worse than simpler methods.

- **Cost efficiency not discussed.** At ~580k tokens per session with GPT-4o (line 278), this is an expensive system per-student per-problem, but no comparison to baseline costs is provided.

### Trivial
None.

## Nice-to-Haves

- Replace or supplement GPT-based evaluation of subjective dimensions (Inspiration, Suitability) with human ratings or validated instruments for at least a subset of data.
- Provide quantitative agreement statistics between GPT-based and human evaluation results rather than the qualitative claim of "strong consistency."
- Discuss failure modes and conditions where the slow-thinking tree search may produce worse outcomes than simpler strategies.
- Report the 18.7% and 22.4% abstract numbers with explicit citation to the table, baseline, and metric they derive from, or remove them.

## Removed Points

These points were flagged in the input review but are removed for the following reasons:

1. **"Related work is thin / doesn't engage with ITS, Bayesian Knowledge Tracing literature"** — Removed per rule: missing related works cannot be confirmed without external sources, and the paper's scope is specifically LLM-powered tutoring.
2. **"Knowledge hierarchy extraction details in Appendix"** — Removed because the appendix is stripped by the parser; this content exists in the original submission.
3. **"No variance/significance for simulated experiments"** — Removed as factually incorrect: Table 2 reports standard deviations, and ANOVA is referenced in the (stripped) appendix.
4. **"LLaMA3.1-8B results glossed over"** — Removed: the paper correctly qualifies "perform well on the hard metrics" (R_coverage, Frequency), not the GPT-based subjective metrics.
5. **"Free-Prompt and Stepwise are weak baselines"** — Removed: comparison against simple baselines alongside published methods (Socratic, Bridge-Based) is standard practice.

## Novel Insights

One observation emerges from synthesizing the review inputs that is not present in the paper itself: the strategy distribution data (Figure 4) shows that most strategies (Suggestion, Confirmation, Correction, Open Question, Closed Question, Simplification, Decomposition) have **identical** percentages across all three cognitive levels. Only Explanation (32/33/30) and Analogies (22/18/15) vary. This suggests the system's adaptation is actually quite narrow — the "personalization" comes almost entirely from modulating how much to explain vs. use analogies, while the remaining strategies are deployed at fixed rates regardless of student ability. This observation cuts against the paper's claim of dynamic adaptation and is worth investigating further.

## Suggestions

1. **If the abstract's +18.7% and +22.4% numbers can be derived from specific data**, cite the exact table, baseline, and metric. Otherwise, remove or correct them. An unsupported abstract claim is an unacceptable presentation error that undermines the entire paper.
2. **Explain the Table 2 vs. Table 3 discrepancy.** State clearly whether the ablation experiments use a different problem subset, different student configurations, or different evaluation protocols. If the numbers are not comparable, say so explicitly.
3. **Reframe the simulated experiments** as a sanity check on system behavior (not effectiveness) and clearly label them. Move the human evaluation to the primary position and make it the basis for the paper's central claims.
4. **Validate the GPT-based evaluation** by reporting correlation with human ratings on a held-out subset, or replace it with human evaluation for subjective dimensions.

## Score and Decision

The paper proposes a sensible framework and includes a valuable human evaluation. However, it is seriously undermined by three major issues: **(a)** the abstract makes quantitative claims (+18.7%, +22.4%) that cannot be traced to any reported data; **(b)** the paper's own reported results are numerically inconsistent between the main experiments and the ablation study (R_coverage differs by 32%); and **(c)** the primary experiments evaluate an LLM tutoring a simulated student without adequate acknowledgment of this limitation, while the human evaluation shows only marginal improvements. These problems collectively prevent the paper from supporting its advertised claims.

**Score: 3.5 | Decision: Reject**

### Calibration Anchors

| Path | Avg Score | Round | Itemized | Comparison |
|------|-----------|-------|----------|------------|
| /home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/iucVyVC8jQ.md | 3.25 | 1 | Yes | Cognitive diagnosis framework; negatives were more severe (-7 to -9 range) than this paper's (-4 to -6), suggesting this paper is slightly stronger |
| /home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/s6X3s3rBPW.md | 4.00 | 1, 2 | Yes | Adaptive LLM testing paper; comparable positive weight range (~+4) but fewer evidential issues |
| /home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/lXwhR7uci1.md | 4.75 | 2 | No | Adaptive human assessment; higher score reflects stronger experimental validation |
| /home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/M4fhjfGAsZ.md | 5.33 | 1, 2 | Yes | Knowledge tracing with LLMs; stronger positives (+5.90 applied contribution) and weaker negatives (~-4 to -6) |
| /home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/1tZLONFMjm.md | 4.00 | 3 | Yes | Gaokao LLM evaluation; negatives included -9.64 (poor articulation), similar positive range (~+3 to +5) |
| /home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/M1CCA6UF0y.md | 4.25 | 2 | No | Math question generation; less topically relevant |
| /home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/ryKrRCbcCX.md | 3.50 | 2 | No | LLM uncertainty review; less topically relevant |

**Bracket determination.** Round 1 bracketing placed the paper between 3.5 and 5.5 by similarity to cognitive diagnosis/education papers. Itemized comparison showed the paper's negative-weighted items (-5.99, -5.90, -4.77, -4.58, -4.04) were more severe than the 5.33 anchor's (-6.38, -4.65) but less severe than the 3.25 anchor's (-8.86, -7.41). The positive weights (+3.95, +3.38, +3.20) were comparable to the 4.00 anchor's range. The unsupported abstract claims and cross-table inconsistency are unique problems not seen in any anchor. Round 2/3 narrowing confirmed no anchor above 4.5 shared this combination of evidential issues. The final score of **3.5** reflects that the paper has a well-motivated framework and real human data, but the evidence presentation problems (unsubstantiated abstract claims, unexplained numerical inconsistencies) are too severe for acceptance.

MY FINAL SCORE: <score>3.5</score>
MY FINAL DECISION: <decision>Reject</decision>