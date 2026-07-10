Now let me compile the final review with all analysis complete.

## Summary

This paper proposes 3D (Dimension Domain Co-Decomposition), a unified PINN framework integrating dimension decomposition via a shared MLP with indexed inputs, an automatic MoE-based domain decomposition, and a new VI metric for per-dimension interpretability. The work contributes three concrete components: a parameter-efficient shared-MLP architecture that processes coordinate-index pairs, a mathematically principled subspace-alignment metric (VI), and a dense MoE router that learns domain partitions without predefined regions or interface conditions.

---

## Strengths

- **Shared-MLP with indexed inputs (Section 3.1).** Feeding coordinate-index pairs `(x_j, j-1)` into a single shared MLP rather than separate per-coordinate networks is clean and practical. Table 1 shows the parameter savings are real and scale with dimension — 5,392 vs 53,280 parameters on 10d Poisson, with memory reduced to 30.4% of the independent-MLP baseline. This is a concrete engineering contribution that removes a bottleneck in CP-decomposition-style approaches.

- **VI metric (Section 3.2).** The subspace-alignment formulation (QR decomposition on normalized F and G, then singular values of Q<sub>F</sub><sup>⊤</sup>Q<sub>G</sub>) is mathematically principled. It correctly handles the s ≤ r case where the predicted subspace may be larger than the ground-truth subspace and is scale-invariant. Among dimension-decomposition PINN papers, this is the first dedicated metric of its kind.

- **MoE domain decomposition visualization (Figures 4, 5).** The router weight maps provide compelling visual evidence that the learned partition aligns with physical features — the shock at x=0 in Burgers (Figure 4) and the diagonal stripes in Transport (Figure 5). The partition emerges without predefined regions or interface penalties, which is a meaningful improvement over XPINNs-family methods that require manual partitioning.

- **Quantitative impact of MoE on Burgers (Section 4.3).** The ℓ₂ error drops from 0.2108 (K=1, single expert) to 0.0011 (K=2) — a ~200× improvement. The large variance of the K=1 result (0.1252) suggests the single-expert dimension decomposition is unstable without MoE, and the dramatic reduction cleanly demonstrates the MoE structure provides a qualitatively different capability from the single-expert version.

---

## Weaknesses

### Major

- **No baseline comparisons against the relevant state of the art.** The paper discusses SPINNs (Section 3.1) and XPINNs/APINNs (Section 2.2) at length and explicitly positions 3D as improving upon them, but provides zero empirical comparisons against any of these methods. The only baselines in the experiments are vanilla PINNs and the paper's own ablation (independent MLPs). On the Poisson/Wave benchmarks — where dimension decomposition is the contribution — no SPINN baseline is run. On Burgers/Transport — where domain decomposition is the contribution — no XPINN/APINN accuracy numbers are reported. Without these comparisons, the central claim that 3D "improves both computational efficiency and solution accuracy" (Abstract) cannot be evaluated relative to what already exists. This is a structural gap in the evaluation, not a minor omission.

- **VI metric's applicability is narrower than the paper's framing suggests.** The Abstract and Introduction claim "interpretable per-dimension representations" as a general capability. In practice, VI requires known ground-truth per-dimension factors, which exist only for product-separable solutions (u = ∏ g_j(x_j)). Every single PDE benchmark used for VI evaluation (5d Poisson, 10d Poisson, 1d Wave, 2d Wave) has exactly this structure. The paper acknowledges this limitation in the conclusion and suggests truncated Fourier series as a workaround, but this is never demonstrated — not even on a simple non-separable synthetic case. The notion of interpretability VI provides is confined to cases where the solution is already known to factorize, which is a narrow subset of PDEs. The abstract does not convey this restriction.

### Minor

- **The "high-dimensional" claim in the abstract is overstated.** The Abstract claims improvements across "a range of high-dimensional PDE benchmarks," but only 2 of 6 benchmarks (5d Poisson, 10d Poisson) are genuinely high-dimensional. The Wave (1d, 2d), Burgers (1d+time), and Transport (1d+time) equations are all low-dimensional. Moreover, the 10d Poisson result is on a trivially separable (product-of-sines) solution — the most favorable possible setting for dimension decomposition.

- **No quantitative ℓ₂ error reported for the Transport equation.** The Transport results (Section 4.3) present only visualizations of the router's domain partition (Figure 5). No accuracy numbers are reported, making it impossible to assess whether the MoE-based decomposition actually improves solution quality on this benchmark.

- **The failure of r=1 for rank-1 ground truth is unexplained.** For the 5d Poisson (where the true solution is a single product, rank 1), r=1 achieves VI of only 4.11% (Table 2), yet r≥4 achieves VI≈1. This is a puzzling discrepancy — the latent dimension matches the true rank — but the paper offers no explanation (e.g., optimization difficulty versus architectural limitation) for why r=1 is insufficient.

---

## Removed Points

These points were flagged to be removed; treat them with caution.

- **Inconsistent/underspecified experimental designs** (from Harsh Critic): The critic notes variable hyperparameters (width 64 vs. 32, varying rank r) across tasks and that convergence conditions and loss weights are deferred to the appendix. Having different hyperparameters for different PDE problems is standard practice — different equations need different capacities. Deferring convergence conditions and loss weights to an appendix is also standard practice for ICLR papers. This criticism does not identify a specific methodological flaw that threatens the results.

- **The critic's "Strengthening the Paper on Its Own Terms" section contained suggestions (add SPINNs baseline, add XPINNs baseline, demonstrate VI on non-separable case) that are captured by the Major and Minor weaknesses already listed above. These are not independent weaknesses.

- **The critic's "No error bars on parameter-efficient comparison" suggestion** — Table 1 compares parameter counts which are deterministic, not stochastic. Error bars are not applicable here.

---

## Novel Insights

None beyond the paper's own contributions. The three components (shared-MLP dimension decomposition, VI metric, MoE domain decomposition) are competently assembled, but the individual ideas draw on existing techniques: indexed inputs for parameter sharing, subspace alignment for metric design, and soft gating for domain partitioning. The novelty lies in the combination and in the specific application to PINNs.

---

## Suggestions

- Add SPINNs as a baseline on all Poisson and Wave benchmarks. This is the single most important addition — the paper differentiates itself from SPINNs in Section 3.1 but never verifies the advantage empirically.
- Add XPINNs (or a comparable manually-partitioned domain decomposition method) as a baseline on Burgers to show that the automatic MoE partition achieves competitive accuracy.
- Report ℓ₂ error for the Transport equation across K settings.
- Either temper the abstract's claims about high-dimensional performance to match the actual benchmarks, or add at least one non-separable high-dimensional PDE (e.g., HJB or high-dimensional elliptic equation).
- If VI is claimed as a general interpretability metric, demonstrate it on at least one non-separable (e.g., sum-of-products) case to show the truncated Fourier series workaround is viable.
- Explain why r=1 fails for rank-1 problems — this would strengthen the empirical understanding of the method.

---

## Score and Decision

**Calibration Anchors Considered:**

| Anchor | Path | Avg Score | Round | Itemized? | Comparison |
|--------|------|-----------|-------|-----------|------------|
| DimOL | hghJJJUJJR.md | 3.00 | R1 | Yes | Weaker architectural contribution and marginal empirical gains; current paper is clearly stronger |
| Hybrid Numerical PINNs | R5FzCFR5yU.md | 3.33 | R1 | Yes | Flawed central claim about AD failure; current paper has sounder core ideas |
| ODNN | ZujMVRn7Md.md | 4.25 | R2 | Yes | Similar-level contribution but different domain; current paper comparable |
| HyResPINNs | 5rfj85bHCy.md | 5.00 | R2 | Yes | Comparable — both have clear architectural contributions but evaluation scope limitations (only 2 PDEs for HyResPINNs) |
| Connecting Solutions PINNs | Q9OGPWt0Rp.md | 5.25 | R1 | Yes | Comparable — both have real contributions but lack comparisons with important baselines |
| PINNacle | ApjY32f3Xr.md | 5.25 | R2 | Yes | Benchmarking contribution with limited novelty; similar aggregate assessed quality |
| Backprop-free training | 4KKqHIb4iG.md | 5.60 | R2 | Yes | Stronger empirical results but more of an optimization contribution; comparable overall |
| PIG | y5B0ca4mjt.md | 6.50 | R1 | Yes | Stronger evaluation with proper baselines and ablation; current paper is below this |

**Bracket (Round 1):** Between 4 and 5.5 — above DimOL (3.00) and Hybrid Numerical PINNs (3.33) but below PIG (6.50).

**Narrowing (Round 2):** The paper's strengths (favorability 12.45–14.11) are comparable to those of HyResPINNs (5.00, strengths 5–14) and Connecting Solutions PINNs (5.25, strengths 7–12). However, its major weaknesses (favorability -3.20, -3.08) are structurally more central — they concern the absence of any competitive baseline comparison, which directly undermines the core claim of improved accuracy over existing methods. In HyResPINNs (5.00), the most negative weakness was about limited novelty (-5.23), but the architectural evaluation itself was sound. In Connecting Solutions PINNs (5.25), missing baseline comparisons were also flagged (favorability 1.88), but the paper's inference-speed contribution was independently verifiable from the architecture. Here, the accuracy claim cannot be verified without SPINN/XPINN comparisons.

Given the genuine architectural contributions (shared MLP, VI metric) balanced against the structural evaluation gap, the paper sits at **4.5** on the ICLR scale — it has real merit but the evaluation does not yet support its central claims.

**Decision: Reject** — The paper contains useful components, but the absence of any empirical comparison against the methods it claims to improve upon (SPINNs, XPINNs) prevents a reviewer from verifying its core contribution. This gap is structural and would require a new set of experiments to address.

MY FINAL SCORE: <score>4.5</score>
MY FINAL DECISION: <decision>Reject</decision>