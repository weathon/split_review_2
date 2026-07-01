## Summary

The paper introduces StragglerAR, a novel AllReduce algorithm that exploits natural variation in GPU execution times (straggler delays) to achieve speedups over traditional bandwidth-optimal algorithms. The key idea is to perform a ReduceScatter among non-straggler GPUs during the straggler delay, then execute a carefully designed schedule to complete the AllReduce. The paper provides theoretical analysis showing up to 2× bandwidth reduction compared to the synchronous lower bound, and presents experiments on 8-GPU DGX servers demonstrating 25% speedups over Ring in ideal conditions and end-to-end training improvements of 2–5% for LLM fine-tuning.

## Strengths

1. **Novel and well-motivated idea.** Exploiting temporal asymmetry in GPU execution times is a fresh perspective on collective communication. The paper provides strong empirical evidence from Llama fine-tuning that straggler delays of up to 30 ms occur regularly even within multi-GPU servers, motivating the approach.

2. **Solid theoretical analysis.** The paper derives communication complexity for StragglerAR in both best-case (\(n + \log n - 2\) rounds, \(\frac{n+\log n-2}{n-1}s\beta\)) and worst-case (matching the \(2s\beta\) baseline at scale) scenarios, and proves the algorithm's correctness. The observation that the critical delay decreases with cluster size is insightful.

3. **Clear experimental validation on real hardware.** The paper benchmarks StragglerAR on DGX H100 and A100 servers against multiple baselines (Ring, RHD, MSCCL, Broadcast) using a fair implementation, and demonstrates consistent bandwidth improvements for large buffer sizes. The end-to-end LLM training experiments show practical speedups.

4. **Well-written and structured.** The paper clearly explains the core insight, the algorithm design, the cost model, and the experimental methodology. Figures 1 and 4 effectively illustrate the algorithm's operation.

## Weaknesses

### Major

1. **The claim of surpassing the bandwidth-optimal lower bound requires more careful framing.** The paper states it "surpasses the decades-old lower bound for bandwidth-optimal synchronous ALLREDUCE by leveraging the asymmetry in when GPUs reach the synchronization barrier." While technically correct when the ReduceScatter is fully overlapped with the straggler delay, the bound is for the case where all GPUs start simultaneously. Exploiting a delayed participant changes the effective problem size (one fewer GPU during the initial phase). The authors should clarify whether this truly constitutes surpassing a fundamental bound or solving a slightly different problem.

2. **Reliance on knowing which rank is the straggler.** The end-to-end evaluation uses a static straggler identified via profiling. The paper acknowledges this limitation and argues that dynamic detection could improve performance, but does not implement or evaluate any online detection mechanism. For practical deployment, a robust method to handle dynamic stragglers is essential. The eager execution approach (starting ReduceScatter as soon as the first \(n-1\) ranks are ready) mitigates this for the worst case, but the paper does not demonstrate this variant experimentally.

3. **Real hardware experiments limited to 8 GPUs.** The scaling results beyond 8 GPUs rely on simulation using the \(\alpha\)-\(\beta\) model. While simulation is a standard methodology and the model is validated on 8-GPU experiments, real experiments on larger scale-up domains (e.g., 32 or 64 GPUs) would significantly strengthen the claims of \(2\times\) speedup at scale. The paper would benefit from at least one data point on a larger system.

### Minor

4. **Naming inconsistency.** The title and abstract use "StragglerAR," while the body (starting from Section 1) uses "StraggLAR" (e.g., "StragglerAR" vs "StraggLAR"). This inconsistency should be resolved.

5. **Limited end-to-end training iterations.** The LLM experiments run only 100 iterations. Longer runs (e.g., 1000+ iterations) would better capture straggler dynamics and provide more reliable speedup estimates. The extrapolation to "GPU-hours saved per day" is based on 100 iterations and may not be representative.

6. **Algorithm complexity for latency-sensitive settings.** StragglerAR uses \(n + \log n - 2\) rounds, while Ring uses \(2(n-1)\) rounds with pipelining, leading to higher latency (\(\alpha\)) cost for small \(n\). The paper acknowledges this and focuses on bandwidth-bound scenarios, but the crossover point where StragglerAR becomes beneficial for small buffers could be discussed more explicitly.

### Trivial

7. **Figure legends.** In Figure 5, the algorithm is labeled "StraggIAR" (missing 'r') in the plot, which is inconsistent with the text.

## Nice-to-Haves

- Release the code for the schedule generator and runtime to enable reproducibility.
- Implement and evaluate a simple online straggler detection mechanism (e.g., using NCCL's barrier timing or start-of-collective triggers).
- Include experiments with multi-node AllReduce to assess the impact of network stragglers.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. Discuss the claim of surpassing the lower bound more precisely, clarifying that the bound is for the synchronous case and that StragglerAR exploits a different problem setting (delayed participant) to achieve lower effective bandwidth cost.

2. Implement an eager conditional execution variant where the ReduceScatter begins as soon as the first \(n-1\) ranks are ready, and evaluate its performance in end-to-end settings with dynamic stragglers. This would directly address the major weakness regarding straggler detection.

3. Fix the naming inconsistency throughout the paper (StragglerAR vs. StraggLAR) and correct the typo in Figure 5's legend.

## Score and Decision

The paper presents a genuinely novel algorithmic contribution with a strong theoretical basis and promising experimental results on real hardware. The main limitations are the framing of the lower-bound claim, the reliance on static straggler detection, and the small scale of real experiments. For a top ML venue, these are addressable concerns. The paper's strengths outweigh its weaknesses.

MY FINAL SCORE: <score>6</score>
MY FINAL DECISION: <decision>Accept</decision>