Here is the final consolidated review.

---

## Summary

This paper proposes R-HORIZON, a method that composes existing single-problem benchmarks (math, code, agent tasks) into sequences of problems with simple arithmetic dependencies between consecutive steps. The authors build a benchmark from this and evaluate 25+ large reasoning models (LRMs) across 6 datasets. The core empirical finding is that even the strongest LRMs suffer severe accuracy degradation as the sequence length grows — e.g., DeepSeek-R1 on AIME25 drops from 87.3% at n=1 to 24.6% at n=5. The paper further shows that standard RL training on single problems barely improves multi-problem performance, while RL training on composed data yields substantial gains (+17.4 on AIME24 n=2) and also transfers positively to single-problem accuracy (+7.5 on AIME24). The work is relevant for anyone deploying LRMs in agentic or multi-step settings.

---

## Strengths

1. **Genuine, non-obvious empirical finding.** The systematic result that LRMs fail to solve N-problem sequences far worse than independent-error probabilities would predict, and that this gap grows with N, is a real discovery about LRM behavior under sustained multi-problem conditions. This is demonstrated consistently across 25+ models and 6 diverse datasets (math, code, web agent).

2. **Clean and actionable RL result.** The contrast between single-problem RL training (AIME24 n=2: 16.4% → 16.7%) and composed-problem RL training (16.4% → 34.1%) is sharp. The transfer benefit to single-problem AIME24 (+7.5 over single-problem training) further strengthens the practical case for composed training data.

3. **Comprehensive evaluation coverage.** Testing 25 models across MATH500, AIME24/25, AMC23, LiveCodeBench, and WebShaper provides a thorough picture spanning scales (1.5B to 235B), families (R1-distill, Qwen, Nemotron, o4-Mini, Gemini), and task types.

4. **Informative error-type taxonomy (Figure 5) and effective reasoning length analysis (Figure 6).** Distinguishing Problem Reasoning Errors, Dependency Reasoning Errors, Early Stop, and Output Truncation provides a useful diagnostic decomposition. The finding that error positions stabilize at model-dependent token budgets (4–6k for 7B, 8–10k for 32B) is a concrete result about LRM behavior.

---

## Weaknesses

### Fatal
None.

### Major

1. **The "complex multi-horizon reasoning" framing is substantially overstated.** The cross-problem dependency is a trivial linear transformation: `f_i(x) = x + (m_{i+1} - a_i)`, which collapses to `f_i(a_i) = m_{i+1}` (Algorithm 1, lines 82–88). The model need only extract a known integer from the next problem and copy it through. Yet the paper repeatedly invokes "long-horizon reasoning," "complex multi-step reasoning tasks," and "interdependent problems" (abstract, introduction). What is actually being tested is sustained attention across a sequence of near-independent problems with trivial arithmetic bookkeeping between them. This does not invalidate the benchmark — the finding that models cannot reliably sequence-solve N problems is still interesting — but the framing is significantly misaligned with what is measured. The paper would be stronger if it acknowledged this gap and described the task as a sustained multi-problem attention stress test rather than a test of complex multi-step reasoning.

2. **The expected accuracy metric (Equation 4) conflates genuine degradation with measurement artifact.** The expected accuracy is `∏ p_i` where `p_i` is the pass rate on the *unmodified* atomic problem `q_i`. This assumes: (a) errors across sub-problems are independent — false, because an error on problem i changes the input to problem i+1 (via the dependency), making it a different problem; and (b) the modified problem `q'_i` (with a placeholder variable and dependency constraint) has the same difficulty as `q_i` — also unlikely, because inserting a placeholder and constraint changes the problem. Both assumptions inflate the gap between actual and expected accuracy, which the paper attributes entirely to "limited effective reasoning length" without decomposing how much is artifact. The authors should either estimate pass rates on the modified problems, or explicitly quantify the artifact's contribution.

3. **The "rollout efficiency" analysis is uninterpretable because "Effective" is never defined and the numbers are internally inconsistent.** The table in Figure 10 reports for n=1 at step 100: Effective=80%, Solve None=30%, Solve All=20%. If "Effective" means "solved at least one problem" (complement of Solve None), it should be 70% (100−30), not 80%. If it means "solved some but not all," that gives 60% (80−20). Neither works, and the inconsistency persists at later steps (n=1 step 600: Effective=65, Solve None=3, Solve All=35 leaves no way to reconcile). The metric is central to the claim that composed data yields "20% more effective samples," but the reader cannot verify the numbers. This section needs a clear definition and internally consistent figures.

### Minor

1. **RL training experiments are limited to a single small model (R1-Qwen-7B).** All RL results (Figures 4, 9, 10; Table 1) use only this 7B model. Claims that composed training "promotes efficient reasoning," "alleviates overthinking," and "improves rollout efficiency" would be substantially strengthened by demonstrating the same benefits on at least one larger model (e.g., 32B). Without that, it is unclear whether the benefits generalize.

2. **Two data anomalies undermine confidence in the reported numbers.** (a) o4-Mini on WebShaper: 43.7% (n=1) → 87.6% (n=2), a 44-point *increase* that reverses the paper's central degradation claim. This is never acknowledged or explained. (b) The main table (line 157) shows Qwen3-32B with 127.6% on MATH500 n=4 — a physical impossibility for accuracy. Both issues suggest insufficient quality control and need to be corrected or explained.

3. **The claim that composed training "alleviates overthinking" conflates response length with answer quality.** The paper reports shorter responses after composed training (Figure 9b) and interprets this as eliminating wasteful verbosity. However, shorter responses could also mean the model learned to give less thorough (but still correct on the training distribution) answers. Without analyzing per-problem answer quality, shorter responses are not unambiguously better.

4. **No comparison to an independent-concatenation baseline.** The paper does not quantify how much harder the dependent version is versus simply concatenating N problems with no dependency (the NEST approach, cited in related work). This would isolate the effect of the dependency structure from the effect of multi-problem sequential solving — and would likely show that most of the degradation is due to the latter.

### Trivial
- The seed problem filtering (Equation 1) restricts to problems with integer answers and at least one integer in the question, which limits coverage and may bias the dataset. The potential bias is not discussed.

---

## Nice-to-Haves
- Extend RL experiments to at least one 32B model.
- Compare against an independent-concatenation baseline (cf. NEST).
- Add confidence intervals or variance estimates for key benchmark numbers, given all-or-nothing scoring and small n for some configurations.
- Compare experimentally with GSM-Infinite, the most closely related method for constructing dependent problem graphs.
- Test harder dependency functions (multi-step arithmetic, conditional logic) to see if degradation worsens.

---

## Removed Points

These points were in the input review but were filtered out:
- **"Reflection analysis uses keyword matching"** — The paper describes this transparently ("such as 'wait,' 'but...'"), and keyword matching for reflection detection is a standard approximation. Not a meaningful weakness.
- **"Missing appendix content / proofs deferred to appendix"** — The parser strips appendices from all papers. These exist in the original submission. Removed per policy.
- **"Reproducibility concerns about unreleased models/tools"** — All cited models, datasets, and tools are assumed to exist per policy. Removed.
- **"Formatting nitpicks and typos"** — Parser artifacts, not author errors. Removed.
- **"All-or-nothing scoring inflates failure appearance"** — The paper addresses this via the expected accuracy comparison, which accounts for the mathematical consequence of requiring multiple successes. This is a reasonable mitigation.
- **"Missing related works"** — Not verifiable per policy.
- **Section-by-section presentation notes** (figures, column headers, etc.) — These are minor presentation issues that do not affect the paper's contribution.

---

## Novel Insights

None beyond the paper's own contributions. The reviews surface no genuinely novel observation about the method or results that the paper itself does not already articulate.

---

## Suggestions

1. **Adjust the framing** to accurately describe what is being tested: sustained attention across a sequence of near-independent problems with trivial coupling, rather than "complex multi-horizon reasoning."
2. **Fix the expected accuracy metric** by either (a) estimating pass rates on the modified (placeholder-bearing) problems, or (b) explicitly quantifying the artifact's contribution to the gap.
3. **Define "Effective" samples** in the rollout efficiency analysis and ensure all reported numbers are internally consistent.
4. **Explain or correct the o4-Mini WebShaper anomaly** (43.7% → 87.6%) and fix the 127.6% table entry.
5. **Extend RL experiments** to at least one 32B model.
6. **Add an independent-concatenation baseline** to isolate the effect of sequential problem solving from the effect of the dependency structure.

---

## Score and Decision

**Calibration anchors retrieved (all rounds):**

| Paper | Avg Score | Round | Comparison |
|---|---|---|---|
| NEMESIS jailbreaking | 1.40 | R1 | Pseudo-paper, no comparison possible |
| Survey paper | 1.00 | R1 | Not a real research paper |
| ProcBench (multi-step reasoning) | 3.75 | R1 | Simple synthetic benchmark with fewer models; R-HORIZON is substantially stronger (25 models, real tasks, RL results) |
| FACTOR (long-context eval) | 5.00 | R1 | Similar benchmarking goal but less comprehensive; R-HORIZON has more models and RL training |
| Abstract Reasoners benchmark | 5.33 | R1 | Benchmark-only, no training intervention |
| Towards Learning to Reason | 5.50 | R2 | Focused on pre-training scale reasoning, less applied |
| Step-Controlled DPO | 6.00 | R2 | Similar score range, math reasoning with DPO |
| CompWoB (compositional agent tasks) | 6.50 | R2 | Very similar contribution (degradation on compositional tasks + training fix); R-HORIZON has broader task scope |
| ActionReasoningBench | 6.75 | R2 | Similar (benchmark showing degradation with sequence length); R-HORIZON has comparable quality but more metric issues |
| KOR-Bench | 7.00 | R1 | Cleaner concept and execution; R-HORIZON has more applied contribution (RL result) but more methodological issues |
| MathGAP | 7.00 | R1 | Cleaner framework for proof complexity; R-HORIZON has broader scope but less controlled design |

**Round 1 bracket:** 5.5–7.0 (above ProcBench/FACTOR, below KOR-Bench/MathGAP)

**Round 2 narrowing:** The paper is closest to CompWoB (6.5) and ActionReasoningBench (6.75) in contribution type — all show degradation on compositional/multi-step tasks and test training interventions. However, R-HORIZON has three major weaknesses (overclaimed framing, flawed expected accuracy metric, undefined rollout efficiency metric) that CompWoB and ActionReasoningBench do not have to the same degree. This places it below those papers.

**Final calibrated score: 6.0.** The paper reports a genuine, non-obvious empirical finding about LRM degradation on multi-problem sequences, with a clean RL training result that has practical utility. However, the framing substantially overstates what is being tested, the headline expected accuracy metric conflates degradation with artifact, and the rollout efficiency analysis is uninterpretable. The core contribution is solid and worth publishing, but these issues need to be addressed in revision.

MY FINAL SCORE: <score>6.0</score>
MY FINAL DECISION: <decision>Accept</decision>