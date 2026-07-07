## Summary

This paper proposes HFPrune, a structured pruning method for LLMs that replaces the standard cross-entropy (CE) loss with the information entropy of the output distribution as the criterion for Taylor-based importance scoring. The key motivation is that CE focuses importance on a single ground-truth token while entropy captures the full output distribution. The method is label-free, avoids the computational overhead of self-distillation approaches, and prunes only MLP modules. Experiments on LLaMA-2-7B, LLaMA3.2, and Qwen models show consistent improvements over existing structured pruning methods.

## Strengths

1. **Simple, well-motivated idea with a clean formulation.** Replacing CE with information entropy for Taylor-based importance scoring is conceptually clear and straightforward to implement (Algorithm 1). The paper correctly identifies that CE focuses on a single token while entropy depends on the full output distribution, and the derivations in Eqs. (2)–(4) are correct.

2. **Clear practical advantage over self-distillation methods.** Table 5 convincingly demonstrates that HFPrune is ~3× faster and uses ~31% less peak GPU memory than SDMPrune (e.g., 508.9s vs. 1539.8s on LLaMA2-7B). This is a genuine practical benefit rooted in avoiding a separate teacher model.

3. **Label-free importance scoring.** Unlike CE-based Taylor pruning, the entropy criterion does not require ground-truth next-token labels in the calibration data, which is a genuine methodological advantage.

## Weaknesses

### Major

1. **Data integrity issue in Table 3 (Qwen experiments).** Four rows in Table 3 contain *exactly identical* numbers across all 10 benchmarks and averages—a pattern that cannot arise from normal experimental variation:

   | Affected Row | Identical To |
   |---|---|
   | Qwen2.5-1.5B 20% SDMPrune | Qwen2.5-7B 40% SDMPrune |
   | Qwen2.5-1.5B 20% HFPrune (ours) | Qwen2.5-7B 40% HFPrune (ours) |
   | Qwen3-1.7B 20% SDMPrune | Qwen2.5-1.5B 40% SDMPrune |
   | Qwen3-1.7B 20% HFPrune (ours) | Qwen2.5-1.5B 40% HFPrune (ours) |

   Every single benchmark score, without exception, is duplicated across these rows that should represent different models at different pruning ratios. Additionally, the Qwen2.5-7B 30% SDMPrune row is missing its average. These appear to be copy-paste errors in table construction. The affected rows (4 of 18 in Table 3) cannot be trusted as reported. Since the paper claims "consistently outperforms existing methods across the ... Qwen series," this undermines a significant portion of the experimental evidence. The authors must correct and re-verify all Qwen results.

2. **Small performance margins with no variance reporting—the core advantage over baselines is thin.** The paper's best-case improvement over SDMPrune is **0.5–0.8 percentage points** on average accuracy (Tables 1, 6). Without fine-tuning (Table 6, the cleanest test of the pruning criterion), the gap is only **0.5 points** (IE 53.1 vs. CE 52.6 at 20%). No standard deviations, confidence intervals, or multi-run statistics are reported for any result. Given the tiny margins, it is impossible to assess whether these improvements are systematic or within measurement noise. This limits the strength of the paper's central claim that entropy provides "fundamentally more accurate measures of neuron importance."

3. **The headline result ("exceeds the original model") is driven primarily by fine-tuning, not the pruning criterion.** The paper prominently claims that at 20% pruning on LLaMA2-7B, the pruned model achieves 59.0 vs. the original 58.3. However, without fine-tuning (Table 6), IE achieves only 53.1—well below the original 58.3—and outperforms CE by just 0.5 points. The paper lacks a critical control: fine-tuning the original unpruned model under the same protocol (LaMini, LoRA, 2 epochs) to separate the recovery effect of fine-tuning from the effect of the pruning criterion. Without this, the claim of "exceeding" is overstated and conflates two separate mechanisms.

4. **Missing comparison against widely-used pruning baselines.** The paper mentions Wanda, SparseGPT, and FLAP in the related work but never compares against them experimentally. SparseGPT is a standard reference in LLM pruning. While these are primarily unstructured methods and a direct comparison is not fully apples-to-apples, the paper should at minimum acknowledge this gap and provide comparison on a common metric (e.g., perplexity at comparable sparsity levels). The omission is particularly problematic given the small absolute margins over the existing structured-pruning baseline.

### Minor

1. **Characterization of SDMPrune's zero-gradient issue is insufficiently justified.** The paper states (line 68) that SDMPrune suffers from a "critical defect, where the initial distillation loss is zero, leaving no gradient to guide the initial importance scoring." If the loss is truly zero initially, SDMPrune would fail to produce any importance scores. The paper does not explain how SDMPrune circumvents this or cite evidence. Either the paper is mischaracterizing SDMPrune or SDMPrune uses a warm-up mechanism that should be described. A more careful explanation or reference is needed.

2. **Entropy is a scalar statistic that discards distributional structure.** Two very different distributions can have identical entropy. The paper treats minimizing Δentropy as a proxy for preserving the full output distribution but does not discuss this gap. Table 7 shows the difference in JS distance is tiny (0.241 vs. 0.243 at 20% sparsity), with no variance reported, making it unclear whether the distribution-preservation claim is meaningfully supported.

### Trivial

None.

## Nice-to-Haves

- Evaluate on tasks that depend on the *tail* of the output distribution (e.g., open-ended generation, translation, summarization) where IE's claimed advantage over CE would be most apparent, rather than only classification-style multiple-choice benchmarks.
- Report perplexity on held-out validation sets (WikiText-2, C4) as a cleaner aggregate measure of distribution preservation.
- Add an ablation with per-layer adaptive pruning ratios based on layer-specific entropy sensitivity.

## Removed Points

**These points are flagged to be removed; treat them with caution.**

- *Criticism about missing appendix/deferred proofs*: The parser strips these sections from all papers; they exist in the original submission. **Removed by rule.**
- *Criticism about the Qwen results being "entirely invalidated"*: The duplication affects 4 of 18 rows, not all Qwen experiments. Qwen2.5-7B results at all ratios and Qwen2.5-1.5B/Qwen3-1.7B at 30% and 40% appear structurally plausible. The original claim was overbroad. **Softened to affect "affected rows."**
- *Criticism about LoRAP having missing benchmark values making averages incomplete*: Using only available benchmarks for averages is standard practice. **Removed as not a genuine weakness.**
- *"The paper is clearly written" strength*: Generic. **Moved here.**

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. **Fix Table 3.** Re-run the Qwen2.5-1.5B at 20% and Qwen3-1.7B at 20% experiments, and correct the missing average for Qwen2.5-7B 30% SDMPrune. Report corrected numbers and explain how the error occurred.
2. **Add the missing fine-tuning control.** Fine-tune the original unpruned LLaMA2-7B on LaMini with LoRA for 2 epochs and report its zero-shot accuracy. This is essential to separate the effect of fine-tuning from the pruning criterion.
3. **Report variance.** Repeat key experiments (at least Tables 1 and 6) across 3–5 random seeds and report standard deviations. Given the 0.5–0.8 point margins, this is necessary to establish that the improvements are systematic.
4. **Address the zero-gradient characterization of SDMPrune.** Either cite the original paper showing how it handles this or correct the claim.
5. **Compare against Wanda and SparseGPT** on perplexity (WikiText-2, C4) at comparable effective sparsity levels, even if structural differences require careful contextualization.

## Score and Decision

### Calibration Summary

| Anchor Paper | Avg Score | Round | Itemized? | Comparison |
|---|---|---|---|---|
| Compresso: Structured Pruning (storaged) | 5.25 | R1 | No | More comprehensive experiments but had inference-cost fairness issues; our paper is weaker due to data integrity problem |
| AggregationPruner (ji6MYm4Htg) | 4.80 | R2 | Yes | Similar missing-baseline issue; our paper has cleaner motivation but adds a data-integrity concern |
| PGZ: Pushing Gradient towards Zero (IU4L7wiwxw) | 4.50 | R1 | Yes | Similar profile (marginal improvements, missing baselines like Wanda); our paper additionally has data integrity issue |
| Rethinking Heterogeneous Sublayers (qG1S5eXMzx) | 3.50 | R2 | No | Similar structured-LLM-pruning paper; rejected for comparable concerns |
| NEPENTHE Entropy Pruning (fk5ePN7YCS) | 3.75 | R2 | No | Entropy-based pruning, limited evaluation; our paper evaluates more thoroughly but has data integrity concerns |
| HENP Dynamic Pruning (g4VGwNqzpB) | 3.00 | R1 | Yes | Entropy-based pruning on smaller models; our paper is stronger in scope and evaluation |

**Bracketing (Round 1):** The paper sits below Compresso (5.25) and PGZ (4.50) due to the verifiable data integrity issue, and above HENP (3.00) due to cleaner formulation and broader evaluation. Initial bracket: **3.0–4.5**.

**Narrowing (Round 2):** The closest comparable anchors are Rethinking Heterogeneous Sublayers (3.50) and NEPENTHE (3.75), both rejected papers with partial strengths and identifiable weaknesses. Our paper shares their profile: a sound idea with modest empirical support and a concrete presentation error. Weighted-item comparison against PGZ (4.50): PGZ had marginal improvements but no table errors. Against HENP (3.00): HENP had limited scope and unclear writing; our paper is stronger on those dimensions. The data integrity issue tips the balance below 4.0 but the genuine efficiency advantage (Table 5) and clean formulation keep it above 3.0. Final: **3.5**.

The paper has a genuinely interesting idea and a clear practical advantage in pruning efficiency over self-distillation baselines. However, the verifiable data duplication in Table 3 (4 of 18 rows with identical numbers across different model/pruning-ratio combinations) is a serious presentation error that undermines trust in the experimental reporting. Even setting this aside, the core accuracy improvement over the strongest baseline (SDMPrune) is only 0.5–0.8 points with no variance reported, and the headline claim of exceeding the original model is largely attributable to fine-tuning rather than the pruning criterion. The missing comparison against widely-used baselines (Wanda, SparseGPT) further limits the evidence.

The decision is **Reject**. The paper cannot be accepted in its current form due to the data integrity issue. If the authors correct Table 3, add the missing fine-tuning control, report variance, and strengthen the distribution-preservation evidence (e.g., perplexity, generation tasks), the paper could become viable for a future venue.

MY FINAL SCORE: <score>3.5</score>
MY FINAL DECISION: <decision>Reject</decision>