## Summary

This paper proposes StragglerAR, a novel ALLREDUCE algorithm that exploits natural variation in GPU execution times (straggler delays) by performing useful communication—a REDUCESCATTER among non-straggler GPUs—during the straggler-induced delay, rather than waiting synchronously. The algorithm achieves a $\beta$ cost approaching $s\beta$ (vs. $2s\beta$ for bandwidth-optimal synchronous algorithms) in the ideal case and converges to $2s\beta$ in the worst case. The theoretical analysis is clean, and hardware experiments on 8-GPU DGX servers demonstrate bandwidth improvements exceeding 25% in idealized microbenchmarks.

## Strengths

1. **Genuinely novel algorithmic insight.** The core idea—exploiting temporal asymmetry (variation in GPU completion times) rather than treating stragglers as an anomaly to be waited out—is a creative departure from decades of collective algorithm design. The paper correctly positions this as opening a new design dimension. The theoretical claim of surpassing the bandwidth-optimal synchronous ALLREDUCE lower bound by relaxing the synchronous-start assumption is properly contextualized (Abstract, §1, §3.2).

2. **Clean theoretical analysis with honest worst-case bounds.** Table 1 and the analysis in §3.2 are clear and rigorous. The best-case bandwidth complexity ($\sim s\beta$) genuinely improves on the $\sim 2s\beta$ of Ring/RHD, and the worst case ($\sim 2s\beta$ at scale) converges to baselines. This is an honest presentation—the algorithm does not hide a poor worst case. The critical-delay analysis (§4.1, §B) showing that the threshold for outperforming baselines *decreases* with cluster size is a valuable theoretical result.

3. **Real hardware results on two GPU generations.** The evaluation on DGX H100 and DGX A100 (Fig. 5) demonstrates genuine bandwidth improvements (>25% on 8-GPU servers) under controlled conditions with artificial stragglers, consistent across hardware generations. The use of the NCCL P2P API rather than a custom stack aids reproducibility.

4. **Honest limitations section.** The paper acknowledges key constraints: best performance with a single persistent straggler, power-of-two requirement, non-zero critical delay on small clusters, and the precondition overlap requirement. This candor is a strength.

## Weaknesses

### Fatal

None.

### Major

1. **Abstract claims are not calibrated to the evidence.** The abstract prominently states "On an 8-GPU server, StragglerAR provides a 25% speedup over state-of-the-art ALLREDUCE algorithms" without qualification. This 25% figure comes from the *optimistic-case microbenchmark* (Fig. 5a/5d), where the straggler delay is artificially introduced and fully masks the REDUCESCATTER precondition. The actual end-to-end training speedups on real LLMs (Table 2) are **2.39–4.75%**—an order of magnitude smaller. The paper body is transparent about this distinction, but the abstract gives a misleading impression of practical performance. The abstract should either state the end-to-end results or clearly qualify the 25% as an idealized microbenchmark bound. This is a presentation issue, not a flaw in the algorithm itself, but it materially affects how readers interpret the paper's contributions.

2. **The strongest scaling claims are simulation-only.** The claim of "nearly a $2\times$ speedup" at 256 GPUs (§4.3, Fig. 6c) is supported only by an $\alpha$-$\beta$ analytical model with a single set of parameters ($\alpha=3\mu$s, $\beta=1/450$ GB/s). While simulation is standard practice in this community for scaling beyond available hardware, the paper's most impressive quantitative result is unvalidated on real hardware. The paper acknowledges this ("as we lack access to hardware like NVIDIA's GB200"), but the claim deserves a sensitivity analysis over different $\alpha$ and $\beta$ values and a more prominent caveat.

### Minor

1. **Limited end-to-end evaluation.** The end-to-end experiments cover three LLMs (all ~3B parameters), on a single 8-GPU configuration, for only 100 iterations per model. The GPU-hours-saved projections (4.59–9.12 per day) are extrapolated from these 100 iterations without validating that the observed speedup is stable over time. This scope is sufficient for a proof-of-concept but limits generalizability.

2. **No decomposition of end-to-end speedups by iteration type.** The paper reports only average speedup (2–5%). Because the evaluation fixes a single straggler rank, some iterations encounter the algorithm's ideal case (profiled rank actually is the straggler) and others its worst case (different/no straggler). Reporting the per-iteration speedup distribution (e.g., a CDF) would clarify whether gains come from many small improvements or a few large ones, and would better characterize the robustness the paper claims.

3. **Average-case microbenchmark uses mean straggler delay without variance.** The "Average Case" (Fig. 5b/5e) uses mean delays of 4.48 ms (H100) and 9.46 ms (A100) from the Llama-3.2 experiments, but Fig. 2a shows the straggler delay distribution is wide (0–30 ms). The "average case" is only representative for iterations near the mean; reporting how performance varies across the delay distribution would strengthen this section.

### Trivial

None.

## Nice-to-Haves

- An end-to-end experiment with *dynamic* straggler detection (e.g., using the first $n-1$ ready ranks as non-stragglers, as suggested in the Limitations section) would significantly strengthen practical relevance.
- A sensitivity analysis of the 256-GPU simulation over different $\alpha$/$\beta$ values and straggler delay distributions would make the scaling claims more robust.
- A CDF of per-iteration speedups (or a similar decomposition) in the end-to-end results would help readers understand the gain mechanism.

## Removed Points

These points were flagged in the input but are removed with justification:

1. **"End-to-end evaluation methodology inflates the algorithm's apparent advantage"** (Critical Issue #3). The paper explicitly frames its static straggler-profiling methodology as a *stress test* (§4.2: "it stress-tests Straggler to encounter both ideal and worst-case conditions"). Fixing a single straggler rank means the algorithm encounters its worst case (no overlap) whenever a different rank is the actual straggler—making the measured 2–5% speedup a *conservative* estimate, not an inflated one. The critic's framing gets this backwards.

2. **"Schedule generation assumes a single specific straggler rank"** (Section-by-Section). The paper states at §3.1 (line 135): "Without loss of generality, we assume rank $n-1$ is the straggler in this section; however, by symmetry, the algorithm applies regardless of which rank is the straggler." This is addressed.

3. **"No sensitivity analysis for the critical delay"** (Section-by-Section). The paper provides the critical delay at the largest buffer size on two hardware platforms (Fig. 5c/5f), shows how the REDUCESCATTER time (which determines the critical delay) varies with buffer size (Figs. 6a/6b), and provides analysis in §B showing how critical delay scales with cluster size. While a full sensitivity surface is a nice-to-have, the paper does provide meaningful analysis.

4. **"Likelihood of two GPUs completing exactly simultaneously is deceptive"** (Section-by-Section). The paper uses this to argue worst-case scenarios are improbable, and this framing is reasonable for continuous random variables. The criticism that "two GPUs may complete within a few microseconds" does not undermine the argument, since the critical delay for large $n$ is shown to approach zero.

## Novel Insights

None beyond the paper's own contributions. The reviews surface a tension between the paper's novel algorithmic contribution and the calibration of its headline claims—the former is genuinely strong, the latter needs adjustment—but do not produce novel technical insights beyond what the paper itself articulates.

## Suggestions

1. **Recalibrate the abstract.** State the end-to-end speedups (2–5% on 8-GPU clusters) and qualify the 25% and 2× figures as idealized bounds achievable under favorable straggler conditions or at larger scales in simulation.

2. **Add a per-iteration decomposition** to the end-to-end results (e.g., a CDF of per-iteration speedups, or separate reporting for iterations where the profiled straggler was/was not the actual straggler).

3. **Add a sensitivity analysis** for the 256-GPU simulation, varying $\alpha$ and $\beta$ across realistic ranges for different hardware generations.

4. **Report straggler delay variance** alongside the mean used in the average-case microbenchmark.

## Score and Decision

MY FINAL SCORE: <score>7.0</score>
MY FINAL DECISION: <decision>Accept</decision>