Now let me compile the final review with calibration.

**Calibration Summary:**

Round 1 anchors (by score band):
- Strong reject (<1.5): Jailbreaking paper (1.4), robotics paper (1.0) — not comparable
- Reject (1.5–3.5): MCTBench (3.0), Benchmark Planning (2.0), Industrial Benchmark (3.0) — less comprehensive, simpler evaluations
- Borderline (3.5–5.5): Compositional RL (4.5), VL CoT (4.25), ICRL (3.75), Reward Design (5.17)
- Borderline Accept to Accept (5.5–7.5): MathCAMPS (5.75, Reject), Omni-MATH (6.75, Accept), DyVal (6.5, Accept), MathGAP (7.0, Accept), Causal Inference (6.0, Accept)
- Strong Accept (7.5–8.5): miniCTX (8.0), MMQA (8.0), Spider 2.0 (8.0) — higher rigor, cleaner evaluations

**Round 1 bracket:** 5.5–7.5

**Narrowing:** Most comparable papers: DyVal (6.5, DAG-based dynamic evaluation), MathCAMPS (5.75, Reject — narrower scope, no RL), Omni-MATH (6.75, Olympiad benchmark), MathGAP (7.0, proof complexity framework).

**Final calibration:** R-HORIZON is most similar to DyVal (6.5) — both propose controlled-complexity composition frameworks with broad model evaluation. R-HORIZON is stronger in evaluation breadth (26 models × 6 datasets vs DyVal's ~8 models × 7 tasks), adds multi-domain coverage (code & agent beyond math), and includes RL training results that DyVal lacks. However, it has two notable weaknesses that pull the score below DyVal: the missing filtering yield transparency gap (a fundamental reporting standard for benchmark papers), and RL experiments on only one model. These gaps are meaningful but not fatal — they are addressable in revision. Therefore the paper sits at 6.0–6.5. I assign **6.0** given the transparency gap prevents full confidence in the benchmark's coverage claims, balanced upward by the strong evaluation breadth and practically significant RL results.

---

## Summary

This paper proposes R-HORIZON, a method to compose existing single-horizon reasoning benchmarks into multi-step problems with explicit answer dependencies, enabling both evaluation and training of long-horizon reasoning in Large Reasoning Models (LRMs). The pipeline filters problems with integer answers and extractable integer key variables, then constructs dependency chains between them. Evaluation across 26 models on 6 datasets (math, code, agent) reveals severe performance degradation beyond what independent error compounding predicts. RL training on composed data improves both multi-horizon performance and single-problem accuracy (e.g., +7.5 on AIME24).

## Strengths

1. **Comprehensive evaluation across 26 models and 6 diverse task types (math, code, agent).** The consistent degradation — e.g., DeepSeek-R1 dropping from 87.3% to 24.6% on AIME25 (n=1→n=5) — establishes the phenomenon robustly across scales and domains (Figure 3). This breadth exceeds comparable benchmark papers.

2. **Simple, scalable composition method.** Algorithm 1 provides a clear pipeline (seed filtering → key variable identification → dependency chain construction) that reuses existing benchmarks at low cost rather than requiring manual construction of new problems.

3. **Clean expected accuracy diagnostic (Acc_expected = ∏ p_i).** The gap between actual and expected accuracy (Figures 1, 6) provides an interpretable baseline that cleanly visualizes the central finding.

4. **RL training results with practical significance.** Training on composed n=2 data improves AIME24 from 57.9 to 65.4 (+7.5) on the original single-problem task, while also improving multi-horizon performance (+17.4 at n=2). The analysis showing improved thinking budget allocation and reduced response lengths (Figure 9) indicates genuine behavioral change rather than memorization.

## Weaknesses

### Major

1. **Missing filtering yield statistics.** The seed filtering criterion (Eq. 1: |I(q)| > 0 ∧ a ∈ ℤ) requires integer answers and integer key variables in the question text. The paper never reports what fraction of each dataset's problems survive this filter (e.g., for MATH500, AIME24, AMC23). Without this number, the reader cannot assess how representative the composed benchmark is of the original task distribution. This is the most important transparency gap for a paper whose central contribution is a benchmark — it directly affects interpretability of the degradation curves.

2. **RL training experiments conducted on a single base model (R1-Qwen-7B only).** Table 1 and Figures 9–10 report results only for R1-Qwen-7B (line 215: "We train on R1-Qwen-7B"). While a reasonable starting point, the abstract and conclusion's claims about R-HORIZON as a paradigm for "enhancing" long-horizon reasoning rest on experiments from one 7B model. Whether the benefits generalize to larger scales (e.g., 32B) is unverified.

### Minor

3. **Data error in the evaluation table.** "Qwen3-32B" appears twice in the main results table with different values. The first entry (line 157 of extracted text) reports 127.6% accuracy at n=4 on MATH500, which is impossible. This appears to be a mislabeling or data error that must be corrected.

4. **The expected accuracy metric conflates two distinct effects.** Acc_expected(Q) = ∏ p_i assumes errors are independent across problems in the composed sequence. However, composing problems introduces attentional and instruction-following demands beyond the dependency structure itself. The paper mentions "Directly Compose" as a no-dependency ablation (Figure 2, Appendix D) but does not include this comparison in the main evaluation to decompose the gap into format effects vs. dependency effects. The main text's interpretation should be more careful.

### Trivial

5. **Operationalization of "effective reasoning length" is imprecise.** The paper states the "7B model's error range is (4–6k tokens)" and "32B model's error range is (8–10k tokens)" without specifying whether this is the median error position, interquartile range, or other statistic. The definition matters for reproducibility.

## Nice-to-Haves

- Include the "Directly Compose" (no-dependency) ablation in the main evaluation figures to decompose the accuracy gap into format effects vs. dependency effects.
- Add at least one larger model (e.g., R1-Qwen-32B) to the RL training experiments.
- Report dataset construction cost / computational overhead.

## Removed Points

- **"Composition method limited to narrow class of problems"** — The paper explicitly defines the filtering criterion (integer answer + integer key variables). This is a stated design constraint, not a hidden limitation. The method also extends to code and agent tasks (Appendix A). The paper is transparent about what it can handle.
- **"Dependency function is trivially solvable"** — The dependency f_i(x) = x + (m_{i+1} − a_i) is a deliberate design to test numerical answer propagation. The error-type analysis (Figure 5) empirically validates that Problem Reasoning Errors dominate, not Dependency Reasoning Errors — confirming the bottleneck is multi-problem solving, not dependency complexity.
- **"Maximum composed query counts differ across datasets"** — Naturally follows from dataset difficulty and available seed problems. Not a weakness.
- **"Controllable is used without definition"** — Minor semantics point; meaning is clear from context.
- **"Scalable, low-cost claims unsupported"** — The method's nature (reusing existing benchmarks) makes these claims self-evidently reasonable. A cost analysis would be a nice-to-have, not a required weakness.
- **"Missing related works"** — Cannot be verified without external sources.

## Novel Insights

None beyond the paper's own contributions. The key empirical finding — that LRMs degrade on multi-step composed tasks far beyond independent error compounding predicts, and that training on composed data provides dual improvements (multi-horizon + single-problem) — is clearly presented by the paper itself.

## Suggestions

1. Report the filtering yield (fraction of seed problems surviving Eq. 1) for each dataset.
2. Correct the Qwen3-32B table error (duplicate entry with impossible 127.6% value).
3. Include the Directly Compose ablation in the main evaluation to decompose the accuracy gap.
4. Clarify the "effective reasoning length" / "error range" operationalization.
5. Consider adding at least one larger model scale to the RL experiments.

## Score and Decision

Average of human scores of anchor papers: DyVal 6.5, MathCAMPS 5.75, Omni-MATH 6.75, MathGAP 7.0, Causal Inference Benchmark 6.0.

R-HORIZON is most comparable to DyVal (6.5): both propose controlled-complexity composition frameworks for evaluating LLM reasoning. R-HORIZON surpasses DyVal in evaluation breadth (26 models × 6 tasks across math/code/agent vs. ~8 models × 7 tasks) and adds the RL training contribution, but trails in transparency (missing filtering yield) and RL generality (single model). The data error and the independence-assumption confound further prevent a higher score. These are genuine but bounded weaknesses — none invalidate the core contribution, and all are addressable.

**Score: 6.0** — a solid Accept. The paper makes a clear, useful contribution with broad evaluation and practically significant RL training results. The requested additions are focused and feasible.

<score>6.0</score>
<decision>Accept</decision>