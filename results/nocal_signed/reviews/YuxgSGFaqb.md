## Summary

SWINGARENA introduces an adversarial evaluation framework for LLM-based code generation that pairs two models as *submitter* (generates patches) and *reviewer* (generates tests to break the patch) in a CI-gated competitive loop, with role-switching across rounds. The paper curates 400 high-quality GitHub issues across C++, Python, Rust, and Go from 2,300 candidates, filtered through CI pipelines and expert review. Experiments across GPT-4o, Claude, Gemini, DeepSeek, and open-source models reveal behavioral trade-offs: some models excel at adversarial patch generation (high win rates) while others prioritize CI stability (higher SPR/RPR).

## Strengths

- **A genuinely novel evaluation paradigm.** The adversarial submitter–reviewer protocol embedded in real CI pipelines is a real conceptual step beyond static, single-pass benchmarks like SWE-Bench or HumanEval. The role-switching design and the scoring scheme that rewards both successful patching and effective testing together create a richer, more dynamic signal than a single pass/fail. This is the most interesting evaluation idea in LLM code generation since SWE-Bench. *(impact: +9.9)*

- **Multi-language, real-CI dataset with expert curation.** The paper curates 2,300 real GitHub issues across C++, Python, Rust, and Go, filtering through actual CI pipelines and human expert review to produce 400 evaluation instances. Multi-language coverage addresses a known limitation of Python-only benchmarks, and CI-grounded validation (build, lint, style, security checks) catches failures that unit-test-only evaluations miss. *(impact: +7.9)*

- **Non-obvious empirical patterns.** The finding that GPT-4o achieves high win rates as a submitter while having lower CI pass rates (SPR/RPR) than DeepSeek or Gemini reveals a genuine trade-off between assertive adversarial patching and reliable CI-compliant patching. This behavioral differentiation is exactly what a good benchmark should surface. *(impact: +6.7)*

## Weaknesses

### Fatal
None.

### Major

- **The win rate metric is inherently ambiguous and the headline conclusions over-interpret it.** The paper acknowledges at line 148 that "higher values may also indicate weaker reviewer tests, so it should be interpreted together with SPR/RPR," and does report SPR/RPR alongside win rates. However, the central claim — "GPT-4o achieves win rates ≥ 0.90 as a submitter regardless of the reviewer, highlighting its dominance in producing adversarially-strong patches" (line 187–189) — goes beyond what the metric can bear. The self-play results (Claude 1.00, GPT-4o 0.97) are trivially inflated because the same model writes both the patch and the test, producing natural alignment. While SPR/RPR reporting provides partial disambiguation, the paper's behavioral taxonomy is built on a metric whose signal is partially a property of reviewer behavior, not submitter quality. *(impact: combined -20.6 across sub-items)*

- **No comparison with existing benchmarks (SWE-Bench) to validate that the framework produces different or deeper insights.** The paper argues SWINGARENA reveals "nuanced trade-offs that static benchmarks miss" (line 36), but provides no demonstration that its rankings or failure modes diverge from those of SWE-Bench on comparable tasks. Without a side-by-side comparison, the central positioning claim — that the extra complexity of the adversarial CI framework yields genuinely new signal rather than correlated measurements — remains unvalidated. *(impact: -8.5)*

### Minor

- **RACG ablation evidence is thin.** Table 3 shows modest Best@3 improvements (+0.02 to +0.09) and Win Rate improvements (+0.03 to +0.13) from RACG, with no confidence intervals, significance tests, or variance estimates. The single-run (temperature=0) design means the +0.04 C++ Best@3 improvement (0.38→0.42) could be within task-selection noise. The paper's own results show Top-20 retrieval achieves Best@3=0.43, which is competitive with RACG, further weakening the evidence that the full pipeline is necessary. *(impact: -3.6)*

- **Expert filtering details are missing.** The paper does not report number of annotators, their background/expertise, inter-annotator agreement, or discard rates at each pipeline stage (line 78). These are standard for dataset papers and critical for assessing dataset quality. *(impact: -0.8)*

- **The common token budget B for model harmonization is never specified numerically** (line 181), making it hard to assess whether the harmonization was fair across models with different context windows. *(impact: -0.5)*

### Trivial

- The battle protocol is described in near-identical terms at lines 96 and 124–128, suggesting an editing redundancy. *(impact: -0.4)*

## Nice-to-Haves

- A human baseline (even small-scale) would calibrate benchmark difficulty and establish what "good" performance looks like.
- A contamination analysis (e.g., measuring performance as a function of repository star count or checking for near-duplicate issues in training data) would strengthen confidence that the benchmark measures generalization.
- Approximate cost and wall-clock time for running the full arena would help the community assess practical usability.

## Removed Points

These points were surfaced in the review process but are excluded from the main assessment for the following reasons:

- **"Reviewer test quality gates are too weak"** — Removed as speculative. The hypothesis that a reviewer could write trivial tests is countered by the scoring mechanism: the reviewer gets +1 only if the test *fails* the submitter's patch, creating a strong incentive against trivial tests. No experimental evidence of degenerate behavior is provided.
- **"The paper never returns to its three blind spots in the experiments"** — Removed as inaccurate. The main results (line 187–189) discuss trade-offs between patch assertiveness and correctness, which directly addresses blind spots 1 and 3.
- **"Table 2 differences are within noise"** — Removed as overblown. The paper describes the small differences factually without over-claiming, and 100 samples per language is a standard benchmark size.
- **"RACG limits context rather than enabling long-context reasoning"** — Removed as a design-choice confusion. The paper explicitly positions RACG as a mechanism for standardized context access across models (line 28), not as a long-context capability claim.
- **Data contamination, human baseline, cost/runtime** — Moved to Nice-to-Haves. These are suggestions for strengthening, not weaknesses that undermine the contribution.

## Novel Insights

None beyond the paper's own contributions. The reviews surface a useful observation about the win-rate metric's ambiguity and the need for cross-benchmark validation, but these elaborate on limitations the paper partially acknowledges rather than discovering new phenomena.

## Suggestions

1. **Disambiguate the win rate metric**: Hold one reviewer model fixed and vary submitters, reporting win rates per reviewer. This would separate submitter quality from reviewer effects.
2. **Compare against SWE-Bench**: Run SWE-Bench or its multi-language extensions on a shared subset of tasks to validate that SWINGARENA surfaces different signal, or demonstrate that its rankings diverge from static benchmarks.
3. **Report variance**: Add bootstrapped confidence intervals or per-language standard deviations to Tables 1–3 to establish which differences are meaningful.
4. **Specify the token budget B** used for model harmonization.
5. **Report expert-filtering statistics**: number of annotators, their background, inter-annotator agreement, and discard rates at each pipeline stage.

## Score and Decision

The paper proposes a genuinely novel and well-motivated evaluation framework — the adversarial submitter–reviewer CI protocol is conceptually significant and represents a real advance over static benchmarks. The dataset curation across four languages with expert filtering and CI validation is a substantial engineering contribution, and the empirical findings reveal interesting behavioral trade-offs among frontier models. The major weaknesses (metric ambiguity and lack of SWE-Bench comparison) are real but addressable — they concern the interpretive weight placed on the results, not a flaw in the framework itself. The paper acknowledges the metric caveat and provides complementary metrics (SPR/RPR) that partially mitigate the concern. On balance, the contribution is strong enough to warrant acceptance.

**MY FINAL SCORE**: <score>8</score>
**MY FINAL DECISION**: <decision>Accept</decision>