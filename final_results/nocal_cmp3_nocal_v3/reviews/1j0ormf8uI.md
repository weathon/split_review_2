## Summary

This paper proposes a conformal prediction procedure for constructing lower prediction bounds (LPBs) for counterfactual survival times under general right-censored data. The core idea is to transform the counterfactual coverage problem into a weighted conformal inference problem using a density ratio that reweights the distribution of uncensored observations to match the target population. The authors claim an exact marginal coverage guarantee (as opposed to PAC-type guarantees from prior work), prove a doubly-robust property, and validate on synthetic and clinical lung-cancer data.

## Strengths

- **Well-motivated problem.** The gap between PAC-type guarantees (which hold only with high probability over the calibration sample) and exact marginal coverage is a genuine limitation of existing work (Gui et al., 2024; Davidov et al., 2025). The paper correctly identifies this gap, and the clinical motivation around personalized treatment decisions is concrete.

- **Robustness experiment with outliers (Figure 3).** The synthetic experiment showing that the proposed method maintains coverage under distribution shift (outliers) while PAC-based methods degrade is informative and demonstrates a practical advantage of the exact coverage framing. This is the strongest empirical evidence in the paper.

- **Doubly-robustness property.** Theorem 4.2 provides a meaningful theoretical contribution: the procedure remains valid if either the weight function or the quantile estimator is consistently estimated. This is non-trivial and goes beyond a basic application of weighted conformal prediction.

## Weaknesses

### Fatal

None.

### Major

1. **The core derivation in Equation (1) is not mathematically sound as presented.** This is the paper's central reduction -- transforming the target marginal coverage into a weighted conformal problem -- and it contains two verifiable problems in the main text:

   - **Step (ii)** (line 132) introduces the factor `1/p(e=1 | X, W=w)` and attributes it to "the tower property." Standard probability gives  
     `𝔼_X[ℙ(T ≤ · | X, W=w)] = 𝔼_X[𝔼[I(T ≤ ·) | X, W=w]]`,  
     which does not produce a factor of `1/p(e=1|X, W=w)`. This step is not justified.

   - **Step (iii)** (line 133) replaces `ℙ(T ≤ · | X=x, W=w)` with `ℙ(T ≤ ·, e=1 | X=x, W=w)` and claims `≤` between the two expressions. Since `ℙ(A) ≥ ℙ(A ∩ B)` for any events A, B, multiplying by the positive factor `1/p(e=1|...)` gives `≥`, not `≤`. The paper asserts the inequality direction is "derived by the proof of Lemma A.1" (in the appendix, which is stripped), but as written in the main text the direction contradicts basic probability.

   **Impact:** This derivation is the theoretical foundation for the entire method. If it is incorrect, the claim that weighted conformal prediction solves the original (unconditional) marginal coverage problem is unsupported. Even if the appendix provides a valid alternative argument, the main text alone is insufficient for reviewers to verify the correctness of the central claim. This is the most serious weakness in the paper.

2. **Mismatch between the stated goal and Theorem 4.1's guarantee.** The paper repeatedly claims (abstract, lines 28, 44, 62-65) to provide coverage for `ℙ_{X,T(w)}(T(w) ≥ LPB) ≥ 1-α`. However, Theorem 4.1 (line 182) guarantees coverage under `ℙ_X × ℙ_{T(w)|X, e=1}` -- i.e., the test distribution for the outcome is the *conditional-on-no-censoring* distribution, not the full marginal. The paper acknowledges this shift (lines 170-172, 140) and asserts it is "sufficient" via the derivation in Equation (1). Because the derivation in Equation (1) has the problems described above, the gap between what is proved and what is claimed remains unbridged. This is not a minor phrasing issue; it concerns the paper's central advertised contribution.

3. **Real-data coverage evaluation is not explained.** For right-censored survival data, the true survival time T is not observed for censored patients. To compute whether `T ≥ LPB` on test data (Figures 4, 5), the paper must either exclude censored patients (inducing selection bias), impute censored times, or use long-enough follow-up that all patients have events. The paper does not state which approach is used. For the clinical dataset (541 patients, four treatment groups), some test patients will inevitably be censored. Without knowing how coverage is computed, the real-data coverage claims in Figure 4 are unverifiable.

### Minor

1. **"Relative LPB" is not defined in the main text.** Figures 1-4 present results in terms of "Relative LPB," and the caption says "A higher relative LPB is better," but no formal definition is given. This metric appears to be the LPB scaled by some reference, but the reader cannot interpret the results without consulting the appendix (which is stripped).

2. **The LPB optimization over τ per test point introduces an unaddressed concern.** Section 4.1 (lines 162-166) selects `τ^*(x)` per test point to maximize the LPB. The coverage guarantee needs to hold for the chosen τ uniformly. The paper asserts "our procedure yields a prediction set that satisfies the coverage guarantee for any τ ∈ (0,1)" but does not discuss whether the per-test-point optimization changes the coverage properties (e.g., through selective reporting or dependence between τ selection and the calibration data).

3. **Baselines are only briefly described.** Methods named "Uncal," "Naive," "Focus," and "Fused" (Figure 1) are introduced in a single sentence (line 236) without definitions of how each constructs its LPB. This makes it difficult to assess whether the comparison is fair.

4. **Effect of weight estimation on coverage is not ablated.** The method's practical coverage depends entirely on how well a Random Forest estimates `γ(x) = P(W=w, e=1 | X=x)`. A simple experiment comparing oracle weights (true γ) vs. estimated weights would isolate whether the slight under-coverage in Setting 6 (Figure 1) is due to weight estimation error or the conformal procedure itself.

### Trivial

None.

## Nice-to-Haves

- The paper would benefit from stating the guarantee more precisely in the abstract and introduction. If the guarantee is for `ℙ_X × ℙ_{T(w)|X, e=1}` (the uncensored subpopulation), this should be transparent from the start rather than described as "exact marginal coverage" without qualification.
- An ablation of the weight estimation (oracle vs. estimated) would strengthen the empirical analysis.
- Reporting the effective calibration sample sizes per treatment group (i.e., number of calibration points with `W=w, e=1`) would contextualize the variance in coverage estimates, especially for the clinical dataset.

## Removed Points

The following points from the input review were removed with justification:

- **"Derivation in Equation (1) has cumulative effect making central identity unreliable"** — kept, but restated more precisely above. The specific step (ii) "tower property" and step (iii) inequality direction issues are retained.
- **"Theorem 4.1 is described as distribution-free exact guarantee when it is actually for a covariate-shifted *and* selection-biased distribution"** — kept (merged with Major weakness #2 above).
- **"Conditioning on e=1 induces selection bias: larger T(w) less likely to satisfy T(w) < C"** — this is a speculation about the relationship between the two distributions but is not presented as a verifiable formal argument in the paper. The *fact* that Theorem 4.1 covers ℙ_{T(w)|X,e=1} rather than ℙ_{T(w)|X} is verifiable; the *claim* about stochastic dominance is speculative reasoning. Retained only the factual mismatch.
- **"Overstates contrast with prior work — Theorem 4.1 also has an error term"** — the error term from weight estimation is explicitly acknowledged in Theorem 4.1 and the text. The paper's distinction between PAC-type (probabilistic over calibration draws) and exact (marginal over X, T) is a different dimension from the weight-estimation error term. The reviewer conflates them. Removed.
- **"Related Work is thin"** — no concrete anchor in the paper; generic. Removed.
- **"Assumption 3.1 is very strong"** — the paper acknowledges this in Remark 3.2 and the Discussion (Section 6). Generic criticism of a standard assumption. Removed.
- **"Non-conformity score uses censored time — should be stated explicitly"** — Algorithm 1 clearly defines `I_cal^{(w)} = {i: W_i=w, e_i=1}` and computes `V_i^{(w)}` for those indices. The paper is sufficiently explicit. Removed.
- **"The clinical sample size is very small for weighted conformal prediction"** — the paper reports results over 10 independent trials with box plots, which partially addresses variance concerns. The concern is valid but speculative about what the "known" finite-sample behavior would be in this specific setting. Demoted to removed (minor concern).
- **"Coverage slightly below 90% in Setting 6 is described as 'remarkably close'"** — this is the authors' subjective characterization of their own results. Not a weakness. Removed.
- **"Discussion limitations without practical remedies"** — the Discussion is candid about limitations; listing remedies is a nice-to-have, not a flaw. Removed.
- **"LPB optimization — coverage guarantee needs to hold for chosen τ uniformly"** — retained as Minor weakness #2.
- **Missing appendix content (definitions, proofs)** — the parser strips these. Per hard rules, removed.

## Novel Insights

None beyond the paper's own contributions. The reviewer's identification of the derivation problems in Equation (1) -- specifically that step (ii) does not follow from the tower property and step (iii)'s inequality direction is backwards relative to basic probability -- constitutes a genuine methodological critique, but this is a flaw, not a novel insight about the subject matter.

## Suggestions

1. **Correct or restate the derivation in Equation (1).** If the appendix provides a correct justification, bring it into the main text with clear probability-theoretic steps. If the derivation is genuinely incorrect, the paper's central claim needs to be revised: either prove that the guarantee extends from `ℙ_{T(w)|X,e=1}` to `ℙ_{T(w)|X}` under additional conditions, or honestly state that the guarantee is for the conditional-on-no-censoring distribution.
2. **Clarify the real-data evaluation protocol.** Specify exactly how coverage is computed on censored test patients. If only uncensored patients are used, state this explicitly and discuss the selection bias.
3. **Define "Relative LPB" in the main text.**
4. **Add an oracle-weight ablation** to isolate the effect of weight estimation error from the conformal procedure itself.

## Score and Decision

Based on the verifiable issues in the main text -- particularly the flawed derivation in Equation (1) which is the foundation of the theoretical contribution, and the unaddressed gap between Theorem 4.1's guarantee and the paper's stated goal -- the paper in its current form does not support its central claims. The problem is well-motivated and the high-level approach is sensible, but the theoretical justification needs substantial correction before the paper can be accepted.

MY FINAL SCORE: <score>4.0</score>
MY FINAL DECISION: <decision>Reject</decision>