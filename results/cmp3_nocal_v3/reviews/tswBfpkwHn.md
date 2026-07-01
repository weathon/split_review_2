## Summary

This paper provides the first theoretical analysis of the SGD training dynamics of a one-layer Mamba model for in-context learning (ICL), studying how the model learns to handle prompts containing additive outliers. The authors prove convergence and generalization guarantees (Theorems 1–2), compare against a one-layer linear Transformer baseline (Theorems 3–4), and decompose Mamba's mechanism into a linear attention component that selects same-pattern examples (Corollary 1) and a nonlinear gating component that suppresses outliers while imposing an exponential recency bias (Corollary 2). Synthetic experiments support the theoretical predictions.

## Strengths

- **First analysis of Mamba *training dynamics* for ICL.** Prior work (Li et al., 2024b; 2025b) studied global minima and expressivity of Mamba-like models; this paper studies whether SGD actually reaches those solutions and with what complexity. Theorems 1 and 3 are direct counterparts to Theorem 3.3 in Li et al. (2024a) for Transformers, establishing the right reference class.

- **Clean ablation through the gating mechanism.** The paper models the linear Transformer as "Mamba with G=1" (Section 2, Equation 3), which means the comparison isolates the effect of the nonlinear gating layer. Any difference in behavior can be attributed to gating, which is the paper's stated goal (Remark 6). This is a principled ablation study.

- **Interpretable mechanistic decomposition.** Corollary 1 shows that linear attention concentrates weight on same-pattern examples; Corollary 2 shows that gating suppresses outlier-containing examples (Equation 17) while imposing exponential decay with index distance (Equation 18). These are specific, falsifiable predictions that the paper then tests empirically (Figures 3 and 4).

- **Empirical experiments verify the main theoretical predictions.** Figure 2 confirms the predicted threshold behavior (Mamba maintains error < 0.01 at α ≈ 0.8, while the linear Transformer's error spikes at α > 0.5). Figures 3–4 directly confirm the attention concentration and gating patterns predicted by Corollaries 1 and 2. Table 1 reveals a nontrivial position-sensitivity trade-off that is discussed in the paper.

- **Transparent scoping and honest caveats.** The paper explicitly clarifies that (i) the comparison is with *linear* Transformers, not softmax-attention Transformers (Remark 6), (ii) the theory is for one-layer models (Section 1.1), (iii) test outliers must contain positive linear combinations of training outliers (Theorem 2(a), line 93), and (iv) the query itself contains no outliers (line 117). The limitations section discusses the scope.

## Weaknesses

### Fatal
None.

### Major
None.

### Minor

- **No statistical reporting.** All experimental results (Figures 2, 3, 4; Table 1) are presented as point estimates without error bars, confidence intervals, or mention of multiple runs. For synthetic data where multiple runs are essentially free, this is a meaningful omission. It is impossible to assess whether observed differences (e.g., the 82.73% vs. 93.96% in Table 1) are reproducible or within run-to-run noise.

- **Mechanistic experiments use 3-layer models while the theory is for 1 layer.** The mechanistic analysis in Section 4.2 (Figures 3, 4, Table 1) uses three-layer Mamba and linear Transformer models, while the entire theoretical framework (Theorems 1–4, Corollaries 1–2) is proved for one-layer models. The paper states that "the results … in the other two layers exhibit the same trend as the first layer" (line 275) and says the experiments "verify" Corollary 1, but this conflates empirical consistency on a deeper architecture with theoretical verification. The one-layer experiments (Figure 2) correctly match the theory. The paper should either provide some argument for why the one-layer analysis extends, or run the mechanistic experiments on one-layer models as well.

- **The test-time outlier guarantee is confined to the span of training outliers.** Theorem 2, Condition (a), requires test outliers to be positive linear combinations of training outlier patterns. While this is stated transparently (line 93, Remark 3), the paper describes it as "a wide range of possible outlier patterns" (line 181). In practical threat models where an adversary can introduce entirely novel outlier types orthogonal to training outliers, the guarantee does not apply. The paper would benefit from a clearer statement of this scope limitation when summarizing the robustness claim.

- **Position sensitivity is an important trade-off that receives insufficient emphasis in the high-level framing.** Table 1 shows that when outliers are placed closest to the query (CQ), Mamba achieves only 82.73% accuracy vs. 93.96% for the linear Transformer — an 11+ point deficit. The paper reports this finding and explains it mechanistically (the gating's exponential decay pushes clean examples' weight down when outliers are near the query). However, the abstract and conclusion characterize Mamba's robustness without referencing this conditional nature. The trade-off (robust to high outlier fraction but sensitive to outlier position) is an important part of the story that deserves more prominence in the paper's high-level claims.

- **The claimed "superior robustness" to high α is conditioned on l_ts ≤ p_a·l_tr.** The claim in the introduction that Mamba "can maintain accurate ICL generalization even when the fraction of outlier-containing context examples approaches 1" (line 31) is technically supported by Theorem 2 only when the test prompt is short enough relative to the training prompt (Condition (c): α < min(1, p_a·l_tr/l_ts)). This is a real constraint and could be stated more prominently alongside the headline claim.

- **Key practical limitations are scoped out.** The analysis assumes (i) the query contains no outliers (line 117), (ii) no softmax attention in the baseline, and (iii) binary classification with orthogonal patterns. These are standard for theoretical work in this area, but the paper could more clearly connect these to practical applicability.

### Trivial
None.

## Nice-to-Haves

- **Test against outliers orthogonal to training outlier span.** An obvious experiment would be to test Mamba's performance when test prompts contain outliers completely orthogonal to all training outlier patterns, to see where the empirical breakdown occurs.

- **Ablation on hyperparameters.** The experiments use a single configuration (d=30, M1=6, M2=10, V=3, β=3, κa=2). An ablation varying the number of patterns, outlier magnitude, or training outlier fraction would demonstrate robustness of the conclusions.

- **Interpretation of the poly(M1^κa) term.** This term in the prompt length requirements (Equations 8 and 12) is not interpreted. It suggests an exponential dependence on outlier magnitude — the paper should clarify what this means practically.

## Removed Points

- **"The comparison with 'Transformers' is misleading — it's really Mamba without gating."** This criticism is factually incorrect. The paper consistently says "linear Transformer" throughout all technical sections: Contribution 2 (line 33), Section 3.4 heading (line 185), P2 (line 95), Remark 6 (line 209), and the experimental sections. The title does not mention Transformers. The abstract says "a linear Transformer can tolerate." The paper is transparent about the comparison being with linear attention. REMOVED: factually wrong.

- **"The paper overclaims by framing as Mamba vs Transformers."** Same as above — the paper repeatedly and explicitly says "linear Transformer." REMOVED: factually wrong.

- **"The test-time guarantee is severely restricted / structural."** The condition is stated transparently in Theorem 2(a) and in plain language (line 93). Calling this "structural" or "fatal" overstates the issue. DEMOTED to Minor with softened language.

- **"The gating/training trade-off is tautological."** The reviewer notes the comparison is "somewhat tautological" because the gating creates the optimization difficulty it then addresses. This is not a weakness — it is the paper's stated thesis. REMOVED: not a valid weakness.

- **Missing appendix content or proofs.** The reviewer mentions not being able to verify derivations in Appendix E.1. The parser strips appendices from all papers. REMOVED: parser artifact.

## Novel Insights

The reviews surface an important subtlety: the gating mechanism's exponential recency bias (Corollary 2(ii)) is simultaneously the source of Mamba's outlier-fraction robustness and its position-sensitivity vulnerability. When outliers are far from the query (FQ), the same exponential decay that discounts them also allows clean near-query examples to dominate. When outliers are placed near the query (CQ), the decay penalizes the clean examples that get "pushed" farther away. This mechanistic double-edged-sword is the paper's most practically relevant insight and deserves to be centered rather than treated as a side finding. No other novel insight emerges beyond the paper's own contributions.

## Suggestions

1. Add error bars (at minimum 5 random seeds) to all experimental figures and Table 1.
2. Either run the mechanistic experiments (Figures 3–4) on one-layer models to directly verify Corollaries 1–2, or soften the "verifies" language to "is consistent with."
3. Rephrase the abstract and conclusion to explicitly note that Mamba's robustness is to high outlier *fraction* and that sensitivity to outlier *position* (particularly near-query placement) is a known vulnerability of the mechanism.
4. Include a brief experiment or discussion of how Mamba performs when test outliers are orthogonal to all training outlier patterns.
5. Provide intuition for the poly(M1^κa) term in the prompt length bounds — does this imply that larger outliers require exponentially more context examples?

## Score and Decision

This paper makes a genuine theoretical contribution: it is the first to analyze SGD training dynamics of a Mamba model for ICL, provides an interpretable decomposition of the gating mechanism's role (Corollaries 1 and 2), and backs its predictions with controlled experiments. The paper is transparent about its scope (one-layer theory, linear attention baseline, orthogonal pattern data model). The main weaknesses — lack of error bars, use of 3-layer models for mechanistic experiments, and insufficient emphasis on the position-sensitivity trade-off in the high-level framing — are addressable and do not undermine the core theoretical contribution.

MY FINAL SCORE: <score>8</score>
MY FINAL DECISION: <decision>Accept</decision>