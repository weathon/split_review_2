Now let me write the final review.

## Summary

This paper proposes **NuSA-CL** (Null Space Adaptation for Continual Learning), a memory-free continual learning method for CLIP-style vision-language models. Before each new task, NuSA-CL performs SVD on the current weight matrices to identify low-energy (null-like) spectral directions, then constrains a LoRA-style low-rank update to remain strictly within those directions throughout training via a *persistent constraint* (freezing the null-space bases \(U_n, V_n\) and learning only a square intermediate matrix \(M\)). After training, the update is merged into the backbone, keeping a fixed parameter budget. The method is evaluated on the MTIL benchmark (11 datasets) and Class-Incremental CIFAR100, showing competitive performance with storage-based SOTA at a fraction of the cost.

## Strengths

- **Clean, well-executed core idea with clear differentiation from prior work.** The key insight—using SVD to identify the low-energy subspace and then enforcing a *persistent* constraint (not just initialization) on updates—is principled and clearly distinguished from MiLoRA (Wang et al., 2025), which uses the low-energy subspace only for initialization and then allows deviations. The ablation in Table 4a (unfreezing \(U_n, V_n\)) directly validates that the persistent constraint is essential.

- **Genuinely memory-free with a fixed parameter budget.** Unlike InflLoRA (which stores gradient projection memory), MoE-Adapters (growing routers), or DIKI (task statistics), NuSA-CL stores nothing between tasks after the merge, maintaining exactly 1.5M parameters throughout. This is a real architectural advantage with practical significance for resource-constrained deployment.

- **Efficiency numbers are concrete and well-documented.** Table 1 provides a clear, apples-to-apples comparison: NuSA-CL (1.5M params, 6.6 GB peak, 1.21 GPU-hours) vs MoE-Adapters (59.8M params, 15.5 GB, 3.42 GPU-hours) makes the efficiency case convincingly. The computation-memory-performance table format is informative.

- **Subspace selection ablation directly tests the central hypothesis.** Figure 3a compares *Tail* (null-like), *Top* (principal), and *Random* subspace selection across ranks 32–256. The result is monotonic and clear: *Tail* yields the lowest forgetting at every rank. This is the right ablation for the method's core claim.

- **Null-space dynamics analysis provides mechanistic evidence.** Figure 2 shows that NuSA-CL's effective rank and null ratio increase across tasks while LoRA and Full-FT remain static. This directly supports the claim that NuSA-CL accumulates knowledge in underutilized directions rather than overwriting principal components.

## Weaknesses

### Fatal

None.

### Major

1. **The theoretical analysis does not establish the claimed connection to forgetting.** Lemma 1 and Theorem 2 bound the Frobenius inner product \(\langle W_{t-1}, \Delta W_t\rangle_F\)—a *parameter-space* interference measure between *consecutive* weight matrices. Two issues prevent this from amounting to a forgetting guarantee:
   - **Function-level gap:** A small Frobenius inner product between weight matrices does not imply that predictions on past tasks' inputs remain unchanged. For overparameterized models, two weight matrices can have near-identical parameter-space inner products while producing arbitrarily different outputs.
   - **Composition gap:** Theorem 2 bounds \(\sum_{t=1}^T |\langle W_{t-1}, \Delta W_t\rangle_F|\)—interference between *consecutive* pairs only. Since the null space is recomputed from the current \(W_{t-1}\) each task (via SVD), the guarantee does not compose across the full trajectory from \(W_0\) to \(W_T\). Directions that were in the null space for task 1 could shift into the principal space of the recomputed SVD at task 5.
   
   The paper acknowledges this limitation in §4.2 ("local stability condition rather than a full function-level guarantee"), but the surrounding language (e.g., "provides a principled mechanism for mitigating catastrophic forgetting" in the theorem statement, line 120) overstates what is actually proven. The empirical results remain valuable, but they carry the full evidentiary burden.

2. **No error bars, confidence intervals, or statistical significance anywhere.** Every result in Tables 1–4 is reported as a single point without variance estimates. For a continual learning benchmark with 11 datasets, the training pipeline involves stochastic elements (SVD of evolving weights, sequential learning dynamics, few-shot sample selection in Table 2). The 5-shot results (Table 2) are especially vulnerable to sampling variance. Without variance information, the reader cannot determine whether improvements such as NuSA-CL vs InflLoRA on 5-shot Transfer (68.1 vs 66.8) or Avg (70.3 vs 68.9) are systematic or within noise. This is a standard expectation for empirical ML papers.

### Minor

3. **The evaluation protocol for the MTIL benchmark is not fully specified.** The paper describes the benchmark as "Multimodal Task Incremental Learning (MTIL)" and reports Transfer, Avg, and Last across 11 diverse datasets, but does not explicitly state whether evaluation is task-aware (the model knows which dataset's class set to use) or task-agnostic. This distinction matters for interpreting the results. Given the benchmark involves different datasets as separate "tasks," task-aware evaluation is likely, but the paper should state this explicitly alongside the CIFAR100 protocol specification.

4. **Conceptual concern about null space recomposition across tasks.** Since the SVD is recomputed on merged weights \(W_t = W_{t-1} + \Delta W_t\) at each task boundary, the null space basis for task \(t+1\) differs from that of task \(t\). An update confined to task \(t+1\)'s null space could, in principle, alter directions that were principal for an earlier task's null-space update. The paper provides empirical evidence that this does not cause problems in practice (§6.1 shows null space remains available even after 50 tasks on CIFAR100, and Appendix Tables 11–12 show spectral stability), but the concern is not addressed theoretically.

### Trivial

None.

## Nice-to-Haves

- **Per-task forgetting curves would strengthen the mechanistic claims.** Instead of (or in addition to) the parameter-space inner product bound, a plot showing how accuracy on each earlier task evolves as later tasks are learned would directly connect the null-space mechanism to its functional effect. The "Last" metric is a single aggregate; per-task retention curves would be more informative.
- The formulation \(\Delta W = U_n M V_n^\top\) with \(M \in \mathbb{R}^{r\times r}\) (a square matrix, not two rectangular LoRA factors) is a genuine structural difference from standard LoRA that could be highlighted more prominently in §3.2—it yields a roughly 12× reduction in trainable parameters per layer compared to standard LoRA at the same rank, which is independently interesting.

## Removed Points

- **CIFAR100 protocol underspecified (from critic's Critical Issue 3):** The paper explicitly states "Class-Incremental CIFAR100 benchmark" (lines 128, 196) and CLIP's 65.92% zero-shot accuracy on CIFAR100 is standard for ViT-B/16. The critic's confusion about whether this is task-incremental or class-incremental is not a valid weakness—the paper clearly specifies the protocol. **Removed** (factually incorrect criticism).

- **Missing hyperparameters (learning rate, optimizer, batch size, etc.):** The paper's appendix (standard location for such details) is stripped by the parser. The hard rule removes nitpicks about missing implementation details that would normally appear in the appendix. **Removed** per hard rule.

- **ZSCL GPU-hours comparison is "extreme":** The critic speculates that ZSCL's 47.24 GPU-hours "may reflect implementation differences rather than a fundamental property of the method." This is speculative and not a concrete weakness of the paper's method or claims. **Removed**.

- **"40x fewer parameters" comparison is selective:** The critic notes that DIKI (1.8M params) is only 0.3M more than NuSA-CL (1.5M). This is an observation, not a weakness—the paper also uses DIKI as a baseline with its own metrics, and the 40× claim is specifically against MoE-Adapters, which is correctly stated. **Removed** (not a weakness).

- **Missing related work:** Not raised by the critic; not included.

## Novel Insights

None beyond the paper's own contributions. The critic's analysis surfaces two well-defined issues (theory gap, missing error bars) that are orthogonal to the paper's contribution and do not synthesize a novel observation beyond what the paper provides.

## Suggestions

- Add standard deviations over at least 3 random seeds to the main results (Tables 1–3) and the 5-shot results (Table 2).
- Re-frame the theoretical section as providing *motivation* and *intuition* rather than a *guarantee* against forgetting. The current language (especially line 120: "provides a principled mechanism for mitigating catastrophic forgetting") should be tempered to reflect the acknowledged parameter-space limitation.
- Explicitly state the evaluation protocol (task-aware vs task-agnostic) for the MTIL benchmark in §5.1.

## Score and Decision

<score>6.5</score>
<decision>Accept</decision>