Now let me write the final consolidated review.

## Summary

This paper proposes Insertion Language Models (ILMs), which generate sequences by inserting tokens one at a time at arbitrary positions, trained via a denoising objective where tokens are dropped rather than masked. The method aims to overcome ARMs' fixed left-to-right generation order and MDMs' reliance on fixed-length mask tokens. The paper evaluates ILMs on planning tasks (star graphs, zebra puzzles) and text generation/infilling (LM1B, TinyStories).

## Strengths

- **Well-motivated problem framing with concrete examples.** Section 1 clearly illustrates ARMs' limitations (left-to-right constraint prevents lookahead for planning) and MDMs' limitations (simultaneous unmasking producing incoherent outputs like "The chef added sugar to the dessert to make it healthier," and fixed mask counts preventing arbitrary infilling). These examples make the motivation compelling and accessible.

- **Insightful synthetic task design (star graphs, Section 5.1.1).** The Star_easy → Star_medium → Star_hard progression isolates specific model failure modes: symmetric vs. asymmetric graphs with variable arm lengths. ILM achieves 100% and 99.1% on Star_medium and Star_hard where MDMs drop to 36.5% and 21.0%. This provides strong evidence that one-at-a-time insertion with relative position information is genuinely beneficial for these planning problems.

- **Zebra puzzle results (Section 5.2, Table 1).** ILM achieves 90.0% sequence accuracy, outperforming both ARM (81.2%) and MDM (82.6%), and approaching the oracle-decomposed ARM (91.2%). This is a clean, well-supported result on a task where out-of-order generation provides a structural advantage.

## Weaknesses

### Major

- **Abstract overclaims text generation performance.** The abstract states ILMs "perform on par with ARMs" in unconditional text generation, but Table 2 shows ILM NLL of 4.67 vs. ARM's 3.94 on LM1B (an 18.5% gap). Only on Stories is ILM close (2.14 vs. 2.11). The introduction more accurately describes ILMs as "competitive with ARMs." The abstract should be revised to match the evidence; the LM1B gap undercuts the claim that ILMs are a viable general-purpose language model.

- **Systematic length miscalibration undermines the variable-length claim.** Table 2 shows ILM generates sequences with mean length 119 on Stories (vs. 205 in training data, 201 for ARM) and 21 on LM1B (vs. 28 in training data, 30 for ARM) — undershoots of 42% and 25% respectively. The stopping classifier (Section 3, L_stop) is designed to govern length but clearly does not work well. Since one of the paper's headline advantages over MDMs is arbitrary-length generation, this is a significant practical limitation.

- **Training objective bias is acknowledged but uncharacterized in the main text.** Section 3 (line 79) states the objective is "biased" and refers to Appendix D, but the main text provides no analysis of: what probability distribution over sequences this objective implicitly defines, under what conditions it approximates the true denoising objective, or whether the inference procedure corresponds to the reverse of any valid noising process. This theoretical gap makes it difficult for readers to assess what the model is actually optimizing.

### Minor

- **Prometheus LLM-judge evaluation (Figure 5) lacks numerical values.** The results are described only in alt text without hard numerical values, error bars, or significance tests. Prometheus 2 is a learned judge with known variability; the paper makes qualitative claims (ILM outperforms on "coherence" and "consistency") without providing the underlying numbers to substantiate them.

- **Missing baselines for improved MDM samplers.** Section 4 discusses improved inference-time samplers for MDMs (greedy unmasking from Gong et al. 2024, top-k sampling from Zheng et al. 2024, flow-based sampling from Campbell et al. 2024), but the text experiments evaluate only vanilla tau-leaping MDM. Since the paper critiques MDMs' simultaneous-unmasking problem, evaluating at least one improved sampler is needed to show ILM's advantage is not merely against the weakest MDM variant.

### Trivial

- The "ARMO" label in Table 1 is not defined in the caption (it means ARM trained on oracle-order outputs).

## Nice-to-Haves

- Report the model's own log-perplexity where tractable (e.g., for ARMs) alongside the external LLM metric.
- Add a wall-clock inference speed comparison, since the paper notes ILMs cannot use KV caching.
- Provide qualitative text generation examples (the paper gives planning examples but not text samples).

## Removed Points

These points from the input review were removed with justification:
- **Stopping classifier training/inference mismatch:** Removed (analysis showed the setup is consistent — during training b=0 means full sequence → classifier predicts "stop," matching inference).
- **Equation (2) normalization concern:** Removed (the paper clearly states d(k,v)=c(k,v)/n sums to 1, making the cross-entropy well-defined).
- **NLL metric criticism (using Llama instead of own likelihood):** Removed (external evaluator LLM is standard for non-autoregressive models where own-likelihood is intractable).
- **"Arbitrary position" framing as overstated:** Removed (the model inserts at any position between existing tokens — "arbitrary" is appropriate).
- **Figure 6 inconsistency:** Removed (alt-text mentioning ARM is a parser artifact; body text clearly compares MDM and ILM).
- **Missing fill-in-the-middle ARM infilling baseline:** Removed (paper explicitly scopes out ARMs for infilling as they need specialized training, and discusses limitations).
- **Formatting/style nitpicks:** Removed (parser artifacts, not author errors).

## Novel Insights

The input review's main insight is that the paper's strongest evidence comes from its planning and constraint-satisfaction experiments, not from text generation. The paper would be more compelling if it reframed its primary contribution around planning tasks (where results are genuinely strong) and presented the text results as preliminary evidence that the approach extends to natural language, rather than claiming parity with ARMs. The structural gap between the abstract's strong claims and the actual text results (especially the 42% length undershoot and 18.5% NLL gap on LM1B) is the review's most actionable finding.

## Suggestions

1. Revise the abstract to replace "perform on par with ARMs" with "are competitive with ARMs" — matching the introduction's language and the actual evidence.
2. Investigate the systematic length undershoot. Report the stopping classifier's precision/recall separately on held-out subsequences to diagnose whether the issue is in training or inference. Consider a learned length predictor or length-conditional sampling.
3. Add at least one improved MDM sampler (greedy or top-k unmasking) as a text-generation baseline to demonstrate the claimed advantage is robust, not a product of comparing against the weakest MDM variant.
4. Report numerical values and confidence intervals for the Prometheus evaluation (Figure 5).
5. Provide a brief theoretical characterization of the biased objective in the main text — even a statement about what approximation it corresponds to (e.g., a variational bound, a moment-matching estimator) would substantially increase reader confidence.

## Score and Decision

**Calibration anchors used across rounds:**

| Path | Score | Round | Itemized | Comparison |
|------|-------|-------|----------|------------|
| FiLM (UbOzNf6hGq) | 4.25 | R1 | Yes | Similar topic (any-order generation); ILM has stronger planning results and more novel method |
| COrAL (0JjsZC0w8x) | 5.75 | R1 | Yes | Similar scope (order-agnostic LM); ILM comparable but weaker theoretical grounding |
| Interpolating AR+DD LMs (tyEyYT267x) | 8.00 | R1 | Yes | Much stronger theoretically and empirically; ILM clearly below |
| EDLM (sL2F9YCMXf) | 6.75 | R1 | Yes | Stronger theory and text results; ILM weaker on both |
| Beyond Autoregression (NRYgUzSPZz) | 6.25 | R2 | Yes | Similar structure (strong planning, weaker text); ILM has slightly weaker theoretical justification |
| DDPD (MJNywBdSDy) | 5.75 | R2 | Yes | Comparable scope; DDPD has stronger theoretical grounding but ILM has stronger planning experiments |

**Bracket determination (Round 1 → Round 2):** The paper sits below high-7 and 8+ anchors (Interpolating AR+DD LMs, EDLM) but above 4.25 (FiLM). The closest comparable anchors are COrAL (5.75), Beyond Autoregression (6.25), and DDPD (5.75). Comparing favorability profiles: ILM's strengths (10.57–11.73) are competitive with these anchors, and its most negative weakness (-0.34 for Prometheus evaluation) is milder than the most negative weakness in any of the comparable anchors (COrAL: -0.33 for missing baseline description; DDPD: -2.03 for narrative issues; FiLM: -4.59 for content concerns). However, the three major weaknesses identified above are substantive and structural, not merely presentational. The paper's genuine contributions on planning tasks, combined with the need to address the length miscalibration and re-align claims with evidence, place it just below the clearly accepted anchors.

MY FINAL SCORE: <score>5.5</score>
MY FINAL DECISION: <decision>Accept</decision>