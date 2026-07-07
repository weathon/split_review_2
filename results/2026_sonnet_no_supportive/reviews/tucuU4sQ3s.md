Now I have enough context to draft the review.Let me read two anchor papers for closer comparison.Now I have sufficient calibration data. Let me write the final review.

---

## Summary
NuSA-CL is a memory-free continual learning framework for CLIP-style vision-language models. It performs SVD on each weight matrix before each new task, constrains LoRA updates to the low-energy (tail singular) subspace via a persistent frozen basis (U_n, V_n) with a trainable intermediate matrix M, then merges updates into the backbone weights—maintaining a fixed parameter budget with zero replay, zero auxiliary models, and zero parameter growth. The method is evaluated on the MTIL benchmark (full-shot and 5-shot), CIFAR-100 class-incremental (10/20/50 steps), and supported by targeted ablations isolating the key design choices.

---

## Strengths
- **Genuinely memory-free, fixed-budget design with quantified efficiency.** The SVD → constrained adaptation → merge cycle requires zero replay buffers, zero auxiliary model storage, and zero parameter growth. Table 1 concretely documents: 1.5M effective parameters, <1 min SVD initialization vs. ~81 min for InflORA's data-dependent subspace computation, and 1.21 GPU-hours total training time at only 6.6 GB peak GPU memory.
- **Core ablations directly and cleanly test the claimed mechanisms.** Figure 3a isolates tail vs. top vs. random subspace selection across all tested ranks, showing tail consistently yields lower forgetting (2.57% vs. 4.44% top at rank 128). Table 4a demonstrates that unfreezing (U_n, V_n) drops Last accuracy from 82.79% to 77.32%, directly confirming the persistent constraint is essential. These ablations are targeted rather than peripheral.
- **Strong empirical results across diverse benchmarks.** Table 1 shows NuSA-CL outperforms LoRA/MiLoRA by ~4–5 points on all MTIL metrics without extra storage. Table 3 shows it outperforms ZSCL (which requires 10.5 GB of data+model storage) by 4.4% in Last accuracy on the challenging 50-step CIFAR-100 split. Table 2 shows it outperforms InflORA (which uses gradient projection memory) on the 5-shot MTIL benchmark in aggregate.
- **Robust to hyperparameters.** Table 4b shows stable performance across ρ ∈ {0.80, 0.90, 0.95, 0.99}, with meaningful degradation only at the extreme 0.999, supporting practical deployability without sensitive tuning.

---

## Weaknesses

### Fatal
None.

### Major

- **Storage-free baseline set contains no method with an explicit forgetting-mitigation mechanism.** The storage-free comparison in Table 1 includes only vanilla LoRA and MiLoRA—both are standard single-task LoRA variants applied sequentially with no CL-specific mechanism. There are no regularization-based baselines (e.g., EWC or SI applied to CLIP with LoRA), no gradient projection baselines derived without replay, and no other memory-free methods targeting forgetting. The decisive wins partly reflect that LoRA/MiLoRA have no forgetting mitigation whatsoever. The claim "state-of-the-art among storage-free methods" is technically accurate given these results, but the peer group is not competitive, which limits the strength of this central claim.

- **Theoretical section title overstates its content.** Section 4.2 is titled "Forgetting Control in Continual Learning," but Lemma 1 and Theorem 2 bound ⟨W, ΔW⟩_F—a parameter-space inner product—not task-performance degradation. The paper itself acknowledges this in Section 4.2: *"the above results are stated in parameter space and should be viewed as a local stability condition rather than a full function-level guarantee."* The empirical evidence for forgetting reduction is solid; the theoretical section framing creates a stronger impression than the content warrants and conflates parameter-space interference with function-level forgetting.

### Minor

- **No variance or task-order sensitivity analysis.** Tables 1–4 contain no error bars and the paper defers task-order sensitivity entirely to future work. The paper notes this in the Limitations section, but for CL evaluation at ICLR a two or three permutation analysis of the MTIL task sequence would meaningfully strengthen the evaluation at low computational cost.

- **"Null space" terminology is imprecise.** Real weight matrices in trained networks are typically full-rank; there is no true null space. The paper uses "intrinsic null space," "approximate null space," and "low-energy subspace" interchangeably (Sections 3.1 and 3.2). A single definitional clarification at first use would prevent confusion for readers familiar with the linear algebra term.

- **~2-point gap in Last accuracy vs. storage-based SOTA is understated.** Table 1 shows NuSA-CL Last = 82.8% vs. DIKI 85.1% and MoE-Adapters 85.0%. The paper characterizes this as "highly competitive," which is defensible in context, but the gap deserves an explicit acknowledgment rather than being absorbed into summary framing.

### Trivial
None.

---

## Nice-to-Haves
- Add at least one storage-free baseline with an explicit forgetting-mitigation mechanism (e.g., EWC or Synaptic Intelligence applied to CLIP/LoRA) to sharpen the storage-free comparison from "we outperform methods with no CL mechanism" to a more informative head-to-head.
- Report performance across two or three random MTIL task orderings to address variance concerns directly.
- Bring the spectral stability numbers from Appendix Tables 11 and 12 (effective rank and null ratio after 10 MTIL tasks and 50 CIFAR-100 steps) into the main body, since scalability is a headline claim.
- Extend the null-space exhaustion analysis to longer task sequences (100+ tasks) or characterize the rate of effective rank growth per task theoretically, to underpin the "lifelong" scalability claim more rigorously.

---

## Removed Points
*These points are flagged to be removed; treat them with caution.*

- **InflORA 5-shot comparison may disadvantage gradient-projection methods** (harsh critic, Section 5.1): This concern depends on speculative assumptions about the re-implementation quality and whether the 5-shot setting asymmetrically disadvantages gradient-projection. It is not verifiable from the paper. Removed as speculative.
- **No formal guarantee that cumulative updates remain low-energy after merging** (harsh critic, Section 3.2): The paper handles this implicitly by re-running SVD at each task and the empirical evidence in Figure 2 supports stability. This is a theoretical gap the paper acknowledges is future work, not a verifiable flaw from the paper as written. Removed as speculative-structural rather than verifiable-fatal.
- **Long-horizon null-space exhaustion beyond 50 tasks** (harsh critic): The paper explicitly scopes this as a limitation and addresses it partially with the 50-task CIFAR-100 result and the 313.58 remaining null directions figure. Retained as a nice-to-have rather than a weakness.

---

## Novel Insights
NuSA-CL's most distinctive finding is that the spectral structure of a pre-trained weight matrix—computed without access to any data—provides sufficient signal to identify safe adaptation directions for continual learning. The quantitative evidence in Figure 2 that NuSA-CL progressively increases effective rank while conventional LoRA and Full-FT exhibit near-static spectral behavior is mechanistically meaningful: the method is demonstrably accumulating knowledge into underutilized spectral dimensions rather than overwriting existing principal components, which is empirically distinguishable from alternatives. The persistent constraint (freezing U_n and V_n rather than using them only for initialization) as a structural design choice separating NuSA-CL from MiLoRA is a concrete and verifiable contribution.

---

## Suggestions
- Include EWC or SI applied to LoRA-fine-tuned CLIP as a storage-free regularization baseline to meaningfully strengthen the storage-free comparison group.
- Report two or three MTIL task-order permutations at low computational cost.
- Rename Section 4.2 or add a clear subsection distinguishing "parameter-space interference bound" from "function-level forgetting," consistent with the paper's own caveat in the same section.
- Move key spectral stability statistics from Appendix Tables 11/12 into the main paper body to directly support the scalability claim.

---

## Score and Decision

**Calibration anchors retrieved:**

| Path | Avg Score | Round | Comparison |
|------|-----------|-------|------------|
| WM5G2NWSYC (Projected Subnetworks) | 2.00 | R1 | Zero-shot CL with subspace updates, weaker method, rejected |
| JIlIYIHMuv (LVLM-CL) | 2.50 | R1 | CLIP/LVLM CL, weaker experimental rigor, rejected |
| TxIrMD6lAN (Task-Specific Adapters) | 3.00 | R1 | Incremental learning adapters, rejected |
| G9Ea7mlqGO (CLIP Online CL) | 3.80 | R1 | CLIP online CL, less rigorous, rejected |
| dOkuRMrWtL (DESIRE) | 4.25 | R1 | LoRA rehearsal-free CL, missing baselines, rejected |
| Hf54sNeeBM (KACP prompts) | 4.75 | R1 | Prompt-based CL, rejected |
| G9qA1JZ0Sy (LLaCA) | 5.33 | R1 | Multimodal CL with EMA, rejected |
| k9NYnsC4Mq (PROOF) | 5.67 | R1 | VLM CL with projection fusion, rejected |
| wE1I9IGqeH (Complementary Memory CLIP) | 6.00 | R2 | Open-vocab CL with memory systems, rejected |
| Ll8PmgD0IB (LMSP) | 6.00 | R1 | Orthogonal projection CL, rejected |
| AZR4R3lw7y (Multi-View RP) | 5.75 | R1 | Pre-trained model CL, accepted |
| ScI7IlKGdI (Spurious Forgetting) | 6.33 | R1/R2 | LLM CL with orthogonal update analysis, accepted |
| Hcb2cgPbMg (Spectral Regularization CL) | 6.25 | R2 | Spectral singular value regularization for CL, accepted |
| TLADT8Wrhn (TiC-CLIP) | 6.25 | R2 | CLIP continual training at web scale, accepted |
| sb7qHFYwBc (C-CLIP) | 6.50 | R2 | Multimodal VLM CL with novel benchmark, accepted |
| 7D9X2cFnt1 (EFC) | 7.00 | R2 | EFCIL with second-order feature drift, accepted |

**Round 1 bracket:** 5.5–7.5 based on method quality and benchmark coverage.

**Round 2 narrowing:** The most topically similar accepted papers cluster at 6.0–6.5 (C-CLIP at 6.5, Spectral Regularization CL at 6.25, TiC-CLIP at 6.25, ScI7IlKGdI at 6.33). NuSA-CL is stronger than most of these in experimental coverage (multi-benchmark, multi-task-count), clean ablations, and memory-efficiency framing. However, its major gap—comparing storage-free performance only against LoRA/MiLoRA with no CL mechanism—is a real evidential weakness that the 6.5-range accepts do not exhibit to the same degree. The overstated theoretical section is secondary. On balance, NuSA-CL sits just above these 6.0-6.25 anchors but below the 7.0 EFC paper (which has more complete baselines and a tighter theory-practice bridge). I anchor at **6.0**.

MY FINAL SCORE: <score>6.0</score>
MY FINAL DECISION: <decision>Accept</decision>