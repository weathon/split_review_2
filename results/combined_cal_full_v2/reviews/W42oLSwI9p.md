## Summary

This paper proposes three one-step diffusion-based neural solvers (CMILP, SCMILP, MFILP) for integer linear programming, combining consistency/shortcut/meanflow generative models with a novel Iterative Integer Projection (IIP) layer that differentiably handles non-binary integer variables. The methods also incorporate objective-guided sampling with momentum. The paper evaluates on three binary ILP benchmarks and two non-binary problem families.

## Strengths

- **Addresses a real bottleneck.** The paper correctly identifies that existing diffusion-based ILP solvers (e.g., IP Guided DDPM/DDIM) have prohibitive inference times — hours in some cases (Table 1 shows DDPM at 11h, 30h, 9h). Replacing multi-step diffusion denoising with a one-step generative model is a natural and potentially high-impact direction. **[weight=9.71]**

- **The IIP layer is a clean technical idea.** The function $f_{\text{proj}}(x) = x - \frac{\sin(2\pi x)}{2\pi}$ is a differentiable, computationally cheap approximation of the rounding function that converges with a few iterations. This is a legitimate contribution over the binary-only Sigmoid relaxation used in prior work, and using few iterations at train time and more at test time is sensible. **[weight=9.94]**

- **Comprehensive breadth of evaluation.** The paper tests on three binary ILP problem classes (set cover, facility location, combinatorial auction), plus two families of non-binary problems (inventory management and synthetic random). This gives a reasonable view of method behavior across problem structures. **[weight=9.64]**

## Weaknesses

### Major

- **Central claim of superiority is contradicted by the binary ILP results.** The abstract states the methods "outperform existing learning-based methods on both binary and non-binary instances." However, on the primary accuracy metric (optimality gap) in Table 1, IP Guided DDIM achieves substantially **lower (better) gaps** on all three binary datasets: SC (68.5% vs 88.4% for MFILP), CF (54.6% vs 76.1%), and CA (25.4% vs 79.2%). The gaps are 20, 22, and 54 percentage points worse than DDIM respectively. The paper's text selectively highlights beating DDPM (the slowest diffusion baseline) on gap while eliding the DDIM comparison. The speed advantage (40–140× faster) is a genuine contribution, but should be framed as a speed-accuracy Pareto trade-off, not as overall "superiority." The paper acknowledges DDIM's lower gaps in Section 4.2 ("Although IP Guided DDIM consistently produces the lowest gap…") but the abstract and contribution claims do not reflect this nuance. **[weight=0.93]**

- **The "nearly 100% feasibility" claim is not supported on all binary datasets.** Contribution 1 states the methods "achieve higher solution feasibility compared to previous neural solvers, reaching nearly 100% on binary ILP problems." On CF (Table 1), sample feasibilities are 88.3–92.1%, which is a stretch to call "nearly 100%." Moreover, IP Guided DDIM achieves 89.7% on CF — tied with MFILP and better than SCMILP (88.3%) — contradicting the "higher" claim for that dataset. **[weight=2.13]**

- **Missing non-binary baseline weakens the "first" claim.** The paper cites Tang et al. (2025) as addressing non-binary ILP via an integer correction layer (Section 2), yet does not include it as a baseline in any non-binary experiment. This undermines the paper's claim of being "the first time" extending binary neural solvers to non-binary cases for feasible solution prediction. **[weight=0.02]**

### Minor

- **IIP evaluation on binarized variants is misleading.** In Table 4, on binarized IM-(50,5,2), all three proposed methods report 0.0% gap but dataset feasibility is only **3.0%**. The 0.0% gap is computed on only the 3% of test instances where any feasible solution was found, making the metric uninformative. The direct (non-binarized) formulation achieves 78–90% feasibility, which is where the IIP advantage actually lies — the paper should frame this more clearly. **[weight=1.07]**

- **The gap metric introduces selection bias.** Section 4.1 states the gap "is only calculated among problems to which the solvers can get a feasible solution." This penalizes methods that find feasible solutions on harder problems (raising their average gap) and rewards conservative methods that only return solutions on easy instances. Alternative metrics (e.g., gap with an infeasibility penalty) would be more robust. **[weight=3.19]**

- **Gaps exceed 100% on some non-binary problems.** On IM-(50,5,10) (Table 2), all proposed methods achieve gaps of 107.1–119.2%, meaning the predicted objective is more than double the optimal value. This represents a serious quality degradation that the paper does not discuss. **[weight=-0.17]**

- **No variance or statistical significance metrics.** None of the 6 results tables include standard deviations or confidence intervals. Since the methods involve stochastic sampling, this makes it impossible to assess whether observed differences between methods are meaningful. **[weight=0.51]**

- **Momentum improvement is overstated.** Table 5 shows momentum improves gap by ~2% and dataset feasibility by at most 4% over standard gradient descent. Claiming this "improves the search quality significantly" is not supported by the magnitude of the improvement. **[weight=1.43]**

### Trivial

None.

## Nice-to-Haves

- Report the total number of forward/backward passes per inference (diffusion denoising steps + gradient steps + IIP iterations) to clarify the "one-step" pipeline cost.
- Include an analysis of why binary gaps are substantially worse than DDIM (e.g., whether the degradation stems from the one-step compression, training distribution, or representation).
- Clarify whether gap and feasibility metrics in Section 4.1 are computed on IIP-projected or hard-rounded solutions, and whether hard rounding itself can produce infeasible solutions.

## Removed Points

*These points were flagged for removal from the input review with justification.*

1. **"One-step label is imprecise"** — "One-step" consistently refers to the diffusion denoising step specifically, which is standard terminology from consistency/shortcut/meanflow models. The paper's usage is clear in context.
2. **"Notation overloaded in Eq. 7-8"** — Re-checking the paper, $\mathbf{y}^*$ is consistently defined as the minimization target in Eq. 8. The notation is consistent, not overloaded.
3. **"IIP function gradient flow issues"** — The critic speculates about potential optimization difficulties without demonstrating an actual problem. This is speculation, not a verified weakness.
4. **"L_{XXILP} not defined for SCMILP and MFILP"** — The paper states these details are in the appendix, which was stripped by the PDF parser. Per policy, appendix-stripped content is not a valid weakness.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

- Reframe the contribution honestly as a **speed-accuracy Pareto trade-off** for binary ILP (40–140× faster than DDIM but with 20–54pp worse gap), rather than claiming "superiority."
- Report gap with a penalty for infeasibility or use a metric like the geometric mean of (gap × penalty) across all instances, to remove selection bias.
- Include standard deviations or confidence intervals across multiple random seeds for all generative methods.
- Add Tang et al. (2025) as a baseline on non-binary problems, or explicitly justify why comparison is infeasible.
- Discuss the >100% gaps on IM-(50,5,10) and what causes the quality degradation on that dataset.

## Score and Decision

**Calibration anchors retrieved:**

| Path | Avg Score | Round | Itemized? | Comparison |
|------|-----------|-------|-----------|------------|
| u1cQYxRI1H.md | 0.50 | R1-bracket | No | Not topically relevant |
| nSDOkm0SKo.md | 1.00 | R1-bracket | No | Not topically relevant |
| Uj0h13lVrR.md | 1.00 | R1-bracket | No | Not topically relevant |
| bEgDEyy2Yk.md | 1.00 | R1-bracket | No | Not topically relevant |
| psDvcWtFdE.md | 3.00 | R1-bracket | No | MILP instance generation, different focus |
| 2o58Mbqkd2.md | 3.25 | R1-bracket | No | Diffusion superposition, different topic |
| XTxdDEFR6D.md | 3.40 | R1-bracket | No | LLM for CO solver design, different approach |
| fkNsgI1nye.md | 3.00 | R1-bracket | No | Secure diffusion, different topic |
| 2oWRumm67L.md | 5.00 | R1-bracket | Yes | ML for large-scale MILP — cleaner claims but fewer novel components |
| 1oIXRWK2WO.md | 4.25 | R1-narrow | Yes | Diff correction layers for MINLP — similar contribution type, no claim-evidence mismatch |
| JQV9gH55Az.md | 4.00 | R1-bracket | No | Diffusion for PDEs, different domain |
| 9p2YMVs1Tl.md | 4.00 | R1-bracket | No | MILP predict-and-search, different approach |
| joMMM9eadc.md | 6.25 | R1-bracket | Yes | Diffusion for IP solution generation — cleaner presentation, no contradictory claims |
| FPfCUJTsCn.md | 7.20 | R1-bracket | Yes | DiffILO (unsupervised ILP solver) — stronger methodology |
| 6JDpWJrjyK.md | 5.75 | R1-bracket | Yes | Diffusion solver for CO — similar speed-focus, stronger claims |
| KbvKjpqYQR.md | 6.00 | R1-bracket | No | Quantum GNN for MILP, different approach |
| uKZdlihDDn.md | 7.60 | R1-bracket | No | Not topically relevant |
| EO8xpnW7aX.md | 8.00 | R1-bracket | No | Not topically relevant |
| 6O3Q6AFUTu.md | 8.00 | R1-bracket | No | Not topically relevant |
| cNmu0hZ4CL.md | 8.00 | R1-bracket | No | Not topically relevant |
| D3vD7ZFIor.md | 3.50 | R2-narrow | Yes | GuideCO — weaker empirical results, clearer claims |
| km2nHt2YoD.md | 3.50 | R2-narrow | No | Integration of neural and problem-specific solver |
| J2kRjUAOLh.md | 4.75 | R2-narrow | No | MILP predict-and-search with contrastive learning |

**Bracket:** Round 1 established a plausible range of 3.5–5.5. Round 2 narrowed to 3.5–5.0, anchored by GuideCO (3.50) on the low end and Light-MILPopt (5.00) on the high end.

**Weighted-item comparison:** Our draft's strengths carry weights (9.64–9.94) comparable to the strongest anchors' positive items, indicating genuine technical merit. However, the claim-evidence mismatch in the abstract (weight=0.93 in our draft, but in my assessment a more central flaw) is a weakness not present in any anchor above 5.0. The most similar anchor in contribution type is "Learning to Optimize for MINLP" (4.25), which also proposes differentiable correction layers for integer outputs — but that paper does not have contradictory central claims. The "gap selection bias" weakness (weight=3.19 in our draft) is the highest-weighted item, consistent with Reviewer 4 of the IP Guided Diffusion anchor (6.25) raising similar concerns about gap-computed-only-on-feasible instances.

**Final placement:** 4.0 — The paper sits below Light-MILPopt (5.00) and the MINLP paper (4.25) because its headline claims are directly contradicted by its own Table 1, a problem those papers do not share. It sits above GuideCO (3.50) because its technical contributions (IIP layer, one-step solvers for non-binary ILP, breadth of evaluation) are more substantial and the core methodology is sound. The speed-accuracy contribution is real and should not be dismissed, but the paper must be honest about the trade-off.

MY FINAL SCORE: <score>4.0</score>
MY FINAL DECISION: <decision>Reject</decision>