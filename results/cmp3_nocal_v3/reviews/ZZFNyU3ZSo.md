## Summary

This paper proposes UniMoD, a task-aware token pruning method for unified multimodal transformers (models handling both generation and understanding tasks). Through diagnostic experiments on attention weights, ARank-based redundancy profiling, and task interaction analysis across four unified transformer architectures (Show-o, JanusFlow, Emu3, Lumina-mgpt), the authors find that token redundancy patterns differ across tasks and layers. They introduce separate routers per task with ARank-guided layer selection and pruning ratios, converting dense layers into three specialized MoD block types (T2I, MMU, Shared). Applied to Show-o and Emu3, the method reduces training FLOPs by 15% and 40% respectively while maintaining competitive benchmark performance.

## Strengths

- **Diagnostic empirical analysis (Sec. 3) is the paper's most distinctive contribution.** The paper runs three diagnostic experiments — attention weight analysis, ARank-based redundancy profiling, and competitive token pruning — across four unified transformer architectures. This surfaces a non-trivial finding: token redundancy patterns differ between tasks even for tokens of the *same* modality (image tokens in generation vs. understanding), and this links to the modeling approach (diffusion vs. autoregressive). Most efficiency papers jump straight to method design without this diagnostic grounding.

- **Core method follows directly from the evidence.** The three-way architecture (T2I MoD layer, MMU MoD layer, Shared MoD layer) with task-specific routers is a natural consequence of the empirical observation that single-router MoD fails because tasks have divergent redundancy profiles. The design is clean and principled.

- **Non-trivial FLOP reductions with bounded performance loss.** 15% FLOP reduction on Show-o (1.4B) and 40% on Emu3 (8.5B) are meaningful numbers. The ablation (Tab. 5) shows that naive MoD collapses generation quality (GenEval 0.15 vs. 0.62 baseline), while the full method recovers to 0.61 — close to the no-pruning baseline — demonstrating that the specific design choices matter.

## Weaknesses

### Major

- **The main results table (Tab. 3) compares against weak baselines, which inflates the apparent advantage.** The two baselines shown (EarlyExit at layer 12, Interleaved Layer Skipping) are simple heuristics that one would expect to perform poorly. The paper does include relevant comparisons — a "Basic MoD" variant (naive application) and a "w/o task-aware router" variant (single router at ARank-selected layers, essentially a γ-MoD-like baseline) — but these are relegated to a separate ablation table (Tab. 5) with a different metric set and never appear alongside the headline results. Notably, the "w/o task-aware router" ablation achieves performance within 0.1–0.7 points of UniMoD on GQA, POPE, MMMU, and VQAv2 (Tab. 5), and the method's advantage concentrates in MME (+41.7) and GenEval (+0.11). Having the most natural baseline comparisons in a separate table makes the main results look stronger than the ablation data supports. The claim "our method achieves the best balance between performance and efficiency" (line 242) would be better supported by integrating the single-router MoD baseline into Tab. 3.

### Minor

- **No variance or confidence intervals reported.** Every benchmark result in Tabs. 3, 4, and 5 is a single point. Many differences between UniMoD and the full-computation baseline (or between UniMoD and the "w/o task-aware router" ablation) are 0.1–2.1 points (e.g., GQA 56.3 baseline → 54.5 UniMoD, a 1.8-point drop; VQAv2 68.3 → 66.2, a 2.1-point drop; MMMU 25.8 → 25.7). Without error bars or multiple runs, the reader cannot assess whether these small deltas are meaningful or noise. Adding variance estimates would substantially strengthen the paper's central claim of "maintaining or improving performance."

- **Training cost metric in Tab. 4 is unclearly defined.** The column reports values like "1.30x/iter & 67G." The "G" presumably means GB of GPU memory, but "1.30x/iter" is unexplained — does "x" denote a ratio (relative to what?), and what does "/iter" measure (seconds per iteration, throughput, normalized wall-clock time)? Since the paper's title emphasizes efficiency, this metric must be transparent for the efficiency claims to be independently evaluated.

- **The Emu3 results rest on a reimplementation whose fidelity is not validated.** The paper states (line 242) that "our full Emu3 results differ from the original paper because we use alternative training datasets, as the official code and data are not publicly available." This means both the "Emu3" baseline and "UniMod" in Tab. 3 come from the authors' reimplementation, not the published model. The 40% FLOP reduction claim is relative to this reimplementation, and without knowing how close it is to the original Emu3's published numbers, the significance is unclear. The paper should report how the reimplementation compares to published Emu3 results and verify that it provides a reasonable reference point.

- **The GQA score of 0.0 when skipping layer 3 (Tab. 1) needs explanation.** A score of 0.0 on a QA benchmark suggests a complete computational breakdown, not merely degraded quality. The paper uses this result as evidence that "early layers are more critical," but the extreme discontinuity (35.0 for layer 1, then 0.0 for layer 3, then 48.0 for layer 5) raises a methodological question: were these inference-time skips on a model trained without skipping (an out-of-distribution intervention that can cause arbitrary behavior), or is there a specific failure mode at layer 3? Clarifying this would strengthen the diagnostic analysis.

- **Pruning schedules and per-layer capacities are not specified precisely enough for reproduction.** Section 5.1 describes pruning for the MMU task as "scale the capacity from 1 down to 0.2" and for T2I as "prune 20% of the tokens in the later layers" without giving the exact per-layer schedule or a precise formula. This vagueness makes independent reproduction harder than necessary.

### Trivial

- **Naming inconsistency:** The paper's title, abstract, and text use "UniMoD" (uppercase 'D'), but Tab. 3 and Tab. 4 use "UniMod" (lowercase 'd'). This should be unified.

## Nice-to-Haves

- An ablation using task-aware routers *without* ARank-based layer selection (e.g., at random layers) would isolate the contribution of ARank-guided selection from the task-aware design and strengthen the ablation story.
- The "w/o task-aware router" ablation could be included directly in Tab. 3 to give the reader a direct visual comparison against the closest natural baseline.

## Removed Points

These points were raised in the input review but are removed for the reasons given:

- **Tab. 2 missing entries ("Only MMU" has no GenEval):** This is natural experimental design — a model trained only on MMU cannot generate images. The reviewer's concern reflects a misunderstanding of the table purpose.
- **Inconsistency between "half of layers" (Sec. 4.1) and "last 12 layers" (Sec. 5.1):** Show-o has 24 layers; the last 12 are half the layers. These are consistent. The ARank charts (Fig. 3) confirm later layers have lower ARank, so "last 12" and "lowest ARank" align.
- **Criticism that "significant fraction of supporting evidence" is in the appendix:** The appendix contains extended results (8B scaling, diffusion models, Pareto analysis). Main papers routinely defer such results to appendices. Furthermore, the parser strips the appendix from the review copy; the authors' original submission contains it.
- **"First work" claim about task-aware token pruning:** The claim is qualified ("first work to propose a *task-aware* token pruning method for unified transformers"). MoMa applied MoD to Chameleon but without task-specific routers. Whether one finds the qualifier convincing is a rhetorical judgment, not a factual error.
- **Request for "w/o task-aware router" ablation at interleaved (not ARank-selected) layers:** This would be a useful additional ablation but is a nice-to-have, not a missing piece that undermines the paper.

## Novel Insights

The synthesis of the three diagnostic analyses (attention weight patterns, ARank-based redundancy, and competitive token pruning) across four distinct unified transformer families yields two genuinely non-obvious findings: (1) token redundancy patterns differ between generation and understanding tasks even for the *same visual tokens* in the same model, and (2) this divergence is driven by the modeling paradigm (diffusion vs. autoregressive), not just the modality. The harsh critic's framing of the diagnostic section as the paper's most distinctive contribution is correct — these observations are valuable beyond the specific method they motivate. No additional novel insight emerges from the review beyond what the paper already surfaces.

## Suggestions

1. Add the "w/o task-aware router" (single-router MoD at ARank-selected layers) as a row in Tab. 3, or at minimum state explicitly that this ablation achieves competitive results on several understanding benchmarks and discuss why.
2. Report variance or confidence intervals for key benchmarks, or at minimum disclose the number of runs per configuration.
3. Clarify the "1.30x/iter" metric: specify absolute units (seconds per iteration), the reference point for the ratio, and throughput details.
4. Add a column or footnote showing how the Emu3 reimplementation compares to published Emu3 numbers on the benchmarks that overlap.
5. Explain the GQA 0.0 result in Tab. 1: was this inference-time layer dropping on a model not trained for skipping? Does the model produce degenerate outputs or crash?
6. Provide the exact per-layer capacity schedule (a table or formula) for both tasks in the main paper, not only in the appendix.

## Score and Decision

<score>6</score>
<decision>Accept</decision>

**Rationale for score 6 / Accept:** The paper makes a genuine contribution through its diagnostic analysis of token redundancy in unified multimodal transformers — this is the kind of empirical grounding that the efficiency literature too often skips. The method is simple, well-motivated, and yields meaningful FLOP reductions (15–40%) with bounded performance loss. The weaknesses are fixable in revision: the baseline comparison in the main table should be strengthened by promoting the relevant ablation; variance reporting, metric clarity, and the Emu3 reimplementation context are presentation issues that do not invalidate the core ideas. The paper should not be rejected for these issues, but the authors should address them thoroughly in the camera-ready version.