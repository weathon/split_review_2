## Summary
This paper introduces R-HORIZON, a method for constructing multi-step reasoning tasks by composing existing single-problem benchmarks with answer-level dependencies. The approach creates sequential problem chains where solving problem (i) requires the answer from problem (i-1), forcing models to reason across multiple interdependent steps. Based on this method, the authors construct a benchmark spanning 6 datasets (MATH500, AIME24/25, AMC23, LiveCodeBench, WebShaper) across mathematics, code generation, and agent tasks, and evaluate 26 LRMs including DeepSeek-R1, Qwen3-235B-Thinking, and o4-mini. 

The key empirical findings are: (1) all tested LRMs show significant and consistent performance degradation as the number of composed queries increases, with actual accuracy falling substantially below an expected accuracy baseline; (2) models exhibit limited effective reasoning length (4-6k tokens for 7B, 8-10k for 32B models), localized reflection patterns, and imbalanced thinking budget allocation favoring early sub-problems; (3) reinforcement learning with composed training data (particularly n=2 composition) improves both multi-horizon and single-problem accuracy compared to training on isolated problems alone.

The paper is timely and addresses a genuine gap — the lack of systematic evaluation of LRMs on multi-step interdependent reasoning tasks. The main strengths are the extensive evaluation (26 models, 6 datasets) and the RL training results showing practical benefits of composed training data. However, the work has several weaknesses: the expected accuracy metric (Eq. 4) assumes independent sub-problem errors, directly contradicting the dependency structure R-HORIZON introduces; the benchmark construction has restrictive filtering (integer-only answers) and uncertain reliability (127.6% accuracy value suggests data corruption); several core analytical claims about "effective reasoning length" and "reflection scope" are descriptively interesting but lack the causal evidence or statistical rigor needed to fully support them; and the conclusion is underdeveloped with no limitations discussion. External literature verification was unavailable in this run, so novelty comparisons are deferred.

## Strengths
1. **Timely and well-motivated problem.** The paper correctly identifies a genuine gap in current LRM evaluation: existing benchmarks focus on isolated, single-horizon tasks while real-world deployment requires multi-step, interdependent reasoning. The core question — how LRMs perform when they must reason across sequentially dependent problems — is both scientifically interesting and practically important.

2. **Extensive evaluation scope.** The benchmark spans 6 datasets across 3 task categories (math, code, agent) and evaluates 26 LRMs, including both open-weight models (DeepSeek-R1, Qwen3, QwQ-32B) and commercial APIs (o4-mini, Gemini-2.5-Pro, Claude-Sonnet-4). This breadth provides a comprehensive picture of the degradation phenomenon across model families and scales.

3. **Practical RL training improvement.** The demonstration that RL with composed training data improves both multi-horizon and single-problem performance (Table 1; +9.6 on AIME24) is a valuable practical result. The finding that n=2 composition provides the best trade-off between difficulty and generalization is actionable for practitioners.

4. **Insightful error-type taxonomy.** The decomposition of errors into Problem Reasoning Error, Dependency Reasoning Error, Early Stop, and Output Truncation (Figure 5) provides a useful diagnostic framework that goes beyond reporting aggregate accuracy drops.

5. **Open-source release.** The inclusion of a GitHub repository and the composition pipeline code supports reproducibility and enables the community to extend R-HORIZON to new datasets.

## Weaknesses
### W1. Expected Accuracy Metric (Eq. 4) Contains a Fundamental Independence Assumption that Contradicts the Dependency Structure (Major)

Equation (4) defines $\text{Acc}_{\text{expected}}(\mathcal{Q}) = \prod_{i=1}^n p_i$, where $p_i$ is the single-problem pass rate. This formula assumes that errors across sub-problems are **independent**. R-HORIZON's core design, however, explicitly creates **dependencies**: Algorithm 1 chains sub-problems so that the answer to problem $i$ is needed to solve problem $i+1$. An error in sub-problem $i$ propagates deterministically to sub-problem $i+1$. Under dependency, the expected accuracy should be $\leq \prod_{i=1}^n p_i$, with the gap widening as dependency strength increases. This means the "expected accuracy" baseline used in Figures 1 and 6 is an **upper bound** for dependent composition, not a neutral baseline. The observed gap between actual and expected accuracy may be partially or entirely driven by this measurement artifact rather than "limited effective reasoning length." The paper's central diagnostic claim — that LRMs degrade more than they "should" — rests on a flawed baseline. **Required fix:** The authors must either (a) use a dependency-aware expected accuracy formula that accounts for conditional error propagation, or (b) explicitly acknowledge that Eq. (4) is an upper bound and report a tighter lower bound.

### W2. Data Integrity Issue in Evaluation Table (Major)

The evaluation table (Figure 3) reports Qwen3-32B achieving **127.6% accuracy** on MATH500 with n=4 composed queries. Accuracy values cannot mathematically exceed 100%. This is almost certainly a data entry error, parsing failure, or corruption. The presence of one such uncorrected value undermines confidence in the entire reported table and suggests insufficient quality control. **Required fix:** Audit all entries in the table, correct or remove the corrupted value, and report confidence intervals or error bars to validate data integrity. Additionally, several non-monotonic results need explanation (e.g., DeepSeek-R1 on AMC23 jumping from 50.9% at n=3 to 89.7% at n=4; o4-mini showing WebShaper accuracy *increasing* from 43.7% at n=1 to 87.6% at n=2, contradicting the paper's central claim of monotonic degradation).

### W3. Benchmark Construction Has Restrictive Filtering and Underspecified Components (Major)

The seed problem filtering (Eq. 1-2) imposes two constraints without adequate justification:
- **Integer-only answers** ($a \in \mathbb{Z}$): This excludes rational answers, expressions, and proof-based problems. The paper does not report what fraction of each original dataset survives this filter, making it impossible to assess selection bias. If 80% of MATH500 is excluded, the benchmark no longer represents mathematical reasoning.
- **Key-variable verification by model M** (Eq. 2): The paper uses an unspecified model M to verify which integers are key variables, but does not identify M, report its accuracy, or discuss calibration. If M is a weaker model, misclassifications propagate; if M is the same model being evaluated, this creates circular reasoning.

**Required fix:** (a) Report the retention rate per dataset after filtering. (b) Specify model M and report its verification accuracy on a held-out sample. (c) Add ablation without key-variable filtering to assess its impact.

### W4. Training Data Filtering Threshold is Arbitrary and Potentially Biasing (Major)

The RL training setup filters composed problems to keep only those with $\text{Acc}_{\text{expected}} > 0.25$. This threshold is not justified, no sensitivity analysis is provided, and it may systematically exclude longer or harder compositions. For n=4 with typical per-problem pass rates of 0.7, $\text{Acc}_{\text{expected}} = 0.7^4 \approx 0.24$, which falls below the 0.25 threshold and would be filtered out. This could explain why n=4 training shows weaker transfer to single-problem tasks (Table 1). **Required fix:** Report results without filtering as a control, or provide an ablation across thresholds (0.1, 0.25, 0.5).

### W5. Conclusion is Underdeveloped with No Limitations Discussion (Major)

The Conclusion section consists of only two sentences that essentially restate the abstract. It lacks: (a) a concise summary of validated findings with evidence anchors, (b) explicit limitations (e.g., integer-only constraint, simple additive dependency function, independence assumption in expected accuracy), (c) failure mode analysis (when does R-HORIZON not work?), (d) actionable next steps for the field. The claim that R-HORIZON "establishes a foundation for future advances" is unsupported forward-looking language that belongs in a discussion section, not a conclusion that should consolidate what was actually shown. **Required fix:** Expand the conclusion substantially following the structure: validated findings, bounded limitations, and prioritized future work.

### W6. Causal Claims about Limited Reasoning Length and Reflection Scope are Overstated (Major)

The Introduction and Section 5 present three diagnosed limitations — limited effective reasoning length, constrained reflection scope, and overthinking hindering budget allocation — as established causal mechanisms. However:
- The "effective reasoning length" is a post-hoc interpolation from accuracy vs. query-number curves, not a directly measured cognitive boundary. Error propagation from dependent composition (W1) could produce the same curve shape.
- The reflection analysis uses keyword-based detection ("wait", "but") without validation of precision/recall, and question-boundary detection is not specified.
- The thinking budget allocation analysis (Figure 8) shows correlation between early-problem token dominance and lower overall accuracy, but does not establish that rebalancing budget would improve accuracy.

**Required fix:** (a) Soften causal language to "consistent with" formulations. (b) Validate reflection detection against human annotation. (c) Run an intervention experiment where budget allocation is explicitly controlled (e.g., by prompt instruction) to test causality.

### W7. Missing Variance, Confidence Intervals, and Significance Tests (Moderate)

Throughout the evaluation and RL training results, accuracy numbers are reported as point estimates without variance, confidence intervals, or significance tests. Given the non-monotonic results (W2), the small margins between some conditions (e.g., Table 1: 65.4% vs 62.9% for n=2 vs n=4 on AIME24), and the zero-shot nature of the evaluation, variance could be substantial. Without statistical rigor, many comparative claims are unverifiable. **Required fix:** Report mean and standard deviation over at least 3 evaluation seeds, and add significance tests for key comparisons (e.g., composed vs. single-problem training).

### W8. GRPO Objective is Standard with No R-HORIZON-Specific Adaptation (Minor)

Equation (5) reproduces the standard GRPO objective. The paper positions Section 3.3 as "reinforcement learning with R-HORIZON," but the only R-HORIZON-specific elements are in data construction and reward design (Eq. 6). The RL algorithm itself is unchanged from prior work. This creates a mismatch between the claimed contribution (a new RL paradigm for long-horizon reasoning) and the actual contribution (a new data composition method with standard RL). **Required fix:** Explicitly acknowledge that GRPO is used without modification, and discuss whether the token-level policy gradient is optimal for multi-step reward signals.

### W9. Abstract Overclaim (Moderate)

The abstract states that R-HORIZON offers a "scalable, controllable, and low-cost paradigm." No scalability analysis, controllability demonstration, or cost comparison is provided in the paper. The term "paradigm" is disproportionate for a data composition method. Additionally, the claimed gain of "+7.5 on AIME2024" has a numerical inconsistency — Table 1 shows the baseline R1-Qwen-7B at 48.3% and the n=2 composed training at 65.4%, a gain of +17.1 points, not +7.5. The relationship between the abstract's "+7.5 on AIME2024" and Table 1's results needs clarification. **Required fix:** Tighten abstract wording to match actual evidence, resolve the numerical inconsistency, and avoid promotional framing.

### W10. External Literature Verification Deferred (Runtime Constraint)

Due to the unavailability of the paper search API in this run, novelty and related-work comparison conclusions are deferred for manual verification. The paper's claims about being distinct from NEST and GSM-Infinite appear reasonable from description, but a thorough novelty audit requires systematic retrieval that was not possible here. **Required fix:** The authors are advised to include a more detailed comparison table with NEST and GSM-Infinite across dimensions (dependency type, input/output length regime, evaluation metric, training use).

## Score
**Final Score: 5.5/10**

**Rationale:** This score prioritizes research value, novelty, and validity, consistent with the prescribed scoring policy. The paper addresses a genuine and timely problem — evaluating LRMs on multi-step interdependent reasoning — and provides an extensive empirical evaluation across 26 models and 6 datasets. The RL training results showing that composed data improves both multi-horizon and single-problem performance are practically valuable.

However, the score is constrained by several validity-critical weaknesses. The expected accuracy metric (Eq. 4) contains a fundamental independence assumption that directly contradicts the dependency structure of R-HORIZON, undermining the paper's central diagnostic claim about "limited effective reasoning length." Data integrity issues (the 127.6% value) and non-monotonic results in the evaluation table reduce confidence in the reported numbers. Several core analytical findings about effective reasoning length and reflection patterns are descriptively interesting but lack the statistical rigor and causal evidence needed to fully support the strong causal claims made in the Introduction. The conclusion is underdeveloped with no limitations discussion. External literature verification was unavailable, so novelty comparisons are deferred.

The strengths (extensive evaluation, practical RL improvement, insightful error taxonomy) and weaknesses (flawed baseline metric, data integrity issues, overclaimed causality, underdeveloped conclusion) balance to a moderate score. With revision addressing the major issues (fixing the expected accuracy metric, auditing data integrity, softening causal claims, expanding the conclusion), the paper could be substantially strengthened.