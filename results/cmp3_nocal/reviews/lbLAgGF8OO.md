Now I have all the verification I need. Let me write the final consolidated review.

## Summary
This paper introduces Dig-DEC, a new model-free Decision-Estimation Coefficient that removes the optimism principle from prior work (optimistic E2D) and instead drives exploration purely through information gain (KL divergence + a divergence term $\overline{D}$). The paper generalizes the AIR framework to handle general divergences, provides an improved unbiased estimator for average estimation error, and applies the framework to both stochastic and hybrid MDPs (bandit feedback). Key claims include: (i) Dig-DEC ≤ optimistic DEC, with strict improvements in some cases, (ii) the first model-free regret bounds for hybrid MDPs with bandit feedback, and (iii) improved regret exponents over [FGQ+23].

## Strengths
- **Clean theoretical motivation for removing optimism (Section 4, Section 6).** The paper provides a clear rationale for why optimism-based exploration (as in [FGQ+23]) is not fundamental and why removing it opens the door to adversarial/hybrid settings where explicit reward estimators are unavailable. The decomposition of the KL term in Dig-DEC into regularization and information-gain components is conceptually elegant.
- **Generalization of the AIR framework (Eq. (2), Algorithm 1).** Replacing the KL-based divergence in AIR with a general divergence $D$, and connecting the analysis to mirror descent via Bregman divergences, is a genuine technical contribution that subsumes prior results ([XZ23, LWZ25]) as special cases while simplifying the analysis.
- **Unbiased estimator for average estimation error (Section 4.2.1).** The split-sample trick for constructing an unbiased estimator of the squared average Bellman error (using $\tau/2$ samples per split) is a clean improvement over the biased estimator in [FGQ+23].

## Weaknesses

### Major
- **Internal inconsistency in reported regret exponents between abstract, introduction, and Table 1.** The abstract (line 13) claims the off-policy average estimation error improves from $T^{5/6}$ to $T^{7/8}$. Since $T^{7/8} > T^{5/6}$ for $T > 1$, this is a *worsening*, not an improvement. Meanwhile, the introduction (line 33) describes the average-error improvement as $T^{3/2}/T^{5/8} = T^{7/8} \to T^{3/2}/T^{5/6} = T^{2/3}$, which is a genuine improvement but uses $T^{7/8}$ as the *old* bound. Table 1 reports the achieved regret as $T^{2/3}$ for all average-error cases. These three sources give three mutually inconsistent values for what the paper claims. A reader cannot determine what exponents are actually being claimed, and this undermines confidence in the paper's central quantitative results.
- **Claim of "sublinear regret" for hybrid MDPs contradicted by Table 2.** The introduction (line 32) states: "We establish the first sublinear regret for model-free learning in hybrid bilinear classes and Bellman-complete coverable MDPs." However, Table 2 shows that 4 out of 5 hybrid-setting entries have super-linear $T$-exponents ($T^{3/2}$ or $T^{13/8}$). These bounds grow faster than $T$ and are worse than the trivial $O(T)$ bound (since per-episode reward is bounded by 1). Only one entry (bilinear star off-policy with completeness) achieves $T^{1/2}$. The disconnect between the "sublinear regret" claim and the reported bounds is a serious credibility issue that must be resolved.

### Minor
- **Vacuous improvement claim for Est bound (line 213).** The paper states that the new estimator "improves their rate of Est from $\sqrt{T}$ to $T^{\frac{1}{2}}$." These are the same quantity, making the claim vacuous. This appears to be a typo, but as written it is confusing and reduces the paper's precision.
- **Lack of intuition for Theorem 14 (3-armed bandit example).** Theorem 14 claims a 3-armed bandit instance where Dig-DEC achieves $\max_a \mathbb{E}[\text{Reg}(a)] \leq 1$ while optimistic E2D suffers $\Omega(\sqrt{T})$. The proof is deferred to the appendix with no intuitive explanation in the main text of how $O(1)$ regret is possible. While this is an existence claim (not a universal bound) and the proof is provided in the appendix, providing at least a sketch of the construction's mechanism would substantially improve clarity and prevent the claim from appearing implausible on first reading.

### Trivial
- "ALR" appears in Eq. (8) where "AIR" is intended (a typo).

## Nice-to-Haves
- The derivation of hybrid-setting regret bounds (Table 2) could be clarified: the paper should explain whether the $T^{3/2}$ exponents arise from an optimal $\eta$ choice, or whether they reflect constraints that force suboptimal tuning. Currently a reader can verify that balancing the $T\cdot\text{dig-dec}$ and $\text{Est}/\eta$ terms optimally would yield a different $T$-dependence.
- A direct comparison table of assumptions required by prior hybrid-MDP work vs. this paper would help readers assess the novelty relative to [LWZ24, LZZ24, ZYW+24, LMWZ24].

## Removed Points
These points from the input review are not included in the final assessment:

- *"Key algorithmic details are entirely in the appendix, making the core contribution unverifiable from the main text"* — Removed because deferring algorithms, proofs, and technical lemmas to appendices is standard practice for theory papers at this venue.
- *"Toy example contradicts Lai-Robbins lower bounds"* — Removed because the critic's objection misunderstands Theorem 14 as a universal claim when it is an existence claim ("there exists a 3-armed bandit instance where..."). The Lai-Robbins lower bound does not apply to a specific constructed instance.
- *"The additive $\eta$ term in Theorem 13 clouds the picture"* — Removed because this is a standard feature of regret bounds with a tunable parameter; it is not a technical weakness.
- *"Missing related works / comparison to prior work"* — Removed per policy (the reviewer cannot verify existence of missing references).
- *All formatting/style nitpicks and appendix-deferred proof complaints* — Removed as parser artifacts or standard practice.

## Novel Insights
None beyond the paper's own contributions.

## Suggestions
1. **Resolve the exponent inconsistencies** between the abstract, introduction, and Table 1. Present a single, consistent set of "before and after" regret exponents with clear labeling of on-policy vs. off-policy and average vs. squared estimation error.
2. **Clarify the hybrid-setting bounds in Table 2.** Either explain why $T^{3/2}$ is the correct exponent (e.g., due to constraints on $\eta$), or correct the entries. If the bounds are indeed super-linear for most settings, the "sublinear regret" claim in the introduction must be qualified appropriately.
3. **Fix the vacuous Est claim** on line 213 and add a brief intuitive explanation for Theorem 14's construction in the main text.

## Score and Decision

MY FINAL SCORE: <score>4</score>
MY FINAL DECISION: <decision>Reject</decision>