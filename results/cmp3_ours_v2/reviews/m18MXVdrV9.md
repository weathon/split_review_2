## Summary

INFO-SEDD proposes using score functions from discrete diffusion models (absorbing-state CTMCs) to estimate KL divergence and mutual information for high-dimensional discrete data, avoiding the "embedding trick" of projecting discrete data into continuous space. Two variants are introduced: joint (INFO-SEDD-J) and conditional (INFO-SEDD-C). The paper presents synthetic experiments with ground-truth MI, consistency tests on text summarization and genomics data, and a model selection application.

## Strengths

**1. Addresses a genuine and underserved problem.** High-dimensional discrete MI estimation is difficult — the standard "embedding trick" is heuristic and lacks guarantees. A native discrete method fills a real gap. This is the paper's strongest motivation.

**2. Strong synthetic results (Table 1).** At MI=10/D=10, INFO-SEDD estimates 9.92±0.12 (true: 10); at MI=50/D=50, it estimates 47.77±1.18. Competitors degrade severely — GAN-DIME drops to 17.27, HD-DIME collapses to 10.47, and MINE/NWJ/SMILE all produce far lower estimates. This is the paper's most compelling evidence.

**3. Clever marginal score recovery (Equation 6).** The observation that an absorbing-state CTMC allows marginal scores to be derived from a single joint-score model is non-trivial and practically valuable. It eliminates the need for separate score networks for marginal distributions.

**4. Pretrained model integration.** Fine-tuning existing discrete diffusion models (MDLM-SMALL, CADUCEUS) rather than training from scratch is a practical advantage.

**5. Model selection application (Table 2).** INFO-SEDD-C achieves Pearson r=0.740 with consistency, far above any competitor (next best HD-DIME at 0.331), demonstrating practical utility for an important downstream task.

## Weaknesses

### Fatal
None.

### Major

**1. The theoretical derivation in Section 2.2 (Equations 2–5) is not properly justified in the main text.**

Equation (2) asserts:

$$\text{KL}[p_0\|q_0] = \mathbb{E}[\log(p_0/q_0)(X_T)] = \mathbb{E}[\log(p_T/q_T)(X_T)]$$

Two unjustified claims are made here:

- **First equality:** $\text{KL}[p_0\|q_0] = \mathbb{E}_{X_T\sim p_T}[\log(p_0/q_0)(X_T)]$ — the KL is defined as $\mathbb{E}_{X_0\sim p_0}[\log(p_0/q_0)(X_0)]$, an expectation under the *initial* distribution. Replacing $X_0$ with $X_T$ changes the averaging distribution, and no justification is provided.

- **Second equality:** $\mathbb{E}[\log(p_0/q_0)(X_T)] = \mathbb{E}[\log(p_T/q_T)(X_T)]$ — this would require $p_0/q_0 = p_T/q_T$ pointwise, which does not generally hold. For an absorbing-state CTMC, $p_T$ and $q_T$ both converge to the same reference $\pi$, so $\log(p_T/q_T) \to 0$ while $\text{KL}[p_0\|q_0] > 0$.

The sentence "We omit the term $\mathbb{E}[\log(p_0/q_0)(X_0)]$, as both $\vec{p}_0$ and $\vec{q}_0$ converge to $\pi$" compounds the confusion: $\vec{p}_0$ and $\vec{q}_0$ are the *initial* distributions (they do not converge), and $\mathbb{E}[\log(p_0/q_0)(X_0)]$ is precisely the KL being estimated, so omitting it is circular.

The paper states the full derivation is in Appendix A.3/E (stripped). This may be a presentation artifact rather than a mathematical error — the approach is analogous to continuous diffusion MI estimation (Girsanov-based) whose foundations are well established. However, **as presented in the main text, a reader cannot verify the mathematical foundation of the method.** For a new-method paper, this is a significant deficiency. The strong synthetic results provide empirical support but cannot substitute for a sound, verifiable derivation.

### Minor

**2. Missing dedicated discrete MI baselines.** The paper compares only against continuous estimators applied via the embedding trick. The claim that classical discrete estimators (NSB, Miller-Madow, etc.) "rapidly decrease with increasing data dimensionality" is asserted but not tested directly. Including at least one discrete-specific baseline would substantiate this claim and strengthen the "our method vs. embedding methods" comparison.

**3. No computational cost comparison.** The paper claims INFO-SEDD is "lightweight and scalable" but provides no runtime or compute comparison. Training a discrete diffusion backbone is computationally expensive; the paper should report how total cost compares to embedding+neural-estimator pipelines.

**4. Real-world tests are consistency checks, not ground-truth validation.** The text "reference" MI (256–303 nats) relies on entropy rate estimates from different corpora. The genomics reference uses classifier accuracy, itself an estimate with unknown variance. The paper explicitly calls these "consistency tests," which is honest, but the claims about outperforming competitors on real data would be stronger with a setting providing known ground-truth MI.

**5. Kendall's Tau discrepancy (Table 2).** INFO-SEDD-C achieves Pearson r=0.740 vs. next-best 0.331, but Kendall's Tau is 0.505 vs. KL-DIME's 0.429 — a much smaller gap. The paper should discuss this, as it suggests the Pearson advantage may be driven by outliers or a nonlinear relationship.

### Trivial

**6. No limitations paragraph.** The conclusion does not discuss sensitivity to the diffusion horizon $T$, the rate schedule $\sigma(t)$, the looseness of the error bound (Equation 7: scales with $D|\chi|\bar{\sigma}(T)$, which could be large), or scenarios where INFO-SEDD might fail.

## Nice-to-Haves

- Report $|\chi|$ explicitly for Table 1 in the main text.
- State the $O(D\cdot|\chi|)$ complexity of the Monte Carlo estimate explicitly.
- Include a sensitivity analysis for $T$ and $\sigma(t)$.
- Add a runtime comparison figure.

## Removed Points

- **"Structural/fatal derivation flaw" (harsh critic):** Demoted to Major. The empirical validation (Table 1, known ground truth) provides strong evidence the method computes the correct quantity. The issue appears to be compressed/poor presentation in the main text, not a genuine mathematical error — the appendix likely contains the complete derivation.
- **"Baseline comparison asymmetry":** The "our method vs. embedding methods" framing is fair and acknowledged. The missing discrete baselines point (Minor #2) is valid, but the asymmetry claim is overstated. Removed.
- **"Consistency tests don't validate accuracy":** The paper explicitly frames these as consistency tests. The model selection correlation (Table 2) provides a separate real-world validation. Downweighted to Minor #4.
- Several section-by-section notes that are minor observations or nitpicks.

## Novel Insights

The harsh critic's analysis of the derivation gap in Section 2.2 (Equations 2–5) is the most valuable critical insight. The presentation of Equation (2) as a chain of unjustified equalities, combined with the confused statement about omitting $\mathbb{E}[\log(p_0/q_0)(X_0)]$, genuinely undermines a reader's ability to verify the mathematical foundation from the main text. A strength-side insight worth highlighting is that the absorbing-state marginal score recovery (Equation 6) is a genuine methodological contribution that solves a practical bottleneck that would otherwise require separate training of joint and marginal score networks.

## Suggestions

1. **Rewrite Section 2.2.** Show the application of Dynkin's formula step by step. State explicitly that $\mathbb{E}[\log(p_T/q_T)(X_T)] \to 0$ as $T\to\infty$ (since $p_T,q_T\to\pi$), so the KL reduces to the path integral term. Fix the $\vec{p}_0$/$\vec{p}_T$ confusion. Provide a complete logical chain in the main text.
2. **Include at least one discrete-specific baseline** (NSB estimator, Miller-Madow, or plug-in with correction).
3. **Add a limitations paragraph** discussing sensitivity to $T$, $\sigma(t)$, computational cost, error bound looseness, and failure modes.
4. **Report wall-clock or compute comparison** against competitors.
5. **Discuss the Pearson vs. Kendall's Tau gap** in Table 2.

## Score and Decision

**Round 1 bracket:** 4.0–6.0 (based on calibration against MINDE [6.50, Accept], Discrete Copula Diffusion [5.25, Accept], f-DIME [5.60, Reject], and Normalizing Flows MI [4.83, Reject]).

**Narrowing:** Compared to MINDE (6.50, Accept), which estimates continuous MI via diffusion with a clearer theoretical foundation (Girsanov theorem) and more thorough experiments, INFO-SEDD addresses the harder discrete setting but has a less clear theoretical derivation in the main text. Compared to f-DIME (5.60, Reject), INFO-SEDD has stronger synthetic validation. The paper sits between these anchors.

**Calibration anchors retrieved:**
- MINDE (0kWd8SJq8d, avg 6.50, Accept): Continuous diffusion MI estimation. Clearer theory, similar experimental paradigm. INFO-SEDD ≈ 1–1.5 pts below due to unclear derivation.
- Discrete Copula Diffusion (FXw0okNcOb, avg 5.25, Accept): Discrete diffusion paper (generation, not estimation). Accepted with concerns about approximations and computation. Similar quality level to INFO-SEDD.
- f-DIME (KC2MViQASx, avg 5.60, Reject): Discriminative MI estimation. Rejected despite 5.60 due to concerns about claims and experiments. INFO-SEDD has stronger empirical results.
- Normalizing Flows MI (vgQmK5HHfz, avg 4.83, Reject): MI estimation via flows. Rejected. INFO-SEDD has more convincing synthetic results.
- Discrete Diffusion Convergence (pq1WUegkza, avg 7.00, Accept): Theoretical discrete diffusion paper. Better-received due to clear theoretical contribution.

MY FINAL SCORE: <score>5.0</score>
MY FINAL DECISION: <decision>Reject</decision>