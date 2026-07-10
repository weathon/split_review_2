Now I have all the information needed. Let me write the final review.

## Summary

This paper addresses Geodesic PCA (GPCA) in the Wasserstein space of probability measures. It makes two main contributions: (1) a mathematically rigorous derivation of exact GPCA for centered Gaussian distributions, lifting the problem to $GL_d$ via the Bures-Wasserstein quotient geometry (Propositions 3–5); and (2) GPCAGEN, a neural-network-based method for GPCA on general absolutely continuous measures using Otto's parametrization of Wasserstein geodesics to avoid input-convex neural networks.

## Strengths

- **Mathematically principled derivation of Gaussian GPCA (Section 3).** The lifting to $GL_d$ via the Bures-Wasserstein quotient geometry is elegantly executed and correct. Proposition 3 cleanly reformulates the geodesic search and Bures-Wasserstein distances into a Frobenius-norm optimization over horizontal line segments, with the clipping operator $p_{A,X}$ properly handling finite-time validity of geodesics. **[impact=+9.98]**

- **Proposition 4 provides a concrete, computable measure of TPCA distortion.** Eq. (14) quantifies exactly when the linearized approximation breaks down—when $|a-b|/(a+b)$ is close to 1, i.e., near the boundary of the SPD cone—going beyond hand-waving about curvature. **[impact=+9.98]**

- **Proposition 5 establishes a non-trivial theoretical consistency result:** for univariate Gaussians, GPCA restricted to the Gaussian submanifold coincides with GPCA in the full space of a.c. distributions. **[impact=+9.80]**

- **Clever parametrization of geodesics without ICNNs (Section 4).** The paper exploits Otto's formulation to parametrize Wasserstein geodesics via $\nabla f$ with a *non-convex* $f$, avoiding the architectural constraints of input-convex neural networks. The trade-off (Hessian eigenvalue monitoring) is honestly stated. **[impact=+4.25]**

- **Honest discussion of limitations (Section 5.1 and Discussion).** The paper candidly reports that GPCA and TPCA differ by <1% on average for random Gaussian data, and admits that in the pathological example where they differ substantially, GPCA "may be seen as worse-behaved" than TPCA. This candor is valuable. **[impact=+1.43]**

## Weaknesses

### Major

- **GPCAGEN has no quantitative evaluation of any kind.** Section 5.2 presents only qualitative visual inspection: MNIST interpolations (Figure 5), subjective interpretations of 3D point cloud components ("captures distinction between hanging lamps and standing lamps"), and subjective interpretations of landscape image components ("captures variations in overall brightness"). There is no reconstruction error, no projection residual, no explained variance, no ground-truth recovery metric, and no loss curve. The paper's central claim that GPCAGEN "fill[s] the gap" for exact GPCA on a.c. measures is not supported by quantitative evidence. The MNIST experiment—where the authors construct data with known geodesic structure and report that GPCAGEN recovers geodesics that *look* like the known modes—is at best a sanity check; it does not demonstrate that the method finds the *optimal* geodesics or that the identified components are actually principal. This is a decisive weakness because a method presented as solving a well-defined optimization problem (Eq. 1) must be shown, quantitatively, to produce solutions that minimize that objective. **[impact=-10.00]**

### Minor

- **The Gaussian GPCA experiments partially undermine the paper's motivation.** Section 5.1 shows that GPCA and TPCA differ by <1% on average for random Gaussian data, and in the setting where they differ substantially (same eigenvalues, different orientations), GPCA is described as "worse-behaved." This undercuts the motivating narrative that TPCA's linearization induces meaningful distortion that GPCA corrects. The paper acknowledges this but does not fully grapple with its implications for why GPCAGEN is needed for non-Gaussian measures. **[impact=-0.07]**

- **No ablation or sensitivity analysis for GPCAGEN's regularization parameters.** The regularization coefficients $\lambda_I$ and $\lambda_O$ are set to 1.0 across *all* experiments with no sensitivity study. No convergence curves are shown. For a method with this many moving parts (two MLPs per component, Sinkhorn divergences, Hessian eigenvalue monitoring, soft intersection and orthogonality constraints), it is hard to assess optimization reliability or whether the constraints are actually satisfied at convergence. **[impact=-0.00]**

- **Compact support assumption vs. Gaussian reference measure.** The Otto-Wasserstein construction (Section 2) explicitly assumes distributions supported on a compact set $\Omega \subset \mathbb{R}^d$, but the experiments use the standard Gaussian $\mathcal{N}(0, I)$ as the reference measure $\rho$, which is not compactly supported. The paper does not discuss whether this mismatch is a practical concern. **[impact=-0.00]**

## Nice-to-Haves

- Report the GPCAGEN objective value (Eq. 15) after convergence, normalized by total $W_2^2$ variance, as an explained-variance-type metric.
- Provide convergence curves for GPCAGEN training and report final orthogonality violation / intersection distance for the second component.
- Discuss computational cost (training time, memory for Hessian computation).

## Removed Points

These points are flagged to be removed, treat them with caution:

- **"GPCAGEN is not exact because it uses Sinkhorn divergences"** — The paper qualifies its claim (p. 2: "our methods are exact in the sense that they do not rely on a linearization"), which is a correct qualifier. The Sinkhorn approximation is a practical implementation choice, not a methodological flaw in the exactness claim as stated. REMOVED.

- **"Hessian eigenvalue estimation from minibatches is underspecified"** — The paper describes the estimation procedure (Algorithm 1, line 5) and references theoretical bounds in the appendix (stripped by parser). REMOVED as a parser artifact issue.

- **"Missing computational cost discussion"** — Reasonable suggestion but not a methodological weakness. MOVED to Nice-to-Haves.

- **"Missing convergence curves is a basic hygiene failure"** — The paper is primarily a geometric method paper, not an optimization paper per se. Convergence curves would be helpful but the criticism is overstated. MOVED to Suggestions/Nice-to-Haves.

- **"Missing comparison with PCA on latent codes for MNIST"** — Valid as a suggestion for improvement but not a decisive weakness. MOVED to Suggestions.

## Novel Insights

None beyond the paper's own contributions. The review process surfaces a tension between the paper's two halves: the Gaussian GPCA derivation is mathematically rigorous and honestly evaluated (finding GPCA offers marginal benefit over TPCA), while GPCAGEN is presented as the main contribution for the general case but entirely lacks quantitative validation. This suggests the paper would be more coherent if restructured to present the Gaussian GPCA as the primary contribution, with GPCAGEN positioned as a promising preliminary proposal requiring further experimental validation.

## Suggestions

- Add a controlled quantitative experiment with known ground truth: generate data along a known Wasserstein geodesic (interpolating between two non-Gaussian distributions with orthogonal perturbations) and test whether GPCAGEN recovers the correct principal direction. Report angular error or fraction of variance captured.
- Report the achieved loss value (Eq. 15) at convergence for each component to demonstrate that the optimization produces meaningful principal geodesics that actually minimize the stated objective.
- Include convergence curves and final constraint satisfaction metrics (orthogonality violation, intersection distance).

## Score and Decision

**Calibration anchors** (all rounds, grouped by round):

**Round 1 (bracketing):**
| Path | Avg Score | Round | Itemized | Comparison |
|------|-----------|-------|----------|------------|
| `Uj0h13lVrR.md` (GFlowNets) | 1.00 | R1 | No | Unrelated topic; strong reject |
| `P49gSPmrvN.md` (UMAP discourse) | 1.00 | R1 | No | Unrelated; strong reject |
| `F5UgXkPgSn.md` (Grassmannian completion) | 3.00 | R1 | No | Less related; weaker theory |
| `4mqt6QxSUO.md` (Riemannian COVID detection) | 3.25 | R1 | No | Different problem domain |
| `gG7P1SL0QS.md` (DP-SGD geometry) | 3.20 | R1 | No | Different problem |
| `qcyn7ESaM8.md` (PCA and neural nets) | 2.50 | R1 | No | Tangentially related |
| `EyWKb7Ltcx.md` (SPD classifiers) | 5.00 | R1 | Yes | SPD manifold work; our theory is stronger and more novel |
| `CrOHzVtWmH.md` (RT Wasserstein) | 3.80 | R1 | No | Different objective |
| `OPKBPz6Qnz.md` (Graph geodesic distance) | 4.40 | R1 | No | Different domain |
| `kvByNnMERu.md` (Shape distances) | 5.25 | R1 | No | Different problem |
| `mkDam1xIzW.md` (Probabilistic GPCA) | 7.33 | R1 | Yes | **Most comparable anchor** — geometric PCA on manifolds, had quantitative evaluation though limited; our theory is stronger |
| `HB4lr0ykTi.md` (Wasserstein Flow Matching) | 6.33 | R1 | Yes | Wasserstein geometry + neural nets; had quantitative experiments but theoretical concerns |
| `P7O1Vt1BdU.md` (Sliced Transport) | 6.67 | R1 | No | Different task |
| `EKaVO0ceh8.md` (Projection OT) | 6.00 | R1 | No | Different task |
| `cNmu0hZ4CL.md` (Neural population dynamics) | 8.00 | R1 | No | Different domain |
| `JWtrk7mprJ.md` (Residual Deep GPs) | 7.60 | R1 | No | Different domain |
| `kbjJ9ZOakb.md` (Invariance manifolds) | 8.00 | R1 | No | Different domain |
| `g7ohDlTITL.md` (Flow Matching on geometries) | 8.00 | R1 | No | Different domain |

**Round 2 (narrowing, bracket 3.5–6.5):**
| `IUmDBY4NOQ.md` (Hyperbolic distance) | 4.75 | R2 | Yes | Hyperbolic geometry; similar evaluation gaps |
| `sRaAt9OOnW.md` (Continuous GWOT) | 6.20 | R2 | Yes | OT-related; had theoretical gaps and evaluation issues |
| `WdhtdjoaVw.md` (Wasserstein Bridge) | 4.80 | R2 | No | Different problem |
| `nS2DBNydCC.md` (Vector quantization) | 4.75 | R2 | No | Different problem |

**Round-1 bracket**: The paper clearly does not belong in the 1–3.5 range (its theoretical contributions are substantial) or in the 8.5+ range (GPCAGEN evaluation gap). The plausible bracket is **3.5–7.5**, narrowed to **4.0–6.5** by comparison with the most relevant anchors (PGPCA at 7.33, WFM at 6.33, SPD classifiers at 5.00).

**Final score placement (5.0):** The PGPCA anchor (7.33) had multiple severe weaknesses (missing baselines at -9.60, unclear importance at -9.50, limited real data at -6.98) but still had at least some quantitative experiments and was accepted. Our paper shares similar theoretical strength (+9.98 vs. +9.91 for PGPCA's theory) but has an even weaker evaluation profile: GPCAGEN has literally *zero* quantitative metrics. The WFM anchor (6.33) had quantitative experiments but was rejected due to theoretical groundlessness concerns. Our paper has the opposite profile—strong theory but no quantitative GPCAGEN evaluation. The SPD classifiers anchor (5.00) was rejected for incremental novelty and unclear contribution; our paper's theory is more novel, but the GPCAGEN evaluation gap is larger. Placing the paper at **5.0** reflects that it has genuine theoretical value (Gaussian GPCA) but the central claim about GPCAGEN "filling the gap" for general a.c. measures is not supported by quantitative evidence—a problem severe enough that the paper in its current form does not meet the bar for acceptance.

MY FINAL SCORE: <score>5.0</score>
MY FINAL DECISION: <decision>Reject</decision>