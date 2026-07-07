Now let me complete the final review.

## Summary

This paper studies the behavior of the Neural Tangent Kernel (NTK) for deep ReLU networks as depth $L\to\infty$ (with width growing faster than depth). The key tension it identifies is genuine: the normalized NTK $\bar\Theta_\infty^{(L)}$ converges entrywise to 1 (making the kernel matrix singular), yet the closed-form predictor $\kappa_x^\top \kappa^{-1}$ is claimed to converge to a well-defined limit. The paper derives a recurrence for the normalized kernel (Proposition 4, Theorem 2) and attempts to prove convergence of the predictor via rough differential equations (Theorem 3).

## Strengths

- **Identifies a genuinely interesting and under-explored tension.** The observation that the normalized NTK converges to the all-ones matrix (seemingly making it singular and useless for prediction) while the closed-form predictor nevertheless may approach a well-defined limit is non-trivial. Prior work (Xiao et al. 2020) explicitly required a decomposition into a constant matrix plus an invertible data-dependent part, which fails when the kernel approaches a singular limit.

- **Proposition 4 and Theorem 2 are cleanly stated and correctly derived** from the known NTK recurrence, providing a useful closed-form reformulation of the normalized kernel and establishing its convergence to 1.

- **The rough differential equations approach is technically creative.** Applying rough path theory to analyze the singularity of the NTK predictor is novel and, if carried through rigorously, could provide a clean resolution.

## Weaknesses

### Major

- **The proof of Theorem 3 (the paper's central result) has decisive gaps that prevent verification.** Specifically:
  **(a)** The quantity $\tilde\Theta_\infty^{(L)}$ is never defined. Definition 4 defines the *normalized* kernel $\bar\Theta_\infty^{(L)}$, but Theorem 3 and its proof exclusively use $\tilde\Theta_\infty^{(L)}$ without specifying whether these are the same object. For a theory paper whose main result depends on this quantity, this is a basic expositional failure.
  **(b)** The construction of the driving paths $v_{ij}^{(L)}$ is never given. The theorem asserts their existence, but the proof jumps into determinant inequalities without specifying what $v_{ij}^{(L)}$ is or how it relates to $A_n^{(L+1)}(t)$.
  **(c)** The application of the Lyons Universal Limit Theorem is asserted without verifying the required topology. The proof only notes pointwise convergence of $v_{ij}^{(L)}$ to 0, but the Universal Limit Theorem requires convergence in a $p$-variation or Hölder topology, which is never checked. The theorem is cited generically (Lyons 1998) without a specific statement or theorem number.
  **(d)** The determinant inequality chain (lines 220–222) is stated without justification. The first inequality relates $\det(A)$ to a weighted geometric mean of two determinants, which would require the log-concavity of the determinant on positive definite matrices — a fact not mentioned in the proof.
  **(e)** The initial condition $u(0)$ for the RDE is never specified. At $t=0$, $A(0)=\tilde\Theta_\infty^{(L)}(XX^\top)$ and $b(0)=\tilde\Theta_\infty^{(L+1)}(x^\top X^\top)$, giving $u(0)=(\tilde\Theta_\infty^{(L)})^{-1}\tilde\Theta_\infty^{(L+1)}$ with mixed superscripts, while the theorem's claimed expression uses only $(L)$. This mismatch is not addressed.
  **(f)** The limit is not characterized. The proof only shows $u_\infty'(t)=0$ (constant in $t$), but does not determine its value. The theorem's descriptive content ("bounded and dependent on $x$ and non-trivial") is too weak to constitute a substantive characterization of the role of depth.

  Taken together, these gaps mean **Theorem 3 is not proved in the submitted manuscript.** For a theory paper whose headline contribution is Theorem 3, this is a structural flaw.

- **The stereographic projection claim in Section 4, case (c), appears mathematically incorrect.** The paper states that after inverse stereographic projection to $S^{n_0}$, "the embedding of the datapoints satisfies $x_i^\top x_j = 1$ for all $x_i, x_j$ in the dataset." For points on the unit sphere, $x_i^\top x_j = 1$ iff $x_i = x_j$ (since $\|x_i-x_j\|^2 = 2-2x_i^\top x_j$), which would collapse all datapoints to a single point. Since this case is presented as one of three justifying settings for the analysis, it undermines the claimed generality. (Definition 7 is in the stripped appendix, but the main-text statement as written is clear and appears impossible.)

### Minor

- **The novelty relative to prior work is overstated.** Lemma 1 ($\rho^{(L)}\to 1$) and Theorem 2 (normalized kernel converges to 1) follow from known results in the mean-field theory and arc-cosine kernel literature (Cho & Saul 2009, Schoenholz et al. 2017, Poole et al. 2016). The paper's genuinely new claim is Theorem 3, whose proof is incomplete as argued above.

- **The experiments do not directly validate the predictor convergence claimed in Theorem 3.** Figure 1 shows convergence of $\rho$, $\eta$, and the normalized kernel entries — which follow from known recurrences — but the third column ($\bar\kappa^{(l)}(x^\top X^\top)(\bar\kappa^{(l)}(XX^\top))^{-1}$) is only shown on synthetic uniform data with no error bars, multiple seeds, or assessment of robustness to $n_0$, $n$, or data distribution.

- **The conclusion contains a self-contradiction:** "while convergence for the limiting kernel is sublinear, the convergence for the limiting kernel is experimentally fast" — the second "limiting kernel" should read "limiting solution," making the sentence as written contradictory.

### Trivial

- None.

## Nice-to-Haves

- The rough path theory framework may be unnecessarily heavy for what is essentially a limit of matrix-valued expressions; a direct analysis of the matrix sequence $(\tilde\Theta^{(L)}(XX^\top))^{-1}\tilde\Theta^{(L)}(x^\top X)$ would be more accessible and convincing.

- Characterizing the limit substantively (e.g., showing it depends only on class-conditional means or some low-dimensional statistic) would substantially strengthen the paper's contribution.

## Removed Points

These points from the input review were removed with justification:

- **"Determinant inequality direction appears backwards":** The reviewer claimed the paper's $\leq$ direction between middle and right fractions is backwards. This is incorrect: for $0<d<1$, $d^\psi \ge d$, making the middle denominator larger, so the middle fraction is *smaller*, consistent with $\le$. The lack of justification for the first inequality (left $\le$ middle) is retained in the Major weaknesses above.
- **"Proof sketch of Proposition 1 is incoherent":** The sketch is sparse but sufficient for a known result from the literature; this is a cosmetic issue at most.
- **Missing related works:** Removed per instruction (cannot independently verify existence of unread works).
- **"Missing appendix proofs":** The appendix is stripped by the parser; the original submission may contain them.
- **"Experiments lack statistical significance / variance":** Demoted to Minor, acknowledging the paper is primarily theoretical and the experiments are illustrative.
- **"Rough path theory is a heavy hammer":** A methodological opinion, not a concrete flaw.
- **"Section 6 properties list too vague":** The paper explicitly frames these as properties to check, not as a complete characterization; the criticism overreaches.

## Novel Insights

None beyond the paper's own contributions. The review reveals that the paper identifies a genuinely interesting open problem (the singularity of the NTK in the infinite-depth limit and the behavior of the predictor), but the proposed resolution via rough differential equations is not carried through to a verifiable proof.

## Suggestions

1. **Define $\tilde\Theta$ explicitly** or reconcile it with $\bar\Theta$.
2. **Complete the proof of Theorem 3** — either by fully specifying the rough path construction, verifying the topology required by the Lyons Universal Limit Theorem, and addressing the initial-condition mismatch, or by adopting a simpler direct analysis of the matrix sequence.
3. **Correct or remove the stereographic projection claim** in case (c) of Section 4.
4. **Characterize the limit substantively**, not just its existence.
5. **Add experiments that directly validate predictor convergence** with multiple random seeds, varying dataset sizes, and error bars.
6. **Fix the contradictory sentence** in the conclusion.

---

### Calibration Anchors

| Path | Avg Score | Round | Itemized | Comparison |
|------|-----------|-------|----------|------------|
| `nSDOkm0SKo.md` | 1.00 | R1 | No | Unrelated financial topic paper that was unanimously rejected |
| `Uj0h13lVrR.md` | 1.00 | R1 | No | GFlowNets paper, unanimously rejected — not topically similar |
| `2NwHLAffZZ.md` | 2.33 | R1/R2 | Yes | NTK linearization paper with severe presentation gaps (-10.95, -11.86). My paper has better motivation and cleaner auxiliary results, but comparable core proof incompleteness. |
| `YN4uWzcbtt.md` | 4.25 | R1/R2 | Yes | NTK positive definiteness paper with clean proofs but incremental contribution. My paper has a more interesting problem but worse proof quality. |
| `3LLkES6nNs.md` | 4.25 | R1 | No | Infinitely deep ResNets paper — mixed reviews, cleaner presentation |
| `kOtFuzoA93.md` | 4.00 | R2 | No | Kernel models beyond over-parameterized regime |
| `VEJzjAvaIy.md` | 5.75 | R1 | Yes | NTK divergence in classification — mixed reviews, some reviewers praised the result |
| `5EtSvYUU0v.md` | 6.00 | R1 | Yes | NTK-NNGP unification — strong positives for importance but large negative (-9.86) for "no verifiable proofs" |
| `AoraWUmpLU.md` | 8.00 | R1 | No | NTK+Neural ODEs, uniformly strong reviews |
| `4xWQS2z77v.md` | 8.00 | R1 | No | Regularized NN loss landscape, uniformly strong |

**Score range from Round 1 bracketing:** The paper sits between the 2.33 anchor (2NwHLAffZZ — severe presentation gaps + incomplete results) and the 4.25 anchors (YN4uWzcbtt — clean proofs but incremental contribution). The decisive factor is that the paper's central theorem (Theorem 3) is not in a verifiably proved state, which is a more damaging flaw than incremental contribution. However, the paper's motivation and auxiliary results (Proposition 4, Theorem 2) are stronger than the 2.33 anchor's. The weighted-item comparison shows shared heavy negatives: proof incompleteness (-8.89) and undefined notation (-5.96) are structurally similar to the 2NwHLAffZZ anchor's "unsupported statements" (-7.77) and "definitions missing" (-10.95). The paper lacks the strong positive (+6.37 for ambitious question) that the 2.33 anchor had, bringing it slightly below. The final score of **3.0** reflects that the paper identifies an interesting problem and has clean auxiliary results, but the central claimed contribution is unverifiable as presented.

MY FINAL SCORE: <score>3.0</score>
MY FINAL DECISION: <decision>Reject</decision>