Now I have enough to draft the review. Let me check Figure 3's table values against Table 2 more carefully before proceeding.

The Figure 3 table (lines 212–225) shows Qwen-7B DR.GRPO at Math=57.6, Logic=39.2 — but Table 2 shows DR.GRPO for Qwen2.5-Math-7B at Math Acc=55.7, Logic Acc=26.2. And Llama-8B DR.GRPO in Figure 3 is 22.6/18.9, while Table 2 shows 22.0/14.9. CANON-Dynamic for Llama-8B in Figure 3 is 35.2/35.2, but Table 2 shows 22.6/18.9 for Cosin-First-Inter-Later-Intra. These are clearly not the same numbers.The Round 1 bracket places this paper between **5.5 and 7.5** — clearly above the borderline reject papers (3.5–5.5) due to the strong theoretical contribution and empirical breadth, but with the Figure 3 data inconsistency and post-hoc scheduling concerns preventing a clean high-score placement. Let me do one more pass to narrow within the 5.5–7.5 range.**Round 1 bracket: 5.5–7.5.** The paper is clearly above the 3.5–5.5 band (stronger theory and more comprehensive experiments than, e.g., F0GNv13ojF avg 5.17), and the Figure 3 data inconsistency and post-hoc scheduling concern prevent a 7.5–8.5 placement.

**Round 2 narrowing:** Anchors in 5.5–7.5 include "A Long Way To Go" (RLHF length, avg 6.0, rejected with solid investigation but no algorithmic contribution) and GReaTer (avg 6.67, accepted, cleaner contribution). CANON's theoretical clarity, multi-model/multi-task empirics, and efficiency Pareto frontier place it above the 6.0 cluster. The Figure 3 data inconsistency is a genuine problem requiring author action but doesn't invalidate any table results. Final score: **6.5**.

---

## Summary
CANON (Conditional Advantage Estimation) is a reinforcement learning framework for large reasoning models that regroups sampled responses into high/low groups based on a target metric (entropy or response length) and computes inter-group and intra-group advantages. The method unifies GRPO-family estimators (DR.GRPO is shown to be a special case at μ=0.5 with equal groups), theoretically proves selective metric amplification without directional bias, and demonstrates consistent gains on math and high-complexity logic tasks across three open-weight LLMs, plus a superior Pareto frontier for efficient reasoning.

## Strengths
- **Precise theoretical unification with DR.GRPO (Eq. 7, Theorem 1).** DR.GRPO is proven to be exactly CANON with μ=0.5 and equal group sizes. This is a mathematically clean derivation that gives the design space a principled anchor, not a post-hoc story.
- **Selective amplification ablation (Table 4).** The contrast between direct numerical scaling (A=A×2), Entropy Adv, and CANON directly tests whether gains come from signal amplification generally or metric-specific amplification. Numerical scaling hurts logic (26.2→25.1) while CANON-Intra lifts it (29.1); CANON-Inter leads on math (57.6). This cleanly supports Theorem 2's selective amplification claim.
- **Efficiency Pareto frontier (Figure 4, Section 5.3).** Multiple α values sweep CANON-Eff's frontier; multiple hyperparameter settings sweep baselines' frontiers, enabling apples-to-apples comparison. The catastrophic collapse of Length Reward(+) at coefficient 0.005 (54.8→22.5 accuracy) versus CANON-Eff's graceful degradation is concrete and practically important.
- **Interpretable training dynamics (Figure 2f / Figure 6).** The "gain of rethinking" diagnostic measures whether reflection patterns actually improve accuracy rather than just consuming tokens. The finding that CANON-Intra develops positive rethinking gains while CANON-Inter does not provides mechanistic grounding for the task-specific advantage recommendations.

## Weaknesses

### Fatal
None.

### Major
- **Figure 3 table values do not match Table 2.** The data table accompanying the radar chart (lines 212–225) contains numbers inconsistent with Table 2. For Qwen-7B, Figure 3 assigns DR.GRPO Math=57.6 and Logic=39.2; Table 2 shows DR.GRPO Math Acc=55.7 and Logic Acc=26.2 (notably, 57.6 is CANON-Inter's math score from Table 1, not DR.GRPO's). For Llama-8B, Figure 3 shows CANON-Dynamic at 35.2/35.2, while Table 2 shows the selected Cosin strategy at 22.6/18.9 — the Figure 3 values are roughly 1.5× higher with no stated normalization. If the radar chart uses a relative/normalized scale (0–100 relative to some reference), this must be stated explicitly; if these are raw accuracy percentages, multiple values are wrong. This figure is the paper's primary cross-model summary and the discrepancy is a genuine data integrity concern.

- **CANON-Dynamic scheduling selected post-hoc across all strategy × model combinations.** Section 5.2 tests four scheduling strategies across three models (12 experiments) and selects per-model winners by observed results to define CANON-Dynamic. The paper partially acknowledges this (line 207: "A specifically designed strategy is acceptable for better performance in practice"), but provides no held-out validation. With no principled blind selection rule, CANON-Dynamic's superiority over DR.GRPO risks reflecting evaluation-set overfitting rather than a generalizable method. This limits the generality claim for CANON-Dynamic, though the individual CANON-Inter/CANON-Intra results in Table 1 stand independently.

### Minor
- **Tension between "no directional bias" framing and Section 4.3.** The abstract and introduction emphasize that CANON avoids presupposing directional preferences, yet Section 4.3 introduces α<1 on the longer-response group, which is explicitly a directional preference (longer-is-worse). The Theorems cover only the α=1 case. The paper frames this as "fine-grained control" without acknowledging the inconsistency with its own stated motivation. The efficiency use case is valid and well-evaluated on its own terms, but needs an explicit distinction from the directional-agnostic α=1 regime.

### Trivial
- Section 4.1 specifies equal-sized groups per Theorem 1 but does not address the odd-G edge case (when G is odd, the median response is borderline). Minor implementation ambiguity.
- Table 2 bold/underline formatting has apparent inconsistencies in the Llama-8B block that should be checked.

## Nice-to-Haves
- Variance estimates (error bars across ≥2 seeds) for MATH-500 and OlympiadBench on the primary model would help establish whether the 1.9-point math gain is reliable, since AIME/AMC already use Avg@10 for variance reduction.
- Extending the "gain of rethinking" analysis (Figure 2f, Figure 6) to all three models in Table 2 would provide mechanistic validation that the scheduling works for the stated reason across model families.
- Clarifying whether ZebraLogic data is included in RL training or represents out-of-domain generalization would strengthen interpretation of the logic results.
- A brief gradient-level explanation of why the asymmetric form of Eq. 9 (applying α differently in the positive and negative group branches) is equivalent to down-weighting longer-response gradients would improve clarity.

## Removed Points
*These points are flagged to be removed, treat them with caution.*

- **"Failure modes of baselines not empirically demonstrated"**: The critic noted that Entropy Adv performs reasonably (best MATH-500 at 87.6) and the failure claim is unverified. However, Section 5.3 / Figure 4 does empirically demonstrate the catastrophic hyperparameter sensitivity of Length Reward(+). The claim is partially but not fully supported. Demoted from weakness because the key point (hyperparameter fragility) IS demonstrated for the efficiency baseline; removed from the review as a standalone weakness.

- **"Eq. 9 asymmetric form unexplained"**: Valid but purely presentational; too minor to affect paper evaluation.

- **"Single-run Pass@1 without variance"**: Legitimate but moved to Nice-to-Haves since single-run evaluation is standard in the RLVR community at this scale.

- **"Numerical scaling gain may stem from effective LR increase"**: Plausible speculation, but verifying with a LR sweep is a nice-to-have rather than a required fix.

## Novel Insights
The conditional regrouping framework reveals a clean decomposition of GRPO-family advantage estimation: DR.GRPO implicitly mixes inter- and intra-group signals equally (μ=0.5) without knowing which component drives a given task. CANON makes this choice explicit and shows it matters: inter-group advantage improves math (by selecting the metric trend leading to higher reward) while intra-group advantage improves complex logic (by amplifying correct responses in the lower-reward group, which tends to be the more exploratory/rethinking group). The "gain of rethinking" diagnostic is a particularly useful instrument that connects training dynamics to task-specific advantage selection, and could be broadly applicable to evaluating whether RL-induced reflection patterns are genuine.

## Suggestions
- Reconcile Figure 3's table values with Table 2, or clearly label the radar chart as using a normalized/illustrative scale rather than raw accuracy.
- Define a principled (non-post-hoc) rule for scheduling strategy selection — e.g., using the training accuracy range as a continuous input signal — and validate it on a held-out model architecture to establish CANON-Dynamic as a general-purpose scheduling approach.
- Separate the directional-agnostic α=1 regime (main contribution) from the directed efficiency α<1 regime (Section 4.3) in the introduction and abstract to avoid inconsistency in motivation.

## Score and Decision

**Anchor papers retrieved:**

| Path | Avg Score | Round | Comparison |
|------|-----------|-------|------------|
| F0GNv13ojF | 5.17 | R1 | RLVR reward design for LLM math; less theoretically grounded, narrower evaluation than CANON |
| OD9pwKQzXl | 5.25 | R1 | Q-learning verifiers for LLM reasoning; similar scope, less principled contribution |
| 0er6aOyXUD | 5.40 | R1 | Reward model robustness for math; empirical-only, no algorithmic contribution |
| sNtDKdcI1f | 6.00 | R2 | RLHF length correlations; solid analysis but no new method, comparable in scope |
| GtpubstM1D | 5.71 | R2 | LLM math reasoning data strategies; broader but less technically sharp |
| e2NRNQ0sZe | 6.25 | R2 | RL with LLM priors; similar combination of theory + empirics |
| uvZDQvjULn | 6.00 | R2 | Bi-objective CLM, Pareto frontier; comparable efficiency framing |
| HGCk5aaSvE | 6.50 | R2 | Pareto prompt optimization; comparable scope and contribution quality |
| fWRBheSJth | 6.67 | R1 | GReaTer prompt optimization; accepted, cleaner contribution without data issues |
| S6cBH99BhB | 6.50 | R2 | Multilingual LLM reasoning; solid empirics, no theory |
| VOAMTA8jKu | 7.00 | R2 | VLM math benchmark; different domain, accepted for systematic contribution |
| tyEyYT267x | 8.00 | R1 | Diffusion LM interpolation; stronger theoretical contribution, clean results |
| rfdblE10qm | 8.00 | R1 | BT reward model theory; cleaner theory + strong empirics, no data issues |

**Round 1 bracket:** 5.5–7.5. Paper is clearly above RLVR papers averaging ~5.2 due to stronger theory and multi-model evaluation, and below 7.5–8.5 due to the Figure 3 data inconsistency and post-hoc scheduling concern.

**Round 2 narrowing:** Anchors cluster at 6.0–6.67 for papers accepted with solid but not exceptional contributions (GReaTer 6.67, Pareto Prompt 6.50, e2NRNQ0sZe 6.25). CANON's theoretical clarity (Theorem 1/2 + DR.GRPO unification), multi-task/multi-model empirics, and efficiency frontier place it at or above GReaTer's tier. The Figure 3 data concern is a genuine issue requiring author response, which nudges the score slightly below 7.0. Final score: **6.5**.

MY FINAL SCORE: <score>6.5</score>
MY FINAL DECISION: <decision>Accept</decision>