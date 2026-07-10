## Summary

This paper proposes Augmented Intermediate Representations (AIR), a method that injects instruction hierarchy (IH) signals into every decoder layer of an LLM rather than only at the input layer, as done in prior work (Delimiters, ISE). AIR adds one small trainable embedding table per layer (0.005% parameter overhead) to encode privilege-level information. The method is evaluated across 3 model families, 2 training methods (SFT, DPO), and multiple attack types, showing consistent improvements in robustness against gradient-based prompt injection attacks.

## Strengths

- **Clean, empirically supported motivation (Section 3, Figure 3).** The paper identifies a concrete limitation — that IH signals degrade as they propagate through layers — and demonstrates it quantitatively with a cosine-similarity analysis showing that Delim and ISE produce increasingly similar representations for tokens with different privilege levels across deeper layers. This observation is specific, falsifiable, and directly motivates the proposed solution.

- **Simple, low-overhead method with clear architectural rationale.** AIR adds one trainable embedding table per decoder layer (0.005% parameter increase for Llama-3.1-8B). The analogy to the evolution from absolute positional encodings to RoPE grounds the design in a known principle — that propagating critical signals through all layers rather than injecting them only at the input is a proven approach.

- **Consistent directional results across a systematic evaluation matrix.** The evaluation spans 3 model families/sizes, 2 adversarial training methods (SFT, DPO), 2 gradient-based attacks (GCG, Astra), 4 static attacks, and the SEP benchmark. Across almost all settings, AIR achieves equal or lower ASR than Delim and ISE. No configuration shows AIR performing worse than the baselines on the key gradient-based metrics.

- **Dramatic improvements on some configurations.** On gradient-based attacks, AIR reduces ASR substantially in several settings (e.g., GCG on Llama-3.2-3B SFT: 38.0% → 4.1%; Astra on Qwen-2.5-7B SFT: 39.2% → 2.4%). These large margins cannot be explained by noise and demonstrate the practical value of the approach.

## Weaknesses

### Fatal
None.

### Major
None.

### Minor

- **Imprecise headline quantitative claim.** The abstract and contributions state that AIR yields a "1.6× to 9.2× reduction" on "gradient-based attacks" generally. However, (a) one GCG configuration (Llama-3.1-8B DPO: best baseline ASR of 4.0 vs. AIR 2.8 = 1.43×) falls below the 1.6× floor, and (b) multiple Astra DPO configurations also fall below this range. The results section (line 242) correctly restricts the range claim to GCG, but the abstract and contributions use broader language. The quantitative finding is correct in direction, but the advertised range is slightly selectively framed. The paper would be more precise stating "up to 9.2×, with consistent improvements across all settings."

- **Static attack results are saturated, narrowing the axis on which AIR's incremental contribution is visible.** For all four static attacks (Naive, Ignore, Completion, Escape Separation), every method including the unprotected baseline achieves ASR near zero. The paper acknowledges this transparently (line 240), but it means the practical advantage of AIR is only demonstrated against adaptive gradient-based attackers with white-box access. The method's value proposition rests primarily on one attack axis. This does not invalidate the contribution (gradient-based attacks are the harder threat model) but should be stated more directly as a scope limitation.

- **Uncertainty about baseline implementation fidelity.** The paper implements Delim and ISE using its own re-implementations (trainable special tokens *[INST]*/*[INPT]* for Delim; trainable segment embeddings for ISE). The original papers may have used different designs — more delimiter tokens, different placement strategies, or different training procedures. While the paper correctly controls for training procedure across methods, the lack of verification that these re-implementations are faithful to the original SOTA methods weakens the "compared to state-of-the-art" framing.

- **The SEP evaluation shows only modest advantages in several configurations** (e.g., Llama-3.1-8B SFT: AIR and ISE tied at 3.1; Llama-3.2-3B DPO: all methods at 2.6). The paper's claim that AIR "consistently enhances" separation is supported directionally but the margins are sometimes small enough that significance is unclear.

- **No confidence intervals or significance tests.** Table 1 reports point estimates without variance. For close comparisons (e.g., the tied SEP scores), it is impossible to assess whether small differences are meaningful. This is especially relevant given the small ASR values (0.0%, 0.1%) where a single successful attack can change the reported value.

### Trivial

- **The motivation diagnostic (Figure 3) is limited to one model (Llama-3.2-3B) and 100 prompts from AlpacaEval.** The subsequent robustness results corroborate the hypothesis, so this does not weaken the paper's conclusions, but the diagnostic itself would be stronger with broader evidence across more models.

## Nice-to-Haves

- An ablation isolating the "layer injection" hypothesis from the "additional parameters" hypothesis — e.g., an ISE baseline with proportionally increased capacity, or a version of AIR with shared (rather than per-layer independent) embeddings.
- Training wall-clock time and peak memory comparison.
- A brief discussion of how privilege-level annotations are generated in practice for real user inputs (a limitation shared by all IH-based methods, but worth noting).

## Removed Points
These points were flagged in the input review and removed with justification:
- "RoPE analogy is slightly overstated" — the paper's analogy is reasonable and appropriately qualified.
- "Section 2: gap between formalism and actual metric" — ASR is a standard practical proxy.
- "Logit-based ASR should be stated explicitly" — the paper already states this (line 190).
- "200 vs 50 optimization steps as a confound" — within each training method, all methods use the same step count.
- "LoRA vs full fine-tuning as a confound" — primary comparisons are within SFT or DPO, not between them.
- "Missing limitations section" — appendix content is stripped by the parser per policy.
- "Training compute cost not quantified" — parameter overhead (0.005%) is provided; cost is stated to be similar to prior works.
- "Practical deployment concerns about privilege annotations" — shared by all IH-based approaches.

## Novel Insights
None beyond the paper's own contributions. The key insight — that IH signals should be injected at every layer rather than only at the input — is well-motivated by the diagnostic and well-supported by the evaluation, but the reviews did not surface any fundamentally new perspective beyond what the paper itself presents.

## Suggestions

1. Correct the "1.6× to 9.2×" claim in the abstract and contributions to either restrict it to GCG (as the results section already does) or accurately reflect the full observed range across all gradient-based configurations.

2. Add an ablation that separates the "layer injection" mechanism from the "additional capacity" mechanism — e.g., an ISE variant with expanded embedding dimension, or a shared (rather than per-layer independent) AIR embedding.

3. Report standard errors or confidence intervals for the main ASR results in Table 1, especially for close comparisons and near-zero values.

4. Explicitly characterize the Delim and ISE baselines as re-implementations and discuss any known differences from the original papers.

## Score and Decision

MY FINAL SCORE: <score>8</score>
MY FINAL DECISION: <decision>Accept</decision>