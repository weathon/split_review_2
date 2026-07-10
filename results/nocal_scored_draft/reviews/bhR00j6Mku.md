Now I have all the information needed. Let me compile the final consolidated review.

## Summary

This paper presents the first systematic study of benchmark contamination detection in Large Reasoning Models (LRMs), structured around two realistic scenarios: (Stage I) contamination introduced during SFT that can be concealed by subsequent GRPO/RL training, and (Stage II) SFT with chain-of-thought (CoT) applied to already-competent LRMs as a final training step. Through experiments across 6 reasoning benchmarks, 10 detection methods, and multiple model families, the paper demonstrates that existing contamination detection methods are fragile in both scenarios. In Stage I, it isolates PPO-style importance sampling/clipping as the causal mechanism for concealment via careful ablations (Table 3). In Stage II, it shows that CoT contamination produces large performance gains while leaving minimal detectable evidence, challenging the memorization assumption underlying most detection methods.

## Strengths

- **The two-stage contamination framework is well-motivated and realistic.** Distinguishing pre-LRM contamination (SFT → RL pipeline) from post-LRM contamination (final SFT with CoT) maps directly onto the actual development pipeline used for models like DeepSeek-R1 (Figure 1). This is not a contrived setup.

- **The Stage I result is convincingly isolated through careful ablations.** The paper does not merely observe that GRPO reduces detection AUROC; it systematically rules out alternative explanations. Table 3 provides the cleanest evidence: removing clipping from GRPO reduces the Loss detector AUROC drop from −14.22 points to −2.20 points, cleanly attributing concealment to PPO-style importance sampling/clipping. Further SFT (even 4 additional epochs on clean data) does NOT conceal contamination, ruling out "forgetting through more training."

- **The Stage II negative result is important and potentially impactful.** Showing that SFT contamination with CoT on advanced LRMs yields large performance gains (e.g., +11.76 points for DeepSeek-R1-Distill-Qwen-14B, Table 4) while AUROC across ten detection methods hovers near chance (Table 5) is genuinely alarming. The finding that LRMs generalize to distributionally similar unseen samples, closing the log-prob gap that detectors depend on, challenges the memorization assumption underlying most existing detection work.

- **The empirical scope is substantial:** 6 reasoning benchmarks, 10 detection methods spanning 5 categories, 2 base models for Stage I, and 4 advanced LRMs for Stage II. This breadth makes the negative findings harder to dismiss as benchmark- or method-specific.

## Weaknesses

### Fatal
None.

### Major
- **No uncertainty quantification for any AUROC value.** Tables 2, 3, and 5 report point estimates without confidence intervals, standard deviations, or statistical tests. This is the most significant weakness because the paper's central negative claims (detection methods fail) hinge on whether observed AUROCs are genuinely near 0.5 or merely appear so due to noise. Values like 55–65% (e.g., LiRA on DS Qwen-14B: 65.55%, Min-K% on DS Llama-8B: 62.42%) cannot be properly interpreted without knowing their variability. The 8-rollout averaging addresses within-question variance but does not capture variance across random member/non-member splits or training runs. The paper would be substantially strengthened by bootstrapped confidence intervals or repeated-trial results showing that these values are or are not statistically distinguishable from 0.5.

### Minor
- **The "near random guess" characterization is overstated for some method-model combinations.** While the overall claim (most methods fail) holds, Table 5 shows non-trivial signal: LiRA on DS Qwen-14B averages 65.55%, LiRA on OpenThink-7B averages 62.74%, Min-K% on DS Llama-8B averages 62.42%. The Table 5 caption states "AUROC ≈ 50%" for all methods, which flattens meaningful variation. The paper should acknowledge whether this residual signal is practically exploitable.
- **The "broad class of RL methods" claim is empirically narrow.** The generalization that "a broad class of RL methods may inherently exhibit similar concealment capability" (Abstract, Sec. 3.2.1) is supported for only two algorithms (GRPO and RAFT++, both PPO-style). While the paper appropriately hedges with "may" and grounds the claim in the identified mechanism, evaluating at least one non-PPO RL method (e.g., plain REINFORCE) would empirically bound the scope.
- **No limitations section.** The paper makes strong negative claims and prescriptive recommendations (releasing checkpoints, advancing beyond memorization-driven detection) but does not discuss limitations such as the specific benchmarks tested, the narrow set of base models, or the idealized nature of the contamination simulation. This is a notable omission for an empirical analysis.
- **Overstrong conclusion claim.** The statement that "Detection approaches that are solely based on log-probs or mitigation approaches such as minor benchmark modifications, are definitely inadequate in this context and risk systematically failing" (line 334) is more categorical than a single study can fully support. The results convincingly demonstrate fragility, but the absolute dismissal exceeds the evidence.
- **Theoretical analysis contains heuristic claims.** Parts of the theoretical analysis (Sec. 3.2) rely on plausibility claims asserted without justification — e.g., non-members have "much more prominent" covariance effects "due to high variance in correct trajectories loss" (line 218). Theorem 3.1 provides a valid first-order expansion, and the empirical work (Table 3) carries the real weight. The heuristic framing does not undermine the result but weakens the theoretical section's rigor.

### Trivial
None.

## Nice-to-Haves
- Add confidence intervals or bootstrapped standard errors for all AUROC values (the single highest-leverage improvement for strengthening the paper).
- Investigate boundary conditions of Stage II: test whether detection degrades uniformly across benchmarks with different distributional similarity to the training set.
- Deeper Stage II analysis of what the LRM acquires during CoT contamination (e.g., does it memorize specific reasoning steps or internalize general patterns? Is confidence calibrated differently for members vs. non-members?).
- Evaluate at least one non-PPO RL method (e.g., REINFORCE with baseline) to empirically bound the scope of the concealment claim.

## Removed Points
None. All points raised by the reviewer were verified against the paper and found to have substance; none were removed.

## Novel Insights
None beyond the paper's own contributions. The review process confirmed the paper's main findings but did not surface unexpected connections or alternative interpretations that the paper itself does not already articulate.

## Suggestions
1. **Add uncertainty quantification** (confidence intervals or repeated-trial results across random splits) for all AUROC values. This is the single most impactful improvement and would substantially strengthen the paper's central negative claims.
2. **Adjust the "near random guess" language** in Table 5's caption and main text to acknowledge the variation across methods — e.g., "most methods perform near random guesses" rather than "AUROC ≈ 50%."
3. **Add a brief limitations section** acknowledging the scope of empirical coverage and the idealized nature of the contamination simulation.
4. **Softne the conclusion's "definitely inadequate"** language to better reflect the level of evidence provided by a single study.

## Score and Decision

The paper has genuine empirical strengths: the Stage I causal attribution is well-executed through careful ablations, the Stage II negative finding is timely and impactful, and the experimental scope is substantial. The core findings are solid. However, the absence of uncertainty quantification for all AUROC values is a real evidential gap — it prevents precise assessment of how close to random the Stage II results truly are. This is addressable in revision. The paper is clearly above the acceptance threshold.

MY FINAL SCORE: <score>7</score>
MY FINAL DECISION: <decision>Accept</decision>