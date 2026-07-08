Now I have all the information needed. Let me compile the final consolidated review.

## Summary

This paper studies the effect of L0 (average number of active latents per token) on sparse autoencoder (SAE) quality. Using toy models with known ground-truth features, it demonstrates that setting L0 too low causes the SAE to mix correlated features (a form of feature hedging), while setting it too high causes degenerate solutions. The paper further shows that standard sparsity-reconstruction tradeoff plots can rank an incorrect low-L0 SAE above a perfect ground-truth SAE, making them a misleading evaluation tool. It introduces a decoder pairwise cosine similarity metric (c_dec) intended to identify the correct L0, and validates this metric on Gemma-2-2b and Llama-3.2-1b SAEs.

## Strengths

- **Clean toy-model demonstration of the core phenomenon (Section 3).** The paper constructs a synthetic setup where ground-truth features are known, and shows directly that low-L0 SAEs mix correlated features while matching-L0 SAEs recover true features. The experiment where the MSE of a ground-truth SAE is *worse* than that of an incorrect low-L0 SAE (Section 3.3: 2.73 vs 4.88) cleanly isolates the mechanism and shows that MSE can actively reward incorrect solutions. This is the strongest evidence in the paper. [weight=9.58]

- **Important critique of sparsity-reconstruction tradeoff plots (Section 3.4, Figure 4).** The paper demonstrates a scenario where a perfect ground-truth SAE would be rejected by the standard evaluation protocol, while a corrupted SAE would be preferred. This is a genuine contribution that challenges a widely used evaluation practice in the SAE literature. [weight=10.21]

- **Investigation of both positively and negatively correlated features (Section 3.1).** Showing that the mixing phenomenon inverts for anti-correlated features (negative components) is insightful and strengthens the mechanistic story. The paper connects this to real language data, noting that negative correlations are prevalent in natural language. [weight=10.69]

## Weaknesses

### Major

- **The claim that "most commonly used SAEs have an L0 that is too low" is not supported by the evidence presented.** This claim appears in the abstract (line 9), the introduction (line 37: "our work implies that most SAEs used by researchers today have too low an L0"), and the discussion (line 240). The sole evidence is "a cursory search of open source SAEs on Neuronpedia showing L0 less than 100 is very common" (relegated to Appendix A.13, which is not available for review). The paper has not established what the *correct* L0 should be for those specific SAEs (different models, different layers, different training distributions), nor is the search quantified or systematically compared. This is an unsupported leap that should be removed or severely qualified. The paper's core technical contributions (toy model demonstrations, c_dec metric) do not depend on this claim, so it is a framing issue rather than a fatal flaw. [weight=0.74]

### Minor

- **The c_dec metric has limited practical utility in real LLMs, despite the strong framing in the abstract ("our method finds the correct L0").** The paper's own results (Figure 8, Gemma-2-2b layer 5) show that c_dec spikes at very low L0 but then enters a "long shallow region" where it is essentially flat across a wide L0 range, with the global minimum in this flat region. The paper resorts to identifying the "elbow" visually, which is subjective. The paper acknowledges this ("we do not view this as a perfect guide," line 246), but the acknowledgment is in tension with the abstract's claim. In real LLMs the metric identifies a range where L0 is "not clearly too low" rather than a single correct value. [weight=-0.49]

- **The LLM evaluation is narrow relative to the paper's broad claims.** The experiments cover only 2 models (Gemma-2-2b, Llama-3.2-1b) and 3 layer-specific SAEs (layer 5 and 12 of Gemma-2-2b, layer 7 of Llama-3.2-1b). Sparse probing F1 scores vary by only ~0.04 across the entire L0 range (0.78 to 0.82). While 3 seeds per L0 are mentioned in the Figure 8 caption, no error bars or significance tests are shown for the probing results. For a paper that claims "most SAEs" have incorrect L0 and implies that current practices are systematically wrong, this is a narrow evidential base. [weight=0.85]

- **The toy model assumes perfectly orthogonal features (line 65), while the LRH states features are only *nearly* orthogonal (line 13).** The paper does not discuss how violations of orthogonality would affect the results or the c_dec metric. If underlying features have non-zero cosine similarity with each other, c_dec could be elevated even for a perfect SAE, potentially confounding the diagnostic. [weight=2.87]

- **The relationship to feature hedging (Chanin et al., 2025) is stated but not clearly delineated.** Chanin et al. showed that *narrow* SAEs (too few total latents) mix correlated features. This paper shows that low *L0 per token* causes mixing even with enough total latents. The paper says it is "a manifestation of feature hedging" (line 230) but does not explain why the mechanism is the same or different. These are related but mechanistically distinct phenomena (dictionary capacity vs. activation sparsity), and the ambiguity makes it harder to assess novelty. [weight=3.39]

### Trivial

None.

## Nice-to-Haves

- The paper could provide a more quantitative criterion for identifying the c_dec "elbow" (e.g., a threshold on the derivative of c_dec with respect to L0) instead of relying on visual inspection.
- Adding error bars and/or confidence intervals to the LLM sparse probing results (Figure 8) would help establish whether the ~0.04 F1 variation is meaningful relative to training variance.
- Discussing how violations of the orthogonality assumption in the toy model may affect generalizability of the c_dec metric to real LLM features.

## Removed Points

These points were raised in the input review but are removed with justification:

- **"Paper sets up a straw man" claim:** The reviewer argued the paper claims practitioners believe "any sufficiently low L0 is equally valid." The paper's actual claim (line 15) is that the *implication* of sparsity-reconstruction tradeoff plots is that any sufficiently low L0 is equally valid — this is an argument about what evaluation conventions imply, not a claim about explicit beliefs. This is a reasonable critique of standard practice, not a straw man.

- **JumpReLU observation caution:** The reviewer said the "sticking" observation should be treated with caution. The paper presents this as an observation and frames it as "a testament to Anthropic's training method," which is a reasonable interpretation of the data. This is speculative caution, not a concrete weakness.

- **"Too low and too high simultaneously" undermines central framing:** The paper explicitly discusses this complexity in Section 4.2. It adds nuance rather than undermining the core claims. The paper acknowledges there is "likely a range of L0s," which is consistent with the metric identifying a range rather than a single point.

- **Alternative mechanism analysis (training dynamics, optimization difficulties):** These are speculative concerns not concretely tied to evidence in the paper. The paper partially addresses initialization concerns (line 77).

- **Missing appendix content / formatting issues:** The appendix was stripped by the PDF parser; these sections exist in the original submission.

## Novel Insights

None beyond the paper's own contributions. The reviews surface no genuinely novel observation that is not already present or directly implied in the paper.

## Suggestions

1. Remove or heavily qualify the unsupported claim about "most commonly used SAEs" from the abstract and discussion. The paper's contributions stand without this claim.
2. Add error bars and/or confidence intervals to the LLM sparse probing results (Figure 8) to establish that the ~0.04 F1 variation is meaningful relative to training variance across seeds.
3. Discuss how the near-orthogonality (rather than perfect orthogonality) of real LLM features may affect the c_dec metric and the generalizability of the toy model findings.
4. Consider providing a more quantitative criterion for identifying the c_dec elbow (e.g., a threshold on the derivative of c_dec with respect to L0) instead of relying on visual inspection.

## Calibration Anchors

| Path | Avg Score | Round | Itemized? | Comparison |
|------|-----------|-------|-----------|------------|
| `tcsZt9ZNKD.md` (Scaling & evaluating SAEs) | 8.20 | 1 | Yes | SAE methods/scaling paper with much broader scope and stronger empirical validation. Not directly comparable. |
| `ghH6YYDs15.md` (Amortisation Gap) | 4.67 | 1 | Yes | Paper about SAE theoretical limitations. Had more negative-weighted weaknesses (-3.96, -1.48). Weaker toy model evidence. This paper is stronger. |
| `sknUS8X9q0.md` (SAGE) | 4.00 | 1 | Yes | SAE evaluation framework. Poorly presented, unclear novelty. This paper is significantly stronger. |
| `1Njl73JKjB.md` (Principled Evaluations) | 7.00 | 1 | Yes | SAE evaluation with supervised dictionaries. Stronger methodology, better writing, but also limited to single task. |
| `9ca9eHNrdH.md` (Canonical Units) | 7.00 | 2 | Yes | Very relevant: analyzes SAE limitations with novel methods (stitching, meta-SAEs). Stronger empirical validation and clearer contributions. |
| `LC2KxRwC3n.md` (A is for Absorption) | 7.50 | 2 | Yes | Very similar paper type: identifies SAE failure mode with controlled setting. Similar scope limitations (one model, one task). Was rejected despite high scores. |
| `89wVrywsIy.md` (Hierarchical Tracing) | 3.40 | 1 | No | SAE circuit analysis paper. Lower quality, less relevant. |
| `UbLvSPMvMA.md` (Sparsity beyond TopK) | 1.67 | 1 | No | Unrelated SAE architecture paper. |
| `XAjfjizaKs.md` (Multi-Layer SAEs) | 6.50 | 2 | No | Architectural contribution (MLSAE). Different kind of contribution. |
| `MDvecs7EvO.md` (Mechanistic Permutability) | 6.50 | 2 | No | Feature matching across layers. Different contribution type. |

**Bracket reasoning (Round 1 → Round 2):** Initial bracketing placed the paper between the 4.00–4.67 range (weaknesses strongly negative-weighted) and the 7.00–7.50 range (more comprehensive methodology). Round 2 narrowed the bracket by comparing weighted items against closely matched anchors. The paper's strengths weights (9.58–10.69) match or exceed those of the 7.00–7.50 anchors, but its weakness profile is more adverse: the overclaim about "most SAEs" and the limited LLM validation are real gaps that the 7.00-range papers (e.g., "Canonical Units," "Principled Evaluations") do not share to the same degree. Compared to the "Absorption" paper (7.50 avg, rejected), this paper has stronger toy model evidence but a similar scope limitation. The final score of 6.0 reflects a paper with genuine and well-supported core contributions that is held back by overclaiming in its framing and limited breadth of LLM validation.

**Score and Decision**

MY FINAL SCORE: <score>6.0</score>
MY FINAL DECISION: <decision>Accept</decision>