Now let me produce the final consolidated review.

## Summary

This paper presents the first theoretical analysis of training dynamics and in-context learning (ICL) generalization for a one-layer Mamba model on binary classification tasks with outliers. It proves explicit convergence bounds (Theorem 1), ICL generalization guarantees under distribution-shifted outliers (Theorem 2), and derives mechanistic insights showing how the gating layer suppresses outliers while inducing an exponential-decay local bias (Corollaries 1–2). A parallel analysis of linear Transformers (Theorems 3–4) establishes that Mamba's gating makes training harder (larger batches, more iterations) but enables robustness to a higher fraction of outliers (α approaching 1 under conditions) versus the linear Transformer's α < 1/2 limit. Experiments on synthetic data support the theoretical predictions.

## Strengths

- **First training-dynamics analysis for Mamba ICL.** Provides explicit, non-vacuous convergence bounds (batch size B ≳ B_M, iteration count T ≥ T_M = Θ(η⁻¹(1−p_a)⁻¹β⁻²M₁), prompt length conditions) that go beyond prior work analyzing only global minima of Mamba-like models (Li et al., 2024b; 2025b). This is a genuine theoretical contribution to an important open problem.

- **Sharp and clean comparison of outlier-fraction thresholds.** Theorems 2 and 4 prove Mamba can generalize when α < min(1, p_a·l_tr/l_ts) (potentially approaching 1 under the right prompt-length ratio) while linear Transformers are fundamentally limited to α < 1/2. Figure 2 experimentally validates this threshold across three distinct outlier-labeling functions. This is the paper's headline result and it is well-supported.

- **Mechanistic decomposition with testable predictions.** Corollaries 1 and 2 show trained Mamba's linear attention selects same-pattern examples (∑ attention ≥ Θ(1) vs. ≤ O(ε)) while the gating layer suppresses outliers (G ≤ O(poly(M₁)⁻¹)) and applies exponential decay (∼1/2^{j−1}) by index distance. These are not existence claims — the specific exponential rate 1/2^{j−1} is verified in Figure 4. This level of mechanistic specificity is unusual and valuable in theoretical ICL papers.

- **Honest treatment of the training-robustness tradeoff.** The paper does not claim unconditional superiority. Remark 4 explicitly quantifies Mamba's larger batch and iteration requirements (T_M = Θ(l_tr)·T_T, plus a lower bound on outlier magnitude κ_a that Transformers do not need). This clarifies the tradeoff rather than overselling.

- **Non-obvious empirical finding with mechanistic explanation (Table 1).** Mamba drops from 99.73% (outliers far from query) to 82.73% (outliers close to query) while linear Transformers remain stable at ∼94%. This is a direct consequence of the local-bias mechanism in Corollary 2 and provides a clean, controlled test of a non-obvious prediction of the theory.

## Weaknesses

### Fatal
None.

### Major
None.

### Minor
- **The "α approaches 1" claim is presented without the required qualification in the abstract and P2.** The paper's headline framing says Mamba "maintains accurate ICL generalization even when the fraction of outlier-containing context examples approaches 1" (line 31) and "α goes to 1" (line 95, 207). The actual guarantee in Theorem 2 condition (c) is α < min(1, p_a·l_tr/l_ts). Remark 3 explains this condition, but the abstract and contributions section use unqualified language that overstates what is proved. The bound is still impressive — it can approach 1 when p_a·l_tr/l_ts ≥ 1 — but the paper should lead with the actual condition.

- **No error bars, confidence intervals, or multi-seed reporting.** For synthetic experiments that are computationally cheap, this is a meaningful omission. Figure 2 shows Mamba error at ∼10⁻⁴ in some conditions; without variance estimates, it is impossible to assess whether this reflects genuine separation or a single favorable run.

- **Experimental batch size not reported.** Theorem 1 requires B ≳ B_M = max{B_T, β⁻⁴V²κ_a⁻²(1−p_a)⁻² log ε⁻¹}. The experiments do not report the batch size used, making it impossible to verify whether the experiments respect or violate this bound.

- **Restrictiveness of the testing outlier condition is under-discussed.** Theorem 2 condition (a) requires test outliers to be linear combinations of training outliers with coefficients summing to L > 0. While the paper says this "captures a wide range of possible outlier patterns," it excludes test outliers orthogonal to the training outlier subspace. This is a genuine limitation that should be discussed explicitly rather than noted as a side qualification.

### Trivial
- The derivation from the full Mamba recurrence (1) to the equivalent form (3) is critical to the analysis but is stated without intuition in the main text (deferred to Appendix E.1). A brief sketch would help the reader understand what assumptions are required.

## Nice-to-Haves
- **The CQ failure mode (Table 1) deserves theoretical analysis.** The paper finds empirically that placing outliers close to the query degrades Mamba to 82.73% while linear Transformers remain at ∼94%. This is the most interesting limitation identified in the experiments, and a theoretical account of why the gating mechanism's local bias becomes a vulnerability in this setting would substantially strengthen the paper.
- **Discussion of sufficient vs. necessary conditions.** The experiments test α up to 0.8 with p_a = 0.6 and l_tr = l_ts = 20, a regime where Theorem 2's sufficient condition gives α < 0.6. The fact that Mamba works beyond the proved bound is a positive result, but a brief comment about looseness of the sufficient conditions would prevent confusion.

## Removed Points

These points were raised by reviewers but are removed with justification:

- **"Condition 1 is referenced but not stated"** — The appendix (which contains Condition 1) was stripped by the PDF parser. The paper explicitly says "We restate this condition as Condition 1, along with a construction... in the Appendix." This is standard practice.
- **"The derivation of (3) from (1) is not justified in the main text"** — Standard for theoretical papers to defer derivations to an appendix. The paper states "The derivation can be found in Appendix E.1."
- **"The experiments exceed the theoretical guarantee (α=0.8 > bound of 0.6)"** — This confuses sufficient conditions (what the theorem proves) with necessary conditions. Showing Mamba works beyond the proved bound is a positive finding, not a flaw.
- **"Comparison is with linear attention, not practical softmax Transformers"** — The paper is transparent about this choice (Section 2, Remark 6). The comparison cleanly isolates the effect of gating, which is the paper's stated goal. Remark 6 explicitly acknowledges that practical Transformers can achieve robustness.
- **"Testing outlier labels differ between training and testing (random vs. arbitrary)"** — This asymmetry is by design to model realistic data-poisoning scenarios (Figure 1 example in Section 3.2). The paper motivates this explicitly.
- **"Missing related works"** — Cannot be verified without external knowledge.

## Novel Insights

None beyond the paper's own contributions. The reviewer inputs did not surface a theoretical or methodological insight that the paper itself does not already contain.

## Suggestions

1. Add the p_a·l_tr/l_ts qualification to the abstract's claim about α approaching 1. A phrasing like "Mamba can maintain accurate ICL generalization even when the fraction of outlier-containing context examples approaches 1, provided the training-to-testing prompt-length ratio is sufficiently favorable" would be accurate and still impactful.
2. Report error bars and the batch size used in all experiments.
3. Add a brief discussion of the restrictiveness of Theorem 2 condition (a) (test outliers as positive linear combinations of training outliers) and note that test outliers orthogonal to the training subspace are not covered.
4. Consider adding a theoretical or empirical analysis of the CQ failure mode (Table 1) to complete the mechanism story.

## Score and Decision

**Bracket (Round 1):** After examining the paper and the calibration anchors, I initially bracket the paper between 5.5 and 7.5, comparable to accepted theoretical ICL papers at venues like ICLR.

**Calibration anchors consulted:**
- `n7n8McETXw` (avg 6.50, accepted) — "Training Nonlinear Transformers for Chain-of-Thought Inference." Similar in nature (1-layer, training dynamics, binary classification, synthetic experiments). Our paper has comparable rigor and similar-level weaknesses (simplified architecture assumptions). → Our paper is slightly stronger in novelty (first Mamba analysis vs. extending CoT to nonlinear Transformers).
- `aKJr5NnN8U` (avg 6.50, accepted) — "Toward Understanding In-context vs. In-weight Learning." Theoretical framework with experiments. → Comparable quality.
- `ikwEDva1JZ` (avg 6.50, accepted) — "How Do Transformers Learn In-Context Beyond Simple Functions?" Construction-based results with probing experiments. → Our paper has stronger training-dynamics results (vs. existence constructions).
- `jwsPS8yRe4` (avg 6.00, accepted) — "Trained Transformer Classifiers Generalize and Exhibit Benign Overfitting In-Context." Linear transformer training-dynamics analysis. → Our paper tackles a harder architecture (Mamba with nonlinear gating) and has a more detailed mechanistic analysis.
- `8p3fu56lKc` (avg 6.00, accepted) — "One Step of Gradient Descent is Provably the Optimal In-Context Learner." Linear attention analysis. → Our paper goes beyond linear attention to analyze gating.
- `i9RTCC6whL` (avg 4.67, rejected) — "MAMBA STATE-SPACE MODELS ARE LYAPUNOV-STABLE LEARNERS." Had mixed theoretical-empirical contribution and was rejected. Our paper is substantially stronger in both theoretical depth and empirical grounding.

**Final calibration rationale:** The paper sits in the 6–7 range. It is clearly above the 4.67 rejected Mamba paper and comparable to the 6.0–6.5 accepted theoretical ICL papers. It makes a genuine first contribution (Mamba ICL training dynamics) with clean theoretical framing and testable mechanistic predictions. The weaknesses are presentation-level (abstract overclaiming the α bound, missing experimental variance) and do not threaten the core claims. It is not in the 7.5+ range because the experimental validation lacks error bars and the simplified setup (one-layer, binary classification) mirrors the standard limitations of the subfield rather than breaking new empirical ground.

MY FINAL SCORE: <score>6.5</score>
MY FINAL DECISION: <decision>Accept</decision>