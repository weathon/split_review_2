Now let me produce the final review.

## Summary

This paper proposes Steady Thought (ST), a framework to mitigate "under-thinking" in Large Reasoning Models (LRMs)—the tendency to abandon promising reasoning trajectories prematurely. ST operates in three stages: (1) entropy-based segmentation of model responses into thought units, (2) forced completion of each thought via logit-suppression of switching trigger words (e.g., "wait," "alternatively"), and (3) thought-level preference optimization (STPO) that trains the model to prefer completions that commit to a promising thought over the original trajectory that switched away. Experiments across three model families show accuracy improvements (up to 5.3%) alongside token reductions (up to 39.3%), including on OOD programming benchmarks.

## Strengths

- **Well-motivated problem distinction.** The paper draws a clear and useful distinction between *under-thinking* (switching away from promising trajectories) and *over-thinking* (general verbosity). The evidence in Figures 1a/1b that correct thoughts often appear early yet are abandoned is visually compelling and grounds the problem in observed model behavior.

- **Clean methodological contribution.** The STPO loss (Equation 7) is a principled adaptation of SimPO to the thought level. Conditioning on (Q, T_i) and comparing the commit trajectory against the original switching trajectory isolates the learning signal at the point of divergence. This is more fine-grained than holistic DPO/SimPO, and the paper's argument that rejecting an entire incorrect response discards correct partial reasoning (Section 3.3) is correct.

- **OOD generalization on LiveCode is informative.** ST trained exclusively on math problems improves accuracy on a competitive programming benchmark (Qwen3-8B: 71.8%→77.1%; 14B: 70.1%→74.3%). This suggests the method teaches a transferable pattern of thought commitment rather than dataset-specific memorization.

- **Ablation cleanly isolates STPO's contribution.** Table 4 (SFT vs. DPO vs. STPO) shows that STPO's length-normalized thought-level preference signal drives the gains, ruling out simpler explanations such as the training data or fine-tuning process alone.

## Weaknesses

### Fatal
None. The core methodological contribution is sound and the empirical results against Vanilla and SEAL are broadly credible.

### Major

- **Anomalous NOWAIT baseline on Qwen3-8B undermines part of the comparison.** The NOWAIT results for Qwen3-8B are not interpretable as a reasonable instantiation of the method: accuracy drops from 91.4% to 61.0% on MATH-500 (a 30-point collapse) and from 62.1% to 26.3% on AIME 2024, while tokens on GSM8K explode from 1,759 to 12,369 (a 7× increase). Since NOWAIT's mechanism is to suppress a class of reflection-trigger keywords during decoding (line 140), this behavior is anomalous and strongly suggests a configuration or implementation issue. Because NOWAIT and NoThink account for two of the three comparative baselines, the paper's claims of superiority over existing test-time methods are partially compromised. The comparison against Vanilla and SEAL remains valid, but the NOWAIT results need verification or removal.

- **The claimed mechanism—teaching models to "recognize" promising thoughts—is not supported by the training setup.** The STPO loss (Equation 7) conditions on (Q, T_i), where T_i is an *externally identified* promising thought. The model is trained to prefer completions from this given prefix, but is never trained to *identify* which intermediate thoughts are promising during its own unconstrained generation. The paper asserts (line 123) that ST teaches the model "to recognize and commit to a promising intermediate thought," but the training only addresses commitment, not recognition. The empirical gains could arise from a simpler mechanism (e.g., biasing the output distribution toward shorter, more focused responses) rather than improved thought-level decision-making. The paper provides no probing experiments (e.g., artificial thought insertion, analysis of switching patterns) to distinguish these explanations.

- **The paper's own data contains a counterexample to a central claim.** Line 219 states that "the final thought consistently accounted for a larger proportion of the total response." However, for DeepSeek-R1-Distill-Qwen-1.5B on AIME 2024, the proportion of the last thought *decreases* from 18.96% to 15.66% (Figure 2 data table), and the average number of thoughts *increases* from 12.87 to 18.21. The paper acknowledges the thought-count increase (line 219: "smaller models... tend to increase the frequency of thought transitions to find the optimal solution") but this explanation is post-hoc and the last-thought proportion decrease is simply not addressed. The characterization of the results as "consistent" is inaccurate.

### Minor

- **No training-based baselines are included.** ST is a training-based method but is compared exclusively against test-time interventions (NoThink, NOWAIT, SEAL) and the untrained Vanilla model. The related work (lines 274–276) cites training-based approaches (L1, RL-based concise reasoning, dynamic switching) that are omitted from experiments. This makes it difficult to assess whether ST's accuracy-efficiency trade-off is competitive with simpler training alternatives.

- **No variance or confidence intervals reported.** The paper states it averaged 8 runs on AIME 2024 and 2 runs on LiveCode (line 143) but reports no variance. Some differences are small (e.g., 14B on MATH-500: Vanilla 93.6% vs. ST 94.2%), making it impossible to assess significance.

- **Training hyperparameters are absent.** Learning rate, batch size, number of epochs, optimizer, number of training problems sampled from omni-math, and decoding parameters (temperature, top-p) are not reported. This hinders reproducibility.

- **Thought segmentation details are under-specified.** The segmentation criterion (line 91: "any of the initial tokens at the beginning of a candidate step") does not specify how many initial tokens are checked. This granularity determines the segmentation quality but is not stated.

### Trivial
None that survive filtering.

## Nice-to-Haves

- Include at least one training-based baseline (e.g., SFT on short CoT data, or a simple RL approach with a length penalty) to calibrate whether ST's three-stage complexity is justified over simpler alternatives.
- Provide probing experiments that test whether the model actually makes better thought-level decisions (e.g., insert artificial correct/incorrect thoughts at inference time and measure switching behavior).
- Report standard deviations for all main results, especially given the small size of AIME 2024 (30 problems).
- The "Overall" column in Table 1 is an unweighted average across datasets of very different sizes (GSM8K: 1,319; AIME 2024: 30). A principled aggregate or per-dataset reporting would be more informative.
- Discuss the potential bias that thoughts near the end of the reasoning chain are easier to complete correctly, which could skew preference data toward later thoughts.

## Removed Points

These points were raised in the input review but are removed here for the following reasons:

- **"NOWAIT suppresses a single trigger word"** — The paper states NOWAIT suppresses *certain keywords* (line 140), not just one word. However, the core observation of anomalous behavior (30-point accuracy collapse, 7× token explosion) is verifiable from Table 1 and is retained in Major weaknesses.
- **"Threshold tuning only on 1.5B model"** — The paper states (line 243) that threshold tuning results on more models are in Appendix D. Since the parser strips appendices, this criticism cannot be verified from the available content and is excluded per policy.
- **"Acc[%]↓ formatting error in Table 1"** — This is a minor table presentation issue; per policy, formatting artifacts are not considered author errors.
- **"Thought completion circularity"** — The concern that chosen completions are generated with suppression and then used as training targets is a reasonable observation but does not constitute a methodological flaw; this is a standard pattern in synthetic-data pipelines for preference optimization.
- **"Missing threshold tuning across models"** — Duplicate of the above; Appendix reference exists.

## Novel Insights

The input reviews do not surface a genuinely novel synthetic insight beyond what the paper itself contributes. The observation that the NOWAIT Qwen3-8B results are anomalous is a factual check of the reported data, not a new analytical finding. The mechanism gap (training conditions on externally identified T_i but claims the model learns to *recognize* promising thoughts) is articulated more sharply by the harsh critic than by the paper itself.

## Suggestions

1. **Re-run or remove the anomalous NOWAIT baseline** on Qwen3-8B. If the numbers cannot be reproduced with a reasonable configuration, either exclude Qwen3-8B NOWAIT from the comparison or report the known-good configurations only.
2. **Add at least one training-based baseline** (e.g., SFT on chosen completions, or a DPO baseline at the response level) to contextualize ST's complexity.
3. **Acknowledge and analyze the DeepSeek-1.5B/AIME 2024 counterexample** rather than claiming consistency. Analyze whether increased switching on hard problems is beneficial exploration or a failure mode.
4. **Provide evidence for the claimed mechanism** (e.g., probe whether the model's switching behavior at inference time depends on the quality of the current thought, or run a controlled experiment with artificial thought insertion).
5. **Report training hyperparameters and variance** for reproducibility and significance assessment.

## Score and Decision

MY FINAL SCORE: <score>6</score>
MY FINAL DECISION: <decision>Borderline Accept</decision>