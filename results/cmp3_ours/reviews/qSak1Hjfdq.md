## Summary

This paper formalizes the all-day multi-scenes lifelong VLN (AML-VLN) problem, where agents must continually learn across both scene and environmental/lighting conditions. The authors propose Tucker Adaptation (TuKA), using Tucker decomposition to represent multi-hierarchical navigation knowledge as a high-order tensor decoupled into shared core knowledge and scene/environment-specific expert factors. They also build the AllDay-Habitat simulation platform and develop the AllDayWalker agent, evaluated against 11 baselines across 24 navigation scenarios.

## Strengths

- **Well-motivated problem formulation:** The AML-VLN setting (lifelong learning across both scene and environment) is a natural and practically relevant extension of VLN, correctly identifying that existing lifelong VLN work focuses only on scene-level forgetting while real deployment requires adapting to both simultaneously (Sections 1–2).

- **Core technical idea is creative and non-obvious:** Using Tucker decomposition to decouple multi-hierarchical knowledge into a shared core tensor, scene experts, and environment experts, with an alignment mechanism (Eq. 3) that reduces the high-order tensor to a 2D weight matrix compatible with LLM backbones (Section 3.2).

- **Thorough baseline coverage:** Comparison against 11 methods spanning standard fine-tuning (Seq-FT, EWC-LoRA, LwF-LoRA), MoE-LoRA variants (Dense MoLE, Sparse MoLE, MoLA, HydraLoRA, BranchLoRA), orthogonal LoRA methods (O-LoRA, SD-LoRA), and test-time adaptation methods (FSTTA, FeedTTA). This is a comprehensive and well-chosen set (Tables 1–2, Section 5.2).

- **AllDay-Habitat benchmark extension (Section 4) is a practical contribution:** Using imaging models (atmospheric scattering, sensor noise models, saturation clipping) to synthesize degraded navigation environments from Habitat, enabling controlled evaluation across conditions that would be expensive to collect in the real world.

## Weaknesses

### Major

1. **Negative forgetting-rate values are unexplained and undermine the central forgetting analysis.** In Table 2, AllDayWalker achieves F-SR = −3% on T14 and F-SR = −4% on T20. By the definition in Eq. 13 (F-SR_t = (M-SR_t − SR_t) / M-SR_t), where M-SR_t is "the performance obtained when training solely on navigation tasks 1 through t" — a multi-task joint-training oracle that should constitute an upper bound — a negative value means the lifelong model outperforms the oracle. This is theoretically anomalous and the paper does not acknowledge or explain it. Without clarification, the reported forgetting rates (including the near-0% values claimed for AllDayWalker) are unreliable as evidence of forgetting mitigation. This is not a minor oversight; the forgetting metric is central to the paper's claim about addressing catastrophic forgetting.

2. **The expert retrieval mechanism (Section 3.4) is critical for task-agnostic inference but is never ablated or evaluated.** During inference in unknown scenarios, the agent matches observations to the correct scene expert (U³) and environment expert (U⁴) via CLIP feature similarity. This retrieval step is the bridge between training (where task-id is known) and testing (where it is not). Yet the paper provides no analysis of retrieval accuracy, no comparison against oracle expert selection or random baselines, and no study of graceful degradation under retrieval errors. The ablation studies (Section 5.3) focus entirely on tensor order and shared components, leaving this core component unevaluated. If the retrieval mechanism is unreliable, the reported task-agnostic test performance could be substantially overstated.

3. **No variance or statistical significance is reported for any result.** Tables 1, 2, 3, 4, and 5 all report single numbers without standard deviations, confidence intervals, or significance tests. VLN-CE results are known to be sensitive to random seeds, data ordering, and simulator stochasticity. Without any measure of variability, it is impossible to assess whether the large reported gaps (e.g., AllDayWalker 65% average SR vs. BranchLoRA 44%) reflect genuine improvement or a single favorable run. This is a basic expectation for experimental papers at this venue.

### Minor

1. **Parameter count transparency.** The paper states it keeps trainable parameters "comparable" across methods (line 231) but defers the actual comparison to Appendix C. TuKA uses rank settings r1=r2=8, r3=r4=64 with a core tensor G ∈ R^(8×8×64×64), while baselines use r=6 (LoRA) or r=16 with K=8 (MoE-LoRA). The main text should include a clear parameter count table to substantiate the "comparable" and "parameter-efficient" claims.

2. **Overclaimed "real-world deployments."** The third contribution bullet (line 28) states "additional real-world deployments also validate the superiority," but Table 5 evaluates on real-world *scene scans* used in simulation, not physical robot deployments in real environments. This wording overstates the evidence.

3. **Loss weighting λ = 1 − (λ1+λ2+λ3) is not justified** (Eq. 9). This forces the task prediction loss weight to decrease as regularization increases, coupling them in a way that complicates interpretation. No sensitivity analysis is provided for λ1, λ2, λ3.

4. **Which transformer weight matrices TuKA targets is unspecified.** The paper writes "the updated weight in the l-th layer" but does not specify whether TuKA replaces Q/K/V/O projections, MLP weights, or all linear layers, making the comparison to LoRA baselines imprecise.

### Trivial

None.

## Nice-to-Haves

- Per-task performance trajectories (a per-task accuracy matrix showing how performance on earlier tasks evolves as new tasks are added) would strengthen the forgetting analysis beyond the aggregate metrics reported.
- A capacity-controlled ablation (TuKA with smaller ranks matched to the LoRA baseline budget) would help disentangle whether the advantage comes from the tensor structure itself or from higher parameter capacity.

## Removed Points

These points from the harsh critic input are removed with justifications:
- "Notation uses same superscript l for layer and scenario" — minor formatting observation, does not affect paper validity.
- "Non-overlapping condition implications not discussed" — scope creep; the definition is clear and sufficient for the problem formulation.
- "M-SR may be undertrained" — speculative explanation that cannot be verified from the paper alone.
- "Section-by-section descriptive notes" — observations rather than concrete, verifiable weaknesses.
- Critic's specific numerical calculation of TuKA parameters (assuming 32 layers / hidden dim 4096) — these numbers may not match the actual Qwen2-7B architecture; the general transparency concern is kept in Minor.
- "Missing related work" — cannot be confirmed without external sources.
- "Missing trajectory of per-task performance" — moved to Nice-to-Haves.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

- Explain why F-SR takes negative values for the proposed method. If the multi-task oracle is undertrained, replace the metric with standard continual learning measures (backward/forward transfer) or properly train the oracle with sufficient budget.
- Add an ablation of the expert retrieval mechanism: compare learned retrieval vs. oracle expert selection vs. random selection, and report retrieval accuracy on held-out tasks.
- Report standard deviations across multiple random seeds for all main results.
- Provide a parameter count table in the main paper and consider a capacity-matched ablation.
- Clarify which specific weight matrices TuKA is applied to.
- Present SPL/OSR results as quantitative tables rather than only in radar charts (Figure 7).

## Score and Decision

**Calibration anchors (all rounds):**

| Path | Avg Score | Round | Comparison |
|------|-----------|-------|------------|
| `/home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/2oKkQTyfz7.md` (GSA-VLN) | 6.40 | R1 | VLN scene adaptation paper. Cleaner evaluation with standard metrics; accepted. This paper has a more fundamental metric issue, so scores lower. |
| `/home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/eWFkMCBySw.md` (CA-Nav) | 5.00 | R1 | Zero-shot VLN-CE paper. Rejected despite sound technical contribution; similar severity of issues. |
| `/home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/YR79EyejsG.md` (Task-Unaware Lifelong Robot Learning) | 5.75 | R1 | Lifelong robot learning. Rejected due to large uncertainties and presentation issues — comparable to this paper's missing variance and metric concerns. |
| `/home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/tpUEqmjZiS.md` (Primitive-level Skill Prompt Learning) | 4.50 | R1 | Lifelong robot manipulation. Rejected with methodology concerns. This paper's problem formulation and baseline coverage are stronger. |
| `/home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/EwFJaXVePU.md` (Scalable Lifelong Multimodal Instruction Tuning) | 6.50 | R1 | Lifelong multimodal LLM tuning. Accepted with minor weaknesses. This paper has more significant evidentiary gaps. |
| `/home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/9aZ2ixiYGd.md` (Vision and Language Synergy for Rehearsal Free Continual Learning) | 5.00 | R1 | Continual learning with vision-language models. Mixed reviews. |
| `/home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/rwmwFnmjAX.md` (Continual LLaVA) | 4.75 | R1 | Continual instruction tuning. Rejected. Similar setting but weaker contributions. |

**Round 1 bracket:** 4.5 – 6.0 (between the 4.50 skill prompt paper and the 6.40 GSA-VLN paper)

This paper has genuine strengths: a novel problem formulation that extends VLN in a practical direction, a creative technical approach (Tucker decomposition for multi-hierarchical knowledge decoupling), thorough baseline coverage, and a useful benchmark contribution. However, it has three significant evidentiary gaps: (1) the forgetting-rate metric produces negative values for the proposed method, which is theoretically impossible for a properly constructed oracle baseline — this directly undermines the paper's central claim about forgetting mitigation; (2) the expert retrieval mechanism, which is the critical bridge between training and task-agnostic testing, is never ablated or evaluated for accuracy; (3) no variance or statistical significance is reported for any result. These are not minor omissions; they affect whether the paper's core empirical claims can be trusted as presented. The problem formulation and technical idea are promising, but the evidence as currently presented does not fully support the claims.

**Score:** 5.0
**Decision:** Reject

MY FINAL SCORE: <score>5.0</score>
MY FINAL DECISION: <decision>Reject</decision>