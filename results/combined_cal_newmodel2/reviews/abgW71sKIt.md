Now let me write the final consolidated review.

## Summary

This paper investigates why naive output alignment fails in 1-bit post-training quantization (PTQ) of LLMs and proposes a method with three components: (1) an Output Error objective that accounts for accumulated quantization error by using full-precision inputs as targets, (2) a selective-layer design that applies output alignment only to the last FC layer of each block, and (3) an Attention Matrix Preservation (AMP) mechanism that uses gradient-sign masking to preserve token-similarity structure. Experiments on OPT (1.3B–30B) and LLaMA-2/3 models show consistent perplexity and accuracy improvements over existing 1-bit PTQ methods.

## Strengths

- **The preliminary analysis in Section 3 is a genuine diagnostic contribution.** The authors demonstrate concretely that (a) layer-wise output alignment (ARB-X) does not monotonically improve block-level loss (Figure 1), (b) the Activation-conditioned Error objective diverges from the true Output Error as quantization errors accumulate (Figure 2, top panels), and (c) token-similarity matrices drift from the full-precision baseline with depth (Figure 2, bottom panel). The design of quantizing one layer at a time while keeping others at full precision cleanly isolates these effects. This analysis is informative independent of the proposed method.

- **Consistent improvement across nearly all evaluated settings.** Tables 1 and 2 show the proposed method outperforms PB-LLM, BiLLM, ARB-RC, and ARB-X on C4, WikiText-2, PTB, and zero-shot QA, across OPT (1.3B–30B) and LLaMA-2/3 families. On smaller OPT models the gains are non-trivial (e.g., 27.70 → 24.69 on OPT-1.3B C4; 26.40 → 24.30 on WikiText-2).

- **Clean ablation of two of the three design choices.** Tables 3 and 4 separate the contributions of AMP (~10 PPL improvement on LLaMA-2-7B C4) and the Output Error objective (~0.7 PPL improvement), providing evidence for individual components.

## Weaknesses

### Major

- **Mathematical error in Equation (9) (AMP objective).** The paper equates the Frobenius norm of a Hadamard product ||A ⊙ B||_F with the Frobenius inner product Tr[AB^T]. These are not equivalent: ||A ⊙ B||_F = sqrt(Σ_i Σ_j (A_ij B_ij)^2), while Tr[AB^T] = Σ_i Σ_j A_ij B_ij. The trace expression defines a sensible objective (maximizing alignment of token-similarity matrices via their inner product), but the first line of Equation (9) with the Hadamard product and Frobenius norm is mathematically incorrect as a derivation. This is an error in a core equation of the proposed method that the authors must correct.

- **Selective-layer design choice is stated without supporting evidence.** The paper restricts output alignment to "only the last fully connected layer of each block" (Section 4.2), claiming it "has the most direct impact on the block loss," but provides no analysis, ablation, or comparison to alternative selection rules (e.g., all layers, attention output layer, two layers per block). Since this is one of three stated design choices alongside the output-error objective and AMP, and the other two are ablated, the absence of validation for this choice is a significant gap.

### Minor

- **The LLaMA-2-7B PTB anomaly is dismissed without investigation.** The proposed method achieves perplexity 3166 vs ARB-RC's 763.19 and ARB-X's 681.24 on this setting. While the paper correctly notes that other baselines also perform poorly (BiLLM: 5243) and that very large perplexity values are uninformative, the fact that Ours (3166) underperforms ARB-RC (763) and ARB-X (681) by a large margin is not explained. This could indicate an undocumented numerical instability or data-dependent vulnerability.

- **AMP mechanism is a heuristic with limited characterization.** The sign-based binary mask (update if gradient>0, keep if gradient<0) uses a threshold at zero with no analysis of why this threshold is appropriate. The paper does not report mask density, stability across layers, or sensitivity to initial parameter values. Additionally, the token-similarity proxy (computed from FFN outputs) is acknowledged as only a proxy for attention but is treated throughout as directly preserving attention mechanisms without validation of the proxy's fidelity.

### Trivial

None.

## Nice-to-Haves

- Reporting variance estimates or result stability over multiple calibration draws would strengthen confidence in small-margin improvements (e.g., OPT-30B C4: 13.34→13.15; AveQA OPT-13B: 55.01→55.06).

## Removed Points

These points are flagged to be removed, treat them with caution:
- "No variance/confidence intervals" → Moved to Nice-to-Haves (standard practice in PTQ is single-run evaluation; not a core flaw).
- "The method is effectively ARB-RC + small modifications" → Removed: the contributions (Output Error objective, AMP, diagnostic analysis) go beyond incremental modification; Tables 3/4 show clear ablation support.
- "Equation 2 typo" → Removed per hard rule (typos/formatting artifacts).
- "How is X obtained during optimization?" → Removed: standard PTQ practice.
- "No comparison to training-based methods (BitNet)" → Removed: outside the paper's PTQ scope.
- "Section 3.1 claim overstated" → Removed: paper's nuanced claim ("does not necessarily improve") is accurate.
- "Overhead analysis deferred to appendix" → Removed: appendix stripped by parser.
- "Missing experimental details (calibration samples, sequence length)" → Removed: likely in stripped appendix.
- Section-by-section presentation notes → Removed as formatting/presentation nitpicks.

## Novel Insights

The most valuable synthetic insight from combining the reviews is the asymmetry in contribution strength: the diagnostic analysis in Section 3 is the paper's strongest, most original element, while the proposed method is pragmatically constructed from individually plausible but less rigorously justified heuristics (selective-layer choice, AMP sign-masking). This creates a mismatch between the paper's framing ("three principled design choices that solve output alignment") and what is actually demonstrated (a set of reasonable heuristics built on genuine diagnostic insights). The diagnostic findings alone could support a stronger contribution if the method were presented more modestly as a proof-of-concept deriving from those findings.

## Suggestions

1. **Correct Equation (9):** Replace the Frobenius norm of the Hadamard product with the Frobenius inner product (which the trace expansion correctly computes), and update the surrounding text.
2. **Ablate the selective-layer design:** Compare output alignment on (a) all layers, (b) attention output layer, (c) two layers per block, and (d) the last FC layer, to justify the chosen rule.
3. **Investigate the PTB anomaly:** Determine whether it is a numerical issue (e.g., pseudoinverse stability on certain activation distributions) or a genuine generalization failure.
4. **Characterize AMP mask behavior:** Report mask density, inter-layer variation, and sensitivity to initial parameter values across models.

## Score and Decision

**Calibration summary:**
- EfficientQAT (3.00, Reject): limited novelty, unfair comparison. *My paper is stronger: clear diagnostic insights, consistent improvements.*
- Pyramid VQ (5.00, Reject): split reviews; poor presentation. *My paper is comparable in contribution level but has a mathematical error.*
- LLM-QAT (5.00, Reject): solid incremental contribution, limited novelty. *My paper has similar overall quality but a more notable flaw (Equation 9).*
- OSTQuant (6.20, Accept): well-received PTQ method with minor issues. *My paper has stronger diagnostic contributions but a mathematical error and missing ablation that OSTQuant does not.*
- One QuantLLM (4.50, Reject): split reviews, practical relevance questioned. *My paper has clearer methodological contributions.*

**Round 1 bracket:** ~3.5–5.5 (above EfficientQAT, below OSTQuant)

**Round 2 narrowing:** The paper's strengths (favorability up to 15.35) rival accepted papers, but its lowest weakness favorability (0.28 for the AMP sign-masking heuristic, 1.30 for the Equation 9 error) places it below the ~6+ acceptance threshold where weaknesses remain comfortably positive. Comparison with LLM-QAT (5.00, all 5s) shows a comparable profile: solid but not exceptional, with notable but not fatal gaps.

**Final score:** 4.5

**Final decision:** Reject

MY FINAL SCORE: <score>4.5</score>
MY FINAL DECISION: <decision>Reject</decision>