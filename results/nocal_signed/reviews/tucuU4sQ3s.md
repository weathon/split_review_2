The scoring model confirms what my analysis found. Let me now write the final review.

---

## Summary

This paper proposes **NuSA-CL**, a memory-free continual learning framework for vision-language models (VLMs). For each new task, it uses SVD to identify a low-energy ("null") spectral subspace of the current weights, then persistently constrains a LoRA-style update to lie within that subspace throughout training. After training, the update is merged into the backbone, keeping the parameter count fixed. The method requires no replay buffer, no gradient memory bank, and no growing module library. Experiments on the 11-dataset MTIL benchmark and CIFAR-100 class-incremental splits show that NuSA-CL outperforms other storage-free PEFT methods (LoRA, MiLoRA) by substantial margins and approaches the performance of storage-based SOTA methods (MoE-Adapters, DIKI) at a fraction of the resource cost.

## Strengths

- **Clean, principled method design.** The paper identifies a genuine scalability limitation of existing CL methods — reliance on growing storage or parameters — and proposes a direct solution: persistent constraint of updates to the low-energy subspace. The three-step cycle (SVD → constrained LoRA → merge) is conceptually simple. The ablation in Table 4a directly validates the persistent constraint design: unfreezing the null-space bases drops Last accuracy from 82.79 to 77.32.

- **Strong efficiency-performance tradeoff on the primary benchmark (Table 1).** NuSA-CL uses 1.5M parameters (vs. 59.8M for MoE-Adapters), zero external storage, 6.6 GB peak GPU memory, and 1.21 GPU-hours, while achieving Transfer=68.6, Avg=75.1, Last=82.8 — close to storage-based SOTA (MoE-Adapters: 68.9/76.7/85.0) at a fraction of the resource footprint.

- **Principled ablation of subspace choice (Figure 3a).** The comparison of Tail, Top, and Random subspace selection across five ranks (32–256) consistently shows the low-energy null-like subspace yielding the lowest forgetting at every rank. This rules out the alternative hypothesis that any low-rank projection would work similarly and is the paper's cleanest empirical evidence for its central claim.

- **Honest treatment of the theoretical limitation (Section 4.2).** The paper explicitly acknowledges that the interference bounds are in parameter space, not function space, and frames them as a local stability condition rather than a full guarantee, with tighter function-level bounds noted as future work.

## Weaknesses

### Fatal
None.

### Major

- **No statistical uncertainty reported for any experiment.** Every quantitative result in Tables 1, 2, 3, and 4 is reported as a single number with no standard deviation, confidence interval, or mention of the number of seeds/runs. A grep of the paper for "seed", "variance", "standard deviation", "std", and "trial" returns zero matches. This makes it impossible to assess whether reported margins are significant. For example, NuSA-CL's Last (82.8) is 0.8% below InflORA (83.6) — without variance estimates the reader cannot tell whether this gap is meaningful or noise. The claimed 4.4% improvement over ZSCL on CIFAR-100 50-step could be robust but cannot be evaluated. This is the single largest gap and must be addressed.

### Minor

- **Zero-shot CLIP baseline absent from the main full-shot results (Table 1).** The paper's framing emphasizes "preserving zero-shot capabilities," and the abstract claims the method "effectively preserves zero-shot transfer capabilities." Table 2 (5-shot) includes the zero-shot CLIP row (65.3 Transfer), but Table 1 does not include any CLIP baseline row. Without the initial CLIP Transfer score, the reader cannot assess what "preserving" means quantitatively in the full-shot setting.

- **The theoretical analysis overstates its explanatory role.** Lemma 1 and Theorem 2 bound parameter-space interference (Frobenius inner product), but catastrophic forgetting is a function-space phenomenon. The paper acknowledges this gap (Section 4.2: "local stability condition rather than a full function-level guarantee"), but the narrative preceding this caveat frames the bound as providing "a principled mechanism for mitigating catastrophic forgetting" (line 120). The conceptual leap from parameter-space boundedness to forgetting reduction is asserted rather than demonstrated; the theory serves more as a motivation than a rigorous explanation.

- **Unclear CIFAR-100 baseline implementations (Table 3).** It is unclear whether ICaRL and LwF are re-implemented on the CLIP backbone or use their original architectures. The table header states that † marks re-implemented methods, but ICaRL and LwF lack this marker. Since the paper otherwise standardizes on CLIP ViT-B/16 for all experiments, this ambiguity affects the fairness assessment of the CIFAR-100 comparison.

### Trivial

- **Naming inconsistency:** The method from Liang & Li (2024) appears as "InflLoRA" (lines 50, 192, 194), "InflORA" (Tables 1–2, line 169), and "InLoRA" (Table 4b, line 284). The correct name per the cited paper is InflLoRA.

## Nice-to-Haves

- Include PEFT baselines (e.g., LoRA, MiLoRA) on the CIFAR-100 benchmark alongside the traditional CL methods, since the paper's focus is PEFT-based CL for VLMs.
- Analyze sensitivity to task order (acknowledged as future work; a small experiment with a few random orders on a subset of datasets would strengthen the paper).

## Removed Points

- **Missing training hyperparameters (learning rate, optimizer, batch size, epochs):** The parser strips appendix content from all papers; these details exist in the original submission and cannot be verified as absent.
- **Speculative concerns about confounders or proxy effects not anchored to specific paper content.**
- **Criticism of the theory as unacknowledged:** The paper does acknowledge the parameter-space vs. function-space limitation (Section 4.2), so this concern was reduced to a Minor framing issue rather than a structural flaw.

## Novel Insights

The convergence of review signals highlights a clear pattern: the paper's strongest evidence comes from the subspace ablation (Figure 3a), which cleanly demonstrates that low-energy subspaces minimize forgetting across all ranks, independently of hyperparameter choices. This is more compelling than the theoretical bound alone. The weakest link is the gap between parameter-space bounds and the forgetting claim — the paper acknowledges this honestly but then relies on the bound in its narrative. The missing variance estimates are the single most impactful fix; without them, the reader cannot evaluate whether the reported margins (especially the smaller ones against storage-based methods) are significant.

## Suggestions

1. **Add multi-seed variance estimates** (standard deviations over at least 3 seeds) to all main results tables. This is the single highest-priority improvement and addresses the most consequential weakness.
2. **Include the zero-shot CLIP baseline row in Table 1** so the Transfer metric can be directly assessed against the initial model, directly supporting the paper's "preserving zero-shot capabilities" claim.
3. **Clarify whether ICaRL and LwF in Table 3** use the CLIP backbone or their original architectures.
4. **Standardize the citation name** for Liang & Li (2024) to "InflLoRA" throughout.

## Score and Decision

MY FINAL SCORE: <score>7.0</score>
MY FINAL DECISION: <decision>Accept</decision>