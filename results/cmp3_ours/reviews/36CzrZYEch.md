## Summary

IRIS proposes using Negative Self-Certainty (NSC) — the negated KL divergence between the model's output distribution and a uniform distribution — as an intrinsic reward signal for fine-tuning autoregressive text-to-image (T2I) models via GRPO. The key empirical insight is that T2I models, unlike LLMs on reasoning tasks, benefit from *minimizing* self-certainty (maximizing uncertainty). The method achieves results competitive with external-reward methods (T2I-R1) on GenEval, T2I-CompBench, and WISE without requiring human labels or domain-specific verifiers.

## Strengths

1. **Core observation is genuinely interesting and empirically grounded.** Figure 2 shows that RL alignment increases self-certainty for an LLM on math reasoning but *decreases* self-certainty for a multimodal LLM on T2I. This directional difference is well-motivated (objective correctness vs. subjective richness) and makes the paper's central intuition more substantive than a re-packaged entropy maximization trick.

2. **No external supervision is a real practical advantage.** A method that improves T2I generation using only the model's own output distribution, without requiring human preference labels, object detectors, VQA models, or domain-specific verifiers, is appealing for scalability and generality.

3. **Ablation study is thorough and well-designed.** Section 4.3 systematically ablates: CoT usage (Fig. 5), image SC direction (Fig. 6), text SC direction (Fig. 7), forward vs. backward KL (Fig. 8), and RL vs. direct optimization (Fig. 9). Each condition is cleanly isolated, and the results support the design choices made (e.g., direct optimization collapsing shows the RL framework is necessary, not decorative).

4. **Clear, well-motivated narrative.** The paper's structure — observe phenomenon → hypothesize → design method → validate with ablations → compare to baselines — is logical and easy to follow, with the contrast to the LLM case used effectively throughout.

## Weaknesses

### Fatal
None.

### Major
None.

### Minor

1. **Framing overstates results relative to the evidence.** The abstract claims IRIS "achieves performance that is competitive with or superior to external rewards." In practice, Table 1 shows IRIS *consistently trails* T2I-R1 on *overall* scores across all three benchmarks for both model sizes (GenEval: 0.72 vs. 0.75 for 1B, 0.77 vs. 0.78 for 7B; WISE: 0.37 vs. 0.38 for 1B, 0.48 vs. 0.50 for 7B). The "9.1%, 13.3%, and 28.8%" improvements cited in the introduction are relative to the *base model*, not the external-reward baseline, but this is not made explicit in the surrounding prose. The paper's genuine contribution — achieving results close to external-reward methods without requiring any external supervision — is strong enough that this overclaiming is unnecessary and distracting.

2. **"Best checkpoint" reporting inflates apparent performance and weakens evidence for the 7B model.** Table 1 reports peak scores selected from checkpoints between 100 and 800 steps rather than final converged performance (line 144). While Fig. 3 provides learning curves for the 1B model showing stable behavior, no comparable curves are provided for the 7B model. This matters because the ablation studies (Figs. 6–9) reveal that several configuration variants collapse after ~200 steps. Without 7B learning curves, it is not possible to verify whether IRIS on the larger model maintains stability or degrades at later steps.

3. **The causal attribution to improved "reasoning" capabilities is not directly evidenced.** The paper claims IRIS "can significantly enhance the reasoning capabilities of T2I models" and that it "improves reasoning and planning capabilities" (Sec. 1, line 44). The evidence for this is higher benchmark scores. However, better scores could arise from increased output diversity (improving the chance that some generations score well on automated metrics) rather than from improved reasoning or planning. The paper does not isolate reasoning ability as a measured variable; it measures downstream benchmark performance and attributes the improvement to reasoning without direct evidence of the causal mechanism.

4. **The explanation for why direct optimization collapses is too vague.** The direct optimization ablation (Fig. 9) is informative — it shows that directly maximizing NSC leads to model collapse while the GRPO-based version maintains performance. The paper's explanation ("GRPO employs a more conservative strategy," line 262) does not identify which component of GRPO (advantage normalization, clipping, or group sampling) prevents collapse. Since the direct objective already includes the KL penalty term (Eq. before line 261), understanding which mechanism is critical would strengthen the theoretical contribution.

### Trivial
- The CoT example in Fig. 4 shows the model generating longer descriptions but provides no analysis showing these CoTs contain better *reasoning* (rather than just more verbiage), which is related to weakness 3 above.

## Nice-to-Haves

- **Human evaluation** would strengthen the evidence that automated metric improvements correspond to genuinely better images, rather than reflecting a diversity-vs.-correctness tradeoff. The paper relies entirely on three automated benchmarks plus four reward models for ablations.
- **Statistical significance testing** for the differences between IRIS and T2I-R1 in Table 1 would clarify whether the small gaps on several sub-metrics (e.g., GenEval: IRIS 0.72±0.01 vs. T2I-R1 0.75±0.01) are meaningful.
- **Quantifying the impact of the chat template fix** (lines 120–121) on numerical values would help contextualize comparisons to the original T2I-R1 paper's reported numbers.

## Removed Points

These points were raised in the input review but are not included as weaknesses in the final review:

- *"Mechanism is straightforward entropy/diversity maximization, framed as more novel"* — This is a characterization of framing style, not an identifiable error or gap. The paper defines NSC explicitly in Eq. (2) and validates design choices empirically. The reviewer's re-description does not identify a factual problem.
- *"Forward KL justification not explained or tested with IRIS-specific data"* — The paper does test this: Fig. 8 ablates forward vs. backward KL and shows forward KL outperforms backward KL. The theoretical justification references external works (Fang et al., 2024; Kang et al., 2025; Zhao et al., 2025b) as context, which is standard practice.
- *"No human evaluation"* — Moved to Nice-to-Haves. The paper already evaluates on three diverse benchmarks plus four reward models for ablation; human evaluation is a strengthening addition, not a core gap.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. Revise the abstract and introduction to clearly distinguish improvements over the base model from comparisons to external-reward baselines. "Competitive with" is accurate; avoid any phrasing that implies blanket superiority over external-reward methods.
2. Report final-checkpoint performance alongside or instead of best-checkpoint numbers in Table 1, or provide learning curves for the 7B model comparable to those in Fig. 3.
3. Tone down or better evidence the "reasoning capabilities" attribution, or add an analysis that isolates reasoning improvements (e.g., measuring CoT quality or planning accuracy independently).
4. Investigate which component of GRPO (advantage normalization, clipping, or group sampling) prevents the direct optimization collapse and discuss the mechanism more precisely.

## Score and Decision

### Calibration Anchors

All anchors are from the deepreview_13k_calibration corpus.

| Path | Avg Score | Round | Comparison |
|---|---|---|---|
| `Let8OMe20n.md` (Confidence-aware Reward Opt. for T2I) | 6.00 | R1 (3.5–5.5) | Similar domain (T2I + reward optimization). IRIS has a more novel core insight (modality-dependent self-certainty direction) but weaker framing clarity. Comparable quality. |
| `bO31lfEdos.md` (Mitigating Object Hallucination w/ Human-Free RL) | 5.00 | R1 (3.5–5.5) | Similar spirit (RL without human supervision). IRIS is stronger: evaluates on 3 benchmarks × 2 model sizes with thorough ablations. |
| `kIP0duasBb.md` (Test-Time Adaptation with CLIP Reward) | 6.67 | R1 (5.5–7.5) | Uses RL with an external CLIP reward model. IRIS is more novel (truly intrinsic signal vs. relying on an external CLIP model). Comparable quality. |
| `4w99NAikOE.md` (IterComp: Iterative Composition-Aware Feedback) | 6.80 | R1 (5.5–7.5) | T2I with reward feedback learning. Stronger empirical results; less novel core idea. Roughly comparable. |
| `MeGDmZjUXy.md` (Moral Alignment for LLM Agents) | 6.33 | R2 (3.5–7.5) | Different domain but similar approach (intrinsic rewards without human feedback). Comparable. |

**Round 1 bracket:** 5.5–7.5 (based on comparison to the five anchors above, IRIS sits in the lower-to-middle of the Accept range).

**Narrowing:** Among the Accept-range anchors, IRIS's closest comparators are "Confidence-aware Reward Optimization" (6.00) and "Moral Alignment" (6.33). IRIS has a more novel empirical observation than either, but its framing issues and missing 7B learning curves hold it back. This places it near the lower end of the Accept range.

**Final calibrated score:** 6.0

MY FINAL SCORE: <score>6.0</score>
MY FINAL DECISION: <decision>Accept</decision>