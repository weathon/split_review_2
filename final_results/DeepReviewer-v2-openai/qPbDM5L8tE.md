## Summary
# Final Review Report

## Summary

This paper presents CoRAL (Contact-Rich Adaptive LLM-based Control), a modular framework that integrates a Vision-Language Model (VLM), a Large Language Model (LLM), and a Model Predictive Path Integral (MPPI) controller for zero-shot contact-rich robotic manipulation. The key idea is to explicitly separate perception (VLM for pose tracking and physical parameter estimation) from reasoning (LLM for cost function generation and contact strategy formulation), with the LLM's output directly grounding the MPPI controller's optimization problem. The framework includes an inner loop (high-frequency MPPI re-planning with reactive feedback) and an outer loop (LLM-driven online adaptation triggered by persistent failures), plus a memory unit for experience reuse via RAG.

The paper evaluates CoRAL on six simulated contact-rich manipulation tasks in ROBOSUITE/MuJoCo, comparing against OpenVLA-OFT and π₀.₅ as end-to-end VLA baselines, plus human-expert-designed cost functions and four ablation variants. The results show CoRAL succeeding on tasks where VLA baselines fail (e.g., Push+Pick Board, Flip with Wall), though it remains below the Expert FSM upper bound.

**Core contribution claims (C1-C3):**
- **C1:** A modular neuro-symbolic framework integrating LLM with reactive MPPI controller for zero-shot contact-rich manipulation.
- **C2:** Explicit separation of VLM (perception) and LLM (reasoning) roles, claimed to enhance performance and explainability.
- **C3:** LLM-driven closed-loop feedback (outer loop) for online adaptation, plus memory unit for experience reuse.

**Novelty verdict (deferred — external literature verification unavailable in this run):** All three claims have partial overlap with existing work (decoupled reasoning VLAs, foundation model + planner integration, and memory-augmented robotics), but the specific combination — LLM generating MPPI cost functions and contact strategies from scratch — has elements that appear novel. A definitive assessment requires manual literature verification, which was not possible in this automated review run due to retrieval service unavailability.

## Strengths
1. **Clear problem motivation and system-level design.** The paper addresses a genuine and important challenge in robotic manipulation — handling contact-rich tasks that require both precise trajectory planning and adaptive force control. The modular architecture (VLM for perception → LLM for reasoning/cost generation → MPPI for execution → outer loop for refinement) is well-motivated and the role separation is a principled design choice.

2. **Strong ablation study design.** The paper includes four ablation conditions (w/o Memory, w/o Refinement, Unified VLM, w/o Pose Tracking) that systematically isolate the contribution of each component. The Unified VLM ablation is particularly informative: showing that a single model tasked with both perception and planning fails catastrophically (0/10 on most tasks) provides compelling evidence for the value of role separation.

3. **Human-expert baselines provide a meaningful upper bound.** Including human-designed cost functions — both single-stage and FSM variants — gives the reader a grounded reference point for what expert-tuned optimization can achieve. This is a more informative baseline than typical leaderboard comparisons.

4. **Detailed robustness analysis.** The guided-vs-unguided contact strategy ablation on T6 (83.9% faster, 63.9% shorter path) and the online mass/friction correction demonstration (Figure 4) provide concrete evidence for the system's adaptive capabilities beyond aggregate success rates.

5. **Reproducibility-friendly disclosures.** The paper reports key hyperparameters (K=200, H=50, λ=0.1, N_retry=15) and hardware specifications, which is helpful for reproduction attempts.

## Weaknesses
### W1. Insufficient statistical rigor in experimental evaluation (High severity)
The entire experimental evaluation is based on only 10 trials per task (6 tasks = 60 total trials), with no confidence intervals, standard deviations, or statistical significance tests reported. Success rates are binary with no variance quantification. For example, CoRAL's 4/10 on T1 has a 95% binomial CI of approximately [12%, 74%], making statements like "significantly outperforms" unsupportable. Completion times are reported as single values without variance. Given the randomized task parameters (mass, friction, pose), substantial trial-to-trial variation is expected and should be quantified. **Fix:** Report 95% Clopper-Pearson confidence intervals for success rates, compute and report standard deviations for completion times over successful trials, and add at least 20-30 trials per condition for more reliable estimates. Use Fisher's exact test or bootstrapping to support comparative claims.

### W2. Key method details are underspecified, harming reproducibility (High severity)
Several critical implementation details are missing across the core method components:
- **Cost function generation (Eq. 2, 5):** The LLM prompt template, output parsing procedure, and validation mechanism for generated cost functions are not provided. The paper states the LLM is "free to introduce any cost terms," but the experimental cost functions used for each task are never reported.
- **Contact strategy (Eq. 3):** How the LLM specifies surface regions {Rⱼ} is undefined (semantic description? geometric parameters?). How C₀ biases MPPI sampling is not described.
- **MPPI dynamics model:** The Planning World dynamics f(·) used for rollouts is never specified — is it a separate MuJoCo instance with estimated parameters θ? This is essential for understanding both the method and its computational cost.
- **Memory unit (Eq. 1):** The RAG implementation (embedding model, similarity metric, retrieval threshold, serialization format for stored strategies) is entirely unspecified.
- **Outer loop input (Section 3.4):** The structure of logged episode data E_t and how it's presented to the LLM is not described.
**Fix:** Provide all prompts, pseudocode, and implementation specifications in an extended appendix. Report actual cost function terms and weights used for each experimental task.

### W3. Overclaiming on multiple fronts (High severity)
The paper systematically overstates its contributions relative to the evidence provided:
- **"Zero-shot planning":** The method relies on FoundationPose (pre-trained), GPT-4o (pre-trained), known 3D object models M, and hand-tuned MPPI hyperparameters. The term "zero-shot" should be scoped to mean "no task-specific demonstration data."
- **"Significantly enhances... explainability":** Only one qualitative LLM diagnosis example is given; no systematic explainability metric, user study, or comparison with baseline explainability is provided.
- **"State-of-the-art outperformance":** The two VLA baselines (OpenVLA-OFT, π₀.₅) are evaluated using LIBERO checkpoints on custom tasks that are likely out-of-distribution — this is expected behavior, not a surprising finding. The closest technical relatives (IMPACT, VLMPC) are not compared against at all.
- **"Precise, force-aware control":** No direct force metrics (force tracking error, contact force profiles) are reported.
**Fix:** Revise all strong claims to match the evidence. Scope "zero-shot" explicitly. Replace "significantly outperforms" with task-specific bounded claims. Acknowledge the distribution shift limiting VLA baselines.

### W4. Missing comparisons with closest related work (Medium-high severity)
The Related Work section identifies IMPACT and VLMPC as the most closely related approaches (foundation model + motion planner), and claims to "significantly advance" beyond them. However, neither method is included as an experimental baseline. This weakens the paper's strongest novelty claim (LLM generating cost functions rather than perceptual guidance). **Fix:** Either add IMPACT/VLMPC as baselines (even on a subset of tasks) or provide a detailed analytical comparison explaining why direct experimental comparison is not feasible, along with a comparison across key design dimensions (e.g., table comparing assumptions, requirements, and capabilities).

### W5. Limited external validity — simulation-only results (Medium severity)
All experiments are conducted in the MuJoCo physics simulator with known 3D object models M, fixed camera, and simulated force/torque sensors. No real-robot experiments are reported, yet the paper discusses "robustness against the inherent sim-to-real gap" and makes claims about "deploying robots in unknown environments." The sim-to-real gap is acknowledged only as a limitation in passing (Section 5) without any analysis or mitigation experiments. **Fix:** Add at least one real-world proof-of-concept experiment, or clearly bound claims to simulation and add a dedicated sim-to-real gap analysis (e.g., adding parameter noise, sensor noise, or latency to the simulation to probe robustness).

### W6. Computational cost and practical feasibility not characterized (Medium severity)
The paper does not report wall-clock time per control cycle, total planning time per task, or number of GPT-4o API calls per episode. MPPI with K=200 rollouts over H=50 steps is computationally expensive, and GPT-4o API calls add latency and cost. Without these numbers, the reader cannot assess the practical deployability of CoRAL. **Fix:** Report average wall-clock time per control step, per episode, and number of LLM/VLM API calls per task. Compare with baseline inference times.

### W7. Memory unit contribution is modest and not statistically validated (Medium severity)
The memory unit's benefit is shown on T1 (2/10 → 4/10, p≈0.31 by Fisher's exact test) and T3 (9/10 → 10/10, p≈1.0). Neither improvement is statistically significant at conventional levels. No cross-task transfer experiments are reported. The memory cold-start problem (first episode always requires expensive LLM call) is not discussed. Memory hit rate across trials is not reported. **Fix:** Increase trials for the ablation conditions, add cross-task memory transfer experiments, and report memory hit rates.

### W8. Outer loop refinement lacks systematic evaluation (Medium severity)
The LLM-driven outer loop is presented as a core contribution, but its evaluation is entirely anecdotal (one mass correction example, one explainability example). No systematic analysis is provided on: (a) how often the LLM correctly diagnoses failures, (b) how many refinement cycles are typically needed, (c) what types of failures are resolvable, (d) whether the LLM ever makes incorrect diagnoses that compound errors. **Fix:** Add a quantitative analysis of outer loop performance across multiple episodes, including diagnosis accuracy, refinement convergence rate, and failure mode categorization.

### W9. Explainability claim is qualitatively illustrated but not measured (Medium-low severity)
The paper claims enhanced explainability as a key advantage, but provides only one example of the LLM producing a natural language diagnosis. No comparison against baseline explainability (e.g., saliency maps for VLA models, or structured logging) is provided. No human evaluation or quantitative explainability metric is reported. **Fix:** Conduct a small user study comparing CoRAL's failure diagnosis output against baseline methods, or at minimum provide multiple diverse examples of the LLM's diagnostic reasoning across different failure types.

### W10. Narrative structure could be improved (Low severity)
(i) The opening paragraph of the introduction uses 10 citations in 5 sentences without explaining what each contributes. (ii) The cognitive analogy (human refinement) is introduced but never revisited or validated against the architecture. (iii) The Related Work section reads as a literature list rather than an organized comparison by design dimensions. (iv) The conclusion adds new unsupported claims ("physically intelligent robotic agents"). These issues reduce readability but do not affect scientific validity. The annotated version in the PDF provides specific Mentor Revised Versions for key paragraphs.

### ASCII Diagram — Paper Structure & Evidence Map

```text
[Problem: Contact-rich manipulation is hard for VLA models]
    │
    ▼
[Proposed: CoRAL — LLM + MPPI + outer loop + memory]
    │
    ├── [C1: Modular LLM+MPPI integration] 
    │       └── Evidence: Zero-shot success on 6 tasks
    │       └── Gap: Missing comparison vs IMPACT/VLMPC
    │       └── Risk: LLM cost function generation is underspecified
    │
    ├── [C2: VLM/LLM role separation]
    │       └── Evidence: Unified VLM variant fails (0/10)
    │       └── Gap: Explainability not measured
    │       └── Risk: Overclaim on explainability
    │
    ├── [C3: Outer loop adaptation + memory]
    │       └── Evidence: Mass correction demo, T1/T3 improvements
    │       └── Gap: No systematic outer loop evaluation
    │       └── Risk: Memory improvements not statistically significant
    │
    ▼
[Key weaknesses: Low statistical power (10 trials), no real-world validation,
 missing baselines (IMPACT/VLMPC), underspecified implementation details,
 overclaimed generality]
```

### ASCII Diagram — Revision Strategy Roadmap

```text
Priority  | Problem                        | Fix                                   | Expected Gain
P0        | Low statistical rigor          | Increase trials, add CI, significance  | Validated conclusions
P0        | Underspecified implementation  | Full prompts, pseudocode, cost tables  | Reproducibility
P0        | Overclaiming                   | Scope claims to evidence               | Scientific credibility
P1        | Missing closest baselines      | Add IMPACT/VLMPC comparison            | Stronger novelty case
P1        | Simulation-only validation     | Real-robot demo or noise analysis      | External validity
P1        | Computational cost unknown     | Report wall-clock time, API calls      | Practical deployability 
P2        | Narrative/readability issues   | Apply Mentor Revised Versions          | Reader engagement
```

## Score
**Final Score: 5.5/10**

**Rationale:** The paper addresses a relevant problem (contact-rich robotic manipulation) with a well-motivated modular architecture that integrates LLM-based reasoning with reactive control. The ablation study is well-designed, the human-expert baselines provide useful context, and the robustness demonstrations (contact strategy guidance, online parameter correction) are informative.

However, the paper is held back by several significant weaknesses that materially affect its contribution. The experimental evaluation lacks statistical rigor (only 10 trials per task, no confidence intervals or significance tests), making the claimed "significant" outperformance of baselines unsupported. Multiple core method components are underspecified to the point of irreproducibility (cost function generation prompt, contact strategy mechanism, MPPI dynamics model, memory unit implementation). The paper systematically overclaims its contributions ("zero-shot" is not properly scoped, "enhanced explainability" is not measured, "state-of-the-art outperformance" is based on missing closest baselines). All experiments are in simulation, and computational cost is not characterized. The two closest technical relatives (IMPACT, VLMPC) are discussed qualitatively but not compared experimentally.

With substantial revision — including statistically rigorous evaluation, full implementation disclosure, claim-scoping, and at least proof-of-concept real-world validation — this work could become a solid contribution. In its current form, it represents a promising but incompletely validated system proposal.

**Scoring breakdown:**
- Novelty/Research value: 6/10 (interesting combination but missing key baselines)
- Validity/Soundness: 4/10 (low statistical power, reproducibility concerns)
- Completeness: 5/10 (missing implementation details, limited tasks)
- Presentation: 6/10 (clear motivation but overclaiming and narrative issues)
- Practical relevance: 6/10 (promising direction but simulation-only, cost unknown)