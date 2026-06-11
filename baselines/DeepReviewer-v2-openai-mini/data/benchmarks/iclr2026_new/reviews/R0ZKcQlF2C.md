## Summary
# Final Review Report

## Summary

This paper introduces ARENABENCHER, a model-agnostic framework for automatic benchmark evolution that updates test cases in existing LLM benchmarks using multi-model competitive evaluation. Given a benchmark and a pool of models, ARENABENCHER (1) extracts the core ability tested by each case, (2) generates candidate rewrites preserving task intent, (3) verifies correctness with an LLM judge, (4) scores candidates using aggregated loss across a sampled subset of models, and (5) iteratively refines via in-context demonstrations. The framework is evaluated on GSM8K (math), CommonsenseQA (reasoning), and AdvBench (safety) using six models (Llama-3.2, Qwen3, Mistral) up to 7B parameters.

**Core claims:**
- ARENABENCHER increases benchmark difficulty (accuracy drops of 12-48% across models)
- Updated benchmarks maintain high alignment (>90%) and fairness (>85%)
- Multi-model feedback (m=3) outperforms single-model feedback (m=1) in generating harder queries
- Human evaluation on 100 GSM8K samples shows 95% alignment and 96% correctness

The paper addresses an important problem (data contamination in LLM benchmarks) with a well-motivated approach (multi-model signal aggregation). However, several key weaknesses — including an inconsistency between the loss definition in equations vs. algorithm, insufficient statistical reporting (no variance or significance), a fairness metric mismatch with its textual definition, and the absence of direct comparison against prior single-model augmentation methods — limit confidence in the empirical conclusions. Novelty assessment is deferred as external literature retrieval was unavailable in this run.

## Strengths
**1. Timely and important problem framing.** The paper addresses a critical and widely recognized challenge in LLM evaluation: data contamination from pretraining corpora inflates benchmark scores and distorts progress measurement. The motivation for dynamic, evolving benchmarks is well-justified with appropriate citations to contamination measurement work.

**2. Principled multi-model aggregation approach.** Unlike prior benchmark augmentation methods that optimize against a single model, ARENABENCHER's use of multi-model feedback is a conceptually clean and sensible design choice. The idea of selecting test cases that "consistently degrade performance across sampled models" is well-motivated to reduce model-specific bias and identify genuinely challenging failure modes. The iterative refinement with in-context demonstrations is a creative application of LLM prompting techniques to the benchmark evolution problem.

**3. Comprehensive evaluation framework with four desiderata.** The paper defines four evaluation criteria (difficulty, separability, fairness, alignment) that go beyond simple accuracy comparisons. This multi-faceted evaluation protocol is a methodological contribution in itself and provides a template for future benchmark evolution work. Using LLM-as-a-judge for alignment verification is appropriate given the semantic nature of the task.

**4. Cross-domain validation.** The framework is tested on three distinct domains (mathematical reasoning, commonsense reasoning, and safety), demonstrating generalizability beyond a single task type. The inclusion of both base and instruction-tuned models (6 models from 3 families) provides reasonable diversity.

**5. Transparent failure analysis with case study.** Figure 2 presents an honest and informative failure case where ARENABENCHER generates an invalid, misaligned test case. This transparency is valuable for understanding the framework's limitations and informs future improvements.

**6. Human evaluation as validation signal.** The inclusion of human annotation (100 GSM8K samples) provides an important sanity check beyond automated metrics, even though the evaluation scope is limited.

## Weaknesses
### W1 (Critical): Inconsistency in loss function definition between equation and algorithm [Page 1 - Section 3.3 Multi-Model Feedback Scoring]
Equation (1) defines the loss as $\mathcal{L}(x_i^j) = \frac{1}{m} \sum_{M_k \in \mathcal{M}_s} \ell(M_k, x_i^j)$, taking only two arguments (model, input). However, Algorithm 1 (line 9) computes $\mathcal{L}(x_i^j, y_i^j) = \frac{1}{m} \sum_{M_k \in \mathcal{M}_s} \ell(M_k, x_i^j, y_i^j)$ with three arguments (model, input, label). For generative models, loss on input alone is not well-defined without a target output; for classification, the loss requires both input and label. This discrepancy is a reproducibility-critical error: a practitioner attempting to implement ARENABENCHER from the paper would not know whether to use $x$ only or $(x, y)$ as the loss argument. **Fix:** Unify the notation to $\ell(M_k, x_i^j, y_i^j)$ throughout, clarify the exact loss function (e.g., cross-entropy or negative log-likelihood) for each task type, and update Equation (1) to include $y_i^j$.

### W2 (Major): $\sqrt{K}$ sampling heuristic is misattributed and unjustified [Page 1 - Section 3.3]
The paper justifies $m = \lceil \sqrt{K} \rceil$ by citing ensemble heuristics (Chen & Guestrin 2016; Breiman 2001). However, Breiman's random forests use $\sqrt{p}$ where $p$ is the *number of features*, not the number of models. The cited papers do not support the claim that $\sqrt{K}$ models provide "sufficiently heterogeneous feedback to decorrelate signals." The number of models ($K=6$) is so small that $\sqrt{6} \approx 2.45$, rounded to 3, which happens to be half the pool. The heuristic is presented as theoretically grounded but is in fact an ad-hoc choice. **Fix:** Remove the misleading citation, explicitly state this as a design choice, and include a sensitivity analysis varying $m \in \{1,2,3,4,5,6\}$ to validate the selection.

### W3 (Major): Fairness metric does not match textual definition [Page 1 - Introduction Desiderata paragraph vs. Section 3.5]
The textual desiderata (Page 1, line 13) defines fairness as "any performance drop should be comparably distributed, avoiding model-targeted artifacts." This implies *relative* fairness (proportional to original performance). However, the formal metric (Eq. 5) measures fairness as the inverse of the average absolute deviation of *failure counts*, without normalizing by each model's baseline performance. A model with 90% original accuracy dropping to 80% (10 failures) and a model with 10% original accuracy dropping to 0% (10 failures) receive the same fairness score, even though the latter represents a much more severe relative degradation. **Fix:** Either (a) normalize per-model failure counts by the maximum possible failures for that model given its original accuracy, or (b) revise the textual definition to match the absolute metric.

### W4 (Major): Missing variance, confidence intervals, and statistical tests [Page 1 - Section 4.2 Main Results]
Table 1 reports only point estimates of accuracy/ASR without any variance, standard errors, or confidence intervals. Model evaluation is inherently stochastic due to sampling, decoding temperature, and random seeds. A single-run point estimate — such as "47.7% drop in GSM8K accuracy for Llama-3.2-3B" — cannot be assessed for statistical reliability. The paper does not report how many evaluation runs were performed, what random seeds were used, or whether the observed drops are statistically significant. **Fix:** Report all results as mean $\pm$ std over at least 3 evaluation seeds, include paired significance tests (e.g., Wilcoxon signed-rank) comparing original vs. updated benchmark performance for each model, and report effect sizes.

### W5 (Major): Separability metric is scale-dependent and conceptually coupled to difficulty [Page 1 - Section 3.5]
Separability is defined as the mean absolute deviation (MAD) of model accuracies, which is scale-dependent. When difficulty increases (all accuracies shift downward), MAD mechanically compresses even if the benchmark's *relative* discriminative power is unchanged. Table 2 shows separability *decreases* on GSM8K (15.2→12.2→11.3) and CSQA (8.5→9.4→7.2) after updates, yet the paper dismisses this as "expected as model performance begins to compress." This creates a contradiction: the abstract and introduction claim that ARENABENCHER "improves model separability," but the evidence shows separability consistently decreases or stays flat. The conclusion more accurately says "largely maintains separability." **Fix:** (a) Use a scale-invariant separability metric (e.g., coefficient of variation or F-test for variance ratio). (b) Consistently state that the goal is to *maintain* separability while increasing difficulty, not to maximize both.

### W6 (Major): No direct comparison against prior single-model augmentation methods [Page 1 - Section 2 Related Work and Section 4]
The paper's central positioning is that multi-model feedback is superior to single-model optimization. Yet Section 4 compares only ARENABENCHER variants (m=1 vs m=3) without including any external single-model baseline such as MATH-Perturb, ArithmAttack, or a gradient-based adversarial method. The m=1 ablation tests single-model feedback *within ARENABENCHER's pipeline*, but this does not constitute a comparison against prior published methods. The claim that ARENABENCHER "ensures that the augmented items are not only more difficult but also more diagnostic and equitable" (Related Work) is aspirational without such comparison. **Fix:** Add at least one direct comparison: apply a representative single-model augmentation method (e.g., MATH-Perturb for math, or random paraphrasing) to the same benchmarks and evaluate using the same four desiderata metrics.

### W7 (Major): Insufficient hyperparameter and cost reporting [Page 1 - Section 4.1 Hyperparameters]
The hyperparameter paragraph does not report: (a) how many benchmark items were updated (full benchmark or subset), (b) total API calls to GPT-4o and approximate dollar cost, (c) whether model sampling was per-test-case or per-batch, (d) the random seed(s) used. These details are essential for reproducibility and for readers to assess practical feasibility. **Fix:** Report total updated items, API cost estimate, sampling strategy, and seeds. Add a compute cost analysis as a supplemental table.

### W8 (Major): Single-point-of-failure dependence on GPT-4o [Page 1 - Section 4.1 and Figure 2]
The same GPT-4o model handles objective extraction, candidate generation, *and* verification. This circular dependence means that verification failures (as shown in Figure 2) are likely systematic rather than rare — if GPT-4o generates an invalid query, it may also fail to detect the invalidity during verification. The paper does not discuss this limitation or test with alternative judges. **Fix:** (a) Add an ablation using a different judge model (e.g., an open-source model). (b) Explicitly discuss the circular dependence in a Limitations section. (c) Measure the verifier's false positive/negative rate against human judgments.

### W9 (Minor): Human evaluation limited in scope and rigor [Page 1 - Section 4.2 Human Annotation]
The human evaluation covers only 100 GSM8K samples (8% of the benchmark), with no human evaluation for CSQA or AdvBench. Inter-annotator agreement is not reported, annotator expertise is vaguely described, and the annotation rubric is not provided. Additionally, the 95/96% positive results contrast with the clear failure in Figure 2, but this tension is not discussed. **Fix:** Report Fleiss' kappa, provide the annotation rubric, expand human evaluation to at least one more benchmark, and discuss how the Figure 2 failure maps to the 5% error rate.

### W10 (Minor): Conclusion introduces unsupported future directions [Page 1 - Section 5]
The conclusion introduces "multimodal settings," "structure-aware constraints," and "ensembles of calibrated judges" as future work, but none of these concepts are discussed earlier in the paper. A conclusion should consolidate validated findings, not introduce new technical ideas without prior context. **Fix:** Either briefly introduce these directions in the paper body (e.g., in a Limitations paragraph) or remove them from the conclusion and keep it focused on findings and specific next steps.

### W11 (Minor): Abstract-conclusion inconsistency on separability [Page 1 - Abstract vs. Section 5]
The abstract claims ARENABENCHER "improves model separability," but the conclusion more cautiously says "largely maintains separability." Table 2 shows separability decreases on 2 of 3 benchmarks. The abstract overstates the result. **Fix:** Use "largely maintains separability" consistently in both abstract and conclusion.

### W12 (Minor): Grammatical error in critical motivation paragraph [Page 1 - Introduction Paragraph 2]
The sentence "Such single-model optimization introduces model-specific bias that test cases that stump one system can be trivial for others" contains a duplicated "that" creating a garden-path parse error. While this is a minor language issue, it appears in the key paragraph motivating the entire framework, and such errors can reduce reviewer confidence. **Fix:** Restructure to "model-specific bias: test cases that stump one system can be trivial for others."

### W13 (Minor): Overlapping contribution statements [Page 1 - Introduction Contribution Paragraph]
The three listed contributions overlap substantially — the "ability-aware update mechanism" and "iterative refinement strategy" are both sub-components of the "ARENABENCHER framework," making them redundant rather than distinct contributions. **Fix:** Reframe along non-overlapping dimensions: (1) conceptual paradigm (multi-model benchmark evolution), (2) algorithmic design (ability-aware generation + multi-model scoring), (3) empirical findings (cross-domain validation, m=1 vs m=3 comparison, human evaluation).

---

**ASCII Diagram — Paper Structure & Evidence Map**

```text
[Problem: Data contamination in LLM benchmarks]
    -> [Claim: Multi-model feedback reduces model-specific bias]
    -> [Evidence gap: No direct comparison vs prior single-model methods (W6)]
    -> [Risk: Central motivation claimed but not empirically validated]
    
[Method: ARENABENCHER pipeline]
    -> [Claim: Loss-based candidate selection improves difficulty]
    -> [Evidence: Table 1 accuracy drops]
    -> [Evidence gap: No variance/statistics reported (W4)]
    -> [Risk: Results may not be statistically reliable]
    
[Method: Multi-model scoring]
    -> [Claim: sqrt(K) rule balances diversity and cost]
    -> [Evidence: Misattributed to Breiman/RF (W2)]
    -> [Risk: Design choice lacks proper justification]
    
[Evaluation: Four desiderata]
    -> [Claim: Fairness ensures equitable distribution]
    -> [Evidence gap: Metric-text mismatch (W3)]
    -> [Risk: Fairness may not measure what is claimed]
    
[Conclusion: Contamination-resilient evaluation]
    -> [Claim: Improves separability]
    -> [Contradiction: Table 2 shows separability decreases (W5, W11)]
    -> [Risk: Overclaim in abstract vs. hedging in conclusion]
```

**ASCII Diagram — Revision Strategy Roadmap**

```text
Priority 0 (Must fix before acceptance):
├── W1: Fix loss function inconsistency (Eq.1 vs Algorithm 1)
├── W4: Add variance reporting and significance tests
├── W5: Fix separability metric normalization + align claims
└── W6: Add direct comparison against prior single-model methods

Priority 1 (Should fix):
├── W2: Correct sqrt(K) justification or acknowledge as ad-hoc
├── W3: Align fairness definition and metric
├── W7: Report compute cost, seeds, and sampling protocol
└── W8: Add alternative judge ablation; discuss circular dependence

Priority 2 (Nice to fix):
├── W9: Expand human evaluation with agreement stats
├── W10: Restructure conclusion around validated findings
├── W11: Harmonize abstract/conclusion on separability
├── W12: Fix grammatical error
└── W13: Reframe contribution statements
```

**ASCII Diagram — Related-Work Taxonomy Tree (Layered)**

```text
Related Work: Benchmark Evolution for LLMs (Root)
├── Branch 1: Static Benchmark Design
│   ├── Leaf 1.1: Domain-specific (GSM8K, Winogrande, CSQA)
│   ├── Leaf 1.2: Comprehensive (MMLU, BIG-bench, HELM)
│   └── Leaf 1.3: Efficiency (BIG-bench Lite, benchmark compression)
│       → Difference vs. This Paper: Static; no contamination resistance
│
├── Branch 2: Benchmark Augmentation via Perturbation
│   ├── Leaf 2.1: Math-domain perturbations (MATH-Perturb, ArithmAttack, GSM-symbolic)
│   ├── Leaf 2.2: General-domain perturbations (AutoRobust Stress Testing, slot-filling noise)
│   └── Leaf 2.3: Adversarial perturbations (gradient-based single-model)
│       → Difference vs. This Paper: Single-model optimization; domain-limited
│       → Novelty Risk: ARENABENCHER's multi-model feedback is distinct but untested against these methods (W6)
│
├── Branch 3: LLM-based Prompt Optimization
│   ├── Leaf 3.1: Performance optimization (APE, RLPrompt, OPRO)
│   └── Leaf 3.2: Jailbreak/red-teaming (PAIR, GCG)
│       → Difference vs. This Paper: Objective is accuracy maximization or safety violation, not benchmark evolution
│
└── Branch 4: Dynamic Benchmarking
    ├── Leaf 4.1: Manual refresh (Chen 2025, Jain 2024)
    ├── Leaf 4.2: Automatic update (Li 2025, White 2024)
    └── [This Paper] ARENABENCHER: Multi-model automatic evolution
        → Novelty Signal: First framework to use explicit multi-model aggregation for benchmark evolution
        → Value: Cross-domain applicability (math, commonsense, safety)
        → Risk: Single-LLM dependence (W8); limited scale validation (W7)
```

## Score
**Final Score: 5/10**

**Scoring rationale:** This score is grounded in the following assessment across four dimensions:

*Research value (weight: high):* The paper tackles a timely and important problem (data contamination in LLM benchmarks) with a conceptually clean idea (multi-model feedback for benchmark evolution). However, the empirical validation is limited in scope (small model pool up to 7B, no frontier models, subset of benchmarks), and the key positioning claim (superiority over single-model augmentation) is not directly tested against prior work (W6). The practical value may be constrained by the dependence on GPT-4o for all pipeline stages (W8), which creates both a cost barrier and a circular verification problem.

*Novelty (weight: high):* The idea of using multi-model competitive evaluation for benchmark evolution appears novel. However, without external literature search (retrieval was unavailable in this run), this judgment is provisional and requires manual verification. The method shares high-level similarities with prior benchmark augmentation pipelines (LLM-based rewriting + verification) and prompt optimization methods (PAIR, APE). The specific contribution — multi-model loss aggregation — is incremental but reasonable. Novelty verdicts for all three claims (C1-C3) are deferred pending manual literature verification.

*Validity/soundness (weight: high):* This is the weakest dimension. The paper contains a critical inconsistency between the equation and algorithm for the loss function (W1), which threatens reproducibility. The sqrt(K) heuristic is misattributed (W2). The fairness metric does not match its textual definition (W3). All experimental results lack variance/confidence intervals (W4). The separability metric is scale-dependent and its decrease contradicts the abstract's "improves" claim (W5, W11). These issues collectively reduce confidence in the paper's empirical conclusions.

*Presentation/clarity (weight: moderate):* The paper is generally well-written and clearly structured. The four-desiderata framework is a strong organizational device. However, there are grammatical issues in a key motivation paragraph (W12), overlapping contribution statements (W13), insufficient hyperparameter reporting (W7), and a conclusion that introduces unsupported future directions (W10).

**Summary:** The paper has a solid conceptual contribution and addresses an important problem, but the empirical validation has significant gaps that prevent stronger conclusions. The critical inconsistency in the loss function (W1) and absence of variance reporting (W4) are the most urgent issues to address. With substantial revisions — particularly fixing the loss definition, adding proper statistical reporting, comparing against prior methods, and aligning the metrics with their definitions — the paper could become a meaningful contribution.

**External literature verification status:** External paper search was unavailable in this run (Retrieval-Disabled Mode). All novelty/comparison conclusions in this review are grounded in the manuscript content only and should be manually verified against the full literature before final acceptance decisions.