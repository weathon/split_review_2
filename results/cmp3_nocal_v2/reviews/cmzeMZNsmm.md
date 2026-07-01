## Summary

This paper systematically investigates whether Large Reasoning Models (LRMs) benefit from prompt optimization and whether they serve as better prompt optimizers than general-purpose LLMs. Using event extraction (EE) as the primary case study with generalization to two additional tasks, the authors test four models (DeepSeek-R1, o1, GPT-4.5, GPT-4o) in a full 4×4 cross of task-model × optimizer under low-resource (15 examples) and medium-resource (120 examples) conditions at two MCTS depths. The core findings—that LRMs benefit more from prompt optimization than LLMs, that LRMs are effective optimizers, and that they converge faster—are plausible and largely supported by the experimental design.

## Strengths

1. **Systematic experimental design (Sections 3–4, Table 1).** The 4×4 cross of task-model × optimizer across two training-set sizes and two MCTS depths is substantially more thorough than typical prompt-optimization studies, which test a single model or role. This allows cleaner attribution of observed effects.

2. **Multi-faceted analysis beyond aggregate scores (Section 5, Figs. 4–5).** The survival analysis of prompt quality, prompt-length vs. performance analysis, and categorized error analysis provide deeper explanations for why LRM-optimized prompts perform better—notably the discovery that DeepSeek-R1 produces concise, rule-heavy prompts rather than verbose format instructions.

3. **Generalization to two held-out tasks (Table 3).** Showing that the optimization trends replicate on Geometric Shapes (symbolic reasoning) and NCBI Disease NER (biomedical) strengthens the claim that findings are not artifacts of the EE dataset or Python-code output format.

4. **Clear articulation of a timely open question (Section 1).** The paper zeroes in on a specific, debated question—whether increasingly capable reasoning models bypass the need for prompt engineering—rather than offering a generic motivation.

## Weaknesses

### Fatal
None.

### Major

1. **Data integrity concern in Table 1: GPT-4o No-Opt baseline inconsistency and broken delta values.**

   GPT-4o's No-Opt AC F1 score is reported as **26.30** in the "MCTS at depth 1 trained on ACE_med" block but as **12.68** in the "MCTS at depth 5 trained on ACE_med" block—the same model, same development set (the paper states "a consistent development set of 100 examples"). A difference this large (more than 2×) cannot be run-to-run variance.

   Furthermore, within the depth-1 ACE_med block alone, the delta annotations are internally inconsistent. Taking No-Opt = 26.30:
   - GPT-4o→GPT-4o optimizer gives 22.32 (+4.98). But 22.32 − 26.30 = **−3.98**, not +4.98.
   - GPT-4.5 as optimizer gives 27.54 (+14.86). But 27.54 − 26.30 = **1.24**, not 14.86.
   - o1 as optimizer gives 26.30 (+0.00). This checks out.
   - DS-R1 as optimizer gives 25.10 (+12.42). 25.10 − 26.30 = **−1.20**, not 12.42.

   Some of these deltas (14.86, 12.42) would check out if the baseline were 12.68, but others (4.98, 0.00) would not. This means either the No-Opt column entry is misreported, the deltas are computed from inconsistent reference points, or there is a deeper data handling error. Since Table 1 is the paper's central evidence table, this inconsistency must be resolved before the empirical claims can be trusted. The authors should clarify the correct values and explain the discrepancy.

2. **Uncontrolled asymmetry from 2.5-bit quantization of DeepSeek-R1 (Section 4.1).**

   DeepSeek-R1 was quantized to 2.5 bits using UnSloth, while o1, GPT-4o, and GPT-4.5 were accessed via API at full precision. The paper justifies this with a reference to a non-peer-reviewed blog post by the creators of the quantization framework itself. 2.5-bit quantization is extraordinarily aggressive for any large model, especially one with the chain-of-thought structure of DeepSeek-R1. This introduces an uncontrolled asymmetry: if quantization degrades DeepSeek-R1's zero-shot performance, the "gain from optimization" would be artificially inflated, making LRMs appear to benefit more than they would at full precision. Conversely, if quantization primarily harms DeepSeek-R1's ability to *follow* optimized prompts, the conclusions about LRMs as task models could be conservative. Either way, the current citation is insufficient evidence that 2.5-bit quantization preserves prompt-following and optimization behavior. A controlled comparison at higher precision (e.g., 8-bit) on at least one critical condition is needed, or the paper must frankly discuss this as a limitation.

### Minor

3. **No variance or statistical significance reporting (Table 1, Table 3).** Every reported score is a single point. Given the small training sets (15 or 120 examples), the stochasticity of LLM output, and the strategy of selecting the *best* prompt node from each search trajectory, it is plausible that 1–2 point gaps between optimizers are within the noise range. The survival plot (Fig. 5a) provides some distributional information but only for one task model. The main tables need either variance estimates across multiple runs of the full pipeline, or at minimum a statement about the number of runs and observed stability.

4. **Low absolute performance and no reference anchor.** The best AC F1 is 44.26, and no-optimization baselines range from 12.68 to 16.47. The paper uses (a) only 10 of 33 event types, (b) a Python-code generation format not standard in EE evaluation, (c) batch prompting rather than per-example inference, and (d) 2.5-bit quantization for one model. The combination makes it difficult to assess whether prompt optimization is genuinely improving task performance or just recovering from a disadvantaged setup. A single reference point from a standard supervised EE method (e.g., fine-tuned RoBERTa or few-shot GPT-4 with a standard output format) on this exact subset would help readers calibrate whether the optimization is producing meaningful improvements. Without this, the reader cannot distinguish task-specific confounders from generalizable findings.

5. **Small numerical discrepancy in Figure 1 / Abstract table.** DeepSeek-R1's no-optimization score is listed as 16.47 in the figure/abstract (lines 17, 25) but is consistently 16.45 in Table 1. GPT-4.5's is listed as 16.45 in the figure/abstract but is consistently 16.47 in Table 1. These values are swapped. While the difference is tiny (0.02), this transcriptional carelessness compounds the concern about Table 1's accuracy.

### Trivial
- The abstract table (lines 19–26) swaps the 16.45 and 16.47 values for DeepSeek-R1 and GPT-4.5 relative to Table 1. Fix for consistency.

## Nice-to-Haves

- **Reference anchor from standard EE.** A single data point from a standard supervised approach on the same 10-type subset would help interpret the absolute scores.
- **Computational cost discussion.** The paper reports output token counts for task models but says nothing about the cost of running MCTS (multiple optimizer calls, reward computation on a dev set), which is relevant for practitioners.
- **Quantified batch-prompting effect.** The paper notes batch prompting yielded "performance gain than querying the task model for one question at a time" (Section 4.1), but this claim is unquantified. Since it changes the evaluation setup from standard per-example inference, reporting the gain would be informative.
- **Cross-model generalization on additional tasks.** Table 3 tests only self-optimization on the two additional tasks; cross-model optimization would strengthen the claim that LRMs generalize as optimizers beyond EE.

## Removed Points

These points from the input review were removed, with brief justifications:

- **RQ3 overstatement / "abstract and conclusion overstate generality."** Removed because the paper specifically qualifies the "consistently outperforms" claim to the low-resource setting (ACE_low, Depth 1) in the body text (line 179). The abstract and conclusion make general claims about LRMs being better optimizers, which are supported by the data overall. The reviewer's criticism here misunderstands the qualification in the paper.
- **"Section-by-section notes" on RQ3 being overstated on ACE_med.** Removed because the paper explicitly notes "a shift" when a larger training set is available (line 195). The paper already acknowledges this nuance.
- **Criticism that "GPT-4o→GPT-4o optimizer" delta uses wrong baseline.** This is already subsumed by the stronger Table 1 data integrity point (Weakness 1), which covers all the delta inconsistencies.
- **Generic framing about event guidelines not being validated.** The paper's claim about event guidelines is about what guidelines *typically contain* (line 101), not a claim that LRMs discovered real annotation guidelines. This criticism reads too much into an offhand descriptive sentence.
- **"No comparison to standard EE methods" as a separate weakness.** Merged into Minor Weakness 4.
- **The miscellaneous "Section-by-section" notes not already covered.** The comments about MCTS framework being adopted from prior work (Section 3), the downsampling justification (Section 4.1), and the batch prompting note are either already addressed in the paper or are observations that don't constitute weaknesses.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. **Correct Table 1.** Resolve the GPT-4o No-Opt inconsistency and verify all delta values. Provide a corrected table or an explanation of any reporting conventions that resolve the apparent arithmetic errors.
2. **Quantify quantization impact.** Run a controlled comparison of DeepSeek-R1 at 2.5-bit vs. a higher precision (e.g., 8-bit or FP16) on at least the ACE_med self-optimization condition to bound the degradation.
3. **Add variance estimates.** Report results from at least 2–3 independent runs of the full MCTS pipeline for the central comparison (e.g., each model as its own optimizer on ACE_med depth 5) to establish whether the reported rankings are stable.
4. **Add a reference anchor.** Report how a standard fine-tuned EE model (or GPT-4 with a conventional output format) performs on the same 10-type subset to calibrate the absolute numbers.
5. **Fix the minor numerical swap** between Fig. 1 and Table 1 for the DS-R1 / GPT-4.5 no-opt values.

## Score and Decision

This paper asks a well-motivated question with a systematic experimental design that is substantially more thorough than typical work in this space. The core findings are plausible and largely supported by the data. However, the paper currently has a **data integrity problem in its central table** (the GPT-4o No-Opt baseline and delta inconsistencies) and a **methodological weakness** (uncontrolled 2.5-bit quantization of DeepSeek-R1 with insufficient justification) that together prevent full confidence in the reported numbers. These are fixable issues—the research question and design are sound—but they must be resolved. A corrected table and a quantization validation experiment (or candid discussion) would address the most serious concerns.

MY FINAL SCORE: <score>6</score>
MY FINAL DECISION: <decision>Accept</decision>