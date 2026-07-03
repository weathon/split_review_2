## Summary

This paper addresses the problem of making Chain-of-Thought (CoT) reasoning traces "monitorable" — faithful (honestly reflecting factors that influenced the answer) and concise (short enough to inspect). The authors formulate this as a constrained optimization problem and show that naive RL fails because the monitorability gradient vanishes when the base model rarely produces high-*f*(*z*) traces. They propose using an instruction-tuned prior model (Qwen 2.5-7B Instruct) to transform base-model traces into monitorable form, filter them for correctness and monitorability, and then train the base model (DeepSeek R1 Qwen-1.5B) via SFT on these transformed traces. Results are reported on MMLU-Pro (faithfulness), GSM8K, and MATH500 (conciseness).

## Strengths

1. **Clean diagnosis of naive RL failure**: The paper provides both a mathematical explanation (Eq. 4–5: the monitorability gradient L₁ vanishes because *f*(*z*)≈0 under the base policy) and empirical verification (Figure 2: faithfulness ~30%, conciseness ~12% remain flat after 500 steps of RL). This clearly identifies the core problem and is the paper's strongest conceptual contribution.

2. **Proof-of-concept experiment isolates the true bottleneck**: Figure 3 shows that when a prior model transforms traces and the *unchanged* base model is conditioned on these transformed traces, faithfulness jumps from ~30% to 85% and conciseness from ~12% to 97%, while accuracy is maintained or slightly improved. This cleanly demonstrates that the base model *can* reason faithfully/concisely — the bottleneck is generation probability, not capability — and directly motivates why supervised imitation of transformed traces is a viable solution.

3. **Algorithm 1's dual filtering is technically sound**: The algorithm filters candidate traces by both the monitorability constraint and reward preservation, then selects the highest-likelihood sample under the base model. This explicitly addresses distribution shift between the prior and the student model, a concrete technical consideration that prior distillation pipelines often overlook.

## Weaknesses

### Fatal

None.

### Major

1. **Numerical inconsistency in the central faithfulness claim**: The results text (line 286) states that the proportion of faithful completions "rises by **22 percentage points**" and that this is "**nearly a two-fold increase**." However, Figure 4's table shows Baseline 15.2% → Trained 25.0%, which is an increase of **9.8 percentage points** (a ~64.5% relative increase, i.e., ~1.64× — not "nearly two-fold"). The Figure 4 caption claims "over 67% relative gain" (actual: ~64.5%). The abstract states "about an additional 10%" (close to 9.8 pp but ambiguous). A reader cannot determine which number to trust, and the "22 percentage points" claim is wrong by more than a factor of two. This is a concrete error in the paper's most prominently advertised result.

2. **Accuracy retention is reported inconsistently**: The contributions list (line 55) claims "maintaining **at least 96%** of the base model's task accuracy in both the tasks." However, the conciseness results (line 296) state "The accuracy drop remains within ~10% relative," implying ~90% retention, and the Figure 5 caption (line 307) says "approximately 90%." The difference between 96% and 90% retention is substantial and the paper offers no clarification or reconciliation.

3. **60-point gap between prior faithfulness (85%) and trained model faithfulness (25%) is not discussed**: Figure 3 shows that the prior-guided transformation (using πₛ to rewrite traces and decoding with π₀) achieves 85% faithfulness. Yet the actual trained policy only reaches 25.0% (Figure 4), only ~10 pp above the baseline of 15.2%. If the prior can produce faithful traces that the base model can successfully decode, why does SFT on those traces recover only a fraction of this capability? This is the method's biggest practical limitation and the paper does not analyze or even acknowledge this gap.

### Minor

4. **Conciseness results lack basic length statistics**: The paper claims a "60% reduction" and "order of magnitude" decrease in reasoning length, but reports only the percentage of responses under a length threshold (β=125 for GSM8K, β=950 for MATH500). Actual mean/median token lengths for the base and trained models are not reported, making it impossible to directly verify these magnitude claims from the data presented. Figure 6 shows distribution shifts but uses density-like y-axis scales (0–1.5) labeled "Number of Responses," which is confusing.

5. **Gradient decomposition (Eq. 4) is technically incomplete**: The policy gradient of the Lagrangian (Eq. 3) through π(z|x) produces a term 𝔼[∇log π(z|x) R(x,y)] that couples reward back through the trace policy; this term is omitted from Eq. 4. The Lagrange multiplier λ is also dropped without comment. These omissions make the derivation technically sloppy, though they do not undermine the paper's central claim (that the monitorability gradient L₁ vanishes).

6. **Algorithm 1 includes potentially flawed training data when the base model is wrong**: When R(x,y)=0 (base model produces the wrong answer), the filter on line 239 (R(x,yᵢ) = R(x,y)) retains only transformed traces that also produce wrong answers. The training dataset D can therefore contain (x, zₛ, wrong_answer) triples. The paper does not discuss this or report the fraction of training data from incorrect base-model outputs.

### Trivial

7. Figure 4 caption claims "over 67% relative gain" but actual computation (25.0/15.2) gives ~64.5%.
8. Figure 6's y-axis scale (0–1.5) suggests these are density rather than count plots, but they are labeled "Number of Responses."

## Nice-to-Haves

- Report absolute accuracy numbers for the trained model on GSM8K/MATH500 in a table alongside the conciseness metrics.
- Provide mean/median token lengths for base and trained models to substantiate the "60% reduction" and "order of magnitude" claims.
- Include an analysis of why trained faithfulness (25%) lags so far behind the prior-guided proof-of-concept (85%).
- Report what value of λ was used in the naive RL experiments.
- Discuss the fraction of training data that comes from incorrect base-model outputs (R(x,y)=0).

## Removed Points

The following points from the reviews were removed (with brief justification):
- **"96.6% appearing in both Figure 3 and Figure 5 on MATH500 is suspicious"** — removed because a ceiling effect naturally explains this; both the prior and the trained model reach near-perfect conciseness on MATH500 under a 950-token threshold.
- **"No comparison to prior conciseness methods"** — removed because the paper's contribution is about overcoming sparse monitorability gradients, not about achieving SOTA conciseness; this is outside the paper's stated scope.
- **"No statistical significance or variance reporting"** — removed because single-run evaluation is standard practice for this line of work.
- **"Missing related works"** — not verifiable without external sources.
- **"Missing appendix content"** — parser artifact; appendices exist in the original submission.
- **Various reproducibility nitpicks (hyperparameters, implementation details)** — standard for the field.
- **Formatting/style complaints about figure descriptions** — parser artifacts.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. Reconcile the numerical claims: correct "22 percentage points" to ~9.8 pp, and resolve the 96% vs 90% accuracy retention discrepancy. Ensure all numbers in the abstract, contributions, results text, and figure captions are consistent with the tables.
2. Add a dedicated analysis section or paragraph discussing why the trained model's faithfulness (25.0%) is far below the prior-guided proof-of-concept (85%), and what this gap implies about the method's limitations.
3. Report actual mean/median token lengths for base and trained models on GSM8K and MATH500.
4. Clarify the gradient derivation in Eq. 4 by including the missing cross-term and λ, or explicitly state the simplifying assumptions.
5. Discuss the handling of training examples where the base model produces incorrect answers.

## Score and Decision

Calibration note: The calibration search tool encountered a filesystem issue and could not retrieve anchor papers. I therefore calibrated based on my knowledge of the ICLR scoring distribution. The paper's core idea is timely and well-motivated, and the proof-of-concept experiment (Figure 3) is clean and informative. However, the numerical inconsistencies in the reporting of the main results (particularly the "22 percentage points" error, which misstates the actual improvement by more than 2×) and the unaddressed 60-point gap between the prior-guided proof-of-concept and the trained model are significant shortcomings that prevent acceptance in the current form. The paper falls between "borderline reject" and "borderline accept" — it has genuine merit but the execution issues are too substantial to overlook. A revised version that corrects the numerical errors, reconciles the accuracy retention claims, and analyzes the prior-to-trained gap could be a solid contribution.

MY FINAL SCORE: <score>4.0</score>
MY FINAL DECISION: <decision>Reject</decision>