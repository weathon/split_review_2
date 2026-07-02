## Summary
SWINGARENA presents an evaluation framework for LLMs on long-context GitHub issue solving, pairing models as submitters (patch generators) and reviewers (test generators) evaluated through real CI pipelines across C++, Python, Rust, and Go. It also introduces a RACG retrieval module and a curated dataset of 400 CI-grounded instances. The paper's main contributions are the multi-language CI-integrated protocol, the adversarial battle formulation, and the RACG baseline.

## Strengths
1. **Multi-language CI integration is a genuine engineering advance.** Going beyond SWE-bench's Python-only unit-test paradigm to support C++, Python, Rust, and Go with real CI workflows (GitHub Actions, Travis CI) running in Docker containers raises the realism bar substantially (Section 4.1, Data Division; Section 3.2, Verification).

2. **The submitter-reviewer dual-role protocol with role-switching is conceptually novel.** Having models act as both patch generators and test generators, with scoring that incentivizes finding tests that differentiate correct from incorrect patches, goes beyond the static one-shot paradigm of existing benchmarks (Section 3.2, Battle Protocol).

3. **Data construction pipeline is thorough and well-motivated.** The four-stage pipeline (repository mining → CI filtering → LLM filtering → expert filtering) employs both automated filtering and human expert verification, yielding higher-quality instances than fully automated pipelines (Section 3.1).

4. **Variance control is commendable.** Temperature=0, fixed prompts, pinned Docker images, fixed random seeds — the paper takes reproducibility seriously in a setting where variance would be easy to overlook (Section 3.3, Variance Control).

## Weaknesses

### Major
1. **The "adversarial" framing is overclaimed relative to what the protocol actually implements.** The reviewer is constrained to write tests that must pass the golden patch (Section 3.2, Reviewer Test Quality Gates: "compile and pass when applied to the golden patch"), and is penalized if a test fails the golden patch. This means the reviewer's optimal strategy is to write tests that differentiate correct from incorrect patches — which is closer to quality assurance than adversarial competition. More critically, Table 1 includes self-play scenarios (same model as submitter and reviewer) where Claude-vs-Claude achieves win rate 1.00 and GPT-4o-vs-GPT-4o achieves 0.97. The paper interprets this as "strong internal alignment" (line 187), but the equally plausible interpretation is that a model writing tests for its own patches is circular — the test matches the patch's implementation choices rather than independently probing the specification. The paper acknowledges that "Win Rate is *adversarial*: higher values may also indicate weaker reviewer tests" (line 148), but this acknowledgment undercuts the main result table without resolving the ambiguity.

2. **Main experimental results are near-ceiling and do not differentiate models meaningfully.** Table 1 reports win rates of 0.89–1.00 across 16 matchups, with 12 of 16 entries at ≥0.94. Every model achieves win rates ≥0.89 as a submitter regardless of the reviewer. The more differentiated metrics (SPR 0.54–0.68, RPR 0.59–0.72, Best@3 0.50–0.64) show modest spreads (e.g., Best@3 spread from best to worst is only 0.09), and the paper reports no confidence intervals, error bars, or significance tests on any result. With 100 instances per language, the uncertainty on every reported number is material, making it unclear whether observed ranking differences would replicate.

3. **No comparison to SWE-bench or any existing benchmark.** The paper repeatedly positions itself relative to SWE-bench — criticizing its Python-only focus, static unit tests, and one-shot paradigm (lines 17, 54) — yet provides no comparison of how the same models perform on SWE-bench vs. SWINGARENA. For a benchmark paper, this is a critical omission. Without it, the reader cannot assess whether SWINGARENA surfaces different insights about model capabilities or largely confirms known rankings, nor whether the adversarial protocol adds signal beyond what simpler multi-language CI evaluation would provide.

### Minor
4. **The "w/o RACG" condition in the ablation study (Table 3) is never defined.** The paper shows "C++ w/o RACG" / "Python w/o RACG" etc. (lines 237–244) but never specifies whether the model receives no code context, the full raw codebase, a random subset, or some other baseline. Without this definition, the ablation results (e.g., Best@3 improving from 0.38 to 0.42 for C++) are uninterpretable. Additionally, the ablation uses Qwen2.5-Coder-7B-Instruct (a 7B model), which the paper does not explicitly state in the ablation section itself — the reader must infer this from line 134. RACG's benefits on a small model with limited context may not transfer to the frontier models used in the main results.

5. **Best@k metric is unclearly specified across tables.** The formal definition (line 140) defines "solved" in terms of an unspecified success function. Table 2 presents "Best@3 across Models and Languages" without clarifying whether this measures submitter performance, reviewer performance, or battle outcome. The gap between Best@3 values (0.37–0.58) and Win Rate values (0.71–0.84) in Table 3 for the same model is large and unexplained, undermining confidence in both metrics.

6. **No confidence intervals or statistical testing on any result.** The paper reports point estimates for all metrics (Tables 1, 2, 3) without error bars, confidence intervals, or significance tests. For a benchmark paper advocating a new evaluation framework, establishing the reliability and discriminative power of the metrics is essential.

### Trivial
7. **"PK-style" terminology** in the contributions list (line 32) is used without definition.

8. The **battle protocol description** appears in two places (lines 96–97 and lines 124–128) with near-verbatim overlap.

## Nice-to-Haves
- A controlled comparison against SWE-bench (or similar static benchmarks) showing whether rankings change or new failure modes emerge under the adversarial protocol.
- Analysis of which CI gates actually fail (compilation errors vs. test failures vs. linting violations) to help practitioners understand what the benchmark measures.
- Using different models as submitter and reviewer (rather than self-play) more consistently, or blinding the reviewer to which model produced the patch.
- Explicitly define the "w/o RACG" condition so the ablation is interpretable.

## Removed Points
These points were raised in the input review but are removed or demoted with justification:
- **Missing related work (CodexGraph, RepoExplain, etc.):** Removed per instructions — do not flag missing related work without external verification.
- **"Owen2.5 vs Qwen2.5 typo":** Removed per instructions — formatting/typo criticisms are parser artifacts.
- **"Three critical blind spots are generic":** Removed — this is a framing critique, not a concrete weakness about what the paper does.
- **"CodeBERT is old (2020)":** Demoted to nice-to-have — the paper positions RACG as a baseline; using a newer model is straightforward to swap.
- **"Grok-3-beta choice unexplained":** Removed — the paper explains it is used for LLM-as-a-Judge filtering (line 76); the specific model choice is not central.
- **"Data construction lacks quantitative detail (attrition rates)":** Weakened — the paper provides 2,300→400 instance numbers; more detail would be nice but the pipeline is adequately described.
- **"No analysis of CI failure types":** Moved to nice-to-haves.
- **"The paper's conclusion overstates what 400 instances can achieve":** Removed — 400 instances across 4 languages is a reasonable benchmark size.

## Novel Insights
None beyond the paper's own contributions.

## Suggestions
1. Add a direct comparison between SWINGARENA results and SWE-bench results for the same models to demonstrate that the adversarial protocol provides information not available from simpler evaluations.
2. Report confidence intervals (e.g., bootstrap) on all metrics, especially given the modest number of instances per language (100).
3. Explicitly define the "w/o RACG" condition in the ablation study, and consider running the same ablation on at least one frontier model.
4. Clarify the operational definition of "solved" for Best@k across different tables, and explain why Best@3 and Win Rate diverge so widely in Table 3.
5. Address the self-play circularity by using different models as submitter and reviewer, or by blinding the reviewer to the patch source.

MY FINAL SCORE: <score>4.5</score>
MY FINAL DECISION: <decision>Reject</decision>