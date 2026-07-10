Based on the favorability analysis, the single-model ablation weakness (0.00) and the comparison-against-random-only concern (0.08) are the dominant negative signals, while the strengths (0.72–1.00) are very strong. The structural findings across 12 models are solid, but the functional claims need broader validation. Let me produce the final review.

## Summary

This paper introduces a cosine-similarity-based method for analyzing the read-write (RW) functionality of gated neurons in transformers, and applies it to 12 LLMs. The key empirical discoveries are: (1) a strengthening-to-weakening transition across layers — early-middle layers are dominated by conditional strengthening neurons, while late layers contain more *weakening* neurons; (2) weakening neurons, though few in number, activate frequently and have outsized influence on model outputs when ablated; (3) part of this influence stems from negative gate values (x_gate < 0), challenging the conventional view that negative SwiGLU activations are negligible. The paper introduces conditional ablation as a methodological tool to isolate which activations drive specific behaviors.

## Strengths

- **Simple, interpretable method that scales across many models.** The core idea — computing cosine similarities between the three weight vectors (w_gate, w_in, w_out) of gated neurons — is straightforward but well-motivated and yields strikingly consistent results across 12 LLMs from different families (Gemma, Llama, OLMo, Mistral, Qwen, Yi), sizes (0.5B–9B), and gating variants (SwiGLU, GeGLU). Figure 1(a) showing the common strengthening-to-weakening transition is the paper's strongest empirical result.

- **Discovery of the weakening-neuron class and the layer pattern.** The identification that cos(w_in, w_out) transitions from positive in early-middle layers to negative in late layers, with weakening neurons (cos < -0.5) forming a discrete cluster in scatter plots (Figure 2), is a genuine empirical finding. This pattern is visually compelling and emerges from a minimally engineered analysis.

- **Conditional ablation method (Section 6.2).** Going beyond standard ablation by ablating only those activations of a neuron that satisfy specific sign conditions on x_gate and x_in is methodologically clean and novel. It is productively used to isolate that negative gate values have measurable functional importance — the paper's most surprising conceptual contribution.

- **The negative-gate-value finding is genuinely interesting.** The paper shows that a non-trivial portion of weakening neurons' sharpening effect comes from activations where x_gate < 0 and x_in < 0 (case iii). This challenges the widely held assumption that negative Swish values are only relevant for training dynamics, demonstrating for the first time a mechanism involving negative gate values in model function.

## Weaknesses

### Fatal
None.

### Major
- **Ablation experiments validating functional importance are conducted on a single model (OLMo-7B).** The weight-based structural analysis (Section 5) convincingly shows weakening neurons exist in similar distributions across 12 models. However, the central claim that weakening neurons have "outsize influence" and "large influence on model behavior" (abstract) rests entirely on ablation experiments from one model. The paper is transparent about this resource-driven choice (Section 6: "to save resources, we focus on a single model"), but the headline functional claims are presented without qualification. Either the ablation should be replicated on at least 2–3 additional models from different families (e.g., Llama-3.1-8B, Gemma-2-9B), or the universality claims should be scoped down to what the weight-based evidence directly supports.

### Minor
- **Entropy ablation results (Figure 3b) lack quantitative support.** The paper claims that case (iii) (x_gate < 0, x_in < 0) "shows entropy effects similar to those of weakening neurons as a whole," but provides no means, standard deviations, effect sizes, or statistical tests to back this up. The parser-extracted figure description reports all six histograms as centered near zero with symmetric shapes, making the claimed differences impossible to assess without numerical statistics. At minimum, the mean and standard deviation of entropy(clean) - entropy(ablated) per condition should be reported.

- **Weight preprocessing impact on classification is not discussed in the main text.** The paper multiplies w_in and w_out by sign(cos(w_gate, w_in)) (Section 3.2), which redefines the coordinate system for all subsequent cosine analyses — including the central taxonomy into strengthening/weakening. The paper does not report: (a) what fraction of neurons have their signs flipped, (b) whether the strengthening-to-weakening pattern (Figure 1a) holds without this preprocessing, or (c) whether ablation results are robust to omitting it. Without these checks, the reader cannot assess whether the main findings depend on this preprocessing choice.

- **The "outsize influence" claim is supported relative to random neurons, a weak standard.** The main-text comparison is against random neurons from the same layers. The paper states that other RW classes' ablation results are "indistinguishable from the clean line" but defers this critical comparison to the appendix. A direct main-text comparison against other similarly small classes (e.g., proportional change neurons in late layers) would more strongly support the claim that weakening neurons are uniquely influential.

- **The τ = 0.5 classification threshold is arbitrary.** While the paper mitigates this by also providing continuous analyses (scatter plots, marginal distributions), a sensitivity analysis showing how class counts change at alternative thresholds (e.g., τ = 0.3, 0.4, 0.6) would strengthen confidence in the taxonomy-driven results (Figure 1b).

- **The activation frequency correlation of -0.97 (Figure 4) may be inflated.** This is reported from a 2D histogram (binned data), which can inflate Pearson correlations. The paper's more conservative statement — correlations are at least -0.71 in all but the last two layers — is the more credible headline result and could be more prominently featured.

### Trivial
None.

## Nice-to-Haves
- Sensitivity analysis for the τ threshold used in the taxonomy.
- Testing the ablation on a held-out domain (not Dolma) to rule out in-distribution effects.
- Reporting the total count and fraction of weakening neurons for each of the 12 models, not just OLMo-7B.
- A brief limitations paragraph in the conclusion acknowledging the single-model ablation scope.

## Removed Points
These points from the input review are flagged for removal; treat with caution:
1. **Case study undermines claims**: Removed — the paper acknowledges the weakening neuron is harder to interpret but finds partial interpretability through the negative-gate lens. The case study shows the method yields insight even for hard cases, which is an honest finding, not a flaw.
2. **In-distribution data concern**: Removed — speculative, no evidence that evaluating on Dolma (OLMo's training corpus) is actually problematic for the ablation conclusions.
3. **Single example for entropy reduction**: Removed — the paper explicitly frames this as a case study, which is an accepted format for illustrating a mechanism.
4. **Missing limitations paragraph**: Removed — trivial presentation preference.

## Novel Insights
None beyond the paper's own contributions.

## Suggestions
1. Replicate the ablation experiments on at least 2–3 additional models (e.g., Llama-3.1-8B, Gemma-2-9B) to support the generality of the functional claims, or explicitly scope the "outsized influence" claims to OLMo-7B.
2. Add quantitative statistics (mean, standard deviation, effect size per condition, paired tests) to the entropy analysis (Figure 3b) to turn a suggestive figure into solid evidence for the negative-gate-value claim.
3. Report in the main text: the fraction of neurons affected by the sign-flipping preprocessing, whether the strengthening-to-weakening pattern holds without it, and sensitivity of class counts to the τ threshold.

## Score and Decision

MY FINAL SCORE: <score>6.0</score>
MY FINAL DECISION: <decision>Accept</decision>