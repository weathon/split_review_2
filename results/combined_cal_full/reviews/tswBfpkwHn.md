Now I have all the information needed. Let me produce the final review.

## Summary

This paper provides the first theoretical analysis of training dynamics and in-context learning (ICL) generalization for a one-layer Mamba model in the presence of outliers. It derives a closed-form expression for the Mamba output (Equation 3), showing it decomposes into a linear attention component and a nonlinear gating component. The paper proves convergence guarantees (Theorem 1), generalization bounds for distribution-shifted prompts with outliers (Theorem 2), and a comparison showing that Mamba can tolerate a higher fraction of outlier-containing examples (α approaching 1) than a linear Transformer (α < 1/2, Theorem 4). Corollaries 1–2 mechanistically explain how the linear attention selects relevant examples and the gating suppresses outliers with exponential recency bias. Experiments on synthetic data qualitatively verify the theoretical predictions.

## Strengths

- **First theoretical analysis of Mamba's ICL training dynamics.** The paper derives a closed-form expression (Equation 3) for a one-layer Mamba in the prompt-query ICL setting, decomposing it into a linear attention component and a nonlinear gating component. This is a non-trivial mathematical derivation that extends the theoretical ICL literature beyond Transformers, and the authors are transparent about its one-layer scope. (weight: +5.38)

- **The mechanism analysis in Corollaries 1 and 2 is genuinely insightful.** It shows concretely how Mamba's two components contribute to ICL: the linear attention selects examples sharing the same relevant pattern as the query (Corollary 1), while the gating layer suppresses outlier-containing examples and induces an exponential "recency bias" (Corollary 2, Equations 17–18). This provides a clean decomposition that explains both Mamba's robustness to outliers and its sensitivity to outlier position (CQ vs FQ in Table 1). (weight: +5.52)

- **The theoretical comparison reveals a concrete, non-obvious threshold.** Linear Transformers provably require α < 1/2 for ICL generalization with outliers (Theorem 4), while Mamba can tolerate α approaching 1 (Theorem 2), provided test outliers lie in the span of training outliers. The experiments (Figure 2) verify this qualitative threshold across three different outlier labeling schemes, making this a crisp theoretical prediction that distinguishes the architectures. (weight: +4.53)

- **The paper is honest about its limitations.** It acknowledges the one-layer, single-head, linear-attention scope (Remark 6), identifies Mamba's sensitivity to outlier position (Table 1, CQ setting), and notes the comparison is to a *linear* Transformer rather than full softmax/multi-head attention. (weight: +1.71)

## Weaknesses

### Fatal
None.

### Major
None.

### Minor

- **"Unseen" outliers terminology could be more precise.** The paper repeatedly uses "unseen" to describe test-time outliers (Abstract: "unseen outliers that are linear combinations of the training-time outliers"; P1: "previously unseen, but should contain a positive linear combination"; Remark 3: "unseen distribution-shifted outliers"). While the condition is always explicitly stated, the term "unseen" invites a broader reading than the theorem supports: test outliers must lie in the convex cone spanned by training outliers (Equation 11: a positive linear combination of training outlier patterns). A genuinely novel outlier pattern orthogonal to all training outliers is not covered. The qualification is present but sharper language (e.g., "unseen *in the sense of having novel coefficients*") would better align with the theorem's scope. (weight: +2.48)

- **Missing statistical rigor in experiments.** Figures 2 and Table 1 do not report error bars, standard deviations, confidence intervals, or the number of random seeds/trials. Given that the data generation involves random sampling (patterns, coefficients, labels, outlier positions), individual runs could vary. While single-run evaluation is common in theory papers where the central contribution is analytic, adding variance information would strengthen the empirical validation and better rule out the possibility that reported differences reflect favorable single runs. (weight: +0.10)

- **Single experimental configuration.** The main experiments use one setting (d=30, M₁=6, M₂=10, V=3, β=3, κ_a=2, δ=0.2, p_a=0.6). Showing robustness to these hyperparameters within the ranges allowed by the theoretical conditions would strengthen the paper and demonstrate that the theory's sufficient conditions are not overly conservative. (weight: -1.59)

- **CQ limitation merits more prominent treatment.** Mamba's significant performance drop when outliers are closest to the query (CQ: 82.73% vs linear Transformer 93.96% in Table 1) is a concrete failure mode predicted by the theory itself. This finding receives only a few sentences at the end of Section 4.2 despite being a differentiating prediction of the mechanism analysis. Highlighting it more prominently would strengthen the paper's scientific narrative and demonstrate that the theory makes testable predictions beyond just "Mamba is better." (weight: +2.63)

### Trivial
None.

## Nice-to-Haves

- **Ablation within Mamba:** The paper compares Mamba to a linear Transformer (which is effectively Mamba without gating). An even cleaner ablation would be to train a "Mamba without gating" (G ≡ 1 in the same architecture) and compare it to the full Mamba under identical conditions. The Transformer comparison already serves this purpose, but an explicit within-Mamba ablation would isolate the gating contribution more directly.
- **Sensitivity analysis over hyperparameters:** Varying d, M₁, M₂, β, κ_a, δ, p_a within the ranges allowed by the theoretical conditions would demonstrate robustness.

## Removed Points

**Removed: "The paper conflates 'Transformers' with 'linear Transformers' — the comparison is framed to invite a broader interpretation."**
Fact-checked against the paper: every mention is explicitly qualified. The abstract says "linear Transformers," Section 3.4 heading says "ONE-LAYER SINGLE-HEAD LINEAR TRANSFORMERS," Remark 6 acknowledges the scope explicitly. The paper is careful about this distinction.

**Removed: "Theorem 2's condition is substantially more restrictive than the paper's language suggests — an evidential issue."**
Fact-checked: every mention of the condition is explicitly qualified. Abstract: "unseen outliers that are linear combinations of the training-time outliers." P1: "previously unseen, **but should contain a positive linear combination**." Remark 3: "Each additive outlier in the test prompt should contain a linear combination of the V training outlier patterns." The critic's characterization as a "significant overstatement" is not supported by the paper text.

**Removed: "'Approaches 1' in the abstract is stronger than what the conditions support in practice."**
Theorem 2 gives α < min(1, p_a·l_tr/l_ts), which can approach 1 when p_a is near 1 or l_tr >> l_ts. The statement is about what the theory *allows*, not a claim about a specific experimental configuration.

**Removed: Generic/superficial strengths** (e.g., "the paper addresses an important problem") — not specific enough to this paper's contribution to be informative.

## Novel Insights

None beyond the paper's own contributions. The reviews do not surface a perspective that meaningfully reframes or extends the paper's own theoretical characterization.

## Suggestions

- Add error bars or variance information (standard deviations over 5–10 random seeds) to Figures 2 and Table 1.
- Tighten the "unseen" terminology in the abstract and main text to match what Theorem 2 actually covers.
- Give the CQ failure mode more prominent treatment — it is a differentiating, testable prediction of the theory.
- Run a sensitivity analysis over at least a few key hyperparameters to demonstrate that the sufficient conditions are not overly conservative.

---

**Calibration Summary**

Retrieved anchors and their relationship to this paper:

| Anchor | Score | Round | Itemized? | Comparison |
|--------|-------|-------|-----------|------------|
| aN4Jf6Cx69 — ICL mechanistic basis | 4.50 | R1 | Yes | Similar theoretical ICL paper but about transformers; had stronger positive items (+7.37) but also meaningful negatives (-4.48). This paper's positives are slightly weaker but it lacks the severe negatives. |
| HuBFimORiz — ICL Markov chains | 4.33 | R1 | Yes | ICL theory with heavy negative weights (-7.12, -4.64, -4.05). This paper has substantially less severe weaknesses. |
| i9RTCC6whL — Mamba Lyapunov stability | 4.67 | R1 | Yes | Similar Mamba analysis with comparable positive weight magnitude but had notable negative weights (-6.36, -5.18). This paper's weaknesses are all minor. |
| gK1rl98VRp — ICL emergence AR-NTP | 6.00 | R1,R2 | Yes | Broader-scope ICL theory accepted at 6.0. Had negative items (-7.42, -7.41) alongside strong positives. This paper has narrower scope (one-layer, binary) but fewer flaws. |
| aKJr5NnN8U — ICL vs IWL | 6.50 | R2 | Yes | Strong ICL theory paper with very heavy criticism on some points (-10.58). This paper has fewer weaknesses overall. |
| E8TPUAimyJ — Context-scaling vs task-scaling | 4.50 | R2 | Yes | ICL paper with severe structural criticism (-10.52, -8.02). Not comparable in weakness severity. |

**Round 1 bracket inference:** The paper sits between the 4.33–4.67 anchors (which have real structural weaknesses absent here) and the 6.0–6.5 anchors (which have broader scope but also more ambitious claims that draw fire). My draft's weighted items: strengths at +5.38, +5.52, +4.53, +1.71 and weaknesses all near-zero or minor positive (range -1.59 to +2.63). No item pushes strongly downward. This places the paper clearly above the 4-range papers and plausibly in the 5.5–6.0 range.

**Narrowing:** Compared to the 6.0 anchor (gK1rl98VRp), this paper's scope is more restricted (one-layer Mamba on binary tasks vs AR-NTP for general sequences) and its experimental validation thinner (single configuration, no error bars). These factors pull it slightly below that anchor, placing the final score at 5.5.

MY FINAL SCORE: <score>5.5</score>
MY FINAL DECISION: <decision>Accept</decision>