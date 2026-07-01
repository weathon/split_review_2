Now let me read the rest of the experiments and conclusion more carefully to verify remaining claims.Now I have thoroughly read the paper. Let me draft the review before calibration.Now let me run Round 1 calibration — bracketing across score bands:Let me read some key anchor reviews in detail for calibration:Now I have enough calibration data. Let me form my bracket and finalize the review.

**Round 1 Bracket:** The paper sits between the 3.5–5.5 band. It has genuine ideas (shared MLP, VI, MoE decomposition) but a critical experimental gap (no comparison with SPINNs/XPINNs/APINNs, only separable benchmarks). This places it comparable to papers like HyResPINNs (5.00, rejected for limited experiments) and NEKM (4.25, rejected for missing comparisons), but the 3D paper's baseline gap is arguably more severe because it explicitly positions against these methods in the related work. Initial bracket: **3.5–5.0**.

Now let me produce the final review.

---

## Summary
This paper proposes Dimension Domain Co-Decomposition (3D), a PINNs-based framework that combines CP-decomposition-style dimension decomposition (using a shared MLP with coordinate-index pairs) with dense Mixture-of-Experts (MoE) domain decomposition. The paper also introduces Variable Interpretability (VI), a metric that quantifies alignment between learned per-dimension components and ground-truth separable factors. Experiments on Poisson, Wave, Viscous Burgers, and Linear Transport equations demonstrate parameter efficiency, interpretability on separable solutions, and automatic domain partitioning near sharp features.

## Strengths

- **Parameter-efficient shared MLP design is concretely demonstrated (Section 3.1, Table 1, Figure 2).** The shared MLP with coordinate-index pairs reduces parameters from 53,280 to 5,392 for 10d Poisson (Table 1), and Figure 2 shows it slightly outperforms independent MLPs on 5d Poisson (ℓ₂ = 1.84×10⁻⁴ vs. 3.26×10⁻⁴). Memory savings are also reported (30.4% of independent MLPs for 10d). The scaling advantage grows with dimensionality — the right behavior for a high-dimensional method.

- **MoE-driven domain decomposition learns physically meaningful partitions (Section 4.3, Figures 4–5).** Figure 4 shows the router correctly identifies the shock at x = 0 in Viscous Burgers (ℓ₂ drops from 0.21 for K=1 to 0.001 for K=2). Figure 5 recovers the diagonal stripe structures in Linear Transport. The consistency experiment across five seeds and robustness under 5% noise (Section 4.3) provide meaningful evidence that partitions are driven by solution structure, not initialization artifacts.

- **VI metric is a principled construction (Section 3.2).** The QR + SVD subspace alignment approach is scale-invariant and permutation-invariant by design, correctly handling the inherent ambiguities of CP-type decompositions. Table 2 shows a clear relationship between rank r and VI across multiple PDEs.

## Weaknesses

### Fatal
None.

### Major

- **No comparison with directly related decomposition-based PINNs methods.** The only baseline is vanilla PINNs (a monolithic MLP). The paper explicitly discusses SPINNs (Cho et al., 2023), XPINNs (Jagtap et al., 2020c), APINNs (Hu et al., 2023), and cPINNs in Section 2 and claims advantages over them — shared MLP removes per-dimension networks (vs. SPINNs), automatic partitioning avoids manual subdomains (vs. XPINNs) — yet no experimental comparison is made with any of them. The paper even notes that APINNs "use soft gating mechanisms to allow more flexible domain decomposition" (Section 2.2), which is architecturally close to the MoE approach proposed here. Comparing only against vanilla PINNs demonstrates that decomposition helps, which is already established; it does not demonstrate that *this* decomposition is better than existing alternatives. This gap prevents assessment of the paper's central claims relative to the state of the art.

- **All benchmarks have exactly separable solutions matching the model's CP-decomposition inductive bias.** The Poisson solution u = ∏ sin(πxᵢ) is a product of univariate functions. The Wave solution u = sin(πx)cos(cπt) is rank-1 separable. Viscous Burgers and Linear Transport, while featuring sharp features, are still amenable to low-rank separable approximation in their smooth regions. Testing a CP-structured model exclusively on CP-structured problems is circular — success demonstrates alignment between model and benchmark, not generality. No PDE with genuinely non-separable solution structure is tested, leaving claims about "high-dimensional PDE solving" and "scalability" unsupported for the problems where these properties matter most.

### Minor

- **VI metric's practical scope is inherently limited.** The authors acknowledge in Section 5: "VI relies on reference solutions that are dimension-separable." This means VI can only be evaluated when (a) the exact solution is known and (b) it factorizes into per-dimension components — conditions that do not hold for the practical problems where interpretability would be most valuable. The metric is better characterized as a diagnostic for factor recovery on separable benchmarks, not a general interpretability measure.

- **VI saturation when s < r weakens its discriminative power.** As the paper acknowledges (Section 3.2), when the ground-truth rank s is less than r (the common case — e.g., s=1 for Poisson while r≥4), VI = 1 means only that the exact subspace is contained in the predicted subspace, not that the predicted subspace is minimal. High VI can thus coexist with spurious latent dimensions, limiting VI's ability to detect whether the model has learned a parsimonious representation.

- **Missing wall-clock time and memory reporting for MoE experiments.** While Table 1 reports parameter counts, the domain decomposition experiments (Burgers, Transport) lack wall-clock training times and peak memory usage. The 5-layer width-64 router MLP adds computational overhead that may offset the parameter savings from the shared expert design. The 10d Poisson comparison does report times (1579s vs. 1184s), showing the shared MLP is actually slower per-run despite better accuracy, which makes the omission for MoE experiments more concerning.

### Trivial
None.

## Nice-to-Haves

- Test on at least one PDE with a genuinely non-separable solution (e.g., 2D/3D Navier-Stokes, nonlinear reaction-diffusion with coupled coordinates) to assess whether the CP structure with multiple experts can approximate non-separable solutions and whether MoE still produces meaningful partitions.
- Discuss how the integer index j−1 scaling interacts with coordinate values at high dimensionality, and whether normalization strategies are needed for very large d.
- Report VI on the Burgers/Transport experiments where MoE is used, to test whether VI remains meaningful in multi-expert settings.
- Consider extending VI to non-separable settings using approximate numerical decompositions (as briefly mentioned in the conclusion) with at least a proof-of-concept experiment.

## Removed Points

*These points are flagged to be removed; treat them with caution.*

- **"The 10d baseline PINN (4-layer width-64) is not configured to be competitive."** The paper explicitly states (Section 4.2): "For fairness, the baseline PINNs uses a single MLP with four hidden layers and width 64, identical to the shared MLP configuration. With a comparable number of parameters (5392 for the shared MLP versus 4929 for the baseline PINNs)." This is a controlled comparison at matched capacity, not a misconfiguration. The broader point about missing SPINNs comparison is valid and captured under Major weaknesses.

- **"Inconsistent statistical reporting."** Some results include standard deviations over seeds while others (e.g., 5d Poisson in Figure 2) report single runs. This is a minor presentation issue that does not affect core claims. Removed as a trivial nitpick.

- **"Abstract overclaims."** The reviewer objected to "significant challenges in high-dimensional settings and when modeling solutions with sharp features." While the experimental scope does not fully justify "significant challenges," the claim is a standard motivational framing. The real issue (insufficient baselines and separable-only benchmarks) is already captured in the Major weaknesses.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

- **Add head-to-head comparisons with SPINNs on dimension decomposition benchmarks and XPINNs/APINNs on domain decomposition benchmarks.** This is the single highest-leverage improvement. The paper's positioning against these methods demands empirical evidence of improvement.
- **Include at least one non-separable PDE** to test whether the CP structure with MoE can approximate solutions that don't match its inductive bias.
- **Reframe VI honestly** as a "diagnostic for factor recovery in separable problems" rather than a general interpretability metric, and provide at least one proof-of-concept with approximate numerical factors for a non-separable problem.
- **Report wall-clock time and peak memory** for all experiments, especially the MoE-based ones, to assess whether the parameter savings translate to computational savings.

## Score and Decision

### Calibration Anchors

| Paper | Path | Avg Score | Round | Comparison |
|-------|------|-----------|-------|------------|
| Hybrid Numerical PINNs | R5FzCFR5yU | 3.33 | 1 | More fundamental conceptual issues (claims already solved by existing methods); 3D paper has better-motivated ideas but weaker baselines. |
| In-Context Neural PDE | fzZfju8y0g | 3.40 | 1 | Different focus (in-context learning for PDEs); similarly rejected for insufficient experimental support. |
| EPINN | SYiOxXWlKU | 2.50 | 1 | Simpler contribution with narrower scope; 3D paper is clearly above this. |
| Data-Driven Discovery of PDEs | LwAG269lIq | 3.00 | 1 | Different focus (PDE discovery); rejected for limited novelty. |
| Connecting Solutions | Q9OGPWt0Rp | 5.25 | 1 | Demonstrated clear practical speed advantages with mathematical grounding; stronger experimental contribution than 3D despite also being rejected. |
| HyResPINNs | 5rfj85bHCy | 5.00 | 1 | Also a PINNs architecture paper rejected for limited experiments (2 PDEs), but had comparisons with competitive baselines — 3D paper has more experiments but weaker baselines. |
| Pseudo PINNs | CrmUKllBKs | 4.33 | 1 | Novel framework but insufficient validation; similar level of issues as 3D paper. |
| NEKM | kKRbAY4CXv | 4.25 | 1 | Novel method with missing comparisons; very similar profile to 3D paper. |
| Backprop-free PINNs | 4KKqHIb4iG | 5.60 | 1 | Also uses separation of variables but provides stronger empirical evidence; above the 3D paper. |
| Learning Neural Solver | jqVj8vCQsT | 5.60 | 1 | Stronger experimental section with clearer practical impact. |
| Physics-Informed Neural Predictor | vAuodZOQEZ | 6.50 | 1 | Accepted; much stronger experimental validation. |
| PIG | y5B0ca4mjt | 6.50 | 1 | Accepted; addresses spectral bias with stronger baselines. |
| Learning Distributions | uKZdlihDDn | 7.60 | 1 | Accepted; substantially more sophisticated method and evaluation. |

**Round 1 bracket:** 3.5–5.0

**Narrowing:** The 3D paper has genuinely interesting ideas (the shared MLP is a clean engineering contribution, MoE domain decomposition avoids manual partitioning, VI is a novel metric). These place it above the 3.0–3.5 papers that have more fundamental conceptual problems. However, the missing baselines are not a minor gap — they are the minimum evidence needed to support the paper's central claims of improvement over SPINNs/XPINNs/APINNs. This places it below HyResPINNs (5.00) which at least compared against competitive baselines, and below Connecting Solutions (5.25) which demonstrated clear practical advantages. The profile is closest to NEKM (4.25) and Pseudo PINNs (4.33): novel methods with some merit but insufficient experimental validation to support their claims.

**Final score: 4.0** — Borderline reject. The paper proposes sensible architectural ideas, but the experimental evaluation has a structural deficiency: the only baseline is vanilla PINNs, while the paper's related work discusses and implicitly claims improvement over SPINNs, XPINNs, APINNs, and others that are never compared against. All test problems have exactly separable solutions matching the model's inductive bias. These gaps prevent the paper's central claims from being adequately supported.

MY FINAL SCORE: <score>4.0</score>
MY FINAL DECISION: <decision>Reject</decision>