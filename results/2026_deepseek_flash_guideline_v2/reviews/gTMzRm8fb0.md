The calibration tool is unavailable due to missing data files. I will proceed with my own judgment calibrated against the ICLR scoring guidelines (1=strong reject, 3=reject, 4=borderline reject, 6=borderline accept, 8=accept, 10=strong accept).

Here is the final consolidated review:

---

## Summary

GoalRank proposes a "generator-only" (one-stage) ranking framework as an alternative to the two-stage Generator–Evaluator (G-E) paradigm. The paper provides: (i) a theoretical result (Theorem 1) showing that a sufficiently large single generator can achieve strictly smaller KL approximation error to the optimal ranking policy than any finite MG-E mixture; (ii) a group-relative optimization principle that constructs a reference policy from a biased reward model using within-group mean/variance normalization; and (iii) an instantiation called GoalRank evaluated on public benchmarks and via large-scale online A/B tests on a platform with >500M DAU.

## Strengths

- **Non-trivial theoretical expressiveness comparison.** Theorem 1 provides a formal bound contrasting the k-mixture $(\alpha,\beta)$-bounded policy space (Definition 2) against a larger generator-only class, proving strict inequality in KL approximation error that tends to zero as generator width grows. While the comparison is asymmetric in capacity (width $k\alpha + n$ vs. $\alpha$), the explicit characterization and convergence guarantee go beyond a generic universal-approximation claim.
- **Clean derivation from oracle to tractable loss.** Starting from the entropy-regularized oracle policy (Eq. 2), the paper constructs a practical surrogate $\pi^{\text{ref}}$ (Eq. 4) using only the mean and standard deviation of the biased reward within a group. The final training loss (Eq. 5) is a simple cross-entropy objective that follows from minimizing $\text{KL}(\pi_\theta \| \pi^*)$. The derivation chain is clearly laid out.
- **All baselines share the same reward model as GoalRank.** The paper states (line 236) that G-E and MG-E baselines use the same evaluator. This eliminates the confound that GoalRank's gains come from a better reward model, isolating the advantage to the architecture and training objective.
- **Credible large-scale online A/B test.** Table 4 reports statistically significant improvements across five business metrics (App Stay Time +0.149%, Watch Time +0.197%, Effective Views +1.212%, Like +0.227%, Comment +0.802%) with pure GoalRank vs. the production MG-E system. The hybrid setting (GoalRank + MG-E) has been deployed to full traffic (line 317), providing strong industrial validation.
- **Systematic ablations with robustness.** Table 2 shows performance across group sizes 3–100, with best results at 8–20 and graceful degradation at extremes. Table 3 shows robustness under injected Gaussian noise ($\lambda \in \{0.0, 0.2, 0.5\}$). Even at worst-case settings, GoalRank outperforms all baselines.

## Weaknesses

### Fatal

None.

### Major

- **Theorem 1's framing as a paradigm-level advantage is overstated.** The theorem compares a $k$-mixture of *bounded* generators (width $\leq \alpha$) against a *single larger* generator (width $\geq k\alpha + n$). The single generator is simply given more capacity — the result does not establish a structural or architectural superiority of the generator-only paradigm. If the MG-E system were allowed to scale each generator's width to $k\alpha + n$ as well, the claimed advantage would disappear. The paper's phrasing — "for any (finite Multi-)Generator–Evaluator model, there always exists a generator-only model that achieves strictly smaller approximation error" — is technically correct but implies a paradigm-level insight that the theorem does not actually deliver. This overclaiming runs through the abstract, introduction, and conclusion.

- **Offline evaluation likely suffers from exposure bias, making the large gains unreliable.** The ground-truth construction (Section 4.1.1) uses "the last six interactions in each user's historical sequence" as the target ranking. These interactions reflect what the user saw and clicked on under the platform's *existing* production ranking system (likely G-E-based). This introduces exposure bias: a model that better mimics the old system's output will appear to perform better on offline metrics, regardless of whether it produces genuinely better rankings. The magnitude of reported offline improvements — +17% to +47% on the Industry dataset (Table 1) — is far larger than the online improvements of 0.1%–1.2% (Table 4). While offline-to-online gaps are expected, a gap of this magnitude strongly suggests the offline protocol does not faithfully measure ranking quality.

- **The "evidence upper bound" claimed in the abstract and introduction is never derived in the main text.** The abstract and introduction (lines 9, 34) state that "by deriving an evidence upper bound of the existing optimization objective, we find that one can leverage a reward model..." However, Section 3.2 does not derive any evidence upper bound — it goes directly from the entropy-regularized oracle (Eq. 1–2) to the group-relative reference policy (Eq. 4) via the biased reward model. The claimed "evidence upper bound" is neither stated nor referenced in the main body. This creates a gap between the paper's stated contributions and what is actually presented.

### Minor

- **Threshold $\sigma^*$ in Equation 3 is undefined.** The paper conditions the validity of the group-relative approach on $\max_{l_i,l_j \in \mathcal{B}} |\hat{r}(l_i) - \hat{r}(l_j)| > \sigma^*$, but $\sigma^*$ is never defined, estimated, or given an order-of-magnitude. The derivation proceeds as though this condition is automatically satisfied. (The method demonstrably works in practice, so this is a theoretical-exposition gap rather than a practical flaw.)
- **No variance estimates in Table 1.** The paper reports t-test significance ($p < 0.05$) but does not provide standard deviations for the five-run averages. This makes it harder to assess the reliability of the reported gains.
- **Scaling experiment confounds model size with training data size.** The paper notes (footnote, line 292) that for very small models, training on the full dataset leads to unstable convergence, so data is proportionally subsampled for all models at the same parameter scale. This means the scaling curves in Figure 3 simultaneously vary model size and data quantity; baselines' flat scaling may partly reflect data insufficiency rather than a fundamental architectural limitation.
- **The auxiliary policy set $\mathcal{M}$ is opaque.** The construction of training groups $\mathcal{B}$ depends critically on $\mathcal{M}$ (heuristic methods and lightweight neural models), yet the paper provides no analysis of $\mathcal{M}$'s composition, the number of policies, their individual performance levels, or how sensitive GoalRank is to the choice of $\mathcal{M}$. Without this, a reader cannot assess how much of GoalRank's performance comes from the training objective vs. the quality of $\mathcal{M}$.

### Trivial

None.

## Nice-to-Haves

- An apples-to-apples scaling comparison where MG-E scales individual generator width (not just generator count) would strengthen the claim that the advantage is structural rather than about ensemble-size saturation.
- Runtime/latency comparisons (the paper mentions latency only in passing with a reference to an appendix figure) would strengthen the practical motivation.
- A discussion of how $\sigma^*$ could be set or why it can be ignored in practice would tighten the theoretical derivation.

## Removed Points

The following points from the inputs were removed with justifications:

- *"The proof is deferred to the appendix, so I cannot evaluate its correctness"* — Removed per the rule about missing appendix content (parser strips appendices from all papers).
- *"The KL divergence may not be well-defined without a smoothing assumption"* — Removed: softmax-based policies assign positive probability to all lists, so KL is well-defined.
- *"Baselines are somewhat dated"* — Removed: DNN (2016), DLCM (2018), PRM (2019) are standard baselines in the ranking literature; the paper also includes recent methods (RankMixer 2025, PIER 2023, NAR4Rec 2024).
- *"The evaluator-sharing statement is ambiguous"* — Removed: the paper states clearly (line 236) that "all baselines share exactly the same evaluator (reward model) as GoalRank" — this is unambiguous.
- *"Robustness ablation only tests three bias levels with Gaussian noise"* — Removed: three levels ($\lambda \in \{0.0, 0.2, 0.5\}$) with clear degradation is a standard ablation; Gaussian noise is a common first robustness test.
- *Formatting nitpicks and style complaints* — Removed per hard rules.
- *Generic concerns that could not be anchored to specific passages* — Removed as noise (e.g., "the evaluation lacks rigor" without concrete anchor points).

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. **Reframe Theorem 1.** Present it as a formal expressiveness comparison under capacity constraints rather than a "paradigm shift" — the comparison of a bounded mixture against a larger single generator is still a valuable theoretical motivation for scaling single generators.
2. **Address the offline evaluation's exposure bias.** Either (a) supplement with a de-biased evaluation protocol (e.g., using hand-annotated test sets or counterfactual estimators), or (b) clearly position the online A/B test (Table 4) as the primary evidence and acknowledge the offline results as potentially confounded.
3. **Either provide the "evidence upper bound" derivation in the main text or remove the claim.** The group-relative optimization principle is sufficiently interesting on its own; the reference to an "evidence upper bound" that is never shown creates an unnecessary credibility gap.
4. **Add standard deviations to Table 1** for the five-run averages.
5. **Analyze the auxiliary policy set $\mathcal{M}$.** Report the number of policies, their performance levels, and the sensitivity of GoalRank to the composition of $\mathcal{M}$.

## Score and Decision

The paper presents a practically useful training method with credible online deployment evidence. The group-relative optimization idea is clean and the online A/B test is well-designed. However, the paper's central claim — that it establishes a paradigm-level theoretical and practical advantage of generator-only over G-E ranking — is not supported by the evidence. Theorem 1 is a capacity comparison, not a structural advantage proof. The offline results are implausibly large and likely contaminated by exposure bias. A claimed "evidence upper bound" derivation is absent from the main text. The overall framing is significantly stronger than what the evidence and theory support. In its current form, the paper should be rejected, though a substantially revised version that tones down the claims, fixes the offline evaluation, and fills the exposition gaps could be a solid conference paper.

**MY FINAL SCORE:** <score>5.0</score>
**MY FINAL DECISION:** <decision>Reject</decision>