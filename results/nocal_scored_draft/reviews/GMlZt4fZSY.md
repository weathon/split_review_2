Now let me put together the final review.

## Summary

This paper presents MobileLLM-R1, a family of sub-billion-parameter reasoning language models (140M–950M) trained with only 4.2T tokens derived from ~2T unique curated open-source data. The core thesis is that careful data curation—via leave-one-out analysis to identify informative datasets, influence-based data mixture weighting (extending AutoMixer), and a mid-training compression procedure—can unlock strong reasoning capabilities in small models with far fewer tokens than commonly assumed. The 950M model achieves competitive AIME/MATH/HumanEval results and matches Qwen3-0.6B on several reasoning benchmarks while using ~11.7% of Qwen3's reported training tokens.

## Strengths

- **Well-controlled ablation isolating pretraining contribution (Table 2).** The paper evaluates all baseline models and MobileLLM-R1 under *identical* reasoning SFT data (one epoch on OpenMathReasoning + OpenScienceReasoning-2 + OpenCodeReasoning-2). This directly addresses the concern that results might be driven by better post-training data rather than better pretraining, cleanly separating the contribution of curated pre-training and mid-training data. This is the right experimental design for the paper's central claim.

- **Leave-one-out analysis (Figure 3) is computationally expensive but informative.** Training separate models while excluding individual datasets and measuring NLL on capability-probing datasets provides real signal about which data sources matter for which capabilities. The finding that FineWeb-Edu has the largest cross-domain impact is non-trivial, and the observation that StarCoder benefits math more than OpenWebMath benefits code is an interesting empirical insight that challenges conventional assumptions about domain transfer in small models.

- **Open-source commitment.** The paper commits to releasing all trained models, code, and training recipes with full rationale for each data selection. For a paper whose contribution is partly a training recipe and partly empirical findings about data curation, this is essential for community impact.

- **The central empirical demonstration is significant.** A 950M model achieving competitive AIME scores and matching Qwen3-0.6B on multiple reasoning benchmarks while using 4.2T tokens (11.7% of Qwen3's 36T) is a tangible demonstration of data-efficiency principles applied to small reasoning models. The comparisons against OLMo-2-1.48B and SmolLM2-1.7B (where MobileLLM-R1-950M is smaller) are particularly clean.

## Weaknesses

### Fatal
None. No identified issue invalidates the paper's core claims or results.

### Major
None. The weaknesses below are addressable and do not undermine the paper's overall conclusions.

### Minor

- **Size asymmetry in the headline comparison is under-acknowledged.** The paper repeatedly frames MobileLLM-R1-950M (~949M params) against Qwen3-0.6B (~600M params) as an apples-to-apples demonstration of data efficiency ("matches or surpasses Qwen3-0.6B" while emphasizing "only 11.7% of the tokens"). This is a **58% parameter increase** that works in the paper's favor and is never mentioned in these comparisons. The comparisons against OLMo-2-1.48B and SmolLM2-1.7B (where MobileLLM-R1 is smaller) are clean, but the most attention-grabbing claim conflates data efficiency and model capacity. The abstract and introduction should either compare 950M against a similarly sized open model or explicitly state the parameter difference alongside the token efficiency claim.

- **Novelty boundary with AutoMixer is unclear.** The influence-based data weighting methodology (Section 2.2) explicitly extends AutoMixer (Chang et al., 2025). The paper cites AutoMixer for the efficient Hessian approximation and describes its extension (capability-probing datasets, self-influence and cross-influence across three domains). However, the demarcation is blurry: the main additions—using multiple capability-specific probing sets instead of a single validation set, and introducing cross-influence terms—are relatively incremental. The paper would benefit from stating explicitly what changes were required to make AutoMixer work at 4.2T-token scale and what specific aspects constitute new methodological contributions versus direct application.

- **"~2T unique tokens" vs. "4.2T total tokens" needs clarification.** The abstract states that ~2T tokens of high-quality data are sufficient, and 4.2T tokens are used via resampling from these ~2T. The comparison to Qwen's "36T-token corpus" is ambiguous: is that 36T unique tokens or 36T total training tokens? If 36T is total training tokens, the comparison as stated is fair; if 36T is unique tokens, the paper's own unique token count (~2T) actually strengthens the data-efficiency claim and should be stated explicitly for both models.

- **Mid-training trajectory description (Figure 6) oversimplifies the data.** The paper claims "the subsampled data maintains higher downstream performance throughout training," but at step 30,000 the original data (MMLU 38.0) substantially outperforms the subsampled data (MMLU 29.0). The "pronounced performance dip around 30K steps" actually occurs between 30K and 40K (38.0 → 31.0). The final performance does favor the subsampled data and the overall stability observation is valid, but the characterization of individual steps should be accurate.

- **Domain-specialized models for influence computation are underspecified (Section 2.2).** The paper states that checkpoints θ_{C,t}, θ_{M,t}, θ_{K,t} are "obtained by training separate models to convergence on the full training sets of domains C, M, K" but does not describe their architecture, token budget, or training setup. Since the influence computation is central to the data mixing methodology, this information is needed for reproducibility.

- **Mid-training data augmentation lacks specifics (Section 3).** The paper augments the Dolmino dataset with "additional mathematics and programming data" without specifying how much data, from which sources, or the augmentation ratio relative to the Dolmino base. These details are necessary for reproducibility.

- **NLL proxy in LOO analysis is not validated against downstream benchmarks (Section 2.1).** The leave-one-out analysis uses NLL on capability-probing datasets rather than actual downstream benchmark performance. The paper acknowledges this is computationally necessary and avoids benchmark overfitting, but it does not provide any correlation evidence linking NLL improvements on probing datasets to actual reasoning benchmark gains. A qualitative or quantitative bridge between the proxy metric and target capabilities would strengthen the analysis.

- **Table 2's controlled SFT comparison has a starting-point asymmetry.** Baseline models use their instruct checkpoints while MobileLLM-R1 uses "intermediate Tulu3-SFT checkpoints" (trained for 2 epochs on Tulu3 data). If a baseline was already well-aligned to a different data distribution, adding one epoch of reasoning SFT on a new distribution could be less beneficial. This does not invalidate the comparison but should be acknowledged as a confound in interpreting the results.

### Trivial

- **Pareto frontier claim (Figure 1, line 46) is stated without explanation.** The paper claims MobileLLM-R1 is on "the Pareto frontier of accuracy-training-token efficiency trade-off curve" but does not explain how the frontier was computed or whether the model is actually on the frontier versus simply closer to it than other models. This should be clarified in the caption or text.

## Nice-to-Haves

- Directly validate the influence-based weighting against simpler alternatives (e.g., random subsampling to 2T unique tokens with uniform weights, or heuristic upsampling of math/code data) on downstream benchmarks rather than just perplexity.
- Train a 600M-parameter variant of MobileLLM-R1 with the same pipeline and compare directly against Qwen3-0.6B to cleanly separate data efficiency from model capacity.

## Removed Points

These points were filtered from the harsh critic input per review guidelines:
1. **Missing architecture details** — The paper states architecture details are in Appendix A (line 408: "We describe data processing procedures, model architectures, training configurations, and hyperparameters in detail in Sections A."). The appendix was stripped by the parser; this is not an author omission.
2. **Tokenizer comparison affecting token counts** — Speculative without evidence the tokenizers differ in compression rate.
3. **Mid-training influence scoring selection bias** — Reasonable in principle but speculative without evidence of actual harm caused.
4. **Section-by-section notes subsumed by specific weaknesses above** (abstract framing, AIME noise floor discussion).

## Novel Insights

None beyond the paper's own contributions. The reviews surface the same strengths and limitations that the paper itself presents, without adding a fundamentally new perspective on the results.

## Suggestions

- Explicitly state parameter counts when comparing MobileLLM-R1-950M against Qwen3-0.6B (e.g., note the 58% size difference alongside the token efficiency claim).
- Clarify whether Qwen's 36T refers to unique or total training tokens, and state both unique and total token counts for both models.
- Correct the mid-training trajectory description in Section 3 to accurately reflect that the subsampled data underperforms at 30K steps but becomes superior later.
- Provide details on the domain-specialized model training (architecture, token budget) and mid-training data augmentation (sources, quantities, ratios) in a revised version.

## Score and Decision

This is a solid empirical paper with a clear thesis, well-designed experiments (particularly the controlled SFT ablation in Table 2 and the LOO analysis), and a genuine open-source commitment. The weaknesses are bounded and addressable: they concern framing (size asymmetry in the headline claim), clarity (novelty boundary with AutoMixer, token count definitions), and underspecified details (domain-specialized models, mid-training augmentation). None invalidate the core contribution — that careful data curation can unlock reasoning in sub-billion models with far fewer tokens than commonly assumed. The paper makes a meaningful contribution to the growing literature on small reasoning models and should be of interest to the community.

MY FINAL SCORE: <score>7.0</score>
MY FINAL DECISION: <decision>Accept</decision>