## Summary

This paper proposes a unified Dimension Domain Co-Decomposition (3D) framework that combines two ideas for solving PDEs with PINNs: (1) a shared-MLP dimension decomposition that processes coordinate-index pairs through a single network instead of separate per-dimension MLPs, reducing parameters; and (2) a Mixture-of-Experts (MoE) router that learns automatic domain partitions without manually predefined subdomains or interface conditions. A Variable Interpretability (VI) metric is introduced to quantify alignment between learned per-dimension factors and ground-truth components for separable PDEs. Experiments on Poisson, Wave, Burgers, and Transport equations demonstrate parameter reductions and automatic domain discovery at physically meaningful boundaries.

## Strengths

- **Shared-MLP dimension decomposition (Section 3.1, Table 1).** Encoding dimension identity via an index input to a single shared MLP achieves dramatic parameter reductions (e.g., 53,280 → 5,392 for 10d Poisson) while maintaining accuracy comparable to or better than independent per-dimension networks. This is a genuine architectural improvement over the separate-MLP approach used in prior methods like SPINNs. **[favorability=10.04]**

- **Automatic domain decomposition via dense MoE (Section 3.3, Figures 4–5).** The router learns to partition the domain at physically meaningful boundaries (e.g., the shock at x=0 for Burgers, diagonal stripes for Transport) without manually predefined subdomains or interface loss terms. Error drops from K=1 (0.2108) to K=2 (0.0011) for Burgers, and the learned partitions are consistent across random seeds (Section 4.3). **[favorability=11.30]**

- **VI metric is technically sound for its intended scope (Section 3.2).** For separable PDEs where ground-truth factors are known, the subspace-alignment formulation (singular values of Q_F^T Q_G after normalization and QR) is a well-motivated, scale-invariant measure of whether the learned factorization captures the correct components. The paper honestly acknowledges its limitation to separable settings in the conclusion. **[favorability=11.22]**

- **Consistency analysis across random seeds (Section 4.3).** Repeating domain decomposition experiments across five seeds and showing the same geometric structures are recovered strengthens the claim that the MoE router captures solution features rather than initialization artifacts. **[favorability=11.02]**

## Weaknesses

### Fatal
None.

### Major

- **Missing quantitative comparison against the most relevant prior methods.** The paper claims to improve upon SPINNs (dimension decomposition, Section 2.1) and XPINNs/APINNs (domain decomposition, Section 2.2), yet provides no numerical comparison against any of them. For dimension decomposition, the baseline is "independent MLPs" — not SPINNs. For domain decomposition, no comparison against XPINNs, APINNs, or any prior domain-decomposition PINN is provided. The K=1 baseline (dimension decomposition without MoE) achieves 0.2108 error on Burgers — without a standard PINN or XPINN baseline, the reader cannot assess whether the MoE improvement is competitive with existing methods. Without these baselines, the claimed improvements in accuracy and efficiency over existing approaches are unsubstantiated. **[favorability=-0.55]**

- **All PDE benchmarks have fully separable solutions, which is the easiest case for a CP-decomposition-based method.** Poisson tests use u(x)=∏sin(πx_i); Wave uses sin(πx)cos(cπt); Burgers and Transport are 1D+time where space/time factorization is trivial. The paper claims to address "high-dimensional PDEs" (title, abstract) but never tests on a genuinely non-separable high-dimensional PDE (e.g., Allen-Cahn, convection-diffusion with interactions). The VI metric is defined only for separable problems. This makes it impossible to assess whether the dimension-decomposition component generalizes beyond product-form solutions. The paper acknowledges this limitation in the conclusion (Section 5) but frames it as a future direction rather than addressing it in evaluation. **[favorability=-0.63]**

### Minor

- **The MoE benefit is not isolated from increased model capacity.** Going from K=1 to K=2 more than doubles the parameters (adds a router network and an additional expert). The error drops from 0.2108 to 0.0011, but no ablation matches total parameter count between a single expert and multi-expert configuration (e.g., widening the single expert's layers to match K=2 capacity). Without this, it is unclear how much of the improvement comes from domain specialization versus simply having more capacity. **[favorability=1.74]**

- **No numerical ℓ2 errors are reported for the Linear Transport equation (Section 4.3, Figure 5).** Results are presented only as visualizations of gate assignments. For a paper claiming improved accuracy, quantitative errors should be reported alongside the visualizations. **[favorability=-0.76]**

- **The "interpretability" framing of the VI metric is somewhat overstated.** VI measures subspace alignment between learned components and known ground-truth factors. For separable PDEs this is a useful diagnostic, but calling it "interpretability" in the same sense as GAMs, NAMs, or self-explaining networks (discussed in Section 2.1) is imprecise. VI cannot be computed for PDEs where ground-truth factors are not known a priori, which is the practically interesting case. The paper acknowledges this limitation in the conclusion but uses the term "interpretability" throughout the title, abstract, and contributions without sufficient qualification. **[favorability=0.10]**

### Trivial

- **Some accuracy results lack statistical reporting.** The 5d Poisson final ℓ2 errors (1.8430×10⁻⁴, 3.2620×10⁻⁴, 7.5451×10⁻³) are reported without variance or number of seeds, while VI and Burgers results do include variance. Inconsistent reporting weakens reproducibility assessment. **[favorability=-0.38]**

- **Runtime analysis is incomplete.** Only the 10d Poisson runtime is reported (1579s vs 1184s). No training time comparisons are given for Burgers, Transport, or other benchmarks, despite "computational efficiency" being a stated contribution. **[favorability=-1.83]**

## Nice-to-Haves

- Add a controlled ablation for the MoE component that matches total parameter count between K=1 and K=2 configurations, to disentangle domain specialization from added capacity.
- Test on at least one non-separable high-dimensional PDE to demonstrate generalizability beyond product-form solutions.
- Add numerical ℓ2 errors for the Transport equation alongside the visualizations.
- Include SPINNs as a baseline for dimension decomposition and XPINNs/APINNs as baselines for domain decomposition on Burgers.

## Removed Points

- "Standard PINNs on Burgers with ν=0.01/π typically achieve ℓ2 errors on the order of 10⁻³" — this external-knowledge claim about a different paper's results cannot be verified from the paper under review; kept only the observation that the K=1 baseline is a weak strawman.
- Various formatting/style nitpicks and grammar complaints — removed per hard rules (parser artifacts, not author errors).
- Missing related work citations — removed per hard rules (cannot confirm existence of missing references).
- "Section-by-section notes" about imprecise language in Section 4.2 regarding "sharing across experts" — the meaning is clear from context; too minor to include.

## Novel Insights

None beyond the paper's own contributions. The main synthesis from the reviews is that the paper has two independently valid architectural ideas (shared-MLP dimension decomposition and MoE-driven domain decomposition) whose combination is evaluated on benchmarks that are favorable to both: separable solutions for the dimension decomposition and low-dimensional (2D) problems with sharp features for the domain decomposition. The paper would benefit from testing each component under conditions that stress its limitations.

## Suggestions

1. **Essential**: Add head-to-head comparisons against SPINNs (for dimension decomposition) and XPINNs/APINNs (for domain decomposition). Without these, the paper's central comparative claims are unsubstantiated.
2. **Essential**: Test on at least one non-separable high-dimensional PDE to establish generalizability of the dimension decomposition.
3. **Recommended**: Add a parameter-matched ablation for the MoE component to isolate the benefit of domain specialization from increased capacity.
4. **Recommended**: Report ℓ2 errors for the Transport equation and add variance bars for all accuracy results.

## Score and Decision

**Anchors consulted (all rounds)**:
- `5rfj85bHCy.md` (HyResPINNs, avg 5.0, Reject, itemized) — Similar PINNs architecture paper; our paper has more benchmarks but also missing baselines → comparable quality.
- `Q9OGPWt0Rp.md` (Connecting Solutions, avg 5.25, Reject, itemized) — Missing key baselines similar to our paper; our paper has stronger architectural novelty → slightly better.
- `60FseFP084.md` (SPONs, avg 4.25, Reject, itemized) — Only 2 experiments, missing baselines; our paper has broader evaluation → above.
- `4KKqHIb4iG.md` (Backprop-free training, avg 5.6, Reject, itemized) — Stronger quantitative comparisons against baselines; our paper lacks this comparative evidence → below.
- `nnicaG5xiH.md` (Interpretable Meta-Learning, avg 6.33, Accept, itemized) — Better experimental grounding and baseline comparisons; our paper below this.

**Final placement**: The paper's strongest items (shared-MLP architecture and MoE domain decomposition, favorability ~10-11) are competitive with anchor papers' strengths. However, the major weaknesses (missing baselines, separable-only benchmarks, favorability -0.55 to -0.63) are more impactful than the corresponding weaknesses in the better-rated anchors, which had more thorough evaluations despite similar scope limitations. The paper sits between the 5.0 (HyResPINNs) and 4.25 (SPONs) anchors — closer to 5.0 given its genuine architectural novelty — but is below the 5.6 (Backprop-free) and 5.25 (Connecting Solutions) anchors, which provided stronger comparative evidence.

MY FINAL SCORE: <score>5.0</score>
MY FINAL DECISION: <decision>Reject</decision>