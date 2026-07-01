## Summary

This paper proposes Neural Network Ising Machines (NPIM), a method that parameterizes the update dynamics of a dynamical Ising machine with a small MLP, using a temporal Fourier basis for time-varying weights, and trains it via zeroth-order optimization. The approach sits at a novel intersection of algorithm unrolling, Ising machine dynamics, and neural combinatorial optimization. The authors demonstrate competitive solution quality on both neural-CO benchmarks (MIS, MaxClique, MaxCut) and standard Ising machine benchmarks (G-set Max-Cut instances), and provide an honest analysis of failure modes and trade-offs between continuous (cNPIM) and discrete (dNPIM) coupling variants.

## Strengths

1. **Novel synthesis of algorithm unrolling with Ising machine dynamics (Section 3.3, Figure 1a).** Parameterizing the update function *F* of a dynamical Ising machine with a small MLP, using a temporal Fourier basis to allow time-varying weights, and training with zeroth-order optimization is genuinely distinct from prior neural-CO work. The Fourier basis parameterization (Eq. 6-7) is a clean way to allow smooth time variation without a parameter explosion, and the no-bias constraint to preserve odd symmetry is a thoughtful design choice.

2. **Honest and informative analysis of failure modes and trade-offs (Section 4.5, Figure 3b/e).** The paper transparently discusses that cNPIM overfits to easy instances and can fail on hard ones, while dNPIM is more robust but slower. The explanation — that continuous coupling may optimize a relaxed problem that misaligns with the true discrete objective — is substantive diagnostic analysis rather than hand-waving. The emergence of momentum-like dynamics from pure reward maximization (Section 4.1) is a genuinely insightful finding.

3. **Competitive solution quality on established benchmarks (Tables 1-2).** On the G-set (Table 2), dNPIM achieves the best median TTS on 3 of 5 instance types, often by a substantial margin (e.g., TTS of 5.51e4 vs 2.22e5 for CFC on N=800,T,+/-). On neural-CO benchmarks (Table 1), dNPIM achieves better average objective values than DiffUCO and LTFT on 4 of 5 problem settings. These results demonstrate that learned dynamics can compete with hand-designed Ising machine algorithms.

## Weaknesses

### Fatal

None.

### Major

1. **TTS reported in iterations rather than wall-clock time (Table 2, Section 5).** The paper reports time-to-solution in "units of number of iterations to solution," justifying this on the grounds that "the compute intensive matrix vector product is the computational bottleneck for each algorithm." However, NPIM adds an MLP forward pass at each iteration (nonlinear activations, matrix multiplications in the hidden layer) that is absent from baselines like CAC, CFC, and dSBM. The claim that the *Jx* product dominates would be true only if the MLP cost is negligible compared to *O*(*N*²), which depends on the problem size *N* relative to the network dimensions *D* and *T_c*. For moderate or smaller *N*, the per-iteration cost of NPIM is higher, and reporting TTS in iterations understates this. Without wall-clock TTS or an empirical demonstration that per-iteration costs are comparable at the tested problem sizes (*N*=800 for G-set), the paper's efficiency claims (abstract: "efficient and scalable") are incompletely supported.

2. **Training cost is not quantified (Sections 3.4, 4.3).** The method requires: (a) generating training instances matching the target distribution, (b) training with a zeroth-order method that maintains a *P × P* covariance matrix (where *P* grows with network size), (c) bootstrapping from easier instances, and (d) fine-tuning. For the G-set results, separate networks were trained for each graph type. None of this training cost is reported — not in epochs, GPU-hours, or number of function evaluations. The zeroth-order method's sample complexity scales poorly with *P* (acknowledged as a limitation in Section 6), but the main paper gives no sense of whether training takes minutes, hours, or days. The baselines (CAC, CFC, dSBM) require no training data or training time; a fair assessment of practical value requires knowing the total cost of deploying NPIM.

### Minor

1. **Large runtime gap on neural-CO benchmarks under-explained (Table 1).** On MIS-large and MaxCut-large, dNPIM takes 1:20 versus 0:02-0:03 for DiffUCO / SDDS — a 20-40× slowdown. The paper attributes this to the "sparse graph library used for the results in Sanokowski et al. (2025) as opposed to the dense PyTorch matrix-matrix product used in our implementation" and concludes "without further optimization it is unclear if this difference in speed is inherent to the algorithm or the implementation." Since both results are reported on the same A100 GPU, the dense product is an implementation choice, not a fixed algorithm property, leaving the reader uncertain about the significance of the runtime comparison. The "top 30" parallelization (running 30 trajectories and selecting the best) further complicates comparison with methods reporting single-trajectory results.

2. **Missing variance estimates for dNPIM results (Table 1).** All baseline methods (Gurobi, DiffUCO, SDDS) report ± standard deviations; dNPIM reports only point estimates. This is a trivially fixable omission that reduces comparability.

3. **Ambiguity in Figure 3b/e problem size.** The parser-extracted figure text indicates N=100 for subplots b/e, while the author-written caption (line 146) states N=800 for the same subplots. This discrepancy needs resolution, as it affects interpretation of the method's scaling behavior.

### Trivial

None.

## Nice-to-Haves

- **Report wall-clock TTS for Table 2.** Running all methods on the same A100 GPU and reporting actual seconds (or milliseconds) to reach 99% success probability would directly validate or qualify the efficiency claim. If per-iteration cost is indeed dominated by the matrix-vector product for *N*=800, this should be empirically demonstrated.
- **Provide instance-level variance for G-set results (Table 2).** The paper references Table 4 in the appendix for instance-wise performance, but including distributional information (e.g., quartiles) in the main table would strengthen the presentation.
- **Ablate the zeroth-order method against alternatives.** The paper argues (Section 2.4, Appendix E) that backpropagation and policy gradient are infeasible; empirical evidence of this failure would strengthen that case.

## Removed Points

These points are flagged to be removed; treat them with caution.

- **Criticism about "algorithm unrolling" framing being too loose.** The reviewer noted that classical algorithm unrolling (e.g., LISTA) starts from a specific iterative algorithm, while NPIM's MLP learns dynamics from scratch. However, the paper unrolls the general Ising machine formulation (Eq. 2-3) by adding learnable parameters, which is a valid and clearly described instantiation. Removed as a strawman — the paper's framing is reasonable.

- **Concern about abstract potentially misleading readers about comparison breadth.** The abstract states the method is compared against "state-of-the-art neural-CO approaches as well as other classical Max-Cut/Ising algorithms." The paper does exactly this (Table 1: neural CO approaches; Table 2: Ising machine algorithms). Removal justified because the comparison is accurately described.

- **Criticism about missing broader baseline comparison for G-set (e.g., Breakout Local Search).** The reviewer acknowledged this is "not a flaw per se" since the paper positions itself within the Ising machine literature. Removed per filter rule — demanding comparisons outside the paper's stated scope is scope creep.

## Novel Insights

The reviewer's analysis surfaces a genuine tension in the paper: the method's novelty and solution quality are well-supported, but its efficiency claim rests on an unvalidated assumption about per-iteration cost parity. This distinction — between "can achieve competitive solution quality" and "is efficient" — is worth making explicit. The paper convincingly shows the former; the latter needs stronger evidence. The emergence of momentum-like dynamics from pure reward maximization, documented in the single-layer analysis, is a genuinely novel observation that deserves more attention in the main narrative, as it suggests learned Ising machine dynamics can rediscover physically meaningful search strategies.

## Suggestions

1. Report wall-clock TTS for Table 2 (or provide per-iteration timing breakdowns showing that the MLP overhead is negligible at the tested *N*).
2. Report training cost (GPU-hours and/or total function evaluations) for the G-set results to allow readers to assess the method's total computational budget.
3. Resolve the N=100 vs N=800 ambiguity in Figure 3's description.
4. Include variance estimates for dNPIM in Table 1.
5. Clarify the "top 30" parallelization — report whether the baselines would also benefit from running multiple parallel trajectories, or adjust the comparison protocol accordingly.

## Score and Decision

MY FINAL SCORE: <score>7.0</score>
MY FINAL DECISION: <decision>Accept</decision>