Here is the final consolidated review.

## Summary
The paper introduces a weight-based method for analyzing gated neurons in transformers, using cosine similarities between w_gate, w_in, and w_out to characterize read-write functionality. This reveals a class of "weakening" neurons that appear mostly in late layers, activate frequently, and have outsized influence on model outputs — including through a mechanism involving negative gate values of the Swish activation function, which was previously thought unimportant for model function. The method is validated across 12 LLMs, and conditional ablation experiments on OLMo-7B show that negative-gate activations account for much of the sharpening effect of weakening neurons.

## Strengths
- **Novel weight-based method for gated neurons.** The cosine-similarity analysis between the three weight vectors is simple, purely weight-based (requiring no activations for the initial classification), and well-motivated by the residual-stream perspective. It cleanly differs from prior work that looks only at activation contexts (Voita et al., 2024) or only at output weights (Gurnee et al., 2024).
- **Robust cross-model consistency.** Section 5 demonstrates the strengthening→weakening pattern across 12 LLMs (2B–9B parameters), including Llama, Gemma, OLMo, Mistral, Qwen, and Yi. Figure 1(a) shows this at a glance. This is not a single-model phenomenon.
- **Surprising finding about negative gate values.** Section 6.2's conditional ablation experiments show that case (iii) (x_gate < 0, x_in < 0) accounts for much of the sharpening effect of weakening neurons. This is genuinely surprising under the conventional view that negative Swish values are negligible or only relevant to training dynamics. The claim that "Swish is not reducible to ReLU for mechanistic interpretability" (p. 7) is well-supported by this finding.
- **Conditional ablation as a methodological contribution.** The idea of ablating only a subset of activations based on the sign of x_gate and x_in is clean and useful beyond this specific paper. It addresses a real need: standard ablation tells you whether a neuron matters, but not *which activations* drive its effect.

## Weaknesses

### Fatal
None.

### Major
None.

### Minor
- **Functional importance demonstrated on only one model.** The ablation experiments establishing that weakening neurons have "outsize influence" are conducted on OLMo-7B alone. The paper acknowledges this (lines 187–188: "to save resources, we focus on a single model"), and the weight-based classification is robustly validated across 12 models. However, the central empirical claim about functional importance rests on ablations from a single model. Testing at least one additional architecture (e.g., Llama-3.2-3B, which is extensively analyzed in Section 5) would substantially strengthen the generality of the claim.
- **Mean ablation results relegated to the appendix.** The paper's primary ablation method is zero ablation, which is known to potentially produce artifacts by pushing the model into activation regimes it was never trained on. The paper notes (line 215) that mean ablation shows "similar" results (Section F.4), but these results are not presented in the main paper. Since the central headline about weakening neurons' outsized influence depends heavily on these ablation experiments, mean ablation results should be shown alongside zero ablation results in the main text.
- **Taxonomy threshold not tested for robustness.** The classification into strengthening/weakening etc. uses τ = ±0.5 for cosine similarity (Section 4.2). The paper provides alternative visualizations (scatter plots, marginal distributions) that partially mitigate this, but never tests whether the main qualitative findings (layer-wise class distribution, correlation with activation frequency) are sensitive to this threshold. A brief demonstration with τ = ±0.3 or ±0.7 would address a natural skepticism.
- **The correlation in Figure 4 is reported as -0.97 for layer 15 of OLMo-7B.** This is an extremely strong linear relationship. The paper should clarify whether this is a Pearson r computed across individual neurons or across binned data (since Figure 4 is described as a "two-dimensional histogram"), and how this very high value relates to the range of "at least -0.71" reported for other layers.

### Trivial
- **"Nine" vs. "12" LLMs.** The abstract and contributions (lines 9, 19) say "nine different LLMs," while Section 5 (line 170) says the method was applied to 12 LLMs. This appears to be because Figure 1(a) shows nine larger models while the full study covers twelve, but the discrepancy is confusing and should be reconciled.
- **Negative gate case (iii) frequency unquantified.** The paper says negative x_gate activations are "relatively rare" in weakening neurons (line 223) but does not give the actual proportion. Reporting this would substantially strengthen the surprise finding.

## Nice-to-Haves
- Provide quantitative summary statistics alongside the figures (e.g., "across all 12 models, on average X% of neurons are weakening, and Y% of those are in the last 25% of layers").
- A brief note clarifying how the -0.97 correlation in Figure 4 is computed (per-neuron Pearson vs. binned) and how it relates to the range of -0.71 to +0.29 reported for other layers would strengthen Section 7.

## Removed Points
These points are flagged to be removed; treat them with caution.
- **Superposition claim is speculation.** The critic flagged that the paper's statement about weakening neurons working "together in superposition" (line 239) is speculation. The paper uses the word "suggests," making this clearly a hypothesis, not an asserted claim. Not a weakness.
- **Case studies are thin.** The critic noted the case studies are "illustrative but thin" but also said they are "fine as a brief illustration." This is not a substantive weakness — the paper's contribution is primarily quantitative, and the qualitative analysis is appropriately scoped.
- **Zero ablation may produce artifacts (as a fatal concern).** The critic raised this as a potential fatal issue, but the paper explicitly states that mean ablation shows similar effects (line 215) and references Section F.4. The prominence concern is valid (kept as Minor above), but the paper does address this methodologically.

## Novel Insights
The reviews collectively surface a productive tension: the weight-based discovery of weakening neurons is independently valuable and validated across 12 models, yet the functional-importance claims rely on ablations from a single model. This suggests that the paper's strongest contribution is the discovery method and the cross-model weight patterns, with the functional claims being promising but requiring broader replication. The negative-gate finding (conditional ablation case iii) is consistently identified as the paper's most striking individual result — it challenges a widespread assumption about Swish being effectively ReLU-like for interpretability purposes.

## Suggestions
- Move the mean ablation results from the appendix (Section F.4) into the main paper, or add a prominent sentence quantifying the agreement between zero and mean ablation effect sizes.
- Report the relative frequency of the negative-gate (case iii) activations as a proportion of all weakening-neuron activations when discussing its outsized effect on entropy.
- Add a brief paragraph or supplementary figure testing whether the layer-wise class distribution at τ = ±0.3 or ±0.7 is qualitatively similar to the reported results at τ = ±0.5.
- Clarify the type and granularity of the correlation coefficient reported in Figure 4.

MY FINAL SCORE: <score>8</score>
MY FINAL DECISION: <decision>Accept</decision>