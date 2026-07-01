Now I have all the evidence. Here is my final consolidated review.

---

## Summary

This paper proposes HFPrune, a structured pruning method for LLMs that replaces the standard cross-entropy (CE) loss with the information entropy (IE) of the model's output distribution as the criterion for Taylor-based neuron importance scoring. The idea is that CE only captures importance relative to the single ground-truth token, while IE considers all tokens in the vocabulary, providing a more holistic measure. The method is tested on LLaMA-2-7B, LLaMA-3.2, and Qwen series models at 20–40% MLP-only pruning ratios. The paper additionally reports a ~3× pruning-process speedup over a self-distillation baseline (SDMPrune).

## Strengths

1. **Well-motivated critique of CE-based Taylor pruning.** Section 4.2 and Figure 1 articulate a genuine limitation: one-hot CE scores importance based on a single ground-truth next token, ignoring the rest of the output distribution. This critique is specific, principled, and, to this reviewer's knowledge, not previously formalized in this way for structured LLM pruning.

2. **Conceptually clean solution.** Replacing CE with the information entropy of the output distribution (Equation 3) is mathematically simple, requires no teacher model, and avoids the "zero initial gradient" issue the paper identifies in self-distillation approaches (Section 1). Algorithm 1 is implementable in roughly 20 lines of code.

3. **Pruning-process efficiency advantage is convincingly demonstrated.** Table 5 shows HFPrune is ~3× faster than SDMPruner and uses 31–43% less peak GPU memory across three model sizes. This is a concrete practical benefit independent of the accuracy comparison.

## Weaknesses

### Fatal

1. **Table 3 contains rows identically duplicated across different model/pruning conditions — a data integrity failure.**

   Inspection of Table 3 reveals at least two pairs of rows where every one of the 10 benchmark scores is exactly identical across different models and pruning ratios:

   - **Qwen2.5-7B at 40%, SDMPrune** (line 241): `32.3, 59.2, 72.1, 56.2, 35.2, 72.0, 37.7, 43.6, 44.7, 58.2, avg=51.1`  
     **Qwen2.5-1.5B at 20%, SDMPrune** (line 244): `32.3, 59.2, 72.1, 56.2, 35.2, 72.0, 37.7, 43.6, 44.7, 58.2, avg=51.1`
   - **Qwen2.5-7B at 40%, HFPrune** (line 242): `41.8, 68.8, 79.4, 55.3, 39.4, 74.1, 38.7, 46.4, 42.2, 59.8, avg=54.6`  
     **Qwen2.5-1.5B at 20%, HFPrune** (line 245): `41.8, 68.8, 79.4, 55.3, 39.4, 74.1, 38.7, 46.4, 42.2, 59.8, avg=54.6`
   - **Qwen2.5-1.5B at 40%, SDMPrune** (line 248) is identical to **Qwen3-1.7B at 20%, SDMPrune** (line 251)
   - **Qwen2.5-1.5B at 40%, HFPrune** (line 249) is identical to **Qwen3-1.7B at 20%, HFPrune** (line 252)

   Two different model families (Qwen2.5 vs Qwen3) at different sizes (1.5B vs 1.7B) at different pruning ratios (40% vs 20%) cannot produce scores that are *identical across all 10 benchmarks*. The most likely explanation is a copy-paste error in table construction. This is a data integrity failure that undermines confidence in Table 3, which provides the primary evidence that HFPrune generalizes beyond the LLaMA family. Without corrected results, the paper's central empirical claim cannot be evaluated.

### Major

2. **The reported accuracy improvements over CE are small (0.5–0.8 pp average) and no statistical significance is reported anywhere in the paper.**

   In Table 6 (no fine-tuning, isolating the criterion effect), IE achieves 53.1 vs CE's 52.6 at 20% pruning — a 0.5 percentage point difference. At 30%, it is 47.3 vs 46.8 — again 0.5 pp. In Table 1 (with fine-tuning), HFPrune achieves 59.0 vs SDMPrune's 58.2 at 20% (0.8 pp) and 56.3 vs 55.6 at 30% (0.7 pp). The paper reports no confidence intervals, no standard deviations, and no information about multiple runs. For 10 diverse zero-shot benchmarks, each with its own variance, a 0.5–0.8 pp average advantage could easily fall within measurement noise. The claim that the IE criterion "fundamentally provides more accurate measures of neuron importance" (Section 5.3.1) is stronger than the evidence supports.

3. **The central mechanistic claim — that IE better preserves the global output distribution — has only marginal empirical support.**

   Table 7 reports JS distances of 0.243 vs 0.241 at 20% (difference of 0.002) and 0.362 vs 0.353 at 30% (difference of 0.009). Top-15 Jaccard values are 0.439 vs 0.445 at 20% and 0.588 vs 0.595 at 30%. These differences are tiny and the paper's own text acknowledges the 20% improvement is "modest." No statistical significance is reported for these comparisons either. The entire narrative of the method depends on the claim that entropy-based pruning *meaningfully* preserves the global distribution better than CE, yet the evidence provided is insufficient to establish that the difference is real or that it mediates the accuracy improvements.

### Minor

4. **The claim that the pruned model "exceeds the original model" (Section 1, abstract) is misleading due to an apples-to-oranges comparison.**

   The paper states that with 20% pruning, HFPrune achieves 59.0% average accuracy, surpassing the original model's 58.3% (Table 1). However, the original model's 58.3% is a zero-shot evaluation without any fine-tuning, while the pruned model's 59.0% is obtained *after* fine-tuning on the LaMini instruction dataset. The improvement may come from the fine-tuning, not from the pruning criterion. A proper comparison would fine-tune the *original* model on LaMini and compare its score against the pruned-then-fine-tuned model. As presented, this "exceeding the original" claim is not informative about pruning quality.

5. **The paper's characterization of SDMPrune's "zero-gradient issue" may be an oversimplification.**

   The paper argues (Section 1, paragraph 5; Section 5.2.1) that SDMPrune suffers from a "zero-gradient issue" because the initial distillation loss is zero, forcing SDMPrune to fall back on CE-based importance scoring. Standard practice for knowledge-distillation-based pruning typically uses warm-up, annealing, or hybrid CE+KD losses to avoid exactly this issue. Without a more detailed analysis of SDMPrune's actual training procedure (which is not provided in the paper), the claimed advantage over it may be overstated. This does not invalidate the paper's results, but it weakens the narrative that SDMPrune is inherently flawed.

6. **Several LoRAP entries in Table 1 are missing ("–") for multiple benchmarks, making the comparison incomplete.** The paper does not explain why these results are absent, which limits the usefulness of this baseline.

## Nice-to-Haves

- Include a "fine-tuned original" baseline so that the claim of exceeding the original model is on equal footing.
- Run multiple trials with different random seeds for calibration data sampling and report means and standard deviations for key comparisons (Tables 1, 6, 7).
- Expand the distributional analysis (Table 7) with per-sample distributions and paired significance tests.
- Add an attention-only ablation to Table 8 to fully isolate which module type causes degradation.
- Discuss the theoretical limitation that entropy gradient magnitude depends on model confidence: when the model is very confident (low entropy), gradients are small, which may systematically underestimate importance of neurons critical for confident predictions.

## Removed Points

These points were raised in the input review but are removed with justification:

- *No code or model weights provided.* Per policy, removal of criticism about release status of resources. The paper states code will be made public.
- *Missing comparison to Wanda and SparseGPT.* These are unstructured pruning methods; the paper's scope is structured pruning. Scope creep.
- *Section-by-section notes about speedup numbers being "modest" and about Table 8 missing attention-only comparison.* The speedup comment is subjective. The attention-only point is addressed in the Nice-to-Haves above rather than as a weakness.
- *SDMPrune efficiency comparison not reporting accuracy.* Table 5 is explicitly about time and memory of the pruning process, not accuracy. Accuracy comparisons are in Tables 1, 2, 3.
- *No limitations section.* Not a standard requirement; the point about entropy gradient magnitude is retained as a Nice-to-Have.
- *Cost of computing entropy gradient not reported.* Table 5 already provides end-to-end efficiency comparison; this is a detail that could be added but is not a weakness.
- *High-entropy vs low-entropy distinction not discussed.* A theoretical nuance that could be addressed in future work; not a weakness of the existing method given the results shown.

## Novel Insights

None beyond the paper's own contributions. The reviews surface the data integrity issue in Table 3 and the lack of statistical rigor, but do not produce a novel analytical insight about the method itself.

## Suggestions

1. **Correct Table 3 immediately.** Verify all entries in Table 3 by re-running the experiments. The duplicated rows strongly suggest copy-paste errors; the entire table needs re-verification.
2. **Add uncertainty quantification.** Report means and standard deviations from multiple calibration-data samples for all key comparisons, so the reader can assess whether the 0.5–0.8 pp margins are real.
3. **Add a "fine-tuned original" baseline.** Compare HFPrune against the original model fine-tuned on the same LaMini dataset, so the claim of "exceeding the original" is on equal footing.
4. **Strengthen the distributional evidence.** Report per-sample JS distances with paired statistical tests, or provide evidence that distributional preservation mediates accuracy improvements (e.g., by analyzing neurons where IE and CE importance rankings diverge).

## Score and Decision

The paper identifies a genuine limitation in CE-based Taylor pruning and proposes an elegant, efficient fix. The pruning-process efficiency advantage over SDMPrune is well-documented. However, the paper cannot be accepted in its current form due to a **fatal data integrity problem**: Table 3 contains rows identically duplicated across different model/pruning conditions, which is virtually impossible without a table-construction error. This casts doubt on the entire experimental corpus. Even setting aside this issue, the reported accuracy improvements are small (0.5–0.8 pp), no statistical significance is reported, and the core mechanistic claim (better distributional preservation) is only weakly supported by the evidence. The paper would need the data integrity issue resolved, proper uncertainty quantification added, and the "exceeds original model" claim properly contextualized to be considered for acceptance.

MY FINAL SCORE: <score>3</score>
MY FINAL DECISION: <decision>Reject</decision>