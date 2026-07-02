## Summary
This paper addresses the challenge of making Chain-of-Thought (CoT) reasoning traces more *monitorable* — specifically, more faithful (accurately reflecting the model's true decision factors) and more concise (short enough for effective human oversight). The authors formulate CoT monitorability as a constrained optimization problem and demonstrate that naive policy gradient methods fail due to sparse gradient signals (the monitorability reward is rarely positive under the initial policy). To overcome this, they propose a prior-guided distillation pipeline: an instruction-tuned model (Qwen 2.5-7B) transforms raw CoT traces into monitorable versions (either verbalizing hidden hints or summarizing verbose reasoning), these transformed traces are filtered for correctness and monitorability, and the base model (DeepSeek R1 Qwen-1.5B) is fine-tuned on the resulting dataset via supervised learning. Experiments on MMLU-Pro (with injected hints), GSM8K, and MATH500 show relative faithfulness improvements of ~67% (from 15% to 25% faithful completions) and reasoning length reductions of up to 80%, while maintaining at least 90% relative task accuracy.

**Core Contribution Claims (C1-C3):**
- **C1:** Formalizing CoT monitorability as a constrained optimization problem with analysis of why policy gradients fail.
- **C2:** A prior-guided data generation pipeline that converts sparse RL into dense supervised learning.
- **C3:** Empirical validation showing improved faithfulness and conciseness with minimal accuracy loss.

**Novelty Verdict:** Due to Retrieval-Disabled Mode in this run, external literature verification was not performed. Novelty claims regarding the formulation and pipeline are deferred for manual literature verification. The empirical results provide partial support for C2-C3, but the core idea of using a larger model to generate training data for a smaller model (distillation) is well-established, and the specific gains over the closest related work (Arora & Zanette, 2025) are not clearly delineated.

## Strengths
**1. Well-motivated problem with clear framing.** The paper identifies a genuinely important and timely problem — CoTs are widely used for interpretability and safety auditing, yet their unfaithfulness is well-documented. The framing as a constrained optimization problem (Eq. 1) is a reasonable formalization that captures the tension between monitorability and task accuracy.

**2. Insightful analysis of why naive RL fails.** The gradient analysis (Section 3, Eq. 4-5) provides a clean theoretical explanation: when the monitorability signal f(z) is rarely positive under the initial policy, the gradient estimator collapses to zero. This diagnosis is intuitive, well-explained, and likely to be broadly applicable to other sparse-reward settings beyond CoT monitorability.

**3. Practical and modular pipeline design.** The prior-guided distillation approach (Algorithm 1) is conceptually straightforward and decouples the three key challenges — trace transformation, quality filtering, and policy learning — into separate steps. This modularity makes the method easy to understand, implement, and potentially extend (e.g., by replacing the prior model or the filtering criteria).

**4. Clear negative result motivates the method.** The "Naive RL fails" demonstration (Figure 2) is a valuable contribution that prevents other researchers from pursuing direct policy gradient approaches for this problem. The empirical negative result, though not comprehensive (single model scale, binary reward), supports the paper's core motivation.

**5. Dual focus on faithfulness and conciseness.** Addressing both dimensions of monitorability within a single framework is more valuable than papers that focus on only one. The proof-of-concept experiment (Figure 3) convincingly shows that both properties are compatible with high accuracy when the prior model provides transformed traces.

**6. Transparent limitation disclosure.** The paper acknowledges key limitations: dependence on external prior quality, and potential subjectivity in LLM-as-a-judge evaluations. This transparency is commendable, though several additional limitations should be discussed (see Weaknesses).

## Weaknesses
### W1. Inconsistent and erroneous numerical claims (Major — Factual Error)

The paper contains mutually contradictory numerical statements about faithfulness improvement:

- **Abstract:** "improves faithfulness by about an additional 10%" — ambiguous (absolute vs relative).
- **Figure 1 caption:** "Base Model at ~15, Ours at ~25 (+10% improvement)" — appears to report +10 percentage points.
- **Figure 4 caption:** "increases the proportion... from 15% to 25%, representing a relative gain of over 67%."
- **Section 5.1 Results:** "rises by 22 percentage points" — but the table in Figure 4 shows Baseline 15.2% → Trained 25.0%, a difference of 9.8 **percentage points** (67% relative), not 22 points.

The "22 percentage points" statement has no basis in the presented data and is a factor-of-2 error. Additionally, the Abstract's "10%" wording is inconsistent with the "67% relative gain" stated elsewhere. These errors erode trust in the paper's quantitative claims.

**Required fix:** Replace "22 percentage points" with "9.8 percentage points (67% relative increase)." Standardize the Abstract to use either "67% relative increase" or "10 percentage points," with explicit wording that distinguishes absolute from relative gains. Provide the absolute accuracy numbers alongside relative changes.

### W2. Lagrangian formulation has formal errors (Major — Mathematical Rigor)

The constrained optimization in Eq. (1)-(3) contains several technical issues:

- **Undefined notation ⟨·⟩ in Eq. (3):** The angle brackets around the constraint term are not defined. Standard Lagrangian relaxation would use λ·(E[R] - R₀) as a penalty that is *subtracted* (not added) when the constraint is violated.
- **Missing λ multiplier in Eq. (4):** The gradient decomposition in Eq. (4) omits the Lagrange multiplier λ from the reward term L₂. If λ ≠ 1, the expression is incomplete.
- **Sign inconsistency:** If λ ≥ 0 and the constraint is satisfied (E[R] ≥ R₀), adding λ⟨E[R] - R₀⟩ would *increase* the Lagrangian for feasible solutions, which is the opposite of standard constrained optimization where the penalty should be zero in the feasible region and positive in the infeasible region.

**Required fix:** Replace ⟨·⟩ with standard max(0, R₀ - E[R]) penalty. Correct Eq. (4) to include λ. Clarify the direction of the Lagrangian (maximization with subtracted penalty or minimization with added penalty).

### W3. Algorithm 1 has an inconsistent filtering criterion (Major — Correctness)

Algorithm 1, Line 13 states: "Keep only z_si such that f(z_si) ≤ β and R(x, y_i) = R(x, y)." The condition f(z_si) ≤ β is inconsistent with the definitions of f(z) in Section 3:

- For **faithfulness**, f(z) = 1{hint verbalized} ∈ {0,1}. Filtering with f(z_si) ≤ β (where β is presumably 1) would accept **both** faithful and unfaithful traces. The correct filter should be f(z_si) ≥ β (accept high-monitorability traces).
- For **conciseness**, f(z) = 1_{Length(z) < 950}, also binary. The same sign error applies.
- Additionally, the selection criterion in Line 14 (highest log-likelihood under π₀) selects traces closest to the base model's distribution — but the paper's core claim is that π₀ assigns low probability to monitorable traces. This selection criterion therefore works **against** the method's goal.

**Required fix:** Change filter to f(z_si) ≥ β for both settings. Replace the likelihood-based selection with f(z_si)-based selection (choose the most monitorable trace among those satisfying the reward constraint). Specify the value of n (number of candidate traces per input).

### W4. Proof-of-concept experiment uses an unfair comparison (Major — Experimental Validity)

Figure 3 compares "Using Prior" (Qwen 2.5-7B Instruct, 7B parameters) against the base model (DeepSeek R1 Qwen-1.5B, 1.5B parameters). The prior is **4.7× larger** than the base model. The dramatic gains (faithfulness: 30%→85%, conciseness: 11.6%→96.6%) should be attributed primarily to the larger model's capacity, not to the *guidance method* itself. Without a same-scale ablation, the paper overclaims the effectiveness of the prior-guided approach.

**Required fix:** Add an ablation using a same-scale prior (e.g., prompting the base model itself with chain-of-thought transformation instructions) or at minimum acknowledge: "The prior model has 4.7× more parameters; we treat this as an upper bound and focus on distilling this capability via SFT." Report 95% confidence intervals for all Figure 3 metrics.

### W5. Faithfulness evaluation has circularity and lacks validation (Major — Metric Validity)

The faithfulness evaluation relies on an LLM-as-a-judge to check whether the hint is verbalized in the CoT. However:

- The **judge model, prompt, and human-agreement rate are not disclosed.** Readers cannot verify the reliability of the metric.
- **Circularity:** The prior model is explicitly prompted to "verbalize the hint influence," and the judge evaluates whether the hint was mentioned. This creates a correlation where the model could learn to *mention* the hint without actually *being influenced* by it — the metric conflates surface-form verbalization with genuine faithfulness.
- **Uncalibrated hints:** The paper reconstructs hints from Chen et al. (2025) but provides no validation that the recreated hints produce comparable baseline faithfulness levels.

**Required fix:** Disclose the judge model, prompt template, and human-agreement rate on a sample of ≥100 examples. Add a counterfactual faithfulness test (e.g., replace the hint with a conflicting hint and check whether the model follows the new hint). Calibrate recreated hints against published baselines.

### W6. Conciseness claims lack absolute accuracy numbers and completeness verification (Major — Reporting)

The paper reports conciseness gains of "approximately 90% relative accuracy" without providing absolute accuracy numbers. A "10% relative drop" could mean a significant absolute drop (e.g., 80% → 72%). Additionally:

- **No semantic completeness check:** Conciseness is defined purely by length threshold. A short trace that omits critical reasoning steps is less monitorable despite being concise. The paper does not verify that shorter traces retain all essential reasoning content.
- **Data source ambiguity:** For conciseness, the paper uses "3,200 training examples from (Arora & Zanette, 2025)." It is unclear whether these examples were processed through the paper's own prior-guided pipeline or used directly from the prior work. If the latter, the conciseness results largely validate Arora & Zanette's data rather than the current method.

**Required fix:** Report absolute accuracies for both base and trained models on GSM8K and MATH500. Add a semantic completeness evaluation (e.g., human rating or automated step-coverage check). Clarify whether the training data was generated by the paper's pipeline or sourced from prior work.

### W7. Related work is a shallow listing without critical differentiation (Moderate — Scholarship)

The Related Work section lists 12+ papers without organizing them by approach, finding, or limitation relative to the current work. Key omissions include:

- No critical comparison with Arora & Zanette (2025), whose data and evaluation code the paper directly uses.
- No positioning within the knowledge distillation literature (the method is essentially a distillation pipeline).
- The "Chain-of-Thought in language models" paragraph reads as a product advertisement (listing OpenAI, Anthropic, DeepSeek, Gemini) rather than a scholarly review.

**Required fix:** Restructure Related Work by methodological axes (e.g., direct RL for conciseness, prompting for faithfulness, distillation for reasoning). Add explicit comparison with Arora & Zanette (2025). Remove or condense the product listing paragraph.

### W8. Vanishing gradient analysis conflates estimator issue with true gradient (Moderate — Theory)

The argument in Eq. (4)-(5) claims that because f(z) ≈ 0 for samples from π₀, the gradient L₁ vanishes. This is correct as a statement about **Monte Carlo estimation** but is presented as a fundamental property of the optimization objective. The true gradient of E[f(z)] may be non-zero even when the estimator from on-policy samples is zero — off-policy corrections, importance sampling, or control variates could recover signal. Furthermore, the conciseness data (Figure 2d) shows f(z) > 0 for ~12% of samples, contradicting the f(z) ≈ 0 assumption.

**Required fix:** Clarify: "The on-policy Monte Carlo gradient estimate is zero in expectation, meaning the policy receives no learning signal under standard REINFORCE. Off-policy methods could partially address this." Acknowledge the conciseness discrepancy explicitly.

### W9. Missing key experiment details that prevent reproduction (Moderate — Reproducibility)

The paper omits several details critical for reproducing the results:

- RL hyperparameters for the naive baseline (algorithm choice, learning rate, batch size, KL penalty).
- Number of candidate traces n in Algorithm 1, Line 7.
- The LLM judge model and prompting template for faithfulness evaluation.
- Training hyperparameters for SFT (learning rate, epochs, batch size, sequence length).
- Acceptance rate of the filtering step (how many prior-generated traces pass both constraints).

**Required fix:** Add a hyperparameter table covering all experiments. Report the filtering acceptance rate. Disclose the judge model.

### W10. Conclusion omits several critical limitations (Moderate — Completeness)

The Limitations paragraph acknowledges prior dependence and LLM-as-a-judge subjectivity but omits:
- **Distillation gap:** The trained model achieves 25% faithfulness vs the prior's 85% — a massive gap that is not discussed.
- **Computational cost:** The pipeline requires multiple forward passes from a 7B model per training example.
- **Uneven gains:** Faithfulness on 3 of 7 MMLU-Pro categories remains below 13% after training.
- **Single model scale:** All experiments use a 1.5B base model; scaling behavior is unknown.

**Required fix:** Add discussion of the distillation gap, uneven category-level gains, computational overhead, and the need for scaling studies.

## Score
**Final Score: 5.5/10**

**Scoring Rationale:**

The paper addresses a timely and important problem — improving CoT faithfulness and conciseness for safety-critical applications. The constrained optimization formulation and the analysis of why naive RL fails are valuable conceptual contributions. The pipeline design (prior-guided transformation + filtering + SFT) is practical and modular.

However, the score is constrained by several significant issues:

- **Factual errors (W1):** The "22 percentage points" claim contradicts the paper's own data, and numerical claims are inconsistent across the abstract, figures, and main text.
- **Mathematical rigor (W2, W3):** The Lagrangian formulation has sign/notation errors, and Algorithm 1's filtering logic is inconsistent with the definitions of f(z).
- **Experimental validity concerns (W4, W5):** The proof-of-concept uses a 4.7× larger prior model, creating an unfair comparison. The faithfulness metric has circularity risks and lacks validation.
- **Incomplete reporting (W6, W9):** Absolute accuracy numbers are missing for conciseness experiments; key hyperparameters are not disclosed.
- **Distillation gap unaddressed:** The trained model achieves only 25% faithfulness vs the prior's 85%, yet this gap is not analyzed or discussed.

**Primary scoring dimensions:**
- Research value / contribution: 6/10 — the problem framing and failure analysis are valuable, but the incremental nature over Arora & Zanette (2025) for conciseness is unclear.
- Novelty: deferred (external verification unavailable in this run); the prior-guided transformation idea is intuitive but its novelty relative to existing distillation and self-training methods cannot be assessed without literature comparison.
- Validity / soundness: 5/10 — the core results have inconsistent numerical claims and several experimental confounds (model scale mismatch, metric circularity).
- Reproducibility: 4/10 — missing hyperparameters, undisclosed judge model, and reliance on non-public hint templates.

The paper has a solid conceptual core but requires substantial corrections to its numerical claims, mathematical formalization, and experimental controls before it can be considered publication-ready. A revised version addressing the top-priority fixes (W1-W5) could be competitive at W1 and above.