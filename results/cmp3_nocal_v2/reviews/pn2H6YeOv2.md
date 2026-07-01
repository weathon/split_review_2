Now I have all the evidence I need from the paper. Let me write the final consolidated review.

## Summary

Pi-CCA proposes a replay-free continual learning method for vision-language models that regularizes the canonical correlation geometry (spectrum and subspaces) of the whitened cross-modal covariance, using a compact sketched "CCA certificate" with prompt-invariance via projector averaging. The method is technically well-specified, replay- and generator-free, and achieves consistent state-of-the-art results across four VL-CL benchmarks (MTIL, X-TAIL, VLCL, ConStruct-VL).

## Strengths

- **Genuinely different conceptual approach to VL-CL.** The central idea — that forgetting can be characterized as drift in the canonical correlation geometry of the whitened cross-modal covariance, and that regularizing this directly rather than proxy signals (logits, similarities, parameters) is a better inductive bias — is clearly articulated and well-motivated (§1, §2). This gives the paper a coherent intellectual identity that distinguishes it from prior regularization-based methods.

- **Technically well-specified method.** Pi-CCA is presented with full mathematical detail: the CCA certificate (Eq. 3–4), randomized sketching for constant-memory storage (Eq. 4, with Gaussian or SRHT), the spectral and subspace losses (Eq. 8, 10), the prompt-invariance mechanism via projector averaging (Eq. 5–6, 11), and streaming EMA estimation (Eq. 12–13). The use of stop-gradient on the certificate and differentiable power iteration (§3.4) shows careful engineering.

- **Consistent empirical advantage across diverse benchmarks.** Pi-CCA outperforms all replay-free baselines on MTIL (76.8 vs. 75.2), X-TAIL (68.1 vs. 67.4), VLCL (I2T R@1 48.6±1.0 vs. 47.3±1.2 for GIFT), and ConStruct-VL (FA 75.2±1.3, AF 2.7±0.2) (Tables 1–2). The margins, especially on retrieval and structured-concept benchmarks, are meaningful. Pi-CCA even surpasses a synthetic-replay baseline (GIFT) without using any generated data.

- **Thorough ablation and analysis.** The component-wise ablation (Table 3) cleanly separates the contributions of spectral, subspace, prompt-invariance, and EMA terms. The Pareto analysis of certificate capacity (Fig. 2) provides practical guidance for selecting (k, h). The 20-order task-order sensitivity study (Fig. 5) addresses a common concern in continual learning. The prompt-invariance stress test (Fig. 4) convincingly demonstrates robustness gains.

## Weaknesses

### Fatal
None.

### Major

1. **Figure 3 reports physically implausible perfect correlations, and the analysis design is circular.** The figure caption states Pearson r=1.00 and Spearman ρ=1.00 for three of four panels, and r=0.99/ρ=1.00 for the fourth. Spearman ρ=1.00 means every pair of data points has identical ordinal ranking — essentially impossible for real experimental data with measurement noise, especially when sweeping multiple independent hyperparameter dimensions (certificate size, EMA rates, invariance strength, LoRA capacity, sketch type, etc.). Beyond the numerical values, the analysis is structurally circular: the paper sweeps hyperparameters that directly weaken the certificate (smaller k, removes L_spec, sets α=0), then correlates the resulting increase in drift (computed from the same certificate) with the resulting drop in performance. Both quantities are consequences of the same intervention; this is a sanity check that the regularization terms work as designed, not independent evidence that "geometry drift causes forgetting." To establish the causal claim asserted in §1 and §5, one would need to show that for a fixed method, naturally occurring drift across tasks or seeds correlates with forgetting. This does not invalidate the method's empirical results, but the paper overstates the evidentiary value of this analysis. (§4.3, Fig. 3)

2. **Table 1 reports point estimates without variance, while Table 2 includes ± intervals.** On MTIL, several methods cluster within 2–3 percentage points; on X-TAIL, Pi-CCA (68.1) leads RAIL (67.4) by only 0.7pp. Without standard deviations, confidence intervals, or significance tests, the reader cannot assess whether these gaps are meaningful or within run-to-run noise. The paper clearly has seed-level data (Fig. 5 reports 3 seeds for the task-order study), so the omission is a significant gap in the primary evidence. (§4.2, Table 1)

### Minor

3. **The certificate is updated via EMA (Eq. 13), which creates a tension with the "preservation" framing.** The paper introduces the certificate as storing "reference (pre-continual) CCA quantities" (§3.2, line 71), but Eq. 13 continuously revises it via ρ* ← (1−α)ρ* + αρ̂. The paper is transparent about this ("controlled plasticity," line 133), and the α=0 ablation still benefits performance (75.6 vs. 76.8 full), so the core contribution does not depend on a strictly fixed certificate. However, the framing as "preserving alignment geometry" rather than "stabilizing alignment geometry via smoothed constraints" inflates the conceptual novelty claim and should be adjusted. (§3.2, §3.4)

4. **Several design choices are insufficiently documented.** (a) The number of prompt perturbations M is stated as M=4 only in the stress test (line 224), but no sensitivity analysis or default value is provided. (b) The subspace-angle loss (Eq. 10) uses sketched projectors as a surrogate for the true subspace angle; the paper notes the approximation (line 109–110) and provides a Pareto sweep of (k, h), but offers no guidance on how to set h to ensure the surrogate is faithful for a different VLM. (c) The "constant-memory" claim applies to the sketched certificate, but the EMA covariance matrices Σ_vv, Σ_tt, Σ_vt (Eq. 12) may have significant memory footprints (each potentially d_v×d_v or d_v×d_t) — the actual dimensions and memory cost are not stated. (§3.2–3.4)

### Trivial
None.

## Nice-to-Haves

- **Computational cost comparison against baselines.** The paper provides Pareto analysis of Pi-CCA's own memory/time trade-offs (Fig. 2), but a wall-clock and GPU-memory comparison against the top 2–3 baselines under the same hardware would help practitioners assess practical overhead.

- **Real replay baseline.** The paper appropriately compares against replay-free methods (with GIFT as a synthetic-replay reference). Adding a standard experience-replay baseline (e.g., ER with a small buffer) would contextualize how close replay-free performance is to the replay upper bound.

- **Fix or replace the correlation analysis.** Given the concerns above, the authors could either: (a) hold the method fixed and measure geometry drift vs. forgetting across different tasks or seeds (not hyperparameter sweeps), or (b) artificially inject geometry drift and measure downstream effects. The current analysis does not support causal inference.

## Removed Points

These points are flagged for removal; treat them with caution.

- **"The GIFT comparison is highlighted without qualification"**: The paper explicitly states "surpasses a synthetic-replay method (GIFT) without storing or generating data" (line 202) and the table marks GIFT with † for synthetic replay (Table 2). The qualification is present. REMOVED.

- **"Missing computational cost comparison"**: The paper provides Pareto memory/time analysis (Fig. 2) for Pi-CCA. A full baseline comparison would be nice-to-have but is not a weakness of the current paper. DEMOTED to Nice-to-Have.

- **"The certificate is a moving target that undermines the core conceptual claim"**: The reviewer framed this as critical/fatal. The paper is transparent about the EMA update. The α=0 ablation proves the core mechanism (spectral + subspace regularization) works even with a frozen certificate. The framing tension is real but minor, not fatal. DEMOTED to Minor (#3 above).

- **"Task-order sensitivity y-axis ranges are narrow"**: This is an observation about the result itself (high robustness), not a weakness. Narrow ranges are evidence FOR the method, not against it. REMOVED.

## Novel Insights

The most novel observation from the reviews is the recognition that the correlation evidence in Figure 3 — which the paper presents as causal evidence linking geometry drift to forgetting — is structurally circular when both the independent variable (drift) and dependent variable (performance drop) are consequences of the same hyperparameter perturbations. The reported perfect Spearman correlations (ρ=1.00) compound this concern. This insight is not about the method itself (which is sound) but about a gap between the paper's evidentiary claims and its experimental design.

## Suggestions

1. Report variance (± standard deviations over multiple seeds) for Table 1 to match Table 2, and add a simple significance test (e.g., paired bootstrap) for the key comparisons on MTIL and X-TAIL.
2. Revise the framing of the certificate mechanism: describe it as "stabilizing alignment geometry via smoothed constraints" rather than "preserving a fixed invariant." This is more accurate and does not diminish the contribution.
3. Either correct or replace the correlation analysis in Figure 3. If the perfect correlations are genuine, explain why (e.g., very small number of configurations, deterministic relationships). If not, provide an honest analysis. Restructure the analysis to avoid circularity — e.g., hold the method fixed and correlate drift with forgetting across tasks or initialization seeds.
4. Document the sensitivity to M (number of prompt perturbations) and report the actual memory footprint of the EMA covariance matrices to substantiate the "constant-memory" claim.

## Score and Decision

MY FINAL SCORE: <score>8</score>
MY FINAL DECISION: <decision>Accept</decision>