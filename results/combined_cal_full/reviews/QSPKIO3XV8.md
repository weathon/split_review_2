## Summary

This paper proposes the Dimension Domain Co-Decomposition (3D) framework, which integrates a shared-MLP dimension decomposition (processing coordinate-index pairs through a single network instead of separate MLPs per dimension) with a Mixture-of-Experts driven domain decomposition that automatically partitions the solution space. The paper also introduces Variable Interpretability (VI), a subspace-alignment metric that quantifies how well learned per-dimension components align with known ground-truth factors. Experiments on Poisson, Wave, Burgers, and Transport equations demonstrate parameter efficiency and solution accuracy improvements over vanilla PINNs and independent-MLP baselines.

## Strengths

- **Shared-MLP dimension decomposition (Section 3.1, Table 1).** Using a single MLP that takes (coordinate value, index) pairs instead of separate networks per dimension is a clean, practical improvement. Table 1 shows parameter savings scale with dimensionality: 5,392 parameters vs. 53,280 for independent MLPs on 10d Poisson — a 10× reduction. The design elegantly makes parameter count independent of input dimension.

- **VI metric (Section 3.2, Table 2).** The subspace alignment approach (QR decomposition + singular values of Q_F^T Q_G) is methodologically sound and scale-invariant. Table 2 shows VI behaves as expected — monotonically increasing with rank r and reaching 1.0 when r is sufficient. For separable test problems where ground-truth factors are known, this fills a genuine gap in the PINNs literature for diagnosing factorization quality.

- **Burgers equation result (Section 4.3, Figure 4).** The improvement from K=1 (ℓ2 error 0.2108) to K=2 (ℓ2 error 0.0011 ± 0.0005) is dramatic and the learned domain partition cleanly separates at the shock x=0. This provides compelling evidence that the MoE router is learning physically meaningful domain decompositions without requiring predefined interfaces.

- **Presentation quality.** The method is well-motivated, the architecture diagram (Figure 1) communicates the two-level decomposition effectively, and the paper clearly distinguishes its contributions from prior work.

## Weaknesses

### Major

- **No experimental comparison against SPINNs or XPINNs/APINNs.** This is the most significant gap. The paper explicitly positions its dimension decomposition as improving upon SPINNs (line 80: "differs in several key aspects that bring advantages") and contrasts its MoE domain decomposition with XPINNs/APINNs (Section 2.2), yet provides no accuracy, runtime, or memory comparison against any of these methods on shared benchmarks. The Poisson/Wave results are compared only against "vanilla PINNs" and "independent MLPs" — neither is the most relevant baseline for the dimension decomposition claim. Similarly, the Burgers results show K=2 vs. K=1 but no comparison against XPINNs or APINNs with a manual partition at x=0. Without these comparisons, the claim that 3D "improves both computational efficiency and solution accuracy" over existing decomposition-based approaches is unsubstantiated by the evidence presented.

### Minor

- **The combined framework (dimension decomposition + MoE) is not demonstrated beyond 2D problems.** The MoE-driven domain decomposition is tested only on Burgers (1D+time) and Transport (1D+time). The high-dimensional Poisson experiments (5d, 10d) use only a single expert (K=1) — they evaluate only the dimension decomposition component in isolation. Training a router in high-dimensional space is itself a challenging problem, and the paper provides no evidence that the full 3D architecture scales beyond low-dimensional settings.

- **VI's scope is narrower than the paper implies.** The metric is presented as "a novel, quantitative, scale-invariant metric" (contributions), but it requires known ground-truth factor decompositions. All test problems use known separable analytical solutions — the ideal case. The conclusion mentions constructing separable approximations (e.g., truncated Fourier series) for non-separable cases, but this workaround is neither demonstrated nor validated. As presented, VI is a useful diagnostic for separable benchmark problems, not a general-purpose interpretability tool.

- **Transport equation results lack numeric ℓ2 errors.** Section 4.3 presents only visual domain decomposition heatmaps for the Linear Transport problem. While Burgers includes ℓ2 errors with standard deviations, Transport shows no accuracy numbers — making the domain decomposition claim for this problem only visually supported.

- **Wave equation VI values are reported without corresponding ℓ2 errors.** Table 2 reports VI for Wave cases with varying frequency c and rank r, but no ℓ2 errors accompany these results. For the c=10 case where VI=84.59 at r=5, one cannot tell whether the model has poor accuracy or high accuracy with misaligned factors. This makes it unclear whether VI provides information beyond what accuracy already reveals.

### Trivial

- The architecture asymmetry between the router (5-layer MLP) and the expert shared MLP (2 hidden layers) is stated but not justified. A brief explanation of why the router needs more capacity would be helpful.

## Nice-to-Haves

- Add SPINNs as a baseline on the Poisson and Wave benchmarks to substantiate the claim that the shared-MLP design improves upon separable factorization approaches.
- Add an XPINNs or APINNs baseline on Burgers with a manual partition at x=0 to benchmark the MoE's automatic decomposition against manual partitioning with interface conditions.
- Report ℓ2 errors for the Transport equation and alongside Wave equation VI values.
- Consider testing the combined (MoE + dimension decomposition) framework on a single problem in ≥3 dimensions to scope the "high-dimensional" claim.

## Removed Points

These points are flagged to be removed, treat them with caution:

- **Criticism about unfair 5d Poisson comparison (10-layer vanilla PINNs vs. 2-layer shared MLP).** Per the asymmetry rule: the asymmetry favors the baseline (deeper, more parameterized network should be more expressive), so this makes the comparison a stronger test for the proposed method, not a weakness. Removed.
- **Generic concern about how the number of sampled points n_j affects QR stability for VI.** This is a minor implementation detail not standardly discussed at this level and is not specific enough to constitute a weakness. Removed.
- **The claim that the paper's headline result is entirely unsupported.** The paper does support improvements against vanilla PINNs and independent MLPs; the gap is specifically the comparison against SPINNs/XPINNs, which is already captured above. Removed due to overbreadth.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. **Add SPINNs as a baseline** on the Poisson and Wave benchmarks (accuracy, parameter count, training time). This is the single most impactful improvement and directly addresses the main weakness.
2. **Add XPINNs or APINNs as a baseline** on Burgers with a manual partition at x=0 to benchmark the MoE's automatic decomposition.
3. **Report ℓ2 errors for the Wave equation** alongside VI values and for the Transport equation to complete the experimental record.
4. **Test the combined framework on a higher-dimensional problem** (e.g., 3D+time) to support the "high-dimensional" scope of the paper's claims.
5. **Slightly reframe VI's scope** in the contributions: acknowledge upfront that it applies to problems with known factor decompositions.

## Calibration

**Round 1 bracket:** [3.5, 5.5]

All anchors retrieved:

| Path | Avg Score | Round | Itemized? | Comparison |
|------|-----------|-------|-----------|------------|
| nSDOkm0SKo.md (financial markets) | 1.00 | R1 | No | Unrelated domain, strong reject |
| u1cQYxRI1H.md (IC-Light) | 10.00 | R1 | No | Unrelated domain, strong accept |
| Uj0h13lVrR.md (GFlowNets) | 1.00 | R1 | No | Unrelated domain |
| 5lUdTogEL3.md (person re-identification) | 1.00 | R1 | No | Unrelated domain |
| R5FzCFR5yU.md (Hybrid Numerical PINNs) | 3.33 | R1+R2 | Yes | Similar domain, also had missing baseline comparisons as main weakness. Our positive weights are stronger (+4.32 to +5.25 vs +2.80 to +3.84), but our missing-baseline weight (-7.28) is comparable to their most severe weakness (-9.89). Their lower positives kept them at 3.33. |
| SYiOxXWlKU.md (EPINN) | 2.50 | R1 | No | PINN variant paper, weaker contributions than ours |
| GkJCgUmIqA.md (trSQP-PINN) | 3.00 | R1 | No | PINN optimization paper, limited PDE scope |
| LwAG269lIq.md (PDE discovery adjoint) | 3.00 | R1 | No | Different task (discovery vs. solving) |
| Q9OGPWt0Rp.md (Connecting Solutions) | 5.25 | R1+R2 | Yes | PINN meta-learning paper. Similar negative weights (-4.33, -4.23, -4.11, -3.87) and similar positives (+5.58, +3.88). Their missing-comparisons weaknesses are comparable to ours, and they landed at 5.25. |
| kKRbAY4CXv.md (NEKM) | 4.25 | R1 | No | PDE kernel method, comparable contribution level |
| H8CtXin7mZ.md (Neural-preconditioned Poisson) | 5.25 | R1 | No | Domain-specific solver, stronger on its narrow task |
| jqVj8vCQsT.md (Neural Solver for Parametric PDE) | 5.60 | R1 | No | Stronger experimental evaluation than ours |
| y5B0ca4mjt.md (PIG) | 6.50 | R1 | Yes | Strong paper with diverse baselines, ablation studies — exactly what our paper lacks |
| vAuodZOQEZ.md (PINN Predictor) | 6.50 | R1 | No | Stronger evaluation and broader scope |
| 4KKqHIb4iG.md (Backprop-free training) | 5.60 | R1 | Yes | Comparable weakness magnitudes (-6.00 insufficient experiments, -5.28 limited range) but also had stronger positive weights for benchmarking. Their score at 5.60 suggests our paper should be slightly lower given our missing-baseline gap. |
| ApjY32f3Xr.md (PINNacle) | 5.25 | R2 | Yes | Benchmark paper; very heavy negatives (-7.88, -8.70, -9.13) offset by strong positives |
| 5rfj85bHCy.md (HyResPINNs) | 5.00 | R2 | Yes | Method paper; had comparable novelty concerns (-8.56) and missing analysis (-6.65). Comparable to our paper in contribution level. |
| 0zZEbHLTwf.md (DeepFDM) | 3.50 | R2 | No | Weaker contribution than ours |

**Weighted-item comparison:** Our paper's strongest negative (-7.28 for missing baselines) is comparable to R5FzCFR5yU's -9.89 and -5.36, Q9OGPWt0Rp's -4.23/-4.11, and 4KKqHIb4iG's -6.00/-5.28. The key difference is that our positive items (+4.32 to +5.25) are stronger than R5FzCFR5yU's (+2.80 to +3.84) but comparable to Q9OGPWt0Rp's (+5.58, +3.88) and 4KKqHIb4iG's (+4.49, +3.85). The anchors with similar positive/negative profiles (Q9OGPWt0Rp at 5.25, 5rfj85bHCy at 5.00, 4KKqHIb4iG at 5.60) suggest our paper sits in the 4.5–5.5 range. Round 2 narrowed this to **5.0**, reflecting genuine contributions held back by an incomplete evaluation against the most relevant baselines.

MY FINAL SCORE: <score>5.0</score>
MY FINAL DECISION: <decision>Reject</decision>