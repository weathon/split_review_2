## Summary
This paper systematically ablates components of the GRPO loss function to determine which are essential for training LLMs on mathematical reasoning. The authors identify two key findings: (1) negative feedback is important for stable learning, and (2) PPO-style clipping and policy ratios can be removed without degrading performance. Based on this, they propose RGR (REINFORCE with Group Relative Advantage), a simplified variant that retains group-relative advantage estimation but drops PPO-style constraints. Experiments on 9 math/STEM benchmarks across Qwen2.5 (0.5B, 1.5B) and Llama3.2 (1B) models show RGR is broadly competitive with GRPO.

## Strengths

- **Well-motivated research question.** Asking whether GRPO's multi-component loss is unnecessarily complex is timely and practically relevant given GRPO's widespread adoption in LLM post-training.

- **Clean, principled ablation design.** The three ablations (positive-only advantages, removing PPO clipping, removing advantage estimation) are logically structured to isolate individual components of the GRPO loss. This systematic decomposition is the paper's primary methodological contribution.

- **Diverse evaluation suite.** Nine benchmarks spanning English math, Chinese math, and STEM (in both English and Chinese) test generalization beyond the training distribution nontrivially. Including Chinese benchmarks is a strength.

- **Training curves (Figure 1) provide genuine process-level insight.** The response-length and reward trajectories over training steps reveal collapse dynamics (e.g., REINFORCE and RAFT on 0.5B, GRPO-pos's response-length decay) that benchmark scores alone would obscure. This is the paper's strongest evidence.

## Weaknesses

### Major

- **The "negative feedback is indispensable" claim is overstated relative to the data.** The paper asserts that methods ignoring negative feedback "exhibit instability, collapse, and consistently degraded performance" (Conclusion) and that negative feedback is "essential" (Abstract). However, on the larger models (Qwen2.5-1.5B, Llama3.2-1B), the evidence tells a more nuanced story. GRPO-pos on Qwen2.5-1.5B achieves Math-English 35.7 vs. GRPO's 37.3 and Chinese Math 65.3 vs. 65.7 — modest degradations of 1–2 points, not collapse. On Llama3.2-1B, GRPO-pos is broadly comparable to GRPO (Math-English 19.8 vs. 20.1, Chinese Math 30.3 vs. 30.1). The clear "collapse" is specific to the 0.5B model. The evidence supports a **size-dependent** phenomenon (small models are fragile; larger models are more robust under positive-only training), not a universal principle. The paper's framing should be hedged accordingly.

- **No statistical significance or variance information.** All benchmark results (Tables 1–3) are single numbers with no error bars, confidence intervals, or mention of multiple seeds. This is particularly problematic because:
  - Many RGR-vs-GRPO differences are very small (e.g., Llama3.2-1B Math-English: 20.2 vs. 20.1; Qwen0.5B: 26.5 vs. 25.6).
  - RL training at small scales (~70 steps, 1,800 training instances) is known to be high-variance. Without multiple runs, the reader cannot determine whether the reported differences (including the "17/27" count of RGR wins) represent signal or noise.
  - The paper's central comparative claim — that RGR "surpasses" GRPO — is not reliably supported without variance estimates.

### Minor

- **RGR retains KL regularization, so the finding is that PPO-style *clipping* is unnecessary, not that "PPO-style constraints" broadly are.** RGR's objective (Equation 2) still includes the β·D_KL penalty against a reference model, which is itself a constraint preventing policy divergence. The paper does not ablate this term, so the finding is more precisely: *PPO-style clipping is unnecessary when KL regularization is present.* An ablation removing both clipping and KL would strengthen the claim.

- **Limited experimental scale.** Training uses 1,800 instances from GSM8K for ~70 steps on 0.5B–1.5B models, far from the scale where GRPO is typically deployed (hundreds of thousands of problems, 7B+ models, thousands of steps). The paper acknowledges this (Conclusion), but the gap between the experimental regime and the generality of the conclusions is large enough to raise questions about transferability.

- **Naming inconsistency for the proposed method.** The same model is called "RGR A" (Section 3.2), "RGR" (Tables 1–3), "RGRa" (Figure 1 caption), and "RGRA" (Conclusion). Terminology should be unified.

- **Decontamination scope for instruction-tuned models.** The paper states GSM8K was "explicitly decontaminated from the training corpora" citing Qwen et al. (2025). However, the baseline models are *instruction-tuned* variants (Qwen2.5-0.5-it, etc.). It is not clear whether these instruction-tuned models were additionally fine-tuned on GSM8K as part of their instruction-tuning data, which could conflate new learning with reinforcement of already-seen examples. This should be clarified.

### Trivial

None.

## Nice-to-Haves

- An ablation that removes **both PPO clipping and KL regularization** would test whether KL alone provides sufficient constraint.
- **Larger models and longer training** (understandably constrained) would substantially strengthen generality.
- The Countdown reasoning-traces analysis (Figure 2) is anecdotal (one example per method). Quantitative metrics (e.g., proportion of responses with explicit reasoning steps) would strengthen this section.

## Removed Points

These points from the input review were removed with justification:

- **"REINFORCE with Direct Rewards" results not in tables.** The critic claimed quantitative results for this ablation are missing. However, the paper's third ablation ("REINFORCE with Direct Rewards," Section 3.2) is vanilla REINFORCE, and its results *are* reported under "REINFORCE" in Tables 1–3 (e.g., Qwen2.5-1.5B: Math-English 30.9, Chinese Math 63.2). The claim that it "collapses even in the larger 1.5B model" is substantiated by the response-length collapse in Figure 1(d). **Removed: factually incorrect — data is present.**

- **`o_{t < t}` notation in PPO equation.** Flagged as a typo for `o_{<t}`. This is a PDF extraction artifact or formatting issue. **Removed: formatting/parser artifact per policy.**

- **Missing code link.** The reproducibility statement's empty link is a PDF extraction artifact stripping URLs. **Removed: parser artifact.**

- **RAFT on 1.5B "far from collapse."** The critic used RAFT's 1.5B results to argue against the negative-feedback claim, but this is subsumed by the retained Major weakness about GRPO-pos overclaiming; the RAFT point adds no independent weakness.

## Novel Insights

The harsh critique surfaces one genuinely novel observation that the paper itself does not fully articulate: the **size-dependent nature of positive-only training failure**. The paper presents collapse at 0.5B and modest degradation at 1.5B as a single story about negative feedback being "essential." But juxtaposing these results reveals a more interesting pattern — the need for negative feedback may be inversely related to model capacity. This is a testable hypothesis the paper could explicitly formulate: as models grow, the negative-advantage signal may shift from a collapse-prevention necessity to a marginal performance booster. The review also correctly notes that the training dynamics (Figure 1) are the paper's strongest evidence, a claim the paper underuses relative to the benchmark tables.

## Suggestions

1. **Add variance information.** Run the main comparisons with at least 3 random seeds and report means ± standard deviations. This is the single highest-leverage improvement.

2. **Hedge the "negative feedback" claim.** Explicitly acknowledge the size-dependent nature of the finding — collapse at 0.5B, modest degradation at 1.5B.

3. **Unify the naming** of the proposed method throughout the paper.

4. **Clarify decontamination status** of the instruction-tuned baseline models' training data beyond pretraining corpora.

5. **Consider adding the KL-ablation** (removing both PPO clipping and KL regularization) to test whether KL alone is the active constraint.

MY FINAL SCORE: <score>6.0</score>
MY FINAL DECISION: <decision>Accept</decision>