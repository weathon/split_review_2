Now I have enough information to finalize. Let me compile the complete review.

## Summary

This paper introduces a cosine-similarity-based method for analyzing the read-write functionality of gated neurons in transformer LLMs, discovering that neurons can be categorized along two cosine axes (cos(w_in, w_out) and cos(w_gate, w_out)) into functional types like "strengthening," "weakening," and "conditional" variants. The key findings are: (1) a consistent strengthening-to-weakening pattern across 12 LLMs, (2) a small class of "weakening" neurons that activate very frequently and have outsized influence on model behavior, and (3) the surprising discovery that negative Swish gate values contribute substantially to the entropy-sharpening effect of weakening neurons. The paper also introduces conditional ablation as a methodological contribution.

## Strengths

- **Conditional ablation is a useful methodological contribution (weight=9.64).** The idea of ablating only a subset of a neuron's activations based on the sign pattern of (x_gate, x_in) is simple, transferable, and cleanly isolates which activation regimes drive a neuron's effect on a given metric.

- **The discovery about negative gate values is genuinely surprising and well-supported (weight=8.54).** The finding that negative Swish gate values (case (iii): x_gate < 0, x_in < 0) contribute substantially to the entropy-sharpening effect of weakening neurons directly challenges the common assumption that negative gate values matter only for training dynamics. The paper appropriately acknowledges concurrent work by Kong et al. (2025).

- **The cross-model consistency finding is substantive (weight=7.93).** The paper demonstrates the same strengthening-to-weakening pattern across 12 LLMs (Gemma, Llama, OLMo, Mistral, Qwen, Yi) spanning 0.5B to 9B parameters, with Figure 1(a) convincingly showing the median cos(w_in, w_out) shifting from positive in early layers to negative in late layers across all models.

- **A genuinely novel analytical lens for gated neurons (weight=7.79).** The idea of analyzing gated neurons through the cosine similarity of their weight vectors (gate, input, output) is simple and has been sitting in plain sight — Gurnee et al. (2024) computed these cosines for GPT-2 but did not interpret them. This paper takes the step of building a taxonomy around them with a computationally lightweight approach.

## Weaknesses

### Fatal
None.

### Major

1. **The ablation baseline is confounded with activation frequency.** Figure 4 shows a strong negative correlation (r = −0.97 in layer 15) between cos(w_in, w_out) and activation frequency — weakening neurons (negative cos(w_in, w_out)) activate much more often than strengthening neurons. The ablation baseline uses "random neurons from the same layers" (line 192), which controls for layer but not for activation frequency. A neuron that activates rarely (as strengthening neurons do) will naturally have a smaller ablation effect than one that activates frequently, regardless of any "weakening" functional role. The paper's conclusion that "weakening neurons have a large effect on the metrics" conflates having high activation frequency with having a distinct functional mechanism. A properly matched baseline (non-weakening neurons with similarly high activation frequencies) is needed to isolate whether the "weakening" label adds explanatory power beyond the activation-frequency confound.

2. **The weight preprocessing step systematically alters cos(w_gate, w_out) and may affect the taxonomy.** Section 3.2 states: "For each neuron, we multiply w_in and w_out by the sign of cos(w_gate, w_in)." This leaves cos(w_in, w_out) unchanged but flips the sign of cos(w_gate, w_out) whenever cos(w_gate, w_in) < 0. The taxonomy in Table 1 has columns for cos(w_gate, w_out) > 0.5 and < 0.5 but not for ≈ −1. After preprocessing, a neuron that was genuinely "weakening" (cos(w_in,w_out)≈−1, cos(w_gate,w_out)≈+1, cos(w_gate,w_in)≈−1) becomes cos(w_gate,w_out')≈−1, which falls in the < 0.5 column and would be classified as "conditional weakening" rather than "weakening." The paper defers justification to Appendix C (stripped), but the concern is structural: the classification scheme that generates the headline categories may be partially determined by this preprocessing convention. Without knowing how many neurons change category due to this transformation, the observed patterns cannot be fully assessed as genuine or conventional.

### Minor

3. **Taxonomy thresholds are arbitrary and the taxonomy is not empirically validated.** The threshold τ = ±0.5 is used throughout without justification. Many neurons cluster near this boundary (the paper notes that "orthogonal output" neurons often "exceed the significance threshold" in Figure 2), so small changes in τ could substantially change class membership. More importantly, the paper never validates that the cosine-based categories correspond to actual functional differences — are "strengthening" neurons actually strengthening the concepts they detect? Only 2 neurons are examined qualitatively in the case study (section 8). The ablation experiments show that "weakening" *as a set* matters but do not validate the taxonomy; they only show that this particular clustering (dependent on preprocessing + threshold) picks out an influential subset.

4. **All ablation experiments use a single model (OLMo-7B) and a single 20M-token dataset.** The weight analysis covers 12 models, but the functional claims about weakening neurons' influence rest entirely on one model. Given that the paper emphasizes universality across models for the weight patterns, it should show at least one additional model for the ablation results to demonstrate that the functional influence generalizes. The paper acknowledges this limitation (line 188: "to save resources"), but it limits the strength of the claims.

5. **The "outsized influence" claim in early-middle layers lacks statistical rigor.** Figure 3(a) shows a single ablation curve without error bars or confidence intervals — it is unclear whether this is a single run or the mean of multiple runs. The claim that weakening neurons show effect "already from layer ≈10 onward, even though weakening neurons are few" (line 207) would benefit from per-neuron effect size analysis (effect divided by number of ablated neurons at each layer) to substantiate that these few neurons are individually powerful.

### Trivial

6. **Model count inconsistency.** The abstract and introduction say "nine different LLMs" but Section 5 lists 12 models. It appears that Figure 1(a) shows 9 of the 12 (the "larger" ones), but this discrepancy should be resolved.

## Nice-to-Haves

- Report the fraction of weakening-neuron activations that fall into each of the four sign quadrants in the conditional ablation. The finding that case (iii) drives the entropy effect is more striking if activations in this quadrant are rare.
- Report how many neurons change taxonomy category when the preprocessing step is not applied.
- Report ablation results for at least one additional model (e.g., Llama-3.2-3B) to support cross-model generalizability.
- Provide error bars or confidence intervals on ablation curves, and report stability across different random seeds or dataset subsets.

## Removed Points

These points from the input review were removed because they are factually incorrect, misunderstand the paper, or are formatting artifacts:

- **Swish formula criticism**: The reviewer claimed that "Swish(x) as x/(1+exp(-x)) is incorrect — that's the sigmoid function." This is factually wrong. Sigmoid(x) = 1/(1+exp(-x)), not x/(1+exp(-x)). Swish(x) = x · sigmoid(x) = x/(1+exp(-x)). The formula in the paper is mathematically correct.
- **GELU vs. SwiGLU comparison clarity**: The reviewer asked the paper to be "clearer about which findings extend previous GELU-based results." The paper already explicitly notes the distinction — line 243 states "Gurnee et al. (2024) found a negative correlation… but in a GELU model." The comparison is already appropriately qualified.
- **Section-by-section formatting notes** about parser artifacts (missing multiplication symbols, figure caption formatting) are not weaknesses of the paper.

## Novel Insights

The reviews surface one genuinely novel observation beyond the paper's own contributions: the activation-frequency confound (weakness 1) is a structural issue that cuts across the paper's main causal claim. The harsh critic correctly identifies that the paper's ablation experiments compare weakening neurons (which activate often) against random neurons (which activate rarely on average), and the observed effect differences could be driven almost entirely by this frequency disparity rather than by any distinct functional mechanism of "weakening." This is a cleaner and more specific critique than general calls for larger-scale or more rigorous experiments, because it targets a specific experimental design choice that, if corrected, would either strengthen or substantially weaken the paper's central claim. The preprocessing concern (weakness 2) is also structurally insightful but is more contingent on how many neurons are affected — something the authors can report.

## Suggestions

1. **Address the activation-frequency confound directly.** Match non-weakening neurons with similarly high activation frequencies from the same layers as the ablation baseline. If weakening neurons still show a larger effect, the "weakening" label has genuine explanatory power beyond activation frequency.
2. **Clarify or remove the preprocessing step's impact.** Either justify why flipping cos(w_gate, w_out) for a subset of neurons does not affect the taxonomy's validity, or re-run the analysis without preprocessing and show results are qualitatively similar.
3. **Validate the taxonomy on a sample of neurons.** Pick 10–20 neurons per RW category and check whether their activation behavior matches the category description — e.g., does a "strengthening" neuron's writing direction align with its input-detected direction when it activates?
4. **Add at least one more model to the ablation experiments** to support the claim of universality.
5. **Add error bars or confidence intervals** to ablation curves and clarify whether results are from a single run or averaged over multiple runs.

## Score and Decision

**Round 1 bracket (after draft weighting and initial anchor comparison):**  
I compared item-weighted drafts between this paper and anchors in each score band. The paper clearly exceeds strong-reject anchors (avg 1.0) but falls well short of high-quality anchors like Retrieval Heads (8.00) and Sparse Feature Circuits (8.00), which have near-minor weaknesses and validated causal claims. Anchors in the 5.5–7.5 range (Capability Localization at 5.75, Influential Neuron Path at 6.00, DOCS at 6.60) provide the most relevant comparison. The initial bracket is **4.0–6.0**.

**Round 2 narrowing:**  
I examined Neuron to Graph (4.00) and DOCS (6.60), plus Capability Localization (5.75), with itemized weights.

- **Neuron to Graph (4.00):** Several reviewers flagged ad-hoc methodology, lack of OOD validation, and arbitrary hyperparameters. Weaknesses include weight -5.92 (no external validation), -2.09 (similar to prior work), -2.38 (insufficient evaluation). This paper's weaknesses are more damaging than my paper's, and its strengths are less specific. My paper is clearly stronger.

- **Capability Localization (5.75):** Has arbitrary thresholds (weight 4.54), missing statistical analysis (4.60), conceptual issues (weight -4.01), and limited scope (3.67). However, it has strong positive weights: 10.08 (important question), 9.63 (assessed prior methods), 8.41 (novel method). My paper's most damaging weaknesses (0.35 single model, 0.61 taxonomy validation, 1.26 activation frequency confound) are collectively more damaging than Cap Loc's. My strengths (9.64, 8.54, 7.93, 7.79) are comparable. Overall, my paper is somewhat below Cap Loc's 5.75.

- **DOCS (6.60):** A cleaner paper with fewer methodological concerns. Weaknesses: 6.14 (needs ablation), 5.50 (needs justification), 2.32 (no direct application). The most damaging weakness is 0.69 (unclear findings). My paper has more methodological gaps. I would place my paper below DOCS.

**Final score:** The paper has genuinely novel findings (negative gate values, cross-model patterns) and a useful method (conditional ablation). However, two structural weaknesses — the activation-frequency confound in ablation experiments (weight 1.26) and the lack of taxonomy validation (weight 0.61) — substantially weaken the causal claims. The preprocessing concern (weight 4.09) is moderate. These issues are addressable, but as presented they prevent the paper from being a clear accept. I place this paper at **5.0**, below Capability Localization (5.75) due to the more damaging nature of its weaknesses.

**Decision rationale:** Score 5.0 corresponds to borderline territory. The paper's contributions are real and novel, but the activation-frequency confound and missing taxonomy validation undermine the central claims about weakening neurons' outsized influence. These are fixable issues, but as currently presented the evidence is not strong enough to warrant acceptance.

**Retrieved anchors (all rounds):**

| Path | Avg Score | Round | Itemized? | Comparison to this paper |
|------|-----------|-------|-----------|--------------------------|
| nSDOkm0SKo.md | 1.00 | 1 | No | Unrelated financial paper, well below |
| 8QTpYC4smR.md | 1.00 | 1 | No | Survey paper, well below |
| gwZ90hFSL2.md | 1.00 | 1 | No | Unrelated robotics paper, well below |
| fSbPwHjdDG.md | 3.00 | 1 | Yes | Llamas think in English — has severe methodological and presentation issues |
| 9L9j5bQPIY.md | 2.50 | 1 | No | Metanetwork approach — less rigorous |
| 89wVrywsIy.md | 3.40 | 1 | No | Hierarchical tracing — similar topic, mixed reviews |
| jsvvPVVzwf.md | 5.00 | 1 | No | Cosine similarity pruning — tangential topic |
| JY6P45sFDS.md | 3.60/6.75 | 1 | No | Optimization trajectories — different topic |
| IlNVkYUSfF.md | 5.00 | 1 | No | Resonator-Gated RNNs — different architecture |
| f6r1mYwM1g.md | 5.75 | 1,2 | Yes | Capability Localization — comparable quality and weaknesses, slightly stronger |
| WQQyJbr5Lh.md | 6.00 | 1,2 | Yes | Vision Transformer neuron paths — cleaner but different domain |
| 41HlN8XYM5.md | 6.33 | 1 | No | Circuit discovery — more rigorous |
| I4e82CIDxv.md | 8.00 | 1 | Yes | Sparse Feature Circuits — significantly stronger |
| EytBpUGB1Z.md | 8.00 | 1 | Yes | Retrieval Heads — significantly stronger |
| d8w0pmvXbZ.md | 8.00 | 1 | No | Training instabilities — different topic, stronger |
| JBLHIR8kBZ.md | 4.00 | 2 | Yes | Neuron to Graph — lower quality, ad-hoc methodology |
| CN2bmVVpOh.md | 4.33 | 2 | No | Transformer mechanisms mimic gating — different topic |
| y3CdSwREZl.md | 4.80 | 2 | No | MINER — different domain (MLLMs) |
| XBHoaHlGQM.md | 6.60 | 2 | Yes | DOCS — cleaner methodology, better score |
| VyxlbbK8WV.md | 6.00 | 2 | No | Self-emergent similarity — vision domain |
| vVxeFSR4fU.md | 6.50 | 2 | No | Tracing representation progression — different topic |
| bkdWThqE6q.md | 6.00 | 2 | No | Interpretable transformer for classification — vision |

MY FINAL SCORE: <score>5.0</score>
MY FINAL DECISION: <decision>Reject</decision>