## Summary

This paper introduces Visuo-Tactile World Models (VT-WM), the first multi-task world model that integrates fingertip tactile sensing from Digit 360 sensors with exocentric vision for robot manipulation. The model uses pretrained Cosmos and Sparsh-X encoders to fuse visual and tactile latents, which are processed by a transformer predictor conditioned on actions. The authors demonstrate that tactile grounding improves imagination quality (33% gain in object permanence, 29% gain in causal compliance under Fréchet distance), translates to up to 35% higher zero-shot real-robot success rates on contact-rich tasks, and yields over 3.5× data efficiency compared to behavioral cloning when adapting to a new task with limited demonstrations.

## Strengths

- **Clear and timely problem**: The paper addresses a genuine limitation of vision-only world models—hallucinations in contact-rich manipulation due to occlusion and visual aliasing. The motivation to ground imagination via tactile sensing is well-articulated and directly relevant to real-world robot learning.

- **Principled evaluation framework**: The authors go beyond cumulative task success by separately assessing object permanence and causal compliance using normalized Fréchet distance combined with CoTracker point trajectories. This provides quantitative, interpretable evidence for why VT-WM outperforms V-WM, rather than relying solely on final planning metrics.

- **Consistent experimental evidence across multiple axes**: The paper evaluates three distinct claims (imagination quality, zero-shot planning, data efficiency), each with its own experimental setup, and the results broadly align with the hypotheses. The zero-shot transfer to a real robot across five tasks of increasing contact-difficulty is particularly convincing.

- **Data efficiency demonstration**: The comparison against behavioral cloning (ACT) on a plate-insertion task with only 20 demonstrations is practically meaningful. The 77% vs 22% success rate shows that multi-task world models can leverage prior contact knowledge far more effectively than task-specific policies in low-data regimes.

## Weaknesses

### Major

1. **Limited statistical power in planning experiments**: The zero-shot planning results (Figure 8) are based on only 5 trials per task per model. For a real-robot study, this sample size is too small to draw strong conclusions, especially when the absolute difference between models is small (e.g., Stack Cubes: 75% vs 83%). No confidence intervals or trial-level variability is reported, making it difficult to assess whether the observed gains are robust.

2. **Unaddressed negative result**: On the *scribble with marker* task, VT-WM shows *worse* causal compliance than V-WM (Figure 6). The authors note the t-test is not significant, but the degradation (≈0.35 to ≈0.50 normalized Fréchet distance) is non-trivial and unexplained. This task involves marker contact that produces visual marks—tactile information may not help here, or may even introduce spurious dependencies. The paper does not analyze this failure case, which weakens the claim that tactile grounding broadly improves physical fidelity.

3. **Lack of ablation studies on key design choices**: The architecture uses frozen pretrained Cosmos and Sparsh-X encoders, a specific transformer with factorized attention, and a particular fusion strategy (concatenation along spatial dimension). There is no ablation to justify these choices. For example: (a) What if tactile tokens are omitted during inference? (b) What if the tactile encoder is fine-tuned? (c) What about alternative fusion methods (e.g., cross-attention, late fusion)? Without such analysis, it is unclear which components drive the improvements and how generalizable the architecture is.

4. **Synchronization and alignment of modalities**: The vision input is 9 frames at 6 fps (1.5 seconds), while tactile input is 2 frames per sensor covering 0.16 seconds. The paper does not explain how these asynchronous streams are temporally aligned, how the shorter tactile horizon is matched to the visual context, or whether misalignment could cause artifacts. This is a practical concern for real-time planning and reproducibility.

### Minor

- **CEM planning details**: The action space is ℝ⁷ (translation, rotation, binary grasp). The paper does not specify the CEM horizon H, population size N, number of iterations, or how the action sequence is executed open-loop. These details are important for reproducibility and for understanding whether the planning method is a bottleneck.

- **Data efficiency comparison could be broadened**: The comparison against only one BC method (ACT) on one new task is suggestive but not definitive. A comparison against a vision-only WM fine-tuned on the same 20 demonstrations, or against a diffusion policy, would strengthen the data efficiency claim.

### Trivial

- The figure numbering in the main text (e.g., repeated references to "fig. 1", "fig. 2") is slightly inconsistent with the inserted figures—this appears to be a formatting artifact from extraction, not a paper flaw.

## Nice-to-Haves

- Provide confidence intervals or standard deviations for all real-robot success rates, and ideally increase the number of trials per condition to at least 10.

- Include an ablation where the tactile modality is removed at test time from a trained VT-WM to isolate the benefit of tactile *during inference* vs. *during training*.

- Analyze the scribble-with-marker failure case: is the marker tip too small for the tactile sensor to resolve, or does the tactile signal incorrectly suggest contact when the marker is lifted?

- Clarify whether the pretrained Cosmos and Sparsh-X encoders are frozen or fine-tuned during world model training, and report any changes in their loss/performance.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

- **Increase the number of real-robot trials and report variance.** With only 5 trials per model per task, the planning results are not statistically compelling. A pilot power analysis or at least 10 trials per condition (with bootstrap confidence intervals) would substantially strengthen the paper.

- **Add an ablation experiment comparing VT-WM with a variant that receives null/padding tactile inputs during training** to determine whether the performance gain comes from the tactile sensory information itself or from the increased model capacity/regularization of training with an additional modality.

- **Explain the scribble-with-marker result** (e.g., does the marker's visual output dominate the tactile signal? Is the contact too gentle to be captured by Digit 360?). This will improve the scientific honesty of the paper and help practitioners understand where tactile world models may not help.

- **Make the planning hyperparameters and open-loop execution protocol explicit** in the main text or appendix for reproducibility.

## Score and Decision

MY FINAL SCORE: <score>6</score>
MY FINAL DECISION: <decision>Accept</decision>