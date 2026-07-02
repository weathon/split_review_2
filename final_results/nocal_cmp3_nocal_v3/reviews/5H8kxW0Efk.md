Now I have verified all claims against the paper. Here is the final consolidated review.

---

## Summary

The paper proposes NPIM (Neural Network Ising Machines), a method that applies algorithm unrolling to parameterize the update dynamics of an Ising machine using a small MLP. The dynamics are trained end-to-end via zeroth-order optimization (evolutionary strategies). The method is evaluated on Max-Cut, Max Independent Set, and Max Clique problems across neural CO benchmarks and the G-set, aiming to show that learned dynamics can match or exceed handcrafted Ising machine algorithms.

## Strengths

1. **Genuinely novel conceptual connection.** The idea of treating the entire iterative Ising machine trajectory as a learnable program by parameterizing the update function *F* with a small MLP and training via zeroth-order optimization is, to my knowledge, new within neural CO. The approach goes beyond plugging a neural network into a solver and is clearly distinguished from prior work (Section 2.3–2.4, Section 3.3).

2. **Interesting emergent dynamics analysis (Section 4.1).** Training a single-layer network from scratch shows that the weights evolve from a greedy "steepest descent" strategy (all weights negative) into dynamics with a momentum-like effect that enables escape from local minima. This is a concrete, nontrivial finding: the network discovers physically meaningful algorithmic structure without being explicitly programmed to do so. The visualization (Figure 2) is compelling.

3. **Competitive raw solution quality.** In Table 1, dNPIM achieves the best reported solution size on 4 of 5 neural CO benchmarks (MIS-small, MIS-large, MaxCut-small, MaxCut-large) compared to the DiffUCO, SDDS, and LTFT baselines from Sanokowski et al. (2025). The margins on MaxCut-large (2988.55 vs. 2974.60 for DiffUCO) are meaningful for an NP-hard problem.

## Weaknesses

### Fatal

None.

### Major

**1. Table 1 compares an unfair statistic: "top 30" vs. mean±std for baselines.**

dNPIM reports the *best solution found out of 30 parallel trajectories* ("top 30") as a single number, while DiffUCO and SDDS report mean ± standard deviation across multiple runs. These statistics are not comparable. The maximum of 30 independent draws from a distribution will systematically exceed the mean, especially when the distribution has high variance — which is typical for stochastic search on NP-hard problems. The reported dNPIM advantage on 4 of 5 benchmarks could be partially or fully explained by this statistical artifact. A fair comparison would report dNPIM's mean ± std across independent runs (with the same run count as baselines), or apply the same best-of-N selection to the baselines. The paper's justification ("our algorithm is less computationally intensive per trajectory") does not address the statistical validity of comparing max-of-30 against mean. This undermines the strongest neural CO comparison table.

**2. TTS measured in iterations, not wall-clock time (Table 2) — the G-set comparison is insufficiently supported.**

The TTS values in Table 2 are reported "in units of number of iterations to solution," with the justification that "the compute intensive matrix vector product is the computational bottleneck for each algorithm." This is not verified. dNPIM's per-iteration cost includes the coupling-field computation (Eq. 3) *plus* an MLP forward pass with matrix multiplications of dimension up to D×T_c (Eq. 4–5) and the temporal basis expansion (Eq. 6). The baselines (CAC, CFC, dSBM) have simpler per-iteration dynamics. An iteration of dNPIM is not the same computational unit as an iteration of CAC or dSBM. The central G-set claim — that dNPIM achieves state-of-the-art TTS among Ising machine algorithms — rests on a metric whose unit varies across methods, and the evidence is insufficient without wall-clock TTS (or at least FLOP-normalized TTS).

**3. "State-of-the-art" claims are calibrated to a niche and overreach the evidence.**

The introduction and conclusion claim "state-of-the-art performance on many commonly used benchmarks" without qualification. The evidence is narrower:

- On G-set (Table 2), the comparison is limited to three Ising machine algorithms (CAC, CFC, dSBM). No comparison with well-known classical heuristics for Max-Cut (e.g., Breakout Local Search, or MQLib best-known cuts) is provided, making the "SOTA" claim relative only to a specific algorithmic subfamily rather than the broader optimization literature.
- On one of five G-set categories (P, +), dNPIM underperforms badly — TTS of 4.42e+07 vs. 1.81e+06 for CAC (≈24× worse) — which is a significant failure on a major benchmark family. The paper acknowledges this briefly but the overall SOTA framing is not appropriately qualified.
- The neural CO comparison (Table 1) is against a single prior paper (Sanokowski et al., 2025) with three methods; other neural CO approaches (e.g., GNN-based methods) are cited in related work but not benchmarked.

### Minor

**4. Training overhead is not accounted for in any comparison.**

For G-set instances, the authors "generate a training set of problem instances which is used to fine-tune a network for that specific set of graph parameters." The computational cost of this per-distribution training is not characterized in the paper — no epoch counts, number of training instances, population size for ES, or amortization point where training pays off. The baselines (CAC, dSBM, etc.) require no per-distribution training. For a practitioner evaluating practical utility, the total cost (training + inference) matters, and the paper provides no basis for this assessment. (This is acknowledged in Section 6 for parameter scaling but not for training cost generally.)

**5. No variance estimates for dNPIM in Table 1.**

dNPIM results are reported as single numbers without any measure of variability (standard deviation, confidence intervals, or run-to-run spread), while DiffUCO and SDDS report mean ± std. Given the stochastic nature of all methods, this makes it impossible to assess whether the reported advantages are statistically meaningful.

**6. The interpretation of the parameter-ablation study (Section 4.2) conflates two explanations.** The paper states that the positive correlation between parameter count and success rate "indicates that the network is learning some non-trivial strategy that needs many parameters to describe." An equally plausible explanation is that underparameterized models are harder to optimize with the zeroth-order method (the optimizer struggles with smaller models, independent of the learned strategy's complexity). The paper does not disentangle these.

### Trivial

None.

## Nice-to-Haves

- Report wall-clock TTS (or FLOP-normalized TTS) for the G-set comparison to directly test the paper's central claim.
- Report dNPIM's mean ± std across independent runs in Table 1, with the same run count as baselines. If the multi-trajectory best is meaningful, report both single-trajectory and multi-trajectory statistics, with baselines also run in best-of-N configuration.
- Include at least one comparison with a non-neural, non-Ising machine classical heuristic for Max-Cut on G-set (e.g., Breakout Local Search) to calibrate expectations against the broader optimization literature.
- Characterize training cost: number of epochs, training instances, ES population size, and amortization break-even point.

## Removed Points

These points are flagged to be removed; treat them with caution.

- **Reproducibility/specification gaps about deferred appendices (Critical Issue 5 in the harsh review).** The harsh critic faults the paper for deferring implementation details (reward functions, optimizer equations, TTS computation) to appendices. Per hard rules: the parser strips appendix content from all papers; these sections exist in the original submission. Removed.
- **Claim that "the paper does not discuss known limitations of ES."** The paper explicitly discusses zeroth-order scaling limitations in Section 6 ("scaling with number of parameters can be a potential limitation... zeroth-order optimization method will cause an additional overhead"). The criticism is inaccurate. Removed.
- **Claim that the abstract claims "state-of-the-art performance."** The abstract says "competitive performance"; the SOTA claim appears in the introduction and conclusion. The reviewer slightly mischaracterized the abstract. Removed.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

- **Table 1:** Re-run dNPIM with the same evaluation protocol as baselines (report mean ± std across independent runs). If the parallel-trajectory "top 30" procedure is justified, include a separate column showing it, but ensure the baseline-aware comparison is the primary one.
- **Table 2:** Report wall-clock TTS (seconds on the same hardware) or FLOP-normalized TTS. Provide a profiling breakdown showing that the coupling-field matrix-vector product dominates per-iteration cost for all methods, or adjust the comparison accordingly.
- **Claims:** Qualify "state-of-the-art" by the specific comparison class (e.g., "among neural-network-tuned Ising machine algorithms" or "among learning-based methods for Max-Cut").
- **Training cost:** Add a brief paragraph (or appendix table) characterizing the training budget for each benchmark, and discuss the practical amortization scenario.

## Score and Decision

MY FINAL SCORE: <score>4</score>
MY FINAL DECISION: <decision>Reject</decision>