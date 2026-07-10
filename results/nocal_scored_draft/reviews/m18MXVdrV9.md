Here is the consolidated final review.

---

## Summary

INFO-SEDD proposes using discrete diffusion models (Continuous Time Markov Chains) to estimate KL divergences and mutual information directly on discrete data, avoiding the "embedding trick" that continuous neural MI estimators require. The method uses a clever absorbing-state construction to share a single score model across joint and marginal distributions, and is evaluated on synthetic benchmarks, text summarization model selection, and genomics (motif discovery, consistency tests). The empirical results are strong across all settings.

## Strengths

- **Well-motivated problem.** The paper targets a genuine and under-addressed gap — information-theoretic estimation for high-dimensional *discrete* data. The motivation is specific and well-grounded (Section 1, supported by Table 1, Figure 1, Figure 4 showing the "embedding trick" leads to systematic bias).

- **Clever use of absorbing-state CTMCs to share a score model.** The insight in Section 3 (Equation 6) that a single score model trained on the joint distribution can provide marginal scores via an absorbing-state construction is elegant and reduces computational overhead. This is a real engineering contribution over a naive implementation of Equation (5).

- **Strong synthetic benchmark design.** The synthetic experiments (Table 1) test a challenging regime (MI increasing from 10 to 50, dimensionality from 10 to 50) where variational estimators are known to fail due to the McAllester-Stratos sample complexity bound. INFO-SEDD achieves near-perfect estimates (e.g., 20.02 ± 0.21 for MI=20, D=20; 47.77 ± 1.18 for MI=50, D=50) with much tighter standard deviations than competitors, suggesting genuine stability rather than lucky runs.

- **Well-chosen real-world applications.** Text summarization (Section 4.2) and genomics (Section 4.3) are naturally discrete domains. The consistency tests using scrambling parameter ρ are a principled way to evaluate MI estimates when ground truth is unavailable, and the TATA-box motif discovery (Figure 5) is a nice qualitative demonstration.

## Weaknesses

### Fatal
None.

### Major

- **Equation (2) contains a genuine mathematical error that undermines the theoretical derivation.** The paper states:
  $$\text{KL}[p_0 \parallel q_0] = \mathbb{E}[\log(p_0/q_0)(X_T)] = \mathbb{E}[\log(p_T/q_T)(X_T)].$$
  This chain of equalities is incorrect:
  1. $\mathbb{E}[\log(p_0/q_0)(X_T)]$ is an expectation over $X_T \sim p_T$, not $X_0 \sim p_0$. This is *not* $\text{KL}[p_0 \parallel q_0] = \mathbb{E}_{x\sim p_0}[\log(p_0(x)/q_0(x))]$ unless $p_T = p_0$.
  2. $\mathbb{E}[\log(p_T/q_T)(X_T)] = \text{KL}[p_T \parallel q_T]$, not $\text{KL}[p_0 \parallel q_0]$. The data processing inequality gives $\text{KL}[p_T \parallel q_T] \leq \text{KL}[p_0 \parallel q_0]$, with strict inequality in general.
  3. The sentence after Equation (4) — "We omit the term $\mathbb{E}[\log(p_0/q_0)(X_0)]$, as both $p_0$ and $q_0$ converge to $\pi$" — is garbled (it should refer to $p_T, q_T$) and conceptually confused.

  The correct derivation via Dynkin's formula would give $\text{KL}[p_0 \parallel q_0] = \text{KL}[p_T \parallel q_T] - \mathbb{E}[\int_0^T (\partial f/\partial t + \mathcal{B}[f]) dt]$, and then the approximation $\text{KL}[p_T \parallel q_T] \approx 0$ for large $T$ justifies the estimator. The paper's Equation (2) bypasses this reasoning with an incorrect equality. While the estimator itself may well be correct (the empirical evidence suggests it is), the paper's claimed theoretical foundation as written is unsupported. A corrected derivation must be provided.

### Minor

- **Missing uncertainty quantification in Table 2.** The correlations between MI and human metrics are reported for only 15 summarization models without confidence intervals, p-values, or standard errors. For n=15, a 95% CI around the headline r=0.74 spans approximately [0.36, 0.91], making it difficult to judge signal strength.

- **No computational cost comparison despite "lightweight" claim.** The abstract calls INFO-SEDD "lightweight," but the paper never reports training time, inference time, or parameter counts vs. competitors. The statement that all methods use "$10^5$ samples and a batch size of 1024 for $10^5$ steps" compares training steps rather than wall-clock time and overlooks per-step cost differences.

- **No hyperparameter sensitivity analysis.** Performance may depend on the number of diffusion steps $T$, the schedule $\sigma(t)$, and the score model architecture. These are not discussed.

- **No dedicated limitations paragraph.** The paper would benefit from acknowledging regimes where INFO-SEDD might struggle (e.g., very small state spaces, very short sequences, settings where the absorbing-state construction introduces edge effects).

### Trivial
None.

## Nice-to-Haves

- Report bootstrap confidence intervals for the correlations in Table 2.
- Provide wall-clock time and parameter count comparisons.
- Add a hyperparameter sensitivity analysis (varying $T$, $\sigma(t)$, score model architecture).
- Include a limitations paragraph.

## Removed Points

These points are flagged for removal; treat them with caution:

- **"Asymmetric comparison with continuous baselines"** — Removed. The paper's central thesis is that the "embedding trick" harms performance; comparing against embedding-based methods *is* the correct test of this thesis. The paper also controls for backbone architecture. Missing discrete-native baselines (e.g., Pinchas et al. 2024) is not a gap because the paper explicitly notes these methods lose accuracy at high dimensionality.
- **"Classifier-based reference in genomics is approximate"** — Removed. The paper explicitly states this is an approximation ("we can approximate order-of-magnitude and slope").
- **"Synthetic data may align with CTMC assumptions"** — Removed. Speculative claim without evidence.
- **"Missing appendix/proofs"** — Removed. Parser artifact, not author omission.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

- **Fix the theoretical derivation.** Provide a corrected version starting from the Dynkin-based identity: $\text{KL}[p_0 \parallel q_0] = \text{KL}[p_T \parallel q_T] - \mathbb{E}[\int_0^T (\partial f/\partial t + \mathcal{B}[f]) dt]$, then argue $\text{KL}[p_T \parallel q_T] \to 0$ as $T \to \infty$ because both distributions converge to $\pi$. This preserves the estimator while correcting the mathematics.
- Add confidence intervals to the correlations in Table 2.
- Report wall-clock cost and parameter counts for all methods.
- Add a hyperparameter sensitivity analysis and a limitations paragraph.

## Score and Decision

MY FINAL SCORE: <score>6</score>
MY FINAL DECISION: <decision>Borderline Accept</decision>