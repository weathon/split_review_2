## Summary

The Open Proof Corpus (OPC) is a human-validated dataset of over 5,000 LLM-generated proofs across 1,010 competition-level mathematics problems, produced by six state-of-the-art models. The paper documents a rigorous annotation pipeline (expert judges, continuous monitoring, ~10% double-grading with 90.4% agreement), uses the dataset to analyze three questions about proof generation (informal-formal gap, final-answer vs. proof correctness, best-of-n selection), and demonstrates practical utility by fine-tuning an 8B model that reaches 88.1% judging accuracy. The primary contribution is the dataset itself.

## Strengths

1. **Dataset size and quality are a genuine step forward.** At 5,062 human-evaluated proofs, the OPC is substantially larger than prior efforts (Petrov et al. evaluated 6 problems; Mahdavi et al. produced a smaller, non-open-sourced set). The inter-judge agreement rate of 90.4% with an estimated individual error rate of ~5% (§4) provides strong evidence of label quality for a task of this difficulty. The dataset fills a clear gap.

2. **The annotation pipeline is rigorous and well-documented.** The use of expert judges (former IMO participants), a pilot phase with elevated double-grading (35%), continuous monitoring of discrepancies with coordinator review, and the deliberate check of whether LLM-flagged issue summaries changed agreement rates before/after their introduction (§3.2–3.3) all demonstrate thoughtful methodology.

3. **The contamination analysis for judging (Table 4) is well-designed.** Providing the ground-truth solution alongside the proof and measuring the delta is a clean way to assess whether knowing the problem matters. The small, non-significant changes across models support the argument that contamination does not drive the judging results.

4. **The self-evaluation finding (Table 3) is interesting and non-obvious.** The pattern that most models are worse at judging their own proofs than others' proofs has practical implications for self-verification systems, and the breakdown by model pair is informative.

5. **The fine-tuned OPC-R1-8B is a meaningful proof-of-concept.** A 17-point improvement over R1-QWEN3-8B (§5.2) shows the dataset has practical utility for training, which is the key utility claim a dataset paper should make.

## Weaknesses

### Fatal
None.

### Major

- **Best-of-n pass@1 computation on the larger subset (Figure 6b) is unexplained.** The dataset description (§4) states that for the 152-problem best-of-n subset, only 60 problems have all 8 generations human-evaluated; the remaining problems "include judgments only for the generations selected by a best-of-n selection strategy." Figure 6(b) then reports pass@1 (alongside selection methods) on 134 problems. The paper does not explain how pass@1 — which requires a human judgment for a single random generation per problem — was computed on the 74 problems where not all generations were judged. If pass@1 was computed only on the 60 fully-judged problems while selection methods used all 134, the comparison is confounded by different problem sets. If it was estimated via imputation, the method is undisclosed. Either way, the reader cannot determine whether the claimed 17% improvement from Rank (Swiss) over pass@1 is a real effect or an artifact of the evaluation design. This does not affect the dataset itself, but it undermines Figure 6(b)'s conclusions as presented.

### Minor

- **Human baseline for judging is measured on a different distribution than the LLM test set.** The human accuracy of 90.4% comes from all double-graded proofs (aggregated across the entire OPC), while LLM judges are evaluated on a specific 293-proof test set (§5.2). The paper argues that "since the test samples are uniformly drawn from the OPC, this does not significantly affect the comparison," but the double-graded set is not a uniform random sample — it includes pilot-phase data with elevated double-grading (35%, §3.3) and targeted monitoring for discrepancy detection. The headline claim "on-par with human performance" would be strengthened by either measuring the human baseline on the actual test set or explicitly qualifying the comparison (e.g., "approaching the estimated human agreement rate of 90.4%").

- **Aggregate correctness statistics lack caveats about adaptive problem selection.** The paper states (§3.1) that model performance was "actively monitored" and problems were added or removed to target roughly 50% accuracy. The overall "43% correct" figure and model-specific numbers in Figure 3 are therefore partially artifacts of this selection policy. The paper should note that these correctness rates reflect the curated difficulty balance and are not unconditional estimates of model capability.

- **Uncertainty acknowledgment detection methodology is underspecified.** The paper reports that out of 1,700+ incorrect solutions, models "explicitly state their inability to solve the problem in only 114 instances" (§5.1), but does not describe how these instances were identified (keyword matching, manual review, LLM parsing). If the detection is keyword-based, it could miss more subtle expressions of uncertainty.

### Trivial
None.

## Nice-to-Haves

- The "Other" competition category (16.4% of the dataset, Figure 2) should be itemized in the main text for reproducibility.
- The out-of-distribution evaluation of OPC-R1-8B (currently deferred to §C in the appendix) would usefully appear as a brief summary in the main text, since the paper acknowledges that in-distribution evaluation may inflate performance.
- A brief note in Table 2 that OPC-R1-8B's cost is "N/A" because it can be run locally at inference cost (rather than API cost) would highlight a practical advantage.

## Removed Points
These points were considered but removed during consolidation:

- *Figure 1 caption duplication* — Parser artifact of the PDF extraction; not an author error.
- *"Three open questions" overstatement* — A framing nuance; the paper quantifies phenomena that prior work touched on only at smaller scale. This is a presentation preference, not a substantive weakness.
- *§3.1 MathArena detail about filtering by correct final answer* — The reviewer acknowledged the paper handles this transparently; not a weakness.
- *§5.3 formal/informal comparison being "expected"* — Comment on the result's unsurprising nature, not a flaw in the paper.
- *Missing appendix content (proofs, OOD results)* — The appendix is stripped by the parser; the original submission contains this material.
- *"Other" competition composition* — Deferred to §A, which is stripped by the parser.

## Novel Insights

The most useful insight across the reviews is that the best-of-n methodology on the larger subset needs explicit clarification of how pass@1 was computed when only selected proofs were judged for a majority of problems. This is a genuine gap in the paper's analytical framing that does not affect the dataset itself but must be resolved for the secondary claims to be trustworthy.

## Suggestions

1. **Clarify the best-of-n pass@1 computation.** State explicitly: was pass@1 computed only on the 60 fully-judged problems, or on all 134 using some imputation procedure? If the former, restrict Figure 6(b)'s comparison to the 60-problem subset or add a clear caveat about the differing problem sets.
2. **Qualify the human-baseline comparison.** Replace "on-par with human performance" with language like "approaching the estimated human agreement rate of 90.4% (measured on a broader set of double-graded proofs)."
3. **Add a caveat about adaptive problem selection** affecting the aggregate correctness percentages reported in §4 and Figure 3.
4. **Specify how the 114 "explicit inability" instances were detected** (§5.1).

## Score and Decision

MY FINAL SCORE: <score>8</score>
MY FINAL DECISION: <decision>Accept</decision>