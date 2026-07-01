## Summary

This paper studies token pruning for unified multimodal transformers (models handling both generation and understanding). It first conducts an empirical analysis of attention patterns, layer importance (via ARank), and task interactions across several unified models, finding that token redundancy is both task-dependent and layer-dependent. Based on these insights, the authors propose UniMoD, which replaces selected transformer layers with task-specific Mixture-of-Depths blocks (separate routers per task) chosen via ARank-based layer selection. Applied to Show-o and Emu3, UniMoD reduces training FLOPs by 15% and 40% respectively while maintaining competitive performance.

---

## Strengths

1. **The empirical analysis in Section 3 is the paper's clearest contribution.** The three investigations — attention weight patterns (Sec. 3.2), ARank-based layer redundancy (Sec. 3.3), and the competitive token pruning experiment (Sec. 3.4, Fig. 4) — provide concrete evidence that token redundancy in unified transformers depends on both the task and the layer. The competitive pruning experiment (Fig. 4) is particularly informative: it shows that a shared router overwhelmingly favors generation tokens over understanding tokens, directly motivating a task-separate design.

2. **The core design choice — separate routers per task — follows naturally from the analysis.** The T2I MoD / MMU MoD / Shared MoD decomposition (Fig. 5) is a clean response to Observation 5 (generation tokens dominate under a shared router) and Observations 2–4 (redundancy varies by layer and task). The connection between evidence and design is logical and well-motivated.

3. **The FLOPs savings are substantial and practically meaningful.** Reducing Emu3 training compute by ~40% (89.0 → 53.5 TFLOPs) and Show-o by ~15% while keeping most benchmarks within a few points of the full model is a genuinely useful result.

---

## Weaknesses

### Fatal

None.

### Major

1. **The ablation study weakens the paper's central claim that task-specific routers are the key to UniMoD's success.**  

   In Table 5, the "w/o task-aware router" variant (single router at ARank-selected layers, 40.8 TFLOPs) achieves MME 1052.0, GQA 54.4, POPE 80.2, MMMU 25.6, VQAv2 65.5, GenEval 0.50. UniMoD (separate routers at the same layers, 43.3 TFLOPs) achieves MME 1093.7, GQA 54.5, POPE 80.3, MMMU 25.7, VQAv2 66.2, GenEval 0.61. On the five understanding benchmarks, the gap between a *single router* and *separate task-specific routers* is ≤1.5 points on MME and ≤0.1–0.7 points on the rest — despite UniMoD using more compute (43.3 vs 40.8 TFLOPs). The only clear improvement from separate routers is on GenEval (0.50 → 0.61).  

   Meanwhile, "w/o layer switch module" (separate routers at interleaved layers, 43.3 TFLOPs) scores GenEval 0.50 — the same as the single-router variant — while its understanding scores (MME 920.3, GQA 52.1, POPE 74.7) are far worse. This strongly suggests that **ARank-based layer selection is the primary driver of the understanding gains, not task-specific routing**. The paper frames its contribution as "task-aware token pruning" with separate routers, but the evidence shows that a single router at ARank-selected layers recovers nearly all understanding performance. The paper should more honestly characterize what drives the gains and consider a matched-FLOP ablation.

### Minor

2. **The Emu3 results are framed slightly inaccurately.** The paper states UniMoD achieves "comparable or better results" on Emu3. On the five MMU benchmarks in Table 3, UniMoD wins on MME (+19.7) and MMMU (+0.2) but loses on GQA (−0.8), POPE (−1.3), and VQAv2 (−0.9). "Comparable" is fair, but the claim should more accurately reflect that understanding benchmarks show small degradations on a majority of tasks. The paper transparently notes the Emu3 baseline is a re-implementation using alternative datasets, which is appropriate, but it further limits the strength of the comparison.

3. **The relationship between the ARank-based layer selection (Sec. 4.1) and the fixed "last 12 layers" implementation (Sec. 5.1) is not explicitly reconciled.** The method section describes a general procedure: compute ARank per layer and select the half with lowest values. The implementation section simply says "transform the last 12 layers into MoD layers." For Show-o (24 layers), half = 12, and Fig. 3 shows ARank decreasing in later layers, so these descriptions are likely consistent — but the paper never explicitly confirms this alignment or reports which layers were actually selected. This makes it unclear whether the ARank computation is used for layer selection in practice or whether "last 12 layers" is a fixed heuristic.

4. **Table 1 reports GQA = 0.0 when layer 3 is skipped, which appears implausible.** Skipping a single transformer layer (layer 3) in a 24-layer model destroying all understanding capability while skipping layer 1 achieves 35.0 is unusual and demands explanation. If this is a real effect, an interpretation is needed; if an experimental artifact (e.g., a model crash on that run), it should be noted.

5. **The dramatic GenEval jump from Basic MoD (0.15) to "w/o task-aware router" (0.50) at identical TFLOPs and pruning rate is unexplained.** Both use a single router and the same 40.8 TFLOPs budget, differing only in *which layers* are pruned (interleaved vs. ARank-selected). A 0.15 → 0.50 improvement from layer selection alone is a strong finding that the paper does not discuss. It is also consistent with the broader point that layer selection matters more than task-specific routing, but the paper should explicitly address it.

6. **The paper does not specify how the three MoD block types (T2I MoD, MMU MoD, Shared MoD) are distributed across the 12 MoD layers** — which layers become which type, and what fraction are shared vs. task-specific. This level of detail is needed for reproducibility and for understanding the method's capacity allocation.

### Trivial

- Table 4's "Training Cost" column mixes measurement units ("1.30x/iter & 67G") without clarifying what "1.30x" is relative to.
- No variance or error bars are reported for any benchmark numbers, making it unclear whether small differences are within noise.

---

## Nice-to-Haves

- A matched-FLOP comparison between UniMoD and a single-router variant (by giving the single-router model a smaller pruning ratio to match compute) would cleanly isolate the effect of task-specific routing.
- A comparison against vanilla MoD (Raposo et al., 2024) at matched FLOPs and matched layers would strengthen the evaluation, as the current baselines (early exit and interleaved skipping) are not competitive token pruning methods.

---

## Removed Points

These points are flagged to be removed; treat them with caution.

- **"Insufficient related work or missing comparison with MoMa"** — The paper already discusses MoMa (Lin et al., 2024b) in Sec. 2.2 and differentiates its contribution. Missing related work critiques are removed per instructions.
- **"Gumbel-Softmax auxiliary loss details deferred to appendix"** — The appendix is stripped by the parser; this is not an author error.
- **"Scalability and diffusion model claims deferred to appendix"** — The same appendix-stripping issue applies.
- **Criticism that "single router (w/o task-aware) at 40.8 TFLOPs is more efficient than UniMoD at 43.3 TFLOPs" used to argue this is fatal.** This conflates a legitimate ablation observation with an invalidating claim. The single-router variant uses a different pruning strategy that reduces throughput at different layers — the TFLOPs difference is small (2.5 TFLOPs, ~6%) and the method's value on generation tasks (GenEval +0.11) is real. This is a framing issue, not a fatal flaw.
- **Criticism about ARank analysis covering 4 models but experiments only on 2** — The paper evaluates on Show-o (diffusion+AR) and Emu3 (full AR), covering both architectural categories of unified transformers. This is sufficient scope for the claims made.

---

## Novel Insights

The most interesting observation to emerge from the review is the asymmetry in the ablation: **layer selection (ARank) accounts for nearly all understanding-task gains, while task-specific routers account for the generation-task gains (GenEval).** This suggests the two components address different failure modes — the layer switch module protects understanding by pruning only the most redundant layers, while separate routers protect generation by preventing generation tokens from being outvoted by understanding tokens. The paper's current framing treats both as part of a unified "task-aware" solution, but the evidence points to a more modular explanation. This insight is not surfaced in the paper itself.

---

## Suggestions

- Reframe the paper's contribution more precisely: the key finding is that ARank-based layer selection is the primary efficiency driver for understanding tasks, while task-specific routers primarily benefit generation tasks. Update the abstract and conclusion accordingly.
- Add a matched-FLOP ablation comparing UniMoD against a single-router variant with a smaller pruning ratio to equalize compute.
- Explain the GQA=0.0 result at layer 3 (Table 1) — this needs either a substantive interpretation or a correction.
- Report which specific layers were selected by the ARank procedure and how they map to the three block types (T2I/MMU/Shared MoD).

---

## Score and Decision

MY FINAL SCORE: <score>5.0</score>
MY FINAL DECISION: <decision>Reject</decision>