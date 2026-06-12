## Final Review

### Summary

This paper presents the first theoretical analysis of training dynamics for a one-layer Mamba model performing in-context learning (ICL) on binary classification tasks with additive outliers. The authors derive a tractable closed-form for one-layer Mamba (Eq. 3) as linear attention followed by nonlinear gating, characterize convergence and generalization via SGD, and compare against linear Transformers (gating-ablated version). The mechanistic analysis (Corollaries 1-2) shows the linear attention selects same-pattern examples while the gating suppresses outliers and imposes a local bias.

### Strengths

1. **First training-dynamics analysis for Mamba ICL.** Prior work (Li et al., 2024b, 2025b; Bondaschi et al., 2025) analyzed representational expressivity (what Mamba can represent at global minima), not whether gradient-based training converges to those solutions. This paper fills a genuine gap by analyzing what can be provably learned via SGD. The formalization in Eq. (3) of one-layer Mamba as linear attention plus learned gating is a concrete starting point.

2. **Mechanistic decomposition (Corollaries 1 and 2).** The paper characterizes how each component contributes: Corollary 1 shows linear attention weights concentrate on same-pattern examples (an "induction head" analogue for linear attention), and Corollary 2 shows the gating suppresses outlier examples and imposes an exponential local bias. This provides a testable hypothesis about Mamba's internal mechanism.

3. **Clean boundary on what linear attention alone can handle.** Theorem 4's condition α < 1/2 for linear Transformers is clean and testable. Figure 2 experimentally validates this threshold, and the contrast with Mamba's ability to handle α approaching 1 gives the comparison a concrete, falsifiable form.

### Weaknesses

#### Fatal
None.

#### Major

1. **The analyzed model (Eq. 3) is a significantly simplified proxy for full Mamba, and the paper does not discuss which Mamba properties are lost.** The derivation collapses Mamba's per-dimension gating (Δ_{j,i} = softplus(w_j^T u_i) for each state dimension j) to a single learned gating vector w shared across all dimensions. The resulting gating function G_{i,l+1}(w) = σ(w^T p_i) ∏_{j=i+1}^{l+1} (1 - σ(w^T p_j)) is input-dependent through w^T p_i (contra one reviewer's incorrect claim otherwise), but uses only one gating channel whereas actual Mamba uses per-dimension gating. The derivation is deferred entirely to Appendix E.1 (not available for review), so readers cannot assess the assumptions required. The paper's title and framing claim conclusions about "Mamba," but the object analyzed is a specific gated bilinear model. A discussion of what is preserved and what is lost (input-dependent per-timestep Δ, content-dependent B/C projections, state dimension > 1, multiple gating channels) is absent from the main text. This gap between what is claimed and what is analyzed undermines the generality of the conclusions. This is the paper's most significant weakness.

2. **The "unseen outlier" generalization (Theorem 2) is more constrained than the abstract and introduction suggest.** Condition (a) requires test outliers to be expressible as a linear combination of training outlier patterns with coefficients summing to a positive value. The paper states this in Remark 3 and P1, but the abstract and introduction frame the result as "unseen outliers" without conveying how restrictive this condition is. For instance, a data poisoning attack using a completely novel trigger pattern (as in the James Bond example in Figure 1) would not generally satisfy this condition. Additionally, Condition (b) requires test outlier magnitudes to be at least as large as training outliers, and Condition (c) limits α < p_a·l_tr/l_ts, making test-time robustness bounded by training-time outlier exposure — a form of interpolation rather than a novel robustness property.

#### Minor

3. **The comparison against "linear Transformers" is structurally an ablation study (gated vs. ungated) framed as an architectural comparison.** The "linear Transformer" comparator is defined by removing the gating (G=1), which is a gating-ablated version of the same model, not a standard linear Transformer (e.g., Katharopoulos et al. 2020). Remark 6 acknowledges this by noting the comparison is designed to probe the effect of gating, and additional experiments with softmax/multi-head attention are referenced in Appendix B.1 (stripped). However, the abstract and title frame this as "Mamba vs. linear Transformers," overstating the generality of the comparison.

4. **The empirical validation is thin for a paper making claims about Mamba's practical ICL advantages.** The main experiments use entirely synthetic data (d=30, M₁=6, M₂=10, V=3) without error bars or variance reporting. Additional experiments are referenced in Appendices B.1 and B.2 (stripped), but as presented in the main text the evidence is limited. Table 1 also reveals a meaningful limitation that is under-discussed: Mamba's accuracy drops to ~83% when outliers are closest to the query (CQ), while the linear Transformer is stable at ~94%. The paper explains this via the exponential decay in gating values (Corollary 2(ii)), but this means Mamba's robustness is highly position-dependent — a significant practical limitation that deserves more prominent treatment.

5. **Strong data assumptions limit generality.** Outliers are assumed orthogonal to all relevant/irrelevant patterns (line 105), ensuring linear separability from the signal and making the gating mechanism's job maximally easy. All theoretical results are sufficient conditions (upper bounds), not necessary ones — so the comparison between T_M and T_T cannot establish that Mamba actually requires more iterations, only that the analysis yields looser sufficient conditions.

#### Trivial

6. The notation \tilde{p}_i in Corollaries 1 and 2 is not defined in the main text.
7. Eq. (11) has a formatting issue with the condition on Σ λ_i.

### Nice-to-Haves

- Analysis of how many outlier patterns V are needed for the gating to generalize (sample complexity of gating learning).
- Lower bounds showing Mamba provably needs gating for certain robustness levels, or that linear Transformers provably cannot exceed α=1/2.
- Error bars or variance reporting on experimental results.
- A limitations paragraph discussing the restrictive outlier assumptions.

### Removed Points

- The critic's claim that Eq. (3) "loses the selective property" and imposes a "fixed location bias regardless of content" is incorrect: G_{i,l+1}(w) = σ(w^T p_i) ∏(1 - σ(w^T p_j)) is input-dependent through w^T p_i. The gating value for each position depends on its content. However, the simplification from per-dimension gating to a single w is real and is retained as Major weakness #1.
- The critic's claim that the "unseen outlier" condition requires a "conical hull" (all λ_i ≥ 0) is incorrect — the paper only requires Σ λ_i ≥ L > 0, allowing negative coefficients. The experimental evaluation uses v_1' = 0.7v_1* + 0.6v_2* - 0.4v_3*, which includes a negative coefficient. The restrictiveness concern is retained as Major weakness #2.
- The critic's claim that the comparison baseline is a "deliberately weakened version" is overstated — Remark 6 transparently frames it as an ablation. Retained in weakened form as Minor weakness #3.
- The critic's demands for experiments with "actual pretrained Mamba/Transformer models" and "standard ICL benchmarks" are scope creep for a theoretical analysis paper.
- Various formatting/style nitpicks from the section-by-section notes are removed.

### Novel Insights

The most penetrating observation emerging from this review is the tension in the gating mechanism: Corollary 2 shows the same exponential-decay structure that suppresses outliers also makes Mamba vulnerable when outliers are close to the query (Table 1, CQ: 83% vs. 94% for the linear Transformer). This trade-off is inherent to the cascading-product gating in Eq. (3) — the gating cannot simultaneously "remember" distant clean examples and "forget" nearby outliers — and may or may not carry over to full Mamba's richer per-dimension gating. The paper does not address this question, but it is precisely the kind of tension that follow-up work should investigate.

### Suggestions

1. Reframe the paper as a theoretical analysis of "gated linear recurrent attention" for ICL, with Mamba as architectural motivation rather than identity.
2. Add a discussion in Section 2 of what Mamba properties are preserved and lost in the Eq. (1) → Eq. (3) simplification. At minimum, state that the model collapses per-dimension gating to a single channel.
3. Report error bars or standard deviations on experimental results.
4. Add a limitations paragraph discussing the outlier assumptions (orthogonality, linear span constraint, magnitude bound).
5. Discuss the position-dependence finding (Table 1, CQ) more prominently as an inherent limitation of the gating mechanism.

### Calibration

**Round 1 bracket:** 4–6 (narrowed from initial 1–10 range via calibration against similar papers).

**Anchors retrieved:**

| Path | Avg Score | Round | Comparison |
|------|-----------|-------|------------|
| State-space models can learn ICL by GD (52XG8eexal.md) | 4.00 | R1 | Similar topic (SSM + ICL theory). Current paper is stronger: analyzes actual training dynamics, not just constructive proof. |
| MAMBA SSMs ARE LYAPUNOV-STABLE LEARNERS (i9RTCC6whL.md) | 4.67 | R1 | Similar Mamba theory paper. Current paper has more novel contributions but weaker experiments. Comparable quality. |
| Global Optimality of ICL Markovian Dynamics (HuBFimORiz.md) | 4.33 | R1 | Theoretical ICL paper with similar approach. Current paper comparable or slightly stronger. |
| Training Nonlinear Transformers for CoT (n7n8McETXw.md) | 6.50 | R2 | Very similar methodology (first training dynamics, simplified architecture, synthetic experiments). **Current paper is weaker** due to additional model-simplification gap (Eq. 3 vs. actual Mamba) and staged comparison baseline. |
| Toward Understanding In-context vs. In-weight (aKJr5NnN8U.md) | 6.50 | R2 | More comprehensive experiments including real LLM. Cleaner theoretical framing. Current paper weaker overall. |
| State Space Models Provably Comparable to Transformers (QFgbJOYJSE.md) | 5.75 | R3 | SSM theory paper, accepted. Compares SSMs to Transformers theoretically. Current paper has more novelty (first training dynamics) but weaker experiments. |

**Narrowing:** After Round 1 bracket (4–6), reading the full reviews of the CoT paper (6.50, accepted) and the SSM-ICL paper (4.00, rejected) confirmed that the current paper sits between these two — better than the SSM-ICL paper (more novel, cleaner results) but weaker than the CoT paper (additional simplification gap, staged comparison). Final score: **5.0**.

**Final assessment:** The paper fills a genuine gap and has real strengths, but the gap between what is claimed ("Mamba") and what is analyzed (a specific gated bilinear model requiring strong assumptions) is too large for the central conclusions to be accepted in their current form. The contribution would be solid if reframed appropriately.

### Score and Decision

MY FINAL SCORE: <score>5.0</score>
MY FINAL DECISION: <decision>Reject</decision>