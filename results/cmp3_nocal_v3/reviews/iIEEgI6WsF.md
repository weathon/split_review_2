## Summary

This paper identifies that FSDP's per-layer collective synchronization creates unnecessary inefficiency under the workload-imbalanced regimes of LLM post-training (SFT and RL), where sequence length variation causes persistent straggler effects. The authors propose On-Demand Communication (ODC), which retrofits parameter-server-style point-to-point communication into FSDP by replacing all-gather/reduce-scatter with gather/scatter-accumulate primitives. This relaxes synchronization from per-layer to per-minibatch granularity and enables simpler minibatch-level load balancing. Evaluations across 1.5B–32B models on SFT and RL tasks show consistent throughput improvements (up to 36% over standard FSDP), with a parametric study characterizing when the advantage is largest.

## Strengths

- **Problem diagnosis is compelling and formally grounded (Section 1, Section 2.2).** Equation (1) cleanly captures how per-layer max-over-devices accumulates idle time, and the identification of this as a root-cause issue rather than a packing-solution problem is well-argued.

- **Proposed solution is conceptually clean and minimally invasive (Section 3, Section 3.1).** ODC replaces only the communication primitives within the existing FSDP layout, preserving memory efficiency, sharding, and synchronous minibatch semantics. The reframing of FSDP as a decentralized parameter server (Figure 6) places the contribution in a well-understood design space.

- **Evaluation covers a usefully diverse range of configurations (Section 5.1–5.2).** The paper tests 1.5B–32B models across SFT (two datasets with different length distributions) and RL on up to 32 GPUs, broader than typical single-setting systems evaluations.

- **Parametric study (Section 5.3, Figure 10) is well-designed and informative.** Varying one factor at a time from a golden setting reveals when ODC's advantage is largest (high sequence length, high device count, moderate minibatch size) and when it erodes (high packing ratios), enabling readers to judge applicability to their own settings.

- **The paper is forthright about its limitations (Section 5.4, Section 6.1).** It does not hide that ODC's point-to-point primitives are significantly slower than collectives across nodes (Figure 11), and provides a reasoned discussion of why this does not dominate in practice (overlapping with O(s²) computation; hybrid sharding as a fallback).

## Weaknesses

### Fatal
None.

### Major

- **No variance or error bars on any throughput measurement (Section 5.2, Figures 8–10).** Every throughput number is reported as a single point. Systems benchmarks on GPU clusters are subject to thermal, power, and OS-level jitter that can shift runtimes by several percent. Without multiple runs or at minimum variance estimates, the reader cannot distinguish genuine improvement from measurement noise. This is especially consequential for the RL experiments (Figure 9), where the claimed speedup is only "up to 10%" — well within typical run-to-run variance in distributed training. The parametric study curves (Figure 10) could also be partially artifacts of single-run measurement.

### Minor

- **"Collective LB-Mini" inconsistency between text and Figure 8 (Section 5.1).** The text (line 179) explicitly states: "As LB-Mini can produce different number of microbatches for different devices, it applies only to ODC." Yet Figure 8's legend lists "Collective LB-Mini (purple triangles)" as one of the compared methods. This is contradictory. The authors must clarify whether this is (a) a legitimate baseline where LB-Mini's minibatch-level balancing is constrained to equal microbatches and run under collectives (requiring text correction), or (b) a labeling error in the figure.

- **RL throughput metric is partial but axis label is unqualified (Section 5.1, Figure 9).** The paper states "we only record the model training time in RL, ignoring forward-only parts like actor rollout" (line 163). However, the y-axis of Figure 9 is labeled "Samples per Second" without this caveat. A reader would naturally interpret this as end-to-end RL throughput. If training is only a fraction of total RL time, the 10% training speedup may translate to a much smaller end-to-end improvement. The metric should be renamed or clearly caveated.

- **50% idle time claim lacks concrete evidence in the main text (Section 1).** The paper states that workload imbalance can cause "device idle times of up to 50%" but defers the evidence entirely to Table 6 in the appendix. For a key motivational claim, at least one concrete configuration and measurement should appear in the main paper so that readers can assess the severity directly.

### Trivial

- **LB-Micro description is vague (Section 5.1).** The algorithm is described only as "a heuristic-based packing baseline designed to minimize workload imbalance across devices within the same microbatch" without specifying what heuristic is used. The details are deferred to Appendix C, but a brief sketch in the main text would improve readability.

## Nice-to-Haves

- The communication primitive benchmark (Figure 11) tests ODC primitives synchronously with barriers — described as a "fairness" measure. This is the worst-case mode for ODC. Running the benchmark in the actual operating mode (asynchronous, overlapped) would give a more informative picture of the bandwidth tradeoff.

- An end-to-end RL measurement (training + rollout) for at least one configuration would contextualize the "up to 10%" training-only speedup and substantiate the RL claim more strongly.

## Removed Points

These points from the input review are flagged for removal; treat them with caution:

- **Critique that the communication primitive benchmark is unfair because it tests synchronous mode.** The paper is transparent about this methodology (Section 5.4: "ODC primitives are launched synchronously... with barriers inserted before and after each primitive") and explains in Section 6.1 why this does not dominate in practice (computation-communication overlap, hybrid sharding). The benchmark's purpose is to isolate raw bandwidth honestly; the system-level results are already presented in Figures 8–10.

- **Request for comparison against asynchronous FSDP variants or other imbalance-handling strategies beyond packing.** The paper's stated scope is comparing ODC against standard FSDP with multiple packing strategies (LocalSort, LB-Micro). This covers the primary alternatives used in LLM post-training. Requesting additional baselines beyond this scope is not a core weakness.

- **"Strengthening the Paper on Its Own Terms" suggestions** (variance bars, LB-Mini clarification, RL end-to-end measurement) — these are already captured in the Major/Minor weaknesses above rather than being separate points. The "Collective LB-Mini" clarification request in the Strengthening section is also redundant with the Minor weakness above.

## Novel Insights

None beyond the paper's own contributions. The review process did not surface any fundamentally new analytical perspective that the paper itself does not already articulate.

## Suggestions

1. **Add variance estimates.** Run each configuration at least 3 times with different random seeds and report mean ± std or min/max intervals. This is the single highest-leverage improvement.
2. **Resolve the "Collective LB-Mini" labeling issue** in Figure 8 and ensure the text and figure are consistent.
3. **Rename or caveat the RL metric** in Figure 9 (e.g., "Training Samples per Second") and provide context on what fraction of total RL pipeline time training constitutes.
4. **Include one concrete example** supporting the 50% idle time claim in the main paper (e.g., a footnote or brief entry in Table 1).
5. **Add a brief algorithmic sketch of LB-Mini** to Section 4 rather than deferring it entirely to Appendix C.

## Score and Decision

This paper makes a genuinely insightful contribution: the diagnosis that FSDP's per-layer collectives are a poor fit for imbalanced LLM post-training workloads is correct and well-motivated, and the proposed ODC scheme is a clean, minimally invasive fix. The evaluation covers a commendable range of configurations and includes a thoughtful parametric study. The paper is also refreshingly honest about its limitations.

However, the lack of any variance or error-bar reporting on throughput measurements is a significant evidential gap for a systems paper claiming speedups — particularly for the RL experiments where the margin is only 10%. The "Collective LB-Mini" inconsistency and the unqualified RL metric labeling also need resolution. These are fixable issues; the core idea is sound and the contribution is solid.

**MY FINAL SCORE: <score>6</score>**
**MY FINAL DECISION: <decision>Accept</decision>**