Now I have everything I need. Let me write the complete final review.

**My score bracket from Round 1:** Between approximately 4.5 and 5.5. The paper is stronger than DISTA (4.50, Reject) which lacked ImageNet results, but weaker than the Saccadic Attention paper (6.60, Accept) which had much clearer presentation and stronger theoretical framing. It is broadly comparable to SDT-V2 (5.67, Accept) in scope but has more method presentation issues.

**Narrowing from Round 2:** The Topoformer (6.00) and Long Range Abilities (4.50) anchors help bound. Topoformer scored 6.00 despite serious weaknesses (incorrect claims: -10.00, undefined variables: -10.00) because it had very high-impact strengths (novelty +9.64, writing +9.98). Our paper's method inconsistency (-9.94, -10.00) is as severe as Topoformer's worst weaknesses, but our high-impact strengths are weaker (SSA diagnosis +8.65 is the strongest, vs Topoformer's +9.98 for writing). This places us below 6.00. Above 4.50 because we have ImageNet results across multiple architectures, unlike DISTA and SAF.

**Final score: 5.0**

Now let me produce the review.

Regarding the causal issue: I need to be precise. Eq. 8 uses sum over j=1..N (full attention). Eq. 11 uses sum over j=1..n-1 (causal). This IS a different attention pattern. The paper says "LRF-SSA can be reformulated through causal inference" — this changes the computation from full to causal attention. This is a weakness but not fatal because the empirical results show it still works well.

Let me finalize my review now.## Summary

This paper identifies two key limitations of Spiking Self-Attention (SSA) in spiking transformers: poor local modeling due to the removal of softmax, and high memory overhead from storing attention matrices. The authors propose LRF-Dyn, which adds local receptive fields (convolutional bias) to SSA to improve locality, and reformulates the computation via neuronal membrane-potential dynamics to avoid explicit attention matrix storage. Experiments on ImageNet classification and ADE20K segmentation across three backbone architectures (Spikformer, QKFormer, SDT-V3) show consistent accuracy improvements (~0.4–1.2%) over baseline SSA, while the dynamics-based variant reduces memory usage at a small accuracy cost.

## Strengths

1. **Clear diagnosis of a genuine SSA limitation.** Section 4.1 and Figure 2 empirically demonstrate that SSA produces near-uniform attention distributions, unlike the localized distributions of VSA. The Manhattan-distance analysis (76.68% of VSA attention within distance 5 vs. 20.31% for SSA) provides a concrete, quantifiable observation that makes the problem statement testable and well-motivated. This diagnostic could inform other work in spiking transformers. **[impact=+8.65]**

2. **Experimental scope is appropriate.** Evaluation spans ImageNet classification (Table 1) and ADE20K segmentation (Table 2) across three distinct backbone architectures (Spikformer, QKFormer, SDT-V3). The accuracy gains are consistent across all settings, and the multi-architecture validation strengthens the claims. **[impact=+4.64]**

3. **Core approach is coherent.** Adding local bias to compensate for SSA's lack of locality, combined with a dynamics-based reformulation to avoid storing attention matrices, is a sensible and internally consistent strategy. **[impact=+1.68]**

## Weaknesses

### Fatal
None.

### Major

1. **Method presentation is internally inconsistent.** The paper shifts between incompatible formulations without acknowledgment or justification. Specifically:
   - **Eq. 8** (Section 5.1) defines LRF-SSA with full attention over all tokens (sum over j=1..N).
   - **Eq. 11** (Section 5.2) changes this to causal attention (sum over j=1..n-1) for the memory-reduced LRF-Dyn variant, stating this "can be reformulated through causal inference." This is not merely a computational reordering — it changes the attention pattern. The paper does not acknowledge this change, discuss its implications for vision tasks (where tokens lack inherent sequential order), or compare against a bidirectional variant. The ablation (Table 3) shows that the causal reformulation itself causes a significant accuracy drop (Causal SSA w/o LRF: 74.30% vs. SSA: 77.86% on CIFAR-100), yet this is discussed only implicitly.
   - **Eq. 15** (Section 5.3) introduces a Fourier-domain formulation (ℱ⁻¹{ℱ(K)*ℱ(X)}) with no connection to the recurrent dynamics in Eq. 12. The expression 𝒦(t) = ΓC Σ_{m=1}^{n-m} 𝒜 is garbled and the notation is undefined. A reader cannot determine whether LRF-Dyn is implemented via the recurrent formulation, the Fourier transform, both, or neither. **[impact=-9.94 / -10.00 — merged]**

   These issues collectively make it difficult to verify what was actually implemented. The core ideas (LRF + dynamics) are understandable, but the presentation needs substantial reconciliation to be publication-ready.

### Minor

2. **The accuracy-memory trade-off is not acknowledged.** The paper presents LRF-Dyn as strictly beneficial, but the evidence consistently shows a small accuracy cost relative to LRF-SSA. On ImageNet (Table 1), LRF-Dyn underperforms LRF-SSA on every configuration (e.g., 74.51 vs. 74.62, 75.58 vs. 75.66, 79.21 vs. 79.24). The CIFAR-100 ablation (Table 3) confirms this pattern. The memory reduction is a worthwhile trade-off, but the paper should present it as such rather than implying LRF-Dyn is a free improvement. **[impact=-5.97]**

3. **Theorems 1–2 overclaim their status.** The paper asserts as mathematical theorems that VSA attention weights are proportional to exp(−βΔ) and SSA weights to (α−βΔ)₊ (functions of Manhattan distance alone). VSA attention weights depend on content (q_i·k_j), not just position; deriving these functional forms requires strong assumptions about data distribution that are not stated. These are best characterized as empirical observations (supported by the qualitative evidence in Figure 2) rather than proven theorems. The paper should clarify their status or provide proper derivations from stated assumptions. **[impact=-9.67]**

4. **Several notational issues affect clarity.** In Eq. 8, **V**^{jk} is undefined (V is the value matrix, but the superscript is not explained). In Eq. 15, the Fourier symbols ℱ and ℱ^{-1} appear without introduction or connection to the surrounding equations. The Attn column in Table 2 marks LRF-Dyn with ✗ despite still computing attention (just in a different form), which is confusing. **[impact=-9.90 / -10.00 — merged]**

5. **Missing experimental details.** The number of simulation timesteps T for ImageNet experiments is not stated, which is essential for SNN papers. Absolute memory numbers (in MB/GB) are not reported — only a single relative percentage (49.4%) for one configuration — making the practical impact hard to assess. **[impact=-3.26]**

### Trivial
None.

## Nice-to-Haves
- Report absolute memory usage (MB/GB) across configurations rather than only relative percentages.
- State the number of simulation timesteps T used for ImageNet experiments.
- Consider adding results with a bidirectional variant of LRF-Dyn (non-causal) to isolate the effect of the causal constraint.

## Removed Points

These points from the Harsh Critic were filtered out for the following reasons:

- **"Three different methods, not one":** Overstatement. Eq. 8 and Eq. 14 describe the same mechanism (LRF-SSA) in different notation; there are two methods (LRF-SSA and LRF-Dyn), not three. The real inconsistency (causal shift, Fourier disconnect) is captured above.
- **"Causal SSA has neither LRF module nor dynamics"** (in the ablation): Factually incorrect. Table 3 shows Causal SSA at all Ω levels (including with LRF), so the comparison at matched Ω levels is valid. The core concern about comparing LRF-Dyn vs. LRF-SSA is retained.
- **Missing appendix / appendix proofs:** Removed per policy — the parser strips supplementary content from all papers; it exists in the original submission.
- **Missing energy consumption estimates:** Scope creep — the paper's focus is memory reduction, not energy.
- **Missing related work references:** Removed per policy.

## Novel Insights

The observation that SSA's near-uniform attention distribution (Section 4.1, Figure 2) is a directly quantifiable cause of its performance gap — with 20.31% vs. 76.68% of attention concentrated within Manhattan distance 5 for SSA vs. VSA — is a genuinely useful diagnostic. This specific measurement methodology could be applied by other researchers working on spiking transformers. However, the insight that LRF-Dyn trades a small (consistent but tiny) accuracy penalty for memory savings emerges from the data upon scrutiny but is not presented as such by the paper.

## Suggestions

1. **Reconcile the method presentation.** Clarify the relationship between the recurrent dynamics (Eq. 12) and the Fourier-domain formulation (Eq. 15) — are these equivalent implementations of the same computation, or different variants? If they are equivalent, explain how; if not, remove one.
2. **Explicitly discuss the causal vs. bidirectional attention choice.** If LRF-Dyn uses causal attention, state this clearly, justify its suitability for vision tasks, and ideally compare against a bidirectional variant.
3. **Acknowledge the accuracy-memory trade-off.** Present LRF-Dyn as a memory-accuracy trade-off (slightly lower accuracy than LRF-SSA but reduced memory), not a free improvement.
4. **Reframe Theorems 1–2** as empirical characterizations supported by Figure 2, or provide proper derivations from explicitly stated assumptions about the data distribution.
5. **Add absolute memory numbers** (MB/GB) for representative configurations and state the simulation timesteps T used for ImageNet experiments.

---

## Score and Decision

**Bracket analysis (Round 1):** The paper sits between 4.5 and 5.5 based on the retrieved anchors. It outperforms lower-anchored papers like DISTA (4.50, Reject — ImageNet results missing) and Spike Accumulation Forwarding (4.00, Reject — limited experiments) because it provides multi-architecture ImageNet results. It underperforms higher-anchored papers like the Saccadic Spiking Transformer (6.60, Accept — clearer presentation, stronger theoretical framing) and Spike-driven Transformer V2 (5.67, Accept — cleaner architecture narrative) due to method presentation issues.

**Narrowing (Round 2):** Compared to Topoformer (6.00), which had serious exposition weaknesses (-10.00 impact for incorrect claims and undefined variables) but was compensated by very high-impact strengths (writing +9.98, novelty +9.64), our paper's strongest strength (SSA diagnosis +8.65) is weaker, while our method inconsistency weakness (-9.94, -10.00) is at least as severe as Topoformer's worst issues. This places us below 6.00. Compared to "On the Long Range Abilities of Transformers" (4.50), our paper offers more extensive experimental validation across multiple vision tasks and architectures, placing us above 4.50.

**Final placement:** The paper's core contribution — that adding localized receptive fields consistently improves SSA — is real and empirically supported. However, the method section's internal inconsistencies (unexplained causal shift, disconnected Fourier formulation) are significant enough that readers cannot confidently verify what was implemented. The theorems overclaim their status, and the accuracy-memory trade-off is not honestly presented. These issues are fixable in revision but prevent acceptance in the current form.

**All anchors retrieved:**
1. `/home/.../qzZsz6MuEq.md` — Spiking Vision Transformer with Saccadic Attention (6.60, Round 1, itemized): Clearer presentation, had weaknesses but stronger theoretical and experimental narrative → **above our paper**
2. `/home/.../1SIBN5Xyw7.md` — Spike-driven Transformer V2 (5.67, Round 1/2, itemized): Cleaner architecture story, only one real weakness (incremental) → **above our paper**
3. `/home/.../mjDROBU93g.md` — DISTA (4.50, Round 1/2, itemized): Lacked ImageNet results, novelty concerns → **below our paper**
4. `/home/.../CwAY8b8i97.md` — Spike Accumulation Forwarding (4.00, Round 1, itemized): Limited experiments, poor writing → **below our paper**
5. `/home/.../R6AA1NZhLd.md` — Topoformer (6.00, Round 2, itemized): Had serious exposition issues but very high writing quality and novelty → **above our paper**
6. `/home/.../lnffMykYSj.md` — On the Long Range Abilities of Transformers (4.50, Round 2, itemized): Good idea but limited experiments → **below our paper**

MY FINAL SCORE: <score>5.0</score>
MY FINAL DECISION: <decision>Reject</decision>