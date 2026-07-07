Now let me draft the review before calibration.## Final Review

## Summary
UniMoD proposes a task-aware token pruning method for unified multimodal transformers (models handling both generation and understanding). Through empirical analysis of four unified models (Show-o, JanusFlow, Emu3, Lumina-mgpt), the authors identify that token redundancy varies significantly by task and layer, motivating separate per-task MoD routers and ARank-guided layer selection. Applied to Show-o and Emu3, the method achieves ~15% and ~40% FLOPs reduction respectively, with broadly maintained benchmark performance.

---

## Strengths
- **Multi-model empirical grounding (Sec. 3, Figs. 2–4).** The ARank analysis and competitive pruning experiments span four unified models and provide quantitative justification for both design choices—layer-selective pruning and task-specific routing—rather than post-hoc rationalization on a single model.
- **Clean ablation isolating the key contribution (Table 5).** The three ablation variants clearly show the task-aware router is the dominant contributor: GenEval degrades from 0.61 (full) → 0.50 (no task-aware router) → 0.15 (Basic MoD), demonstrating the proposed method is not merely an incremental configuration tweak.
- **Coverage of two architecturally distinct model families.** Applying the method to both Show-o (diffusion + AR) and Emu3 (fully AR) demonstrates that the design is not architecture-specific.
- **Mechanistically grounded FLOPs explanation.** The link between Emu3's larger token count (4096 vs. 1024 in Show-o) and its larger FLOPs savings is substantive and predictive, not ad hoc.

---

## Weaknesses

### Fatal
None.

### Major

- **Non-standard Emu3 baseline undermines the paper's strongest quantitative claim.** Sec. 5.2 acknowledges: "Our full Emu3 results differ from the original paper because we use alternative training datasets, as the official code and data are not publicly available." The baseline Emu3 reaches only 881.3 MME and 46.0 GQA—well below the original published numbers—indicating the model is either undertrained or trained on a mismatched data mixture (LLaVA-v1.5-mix-665K, designed for a different model family). When both the baseline and the proposed variant are trained under non-standard conditions that substantially depress baseline performance, it is impossible to determine how much of the 40% FLOPs savings is attributable to the method versus the training setup. The 40% reduction is the headline result in the abstract; the limitation should be prominently stated in a dedicated Limitations section rather than buried in a single sentence in Sec. 5.2.

- **No FLOPs-matched task-agnostic MoD comparison in Table 3.** The natural direct competitor for UniMoD is task-agnostic MoD (i.e., Basic MoD) applied to the same layers at the same FLOPs budget. This appears in the ablation (Table 5) but at **40.8 TFLOPs**, while UniMoD operates at **43.3 TFLOPs**—a different budget. The Table 3 baselines (Early Exit, Interleaved Layer Skipping) are demonstrably naive alternatives; neither tests the core claim that task-aware routing specifically beats task-agnostic routing at equal compute. A FLOPs-matched Basic MoD row in Table 3 is necessary to isolate whether the benefit is from the task-aware design or from the 6% larger compute allocation.

### Minor

- **Show-o performance drops are understated relative to abstract claims.** The abstract states UniMoD "maintains or improves performance." Table 3 shows: GQA 56.3→54.5 (−1.8), VQAv2 68.3→66.2 (−2.1), GenEval 0.62→0.61, with partial offsets from MME (+37.7) and DSG (+1.4). At only 15% FLOPs reduction, these drops are material; the selective framing obscures a meaningful tradeoff and should be more precisely qualified in the abstract and Sec. 5.2.

- **Layer selection description is ambiguous.** Sec. 4.1 (Layer Switch Module Step 1) states: "we select the half of layers with the lowest [ARank] values for each task." Sec. 5.1 states: "we transform the last 12 layers into MoD layers for both tasks." It is never clarified whether the last 12 layers coincidentally have the lowest ARank values (making the descriptions consistent) or whether the final implementation deviates from the ARank-guided procedure described in the method. This ambiguity matters because the ARank-based selection is presented as a principled design choice.

- **Shared MoD block contribution not evaluated.** Figure 5 introduces three block types: T2I MoD, MMU MoD, and Shared MoD. The ablation (Table 5) tests task-aware vs. single router but does not evaluate the Shared block independently. The assignment policy (which layers receive Shared blocks versus task-specific blocks) is not described in the main text, leaving this component opaque.

### Trivial
None.

---

## Nice-to-Haves
- A sensitivity analysis on ARank-guided layer selection showing what happens when different subsets of layers (not just the last 12) are chosen would confirm that the metric is doing useful selection work rather than approximating a manually tuned choice.
- A training-matched Emu3 baseline (same alternative data, same training steps, no UniMoD) constructed alongside the UniMoD variant would make the Emu3 FLOPs result internally valid even without access to official data.
- Brief discussion of whether the inference-time layer importance experiment (Table 1, skipping layers at inference) transfers to training-time MoD dynamics, since training with token pruning may differ from a simple inference skip.

---

## Removed Points
*These points are flagged as removed; treat them with caution.*

- **MoMa as a missing Table 3 comparison** (Harsh Critic): Removed per hard rule—do not criticize absence of specific related-work comparisons.
- **No variance / single-run statistics** (Harsh Critic): Removed — single-run evaluation is the community norm for large-scale multimodal benchmarks; this is a nice-to-have at best.
- **Task independence → separate routing logical gap (Sec. 3.4 / Table 2)** (Harsh Critic): Removed as substantially addressed; the competitive token pruning experiment (Fig. 4) directly shows cross-task imbalance under a shared router, providing the needed empirical bridge beyond Table 2 alone.
- **Inference-skip vs. training-time MoD discrepancy** (Harsh Critic): Removed from weaknesses; downgraded to a nice-to-have since the authors use Table 1 only to motivate layer ordering, not to equate inference skipping with training-time pruning behavior.

---

## Novel Insights
The competitive token pruning diagnostic (Fig. 4, Sec. 3.4)—where T2I and MMU tokens compete for router capacity using Gumbel-Softmax—is a genuinely clean lightweight protocol for diagnosing cross-task token imbalance without full training runs. This protocol could be broadly applicable as a pre-design tool when adapting any single-task efficiency method to a unified multimodal setting.

---

## Suggestions
1. Add a FLOPs-matched Basic MoD row to Table 3 (re-train Basic MoD at 43.3 TFLOPs for Show-o) so the task-aware router's contribution can be cleanly attributed.
2. Promote the Emu3 data-substitution caveat to a Limitations section in the main body with explicit discussion of which conclusions can and cannot be drawn from non-standard training.
3. Clarify in Sec. 5.1 whether "last 12 layers" is the ARank-guided output or a manual override, and provide the supporting ARank values.
4. Add a single ablation row (Shared MoD block removed) to Table 5 to justify its inclusion in the design.

---

## Score and Decision

**Anchor papers retrieved:**

| Path | Avg Score | Round | Comparison |
|------|-----------|-------|-----------|
| `IqGVIU4rvM.md` | 2.50 | R1 | VQ-VAE + diffusion tokenizer combo; much weaker analysis and no real FLOPs savings |
| `5ncdKonxd4.md` (PyramidDrop) | 3.00 | R1 | Visual token pruning for VLMs inference; simpler contribution, no training efficiency analysis |
| `cagNCwQEEN.md` | 3.40 | R1 | Hybrid SSM for multimodal LLMs; narrower scope |
| `DDxLsxiZR8.md` (CAT Pruning) | 4.00 | R1 | Token pruning for T2I diffusion only; weaker analysis, no unified-model scope |
| `SfZpk8CV9l.md` (PUMA) | 4.75 | R1 | Unified MLLM with multi-granular generation; comparable scope but weaker empirical analysis |
| `1xG3MN1RRW.md` (SparseVLM) | 5.20 | R1/R2 | Training-free token pruning for VLMs; similar topic but understanding-only, no training efficiency |
| `Acdd83rF1s.md` (LLM-VTP) | 5.80 | R1/R2 | Task-aware visual token pruning for video; comparable rigor, understanding-only scope |
| `oS79Tw3G0c.md` | 5.75 | R2 | Visual attention shrinking for video VLMs; comparable rigor, inference-only |
| `iIT02bAKzv.md` (ECoFLaP) | 5.50 | R2 | Layer-wise pruning for VLMs; somewhat comparable methodological depth, accepted |
| `jIAKjjEmWi.md` (A-MoD) | 4.00 | R2 | Alternative MoD routing; narrower and simpler contribution than UniMoD |
| `ym1dS37mZE.md` | 4.67 | R2 | Token grouping for MLLMs; comparable pruning topic, weaker analysis |
| `o6Ynz6OIQ6.md` (Show-o) | 6.50 | R1 | The base unified model; UniMoD extends it but is a narrower efficiency contribution |

**Round-1 bracket:** 4.5–6.0. UniMoD is clearly above the naive token-pruning papers (3.0–4.0) due to its multi-model empirical analysis and principled ablation. It sits below the Show-o base paper (6.5) and comparable unified-model papers accepted in the 6+ range, largely because it is a narrower efficiency contribution on top of existing models rather than a new unified model.

**Round-2 narrowing:** Papers like ECoFLaP (5.5, accepted) and SparseVLM (5.2, rejected) are the closest in scope. UniMoD's multi-model analysis and clean ablation are stronger than SparseVLM's, but the compromised Emu3 baseline and missing FLOPs-matched comparison are real evidential gaps that prevent the Emu3 headline result from being taken at face value. The Show-o result (15% FLOPs savings with meaningful benchmark drops) is weaker than the abstract implies. This places the paper slightly below ECoFLaP territory. Final score: **5.0**.

MY FINAL SCORE: <score>5.0</score>
MY FINAL DECISION: <decision>Reject</decision>