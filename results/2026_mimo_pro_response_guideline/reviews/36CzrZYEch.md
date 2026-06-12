Now I have a comprehensive calibration picture. Let me finalize the review.

**Calibration summary:**
- **Rejected papers (4.5–5.75):** jQP5o1VAVc (5.75, scaling AR T2I — SOTA but limited novelty), bO31lfEdos (5.00, human-free RL for hallucination), zkMRmW3gcT (4.80, design space for AR image gen)
- **Borderline accepted (6.0):** Let8OMe20n (6.0, confidence-aware reward optimization for T2I), 38E4yUbrgr (6.0, LM self-improvement by RL contemplation), lHbLpwbEyt (6.0, self-synthesized data for multimodal models)
- **Solid accepted (6.2–6.8):** cJQ1K2fjpD (6.20, fine-grained verifiers), sgAp2qG86e (6.25, JetFormer), kIP0duasBb (6.67, TTA with CLIP reward), TmCcNuo03f (6.75, engagement T2I), 4w99NAikOE (6.80, IterComp)
- **Strong accepted (7.25+):** tmBKIecDE9 (7.25, Motif — intrinsic motivation), SI2hI0frk6 (7.60, Transfusion)

**Initial bracket: 5.5–7.0**

IRIS has stronger novelty than the rejected 5.0–5.75 papers (clear task-dependent self-certainty finding, comprehensive ablations, first intrinsic-reward T2I RL). It's comparable to the 6.0 accepted papers (Let8OMe20n has similar domain, similar quality issues). It's slightly below the 6.5+ papers due to overclaiming and biased ablation evaluation.

**Final score: 6.0** — The core scientific contribution (task-dependent self-certainty behavior, first intrinsic-reward T2I RL) is genuine and valuable, placing it clearly above rejected papers. But consistent overclaiming ("superior" when never beating the baseline on overall scores) and potentially biased ablation metrics prevent it from reaching the 6.5+ range of stronger accepted papers.

---

## Summary
This paper proposes IRIS, a reinforcement learning framework for autoregressive text-to-image generation that uses Negative Self-Certainty (NSC) — the negative KL divergence between the model's output distribution and a uniform distribution — as an intrinsic reward. The central finding is that, in contrast to text reasoning where maximizing self-certainty improves performance, T2I generation benefits from *minimizing* self-certainty. Applied to Janus-Pro (1B and 7B), IRIS achieves meaningful improvements over the base model (9.1%, 13.3%, 28.8% on GenEval, T2I-CompBench, WISE for 1B) using no external reward models, though it consistently falls short of the external-reward baseline T2I-R1 on overall benchmark scores.

## Strengths
- **Genuinely novel empirical observation**: Figure 2 cleanly demonstrates that RL alignment with external rewards increases text-token self-certainty during math reasoning (blue line rising from ~31.5 to ~36.5) but decreases image-token self-certainty during T2I generation (orange line falling from ~20.2 to ~19.0). This task-dependent behavior is a new and well-supported finding.
- **Comprehensive ablation studies isolating each design choice**: Five ablation experiments (Figs. 5–9) cover semantic CoT, minimize vs. maximize image SC, minimize vs. maximize text SC, forward vs. backward KL, and RL vs. direct optimization. Effect sizes are large and consistent, supporting the method's design decisions.
- **Meaningful improvements with zero external supervision**: Table 1 shows IRIS on 1B achieves 0.72 on GenEval (vs. base 0.66), competitive scores on several T2I-CompBench subcategories, and 0.37 on WISE (vs. base 0.28) — all without any external reward models.
- **Insightful task-dependent analysis**: Section 4.2 identifies that IRIS excels on categories like natural science (WISE) where external rewards (HPSv2, DINO) provide no relevant signal, while T2I-R1 has advantages on tasks where its external rewards are specifically trained.
- **Baseline implementation bug correction**: Section 4.1 identifies that T2I-R1 uses incorrect chat templates for Janus-Pro, and the paper re-runs all experiments with the correct template, strengthening comparison validity.
- **RL necessity demonstrated**: Figure 9 shows that directly maximizing NSC via gradient descent causes model collapse (GIT and ORM scores drop to 0.00), while GRPO-based RL maintains stable performance.

## Weaknesses

### Fatal
None.

### Major
- **Overclaiming in abstract and framing**: The abstract states IRIS achieves "performance that is competitive with or superior to external rewards." Table 1 shows IRIS never exceeds T2I-R1 on any overall benchmark score for either model size: GenEval 1B (0.72 vs. 0.75), WISE 7B (0.48 vs. 0.50), T2I-CompBench 7B (behind on shape, texture, 2D-spatial). The word "superior" is unsupported. The percentage improvements cited (9.1%, 13.3%, 28.8%) are relative to the *base* Janus-Pro, not the external-reward baseline. Reframing honestly — "recovers a large fraction of external-reward performance with zero external supervision" — would be more accurate and more convincing.
- **Ablation evaluation using baseline's reward models as metrics**: Section 4.3 evaluates all ablations using HPSv2, DINO, GIT, and ORM — the exact reward models used to train T2I-R1. The paper claims these are "simple and unbiased metrics" because they are not in IRIS's training objectives. However, these models encode preferences aligned with the external-reward paradigm, potentially biasing results. The ablations should be evaluated on GenEval/T2I-CompBench/WISE for consistency with the main results.

### Minor
- **No mechanistic explanation for why lower self-certainty helps**: The paper's central scientific claim rests on correlational observations and empirical validation but does not investigate *why* peaked distributions on image tokens produce simpler images. Even a preliminary analysis (e.g., token-level distribution entropy over spatial positions, or codebook utilization statistics) would strengthen the contribution.
- **Missing analysis of the largest performance gap**: On GenEval counting (1B), IRIS scores 0.41 vs. T2I-R1's 0.50 — the single largest gap on any subcategory — yet this is not discussed.
- **Generalizability claim unsubstantiated**: The paper claims IRIS is "agnostic to the model architecture or dataset" but only experiments on Janus-Pro. Section 4.4 acknowledges this as future work, but the method section claim should be tempered.

### Trivial
None.

## Nice-to-Haves
- Human evaluation, even small-scale, to validate the claim of producing images "better aligned with human preferences."
- Show full checkpoint trajectories in tabular form to help understand consistency across training steps.
- Report CoT diversity metrics to validate that NSC on text tokens encourages more diverse semantic CoTs.

## Removed Points
These points are flagged to be removed, treat them with caution:
- No missing related works flagged per policy.
- No formatting/typographical issues flagged per policy (parser artifacts).

## Novel Insights
The paper's genuinely novel contribution is the empirical demonstration that self-certainty exhibits opposite effects across modalities: maximizing it benefits text reasoning while minimizing it benefits image generation. This is well-supported by Figure 2 (parallel training experiments on Qwen2.5 for math and Janus-Pro for T2I) and is a new observation. The complementary insight that intrinsic rewards cover different failure modes than external rewards (excelling on natural science tasks where HPSv2/DINO are irrelevant) is also informative.

## Suggestions
- Reframe the abstract and introduction honestly: replace "competitive with or superior to" with language like "achieves a substantial fraction of external-reward performance without any external supervision."
- Re-run ablation evaluations on the main benchmarks (GenEval, T2I-CompBench, WISE) for consistency.
- Add analysis of the counting subcategory gap (0.41 vs. 0.50 on GenEval 1B).
- Consider a brief mechanistic investigation of why peaked distributions collapse spatial diversity.
- Temper the generalizability claim or provide evidence from at least one additional model family.

## Score and Decision

**Retrieved anchors (all rounds):**
| Path | Avg Score | Round | Comparison |
|------|-----------|-------|------------|
| jQP5o1VAVc | 5.75 | 2 | Scaling AR T2I — SOTA but limited novelty over MAR; IRIS has clearer novel finding |
| bO31lfEdos | 5.00 | 1,2 | Human-free RL for hallucination — limited generalizability; IRIS is broader and more novel |
| zkMRmW3gcT | 4.80 | 1 | Design space for AR image gen — rejected despite SOTA; IRIS has stronger insight |
| Let8OMe20n | 6.00 | 1,2 | Confidence-aware reward for T2I — similar domain, accepted with uniform 6s |
| 38E4yUbrgr | 6.00 | 2 | LM self-improvement by RL contemplation — accepted, similar quality tier |
| lHbLpwbEyt | 6.00 | 2 | Self-synthesized data for multimodal — accepted, comparable contribution |
| cJQ1K2fjpD | 6.20 | 2 | Fine-grained verifiers for VL alignment — accepted, self-alignment |
| sgAp2qG86e | 6.25 | 2 | JetFormer — accepted, broader contribution |
| kIP0duasBb | 6.67 | 1,2 | TTA with CLIP reward — accepted, cleaner framing |
| TmCcNuo03f | 6.75 | 1 | Engagement of T2I — accepted, novel concept + large dataset |
| 4w99NAikOE | 6.80 | 1 | IterComp — accepted, iterative feedback for T2I |
| tmBKIecDE9 | 7.25 | 2 | Motif — intrinsic motivation from AI — accepted, stronger novelty |

**Round-1 bracket: 5.5–7.0**. IRIS has stronger novelty than rejected papers at 5.0–5.75 but overclaiming issues compared to accepted papers at 6.5+.

**Round-2 narrowing: 5.5–6.5**. IRIS is clearly above jQP5o1VAVc (5.75, rejected) but slightly below the 6.5+ accepted papers due to overclaiming. Comparable to the 6.0 accepted papers (Let8OMe20n, 38E4yUbrgr).

**Final score: 6.0** — Genuine novel insight, comprehensive ablations, first intrinsic-reward T2I RL. Overclaiming and biased ablation evaluation prevent a higher score.

MY FINAL SCORE: <score>6.0</score>
MY FINAL DECISION: <decision>Accept</decision>