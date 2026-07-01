Now I have verified all the critic's claims against the paper. Let me write the final consolidated review.

---

## Summary

This paper introduces INFO-SEDD, a method for estimating mutual information (MI), KL divergence, and entropy on high-dimensional discrete data using score functions from discrete diffusion models (Continuous Time Markov Chains). It leverages Dynkin's formula and the absorbing-state construction to derive estimators that require training only a single diffusion model on the joint distribution — the marginal scores needed for INFO-SEDD-J (joint) follow automatically (Eq. 6). The method is validated on synthetic benchmarks with known ground truth, on text summarization (model selection via MI–human metric correlation), and on genomics (motif discovery via MI profiling).

## Strengths

1. **Novel and well-motivated approach.** The paper identifies a genuine gap — existing diffusion-based MI estimators (Kong et al., 2022; Franzese et al., 2023a) target continuous data, while the "embedding trick" for discrete data has known limitations (Section 1). Extending the CTMC score framework to discrete MI estimation is a non-obvious and timely contribution.

2. **Compelling synthetic results (Table 1).** INFO-SEDD recovers ground-truth MI values ranging from 10 to 50 at dimensionalities 10–50 with consistently lower bias and dramatically lower variance than all competitors (e.g., 20.02±0.21 vs. 22.09±1.75 for the next best at MI=20, D=20). The gap widens at higher MI/D, where competing methods degrade sharply.

3. **Elegant theoretical observation (Eq. 6).** The absorbing-state CTMC construction allows computing marginal scores from a single model trained only on the joint distribution, bypassing the need for separate score models for each marginal. This is a genuine practical advantage over naive application of Eq. (5).

4. **Meaningful real-world validation.** The TATA-BOX motif discovery experiment (Figure 5) provides a qualitative yet compelling demonstration — the MI profile correctly peaks in the known motif region (−39 to −26 relative to TSS), showing that INFO-SEDD can localize biologically meaningful signals. The model selection experiment (Table 2) further demonstrates practical utility by showing alignment with human consistency judgments.

## Weaknesses

### Fatal
None.

### Major

1. **The derivation in the main text (Equation 2 and surrounding explanation) is mathematically confused as presented.** The first claimed equality, $\text{KL}[\vec{p}_0\parallel\vec{q}_0] = \mathbb{E}[\log\frac{\vec{p}_0}{\vec{q}_0}(\vec{X}_T)]$, is not generally true: the left side is $\mathbb{E}_{x\sim\vec{p}_0}[\log(\vec{p}_0/\vec{q}_0)(x)]$, while the right side (marginalizing over $\vec{X}_T\sim\vec{p}_T$) is $\mathbb{E}_{x\sim\vec{p}_T}[\log(\vec{p}_0/\vec{q}_0)(x)]$, and these are not equal without further justification. The second equality, $\mathbb{E}[\log\frac{\vec{p}_0}{\vec{q}_0}(\vec{X}_T)] = \mathbb{E}[\log\frac{\vec{p}_T}{\vec{q}_T}(\vec{X}_T)]$, is stated without proof. Furthermore, the sentence "We omit the term $\mathbb{E}[\log\frac{\vec{p}_0}{\vec{q}_0}(\vec{X}_0)]$, as both $\vec{p}_0$ and $\vec{q}_0$ converge to $\pi$" (line 59) is doubly problematic: (i) $\mathbb{E}[\log(\vec{p}_0/\vec{q}_0)(\vec{X}_0)]$ is precisely the KL divergence being estimated, not a term to omit, and (ii) $\vec{p}_0,\vec{q}_0$ are the *initial* distributions and do not "converge to $\pi$" — it is $\vec{p}_T,\vec{q}_T$ that converge to the stationary distribution. The correct approach (applying Dynkin's formula to $\log(\vec{p}_t/\vec{q}_t)$ and using the fact that $\mathbb{E}[\log(\vec{p}_T/\vec{q}_T)] \approx 0$ for large $T$) is standard, but its garbled presentation makes the main text  misleading. Since the appendix (which is stripped from the review copy) may contain a correct derivation, this does not necessarily invalidate the method, but the main text must be corrected before publication. *Why it matters:* The theoretical foundation of the estimator is not reliably communicated, which undermines reader confidence even if the empirical results are strong.

### Minor

2. **The theoretical error bound (Eq. 7) scales as $D|\chi|$, which may be loose for realistic vocabulary sizes.** The bound contains the factor $D|\chi|(\epsilon_p+\epsilon_q)$. For the text experiments with a vocabulary of thousands and sequence length $D$, this product can reach $10^6$–$10^7$, requiring score errors $\epsilon$ on the order of $10^{-6}$ for a non-vacuous bound. The paper does not report empirical estimates of $\epsilon_p,\epsilon_q$ or discuss when the bound becomes informative. This does not undercut the empirical results (which are strong), but it means the stated theoretical guarantee is weaker than suggested.

3. **Computational cost is not reported.** The paper describes INFO-SEDD as "efficient" and "lightweight" but provides no measured training times, inference costs, or parameter counts for any method. Training discrete diffusion models (SEDD/MDLM/CADUCEUS) is substantially more expensive than training the MLP-based competitors (MINE, NWJ, F-DIME). A practitioner evaluating this tool needs to know the cost–accuracy trade-off. *Why it matters:* For a paper positioning itself as providing a practical "tool," the absence of runtime comparison is a notable omission.

4. **Model selection evaluation lacks statistical significance reporting.** The headline result (INFO-SEDD-C vs. consistency, Pearson $r=0.740$, Kendall's $\tau=0.505$) is reported over only 15 data points (models), but no $p$-values or confidence intervals are given for the correlations. While the GP regression with 95% CI (Figures 2–3) provides some visualization, a reader cannot assess whether the observed correlations could arise by chance. *Why it matters:* Model selection recommendations based on small-sample correlations need uncertainty quantification.

5. **No empirical analysis of sensitivity to the time horizon $T$ or the noise schedule $\sigma(t)$.** The bound in Eq. (7) involves a truncation bias that depends on $T$, but no ablation studies examine how these hyperparameters affect estimation accuracy. This makes it harder for practitioners to apply the method to new domains.

### Trivial

6. **Notation $s_b^p(\vec{X}_t)_x$ is unclear.** The sub/superscripts $b$ and $p$ are not explicitly defined, and $(\vec{X}_t)_x$ is potentially confusable with component indexing.

## Nice-to-Haves

- **Report backbone architecture for synthetic experiments.** The paper states "same backbone" (with details in Appendix C.1, which is stripped). Specifying this in the main text would allow readers to assess comparison fairness directly.
- **Rank-based model selection evaluation.** Beyond Kendall's $\tau$, reporting what fraction of pairwise model comparisons the MI ranking gets correct relative to human rankings would be more actionable for practitioners.
- **Discussion of failure modes.** The paper could usefully discuss settings where INFO-SEDD might break down (e.g., very small supports, extremely long sequences, or distributions far from the stationary distribution).

## Removed Points

*These points were identified in the source review but are removed for the following reasons:*

- **Critique that Equation (2) issue is "fatal/structural" and collapses the paper:** Demoted to Major because (a) the underlying Dynkin-based approach is standard and the estimator (Eq. 4) is independently validated by strong empirical results, (b) the appendix (stripped from review copy) likely contains a correct derivation, and (c) the error is in the *presentation* of the derivation, not in the final estimator itself. A presentation error, even a significant one, does not constitute a fatal methodological flaw when the empirical evidence supports the claims.
- **Criticism about "embedding trick" framing being overstated:** The paper's claim about being "unique" (Conclusion) is standard rhetorical practice and the paper clearly builds on prior work. This is not a meaningful weakness.
- **Criticism that backbone architecture is unknown/unfair:** The paper explicitly states "We use the same backbone for all methods (see Appendix C.1)" and "We use the MDLM-SMALL model... as the backbone, with minimal changes to the architecture to accommodate our competitors." Details are in the (stripped) appendix. The critic's speculation about architectural advantage is not grounded in what the paper actually says.
- **Criticism about conflating entropy with MI in the consistency test:** The paper uses entropy rate × length as an *order-of-magnitude* upper bound for MI (since $I(X,Y) \leq H(Y)$), which is a reasonable approximation and is appropriately caveated.
- **Critique about Kendall's $\tau = 0.505$ not being significant:** With $n=15$, the critical value for Kendall's $\tau$ at $\alpha=0.05$ (two-tailed) is approximately 0.39, so 0.505 would be statistically significant. The lack of reported $p$-values is the real issue (kept as Minor weakness 4).
- **Pure speculation about method failure modes in extreme regimes:** This is a nice-to-have, not a weakness.
- **Section-by-section notes that are purely observational or subjective** (e.g., "the CTMC background is competently summarized but quite dense"): These do not constitute actionable weaknesses.

## Novel Insights

The most striking observation from the harsh review is that the paper's mathematical derivation in the main text (Eq. 2) is genuinely confused — it claims $\text{KL}[\vec{p}_0\parallel\vec{q}_0] = \mathbb{E}[\log(\vec{p}_0/\vec{q}_0)(\vec{X}_T)]$, which swaps the initial expectation distribution ($\vec{p}_0$) with the terminal one ($\vec{p}_T$), and then confusingly says it "omits" the term $\mathbb{E}[\log(\vec{p}_0/\vec{q}_0)(\vec{X}_0)]$ (which is the KL itself) because "$\vec{p}_0$ converges to $\pi$" (when it should be $\vec{p}_T$). The correct Dynkin-based derivation can be reconstructed (see Major weakness 1), but the text as written would mislead a careful reader. This is surprising because the empirical work is clearly competent — the synthetic experiments are well-designed and the genomics application is creative. The disconnect suggests the mathematical presentation was rushed or carelessly checked, not that the method is unsound. Fixing this is the single highest-priority revision; once corrected, the paper would be significantly stronger than its current presentation suggests.

## Suggestions

1. **Rewrite Section 2.2 with a clean derivation.** Start from Dynkin's formula applied to $f(\vec{X}_t, t) = \log(\vec{p}_t/\vec{q}_t)(\vec{X}_t)$, show that $\mathbb{E}[f(\vec{X}_T,T)] - \text{KL}[\vec{p}_0\parallel\vec{q}_0] = \mathbb{E}[\int_0^T (\partial_t + \mathcal{B})f(\vec{X}_t,t)dt]$, then argue that $\mathbb{E}[f(\vec{X}_T,T)] \to 0$ as $\vec{p}_T, \vec{q}_T \to \pi$, leaving the integral as the estimator. Correct all instances where $\vec{p}_0$ is confused with $\vec{p}_T$.

2. **Add a computational cost table** reporting training time (or steps), parameter count, and approximate inference FLOPs for INFO-SEDD and each competitor across all experiment settings.

3. **Report $p$-values or bootstrap confidence intervals** for the correlations in Table 2.

4. **Add a brief ablation study** of the time horizon $T$ and noise schedule $\sigma(t)$ on the synthetic benchmark to help practitioners set these hyperparameters.

## Score and Decision

<score>6</score>
<decision>Accept</decision>

MY FINAL SCORE: <score>6</score>
MY FINAL DECISION: <decision>Accept</decision>