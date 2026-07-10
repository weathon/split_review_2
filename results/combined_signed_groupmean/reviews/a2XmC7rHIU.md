Now I have sufficient calibration data. Let me finalize the review.

## Summary

This paper introduces the Open Proof Corpus (OPC), a dataset of 5,062 human-evaluated LLM-generated proofs across 1,010 competition-level problems (IMO, USAMO, Putnam, etc.), annotated by 13 judges (former IMO participants/finalists) with 90.4% inter-judge agreement. Using the OPC, the authors address several open questions: the gap between informal and formal proof generation (~83% vs. <19% on PutnamBench), the discrepancy between final-answer accuracy and proof correctness, and the effectiveness of best-of-n selection strategies (ranking methods improving accuracy by 17%). They also fine-tune an 8B model (OPC-R1-8B) on the OPC, achieving 88.1% judgment accuracy — matching Gemini-2.5-Pro.

## Strengths

- **Scale and comprehensiveness.** The OPC is meaningfully larger than prior human-evaluated proof datasets. Previous efforts evaluated 6 problems (Petrov et al., 2025) or found no model above 5% accuracy. The OPC's 5,062 proofs across 1,010 problems from multiple models, partitioned into four purpose-specific subsets (MathArena, PutnamBench, Best-of-n, Generic), represents a genuine step up. [impact: +9.96]

- **Rigorous annotation pipeline.** Judges are former IMO participants/finalists; a pilot phase with 35% double-grading refined guidelines; 10% of the full dataset was double-graded; a coordinator monitored consistency. The 90.4% inter-judge agreement rate (with the derived 5% per-judge error rate) indicates reasonable annotation quality for this difficult task. [impact: +9.29 to +9.44]

- **Integrated demonstration of utility.** Rather than merely releasing a dataset, the paper fine-tunes R1-QWEN3-8B on the OPC to produce a model achieving 88.1% judgment accuracy, matching Gemini-2.5-Pro. This grounds the dataset's practical value. [impact: +8.90]

- **Honest uncertainty acknowledgment in §5.6.** The contamination analysis is appropriately bounded — the paper acknowledges that the Gemini-Pro vs. o4-mini gap cannot be conclusively attributed to genuine performance differences. The "worst-case" experiment on judging (providing ground-truth solutions) is a creative and informative control. [impact: +9.64]

## Weaknesses

### Fatal

None.

### Major

- **LLM-generated issue summaries introduce an uncontrolled potential bias that the current check cannot rule out (§3.2).** After several hundred graded proofs, the authors introduced O4-MINI-generated summaries flagging potential issues. The paper's bias check — measuring whether O4-MINI-human agreement changed before vs. after — tests only whether *agreement levels* shifted, not whether both parties converged under the summaries' influence. If summaries caused human judges to align toward O4-MINI's own judgment patterns, agreement between O4-MINI and humans would stay the same or increase, while the human labels would become less independent. The proper check would compare *inter-judge* (human-human) agreement rates before vs. after the summaries' introduction, which the paper does not provide. The paper reports that "most inconsistencies came from overlooked errors in the proofs" — but this is precisely the scenario where summaries pointing to those errors would improve detection *and* simultaneously align judgments with the LLM. The paper explicitly says the summaries were introduced to improve "efficiency and accuracy in detecting errors," which makes it *more* likely that they shifted judgments. This does not invalidate the dataset, but it weakens the claim that labels are fully independent human judgments for proofs graded after the summaries were introduced. The Limitations section (§6) omits this concern entirely. [impact: -9.89]

- **The "human-level proof judges" claim is framed more strongly than the evidence supports (§5.2).** The 90.4% human baseline is *inter-judge agreement*, not accuracy against ground truth. The paper's error-rate model (solving (1-p)² + p² = 0.904 to estimate p=5%) assumes independent errors and symmetric error rates — assumptions violated when two judges can make the *same* mistake on a subtle proof. True human accuracy could be anywhere from 90.4% to 100%. Additionally, the human baseline is measured on all double-graded proofs in the OPC, not on the specific 293-proof test set used for model evaluation. The paper's justification ("samples are uniformly drawn") does not fully account for sampling variance across competition sources and difficulty levels. [impact: -1.62]

### Minor

- **The formal vs. informal comparison (§5.3) is framed more broadly than the single system-vs-system comparison supports.** The paper compares Gemini-2.5-Pro (general-purpose, non-agentic, informal) against Goedel-Prover-V2 (specialized formal prover) and frames this as "formal proof generation lags behind." However, agentic formal systems like Seed-Prover (50% on PutnamBench) narrow this gap, and the paper's own acknowledgment that informal results do not use agentic techniques (and thus comparison with Seed-Prover is "not accurate") creates a selective comparison. The section title and headline claims remain broader than the specific evidence warrants. [impact: -0.03]

- **The best-of-n larger-subset evaluation has a structural limitation (§5.5).** On the 134-problem larger subset, only proofs *selected* by each strategy are human-evaluated for 92 of 152 problems. This means oracle pass@n cannot be computed on that set, and the gap between pass@n and selection methods on different subsets confounds evaluation-set differences with genuine method differences. The paper separates the two analyses clearly, but this reduces what can be concluded from the larger-subset comparison. [impact: -0.01]

- **The bug in Rank (Swiss) that affected 18 problems (footnote 1) is not explained**, making it difficult to assess its severity or reproduce the corrected analysis. [impact: -0.00]

### Trivial

None.

## Nice-to-Haves

- Compute human accuracy on the exact 293-proof test subset, or report the human baseline with a confidence interval that accounts for the different measurement sample.
- Scope the formal vs. informal comparison more precisely: "Under current best non-agentic systems, informal methods outperform formal on PutnamBench. However, agentic formal systems narrow this gap, and formal proofs provide automatic verifiability that informal proofs lack."
- Document the nature of the Rank (Swiss) bug for reproducibility.
- Report inter-judge agreement breakdown by competition/difficulty level.

## Removed Points

These points are flagged to be removed; treat them with caution.

- **"Ambiguous phrasing about 'first large dataset'"** — formatting/presentation nitpick. The paper's phrasing is sufficiently clear in context.
- **"50% model accuracy selection criterion should be mentioned as limitation"** — the paper already mentions this in §3.1.
- **"MathArena design choice should be more prominently highlighted"** — the paper states it clearly.
- **"Human baseline caveat in line-broken position"** — formatting artifact from PDF extraction, not an author issue.
- **"Confidence intervals absent from main text"** — paper states they are in §C.4; appendix is stripped by parser.
- **"Annotation timeline unclear"** — the paper clearly describes the two partitions.
- **Various section-by-section notes that are presentation preferences** rather than substantive weaknesses (e.g., phrasing preferences, organization suggestions).

## Novel Insights

The harsh critic's most insightful methodological contribution is recognizing that the LLM-summary bias check tests the wrong quantity: O4-MINI-human agreement before vs. after is insensitive to the scenario where both parties converge under the summaries' influence. The correct control is human-human (inter-judge) agreement before vs. after. This is a genuinely subtle methodological point that goes beyond what the paper acknowledges and applies to any annotation pipeline that introduces model-generated aids during the process.

## Suggestions

- Conduct a proper bias analysis for the LLM-generated issue summaries by comparing inter-judge agreement rates before vs. after their introduction (or run a controlled experiment with a subset graded both with and without summaries by different judges).
- Present the human baseline for judging with a clear statement that it is inter-judge agreement (not ground-truth accuracy), and either compute it on the test subset or provide a confidence interval.
- Revise the formal vs. informal framing to explicitly acknowledge that agentic formal systems narrow the gap and that this is a system-level rather than paradigm-level comparison.

## Score and Decision

**Bracket determination (Round 1):** The paper sits in the 6.0–7.5 range. It is clearly stronger than Putnam-AXIOM (5.80, Reject) and U-MATH (5.25, Reject) — larger scale, more rigorous human evaluation, demonstrated downstream utility. It is comparable to MUSTARD (7.33, Accept) and Omni-MATH (6.75, Accept), which are the closest topic-matched anchors.

**Narrowing (Round 2):** Comparing itemized impact scores:
- OPC's top strengths (+9.96, +9.29/+9.44, +8.90, +9.64) are at the high end of the 6.0–7.5 band — stronger than or comparable to MUSTARD's (+9.25, +7.67, +7.96) and Omni-MATH's (+6.88, +6.36).
- OPC's primary weakness (-9.89) is comparable in magnitude to MUSTARD's top weaknesses (-8.33, -9.63) and Omni-MATH's (-9.47, -9.93).
- Crucially, the OPC's other weaknesses are all very low impact (≤ -1.62), whereas both MUSTARD and Omni-MATH have additional high-impact weaknesses.
- The OPC is stronger than MathCheck (6.25, Accept) and ProverGen (6.25, Accept) across all dimensions.

The -9.89 weakness prevents a score in the 7+ range. However, the harsh critic explicitly states it does not invalidate the core dataset contribution. I place the final score just below MUSTARD (7.33) due to the methodological nature of the bias concern being harder to address than MUSTARD's data-scale limitations.

**Calibration anchors retrieved (all rounds):**

| Anchor | Avg Score | Round | Itemized | Comparison |
|--------|-----------|-------|----------|------------|
| 8QTpYC4smR (LLM survey) | 1.00 | R1 | No | Not relevant; non-paper survey. |
| 5kMwiMnUip (jailbreaking) | 1.40 | R1 | No | Not relevant. |
| EXaKfdsw04 (StepProof) | 3.25 | R1 | No | Related topic (stepwise verification) but lower quality/scale. |
| JNZ3Om6NPS (LLM limitations) | 2.00 | R1 | No | Not relevant. |
| DexGnh0EcB (MathEval) | 4.20 | R1 | No | Benchmark paper; lower rigor than OPC. |
| WrBqgoseGL (Putnam-AXIOM) | 5.80 | R1, R2 | Yes | Same topic area; OPC is larger and has human evaluation. |
| xlxGsX1pc7 (U-MATH) | 5.25 | R1 | Yes | University benchmark; OPC larger and more rigorous. |
| 8xliOUg9EW (MUSTARD) | 7.33 | R1, R2, R3 | Yes | Closest comparator (dataset paper); OPC has real human eval. |
| 5ck9PIrTpH (MathGAP) | 7.00 | R1, R2 | Yes | Proof complexity evaluation; different contribution type. |
| jKHmjlpViu (OpenWebMath) | 6.00 | R1 | No | Web-math dataset; automated processing, no human eval. |
| yaqPf0KAlN (Omni-MATH) | 6.75 | R2 | Yes | Olympiad benchmark; similar scope but no proof eval. |
| nDvgHIBRxQ (MathCheck) | 6.25 | R2 | Yes | Math reasoning evaluation; no proof component. |
| C25SgeXWjE (ProverGen) | 6.25 | R3 | No | FOL reasoning dataset; less directly relevant. |
| KIgaAqEFHW (miniCTX) | 8.00 | R1 | No | Formal theorem proving; different sub-area. |

MY FINAL SCORE: <score>6.5</score>
MY FINAL DECISION: <decision>Accept</decision>