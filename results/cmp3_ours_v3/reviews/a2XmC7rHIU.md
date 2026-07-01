## Summary

This paper introduces the Open Proof Corpus (OPC), a dataset of 5,062 human-evaluated LLM-generated mathematical proofs across 1,010 competition-level problems (IMO, USAMO, Putnam, etc.). The annotation pipeline uses 13 former IMO participants with rigorous double-grading (90.4% agreement) and coordinator oversight. Using the OPC, the paper addresses three open questions: (1) informal proof generation substantially outperforms formal (82.7% vs 19%), (2) final-answer accuracy is a poor proxy for proof correctness (o3 drops ~28 percentage points), and (3) pairwise ranking best-of-n strategies significantly improve proof quality. The paper also fine-tunes and openly releases an 8B judge model (OPC-R1-8B) that achieves 88.1% accuracy, approaching GPT-5.

## Strengths

- **Fills a genuine gap with a large, high-quality human-annotated dataset.** Prior proof-evaluation datasets were small (6–few hundred problems), used outdated models, or were not open-sourced. The OPC's 5,062 proofs across 1,010 problems with binary human labels and justifications is a substantial new resource.

- **Rigorous annotation pipeline.** Judges are former IMO participants, with a pilot phase (35% double-grading), ongoing 10% double-grading, coordinator discrepancy resolution, an abstention option, and 90.4% inter-annotator agreement. This sets a high quality bar that exceeds most LLM-output datasets.

- **Clean, non-obvious empirical finding in Fig. 5.** By conditioning on correct final answers and then evaluating proof correctness, the paper isolates a meaningful gap. The finding that o3 drops ~28 points in proof correctness below its final-answer accuracy (vs ~7 for Gemini-2.5-Pro and o4-mini) is a genuinely informative observation that justifies the paper's central thesis about final-answer benchmarks being insufficient.

- **Open release of both the dataset and the fine-tuned 8B judge model.** The OPC-R1-8B model improves 17 points over its base, demonstrating the dataset's training utility. Open release substantially increases practical impact and reproducibility.

## Weaknesses

### Fatal

None.

### Major

None.

### Minor

1. **Adaptive difficulty-tuning is not adequately flagged when reporting aggregate statistics.** The paper states (lines 99–102) that problem selection was adjusted during construction based on model performance: "more problems from international competitions were added when initial results indicated that models were performing very well (≈65%) on national-level problems." This means aggregate numbers like "43% correct proofs" and the per-model accuracies in Fig. 3 reflect the adaptive sampling procedure, not unconditional performance estimates on competition mathematics. The Limitations section does not mention this. While relative rankings are likely robust, readers may be misled about absolute performance levels. The paper should add a clear caveat when discussing these numbers.

2. **The "human-level judge" claim is modestly overstated.** The paper states GPT-5 achieves 90.8% judgment accuracy, "on-par with human performance" (abstract and Fig. 1b). The human baseline (90.4%) is inter-annotator agreement (agreement between two judges), not accuracy against an absolute ground truth. The model's 90.8% is measured against one human's labels as ground truth. Framing this as "within the range of human inter-annotator agreement" would be more precise. This is not a fatal error — the evidence still convincingly shows LLMs are highly capable proof judges — but the claim as stated is slightly stronger than what the data directly supports.

3. **The best-of-n larger-subset analysis has a methodological transparency gap.** The best-of-n subset contains 152 problems; only 60 have all 8 generations fully judged (line 179). For the larger-subset analysis (134 problems, Fig. 6b), it is not clarified how the pass@1 baseline of 22.7% was computed — whether it was measured on the same 134 problems or only on the 60 fully-judged ones. If the problem sets differ, the comparison is confounded. The paper should clarify this, as the current presentation implies an apples-to-apples comparison that may not hold.

4. **The best-of-n bug is not described.** The paper excludes 18/152 ≈ 12% of the best-of-n problems due to a "small bug" in Rank (Swiss) (line 321, footnote 1) but does not describe the bug. Reproducibility would benefit from a brief description of what went wrong.

5. **MathArena "retrying" is underspecified.** The paper states it "only retained solutions with a correct final answer, retrying generation if necessary" (line 103). The retry strategy (number of attempts, stopping criterion) is not specified. This does not affect the conditional analysis in §5.4 but is relevant context for understanding the procedure.

6. **The Limitations section (§6) is thin.** It does not discuss the adaptive problem selection, the MathArena conditioning, or the partial best-of-n validation — real limitations that the paper would benefit from addressing directly.

### Trivial

None.

## Nice-to-Haves

- Add a systematic comparison table with prior proof-generation datasets (Petrov et al., Mahdavi et al., Frieder et al., Sheng et al., Guo et al., Zhang et al.) along dimensions like scale, model coverage, human evaluation, and open-source status.
- Report sample sizes for the before/after LLM-summary bias test to establish statistical power.

## Removed Points

These points were considered but removed or demoted after cross-checking against the paper:

- **"First large dataset" overclaim**: Removed. Prior datasets are small (6 problems in Petrov et al.) or use outdated models. The claim is accurate.
- **OPC-R1-8B in-distribution evaluation concern**: Removed. The paper acknowledges this (§5.2) and includes OOD analysis in §C.
- **Formal vs informal comparison rhetoric**: Removed. The paper notes Seed-Prover is agentic and "not accurate to directly compare," which is fair disclosure.
- **Self-evaluation table formatting**: Removed. Minor presentation preference.
- **MathArena retrying inflating final-answer accuracy**: Removed. Misreading — the analysis conditions on correct final answers, so retrying is appropriate.
- **LLM summary bias test statistical power**: Demoted to Nice-to-Haves (a reasonable suggestion but not a weakness).
- **Missing related work comparison table**: Demoted to Nice-to-Haves (helpful addition but not a flaw).

## Novel Insights

The critic's most valuable observation is that the adaptive difficulty-tuning (lines 99–102) has implications for interpreting aggregate statistics that the paper does not adequately flag. The "43% correct proofs" and Fig. 3 accuracy numbers reflect an active sampling procedure, not unconditional performance estimates. The critic also correctly identifies the asymmetry in the "human-level" claim: comparing model accuracy against human labels with human inter-annotator agreement is acceptable practice but should be framed more precisely. The best-of-n validation gap is a valid transparency concern. None of these is fatal, but all point to areas where a few sentences of additional caveats would substantially strengthen the paper.

## Suggestions

1. When reporting Fig. 3 and aggregate accuracy statistics, add a clear caveat that these reflect the adaptive sampling procedure and should not be interpreted as unconditional performance estimates on competition mathematics.
2. Recalibrate the "human-level judge" claim: report that GPT-5's agreement with human judgments (90.8%) falls within the range of human inter-annotator agreement (90.4%).
3. Clarify how pass@1 was computed on the larger best-of-n subset (Fig. 6b) and ensure baselines are computed on identical problem sets.
4. Describe the Rank (Swiss) bug that caused exclusion of 18 problems.
5. Expand the Limitations section to address adaptive problem selection, MathArena conditioning, and best-of-n validation scope.

MY FINAL SCORE: <score>7.0</score>
MY FINAL DECISION: <decision>Accept</decision>