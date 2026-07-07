## Summary

CoRAL proposes a modular neuro-symbolic framework for contact-rich robotic manipulation that integrates VLMs (FoundationPose + GPT-4o for perception), an LLM (GPT-4o for cost function and contact strategy generation), an MPPI reactive controller, and a memory unit. The key architectural idea is to use the LLM to configure a model-based controller — formulating cost functions and contact strategies — rather than learning an end-to-end policy. The system is evaluated on six simulated manipulation tasks against VLA baselines (OpenVLA, π0.5), human-expert-designed cost baselines, and ablations.

## Strengths
- **Well-structured neuro-symbolic architecture (Sections 3.1–3.4).** The decomposition into a VLM-based perception pipeline, an LLM-driven task formulation module, an MPPI reactive controller, and a memory unit with nested feedback loops (high-frequency inner loop for reactive re-planning and low-frequency outer loop for strategic re-formulation) is clean, well-motivated, and maps intuitively onto the contact-rich manipulation problem.
- **Comprehensive ablation study (Table 1, Section 4.1.3).** The paper systematically ablates each component (memory, refinement, unified VLM, pose tracking) across all six tasks. The dramatic collapse of the "Unified VLM" and "w/o Pose Tracking" variants (0/10 on nearly all complex tasks) convincingly demonstrates that these design choices matter and provides the strongest empirical support in the paper.
- **Human-expert cost baselines (Section 4.1.2).** Including hand-designed single-stage and FSM cost functions as baselines, evaluated with the same MPPI backbone, is a sound methodological choice. It provides a meaningful upper bound and contextualizes what fraction of expert-designed structure the LLM can recover automatically.

## Weaknesses

### Fatal
- **Internal inconsistency in the mass correction experiment (Section 4.1.4, Figure 4).** The text states the Evaluation World was initialized with mass 2.0 kg vs. ground truth 0.1 kg and that after adaptation "the agent's belief about both mass and friction converged remarkably close to their true values." However, Figure 4's caption describes: a y-axis ranging 0.75–1.00 kg (neither 2.0 nor 0.1 appears), a "Corrected Mass" line starting at ~1.0 kg and converging to ~0.85 kg (8.5× the stated ground truth), and an "Initial Mass" line constant at ~1.0 kg (not 2.0 kg). This figure-text mismatch means the paper's primary evidence for online parameter adaptation — a cornerstone claimed capability — is unverifiable as presented. Accepting the paper would require trusting claims that the exhibited evidence contradicts.

### Major
- **VLA baseline comparison does not support the headline claims (Section 4.1.1, Table 1).** The paper claims CoRAL "significantly outperforms both state-of-the-art baselines, OpenVLA-OFT and π0.5" and concludes "even fine-tuning an end-to-end policy is insufficient for scenarios that demand explicit physical modeling." However, the VLAs are evaluated using their LIBERO-GOAL checkpoints on tasks T1, T4, T5, T6 — custom tasks with no presence in the LIBERO suite. This tests whether frozen LIBERO checkpoints can zero-shot solve novel OOD tasks. On the two tasks that are LIBERO-compatible (T2, T3), OpenVLA achieves 10/10 and 9/10, matching or nearly matching CoRAL. The experimental design does not test whether VLAs can be fine-tuned on these contact-rich tasks, so the strong conclusion about VLA inadequacy is not supported.
- **Underpowered evaluation with no statistical rigor (Table 1, Section 4).** All results are based on 10 Bernoulli trials per condition. With n=10, the 95% CI for a 4/10 success rate is approximately [0.12, 0.74]. The paper treats differences of 2–3 successes as meaningful (e.g., memory "boosted the success rate from 2/10 to 4/10" on T1). No confidence intervals, standard deviations, or statistical tests are reported anywhere. Given the strong comparative claims, this is insufficient.

### Minor
- **No real-world validation.** The paper motivates CoRAL with real-world contact-rich manipulation challenges but evaluates entirely in simulation (ROBOSUITE/MuJoCo). The reactive control augmentation (Eq. 7) is explicitly motivated by the sim-to-real gap, yet no real-robot experiments are conducted to validate whether the system transfers. This limits confidence in practical applicability.
- **The "Unified VLM" ablation conflates prompt design with architectural separation (Section 4.1.3).** GPT-4o is a single model used for both roles; the "separation" is implemented via different prompts and API calls. The finding that structured, focused prompts outperform a single omnibus prompt is empirically interesting but does not support the architectural claim about "explicitly separating the roles of vision models for perception and the LLM for reasoning." This is prompt engineering, not a modular architecture distinction.
- **Inflated "zero-shot" framing.** The paper repeatedly describes CoRAL as "zero-shot" (Abstract, Contributions, Section 3, RQ1). In the VLA robotics literature, "zero-shot" typically implies generalization to novel tasks/objects without per-task engineering. CoRAL requires known 3D CAD models of every object, a MuJoCo simulation of the full dynamics, hand-tuned feedback gains K_f, hand-tuned MPPI hyperparameters, and a manually specified state/action space. The contribution — no task-specific training data — is valuable, but the framing overstates generality relative to common usage.

### Trivial
- None.

## Nice-to-Haves
- Report wall-clock time per MPPI control cycle to assess real-time applicability (K=200, H=50 rollouts in MuJoCo).
- Quantify GPT-4o API costs (number of calls, tokens, dollar cost per task).
- Add a friction correction figure parallel to the mass figure for completeness of the robustness analysis.

## Removed Points
These points are flagged to be removed; treat them with caution.
- **"Human expert comparison less favorable than presented"** — The paper uses measured language ("narrows the gap," "approaching expert-level performance," "remaining below the FSM upper bound"). The gap (4/10 vs 8/10 on T1) is acknowledged; the paper does not claim to match or exceed. Overstated by the reviewer.
- **Missing wall-clock time / LLM API cost analysis** — Nice-to-haves, not core weaknesses. The paper acknowledges computational latency as a limitation.
- **Memory unit underspecification** — The memory module is described at a reasonable level (RAG-based, indexed by task and parameters). Implementation details of embedding models and similarity metrics are standard practice.
- **w/o Pose Tracking ablation uninformativeness** — While straightforward, it usefully demonstrates that FoundationPose is necessary; this is a valid ablation result.
- **Missing CAD model requirement in limitations** — FoundationPose's CAD requirement is stated in the methodology. While it could be more prominent, this is not a fatal omission.
- **Missing related works / references** — Per guidelines, the merger should not criticize missing related works as external sources cannot confirm their existence.

## Novel Insights
None beyond the paper's own contributions.

## Suggestions
1. **Fix the mass correction experiment.** Ensure Figure 4 axes, initial values, and convergence targets match what the text describes. If the figure is correct, update the text; if the text is correct, replot the figure. This inconsistency must be resolved for the adaptation capability claim to be credible.
2. **Replace or supplement the VLA comparison.** Either fine-tune VLAs on the contact-rich tasks (even with limited demonstrations), or restrict the headline comparison to LIBERO tasks where VLAs are on-distribution. Without this, the central comparative claim is unsupported.
3. **Report confidence intervals or increase trial counts** (e.g., 20–30 per condition) for the main comparisons. At minimum, add Clopper-Pearson intervals to Table 1.
4. **Calibrate the "zero-shot" language** to reflect the system's actual prerequisites (CAD models, simulator, hand-tuned gains/hyperparameters).
5. **Acknowledge CAD model requirements and simulation-only evaluation** more prominently in the main limitations section.

## Score and Decision
**Round 1 bracket:** After comparing weighted items from my draft against calibration anchors, the narrowest plausible range is [2.5, 4.0]. The most topically similar anchor — "Generating Robot Policy Code for High-Precision and Contact-Rich Manipulation Tasks" (WtHKqtHVXo.md, avg 4.0) — has stronger negative weights (-9.28, -9.26, -7.91) but also includes real-robot validation and a cleaner evaluation. Our paper has a verifiable internal inconsistency in its primary adaptation experiment (the fatal-tier weakness), a structurally problematic VLA comparison, and no real-robot validation — issues that collectively push its score below the 4.0 anchor. At the same time, the paper's architecture is well-designed and the ablation study is comprehensive, distinguishing it from papers scoring ≤2.0 (which lack coherent methodology and any meaningful evaluation). The GRAIL anchor (oyXoGJQlUf.md, avg 3.0) faced extremely weak evaluation and unclear contribution — our paper is stronger in architecture and ablation quality but has a similar severity of core-evidence problems. Considering the fatal inconsistency combined with the other major weaknesses, the paper falls at the lower end of this bracket.

**Final score:** 3.0 — a reject. The paper presents a promising architectural direction and a thorough ablation study, but the mass correction figure-text inconsistency undermines a key claimed capability, the VLA comparison does not support the headline claims, and the evaluation lacks statistical rigor. These issues collectively prevent the paper from substantiating its central claims in its current form.

**Calibration anchors consulted across all rounds:**
| Path | Avg Score | Round | Itemized? | Comparison |
|------|-----------|-------|-----------|------------|
| gwZ90hFSL2.md | 1.00 | 1 | No | Unrelated (cross-lingual robotics); far weaker |
| 5kMwiMnUip.md | 1.40 | 1 | No | Unrelated (LLM jailbreaking) |
| I0To0G5J7g.md | 3.20 | 2 | No | Online self-improvement for embodied models; different approach |
| oyXoGJQlUf.md | 3.00 | 2 | Yes | GRAIL (LLM+PDDL planning); similar evaluation severity concerns |
| WtHKqtHVXo.md | 4.00 | 1,2 | Yes | Closest topical anchor (LLM code for contact-rich); has real-robot validation and no internal inconsistency |
| KTtEICH4TO.md | 4.75 | 1 | Yes | CORN (contact-based object rep); stronger experiments, real-robot transfer |
| RQDuFF1rOn.md | 3.67 | 1 | Yes | Wonderful Team (VLM zero-shot robotics); similar overclaiming issues |
| QOfswj7hij.md | 7.33 | 1 | No | Online neuro-symbolic predicates; stronger theoretical framing |
| hQVCCxQxYN.md | 6.67 | 2 | Yes | Plan-Seq-Learn; simulation-only but stronger methodology |
| h7aQxzKbq6.md | 6.00 | 1 | No | HAMSTER; stronger evaluation despite simulation-only |

**Final weighted-item reasoning:** My draft's strongest positive weights (+5.73 architecture, +4.96 ablation) are comparable to the top strengths of the 4.0 anchor (WtHKqtHVXo: +4.90 ablation, +4.23 action space). However, my draft's fatal-tier (-5.13) and major-tier (-7.58, -5.11) weaknesses are collectively heavier and include an internal inconsistency absent from the 4.0 anchor. The mass inconsistency alone pulls the paper below the 4.0 threshold and into the 2.5–3.5 range, where papers with critical experimental problems reside.

MY FINAL SCORE: <score>3.0</score>
MY FINAL DECISION: <decision>Reject</decision>