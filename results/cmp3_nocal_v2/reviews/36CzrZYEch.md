## Summary

This paper proposes IRIS, the first RL-based alignment method for autoregressive text-to-image (T2I) generation that uses only an intrinsic reward signal — the Negative Self-Certainty (NSC), defined as the negative forward KL divergence between the model's output distribution and a uniform distribution — without any external reward models or human-labeled data. The key finding is that minimizing self-certainty (maximizing uncertainty) improves T2I generation on Janus-Pro models, opposite to findings in text-only reasoning. On GenEval, T2I-CompBench, and WISE benchmarks, IRIS achieves results broadly comparable to T2I-R1 (which uses four external reward models) while requiring zero external supervision.

## Strengths

1. **A genuinely counterintuitive empirical finding, well-demonstrated through ablation.** The paper identifies that minimizing self-certainty (maximizing uncertainty) improves T2I generation, contrary to findings in text-only reasoning (Zhao et al., 2025b; Zhang et al., 2025a). This finding is substantiated by Figures 6 and 7, which isolate the direction of optimization: maximizing image SC collapses performance while minimizing it improves it, and minimizing text SC consistently outperforms maximizing it. The ablation design controls for other factors and provides clear causal evidence.

2. **Zero external supervision is a meaningful practical advantage.** IRIS operates entirely on the model's own output distributions, removing the bottleneck of collecting human preference data or training domain-specific verifiers. The paper correctly frames this as a complement to, not a replacement for, external rewards. Achieving results within striking distance of T2I-R1 (which uses four external reward models) while using no external signals is genuinely interesting.

3. **Thorough ablation covering the design space.** Section 4.3 systematically tests: CoTs vs. no CoTs, maximize vs. minimize image SC, maximize vs. minimize text SC, forward vs. backward KL, and RL vs. direct optimization. Each ablation has a clear takeaway, and the "directly optimize NSC without RL" ablation (Figure 9) is particularly informative — it demonstrates why the GRPO framework is necessary despite the reward being differentiable.

## Weaknesses

### Fatal
None.

### Major

1. **The abstract overclaims — "superior" is not supported by the data.** The abstract states IRIS achieves performance "competitive with or superior to external rewards." However, Table 1 shows IRIS is consistently slightly *below* T2I-R1 on every overall metric across both model sizes:
   - GenEval 1B: 0.72 vs. 0.75; GenEval 7B: 0.77 vs. 0.78
   - T2I-CompBench 1B: 0.3793 vs. 0.3820; 7B: 0.3916 vs. 0.3992
   - WISE 1B: 0.37 vs. 0.38; 7B: 0.48 vs. 0.50
   
   The 7B results show IRIS *consistently and sometimes significantly* below T2I-R1 (e.g., GenEval sub-metrics: Counting 0.52 vs. 0.55, Colors 0.88 vs. 0.91). The claim of being "superior" is unsupported. "Competitive" is accurate; "comparable" (used in Section 4.2) is fair. The 9.1%/13.3%/28.8% "boost" numbers (Section 1, line 44) are relative to the *base* Janus-Pro model, not the external-reward baseline — this is a valid description of improvement over the base model but weaker than the abstract's framing implies. The claims should be recalibrated to match the evidence.

2. **The ablation study's evaluation metrics asymmetrically favor the baseline.** Section 4.3 uses HPSv2, DINO, GIT, and ORM as evaluation metrics for the ablation experiments. These are the exact same four reward models used to *train* T2I-R1. The paper claims they are "simple and unbiased metrics" because IRIS does not train on them — but this is misleading for the *comparison with T2I-R1*: T2I-R1 explicitly optimized these four objectives. When the paper later argues IRIS variants are "competitive" (e.g., which IRIS variant best closes the gap to T2I-R1), the measuring stick is one that T2I-R1 was designed to maximize. The main benchmarks (GenEval, T2I-CompBench, WISE) used in Table 1 do not have this issue, but the ablation studies should include at least one held-out metric that neither method trained on.

### Minor

3. **Theoretical explanation for the direction reversal is primarily descriptive, not mechanistic.** The paper's central claim — that image benefits from low self-certainty while text benefits from high self-certainty — is supported empirically but the offered explanation is essentially "we observe that models with low uncertainty generate simple and uniform images." The paper does not provide a mechanistic account of *why* image token distributions should behave differently from text token distributions within the same multimodal model. Section 3.2's speculation about "information-seeking agents" (Team et al., 2025) is vague. This is not fatal — the empirical finding stands on its own — but the paper positions this observation as a key contribution (contribution bullet 2: "We observe and confirm that the model's self-certainty exhibits task-dependent behaviors") and offers little analysis into the underlying mechanism.

4. **Figure 2's evidence for divergent self-certainty trends compares different models and tasks.** The figure compares text self-certainty from Qwen2.5-1.5B-Instruct (on math reasoning) against image self-certainty from Janus-Pro-1B (on T2I). These differ in model architecture, task, and token type simultaneously, making it difficult to attribute the divergence to modality rather than model or task differences. A within-model comparison (text vs. image tokens from the same Janus-Pro model) would be a cleaner test of the claim.

5. **Only one model family (Janus-Pro) is tested.** The paper claims IRIS is "agnostic to the model architecture" (Section 1, line 44) but evaluates only on Janus-Pro 1B and 7B. While Section 4.4 acknowledges this limitation, the paper's title and claims about "autoregressive T2I models" generally would be substantially strengthened by testing on at least one additional autoregressive architecture (e.g., Show-o, VILA-U).

6. **The qualitative claim about "visually rich and colorful" images is never quantified.** The paper repeatedly states that lower self-certainty produces "visually rich and colorful" images (abstract, introduction, conclusion) but never directly measures image diversity, color variance, or any related perceptual metric. This qualitative description is used to explain the quantitative results, but it remains unvalidated.

7. **Tension between Figure 3 and Table 1.** Figure 3 shows IRIS (1B) surpassing T2I-R1 after ~200 training steps on all three benchmarks, yet Table 1 reports T2I-R1's best checkpoint as higher across all overall metrics (e.g., GenEval: IRIS 0.72 vs. T2I-R1 0.75). The paper should clarify this discrepancy — does T2I-R1 peak earlier and then degrade? The caption of Figure 3 ("IRIS...achieves higher scores than T2I-R1") directly contradicts Table 1 and needs correction.

### Trivial
None.

## Nice-to-Haves

- **Human evaluation**: The paper relies entirely on automated benchmarks. A small-scale human preference study (e.g., 100 prompts) between IRIS and T2I-R1 would substantially strengthen the claim of alignment with human preferences.
- **Direct CoT diversity analysis**: The paper infers that minimizing text SC encourages diverse semantic CoTs from the score improvements. Directly measuring CoT diversity (e.g., n-gram diversity, embedding variance) would strengthen the causal chain.
- **T2I-R1 chat template disclosure**: The paper identifies a chat template bug in the T2I-R1 codebase (line 120). Reporting results both with and without the corrected template would let readers assess the impact on the comparison.

## Removed Points

- **"Evaluation metrics asymmetrically favorable to the baseline — main comparison uses HPSv2/DINO/GIT/ORM"**: The reviewer claimed the main comparison uses the four reward models as evaluation metrics. This is factually incorrect: the main results (Table 1) use GenEval, T2I-CompBench, and WISE — separate benchmarks, not the training rewards. Only the ablation study (Section 4.3) uses the four reward models, for comparing IRIS variants among themselves rather than IRIS vs. T2I-R1. The criticism as stated was wrong and has been corrected into Major weakness #2 above.
- **"Semantic CoT pipeline inherited without independent scrutiny"**: The reviewer's concern about not disentangling CoT content improvement from image generation improvement is partially addressed by the existing ablation (Figures 6-7 separate text and image SC). The paper does not claim to fully disentangle this, and the ablation provides reasonable evidence. This is moved to Nice-to-Haves.
- **"The chat template bug disclosure is incomplete"**: The reviewer's suggestion to report both versions is reasonable but the paper's disclosure is itself a useful contribution. Elevated to Nice-to-Haves.
- **Various formatting complaints and speculation about missing appendix content**: Removed per hard rules.
- **Strength about "addressing an important problem"**: This is generic; dropped. The remaining three strengths are specific and evidence-grounded.

## Novel Insights

None beyond the paper's own contributions. The reviews do not surface a novel interpretation that the paper itself does not already provide.

## Suggestions

1. **Calibrate all claims to match the evidence.** Replace "competitive with or superior to" in the abstract with "competitive with" or "comparable to." Clarify that IRIS is slightly below T2I-R1 on most metrics, especially on 7B, and that its value is in requiring *zero* external supervision — not in outperforming external rewards.

2. **Add a held-out evaluation metric in the ablation study.** Include at least one image quality metric (e.g., CLIP score) that neither T2I-R1 nor IRIS trained on, to demonstrate that IRIS's gains are not artifacts of using metrics that favor T2I-R1's training objectives.

3. **Resolve the Figure 3 vs. Table 1 discrepancy.** Explain whether T2I-R1's best checkpoint occurs early in training and why Figure 3 shows a different trajectory. Correct the caption if it overstates the comparison.

4. **Quantify the "visually rich and colorful" claim.** Add a simple diversity metric (e.g., color histogram variance, LPIPS self-diversity) to substantiate the qualitative description.

## Score and Decision

MY FINAL SCORE: <score>6</score>
MY FINAL DECISION: <decision>Accept</decision>