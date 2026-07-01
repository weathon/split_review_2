## Summary

This paper introduces Dynamic Nested Depth (DND), a method that adds a lightweight router to a frozen pretrained LLM and, during a subsequent SFT stage, learns to select "critical" tokens at each layer and reprocess them through the same layer (nested depth). The router uses a linear layer with sigmoid output per token, compared against a threshold. Two training-strategy components are introduced: a router-controlling loss (score dispersion + distribution preservation) and a threshold control scheme (buffer proportional control + EMA synchronization). DND is evaluated on three 1B-class dense models (Qwen3-1.7B, Llama3.2-1B, Gemma3-1B) and a 30B MoE model (Qwen3-30B-A3B), showing improvements of +1.88–+2.61 on the small models and +0.87 average on the 30B model, with ~6% extra FLOPs and 91–93% throughput.

## Strengths

1. **Well-motivated problem framing.** The paper correctly identifies that token-level difficulty varies within a sequence and that allocating uniform compute is wasteful (Section 1, Figure 1). The connection to test-time scaling and the specific direction — deepening representations for difficult tokens rather than just pruning easy ones — is clearly articulated and grounded in cited literature (Gloeckle et al. 2024; Hao et al. 2024).

2. **Thoughtful training strategy design (Section 3.2, Figures 5–6).** The dual-loss approach (score dispersion via entropy maximization + distribution preservation via MSE pull toward 0.5) and the two-tier threshold control (buffer proportional control for real-time correction + EMA synchronization for drift prevention) address a real engineering problem in token-choice routing: making selection both discriminative and stable. The ablation (Table 4, columns 2–5) and visualizations (Figures 5, 6a, 6b) convincingly show these components are doing useful work.

3. **Token selection analysis (Section 4.5, Figures 4a/4b).** The correlation between selection frequency and vanilla-model logit entropy (r = 0.336, Figure 4a) and the reduction in entropy after DND processing (r = −0.581, Figure 4b) provide direct evidence that the router selects genuinely uncertain tokens and that the nested pass reduces that uncertainty. This mechanistic evidence grounds the method's claims in actual model behavior and is rare in papers of this type.

## Weaknesses

### Fatal
None.

### Major

1. **Missing control: selective deepening vs. uniform deepening is never tested.** The paper's central motivation (Section 1, lines 19–20: "Instead of uniformly applying extra recurrent depth to all tokens, we dynamically select the subset of tokens that pose greater difficulty") is an architectural claim about *selectivity*. Yet no experiment compares DND's selective version against the obvious control: applying the nested pass to **all** tokens (or a random 20% of tokens). The ablation in Table 4 varies the selection ratio (10%, 20%, 30%) but always uses the learned router — never a uniform-100% baseline or a random-selection baseline. Without this, the reader cannot determine whether the gain comes from the *selection mechanism* or simply from the extra forward pass and gradient updates on some tokens during SFT. This is the single most important missing experiment for the paper's advertised contribution.

2. **Thin baseline set.** The only direct baseline is ITT (Table 1), which shows a trivial +0.05 improvement. The paper dismisses MOR as requiring pretraining from scratch (valid), but then does not provide any additional comparison — neither to other post-training methods, nor to compute-matched alternatives (e.g., training the vanilla model for additional steps, or using the extra FLOPs for ensembling/self-consistency at inference). On the 30B model (Table 2), there is no baseline at all beyond the vanilla SFT model. The paper's efficiency claim ("minimal computing increase") would be strengthened by showing that the ~6% extra FLOPs cannot be better spent in a simpler way.

### Minor

3. **No statistical reliability reported.** Gains on the 30B MoE model average +0.87, with many individual benchmarks under +1 point (MMLU: +0.50, CMMLU: +0.37, BBH: +0.13, DROP: +0.27). No standard deviations, confidence intervals, or multiple-seed runs are reported. While single-run SFT is common in this field, the small deltas on the large model make it difficult to distinguish meaningful improvement from training noise. At minimum, the most critical results should be accompanied by variance estimates.

4. **Unsubstantiated claim about ITT's failure mode.** The paper states that ITT's limited performance "stems from the use of Top-P-based token selection for auto-regressive LLM, which introduces a mismatch between training and inference" (line 203). This is presented as an explanation but is not accompanied by any analysis, diagnostic, or ablation of ITT's behavior. It reads as an assertion rather than an evidence-backed conclusion.

5. **The fusion weight β is not ablated.** Equation (4) introduces a learnable parameter β that balances the vanilla and nested outputs. The contribution of this design choice is not tested independently (e.g., ablating to fixed mixing, or using p^i directly without β scaling). This is a non-trivial hyperparameter that could affect results.

6. **No limitations section or discussion of failure modes.** The paper presents only positive results. A candid discussion of where DND does not help, or cases where selection fails, would strengthen the paper — especially given the modest average gain on the 30B model.

### Trivial

7. **Table 4 formatting is confusing.** The column headers use ✓/×/– in a way that is not self-explanatory. In particular, column 2 (the full method) shows RC=✓ and TC=–, but "–" for TC is ambiguous — it is unclear whether it means "both components included" or "neither." The caption says "TC indicates threshold control (including buffer proportional control and EMA synchronization)," but does not clarify what "–" encodes.

8. **Qualitative claim about hierarchical processing is based on a single example.** Section 4.5 (lines 326–339) infers that "tokens selected by shallower layers are predominantly essential nouns, while those selected by deeper layers correspond to more abstract or syntactically critical components" from one example on GPQA. While presented as an observation ("reveals an interesting phenomenon"), this claim would benefit from systematic quantification across many examples.

## Nice-to-Haves

- **Approximate comparison to MOR.** The paper correctly notes that MOR requires pretraining from scratch, but a lightweight adaptation of pre-trained weights into a recurrent-like structure would make the "DND vs. alternative dynamic-depth method" comparison more complete.
- **Compute-matched baselines.** Spending the ~6% extra FLOPs on longer vanilla SFT training, or using self-consistency at inference time, would strengthen the efficiency claim.

## Removed Points

These points are flagged to be removed; treat them with caution:

- **"Post-training" framing is misleading** — removed because the reviewer's interpretation is non-standard. In the LLM literature, "post-training" refers to stages after pre-training (including SFT). The paper clearly states it uses full-scale SFT (Section 4.2), and the baseline comparison is SFT vs. SFT+DND, which is standard and transparent.

- **"Computing increase during training is not discussed"** — removed because the paper's efficiency focus is on inference (FLOPs and throughput), and training cost is implicitly the same as standard SFT. This is a standard scope choice.

- **Criticism of the "natural next step" framing in Section 1** — removed as a subjective stylistic opinion that does not affect technical validity.

- **Missing appendix details** — removed per instructions (parser strips appendices from all papers; they exist in the original submission).

- **Parameter count verification (0.03M vs. 86K)** — removed because the exact count depends on per-layer details in the appendix. The paper's claim of "negligible parameter increase (< 0.1M)" is in the right order of magnitude regardless.

## Novel Insights

None beyond the paper's own contributions. The reviews surface a structural evaluation gap (missing uniform-depth control) but do not contribute novel analytical insights beyond what the paper already provides.

## Suggestions

1. **Run the uniform-depth control experiment.** Apply the nested pass to 100% of tokens (or a random 20% baseline) under the same SFT recipe. If the selective version beats uniform, the central claim is supported. If uniform does equally well or better, the selection mechanism is unnecessary and the gain comes from the extra representational capacity.

2. **Add at least one compute-matched baseline.** For example, train the vanilla SFT model for ~6% more steps (matching DND's extra FLOPs), or report a simple "run the base model twice and average logits" baseline.

3. **Report variance.** Run at least 3 seeds on a subset of key benchmarks (e.g., the 30B MoE model's primary results) and report mean ± std.

4. **Tone down or evidence the ITT analysis.** Either remove the unsubstantiated explanation for ITT's performance or provide diagnostic evidence (e.g., selection ratio analysis, entropy analysis for ITT).

## Score and Decision

MY FINAL SCORE: <score>5.0</score>
MY FINAL DECISION: <decision>Reject</decision>