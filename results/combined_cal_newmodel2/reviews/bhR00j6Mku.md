Now I have sufficient data for calibration. Let me now produce the final review.

**Calibration Summary:**

| Anchor | Score | Round | Itemized | Comparison |
|--------|-------|-------|----------|-----------|
| Evading Data Contamination Detection (Nk1MegaPuG) | 4.25 | R1 | Yes | Less technical depth; proposed a simple rephrasing attack. Current paper has rigorous ablation isolating mechanism and theoretical analysis. Clearly stronger. |
| How much can we Forget (Nsms7NeU2x) | 6.75 | R1 | Yes | Comparable quality in experiment+theory design. Current paper has tighter theory-experiment connection. |
| To the Cutoff and Beyond (m2NVG4Htxs) | 6.75 | R1 | Yes | Interesting longitudinal analysis but limited methodology. Comparable quality. |
| LM Detectors Easily Optimized Against (4eJDMjYZZG) | 6.00 | R1/R2 | Yes | Similar theme of detector fragility. Current paper is more comprehensive (10 methods, 2 scenarios, theory). Slightly stronger. |
| Detecting Pretraining Data from LLMs (zWqr3MQuNs) | 6.25 | R2 | Yes | Simple method with solid experiments. Current paper has greater technical depth. |
| Numerical Pitfalls in Policy Gradient (u4dORXVAnx) | 5.60 | R2 | No | Different topic (RL numerical stability). Less relevant. |

**Bracket:** Round 1 placed the paper in the 5.5–7.5 range. Within this bracket, the paper compares favorably to the 6.00–6.25 anchors (more comprehensive evaluation, tighter theory-experiment link) and is comparable to the 6.75 anchors. The missing error bars and overclaiming on Stage II prevent it from reaching 7+. **Final score: 6.5.**

Now writing the review:

## Summary
2-3 sentence summary.

## Strengths
- strength 1
- etc.

## Weaknesses
### Fatal
None

### Major
- No variance estimates for AUROC

### Minor
- Stage II overclaiming
- Theory-empirical mismatch
- "Broad class" generalization
- Stage II mechanism not distinguished from alternatives

### Trivial
None specific after filtering

## Nice-to-Haves
...

## Removed Points
...

## Novel Insights
...

## Suggestions
...

## Score and Decision
Score: 6.5, Decision: Accept## Summary

This paper presents the first systematic study of benchmark contamination detection in large reasoning models (LRMs), structured around two realistic contamination scenarios: (Stage I) contamination introduced during the base-model-to-LRM transition via SFT and RL, and (Stage II) contamination applied as a final SFT step to an already-capable LRM. The key findings are that (1) GRPO training can conceal SFT contamination evidence, with the effect traced to the PPO-style importance sampling/clipping objective through a clean ablation chain, and (2) extensive SFT contamination with CoT on advanced LRMs largely evades existing memorization-based detection methods.

## Strengths

- **The Stage I ablation chain (Table 3) that pinpoints the clipping/importance-sampling term as the concealment mechanism is genuinely well-executed.** The sequence — SFT contamination is detectable → GRPO conceals it → RAFT (no clipping) does not conceal → RAFT++ (adds clipping) does → removing clipping from GRPO/RAFT++ restores detectability — is a controlled experimental chain that convincingly isolates the cause. This is the strongest evidence in the paper.

- **The two-stage taxonomy of contamination (Stage I: during base-model-to-LRM transition via SFT+RL; Stage II: contamination applied as final SFT to an advanced LRM) is well-motivated** and captures realistic development pipelines that are not conflated in prior work.

- **Breadth of evaluation:** 10 detection methods across 6 challenging reasoning benchmarks with multiple model families (Qwen-7B, Llama-8B, DeepSeek-R1-Distill variants, OpenThinker). The consistent pattern across all methods in Stage I after GRPO (uniform AUROC drop) strengthens the conclusion beyond what any single method could provide.

- **The theoretical analysis is linked to targeted experiments:** the paper tests specific predictions (removing clipping restores detectability, RAFT vs. RAFT++ comparison) rather than presenting theory in isolation. This theory-experiment connection is the right structure for this kind of empirical analysis.

## Weaknesses

### Fatal
None.

### Major

- **No variance or uncertainty estimates reported for any AUROC value.** All values in Tables 2, 3, and 5 are single point estimates with no standard deviation, confidence interval, or significance test. This is especially consequential for Stage II (Table 5), where values of 50–66% AUROC are the basis for the claim that detection methods "perform near random guesses" — without variance estimates, it is impossible to assess which values are statistically distinguishable from chance and which are not. For Stage I, the differences are large enough (LiRA dropping from ~89% to ~80%, Min-K% from ~75% to ~61%) that the qualitative pattern is robust even without error bars. But for Stage II, where the "near random guess" claim is central, this omission limits the evidentiary strength of the conclusion.

### Minor

- **The Stage II "near random guess" characterization overstates the data.** Table 5 shows several methods achieving AUROC of 60–66% on multiple model/benchmark combinations (e.g., LiRA on DeepSeek Qwen-14B: 65.55%; Loss on DS Llama-8B: 62.59%). An AUROC of 65% is well above random chance and does not support the "≈ 50%" label used in the table caption (line 263). The real finding — that detection performance drops from 75–89% (Stage I pre-RL) to 50–65% (Stage II) — is still important but should be characterized precisely rather than as universal failure.

- **The theoretical analysis (Section 3.2) assumes that "the RL training is performed on the benchmark data" (line 188),** but the main empirical Stage I experiments train GRPO on clean data, not benchmark members. While the "RL w/ Clean&Mem" condition in Table 2 partially addresses this, the mismatch between the theory's training-data assumption and the primary empirical setting is not discussed.

- **The claim that a "broad class of RL methods" may exhibit concealment (abstract, line 255) goes beyond what was tested.** Only GRPO and RAFT++ (both PPO-derived) were evaluated. The paper uses hedging language ("suggests," "may"), but the scope of generalization is broader than the evidence supports.

- **The Stage II causal explanation — that LRMs "internalize" knowledge and generalize to non-members — is plausible but not distinguished from simpler alternatives** (e.g., CoT trajectories being too long/diverse for memorization; detection methods being ill-suited to LRM response formats). The paper presents this as "may indicate" (line 330), which is appropriately hedged, but should more explicitly acknowledge that the proposed mechanism is one of several possible explanations consistent with the data.

### Trivial
None.

## Nice-to-Haves

- A single controlled experiment testing whether the Stage II detection failure is specific to CoT-based contamination or persists with question-answer pairs (non-CoT) would strengthen the causal claim. If detection succeeds without CoT, it would directly support the paper's proposed mechanism.
- Including training hyperparameters (epochs, batch sizes, learning rates) in the main text rather than solely in the appendix would aid quick assessment of how realistic the contamination scenarios are.

## Removed Points

These points from the input review are flagged to be removed; treat them with caution.

- **Missing hyperparameter/training details in main text:** The critic faulted the paper for deferring implementation details to the appendix. This is a formatting choice, not a substantive flaw; the paper references the appendix and states the key design decisions (8 responses per question, 156 training steps for GRPO) in the main text.
- **Conclusion directions are "vague":** The critic acknowledged this "is not a limitation for an analysis paper." Removed.
- **Request for additional Stage II mechanism experiments (CoT vs. non-CoT):** This is a nice-to-have extension, not a flaw in the existing analysis.
- **Criticism about "rendering members and non-members indistinguishable" wording:** This is a very minor phrasing issue in one sentence; the actual evidence (Figure 3) shows substantial overlap consistent with the claim.
- **Criticism that the Stage II explanation is speculative:** The paper uses "may indicate" (line 330) and presents the explanation as a plausible hypothesis, not a concluded mechanism. The core empirical finding that detection methods struggle does not depend on this explanation.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. Add confidence intervals (e.g., via bootstrapping) for all Stage II AUROC values, and for Stage I values where differences across methods are small.
2. Replace the "≈ 50%" characterization of Stage II results with a more precise statement of the observed range (e.g., "50–65% AUROC, with most methods below 60%").
3. Acknowledge the gap between the theory's training-data assumption (benchmark data) and the main empirical setting (clean data) in Section 3.2.
4. Scope the "broad class of RL methods" generalization more precisely to PPO-style algorithms using importance sampling and clipping.
5. Present the Stage II causal mechanism as one possible explanation and explicitly note that alternative mechanisms are not ruled out.

MY FINAL SCORE: <score>6.5</score>
MY FINAL DECISION: <decision>Accept</decision>