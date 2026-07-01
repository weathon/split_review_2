## Summary

This paper introduces EditBench, a benchmark for evaluating LLMs on instructed code editing tasks. The benchmark is constructed from real-world user data collected via a VS Code extension spanning 458 users. It contains 109 unique problems translated into 5 languages (540 total problems), requires models to integrate code context, highlighted code, and cursor position, and is evaluated across 40 models. The key finding is that EditBench correlates only weakly with existing benchmarks (Aider Polyglot r=0.24, Chatbot Arena r=0.11), suggesting it captures a distinct dimension of code editing capability.

## Strengths

- **Genuinely in-the-wild data source (Section 3.1, Table 2).** The paper convincingly shows that prior edit benchmarks rely on annotator-written or educational problems. Table 2's side-by-side comparison — e.g., real user instructions like "do not use R style, use python style" or pasted error traces vs. the templated, well-specified prompts in prior datasets — makes the qualitative difference clear. The VS Code extension collection method is a legitimate way to obtain this data.

- **Context-dependent problem design (Section 3, Table 1, Table 3).** Including highlighted code and cursor position alongside the full file context is genuinely new for an edit benchmark. The ablation study (Table 3) shows that adding highlighted code changes pass@1 by up to ~3.5 percentage points, demonstrating that this contextual information measurably affects outcomes.

- **Weak correlation with existing benchmarks (Section 5.2).** The finding that EditBench correlates only weakly with Aider Polyglot (r=0.24, p=0.06) and Chatbot Arena coding (r=0.11, p=0.01) is the paper's most interesting result. It supports the claim that the benchmark captures something distinct from existing evaluations. The honest reporting of p=0.06 (just shy of conventional significance) is commendable, and the discussion of why (different interaction modalities, code-centricity, real-world user intent) is reasonable.

- **Broad model coverage.** Evaluating 40 models across multiple families, sizes, and training paradigms (GPT, Qwen, Llama, Mistral, Sonnet, Gemma, DeepSeek, etc.) is a substantial effort that enables meaningful comparative analysis.

## Weaknesses

### Fatal

None.

### Major

None.

### Minor

1. **Effective problem count and missing confidence intervals (Sections 3.2, 4, Abstract).** The paper consistently foregrounds "540 problems" (Abstract, Table 1, Section 4). Section 3.2 discloses that these come from 109 unique problems translated into 5 languages, but the evaluation section never specifies whether results are on the 109-problem core or the 540-problem complete set. With ~109 independent binary outcomes, a model scoring 60% would have a 95% confidence interval of roughly ±9 percentage points (Wilson score interval). This makes fine-grained model comparisons (e.g., ranking models within a few points of each other) less reliable than the presentation suggests. The paper should report confidence intervals on all main results and clarify which problem set is used for evaluation.

2. **No human baseline (Section 5).** A benchmark paper claiming to measure task difficulty should provide a human performance estimate. Without it, statements like "only 1 model scores over 60%" lack calibration — we do not know what a competent human programmer would score. This is standard practice for major benchmark papers (HumanEval, SWE-Bench, etc.) and would meaningfully strengthen the difficulty claims.

3. **Tension between "ambiguity" framing and curation pipeline (Sections 1, 3.2, 3.3, 4).** The paper markets real-world instructions as "ambiguous," "informal," and "less well-specified" (Sections 1, 4), yet Section 3.2 explicitly removes "ambiguous problems" during filtering, and Section 3.3 instructs annotators to remove problems that are "still too ambiguous." The surviving problems are those whose intent was clear enough for annotators to write test cases for. While the paper can still claim value from real-world data *sourcing*, the framing should acknowledge that the curation process necessarily filters out the most ambiguous cases — it is not preserving ambiguity.

4. **Selection bias in data source unacknowledged (Section 3.1).** The 458 users were recruited by offering free access to state-of-the-art models. This selects for developers who cannot or will not pay for these models, are willing to install a research extension, and consent to data collection. This population may skew toward hobbyists, students, or resource-constrained developers, and their tasks may not represent professional software engineering workflows. The paper does not discuss this bias, which would strengthen the paper's credibility if acknowledged.

5. **No analysis of performance across natural languages (Section 4).** The paper touts 5 natural languages as a differentiator but never analyzes whether model performance differs across them. Since the 540 problems are translations of the 109 core problems, this would also test whether the translation pipeline introduces artifacts.

6. **No characterization of test case quality (Section 3.3).** The paper does not report how many test cases exist per problem, what they cover (e.g., functional vs. edge-case testing), or whether a model could pass all tests while producing incorrect code. The annotation process is described but no quality metrics (e.g., inter-annotator agreement) are reported.

7. **Full-file regeneration design choice not discussed (Section 5).** Models are asked to regenerate the entire file rather than output a diff or targeted edit. In real IDE usage, full-file regeneration is less common than targeted edits or diffs. This design choice may systematically favor models with larger context windows or better ability to reconstruct unchanged regions. It should be justified or acknowledged as a limitation.

### Trivial

None.

## Nice-to-Haves

- A breakdown of which problems are dropped at each stage of the 2672→~1700→~470→109 curation pipeline (with counts and examples) would help readers understand the benchmark's coverage.
- The difficulty split (k=20) is described and reasonable; reporting problem-level pass rates per model as a supplement would enable more fine-grained analysis by the community.

## Removed Points

These points from the input are flagged to be removed; treat them with caution.

- **"Table 3 framing overstates 'crucial' because 2/7 models didn't improve."** The paper says "Highlighted code is crucial to performance, improving task success rate across 5 out 7 models." This is factually accurate — "crucial" is supported by a clear majority benefiting, and the exact proportion is honestly stated. The critic's objection is an overreading.
- **"Difficulty split is a post-hoc heuristic."** The paper transparently explains the methodology (Section 5: k=20 chosen to achieve roughly even split), following prior work (Gauthier, 2025). This is standard practice and not a weakness.
- **"Section-by-section commentary about prompt design, AB tests, annotation team size, and specific model behaviors."** These are observations rather than identified weaknesses; they do not raise concrete flaws.
- **"The Aider Polyglot correlation not being significant at p<0.05."** The paper already presents this honestly (p=0.06) and calls it "weak, positive correlation," which is appropriate.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. **Report confidence intervals** for all main pass@1 results, and clarify whether evaluations use EditBench-core (109) or EditBench-complete (540).
2. **Add a human baseline** — even a rough estimate from 2–3 programmers solving a subset of 20–30 problems would calibrate the difficulty claims.
3. **Expand the limitations section** (currently one paragraph) to address: the ambiguity-curation tension, user population selection bias, the effective problem count, and the full-file regeneration design choice.
4. **Analyze performance across natural languages** to verify that the translation pipeline is not a confound.
5. **Report test case statistics** (count per problem, coverage characteristics) to strengthen the benchmark's validity.

## Score and Decision

MY FINAL SCORE: <score>8</score>
MY FINAL DECISION: <decision>Accept</decision>