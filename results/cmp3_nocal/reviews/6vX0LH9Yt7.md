## Summary

This paper proposes a hybrid neural-MPM system for interactive fluid simulation and control. The system combines (1) a GNN-based neural physics simulator operating at low spatiotemporal resolution, (2) a fallback mechanism to classical MPM when fluid complexity rises above a threshold, and (3) a diffusion-based generative controller trained via a reverse simulation strategy to produce external force fields from user sketches. Experiments are conducted on seven 2D/3D scenarios covering water, sand, ramps, and multiphase interactions.

## Strengths

1. **Reverse simulation strategy for training data generation (Sec. 3.2.2).** The idea of running forward MPM simulations and then solving for the force fields that would reverse them — thereby producing paired sketch→force-field training data without manual annotation — is creative and addresses a genuine bottleneck in learning-based fluid control. This is concretely described with Equation 3 and Figure 8.

2. **Broad scenario coverage (Table 2).** The method is tested on seven simulation domains spanning 2D/3D, water, sand, ramps, and Water-Sand interactions, with 1,000 trajectories per domain. This provides reasonable evidence that the approach is not narrowly tuned to a single setting.

3. **Systematic ablation of the hybrid threshold (Table 1, Figure 6).** The paper varies the fallback threshold r_c and shows the resulting trade-off between RMSE_m and latency, making the design choice of r_c=0.8 transparent and reproducible. The full sweep from r_c=0.0 to r_c=0.9 is presented.

## Weaknesses

### Fatal

None.

### Major

1. **The "real-time" claim is not consistently supported by the presented timing data.** The paper's title, abstract, and introduction all assert real-time performance. However, the timing data shows mixed support:
   - For Water-Sand 2D (the most complex scenario), Section 4.2 states the hybrid solver accelerates MPM "from 0.114s per frame to 0.08s" — 80ms per frame is ~12.5 FPS, well below the 30–60 FPS standard for real-time. Notably, even the baseline MPM at 0.114s/frame (~8.8 FPS) is not real-time, so the 29.8% relative improvement does not cross the real-time threshold.
   - For all other scenarios, timing is reported as "ms per step" (Table 1, Figure 10) with no stated simulation-step-to-rendered-frame ratio. For example, Sand 3D at 0.90ms/step could support real-time if, say, 10 steps produce one frame (9ms/frame = ~111 FPS), but the paper never specifies this mapping. Without it, the per-step numbers cannot be interpreted as frame rates.
   - The abstract and title are unqualified, yet the system clearly does not achieve real-time performance uniformly across all tested scenarios.

2. **The fluid control evaluation is insufficient to validate the claimed capabilities.** The diffusion-based Fluid ControlNet (Sec. 3.2.3) is a core contribution, but its evaluation (Sec. 4.3, Table 3) has several gaps:
   - **Single weak baseline:** The only comparator is a constant force field with magnitude and orientation solved from the start-to-end displacement — any learned model producing spatially varying forces should outperform this.
   - **No sketch-adherence metric:** The paper's stated use case (Sec. 3.2.1) is that "a user would like to draw a simple sketch... following which the fluid particles should move." Yet the evaluation only measures grid RMSE at the final time step, which tests whether particles end up in the right final configuration, not whether they follow the user's drawn arrow or fill the drawn oval. No metric directly measures sketch fidelity.
   - **No timing of the diffusion model:** The inference latency of the generative controller is never reported. If generating a force field takes seconds per control step, the "interactive" claim fails regardless of accuracy.
   - **No uncertainty quantification:** All reported metrics (Table 1, Table 3, Figure 10) appear to be point estimates without variance, confidence intervals, or significance tests across multiple runs.

### Minor

1. **The hybrid simulator comparison omits the most revealing baseline from the main figure.** Figure 10 includes full-resolution neural physics, full-resolution MPM, and low-resolution MPM, but does not include the pure low-resolution neural physics without the MPM fallback (the r_c=0 case from Table 1). Including this would honestly show the trade-off introduced by the hybrid mechanism (e.g., for Water 2D: r_c=0 gives RMSE=0.0232 at 0.4048ms; hybrid at r_c=0.8 gives RMSE=0.0169 at 0.6966ms — a 27% error reduction at 72% latency cost). The data exists in Table 1, but its absence from the main comparison figure makes the evaluation look more favorable than a complete picture would.

2. **The fluid complexity trigger relies on a modest signal.** The fallback trigger uses cosine similarity of particle accelerations over a window, with a reported Spearman correlation of only -0.3902 against simulation error (Figure 5). The paper does not analyze the precision/recall or false-positive/negative rate of this trigger, nor compare against alternative complexity measures beyond noting that velocity divergence is more expensive to compute. While a -0.39 correlation is not useless in a complex physical system, the lack of diagnostic analysis makes it difficult to assess how often the trigger fires unnecessarily (adding latency) or misses error accumulation (undermining accuracy).

3. **No discussion of limitations or failure cases.** The paper acknowledges no scenario where the hybrid approach struggles, where the fallback trigger fails, or where the diffusion controller produces poor force fields. For a systems paper integrating multiple components, this omission limits the reader's ability to assess the method's适用范围.

4. **Overclaim in the conclusion.** Line 300 states the system achieved fluid dynamics "without sacrificing accuracy." This is imprecise — the hybrid system does sacrifice accuracy relative to full MPM (the gold standard), trading it for speed. This is the explicit design choice, and describing it as "without sacrificing accuracy" misrepresents the trade-off.

### Trivial

1. **Undefined term "MPN."** The paper uses "MPN" (Section 3.1.2, appearing at lines 127, 129, 131, 140, 142, 144) in contexts where "MPM" is clearly intended. The term MPM is defined in Section 2.1; "MPN" is never defined. This appears to be a drafting error. **Fix:** Replace "MPN" with "MPM" throughout Section 3.1.2.

## Nice-to-Haves

- Report the inference latency of the diffusion-based Fluid ControlNet to support the "interactive" claim.
- Include the r_c=0 (pure low-resolution neural physics) baseline directly in Figure 10 for a complete visual comparison.
- Add variance or confidence intervals to all reported metrics.
- Compare against at least one additional learned simulation approach (the paper cites Neural SPH and MPMNet in the related work section but does not compare against them).

## Removed Points

These points are flagged to be removed, treat them with caution:

1. **Grid RMSE_m is a lossy metric that may not reflect particle-level accuracy.** The paper acknowledges this limitation in Section 3.1.1 ("we will lose the particle-wise correspondence...we use a normalized grid-level RMSE_m") and explicitly follows prior work (Huang et al., 2021). This is a transparent design choice, not an unaddressed weakness. **Reason for removal:** The paper already addresses this concern and follows established methodology.

2. **Equation 3 (reversed simulation) physical interpretability concern.** The harsh critic questions whether the solved acceleration produces physically realizable trajectories. The paper describes it as "a physically interpretable approximation" (line 172), which is appropriate for generating training data for a learned model. No concrete error in the derivation is demonstrated. **Reason for removal:** Speculative concern without demonstrated error in the paper.

3. **Q1/Q2 framed too broadly.** The criticism that the paper's research questions are broader than the experimental support is generic and applies to most papers posing general research questions. The contributions are appropriately scoped. **Reason for removal:** Generic criticism, not a concrete weakness specific to this paper.

4. **"Improves both latency and errors" on 3D is due to resolution reduction.** The comparison is between the full proposed hybrid system (reduced resolution + MPM fallback) and the original full-resolution neural physics baseline. This is a valid system-level comparison even if part of the gain comes from resolution reduction — that is part of the method design. **Reason for removal:** The comparison is valid as an ablation of the complete system versus the original baseline.

5. **Missing comparison with recent learned simulators.** Implementing and fairly comparing against Neural SPH, MPMNet, and subequivariant GNNs is a substantial undertaking that extends well beyond standard expectations for a conference submission. **Reason for removal:** Scope-creep; the paper already compares against the most standard baseline (GNS/Sanchez-Gonzalez et al., 2020).

6. **Per-step timing is fundamentally uninterpretable.** The critic originally claimed timing could not be interpreted because the step-to-frame ratio was unknown. However, the paper does report "per frame" timing for Water-Sand 2D (0.08s), and the per-step times for other scenarios (0.4–1.6ms) are fast enough to support real-time if a reasonable step-to-frame ratio is assumed. The remaining valid concern (inconsistency, lack of explicit ratio) is preserved in Major weakness #1. **Reason for removal:** The original framing overstates the issue; the substantiated concern is already captured.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. **Clarify the "real-time" claim:** Specify which scenarios achieve real-time (and by what definition — e.g., ≥30 FPS). Report frame rates (FPS) rather than or in addition to per-step timing. State the simulation-step-to-rendered-frame ratio explicitly. Qualify the title or abstract if the hardest scenario (Water-Sand 2D) only achieves interactive (not real-time) rates.

2. **Strengthen fluid control evaluation:** (a) Add a metric that directly measures sketch adherence (e.g., average particle-to-sketch distance for arrows, IoU of particle cloud with drawn oval). (b) Report the inference latency of the diffusion model. (c) Add error bars or confidence intervals across multiple runs. (d) Consider at least one more baseline beyond the constant-force heuristic.

3. **Include the r_c=0 baseline in Figure 10** to honestly depict the trade-off introduced by the hybrid mechanism.

4. **Analyze the fallback trigger more rigorously** — report precision/recall or false-positive/negative rates for the cosine similarity threshold.

5. **Add a limitations section** to discuss scenarios where the hybrid approach may struggle or the trigger may fail.

6. **Fix the "MPN" → "MPM" typos** and rephrase the "without sacrificing accuracy" language in the conclusion to accurately reflect the accuracy-speed trade-off.

## Score and Decision

MY FINAL SCORE: <score>5</score>
MY FINAL DECISION: <decision>Reject</decision>