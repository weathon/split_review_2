Now let me write the complete final review.

## Summary

The paper proposes IRIS, an RL-based alignment method for autoregressive text-to-image generation that uses only an intrinsic reward — Negative Self-Certainty (NSC = -KL(U ∥ π_θ)) — requiring no external reward models or human preference data. The key insight is that, contrary to findings in text-domain reasoning where maximizing self-certainty helps, minimizing self-certainty (maximizing uncertainty) improves T2I generation by encouraging visually richer, more diverse outputs. Experiments on Janus-Pro models across GenEval, T2I-CompBench, and WISE show IRIS achieves results broadly competitive with T2I-R1 (which uses multiple external reward models) while requiring no external supervision.

## Strengths

- **Genuinely novel idea.** The core finding — that minimizing self-certainty improves T2I generation while maximizing it helps text reasoning — is non-obvious and interesting. Section 3.2 and Figure 1 clearly illustrate this contrast, and the paper convincingly demonstrates the asymmetry through ablation studies (Figures 6-7).
- **Clean, well-motivated method.** The NSC reward is simple (a single KL divergence computation), architecture-agnostic, and requires no external reward models, human preference data, or domain-specific verifiers. This substantially reduces the dependency chain for T2I alignment.
- **Comprehensive ablation study.** Section 4.3 systematically examines: training with/without semantic CoTs (Figure 5), minimizing vs. maximizing image self-certainty (Figure 6), minimizing vs. maximizing text self-certainty (Figure 7), forward vs. backward KL divergence (Figure 8), and optimizing with vs. without RL (Figure 9). This is more thorough than most method papers in this space and cleanly supports the design choices.

## Weaknesses

### Fatal
None.

### Major

- **The "superior" claim is unsupported by the presented data.** The abstract states IRIS achieves performance "competitive with or superior to external rewards," but Table 1 shows IRIS consistently trails T2I-R1 on almost every metric: GenEval Overall 1B (0.72 vs. 0.75), WISE Overall 1B (0.37 vs. 0.38), GenEval Overall 7B (0.77 vs. 0.78), WISE Overall 7B (0.48 vs. 0.50), GenEval Counting 1B (0.41 vs. 0.50), and GenEval Color Attribution 1B (0.51 vs. 0.63). While the gaps are often small and IRIS achieves this *without* any external supervision — which is itself a meaningful result — the "superior" part of the claim has no evidence in the results. The paper should claim "competitive with" and let the lack-of-external-supervision advantage be the differentiator.

- **"Best checkpoint" reporting is non-standard and potentially misleading.** Table 1 selects the single best checkpoint among steps 100–800 (8 checkpoints). This risks cherry-picking the peak of a noisy training curve rather than reporting reliably achieved performance. Standard practice is to report final performance or average over the last N checkpoints. Given that Figure 3 appears to show IRIS outperforming T2I-R1 after step 200 while Table 1 shows T2I-R1 leading, this reporting choice is consequential. The paper should report final/averaged performance alongside best-checkpoint results.

- **Figure 2's comparison is confounded and does not cleanly support the task-dependent self-certainty claim.** The figure compares text self-certainty from Qwen2.5-1.5B-Instruct on math reasoning with image self-certainty from Janus-Pro-1B on T2I generation — differing in model architecture, model size, task domain, token type (text vs. image), and absolute scale (~31–38 vs. ~19–20). Any of these confounds could explain the different trends. The conclusion that "self-certainty exhibits task-dependent behaviors" (contribution bullet 2) is too strong given this uncontrolled comparison. A cleaner test would compare within the same multimodal model (e.g., Janus-Pro) across both a text-only reasoning task and a T2I task, tracking self-certainty on text tokens in both settings.

### Minor

- **Arithmetic discrepancy in reported improvement.** The paper states a 28.8% WISE improvement for Janus-Pro-1B, but (0.37−0.28)/0.28 ≈ 32.1%. While a small error, it suggests imprecision in reporting.
- **Overclaimed advantage on natural science sub-benchmarks.** The paper claims IRIS "surpasses" T2I-R1 on biology, physics, and chemistry within WISE. The actual scores are essentially tied: Biology 0.36 vs. 0.36, Physics 0.45 vs. 0.43, Chemistry 0.22 vs. 0.22. The broader argument that IRIS generalizes better to tasks outside the external reward domain is reasonable, but the specific claim of surpassing is overstated.
- **Short training horizon (800 steps).** Training is conducted for only 800 steps. Convergence behavior beyond this point is not examined, leaving open whether the gap between IRIS and T2I-R1 would widen, narrow, or reverse. While consistent with the T2I-R1 protocol, this limitation should be acknowledged and ideally addressed with longer runs.
- **Limited discussion of failure modes.** Section 4.4 is very brief and does not discuss potential failure modes of the NSC objective, such as whether maximizing uncertainty could lead to degenerate high-entropy solutions (diverse but semantically wrong images). The "Optimize without RL" ablation (Figure 9) shows collapse occurs without RL, but the mechanism is not analyzed, and the paper does not discuss what failure modes might survive in the RL setting.

### Trivial
None.

## Nice-to-Haves

- **Analysis of post-training model behavior.** The paper uses NSC as a reward but never checks whether the trained model actually exhibits lower self-certainty at test time, or how the token-level distribution changes. This would strengthen the causal chain from reward to behavior.
- **Quantitative diversity metrics.** The paper argues lower self-certainty yields more diverse images (Figure 1) but provides no quantitative diversity measure (e.g., LPIPS, intra-class variance). Adding such metrics would substantiate the claim.
- **Human evaluation.** The central claim is that lower self-certainty aligns better with human preferences, yet no human evaluation is presented — only automated benchmarks. A small human preference study comparing IRIS, base model, and T2I-R1 outputs would directly test this claim.

## Removed Points

These points surfaced in the original review but were filtered:
- *"Bug fix in the baseline" listed as a strength* → a minor implementation detail, not a substantive contribution.
- *"T2I-R1 overtakes IRIS later in training"* → the paper's Figure 3 description states IRIS achieves higher scores after ~200 steps, directly contradicting this claim.
- *"Ablation uses external rewards that T2I-R1 was trained on"* → noted but actually a strength that IRIS does well on metrics it never optimized for; the ablation uses these as evaluation metrics, which is standard.
- *"No human evaluation" / "No diversity analysis"* → moved to Nice-to-Haves.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. **Tone down the "superior" claim** to "competitive with," and let IRIS's advantage (no external supervision) speak for itself.
2. **Report final or averaged performance** alongside best-checkpoint results in Table 1.
3. **Add a within-model controlled comparison** (e.g., Janus-Pro on a text-only reasoning task) to cleanly support the task-dependent self-certainty claim.
4. **Extend training beyond 800 steps** to demonstrate convergence behavior, or at minimum discuss this as a limitation.
5. **Expand the limitations section** to explicitly discuss potential failure modes of the NSC objective.

MY FINAL SCORE: <score>6</score>
MY FINAL DECISION: <decision>Accept</decision>