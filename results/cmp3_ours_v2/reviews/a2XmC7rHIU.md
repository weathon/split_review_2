## Summary

The paper introduces the Open Proof Corpus (OPC), a dataset of 5,062 human-evaluated LLM-generated mathematical proofs across 1,010 competition problems from sources like the IMO, USAMO, and Putnam. Using the OPC, the authors address three open questions: (1) the gap between natural language and formal proof generation, (2) how final-answer accuracy relates to proof correctness, and (3) the effectiveness of best-of-n selection strategies. They also fine-tune an 8B model on the OPC that achieves 88.1% judging accuracy, matching Gemini-2.5-Pro and approaching GPT-5.

## Strengths

1. **Largest human-evaluated proof dataset by a substantial margin.** The OPC's 5,062 proofs across 1,010 problems is genuinely the largest dataset of its kind. The paper convincingly shows that prior work is limited by small scale (Petrov et al.'s 6 problems, Mahdavi et al.'s <5% accuracy ceiling), outdated models, or lack of open-sourced data. This alone makes the paper a significant community contribution.

2. **Rigorously designed human evaluation pipeline.** The grading methodology (§3) is unusually thorough: a pilot phase with 35% double-grading to calibrate instructions (§3.3), built-in abstention and uncertainty flags (<3%), LLM-generated issue summaries with a bias check (§3.2), and ongoing monitoring of inter-judge consistency (~10% double-graded overall, 90.4% agreement). The care taken here is well above what is typical for comparable resources.

3. **Multifaceted utility demonstrated.** The paper does not just release a dataset — it produces empirically interesting findings (formal/informal gap, final-answer vs. proof correctness misalignment, best-of-n scaling) and a fine-tuned judge model (OPC-R1-8B), demonstrating value for evaluation, analysis, and training within the same paper.

4. **Transparent contamination analysis (§5.6).** The paper runs a control experiment feeding ground-truth solutions to judge models and measuring the accuracy difference; the changes are small and non-significant. This is a clean way to bound one specific contamination risk, more rigorous than the typical hand-waving in dataset papers.

## Weaknesses

### Fatal

None.

### Major

1. **The "human-level judging" claim compares inter-rater agreement with model accuracy.** The 90.4% human figure in Table 2 is the inter-rater agreement rate on double-graded proofs (line 173: "judges agreed on the proof's correctness in 90.4% of cases"), while GPT-5's 90.8% is accuracy against human-provided labels on a held-out test set. These are different quantities: inter-rater agreement measures label reliability (how often two judges agree), while model accuracy measures match against a reference label set. The paper acknowledges this mismatch briefly (line 246: "the human baseline is not measured on the test subset, but rather on all double-graded proofs" and justifies it by saying the test samples are "uniformly drawn from the OPC"). This justification is too brief for what is arguably the paper's most prominent claim. The comparison is not invalid, but the paper should either (a) measure human accuracy on the exact same test set, or (b) explicitly frame the result as "GPT-5 matches the human agreement rate" rather than "GPT-5 matches human performance." This is a significant evidential gap for the claim that gets top billing in the abstract and §5.2.

2. **Adaptive problem selection not transparently discussed.** The paper describes (lines 99-101) that problem selection was dynamically adjusted during construction: competitions were chosen to "align with our target of roughly 50% model accuracy," and "model performance was actively monitored to ensure that the selected problems remained appropriately challenging." Furthermore, "each day, problem prioritization was adjusted based on ongoing performance metrics ... and progress towards the specific conclusions we aimed to draw from the dataset." The abstract presents "the OPC generally consists of 43% correct proofs" as a descriptive statistic without caveating that this balance is a direct consequence of the curation policy. The paper's limitations section (§6) does not mention this. This does not undermine the dataset's utility — many datasets are constructed with target distributions — but transparent disclosure is needed for proper interpretation by downstream users.

### Minor

3. **MathArena conditional analysis has a selection confound for cross-model comparisons.** In §5.4, the analysis conditions on correct final answers (line 103: "we only retained solutions with a correct final answer"). Since each model's correct-answer set may differ in difficulty (some models may solve harder problems correctly, others may only get easy ones right), the cross-model comparison of proof correctness — e.g., o3's 59.5% vs. Gemini-Pro's 77.6% — could partially reflect differences in which problems each model solves correctly rather than differences in proof-writing quality. The overall finding (final-answer accuracy overestimates proof correctness) is robust — a gap exists for all four models — but the specific cross-model comparison is noisier than presented.

4. **Insufficient bias check for LLM issue summaries.** The paper introduced automated issue summaries by o4-MINI during grading (line 115). To check for bias, the paper evaluates whether the agreement rate between o4-MINI-as-judge and human graders changed before vs. after their introduction. This tests whether the LLM judge's relationship to humans changed, but it does not test whether the human labels themselves shifted due to the summaries. The claim that "no bias was introduced" (line 115) is not fully supported by the analysis provided. A more targeted check would compare label distributions before and after the intervention, or have a subset of proofs graded both with and without summaries.

### Trivial

5. **Naming inconsistency.** Table 1 lists "GEMINI-PRO" while elsewhere the model is "GEMINI-2.5-PRO" or "Gemini-Pro," which could cause confusion for readers trying to verify results.

## Nice-to-Haves

- The uncertainty-acknowledgment analysis (§5.1) already notes that o3 generated 109 of the 114 acknowledgments, but a fuller breakdown by model would be informative.
- The Best-of-n bug (footnote on line 353) should clarify whether it affected the 60-problem or 134-problem subset.

## Removed Points

The following points from the input review are removed with justification:
- "The 43% figure is an artifact, not a finding" — The paper presents this as a descriptive statistic about dataset composition (standard practice), not as an independent empirical finding about LLM capabilities. However, the adaptive selection disclosure concern remains in Major weakness #2.
- "Model comparisons are confounded by adaptive selection" — All models are evaluated on the same problem set, so relative rankings are unaffected. Generalizability concerns are standard for any curated dataset.
- Claims that the MathArena confound invalidates cross-model comparisons entirely — The paper's overall conclusion (gap exists) is robust; only the precision of cross-model comparison is affected (now Minor weakness #3).
- Section-by-section notes about figure caption formatting, cost definitions, and other minor presentation issues that are either addressed in Appendix C.4 or are standard practice.

## Novel Insights

The harsh critic's analysis provides a useful lens for evaluating the paper's methodological rigor, particularly the insight that the human baseline comparison mixes inter-rater agreement with model accuracy — a distinction that the paper elides but that meaningfully affects the strength of its central claim. The critic's identification of the adaptive selection-disclosure gap is also well-grounded in the paper's own description of its construction process. These observations sharpen the evaluation without overstating their severity.

## Suggestions

1. Re-frame the human baseline comparison in §5.2 and the abstract: either measure human accuracy on the test set, or explicitly state that GPT-5's 90.8% matches the human inter-rater agreement rate of 90.4%, without claiming "human-level performance."
2. Add a subsection to §4 or §6 transparently discussing the adaptive selection process and its implications for interpreting the 43% correctness figure and the dataset's composition.
3. Acknowledge the limitation of the issue-summary bias check in §3.2.
4. Add a caveat to §5.4 about the conditional selection confound when comparing proof correctness across models.
5. Resolve the GEMINI-PRO / GEMINI-2.5-PRO naming inconsistency in Table 1.

## Score and Decision

**Calibration Anchors (all rounds):**

| Anchor | Avg Score | Round | Comparison |
|--------|-----------|-------|------------|
| StepProof (proof verification) | 3.25 | R1 | Much weaker — fundamental methodological issues, small scale, poor evaluation. OPC is clearly stronger. |
| U-MATH (university math benchmark) | 5.25 | R1 | Uses LLM-as-judge (not human eval), smaller (1,100 problems). OPC's human evaluation is more rigorous. |
| Putnam-AXIOM (Putnam benchmark) | 5.80 | R1 | Smaller (236 problems), no human evaluation of proofs. OPC is larger and more thorough. |
| SciBench (college science benchmark) | 5.60 | R2 | LLM-as-judge, smaller scale. OPC compares favorably. |
| MathCheck (reasoning checklist) | 6.25 | R2 | Similar scope but OPC has more data and human evaluation. |
| Omni-MATH (Olympiad benchmark) | 6.75 | R2 | Comparable scale but uses LLM-as-judge with known reliability issues. OPC's human evaluation is cleaner but OPC has its own methodological issues. |
| ImProver (proof optimization) | 6.75 | R2 | Different task (proof optimization vs. dataset). Comparable quality tier. |
| MathGAP (proof complexity eval) | 7.00 | R2 | Cleaner methodology (synthetic data with controlled complexity) but narrower scope. |
| MUSTARD (theorem/data synthesis) | 7.33 | R2 | Synthetic data generation; different sub-area. Comparable quality. |
| LEGO-Prover (theorem proving) | 7.50 | R2 | Formal theorem proving system; different sub-area. |
| miniCTX (formal theorem proving) | 8.00 | R1 | Cleanest methodology (formal verification eliminates human evaluation concerns) but different sub-area. |

**Round 1 bracket:** 6.0–7.0. The OPC is clearly stronger than 5-range benchmark papers (has real human evaluation, larger scale, more downstream uses) but has methodological issues that prevent it from reaching the 8+ tier of papers like miniCTX.

**Narrowing:** Comparing against Omni-MATH (6.75, Accept) — which has similar scale but uses LLM-as-judge (a weakness flagged by its reviewers) — the OPC's human evaluation is more rigorous, but its human baseline comparison issue is a countervailing concern. MathCheck (6.25) and SciBench (5.60) are weaker. MathGAP (7.00) has cleaner methodology but is limited to synthetic arithmetic word problems. The OPC sits between MathCheck (6.25) and MathGAP (7.00), closest to Omni-MATH (6.75).

MY FINAL SCORE: <score>6.5</score>
MY FINAL DECISION: <decision>Accept</decision>