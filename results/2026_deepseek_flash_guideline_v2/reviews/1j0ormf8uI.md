Now I have verified the key claims from the paper. Let me write the final consolidated review.

## Summary

The paper proposes a conformal prediction method for constructing Lower Prediction Bounds (LPBs) for counterfactual survival times under different treatments with general right-censored data. It employs a reweighting scheme to transform the problem into a weighted conformal inference problem, claiming to achieve exact marginal coverage guarantees rather than the PAC-type guarantees of prior work.

## Strengths

1. **Doubly robust property (Theorem 4.2).** The method is shown to maintain coverage even when either the weight function or the quantile estimator is misspecified, provided the other is consistently estimated. This is a genuine theoretical addition beyond standard weighted conformal prediction.

2. **Empirical robustness to outliers.** Figure 3 demonstrates that the proposed method maintains coverage near the nominal level under outlier contamination, while the PAC-type baselines (Focus, Fused) degrade substantially. This is the clearest empirical validation of the practical distinction the paper aims to draw.

3. **Real clinical validation.** The method is applied to 541 NSCLC patients across four radiochemotherapy regimens, producing LPBs consistent with established clinical findings (VMAT > IMRT, induction/concurrent chemotherapy benefit). This demonstrates applicability in a heterogeneous clinical setting.

## Weaknesses

### Major

1. **The derivation of Equation (1) contains an unjustified inequality direction that undercuts the central theoretical claim.** Step (iii) states
   \[
   \mathbb{E}_X[\mathbb{P}(T \leq \cdot \mid X, W) \cdot 1/p(e{=}1\mid X,W)] \leq \mathbb{E}_X[\mathbb{P}(T \leq \cdot, e{=}1 \mid X, W) \cdot 1/p(e{=}1\mid X,W)]
   \]
   but basic probability gives \(\mathbb{P}(A) \ge \mathbb{P}(A\cap B)\), making the left side \(\ge\) the right side. The paper states that this step "is derived by the proof of Lemma A.1" (in the appendix), but the main-text derivation as presented has the inequality reversed. If the direction is truly \(\ge\) rather than \(\le\), then the chain does not produce an upper bound on \(\alpha\) — it produces a lower bound, and calibrating the weighted conformal procedure would not guarantee the claimed coverage. This is a structural problem with the paper's central theoretical contribution.

2. **The coverage guarantee in Theorem 4.1 is for a different distribution than the claimed target.** Theorem 4.1 (line 182) guarantees coverage for \((X, T(w)) \sim \mathbb{P}_X \times \mathbb{P}_{T(w)\mid X, e=1}\), a mixture where \(X\) is drawn from the marginal but \(T(w)\) is drawn conditional on being uncensored. The stated goal (line 64) is coverage for \(\mathbb{P}_{X,T(w)}\), the joint marginal distribution. Even under the ignorability assumption \(T \perp\!\!\perp C \mid X, W\) (Assumption 3.1), the event indicator \(e = \mathbf{1}\{T < C\}\) depends on \(T\), so \(\mathbb{P}_{T(w)\mid X, e=1} \neq \mathbb{P}_{T(w)\mid X}\) in general. The paper asserts (line 140) that "it is sufficient" for the LPB to satisfy coverage for the conditional-on-\(e{=}1\) distribution, but provides no justification or bound on the gap. This means the theoretical result does not establish coverage for the quantity the paper claims to cover.

   These two issues together mean that the paper's core theoretical contribution — the "exact marginal coverage guarantee" highlighted in the abstract, introduction, and contributions list — is not adequately supported by the derivations and theorems as presented in the main text.

3. **The "exact marginal coverage" claim is overstated relative to what is actually proved.** Theorem 4.1 includes an error term \(\frac12 \mathbb{E}[|\tilde{\omega} - \omega|]\) that depends on weight estimation quality, and Theorem 4.2 is asymptotic (\(N,n \to \infty\)). The contrast drawn in the paper between "exact" guarantees and prior PAC-type guarantees is therefore less sharp than claimed: the proposed method also depends on estimation quality (of \(\gamma(x)\)), and in finite samples the guarantee is only approximate.

### Minor

4. **Only uncensored treated observations are used for calibration** (Algorithm 1, Step 3). In settings with high censoring rates or imbalanced treatment proportions, the effective calibration sample can be very small, affecting the reliability of quantile estimates. The paper does not discuss this limitation or report effective sample sizes.

5. **No comparison with alternative conformal survival approaches.** The baselines (Uncal, Naive, Focus, Fused) are all from the same family (Davidov et al., 2025). Comparisons with Cox-based conformal calibration or the method of Candès et al. (2023) (for Type-I censoring settings where it applies) would strengthen the evaluation.

6. **Real-data experiments lack confidence intervals for coverage rates.** With ~541 patients split 50/10/30/10 across four treatment regimens, some test cells are very small (~10–20 patients per regimen). Coverage estimates from 10 independent trials are reported without confidence intervals, making it difficult to assess whether observed coverage is statistically different from the nominal level.

7. **No discussion of sensitivity to weight model misspecification** beyond the asymptotic doubly robust result. The method requires estimating \(\gamma(x) = P(W=w, e=1 \mid X)\), which involves modeling both treatment assignment and the censoring mechanism. The paper uses a Random Forest for this but does not evaluate how misspecification affects finite-sample performance.

### Trivial

None.

## Nice-to-Haves

- Report effective calibration sample sizes for each experimental setting to help assess practical reliability.
- Add confidence intervals (e.g., binomial tests or bootstrap) for coverage rates in real-data experiments.
- Include comparisons against Cox-based conformal calibration methods where applicable.

## Removed Points

- **Criticism about "tower property" justification in step (ii):** This is a presentation issue rather than a substantive mathematical error. The real problem is the inequality direction in step (iii), which is kept above.
- **Criticism about the characterization of Candès et al. (2023):** The paper's framing of prior work is adequate for context.
- **Criticism about missing related work:** Cannot be verified without external sources.
- **Formatting and appendix-related nitpicks:** Stripped in the PDF extraction process.
- **Strength Finder's generic strengths** (e.g., "firstly establishes exact guarantee"): This conflicts with verified weaknesses #1–3 and cannot be retained as stated.

## Novel Insights

None beyond the paper's own contributions. The review surfaces a significant gap between what the paper claims to prove (exact marginal coverage for \(\mathbb{P}_{X,T(w)}\)) and what it actually proves (coverage for \(\mathbb{P}_X \times \mathbb{P}_{T(w)\mid X, e=1}\) with a potentially reversed inequality in the derivation linking the two). This gap is the reviewers' main finding.

## Suggestions

1. **Fix the derivation of Equation (1).** Clarify the justification for step (iii) and verify the inequality direction. If Lemma A.1 contains a correct argument, summarize it faithfully in the main text.
2. **Clarify the target distribution.** Either prove that \(\mathbb{P}_{T(w)\mid X, e=1} = \mathbb{P}_{T(w)\mid X}\) under the stated assumptions (or additional ones), or bound the gap between coverage under the two distributions. Alternatively, explicitly state that the guarantee is for the mixture distribution \(\mathbb{P}_X \times \mathbb{P}_{T(w)\mid X, e=1}\) and qualify the "exact marginal" claim accordingly.
3. **Qualify the "exact" claim** in the abstract and introduction to reflect the dependency on weight estimation quality and the asymptotic nature of Theorem 4.2.
4. **Add confidence intervals** to real-data coverage estimates and report per-treatment calibration/test sample sizes.

MY FINAL SCORE: <score>3.0</score>
MY FINAL DECISION: <decision>Reject</decision>