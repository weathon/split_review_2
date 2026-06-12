## Summary

This paper presents the first theoretical analysis of the training dynamics and in-context learning (ICL) generalization of one-layer Mamba models, including robustness to additive outliers in prompts. The authors prove that Mamba's linear attention layer selects informative context examples sharing the query's relevant pattern, while its nonlinear gating layer suppresses outlier-containing examples and induces exponential positional decay. Theoretical comparison with linear Transformers shows that while Mamba converges more slowly, it can tolerate outlier fractions approaching 1 (vs. 1/2 for linear Transformers).

## Strengths

- **First theoretical analysis of Mamba training dynamics for ICL**: The paper fills a genuine gap by providing convergence guarantees, sample complexity bounds, and generalization results for Mamba in the ICL setting with outliers. This is a timely contribution given the growing practical importance of Mamba-like architectures.

- **Well-designed comparison framework**: By defining the linear Transformer as the special case where G_{i,l+1}(w) = 1 (removing only the nonlinear gating), the paper isolates the precise architectural difference and provides a fair apples-to-apples comparison. This is methodologically clean and the resulting Theorems 1–4 are directly comparable.

- **Insightful mechanism characterization**: Corollaries 1 and 2 provide concrete, interpretable explanations of how Mamba implements ICL—linear attention performs pattern-based selection (analogous to induction heads) while nonlinear gating filters outliers and creates local positional bias. These results connect to established attention mechanisms and provide genuine mechanistic understanding.

- **Consistent theoretical and experimental narrative**: The experimental results in Figures 2–4 and Table 1 directly validate the theoretical predictions (the α < 1/2 threshold for Transformers, the gating values on outlier vs. clean examples, the attention score separation). The sensitivity of Mamba to outlier positioning (Table 1) is an honest and interesting finding that enriches rather than undermines the analysis.

## Weaknesses

### Fatal

None.

### Major

- **Restrictive outlier structure assumption**: Theorem 2 requires test-time outlier patterns to be positive linear combinations of training-time outlier patterns (Condition (a) with ∑λ_i ≥ L > 0). While the authors frame this broadly, this is a non-trivial structural assumption that limits the practical applicability of the robustness guarantee. If test-time outliers are qualitatively different from training-time outliers (e.g., entirely novel perturbation types), the theory provides no guarantees. This should be discussed more prominently as a limitation.

- **One-layer architecture only**: The theoretical analysis is restricted to a one-layer Mamba, which is explicitly acknowledged as aligned with prior theoretical work. However, the multi-layer experiments in Section 4.2 reveal a qualitative phenomenon—the sensitivity to outlier positioning near the query (Table 1, CQ setting: 82.73% vs. 99.73%)—that the one-layer theory does not capture or explain. This interaction between layer depth and positional sensitivity is an important practical consideration that deserves deeper theoretical treatment.

- **Thin main-paper experiments**: The main experimental section relies solely on synthetic data with a specific parameter configuration. While the Appendix reportedly contains additional experiments, the main paper's empirical support is limited. Given that the practical relevance of the theoretical claims is a natural concern for this type of work, stronger main-paper experiments (even one real-world task illustration) would strengthen the contribution.

### Minor

- The comparison with multi-head softmax Transformers—which are the architectures actually used in practice—is deferred to the appendix. While the paper justifies focusing on linear attention, practitioners may question how the robustness advantage translates to standard Transformer architectures.

- The requirement that Mamba's batch size includes an extra term β⁻⁴V²κ_a⁻²(1−p_a)⁻² compared to Transformers suggests potentially significant computational overhead during training, but the paper does not quantify this gap experimentally or discuss practical implications.

- The claim that Mamba "maintains accurate predictions even when the proportion of outliers exceeds the threshold that a linear Transformer can tolerate" is conditioned on α < min(1, p_a·l_tr/l_ts), which requires careful tuning of prompt lengths. A brief discussion of how sensitive this is in practice would be useful.

### Trivial

None.

## Nice-to-Haves

- A brief discussion or experiment showing how the theoretical advantages of Mamba (outlier robustness) trade off against its disadvantages (slower convergence, positional sensitivity) in realistic settings would make the contribution more actionable.
- Analysis of whether the positional bias of Mamba's gating could be mitigated (e.g., through random permutation of context examples during inference) would be a natural extension given Table 1's findings.

## Novel Insights

The paper provides several genuinely novel observations beyond its technical contributions. The finding that Mamba's nonlinear gating simultaneously implements outlier filtering and exponential positional decay (Corollary 2) offers a unified mechanistic explanation for two distinct behaviors. More importantly, the theoretical characterization that the outlier tolerance threshold for linear Transformers is exactly 1/2 (a majority-vote boundary) while Mamba's threshold can approach 1 is a clean, interpretable result that has clear practical implications for prompt engineering with corrupted data. The connection between the induction head mechanism and Mamba's linear attention (Corollary 1) also suggests that pattern-based context selection may be a fundamental computational primitive across architectures, not specific to softmax attention.

## Suggestions

- Add a controlled real-world experiment (e.g., sentiment classification with injected label noise) in the main paper to bridge the synthetic-to-practical gap.
- Quantify the training efficiency gap (Mamba vs. Transformer) experimentally—e.g., wall-clock time to reach the same generalization error—to make the convergence speed trade-off concrete.
- Discuss explicitly whether the positional sensitivity issue (Table 1, CQ) could be addressed through context reordering or other architectural modifications, as this is a practical concern that somewhat undermines the robustness narrative.

## Score and Decision

This paper makes a genuine first contribution to the theoretical understanding of Mamba's ICL capabilities and its robustness to outliers. The technical approach is sound, the comparison framework is well-designed, and the mechanism analysis provides interpretable insights. However, the restrictive outlier assumptions, one-layer limitation, and thin main-paper experiments temper the practical impact. The positional sensitivity finding in Table 1 is important but underexplored. Overall, this is a solid theoretical contribution that advances understanding of an important topic, though with limitations typical of theoretical work in this area.

MY FINAL SCORE: <score>6</score>
MY FINAL DECISION: Accept