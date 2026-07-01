Now let me write the final consolidated review.

## Summary

This paper investigates whether structuring prompts with the Task-Method-Knowledge (TMK) framework — a knowledge representation from cognitive science — improves LLM performance on the PlanBench Blocksworld planning benchmark. Across models ranging from GPT-4 to o1 and GPT-5, TMK-structured prompts generally improve accuracy, with the headline result being o1 improving from 31.5% to 97.33% on the opaque Random Blocksworld variant, producing a "performance inversion" where the model does better on symbolic tasks than semantic ones. The paper interprets this as evidence that TMK steers models toward "code-execution pathways."

## Strengths

1. **The performance inversion result (Table 2, o1 on Random vs. Mystery).** The finding that o1 under TMK achieves 97.33% on Random Blocksworld (vs. 31.5% plain-text) while scoring 83.3% on Mystery (vs. 74.3% plain-text) — reversing the usual difficulty ordering — is a concrete, specific behavioral phenomenon that genuinely motivates follow-up investigation, even if its mechanistic interpretation remains unsettled.

2. **Clear diagnosis of prior work's methodological flaws (Section 2.1–2.2).** The paper correctly identifies the key criticisms of prior prompting-for-planning work: n-shot pattern matching, final-answer-only evaluation, and lack of formal plan validation. Its decision to use PlanBench (which validates full plans via automated planners) and to report one-shot results with a non-matching example is a reasonable attempt to address these issues.

3. **The TMK framework is clearly described (Section 3.1, Figure 1).** The hierarchical decomposition into Tasks, Methods, and Knowledge, with explicit preconditions and effects, is well-illustrated. The rationale for why this structure might help (providing precise domain semantics in a format aligned with structured-training data) is easy to follow.

## Weaknesses

### Fatal
None.

### Major

1. **Mechanistic claims significantly overreach the experimental evidence (Abstract, Section 5.2.1, Conclusion).** The abstract claims TMK "functions not merely as context, but also as a mechanism that steers reasoning models away from their default linguistic modes to engage formal, code-execution pathways." Section 5.2.1 states the performance inversion "serves as empirical validation of this steering effect." The conclusion frames this as established: "This confirms that TMK acts as a symbolic scaffold, effectively steering reasoning models toward formal code-like manipulation."

   The experiments measure only **output accuracy**. No internal representations, attention patterns, inference-token analyses, or controlled baselines (e.g., a different structured format without TMK's teleological content) are presented. The performance inversion is **consistent with** a code-like processing shift, but it is also consistent with simpler explanations — e.g., the TMK prompt simply conveys domain semantics more precisely, or the JSON structure reduces output-format errors regardless of processing mode. Claiming "validation" or "confirmation" of a specific mechanistic pathway goes well beyond what the evidence supports. The paper would be substantially stronger if it clearly separated the behavioral results from the speculative interpretation.

2. **Insufficient transparency about evaluation pipeline uniformity (Section 3.2, lines 183–193, Table 2 caption).** The paper describes an "enhanced extraction function" for Random Blocksworld that tolerates variant action labels, extra symbols, and alternate wording. What is not clearly stated is whether this enhanced extraction was applied uniformly to **both** the plain-text and TMK conditions for every model. The paper indicates it ran its own evaluations for "newer models" (o1, GPT-5, o1-mini — line 193), strongly implying the comparison is fair for those models. However, the Table 2 caption's note about "Results extracted from Valmeekam (2023)" is ambiguously placed (it is attached via an asterisk to o1preview, but the formatting could confuse readers). For o1preview, the plain-text baseline uses the original PlanBench extraction while TMK is N/A, so no comparison is affected. **Nevertheless**, the paper never explicitly states "the enhanced extraction was used for both plain-text and TMK conditions across all models we evaluated." A clear, unambiguous methodology statement is essential for readers to trust the headline 31.5% → 97.33% result.

### Minor

3. **No variance or multiple-trial information (Table 2).** All accuracy numbers are reported as point estimates with no confidence intervals, number of trials, or discussion of run-to-run variability. LLM outputs are known to vary across runs. For modest gains (e.g., GPT4 Classic: 34.6% → 39.7%; GPT-5 Mystery: 98.1% → 98.3%), the reader cannot assess whether these improvements exceed run-to-run noise. The paper should at minimum state the number of trials per condition and ideally provide variance estimates.

4. **The o1-mini outlier is acknowledged but not deeply engaged with (Section 4.2, Section 5.2.2, Conclusion).** o1-mini shows a *decrease* on Mystery (19.1% → 16.83%) and only flat performance on Classic (56.7% → 57.0%). The paper attributes this to "capacity limitations" and "semantic overload" — speculative explanations that are not tested. If TMK works by invoking code-like processing pathways, then o1-mini's selective degradation on Mystery (not on Classic or Random) requires more explanation than the paper provides. This inconsistency limits the generalizability of the central claim.

5. **The cognitive scaffolding discussion is not connected to any experimental variable (Section 5.2.2).** The discussion of Bloom's taxonomy, cognitive load theory, and the worked example effect reads as a separate literature review. No experimental manipulation targets these constructs, and no observable variable in the study measures cognitive load or procedural vs. factual focus in the model's outputs. This section does not advance the paper's argument.

### Trivial
None.

## Nice-to-Haves

- **A controlled comparison against another structured format** (e.g., flat JSON action table without TMK's teleological linking) would directly test whether TMK's specific structure drives the gains or whether any well-formatted domain description would suffice.
- **Inference-token analysis** for models with transparent reasoning traces could provide direct evidence for or against the code-execution pathway hypothesis.
- **The number of test problems per Blocksworld variant** should be stated so readers can contextualize the percentages.

## Removed Points

- **"The extraction function change may invalidate the comparison" (reviewer's Critical Issue 1).** The reviewer speculates that plain-text baselines for o1, GPT-5, and o1-mini "were taken from the PlanBench leaderboard." The paper states it "further confirm[s] these findings by running the PlanBench benchmark for newer models for which it has not been reported" (line 193), meaning these models' plain-text numbers are from the authors' own runs, not the leaderboard. The o1preview row — the only one flagged with an asterisk referencing Valmeekam (2023) — has N/A for TMK, so no comparison is affected. The concern is therefore largely speculative; what remains is the valid transparency point noted above in Major #2.

- **"The one-shot example content is not fully described" (reviewer's Critical Issue 6).** The paper references an OSF repository and appendix A for the full prompts. The appendix was stripped by the parser, not omitted by the authors. This is not a weakness of the paper.

- **Reviewer's Section-by-Section notes on Abstract, Section 2.1, Section 4.2, Section 5.2.1, Section 5.2.2.** These are merged into the major/minor weaknesses above (primarily the mechanistic overclaiming point). The note about Section 2.1 being "well-articulated" is not a weakness.

- **"Missing Parts and Places to Improve" items about temperature, sampling parameters, GPT-4o-mini.** These are suggestions for strengthening the paper, not weaknesses of the current submission. The temperature/sampling concern is covered by the variance reporting point (Minor #3). The suggestion about GPT-4o-mini is a nice-to-have.

## Novel Insights

None beyond the paper's own contributions. The reviews surface a consistent concern about the gap between the paper's mechanistic claims and its behavioral evidence, and raise legitimate questions about methodological transparency, but these are critiques of known issues rather than novel discoveries about the science.

## Suggestions

1. **Clearly separate behavioral findings from mechanistic interpretation.** Rewrite the abstract, Section 5.2.1, and conclusion to present the "code-execution pathway" as a hypothesis consistent with the results, not a conclusion validated by them. The performance inversion and accuracy gains are the paper's contributions; the interpretation is a secondary discussion point.

2. **Add a methodology section explicitly stating:** (a) which models' plain-text baselines were run by the authors vs. taken from external sources, (b) that the enhanced extraction function was applied uniformly to both conditions for all author-run experiments, and (c) the number of test instances and trials per condition.

3. **Include variance information** (number of runs per condition, ideally confidence intervals or standard deviations) for the headline results, particularly the o1 Random Blocksworld comparison.

## Score and Decision

MY FINAL SCORE: <score>6.0</score>
MY FINAL DECISION: <decision>Accept</decision>