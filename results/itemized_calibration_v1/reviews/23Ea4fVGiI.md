Now let me write the final consolidated review.

## Summary

This paper introduces Task-Method-Knowledge (TMK) structured prompting, adapted from cognitive science and intelligent-agent architectures, to improve LLM planning performance on the PlanBench Blocksworld benchmark. Evaluated on GPT-4, GPT-4o, o1, o1-mini, and GPT-5, the method shows consistent improvements, with a headline result on o1 for Random Blocksworld (31.5% → 97.3%), demonstrating what the paper calls a "performance inversion" where opaque symbolic tasks become easier than semantically meaningful ones under TMK prompting.

## Strengths

1. **Novel methodological transfer.** Borrowing TMK from cognitive science / intelligent-agent architectures and applying it to LLM prompting is genuinely novel. The paper is not recycling another variant of "add chain-of-thought" or "add structured reasoning tags."

2. **Genuinely interesting phenomenon.** The "performance inversion" — o1 going from 31.5% → 97.3% on Random Blocksworld while improving only modestly on Mystery (74.3% → 83.3%) — is a surprising and noteworthy result that warrants attention and further investigation.

3. **Well-motivated design against known criticisms.** The paper correctly identifies that prior prompting-for-planning work (CoT, ReACT) has been credibly criticized for issues like n-shot pattern matching and partial evaluation, and explicitly designs its protocol to address these criticisms (Section 5.1). This is a principled starting point.

## Weaknesses

### Major

1. **Unevaluated extraction function confound for the headline result.** In Section 3.2 (lines 183–191), the authors state that the Valmeekam (2023) extraction code "required update" for Random Blocksworld, and that they "added new code to the extraction criteria which was applied for random blocksworld data set." The enhanced extraction is more lenient: it ignores extraneous symbols ("-", "_"), word substitutions ("o", "obj" for "object"), and paraphrased action steps. **The plain-text baseline results in Table 2 for Random Blocksworld — the domain where the headline 65.8% improvement is reported — come from the public PlanBench leaderboard (Valmeekam, 2023), which used the original (unmodified) extraction code.** Because TMK results and baseline results were evaluated with different extraction functions, we cannot determine how much of the reported gain reflects genuine planning improvement versus a more permissive evaluation. The authors should re-evaluate the plain-text baseline using their own enhanced extraction, or evaluate TMK using the original extraction, and report both sets of results.

2. **No ablation isolating what TMK contributes vs. structured JSON or detailed operator information.** The TMK prompt is a complex intervention: it adds structured JSON, hierarchical decomposition, explicit pre/post conditions, teleological framing, and domain knowledge all at once. There is no control condition where the same Blocksworld operator information is provided in an alternative structured format (e.g., plain JSON without TMK's Task/Method/Knowledge framing, or a PDDL-like description). Without these controls, we cannot attribute gains specifically to the TMK framework's structure — they could equally arise from simply providing more detailed operator descriptions in a structured format, which any knowledge-representation approach would provide.

### Minor

1. **Comparison confound: one-shot TMK vs. best-of-zero/one-shot plain text.** Table 2 compares one-shot TMK against plain-text baselines described as "best of sampled Zero & One shot." The authors argue this is conservative because zero-shot is harder (Section 3.2), but the claim that zero-shot outperforms one-shot on these specific models and problems is verified only through "sample testing" in an external OSF repository rather than reported directly. Running one-shot plain text on the same models under the same extraction function would remove this confound entirely.

2. **No statistical reliability information.** Every result in Table 2 is a single point estimate with no error bars, confidence intervals, or variance measures. The paper does not report the number of test problems, temperature settings, or number of trials. For modest improvements (e.g., GPT-4 Classic: 34.6% → 39.7%), run-to-run variance could easily account for the difference.

3. **The "symbolic steering" hypothesis is presented as a finding rather than a hypothesis.** The abstract and conclusion claim that TMK "steers reasoning models away from their default linguistic modes to engage formal, code-execution pathways." However, the paper provides no direct evidence about the model's internal reasoning mode — no analysis of reasoning traces, no comparison of attention patterns, and no experiments distinguishing the steering hypothesis from simpler alternatives (e.g., TMK provides better operator definitions that happen to help more on Random than Mystery). The paper partially acknowledges this (Section 5.3, line 303: "the cause of that increase is left to future work"), but the abstract and conclusion present the steering claim as a confirmed finding.

### Trivial

- The paper does not state the number of test instances, temperature, or generation parameters, which are standard reporting details for LLM evaluation on planning tasks.
- The one-shot example used in the TMK prompt is not shown in the main text (relegated to appendix/OSF), making it difficult for readers to assess potential pattern matching.

## Nice-to-Haves

- A comparison against CoT prompting as a baseline would contextualize the TMK results against the most widely-criticized prompting method the paper discusses.
- The o1-mini outlier (Mystery: 19.1% → 16.83%) is noted but not deeply analyzed. The asymmetry between Mystery (degradation) and Random (improvement) could be diagnostically informative for the paper's steering hypothesis.

## Removed Points

- **"Single domain, single model family":** Removed because the paper explicitly acknowledges this limitation (Section 5.3). This is a scope note, not a flaw in what was done.
- **"o1-preview in Table 2 is misleading":** Removed because the paper clearly notes o1-preview is deprecated and results are from Valmeekam (2023). This adds useful historical context.
- **"TMK superiority over BDI/HTN claimed without comparison":** Removed because the paper describes why TMK was chosen (Section 2.3), not as an empirical superiority claim.
- **"Section 3.1.4 prompt differences across domains":** Removed because the paper acknowledges this ("efforts are made to keep it as similar as possible, given constraints"). The comparison is within-domain (TMK vs. plain text for each domain separately), not a cross-domain A/B test.

## Novel Insights

The key insight from the review is that the paper's headline result depends on a comparison across two different extraction functions — a confound that is disclosed but not addressed. This is more specific and actionable than generic concerns about "evaluation rigor." The call for ablation controls (structured JSON without TMK framing) is a grounded suggestion that directly tests whether the TMK framework's specific structure contributes beyond general structured formatting. The observation that the "symbolic steering" hypothesis, while plausible, is stated more strongly as a finding than the evidence supports, is a useful calibration of the paper's claims versus its empirical support.

## Suggestions

1. **Re-evaluate the plain-text baseline** using the same enhanced extraction function used for TMK results, especially for Random Blocksworld. Report both the original and re-evaluated numbers.
2. **Run one-shot plain text** on all tested models under the same extraction function for a clean comparison.
3. **Add at least one ablation control:** provide the same Blocksworld operator definitions in a structured JSON format without TMK's Task/Method/Knowledge framing.
4. **Report variance information:** number of test instances, temperature, and run-to-run variability (e.g., 3 runs with different seeds).
5. **Tone down the "symbolic steering" language** in the abstract and conclusion to match what the evidence supports, or add direct evidence for the claimed mechanism (e.g., analysis of reasoning traces).

## Score and Decision

**Score calibration.** Four anchors were itemized:

| Anchor | Avg Score | Comparison to this paper |
|--------|-----------|-------------------------|
| `jOuHjFw71C.md` ("Planning in Strawberry Fields") | 3.00 | Similar evaluation of o1 models on planning benchmarks, but this paper has the additional novelty of TMK transfer; should score higher. |
| `koza5fePTs.md` ("Exploring and Benchmarking Planning Capabilities of LLMs") | 2.00 | Criticized for lacking novelty; this paper has genuine novelty, so should score higher. |
| `85Ik12q2hP.md` ("Do Think Tags Really Help LLMs Plan?") | 4.00 | Similar evaluation-quality concerns and critical analysis, but this paper has a positive contribution (novel prompting method) that the anchor lacks. |
| `K3KrOsR6y9.md` ("LLMs Can Plan Only If We Tell Them") | 6.40 | Achieves SOTA on Blocksworld with clean evaluation and ablation; this paper shares missing-baseline and no-variance weaknesses but additionally has the extraction confound, so should score lower. |

**Round-1 bracket:** 3.0–6.4. **Narrowing:** The extraction confound (no anchor in this range has a comparable measurement issue) and lack of ablation push this paper below the 5.25–6.40 band occupied by papers with cleaner evaluations. The genuine novelty of TMK transfer and the interesting performance-inversion phenomenon lift it above the 2.0–3.0 band occupied by papers that merely benchmark existing models or lack novel contributions. The most comparable anchor is the 4.00 "Do Think Tags" paper, which shares critical-evaluation weaknesses but lacks a positive contribution.

MY FINAL SCORE: <score>4.5</score>
MY FINAL DECISION: <decision>Reject</decision>