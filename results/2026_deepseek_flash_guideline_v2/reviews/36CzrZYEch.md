Now let me produce the final consolidated review.

## Summary

The paper proposes **IRIS** (Intrinsic Reward Image Synthesis), a reinforcement-learning framework for autoregressive text-to-image (T2I) models that uses **only an intrinsic reward** — Negative Self-Certainty (NSC), defined as forward KL divergence from the model's output distribution to a uniform distribution — eliminating the need for human preference data or domain-specific external verifiers. The key empirical discovery is a task-dependent reversal of self-certainty: while maximizing self-certainty benefits text-based reasoning, *minimizing* self-certainty improves T2I generation because low-certainty models produce visually richer, more diverse images. Experiments on Janus-Pro (1B and 7B) across GenEval, T2I-CompBench, and WISE show results competitive with external-reward baselines.

## Strengths

1. **First intrinsic-only RL alignment for T2I generation.** The paper is the first to use a purely intrinsic reward (NSC = −KL(U∥π_θ)) for T2I alignment, requiring no human annotations, object detectors, VQA models, or any external verifier (Section 3.2). The Related Work (Section 2) clearly confirms that prior T2I alignment work relied on human-labeled data or external models, making this a genuine novel contribution to the area.

2. **Empirical discovery that self-certainty behaves oppositely for T2I vs. language.** Figure 2 shows that during RL training with external rewards, text self-certainty on Qwen2.5-1.5B-Instruct (math reasoning) increases from ~31.5 to ~36.5, while image self-certainty on Janus-Pro-1B (T2I) decreases from ~20.2 to ~19.0. This supports the central claim that self-certainty's effect is task-dependent. The claim is further rigorously validated through controlled ablations in Section 4.3 (Figures 6 and 7), which cleanly demonstrate on the *same model* that minimizing image self-certainty improves performance while maximizing it causes rapid collapse.

3. **IRIS achieves competitive results with external-reward baselines across three benchmarks.** Table 1 shows IRIS results are comparable to T2I-R1 (which uses four external reward models) on both model scales. On Janus-Pro-1B: GenEval Overall 0.72 vs. 0.75; T2I-CompBench Complex 0.3793 vs. 0.3820; WISE Overall 0.37 vs. 0.38. On Janus-Pro-7B the gap narrows further (GenEval 0.77 vs. 0.78). IRIS also wins on several subcategories (Colors 0.88 vs. 0.86, Position 0.66 vs. 0.64, Color attribute binding 0.7946 vs. 0.7924, Physics on WISE 0.45 vs. 0.43).

4. **Systematic ablation study isolating each design choice.** Section 4.3 ablates five decisions (CoT vs. no CoT in Figure 5; minimize vs. maximize image SC in Figure 6; minimize vs. maximize text SC in Figure 7; forward vs. backward KL in Figure 8; RL vs. direct optimization in Figure 9), each evaluated on four independent external reward metrics. This provides robust, disentangled evidence for the specific design choices in IRIS. Figure 6 is particularly convincing: maximizing image self-certainty leads to rapid collapse, directly supporting the paper's core claim.

5. **Careful experimental hygiene — identified and fixed a template bug in prior work.** Section 4.1 correctly identifies that T2I-R1 (Jiang et al., 2025) used the wrong chat template for Janus-Pro (using Janus's "User"/"Assistant" keys instead of Janus-Pro's "<User>"/"</Assistant>" keys) and re-ran all experiments with the correct template. This demonstrates unusual care in ensuring a fair comparison.

## Weaknesses

### Fatal

None.

### Major

1. **Figure 3 / Table 1 discrepancy needs resolution.** Figure 3's alt-text claims IRIS with CoT achieves "higher scores than T2I-R1 (external) after approximately 200 training steps" across *all three* benchmarks. However, Table 1 reports "best checkpoint" results (selected from steps 100–800) where T2I-R1 leads on all three aggregate metrics (GenEval: 0.75 vs. 0.72, non-overlapping ±0.01 CIs; T2I-CompBench Complex: 0.3820 vs. 0.3793; WISE: 0.38 vs. 0.37). The figure's own caption (line 130) weakens the claim to "comparable results" on T2I-CompBench and WISE, adding further ambiguity. While this could be mathematically consistent if T2I-R1 peaks before the crossover point (~steps 100–150) and then declines while IRIS rises more slowly to a lower peak, the paper provides no explanation. The authors should clarify where each method's best checkpoint falls on the training curves and reconcile the two presentations. Without this, the empirical evaluation is ambiguous.

### Minor

1. **Figure 2 compares confounded variables.** The observation that text self-certainty rises while image self-certainty falls during RL training compares Qwen2.5-1.5B-Instruct (text-only LLM on math reasoning) with Janus-Pro-1B (multimodal LLM on T2I generation). These differ in architecture, task, token modality, and training data — all confounded. The paper's later controlled ablations (Figures 6, 7) on the same model do support the core claim, so this does not threaten the method. But the foundational observation as presented is weaker than it appears, and the paper should present it more cautiously as a motivating correlation.

2. **"Emergence of long-form reasoning" is supported only by a single qualitative example.** Section 4.2 presents one example (Figure 4) and references the appendix for more. While this is illustrative, quantitative measures (e.g., average CoT length over training, diversity) would substantially strengthen the claim.

3. **Limited analysis of why 7B gains are smaller.** Gains on the 7B model (1.3–6.5%) are much smaller than on the 1B model (9.1–28.8%), and in several subcategories IRIS underperforms the base model (e.g., Colors 0.88 vs. 0.89, Color Attri. 0.61 vs. 0.62 on GenEval; Shape 0.5155 vs. 0.5661 on T2I-CompBench). The paper attributes this to "stronger capability of larger base models" but does not analyze whether the intrinsic reward is partially redundant with existing capabilities or whether the method is more helpful for less capable models. This has implications for generality.

4. **Ablation evaluation uses reward models that train the baseline.** The paper correctly notes these are used only for evaluation, not training. However, since these same metrics informed design decisions (choosing which NSC variant, KL direction, etc.), the claim of operating entirely "without external signals" is slightly attenuated — method development was indirectly guided by these external metrics. The paper acknowledges this use case but could be more explicit about this limitation.

### Trivial

None.

## Nice-to-Haves

- A small-scale human evaluation study would strengthen claims about alignment with human preferences.
- Reporting total compute budget (GPU hours, number of training runs) would aid reproducibility.
- A controlled version of Figure 2 on the *same model* (measuring both text and image token self-certainty within Janus-Pro) would remove confounds.

## Removed Points

- **"Superior to external rewards" claim is overclaimed (Harsh Critic):** Removed. The abstract says "competitive with or superior to," which is accurate. IRIS is within ~4% on headline metrics and wins on several subcategories. The contribution list (bullet 3) uses "competitive performance." The paper does not overclaim.
- **No human evaluation (Harsh Critic):** Demoted to Nice-to-Have. The paper's contribution is a method that avoids external supervision; requiring a human evaluation study as a condition of acceptance would be scope-creep. The automated benchmarks (GenEval, T2I-CompBench, WISE) are the community standard.
- **Compute budget not reported (Harsh Critic):** Demoted to Nice-to-Have. Standard reproducibility concern but not a flaw that threatens any claim.
- **Why RL is necessary — explanation is vague (Harsh Critic):** Removed. The paper provides a coherent explanation: GRPO's grouping and clipping mechanism provides conservative updates, whereas direct optimization causes collapse (Figure 9 shows this clearly). The paper also notes this is standard practice in prior intrinsic-reward work.
- **Foundational observation in Figure 2 is confounded (Harsh Critic's framing as "Critical Issue #2"):** Retained but downgraded to Minor (#1 above). The confounds are real but do not threaten the core method, which is supported by the controlled ablations.

## Novel Insights

None beyond the paper's own contributions. The two reviews are largely convergent: they agree on the paper's key strengths (first intrinsic-only T2I alignment, thorough ablations, careful experimental setup) and on the Figure 3/Table 1 issue as the primary concern. The harsh critic's other "critical issues" either misread the evidence (the "superior to" claim) or overstate the severity of confounds that the paper's controlled experiments already address.

## Suggestions

1. **Resolve the Figure 3 / Table 1 ambiguity.** This is the single most important fix. Show where each method's best checkpoint falls on the training curves and explain the temporal dynamics. If T2I-R1 peaks early (before the crossover point), state this explicitly. If the figure description is inaccurate, correct it.
2. **Present the Figure 2 observation as a motivating correlation** rather than implying a causal demonstration, given the confounded variables. The controlled ablations already provide the rigorous evidence.
3. **Add quantitative metrics for CoT emergence** (e.g., average CoT length, diversity, or semantic similarity over training steps).
4. **Expand the analysis of 7B results** to explore when IRIS helps versus when it hurts, and whether the method is differentially beneficial across model scales.

## Score and Decision

MY FINAL SCORE: <score>6.5</score>
MY FINAL DECISION: <decision>Accept</decision>