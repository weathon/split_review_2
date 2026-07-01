## Summary

This paper tackles post-treatment selection (samples retained only if they pass quality control after intervention) in interventional causal discovery, a problem that causes spurious dependencies that mimic causal relationships. It introduces a formal causal framework with ℱℐ-Markov equivalence (a finer equivalence class that can distinguish selection from causation), a new graphical representation ℱ-PAG that extends PAG with new edge types, and the ℱ-FCI algorithm that learns this representation from observational and interventional data with soundness and completeness guarantees.

## Strengths

1. **Well-motivated, underexplored problem.** The paper identifies a genuine gap: post-treatment selection produces the same interventional CI patterns (variant marginal, invariant conditional) as direct causation, making them non-identifiable in existing frameworks. Figure 1 and the accompanying analysis in Section 1 clearly articulate this problem with concrete examples from genomics and clinical trials.

2. **Coherent and principled formal framework.** The paper builds from an augmented DAG with selection (Definition 1), through Markov properties characterizing CI/invariance patterns (Theorem 1, Lemmas 1–4), to the ℱℐ-Markov equivalence definition (Definition 2) and graphical criteria (Theorem 2). The extension of PAG to ℱ-PAG with new mark types (square □, triangle ▲) is a genuine extension of the standard representation, shown in Figure 5. Soundness and completeness are stated as Theorems 3 and 4.

3. **Well-structured algorithm design.** ℱ-FCI's decomposition into skeleton discovery from observational data (Step 1), edge orientation among intervened variables using interventional CI patterns (Step 2), and FCI rules for remaining edges (Step 3) is a sensible decomposition that leverages interventional data where it is most informative. The refinement procedure (Step 2.3) using Type I inducing nodes to disambiguate cases that endpoint CI patterns alone cannot resolve is a novel algorithmic contribution.

## Weaknesses

### Major
None. The core theoretical contributions are sound, and no verified issue invalidates the paper's claims.

### Minor

1. **"Post-treatment" framing overstates what the model structurally encodes.** The paper says at lines 43–60 that S "generally represent both pre-treatment selection and post-treatment selection" and then specializes to post-treatment selection as an assumption. The model itself (augmented DAG with S) does not encode any temporal or structural distinction between pre- and post-treatment selection — the distinction is simply an interpretive assumption. The CI patterns used (involving ψ indicators) would work for selection bias in interventional settings generally. The paper does not show a concrete scenario where pre-treatment and post-treatment selection would produce different CI patterns that the method could exploit. This does not undermine the technical contribution (handling selection in interventional settings is valuable), but the title and abstract's repeated emphasis on "post-treatment" as a structurally distinct challenge is not supported by the model.

2. **Evaluation protocol for DAG Precision and SHD is not specified in the main text.** The output of ℱ-FCI is a ℱ-PAG with four mark types and eight edge types (Definition 5), but the main experimental results (Figure 6) report "DAG Precision" and "DAG SHD" — metrics that compare against a ground-truth DAG. The paper does not explain how the ℱ-PAG was mapped to a DAG for this comparison (e.g., were new edge types □, ▲ collapsed into simpler types? Were circles treated as edges?). Since Precision and SHD are the primary quantitative results in the main text, this omission makes the results difficult to interpret.

3. **The CI test used in practice is not stated.** The theoretical results assume oracle CI tests. The experiments necessarily use a finite-sample CI test, but the paper does not say which one (Gaussian CI test? Kernel test? HSIC? Conditional permutation test?). This is a reproducibility concern.

4. **Real-world experiment is too thin in the main text.** Section 5.2 consists of three sentences with no quantitative results presented in the main body. All results are deferred to Figure 13 and Appendix D.3, with evaluation only via Enrichr enrichment analysis (which measures functional relevance, not structural correctness). While the appendix exists in the full submission, the main text should contain at least one quantitative result or clear summary of the real-data findings.

5. **Only 10 random graphs per configuration.** Results averaged over 10 replications with 95% confidence intervals are on the low end for stable conclusions. Given that the method relies on CI tests to infer six CI patterns per edge pair and then detect Type I inducing nodes, more replications would strengthen confidence in the reported precision and SHD values.

6. **Algorithm pseudocode lacks explicit CI-pattern-to-orientation mapping.** Step 2.2 lists six orientation rules, each testing different CI pattern vectors. The paper states these use "orientation rules summarized in Figure 4" (line 249), but the mapping from the six CI pattern columns in Figure 4(i) to the six specific tuples of CI test results in Step 2.2 is not made explicit. The reader must reverse-engineer this mapping from the figure caption and surrounding text.

7. **Computational complexity of AllPaths enumeration is not discussed.** Step 2.1 enumerates conditioning sets over `AllPaths(𝒢ₚ⁽⁰⁾, X_{ℐ⁽ⁱ⁾}, X_{ℐ⁽ʲ⁾})`. The number of paths between two nodes in a graph can be exponential, and the subsequent search over subsets of nodes on those paths compounds this. The paper does not discuss tractability or practical heuristics.

8. **Restrictiveness of the "≥2 observed variables" assumption (line 60) is not discussed.** If selection acts on only one observed variable, the CI patterns that distinguish selection from causation may collapse. The paper does not address whether this assumption is necessary or how common the ≥2 case is in practice.

### Trivial

- The simulation noise distribution `Uniform([0,2] ∪ [2,4])` is a bimodal distribution with a gap at 2, which is unusual. The rationale for this choice is not explained (line 275).

## Nice-to-Haves

- **Control experiment without selection.** The paper compares ℱ-FCI against baselines that do not handle selection, showing ℱ-FCI wins on data with selection. A natural next question is whether ℱ-FCI loses performance on data *without* selection — i.e., the cost of the more expressive model in the standard setting. This control is absent and would strengthen the empirical case.
- **A dedicated mapping table** from CI pattern vectors to ℱ-PAG edge types in the main text would make Algorithm 1 substantially more usable and clarify the core orientation logic at a glance.

## Removed Points

The following points from the input review were removed:

- **"Baselines are fighting a war they were not equipped for" / "missing control experiment"** → Downgraded and moved to Nice-to-Haves. The comparison as-is demonstrates that ℱ-FCI handles selection while baselines do not — this is informative even without the "no selection" control. The missing control is a strengthening suggestion, not a flaw.
- **"The pseudocode CI patterns are all identical (⊥,⊥,⊥,⊥)"** → Removed as a parser artifact. The original submission has distinct CI pattern entries; the extraction corrupted them.
- **"The code URL is missing"** → Removed as a parser artifact. The original submission contains the link.
- **"The theoretical contribution is narrower than claimed"** → Removed. The paper claims a *finer* equivalence class, which it delivers. "Going beyond traditional equivalence classes toward the underlying true causal structure" (abstract) is an accurate description of what a finer equivalence class provides.
- **"Theorem 1 is standard"** → Removed. The paper does not claim Theorem 1 is novel; it establishes foundational properties needed for the framework.
- **"The ℱ-PAG definition would benefit from a table"** → Moved to Nice-to-Haves as a presentation suggestion.
- **"Faithfulness assumption implications not discussed"** → Removed as speculative. The paper states the faithfulness assumption (line 247) which is standard in this literature.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. Specify the finite-sample CI test used in experiments. This is essential for reproducibility.
2. Add a paragraph describing how ℱ-PAG edges are mapped to DAG Precision and SHD. This would let readers interpret Figure 6 correctly.
3. Add a brief discussion of the ≥2-variable assumption: is it provably necessary, and what happens when it is violated?
4. Expand the real-data section with at least one quantitative summary statistic in the main text.
5. Provide an explicit table mapping each CI pattern vector in Figure 4(i) to the resulting ℱ-PAG edge orientation.

## Score and Decision

The paper addresses a genuine and underexplored problem with a coherent theoretical framework (ℱℐ-Markov equivalence, ℱ-PAG, sound and complete ℱ-FCI algorithm). The weaknesses are all addressable — none are fatal — but they collectively mean the empirical validation falls short of fully supporting the claims. The evaluation protocol needs clarification, the real-data results are too thin in the main text, and the CI test choice is unspecified. With these addressed, this would be a solid paper.

MY FINAL SCORE: <score>7.0</score>
MY FINAL DECISION: <decision>Accept</decision>