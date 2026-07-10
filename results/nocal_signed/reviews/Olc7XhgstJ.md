Now I have the impact signals. Let me compose the final consolidated review.

## Summary

This paper introduces **Steady Thought (ST)**, a three-stage framework (entropy-based thought segmentation, suppression-guided thought completion, and thought-level preference optimization) designed to mitigate "under-thinking" — the tendency of Large Reasoning Models (LRMs) to abandon promising reasoning trajectories prematurely. The core idea is to train the model to recognize and commit to promising thoughts via thought-level preference optimization (STPO), rather than globally suppressing switching behavior. Experiments across three model scales (1.5B–14B) and four benchmarks (MATH-500, AIME 2024, GSM8K, LiveCode) show consistent accuracy gains (up to 5.3%) with simultaneous token reductions (19.0%–39.3%), including on the out-of-distribution LiveCode dataset.

## Strengths

- **Clear problem visualization and motivation.** Figures 1a and 1b provide direct empirical evidence that correct thoughts often appear early in the reasoning trajectory but are followed by numerous wasteful switches. This grounds the paper's thesis in data rather than speculation.

- **Consistent accuracy gains with simultaneous token reduction across all three model scales.** In Table 1, ST improves or maintains accuracy on 11 out of 12 model-dataset combinations while reducing token count on all 12. This is an unusual result — most efficiency methods trade accuracy for speed.

- **OOD generalization on LiveCode is notable.** The training data (omni-math) is purely mathematical, but ST improves accuracy on competitive programming (LiveCode) for all three models. This argues against the concern that ST simply memorizes shorter responses — it appears to learn a generalizable reasoning pattern.

- **The entropy-based thought segmentation is a principled design choice.** Using entropy spikes as signals for thought boundaries is well-motivated, and the ablation on thresholds (Table 3) provides useful insight into the trade-off between segmentation granularity and data quality.

## Weaknesses

### Fatal
None.

### Major

- **Missing SimPO-on-full-sequences baseline in the ablation (Table 4).** The ablation compares STPO against SFT and DPO on full sequences, but does not include a standard SimPO baseline (i.e., applying the length-normalized SimPO objective to full sequences without thought-level conditioning). Since the paper explicitly adopts SimPO's length-normalized formulation to address the length mismatch between chosen and rejected responses, the observed improvements over DPO could be attributed to switching from DPO's length bias to SimPO's length-normalized rewards rather than to the thought-level conditioning that the paper claims as its key innovation. Without this ablation, the paper's central claim — that thought-level optimization is what drives the improvement — is under-supported. This is the most consequential gap in the paper's evidence chain.

### Minor

- **No variance estimates on AIME 2024 (30 problems).** The paper reports averaging eight test runs for AIME but provides no variance, confidence intervals, or per-run results. For the 1.5B model, accuracy moves from 27.5% to 31.2% — roughly one additional correct problem out of 30. A single-problem swing represents 3.3% accuracy, so the reported improvements of 3.7%–5.0% are all within ±1–2 problems. Without variance estimates, it is impossible to distinguish signal from noise on this dataset.

- **Training hyperparameters are absent from the main text.** No learning rate, batch size, optimizer, number of epochs, β/γ values for STPO, amount of training data sampled from omni-math, or filtering criteria for training examples are provided. For a paper proposing a new training objective, these omissions hinder reproducibility.

- **The PCT metric for measuring "correct intermediate thoughts" (Table 2) uses the same suppression-based completion procedure that generates the training data.** The paper determines whether an intermediate thought is "correct" by completing it with suppression (Stage 2 method) and checking if the final answer is correct. This could systematically overestimate correctness: suppression forces the model to continue without switching, potentially arriving at the right answer through a path that would not have been taken naturally. Since reduced PCT is the paper's key evidence for improved switching decisions, the measurement methodology needs validation against an independent ground truth.

- **Narrative tension around suppression.** Section 1 criticizes prior suppression-based methods for "appl[ying] suppression globally, potentially limiting the model's flexibility," yet Stage 2 (Thought Completion) uses the same technique of suppressing trigger words. While Stage 2 is a data-generation step and not used at inference, the paper does not explicitly make this distinction. It also does not address the failure mode where suppression during data generation could block a valuable switch, potentially creating corrupted training labels.

### Trivial

- The claim that "the number of correct intermediate thoughts is equal to the number of Invalid Switches" (line 223) is definitionally true but conflates switching from a correct thought with wasteful switching in all cases. A model could switch from a correct thought, explore an alternative, correctly reject it, and return productively — this is not necessarily an "invalid" switch.

- The trigger words used for suppression are listed as "e.g., 'wait' and 'alternatively'" but the full set and the suppression coefficient (how much logits are decreased) are not specified.

## Nice-to-Haves

- Interrupt the ST-trained model at an intermediate thought and independently evaluate (e.g., via human annotation or an external verifier) whether switching or persisting was the better decision, to provide direct evidence that the model makes better switching decisions rather than simply producing shorter outputs.
- Discuss potential failure cases where ST could cause the model to over-commit to an incorrect thought, since training data only includes "correct" completions of promising thoughts.
- Clarify how preference pairs are constructed when multiple thoughts in a single response qualify as "promising."

## Removed Points

These points were flagged in the input review but are removed for the following reasons:

- **Baselines may not be well-tuned (NOWAIT on Qwen3-8B):** speculative; the paper does not claim baselines are optimally tuned for every model.
- **Steadiness Score formalization not instantiated:** the paper explicitly states it can be instantiated via log-probabilities (line 65) and connects it to DPO/SimPO.
- **Missing discussion of failure cases / distribution mismatch between training and inference:** plausible concerns but speculative with no evidence of actual harm; better suited as limitations or nice-to-haves.
- **Table 1 using ↓ for accuracy:** a parser-induced formatting artifact, not an author error.
- **Missing related works:** cannot be verified without external sources.
- **Various formatting/style nitpicks and missing appendix content:** stripped by the parser; the original submission contains these.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. **Most important:** Add a standard SimPO-on-full-sequences baseline to Table 4 to disentangle the effect of thought-level conditioning from the switch to length-normalized rewards.
2. Report standard deviations or confidence intervals for AIME 2024 results.
3. Add a table of training hyperparameters (learning rate, batch size, optimizer, number of epochs, β, γ, training data size, filtering criteria).
4. Explicitly state that suppression is used only during data generation (Stage 2) and not during inference, and discuss the potential failure mode where suppression could block a valuable switch.
5. Validate the PCT metric with an independent ground-truth assessment (e.g., human annotation or external verifier).

## Score and Decision

The paper addresses a real and well-motivated problem with a clean, principled framework. The empirical results are unusually strong — consistent accuracy improvements with simultaneous token reduction across three model sizes and four benchmarks, including convincing OOD generalization. The key weakness is the missing SimPO-on-full-sequences ablation, which is necessary to substantiate the paper's central claim that thought-level conditioning (rather than the switch to a length-normalized objective) drives the improvement. This gap is fixable and does not invalidate the overall contribution, but it presently weakens the attribution of what makes the method work.

MY FINAL SCORE: <score>6.5</score>
MY FINAL DECISION: <decision>Accept</decision>