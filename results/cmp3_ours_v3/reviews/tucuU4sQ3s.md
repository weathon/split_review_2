Now let me compile the final review with the calibrated score.

## Summary

This paper proposes NuSA-CL, a memory-free continual learning method for vision-language models (specifically CLIP). The core idea is to identify a low-energy null space of the model's weight matrices via SVD before each task, then persistently constrain all task-specific low-rank updates to lie strictly within this null space throughout training. The updates are then merged into the backbone, maintaining a fixed parameter budget with zero persistent storage across tasks. Experiments on MTIL and CIFAR100 benchmarks show strong efficiency (1.5M parameters, 6.6 GB GPU, 1.21 GPU-hours) while achieving competitive accuracy with storage-based methods.

## Strengths

1. **Principled and clean method design.** The idea of persistently constraining updates to an SVD-identified null space (Eq. 3) is conceptually elegant. The persistent constraint (freezing U_n, V_n throughout training) is a clearly articulated distinction from prior work like MiLoRA which uses similar subspaces only for initialization.

2. **Genuinely impressive efficiency.** Table 1 shows NuSA-CL uses 1.5M trainable parameters (vs. 15.7M for LoRA, 149.6M for ZSCL), 6.6 GB peak GPU memory, and 1.21 GPU-hours with zero persistent storage. The 40× parameter reduction vs. MoE-Adapters while maintaining competitive accuracy is a strong result for resource-constrained deployment.

3. **Well-designed ablations.** The subspace selection ablation (Fig. 3a: Tail vs. Top vs. Random) convincingly shows that low-energy directions minimize forgetting across all tested ranks. The persistent constraint ablation (Table 4a: training M only vs. also unfreezing U_n/V_n) cleanly demonstrates that the constraint is functionally important.

4. **Competitive long-sequence performance.** The CIFAR100 50-step result (Table 3: NuSA-CL 71.85% vs. ZSCL 67.36% Last accuracy) provides meaningful evidence that the method does not collapse over long task sequences.

## Weaknesses

### Fatal

None.

### Major

1. **Spectral dynamics data contain an internal inconsistency that undermines the "accumulation vs. overwriting" narrative.** The paper defines effective rank (r₉₅/d) and null ratio as complementary quantities representing "the capacity used to encode core knowledge" and "the remaining underutilized capacity" (Section 6.1). By construction, null_ratio = 1 − effective_rank per layer, and averaging preserves complementarity. Yet Figure 2 (line 206) reports that for the text encoder, effective rank increases from ~57.9% to ~58.8% while null ratio *also* increases from ~41.0% to ~42.2% — a mathematical impossibility if they are complementary as claimed. The numbers sum to 98.9% and 101.0%, not 100%. For the vision encoder, both metrics also increase simultaneously (51.8%→52.4% and 47.4%→48.2%), summing to 99.2% and 100.6%. Even ignoring the inconsistency, the changes are tiny (sub-1 percentage point over 10 tasks). The paper frames this as central evidence that NuSA-CL "actively accumulates knowledge by progressively filling the underutilized null space" (line 218), calling it "the core mechanism behind NuSA-CL's ability to mitigate catastrophic forgetting." The data as presented cannot support this claim. The main experimental results (Tables 1-3) and ablations (Fig. 3, Table 4) remain valid, but the spectral analysis used to explain *why* the method works is unreliable in its current form.

2. **The "state-of-the-art in the storage-free setting" claim rests on a narrow baseline set.** In the storage-free setting (Table 1), NuSA-CL is compared only against Continual-FT, LoRA, and MiLoRA — none of which are strong continual learning methods. The paper does not include comparisons against other memory-free CL approaches (e.g., weight-regularization methods like EWC adapted to PEFT, or other orthogonal-projection methods that operate without replay). The advantage over the included baselines is clear, but calling this "state-of-the-art within the practical and challenging storage-free setting" (line 190) would carry more weight with a broader comparison set.

### Minor

3. **No variance or statistical significance reporting.** All main results (Tables 1-3) report single numbers without standard deviations or confidence intervals. Given modest margins in some comparisons (e.g., Table 3: NuSA-CL 74.51% vs. ZSCL 73.65% on 10-step Last), it is unclear whether differences are statistically meaningful.

4. **The theoretical contribution (Lemma 1, Theorem 2) adds limited insight.** The bound is on the parameter-space inner product — not on forgetting, output changes, or function-level interference. The paper's own caveat (line 122: "local stability condition rather than a full function-level guarantee") concedes this. The theory section is not incorrect, but it adds little beyond the intuitive motivation already provided by the method description.

5. **The drop at ρ=0.999 in Table 4b is underexplained.** Performance drops notably (Last accuracy from ~82.7% to ~79.2%) when the energy threshold is set to 0.999. This is counterintuitive: a tighter constraint (more dimensions assigned to the null space) would be expected to reduce interference, not increase it. The paper attributes this to robustness without further analysis.

### Trivial

None.

## Nice-to-Haves

- Adding variance reporting (standard deviations across multiple seeds) would strengthen the evidence, especially for comparisons where margins are small.
- Including additional storage-free baselines (e.g., weight-regularization methods adapted to PEFT) would strengthen the SOTA claim.
- Providing more granular per-layer spectral data rather than just averaged metrics would make the dynamics analysis more interpretable.
- An analysis of why ρ=0.999 degrades performance would be informative.

## Removed Points

1. **Missing details on which weight matrices are adapted** — REMOVED because the paper explicitly states on line 286: "we compute SVD once per task and per layer on the attention projection matrices (e.g., W_q, W_k, W_v, W_o)."
2. **Missing validation of re-implemented baselines** — REMOVED because the paper provides reasonable implementation details (unified framework, consistent rank, same architecture), which is standard for conference submissions.
3. **Comparison to CLIP zero-shot on MTIL transfer is modest** — REMOVED because the paper presents and contextualizes this comparison in Table 2; the transfer improvement of ~3.3pp over zero-shot is honestly reported.
4. **Formatting/style nitpicks** — REMOVED as parser artifacts.
5. **Strength about "addressing an important problem"** — REMOVED as generic; retained strengths are concrete and specific.

## Novel Insights

None beyond the paper's own contributions. The spectral dynamics inconsistency is a genuine finding that emerged from cross-referencing the paper's definitions with the reported numbers.

## Suggestions

1. **Resolve the spectral dynamics inconsistency.** Re-examine the effective rank and null ratio computation in Figure 2. If the data cannot support the "accumulation vs. overwriting" narrative, either provide alternative evidence (e.g., per-layer energy redistribution rather than averaged metrics) or appropriately scale back the mechanistic claim.
2. **Expand the storage-free baseline set** by adding at least a weight-regularization method (e.g., EWC) adapted to the PEFT setting, or another memory-free orthogonal projection approach.
3. **Add variance/confidence intervals** to the main results tables.
4. **Analyze the ρ=0.999 degradation** — the tighter constraint leading to worse performance is a counterintuitive result worth explaining.

## Calibration Anchors

All anchors retrieved across rounds:

**Round 1 (Bracketing):**
- `gwZ90hFSL2.md` — avg 1.00 — Cross-lingual robotics paper; irrelevant, vastly weaker than NuSA-CL.
- `5lUdTogEL3.md` — avg 1.00 — Lifelong person re-id; weaker, different domain.
- `WM5G2NWSYC.md` — avg 2.00 — Projected subnetworks for CL; clearly weaker.
- `sr0My6yDNu.md` — avg 3.25 — Gradient projection for robust CL; comparable domain but weaker method.
- `TxIrMD6lAN.md` — avg 3.00 — Task-specific adapters for IL; outdated baselines, less novel.
- `HCCkCjClO0.md` — avg 3.00 — Online weight approximation for CL; weaker.
- `9aZ2ixiYGd.md` — avg 5.00 — Prompt-based rehearsal-free CL; accepted despite split reviews (8,6,3,3).
- `Hf54sNeeBM.md` — avg 4.75 — Contrastive prompt CL; rejected, comparable quality.
- `G9Ea7mlqGO.md` — avg 3.80 — CLIP as online continual learner; weaker.
- `rkAqvDnnmO.md` — avg 5.25 — SimE multi-adapter IL; rejected, comparable but less novel.
- `sb7qHFYwBc.md` — avg 6.50 — C-CLIP multimodal CL; stronger (more comprehensive baselines, no spectral issue).
- `k9NYnsC4Mq.md` — avg 5.67 — Proof/LwF-VLM; rejected, comparable domain, similar contribution level.
- `TLADT8Wrhn.md` — avg 6.25 — TiC-CLIP continual training; stronger (large-scale benchmarks).
- `mz8owj4DXu.md` — avg 6.50 — SLM for language model CL; stronger.

**Round 2 (Narrowing, 4.0–6.0):**
- `gV0Moskp7k.md` — avg 4.40 — Low-rank CL for LLMs; weaker.
- `7L2bpe7lfm.md` — avg 4.50 — Video CL with compression; less relevant.
- `bqv7M0wc4x.md` — avg 5.50 — ICL-TSVD SVD-based CL; accepted, comparable (also SVD-based, theory+empirical).
- `BRDqmYU8A0.md` — avg 5.50 — Model developmental safety for VLMs; different framing.
- `DiG14qg4ok.md` — avg 4.33 — Low-coherence subspace projection; weaker (learning capacity degradation).

**Round 1 bracket:** 4.0 – 6.0.
**Narrowing reasoning:** NuSA-CL is clearly stronger than the 4.0–4.5 papers (cleaner method, stronger results). It is comparable to the 5.0–5.5 papers (ICL-TSVD at 5.50, Proof at 5.67, SimE at 5.25) but the spectral inconsistency is a concrete error that ICL-TSVD and Proof do not have. At the same time, the efficiency story (1.5M params, zero storage) is stronger than SimE's. The paper sits at the lower end of the 5.0–5.5 band. **Final score: 5.0.**

MY FINAL SCORE: <score>5.0</score>
MY FINAL DECISION: <decision>Reject</decision>