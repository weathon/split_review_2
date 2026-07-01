## Summary

This paper proposes Dimension Domain Co-Decomposition (3D), a PINNs-based framework that combines dimension decomposition (via a shared MLP processing coordinate-index pairs) with MoE-driven domain decomposition. It also introduces Variable Interpretability (VI), a metric that measures alignment between learned per-dimension components and ground-truth factors. Experiments on Poisson, Wave, Viscous Burgers, and Linear Transport equations demonstrate parameter efficiency and the ability to automatically partition solution domains.

## Strengths

- **Shared-MLP with indexed inputs is a clean, practical contribution (Section 3.1, Table 1).** The design decouples the parameter count from the input dimension: the shared MLP uses 5,392 parameters for both 5d and 10d Poisson, versus 26,640 and 53,280 for independent MLPs. This dimension-independent parameter count is a genuine improvement over prior per-dimension network approaches.

- **MoE-driven domain decomposition produces compelling automatic partitions (Section 4.3, Figures 4-5).** The router's ability to identify the shock at x=0 for the Viscous Burgers equation without explicit interface conditions is visually striking. The quantitative result is strong: ℓ₂ error drops from 0.2108 (K=1, single expert) to 0.0011 (K=2) — a ~200× improvement. Consistency across five random seeds is reported for this experiment.

- **The paper honestly acknowledges the VI metric's core limitation** (Conclusion, Section 5), stating that VI relies on separable reference solutions and that constructing separable approximations for non-separable cases is future work.

## Weaknesses

### Major

- **No experimental comparison against the most directly relevant baselines, despite positioning the paper relative to them.** The paper discusses SPINNs (Section 3.1) as a related approach, claiming memory and MoE-compatibility advantages, but never benchmarks against SPINNs on the Poisson or Wave problems. Similarly, the Related Work (Section 2.2) discusses XPINNs, cPINNs, and APINNs as methods requiring "predefined subdomains" and "interface conditions," and the paper claims to overcome these (line 46-47), but the Burgers and Transport experiments include no comparison against any of these domain-decomposition PINN methods. Without these comparisons, the reader cannot assess whether 3D advances the state of the art or merely achieves comparable accuracy with a different design. The paper's own abstract claims "improves both computational efficiency and solution accuracy" — this level of claim requires evidence against the most relevant prior work, not only against vanilla PINNs.

- **The VI metric's practical utility is limited by its reliance on known separable reference solutions.** The paper acknowledges this (Section 5), but treats it as a future-work item when it is a structural constraint. To compute VI, one needs either the exact solution in factorized form (defeating the purpose for unknown solutions) or a constructed separable approximation (e.g., truncated Fourier series). The paper provides no analysis of how VI behaves with approximate references, how to choose the truncation, or how sensitive the metric is to approximation quality. The core use case — "use VI to verify interpretability when you don't know the ground truth" — is therefore not supported.

- **All four PDE benchmarks have solutions that are either separable or nearly separable in their dimension-decomposition core.** The 5d/10d Poisson solutions are products of univariate sine functions. The Wave solutions are products of sinusoids. While the MoE component handles non-smooth features (Burgers shock), the CP-decomposition core's ability to handle non-separable cross-dimension interactions within a single expert is not stress-tested. A problem with genuine multiplicative coupling between dimensions (e.g., Allen-Cahn, Navier-Stokes) would better probe this limitation.

### Minor

- **Inconsistent statistical reporting.** The 5d Poisson accuracy results (Section 4.2, line 137) are reported as single-run ℓ₂ errors (1.8430e-4, 3.2620e-4, 7.5451e-3) without standard deviation, while the domain decomposition results (Section 4.3) and VI results (Table 2) are averaged over five seeds. The reader cannot assess the variance of the accuracy claims.

- **Training time is only reported for one comparison** (10d Poisson: shared MLP 1,579s vs vanilla PINNs 1,184s, line 139). No wall-clock times are given for the MoE experiments (Burgers, Transport), making the "computational efficiency" claim for the full 3D framework hard to evaluate beyond parameter counts.

- **The vanilla PINN baselines receive minimal architectural tuning.** The 5d Poisson uses a 10-layer MLP (width 64), while the 10d Poisson uses a 4-layer MLP (width 64). These are reasonable but not necessarily strong baselines; no hyperparameter search is reported. Given the paper's accuracy claims, the reader cannot be sure that PINNs were given a fair chance to perform competitively.

### Trivial

None.

## Nice-to-Haves

- Run the Poisson and Wave experiments with SPINNs as a baseline to substantiate the claimed advantages over it.
- Run the Burgers experiment with XPINNs or APINNs using a manually placed partition at x=0 to compare automatic vs. manual decomposition.
- Demonstrate VI on a problem without an analytically separable reference, using a truncated Fourier approximation, with analysis of how VI varies with approximation quality.
- Report wall-clock times for the MoE experiments.
- Include standard deviations for all accuracy results, not only the decomposition and VI results.

## Removed Points

These points were removed from the harsh critic input after verification:

1. **"Router's parameter cost is not accounted for"** — Factually incorrect. Table 1's "Shared MLP" column for Burgers (23,586) and Transport (29,043) already includes the router parameters. Verified by matching the back-of-the-envelope calculation: 2 experts × 5,392 (shared MLP) + 12,802 (5-layer router) = 23,586 for Burgers; 3 experts × 5,392 + 12,867 (router for K=3) = 29,043 for Transport.

2. **"VI=1 doesn't mean subspace identity when s < r"** — The paper itself acknowledges this on line 100: "when s < r, VI measures whether the predicted subspace totally covers the exact subspace instead of testing if two subspaces are identical." The criticism is preemptively addressed.

3. **Criticism of SPINNs forward-mode AD compatibility with MoE** — The paper states this as a design observation, not an empirical claim. It is a technical limitation of SPINNs' architecture that justifies the design choice; including it as an evaluation weakness is not warranted.

4. **Reproducibility concerns about missing appendix / hyperparameter details** — These are parsing artifacts. The paper states all hyperparameters are in Appendix B and code is provided as supplementary material. The parser strips appendix content from all submissions.

5. **"Baseline unfairness" claim about vanilla PINNs** — Using standard 10-layer and 4-layer MLPs with width 64 is a reasonable baseline choice. While hyperparameter tuning could improve the baselines, the criticism that they are categorically "weak" without proposing a specific stronger baseline is not actionable.

## Novel Insights

The harsh critic's key insight is that the paper evaluates its architecture in a vacuum: dimension decomposition is compared against self-constructed independent-MLP baselines and vanilla PINNs, but not against the SPINNs method it derives from and claims advantages over; domain decomposition is compared only against K=1 (single expert), not against XPINNs or APINNs — the very methods it positions itself as overcoming. This disconnect between the paper's comparative positioning (vs. SPINNs, XPINNs) and its actual baselines (vanilla PINNs, self-constructed variants) is the central weakness. The VI metric limitation is also well-identified: requiring a known separable reference creates a circularity problem — you need the answer to verify that the model has found the answer.

## Suggestions

1. **Add SPINNs as a baseline** for the 5d and 10d Poisson benchmarks. This is the single most important addition because the paper explicitly claims advantages over SPINNs but provides no comparison. Report accuracy, training time, and parameter counts.

2. **Add XPINNs or APINNs as baselines** for the Burgers equation with a manually placed partition at x=0 (the natural splitting point). This would either confirm that 3D's automatic decomposition matches or exceeds manual decomposition, or reveal the gap.

3. **Demonstrate VI on a non-separable problem** using a constructed separable approximation (e.g., truncated Fourier series) with error analysis. Show how VI behaves as the approximation quality degrades, so practitioners can assess the metric's reliability when the ground truth is unknown.

4. **Standardize statistical reporting** by providing mean ± std for all accuracy results across multiple seeds.

## Score and Decision

**Calibration Anchors (all from `deepreview_13k_calibration`):**

| Anchor | Avg Score | Round | Comparison |
|--------|-----------|-------|------------|
| HyResPINNs (`5rfj85bHCy.md`) | 5.00 | 1 | Similar PINNs architecture paper, tested on 2 PDEs, rejected. Current paper tests more PDEs but shares same missing-baseline weakness. |
| Solving PDEs via learnable quadrature (`tl63stKeSC.md`) | 4.50 | 1 | Learnable sampling for PINNs, limited evaluation scope, rejected. |
| Connecting Solutions/Params (`Q9OGPWt0Rp.md`) | 5.25 | 1 | Fast PINNs inference, impressive speed claims but limited PDE scope, rejected (scores 5,5,8,3). |
| Ensemble/MoE DeepONets (`BvMuyqPvk1.md`) | 4.33 | 1 | MoE for operator learning, missing baselines vs other frameworks, rejected. |
| M²M Multi-expert operators (`MUL7tKvNei.md`) | 4.00 | 1 | Multi-scale multi-expert PDE solver, missing baselines, rejected. |
| PINNacle benchmark (`ApjY32f3Xr.md`) | 5.25 | 1 | PINN benchmark paper, different category. |
| Neural Metriplectic Systems (`uL1H29dM0c.md`) | 7.00 | 1 | Accept. Has theoretical proofs, extensive baselines, rigorous evaluation — a higher standard than current paper achieves. |
| PhysPDE (`G3CpBCQwNh.md`) | 6.50 | 1 | Accept. Clear motivation, robust experiments, multiple baselines, domain-specific datasets. |

**Round 1 bracket:** 4.5–6.0. The paper has genuine contributions (shared MLP architecture, VI metric, compelling Burgers result) but the evaluation gap against SPINNs and XPINNs is significant.

**Final score:** 5.0

**Rationale:** The paper contains genuine ideas (shared-MLP parameter efficiency, VI metric concept, MoE-driven domain decomposition) and one strong result (Burgers 200× error reduction). However, the evaluation does not support the breadth of the claims. The most critical issue is the absence of experimental comparison against SPINNs and XPINNs — methods the paper explicitly positions itself relative to and claims advantages over. Without these comparisons, the reader cannot assess whether 3D advances the state of the art. The VI metric's limitation (requiring separable reference solutions) further narrows the claimed contribution. The paper would need at minimum (a) comparison against SPINNs on the Poisson benchmarks and (b) comparison against XPINNs/APINNs on Burgers to substantiate its central claims.

MY FINAL SCORE: <score>5.0</score>
MY FINAL DECISION: <decision>Reject</decision>