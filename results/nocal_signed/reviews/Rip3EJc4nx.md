Now let me finalize the review. I'll merge the two data-integrity sub-points and adjust slightly based on the impact scores.

## Summary

The paper proposes HFPrune, a structured pruning method for LLMs that replaces the standard cross-entropy loss criterion with the information entropy of the model's output distribution for Taylor-based neuron importance estimation. The core insight is that cross-entropy focuses importance on the single ground-truth token, while entropy captures the full prediction distribution, producing better pruning decisions without requiring a separate teacher model. The paper demonstrates the approach on LLaMA-2-7B, LLaMA3.2-3.2B/1.2B, and Qwen series models across multiple zero-shot benchmarks.

## Strengths

- **Clean, well-motivated idea (Figure 1, §4.2).** The paper identifies a genuine limitation of standard Taylor pruning — using cross-entropy loss focuses importance estimation on the single ground-truth token, ignoring the rest of the model's output distribution. Replacing it with information entropy of the full prediction distribution is conceptually elegant, label-free, and avoids the complexities of self-distillation approaches. The motivation is clearly laid out with intuitive visual support.

- **Strong practical efficiency gains (Table 5).** HFPrune is ~3× faster than SDMPruner and uses 31–41% less peak GPU memory across three model sizes (LLaMA3.2-1.2B, LLaMA3.2-3.2B, LLaMA2-7B). This is a direct and well-documented consequence of avoiding a separate teacher model, and represents a real engineering advantage.

- **Principled ablation study validates the core claim (Table 6).** The paper compares IE, CE, and SD criteria *without any post-pruning fine-tuning*, isolating the effect of the criterion itself. IE achieves the best average performance at both 20% pruning (53.1% vs. 52.6% for CE) and 30% pruning (47.3% vs. 46.8% for CE), directly supporting the central hypothesis.

- **Output distribution analysis corroborates the mechanism (Table 7).** The IE-criterion pruned model achieves lower JS divergence and higher Top-15 Jaccard similarity to the original model's output distribution than the CE-criterion pruned model, confirming that entropy-based pruning better preserves global prediction fidelity.

## Weaknesses

### Fatal

None.

### Major

- **Verified data integrity problem in Table 3.** Four rows of experimental results are duplicated verbatim across different model/pruning-ratio combinations. Specifically: (a) The Qwen2.5-7B 40% row (lines 241–242) is numerically identical to the Qwen2.5-1.5B 20% row (lines 244–245) — every single benchmark value for both SDMPrune and HFPrune matches exactly across 10 benchmarks. (b) The Qwen2.5-1.5B 40% row (lines 248–249) is identical to the Qwen3-1.7B 20% row (lines 251–252). These are not rounding coincidences across 20 numbers each; they are unambiguous copy-paste errors. Additionally, for Qwen2.5-1.5B the 40% averages (SDMPrune 50.3, HFPrune 54.3) are *higher* than the 30% averages (47.4, 51.7), violating the expected monotonicity under increased pruning. These issues together undermine the credibility of the entire Qwen experimental campaign and the paper's claim of "consistently surpass[ing] SDMPrune across various model sizes and pruning ratios" (§5.2.1). The authors must either provide corrected, independently verifiable data or retract the Qwen results.

- **The "exceeds the original model" claim (lines 80, 209) is based on an invalid comparison.** The paper states that at 20% pruning, HFPrune achieves 59.0% vs. the original dense model's 58.3% (Table 1). However, the pruned model received 2 epochs of LoRA fine-tuning on the LaMini instruction dataset, while the original model (line 181) was *not* fine-tuned. The improvement could plausibly come entirely from fine-tuning, not from the quality of the pruning criterion. To make this claim fairly, the authors need to either (a) fine-tune the original dense model under the same LoRA protocol and compare, or (b) compare pruned models *without* fine-tuning (Table 6 shows IE achieves only 53.1% at 20%, well below the original's 58.3%). As presented, this claim is misleading.

### Minor

- **Speedup number inconsistency between text and Table 4.** The text (line 260) states that pruning 30% of MLP layers "results in a 1.47× speedup in prefill latency," but Table 4 reports 1.35×. Verified: 57.5 ms / 42.1 ms ≈ 1.365×, which rounds to 1.35× or 1.37×, not 1.47×. This discrepancy suggests an error in either the text or the table.

- **No variance or statistical significance reporting.** All results in all tables are point estimates with no standard deviations, confidence intervals, or multiple seeds. The reported improvements are often 0.5–1.0 percentage points — within the range where statistical noise could reverse conclusions. While single-run evaluation is common for large-model benchmarks, the absence of any variance characterization makes it difficult to assess reliability, especially for the modest margins in Table 6.

- **Narrowed baseline comparison for Qwen models (Table 3).** For the Qwen experiments, the comparison is reduced to only SDMPrune, with no justification for dropping LLM-pruner, LoRAPrune, and LoRAP that appeared in the LLaMA-2-7B comparison (Table 1). This makes it harder to assess where HFPrune sits relative to the broader landscape for these models.

### Trivial

None.

## Nice-to-Haves

- Fine-tune the original (unpruned) model under the same LoRA protocol on LaMini and report alongside pruned results, to disentangle the effect of pruning from fine-tuning.
- Add a direct analysis of what entropy gradients capture that cross-entropy gradients miss (e.g., comparing top-k important neurons under each criterion for qualitative functional differences).
- Include an analysis of layer-specific entropy sensitivity — are some MLP layers more or less affected by entropy-based pruning?

## Removed Points

These points are flagged to be removed, treat them with caution:
- The critique that the CE gradient actually depends on all logits through the softmax denominator (so the paper overstates the dichotomy). This is a technically nuanced point; the paper's characterization that CE "focuses on" label-related prediction is directionally correct and not a real weakness.
- Request for comparison with FLAP, SlimGPT, Compresso — removed per instruction (missing related work concerns cannot be cited without external verification).
- "Modest improvement in ablation" (IE beats CE by 0.5pp) — removed; 0.5pp improvement in a no-fine-tuning setting is meaningful for a pruning criterion comparison.
- Request for Wanda/SparseGPT comparison — these are unstructured pruning methods outside the paper's scoped structural pruning comparison, and the paper explicitly notes this distinction.
- Various reproducibility nitpicks about undisclosed hyperparameters — addressed in the appendix (Section A.1).

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. **Fix Table 3 completely.** The duplicated rows must be corrected with actual experimental results, or the Qwen experiments should be transparently retracted/reported as incomplete. Reconcile the monotonicity violation.
2. **Add the missing fine-tuning baseline.** Fine-tune the original dense model under the identical LoRA protocol on LaMini and report it alongside pruned results so the "exceeds original" claim can be fairly assessed.
3. **Reconcile the speedup number** — either correct line 260 (1.47× → 1.35× or 1.37×) or correct Table 4.
4. **Add variance estimates** (multiple seeds or bootstrapped confidence intervals) for at least the key comparisons and the ablation study.

## Score and Decision

The paper's core methodological contribution — using information entropy as the Taylor-pruning criterion — is sound, well-motivated, and supported by a clean ablation (Table 6). The practical efficiency gains over self-distillation (Table 5) are clear and valuable. However, the experimental presentation has **verified, serious issues**: a data integrity problem in Table 3 (four rows of duplicated results across different model/ratio conditions, plus a monotonicity violation) that undermines all Qwen claims, a misleading "exceeds original model" comparison, and an internal speedup inconsistency. These issues erode trust in the reported experimental evidence. The paper's core idea merits publication, but the evidence as currently presented is not reliable enough to support acceptance. A corrected version would deserve reconsideration.

**MY FINAL SCORE: <score>4.0</score>**
**MY FINAL DECISION: <decision>Reject</decision>**