## Summary

This paper proposes Dig-DEC, a new model-free Decision-Estimation Coefficient that replaces optimism-based exploration (used in prior work FGQ+23) with information-gain regularization via KL divergence. This conceptual shift enables handling hybrid MDPs (stochastic transitions + adversarial rewards) with bandit feedback, which optimism-based methods could not handle. The paper also refines the online function-estimation procedure with an unbiased split-sample estimator. Applications include regret bounds for bilinear classes, Bellman-Eluder dimension, and coverable MDPs.

## Strengths

1. **Clean conceptual advance: removing optimism.** The paper correctly identifies that FGQ+23's optimism mechanism requires explicit reward estimators, which breaks down in adversarial/hybrid settings with bandit feedback (Section 6, lines 303–307). Replacing optimism with a KL regularization term that drives exploration via information gain is well-motivated and directly enables handling hybrid MDPs. The decomposition of the KL term into regularization and information-gain components (lines 305–306) insightfully explains the dual role.

2. **Unbiased estimator for average estimation error.** The split-sample product estimator (Section 4.2.1, line 213) — $(\frac{2}{\tau}\sum_{i=1}^{\tau/2} \ell_h)(\frac{2}{\tau}\sum_{i=\tau/2+1}^{\tau} \ell_h)$ instead of FGQ+23's biased squared-average estimator — is a genuine technical improvement that eliminates bias and is likely of independent interest.

3. **Constant Est bound under squared error.** Theorem 11 achieves $\mathbb{E}[\text{Est}] \lesssim \log^2|\Phi|$ (constant in T) for Bellman-complete MDPs, which is the foundation for $\sqrt{T}$ regret results. This improves over FGQ+23's $T^{1/2}$ Est rate.

4. **Theorem 13: Dig-DEC ≤ optimistic DEC + η.** This establishes that Dig-DEC offers at least as good coverage as optimistic DEC in the stochastic setting, with the additive slack being at most the natural DEC parameter scale.

## Weaknesses

### Major

1. **Hybrid setting regret bounds in Table 2 are superlinear ($T^{3/2}$, $T^{13/8}$), contradicting the claimed "sublinear regret."** The paper's headline claim (line 32) states "the first sublinear regret for model-free learning in hybrid bilinear classes and Bellman-complete coverable MDPs." However, Table 2 reports regret bounds of $T^{3/2}$ (bilinear on-policy, bilinear star on-policy, coverable) and $T^{13/8}$ (bilinear off-policy). These grow faster than T — the average per-episode regret diverges. Only one entry (bilinear star off-policy with completeness, $T^{1/2}$) is sublinear. As printed, the table directly contradicts the central claim. Whether these are genuine results or formatting errors, the main text does not present reliable evidence for the hybrid contribution. The appendix (containing the derivations) is not available for verification.

2. **Internally inconsistent exponent claims across abstract, introduction, and Table 1, with an "improvement" going in the wrong direction.** The abstract (line 13) claims improvement "from $T^{\frac{5}{6}}$ to $T^{\frac{7}{8}}$ (off-policy)" — but $7/8 > 5/6$, so this is a worsening, not an improvement. The introduction (line 33) gives entirely different numbers: "improve the $T^{\frac{3}{2}}/T^{\frac{5}{8}}$ regret... to $T^{\frac{3}{2}}/T^{\frac{5}{6}}$" — where $T^{5/8} \to T^{5/6}$ is again a worsening. Table 1 shows $T^{2/3}$ for the average-error stochastic cases, matching neither the abstract nor the introduction. These are three different sets of numbers for what should be the same claimed result. This undermines confidence in the paper's quantitative claims.

### Minor

3. **Theorem 14's constant-regret-on-a-3-armed-bandit claim is unverifiable from the main text.** Theorem 14 (line 307) states constant regret ($\leq 1$) vs. $\Omega(\sqrt{T})$ for FGQ+23 on a constructed 3-armed bandit instance. Constant regret on a multi-armed bandit is far beyond standard results. While proofs in the appendix are standard for theory papers, the strength of this claim warrants at least a sketch of the construction in the main text so the reader can assess whether this is a genuine strict improvement or a pathological corner case.

### Trivial

None.

## Nice-to-Haves

- A brief discussion of when the saddle-point problem in Algorithm 1 simplifies (e.g., when the minimax has a closed form) would improve completeness. The paper is upfront about not addressing computational constraints (line 37), but even a brief remark would help readers gauge implementability.

## Removed Points

These points were removed from the inputs; treat with caution:

- **Computational intractability of Algorithm 1** (Harsh Critic Issue 4): The paper explicitly states (line 37) that "model-free" in this context does not imply computational constraints, and the scope is information-theoretic. This is a scope choice, not a flaw.
- **Theorem 14 proof location**: Demoted from major to minor. Proofs in appendices are standard for theory papers; the concern is about the strength of the claim itself, not the location of the proof.
- **Missing appendix proofs for Est analysis**: Removed per instructions — the appendix was stripped by the parser.
- **Missing comparison with LWZ25's results**: The paper includes qualitative discussion of this (Section 2.2). Removed as not central.

## Novel Insights

The harsh critic's observation that the exponent inconsistencies run deeper than a simple typo — the abstract claims an "improvement" from $T^{5/6}$ to $T^{7/8}$ that is actually a worsening, while the introduction and Table 1 each give different numbers — is a genuinely novel diagnostic. This is not a formatting artifact; it reveals that the paper's own stated results are unreliable across three separate locations. The superlinear hybrid bounds in Table 2 ($T^{3/2}$, $T^{13/8}$) directly contradict the "sublinear regret" headline claim, creating an evidential gap that prevents a reader from assessing the hybrid contribution without the (stripped) appendix.

## Suggestions

1. **Resolve the Table 2 exponents.** Either correct the entries to show genuinely sublinear rates with the correct exponents, or clearly state which hybrid settings achieve sublinear regret and which do not. The "first sublinear regret" claim must be accurately scoped.

2. **Reconcile the three different sets of exponent claims** (abstract, introduction, Table 1) for the stochastic setting. At most one set can be correct. The abstract's $T^{5/6} \to T^{7/8}$ "improvement" needs correction — it is currently a worsening.

3. **Include a brief sketch of the 3-armed bandit construction** for Theorem 14 in the main text, so the claim of strict improvement can be qualitatively assessed without consulting the appendix.

## Score and Decision

MY FINAL SCORE: <score>5.0</score>
MY FINAL DECISION: <decision>Reject</decision>