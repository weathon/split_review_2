## Summary

This paper proposes UniMoD, a task-aware token pruning method for unified multimodal transformers that handle both generation and understanding tasks. Based on empirical analysis of attention weights, ARank (token redundancy), and task interactions across four unified transformers (Show-o, JanusFlow, Emu3, Lumina-mgpt), the authors identify that token redundancy varies across layers and tasks — especially when generation uses diffusion and understanding uses autoregressive modeling. UniMoD uses task-specific routers with different capacities to prune tokens separately per task. Applied to Show-o and Emu3, the method reduces training FLOPs by ~15% and ~40% respectively while maintaining or slightly improving performance on several benchmarks.

## Strengths

1. **Task-specific router design directly validated by ablation (Table 5).** The ablation provides direct evidence that separate routers per task are the mechanism behind the gains: removing task-aware routers drops GenEval from 0.61 to 0.50 and MME from 1093.7 to 1052.0 at comparable FLOPs, while "w/o layer switch module" shows the layer selection component also matters independently.

2. **Empirical analysis across four models and two task types (Section 3).** The analysis systematically measures attention weights, ARank values, and task competition in Show-o, JanusFlow, Emu3, and Lumina-mgpt. The finding that ARank patterns diverge between diffusion-based generation and autoregressive understanding (Observation 3, Fig. 3) is a concrete insight that prior MoD work on MLLMs (γ-MoD, VideoLLM-MoD) did not address, since they focused on settings where tasks share the same modeling paradigm.

3. **Generalization across two architecturally distinct unified transformers (Table 3).** Results on Show-o (diffusion+AR, 1.4B params) and Emu3 (fully AR, 8.5B params) show the method is not architecture-specific. FLOPs reductions are substantial (15% for Show-o, 40% for Emu3) with maintained or slightly improved performance on multiple benchmarks.

## Weaknesses

### Major

1. **Disconnect between the described ARank-based procedure and the actual heuristic implementation.** Section 4.1 describes a three-step Layer Switch Module: compute ARank per layer, select the half of layers with lowest values per task, normalize ARank scores by sequence length to derive pruning ratios. However, Section 5.1 states: *"we transform the last 12 layers into MoD layers for both tasks"* — a fixed positional selection, not the output of an explicit ARank-based selection. The pruning ratios are also set by hand (*"scale the capacity from 1 down to 0.2"* for MMU, *"prune 20% of the tokens"* for T2I, *"80% token pruning in the last 16 layers"* for Emu3). The paper does not clarify whether the ARank procedure produced these same choices or whether the heuristic is an independent simplification. Since the method description claims a principled ARank-driven selection, the gap between what is described and what is actually run undermines confidence in the "Layer Switch Module" as a contribution. The authors should either (a) show that the ARank-selected layers match the last-12 heuristic and report pruning ratios derived from ARank normalization, or (b) reframe the method to honestly describe the heuristic.

### Minor

2. **No variance reporting or statistical significance for any result.** Every number in Tables 3, 4, and 5 is a point estimate without error bars, multiple seeds, or significance testing. Several changes are small (e.g., GQA 56.3→54.5, VQAv2 68.3→66.2, MME 1056.0→1093.7), making it impossible to assess whether differences reflect genuine effects or noise. Since the central claim is "maintaining or improving performance," some estimate of variance would substantially strengthen the paper.

3. **Weak baselines in the main results table (Table 3).** Early Exit and Interleaved Layer Skipping are generic efficiency methods, not adapted MoD baselines. The most directly relevant comparison — a single-router MoD handling both tasks — appears only in the ablation (Table 5). Since the paper's central thesis is that a single router is suboptimal for unified transformers, the single-router baseline should be in the main table.

4. **Emu3 results rest on a non-standard re-implementation.** The paper acknowledges this (*"Our full Emu3 results differ from the original paper because we use alternative training datasets"*). While the within-experiment comparison (baseline vs. UniMoD under the same training setup) is valid, the headline 40% FLOPs reduction claim is presented with weaker experimental grounding than the Show-o results. The re-implemented baseline's MMU scores (e.g., MME 881.3) are notably lower than typical original Emu3 numbers, and readers cannot assess how the re-implementation relates to the original model's performance.

5. **Missing direct comparison with γ-MoD.** The paper borrows the ARank metric from γ-MoD (Luo et al., 2024) and discusses it in Related Work but never compares against it experimentally. Since γ-MoD applies MoD to multimodal LLMs including understanding tasks, a direct comparison would contextualize UniMoD's contribution relative to the closest prior work and strengthen the case that task-specific routing is the key differentiator.

6. **Table 1 anomaly: skipping layer 3 causes GQA to collapse to 0.0.** A single layer whose removal causes total failure during inference is striking and unexplained. This deserves an explanation — either an architectural reason for layer 3 being uniquely critical, or a check for experimental artifact.

7. **Modest practical speed gains for Show-o (Table 4).** The 15% FLOPs reduction translates to only ~2–4% improvement in training speed (1.30x → 1.27x for T2I, 1.30x → 1.25x for MMU), with memory savings of 3–6 GB. The paper leads with FLOPs reduction as the headline metric, but the actual wall-clock and memory gains for Show-o are modest. The Emu3 results show more practical benefit but rest on the weaker experimental foundation noted above.

### Trivial

8. **Notation inconsistency between Eq. (2) and Eq. (4).** In Eq. (2), $D^l$ is the transformer layer and $R^l$ is the routing function. In Eq. (4) and its surrounding text, $D_t^l$ is called the "router function" and $R_t^l$ is called the "task-specific weight" — roles appear swapped relative to Eq. (2). The math still computes correctly, but the notation is confusing.

## Nice-to-Haves

- Adding a single-router MoD baseline to the main results table (Table 3) rather than only the ablation.
- Including the γ-MoD comparison to contextualize the contribution.
- Reporting results with 2–3 seeds for the Show-o experiments to provide variance estimates.

## Removed Points

- "Competitive token pruning observation does not directly imply separate routers are better" — The paper's Observation 5 is a descriptive finding about token importance under competition; the direct evidence for task-specific routers is in the ablation (Table 5). The observation motivates the design, and the ablation validates it — this is a standard and reasonable research flow, not a weakness.
- "Training cost should be presented differently" — FLOPs is a standard metric in the efficiency literature, and Table 4 also reports training speed and memory. This is a presentation preference, not a flaw.
- "Missing appendix results (scaling to more tasks, diffusion model adaptation)" — The parser strips appendix sections from all papers; these results exist in the original submission.
- Criticism about the competitive token pruning experiment not being precisely described — The paper states it uses "Straight-Through Gumbel-Softmax" with "router capacity to 0.5" and refers to Appendix A.6 for details. The description is adequate for the main paper.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. **Clarify the method-implementation relationship.** Either (a) report that the ARank-based selection produces the last-12-layers heuristic and use ARank-normalized pruning ratios, or (b) honestly reframe the method as a heuristic-informed design and remove the claim of an ARank-driven procedure. This is the most impactful fix the paper can make.
2. **Add a single-router MoD baseline to Table 3** to center the main comparison on the paper's core claim.
3. **Report results with at least 2–3 random seeds** for the Show-o experiments to provide variance estimates and support the "maintaining performance" claim.
4. **Include a direct γ-MoD comparison** in the experiments.
5. **Explain or investigate the Table 1 anomaly** (layer 3 → GQA 0.0).

## Score and Decision

SCORE: 6.0
DECISION: Borderline Accept

**Rationale:** The paper addresses a genuine problem — unified multimodal transformers are computationally expensive, and naive token pruning fails because different tasks have different redundancy patterns. The empirical analysis (Section 3) is thorough and yields genuinely useful observations. The core idea of task-specific routers with different capacities is clean, well-motivated by the analysis, and validated by a well-designed ablation study showing that both the task-aware router and the informed layer selection contribute to the gains.

However, the most significant issue is the disconnect between the described ARank-based layer selection procedure and the actual heuristic implementation — this undermines a key claimed contribution and must be resolved. The experimental evaluation also has gaps: no variance reporting, weak baselines in the main table, Emu3 results on a non-standard re-implementation, and no direct comparison with γ-MoD. These issues are all addressable without changing the paper's core claims. The paper is acceptable in principle with revision.

**Final calibration note:** The calibration database was unavailable during review. Score 6.0 reflects a paper with a sound core idea and reasonable evidence, but with presentation/validation gaps that prevent a higher score and are clearly fixable. The paper is above the rejection threshold (weaknesses do not invalidate the core contribution) but below a strong accept (gaps weaken the confidence in the claimed results).

MY FINAL SCORE: <score>6.0</score>
MY FINAL DECISION: <decision>Borderline Accept</decision>