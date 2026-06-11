## Summary
# Final Review Report

## Summary

This paper presents the first theoretical analysis of the training dynamics and in-context learning (ICL) generalization of a one-layer Mamba model, focusing on binary classification tasks where prompts may contain additive outliers. The authors prove convergence and sample complexity bounds (Theorem 1), characterize ICL generalization under distribution-shifted outliers (Theorem 2), and compare these results with one-layer linear Transformers (Theorems 3-4). A key finding is that Mamba's nonlinear gating mechanism enables robustness to outlier fractions approaching 1, whereas linear Transformers can only tolerate outlier fractions less than 1/2. The paper also characterizes the dual mechanism—linear attention for pattern selection and nonlinear gating for outlier suppression and local bias (Corollaries 1-2). Experiments on synthetic orthogonal-pattern data confirm the theoretical predictions.

The analysis is technically rigorous within its scope but rests on strong assumptions (orthogonal patterns, one-layer architecture, hinge loss, SGD) that significantly limit its generality. The position-dependent robustness revealed in Table 1 (82.73% accuracy when outliers are closest to the query vs 99.73% when farthest) represents a critical caveat to the paper's central robustness claim.

## Strengths
**1. First theoretical analysis of Mamba's ICL training dynamics.** The paper addresses an important gap: while Mamba has shown empirical ICL capabilities, its theoretical understanding was limited. The analysis of training dynamics via SGD with hinge loss is a meaningful contribution to the theoretical literature on state-space models.

**2. Clean conceptual separation of mechanisms.** The decomposition of Mamba's output into a linear attention term and a nonlinear gating term (Eq. 3) is elegant and enables direct comparison with linear Transformers. This formulation makes the role of each component explicit and the derivations of Corollaries 1-2 intuitive.

**3. Rigorous sufficient-condition analysis.** The theorems provide well-structured sufficient conditions (batch size, outlier magnitude, context length, iterations) for convergence and generalization. The comparison with linear Transformers is systematically conducted under the same data model, isolating the effect of gating.

**4. Honest acknowledgement of comparison scope.** Remark 6 explicitly clarifies that the comparison is between one-layer linear Transformers and one-layer Mamba, and acknowledges that larger Transformers with softmax attention may achieve better robustness. This transparency is commendable.

**5. Position-dependent robustness identified in experiments.** Table 1 revealing Mamba's vulnerability to outlier placement (CQ setting) is an important empirical finding that enriches the paper's narrative beyond the theoretical claims. The connection between this vulnerability and the exponential decay of gating values (Corollary 2) demonstrates good theory-experiment alignment.

## Weaknesses
### W1. Strong orthogonality assumptions limit generality (Major)
The entire theoretical framework rests on the assumption that relevant patterns $\mu_j$, irrelevant patterns $\nu_k$, and additive outliers $v_s^*$ are all mutually orthogonal with equal norms $\beta$. This assumption is critical for the proof mechanisms: the linear attention selects relevant patterns precisely because they are geometrically separable from irrelevant and outlier components in orthogonal dimensions. In real-world data, features are rarely orthogonal—relevant signal correlates with noise, and outliers are not strictly orthogonal to the data manifold. The paper does not discuss how results would degrade under approximate orthogonality or feature correlation. This is a significant limitation that should be explicitly acknowledged and ideally analyzed through perturbation bounds.

**Recommended action:** Add a subsection discussing the role of orthogonality in the proofs, provide perturbation analysis (or at least a conjecture) for near-orthogonal settings, and bound the main results with explicit statements of what happens when patterns have nonzero cosine similarity.

### W2. Position-dependent robustness contradicts the paper's central narrative (Major)
The paper's headline claim is that "Mamba maintains accurate predictions even when the proportion of outliers exceeds the threshold that a linear Transformer can tolerate." However, Table 1 shows that Mamba's accuracy drops from 99.73% (outliers farthest from query) to 82.73% (outliers closest to query), a 17-percentage-point degradation—while the linear Transformer stays at 93.96% regardless of position. This means Mamba's robustness is highly dependent on the *position* of outliers, not just their *fraction*. When outliers are positioned near the query, the linear Transformer actually outperforms Mamba by a large margin. This caveat fundamentally qualifies the paper's main comparative advantage claim and should be prominently discussed in the abstract and conclusion, not only in Section 4.2.

**Recommended action:** (a) Add explicit qualifiers to the abstract and conclusion stating that Mamba's robustness advantage over linear Transformers is contingent on outlier position. (b) Provide a theoretical discussion of why the CQ setting causes degradation, linking Corollary 2's exponential decay to the empirical drop. (c) If possible, propose a modification to the gating mechanism that mitigates position sensitivity while preserving outlier robustness.

### W3. The "Transformer" comparison uses a non-standard variant (Major)
The paper compares Mamba with a "linear Transformer" where the nonlinear gating is removed ($G_{i,l+1}(\mathbf{w}) = 1$). This is not a standard Transformer—real Transformers use softmax attention, multi-head attention, layer normalization, and residual connections, all of which are removed in this comparison. While Remark 6 acknowledges this limitation, the paper's title ("Can Mamba Learn in Context with Outliers?") and abstract refer to "linear Transformers" without consistently emphasizing the non-standard nature of the baseline. Readers unfamiliar with the literature may misinterpret the comparison as applying to standard Transformer models used in practice. Furthermore, the paper's central "Mamba vs Transformer" framing in titles and contribution claims (C2) risks overclaiming the practical implications of the comparison.

**Recommended action:** (a) Replace every occurrence of "Transformer" with "linear Transformer" (or "simplified linear Transformer") in the abstract, introduction, and contribution statements. (b) Add a sentence in the abstract explicitly stating "where the Transformer baseline is a simplified one-layer linear-attention model without softmax normalization." (c) In the conclusion, clarify that the proven advantages apply to this simplified architecture and may not transfer to standard multi-layer softmax Transformers.

### W4. Sufficient-condition comparison may reflect proof artifacts (Major)
The comparison in Theorems 1 and 3 is between *sufficient conditions* for convergence, not *necessary conditions*. The paper reports that "linear Transformers need a smaller batch size, a smaller number of training iterations" and that Mamba's required iterations scale as $\Theta(l_{tr})$ times that of Transformers. However, these differences could partly reflect slack in the analysis rather than fundamental optimization advantages. The paper does not discuss whether the bounds are tight or whether alternative proof techniques could narrow the gap. Without tightness guarantees, the quantitative comparison should be interpreted cautiously.

**Recommended action:** Add a paragraph in Section 3.4 explicitly stating that the comparison is between sufficient conditions and that the quantitative differences may not be fundamental. If known, provide lower bounds or discuss tightness.

### W5. Missing error bars and statistical confidence in experiments (Minor-Major)
All experimental results (Figures 2-4, Table 1) are presented without error bars, confidence intervals, or significance tests. Given that the theoretical analysis involves high-probability bounds, the experiments should follow similar statistical rigor. The error rate of Mamba is reported as "smaller than 0.01" for α close to 0.8, but it is unclear whether this reflects a single run, the mean of multiple seeds, or the best run.

**Recommended action:** (a) Report mean ± std over at least 5 independent seeds for all experiments. (b) Add statistical significance tests (e.g., paired t-test) for the key comparisons in Table 1. (c) Provide the number of runs and seed information in the experiment setup.

### W6. Notation ambiguity in Theorem 2 and Corollaries (Minor)
Two notational issues affect readability and precision: (1) Equation (11) in Theorem 2 mixes a vector equation $v = \sum \lambda_i v_i^*$ with a scalar inequality $\sum \lambda_i \geq L > 0$ in one ill-formed expression. (2) Corollary 1 uses $\tilde{\mathbf{p}}_i$ without definition, and Corollary 2 does not specify the distance metric for $h(j)$ (index distance vs. Euclidean distance in input space).

**Recommended action:** (a) Separate Eq. (11) into a vector definition and a scalar coefficient constraint. (b) Define $\tilde{\mathbf{p}}_i$ explicitly before Corollary 1. (c) Specify the distance metric used for the local bias ordering in Corollary 2.

## Score
**Final Score: 5/10**

**Scoring rationale:**

The paper presents a technically rigorous theoretical analysis of Mamba's in-context learning with outliers, which is a timely and relevant topic. The strengths include the first known theoretical analysis of Mamba's ICL training dynamics, clean mechanism decomposition, and well-structured sufficient-condition theorems.

However, several factors significantly limit the paper's impact and scientific contribution:

1. **Assumption strength vs. conclusion generality (research value):** The orthogonality assumptions are so strong that the theoretical framework effectively operates in a geometrically idealized setting far removed from real data. While simplifying assumptions are standard in theoretical work, the paper does not adequately discuss how results would change under more realistic conditions. This reduces the research value of the theoretical guarantees.

2. **Central claim inconsistency (novelty):** The paper's main comparative claim—that Mamba outperforms Transformers under high outlier fractions—is contradicted by the paper's own Table 1, which shows Mamba performing 11 percentage points *worse* than the linear Transformer when outliers are near the query. This inconsistency between the headline narrative and the empirical evidence is a significant weakness that undermines confidence in the paper's framing.

3. **Comparison baseline (novelty):** The comparison uses a non-standard "linear Transformer" (without softmax, multi-head attention, or normalization), which limits the practical relevance of the comparative advantage claims.

4. **Empirical validation (validity):** Experiments are conducted only on synthetic data matching the theoretical assumptions, with no error bars or statistical significance reporting.

The paper has solid technical merit and addresses a genuine gap in the theoretical literature on state-space models. The mechanism analysis (Corollaries 1-2) is insightful, and the position-dependent robustness finding (Table 1) is valuable. However, the gap between the paper's broad claims and the narrow scope of the theoretical assumptions, combined with the unresolved position-sensitivity caveat, warrants a score in the lower-mid range. With substantial revisions to the narrative framing, addition of assumption-robustness analysis, and more comprehensive experiments, the paper has potential for a higher score.