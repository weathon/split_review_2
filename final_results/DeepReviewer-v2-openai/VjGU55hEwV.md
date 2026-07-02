## Summary
# Final Review Report

## Summary

This paper proposes **RLIE**, a framework that integrates Large Language Models (LLMs) with probabilistic modeling for rule learning. The framework operates in four stages: (1) an LLM generates candidate rules in natural language from a small sample of training data, with coverage-based filtering; (2) a regularized logistic regression model (with Elastic Net) learns probabilistic weights for the rules; (3) hard examples identified by prediction errors drive an iterative refinement loop where the LLM revises or generates new rules; and (4) four inference strategies are compared — direct Linear-only prediction, LLM+Rules, LLM+Rules+Weights, and LLM+Rules+Weights+Linear Prediction.

The core contribution is a neuro-symbolic architecture where LLMs handle **local semantic tasks** (rule generation, individual rule evaluation via ternary judgments) while a classical probabilistic model handles **global aggregation** (weighting and selection). Experiments on six binary text-classification datasets from HypoBench (200/200/300 train/val/test splits) show that the Linear-only inference strategy (using the logistic regression combiner directly) outperforms all LLM-based inference strategies on nearly all datasets, often by 5–10 F1 points. The paper argues that this reveals a fundamental limitation of current LLMs in integrating explicit probabilistic signals.

**Strengths:** The research question is well-motivated — combining LLM expressiveness with probabilistic calibration is a timely topic. The RLIE framework is clearly structured with four well-defined stages. The evaluation design, particularly the hierarchical comparison of four inference strategies (E1–E4), is informative and yields a counterintuitive finding about LLM limitations that is of practical interest. The use of Elastic Net regularization for automatic rule selection is methodologically sound.

**Weaknesses:** (1) The small dataset sizes (200/200/300) and missing standard deviations in Table 1 undermine the statistical reliability of the reported comparisons. (2) The "first to explicitly combine LLMs with probabilistic methods" novelty claim cannot be verified without literature search (deferred). (3) The iterative refinement prompt and LLM revision logic are underspecified, compromising reproducibility. (4) The explanation for the counterintuitive LLM degradation is speculative — no reasoning trace analysis is provided. (5) Several key hyperparameters (γ=0.2, H=10, k=20) are used without sensitivity analysis. (6) The Conclusion overclaims about "knowledge discovery" and generalizability without supporting evidence.

## Strengths
**1. Well-motivated and timely research question.** The problem of combining LLM-driven rule generation with principled probabilistic aggregation is relevant to the growing interest in neuro-symbolic AI and interpretable machine learning. The paper correctly identifies that existing LLM-based rule learning methods either optimize a single hypothesis or independently aggregate multiple rules, lacking a mechanism for joint weighting and selection.

**2. Cleanly designed framework with logical four-stage pipeline.** The RLIE framework (Rule Generation → Logistic Regression → Iterative Refinement → Evaluation) is presented in a clear, modular structure. Using an LLM for ternary rule judgments (−1/0/+1, allowing abstention) is a practical design choice that explicitly models rule coverage and avoids forcing binary decisions when rules are inapplicable.

**3. Informative hierarchical evaluation strategy.** The contrast between four inference strategies (E1 Linear-only, E2 LLM+Rules, E3 LLM+Rules+Weights, E4 +Linear Prediction) is the strongest experimental contribution. The finding that injecting more information into the LLM consistently degrades performance (Table 2) is counterintuitive and practically valuable, as it challenges the assumption that LLMs can straightforwardly integrate probabilistic signals.

**4. Methodological soundness of the probabilistic combiner.** Using Elastic Net regularization (L1 + L2) for weight learning is appropriate for this setting: L1 sparsity automatically selects a subset of rules, reducing overfitting and improving interpretability, while L2 provides robustness when rules are correlated. The use of stratified K-fold cross-validation on a separate validation set for hyperparameter selection follows best practices.

**5. Multi-backbone validation.** Reporting results with three different backbone LLMs (Qwen3-Next-80B, Qwen3-235B, DeepSeek-V3) demonstrates some degree of model-agnostic effectiveness and provides insight into how backbone capacity affects rule quality.

**6. Transparent discussion of limitations.** The paper acknowledges that LLMs are "less reliable at fine-grained, controlled probabilistic integration" and discusses the division of labor principle. The Ethics Statement and Reproducibility Statement are thorough and address relevant concerns about bias and code release.

## Weaknesses
### W1. Unverifiable variance and missing standard deviations (Major)
**Location:** Page 6–7 — Section 4.3 and Section 5.1 (Table 1)

The paper states that "each experiment was repeated at least three times, and we report the mean and standard deviation" but Table 1 does **not display any standard deviations**. The table cells contain only Accuracy/Macro-F1 pairs without error bars. The narrative claims "low variance" and "robustness" but provides no visible evidence. This is a direct inconsistency between the text and the presented data.

**Impact:** Without variance information, readers cannot assess whether the reported performance differences (often 1–5 F1 points) are statistically meaningful. Given the small test set size (N=300), the 95% confidence interval for accuracy is approximately ±5.7 percentage points, which encompasses many of the observed differences.

**Required fix (Must):** Restructure Table 1 to include standard deviations (e.g., "71.5±2.1 / 71.4±2.3") and add a subsection discussing statistical significance. Provide per-seed results in the appendix.

### W2. Small datasets and limited generalizability (Major)
**Location:** Page 6 — Section 4.3 (lines 301–304)

Each dataset uses only 200 training, 200 validation, and 300 test samples. With 200 validation samples, cross-validation hyperparameter selection is noisy. With 300 test samples, the reliability of accuracy/F1 estimates is limited. The paper does not discuss these limitations or their impact on the strength of the conclusions.

**Impact:** The claim that RLIE "achieves superior overall performance" is conditional on these small-scale experiments. The method may not scale to larger, more diverse datasets where the logistic regression combiner's linearity assumption could break down.

**Required fix (Must):** (1) Explicitly state the statistical power limitation in Section 5.1. (2) Report 95% confidence intervals for main results. (3) Add experiments on at least one larger dataset (e.g., 1000+ samples) if possible, or clearly bound the claims to the tested small-data regime.

### W3. Unverifiable novelty claim — "first to explicitly combine" (Major)
**Location:** Page 2 — Section 2.2 (line 28), also in contributions

The paper states it is "the first to explicitly combine LLMs with probabilistic methods to learn a set of weighted rules." This strong novelty claim cannot be verified without a systematic literature search, which is unavailable in this review (Retrieval-Disabled Mode). There are several related paradigms (ProbLog, Markov Logic Networks, DL2, neuro-symbolic programming, recent LLM+rule papers like HypoGeniC, IO Refinement, RuAG) that may touch on similar combinations. The paper itself cites Zhou et al. (2024) and Qiu et al. (2023) as related but does not explain what specific technical mechanism is missing in those works that RLIE uniquely provides.

**Impact:** If a reviewer identifies prior work with overlapping methodology, the core contribution claim is invalidated.

**Required fix (Must):** Replace the "first" claim with a bounded, falsifiable statement: specify the exact gap (e.g., "no prior work has applied regularized logistic regression specifically to the ternary judgments of LLM-generated natural-language rules with a systematic comparison of inference strategies"). Add explicit differentiation from the most closely related methods, ideally in a comparison table.

### W4. Underspecified iterative refinement loop (Major)
**Location:** Page 3–4 — Section 3.3 (lines 33, 70–75)

The iterative refinement stage sends hard examples and the current rule set to the LLM for "reflective generation of improved rules." However, the prompt structure, the LLM's decision logic (revise vs. generate new vs. delete), and the criteria for revision are not described in the main text. The paper does not clarify whether the LLM is shown the learned weights alongside the rules during refinement, which would significantly affect whether the feedback loop actually improves rule quality.

**Impact:** The refinement mechanism is a key component differentiating RLIE from single-pass rule generation. Without specification, the method cannot be independently reproduced, and the improvement from iteration cannot be attributed to a specific mechanism.

**Required fix (Must):** (1) Add a paragraph summarizing the revision prompt structure in Section 3.3. (2) Specify whether weights are shown to the LLM during refinement. (3) Add a convergence analysis showing how validation performance changes across iterations.

### W5. Speculative explanation for the central finding (Major)
**Location:** Page 7 — Section 5.2 (lines 153–156), Section 6 Discussion

The paper's most interesting finding — that LLM-based inference degrades when given more information — is attributed to LLMs being "less reliable at fine-grained, controlled probabilistic integration" and "can be led astray." However, no direct evidence is provided for this explanation. The paper lacks:
- Reasoning trace analysis (what did the LLM actually do with the weights?)
- Controlled experiments (e.g., varying prompt format, testing simpler weight presentations)
- Ablation of the information type (is the degradation from weights, from the Linear prediction, or from context length?)

**Impact:** Alternative explanations are equally plausible: the LLM may be confused by poor prompt formatting, may treat the Linear prediction as a conflicting authority rather than supplementary evidence, or may suffer from context-length interference. Until these are ruled out, the claimed "limitation of LLMs" is not firmly established.

**Required fix (Must):** (1) Add a post-hoc analysis categorizing LLM disagreements. (2) Include 5–10 qualitative examples of LLM reasoning traces showing how it handles (or fails to handle) the weighted rules. (3) Add a control experiment with a simplified weight presentation format.

### W6. No sensitivity analysis for critical hyperparameters (Minor–Major)
**Location:** Page 5 — Section 4.3 (lines 305–308)

Three key hyperparameters are reported but never analyzed for sensitivity:
- Coverage threshold γ = 0.2
- Hard example count k = 20
- Capacity limit H = 10

These values directly affect rule set quality, learning dynamics, and final performance. Without ablation, readers cannot assess whether the chosen values are optimal or whether the method is robust to reasonable variations.

**Recommended fix (Nice-to-have):** Add a sensitivity analysis for γ ∈ {0.1, 0.2, 0.3, 0.5} and k ∈ {10, 20, 30} on at least two datasets, reporting validation F1.

### W7. Overclaiming in Discussion and Conclusion (Minor)
**Location:** Page 8 — Section 7 (lines 161–162)

The Conclusion introduces the unsupported concept of "knowledge discovery" and claims the framework "paves the way for more building reliable AI." The Discussion proposes a "replicable engineering principle" based on limited experiments (six small datasets, one LLM for rule evaluation, one probabilistic combiner). These claims go beyond what the evidence supports.

**Recommended fix (Nice-to-have):** Rewrite the Conclusion to focus on validated findings, enumerate limitations, and propose specific next steps. Replace "replicable engineering principle" with "promising design pattern observed under the tested conditions."

### W8. Missing prompt format details for E2–E4 (Minor)
**Location:** Page 5 — Section 3.4 (lines 76–82)

The evaluation strategies E2–E4 differ only in what information is included in the LLM prompt, but the main text does not describe how weights and the Linear prediction are formatted. This is critical because the central finding (that more information degrades performance) could be an artifact of poor prompt design.

**Recommended fix (Nice-to-have):** Add 3–4 sentences in the main text summarizing the weight/Linear-prediction prompt format, with an example. Verify that at least two different prompt phrasings produce the same qualitative result.

### W9. Missing rule quality evaluation beyond predictive performance (Minor)
**Location:** Page 7 — Section 5

The paper claims "the learnt rule sets are more compact and semantically clearer, prompting knowledge discovery and human-AI consensus" (Contribution 3) but provides no human evaluation or quantitative measure of rule quality beyond predictive accuracy. There is no assessment of rule interpretability, novelty, or semantic coherence.

**Recommended fix (Nice-to-have):** Add a small user study or at least an automated rule quality metric (e.g., uniqueness, coverage diversity, overlap with ground-truth patterns) to support the "semantically clearer" claim.

## Score
**Final Score: 5.5/10**

**Scoring rationale (research value + novelty prioritized):**

- **Research value:** The paper addresses a relevant and timely problem (combining LLM rule generation with probabilistic aggregation). The hierarchical inference strategy comparison (E1–E4) produces practically useful insights. However, the small scale of experiments (200/200/300 splits, six datasets) and missing variance reporting substantially limit the strength of the empirical contribution. **Score contribution: 6/10.**

- **Novelty:** The core idea of using logistic regression to weight LLM-generated rules is methodologically sound but incremental. The "first to combine" claim cannot be verified without literature search (deferred). The main novelty is the systematic evaluation design rather than a fundamentally new algorithm. **Score contribution: 5/10.**

- **Validity/Soundness:** The framework is clearly described but underspecified in key components (iterative refinement prompt, hyperparameter selection details). The central empirical finding lacks mechanistic evidence (no reasoning trace analysis). Missing standard deviations in the main table weaken statistical validity. **Score contribution: 5/10.**

- **Reproducibility:** Prompts are promised in Appendix E (not reviewed), hyperparameter search grids are not reported, backbone-specific details are incomplete. The method description lacks sufficient detail for independent reimplementation. **Score contribution: 4.5/10.**

**Overall assessment:** The paper has a well-motivated research question and a clean framework design, with an informative evaluation strategy that yields a counterintuitive finding. However, several major weaknesses — missing variance reporting, unverifiable novelty claims, underspecified iterative refinement, speculative mechanistic explanation, and small-scale evaluation — prevent the paper from meeting the threshold for a top-tier conference in its current form. The core idea is promising and the negative result about LLM-based inference is interesting, but the evidentiary foundation needs substantial strengthening.

### ASCII Diagram — Paper Structure & Evidence Map

```text
[Problem: No principled combination of LLM rules]
    |
    v
[RLIE Framework]
    |-- Stage 1: Rule Generation (LLM + coverage filter)
    |       Evidence: γ=0.2 threshold, k=20 random samples
    |       Gap: No sensitivity analysis for γ
    |
    |-- Stage 2: Logistic Regression (Elastic Net)
    |       Evidence: Selected via stratified CV on S_val
    |       Gap: (λ, α) grid not reported
    |
    |-- Stage 3: Iterative Refinement (error-driven)
    |       Evidence: k=20 hard examples, H=10 capacity
    |       Gap: LLM revision prompt not described
    |
    |-- Stage 4: Evaluation (E1-E4 inference strategies)
    |       Evidence: Table 1-2 results
    |       Gap: No std dev shown, no reasoning traces
    |
    v
[Claims]
    C1: "first to combine LLMs + probabilistic methods"
        -> UNVERIFIABLE (literature search deferred)
    C2: "hierarchical evaluation reveals LLM limitations"
        -> PARTIALLY SUPPORTED (missing mechanistic evidence)
    C3: "superior overall performance"
        -> PARTIALLY SUPPORTED (missing std dev, small datasets)
```

### ASCII Diagram — Revision Strategy Roadmap

```text
P0 (Must fix — before acceptance)
├── W1: Add std dev to Table 1 + significance tests
├── W2: Bound claims to small-data regime, add CIs
├── W3: Replace "first" claim with bounded gap statement
├── W4: Specify iterative refinement prompt in main text
└── W5: Add reasoning trace analysis + controlled experiments

P1 (Should fix — strengthens paper)
├── W6: Add sensitivity analysis for γ, k, H
├── W7: Rewrite Conclusion to remove unsupported claims
└── W8: Summarize prompt format for E2-E4 in main text

P2 (Nice-to-have — extends contribution)
├── W9: Add human evaluation of rule quality
├── Larger dataset experiments (1000+ samples)
├── Test with different LLMs for rule evaluation (beyond gpt-4o-mini)
└── Compare with stronger combiners (GAMs, Bayesian LR)
```

### ASCII Diagram — Related-Work Taxonomy Tree (Layered)

```text
Rule Learning (Root)
├── Branch 1: Classical Rule Learning
│   ├── Leaf 1.1: ILP & symbolic [Cropper+22, Cerna+24]
│   ├── Leaf 1.2: Rule sets & lists [Yang+17, Xu+24, Qiao+21]
│   └── Leaf 1.3: Probabilistic rule combinations [Ruczinski+03, Friedman+08]
│       └── Our work builds on Leaf 1.3's linear log-odds model
│
├── Branch 2: LLM-Based Rule Learning
│   ├── Leaf 2.1: Single-hypothesis refinement [Qiu+23, IO Refinement]
│   ├── Leaf 2.2: Multi-hypothesis sets [Zhou+24, HypoGeniC; Yang+23]
│   └── Leaf 2.3: LLM+retrieval/context rules [Zhang+24, RuAG]
│       └── Our work: RLIE combines Leaf 2.2 (multi-rule)
│           with Leaf 1.3 (probabilistic weighting)
│
└── Branch 3: Neuro-Symbolic & Differentiable Methods
    ├── Leaf 3.1: Differentiable ILP [Glanois+22, Yang+24a]
    └── Leaf 3.2: Neural rule generation [Singh+22, Ellis+23]

[Novelty Note: RLIE's claimed contribution — applying logistic
 regression as a global combiner over LLM-generated ternary
 rule judgments — is a specific technical integration not
 present in any single prior work. However, the individual
 components (LLM rule generation + logistic regression on
 binary features) are well-established. The verification of
 "first" requires external literature search.]
```

**Note on Novelty Verification:** This review operates in Retrieval-Disabled Mode (external paper search unavailable). All novelty/comparison claims (especially C1's "first" assertion) should be treated as **deferred manual verification required**. The authors are strongly advised to conduct a thorough literature search and position their contribution relative to the nearest related works, particularly incorporating comparisons with probabilistic rule learning in ILP (ProbLog), recent LLM+ensemble methods, and soft-rule neuro-symbolic frameworks.