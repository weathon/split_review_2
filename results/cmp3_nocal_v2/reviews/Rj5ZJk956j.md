## Summary

This paper proposes a simple but effective method for analyzing gated neurons in LLMs: computing cosine similarities between the three weight vectors (w_gate, w_in, w_out) of each neuron to characterize its read-write (RW) functionality. Applying this method across 9-12 models, the authors discover a consistent cross-model pattern where early-middle layers are dominated by conditional strengthening neurons while late layers shift toward weakening neurons. Focusing on the small class of weakening neurons, the paper reports that they activate very frequently and have outsized influence on model behavior, with a surprising mechanism involving negative gate values.

## Strengths

1. **Simple lens that reveals consistent cross-model structure.** Computing cosine similarities between the three weight vectors of gated neurons is refreshingly simple. Its most compelling output is Figure 1(a): the median of cos(w_in, w_out) traces a positive-to-negative trajectory across layers that is qualitatively the same in nine different LLMs. This is not an artifact of a single architecture or training setup, and it is the kind of finding that could genuinely influence how the community thinks about MLP layer roles.

2. **The negative-gate-value finding is genuinely surprising.** The discovery that case (iii) activations (x_gate < 0, x_in < 0, producing x_post > 0) of weakening neurons contribute meaningfully to sharpening the output distribution runs counter to the sensible intuition that negative gate values are negligible training artifacts. The specific mechanism — weakening neurons flipping to strengthening behavior under negative gate values — is mechanistically well-explained (Section 6.2) and cleanly connected to the RW taxonomy.

3. **The conditional ablation tool is useful and cleanly defined.** Splitting activations by the sign of x_gate and x_in to localize which sub-behavior drives an effect (Section 6.2) is a natural but effective methodological contribution that can be reused in other neuron analysis work.

## Weaknesses

### Fatal
None.

### Major

1. **Ablation evidence for "outsized influence" does not control for activation frequency, which Section 7 identifies as a strong confound.** The headline claim is that weakening neurons have outsized influence on model behavior. The ablation baseline — random neurons from the same layers (Section 6.1, line 192) — controls for layer distribution but not for activation frequency. Section 7 itself demonstrates that weakening neurons activate very often (consistent with Gurnee et al., 2024), while strengthening neurons activate rarely. The paper does not check whether a matched set of high-frequency non-weakening neurons produces similar effects. The claim that "other RW classes do not show effects" (deferred to appendix) does not answer this because other classes may have vastly different activation frequencies. The experimental design conflates class identity with activation frequency, and the conclusion may be correct but is not cleanly separated from this alternative explanation.

2. **Functional-importance claims rely on one model (OLMo-7B).** The universal cross-model pattern in Section 5 is demonstrated across 12 models, but the ablation experiments establishing the "outsized influence" of weakening neurons (Sections 6–8) are conducted only on OLMo-7B. The paper states this is for resource reasons (line 188), but it creates a gap: the strongest evidence for universality is about weight geometry, while the functional-importance claim rests on a single model.

### Minor

3. **No statistical testing for ablation results.** The entropy histograms (Figure 3b) and attribute rate comparisons (Figure 3a) are described qualitatively. No confidence intervals, standard errors, effect sizes, or significance tests are reported for the ablation experiments. For a nuanced claim like "case (iii) shows entropy effects similar to weakening neurons as a whole," quantitative comparisons (e.g., mean entropy shift, distribution tests between conditions) would substantially strengthen the evidence.

4. **Preprocessing justification deferred to appendix.** The paper multiplies w_in and w_out by sign(cos(w_gate, w_in)) as a preprocessing step (Section 3.2, line 85). Since the entire taxonomy (Table 1) is defined by cosine similarities computed on these transformed weights, the mathematical justification that this does not change model behavior should be prominent in the main text rather than deferred to Appendix C. While the transformation likely preserves model output (two sign flips cancel), a reader cannot verify this from the main text.

5. **Activation frequency analysis only on OLMo-7B.** Unlike the weight-cosine analysis, which is cross-validated across 12 models, the activation frequency analysis (Section 7) and its connection to neuron importance is shown only for OLMo-7B. The correlation breakdown in the last two layers (r = -0.29, +0.29) also suggests the relationship is less universal than implied, but the paper does not discuss whether this pattern holds across models.

6. **"First to observe" framing partially undercut by concurrent work.** The paper claims to be "the first to observe a mechanism involving negative gate values" (abstract, line 9; conclusion, line 281) while acknowledging Kong et al. (2025) as "concurrent work who focus on a different phenomenon" (line 227). If another group has independently found that negative gate values are functionally important, the "first" framing is fragile regardless of differences in the specific phenomenon studied.

### Trivial

7. The 243 weakening neurons ablated in Section 6 are not contextualized with the total neuron count for OLMo-7B, making it hard for the reader to assess how small this class really is.
8. Attribute rate (one of two main ablation metrics) is not defined or explained in the main text — it is referenced to Geva et al. (2023) and deferred to Appendix F (line 213). A reader unfamiliar with that work cannot evaluate whether attribute rate is a meaningful or narrow metric.
9. The relationship between Table 1's six prototypical classes and Figure 1(b)'s eight categories (which include "atypical" variants) could be clearly stated for the main ablation: do the 243 "weakening neurons" include atypical weakening, or just the non-atypical weakening class?

## Nice-to-Haves

- Disentangle class identity from activation frequency in the ablation experiments: add a baseline of high-frequency non-weakening neurons (frequency-matched to weakening neurons). If the effect persists, the claim is much stronger; if it disappears, the contribution shifts to "weakening neurons have high activation frequency, which correlates with functional impact" — still valuable but a weaker claim.
- Replicate ablation experiments on at least one more model (e.g., Llama-3.2-3B or Gemma-2-2B) to support the claim that weakening neurons are universally influential rather than a quirk of OLMo-7B.
- Include a table showing, for OLMo-7B, the count of neurons per RW class per layer to contextualize all ablation results.
- Provide formal statistical comparisons (e.g., distribution tests, effect sizes) for the conditional ablation entropy results.

## Removed Points

These points from the harsh review are flagged for removal; treat them with caution:

- **Histogram similarity speculation:** The reviewer claims the six histograms in Figure 3(b) "all look similar" and the key comparison rests on "a minor difference in distribution tails." This judgment is based on an incomplete figure caption, not the actual figure. Without seeing the visual evidence, this criticism is speculative rather than grounded.
- **Case study criticism ("only illustrative"):** The reviewer faults the case study (Section 8) for not providing "independent evidence for the claims." Case studies in interpretability work are inherently illustrative; their value is in grounding abstract claims in concrete examples. This is not a weakness.
- **Preprocessing affecting sign analysis (speculative):** The reviewer worries the preprocessing "could change which vector is 'positive' and affect the conditional ablation sign analysis." The paper applies preprocessing consistently to the entire analysis framework (taxonomy, ablations, and sign analysis). Since the transformation preserves model behavior exactly, the analysis is internally consistent; this concern is a hypothetical without evidence that it causes a problem.

## Novel Insights

The most valuable observation from the harsh review is the activation frequency confound in the ablation experiments. The reviewer correctly identifies that the paper's strongest functional claim ("weakening neurons have outsized influence") is supported by an experimental design that does not separate class identity from a known correlate (activation frequency). This is not a flaw in the RW taxonomy or the cross-model patterns (which are well-evidenced), but it means the paper's most attention-grabbing claim needs tighter evidence. Interestingly, the reviewer's own suggested fix — frequency-matched baselines — would strengthen the paper considerably if the effect survives, or reframe it if it doesn't. Either outcome is informative.

## Suggestions

1. **Add frequency-matched baselines to the ablation experiments** (non-weakening neurons matched on activation frequency from the same layers). This is the single highest-impact improvement.
2. **Move the preprocessing justification from the appendix to Section 3.2** (or at minimum provide a brief intuitive argument in the main text). The taxonomy depends on it.
3. **Run ablation experiments on at least one additional model** to extend the functional-importance claim beyond OLMo-7B.
4. **Add a table of class counts per layer** for OLMo-7B (and ideally other models) to help readers contextualize the ablation results.
5. **Report effect sizes or confidence intervals** for the entropy and attribute rate ablation comparisons.

## Score and Decision

MY FINAL SCORE: <score>6</score>
MY FINAL DECISION: <decision>Accept</decision>