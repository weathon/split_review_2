Now I have a clear calibration picture. Let me write the final consolidated review.

## Summary

This paper investigates whether translating benchmark data into Arabic can mask data contamination signals in LLM evaluation. The authors fine-tune four open-weight models on varying proportions (0%, 10%, 50%, 100%) of Arabic-translated test data from MMLU, XQuAD, and MLQA (while always including the English test set), then evaluate on the original English benchmarks. An extended TS-Guessing probe with choice reordering is used to detect memorization. The core insight—that translation could create a blind spot in contamination detection—is genuinely interesting, but the experimental design has structural gaps that prevent the paper from supporting its central claims as presented.

## Strengths

1. **Well-motivated and timely research question.** The paper identifies a genuine gap: contamination detection methods focus overwhelmingly on English, and whether translation into lower-resource languages alters contamination dynamics is genuinely underexplored (Sections 1, 2). This framing is a legitimate contribution to the contamination literature.

2. **Multiple model families and task formats.** Four distinct instruction-tuned models (Llama-3.2-1B, Mistral-7B, Gemma-3-1B, Qwen3-1.7B) and three datasets covering two task formats (MCQ and extractive QA) are tested with a standardized fine-tuning setup (Section 3.1), providing useful breadth.

3. **Methodological adaptation of TS-Guessing.** Extending TS-Guessing with choice reordering for MCQ tasks (Section 3.3) is a sensible adaptation that could be useful in future work, even if its current instantiation produces ambiguous results.

## Weaknesses

### Fatal
None.

### Major

1. **Missing English-only contamination baseline undermines the central "masking" claim.** To demonstrate that translation "masks" or "conceals" contamination, the paper requires a comparison between contamination detection with vs. without translation. The needed control is: fine-tune models on the *English* test set at the same proportions p ∈ {10, 50, 100}%, evaluate on English, and run the same TS-Guessing probes. The current design only varies Arabic exposure while English exposure is constant across all conditions. Without this control, the paper cannot distinguish between "translation makes contamination harder to detect" and "TS-Guessing has low sensitivity in general, and the observed performance gains are a trivial consequence of fine-tuning on the evaluation set." This is the most serious weakness because it directly affects the paper's core claim, stated in the abstract: "translation into Arabic conceals traditional contamination signals."

2. **Internal contradiction: monotonic increase vs. near-flat trend.** Section 4.1 states: "Across all models, MMLU exhibits a generally monotonic increase as contamination rises from 0% → 100%" and reports substantial gains (Mistral: 0.577→0.690, +0.113; LLaMA: 0.332→0.431, +0.099). Section 4.2 then claims: "Across contamination levels p ∈ {10, 50, 100}%, the models exhibit approximately equal performance on all evaluated benchmarks. This near-flat trend indicates that Arabic → English translation is effectively masking contamination effects." These two characterizations are inconsistent. MMLU results are not flat—they rise meaningfully and monotonically—and the paper cannot simultaneously argue that contamination inflates scores (Section 4.1) and that the trend is flat (Section 4.2) without resolving this tension. This contradiction undermines the "masking" narrative.

3. **TS-Guessing probe produces null results that are ambiguously interpreted.** Table 3 shows TS-Guessing scores at or below random chance across nearly all conditions (e.g., Mistral IDR = 0.000 on MMLU across all contamination levels; most XQuAD EM values below 0.02). The paper interprets this as "translation conceals leakage" (Section 4.2), but the equally parsimonious explanation is that the TS-Guessing implementation has low sensitivity or the probe design does not reliably trigger recall in these fine-tuned models. No validation experiment (e.g., testing TS-Guessing on models fine-tuned on English-only contamination to confirm the probe works when contamination is known to be present) is presented. This makes it impossible to attribute the null results to translation specifically.

4. **The D_EN^d (p=0) baseline is already contaminated with English test data.** The training set at p=0 includes the English test items (for MMLU: "English test items formatted as MCQ"; for XQuAD/MLQA: "English QA"). This means the baseline condition already involves fine-tuning on the exact evaluation set. The p=0 performance is therefore not a clean baseline—it reflects test-set memorization in English. This compresses the observable range and muddies the interpretation of incremental score increases from adding Arabic translations on top of an already-contaminated English baseline.

### Minor

5. **No statistical reliability reporting.** All results come from single training runs (Tables 2-3). No standard deviations, confidence intervals, or multiple seeds are reported. Given the non-monotonic patterns in XQuAD/MLQA (e.g., Qwen MLQA spikes at 10% and collapses at 50%), it is impossible to assess whether observed differences are systematic or seed-dependent noise.

6. **TACD is a proposal, not a demonstrated contribution.** Section 5 explicitly states TACD is "a forward-looking blueprint rather than a complete implementation" (line 252). While the three components (cross-translation benchmarking, TS-Guessing across variants, back-translation consistency) are reasonable ideas, there are no experiments, implementation, or validation. The paper should not count TACD as a contribution in its current unimplemented form.

7. **Arabic proficiency claim is unsupported.** The abstract claims models with "stronger Arabic capabilities" benefit more from contamination, but no Arabic proficiency metric is reported or controlled for. The four models differ on many axes (size, training data, architecture) beyond Arabic competence.

### Trivial
None.

## Nice-to-Haves
- Running the English-only contamination control (weakness #1) would directly test the core thesis.
- Reporting results across 3+ random seeds would enable assessment of statistical reliability.
- Adding Arabic proficiency metrics would substantiate the claim about Arabic-capable models benefiting more.

## Removed Points

The following criticisms from the input review were removed under the filtering rules:

1. **"The experimental design does not study contamination—it studies targeted test-set memorization"** — Removed because it overstates the problem. The paper studies a controlled form of contamination (fine-tuning on translated test sets), which is a valid experimental paradigm for investigating whether translation affects contamination detectability. The paper is transparent about its setup. The remaining weaknesses (#1, #4 above) already capture the legitimate design concerns without dismissing the entire paradigm as irrelevant.

2. **Section-by-section notes about presentation quality and missing appendix content** — Removed. Appendix content was stripped by the PDF extraction process. The paper states hyperparameters are in Appendix A (line 262), so this is a parser artifact, not an author omission.

3. **Reproducibility concerns about undisclosed hyperparameters** — Removed. The paper refers to Appendix A for these details (line 262-264), which was stripped by the parser.

4. **"What is D_EN^d exactly?" ambiguity for XQuAD/MLQA** — Partially addressed by the paper's description ("English QA"). While somewhat ambiguous, this is a relatively minor clarification issue and is subsumed by weakness #4 above.

## Novel Insights

The key insight emerging from the review is that the paper's central claim requires a comparison it never runs: the English-only contamination control. Without it, the paper cannot attribute the null TS-Guessing results to translation rather than to probe insensitivity. The internal contradiction between Sections 4.1 and 4.2 (monotonic increase vs. near-flat trend) is a genuine coherence issue. The observation that the p=0 baseline is already contaminated with English test data is another structural concern that weakens the experimental interpretation.

## Suggestions

1. Add an English-only contamination condition (fine-tune on English test data at p ∈ {10, 50, 100}%) and compare TS-Guessing detection rates between the English and Arabic conditions. This directly tests whether translation masks contamination.
2. Resolve the contradiction between the monotonic MMLU increases in Section 4.1 and the "near-flat" characterization in Section 4.2.
3. Validate TS-Guessing on a positive control (models fine-tuned on English test data) to confirm the probe can detect contamination when it exists.
4. Clarify what D_EN^d contains for each dataset (especially XQuAD/MLQA) and acknowledge that p=0 is not a clean baseline.
5. Report results with multiple random seeds and standard deviations.
6. Either implement and validate TACD, or reframe it as explicit future work rather than a claimed contribution.

---

**Calibration Anchors.** The following human-scored papers were retrieved during calibration:

| Paper | Avg Score | Round | Comparison |
|---|---|---|---|
| Evading Data Contamination Detection (Nk1MegaPuG) | 4.25 | 1,2 | Similar topic (evading detection); concrete attack but incomplete validation. Comparable quality level. |
| Benchmark Inflation (rAylWUIKtu) | 4.25 | 1,2 | Methodology for retro-holdouts; criticized for narrow scope. Similar level of contribution. |
| Elephants Never Forget (lwtaEhDx9x) | 4.75 | 1,2 | Memorization tests for tabular data; mixed reception. Slightly stronger empirical contribution. |
| Predicting Memorization in fine-tuned LLMs (XcSJ6hoc1O) | 4.00 | 2 | Lower-scored memorization paper; weaker validation. |
| Crosslingual Capabilities (BCyAlMoyx5) | 5.67 | 2 | Solid cross-lingual analysis with experiments; stronger execution. |
| How much can we Forget (Nsms7NeU2x) | 6.75 | 1,2 | Comprehensive contamination study with theory; clearly stronger. |
| To the Cutoff and Beyond (m2NVG4Htxs) | 6.75 | 1,2 | Longitudinal contamination analysis with strong evidence; clearly stronger. |
| Detecting Pretraining Data (zWqr3MQuNs) | 6.25 | 2 | Well-executed detection benchmark; stronger. |

**Round 1 bracket:** The paper sits in the 3.5–5.5 range based on comparison to contamination papers. **Narrowing:** The paper is weaker than the 6+ papers ("How much can we Forget", "To the Cutoff") due to missing critical controls and internal contradictions. It is comparable to "Evading Data Contamination Detection" (4.25) and "Elephants Never Forget" (4.75), which share similar patterns of an interesting question with incomplete validation. I place it at the lower end of this band because the missing English-only control is more central to the paper's thesis than the gaps in the comparison papers.

MY FINAL SCORE: <score>4.0</score>
MY FINAL DECISION: <decision>Reject</decision>