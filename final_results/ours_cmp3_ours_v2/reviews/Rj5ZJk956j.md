Now let me write the final consolidated review.

## Summary

This paper introduces a weight-based method for analyzing gated neurons in transformers by computing cosine similarities between input, gate, and output weight vectors. Based on these cosine similarities, it proposes a taxonomy classifying neurons as "strengthening," "weakening," "conditional strengthening," etc. The key empirical findings are: (i) the weight-geometry pattern (positive cos(w_in, w_out) in early layers trending negative in late layers) generalizes across 12 LLMs; (ii) a small set of "weakening" neurons (cos(w_in, w_out) < -0.5) has outsized influence on model output, as measured by ablation experiments on OLMo-7B; (iii) negative gate values in the Swish activation play a mechanistically important role — a novel observation. The paper also introduces conditional ablation as a methodological tool.

## Strengths

- **Cross-model validation of the weight-geometry pattern (Section 5).** The paper computes cosine similarities across 12 LLMs (Llama-2/3, Gemma-2, OLMo, Mistral, Qwen2.5, Yi) and finds a consistent layerwise pattern: median cos(w_in, w_out) is positive in early layers and negative in late layers. Figure 1(a) provides a clean summary of this robust empirical observation.

- **The negative gate value finding is novel and well-supported (Section 6.2).** Conditional ablation experiments demonstrate that activations with x_gate < 0 (specifically x_gate < 0, x_in < 0 → x_post > 0) contribute substantially to the entropy-sharpening effect of weakening neurons. Prior work treated negative Swish values as relevant only for training dynamics (smooth differentiability), so showing mechanistic consequences is a genuine contribution. The paper appropriately acknowledges concurrent work by Kong et al. (2025).

- **The entropy sharpening result is counter-intuitive and interesting (Section 6.1).** Normally, removing information via ablation flattens the output distribution. The finding that weakening neurons *sharpen* the distribution, so ablating them flattens it, is surprising and makes the phenomenon worth understanding.

- **Conditional ablation is a useful methodological contribution (Section 6.2).** The idea of ablating only sign-conditioned subsets of activations to attribute effects is simple and effective, and could be adopted by other interpretability work.

## Weaknesses

### Major

- **The "weakening" label implies a functional interpretation that is not directly validated.** The taxonomy (Table 1) labels neurons as "strengthening" or "weakening" based on cosine similarity thresholds of weight vectors, with the paper claiming weakening neurons "remove" a direction from the residual stream (Section 4.2: "adds it to / removes it from the residual stream"). However, the paper never directly validates that a neuron classified as "weakening" actually subtracts its detected direction during normal operation — it only shows that these neurons *matter* when ablated. Furthermore, the paper's own most important finding — that negative gate values reverse the behavior, making weakening neurons *strengthen* in their most influential mode (Section 6.2: "weakening neurons take on a strengthening behavior") — undercuts the naming convention. A neuron whose most functionally significant activations are strengthening should not be primarily labeled "weakening." The geometric observation is valid and interesting, but the functional framing overreaches the evidence.

- **Ablation experiments demonstrating "outsized influence" are conducted on only one model (OLMo-7B).** The paper is transparent about this resource constraint (Section 6: "to save resources, we focus on a single model"), but the headline claim of "outsized influence" (title, abstract, conclusion) is presented without model-scope qualification. The weight-geometry pattern generalizes across 12 models, but the evidence for functional importance rests on one model. This narrows the scope of the central claim relative to its presentation.

### Minor

- **The cosine threshold τ = ±0.5 is not defended with sensitivity analysis.** The taxonomy (Table 1) uses τ = 0.5 to classify cosines as "approximately ±1" vs. "approximately 0." The paper acknowledges that "Many cosines will not be close to 0 or ±1" (Section 4.2) and offers continuous alternatives (scatter plots, marginal distributions). However, the categorical classification drives the paper's framing and labeling. No analysis of how class composition varies with τ (e.g., τ = 0.3 to 0.7) is provided, so the robustness of the taxonomy is unclear.

- **Qualitative case study examines only two neurons (Section 8).** The manual analysis covers one strengthening and one weakening neuron. The weakening neuron is honestly described as "much harder to interpret" (line 269). Two neurons is a very small sample for qualitative analysis, and the paper's claim that this reveals "the nature of weakening" (line 273) is thinly supported from the main text alone.

- **The scope claim is limited to decoder-only autoregressive transformers despite the title saying "Transformers."** All 12 models tested are decoder-only autoregressive LLMs. The title and framing reference "Transformers" more broadly, which modestly overclaims relative to the evidence.

### Trivial

- Minor numerical inconsistency: the abstract says "nine different LLMs" while Section 5 analyzes 12 models. (The nine correspond to the larger models in Figure 1(a), while 12 includes smaller variants — this discrepancy should be harmonized.)

## Nice-to-Haves

- A sensitivity analysis of how class composition changes as τ varies from 0.3 to 0.7 would strengthen the taxonomy's robustness.
- Running the ablation protocol on at least one additional model (e.g., Llama-3.2-3B, already analyzed in Section 5) would substantially strengthen the "outsized influence" claim.
- A simple validation check — measuring the dot product of the neuron's actual output (during a forward pass) with the direction it supposedly weakens — would directly test whether the "weakening" label matches functional behavior.

## Removed Points

These points are flagged to be removed; treat them with caution.

- **Preprocessing step deferred to appendix (Section 3.2):** Removed per rule: the parser strips appendices from all papers; they exist in the original submission.
- **No investigation of interaction with attention heads:** Removed as scope creep — the paper explicitly focuses on MLP neuron analysis.
- **"Weakening neurons activate often" may be confounded by layer position:** The paper already reports within-layer correlations (most layers -0.71 or stronger across ~30 layers) and transparently reports the last two layers' deviations. The criticism does not account for this existing within-layer analysis.
- **Grammar/formatting/style nitpicks:** Removed per rule: these are parser artifacts, not author errors.

## Novel Insights

The most incisive observation in the reviews is that the paper's own best finding — the mechanistic importance of negative gate values causing weakening neurons to *strengthen* — undercuts the "weakening" naming convention. This is not a contradiction in the paper's evidence (the paper honestly reports the behavior reversal), but it exposes a framing tension: the central taxonomy label describes the prototypical (x_gate > 0) case, while the paper's most novel result concerns the (x_gate < 0) case where the label is misleading. This points toward a clean reframing: present the weight-cosine analysis as a geometric observation (robustly supported across 12 models) and treat the functional labels as mnemonic descriptors rather than validated mechanisms.

## Suggestions

- Reframe the contribution: present the weight-cosine geometry as the primary discovery (robust across 12 models) and the "weakening/strengthening" labels as geometric descriptors, not validated functional roles. This would let the geometric universality claim stand on its own evidence while the ablation findings are properly scoped.
- Add ablation evidence on at least one additional model, or explicitly qualify the "outsized influence" claim in the title and abstract as applying to the specific model tested.

---

**Calibration Report**

Round 1 bracket: 5.0–6.5

Anchors consulted:
- **DOCS: Quantifying Weight Similarity (6.60)** — Uses cosine similarity of weights to study LLMs. Cleaner metric validation but less interesting mechanistic discoveries. Current paper comparable in quality but has a more significant framing issue. → suggests ceiling
- **Towards Universality (6.50)** — Studies mechanistic similarity across architectures. Solid empirical work. Current paper has stronger individual findings but a more notable overclaiming issue. → suggests ceiling
- **Discovering Influential Neuron Path (6.00)** — Vision transformer neuron influence analysis. Clean evaluation. Current paper similarly positioned but with more significant interpretability concern. → suggests anchor
- **Gated RNNs discover attention (5.50)** — Theoretical construction of attention in RNNs. Rejected despite interesting ideas. Current paper is empirically stronger. → suggests floor
- **Identifying Sub-networks via Functionally Similar Representations (4.60)** — Weak empirical validation, unclear contribution. Current paper is clearly stronger. → confirms floor is above 4.6
- **Retrieval Head (8.00)** — Gold-standard for this research paradigm: discovers functional class of attention heads, validates across models, clean ablation. Current paper has similar aims but weaker validation and a framing issue. → confirms ceiling is well below 8.0

Score rationale: The paper sits below 6.0–6.5 (DOCS, Towards Universality) because of the gap between its functional framing and the evidence that directly supports it, and because ablation evidence comes from a single model. It sits above 4.6–5.5 (Identifying Sub-networks, Gated RNNs) because the core empirical findings (cross-model geometric patterns, negative gate value mechanism) are genuinely novel, well-supported within their scope, and of clear interest to the mechanistic interpretability community.

MY FINAL SCORE: <score>5.5</score>
MY FINAL DECISION: <decision>Accept</decision>