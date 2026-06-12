## Summary

This paper presents the first systematic study of how reasoning data—varying in scale, diversity, and quality—affects LLM performance when introduced at different training stages (pretraining vs. supervised fine-tuning). Through large-scale experiments pretraining 8B models from scratch for 1T tokens with controlled reasoning data injections, the authors find that front-loading reasoning into pretraining creates durable foundations that post-training cannot recover (≈19% gain on expert benchmarks). Crucially, they uncover an asymmetric allocation principle: diversity drives pretraining effectiveness while quality governs SFT, and naïve SFT scaling with noisy data can be actively harmful.

## Strengths

* **First systematic study of reasoning data placement across full training pipeline:** The paper addresses an important gap by jointly examining pretraining, SFT, and RL phases under controlled conditions, providing clear causal evidence about the role of timing in reasoning data allocation.
* **Clear, actionable asymmetric principle:** The finding that pretraining benefits most from diversity/scale while SFT is dominated by quality is a novel and practically useful guideline that challenges simplistic "more is better" approaches.
* **Robust experimental design with controlled budgets:** The authors fix total token budgets (1T) and reasoning token budgets (80B) across comparisons, isolate effects through fully crossed designs (4 pretrain variants × 3 SFT recipes), and include RL validation on expert benchmarks like AIME.
* **Important refutation of the "catch-up" hypothesis:** Showing that doubling SFT epochs on high-quality data cannot compensate for missing reasoning-rich pretraining (Table 4) has significant implications for training strategy.
* **Demonstration of latent quality effects:** The finding that high-quality pretraining data shows minimal immediate benefit but "unlocks" +4% gains after SFT is a subtle and insightful result that deepens understanding of pretraining–alignment interactions.

## Weaknesses

### Fatal
None.

### Major
* **Limited to single architecture and scale:** The main experiments use only one 8B hybrid Mamba2-attention model from a specific family. While the authors reference a 1.2B Transformer experiment (Table 14), the full details are in the stripped appendix, making it difficult to assess robustness across architectures in the main paper. Generalizability to pure Transformers, different model sizes, and other training infrastructures remains unverified from the main text alone.
* **RL phase comparison is very narrow:** Only two models (M_base and M_LMQ with SFT_SH) are carried through RL (Table 3). This limited comparison (one baseline, one best variant) weakens the claim that pretraining advantage "compounds" through RL—the paper would benefit from showing at least 3–4 model variants through RL.

### Minor
* **Lack of uncertainty quantification:** All results are reported as point estimates without standard deviations, confidence intervals, or multiple seeds. Given the stochasticity in pretraining and evaluation, some measure of variability would strengthen the reliability claims.
* **The SFT data budget (4.8M samples) is not consistently specified:** Section 3.1 says "4.8M reasoning samples from D_res" but it is unclear which specific dataset(s) this refers to in the main averaged results (Table 2), making it hard to reproduce the exact SFT setup.
* **Baseline model receives more base data than reasoning models:** The design gives M_base 1T base tokens while reasoning models get 920B base + 80B reasoning tokens. While total tokens are fixed, this confound means the comparison tests "replace some base data with reasoning data" rather than "add reasoning data." This is a reasonable trade-off but should be explicitly discussed as such.

### Trivial
None.

## Nice-to-Haves
* Include error bars or multiple seeds for at least the key comparisons (Tables 1, 3, 4) to quantify variability.
* Show more RL baselines (e.g., M_LDQ + SFT_SH + RL, M_SHQ + SFT_SH + RL) to strengthen the claim that pretraining benefits compound consistently.
* Provide a public subset of the reasoning data or a detailed recipe that would allow partial reproduction without proprietary corpora.

## Novel Insights

The paper's most compelling contribution is the discovery of the asymmetric data allocation principle—the same data characteristics (diversity vs. quality) have opposite optimality patterns depending on training phase. This reveals that the long-standing assumption that "good data is good data" regardless of when it is used is incorrect. Furthermore, the latent effect of high-quality pretraining data that only manifests after SFT is a genuinely novel observation that suggests pretraining and alignment interact in more complex ways than simple "foundation + fine-tuning" models capture. The finding that naively scaling SFT with mixed-quality data actively harms math reasoning (-5%) while a mere 0.4% addition of high-quality data improves performance is a stark demonstration that quality, not quantity, governs SFT efficacy.

## Suggestions
- Clarify in Section 3.1 which specific SFT dataset(s) constitute the "4.8M reasoning samples" used in the default SFT recipe, and specify how these map to D_SHQ, D_LDQ, etc. in the averaged results.
- Add a discussion of the limitation that M_base sees more base data than reasoning models, and explain why this is a conservative test (if anything, more base data should favor M_base, making the gap conservative).
- In Table 6 and Table 7, consider reporting per-domain breakdowns consistently with earlier tables to make the breadth-alignment trade-off more transparent.

## Score and Decision

MY FINAL SCORE: <score>8.0</score>
MY FINAL DECISION: <decision>Accept</decision>