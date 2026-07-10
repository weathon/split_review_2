## Summary

This paper proposes HFPrune, a structured pruning method for LLMs that replaces the standard one-hot cross-entropy loss with information entropy as the criterion for Taylor-based neuron importance scoring. The motivation is that cross-entropy only considers the single ground-truth token, while entropy considers the full output distribution. The method is evaluated on six models from LLaMA and Qwen families, at three pruning ratios (20%, 30%, 40%), across ten zero-shot benchmarks.

---

## Strengths

- **Conceptually clean and practical modification.** The paper identifies a genuine limitation of one-hot cross-entropy for Taylor pruning — it assesses importance based on a single token, ignoring the rest of the output distribution — and proposes a simple, computationally cheap fix that requires no auxiliary teacher model. Any practitioner can implement this change on top of existing Taylor-pruning pipelines.

- **Practical efficiency advantage over SDMPrune.** Table 5 shows HFPrune is roughly 3× faster and uses ~30% less peak GPU memory during the pruning process (e.g., LLaMA2-7B: 509s / 35.3 GB vs. 1540s / 51.2 GB). This is a meaningful practical benefit.

- **Well-motivated ablation study.** Table 6 isolates the pruning criterion effect without fine-tuning, and Table 7 measures distribution preservation via JS distance and Jaccard similarity. These help disentangle the contribution of the criterion change from the recovery fine-tuning.

---

## Weaknesses

### Fatal
None.

### Major

- **Table 3 contains duplicated numerical data, invalidating the Qwen experimental evidence.** Four pairs of rows are byte-identical across all ten benchmark scores plus the average for different model/pruning-ratio combinations:

  | Duplicate pair | Rows in paper |
  |---|---|
  | Qwen2.5-1.5B 20% SDMPrune = Qwen2.5-7B 40% SDMPrune | Lines 244 and 241 |
  | Qwen2.5-1.5B 20% HFPrune = Qwen2.5-7B 40% HFPrune | Lines 245 and 242 |
  | Qwen3-1.7B 20% SDMPrune = Qwen2.5-1.5B 40% SDMPrune | Lines 251 and 248 |
  | Qwen3-1.7B 20% HFPrune = Qwen2.5-1.5B 40% HFPrune | Lines 252 and 249 |

  These are not close values — they are numerically identical across all columns. The probability of two different models at different pruning ratios producing exactly the same performance on every one of ten diverse benchmarks is effectively zero. This is a clear table construction error. Since the paper uses the Qwen results (Table 3) as core evidence that HFPrune "consistently surpasses SDMPrune across various model sizes and pruning ratios," the affected Qwen experiments (Qwen2.5-1.5B at 20%, Qwen3-1.7B at 20%) are not trustworthy. The authors must explain this error and provide corrected results.

- **The headline claim ("exceeds original model") conflates pruning with fine-tuning.** The paper states (line 80) that "with 20% parameters and FLOPs reduction, our pruned model not only recovers but even exceed the performance of the original dense model." In Table 1, the original LLaMA2-7B achieves 58.3% without any fine-tuning on LaMini, while HFPrune at 20% achieves 59.0% **after 2 epochs of LoRA fine-tuning on LaMini**. The improvement could simply reflect the fine-tuning signal, not the pruning quality. The correct comparison would fine-tune the original model under the same protocol, or compare without fine-tuning. The latter (Table 6) shows only a 0.5 pp margin (53.1% IE vs. 52.6% CE at 20%). Stating "exceeds the original model" without qualifying this confound is misleading.

- **The JS distance evidence for the central claim is extremely weak.** Table 7 shows that at 20% pruning the JS distance gap between IE and CE is 0.002 (0.241 vs. 0.243). At 30% it is 0.009. No variance, confidence intervals, or significance tests are reported. For a paper whose central thesis is that entropy better preserves the global distribution, a 0.002 JS difference on a ~0.24 scale — without error bars — is not persuasive evidence.

### Minor

- **The "zero-gradient" criticism of SDMPrune is overstated.** The paper claims (line 68) that SDMPrune suffers from a "critical defect, where the initial distillation loss is zero, leaving no gradient to guide the initial importance scoring." Yet SDMPrune achieves 58.2% at 20% pruning (Table 1) — competitive with HFPrune's 59.0% — suggesting the characterization is incomplete. The paper does not explain how SDMPrune achieves reasonable performance despite this claimed defect.

- **No statistical significance or variance reporting.** None of the tables report standard deviations, confidence intervals, or significance tests. Given that many reported gains are small (0.5–0.8 pp), it is unclear whether differences are systematic or reflect stochastic variation in calibration data sampling, LoRA initialization, or fine-tuning.

- **Missing average value in Table 3.** The row for Qwen2.5-7B at 30% SDMPrune (line 239) has 10 benchmark scores but the average column is empty. While possibly a formatting artifact, this adds to presentation concerns given the data duplication issue.

- **Gap between the pruning criterion (scalar entropy) and the evaluation metric (distributional JS distance).** The paper evaluates using JS distance (a distribution-level divergence) but prunes using entropy (a scalar summary statistic). Two distributions can have identical entropy while differing arbitrarily. The paper's argument would be stronger if the criterion directly targeted distribution-level preservation.

### Trivial
None.

---

## Nice-to-Haves

- Adding a controlled experiment that fine-tunes the original model on LaMini under the same LoRA protocol, to enable an apples-to-apples comparison for the "exceeds original model" claim.
- Reporting bootstrap confidence intervals for the JS distance measurements in Table 7.
- Reporting results averaged over multiple pruning runs to distinguish signal from noise.

---

## Removed Points

These points are flagged as removed; treat them with caution:
- **Missing baselines (Wanda, SparseGPT, FLAP, SlimGPT):** The paper explicitly focuses on **structured** Taylor-based pruning; Wanda and SparseGPT are unstructured one-shot methods outside this scope.
- **Computational cost of full-vocabulary entropy summation:** The efficiency numbers in Table 5 demonstrate the cost is manageable.
- **Any criticism about the appendix or missing supplementary materials:** The appendix is stripped by the parser; it exists in the original submission.
- **Formatting / style nitpicks:** These are parser artifacts, not author errors.

---

## Novel Insights

None beyond the paper's own contributions.

---

## Suggestions

1. **Fix Table 3 and re-run the affected Qwen experiments.** This is the highest priority. The data duplication must be explained and corrected.
2. **Reword or contextualize the "exceeds original model" claim.** Either fine-tune the original model on LaMini and compare, or clearly state that the comparison is against the original model *without* fine-tuning.
3. **Strengthen the distribution-preservation evidence.** Report JL distance with confidence intervals, or consider using a distribution-level divergence directly as the pruning criterion to close the gap between criterion and evaluation.
4. **Report variance across multiple runs** for all main results, especially where margins are narrow.

---

## Score and Decision

**Calibration anchors retrieved across all rounds:**

| File | Avg Score | Round | Itemized? | Comparison to this paper |
|---|---|---|---|---|
| MoreauPruner (Y0qmwm6tgy.md) | 4.80 | R1 | Yes | Structured LLM pruning paper; marginal gains over baselines but no data integrity issues. My paper's data duplication is more severe. |
| Reassessing Layer Pruning (EjHtQlKEzV.md) | 4.50 | R1 | Yes | Empirical study of layer pruning; limited novelty but sound experiments. No data concerns. |
| OWL (pOBvr1PxFd.md) | 6.00 | R1 | Yes | Non-uniform sparsity pruning; strong results at high sparsity. No data concerns. |
| NEPENTHE (fk5ePN7YCS.md) | 3.75 | R2 | Yes | Entropy-based pruning but on small models; questionable methodology but no data fabrication. |
| FASP (f4b0YVwKUO.md) | 4.00 | R2 | Yes | Fast structured pruning; novelty concerns but clean experiments. |

**Bracket determination:** Round 1 narrowed to [3, 5]. Round 2 compared against FASP (4.00) and MoreauPruner (4.80), which both have clean experimental data but limited novelty/marginal gains. This paper has a **confirmed data duplication error** — a more severe problem than any weakness in those anchors. The LLaMA experiments support the method but the gains are modest (0.5-0.8 pp) and the headline claim is confounded by fine-tuning. The paper falls below all of the clean-data anchor papers.

**Final score: 3.0.** The paper proposes an interesting and well-motivated idea, but its experimental evidence is compromised by a confirmed data duplication error in Table 3 that affects two of the three Qwen model evaluations. Combined with inflated claims about exceeding the original model, weak distribution-preservation evidence, and no variance reporting, the paper in its current form does not meet the bar for acceptance.

MY FINAL SCORE: <score>3.0</score>
MY FINAL DECISION: <decision>Reject</decision>