## Summary

This paper proposes PELICAN, a two-stage LLM-based tutoring framework combining collaborative cognitive diagnosis (successor-first question generation with an expert-assistant-verifier pipeline) with adaptive tutoring using a fast/slow-thinking strategy selection mechanism. The slow-thinking mode constructs a Simulated Teaching Tree to compare alternative dialogue paths when students face persistent difficulty. The paper reports simulated experiments on the Gaokao dataset (184 questions, LLM-simulated students at three cognitive levels) and a real human evaluation with 169 high school students (1335 tutoring reports).

## Strengths

- **Real human study with 169 students and 1335 tutoring reports (Table 6).** Running a genuine deployment with high school students is non-trivial and distinguishes this paper from the many LLM-tutoring papers that stop at automated or simulated evaluation. This is the paper's strongest evidence.

- **Well-motivated problem and clear architecture.** The core insight — that a one-size-fits-all LLM response fails students at different cognitive levels (Figure 1) — is genuine and important. The two-stage pipeline (diagnose first, then adapt) is educationally sensible, and the slow-thinking simulated teaching tree (Section 3.3.3) is an interesting attempt to operationalize dual-system theory for strategy selection.

- **The slow-thinking search mechanism is an interesting architectural concept.** Using LLM self-simulation to compare candidate teaching strategies before committing to one, with node expansion, dialogue simulation, and state evaluation (Eqs. 1–5), is a creative approach to strategy selection.

## Weaknesses

### Major

- **Unexplained 32% discrepancy between Table 2 and Tables 3/4 for the same method.** PELICAN reports R_coverage = **72.36** in Table 2 (main results) but R_coverage = **54.84** in Tables 3 and 4 (ablation and backbone studies). The F_frequency metric shows a similarly large gap (72.06 vs. 61.47). The paper offers no explanation. Since Tables 3 and 4 present PELICAN as the baseline within their own comparison, this inconsistency means either the ablation uses a different experimental protocol without stating it, or the results are not reproducible. Either reading undermines confidence in the entire quantitative evaluation. *(Verified against the paper: Table 2 line 305, Table 3 line 321, Table 4 line 332.)*

- **Abstract claims (+18.7% critical thinking, +22.4% task completion) are unsupported in the paper body.** These exact percentages appear only in the abstract. No table, figure, or section anywhere in the paper shows how they are derived. The closest reported metrics show far smaller improvements: Inspiration scores in Table 2 (4.21 vs. 3.99, ~5.5% relative) and success rate in Table 6 (86.8% vs. 85.2%, ~1.9% relative). Neither matches 18.7% or 22.4%. Whether these numbers are defined over a different metric, baseline, or subset cannot be determined from the presented evidence. This is a credibility problem for the paper's headline quantitative claim. *(Verified: the abstract appears at line 9; the numbers do not appear elsewhere in the paper.)*

- **The cognitive diagnosis evaluation (Table 1) lacks independently validated ground truth.** Table 1 reports Precision, Recall, and F1 for the diagnosed knowledge state \(\hat{K}_u\) against the "actual state" \(K_u\). However, Section 3.1 defines \(K_u\) as binary values assigned to nodes in a hierarchical knowledge structure. For the simulated students used in Tables 1–5, the ground truth \(K_u\) is defined by the same simulation initialization (Section 4.4: "we initialize three different cognitive levels"). The reported 94.31% F1 therefore measures the system's ability to reconstruct an internally-defined state, not an externally validated one. The number is uninterpretable without independent ground truth. *(Verified: Section 3.1 line 186, Section 4.4 line 336, Table 1.)*

- **The simulated evaluation pipeline (Tables 1–5) is circular.** The pipeline is: an LLM (GPT-4o) simulates a student's cognitive state → the system diagnoses this simulated state → the system tutors the simulated student → an LLM judge (GPT-based) evaluates the tutoring on dimensions like Inspiration and Suitability. Since every component is a GPT-family model, results may reflect self-consistency rather than genuine educational effectiveness. The human evaluation (Table 6) is a meaningful partial mitigation, but even there the majority of metrics (Appropriateness, Sentiment, Inspiration) are GPT-based, inheriting the same judge circularity. Only the "Success rate" column in Table 6 is an independent outcome measure, and there PELICAN's advantage over Free-Prompt is 1.6 percentage points. *(Verified: Section 4.1 line 278 specifies GPT-3.5 assistant and GPT-4o base model; Table 6 shows the metrics.)*

### Minor

- **In the ablation study (Table 3), removing both the diagnosis and slow-thinking modules achieves the highest Inspiration score (4.56 vs. 4.30 for full PELICAN).** The paper states that "removing any module degrades performance" but does not address why the ablated system outperforms PELICAN on this specific GPT-evaluated dimension. *(Verified: Table 3 line 320 shows w/o. Diagnosis & slow Inspiration=4.56 bolded; Section 4.3 line 310 text.)*

- **Margins in the human evaluation are thin on the primary independent metric.** PELICAN's success rate (86.8%) is only 0.3 percentage points above Stepwise (86.5%) and 1.6 pp above Free-Prompt (85.2%). The paper does not report whether these differences are statistically significant in the main text. *(Verified: Table 6 lines 431-437.)*

- **The slow-thinking mechanism is very shallow.** With M=1 (activated after one round of difficulty), k=2 iterations, and m=2 candidate strategies per leaf node, the Simulated Teaching Tree explores at most 4 leaf nodes. This calls into question whether the ~40% token cost (~230k tokens) is justified given the marginal improvements in the human evaluation. The paper does not provide a cost-effectiveness analysis. *(Verified: Section 4.1 line 278.)*

- **The expert-assistant-verifier pipeline checks consistency between two LLMs** (GPT-3.5 assistant, GPT-4o verifier). Agreement between them does not guarantee correctness — both models can share systematic blind spots. The paper acknowledges this as a "simple assumption" (Section 3.2) but provides no failure analysis quantifying how often both agree on a wrong answer. *(Verified: Section 3.2 lines 196-197.)*

### Trivial

None.

## Nice-to-Haves

- Reporting statistical significance for the human evaluation success rate differences.
- A cost-benefit analysis comparing the ~40% token overhead of slow thinking against simpler alternatives.
- A failure analysis examining cases where PELICAN's diagnosis or tutoring fails.

## Removed Points

These points are flagged to be removed; treat them with caution.

- *Criticism that "the evaluation uses simulated students and this is not clearly communicated"*: The paper does state in Section 4.4 "we initialize three different cognitive levels for the students," which signals the use of simulated students. The labeling could be clearer (e.g., in table captions) but the information is present. Moved to a contextual note rather than a standalone weakness.
- *Criticism about missing statistical significance for the human evaluation*: The paper states ANOVA analysis is provided in Appendix K.1, which is stripped by the parser. Per policy, penalizing missing appendix content is not appropriate.
- *Request for cost-benefit analysis*: This is a nice-to-have suggestion, not a weakness.
- *Speculation that Free-Prompt's 85.2% success rate suggests the task is too easy*: This is an unverifiable interpretation of the data.
- *Section-by-section notes about presentation (e.g., M=1 threshold, contribution vagueness)*: These are either addressed in the minor weaknesses above or are too granular to retain as separate items.
- *Generic strengths about "important problem"*: Removed as lacking specific evidence.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. Resolve the Table 2 vs. Tables 3/4 discrepancy: state explicitly whether different evaluation protocols, data subsets, or metric definitions were used, and report the correct numbers.
2. Either remove the unsupported abstract percentages (+18.7%, +22.4%) or trace them to specific tables with clear calculation methodology.
3. Clarify how the ground truth knowledge state \(K_u\) is established for the simulated students in the cognitive diagnosis evaluation, or re-label the diagnostic accuracy numbers as simulation-internal consistency measures.
4. Restructure the paper to make the human evaluation the primary evidence (which is a stronger position) and clearly label simulated experiments as synthetic demonstrations of the mechanism.

## Score and Decision

MY FINAL SCORE: <score>4.5</score>
MY FINAL DECISION: <decision>Reject</decision>

### Calibration Summary

All anchors retrieved across rounds:

| Path | Avg Score | Round | Itemized? | Comparison to PELICAN |
|---|---|---|---|---|
| iucVyVC8jQ (CD framework) | 3.25 | 1 | Yes | Still has real-data evaluation, but PELICAN's human study is stronger; however PELICAN's structural issues (table discrepancy, abstract claims) are more severe. PELICAN moderately above. |
| a2rSx6t4EV (EDU-RAG) | 2.33 | 1 | Yes | Simple RAG benchmark with limited novelty. PELICAN has significantly more method contribution. |
| M4fhjfGAsZ (KCQRL) | 5.33 | 1 | Yes | Clean, well-supported experiments across 15 models. PELICAN has weaker evaluation rigor and unsupported claims — clearly below this anchor. |
| NgaLU2fP5D (PSI-KT) | 6.75 | 1 | Yes | Strong methodological rigor and solid experiments. PELICAN does not approach this quality. |
| s6X3s3rBPW (CAT for LLMs) | 4.00 | 1 | No | Different focus (measuring LLM ability, not tutoring). Less relevant. |
| lXwhR7uci1 (TestAgent) | 4.75 | 2 | Yes | Similar mix of simulated + human eval, similar evaluation concerns. PELICAN's human study is larger but TestAgent has cleaner execution. Roughly comparable. |
| BzvVaj78Jv (Virtual Students) | 5.00 | 2 | Yes | Both have real human eval + LLM-based metrics. PELICAN's structural weaknesses are more severe than this paper's novelty concerns. PELICAN slightly below. |
| 7AS7vaVU8d (Personalized Story Eval) | 5.75 | 2 | No | Different domain (story evaluation). Less relevant. |
| ma4SUzeCLR (Math Word Problems) | 5.33 | 2 | No | Different task (question design support). Less relevant. |
| GtpubstM1D (Math Reasoning) | 5.71 | 2 | No | Different focus (math reasoning training). Less relevant. |

**Bracket**: Round 1 bracket was 4.0–5.0. **Narrowing**: The 5.00 anchor (virtual student paper) has comparable human evaluation scope but fewer structural integrity issues; the 4.75 anchor (TestAgent) has similar evaluation circularity concerns. PELICAN's combination of the table discrepancy, unsupported abstract claims, and circular evaluation pulls it below these anchors. The 3.25 anchor (CD framework) has more fundamental methodological problems. **Final placement**: 4.5 — above the 3.25 CD paper due to the valuable human study and interesting architecture, but below the 5.00 and 4.75 anchors due to the severity of the structural inconsistencies, and well below the 5.33 KT paper's clean empirical work.