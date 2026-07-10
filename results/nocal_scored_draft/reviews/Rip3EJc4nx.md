## Summary

This paper proposes HFPrune, a structural pruning method for LLM MLP neurons that replaces the standard cross-entropy loss criterion with information entropy of the full output distribution for Taylor-expansion-based importance scoring. The method is label-free, avoids the computational overhead of self-distillation approaches, and aims to preserve the model's global prediction distribution rather than just the ground-truth next-token probability.

## Strengths

- **Clear and well-motivated idea (Sections 1, 4.2).** The paper correctly identifies a genuine limitation of standard Taylor pruning — using one-hot cross-entropy restricts importance estimation to only the ground-truth next token, ignoring the rest of the output distribution. The proposed alternative (information entropy of the full output distribution) is conceptually clean and directly addresses this limitation.

- **Method is simple and computationally efficient (Section 4.2, Table 5).** Unlike the self-distillation approach (SDMPrune), which requires a separate teacher model and suffers from a zero-gradient initialization problem, the entropy criterion requires only a single forward and backward pass per sample, with no labels. Table 5 shows meaningful speedups (~3× faster than SDMPrune for LLaMA2-7B) and reduced memory.

- **Ablation that isolates the criterion's effect (Table 6).** The paper compares IE, CE, and SD criteria *without post-pruning fine-tuning*, which directly tests the claim that the entropy criterion produces better importance scores per se, independent of the recovery phase. IE outperforms the best baseline by 0.5 pp at both ratios.

- **Distribution-preservation analysis (Table 7).** The JS Divergence and Top-15 Jaccard metrics offer evidence that the IE criterion better preserves the output distribution shape, aligning with the paper's central motivation.

## Weaknesses

### Fatal

- **Duplicate numerical results in Table 3 invalidate the Qwen experiments.** Two independent pairs of entries are bit-for-bit identical across different model families, sizes, and pruning ratios. Specifically: (1) Qwen2.5-7B at 40% pruning (both SDMPrune and HFPrune rows) is numerically identical to Qwen2.5-1.5B at 20% pruning across all 11 benchmark scores. (2) Qwen2.5-1.5B at 40% pruning is identically duplicated for Qwen3-1.7B at 20% pruning. This pattern cannot arise from legitimate experimentation. Table 3 is the central evidence for the claim that HFPrune "consistently surpasses SDMPrune across various model sizes and pruning ratios" on Qwen models. With duplicated entries, the Qwen results are unreliable, and the paper's empirical contribution is partially compromised. *(Verified directly from the paper text — lines 241–252.)*

### Major

- **The claim that the pruned model "outperforms the original model" confounds pruning with fine-tuning.** Section 5.2.1 states: *"our method even outperforms the original model by 0.7%"* (Table 1: 59.0 vs 58.3). However, the pruned model receives 2-epoch LoRA fine-tuning on the LaMini instruction dataset, while the original dense model receives none. Table 6 (which reports performance *without* any fine-tuning) shows the pruned model at 20% achieves only 53.1% — far below the original's 58.3%. This confirms that the reported improvement is attributable to the fine-tuning stage, not the pruning method. A proper comparison would fine-tune the original model under identical conditions.

### Minor

- **Speedup discrepancy between text and Table 4.** Section 5.2.2 states that pruning 30% of MLP layers yields a *1.47×* speedup in prefill latency, but Table 4 reports *1.35×*. Computing from the raw table values (57.5 ms / 42.1 ms ≈ 1.37×) supports neither number exactly. This suggests a reporting error. *(Lines 260 vs 270.)*

- **Baseline comparison procedure is underspecified.** The paper states it uses the LaMini dataset "across all experiments for fair comparison" and fine-tunes "each model variant" with LoRA for 2 epochs, but does not state whether the baseline results in Tables 1 and 2 (LLM-pruner, LoRAPrune, LoRAP, SDMPrune) were re-run by the authors with this identical pipeline or cited from original publications. The presence of "--" entries for LoRAP suggests at least some numbers are drawn from original papers, potentially with different fine-tuning setups.

- **No statistical significance or variance reported.** Gains over the best baseline are modest (0.5–0.8 pp on average in Tables 1 and 6). With single-run point estimates, these margins could fall within evaluation noise. While single-run reporting is common in this literature, the small margins make this limitation more consequential here.

### Trivial

None.

## Nice-to-Haves

- When claiming the pruned model exceeds the original, fine-tune the original model under identical conditions (same LoRA, same LaMini dataset, same 2 epochs) and compare.
- Report variance or confidence intervals for main results given the modest margins.
- Explicitly state in the experimental setup how each baseline result was obtained (re-run vs. cited).

## Removed Points

These points are flagged to be removed; treat them with caution:

- *Missing comparison with SparseGPT:* The paper focuses on structural pruning; SparseGPT is an unstructured method. Comparing against it is outside the paper's stated scope.
- *Only one baseline on Qwen models:* The paper explicitly focuses on SDMPrune as the strongest baseline. Also moot given the data duplication issue.
- *Conceptual concern about entropy vs prediction quality:* The reviewer notes this does not materialize empirically; it is speculative rather than a concrete weakness.
- *Section-by-section observations with no actionable criticism:* Notes about Tables 1–2 gaps being modest, Table 4 speedup being expected, Table 8 speculation, etc. — these are observations, not weaknesses.

## Novel Insights

None beyond the paper's own contributions. The reviews surface no perspective on the method or its implications that the paper itself does not already articulate.

## Suggestions

1. Correct all entries in Table 3 and verify against original experimental records before any resubmission.
2. When claiming the pruned model exceeds the original, fine-tune the original model under identical conditions and compare.
3. Report variance or confidence intervals for main results, since gains are modest.
4. Clarify how each baseline result was obtained.

MY FINAL SCORE: <score>3</score>
MY FINAL DECISION: <decision>Reject</decision>