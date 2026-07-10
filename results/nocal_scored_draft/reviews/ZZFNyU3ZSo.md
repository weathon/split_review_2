Now I have a clear picture. Let me assemble the final review.

## Summary

The paper proposes UniMoD, a task-aware token pruning method for unified multimodal transformers that handle both generation and understanding tasks. It first conducts an empirical analysis of attention patterns, layer importance, and token redundancy across tasks, then uses separate Mixture-of-Depths routers per task with task-specific capacities. The method is evaluated on Show-o (diffusion + autoregressive) and Emu3 (fully autoregressive), achieving 15% and 40% FLOPs reductions respectively with maintained performance.

## Strengths

- **Principled empirical motivation (Section 3).** The paper systematically investigates attention weight patterns (Fig. 2), ARank token redundancy across layers and tasks (Fig. 3), and task interactions (Fig. 4, Table 2), establishing that token redundancy differs across tasks and layers in unified transformers — providing evidence for *why* task-aware pruning is needed, rather than just proposing one.

- **Generality across model families.** The method is evaluated on Show-o (diffusion + autoregressive) and Emu3 (fully autoregressive), demonstrating applicability beyond a single modeling strategy.

- **Non-trivial FLOPs savings with maintained performance.** The 40% FLOPs reduction on Emu3 (89.0 → 53.5 TFLOPs) and 15% on Show-o with roughly comparable benchmark results are meaningful efficiency gains.

- **Well-structured ablation (Table 5).** The ablation decomposes the method into basic MoD, w/o layer switch, and w/o task-aware router variants, allowing readers to assess each design choice independently.

## Weaknesses

### Fatal
None.

### Major

**1. Method description vs. implementation discrepancy in layer selection.** Section 4.1 describes a principled ARank-based procedure that selects "the half of layers with the lowest values for each task." But Section 5.1 says they simply "transform the last 12 layers into MoD layers" (Show-o) and prune "in the last 16 layers" (Emu3) — a fixed choice based on layer index, not ARank-driven selection. The paper never states that the last N layers are in fact the ones with lowest ARank values, nor provides evidence that the fixed choice coincides with the data-driven selection. A reader following the method section would not end up with the system described in the experiments. This is a structural inconsistency that undermines trust in the paper's reported procedure.

**2. The ablation data tells a more nuanced story than the paper acknowledges.** The "w/o task-aware router" variant (single shared router) achieves nearly identical understanding performance (GQA 54.4 vs 54.5, POPE 80.2 vs 80.3, MMMU 25.6 vs 25.7, VQAv2 65.5 vs 66.2) at *6% lower* FLOPs (40.8 vs 43.3) than the full UniMoD. The only clear gap is on GenEval (0.50 vs 0.61). This suggests the primary value of task-aware routing is preserving generation quality, while understanding tasks are served nearly as well by a shared router. The paper mentions this variant "slightly worsens understanding results and severely degrades generation performance" but does not discuss the pattern that understanding scores are within noise of UniMoD while efficiency is better. This omission is significant because it directly bears on the paper's central claim that task-aware routing is essential.

### Minor

**3. Emu3 evaluation uses a substantially different training setup.** The paper states: "Our full Emu3 results differ from the original paper because we use alternative training datasets, as the official code and data are not publicly available." It is ambiguous whether the "Emu3" baseline row in Table 3 reflects the original model's numbers or a fine-tuned version on this alternative data. If both rows are fine-tuned on the same alternative data, the relative comparison is controlled but the absolute numbers do not reflect the original Emu3's capabilities. The headline 40% FLOPs reduction needs this caveat stated more prominently than a single sentence.

**4. Basic MoD's GenEval collapse (0.15) is unexplained.** Generation quality drops from 0.62 to 0.15 — a catastrophic failure. Understanding metrics also drop but far less dramatically (MME 1056→960). A drop of this magnitude suggests something structural went wrong (e.g., the basic MoD implementation removing tokens from generation sequences in a way incompatible with diffusion). The paper should explain this, as it bears on whether Basic MoD is a meaningful baseline or an inappropriate adaptation.

**5. Pruning ratio estimation lacks a concrete formula.** Section 4.1 says: "We approximate each layer's pruning ratio by normalizing its ARank score by the sequence length." No formula or worked example is given, so it is unclear how ARank values (range ~400–600 in Show-o) translate to concrete K values for Top-K token selection.

### Trivial
None.

## Nice-to-Haves

- **Compute-matched comparison.** The "w/o task-aware router" ablation runs at 40.8 TFLOPs (vs UniMoD's 43.3). A comparison at exactly matched FLOPs would cleanly isolate whether the task-aware router itself drives performance differences or simply different pruning distributions.
- **Variance reporting.** Many ablation differences are very small (GQA 54.4 vs 54.5, POPE 80.2 vs 80.3). While multiple seeds are expensive for large models, some indication of evaluation stochasticity would help interpret these differences.
- **FLOPs-to-wall-clock explanation.** A 15% FLOPs reduction on Show-o yields only ~2% faster training (Table 4). A brief note on why (e.g., attention is a small fraction of total compute) would prevent reader confusion.

## Removed Points

These points were flagged for removal from the input review; treat them with caution:

- **"First work" claim and MoMa discussion** — The paper discusses MoMa (line 67) and notes it "lacks results on generation tasks" and involves "only a simplistic combination." The differentiation is reasonable and the paper addresses this prior work.
- **Table 2 showing "absence of interaction"** — The paper claims the model accommodates both tasks without negative interference, which is what Table 2 shows. The motivation for task-specific pruning comes from the competitive token pruning experiment (Observation 5), not from positive task interaction.
- **Layer 3 GQA of 0.0 being suspicious** — The paper honestly reports this empirical result. Without additional information this is a data point, not a paper flaw.
- **Baselines consuming fewer FLOPs** — The comparison is valid: these aggressive baselines perform poorly. A compute-matched baseline would be a nice addition but is not required.
- **Missing γ-MoD experimental comparison** — γ-MoD is an MLLM method, not a unified transformer method. Its absence is a limitation but not a flaw in what is presented.
- **8B results "relegated to appendix"** — Appendix sections are stripped in this format; the paper states the results exist there.
- **No variance/statistical significance** — Moved to Nice-to-Haves since multi-seed runs for large multimodal model training is expensive and not standard practice in this sub-area.
- **FLOPs-to-wall-clock gap** — Moved to Nice-to-Haves since the paper points to the appendix for details.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

- Explicitly state whether the fixed "last N layers" choice coincides with the ARank-based selection described in Section 4.1, and provide evidence (e.g., mark the chosen layers on the ARank plot in Fig. 3).
- Discuss the ablation finding that task-aware routing mainly helps generation quality while a shared router serves understanding tasks nearly as well — either as a limitation or as a selective-application strength.
- Clarify whether the "Emu3" baseline row in Table 3 was trained on the same alternative data as UniMod or uses original paper numbers, and prominently caveat the absolute numbers.
- Add a formula or worked example for how ARank values translate to pruning ratios.

## Score and Decision

The paper makes a genuine empirical contribution through its systematic analysis of token redundancy in unified transformers, and the conceptual idea of task-aware routing is sensible. The experiments show real FLOPs savings. However, the paper has two significant weaknesses in its current form: (1) a structural inconsistency between the method description (principled ARank-based layer selection) and the implementation (fixed last-N-layers choice), and (2) the ablation data reveals that a single shared router achieves near-identical understanding performance with better efficiency — a pattern the paper does not honestly discuss, which undermines the central claim that task-aware routing is essential. With the method/implementation gap and the narrative-overclaiming issue, the paper in its current form is not ready for acceptance. The empirical analysis is valuable enough to warrant a major revision and resubmission.

MY FINAL SCORE: <score>4.0</score>
MY FINAL DECISION: <decision>Reject</decision>