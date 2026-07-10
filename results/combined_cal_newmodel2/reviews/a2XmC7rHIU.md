Now let me integrate everything into the final review.

## Summary

This paper introduces the Open Proof Corpus (OPC), a human-validated dataset of 5,062 LLM-generated proofs across 1,010 competition-level mathematical problems, evaluated by 13 expert judges (former IMO participants). Using the dataset, the paper addresses several questions about proof generation: comparing formal vs. informal proof generation, the gap between final-answer accuracy and proof correctness, and best-of-n selection strategies. The authors also fine-tune an 8B-parameter model on the OPC that matches GEMINI-2.5-PRO in proof-judging accuracy, demonstrating the dataset's practical utility.

## Strengths

- **Scale of human annotation**: 5,062 human-evaluated proofs across 1,010 competition-level problems is substantially larger than prior efforts (Petrov et al. evaluated 6 problems; Mahdavi et al. found very few correct proofs), filling a genuine gap in community resources. **[favorability=12.95]**

- **Rigorous annotation pipeline**: The paper describes a credible annotation process: 13 expert judges (former IMO participants), a pilot phase with ~35% double-grading, a coordinator resolving discrepancies, detailed grading guidelines, and a final 90.4% inter-judge agreement rate. The ~10% double-grading rate throughout the main phase is reasonable for a dataset of this complexity. **[favorability=9.97]**

- **Demonstrated utility through fine-tuning**: Fine-tuning R1-QWEN3-8B on OPC yields a 17% improvement in proof-judging accuracy (from 70.7% to 83.8% pass@1, matching GEMINI-2.5-PRO). The open release of both the dataset and the fine-tuned model is a genuine contribution to the community. **[favorability=12.03]**

- **Self-evaluation analysis (Table 3)**: The finding that all tested models except QWEN3-235B-A22B perform worse when judging their own proofs vs. others' is non-obvious and practically important for applications relying on self-verification. **[favorability=11.01]**

## Weaknesses

### Major

- **Human judging baseline mismatch**: The claim that LLMs are "human-level judges" (section title, line 213) or that GPT-5 "approaches the 90.4% human baseline" (line 248) compares model accuracy on a specific held-out test set (293 proofs from the generic subset) against the 90.4% inter-judge agreement rate computed on all double-graded proofs — a different, non-random 10% sample of the dataset with a much higher double-grading rate during the pilot phase. The paper's justification (line 246: "Since the test samples are uniformly drawn from the OPC, this does not significantly affect the comparison") is unsubstantiated — the double-graded proofs were selected for quality assurance purposes, not as a random sample. Without the human baseline recomputed on the exact same test set, the central claim that GPT-5's performance is "on-par with human performance" is not adequately supported by the evidence presented. **[favorability=-1.37]**

- **Formal-vs-informal comparison confounded by asymmetric setup**: The headline result that informal proof generation "solves 4x more problems in the PutnamBench" (abstract, Fig. 1(b)) relies on a comparison where informal models received the final answer appended to the problem statement (line 103: "we appended the informal final answer... to mirror the setup for formal models"). For Putnam-level problems where deriving the answer is itself non-trivial, this reduces the task from "find the answer and construct a proof" to "prove this given result." While the paper's motivation (mirroring formal theorem-proving setup) is reasonable, the headline framing does not reflect this asymmetry. The comparison is between specific systems under specific conditions, not an unbiased measure of the formal-vs-informal capability gap. **[favorability=-0.20]**

### Minor

- **Dynamic problem selection limits benchmark interpretability**: The dataset was constructed with active difficulty monitoring (line 101: "model performance was actively monitored to ensure that the selected problems remained appropriately challenging"), targeting "roughly 50% model accuracy" (line 99). While appropriate for training data, this curation means the aggregate model accuracy comparisons in Fig. 3 describe the curated distribution rather than intrinsic model capabilities. The two-partition presentation partially addresses this, but accuracy numbers between models cannot be straightforwardly interpreted as rankings on a fixed problem distribution. **[favorability=4.30]**

- **MathArena proof analysis conditions on non-standard generation**: The analysis in §5.4 conditions on correct final answers, but the generation process allowed multiple attempts (line 103: "we only retained solutions with a correct final answer, retrying generation if necessary"). The conditional proof-correctness rate is measured on a distribution where models may have needed multiple tries to get the answer right, which could affect proof quality differently than single-pass evaluation would. **[favorability=7.20]**

- **Best-of-n analysis has opaque reproducibility issue**: The bug in the Rank (Swiss) method (footnote 1) is mentioned but not described, making it impossible for readers to assess its scope. On the larger subset (Fig. 6b), only proofs selected by each method are human-evaluated, which validates selectors' choices rather than providing independent ground-truth evaluation of all generations. **[favorability=3.98]**

- **Contamination analysis uses an indirect test**: The experiment testing whether providing ground-truth solutions improves judging accuracy (Table 4) is an indirect test for data contamination — if a model has already seen a problem during training, providing the solution again is a redundant manipulation. The authors acknowledge this limitation, but the experiment does not provide the reassurance the text implies. **[favorability=1.86]**

### Trivial

None.

## Nice-to-Haves

- Recompute the human judging baseline on the exact test set used for model evaluation, and report both inter-judge agreement and per-judge accuracy on that set.
- For the formal-informal comparison, either withhold the answer from informal models or prominently acknowledge the answer-hinting in the abstract and conclusion.
- Add statistical significance testing for between-model differences in Fig. 3 and Fig. 6.
- Describe the Rank (Swiss) bug so readers can assess its scope and impact.

## Removed Points

These points from the input review are flagged to be removed; treat them with caution:

1. **Criticism about Seed-Prover baseline selection (part (b) of Weakness 1)**: The paper explicitly addresses Seed-Prover (line 295) and explains why it is not directly comparable (private, agentic techniques while informal results are non-agentic). The paper's justification is reasonable; this weakly overlaps with the asymmetric setup concern but was removed to avoid conflating a legitimate methodological choice with a confound.

2. **Criticism about lack of statistical testing**: The paper reports 95% confidence intervals and justifies that relative differences in the best-of-n analysis are significant because methods share the same underlying generations (line 320). Demoted to nice-to-have.

3. **Limitation section being "oddly framed"**: The limitation about GROK-4/GPT-5 timing is a framing preference, not a substantive weakness.

4. **Strength about "targeting an important problem"**: Generic strength, not specific to this paper's content.

5. **Request for larger dataset**: The current size (5,062 proofs) is already the largest of its kind — this is not a realistic or reasonable ask.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. Recompute the human judging baseline on the exact test set used for model evaluation. This is the single most important missing piece — without it the "human-level judges" claim is unsupported.
2. Prominently acknowledge in the abstract and conclusion that the formal-vs-informal comparison gave informal models the final answer. Reframe as "informal (with answer hints) vs. formal" rather than "informal vs. formal."
3. Describe the Rank (Swiss) bug so that readers can independently assess its impact.
4. Add a discussion of how the dynamic problem selection affects interpretation of aggregate accuracy figures.

## Score and Decision

**Calibration process:**

**Round 1 bracket:** After drafting the review with kept strengths (favorability 5.98–12.95) and weaknesses (favorability -1.37 to 7.20), I queried for anchors in six score bands. The most topically similar papers retrieved were: Putnam-AXIOM (5.80, Reject), MUSTARD (7.33, Accept), U-MATH (5.25, Reject), ProverGen (6.25, Accept), and Decomposing the Enigma (6.33, Reject). All are dataset/benchmark papers involving mathematical reasoning evaluation, making them strong comparators. Initial bracket: **5.5–7.0**.

**Round 2 narrowing:** I itemized the closest anchors for detailed favorability comparison.

- **vs. Putnam-AXIOM (5.80, Reject)**: Putnam-AXIOM's worst weakness (favorability=-0.56) was about a methodological gap. My paper's worst weakness (-1.37) is more severe. However, my paper has substantially stronger strengths (up to 12.95 vs. 8.62) and a much larger, more rigorously annotated dataset. My paper also demonstrates practical utility through fine-tuning, which Putnam-AXIOM lacks. My paper is stronger overall.

- **vs. MUSTARD (7.33, Accept)**: MUSTARD's worst weakness (-0.51) was about dataset misalignment. My paper's worst weakness (-1.37) is more negative, reflecting a more central methodological gap affecting a headline claim. MUSTARD's strengths (up to 12.23) are comparable to my paper's (12.95). Both demonstrate fine-tuning gains. However, MUSTARD's weaknesses are less damaging to its core claims. My paper is slightly weaker overall.

- **vs. Decomposing the Enigma (6.33, Reject)**: This anchor had weaknesses at -3.62 and -0.60 with strengths up to 13.93. My paper's worst weakness (-1.37) is less severe than -3.62 but more severe than -0.60. Both have strong strengths. This anchor was rejected due to concerns about experimental validity, while my paper's core contribution (the dataset) remains solid.

**Final placement:** My paper's most negative weakness (-1.37: human judging baseline mismatch) is more negative than MUSTARD's worst (-0.51) and Putnam-AXIOM's worst (-0.56), but less negative than Decomposing the Enigma's worst (-3.62). The strength ceiling is comparable to the best anchors (12.95). The dataset contribution is genuine and fills a real gap — unlike pure-benchmark papers, this paper also demonstrates practical utility via fine-tuning. However, the headline claims (human-level judging, 4x gap) are overstated relative to what the evidence supports. These are fixable through revision: recompute human baseline on the test set and reframe the formal comparison. The core dataset work is solid.

**Score: 6.0** — borderline accept. The dataset contribution is significant, and the fine-tuning results are compelling evidence of practical value. The methodological issues with the human baseline comparison and the formal-informal framing are real but addressable in revision. The paper would be stronger if the evaluation claims were brought into alignment with what the experimental design actually supports.

**Decision: Reject** with encouragement to revise — the evaluation claims need substantial reframing or better evidence before the paper can be recommended for acceptance. (If the authors recompute the human baseline on the exact test set and prominently caveat the formal-informal comparison, the paper would warrant acceptance.)

MY FINAL SCORE: <score>6.0</score>
MY FINAL DECISION: <decision>Reject</decision>