Now let me produce the final review.

## Summary

The paper introduces Visuo-Tactile World Models (VT-WM), which integrate fingertip tactile sensing (Digit 360 sensors) with vision to ground world models in contact physics for robot manipulation. The architecture encodes visual frames via Cosmos tokenizer and tactile images via Sparsh-X, concatenates tokens, and processes them through a 12-layer transformer predictor. The model is trained on multiple contact-rich tasks and evaluated on imagination quality (object permanence, causal compliance), zero-shot CEM planning on a real Franka Panda + Allegro Hand, and data efficiency for a new task. Results consistently favor VT-WM over a vision-only baseline (V-WM).

## Strengths

1. **Well-motivated problem with clear physical grounding.** The paper articulates why vision-only world models fail under occlusion and contact ambiguity (§1, §3.1). The reasoning that tactile sensing provides the missing local contact signal that vision cannot resolve (e.g., distinguishing no-contact from firm grasp from the same camera view) is concrete and physically sensible.

2. **Multi-faceted evaluation on real hardware.** The paper evaluates along three complementary axes — imagination quality with statistical tests (§4.1), zero-shot real-robot CEM planning (§4.2), and data efficiency for a new task (§4.3) — on a Franka Panda + Allegro Hand + Digit 360 platform. The real-robot validation goes beyond simulation-only visuo-tactile works (e.g., M3L) and adds credibility.

3. **Honest statistical reporting for Fréchet distance metrics.** The paper reports paired t-tests with specific t-values and p-values for object permanence and causal compliance comparisons (§4.1), including non-significant results and one negative trend.

## Weaknesses

### Major

1. **The V-WM baseline against which all gains are measured is never specified (§4.1).** The paper's central quantitative claims — 33% improvement in object permanence, 29% in causal compliance, up to 35% in planning — all derive from a comparison between VT-WM and "a multi-task vision-only world model (V-WM)." Yet the paper contains no description of V-WM's architecture, training data, hyperparameters, or even a statement about whether it is the same 12-layer transformer with tactile tokens removed or a fundamentally different model. The reader cannot determine whether the comparison is a clean ablation (VT-WM minus tactile = V-WM) or an uneven comparison (different architectures, different training). Until this is clarified, the headline numbers are ungrounded. This is not an appendix-level detail; it is a core methodological specification that belongs in the main text.

2. **The data efficiency experiment (§4.3) confounds pre-training with modality advantage.** VT-WM is pre-trained on the full multi-task dataset and fine-tuned on 20 new demonstrations, while the BC policy (ACT) is trained from scratch on only those 20 demonstrations. The comparison does not isolate whether the advantage comes from tactile sensing or from having seen many more demonstrations across multiple tasks. Moreover, the BC policy also receives tactile inputs ("The BC policy is deployed in closed loop, where at each timestep it receives the latest RGB and tactile inputs"), so the comparison does not even test vision-vs-visuo-tactile. A controlled comparison would pre-train the BC policy on the same multi-task data or train VT-WM from scratch on the 20 demonstrations.

### Minor

3. **Planning experiments use only 5 trials per task (§4.2).** With N=5, a difference of e.g., 69%→93% (≈3.5/5 vs ≈4.6/5 successes) is a 1–2 trial swing. No confidence intervals or statistical tests are reported for planning results. While 5 trials is not unusual in real-robot papers, the small N combined with open-loop execution and no uncertainty quantification weakens the planning evidence.

4. **Scribble-with-marker task shows degradation on causal compliance without discussion (§4.1).** VT-WM performs descriptively *worse* than V-WM on this task (t = -1.22, p = 0.23, negative trend). The paper reports this honestly but offers no hypothesis about why tactile input might hurt performance on certain tasks. This is relevant because it suggests tactile grounding may not be universally beneficial.

5. **Minor inconsistency between abstract and conclusion.** Abstract claims "over 3.5×" data efficiency improvement, while conclusion claims "over 3×" for the same 78% vs 22% result (actual ratio ≈3.54×, so "over 3.5×" is accurate).

## Removed Points
- *CoTracker confound* (speculative — no evidence that CoTracker is differentially biased by model output quality).
- *Missing architecture dimensions / token counts* (paper states "Additional details... provided in appendix A" — these were stripped by the parser).
- *"1250.0%" formatting in Figure 8* (acknowledged parser artifact from formula rendering).
- *Action conditioning granularity mismatch* (technical design choice, not clearly problematic).
- *Temporal rate synchronization* (reasonable to assume timestamp alignment; standard practice).
- *Missing related work on Zhang & Demiris (2023)* (claim about "first multi-task" vs "task-specific" is a valid distinction that the paper explicitly makes).

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. **Specify the V-WM baseline unambiguously.** State explicitly: (a) whether V-WM is the same architecture as VT-WM with tactile encoder/ tokens removed, (b) training data and hyperparameters, and (c) whether it is a separately trained model or a single model with tactile inputs masked.

2. **Run additional planning trials (≥20/task) or report bootstrapped confidence intervals for the existing data** to quantify the uncertainty in the 5-trial planning results.

3. **For the data efficiency comparison, add a controlled baseline** — either a BC policy pre-trained on the multi-task data or a from-scratch VT-WM — to isolate the pre-training effect from the tactile advantage.

4. **Discuss the scribble-with-marker degradation** — even a brief hypothesis (e.g., "marker visual appearance may dominate tactile signal") would demonstrate awareness of when tactile sensing may not help.

## Score and Decision

**Calibration anchors:**
| Paper | Avg Score | Round | Comparison to this paper |
|---|---|---|---|
| DINO-WM (GARbxyCV13) | 5.75 (reject) | Bracket | World model + zero-shot planning, but vision-only. More thorough baseline comparisons but less novel modality. |
| CORN (KTtEICH4TO) | 4.75 (accept) | Bracket | Contact-based manipulation, real-world transfer. Stronger experiments, cleaner baselines. |
| M3L — The Power of the Senses (FMsmo01TaI) | 4.33 (reject) | Bracket | Visuo-tactile RL, simulation-only. VT-WM stronger due to real-robot validation but similar baseline concerns. |
| Learning to Jointly Understand Vis & Tact (NtQqIcSbqv) | 6.00 (accept) | Narrow | Visuo-tactile dataset + manifold learning. Cleaner paper but different contribution type. |
| Unleashing Large-Scale Video Pre-training (NxoFmGgWC9) | 5.50 (accept) | Narrow | Video pre-training + robot manipulation. Similar baseline criticism but accepted. |
| DIFFTACTILE (eJHnSg783t) | 6.50 (accept) | Narrow | Differentiable tactile simulator. Stronger, cleaner evaluation. |

**Round 1 bracket:** 3.5 – 5.5 (between M3L-level and DINO-WM-level).

**Narrowing:** The paper's real-robot validation and multi-faceted evaluation place it above M3L (4.33, sim-only). However, the unspecified V-WM baseline and confounded data efficiency comparison are more serious than the baseline issues in the "Unleashing Large-Scale Video" paper (5.50, accepted), which at least described its baselines. The closest comparable is CORN (4.75, accepted), but CORN had cleaner comparisons. The paper under review has structural weaknesses that prevent full evaluation of its claims, placing it below accepted papers in this space.

MY FINAL SCORE: <score>4.0</score>
MY FINAL DECISION: <decision>Reject</decision>