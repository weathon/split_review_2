I have thoroughly verified all claims against the paper. Let me produce the final review.

## Summary

This paper formalizes Dual-level Noisy Correspondence (DNC) — noise at both intra-entity (entity-attribute) and inter-graph (entity-entity and attribute-attribute) levels — as an under-explored problem in Multi-Modal Entity Alignment (MMEA). It proposes RULE, a framework that: (1) estimates correspondence reliability via a two-fold principle combining uncertainty (evidential deep learning) and consensus; (2) uses these reliabilities for robust attribute fusion (DRF) and robust inter-graph discrepancy elimination (DRL); and (3) incorporates a test-time MLLM-based reasoning module (TTR). Experiments on five benchmarks with injected noise show consistent gains over seven baselines.

## Strengths

- **Novel and well-motivated problem formulation.** DNC is a genuine gap in the MMEA literature — the paper is the first to formalize dual-level noise, and it provides evidence (over 50% NC in real benchmarks) that this is practically relevant. The distinction between intra-entity and inter-graph noise is not merely taxonomic; the paper shows (Figure 1b) they corrupt different pipeline stages.

- **Theoretically principled two-fold reliability principle.** Theorem 1 correctly identifies that low uncertainty does not guarantee correct correspondence (the highest belief mass may not fall on the annotated match), which motivates adding consensus as a second principle. The grounding in Dempster-Shafer theory and subjective logic is appropriate, and the combination of uncertainty + consensus is a non-trivial extension beyond standard evidential deep learning.

- **Consistent and substantial empirical gains.** On the Non-name setting (Table 1), under inherent DNC, RULE achieves 73.8% avg H@1 vs. next best 68.6% (+5.2 pts); under 50% injected DNC the gap widens to 10.3 pts (64.3% vs. 54.0%). The ablation (Table 3) shows that even without the MLLM-based TTR module, RULE w/o TTR (56.5% H@1 on ICEWS-WIKI 50% DNC, Non-name) substantially outperforms the best baseline (MEAformer at 42.4%). Gains hold across all five datasets and all three noise levels.

- **Clear ablation structure.** Table 3 decomposes contributions of each module (DRL, DRF, TTR, uncertainty-only, consensus-only), confirming each component contributes positively and the two principles together outperform either alone.

## Weaknesses

### Fatal
None.

### Major

- **Comparison asymmetry from the MLLM-based TTR module is not adequately disentangled in the main evaluation.** The TTR module uses Qwen2.5-VL-72B-Instruct (72B parameters) at inference time via chain-of-thought reasoning (Eq. 15-16). None of the seven baselines use any LLM or MLLM at any stage. The paper states "For fair comparisons, we adopt the same backbone (i.e., CLIP)" — this refers only to the initial feature extractor, not the inference-time module. The main comparison tables (Tables 1-2) present full RULE (with TTR) against baselines without such resources, conflating the training-time contribution with the MLLM's capability. The ablation in Table 3 partially addresses this on one dataset (ICEWS-WIKI), showing w/o TTR (56.5% H@1, Non-name) vs. Default (58.2%), but this decomposition should be in the main tables across all datasets. **This does not invalidate the core contribution** — the training-only method still substantially outperforms baselines — but the current presentation prevents readers from cleanly separating the two effects.

- **The greedy yᵢ estimator used at inference is underspecified and unvalidated.** During inference, the consensus score (Eq. 5: cᵢ = max(0, sᵢ · yᵢ)) requires ground-truth correspondence yᵢ, which is unavailable. The paper proposes a greedy attribute-selection strategy (Eq. 6-7) resting on Assumption 1 (Δ ≥ 0 for correct attributes, Δ < 0 for irrelevant ones) — a strong monotonicity condition that is neither analyzed nor validated. The one-hot conversion at the end (yᵢ = one-hot(arg max ...)) discards distributional uncertainty, contradicting the evidential framework's design. The paper reports **no empirical evaluation** of how often the estimated yᵢ matches the true yᵢ or how estimation errors propagate to the consensus score and final reliability. Since yᵢ estimation is critical for the consensus principle during inference, this omission is significant.

- **No error bars or multiple-run statistics despite random noise injection.** All experiments involve random noise injection (entity-entity NC, entity-attribute NC, attribute-attribute NC), yet results are single numbers without standard deviations, confidence intervals, or multiple-run statistics. Given the stochastic nature of the injected noise, single-run results are insufficient to quantify the uncertainty around the reported conclusions.

### Minor

- **The attribute-level reliability wᵢᵐ is not specified.** The DRF module (Eq. 14: zᵢ = ⊕ₘ (wᵢᵐ · zᵢᵐ)) weights attribute representations by wᵢᵐ, but the paper never defines how wᵢᵐ is computed from the entity-level reliability framework (Eq. 1). It states "the inter-graph reliability wᵢᵐ could be employed" (line 166) without specifying the mapping. This is a reproducibility gap.

- **No computational cost analysis of the TTR module.** Using a 72B-parameter MLLM at test time via chain-of-thought prompting has nontrivial computational implications. The paper reports no inference latency, GPU memory requirements, or API costs, which are relevant for assessing practical deployability.

### Trivial
None.

## Nice-to-Haves

- The hard filtering of high-uncertainty pairs (indicator I(i ∉ Sᵤ) in Eq. 11 drops them entirely from the loss) is a design choice that early in training risks discarding hard-but-clean examples; a soft weighting variant could be ablated for completeness.
- Validating the greedy yᵢ estimator against ground-truth on a held-out validation set would substantially strengthen the inference pipeline.

## Removed Points
These points were raised in the input review but removed per filtering instructions:
- **"DBP15K columns labeled GEN repeatedly"** — parser artifact, not author error.
- **"Misidentification example conflates attribute-attribute with entity-entity alignment"** — the example is a reasonable illustration of how attribute-level confusion causes entity-level misalignment.
- **"Eq. 2 uses unusual exp-tanh composition"** — a design choice observation, not a weakness.
- **"Missing related works"** — cannot be verified without external sources.
- **"Appendix details stripped"** — parser artifact, not author error.
- **"Should add baselines with MLLM"** — impractical for a conference paper; the ablation already provides the essential decomposition.

## Novel Insights
None beyond the paper's own contributions. The reviews primarily surface presentation and validation gaps rather than providing new conceptual perspectives on the method.

## Suggestions
1. Add "RULE (w/o TTR)" as a separate row in Tables 1-2 so readers can clearly see the training-time contribution across all datasets.
2. Validate the greedy yᵢ estimator empirically — report accuracy against ground-truth on a validation set and analyze when Assumption 1 holds or breaks.
3. Report all main results with error bars over at least 3 random noise-injection runs.
4. Specify how wᵢᵐ is derived from the reliability framework (or from hᵢᵐ).
5. Add a discussion of the MLLM's computational cost (inference latency, GPU/API costs) and acknowledge the comparison asymmetry in the main text.

## Score and Decision

This paper identifies a genuinely new and important problem and proposes a technically substantive solution. The core training-time contributions (two-fold reliability principle, DRL, DRF) are sound, well-motivated, and supported by data — even without the MLLM, RULE substantially outperforms all baselines. The main weaknesses are in presentation clarity (the MLLM comparison asymmetry is not adequately decomposed in the main tables), missing validation of one inference component, and absent statistical significance reporting. These are addressable and do not undermine the core contribution.

MY FINAL SCORE: 7.5
MY FINAL DECISION: Accept