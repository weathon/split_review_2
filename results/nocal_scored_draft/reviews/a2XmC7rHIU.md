## Summary

This paper introduces the Open Proof Corpus (OPC), a dataset of over 5,000 LLM-generated mathematical proofs across 1,010 competition problems, each human-evaluated by expert judges (13 former IMO participants/finalists). The dataset is used to investigate three open questions: the gap between natural language and formal proof generation, the relationship between final-answer accuracy and full proof correctness, and the effectiveness of best-of-\(n\) selection strategies. The authors also fine-tune an 8B model on the OPC that achieves 88.1% judgment accuracy, approaching frontier-model performance.

## Strengths

- **Scale and quality of human annotation.** At 5,062 expert-judged proofs, the OPC is substantially larger than prior efforts (Petrov et al.: 6 problems; Mahdavi et al.: small scale, no open release). The use of 13 former IMO participants or final-stage selectees as judges, combined with a pilot phase refining instructions, ~10% double-grading, explicit abstention/uncertainty options, and 90.4% inter-judge agreement, makes this the most carefully constructed dataset of its kind.

- **Honest handling of known confounds.** The paper transparently acknowledges distributional overlap between training and test data for OPC-R1-8B (§5.2), potential data contamination (§5.6), adaptive problem selection (§3.1), exclusion of buggy best-of-\(n\) results (footnote 1), and that Seed-Prover is an agentic system not directly comparable (§5.3). This candor makes the remaining claims more credible.

- **Non-obvious empirical findings.** The discovery that o3 drops ~30% in accuracy when moving from final-answer to proof-correctness evaluation while Gemini-2.5-Pro drops only ~8% (Fig. 5) is genuinely informative — it shows the final-answer/proof-correctness gap is model-dependent, not a uniform phenomenon. Similarly, the result that ranking-based best-of-\(n\) strategies (Swiss, Bracket) continue scaling with \(n\) while discrete/continuous methods plateau (Fig. 6) is a useful empirical contribution.

- **Demonstrated utility of the dataset.** The OPC-R1-8B fine-tuned model (88.1% judgment accuracy maj@5) matches GEMINI-2.5-PRO and approaches GPT-5, concretely validating that the dataset has value for training, not just evaluation.

## Weaknesses

### Fatal

None.

### Major

1. **Adaptive problem selection undermines absolute accuracy as generalizable estimates.** Section 3.1 describes actively selecting problems to target roughly 50% model accuracy: "model performance was actively monitored to ensure that the selected problems remained appropriately challenging" and "problem prioritization was adjusted based on ongoing performance metrics, judge availability, and progress towards the specific conclusions we aimed to draw." This means the reported per-model accuracies (§5.1) and the abstract's "43% correct proofs" figure are dataset-internal statistics — they were engineered by construction, not discovered as a general property of LLM proof generation on competition problems. Relative model comparisons on the same problem subset remain valid, but any absolute claim about "how often" models produce correct proofs on competitions is unsupported. The paper does not flag this adequately when presenting these numbers, and the Limitations section (§6) does not mention it.

2. **The formal vs. informal comparison ("informal solves 4x more problems") compares different correctness standards without sufficient caveat.** Natural language proofs are judged by humans who accept small gaps, implicit reasoning, and informal language, while formal proofs require machine-verifiable correctness — a dramatically higher bar. This is presented as a head-to-head performance comparison in the abstract, Fig. 1(b), and §5.3. The paper does note that "formal proofs offer a major advantage: automatic verifiability" and mentions that Seed-Prover is agentic and not directly comparable, but these caveats are insufficient for the strength of the headline claim. The reader is left with the impression that the same capability is being measured, when in fact the two settings use fundamentally different standards of correctness.

### Minor

3. **Human baseline measured on a different sample than the model test set.** The 90.4% human inter-judge agreement is measured on all double-graded proofs across the OPC, while model accuracy (89.3% pass@1, 90.8% maj@5) is on a specific 293-proof test set. The paper's defense — "since the test samples are uniformly drawn from the OPC, this does not significantly affect the comparison" — is weak because double-graded proofs may be systematically different: the paper itself notes that harder or more ambiguous proofs were likelier to be flagged, discussed, or double-graded. The "on-par with human performance" claim is based on numbers measured under different conditions.

4. **Best-of-\(n\) results rely on a small sample (N=60 fully-judged problems).** The main best-of-\(n\) ranking conclusions (Fig. 6a) are based on only 60 problems where all 8 generations were human-evaluated. The paper acknowledges "relatively large confidence intervals" but dismisses the concern with a single sentence: "all selection methods rely on the same underlying answers from O4-MINI, making the relative performance differences significant." This is not a rigorous statistical argument — shared underlying answers do not automatically make relative differences significant. Per-problem breakdowns, bootstrap confidence intervals, or permutation tests would strengthen these claims.

5. **The Limitations section (§6) omits several substantive issues discussed elsewhere in the paper.** The adaptive problem selection bias, the small-\(N\) limitations of the best-of-\(n\) analysis, and the human baseline measurement inconsistency are not mentioned, despite being genuine concerns that readers should be aware of when interpreting the results.

## Nice-to-Haves

- A per-problem breakdown or bootstrap confidence intervals for the best-of-\(n\) analysis would substantially strengthen the claims about method ordering.
- Connecting the qualitative error observations in §E more directly to the o3/Gemini final-answer-to-proof drop asymmetry (e.g., examples of o3's incorrect proofs vs. Gemini's correct ones on the same problem) would deepen the analysis.

## Removed Points

*These points are flagged for removal; treat them with caution:*

- Criticism of the "first large dataset" claim: the paper's phrasing is reasonable given the cited related work (Petrov et al.: 6 problems; Mahdavi et al.: small scale, no open release).
- Criticism about confidence intervals not being in the main text for Table 2: the paper explicitly states "Full confidence intervals are given in §C.4" — the appendix is stripped by the parser, but the intervals exist in the original submission.
- Criticism that the contamination analysis is "thin": the paper provides a reasonable contamination analysis for its scope (a dedicated experiment with ground-truth solutions, the MathArena-specific justification, the informal-formal gap argument).
- "Dataset documentation" concern: the paper references supplementary material, which the parser cannot access.
- "Analysis of where models fail" and "more analysis of o3's drop": these are suggestions for strengthening, not weaknesses of the current paper.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

- Reframe absolute accuracy numbers as dataset-internal statistics (not generalizable estimates of LLM capability on competitions), or add explicit caveats to the abstract and §5.1.
- Re-frame the formal/informal comparison with an explicit statement that the two settings use different standards of correctness, or remove the numerically simplified "4x" framing from the abstract and Fig. 1(b).
- Either re-measure the human baseline on the same 293-proof test set, or add a clear caveat to the headline "on-par with human" claim.
- Add per-problem error analysis or bootstrapped confidence intervals for the best-of-\(n\) results.
- Expand the Limitations section to cover adaptive selection bias, the small-\(N\) issue in best-of-\(n\), and the human baseline measurement.

## Score and Decision

The OPC is a genuinely valuable contribution — a large, carefully annotated, open dataset that fills a clear gap. The annotation methodology is among the most rigorous I have seen for mathematical proof evaluation, and the empirical findings are interesting and suggestive. However, the paper overstates what the dataset can support in two specific ways: (1) absolute accuracy numbers are presented as if they reflect general LLM capability when they were engineered through adaptive problem selection, and (2) the "4x" formal/informal comparison is presented as a head-to-head result when the two settings use fundamentally different correctness standards. These issues are correctable with revisions and do not invalidate the dataset itself, but they weaken the headline narrative. I recommend acceptance with major revisions.

MY FINAL SCORE: <score>7</score>
MY FINAL DECISION: <decision>Accept</decision>