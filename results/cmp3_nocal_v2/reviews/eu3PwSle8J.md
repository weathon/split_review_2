## Summary

This paper identifies a key limitation in existing prompt injection defenses that rely on instruction hierarchy (IH) signals: they inject the IH signal only at the input layer, and the signal degrades as it propagates through the decoder layers. To address this, the authors propose Augmented Intermediate Representations (AIR), which injects layer-specific, trainable IH embeddings at every transformer layer. Across three model families (3B–8B) and two training methods (SFT, DPO), AIR consistently improves robustness against gradient-based prompt injection attacks, yielding 1.4–9.3× reduction in attack success rate over prior input-only methods (Delimiter, ISE) while adding only 0.4M parameters (~0.005% increase).

## Strengths

- **Empirically motivated architectural insight (Figure 3).** The paper demonstrates that input-only IH injection (Delimiter, ISE) suffers from increasing cosine similarity between differently-privileged token representations as they propagate through deeper layers — Delimiter yields a flat 1.0 similarity across all layers. This directly motivates the need for per-layer injection and is supported by concrete measurements, not just intuition.

- **Extremely low overhead.** AIR adds 0.4M parameters to Llama-3.1-8B (0.005% increase). Inference cost is negligible — just a table lookup and addition per token per layer — which is a genuine practical advantage over architectural alternatives.

- **Consistent and large improvements on gradient-based attacks (Table 1).** Across all 6 model/training configurations, AIR strictly outperforms both Delimiter and ISE on GCG and Astra attacks, often by wide margins. On Qwen-2.5-7B (DPO), GCG ASR drops from 7.7% (ISE) to 1.6% (AIR); Astra ASR drops from 2.3% (ISE) to 0.9% (AIR). The pattern holds across Llama-3.2-3B, Qwen-2.5-7B, and Llama-3.1-8B.

- **Controlled comparison methodology.** Rather than reusing prior papers' separate pipelines, the paper re-implements all three IH injection mechanisms (Delimiter, ISE, AIR) within a single pipeline with shared training data, hyperparameters, and evaluation, isolating the variable of interest.

## Weaknesses

### Fatal

None.

### Major

- **SFT vs. DPO comparison is confounded by training regime differences.** The paper compares SFT (full fine-tuning, LR 1e-5) and DPO (LoRA-based, LR 2e-4) and draws conclusions such as "adversarial training with DPO yields more robust models than SFT." However, the training method (SFT vs. DPO) is not cleanly separable from the parameter efficiency (full FT vs. LoRA) and learning rate. This does not affect within-training-method comparisons (Delim vs. ISE vs. AIR under SFT, and separately under DPO), which are the paper's main claims. But any claim comparing SFT and DPO directly should be caveated.

- **Limited attack optimization budget.** The gradient-based attacks use only 50 steps (SFT) or 200 steps (DPO), whereas standard GCG in the literature often uses 500–1000 steps. The paper's own Figure 7 shows attacker loss continuing to decrease at 200 steps without plateauing for several configurations. With more optimization steps, the advantage of AIR could shrink. The paper should test longer optimization or argue why the current budget is sufficient.

- **No confidence intervals or variance for the main ASR results in Table 1.** While Figure 7 shows shaded standard deviations for loss curves, the headline ASR numbers (GCG, Astra, SEP) are reported as point estimates. For close comparisons (e.g., SEP on Llama-3.1-8B SFT: ISE and AIR both at 3.1), a reader cannot assess whether methods genuinely tie or the estimate is noisy. Bootstrap confidence intervals would substantially strengthen the table.

### Minor

- **The claimed 1.6× lower bound for GCG ASR reduction is slightly overstated.** The paper states "1.6× to 9.2× reduction in ASR on gradient-based attacks." Computing ratios against the best non-AIR defense per row yields a minimum of ~1.43× (Llama-3.1-8B DPO: ISE 4.0 / AIR 2.8 ≈ 1.43×). The discrepancy is small (~11% relative) but the reported lower bound should be tightened or the data point should be explained.

- **Evaluation uses only one adversarial target ("hacked!").** All robustness tests optimize or check for the string "hacked!" as the adversary's goal. This is simple to measure but does not represent the full range of prompt injection objectives (data exfiltration, tool misuse, chain-of-thought manipulation). The paper should at minimum acknowledge this limitation.

- **Figure 3 methodology is underspecified.** The paper reports encoding "100 prompts from the AlpacaEval dataset with two different privilege levels" to measure cosine similarity, but does not clarify whether the same tokens are assigned different privilege levels (measuring representation drift) or different tokens from different privilege segments are compared. The intent is inferable from context but should be stated precisely.

- **Utility evaluation is narrow.** The paper measures instruction-following quality (AlpacaEval 2.0, SEP utility) but does not evaluate general language understanding (MMLU, GSM8K, HumanEval). Since AIR modifies representations at every layer, it could plausibly affect broader capabilities beyond instruction following. A few standard benchmarks would strengthen the claim that utility is not significantly degraded.

### Trivial

None.

## Nice-to-Haves

- Broader utility benchmarks (MMLU, GSM8K) to verify that per-layer IH embeddings do not degrade general capabilities.
- Longer attack optimization (500–1000 GCG steps) to test whether AIR's advantage persists under more thoroughly optimized attacks.
- Confidence intervals for the ASR values in Table 1.
- Clarify how the SEP separation score relates to the gradient-based attack results — the two evaluate different aspects of robustness, and a brief discussion would help readers connect them.
- Clarify that the 1.6×–9.2× range is computed against the best-performing non-AIR defense in each row, which varies between Delimiter and ISE.

## Removed Points

*These points were flagged in the input review but are removed with justifications below:*

- **"Abstract conflates two distinct families of prior work."** Removed: The abstract explicitly says "special delimiter tokens or additive embeddings," naming both families. The paper correctly groups them under the shared limitation of input-only injection, which is the relevant category for the critique.
- **"Strengthening the Paper on Its Own Terms point about transparency of ASR reduction computation."** This was already noted in Nice-to-Haves above; it does not need to be listed as a weakness.
- **"SEP evaluation relationship to gradient-based attacks needs explanation."** Moved to Nice-to-Haves; it is a clarity suggestion, not a weakness.
- **"Figure 3 needs more description about how privilege levels are assigned."** Kept as Minor weakness above with softened wording.

## Novel Insights

The most interesting observation from the review process is the parallel the paper draws between AIR and the evolution of positional embeddings (from input-only to RoPE's per-layer injection). This framing is not just rhetorical — it suggests a design principle that could generalize beyond prompt injection: when a signal needs to persist across transformer layers, injecting it only at the input may be fundamentally insufficient. The cosine similarity measurements in Figure 3 provide a concrete diagnostic for when input-only injection fails. The review also surfaces that the SFT vs. DPO comparison is inadvertently confounded with full FT vs. LoRA, which the paper itself does not flag as a confound.

## Suggestions

- Correct the lower bound of the GCG ASR reduction claim from 1.6× to the actual minimum (~1.4×) or provide a justification for excluding the Llama-3.1-8B DPO data point.
- Add a caveat to the SFT vs. DPO comparison noting the full FT vs. LoRA confound.
- Increase the GCG optimization budget to 500+ steps for a subset of configurations to test whether AIR's advantage persists.
- Report bootstrap confidence intervals or standard errors for the ASR values in Table 1.

## Score and Decision

**MY FINAL SCORE:** <score>8</score>
**MY FINAL DECISION:** <decision>Accept</decision>