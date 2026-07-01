## Summary

This paper analyzes the role of pooled CLIP text embeddings in diffusion transformer models for text-to-image/video generation. The authors find that in conventional usage, the pooled embedding contributes little to output quality (compared to attention-based text conditioning), but demonstrate that it can be repurposed as a guidance signal — applying CFG-style extrapolation in modulation space using positive/negative prompt pairs — to controllably improve aesthetics, complexity, object counting, and hands correction. The method is training-free for models that natively use CLIP, extends to CLIP-free models via lightweight fine-tuning, and is evaluated across five T2I models, two T2V models, and image editing.

## Strengths

1. **Clean, well-targeted analysis of pooled embedding inactivity (Section 4, Table 1).** The paper provides a direct empirical test across prompt lengths for FLUX schnell and HiDream-Fast. The finding that CLIP's contribution ranges from negligible (long prompts in FLUX) to literally zero (all prompts in HiDream) is clearly documented and valuable as a design justification for practitioners.

2. **The core insight — reusing the pooled embedding as a guidance signal — is practically useful and elegantly simple.** Equation 3 (modulation guidance) is straightforward: it applies extrapolation in modulation space using positive/negative prompt pairs. The dynamic variant (applying guidance only to later layers) demonstrably improves the quality-fidelity trade-off (Figure 3a). The method is training-free, adds negligible overhead, and works across multiple models.

3. **Broad and honest evaluation scope.** The paper tests five T2I models (FLUX schnell, FLUX dev, SD3.5 Large, HiDream, COSMOS), two T2V models (Hunyuan, CausVid), and image editing (FLUX Kontext). It uses both automatic metrics (CLIP Score, PickScore, ImageReward, HPSv3, GenEval, VBench) and human side-by-side evaluation. This breadth makes the claims more credible than a single-model evaluation.

## Weaknesses

### Fatal
None.

### Major

1. **Distillation fine-tuning circularly guarantees CLIP inactivity for COSMOS/CausVid.** For models without native CLIP (COSMOS, CausVid), the authors fine-tune an MLP using an MSE distillation objective that minimizes the difference between the original model's output (no CLIP) and the modified model's output (with CLIP). As described in lines 134–166: *"The objective is to minimize the MSE loss between these two predictions."* By construction, this training makes CLIP have zero net effect. The paper then states (line 197) *"confirming that CLIP alone is ineffective"* — but this "confirmation" is a direct consequence of the training protocol, not a discovery about pooled embeddings in general. This is misleading. The core method's validation on native-CLIP models (FLUX, SD3.5, HiDream) is unaffected, but the framing should be corrected to acknowledge that the COSMOS/CausVid experiments demonstrate only that *their specific distillation+guidance pipeline works*, not that CLIP embeddings are inherently inactive in those models.

### Minor

2. **The abstract overclaims relative to the paper's own data.** The abstract states (line 9) *"the pooled embedding contributes little to overall performance, suggesting that attention alone is generally sufficient."* Yet Table 1 shows that for FLUX schnell with short prompts, removing CLIP reduces ImageReward from 6.2 to 4.5 (a 28% drop) and CLIP Score from 30.1 to 29.0. The paper body (lines 80–81) properly qualifies this: *"the influence of CLIP in FLUX schnell is inconsistent: it is negligible for long prompts but can be impactful for short ones."* The abstract should match this precision.

3. **The most relevant baseline comparisons are relegated to the appendix.** The main results (Tables 2 and 3) compare only against the original model without guidance. Comparisons against Normalized Attention Guidance and Concept Sliders — the two most directly related prior methods — appear only in Appendix E (referenced at line 223). While the win rates (34%, 16%) are stated in the main text, a summary table in the main paper would allow readers to directly assess the method's relative merit.

4. **Trade-offs between guidance objectives are understated.** In Table 2, FLUX dev with aesthetics guidance achieves only a 44% relevance win rate (meaning the original model is preferred for text relevance 56% of the time), and COSMOS with complexity guidance achieves a 44% defects win rate. The paper describes these as *"slight drops"* (line 197), but a 12-percentage-point deficit in relevance or defects is a substantial degradation that merits more candid discussion, especially since users typically value both fidelity and quality.

5. **Dynamic guidance hyperparameter is underspecified.** The dynamic strategy (Section 5, Figure 3b) uses a step function controlled by a layer index *i*, but the main text never specifies what value of *i* is used, how it was selected, or whether it varies per model. This is a reproducibility concern for the core result in Figure 3a.

6. **Confidence intervals are absent for automatic metrics.** Table 2 reports automatic metrics to one decimal place. For improvements as small as 0.1–0.2 in CLIP Score or PickScore, readers cannot assess whether these are within the noise floor. The human evaluation includes statistical significance markers; the automatic metrics should too, or at minimum report standard errors.

7. **Reliance on prompt engineering is not acknowledged as a limitation.** The method requires selecting a positive/negative prompt pair for each desired improvement direction (aesthetics, complexity, hands, counting). This is prompt engineering, which inherits concerns about transferability and brittleness. The paper should explicitly acknowledge this as a practical limitation rather than implying it is a free parameter.

### Trivial

8. **The "zero effect" result for HiDream-Fast is not literally zero.** Table 1 shows ImageReward actually improves slightly when CLIP is removed (7.9→8.1 short, 12.8→13.0 long). This strengthens rather than weakens the paper's claim, but the description should be precise: CLIP has no *positive* effect.

9. **Attention-map analysis is correlational.** The analysis in Figure 4 shows that attention shifts toward relevant tokens when guidance is applied, but this does not establish that the attention shift *causes* the improvement — it could be a downstream effect. The paper should avoid implying a causal interpretation.

## Nice-to-Haves

- A hyperparameter sensitivity analysis showing how the guidance scale *w* and layer cutoff *i* affect results across models would increase practical usefulness.
- The COSMOS/CausVid fine-tuning experiments would be stronger if framed as: "we can inject a CLIP pathway into CLIP-free models, activate it via guidance, and improve outputs," rather than as evidence that CLIP is inherently ineffective.

## Removed Points

- *"The CLIP pooling in HiDream-Fast having zero effect on all three metrics is suspicious"* — This is simply an empirical finding; there is no evidence of an error. The paper shows CLIP is genuinely ignored by the modulation layers.
- *"Section 3 notation conflates FLUX and COSMOS architectures"* — The notation y(p,t) is general and correctly covers both cases; no actual confusion arises in Section 5.
- *"The CausVid dynamic degree improvement is an order of magnitude larger than others"* — Large gains on specific metrics can occur in specific models; this is not inherently a flaw unless the metric is known to be unreliable, which is not argued.
- *"Table 1 shows FLUX schnell short prompts drop ImageReward 28%"* — The paper body properly acknowledges this at lines 80–81. This critique duplicates Minor weakness 2 above.

## Novel Insights

None beyond the paper's own contributions. The harsh critic's analysis mainly surfaces known concerns about framing and completeness that are standard for conference reviewing.

## Suggestions

1. **Re-frame the COSMOS/CausVid experiments.** Explicitly acknowledge that the distillation objective is designed to make the CLIP embedding neutral, and that the value of these experiments is in demonstrating that modulation guidance can *activate* a CLIP pathway in models designed without one — not that CLIP embeddings are inherently inactive.

2. **Add a summary comparison table to the main paper.** A single table comparing modulation guidance against Normalized Attention Guidance and Concept Sliders on a common set of prompts would address the most significant evidential gap.

3. **Tone down the abstract** to match the nuanced finding: CLIP's contribution is prompt-length-dependent and model-dependent, rather than "generally negligible."

4. **Report confidence intervals or error bars** for all automatic metrics, especially given the small magnitude of some reported improvements.

## Score and Decision

The paper makes a genuine contribution: it identifies that pooled CLIP embeddings are underutilized in several current diffusion transformers, and proposes a simple, effective guidance method that produces measurable improvements across diverse models and tasks. The core method is clean, well-motivated, and training-free. The evaluation is broad. None of the identified weaknesses invalidate the core claims — they concern framing, presentation, and completeness. With relatively modest revisions (re-framing the CLIP-free experiments, adding a baseline summary table, and adjusting the abstract), the paper would be clearly acceptable.

MY FINAL SCORE: <score>7.0</score>
MY FINAL DECISION: <decision>Accept</decision>