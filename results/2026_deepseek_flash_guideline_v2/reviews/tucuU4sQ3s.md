The calibration tool is encountering file system issues. Let me proceed with the final review based on my careful reading of the paper and filtering of the reviewer inputs.

Here is my final consolidated review:

---

## Summary

This paper proposes NuSA-CL, a memory-free continual learning framework for vision-language models. It identifies an approximate null space of the model's current weights via SVD and constrains low-rank (LoRA-style) updates to lie within that subspace through a persistent constraint (frozen bases U_n, V_n with a learned intermediate matrix M). After each task, the update is merged into the backbone, maintaining a fixed parameter budget. On the MTIL benchmark (11 datasets), NuSA-CL achieves Transfer=68.6%, Avg=75.1%, Last=82.8% with 1.5M trainable parameters, zero additional storage, and 1.21 GPU-hours — competitive with storage-based methods that require orders of magnitude more resources. On long-sequence CIFAR-100 (50 tasks), it outperforms even storage-based ZSCL by 4.49 points on Last accuracy.

## Strengths

- **Memory-free operation with a strong efficiency–performance trade-off (Table 1).** NuSA-CL outperforms all other storage-free methods (LoRA, MiLoRA, Continual-FT) by a wide margin (e.g., Transfer 68.6% vs. LoRA's 63.9%) and closely approaches storage-based methods (DIKI 68.7%, MoE-Adapters 68.9%) while using 40× fewer parameters, zero storage, and ~3× less GPU time than MoE-Adapters. This directly substantiates the paper's central claim.

- **Persistent constraint validated as the decisive design choice (Table 4a).** Making the null-space bases trainable causes Transfer to drop from 68.58% to 62.60%, Avg from 75.08% to 68.12%, and Last from 82.79% to 77.32%. This cleanly isolates the persistent constraint (not just subspace initialization) as the mechanism driving the method's success.

- **Long-sequence scalability with a widening advantage (Table 3).** On CIFAR-100, NuSA-CL's advantage over the strongest baseline (ZSCL) grows from +0.86 (10-step) to +4.26 (20-step) to +4.49 (50-step). This monotonic trend provides strong empirical evidence against null-space saturation concerns and demonstrates that dynamic task-wise null-space re-computation scales effectively.

- **Principled subspace selection via systematic ablation (Figure 3a).** Across five ranks (32–256), the Tail (null-like) subspace consistently yields the lowest forgetting (e.g., at r=128: Tail 2.57% vs. Top 4.44% vs. Random 4.57%). This exhaustive comparison across the rank dimension convincingly shows that low-energy directions provide a safer region for continual updates.

- **Empirical evidence of accumulation vs. overwriting dynamics (Figure 2).** While LoRA and Full-FT exhibit near-static spectral behavior (e.g., LoRA vision output effective rank shifts from 447.42 to 447.58 across 11 tasks), NuSA-CL shows progressive effective-rank increases. The paper further reports that even after 10 tasks, the most saturated layer retains 313.58 available null directions — more than double the update rank r_max=128 — providing direct evidence against null-space exhaustion concerns.

## Weaknesses

### Fatal
None.

### Major
None.

### Minor

1. **Missing training hyperparameters and variance reporting.** The main text does not report learning rate, optimizer, batch size, or training schedule for the main experiments (only "1000 training iterations" is mentioned for ablations). All results in Tables 1–4 are reported as point estimates without standard deviations, confidence intervals, or seed counts. For a methods paper, these details are needed to assess result reliability and enable fair comparison of training budgets across methods. *(Note: some details may reside in the stripped appendix, but the main text should at minimum state the key settings.)*

2. **LoRA baseline re-implementation uses weight merging.** The paper re-implements LoRA baselines with adapters "merged after each task." In standard continual learning practice, LoRA typically keeps task-specific adapters separate. While the paper is transparent about this modification for fair comparison, the potential impact on baseline performance is not discussed — merging may disadvantage LoRA relative to its standard usage, and this deserves a note.

3. **Theoretical analysis covers only adjacent-task interference.** Theorem 2 bounds cumulative interference ∑⟨W_{t-1}, ΔW_t⟩ but does not bound cross-update interference (e.g., ⟨ΔW_i, ΔW_j⟩ for non-adjacent i, j) or the interference between ΔW_t and components of earlier weights displaced by intermediate updates. The paper honestly qualifies the analysis as a "local stability condition rather than a full function-level guarantee," but this gap between the theory and the multi-task experimental setup is worth noting.

4. **Evaluation limited to a single backbone scale (ViT-B/16).** The paper's scalability claims would be strengthened by results on at least one larger backbone (e.g., ViT-L/14). This is acknowledged in the limitations section as future work.

### Trivial
None.

## Nice-to-Haves

- Reporting results with standard deviations over 3 seeds would substantially strengthen the empirical claims.
- A sensitivity analysis on task order (even 2–3 permutations) would address known concerns in continual learning evaluation.
- A brief discussion of how the merging design choice for LoRA baselines may affect comparison fairness would improve the paper.

## Removed Points

These points were raised by reviewers but removed after cross-checking against the paper:

- **"Null space terminology is misleading"** — The paper consistently uses "approximate null space" and defines it clearly via SVD truncation (Eq. 1–2). The "null space" label is standard in the subspace learning literature for low-energy subspaces, and the paper is transparent about the approximation. The bound-tightness concern at ρ=0.95 is not a flaw in the method; empirical ablations show robustness across ρ∈[0.80, 0.99].

- **"Theoretical framing overclaims"** — The paper explicitly states its analysis is "in parameter space" and "should be viewed as a local stability condition rather than a full function-level guarantee." The abstract and introduction describe the method's mechanism without claiming a stronger theoretical result than is provided.

- **"MiLoRA comparison is unclear"** — The paper clearly marks re-implemented baselines with † and states they use a "unified framework" with consistent rank. This is standard and appropriate.

- **"Missing appendix content"** / **"Parser artifact formatting"** — Removed per system instructions; the stripped appendix is a PDF-extraction artifact, not a paper flaw.

## Novel Insights

None beyond the paper's own contributions. The reviews do not surface a perspective that the paper itself does not already convey.

## Suggestions

1. Add training hyperparameters (learning rate, optimizer, batch size, schedule) and report main results with variance (at least 3 seeds).
2. Clarify whether standard (non-merged) LoRA would produce different numbers, and discuss the implications of the merging choice for comparison fairness.
3. Extend evaluation to at least one larger backbone (e.g., ViT-L/14) or explicitly justify why the ViT-B/16 results are sufficient to support the scalability claims.

## Score and Decision

**MY FINAL SCORE: 7.0**
**MY FINAL DECISION: Accept**

*Rationale:* The paper introduces a well-motivated, clean method with strong empirical support. The core idea — constraining updates to the approximate null space via a persistent constraint — is clearly explained, and the ablations convincingly validate that this design choice drives performance. The memory-free property combined with competitive results (especially on long sequences) represents a genuine contribution. The weaknesses (missing training details, no variance reporting, single backbone) are real but fixable and do not undermine the core claims. The paper is clearly a solid accept at a top venue like ICLR.