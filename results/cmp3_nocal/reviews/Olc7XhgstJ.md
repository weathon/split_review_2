Now let me produce the final review.

## Summary

This paper proposes Steady Thought (ST), a three-stage framework (thought segmentation → thought completion → thought-level preference optimization) to address "under-thinking" in Large Reasoning Models—the tendency to abandon promising reasoning paths through excessive thought switching. ST segments model responses into thoughts, force-completes each thought to assess its promise, then trains a preference optimization objective (STPO) that conditions on (question, promising thought) prefixes to prefer committed continuation over switching. Experiments across three model scales (1.5B–14B) and four datasets show consistent accuracy gains of 1.9–5.3% with token reductions of 17.3–24.9%.

## Strengths

1. **Well-motivated problem with a sound core idea.** The observation that LRMs generate correct thoughts early but then switch away (Figures 1a, 1b) is concrete and measurable. The insight that prior methods (NOWAIT, SEAL) suppress switching globally—blocking all switches—is a genuine limitation, and the idea of selectively training the model to commit to promising thoughts while preserving switching ability is a natural and sensible response.

2. **Consistent results across multiple model scales and architectures.** ST improves accuracy and reduces token count on all three models (DeepSeek-R1-Distill-Qwen-1.5B, Qwen3-8B, DeepSeek-R1-Distill-Qwen-14B) across all four datasets (Table 1). This breadth is real evidence that the method is not an artifact of a single architecture.

3. **Out-of-distribution generalization to LiveCode.** The LiveCode dataset (code, trained only on math) serves as an OOD test. ST improves accuracy there (e.g., +5.3% on Qwen3-8B, +4.2% on the 14B model), suggesting the method teaches a generalizable reasoning pattern rather than dataset-specific memorization.

4. **Ablation isolating the effect of preference optimization (Table 4).** The comparison SFT vs DPO vs STPO shows that STPO contributes beyond simple fine-tuning on the chosen responses. SFT on the same chosen data actually hurts accuracy (80.4% vs 82.2% base on MATH-500), ruling out the concern that improvements come merely from learning shorter outputs.

## Weaknesses

### Major

1. **Train–inference mismatch in the preference optimization objective.** The STPO loss (Equation 7) conditions the policy on a *specific intermediate thought* T_i that is known (by construction) to be promising:
   
   $$\mathcal{L}_{\text{STPO}} = -\mathbb{E}_{(Q, T_i, \mathbf{y}_w, \mathbf{y}_l) \sim \mathcal{D}} \left[ \log \sigma \left( \frac{\beta}{|\mathbf{y}_w|} \log \pi_\theta(\mathbf{y}_w | Q, T_i) - \frac{\beta}{|\mathbf{y}_l|} \log \pi_\theta(\mathbf{y}_l | Q, T_i) - \gamma \right) \right]$$
   
   During training, the model is given a promising thought T_i as a prefix and learns to prefer continuing it over switching away. At inference, the model generates from scratch given only Q—it must simultaneously (a) discover which of its own generated thoughts are promising, and (b) decide to commit to them. The STPO loss never trains the model on the first of these tasks. The paper claims (line 123) that ST teaches the model "to recognize and commit to a promising intermediate thought," but the training signal is entirely about what to do *given* a promising thought, not about how to *identify* one. The paper provides no analysis of whether this transfer actually occurs, e.g., by measuring how often the ST model's *first* correct thought is also its *final* thought compared to the base model. This gap weakens the paper's central mechanistic claim.

2. **The "correct thought" metric (PCT) has circularity concerns.** Table 2 reports the proportion of correct intermediate thoughts (PCT) before and after ST as evidence that ST reduces invalid switching. However, a "correct thought" is defined by the same force-completion procedure (Section 3.2) used to construct the training data, and the evaluation is performed using the **ST-trained model itself** to do the force-completion. The ST model has been explicitly optimized to be better at completing thoughts without switching. Consequently, a lower PCT after ST could simply reflect that the model has become better at completing the *first* promising thought it encounters (which then becomes the "final thought" and is excluded from PCT calculation), rather than reflecting genuinely fewer invalid switches. The paper does not control for the base rate of the number of thoughts generated, leaving the PCT metric confounded between "fewer thoughts" and "more purposeful switching."

3. **Undiscussed negative results in Table 1.** Two notable cases are not addressed:
   - **SEAL outperforms ST on Qwen3-8B LiveCode** (83.4% vs 77.1%). If the paper claims ST is superior to prior methods, it should explain this case.
   - **NOWAIT collapses on Qwen3-8B** (overall accuracy drops from 80.23% to 59.03%, tokens increase by 84.6%). This is dramatic and unusual; since ST's own Thought Completion stage uses a similar logit-suppression mechanism, understanding whether this collapse reflects a tuning issue or a fundamental risk of aggressive suppression is important context for evaluating ST.

### Minor

4. **Missing training hyperparameters.** The paper omits nearly all training details: learning rate, values of β and γ in the STPO loss, batch size, number of epochs, and optimizer. The training dataset size is described only as "thousands of problems." This is insufficient for reproducibility.

5. **No variance or statistical significance reported.** The paper reports "the average of eight test runs for AIME 2024 and two runs for LiveCode" but provides no standard deviations or confidence intervals. AIME 2024 has only 30 problems, so variance across runs could be substantial. Without variance measures, the reader cannot assess whether a 1.9–5.3% accuracy gain is meaningful or within the noise floor.

6. **The "Overall" column averages across datasets of very different sizes.** The simple mean of accuracy across MATH-500 (500 problems), GSM8K (1319), AIME (30), and LiveCode (400) gives equal weight to each, making the overall metric sensitive to fluctuations on the smallest dataset (AIME). Dataset-wise results are available in the table, but the "Overall" column is misleading.

7. **Thought count increases on AIME for the 1.5B model.** For DeepSeek-R1-Distill-Qwen-1.5B on AIME 2024, the average number of thoughts increases from 12.87 to 18.21 (Figure 2a). The paper explains this as the small model needing "to increase the frequency of thought transitions to find the optimal solution" on hard problems, which is reasonable. However, this undercuts the "steady" narrative on the hardest dataset—the method's effect is not uniformly about reducing switching, and the paper's treatment of this as a straightforward positive deserves more nuance.

### Trivial

None.

## Nice-to-Haves

- A direct behavioral analysis: measuring the "first-correct-thought commitment rate" (how often the model's first correct thought is also its final thought) for ST vs. base model would directly test the claimed mechanism.
- A controlled evaluation of whether ST preserves beneficial switching (e.g., on problems where the first approach leads to a dead end).
- A comparison against a variant of ST that uses a different thought-completion method (e.g., higher temperature decoding) to isolate the effect of the NOWAIT-like suppression in Stage 2.
- Explicit statement of whether the same entropy threshold (3.0) was used across all model scales or separately tuned.

## Removed Points

The following points from the input review were removed:
- *"The improvements could come from length regularization."* — The ablation in Table 4 (SFT on the short chosen responses performs poorly) partially addresses this; not the primary explanation.
- *"Speculative concerns about threshold transfer across models"* — The paper references Appendix D for threshold tuning on other models; appendix content is stripped by the parser and should not be penalized.
- *"NoThink is an odd baseline"* — Not a weakness; baselines are included for completeness.
- *"The quality ceiling is tied to NOWAIT"* — This is inherent to the method design, not a weakness.
- *"The paper never addresses how the model discovers T_i"* — Merged into Major Issue 1.
- *"Formatting and style nitpicks"* — These are parser artifacts, not author errors.
- *"Missing appendix content"* — Per guidelines, the parser strips these; they exist in the original submission.

## Novel Insights

The most interesting insight that emerges from the reviews is the fundamental tension between the training setup (where promising thoughts are given as known prefixes) and the inference-time behavior (where the model must self-discover promising thoughts). This gap is not unique to this paper—it applies broadly to any method that trains on oracle-conditioned data and then deploys autoregressively. The paper's PCT metric tries to bridge this gap but is itself confounded by the reuse of the force-completion procedure. A clean resolution would require comparing thought-level commitment behavior on a per-trajectory basis, which the paper has the machinery to do but does not pursue.

## Suggestions

1. Add a behavioral analysis showing the "first-correct-thought commitment rate" (as a fraction of cases where the first correct thought is also the final thought) for both base and ST models.
2. Report standard deviations for the 8-run AIME and 2-run LiveCode evaluations.
3. Add a discussion of the SEAL > ST result on Qwen3-8B LiveCode and the NOWAIT collapse on Qwen3-8B.
4. Report all training hyperparameters (learning rate, β, γ, batch size, epochs, optimizer).
5. Disclose the entropy threshold selection procedure across all model scales.
6. Either remove the "Overall" column or replace it with a size-weighted average.

## Score and Decision

The paper addresses a well-motivated problem with a cleanly designed method. The empirical results—consistent accuracy gains with substantial token reductions across multiple model scales and out-of-distribution data—are real and useful. However, the paper's evaluation has three significant gaps: (1) the training objective conditions on oracle-known promising thoughts while inference requires self-discovery of those thoughts, and no analysis confirms this transfer; (2) the key metric for invalid switching (PCT) is confounded with the training procedure; (3) notable negative comparisons (SEAL beating ST on one dataset, NOWAIT collapse) are left unaddressed. These gaps prevent the paper from fully supporting its mechanistic claims, though the empirical performance is still positive and the method represents a meaningful contribution.

MY FINAL SCORE: 6
MY FINAL DECISION: Accept