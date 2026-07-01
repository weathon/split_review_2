## Summary

This paper proposes IRIS, a framework that uses the model's negative self-certainty (NSC) — defined as negative forward KL from a uniform distribution over the vocabulary — as an intrinsic reward signal to fine-tune autoregressive text-to-image models via GRPO, without any human preference data or external reward models. The key motivating observation is that image self-certainty *decreases* during external-reward RL training for T2I models (while text self-certainty increases for LLMs on reasoning tasks), suggesting that lower self-certainty is beneficial for image generation. On Janus-Pro 1B and 7B, IRIS achieves performance competitive with T2I-R1 (which uses four external reward models: HPSv2, DINO, GIT, ORM) across GenEval, T2I-CompBench, and WISE benchmarks.

## Strengths

1. **Novel and empirically grounded observation (Section 1, Fig. 2).** The paper demonstrates that self-certainty dynamics differ across modalities: it increases during RL training for text-domain LLMs (consistent with prior work) but decreases for multimodal LLMs on text-to-image generation. This challenges the default assumption from text reasoning that self-certainty maximization is universally beneficial and provides a principled foundation for the method.

2. **Clean, minimal method (Section 3.2).** IRIS uses only the negative forward KL between the output distribution and a uniform distribution as the reward, combined with GRPO. No external reward model, no human preference data, no domain-specific verifier. This simplicity is a genuine virtue — it means the method can in principle be applied wherever an autoregressive T2I model exists, without engineering reward pipelines.

3. **Thorough and informative ablation study (Section 4.3, Figs. 5–9).** The paper systematically tests five design choices: (a) with vs. without semantic CoTs, (b) minimizing vs. maximizing image self-certainty, (c) minimizing vs. maximizing text self-certainty, (d) forward KL vs. backward KL (entropy), and (e) RL vs. direct optimization. Each ablation isolates a distinct question and the results are consistent. The finding that direct NSC optimization collapses (Fig. 9) while GRPO works is particularly informative and prevents a naive interpretation of the method.

4. **Competitive performance without external supervision (Table 1).** IRIS-1B scores 0.72 vs. T2I-R1's 0.75 on GenEval Overall, 0.3793 vs. 0.3820 on T2I-CompBench Complex, and 0.37 vs. 0.38 on WISE Overall — close margins for a method using zero external supervision. On several sub-metrics (e.g., Colors in GenEval, Natural Science sub-categories in WISE), IRIS matches or slightly exceeds the external-reward baseline. For a method with no external supervision, this is a meaningful result.

## Weaknesses

### Fatal
None.

### Major

1. **Incomplete characterization of the mechanism (Section 4.3, Fig. 9).** The paper's framing centers on "maximizing self-uncertainty," but the ablation in Fig. 9 reveals a critical nuance: *directly* optimizing NSC (differentiable, without GRPO) causes model collapse. Only GRPO — which ranks outputs by their NSC values within a sampled group and uses relative advantage estimation with KL regularization to π_ref — succeeds. The paper's explanation ("GRPO employs a more conservative strategy by first generating a batch of responses and then aligning with the largest NSC") is vague and underspecified. This means the method is not straightforwardly "maximizing self-uncertainty"; it is *selecting outputs that are relatively more uncertain than their peers in a sampled group while staying close to the reference policy via KL regularization*. These are two very different mechanisms. The collapse of the direct-NSC baseline suggests unbounded uncertainty maximization is harmful, and the GRPO mechanism (group-relative selection + KL constraint) is doing critical work that the paper's framing glosses over. This does not invalidate the empirical results, but it substantially weakens the causal story about *why* the method works.

### Minor

2. **Undiscussed asymmetry in the T2I-R1 comparison (Section 4.1).** The paper correctly identifies that the official T2I-R1 implementation uses the wrong chat template (Janus template instead of Janus-Pro template) and corrects it for both methods. However, T2I-R1 was developed and tuned using the Janus template. Switching templates may asymmetrically affect T2I-R1 (whose hyperparameters and prompt formatting were optimized for a different tokenization pattern) while IRIS was always trained with the correct template. The paper does not report whether the original-template T2I-R1 numbers differ from the corrected-template numbers, nor discuss whether the correction could systematically disadvantage T2I-R1.

3. **Slight overclaim in the abstract and conclusion.** The abstract claims performance "competitive with or superior to external rewards" and the conclusion claims "even better results in the initial learning." "Competitive" is well-supported (Table 1 scores are close). However, "superior" is only supported on a few specific sub-metrics (Colors in GenEval, some Natural Science sub-categories in WISE) while T2I-R1 leads on the three overall metrics for both model sizes. The "initial learning" advantage visible in Fig. 3 is genuine, but the paper's main results (Table 1) report the best checkpoint from steps 100–800, not an initial-phase advantage. The abstract and conclusion should be calibrated to the table results.

4. **Statistical significance not discussed (Table 1).** Standard deviations are reported but the paper does not discuss which IRIS vs. T2I-R1 differences are statistically significant. On several metrics (e.g., Counting in GenEval: IRIS-7B has std 0.06 on mean 0.52, CV ≈ 12%), error bars overlap substantially, making it unclear whether apparent gaps are meaningful or within measurement noise.

5. **Forward KL's sequence-length bias explanation is imported without T2I verification (Section 3.2).** The paper notes that forward KL "mitigates the common bias against longer sequences found in perplexity and entropy-based measures," citing text-domain papers (Fang et al., 2024; Kang et al., 2025). While the ablation empirically shows forward KL > backward KL, the specific explanation about sequence-length bias is not verified in the image generation domain.

6. **Tension between criticizing external rewards and using them for evaluation (Section 4.3).** The paper argues that external rewards are limited, domain-specific, and unreliable (Section 2), yet uses the same four external reward models (HPSv2, DINO, GIT, ORM) as evaluation metrics in the ablation studies. The paper states these are "unbiased" because they are not used in IRIS training, which is reasonable in a narrow sense, but the tension should be explicitly acknowledged.

7. **Single architecture class tested (Section 4.4).** Only Janus-Pro (an autoregressive model) is tested. The paper claims IRIS is "agnostic to the model architecture" (contributions section), but this remains unverified for diffusion, masked-modeling, and other T2I architectures. The paper acknowledges this in Section 4.4, but the forward claim should be qualified.

8. **No quantitative measure of visual diversity/richness.** The paper claims that lower self-certainty produces "visually rich and colorful" images but relies on qualitative inspection of a few examples (Fig. 1, Fig. 4). A diversity metric (e.g., LPIPS-based pairwise diversity, color histogram entropy, or CLIP score variance across generations) would ground the central intuition quantitatively.

### Trivial
- The effective batch size of 8 (8 prompts per gradient step) is small for RL training, though it follows the T2I-R1 protocol. Variance implications are not discussed.

## Nice-to-Haves
- **Report NSC values over the IRIS training trajectory** (analogous to Fig. 2) to directly connect the motivating observation to the method's actual behavior. Does IRIS actually decrease self-certainty relative to the base model? By how much? Does it converge to a stable level?
- **Controlled experiment isolating GRPO components** (e.g., fixing advantage to raw NSC without group normalization, or removing the KL penalty) to characterize which component prevents collapse.
- **A small-scale human preference study** would strengthen the claim that the intrinsic reward aligns with human judgment, though automated benchmarks are the standard evaluation protocol for this task.

## Removed Points
These points from the input review were removed with justification:
- **"Abstract sentence about low uncertainty"**: The reviewer claimed the sentence "autoregressive T2I models with low uncertainty tend to generate simple and uniform images" has the relationship backwards. This is incorrect: SC = KL(U‖π_θ), so "low uncertainty" = high SC = peaked distribution. The paper correctly states that this leads to simple images. The reviewer's criticism is a misreading.
- **"Demand for human evaluation treated as a missing requirement"**: The paper is evaluated on three standard automated benchmarks (GenEval, T2I-CompBench, WISE) that are the established evaluation protocol for T2I alignment. Adding human evaluation is welcome but not a core gap.
- **"Should discuss whether method recapitulates a natural learning dynamic"**: This is an interesting analysis question but not a weakness of the presented empirical results.
- **Miscellaneous speculative concerns** about whether the template correction might affect T2I-R1 (already retained as Minor #2) were separated from speculation about specific quantitative impacts not in the paper.

## Novel Insights
None beyond the paper's own contributions.

## Suggestions
1. Report NSC values over the IRIS training trajectory to directly connect Fig. 2's observation to the method's behavior.
2. Calibrate abstract/conclusion wording: replace "superior to" with "competitive with" unless referring to specific sub-metrics, and ground the "initial learning" claim in a quantitative statement (e.g., "IRIS achieves higher scores in the first 200 steps, though gaps narrow by 800 steps").
3. Add a discussion of statistical significance for the main comparisons in Table 1.
4. Run a small control experiment with the original Janus chat template to verify whether the correction asymmetrically affects T2I-R1 vs. IRIS.
5. Add a quantitative diversity metric (e.g., LPIPS-based pairwise diversity or image color histogram entropy) to substantiate the visual richness claim.

MY FINAL SCORE: <score>7</score>
MY FINAL DECISION: <decision>Accept</decision>