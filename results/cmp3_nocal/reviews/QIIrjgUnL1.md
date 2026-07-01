## Summary

This paper proposes EPAR (Explicit Position-Attention Relationship), a framework that models position-attention interactions through a parametric exponential decay function applied at the attention score level. The method introduces an exponential position effect function P_effect(i,j,L) = α·e^{-β|i-j|/L} with an enhanced variant incorporating a γ floor to prevent long-range attention collapse, and a triple-attention architecture with task-aware and content-aware modules. Empirical results across five NLP benchmarks show modest but consistent improvements (1.8-8.9%) over baselines including RoPE, ALiBi, and relative position encoding.

## Strengths

- **Clean, simple formulation.** The position effect function P_effect(i,j,L) = α·e^{-β|i-j|/L} and its enhanced variant with γ (Equation 3) are mathematically simple and easy to implement, with clear equations provided in Sections 4.1 and 7.1.

- **Consistent empirical improvements across several tasks.** Table 3 shows the proposed method achieves modest but consistent gains over the best baseline across WikiText-103 (PPL 22.4 vs 23.5), WMT'14 En-De (BLEU 30.1 vs 29.1), SQuAD 2.0 (F1 0.851 vs 0.831), GLUE (Acc 0.867 vs 0.852), and ArXiv (ROUGE-L 0.478 vs 0.439). Statistical testing (Bonferroni-corrected p<0.01) and Cohen's d effect sizes are reported.

- **Explicitly acknowledges limitations.** Sections 9.1-9.2 discuss scenarios where the method underperforms (noisy data, non-sequential tasks, extreme parameter values, sequences beyond 2048 tokens), which many papers omit.

## Weaknesses

### Fatal
None.

### Major

- **Factual inconsistency and overclaimed novelty relative to ALiBi.** The paper repeatedly claims that "existing position encoding methods (RoPE, ALiBi, relative position encoding) operate at the vector representation level" (line 15, also lines 23, 58–62, 120, 132) and that a "fundamental shift" is to operate at the attention score level. **This is factually incorrect for ALiBi.** ALiBi (Press et al., 2021) adds a distance-based bias directly to attention scores: A_ij = Q_i^T K_j / √d_k + m·|i−j|. Worse, the paper's own Table 2 correctly lists ALiBi's "Operation Level" as "Attention score," creating a direct internal contradiction between the prose and the table. The genuine contribution — the specific parametric form (multiplicative exponential decay with a γ floor) — is a variation on distance-based attention modulation, not the "fundamental paradigm shift" the paper claims. This overclaiming pervades the Abstract, Introduction, and Section 5.1.1 and undermines the paper's central argument.

- **Inflated theoretical contributions.** The paper presents continuity, differentiability, and monotonicity as "provable properties" and "fundamental mathematical properties that distinguish our approach" (Abstract, Sections 1, 4.2, 5.1.2, line 88). For the function α·e^{-β|x|/L}, these are trivial properties following directly from the exponential function being continuous, differentiable, and monotonically decreasing. Proving them is a basic calculus exercise, not a substantive theoretical contribution. Claiming they "are not possible with implicit encoding approaches" (line 88) is overstated — these properties also hold for ALiBi's linear bias and RoPE's rotation function. The paper lists "Rigorous Mathematical Foundation" as one of three main contributions (line 30), but the main text provides no mathematics beyond writing down the exponential function and noting standard properties of exponentials. Theorems 2–5 are mentioned by name but their content, assumptions, and conclusions are never summarized in the main text.

- **Unexplained mutual information claims.** Section 5.1.1 (line 134) claims the method achieves I(P;A) = 0.78·H(P) (78% of theoretical maximum), outperforming RoPE (52%), ALiBi (61%), and Shaw (48%). These numbers are presented as bare assertions with no definition of the probability space, no explanation of how mutual information between "position" (P) and "attention" (A) is defined or computed, and no supporting analysis in the main text. These claims are central to the "information-theoretic superiority" narrative but are entirely unsubstantiated as presented.

- **Circularity in the synthetic evaluation framework.** The consistency metric C (Section 5.2) measures "agreement between attention distributions and theoretical optimal positions." However, these "theoretical optimal positions" are derived from the position value function V(i) = Σ_j A_ij · I_j (Section 4.5), where A_ij itself depends on the proposed P_effect function. The optimal position is thus defined within the method's own framework, making it tautological that the method scores highly on alignment with it. When the paper reports 0.9063 consistency (ours) vs 0.78 (RoPE) at line 92, it is unclear whether this reflects genuine superiority or merely that the metric is implicitly calibrated to favor the proposed approach.

### Minor

- **Triple-attention architecture underspecified in the main text.** The TaskWeight and ContentImportance functions in Equation (4) are defined only by references to Appendix A.4 and A.5. The main text does not explain how these modules are computed, parameterized, whether they are learned or hand-designed, or what features they use. Since the triple-attention architecture is listed as a main contribution (Section 1) and produces the best results (Table 3), leaving these components opaque in the main text makes the results difficult to interpret or reproduce from the paper alone.

### Trivial
None.

## Nice-to-Haves

- Including a summary of training hyperparameters (optimizer, learning rate, schedule, batch size, epochs) in the main text would make the experimental setup more accessible, though relegating these to the appendix is standard practice.
- Demonstrating a case where the explicit analyzability yields a non-trivial actionable insight (e.g., deriving an optimal information placement strategy and verifying it experimentally with an independent ground truth) would break the circularity of the current "optimal position derivation."

## Removed Points

These points from the harsh critic's review were removed or moved here with justification:

- "Missing training details in main text" — training hyperparameters are relegated to Appendix A.13, which is standard practice for ICLR papers; not a substantive weakness.
- "Missing comparisons against more recent position-aware methods" — cannot verify the existence or appropriateness of such methods without external knowledge.
- "Related work too brief" — the paper has a dedicated related work section (Section 3) plus Table 2; brevity is stylistic, not substantive.
- "Theorems 2-5 relegated entirely to appendix" — the parser strips the appendix from the submitted paper; the criticism that the main text does not summarize these theorems is absorbed into the "Inflated theoretical contributions" weakness above.
- Several formatting/style nitpicks — these are PDF parser artifacts, not author errors.
- "Fundamental shift framing is misleading" — this criticism is valid; it has been absorbed into the ALiBi inconsistency weakness above.
- Training details criticism — the paper provides model dimensions, datasets, baselines, default hyperparameters, seeds, and references Appendix A.13; this is adequate for main-text disclosure.

## Novel Insights

The input review's key insight beyond the paper's own contributions is the identification that the paper's central novelty claim (operating at the attention score level vs. vector representation level) is factually undercut by ALiBi, which already operates at the attention score level — and that the paper's own Table 2 contradicts its prose on this point. This is not speculative but directly verifiable from the paper. A second important observation is that the "theoretical guarantees" (continuity, differentiability, monotonicity) are trivial properties of an exponential function presented as substantive contributions, and that the mutual information claims are presented without any derivation. These three observations collectively reveal a pattern where a modest but real empirical contribution is dressed in substantially overstated novelty and theoretical claims.

## Suggestions

1. **Correct the factual claim about ALiBi.** Acknowledge that ALiBi also operates at the attention score level, and reframe the paper's novelty as the specific multiplicative exponential functional form (with γ floor) rather than a "fundamental shift" in operation level.
2. **Recalibrate the theoretical contribution.** Remove or significantly downplay the "theoretical guarantees" framing for continuity, differentiability, and monotonicity. If Theorems 2–5 contain genuine results, summarize their key content and assumptions in the main text.
3. **Either derive the mutual information claims or remove them.** Presenting bare percentages without any explanation of the underlying computation, probability space, or definition of variables is not acceptable.
4. **Clarify the consistency metric's ground truth.** Explain how "theoretical optimal positions" are defined independently of the proposed P_effect, or reframe the metric as an internal diagnostic rather than a comparative evaluation against baselines.
5. **Sketch TaskWeight and ContentImportance in the main text.** Even a paragraph-level description of how these functions operate, what inputs they use, and whether they are learned would significantly improve reproducibility.

## Score and Decision

MY FINAL SCORE: <score>4.5</score>
MY FINAL DECISION: <decision>Reject</decision>