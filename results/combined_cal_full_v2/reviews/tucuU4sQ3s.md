Now I have all the information I need. Let me construct the final consolidated review.

## Summary

The paper proposes NuSA-CL, a memory-free continual learning framework for vision-language models. It identifies an approximate null space of the model's current weights via SVD and constrains LoRA-style updates to those low-energy directions, then merges the update back into the backbone. This enables the model to adapt to new tasks while preserving zero-shot capabilities, with zero external storage and no parameter growth.

## Strengths

- **Conceptually clean and principled method (Sections 3.1–3.2).** The idea of using SVD to separate principal from null spectral directions and persistently constraining updates to the latter is elegant and well-motivated. The frozen SVD bases with a trainable intermediate matrix M is a natural instantiation of the "don't touch the principal components" intuition. This is a genuine advance over MiLoRA (initialization-only) and InflLoRA (requires storing past gradients).

- **Strong and consistent empirical results in the storage-free regime (Tables 1, 2).** On the MTIL benchmark, NuSA-CL (Transfer=68.6, Avg=75.1, Last=82.8) convincingly outperforms both LoRA (63.9, 70.1, 79.9) and MiLoRA (62.8, 68.7, 77.4). The 4–7pp gap on Transfer demonstrates that the null-space constraint genuinely protects zero-shot capabilities. The 5-shot results (Table 2) reinforce this — NuSA-CL leads on 8 of 11 individual datasets.

- **Scaling advantage on long task sequences (Table 3).** On CIFAR-100 with 50 steps, NuSA-CL achieves 71.85% Last accuracy, outperforming ZSCL by 4.4pp. The gap widens from the 10-step split (0.86pp) to the 50-step split (4.49pp), suggesting the method's advantages compound with sequence length.

- **Clean ablations that validate the core claims (Tables 4a, 4b; Figure 3).** The paper convincingly shows that (a) the persistent constraint matters (unfreezing bases hurts performance), (b) the Tail (low-energy) subspace is superior to Top or Random, (c) multimodal adaptation helps, (d) performance is robust to the energy cutoff threshold ρ over a wide range (0.80–0.99).

- **Genuine memory-free and parameter-budget-fixed operation.** Unlike MoE-Adapters (59.8M parameters, growing) or InflLoRA (needs gradient projection memory), NuSA-CL uses 1.5M trainable parameters, zero external storage, and zero parameter growth. This is a meaningful practical advantage for resource-constrained deployment.

## Weaknesses

### Fatal
None.

### Major

- **Theoretical framing overclaims what the bound guarantees (Section 4).** Lemma 1 bounds interference between an update and the *current* weights: |⟨W_{t-1}, ΔW_t⟩| ≤ σₖ₊₁·‖M‖_F. Theorem 2 sums these pairwise bounds across consecutive tasks. However, catastrophic forgetting concerns interference with *all* prior tasks, especially the *original* pre-trained weights W₀. The quantity ⟨W₀, ΔW_t⟩ for t ≥ 2 is not bounded by Theorem 2 — after merging, W₁'s null space has shifted relative to W₀'s. The paper acknowledges this as a "local stability condition" (Section 4.2), but the abstract and introduction frame the theoretical motivation more strongly than this caveat warrants ("minimizes interference with previously acquired knowledge," "confines all weight updates within these interference-free dimensions"). The method works empirically — and that is the main evidence — but the theoretical apparatus provides a weaker guarantee than the surrounding text sometimes implies. This is a framing issue, not a methodological flaw.

### Minor

- **The spectral analysis narrative overstates the evidence (Figure 2).** The paper describes effective rank changes (text encoder: ~57.9% → ~58.8%; vision encoder: ~51.8% → ~52.4% across 10 tasks) as "active accumulation of knowledge" and "dynamically reshapes the parameter space." These are changes of less than 1 percentage point. While the trend is consistently upward (unlike the static baselines), the magnitude is more consistent with minimal spectral perturbation than with "filling the null space." The small change is actually a *positive* indicator for stability, not a weakness — but the framing should be calibrated to match the evidence. (Note: the critic's specific mathematical argument about "1280 out of 768 directions" is removed from this review as it misunderstands how updates interact with the re-computed null space across tasks.)

- **No variance or multiple-trial reporting.** No standard deviations, confidence intervals, or multiple random seeds are reported anywhere in the paper. CL experiments on the MTIL benchmark are subject to variance from seeds, task ordering, and optimization stochasticity. Without knowing whether the reported improvements (e.g., 68.6 vs 63.9 Transfer in Table 1) are significant relative to run-to-run noise, the reliability of the comparisons is harder to assess. This is a common gap in the CL literature, but addressing it would substantially strengthen the paper.

### Trivial

- **Inconsistent naming of a key baseline.** The paper refers to "InflLoRA" (Liang & Li, 2024) in the text (Section 2.2), uses "InflORA" in Tables 1 and 2, and uses "InLoRA" in Table 4b. These inconsistencies could confuse readers unfamiliar with the literature and should be standardized.

## Nice-to-Haves

- **Training hyperparameters in the main text.** Optimizer, learning rate schedule, batch size, and number of training iterations per task are not specified in the main paper. While these may exist in the appendix, the main text should at least mention them for basic reproducibility.

- **CLIP checkpoint specification.** The paper says "CLIP ViT-B/16" but does not specify whether it is the OpenAI or OpenCLIP version. This matters for exact reproducibility.

- **Clarify the 5-shot setting.** The paper says "5-shot MTIL benchmark" without defining whether this means 5 examples per class, per task, or per dataset.

## Removed Points

These points are flagged to be removed; treat them with caution:

1. *Critic's mathematical argument about effective rank* ("if each of 10 tasks uses r=128 new directions out of d=768, that's ~1280 out of 768 directions") — **Removed** because the calculation misunderstands the method. The null space is re-computed each task from the current weights; updates do not linearly add orthogonal directions in the original weight space. The effective rank measures 95% spectral energy capture, not cumulative direction usage.

2. *Critic's complaint that SVD layers are not specified* — **Removed** because Section 6.3 explicitly states SVD is applied to attention projection matrices (W_q, W_k, W_v, W_o).

3. *Critic's complaint about missing related works* — **Removed** per policy: "DO NOT mention missing related works, as you do not have external sources to confirm their existence."

4. *Several minor critic notes about presentation and formatting* — **Removed** as parser artifacts.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

- Reframe the theoretical contribution to explicitly state that Theorem 2 bounds only pairwise consecutive interference, and that the preservation of zero-shot capabilities is supported empirically rather than by the theoretical bound. The "local stability condition" caveat in Section 4.2 should be stated alongside Lemma 1, not deferred to the end of the section.

- Calibrate the "knowledge accumulation" language in Section 6.1 to match the <1% effective rank change shown in Figure 2. The small perturbation is actually a *positive* sign for stability and can be presented as evidence that the method preserves spectral structure, not that it "fills" the null space.

- Report mean ± std over at least 3 random seeds on the MTIL benchmark to establish statistical significance. This is the single highest-leverage addition the paper could make.

- Standardize the baseline name to "InflLoRA" throughout the paper, tables, and figures.

## Score and Decision

### Calibration Report

**All anchors retrieved across rounds:**

| Anchor | Path | Avg Score | Round | Itemized? | Comparison |
|--------|------|-----------|-------|-----------|------------|
| Balancing Differential Discriminative Knowledge | 5lUdTogEL3.md | 1.00 | 1 | No | Irrelevant topic (person re-id); far weaker paper |
| NEMESIS Jailbreaking LLMs | 5kMwiMnUip.md | 1.40 | 1 | No | Unrelated topic |
| Projected Subnetworks Scale Adaptation | WM5G2NWSYC.md | 2.00 | 1,2 | No | Related (projected updates for zero-shot), but score 2.00 with severe weaknesses; NuSA-CL is far stronger empirically and methodologically |
| Maintaining Adversarial Robustness in CL | sr0My6yDNu.md | 3.25 | 1,2 | No | Related (gradient projection for CL); significantly weaker results |
| Replay can provably increase forgetting | kf9phcBvQ5.md | 3.00 | 1 | No | Theory paper; not comparable |
| CLIP model is an Efficient Online Continual Learner | G9Ea7mlqGO.md | 3.80 | 1,2 | Yes | Similar topic (CLIP continual learning) but scored lower due to lack of novelty and weak theory; NuSA-CL has a more principled method |
| Class-Incremental Learning with PEFT Prompts | 4lqo5Jwfnq.md | 4.67 | 1,2 | No | Similar topic but lower score; prompt-based approach |
| SimE: Simple Efficiency IL Framework | rkAqvDnnmO.md | 5.25 | 1,2 | No | Similar topic; lower score |
| **Learning without Forgetting for VLMs** | k9NYnsC4Mq.md | **5.67** | 1,2,3 | **Yes** | Directly comparable VLM continual learning paper; had concerns about missing std dev and method depth. NuSA-CL has cleaner method and stronger ablations → above this |
| **TiC-CLIP: Continual Training of CLIP** | TLADT8Wrhn.md | **6.25** | 2,3 | **Yes** | Benchmark paper for continual CLIP training; design concerns (W3). NuSA-CL has a novel method rather than benchmark → comparable tier |
| **C-CLIP: Multimodal CL for VLM** | sb7qHFYwBc.md | **6.50** | 1,2,3 | **Yes** | Most directly comparable (CLIP CL with LoRA + distillation). NuSA-CL has a cleaner, more principled null-space approach vs. C-CLIP's LoRA+CKC. Comparable strengths, similar weaknesses → same tier |
| Scalable Language Model with Generalized CL | mz8owj4DXu.md | 6.50 | 3 | No | Language model focus; not directly comparable |
| **Adapting MLLM to Concept Drift** | b20VK2GnSs.md | **7.00** | 3 | **Yes** | Higher score but had significant methodological concerns (inappropriate experiment setup, unclear comparisons). NuSA-CL has fewer validity concerns → slightly below this |
| Capturing Temporal Dependence | uHLgDEgiS5.md | 8.00 | 1 | No | Unrelated topic (data influence) |
| Spectrally Transformed Kernel Regression | OeQE9zsztS.md | 8.00 | 1 | No | Unrelated topic |

**Round 1 bracket:** Based on the paper's strengths (clean method, strong empirical results, thorough ablations) and weaknesses (overclaimed theory framing, overstated spectral narrative, no variance reporting), the plausible range was 5.5–7.5.

**Round 2–3 narrowing:** The closest anchors are C-CLIP (6.50) and Learning without Forgetting for VLMs (5.67). NuSA-CL's strongest weighted items (empirical results at 12.02, method at 11.01, ablations at 11.20) are substantially higher than C-CLIP's top strengths (10.75 for ablations, 9.49 for benchmark contributions). Its main drags (theoretical framing at 3.13, spectral narrative at 7.32, no variance at 3.03) are comparable to or milder than C-CLIP's main weaknesses (computational cost missing at 8.39, missing baselines at 6.27). The paper sits above the 5.67 anchor (which had more severe methodological concerns) and slightly below the 7.00 anchor (which had deeper theoretical analysis albeit with experiment design issues). The weighted-item comparison confirms placement at **6.5**.

**Final Score: 6.5** — The paper has a clean, principled method, strong empirical results, and thorough ablations. Its weaknesses are about framing and reporting rather than validity. This places it in the borderline-accept / accept range, consistent with similar CLIP continual learning papers.

MY FINAL SCORE: <score>6.5</score>
MY FINAL DECISION: <decision>Accept</decision>