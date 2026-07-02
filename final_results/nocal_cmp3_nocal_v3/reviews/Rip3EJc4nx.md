## Summary

This paper proposes HFPrune, a structured pruning method for LLMs that replaces the standard cross-entropy loss with the Shannon entropy of the model's output distribution as the criterion for Taylor-based importance scoring. The key idea is that entropy (Equation 3) considers all token probabilities rather than just the ground-truth token, providing a label-free, holistic importance measure. Experiments on LLaMA-2-7B, LLaMA-3.2, and Qwen models show consistent improvements over existing structural pruning baselines, and the method is ~3× faster and uses ~31% less memory than the self-distillation baseline.

## Strengths

1. **Clean, well-motivated idea grounded in a concrete limitation of prior work.** Section 1 and Figure 1 precisely identify the problem: standard Taylor pruning uses cross-entropy, which only measures importance relative to the single ground-truth token. Replacing it with output entropy is conceptually simple, requires no teacher model, and is clearly specified in Equations 3-4 and Algorithm 1.

2. **Consistent empirical advantage on LLaMA models.** On LLaMA-2-7B (Table 1), HFPrune outperforms SDMPrune by 0.8% at 20% pruning and 0.7% at 30%. On LLaMA-3.2-1.2B (Table 2), the gap widens to 1.8% at 20% and 2.2% at 30%. The trend is consistent across model families and pruning ratios.

3. **Clean ablation isolating the criterion's effect.** Table 6 compares CE, SD, and IE criteria *without any fine-tuning*, directly validating the pruning criterion itself. This is the right experimental design to separate the criterion's contribution from post-pruning recovery. The IE criterion outperforms CE (53.1 vs. 52.6 at 20%; 47.3 vs. 46.8 at 30%).

4. **Practical efficiency advantage.** Table 5 shows HFPrune is ~3× faster and uses ~31% less peak memory than SDMPruner during the pruning process — a meaningful practical benefit that follows directly from the method's simplicity (no teacher model).

## Weaknesses

### Fatal
None.

### Major

1. **Data duplication in Table 3 (Qwen results).** Four pairs of rows in Table 3 are numerically identical despite reporting results for different models and pruning ratios:

   - Qwen2.5-7B 40% SDMPrune (line 241) = Qwen2.5-1.5B 20% SDMPrune (line 244) — all 11 values match exactly.
   - Qwen2.5-7B 40% HFPrune (line 242) = Qwen2.5-1.5B 20% HFPrune (line 245) — all 11 values match exactly.
   - Qwen2.5-1.5B 40% SDMPrune (line 248) = Qwen3-1.7B 20% SDMPrune (line 251) — all 11 values match exactly.
   - Qwen2.5-1.5B 40% HFPrune (line 249) = Qwen3-1.7B 20% HFPrune (line 252) — all 11 values match exactly.

   The probability of two different models at different pruning ratios producing identical results across all 10 benchmarks for both methods is negligible. This is either a copy-paste error or a data processing mistake, affecting approximately half the rows in this table. Every affected result is unreliable. The paper cannot be accepted without correcting or rerunning these experiments.

### Minor

2. **Imprecise framing: entropy is a scalar summary of the distribution, not the distribution itself.** The paper repeatedly claims that entropy-based pruning "minimizes the change of the global prediction distribution" (Abstract, Sections 1, 4.1, 4.3, 6). However, the Taylor criterion (Equation 4) is computed on \(C_H(x)\) — a scalar that collapses the \(V\)-dimensional output distribution into a single number. Minimizing the change in entropy is not equivalent to minimizing the change in the full distribution; two very different distributions can share identical entropy. The method is better described as preserving the model's *uncertainty profile*. The empirical evidence that entropy better preserves the actual distribution (Table 7) shows only tiny margins: JS distance differences of 0.002 at 20% and 0.009 at 30%. The method still has the genuine advantage that \(\partial C_H/\partial h_i = \sum_j (\partial C_H/\partial p_j)(\partial p_j/\partial h_i)\) depends on all tokens via the chain rule, unlike cross-entropy which only receives gradient from the single ground-truth token — but this is not the same as "minimizing distributional change." The paper should either provide a theoretical bridge or recalibrate its claims.

3. **"Exceeding the original dense model" claim is uncontrolled.** The paper states that the 20% pruned+fine-tuned LLaMA-2-7B (59.0%) "exceeds the performance of the original dense model" (58.3%) (lines 80, 209). However, the original model was *not* fine-tuned on LaMini, while the pruned model was. The gain could partially or entirely come from the LaMini fine-tuning rather than from pruning quality. The no-fine-tuning results (Table 6) show the 20% IE model at 53.1% — far below the original's 58.3% — confirming that the claim conflates pruning quality with recovery fine-tuning. This should be either retracted or supported by a controlled comparison where the original model is also fine-tuned on LaMini.

4. **No variance reporting.** None of the tables report standard deviations, confidence intervals, or results across multiple random seeds. While zero-shot benchmark evaluations are often deterministic, the pruning+fine-tuning pipeline has stochastic elements (LoRA training, data ordering). The performance differences between methods are often small (0.5-0.8%), and without variance estimates the reader cannot assess reliability.

### Trivial
None.

## Nice-to-Haves

- A sensitivity analysis on calibration dataset size would be useful; the method uses 43k sequences, but a smaller set would be more practical for broader adoption.
- An analysis of which neurons get pruned (by frequency, magnitude, or layer depth) could deepen the contribution.
- A brief check on sensitivity to fine-tuning duration or LoRA rank would strengthen the paper, though the contribution is the pruning criterion itself.

## Removed Points

- **"No comparison with Wanda or SparseGPT"**: Wanda and SparseGPT are unstructured pruning methods; the paper explicitly focuses on structural pruning and compares against structural baselines. This comparison is outside the paper's stated scope.
- **"Missing analysis of calibration dataset size"** and **"Missing pruned neuron analysis"**: These are useful extensions, not core weaknesses. Moved to Nice-to-Haves.
- **"The 30% Qwen2.5-7B SDMPrune row has a missing Wino value"**: Could be a PDF parsing artifact; the clear verified problem is the data duplication.
- **"Entropy scalar ≠ distribution is a fatal flaw"**: Downgraded to Minor. The gradient \(\partial C_H/\partial h_i\) depends on all \(p_j\) through the chain rule, so the method genuinely considers the full distribution — the issue is that it aggregates to a scalar. The practical advantage is real; only the framing is imprecise.

## Novel Insights

The reviewer's observation about the entropy-distribution gap is the most incisive point: the paper's central framing claims to "minimize the change of the global prediction distribution," but the Taylor expansion is on a scalar entropy value. Two distributions with identical entropy but different token-level probabilities would be equally preferred by the criterion. This gap is real but not fatal — the method still considers all tokens (unlike cross-entropy, whose gradient only flows through the single ground-truth probability) and the empirical results are consistent. The paper would be stronger if it acknowledged this nuance and positioned the method as considering the full output distribution in the importance criterion rather than claiming to preserve the distribution itself.

## Suggestions

1. **Fix Table 3.** The duplicated rows must be corrected with properly computed results. This is the single most important fix.
2. **Reframe the "global prediction distribution" language.** Replace phrases like "minimizes the change of the global prediction distribution" with more precise alternatives such as "considers all potential predictions in the importance criterion" or "preserves the model's output uncertainty profile."
3. **Qualify the "exceeding the original model" claim.** Either add a controlled comparison (original model fine-tuned on LaMini) or explicitly note that the comparison is with the original dense model without fine-tuning.
4. **Add a brief note on variance** — even a statement that benchmark evaluations are deterministic for a fixed model checkpoint would help readers calibrate their confidence.

MY FINAL SCORE: <score>6.0</score>
MY FINAL DECISION: <decision>Accept</decision>