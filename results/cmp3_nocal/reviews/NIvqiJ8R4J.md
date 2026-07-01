## Summary

This paper proposes PELICAN, a two-stage LLM-based tutoring framework. In the first stage, the system diagnoses a student's cognitive state via collaborative dialogue with a successor-first knowledge traversal and an expert-assistant-verifier pipeline. In the second stage, it dynamically selects tutoring strategies using a "fast thinking" (prompt-based) and "slow thinking" (tree-of-thoughts simulation) dual-system approach. Experiments are reported on the Gaokao dataset (184 questions) and a human evaluation with 169 students.

## Strengths

1. **Human evaluation with 169 students (Section 4.6, Table 6).** The paper reports a real-world experiment collecting 1,335 tutoring reports. Conducting human evaluation at this scale is genuinely labor-intensive and provides the most ecologically valid evidence in the paper.

2. **The simulated teaching tree for strategy selection (Section 3.3.3).** The idea of simulating dialogue paths under different strategies before picking one, with a depth-penalty scoring mechanism (Eq. 5), is a reasonable application of planning/rollout to tutorial strategy selection.

## Weaknesses

### Fatal
None.

### Major

1. **Unsupported headline claims in the abstract (+18.7% critical thinking, +22.4% task completion).** These two percentage values appear **only** in the abstract. They are never defined, never referenced in any experiment section, and cannot be derived from any table in the paper:
   - The closest metric to "critical thinking" in the paper is "Inspiration" (Table 2). PELICAN scores 4.21 vs. Socratic's 3.99 — a 5.5% relative improvement, not 18.7%.
   - The closest to "task completion" is the success rate in the human evaluation (Table 6): PELICAN 86.8% vs. Free-Prompt 85.2% — a 1.9% relative improvement, not 22.4%. If $R_{coverage}$ (a process metric, not task completion) is used from Table 2, (72.36−59.81)/59.81 ≈ 21.0%, which is close but does **not** measure task completion. No table defines or supports either claimed figure. This is a serious reporting failure; claims in the abstract must be traceable to evidence in the body.

2. **Main experiments (Tables 1–4) use LLM-simulated students without clear acknowledgment or discussion of limitations.** The paper never explicitly states that Tables 1–4 involve simulated rather than real students, nor does it include a limitations section. The context makes this clear — Section 4.6 is labeled "Human Evaluation" and says "We **further** conducted a real-world experiment," and Section 4.4 states "we initialize three different cognitive levels for the students" — but the main results are presented without flagging the implications: the tutor (GPT-4o), the simulated student (GPT-4o), and the automated evaluator (GPT-4o) are from the same model family. Diagnostic accuracy (Table 1) compares an estimated knowledge state against a ground truth that was initialized by the experimenters in the simulated student. This creates a closed-loop consistency check that cannot, on its own, support conclusions about real educational outcomes.

3. **Human evaluation shows only marginal improvements over simple baselines.** In Table 6, PELICAN's success rate (86.8%) effectively ties with Stepwise (86.5%) — a baseline that simply asks step-by-step questions. The 0.3 percentage point gap is minimal, and no statistical significance is reported in the main text (ANOVA is deferred to the stripped appendix). Without significance testing, we cannot conclude that PELICAN outperforms even the simplest baseline on the primary outcome measure with real students.

### Minor

1. **Suspiciously small standard deviations in GPT-based evaluation (Table 2).** The GPT-4o-based evaluations report standard deviations as low as ±0.003 on a 5-point Likert scale (e.g., Suitability ±0.003, Inspiration ±0.002, Overall ±0.003). These are implausibly tight for any rating-based evaluation and are not explained — the paper does not state how many evaluation runs were performed or how these SDs were computed.

2. **Ablation anomaly (Table 3).** Removing both diagnosis and slow thinking ("w/o Diagnosis & slow") yields an Overall score of 4.11, which is *higher* than removing only slow thinking ("w/o slow" = 4.08). This counterintuitive result is not discussed. Additionally, the $R_{coverage}$ and Frequency values in Table 3 (43–61 range) are substantially lower than in Table 2 (72 for PELICAN), suggesting different experimental conditions that are not explained.

3. **Backbone ablation reveals Qwen-max outperforming GPT-4o on a key metric (Table 4).** Qwen-max achieves $R_{coverage}$ of 64.41 vs. GPT-4o's 54.84, yet the paper does not comment on this, even though it means a different backbone substantially outperforms the main experimental model on this coverage metric.

4. **Diagnosis mechanism under-specified (Section 3.2).** The validator's method for determining whether a student's response indicates mastery of a knowledge node is described in one sentence ("the validator checks student's response $r^t$ to determine the value of $v$"). The actual mechanism — presumably an LLM call with specific instructions — is not described.

5. **Simulated student success rates (Table 5) are lower than real student baseline success rates.** The simulated students succeed at 75–82.5%, while real students using the Free-Prompt baseline succeed at 85.2% (Table 6). This suggests the simulated students are not calibrated to real student behavior, further undermining the validity of the simulated experiments as predictors of real-world performance.

### Trivial

1. The "fast thinking" strategy selection (Eq. 1) is essentially an LLM prompt selecting from a strategy pool — described as a function call but not an algorithmic contribution. The simulated teaching tree uses $k=2$ iterations and $m=2$ candidate strategies per leaf, making it a very shallow search that is modest in scope.

## Nice-to-Haves

- Report the human evaluation with confidence intervals or effect sizes to establish whether PELICAN significantly outperforms Stepwise.
- Include a limitations section acknowledging the simulated-student experimental setup, the closed-loop nature of GPT-based evaluation, and the scope conditions of the human evaluation.
- Clarify who provided the subjective ratings in Table 6 (the students themselves, independent evaluators, or teachers).

## Removed Points

These points were flagged by the input review but are removed per the filtering rules:

- **"The paper overstates that existing research largely overlooks LLMs in personalized education"** (line 106) — The paper does cite Ding et al. 2024 and Liu et al. 2025 as examples of work on LLM tutoring, but frames them as overlooking cognitive state. This is a reasonable characterization of the gap, not an overstatement.

- **"No discussion of limitations"** — This is merged into Major weakness #2 rather than kept as a separate point.

- **"Code availability URL is '[here]' with no actual link"** — The Reproducibility Statement states the code is available via anonymous repository in supplementary materials. The placeholder link in the abstract is a formatting artifact of the anonymized PDF, not a genuine omission.

- **"The 184-question Gaokao dataset is small"** — Generic dataset size criticism not specific enough to harm the core claim.

- **"The strategy pool of 10 strategies is listed but not analyzed"** — The paper does analyze strategy distribution by cognitive level (Figure 4), partially addressing this.

- **"No error analysis or failure case discussion"** — Nice-to-have but not a core weakness for an empirical systems paper at this stage.

- **"Missing related works"** — Per rules, this cannot be included as the reviewer lacks external sources to confirm omissions.

- **Criticism about the paper not citing ToT/MCTS work** — Per rules, missing citations cannot be raised.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. **Remove or rigorously justify** the +18.7% and +22.4% abstract claims. If they come from an analysis not shown, add that analysis with clear mapping to a labeled table. Otherwise, remove the unsupported numbers.

2. **Explicitly label** the experimental condition for Tables 1–4 (i.e., "All experiments in this section use LLM-simulated students as described in Appendix G") and add a limitations paragraph discussing the closed-loop nature of the evaluation.

3. **Report statistical significance** for the human evaluation (Table 6). The current success rate gap of 0.3 pp over Stepwise is too small to interpret without confidence intervals or a test statistic.

4. **Explain** the suspiciously small standard deviations in Table 2 and the ablation anomaly in Table 3.

## Score and Decision

MY FINAL SCORE: <score>4.5</score>
MY FINAL DECISION: <decision>Reject</decision>