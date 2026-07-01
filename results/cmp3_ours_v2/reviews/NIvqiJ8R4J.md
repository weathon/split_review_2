Now I have enough calibration data. Let me finalize the review.

**Bracket determination:** After comparing with anchor papers — EDU-RAG (2.33, clearly weaker), Dual-Fusion CD (3.25, somewhat weaker), TestAgent (4.75, similar domain/methodology with analogous strengths and weaknesses), Students Rather Than Experts (5.00, similar concerns about simulation-based evaluation), and Automated KC Annotation (5.33, cleaner applied work) — I place PELICAN between 4.0 and 5.0.

**Final narrowing:** The paper's real human evaluation (169 students) is a genuine strength that many comparable papers lack. However, the abstract number mismatch and M=1 threshold issue are weaknesses not present in the TestAgent or KC Annotation papers. Compared to TestAgent (4.75), PELICAN is slightly weaker due to clearer flaws in claim-evidence alignment. Final score: **4.0**.

---

## Summary

PELICAN proposes a two-stage LLM-based tutoring framework: collaborative cognitive diagnosis (successor-first knowledge state assessment with an expert-assistant-verifier pipeline) followed by adaptive tutoring with fast/slow-thinking strategy selection (simulating dialogue paths to pick optimal teaching strategies). Evaluated on the Gaokao dataset (184 math questions) with both simulated-student experiments and a real-world study with 169 high school students.

## Strengths

1. **Well-motivated problem and clear architecture.** The paper correctly identifies that standard LLM responses are one-size-fits-all (Figure 1) and proposes a sensible two-stage separation of diagnosis from tutoring. The successor-first diagnostic strategy and the expert-assistant-verifier pipeline for question correctness are technically reasonable design choices.

2. **Real human evaluation with 169 students.** The paper reports a real-world experiment with 169 high school students and 1,335 tutoring reports (Section 4.6, Table 6). This goes beyond purely simulated evaluations and provides some ecological validity that many papers in this space lack.

3. **The slow-thinking simulation tree is a novel mechanism.** Using simulated dialogue paths to evaluate teaching strategies before deploying them is a legitimate methodological contribution, even if its practical value relative to cost remains unproven.

## Weaknesses

### Major

1. **The primary experimental evaluation uses LLM-simulated students, but this is not clearly stated in the main text, and the abstract's headline numbers come from this simulation.** The paper's core quantitative results (Tables 1–4, Section 4.2) are obtained by having an LLM play the role of the student with a pre-defined knowledge state. The paper mentions "Design details of the student role (Appendix G)" but never explicitly discloses in the main body that the "students" are simulated. When evaluated on real students (Table 6), PELICAN's success rate (86.8%) is essentially tied with Sepwise (86.5%) — a 0.3 percentage point difference. The large margins in Tables 1–2 are artifacts of the simulation, not evidence of real-world efficacy. The paper presents simulated results as its primary evidence and the human study as a secondary validation, which inverts the evidentiary priority.

2. **The abstract's claimed improvements (+18.7% critical thinking, +22.4% task completion) do not clearly map to any reported metric in the paper.** The "Inspiration" score in Table 2 (PELICAN 4.21 vs. next-best Socratic 3.99) shows a ~5.5% relative increase, not 18.7%. The $R_{\text{coverage}}$ metric (72.36 vs. 59.81 for Free-Prompt, ~21% relative) could be the source of the 22.4% figure, but this measures *coverage of non-mastered knowledge points*, not "task completion rates." The actual task completion rate in the human evaluation (Table 6) shows PELICAN at 86.8% vs. Sepwise at 86.5%. The abstract's numbers are not grounded in clearly identified metrics or baselines.

3. **The slow-thinking mechanism is trivially triggered (M=1) and consumes 40% of total tokens, with the cost-benefit trade-off unaddressed.** The paper reports that slow thinking activates after M=1 round (Section 4.1), meaning after a single dialogue round on a sub-task the system switches to the expensive slow-thinking mode (~230k tokens, ~40% of ~580k total). With M=1, the "fast thinking" branch is nearly meaningless — the system almost always escalates to the full simulation tree. The human evaluation shows PELICAN's success rate at 86.8% vs. Sepwise's 86.5%; even if this margin were significant, it is hard to justify a massive token cost increase. No cost-benefit analysis or ablation over M values is provided.

4. **Ablation results contradict the claimed benefits of key modules.** Table 3 shows that removing both Diagnosis AND slow thinking yields the *highest* Inspiration score (4.56 vs. 4.30 for full PELICAN) and comparable Reliability (4.21 vs. 4.44). The paper asserts this "emphasizes the key roles" of these modules, but the data show the modules primarily improve coverage metrics ($R_{\text{coverage}}$, Frequency) while not consistently improving subjective quality ratings. This pattern warrants explanation that the paper does not provide.

### Minor

1. **The human evaluation reports only point estimates without confidence intervals or effect sizes.** Table 6 shows success rates and subjective ratings without uncertainty quantification. The paper mentions "ANOVA analysis in Appendix I" but does not present any significance testing or confidence intervals in the main text, making it impossible to assess whether reported differences are meaningful.

2. **The strategy distribution analysis (Figure 4) shows minimal adaptation by cognitive level.** Most strategies (Suggestion, Confirmation, Correction, Open Question, Closed Question, Simplification, Decomposition) show nearly identical percentages across low, medium, and high cognitive levels. Only Analogies shows meaningful variation (22%, 18%, 15%). This undercuts the claim that the system substantially adapts its strategy selection to cognitive level.

3. **GPT-based evaluation likely suffers from self-enhancement bias.** The system uses GPT-4o as its backbone (Section 4.1), and the evaluator is also GPT-based for the five subjective dimensions (Suitability, Logic, Inspiration, Reliability, Overall). LLM judges tend to rate content from the same model family more favorably. The paper does not discuss or attempt to control for this.

4. **The successor-first diagnostic propagation is asymmetric.** The paper states: "If v is mastered (value 1), all its prerequisite nodes are also updated to 1" (line 194). It does not discuss the reverse case — if a prerequisite is not mastered, whether dependent (successor) nodes should also be marked as not mastered. This asymmetry in the propagation logic is not addressed.

### Trivial

None.

## Nice-to-Haves

- A cost-benefit analysis comparing PELICAN's token consumption (~580k tokens/session) against baselines.
- Long-term learning measurement (retention, transfer) beyond immediate problem-solving success.
- Analysis of failure cases — when PELICAN fails (13.2% on real students), understanding why would be informative.
- An ablation over different values of M (slow-thinking threshold) to justify the M=1 choice.

## Removed Points

These points are flagged to be removed; treat them with caution:
- "Related work is thin / does not cite enough work (e.g., Bayesian Knowledge Tracing, deep knowledge tracing)" — specific missing references cannot be confirmed as valid omissions per review policy.
- "The knowledge hierarchy construction process is not described in the main text" — the paper defers this to Appendix B, which was stripped by the parser.
- "The ten strategies are not named or described in the main text" — the paper defers this to Appendix E, which was stripped by the parser.
- "The selection score function (Equation 5) conflates two separate desiderata" — this is a methodological observation about a design choice with a tunable hyperparameter, not a clear flaw.
- "No analysis of per-question or per-student variance" — a useful addition but not a core weakness for the claims made.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. Restructure the paper to make the human evaluation the primary evidence, with simulated experiments positioned as sanity checks. Clearly label simulated vs. real results throughout.
2. Trace the abstract's headline numbers (+18.7%, +22.4%) to specific metrics and baselines, or remove unsubstantiated numerical claims.
3. Add confidence intervals or statistical significance tests to the human evaluation results.
4. Justify the M=1 threshold or present an ablation over M values to show the effect of slow-thinking activation frequency.
5. Report token costs alongside success rates for all methods and discuss the cost-benefit trade-off.

## Score and Decision

When calibrating against anchor papers from the human-review corpus:
- **EDU-RAG** (avg 2.33): Simple RAG benchmark with poor presentation and minimal contribution. PELICAN is clearly stronger.
- **Dual-Fusion Cognitive Diagnosis** (avg 3.25): Significant methodological concerns about missing baselines and scalability. PELICAN is somewhat stronger.
- **TestAgent** (avg 4.75, scores 5,3,5,6): LLM-based adaptive testing with simulated + human evaluation; very similar strengths and weaknesses. PELICAN has a larger human study but additional claim-evidence issues.
- **Students Rather Than Experts** (avg 5.00, scores 3,6,5,6): LLM-based student simulation with GPT evaluation bias concerns. Similar simulation validity issues.
- **Automated KC Annotation** (avg 5.33, scores 5,5,6): Cleaner applied work with consistent improvements across 15 models.

Round-1 bracket: [4.0, 6.0]. Round-2 narrowing to [4.0, 5.0] based on comparison with TestAgent and Students Rather Than Experts. Final calibrated score: 4.0.

PELICAN addresses a well-motivated problem with a coherent architecture and includes a valuable real human evaluation. However, the primary quantitative evidence comes from a simulated-student setup whose limitations are not transparently disclosed, the abstract makes unsubstantiated numerical claims, the slow-thinking mechanism's design choice (M=1) undermines the fast-slow framing, and the ablation results do not consistently support the claimed importance of the key modules. These issues prevent acceptance in its current form.

MY FINAL SCORE: <score>4.0</score>
MY FINAL DECISION: <decision>Reject</decision>