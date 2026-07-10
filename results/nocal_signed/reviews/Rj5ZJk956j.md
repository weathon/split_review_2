Now let me compose the final review based on the validated evidence and the favorability signals.

## Summary

This paper introduces a mechanistic interpretability method for gated neurons based on cosine similarities between weight vectors (w_gate, w_in, w_out), and uses it to classify neurons into read-write (RW) functionality categories. Applying this method across 12 LLMs, the paper discovers a consistent pattern: early-middle layers are dominated by *conditional strengthening* neurons, while late layers contain more *weakening* neurons. Through ablation experiments on OLMo-7B, the paper finds that weakening neurons (a small class of a few hundred neurons) have a disproportionately large effect on model behavior, and — most surprisingly — that this effect is partly driven by negative gate values (x_gate < 0), which were previously assumed to be functionally negligible. The paper also introduces *conditional ablation*, a method for identifying which activation regimes of a neuron drive specific behaviors.

## Strengths

- **Cross-model consistency of weight-based patterns (Section 5, Figure 1a, 12 LLMs).** The paper demonstrates that the median cos(w_in, w_out) goes from positive in early layers to negative in late layers across 12 LLMs spanning multiple families (Llama, Gemma, OLMo, Mistral, Qwen2.5, Yi). This is the paper's most robust finding and genuinely suggests a universal architectural property of gated transformers. The thoroughness of this cross-model validation is a strong point.

- **Conditional ablation method (Section 6.2).** The idea of selectively ablating activations based on the sign of x_gate and x_in is a clean, principled way to attribute functional effects to specific activation regimes. This is a methodological contribution that other interpretability researchers can directly adopt. Using it, the paper convincingly shows that the entropy-sharpening effect of weakening neurons is driven disproportionately by case (iii) (x_gate < 0, x_in < 0).

- **Discovery that negative gate values have functional importance (Sections 6.2–6.3).** The finding that negative Swish activations — which are small in magnitude and were previously assumed to matter only for training dynamics — contribute meaningfully to model behavior is genuinely novel. The concrete case study (the "O" → "mic" example) provides a legible illustration of the mechanism at work.

## Weaknesses

### Fatal
None.

### Major

- **Functional ablation experiments run on only one model (OLMo-7B).** The weight-based analysis in Section 5 covers 12 models, but the ablation experiments in Sections 6–8 — which support the paper's most striking claims about weakening neurons' "outsize influence" and negative gate values being "important for transformer functionality" — are executed on a single model (OLMo-7B) with a single dataset (20M tokens from Dolma). The paper acknowledges this choice (line 188: "to save resources"), but this does not resolve the evidential gap. Without at least one additional model showing qualitatively similar ablation results, the generality of the functional importance findings remains unsubstantiated. This is the most consequential gap in the paper.

- **No error bars, confidence intervals, or multiple-run statistics on any ablation result.** All ablation results (attribute rate curves in Figure 3a, entropy histograms in Figure 3b) appear to be from single runs. Without variance estimates, the reader cannot assess whether the observed effects are stable or could shift substantially with different random seeds, data subsets, or neuron selections for the baseline. This weakens all quantitative claims from the ablation experiments and is a standard expectation for empirical work of this kind.

### Minor

- **The entropy result (Figure 3b) lacks quantitative precision.** The caption states "in ~10^6 next-token predictions, weakening neurons decrease the entropy by about 10 nats" — it is unclear whether this "about 10 nats" refers to a maximum in the tail, an average effect, or something else. The histograms are described as "centered around 0," making the practical significance of the effect hard to assess without reporting the mean/median entropy shift and its standard deviation.

- **The claim that other neuron classes are "indistinguishable from the 'clean' line" (Figure 3 caption) is deferred entirely to the appendix without quantifying effect sizes in the main text.** The reader cannot judge from the main paper whether weakening's effect is 2×, 10×, or 100× larger than other classes.

- **The case study in Section 8 is a single weakening neuron from one model.** While presented as illustrative, the paper's broader narrative about weakening neurons' complex behavior relies on this one example without a systematic analysis of how representative this behavior is across the 243 weakening neurons.

- **No limitations section.** Given the acknowledged single-model ablation, lack of error bars, and threshold-dependent taxonomy, an explicit limitations discussion would help calibrate reader expectations and strengthen the paper's credibility.

### Trivial
None.

## Nice-to-Haves

- Consider reporting perplexity change under ablation to connect the findings to a familiar metric that the community knows how to interpret.
- A cumulative ablation analysis (ablate 10, 50, 100, 200 weakening neurons) could reveal whether the effect is driven by a handful of high-leverage neurons or broadly distributed.

## Removed Points

These points were flagged by reviewers but are removed for the following reasons:
- **Weight preprocessing effect on taxonomy:** The paper states this transformation in the main text (line 85) and defers justification to the appendix; this is standard practice.
- **Taxonomy threshold (τ=0.5) arbitrariness:** The paper already addresses this by offering three levels of granularity (threshold, marginal distributions, scatter plots).
- **"25% depends on threshold":** The paper acknowledges explicitly (lines 176-177) that even "orthogonal output" neurons perform input manipulation to some extent.
- **Activation frequency confirms prior work:** The paper credits Gurnee et al. (2024) transparently (lines 243-245); this is proper positioning.
- **No perplexity/downstream evaluation:** The paper justifies its metric choices in Section F; this is a deliberate scope choice, not an omission.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. Run ablation experiments on at least one additional model (e.g., Llama-3.2-3B or Gemma-2-2B, both small enough) to demonstrate the generality of the functional findings. Even a partial replication on 5M tokens would dramatically strengthen the claims.
2. Report the mean/median entropy shift with standard deviation alongside the histograms in Figure 3b, so the average effect size is legible.
3. Quantify in the main text how much larger weakening neurons' effect on attribute rate/entropy is relative to other RW classes, rather than stating "indistinguishable" without numbers.
4. Add a limitations section discussing the scope of the ablation evidence, the absence of error bars, and the arbitrary nature of the τ = 0.5 threshold.

## Score and Decision

The paper has three genuine strengths: a thorough cross-model weight-based analysis that reveals a consistent architectural pattern, a novel conditional ablation methodology, and a surprising discovery about the functional relevance of negative gate values. However, the paper's headline functional claims rest on a narrow empirical foundation — one model, single runs, no error bars — creating a significant gap between claim strength and evidence. The weight-based patterns are convincingly universal; the functional importance findings are suggestive but not yet at the same standard of evidence.

The paper should be accepted as a solid empirical contribution with a valuable new methodology, but the authors should address the evidential gaps for the functional claims either through additional experiments or by appropriately tempering the claims in the final version.

MY FINAL SCORE: <score>6</score>
MY FINAL DECISION: <decision>Accept</decision>