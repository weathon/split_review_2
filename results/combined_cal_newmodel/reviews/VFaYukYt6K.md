Now I have enough calibration data. Let me write the final consolidated review.

**Round-1 Bracket:** 4.0–5.5. The paper's novel ideas (adaptive quantization + latent search) are stronger than typical 3-range papers, but the evaluation gaps prevent it from reaching the 6+ range where papers need thorough experimental validation.

**Final Score: 5.0.** Grounded in the favorability comparison: the paper shares with Large Trajectory Models (5.00) the pattern of a novel architecture with insufficient experimental validation (missing baselines, no uncertainty quantification), and sits below ITPNet (6.75) which had stronger experiments. The strengths (adaptive soft quantization favorability ~12, behavior transfer ~12) are genuine, but the major weaknesses (planning without baselines favorability ~0.8, qualitative evidence ~-0.9) are too large to overcome without revision.

---

## Summary

This paper proposes training a maximally compressed conditional autoencoder for trajectories (3 tokens, dimensionality 3) using adaptive soft quantization and causal masking, then at test time performing greedy search over the discrete token space to optimize arbitrary user-specified objectives. The core idea — using a learned latent bottleneck both for compression and as a search space for test-time planning — is novel and well-motivated by recent work on image tokenization. The paper presents experiments on behavior transfer, prediction via variance-minimization, planning with two objectives (left turn, speed reduction), and multi-agent interaction modeling.

## Strengths

- **Novel synthesis of ideas.** The core proposal — train a maximally compressed conditional autoencoder with causal, discrete latent tokens, then perform motion planning by greedy search in this latent space — is genuinely new for robotics trajectory generation. The paper draws a clean intellectual line from image tokenization (TiTok, VQGAN) to a setting where test-time objectives are natural and useful.
- **Adaptive soft quantization is a practical contribution.** The noise-based soft quantization with an adaptively scheduled noise level (Eq. 1–2) avoids codebook collapse and auxiliary-loss engineering typical of VQ-based methods, while still producing near-discrete latents. Figure 2 shows this adaptive schedule meaningfully outperforms fixed noise injection, a concrete and reproducible engineering result.
- **Causal ordering + greedy search is elegant and efficient.** The combination of causal masking, nested dropout, and test-time hard quantization yields a latent space where greedy token-by-token search (requiring only 24 decoder evaluations) can optimize arbitrary objectives at 115 trajectories/second on an RTX 6000 Ada.
- **Environment-conditioned behavior transfer (Sec. 3.1) is genuinely compelling.** The token-swapping experiment (Fig. 5a) and the cross-environment decoding of a single token sequence into ~250 different intersection scenarios (Fig. 5b) demonstrate that the latent space has learned semantically meaningful, environment-relative representations — not just trajectory compression. This is a genuine finding not obvious from the architecture.

## Weaknesses

### Major

- **Planning evaluation (Sec 3.4) lacks baselines and kinematic feasibility checks.** Table 3 reports success rates for two user-specified objectives but compares only against a "None (original scenario)" row with no planning baseline — no rule-based trajectory optimizer, no sampling-based planner, no diffusion guidance method. The evaluation checks only static road-edge contact; it does not address acceleration limits, jerk, curvature constraints, collision rates with other agents, or multi-objective trade-offs. The paper claims "motion planning" (title, abstract) but the experiments demonstrate *controllable trajectory generation*, a less ambitious claim.
- **The prediction experiment (Sec 3.3) uses a variance-minimization heuristic without theoretical justification.** The model is trained only for reconstruction; at test-time it searches for tokens minimizing decoded trajectory variance. The paper provides no analysis of when or why low variance corresponds to correctness. Comparing against end-to-end prediction models (MTR, DriveGPT) is not informative since the method solves a different problem (reconstruction + variance-minimizing search). While the paper honestly notes it is "not competitive with highly tuned state-of-the-art trajectory prediction methods," the comparison in Table 2 serves mainly to show the method works less well than specialized models, which is neither surprising nor informative.
- **Several central claims rely on qualitative or single-point evidence.** (a) Behavior transfer (Sec 3.1): three hand-picked token-swapping examples; the library-of-behaviors experiment (~250 environments) is described qualitatively with no quantitative success rate, failure analysis, or metric. (b) Multi-agent interaction (Sec 3.5, Fig 6): a single qualitative example supports the claim that the joint trajectory decoder adjusts other agents' behavior. (c) Multi-agent reconstruction (Table 5): referenced with no baseline comparisons to contextualize the claim.
- **No uncertainty quantification on any result.** Tables 1–4 report single-point results without standard deviations, confidence intervals, or multi-seed experiments. Several comparisons are close (0.298 vs 0.301 in Table 1, 0.788 vs 0.792 in Table 4), making it impossible to know whether differences are meaningful or within noise.
- **No limitations discussion.** For a framework proposed in a safety-critical domain (autonomous driving), the paper does not discuss failure modes: when latent search might get stuck in local optima, what types of objectives are ill-suited, or why ~25% of left-turn and ~37% of speed-reduction searches fail (whether due to genuinely impossible scenarios vs. method limitations).

### Minor

- **The interaction understanding experiment (Sec 3.5, Table 4) is somewhat tangential.** It tests a different pipeline (LoRA fine-tuning of Qwen3-4B with projection layers) that does not use token search at all. It demonstrates that the autoencoder's encoder produces informative representations — a valid claim but separate from the paper's core thesis about search-based planning.
- **Greedy search outperforming the learned encoder at reconstruction (Table 1) raises an ambiguity the paper does not discuss.** If search beats the encoder at reconstruction, the encoder may not be learning a truly compact representation so much as the decoder is good at producing reasonable trajectories from many latent codes. The paper treats this as a strength but does not explore the implications.
- **Hyperparameter sensitivity and train-test mismatch.** The adaptive noise schedule uses ADE_target as a fixed hyperparameter with no sensitivity analysis. The hard quantization at test time creates a train-test mismatch (training uses continuous noisy latents; test uses hard rounding) that is asserted to work but not analyzed.

### Trivial

- The architectural contributions are not clearly separated from borrowed work — the environment encoder follows MTR (Shi et al., 2022) closely, but the paper does not cleanly delineate novel vs. adopted components.

## Nice-to-Haves

- Add at least one trajectory-optimization or diffusion-guidance baseline to Table 3 to contextualize the token search results.
- Report standard deviations or confidence intervals on all main results.
- Add a limitations section discussing failure modes, local optima, and ill-suited objectives.
- Provide quantitative metrics for the behavior transfer experiments (e.g., fraction of cross-environment decodings that are collision-free and within-road).
- Analyze the train-test mismatch from hard quantization and its effect on downstream task performance.

## Removed Points

*Critique about Table 5 being in the appendix* — removed per rule: the parser strips appendix sections from all papers, so this is not a genuine weakness.
*Critique that the Smith (1971) citation is a "stretch"* — a judgment about writing style rather than a substantive methodological flaw.
*Critique about the prediction section's comparison being "misleading"* — the paper itself acknowledges it is "not competitive," so the comparison is presented transparently; this weakens the force of the criticism.
*Critique that the decoder's output distribution lacks comparison to alternatives* — the rule says to remove criticisms about unfair comparisons when the asymmetry favors baselines, not the author's method.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. Reframe the paper's contribution as "controllable trajectory generation via latent space search" rather than "motion planning" unless planning baselines and kinematic feasibility checks are added.
2. Either remove the prediction section (3.3) or reframe it as a qualitative demonstration of the latent space's properties, removing the direct comparison against SOTA end-to-end prediction models.
3. Add quantitative metrics to the behavior transfer experiments — even basic collision-free rates and within-road fractions would substantially strengthen the most compelling results.
4. Report standard deviations across multiple seeds or bootstrap estimates for all tables.
5. Add a limitations section discussing when latent search fails, what objectives are not well-suited, and the train-test mismatch from hard quantization.

## Score and Decision

**Score: 5.0 / Decision: Reject**

**Calibration anchors used (all rounds):**

| Path | Avg Score | Round | Itemized | Comparison |
|------|-----------|-------|----------|------------|
| Large Trajectory Models (r125wFo0L3) | 5.00 | R1 | Yes | Less novel ideas but more thorough experiments; similar score |
| Latent Diffusion Planning (k1qVBh5fnb) | 3.40 | R1 | Yes | Less novel, simulation-only; our paper is stronger |
| RedMotion (72MSbSZtHv) | 5.33 | R1 | Yes | More complete WOMD eval but novelty debated; comparable quality |
| Words in Motion (J9eKm7j6KD) | 4.80 | R1 | No | Mixed reviews (5,8,3,3,5); different sub-problem |
| ITPNet (mDIXfHvoqH) | 6.75 | R1 | Yes | Stronger experiments, ablation studies; our paper is less complete |
| PcLast (NlBuWEJCug) | 4.50 | R2 | Yes | Similar latent-space-for-planning concept; less domain relevance |
| Subwords as Skills (sAOtKKHh1i) | 5.00 | R2 | Yes | Similar strength (novel idea) / weakness (missing baselines) profile |
| Predictive aux objectives in deep RL (agPpmEgf8C) | 8.00 | R1 | Yes | High-quality experiments and writing; very different topic |
| GAP (H6i47PKXSN) | 5.25 | R2 | No | End-to-end driving; similar score range |

**Score justification:** The paper's core ideas — adaptive soft quantization, causal token ordering with greedy search for trajectory generation, and environment-relative behavior transfer — are genuinely novel and well-motivated. However, the evaluation falls short of fully supporting the claimed contribution. The central planning experiments lack baselines and kinematic feasibility checks, the prediction section is a heuristic exercise compared against trained prediction models, and several key claims rest on qualitative or single-point evidence. These gaps are significant enough that the paper in its current form does not meet the bar for acceptance. A substantially revised version with proper planning baselines, quantitative behavior transfer metrics, uncertainty quantification, and an honest reframing of the contribution could be a worthwhile contribution.

MY FINAL SCORE: <score>5.0</score>
MY FINAL DECISION: <decision>Reject</decision>