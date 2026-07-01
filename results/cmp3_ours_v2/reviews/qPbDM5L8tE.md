Now I have strong calibration anchors. Let me write the final consolidated review.

**Calibration Summary:**
- **Round 1 bracket**: 4.0–5.5, derived from the most comparable anchors: RePLan (4.25, Reject) — same architecture pattern (LLM generates rewards/costs + VLM perception + replanning), same issues (underspecified LLM output, small N, simulation-only); Make a Donut (5.25, Reject) — LLM-guided zero-shot manipulation with real-world experiments, still rejected; Instruct2Act (5.00, Reject); CrayonRobo (5.20, Reject); GenBot (5.50, Reject).
- **Round 2 narrowing**: The paper sits above RePLan (more thorough ablation, more tasks, more trials) but below Make a Donut (which had real-world validation and still was rejected at 5.25). Papers scoring 5.5+ in this topic area (GenBot, LGA) either had substantially broader evaluation or a more clearly specified core mechanism.
- **Final placement**: Score **5.0**, Decision **Reject** — the paper has a genuinely interesting architecture and informative ablations, but the core technical novelty (LLM generating cost functions) is not adequately specified or isolated, and the evaluation falls short of the acceptance bar for this area.

---

## Summary

CoRAL proposes a modular framework for contact-rich robotic manipulation that separates perception (VLM for pose tracking and physical parameter estimation) from strategic reasoning (LLM generating MPPI cost function structures, contact strategies, and online adaptation). The system uses FoundationPose for 6-DoF tracking, GPT-4o for both VLM and LLM roles, and an MPPI controller for reactive execution, with a memory unit for experience reuse. Evaluated on six simulated contact-rich tasks, CoRAL succeeds where end-to-end VLAs (OpenVLA, π₀.₅) fail completely, and the ablations provide interpretable evidence that the modular decomposition matters.

## Strengths

1. **Well-motivated architectural decomposition with empirical backing.** The paper identifies a genuine failure mode of end-to-end VLA models — brittleness on contact-rich tasks requiring force reasoning — and the ablation evidence supports the separation: the Unified VLM variant (0/10 on most tasks) and the w/o Pose Tracking variant (0/10 nearly everywhere) show that the specialized modules are not merely cosmetic.

2. **LLM-as-cost-function-designer is a genuinely novel direction.** Unlike prior neuro-symbolic work where foundation models identify subgoals (VLMPC) or generate static cost maps (IMPACT), CoRAL has the LLM produce the *mathematical structure and weights* of the MPPI objective itself (Sec. 3.2). This is a conceptually clean way to ground commonsense reasoning in optimal control.

3. **Contact strategy ablation on T6 is the strongest single piece of evidence.** The guided vs. unguided comparison (83.9% fewer steps, 63.9% shorter path) cleanly isolates the value of the LLM's contact proposals and shows it transforms an intractable search problem into a solvable one.

4. **Systematic ablation study with interpretable results.** The four ablations (w/o Memory, w/o Refinement, Unified VLM, w/o Pose Tracking) each test a claimed design element and produce differentiated, interpretable outcomes. The w/o Pose Tracking result (0/10 on 5 of 6 tasks) is particularly conclusive.

## Weaknesses

### Major

1. **Core technical novelty (LLM-generated cost functions) is underspecified and unverified.** The paper's central claim is that the LLM generates the structure and weights of the MPPI cost function, yet:

   - **No parsing mechanism is described.** The paper states the LLM is "free to introduce any cost terms constructible from the available state, pose, and action variables" (line 91). How free-form LLM text becomes a runnable MPPI objective is never explained — no output grammar, no code generation, no structured interface.  
   - **No characterization of LLM output quality.** What cost functions does GPT-4o actually produce for each task? How consistent are they across repeated calls? How often does the LLM produce invalid, degenerate, or non-functional cost functions? The LLM is treated as a black box that, by fiat, works.  
   - **No baseline isolating the LLM's cost function contribution.** The Expert baselines use hand-tuned costs. A simple fixed-cost baseline (e.g., quadratic distance-to-goal with a fixed contact penalty) using the same MPPI backbone, pose tracker, and contact strategy would isolate whether the LLM's cost function adds value over a trivial alternative. Without it, the paper cannot distinguish whether the framework's success comes from the LLM's cost function or from the MPPI/pose-tracking/contact-strategy infrastructure.  
   - **Eq. 2 is acknowledged as "illustrative"** (line 91), but the paper's novelty rests on the LLM generating *actual* cost functions. The reader needs to see the functional forms used for the six tasks, not an illustrative template.

   **Why this matters:** If the LLM cost function generation is the paper's key differentiator from prior work (IMPACT, VLMPC, RePLan), the paper must characterize what is produced, how reliably, and demonstrate that it beats a reasonable fixed alternative. Currently this core mechanism is unverifiable.

### Minor

2. **Statistical characterization is insufficient for within-ablation comparisons.** With N=10 per condition and binary success, the 95% Clopper-Pearson confidence intervals are wide (e.g., 4/10 → CI ≈ [12%, 74%]). Many comparisons the paper treats as meaningful — CoRAL with Memory (4/10) vs. without Memory (2/10) on T1; CoRAL w/o Refinement (6/10) vs. full CoRAL (9/10) on T4 — have overlapping intervals. No confidence intervals, standard errors, or significance tests are reported. The paper uses language like "significantly outperforms" and "dramatic performance drop" without statistical backing. This does not undermine the main finding (VLAs fail, CoRAL succeeds; the gaps there are large), but the within-ablation contrasts are over-interpreted.

3. **The Unified VLM ablation conflates architecture with prompt complexity.** This ablation uses a single multimodal prompt for *both* perception and planning, meaning the model must estimate poses, estimate physical parameters, generate cost functions, and generate contact strategies — all at once. The catastrophic failure (0/10 on most tasks) is interpreted as evidence that separating VLM and LLM *roles* is crucial. But the ablation also removes FoundationPose (since a "single prompt for both perception and planning" subsumes pose estimation into the VLM). A cleaner test would keep FoundationPose pose estimates and only collapse physical parameter estimation and cost/strategy generation into one model. The current design conflates removing a dedicated pose estimator with removing role separation.

4. **Memory unit is underspecified for a claimed contribution.** The memory unit is listed as a contribution (bullet 4, Sec. 1), yet its implementation is described only as RAG where "the LLM embeds the current task into a latent semantic space" (Sec. 3.2). No embedding model, similarity metric, retrieval threshold/top-k, or indication of how retrieved plans are adapted to the current scene is provided. The empirical benefit shown (e.g., T1: 2/10 → 4/10) is modest and the implementation sensitivity is unknown.

5. **Reactive control augmentation not ablated.** The proportional feedback law (Eq. 7) is never independently ablated, so its contribution to the results cannot be separated from the MPPI planning.

6. **No validation of VLM physical parameter estimate accuracy.** The VLM estimates mass and friction from appearance. Figure 4 shows online correction, but the initial estimation error distribution is never characterized, making it unclear how much the outer loop adaptation must compensate.

### Trivial

- No wall-clock time, number of LLM API calls, or inference cost reported. The "average completion time" is in simulation steps without stating the step frequency, so it is not interpretable as real time.

## Nice-to-Haves

- **Comparison with IMPACT or VLMPC** would strengthen the positioning against related neuro-symbolic approaches. The paper discusses them in Related Work but does not compare experimentally; this is reasonable given scope constraints but would be a useful addition.
- **A real-robot demonstration** on at least one task would substantially strengthen the claimed robustness, though the paper's contribution is primarily algorithmic and simulation-only work is accepted at ICLR when properly scoped.

## Removed Points

These points were moved here per the filtering protocol:

1. *"No prompt templates are provided"* — The appendix was stripped by the parser; the original submission may contain prompts. The main-paper criticism about undescription of the parsing mechanism is kept (Major weakness 1), but the specific prompt-template complaint is removed.
2. *"Neither IMPACT nor VLMPC is included as a baseline"* — Reasonable scope decision; not including every related method is not a weakness. Moved to Nice-to-Haves.
3. *"The claim that VLAs 'often lack adaptability and explainability' is fair"* — This is a neutral comment, not a weakness.
4. *"Explainability claim is supported only by a single anecdotal LLM output"* — This is subsumed by weakness 1 (underspecified LLM behavior). The explainability claim is secondary to the main contribution.
5. *"Formatting/style nitpicks"* — Removed per protocol (parser artifacts).
6. *"Missing related works"* — Removed per protocol (cannot verify external completeness).

## Novel Insights

The Harsh Critic's observation that the guided-vs-unguided contact strategy ablation (83.9% fewer steps, 63.9% shorter path on T6) is the paper's cleanest evidence is correct and worth emphasizing: it is the one experiment where the comparison isolates a single variable (contact strategy present vs. absent) and sees a dramatic, easily interpretable effect. The reviewer also correctly identifies that the Unified VLM ablation is confounded — this is a subtle design flaw that the paper's own interpretation glosses over, and fixing it would sharpen the paper's central claim about role separation. Beyond these, the review surfaces no fundamentally novel insight beyond the paper's own contributions.

## Suggestions

1. **Specify the LLM cost function pipeline.** Describe: (a) the prompt format given to the LLM, (b) how the LLM's text output is parsed into a runnable MPPI cost function (grammar? code generation? structured output?), (c) the actual cost functions GPT-4o produced for 2–3 of the six tasks, and (d) how often the LLM produces valid vs. invalid outputs across repeated calls with the same input.

2. **Add a minimal-viable cost baseline.** Run the same MPPI controller with the same pose tracker and contact strategy, but replace the LLM-generated cost with a simple fixed alternative (e.g., quadratic distance-to-goal + fixed contact penalty). This isolates the value of the LLM's cost function from the rest of the infrastructure.

3. **Deconfound the Unified VLM ablation.** Keep FoundationPose pose estimates and only collapse physical parameter estimation + cost/strategy generation into one model. This cleanly tests the role-separation hypothesis.

4. **Scale up trials for within-ablation comparisons.** N=100 per condition in simulation is cheap and would provide meaningful confidence intervals for the ablation contrasts (memory, refinement) that are currently statistically ambiguous.

5. **Provide memory unit implementation details** (embedding model, similarity metric, retrieval mechanism) sufficient for reproducibility.

## Score and Decision

| Anchor Paper | Avg Score | Round | Comparison |
|---|---|---|---|
| RePLan | 4.25 (Reject) | R1 | Most similar architecture (LLM reward gen + VLM perception + replanning); same structural issues (underspecified components, small N, simulation-reliance). CoRAL has better ablations and more tasks/trials. |
| Make a Donut | 5.25 (Reject) | R1, R2 | LLM-guided zero-shot manipulation with real-world experiments. Stronger empirical validation but still rejected. |
| LLMPhy | 4.40 (Reject) | R2 | LLM + world model for physical reasoning. Similar scope but less thorough evaluation. |
| Instruct2Act | 5.00 (Reject) | R2 | LLM mapping instructions to actions. Comparable scope and evaluation depth. |
| CrayonRobo | 5.20 (Reject) | R1 | Visual prompting for manipulation with sim+real experiments. Rejected despite real-world validation. |
| GenBot | 5.50 (Reject) | R2 | Generative simulation for robotic skill learning. Rejected. |
| LGA | 5.67 (Accept) | R2 | Language-guided state abstractions. Clearer specification of core mechanism. |

**Round 1 bracket**: 4.0–5.5  
**Narrowing rationale**: CoRAL is stronger than RePLan (4.25) due to more thorough ablations, the informative contact strategy analysis, and a larger evaluation (6 tasks × 10 trials vs. 4×3). But it is weaker than Make a Donut (5.25, rejected) which had real-world experiments and still fell below the acceptance threshold. Papers scoring 5.5+ in this topic area either had substantially broader evaluation (GenBot) or a more clearly specified core mechanism (LGA).  
**Final score**: 5.0 — the architectural insight is genuine and the ablation study is well-motivated, but the core technical novelty is insufficiently specified and the evidence does not meet the acceptance bar.

MY FINAL SCORE: <score>5.0</score>
MY FINAL DECISION: <decision>Reject</decision>