Now let me write the final review with all calibration incorporated.

## Summary

NuSA-CL proposes a memory-free continual learning method for vision-language models (CLIP). The key idea is to identify the approximate null space (low-energy subspace) of each weight matrix via SVD before each task, persistently constrain all low-rank updates to this null space during training, and merge the update back into the backbone. This cycle repeats across tasks with zero parameter growth, no replay buffers, and no knowledge distillation. The method is well-specified, cleanly motivated, and empirically strong.

## Strengths

1. **Clean and principled method.** The null-space identification via SVD (Eqs. 1–2), the reparameterization ΔW = U_n M V_n^T (Eq. 3) that mathematically guarantees orthogonality to the principal subspace, and the update-and-merge cycle (Eq. 4) are fully specified and grounded in a clear intuition. The distinction from prior SVD-guided methods that use the null-like subspace only for initialization (Section 2.3) is clearly drawn and experimentally validated (Table 4a — unfreezing U_n, V_n drops Last from 82.79→77.32).

2. **Genuinely memory-free with zero parameter growth.** The method maintains a fixed parameter budget across all tasks — no replay buffers, no expanding routers, no task-specific statistics. This is a real architectural advantage demonstrated quantitatively in Table 1 (1.5M parameters, no additional storage vs. MoE-Adapters at 59.8M parameters + expanding routers, vs. DIKI at 1.8M + 159MB task stats).

3. **Strong empirical results in the storage-free regime.** On the MTIL benchmark (Table 1), NuSA-CL outperforms other storage-free methods (LoRA, MiLoRA, Continual-FT) by substantial margins — Transfer 68.6 vs. 63.9 (LoRA), Avg 75.1 vs. 70.1, Last 82.8 vs. 79.9. It also achieves performance close to far more expensive storage-based methods (e.g., MoE-Adapters at 85.0 Last vs. 82.8 for NuSA-CL) with 40× fewer parameters and ~3× less training time.

4. **The 50-step CIFAR-100 result (Table 3) is the strongest evidence for scalability.** NuSA-CL achieves 71.85% Last accuracy vs. ZSCL's 67.36% — a gap of 4.4 points that widens with sequence length (10 steps: 74.51 vs. 73.65; 50 steps: 71.85 vs. 67.36). This directly supports the claim that dynamic null-space recomputation prevents cumulative degradation.

5. **Well-designed ablations that validate the core claims.** The Tail vs. Top vs. Random subspace comparison (Fig. 3a) cleanly isolates the effect of the null-space choice across ranks. The persistent constraint ablation (Table 4a) confirms that unfreezing U_n, V_n causes a sharp performance drop, proving that the *persistence* of the constraint — not just initialization — is what matters. The robustness analysis across energy cutoff thresholds ρ (Table 4b) shows stable performance from 0.80 to 0.999.

## Weaknesses

### Fatal
None.

### Major

1. **Missing prompt-based storage-free baselines.** The paper positions itself against storage-free methods but evaluates only LoRA, MiLoRA, and Continual-FT within this category. Well-known prompt-based continual learning methods for vision transformers — L2P (Wang et al., CVPR 2022), DualPrompt (Wang et al., ECCV 2022), and CODA-Prompt (Smith et al., CVPR 2023) — are also storage-free (shared prompt pool with query-based selection, fixed parameter budget) and are directly relevant to the paper's core claim of being the best in the storage-free regime. The paper mentions prompt-based methods only in the related work section (line 44) but does not include them experimentally. Adding these would either strengthen the claim (if NuSA-CL still wins) or reveal its boundaries. This is the most significant gap in the evaluation. That said, these methods would require adaptation to the MTIL setting, so this is an addressable concern rather than a fatal one.

### Minor

2. **Theory provides weaker guarantees than the framing suggests.** Lemma 1 and Theorem 2 bound the Frobenius inner product ⟨W_{t-1}, ΔW_t⟩ — interference between a weight matrix and its immediate update. But catastrophic forgetting concerns interference with *all previous tasks'* knowledge, not just the immediately preceding weight state. After task 1, the update ΔW₁ is merged: W₁ = W₀ + ΔW₁. When task 2's update ΔW₂ is constrained to the null space of W₁, some knowledge from ΔW₁ may now reside in components of W₁ that are not in the top-k principal subspace. The paper does acknowledge this caveat (line 122: "stated in parameter space and should be viewed as a local stability condition rather than a full function-level guarantee"), but this qualification is absent from the stronger claims in the abstract and introduction ("This strategy minimizes interference with previously acquired knowledge"). The gap is between framing and evidence; the empirical results remain strong.

3. **The Transfer metric definition and its relation to "zero-shot preservation" needs clarification.** The paper defines Transfer as "the zero-shot accuracy on unseen tasks" (line 128) and later compares NuSA-CL's Transfer (68.6%) to the original CLIP zero-shot score of 65.3% (Table 2, first row). These are different quantities: CLIP zero-shot is a single evaluation on all 11 tasks, while Transfer aggregates accuracy on tasks at the time they are unseen (which depends on task ordering). The paper should clarify the exact aggregation protocol and report the task ordering to make the "zero-shot preservation" claim precise.

4. **Describing spectral changes as "clear and consistent increase" overstates the magnitude.** The effective rank increase reported in Figure 2 is very small in absolute terms (~51.8% to ~52.4% for the vision encoder). While the trend direction is meaningful and the more important finding — that the null space remains large (313.58 directions remaining after 10 tasks, as reported in line 220) — is well-supported, the language should match the scale of the observed change.

5. **No standard deviations or confidence intervals.** None of the tables report variance. The large margins between NuSA-CL and storage-free baselines in Table 1 (4–5 points) mitigate this concern, but some cells in Table 2 have smaller margins and the ablation results in Table 4 would benefit from variance estimates.

### Trivial

6. **Task ordering for the 11 MTIL datasets is not stated.** Since Transfer measures accuracy on "unseen" tasks and the evaluation depends on when each task is encountered, the ordering should be specified in the main text.

## Nice-to-Haves

- Adding a forward/backward transfer accuracy matrix (triangular heatmap showing accuracy on each task after each learning step) would directly visualize the forgetting dynamics and strengthen the paper's core claim.
- Clarifying whether full or truncated SVD is used in practice (Section 6.3 mentions "reduced SVD" but does not specify the algorithm), and quantifying the computational savings from truncation.

## Removed Points

- **Uneven SVD efficiency comparison (InLoRA vs. NuSA-CL):** The Harsh Critic flagged this as an apples-to-oranges comparison. However, the paper explicitly acknowledges this (lines 284–286), stating that InLoRA "requires heavy, data-dependent computations" while NuSA-CL's SVD is data-agnostic. The paper is transparent; this is an accurate description of a genuine advantage, not a misrepresentation.
- **No hyperparameter disclosure (LR, optimizer, batch size, etc.):** The appendix is stripped by the parser; these details are present in the original submission. Per filtering rules, this is not a valid criticism of the paper as submitted.
- **Speculative concerns about confounders or metric proxies not tied to specific sentences, equations, figures, or tables:** Removed per filtering rules.

## Novel Insights

None beyond the paper's own contributions. The reviews identify a missing baseline category (prompt-based methods) that the authors should address, and clarify the gap between the theoretical framing and the actual guarantees. Neither is a novel insight beyond what the paper already presents.

## Suggestions

- Add L2P, DualPrompt, and CODA-Prompt as storage-free baselines in the main comparison (Table 1).
- Clarify the Transfer metric aggregation protocol and report the exact task ordering for MTIL.
- Tone down the claim in Section 6.1 about "clear and consistent increase" in effective rank to match the small magnitude, or refocus the language on the more important finding that the null space remains large after many tasks.
- Report standard deviations or confidence intervals, at least for the main results.
- Include a forward/backward transfer accuracy matrix to make forgetting dynamics transparent.

## Calibration Anchors

All anchors retrieved from the calibration corpus:

| Path | Avg Score | Round | Comparison |
|------|-----------|-------|------------|
| JIlIYIHMuv.md (LVLM-CL) | 2.50 | R1 | CL for LVLMs with memory bank and poor presentation. NuSA-CL is far stronger. |
| sb7qHFYwBc.md (C-CLIP) | 6.50 | R1, R2 | CL for CLIP using LoRA+distillation. NuSA-CL is cleaner (no distillation), more memory-efficient, and has better ablations. |
| k9NYnsC4Mq.md (PROOF) | 5.67 | R1 | CL for VLMs with task-specific projections (parameter growth). Rejected due to inference mismatch. NuSA-CL is clearly stronger. |
| Hcb2cgPbMg.md (Spectral Regularization) | 6.25 | R2 | Spectral regularization (max singular value) for CL; marginal improvement concerns. NuSA-CL has stronger empirical evidence. |
| TLADT8Wrhn.md (TiC-CLIP) | 6.25 | R2 | Benchmark-focused CL for CLIP (time-continuous data). Different contribution type. |
| 7D9X2cFnt1.md (Elastic Feature Consolidation) | 7.00 | R2 | Exemplar-free CIL with feature drift regularization. Comparable quality; NuSA-CL has more novel weight-space approach. |
| ScI7IlKGdI.md (Spurious Forgetting) | 6.33 | R2 | Theoretical analysis of forgetting in LLMs. Different domain. |

**Round 1 Bracket:** 7.0–8.0. Based on comparisons with C-CLIP (6.50, Accept) and PROOF (5.67, Reject).

**Narrowing:** After reading the full reviews of C-CLIP (6.50), EFC (7.00), and Spectral Regularization (6.25), NuSA-CL is stronger than C-CLIP (cleaner method, no distillation, better ablations) and comparable to or slightly above EFC (more novel approach, similarly rigorous validation). The missing prompt-based baselines gap prevents it from reaching 8+.

**Final Score: 7.5.** The paper has a clean, principled method, strong empirical support, and genuine practical advantages (memory-free, zero parameter growth). The main weakness — missing prompt-based baselines — is significant but addressable. This score places it above comparable accepted CL-for-VLM papers (C-CLIP at 6.5) and in line with strong exemplar-free CL papers (EFC at 7.0).

MY FINAL SCORE: <score>7.5</score>
MY FINAL DECISION: <decision>Accept</decision>