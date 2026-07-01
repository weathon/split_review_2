## Summary

This paper identifies a training-inference mismatch in tree-based speculative decoding: draft models are trained on linear token sequences but deployed on trees during inference. It contributes two complementary techniques to address this: TALF (Tree-Aware Loss Function), which aggregates cross-entropy losses over tree-structured training data to align draft model predictions with the target LLM across all branches, and SALF (Stopping at Low Further Gains), a dynamic tree construction algorithm with a principled monotonicity-based stopping criterion that balances drafting overhead against tree optimality. The combined system achieves 15.6–39.4% and 6.5–24.4% end-to-end speedups over EAGLE-2 and HASS across three model families and five tasks without changing the draft model architecture.

## Strengths

1. **Well-diagnosed and motivated problem (Section 3.1, Figure 2).** The paper identifies a genuine oversight in prior draft model training (EAGLE, HASS): sequence-based training ignores that inference uses trees. Figure 2 provides concrete evidence — HASS improves calibration on 1st-ranked tokens but has marginal/negative gains on lower-ranked tokens, which nonetheless constitute >10% of draft tree nodes. This diagnosis directly motivates TALF.

2. **Clean contribution decomposition (Table 2).** The 9-condition ablation (3 tree construction methods × 3 loss functions) cleanly isolates the individual and combined benefits of TALF and SALF. This design reveals meaningful patterns, e.g., that SALF reduces draft quality (τ) but improves end-to-end speedup by cutting drafting overhead, and the improvement is smaller for TALF-trained models (which have fewer "wasteful" nodes to prune) — a nice internal consistency check.

3. **Consistent and substantial empirical gains (Table 1).** Across Llama-2-7B, Llama-3.1-8B, and DeepSeek-R1-Distill-Llama-8B, on 5 diverse tasks at 2 temperatures, SALF & TALF consistently outperform both EAGLE-2 and HASS with large margins (15.6–39.4% and 6.5–24.4% relative improvements). The gains are systematic rather than cherry-picked.

4. **Theoretical grounding for SALF (Theorem 1, Appendix C).** The monotonicity guarantee for the probability sum S_i provides a principled justification for the SALF stopping criterion, distinguishing it from a heuristic early-exit.

5. **Parameter sensitivity analysis (Tables 3, 4).** The paper examines the effect of the top-k training parameter and the SALF threshold th, showing how performance varies and providing guidance for default choices.

## Weaknesses

### Fatal

None.

### Major

1. **Missing ablation: regression loss removal vs. tree structure as the source of TALF's improvement.** TALF drops the feature regression loss L_reg that both EAGLE and HASS use (line 114). The paper states that "training solely on the token probability distributions across multiple nodes was sufficient... yielding better performance," but provides no ablation comparing TALF *with* regression loss against TALF *without* it. Since HASS also uses tree attention during loss computation, the key difference between HASS and TALF is twofold: (a) tree-structured training data and (b) removal of L_reg. Without this ablation, we cannot fully attribute TALF's gains to tree-awareness vs. the removal of a potentially harmful loss term. The paper's core claim (that tree-awareness drives improvement) would be stronger if this were isolated. While TALF clearly outperforms HASS regardless of which factor dominates, a direct ablation would cleanly resolve the attribution question.

### Minor

2. **Unsupported claim of "no generation quality degradation" (line 274).** The conclusion asserts speedups "without any generation quality degradation." While this is a *theoretical* property of speculative decoding with rejection sampling (assuming correct implementation), and neither TALF nor SALF modifies the verification mechanism, the paper makes an explicit empirical-sounding claim without any supporting measurement (e.g., output perplexity, task accuracy, or distribution distance). Providing even a brief empirical sanity check or clearly qualifying this as a theoretical property would strengthen the paper.

3. **Training protocol asymmetry for EAGLE-2 comparison (line 196).** For Llama-2-7B and Llama-3.1-8B, EAGLE-2 is evaluated with a 10-epoch draft model, while TALF and HASS get 3 additional epochs of fine-tuning. This gives TALF/HASS a small extra training budget relative to EAGLE-2, which could partly explain the speedup gap. The comparison between TALF and HASS is fair (same protocol), but the EAGLE-2 baseline comparison is not fully controlled for training compute. The paper should acknowledge this confound more explicitly.

4. **SALF threshold default choice justification (Table 4, line 264).** The paper chooses th=0.6 as the default, citing "more consistent performance improvements for the tested target LLMs," but sensitivity data is only shown for DeepSeek-R1-Distill-Llama-8B. For this model, th=0.5 yields the highest mean speedup (2.62× vs. 2.59× for th=0.6). The claim of "more consistent performance" across models is not empirically demonstrated in the paper.

### Trivial

None.

## Nice-to-Haves

- **Fixed tree during training vs. dynamic tree during inference (lines 110–112).** The paper acknowledges that the training tree is precomputed by the target model and fixed across epochs, while inference trees depend on the draft model. This is a practical compromise the paper is transparent about; discussing it as a limitation in the conclusion would be helpful but is not required.
- **Output quality verification.** As noted in Weakness #2, a brief empirical check (even a single paragraph in the appendix) would provide direct support for the "no quality degradation" claim.
- **Regression loss ablation.** As noted in Weakness #1, adding TALF+L_reg to Table 2 would cleanly isolate whether the improvement comes from tree-structured data or loss function simplification.

## Removed Points

- **"Fixed tree during training vs. dynamic tree during inference" framed as a limitation:** The paper already explicitly acknowledges this (lines 110–112) as a practical compromise. Restating it as a weakness without adding new analysis is redundant.
- **"Omission of Griffin (Hu et al., 2025) as a direct baseline":** The paper mentions Griffin in the introduction (line 17) and focuses comparisons on the most directly relevant prior methods (EAGLE-2, HASS). What constitutes the appropriate baseline set is a scope judgment, and the paper provides sufficient comparison.
- **"Comparison with a tree-trained variant of HASS":** The reviewer acknowledges this would be "substantial" and "not strictly necessary." It is speculative and burdensome.
- **Various framing/section notes:** General observations that the paper is "clear" or "adequate" are not weaknesses; they are commentary.
- **The reviewer's Section-by-Section notes that praise clarity:** These are already captured in the Strengths or are neutral commentary.

## Novel Insights

The main novel observation is that existing tree-based SpD methods train draft models on linear sequences while deploying them on trees, causing a systematic misalignment on lower-ranked tokens. This is well-documented with calibration evidence (Figure 2). A second insight is that the probability sum of candidate nodes during tree expansion is monotonically decreasing (Theorem 1), which enables a principled stopping criterion that replaces heuristic early-exit approaches.

## Suggestions

1. Add an ablation to Table 2 (or a new table) comparing TALF without L_reg (current) against TALF with L_reg (re-adding the feature regression loss used in EAGLE/HASS). This would directly answer whether the tree-structure or the loss function simplification drives TALF's gains.
2. Include a brief empirical output quality check (e.g., perplexity on a held-out set or task accuracy) to support the "no quality degradation" claim, or qualify it as a theoretical property of the SpD framework.
3. Add a paragraph or table showing SALF threshold sensitivity for at least one more model family to support the claim of "more consistent performance" for th=0.6.
4. Acknowledge the training protocol asymmetry (extra 3 epochs for TALF/HASS vs. EAGLE-2) explicitly in the experimental setup or limitations.

## Score and Decision

The paper makes genuine, well-motivated contributions with consistent empirical gains across multiple models and tasks. The two main weaknesses (missing regression loss ablation, unsupported quality claim) are evidential gaps rather than structural flaws — they do not undermine the core finding that SALF & TALF improve upon strong baselines. The evaluation is thorough, the ablation is informative, and the theoretical grounding for SALF is a nice addition.

<score>8</score>
<decision>Accept</decision>