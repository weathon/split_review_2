## Summary

This paper introduces Insertion Language Models (ILMs), a novel sequence generation paradigm where tokens are inserted one at a time at arbitrary positions, in contrast to left-to-right autoregressive models (ARMs) and fixed-length masked diffusion models (MDMs). The key methodological departure is removing tokens completely (rather than masking them) and learning to predict insertion positions jointly with token identities. A biased training objective is used to avoid high variance in trajectory marginalization. Empirically, ILMs achieve near-perfect accuracy on planning tasks (star graphs, zebra puzzles) where both ARMs and MDMs struggle badly, and produce competitive text generation and infilling results on LM1B and TinyStories.

## Strengths

1. **Strong planning-task results that are clearly not incremental.** On Star_hard, ILM achieves 99.1% exact match vs. MDM's 21.0% and ARM's 23.0% (Table 1). On Star_medium, ILM achieves 100% vs. MDM's 36.5% and ARM's 75.0%. These are qualitative regime changes, not small improvements. The hypothesized mechanism (relative vs. absolute position information, line 147) is well-reasoned and consistent with the results.

2. **Genuinely novel core idea.** The ILM formulation—removing tokens completely (rather than masking them) and inserting one at a time at learned positions—is a clean conceptual departure from both ARMs (fixed order) and MDMs (fixed-length masked sequences). The insight that token removal avoids the fixed-length constraint of masking while one-at-a-time insertion avoids the simultaneous-unmasking problem is clearly articulated and distinct from prior work.

3. **Well-motivated diagnosis of MDM limitations.** Section 2 (lines 68–73) crisply identifies two genuine weaknesses of MDMs: (a) simultaneous unmasking violates sequential dependencies, and (b) fixed-mask-count inputs preclude arbitrary-length infilling. The examples (e.g., "chef added sugar...healthier" vs. "sugar...sweeter") are simple but effective illustrations of these failure modes.

## Weaknesses

### Fatal
None.

### Major

1. **The biased training objective is asserted but never analyzed.** The paper acknowledges the training objective in Equation 2 is biased (line 79: "we use a biased training objective") and states that the exact Monte Carlo objective would have "extremely high variance" (line 18). However, it provides no analysis—theoretical or empirical—of the bias magnitude, its dependence on sequence length or removal ratio, or settings where it could fail. This matters because there is a structural mismatch: the *training* objective aggregates over all removed tokens simultaneously (a bag-of-tokens prediction: the target distribution $d(k, v; \mathbf{x}, b)$ is an average over insertion orders), while the *inference* procedure (Algorithm 2) inserts tokens one at a time sequentially. Without any diagnostic, the reader must take on faith that this approximation preserves the correct sequential generation behavior. This is a significant methodological gap for a paper whose central contribution is a new training objective for a new model class.

### Minor

2. **The text-evaluation metric has a systematic bias that is inadequately discussed.** The primary metric in Table 2 is per-token NLL under Llama 3.2 3B, an autoregressive model. Non-autoregressive models like ILMs do not optimize for left-to-right predictability, so this metric conflates "good generation" with "predictable under an ARM's inductive bias." The paper does use Prometheus-2 (Figure 5) as a complementary metric, which shows ILM outperforming ARM on several linguistic dimensions. However, the abstract's claim that "ILMs perform on par with ARMs" is too strong given the LM1B NLL gap (ILM 4.67 vs. ARM 3.94, an ~18.5% difference), and the paper's own discussion (line 215) attributes this gap to "training token efficiency and scaling laws" without further investigation. The text-generation claims should be softened to reflect their metric-dependent nature.

3. **The MDM baseline uses a different architecture (DDiT with AdaLN) with more parameters.** The paper acknowledges this on lines 133–134 ("MDMs with the same hyperparameters as ILMs have slightly more trainable parameters") but does not control for it. The wall-clock comparison in Figure 6 is particularly confounded: it compares ILM and MDM on a speed-vs-quality Pareto frontier where the architectures differ, so the comparison conflates method differences with architectural differences. The planning-task gaps are so large (99.1% vs. 21% on Star_hard) that architecture alone cannot explain them, but the text-generation and speed comparisons warrant an architecture-controlled ablation.

4. **The stopping classifier's train-inference distribution shift is not discussed.** During training (Algorithm 1), the stopping classifier sees partial sequences produced by random token removal. During inference (Algorithm 2), it sees sequences produced by the model's own insertion decisions, which likely have different statistical properties (certain tokens are more likely to be inserted early). This is a known pitfall for learned stopping criteria, yet the paper does not comment on whether or why the classifier generalizes across this shift.

5. **No Fill-in-the-Middle (FIM) baseline for single-segment infilling.** The paper argues ARMs cannot perform infilling without specialized training (line 245). While this is true for multi-segment infilling, Bavarian et al. (2022) introduced FIM for single-segment infilling. Including FIM as a baseline for the single-segment experiments (Table 3) would help calibrate what "good" infilling quality looks like.

6. **The Prometheus LLM-judge results are reported only as a figure (Figure 5) without numerical values.** This prevents precise comparison. The values should be tabulated.

### Trivial

7. **Equation 2 has ambiguous notation.** The loss uses $c_{i_k, i_{k+1}}(v; \mathbf{x})$ which depends on $v$, but the sum over $k$ does not include an explicit $\sum_v$. A summation over vocabulary items is implied to form a cross-entropy loss but is not stated.

8. **The Insertion Transformer reimplementation uses a "single transformer version"** (line 147) of the original method, which used separate left/right RNN encoders (Stern et al., 2019). The paper is transparent about this, but the reported weakness (17.5–35.2% on star tasks) should note that this may not reflect the original IT's performance.

## Nice-to-Haves
- A small-scale diagnostic of the biased objective (comparing against a Monte Carlo estimator or exact marginalization on a synthetic task) would greatly increase confidence in the method.
- An architecture-controlled ablation (e.g., ILM with AdaLN or MDM without it) would clarify whether the text-generation and speed differences are due to formulation or architecture.
- Numerical values for the Prometheus evaluation should be provided in a table.

## Removed Points
These points from the input review are removed and listed here for transparency:

- **"MDM baseline difference is a critical evidential weakness"** — Downgraded from Critical to Minor. The paper is transparent about the architecture difference, and the planning-task results are so decisive (99.1% vs 21%) that no plausible architecture confound can explain them. Keeping the concern as a minor issue for the text-generation speed comparison.

- **"ARMO outperforming ILM on Zebra (91.2% vs 90.0%) not discussed"** — Removed. The paper does discuss this on line 180: "it even gets close to the performance achieved by the ARM trained on oracle solver decomposed sequence order." The critic's framing as a missing discussion is inaccurate.

- **"IT baseline is not a faithful reimplementation"** — Downgraded to Trivial. The paper is transparent about using a single-transformer version.

- **"FIM baseline missing"** — Downgraded from a standalone weakness to Minor (#5) and softened from the critic's framing ("the omission is notable") to a nice-to-have. The paper's focus is on methods that handle *arbitrary* (including multi-segment) infilling without specialized training, which FIM cannot do.

- **Generic sweeping concerns from the "Strengthening the Paper on Its Own Terms" section** — These were folded into the specific weaknesses above (biased objective diagnostic → Major #1; stopping classifier shift → Minor #4; architecture-controlled comparison → Minor #3) and Nice-to-Haves.

- **"Equation 2 notation" and "IT reimplementation"** — Kept but downgraded to Trivial.

## Novel Insights
None beyond the paper's own contributions.

## Suggestions
1. Add a small-scale analysis of the biased objective (synthetic task where exact marginalization is feasible) to characterize the bias magnitude and when it breaks down.
2. Soften the abstract's "on par with ARMs" to reflect the metric-dependent nature of the comparison (e.g., "competitive with ARMs on some metrics and moderately worse on others").
3. Provide numerical values for the Prometheus evaluation in a table.
4. Include a discussion of the stopping classifier's generalization under inference-time distribution shift.
5. Consider adding a Fill-in-the-Middle baseline for the single-segment infilling experiments.

## Calibration

**Round 1 — Bracketing (5.5–7.5).** After reading the paper and filtering the reviewer input, I searched the calibration corpus for papers on (a) insertion/any-order language models, (b) masked diffusion for text/planning, (c) novel sequence generation with biased objectives, and (d) evaluation of non-autoregressive models.

**Round 2 — Narrowing.**

*Anchors retrieved (all rounds):*

| Path | Avg Score | Round | Comparison to ILM |
|------|-----------|-------|-------------------|
| `UbOzNf6hGq.md` (FiLM) | 4.25 (Reject) | R1 | Similar topic (any-order generation via MLM) but clearly weaker: less novel, more limited results. ILM is stronger. |
| `FJWT0692hw.md` (SequenceMatch) | 6.00 (Accept) | R1/R2 | Different approach (imitation learning for AR models). Comparable strength but ILM is more novel. |
| `0JjsZC0w8x.md` (COrAL) | 5.75 (Reject) | R1/R2 | Order-agnostic modeling. ILM has stronger planning results and more novel formulation. |
| `tyEyYT267x.md` (SAD3-LM) | 8.00 (Accept) | R1/R2 | Strong, theoretically grounded diffusion+AR interpolation. ILM is less theoretically developed but has a more novel core idea. |
| `MJNywBdSDy.md` (DDPD) | 5.75 (Accept) | R1 | Planner+denoiser for discrete diffusion. ILM is comparable in quality, slightly more novel conceptually. |
| `WNvvwK0tut.md` (Scaling MDMs) | 6.50 (Accept) | R1 | Scaling MDMs—different contribution type. |
| `71mqtQdKB9.md` (SEDD) | 6.60 (Reject) | R1 | Score entropy diffusion. Similar quality tier but accepted. |
| `SLw9fp4yI6.md` (LM Arithmetic) | 7.00 (Accept) | R2 | Controlled generation. Different subarea, similar quality. |
| `oXYZJXDdo7.md` (Retrieval) | 7.00 (Accept) | R2 | Different method, similar quality tier. |
| `sL2F9YCMXf.md` (Energy-based Diffusion) | 6.75 (Accept) | R2 | Diffusion LMs with EBM. Comparable quality. |
| `koza5fePTs.md` (Planning Benchmark) | 2.00 (Reject) | R1 | Planning benchmark paper—much weaker, very different contribution type. |

**Round-1 bracket:** 5.5–7.5. **Round-2 narrowing:** The ILM paper is clearly stronger than FiLM (4.25) and COrAL (5.75), comparable to DDPD (5.75, Accept), SequenceMatch (6.00, Accept), and Energy-based Diffusion LMs (6.75, Accept). It is weaker than SAD3-LM (8.00) which has deeper theoretical analysis and larger-scale experiments. The novelty of the core idea and the strength of the planning results push it above the middle of the band, while the unanalyzed biased objective prevents it from reaching the top tier.

**Final score: 6.5** — a borderline-to-clear accept. The paper makes a genuinely novel contribution and provides compelling empirical evidence on planning tasks. The main weakness (unanalyzed biased objective) is significant but does not invalidate the core empirical findings; it can be addressed with additional analysis.

## Score and Decision

MY FINAL SCORE: <score>6.5</score>
MY FINAL DECISION: <decision>Accept</decision>