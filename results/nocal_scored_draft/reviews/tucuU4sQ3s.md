## Summary

This paper introduces NuSA-CL, a memory-free continual learning framework for vision-language models (CLIP). The method uses SVD to identify a low-energy ("null") subspace of each weight matrix, then constrains task-specific low-rank updates (via a learnable matrix M ∈ ℝ^{r×r}) to this subspace. Updates are merged into the backbone after each task, keeping a fixed parameter budget with no replay buffers, distillation, or growing module counts. Experiments on MTIL (11 tasks) and CIFAR-100 CIL (up to 50 steps) show competitive performance against storage-free baselines and efficiency advantages over storage-based methods.

## Strengths

- **The core idea is clean and well-motivated.** Confining task-specific updates to the low-energy subspace (identified via SVD of the current weights) is intuitive and principled. The three-stage cycle (SVD → constrained adaptation → merge) is simple, mathematically clear, and genuinely memory-free — no replay buffers, distillation, or growing parameter counts (Section 3, Figure 1).

- **Efficiency gains are concrete and quantified:** 1.5M trainable parameters vs. 15.7M for LoRA, <1 min SVD initialization vs. ~81 min for InflLoRA, 1.21 GPU-hours vs. 47.24 for ZSCL (Table 1). These are meaningful for resource-constrained deployment.

- **The ablation on subspace selection (Tail vs. Top vs. Random, Figure 3a) directly validates the paper's central premise:** the low-energy (tail) subspace consistently yields the lowest forgetting across all tested ranks. The persistent-constraint ablation (Table 4a) further confirms that freezing the null-space bases is critical.

- **The analysis of null-space dynamics (Figure 2) provides mechanistic insight** beyond final accuracy numbers — showing that effective rank increases across tasks for NuSA-CL while staying static for LoRA and Full-FT gives a concrete picture of knowledge accumulation rather than overwriting.

## Weaknesses

### Fatal
None.

### Major

- **Missing ablation: standard LoRA with matched parameter count.** The paper compares NuSA-CL (1.5M trainable parameters, M∈ℝ^{r×r} at r=128) against LoRA at 15.7M parameters (two projection matrices at r=128) — a ~10× difference. Without a LoRA baseline with matched parameter count (r≈10, ~1.2M params), the reader cannot fully attribute the performance gains to the null-space constraint rather than simply having fewer trainable parameters. The subspace selection ablation (Figure 3a) and persistent constraint ablation (Table 4a) provide partial independent support, but a direct matched-parameter comparison is the cleanest test and is missing. This is the single most impactful experiment the authors should add.

### Minor

- **The theoretical analysis (Section 4) bounds interference only in parameter space (Frobenius inner product between W and ΔW), not in function space.** Catastrophic forgetting is a function-level phenomenon: weight updates with small Frobenius inner product can still cause large output changes on past-task data. The paper acknowledges this caveat (Section 4.2: "should be viewed as a local stability condition rather than a full function-level guarantee"), but the framing — "principled mechanism for mitigating catastrophic forgetting" — overstates what the parameter-space bound actually delivers. The theory serves as useful motivation but does not provide a forgetting guarantee.

- **The "null space" terminology, while qualified in-text as "approximate" or "intrinsic," is not strictly accurate** — the method uses the low-energy subspace (small but non-zero singular values), not the true null space (zero singular values). The paper's own ablation (Figure 3a) shows that forgetting increases with rank, which is consistent with the fact that larger ranks include higher-energy directions that cause more interference — exactly the behavior expected from a "low-energy, not null" subspace. The title uses "Null Space Adaptation" without qualification.

### Trivial

- The method section (Section 3) refers generically to "a weight matrix from the model" but does not specify which layers are adapted. The detail that only attention projection matrices (W_q, W_k, W_v, W_o) are used appears only in Section 6.3; MLP layers are not mentioned. This should be stated explicitly in Section 3.

## Nice-to-Haves

- Per-task forgetting curves (accuracy on early tasks as later tasks are learned) would make the forgetting comparison more transparent.
- A brief experiment on ViT-L/14 would strengthen the claim of generality to larger backbones.
- A simple task-order shuffling experiment on MTIL would address a known concern in continual learning.

## Removed Points
These points are flagged to be removed; treat them with caution:
- "No results on larger backbones" — removed as scope creep; the paper focuses on ViT-B/16 and discusses scalability in Section 6.3.
- "Task-order sensitivity is not addressed" — removed; the paper acknowledges this as future work (Section 7).
- "The persistent constraint ablation is insufficient" — removed; the paper already ablates this in Table 4a.
- "No per-task forgetting curves" — removed; this is a nice-to-have enhancement, not a weakness.
- "Transfer metric definition is ambiguous" — removed; the definition "zero-shot accuracy on unseen tasks" (Section 5.1) is clear enough given the experimental setup.
- "InflLoRA has higher Last accuracy" — removed; this is a factual observation, not a weakness. The paper correctly places InflLoRA in the storage-based category and claims SOTA only within the storage-free setting.
- The speculation "if LoRA with r=10 matches NuSA-CL's performance" — removed from the weakness statement; only the fact that the experiment is missing is retained.

## Novel Insights

The most insightful observation from the reviews is that the spectral dynamics analysis (Figure 2) shows changes of only ~1% in effective rank over 10 tasks. The paper describes this as a "clear and consistent increase," which is technically true, but the tiny magnitude raises an interesting question: if the null space barely shrinks even after many tasks, how aggressively is the method actually using the available capacity? The paper partially addresses this by noting that 313.58 null directions remain in the most saturated layer after 10 tasks (>2× the update rank), but the gap between the small effective-rank change and the strong performance results merits further probing.

## Suggestions

- **Highest priority:** Add a LoRA baseline with matched parameter count (~1.5M params, r≈10) on the MTIL benchmark. This single experiment would cleanly resolve whether the null-space constraint or simply the lower parameter count drives the gains.
- Either strengthen the theory to function-level bounds under Lipschitz smoothness assumptions, or reframe Section 4 explicitly as a "heuristic motivation" rather than implying a forgetting guarantee from a parameter-space bound.
- State explicitly which layers are adapted (attention only, or attention + MLP) in the Method section (Section 3) rather than deferring to Section 6.3.

## Score and Decision

MY FINAL SCORE: <score>7.0</score>
MY FINAL DECISION: <decision>Accept</decision>