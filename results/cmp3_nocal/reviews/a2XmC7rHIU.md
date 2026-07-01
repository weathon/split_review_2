## Summary

The paper introduces the Open Proof Corpus (OPC), a dataset of 5,062 human-evaluated LLM-generated mathematical proofs across 1,010 problems from high-level competitions (IMO Shortlist, USAMO, Putnam, etc.). It uses the dataset to answer three open questions about LLM proof generation: (1) comparing informal vs. formal proof generation, (2) measuring the gap between final-answer accuracy and full proof correctness, and (3) evaluating best-of-n selection strategies. The paper also fine-tunes an 8B model on the OPC to demonstrate its utility for proof judging.

---

## Strengths

1. **Large-scale human evaluation fills a genuine gap.** The OPC contains 5,062 human-evaluated proofs across 1,010 problems from prestigious competitions — substantially larger than prior efforts (Petrov et al. had 6 problems; Mahdavi et al. had <5% correct proofs). This addresses a clear need in the community.

2. **Well-designed data splits for multiple research questions.** The four splits (MathArena, PutnamBench, Best-of-n, Generic) are thoughtfully chosen to support different analyses — final-answer-vs-proof comparison, formal-vs-informal comparison, best-of-n evaluation, and general training/benchmarking. This design multiplies the dataset's utility.

3. **Rigorous quality-control pipeline.** The grading pipeline uses former IMO participants as judges, includes a pilot phase with ~35% double-grading, achieves 90.4% inter-judge agreement on ~10% double-graded proofs, allows judge abstention (<3% flagged uncertain), and checks for bias from LLM-generated issue summaries. The documentation of these quality measures is thorough and above the norm for dataset papers.

4. **Demonstrated utility via fine-tuning.** OPC-R1-8B improves from 70.7% (base R1-QWEN3-8B) to 83.8% on proof judging — a 13-point gain — and approaches GPT-5's performance (Table 2). This validates the dataset's value for downstream training.

5. **Contamination analysis that goes further than most similar papers.** Table 4 empirically tests whether providing ground-truth solutions inflates judging accuracy, finding minimal impact. This is a non-obvious, substantive check that most dataset papers in this area omit.

---

## Weaknesses

### Fatal

None.

### Major

1. **The "human-level" judging claim compares non-comparable metrics (§5.2, Table 2, abstract).** The paper states GPT-5's 90.8% accuracy is "on-par with human performance" (90.4%). However, the human baseline is the *inter-annotator agreement rate* on all double-graded proofs in the OPC (two humans agreeing with each other), while the LLM accuracy is the model's *agreement with a single human label* on a 293-proof test subset. These measure fundamentally different quantities. The paper acknowledges the mismatch ("the human baseline is not measured on the test subset") but argues that uniform sampling makes it unproblematic — this is an unsupported assertion, not an analysis. Uniformly drawn does not guarantee identical difficulty distribution along dimensions that affect agreement rates. To substantiate the claim, the authors would need human re-grading of the exact test-set proofs (ideally with multiple judges and majority voting). The dataset contribution is unaffected, but this central claim is overstated relative to the evidence.

### Minor

2. **Best-of-n bug exclusion lacks sensitivity analysis (§7, footnote 1).** A bug in the Rank (Swiss) method caused incorrect selections for 18 of 152 problems (~12%), and these are excluded without analysis. There is no characterization of whether the bug was random or systematic, and no sensitivity analysis showing that conclusions hold with the 18 problems included (even with corrected method results). This risks optimism bias in the reported gains for Rank (Swiss).

3. **Informal-vs-formal comparison scope is narrower than the conclusion suggests (§5.3).** The paper reports GEMINI-2.5-PRO at ~83% vs. GOEDEL-PROVER-V2 at <19% on PutnamBench, and concludes that "natural language proof generation significantly outperforms formal proof generation." However, the paper also notes that an agentic formal system (Seed-Prover) achieves 50% and dismisses the comparison because the informal results don't use agentic techniques. This means the actual comparison is *non-agentic informal vs. non-agentic formal*, while the conclusion is stated more broadly. The paper is transparent about the Seed-Prover result, so this is a framing issue rather than a methodological error, but it should be calibrated.

4. **Dataset difficulty is partly determined by dynamic selection during construction (§3.1).** The paper describes actively monitoring model performance and adding more international problems when models did well on national ones. This adaptive process means the dataset's difficulty distribution is a function of ongoing model performance during construction, which could introduce unintended selection effects. The paper does not discuss how this might affect the generalizability of findings.

5. **The two difficulty partitions shown in Fig. 3 are coincidental rather than designed (§5.1, Fig. 3 caption).** The paper explains that the first partition contains problems answered by all models except R1, and the second contains problems from "more challenging competitions." However, the partitions were determined by model release timing (R1 replaced GROK-3-MINI mid-way through construction), not by deliberate difficulty design. The explanation in the caption appears post-hoc; this should be clarified.

### Trivial

6. **MathArena figure axis labeling is ambiguous (Fig. 5).** The Y-axis label "Pcorrect proof (%)" does not indicate that the metric is conditional on a correct final answer (P(correct proof | correct final answer)), which is how it is defined in §5.4. This could confuse readers.

---

## Nice-to-Haves

- **Re-run or simulate the corrected Rank (Swiss) method** for the 18 bug-affected problems and report whether conclusions change.
- **Report per-problem difficulty distribution** (e.g., how many problems had 0/5 models correct vs. 5/5) to help users understand where the dataset's difficulty mass lies.
- **Provide a summary of key prompt design choices** for proof generation in the main text (the prompt itself is deferred to supplementary §I.1), particularly whether the prompt implicitly discourages "I don't know" responses, which could affect the uncertainty-acknowledgment finding.

---

## Removed Points

These points were raised by the reviewer but are removed with justification:

- **"Appending informal final answers could artificially help informal models"** — The paper explicitly states this was done to *mirror the setup for formal models* (§3.1). This equalizes the comparison, not creates an advantage. The criticism misunderstands the intent.
- **"Missing appendix analysis"** — The parser strips appendices from all submissions. The analyses referenced in §C exist in the original paper.
- **"Prompt design only in supplementary"** — A common practice; the prompt is referenced as available in supplementary material. Not a weakness of the paper.
- **"Only selected proofs evaluated on larger best-of-n subset"** — The paper acknowledges this (§4) and validates conclusions on the 60-problem subset where all proofs are judged, with consistent results. This is a documented limitation, not an overlooked flaw.

---

## Novel Insights

None beyond the paper's own contributions.

---

## Suggestions

- Calibrate the "human-level" claim. Either have humans re-judge the same 293 test-set proofs, or reframe the claim to acknowledge that the comparison is between different metrics (inter-annotator agreement vs. agreement with a single human label).
- Add a sensitivity analysis for the 18 bug-excluded problems in the best-of-n evaluation.
- Reframe the informal-vs-formal conclusion in §5.3 to more precisely reflect the non-agentic scope of the comparison.
- Clarify the Fig. 5 axis label to indicate the conditional nature of the proof-correctness metric.

---

## Score and Decision

MY FINAL SCORE: <score>7.5</score>
MY FINAL DECISION: <decision>Accept</decision>