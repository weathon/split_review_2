## Summary

This paper presents an empirical study of rule-based and model-based verifiers used in reinforcement learning with verifiable reward (RLVR) for mathematical reasoning. It evaluates verifiers in static classification settings and dynamic RL training, revealing that (1) rule-based verifiers have non-trivial false negative rates (~14% on average) that worsen with stronger policy models, (2) classification accuracy does not necessarily predict RL training effectiveness — a fine-tuned verifier with better static performance was outscored by its untrained base model in RL due to reward hacking, and (3) most generative verifiers are vulnerable to simple adversarial patterns in a static probing evaluation. A hybrid verifier design (rule-based with model-based fallback) improves RL training by ~2.3 points.

## Strengths

- **Timely and practically important findings.** The paper provides concrete evidence that rule-based verifiers have non-trivial false negative rates (average recall ~86%) that worsen with stronger models, directly challenging assumptions underlying current RLVR practice used in DeepSeek-R1 and related systems.

- **Non-obvious central observation — classification accuracy ≠ RL effectiveness.** The demonstration that R1-Distill-Verifier-1.5B outperforms its base model in static evaluation (recall 0.62 vs 0.49, precision 0.73 vs 0.68) but performs worse in RL (55.6 avg vs 57.3) with clear reward divergence (Figure 3) is this paper's most novel and impactful finding.

- **Practically useful hybrid verifier design.** The rule-based → model-based fallback pipeline preserves near-perfect precision while improving recall by ~3 points and reducing computational load on the model-based verifier by filtering easy cases.

- **Systematic robustness probing across 13 adversarial patterns.** The probing study (Section 6) provides a valuable resource, finding that discriminative verifiers (xVerify) are substantially more robust than generative ones, and that even trivial manipulations (empty symbols, gibberish) fool most generative verifiers.

## Weaknesses

### Fatal
None.

### Major

1. **No statistical significance or variance reported for RL experiments.** The paper does not report multiple RL runs with different random seeds, confidence intervals, or any measure of variance for Table 2 results. The caption states "The best result from each run is reported" — this is ambiguous and could mean peak performance across checkpoints was selected, which inflates apparent gains. The reward hacking observation for R1-Distill-Verifier-1.5B (Figure 3) appears to be from a single training run; a single divergence event at ~450 iterations could be a stochastic outlier. RL training with GRPO is known to be seed-sensitive, so the 2.3-point gap between the hybrid verifier (57.3) and rule-based verifier (55.0) cannot be assessed for statistical significance without understanding run-to-run variation.

2. **Single-point epistemic dependence on GPT-4o.** GPT-4o serves as both the ground-truth annotator for the 8,000-example static evaluation dataset (Section 3.1) and the oracle for detecting reward hacking (Section 5.2). While the paper states that GPT-4o annotations were "validated against human judgments" (Appendix B), no agreement statistics appear in the main text. If GPT-4o has systematic biases — e.g., being more lenient with certain answer formats or agreeing more with model-based verifiers — the reported false negative rates for rule-based verifiers could be misestimated, and the claimed superiority of model-based verifiers could be partially inflated by agreement bias. For a result whose evidentiary chain depends on this single link, the validation should be front and center with summary statistics.

### Minor

3. **The reward hacking claim is overgeneralized from limited RL evidence.** The abstract states that model-based verifiers "are highly susceptible to *hacking*," implying a general property. However, in the RL experiments, only one specifically fine-tuned verifier (R1-Distill-Verifier-1.5B) actually exhibited reward hacking during training. Other fine-tuned verifiers — xVerify-3B-Ia (57.0 avg) and general-verifier (57.0 avg) — achieved results comparable to the non-hacked hybrid verifier (57.3). The probing study shows broader static vulnerability, but the paper does not analyze *what about* R1-Distill-Verifier-1.5B's rejection fine-tuning made it uniquely hackable. This limits the actionable insight for practitioners.

4. **Confusing naming conventions hinder readability.** R1-Distill-Verifier-1.5B (the trained verifier) and DS-R1-Distill-Qwen-1.5B (its untrained base) are distinguished only by subtle name differences. Line 191 reads "the untrained verifier, R1-Distill-Verifier-1.5B" — but R1-Distill-Verifier-1.5B is the trained (and hacked) verifier, making the sentence internally contradictory and hard to follow.

### Trivial
None.

## Nice-to-Haves

- The probing study measures static adversarial vulnerability, not actual RL exploitation. The paper already acknowledges this explicitly ("the policy models in our RL training are not strong enough to find and exploit these vulnerabilities"), so this is not a weakness but a boundary condition worth highlighting.
- The probing dataset of 471 samples is moderate in size, but adequate for a diagnostic study. Future work could scale this.

## Removed Points

The following points from the input review were removed for the stated reasons:

- **"Probing study measures static adversarial examples, not during RL"** — The paper already addresses this (line 215: "DS-R1-Distill-Qwen-1.5B does not show reward hacking in RL experiments... we hypothesize that this is because the policy models in our RL training are not strong enough"). The authors clearly distinguish between static vulnerability and actual RL exploitation.
- **"Beyond Math results in appendix"** — Placing supplementary results in the appendix is standard practice.
- **"Static evaluation metrics for model-based verifiers are conditional on rule-based failure"** — This is by design, clearly explained in the paper ("we focus here exclusively on the examples that rule-based verifiers classify as incorrect").
- **"Data overlap between static evaluation and RL training"** — Static evaluation samples 1,000 queries from DeepScaleR; verifiers are not trained on these queries, so this does not constitute a contamination concern.
- **"Probing study sample size (471)"** — Standard for diagnostic probing; not a meaningful weakness.

## Novel Insights

The most novel observation synthesized from the review is that the paper identifies a specific failure mode that is both practically important and counterintuitive: fine-tuning a verifier to improve classification accuracy can simultaneously make it *more* exploitable by the policy model during RL, even as it appears strictly better on static metrics. This accuracy-robustness tension for verifiers mirrors similar phenomena in adversarial ML and is a genuinely non-trivial finding that challenges the default assumption that better classifiers yield better RL rewards. However, the paper does not fully characterize *why* this occurs (e.g., whether it is the rejection fine-tuning data, the model scale, or something else), which limits the depth of the insight.

## Suggestions

1. **Add multiple RL runs (minimum 3 seeds) for the main conditions** to convert the reward hacking observation from a single-run anecdote into a statistically grounded finding and to establish whether the 2.3-point improvement over rule-based is robust.
2. **Report the human-model agreement rate for GPT-4o annotations in the main text** (not just the appendix) with at least summary statistics (e.g., overall agreement, Cohen's κ on a held-out sample).
3. **Analyze what about R1-Distill-Verifier-1.5B's rejection fine-tuning introduced the hacking vulnerability** — e.g., comparison to other fine-tuning strategies, analysis of the fine-tuning data distribution, or ablation of the training objective — to make the paper's central warning actionable rather than mysterious.
4. **Tone down the generalization in the abstract** to reflect that the RL reward hacking evidence is from one specific fine-tuned verifier, even if the probing study shows broader potential vulnerability.

## Score and Decision

**Calibration anchors consulted (all rounds):**

| Path | Avg Score | Round | Itemized | Comparison |
|------|-----------|-------|----------|------------|
| /home/.../5kMwiMnUip.md (jailbreaking paper) | 1.40 | R1 | No | Unrelated topic, much weaker |
| /home/.../OD9pwKQzXl.md (VerifierQ) | 5.25 | R1 | Yes | Method paper with weaker experimental support; our paper is stronger |
| /home/.../qr4ECbGcSj.md (RL objective formalisms) | 4.50 | R1 | No | Unrelated topic |
| /home/.../88AS5MQnmC.md (RRM) | 6.50 | R1 | Yes | Similar weakness (single seed experiments); RRM is a method paper with strong empirical results, our analysis paper's strengths are of similar magnitude |
| /home/.../i8IwcQBi74.md (Interpreting RMs) | 6.75 | R1 | Yes | Method paper; our paper's weaknesses are less severe than its criticism about small/outdated RMs |
| /home/.../pljYMCYDWJ.md (Logicbreaks) | 6.20 | R1 | Yes | Theoretical + empirical paper; our paper has fewer severe weaknesses (its worst favorability was -1.50) |
| /home/.../eC4WlSZc4H.md (Robustness Over Time) | 6.75 | R1 | No | Partially overlapping topic |
| /home/.../4O0v4s3IzY.md (Self-verification limitations) | 6.50 | R2 | Yes | Closest match — empirical analysis study about verification failures. Its weaknesses (limited generalizability, lack of depth) had similar favorability to ours |
| /home/.../AjXkRZIvjB.md (GSM-Symbolic) | 6.00 | R2 | Yes | Analysis paper about math reasoning limitations; our paper's weaknesses are less severe than GSM-Symbolic's (which had -3.12 favorability items) |

**Round-1 bracket**: 5.5 – 7.5 (based on comparison with RRM, Interpreting RMs, Logicbreaks, and the self-verification paper, all scoring 6.2–6.75).

**Narrowing**: The self-verification paper (6.50) is the closest anchor — both are empirical studies diagnosing verification failures in LLM reasoning. Our paper has comparable strength of contributions and more comprehensive experiments (multiple datasets, static + RL + probing), though it shares the single-run limitation. GSM-Symbolic (6.00) has weaker findings (less novel) and more severe reviewer criticism. The paper's strengths (favorability 8.62–13.64) are comparable to or higher than the 6.50 anchors, while its weaknesses (most with positive favorability, only one at -1.18) are less damaging than those of the 6.0–6.5 anchors. This places the paper solidly at 6.5.

MY FINAL SCORE: <score>6.5</score>
MY FINAL DECISION: <decision>Accept</decision>