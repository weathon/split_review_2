## Summary

The paper proposes HFPrune, a structured pruning method for LLMs that replaces the standard cross-entropy loss with information entropy as the criterion for Taylor-expansion-based neuron importance scoring. The method focuses on pruning MLP modules and uses entropy to preserve the model's full output distribution rather than just the single-target-token probability. Results are reported on LLaMA and Qwen series models across zero-shot benchmarks, with claimed improvements over cross-entropy-based pruning and self-distillation baselines.

## Strengths

- **Conceptually clean and well-motivated idea.** The paper identifies a genuine limitation of standard Taylor pruning: cross-entropy measures importance only through the single target token probability, ignoring the rest of the output distribution. Replacing this with information entropy of the full output distribution (§4.2, Equation 3) is simple, intuitive, and directly addresses this limitation. The contrast is clearly illustrated in Figure 1.

- **Label-free property is a genuine practical advantage.** Because entropy depends only on the model's own output probabilities, importance scores can be computed from unlabeled calibration data without requiring ground-truth labels (§4.2). This is a real practical benefit for deployment.

- **Efficiency gains over self-distillation are real and well-demonstrated.** Table 5 shows HFPrune is ~3× faster than SDMPrune and consumes ~31% less peak memory on LLaMA2-7B. This follows naturally from requiring only one forward-backward pass per sample rather than a separate teacher model.

- **Pruning-process analysis (Table 5 vs. Table 4).** The paper usefully separates the *cost of the pruning procedure itself* from the *inference speed of the pruned model* — a distinction many pruning papers blur.

## Weaknesses

### Fatal

None.

### Major

1. **Duplicated rows in Table 3 — data integrity concern.** Four pairs of rows are numerically identical across all 11 benchmark scores despite belonging to different models (Qwen2.5-7B, Qwen2.5-1.5B, Qwen3-1.7B) at different pruning ratios:
   - Qwen2.5-7B @ 40% SDMPrune (line 241) = Qwen2.5-1.5B @ 20% SDMPrune (line 244): all 11 scores match exactly.
   - Qwen2.5-7B @ 40% HFPrune (line 242) = Qwen2.5-1.5B @ 20% HFPrune (line 245): all 11 scores match exactly.
   - Qwen2.5-1.5B @ 40% SDMPrune (line 248) = Qwen3-1.7B @ 20% SDMPrune (line 251): all 11 scores match exactly.
   - Qwen2.5-1.5B @ 40% HFPrune (line 249) = Qwen3-1.7B @ 20% HFPrune (line 252): all 11 scores match exactly.

   It is probabilistically impossible for different model architectures at different sparsity levels to produce identical sets of 11 numbers across diverse benchmarks (ARC-challenge, BoolQ, PIQA, Winogrande, etc.). This appears to be a copy-paste error during table construction. It means the claimed results for Qwen2.5-1.5B @ 20%, Qwen2.5-7B @ 40%, Qwen2.5-1.5B @ 40%, and Qwen3-1.7B @ 20% cannot be trusted as presented. Since Table 3 is central to the paper's multi-model evaluation, this substantially undermines confidence in the experimental evidence.

2. **"Exceeds the original model" claim lacks proper control.** The paper claims (abstract, §1, §5.2.1) that at 20% pruning on LLaMA2-7B, the pruned model (59.0%) exceeds the original dense model (58.3%). However, the pruned model receives 2 epochs of LoRA fine-tuning on LaMini instruction data, while the original model is evaluated without any fine-tuning. The proper control would be to fine-tune the *unpruned* model identically and compare against that. The observed gain could simply reflect the fine-tuning adaptation rather than any benefit of pruning.

### Minor

1. **Text/table inconsistency in speedup.** The text (§5.2.2) states "pruning 30% of the MLP layers results in a 1.47× speedup in prefill latency," but Table 4 shows 1.35× for 30% pruning. Computing from the latency values in the table (57.5 ms / 42.1 ms ≈ 1.366×) confirms the table is correct and the text is wrong.

2. **No variance or significance reporting.** The margins of improvement are consistently small — typically 0.5–0.8 percentage points in average accuracy (e.g., Table 1: 59.0% vs 58.2% over SDMPrune at 20%). No confidence intervals, standard deviations, or significance tests are reported anywhere. Given that zero-shot accuracies on these benchmarks depend on few-shot formatting, prompt phrasing, and randomness, the reader cannot determine whether these differences reflect systematic improvement or measurement noise. This is standard practice in this area but still limits the strength of the claims.

3. **No perplexity evaluation.** The paper evaluates only zero-shot classification/QA benchmarks. Perplexity on a held-out language modeling corpus (e.g., WikiText-2, C4 validation) would directly measure preservation of language modeling capability and is standard in most LLM pruning papers (SparseGPT, Wanda, etc.). Its absence is a notable gap, especially for a method whose central claim is about preserving the output distribution.

4. **Calibration dataset size not controlled across baselines.** The paper uses 43,128 sequences × 1024 tokens for calibration, which is substantially larger than typical calibration sets (e.g., Wanda and SparseGPT use 128 sequences). It is unclear whether the baseline methods (LLM-pruner, LoRAPrune, SDMPrune) used calibration data of comparable size. A larger calibration set could give HFPrune an advantage independent of the entropy criterion.

### Trivial

- The 30% SDMPrune row for Qwen2.5-7B in Table 3 is missing its average column value.

## Nice-to-Haves

- Explore adaptive/non-uniform sparsity allocation using layer-specific entropy values (mentioned as future work in the conclusion).
- Include perplexity evaluation on held-out language modeling data to directly test the core hypothesis about distribution preservation.
- Provide a brief discussion situating structured MLP pruning with entropy against well-known unstructured methods (SparseGPT, Wanda) for context.

## Removed Points

These points from the input review were removed with justification:
- **Taylor approximation breakdown speculation** — not evidenced; does not apply to the actual experimental results.
- **Figure 1 framing being "overstated"** — stylistic preference, not a substantive weakness.
- **SD criterion wins on some individual benchmarks in Table 6** — the paper reports averages, which is the standard evaluation practice.
- **Table 8 ablation confounded variables** — the comparison is MLP-only vs attention+MLP both at the stated ratio; the concern is unclear from the paper but not clearly wrong either; moved to nice-to-have.
- **Missing related works** — cannot verify existence of unmentioned works.
- **No adaptive sparsity exploration** — stated as future work; not a weakness.
- **Generic area-of-concern speculations without concrete evidence** — removed per filtering guidelines.

## Novel Insights

None beyond the paper's own contributions. The input reviews did not surface a new perspective that the paper itself does not already articulate.

## Suggestions

- **Fix Table 3 immediately.** Every duplicated row must be replaced with the correct experimental result. Verify all other tables for similar copy-paste errors. Without corrected data, the Qwen experiments cannot be evaluated.
- **Add a controlled experiment** fine-tuning the unpruned LLaMA2-7B on LaMini under the identical LoRA protocol, then compare. This would validate or refute the "exceeds original" claim.
- **Correct the speedup discrepancy** in §5.2.2 (1.47× → 1.35× or whichever is correct).
- **Add variance estimates** (e.g., multiple seeds or bootstrapped confidence intervals) for the central comparisons in Tables 1 and 6, given the small margins.
- **Report perplexity** on a held-out LM dataset (WikiText-2, C4) to complement the zero-shot benchmarks.

## Score and Decision

**Calibration anchors** (retrieved from human-review corpus):

| Paper (path suffix) | Avg Human Score | Round | Comparison |
|---|---|---|---|
| 8QTpYC4smR (survey paper) | 1.00 | R1 | Not comparable — pure literature survey, far weaker contribution |
| yx8bU8T5ZN (delta parameter editing) | 2.33 | R1 | Comparable rejection-level paper; HFPrune has stronger motivation |
| EOPLy80bBm (data pruning study) | 3.00 | R1 | Empirical study with flaws; HFPrune has a more novel method |
| EjHtQlKEzV (layer pruning benchmarking) | 4.50 | R1 | Empirical study with limited novelty; HFPrune has a cleaner idea but worse data integrity |
| Y0qmwm6tgy (MoreauPruner) | 4.80 | R1 | Structured LLM pruning with marginal gains; HFPrune has comparable contribution but a data-integrity issue |
| ji6MYm4Htg (AggregationPruner) | 4.80 | R1 | Training-free pruning with practical focus; HFPrune has better motivation but weaker experimental trustworthiness |
| 9KVT1e1qf7 (LoRAPrune) | 5.20 | R1 | Integrates LoRA with pruning; HFPrune has a simpler, cleaner idea but a more serious experimental flaw |
| mMmzHS28ht (LLM pruning + distillation) | 5.00 | R1 | Practical compression with modest contributions; HFPrune comparable |
| pOBvr1PxFd (OWL) | 6.00 | R1 | Thorough analysis and strong results; HFPrune is less thorough and has weaker experimental evidence |
| ngmEcEer8a (layer pruning analysis) | 6.50 | R1 | Strong empirical study, clear contribution; HFPrune has a more novel method but weaker execution |

**Round 1 bracket**: 3.5 – 5.5 (borderline reject to borderline accept)

**Final score determination**: The paper's core idea is clean and well-motivated, placing it clearly above papers in the 1–3 range. However, the data integrity issue in Table 3 (duplicated numerical rows) is a genuine and serious concern that erodes confidence in the experimental results. The LLaMA results (Tables 1, 2) and ablation (Table 6) provide some evidence, but without the Qwen results being trustworthy, the paper's multi-model claims are weakened. Compared to the calibration anchors, the paper has a stronger conceptual contribution than the ~4.5–5.0 papers but a worse experimental foundation. The idea itself is sound enough to warrant further investigation, but the present manuscript's experimental evidence is not fully credible. This places it at the lower end of the borderline reject range.

MY FINAL SCORE: <score>4.0</score>
MY FINAL DECISION: <decision>Reject</decision>