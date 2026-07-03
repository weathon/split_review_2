Now let me write the final consolidated review.

## Summary

CoRAL proposes a modular neuro-symbolic framework for contact-rich robotic manipulation that integrates FoundationPose (6-DoF pose tracking), GPT-4o (as a VLM for physical parameter estimation and as an LLM for cost function/contact strategy generation), and an MPPI controller. The key architectural innovations are: (1) the LLM generates the mathematical structure and weights of the MPPI cost function itself (not just sub-goals or cost maps, as in prior work like IMPACT/VLMPC); (2) explicit separation of VLM (perception) and LLM (reasoning) roles; (3) an outer-loop LLM-driven refinement mechanism for online adaptation; and (4) a memory unit for experience reuse. The framework is evaluated on 6 simulated contact-rich tasks against VLA baselines (OpenVLA-OFT, π₀.₅) and human-expert-designed cost baselines.

## Strengths

1. **LLM generates the cost function structure for MPPI directly** (Section 3.2, Eq. 2). Unlike prior work where foundation models provide perceptual guidance (IMPACT: cost maps; VLMPC: sub-goals), CoRAL's LLM outputs the mathematical form and weights of the optimization objective itself. This is a structural advance over existing foundation-model-plus-planner integrations, grounding abstract reasoning directly in the optimal control problem.

2. **Ablation evidence for role separation is striking**. The Unified VLM ablation (single model for perception and planning) collapses to 0/10 on 4 of 6 tasks and only 2/10 on a fifth (Table 1). This provides direct quantitative support for the paper's central architectural claim — separating VLM and LLM roles is empirically necessary, not just a design preference.

3. **LLM-guided contact strategy produces large, measurable efficiency gains**. In the Flip with Wall task (Section 4.1.4), the LLM-provided contact strategy makes execution 83.9% faster (32 vs. 199 steps) with a 63.9% shorter end-effector path (1.33 m vs. 3.69 m) compared to using only the cost function. These are concrete figures from a controlled ablation.

4. **Online parameter adaptation recovers from severe mis-estimation**. When mass was intentionally set to 20× the true value (2.0 kg vs. 0.1 kg) and friction to nearly double (0.9 vs. 0.5), the outer-loop LLM-driven correction converged both parameters close to true values (Section 4.1.4, Figure 4). This demonstrates a failure-recovery mechanism that end-to-end VLA systems lack.

5. **Memory unit provides a measurable, transferable improvement**. Adding the memory unit raises success from 2/10 to 4/10 on T1 (Push & Pick Board) and from 5/10 to 7/10 on T6 (Flip with Wall), with evidence that a "push-to-edge" strategy is retrieved and reused (Section 4.1.3).

## Weaknesses

### Fatal

None.

### Major

1. **Statistical power is too low to support the ablation conclusions reliably**. Every result is based on 10 trials per condition with no confidence intervals, standard deviations, or statistical significance tests. With 10 Bernoulli trials, the 95% confidence interval for a 40% success rate spans roughly 12–74%. Key claims about component contributions (memory benefit on T1: 4/10 vs 2/10; refinement benefit on T1: 4/10 vs 0/10) rest on differences of 2–4 successes, which are well within the noise range of the measurement. Completion times are reported as point estimates without variance. For a paper that makes comparative claims about which components matter and by how much, this level of statistical support is insufficient.

2. **VLA comparison is informative but oversold**. The VLA baselines (OpenVLA-OFT, π₀.₅) are evaluated using LIBERO checkpoints on tasks T1, T4, T5, T6 — custom tasks outside the LIBERO distribution. Their near-zero performance on these tasks is predictable: they are being tested out-of-distribution. This comparison does demonstrate that fixed-weight VLA policies fail to generalize to novel contact-rich tasks, which is a legitimate (if expected) finding. However, the paper frames this as "significantly outperforming" the baselines (Section 4.1.1) without adequately qualifying that this is a comparison between "LLM-with-in-context-adaptation" and "fixed-policy" approaches, where the asymmetry structurally favors CoRAL. The claim the paper can legitimately make from this data is narrower than what it asserts.

### Minor

3. **Sim-to-real robustness claims are untested**. The paper invokes the sim-to-real gap as a motivation (Section 3.3: "robustness against the inherent sim-to-real gap") and tests robustness only by intentionally mis-specifying parameters within the same simulator (Section 4.1.4). This is a valid test of robustness to model parameter mismatch, but it is not a test of sim-to-real transfer, which involves unmodeled friction, stiction, actuator limits, sensor noise, calibration errors, and deformation. The absence of any real-robot experiment limits the scope of what the sim-to-real claims can substantiate.

4. **Unified VLM ablation may be confounded with pose estimation**. The paper defines "Unified VLM" as using a single multimodal prompt for both perception and planning (Section 4.1.3), but does not clearly specify whether FoundationPose is retained or removed. If Unified VLM also discards FoundationPose, its catastrophic failure (0/10 on most tasks) could be driven by poor pose estimation rather than the lack of role separation. The "w/o Pose Tracking" ablation (also removing FoundationPose) shows similarly catastrophic failure. This confound weakens the diagnostic value of the Unified VLM ablation for the specific claim about role separation.

5. **VLM physical parameter estimation is unevaluated**. The system relies on GPT-4o to estimate mass and friction from RGB-D appearance (Section 3.1) — a fundamentally ill-posed problem. The paper provides no evaluation of estimate accuracy, nor any analysis of failure cases where the VLM is confidently wrong but execution provides no clear error signal for the outer loop to correct. While the outer-loop adaptation can fix bad estimates, this only works when the failure signal is informative and the adaptation loop is triggered.

6. **LLM output reliability for cost function generation is uncharacterized**. The system depends on GPT-4o generating syntactically and semantically valid cost functions (Section 3.2, Eq. 2). The paper provides no analysis of how often the LLM produces invalid, malformed, or internally consistent but counterproductive cost functions. For a system whose core pipeline includes LLM-generated optimization code, this is an important reliability question.

7. **No sensitivity analysis for key hyperparameters**. N_retry=15, MPPI temperature λ=0.1, sample count K=200, planning horizon H=50 — none are varied. The reader cannot assess how robust the system is to these choices.

8. **Latency is noted but not analyzed**. CoRAL takes 45s on T2 vs. OpenVLA's 5s (Table 1). The paper mentions latency as a limitation (Section 5) but provides no breakdown of wall-clock time by component (perception, LLM API call, MPPI optimization), nor the cost of the outer-loop refinement in terms of API calls or time.

9. **Explainability claims are supported only by anecdote**. The paper presents a single natural-language diagnosis example (Section 4.1.4) and claims this as a key advantage. No evaluation of explanation faithfulness or correctness is provided. This is a promissory claim, not a demonstrated property.

### Trivial

None.

## Nice-to-Haves

- An evaluation of VLM physical parameter estimation accuracy against ground truth, and an analysis of failure modes where incorrect estimates cannot be corrected by the outer loop.
- Per-component latency breakdown and total API call cost.
- Sensitivity analysis on key hyperparameters (N_retry, λ, K, H).

## Removed Points

*These points were raised by reviewers but removed after cross-checking against the paper.*

- **"CoRAL does not outperform human-engineered baselines, and this is obscured by framing"** — Removed. The paper explicitly acknowledges this (Section 4.1.2: "while remaining below the FSM upper bound") and frames its contribution as automating cost-function design, not surpassing human experts. This is an honest characterization.
- **"Missing discussion of classical contact-rich optimization approaches"** — Removed. The paper's related work appropriately focuses on foundation-model approaches. Scope-creep to demand coverage of complementarity-based methods or contact-implicit optimization is not justified.
- **"Mass/friction inference from appearance is audacious"** — Demoted from standalone weakness to Minor Weakness #5, since the adaptation mechanism partially addresses this concern and the critic's framing was too strong for a claim that is acknowledged to be a heuristic.
- **"The comparison is between LLM-with-adaptation vs. fixed-weight policy, which is fundamentally asymmetric"** — Removed as a standalone criticism. This asymmetry is precisely the paper's thesis. The comparison is legitimate for demonstrating that the modular adaptive architecture succeeds where fixed-weight policies fail. The framing concern is captured in Major Weakness #2.
- **"VLM has ingested robotics content during pre-training"** — Removed. Speculative and unverifiable. All pre-trained models have ingested web data; this is not a meaningful criticism of one system over another.

## Novel Insights

None beyond the paper's own contributions. The synthesis of reviews surfaces no pattern or failure mode that the paper itself does not already identify or that would redirect its contribution.

## Suggestions

1. Increase trial count (to at least 50 per condition) and report confidence intervals or Bayesian credible intervals for all success rates and completion times. Without this, the ablation conclusions are not statistically grounded.
2. Run at least one real-robot experiment to substantiate the sim-to-real robustness claims that the paper makes. Alternately, clearly scope the claims to "robustness to parameter mis-specification within simulation" rather than "sim-to-real."
3. Clarify the Unified VLM ablation design — explicitly state whether FoundationPose is retained — and add an ablation that keeps FoundationPose while merging VLM/LLM roles to genuinely test role separation without confounds.
4. Provide reliability statistics for LLM-generated cost functions (syntactic validity rate, fraction leading to solvable MPPI problems, qualitative analysis of failure modes).
5. Include a sensitivity analysis for key hyperparameters (N_retry, λ, K, H).
6. Provide a per-component latency and API-cost breakdown for the pipeline.

## Score and Decision

Based on my analysis of the paper and the reviewer inputs, the paper proposes a genuinely novel architecture (LLM-generated MPPI cost functions) with informative ablation studies supporting its design choices. However, the evaluation has significant limitations — insufficient statistical power, an oversold VLA comparison, simulation-only validation for sim-to-real claims, and a confounded ablation — that prevent full confidence in the results. The contribution is real but the evidence is not yet at the level needed for acceptance.

After careful calibration, I assess the paper as between borderline reject and borderline accept. The core idea is strong and well-motivated, and the paper is clearly written, but the evaluation needs substantial strengthening (more trials, finer-grained ablations, real-robot validation) to fully establish the claims.

MY FINAL SCORE: <score>5.5</score>
MY FINAL DECISION: <decision>Reject</decision>