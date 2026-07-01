Now let me write the final consolidated review.

## Summary

This paper introduces a deletion-based probing framework to evaluate how much LLMs depend on their own chain-of-thought (CoT) traces when solving physics problems. By intercepting CoT generation, deleting varying fractions of tokens (end, random, or physics-aware), and measuring downstream effects on answer score, length, and information overlap, the authors find that accuracy remains stable under 40–60% deletion while answer length increases—a "cramming" pattern where models appear to reconstruct missing reasoning in the final answer. Evaluated across three open-source models (Phi-4, Qwen-A3B, Magistral) and three physics benchmarks, the paper argues that current accuracy-based evaluations are insufficient and that CoT traces are simultaneously informative and redundant.

## Strengths

1. **The core question is well-motivated and timely.** The paper identifies a genuine gap: most evaluations measure end-task accuracy without testing whether models actually depend on their reasoning traces. Physics, with its structured equations, units, and derivations, is a strong testbed where faithfulness is both essential and measurable. Section 1 makes this case clearly and connects it to the broader AI-for-Science agenda.

2. **The deletion sweep design is conceptually clean.** Intercepting CoT mid-generation, systematically removing tokens, and measuring downstream effects on multiple metrics (score, length, information overlap) is a natural and sensible operationalization of "how much does the model actually need this trace." The three deletion strategies (end, random, physics-aware) provide a useful comparison axis that reveals different robustness properties. The figures (Figures 4–7) are largely clear and well-annotated.

3. **The "cramming" observation is genuinely interesting and supported by objective metrics.** The X-shaped pattern where answer length increases as CoT is deleted (Figures 5–6) is a non-obvious finding, and it is corroborated by the information overlap analysis (Figure 7) showing that deleted content reappears in final answers. These two metrics (length and overlap) are objective and do not depend on the LLM judge, lending credibility to the empirical observation.

4. **The information overlap analysis provides a useful quantification tool.** Using Jaccard similarity and Manhattan distance to measure recovery of deleted content in final answers is a sensible approach for a structured domain like physics, and the cross-strategy comparisons (end vs. random vs. physics-aware) surface genuinely different recovery patterns.

## Weaknesses

### Fatal
None.

### Major

1. **The LLM judge used to score answers is not validated, and the paper's central claim depends on it.** The paper relies on Claude-4 Sonnet as a judge to produce the "Score" metric (0–1 based on correctness, derivation accuracy, logic, formatting, and clarity). The judge is provided the expected answer for comparison (Section 2.4), which is helpful, but the paper never validates whether the judge's scores correlate with human expert judgments or with objective correctness metrics (e.g., exact-match on numeric answers for PhyBench). The rubric includes "formatting, and clarity"—factors unrelated to correctness—raising the concern that a longer, well-formatted wrong answer could score higher than a concise correct one. Since the paper's headline finding ("accuracy remains stable under 40–60% deletion") depends on this metric, and since the paper's own thesis warns that LLM outputs can be superficially plausible but unfaithful (citing Turpin et al. 2023, Lanham et al. 2023), the lack of judge validation is a significant gap. The paper does not acknowledge this limitation in Section 4.4.

2. **The "cramming" interpretation is underdetermined by the evidence.** The paper interprets increased answer length and token-level overlap under deletion as evidence that models "reconstruct" missing reasoning. Several alternative explanations are not ruled out:

   - **Verbosity from freed context:** When CoT tokens are deleted, more context window capacity remains, which may cause the model to generate more text in the answer section generically. Without a control where tokens from the *problem input* (not CoT) are deleted at the same rates, it is unclear whether the length increase is CoT-specific or a general response to reduced context length.
   - **Baseline vocabulary overlap:** The information overlap metrics (Jaccard, Manhattan) measure token-level similarity between the deleted CoT and regenerated answers. Two independently generated correct solutions to the same physics problem will share a high baseline of common vocabulary ("force," "mass," "kg," "m/s²"). The paper does not report what "normal" overlap looks like (e.g., overlap between two independently generated solutions without deletion), so the observed overlap numbers are uncalibrated.
   - **Generation from parametric knowledge vs. reconstruction:** Stable accuracy under deletion could mean the model ignores the truncated CoT entirely and solves the problem from its parametric knowledge, producing longer answers simply because it now includes reasoning that was previously in the CoT. This is functionally different from "reconstructing the specific deleted content." The paper's own analysis acknowledges that recovery may reflect "surface-level similarity rather than genuine fidelity" (Section 4.2), but this caveat should be elevated earlier and the "cramming" narrative tempered accordingly.

3. **Missing baseline controls weaken the CoT-specificity of the findings.** The deletion experiments lack:
   - **Input deletion control:** Deleting the same fraction of tokens from the *problem statement* (not the CoT) would test whether accuracy degradation is CoT-specific or a general response to context loss.
   - **CoT replacement control:** Replacing deleted CoT tokens with irrelevant but grammatical text (e.g., filler text) would test whether the effect is about *content* loss or simply *token count* reduction.
   
   Without these, the paper's conclusions about CoT-specific dependence are less precise than they could be.

4. **The practical recommendation about early stopping outruns the evidence.** Section 4.3 suggests that "early stopping of CoT generation may provide a cost-effective way to save tokens without proportionally sacrificing accuracy." The paper tests deletion *after full CoT generation*, not early stopping *during* generation. These are different interventions (one removes already-generated tokens, the other halts generation before completion), and the recommendation is not directly supported by the experiments.

### Minor

1. **Figure 2 omits PhysReason without explanation.** The prompting-style evaluation (Figure 2) presents results for only 2 of the 3 datasets (UG Physics and PhyBench). PhysReason, which is described as part of the benchmark suite (Section 2.1), is absent from this figure with no stated reason.

2. **No statistical significance testing for claimed deletion thresholds.** The paper states that accuracy remains stable until "approximately 40%" (end deletion) or "approximately 60%" (random deletion), but these thresholds are based on visual inspection of line plots. No formal statistical test (e.g., at what deletion fraction does performance first significantly differ from the no-deletion baseline via a paired test) is reported, making the claimed thresholds approximate.

3. **Information overlap metrics lack calibration baselines.** As noted above, the paper does not establish what baseline overlap looks like between two independently generated correct solutions to the same physics problem. Without this calibration, it is unclear whether the observed overlap values reflect genuine reconstruction or merely shared domain vocabulary.

4. **Shared Claude-4 Sonnet dependency.** Claude-4 Sonnet is used both for physics-aware deletion (tagging physics tokens, Section 3.2) and as the evaluation judge (Section 2.4). Any systematic bias in how it identifies "physics content" simultaneously affects which tokens are deleted and how the final answer is scored. This shared dependency is not acknowledged.

### Trivial

- **"PhysBench" typo in Figure 3 caption.** The dataset is called "PhyBench" throughout the paper, but the Figure 3 caption refers to "PhysBench."
- **The "systematic deletion framework" framing slightly overstates methodological novelty.** The core intervention (intercept generation, delete tokens, resume) is a straightforward manipulation of autoregressive decoding. The paper's genuine contribution lies more in the empirical findings than in a new method.

## Nice-to-Haves

- A per-problem breakdown identifying which types of physics problems (e.g., numerical calculation vs. conceptual reasoning) are robust vs. fragile under CoT deletion.
- Reporting whether cramming patterns correlate with model scale (14B vs. 24B vs. 30.5B parameters).
- Formal statistical tests (e.g., paired significance tests at each deletion fraction) to replace eyeballed thresholds.
- A baseline Jaccard/manhattan overlap score computed between two independently generated correct solutions to the same problem, to calibrate the information overlap numbers.

## Removed Points

These points were raised in the input but are removed or downgraded for the following reasons:

- **"No ground-truth correctness verification"** (critic's Point 3). The judge is provided the expected answer for comparison (Section 2.4). The issue is not absence of ground truth but lack of judge *validation*. This is addressed in Major Weakness 1 above.
- **"5-prompt calibration is under-described"** (critic's section notes). The paper describes 50 questions with 5 re-runs and bootstrapped confidence intervals (Section 3.1). This is adequate for a calibration study.
- **"Temperature 0.6–0.7 is relatively high"** (critic's section notes). This range is standard for nucleus sampling with top-p=0.95 and is not a meaningful concern.
- **The critic claims the paper "never reports what the correct answers are for any sample problem"** — the evaluation is done by a judge that compares to the expected answer, which is the standard way to operationalize correctness at scale. Judge validation is the real issue, not the absence of a printed answer key.
- **Strength about "core question well-motivated"** is generic but supported by specific evidence in the paper; retained in Strengths.
- **"Reproducibility details" about appendix** — the appendix is stripped by the parser, not omitted by the authors. Removed per hard rules.
- **Criticisms about missing related works** — removed per hard rules.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. **Validate the LLM judge.** On a held-out sample of 100–200 answers, have physics experts grade the answers on correctness only (not formatting/clarity). Report agreement or correlation with Claude-4 Sonnet scores. For PhyBench problems with numeric answers, also compute exact-match accuracy and compare to the judge scores. If the correlation is high, this addresses the most serious concern.

2. **Add two baseline conditions:** (a) input-deletion (delete tokens from the problem statement at matching rates) and (b) CoT-replacement (replace deleted tokens with irrelevant but coherent text). These directly test whether the observed effects are CoT-specific.

3. **Calibrate the information overlap metrics** by computing Jaccard and Manhattan distances between two independently generated correct solutions to the same problem (no deletion). This provides a baseline for what "normal" overlap looks like.

4. **Tone down the "cramming" narrative.** The length-increase and overlap observations are genuinely interesting, but they should be presented as a behavior consistent with multiple explanations (reconstruction, generic verbosity, parametric knowledge substitution) rather than a demonstrated compensatory mechanism. The conclusion and abstract should reflect this uncertainty.

5. **Add statistical tests** for the claimed deletion thresholds (e.g., at what deletion fraction does accuracy first differ significantly from baseline via a paired t-test or bootstrap test).

## Score and Decision
MY FINAL SCORE: <score>5.0</score>
MY FINAL DECISION: <decision>Reject</decision>