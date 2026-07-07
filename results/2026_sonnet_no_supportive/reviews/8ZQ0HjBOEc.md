Now I have a thorough understanding of the paper. Let me draft the review.**Round 1 bracket: 3.5–5.5.** The paper sits between the rejected NTK-related papers at 3–4.25 (more incremental or incomplete) and the accepted papers at 5.75–6 (cleaner, complete results). The main weaknesses (Theorem 3 proves existence not characterization; proof gap; erroneous case (c)) place it below the 5.75 NTK divergence paper but above the 2.33 NTK linearization rejects. I'll narrow to **4.0** — borderline reject.

---

## Summary
The paper studies the behavior of the ReLU neural tangent kernel (NTK) of overparameterized fully-connected networks as depth $L \to \infty$ (with $L = o(\min_l n_l)$). Two main theoretical results are presented: (1) Theorem 2 / Proposition 4 show that the normalized kernel $\bar{\Theta}_\infty^{(L)}$ converges strictly and monotonically to the all-ones matrix, meaning the kernel becomes singular; (2) Theorem 3 shows that the NTK predictor weight vector $\kappa_x(\kappa_{XX})^{-1}$ nevertheless converges to a well-defined finite limit, even in the singular regime, using rough differential equation (RDE) machinery. The second result explicitly addresses a case that Xiao et al. (2020) could not handle.

## Strengths

- **Theorem 2 / Proposition 4**: The recursive formula in Proposition 4 and the strict monotone convergence proof (Theorem 2) provide a clean, closed-form analysis of the normalized NTK's behavior under increasing depth, sharpening the earlier qualitative observations of Seleznova & Kutyniok (2022).
- **Theorem 3 — conceptual decoupling**: The key insight that the kernel matrix $\kappa_{XX}$ becomes singular while the predictor ratio $\kappa_x\kappa^{-1}$ remains well-behaved is genuinely illuminating. The explicit identification of the limit as the standard basis vector $e_i$ when $x = x_i \in X$ provides a non-trivial anchor for the abstract existence result.
- **Creative proof technique**: Routing the matrix inversion problem through rough differential equations and applying the Lyons Universal Limit Theorem is non-standard and opens a potentially broader proof strategy for other deep kernels.

## Weaknesses

### Fatal
None.

### Major

- **Theorem 3 leaves the limiting predictor uncharacterized for test points $x \notin X$**: The paper's stated goal is to "characterize the corresponding limiting kernel" and to understand "the role of depth in the limiting kernel." Theorem 3 proves existence and establishes the upper bound $C(x)\mathbf{1}_n^\top$ and $L^2$-norm $\mathcal{O}(n)$, but for any test point $x \notin X$ the actual value of the limit is nowhere identified. The summary following the proof (Section 5) explicitly acknowledges this: "the limiting expression, is dependent on $x$ and non-trivial." The conclusion (Section 7) then claims "the convergence for the limiting kernel is experimentally fast" — but without knowing the limit, this is convergence to an empirically measured finite-depth value ($L=20$), not the true theoretical limit. For a theoretical paper whose central claim is characterization, proving existence without identification leaves the core question half-answered.

- **Unjustified step in the proof of Theorem 3**: The chain of inequalities (page 7, displayed chain following eq. (5)) replaces $\det(A_n^{(L+1)}(t))$ in the denominator with $\det(\tilde{\Theta}^{(L+1)})^{\psi_\mathcal{D}(2t-1)} \det(\tilde{\Theta}^{(L)})^{1-\psi_\mathcal{D}(2t-1)}$. This first step (establishing that the interpolated determinant is lower bounded by this geometric mean) requires log-convexity of $\det(\cdot)$ along the interpolation path $A_n^{(L+1)}(t)$. Log-convexity holds for positive-definite matrices along geodesics in PD space, but the interpolation here is controlled by $\psi_\mathcal{D}$ (not a geodesic), and no justification is provided. The paper's only explanation for the last inequality ("strictly positive determinants are all smaller than 1") accounts for the third step, not the critical first step.

### Minor

- **Case (c) invertibility claim is likely erroneous**: Section 4 states that the inverse stereographic projection onto $S^{n_0}$ ensures "the embedding of the datapoints satisfies $x_i^\top x_j = 1$ for all $x_i, x_j$ in the dataset." However, if all data points lie on the unit sphere and satisfy $x_i^\top x_j = 1$ pairwise, then $\|x_i - x_j\|^2 = 2 - 2x_i^\top x_j = 0$ for all $i \neq j$, meaning all points coincide—contradicting the distinctness assumption from Section 3. Footnote 2 does not resolve this.

- **Inconsistent notation $\bar{\Theta}$ vs $\tilde{\Theta}$**: Definition 4 introduces $\bar{\Theta}_\infty^{(L)}$ as the normalized kernel with explicit formula $\frac{n_0 2^{L-1} \Theta_\infty^{(L)}}{L}$. However, Theorem 3 and the surrounding proof use $\tilde{\Theta}_\infty^{(L)}$ throughout without defining this symbol or establishing its equivalence to $\bar{\Theta}_\infty^{(L)}$.

### Trivial
None beyond what is covered above.

## Nice-to-Haves

- Computing or explicitly bounding the limiting value of $\kappa_x\kappa^{-1}$ for $x \notin X$ would transform Theorem 3 from an existence result into a genuine characterization. One candidate approach: write $\bar{\kappa}^{(L)} = \mathbf{1}\mathbf{1}^\top + \epsilon^{(L)} M^{(L)}$ near $L \to \infty$ and apply Sherman-Morrison-Woodbury to $(\bar{\kappa}^{(L)})^{-1}$; if $M^{(L)}$ converges to a limit encoding first-layer correlations, the predictor weights could be expressed in terms of dataset geometry.
- The "small determinant implies fast convergence to the limiting solution" conjecture at the end of Section 6 should be explicitly flagged as a conjecture rather than presented as an observation.
- Lemma 1 (convergence of $\rho^{(L)} \to 1$) is foundational to Theorem 2 but is only given a brief sketch in the main text; a brief structural argument would increase confidence in this key ingredient.

## Removed Points
*These points are flagged to be removed; treat them with caution.*

- **"The appendix is missing / proofs cannot be verified"**: The harsh critic used this as additional justification for concerns. Per the review rules, appendix content is stripped in the reviewed version; this framing is removed. The underlying concern (unjustified proof step) is kept but only to the extent it is verifiable from the main text.
- **Generic claim that "experiments only go to L=20, not the true limit"**: Retained only as a minor point that the convergence is to an empirical proxy, since the true limit is uncharacterized—not as a standalone weakness.

## Novel Insights
The paper's most original contribution is not the convergence of the kernel per se (already known to be singular) but the conceptual separation of kernel singularity from predictor stability: proving that $\kappa_x\kappa^{-1}$ can have a well-defined limit even when $\kappa_{XX}$ degenerates is a mathematically non-trivial and practically meaningful observation. The RDE framework—used here to track a matrix inversion through a singularity—may be a transferable tool for analyzing other deep kernels (CNNs, skip-connection networks) facing similar singular limits.

## Suggestions
1. Resolve the notation conflict between $\bar{\Theta}$ and $\tilde{\Theta}$ by either unifying the two or providing an explicit cross-reference between Definitions 3–4 and Theorem 3.
2. Correct or carefully re-examine the case (c) invertibility claim: if the inverse stereographic projection forces $x_i^\top x_j = 1$ for all pairs, then distinct points cannot lie on the unit sphere simultaneously.
3. Add a short justification (or citation) for the log-convexity step in the Theorem 3 proof chain, or replace the interpolation argument with a bound that does not require log-convexity of $\det(A_n^{(L+1)}(t))$.
4. Explicitly label the "small determinant → fast convergence" hypothesis as a conjecture.
5. If feasible, attempt to identify the limit of $\kappa_x\kappa^{-1}$ for $x \notin X$, even for a simple two-point dataset, to ground Theorem 3's existence claim with an explicit example.

---

## Score and Decision

**Anchor papers retrieved:**

| Path | Avg Human Score | Round | Comparison |
|---|---|---|---|
| `2NwHLAffZZ.md` | 2.33 | R1 | NTK linearization via weak correlations — more speculative, rejected; weaker than this paper |
| `NbbsRnPBoS.md` | 2.33 | R1 | Depth in deep linear networks — rejected for incremental negative-then-positive depth analysis |
| `fUz6Qefe5z.md` | 3.00 | R1 | NTK with derivative labels — rejected; less technically creative |
| `KNQJtoPZmz.md` | 3.00 | R1 | Simplicity bias — not closely comparable |
| `YN4uWzcbtt.md` | 4.25 | R1 | NTK positive definiteness — rejected as incremental; similar theoretical depth but more complete proof |
| `3LLkES6nNs.md` | 4.25 | R1 | Infinitely deep ResNets → GP — similar depth-to-infinity analysis, comparable maturity |
| `kOtFuzoA93.md` | 4.00 | R1 | Novel kernel models beyond overparameterized regime — rejected; somewhat comparable theory paper |
| `WH9NhxOeu9.md` | 5.00 | R1 | Sharp generalization for overparameterized NN — rejected; more complete analysis |
| `VEJzjAvaIy.md` | 5.75 | R1 | NTK divergence in classification — accepted; cleaner result with full proof |
| `5EtSvYUU0v.md` | 6.00 | R1 | Connecting NTK and NNGP — accepted; complete unified framework |
| `8wAL9ywQNB.md` | 6.00 | R1 | Generalizability via expressive power — not closely comparable |
| `S04xvGXjEs.md` | 6.00 | R1 | NTK spectrum collective variables — empirical, not closely comparable |
| `AoraWUmpLU.md` | 8.00 | R1 | Neural ODEs with activation functions — more complete theoretical treatment |
| `4xWQS2z77v.md` | 8.00 | R1 | Loss landscape via convex duality — stronger, complete theoretical paper |

**Round 1 bracket: 3.5–5.5.**

The paper's creative use of RDE and the genuine insight of Theorem 3 place it above the 2.33–3.0 anchors (which have more fundamental issues). However, compared to accepted papers in the 5.75–6.0 range (NTK divergence, NTK/NNGP unification), those papers deliver complete, clean characterizations of their claimed limits. The central gap here—Theorem 3 proves existence but not identification of the limiting predictor for test points—is the precise weakness that separates this work from the 6-point band. The erroneous case (c) claim and the unjustified proof step further weigh against acceptance. The paper aligns most closely with the 4.0–4.25 anchors (`YN4uWzcbtt`, `3LLkES6nNs`, `kOtFuzoA93`): genuinely interesting theoretical work with real contributions (Theorem 2, creative RDE approach), but falling short of a complete characterization and containing verifiable gaps.

**Final score: 4.0 (borderline reject).**

MY FINAL SCORE: <score>4.0</score>
MY FINAL DECISION: <decision>Reject</decision>