## Summary

This paper proposes LoLoRA, a hybrid fine-tuning method for LoRA adapters that combines local unsupervised (forward-pass) updates for the A matrix with gradient-based backpropagation for the B matrix. The paper also provides a theoretical analysis (Theorem 4.4) proving that under a random-target assumption, the optimal initialization of A is any nonsingular transformation of the first *r* eigenvectors of the input covariance matrix — formally grounding the empirical success of PCA-based initialization (EVA, Paischer et al., 2024). Experiments compare LoLoRA against LoRA, LoRA-FA (frozen A), and LoRA-FA with EVA initialization across GLUE, math reasoning, multimodal, and ablation settings.

## Strengths

1. **Theoretical result (Theorem 4.4, §4).** The paper proves that under a random-target assumption, optimal A reduces to a nonsingular transformation of the first *r* eigenvectors of the input covariance matrix. This provides formal justification for the empirical observation in EVA (Paischer et al., 2024) that PCA-initialized A outperforms random initialization. The proof connects a concrete optimization criterion to the principal subspace — a clean and nontrivial result.

2. **Thorough ablation of local learning rules (Table 6, §5.4).** The paper systematically benchmarks five local update rules (HPCA with/without centering, HPCA with SVD-first initialization, autoencoder loss, SoftHebb) across ranks 2, 4, 8. This is useful for practitioners and shows the expected convergence: methods that track the PCA subspace perform similarly, while SoftHebb clearly does not.

3. **Clear conceptual framing of the A/B asymmetry.** The paper correctly identifies that A's role is primarily about capturing the input's intrinsic subspace structure while B handles task-specific adaptation, and the hybrid design follows naturally from this insight.

## Weaknesses

### Fatal
None.

### Major

1. **LoLoRA does not empirically outperform the simpler LoRA-FA (EVA) baseline it is designed to improve upon.** Across every experiment reported, LoLoRA is indistinguishable from LoRA-FA with EVA initialization — which is simpler (no online updates, no extra optimizer state for A):

   | Setting | LoLoRA HPCA | LoRA-FA (EVA) |
   |---|---|---|
   | GLUE (CoLA) | 66.3 | 64.7 |
   | GLUE (RTE) | 84.6 | 83.6 |
   | GLUE (MRPC) | 89.9 | 90.0 |
   | GLUE (STS-B) | 92.0 | 91.9 |
   | GLUE (MNLI) | 90.3 | 90.4 |
   | GLUE (QNLI) | 94.7 | 94.5 |
   | GLUE (QQP) | 90.6 | 90.6 |
   | GLUE (SST-2) | 96.4 | 96.3 |
   | Math (GSM8K, Table 3) | 0.829 | 0.829 |
   | LLaVA PPL (Table 4) | 2.93 | 2.92 |
   | TinyLlama r=8 PPL (Tables 5-6) | 2.535 | 2.536 |

   On every single metric the two methods overlap within one standard error. The paper's conclusion that "HPCA consistently outperforms standard LoRA-FA" refers to LoRA-FA *with uniform initialization*, not LoRA-FA with EVA initialization — but EVA initialization achieves the same theoretical optimum characterized by Theorem 4.4. The paper provides no evidence that *online adaptation* of A (the core novel mechanism of LoLoRA) provides any benefit over *static PCA initialization* of A. This undermines the central claim that the method's dynamic adaptation matters empirically.

2. **Memory advantage over LoRA-FA (EVA) is slightly negative.** In Table 4 (LLaVA), LoLoRA uses **24.1 GB** vs. LoRA-FA's **23.9 GB**. The paper acknowledges the extra optimizer state in §6, but this means that in settings where memory is the binding constraint, a practitioner would strictly prefer LoRA-FA (EVA) — it is both simpler and more memory-efficient. The method's main practical advantage (no separate PCA pre-training pass) is a convenience feature, not a memory or quality advantage.

### Minor

3. **The theoretical framing (§4) uses an uninformative prior that could be better discussed.** Assumption 4.1 models ΔW₀ as i.i.d. Gaussian — a mathematical device to derive optimal A under an unknown target. The paper does not discuss the gap between this assumption and realistic fine-tuning settings where ΔW is low-rank and structured. While using an uninformative prior is a standard technique (average-case analysis), the paper would benefit from explicitly addressing how well conclusions under this assumption transfer.

4. **The abstract's claim of "comparable performance" to standard LoRA is imprecise.** On GLUE, LoLoRA underperforms standard LoRA on 7 out of 8 tasks (e.g., CoLA: 66.3 vs. 69.6; QQP: 90.6 vs. 91.7). On LLaVA, perplexity is 2.93 vs. 2.90. The differences are small on several tasks but systematic, and the claim should be more carefully qualified.

5. **The LLaVA experiment (§5.3) uses a 20% subset of the Visual Instruct 150K dataset with validation on the deferred portion of the same instruction/image pool.** As the paper transparently notes, this means the validation distribution closely matches training, which limits the conclusions to training-set fit rather than generalization. The results should be interpreted with this caveat in mind.

### Trivial
- §5.1 describes LoLoRA as achieving "slightly better results than LoRA-FA (EVA)"; looking at Tables 1-2, LoLoRA leads on 5/8 tasks, trails on 1, and ties on 2 — all within one standard error. Calling this "slightly better" overstates what is effectively a statistical tie.

## Nice-to-Haves

- A comparison to gradient checkpointing (a standard baseline for reducing activation memory) would help contextualize LoLoRA's memory savings within the broader landscape of memory-efficient training.
- A runtime throughput comparison (samples/second) across methods would clarify where LoLoRA's per-step HPCA computation overhead falls relative to saved backward passes.
- The paper would be strengthened by identifying at least one setting where *online adaptation of A* matters — e.g., non-stationary data streams or multi-task continual learning — where a static PCA pass cannot anticipate future distribution shifts. Without such evidence, the method's iterative adaptation remains a theoretical possibility without demonstrated practical impact.

## Removed Points

- *Criticism about §4's notation (𝔼_{½})*: This is a parser formatting artifact, not an author error.
- *Criticism about "best checkpoint selection" (§5.2) inflating results*: The paper transparently states this practice applies to all methods equally, so inter-method comparisons remain valid. Moreover, the standard practice on small-benchmark GLUE tasks is heterogeneous across the literature.
- *Criticism about missing gradient checkpointing baseline (§3.3)*: Reduced to Nice-to-Have — the paper's scope is LoRA-variant comparisons, not exhaustive memory-saving techniques.
- *Criticism framed as "Assumption 4.1 contradicts LoRA's premise"*: Reduced to Minor — the random-target assumption is a standard uninformative-prior modeling device, not a claim about the actual structure of ΔW. The retained version reflects the actual gap in the paper (lack of discussion about transferability), not the stronger assertion that the assumption is invalid.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

- Reframe the paper's contributions to separate the theoretical result (Theorem 4.4, which stands on its own) from the method claim. The PCA-based initialization theory is the paper's strongest contribution and need not depend on LoLoRA outperforming LoRA-FA (EVA).
- If the online adaptation claim is to be preserved, design a controlled experiment (e.g., non-stationary input distributions, sequential task fine-tuning) where a one-time PCA pass is provably insufficient and LoLoRA recovers performance. Without this, the paper should acknowledge that LoLoRA is functionally equivalent to LoRA-FA (EVA) with a convenience advantage.
- Qualify the abstract's "comparable performance" claim with the specific task types where degradation is observed.

## Score and Decision

MY FINAL SCORE: <score>5</score>
MY FINAL DECISION: <decision>Reject</decision>