## Summary

This paper studies offline change point localization and inference in dynamic multilayer random dot product graphs (D-MRDPGs), where at each time point a multilayer network is observed with shared latent node positions but time-varying layer-specific weight matrices. It proposes a two-stage algorithm (coarse detection via seeded binary segmentation with CUSUM statistics, followed by refinement via low-rank tensor estimation via TH-PCA), establishes consistency for both the number and locations of change points (Theorem 1), and derives the first limiting distributions for change point estimators in network data (Theorem 2) with an associated data-driven confidence interval procedure. Extensive simulations and a real-data application on agricultural trade networks demonstrate the method's practical viability.

## Strengths

1. **Novel problem formulation (Sections 1–2.1).** The paper formalizes offline change point detection in D-MRDPGs, a setting that is genuinely underexplored. The D-MRDPG model (Definition 2) and Model 1 are carefully specified, with layer-specific weight matrices allowed to change while latent positions remain fixed, motivated by a clear application domain.

2. **Substantial theoretical contributions (Theorems 1 and 2).** Theorem 1 establishes consistency with a localization rate of order κₖ⁻² log(T). Theorem 2 derives limiting distributions for the refined change point estimators under vanishing jumps — as the paper correctly claims, the first such results in the network literature. The associated data-driven confidence interval construction (Section 3.1) follows naturally and is a meaningful practical addition.

3. **Elegant two-stage architecture (Algorithm 1).** The coarse-to-fine design is well-motivated: seeded binary segmentation provides a computationally efficient screening stage, and the tensor-based refinement (TH-PCA) leverages the low-rank structure of expected adjacency tensors to improve localization accuracy. The CUSUM statistics are extended to the tensor setting in a principled way.

4. **Robustness to model violations (Scenarios 2–3, Table 1).** The paper includes scenarios where changes occur in community structure rather than weight matrices alone (violating Model 1). The proposed method maintains strong performance: in Scenario 2 with K=5 change points at n=50 and n=100, CPDmrdpg achieves perfect scores on all metrics, while the best competitor (kerSeg nets.) reports |K̂−K|=0.15 and d(C, Ĉ)=1.53.

5. **Interpretable real-data application (Section 4.2).** The detected change points on the agricultural trade network (1991, 1999, 2005, 2013) align with documented geopolitical and policy events (German reunification/Soviet dissolution, WTO Ministerial Conference, agricultural export subsidy elimination, Bali Package), providing a compelling narrative.

## Weaknesses

### Fatal

None.

### Major

1. **Gap between theoretical independence requirement and practical implementation (lines 89, Algorithm 1).** Algorithm 1 requires four mutually independent tensor sequences {A(t)}, {A'(t)}, {B(t)}, {B'(t)} as input. The paper states (line 89) that in practice "Stage I and Stage II are implemented using the same two split tensor sequences via the odd-even splitting approach." An odd-even split of a single observed sequence produces at most two sequences, not four. It is not explained how the theoretical guarantees (which rely on four independent sequences) transfer to the practical implementation using only two (and potentially correlated) sequences. The paper acknowledges this is "for theoretical convenience" but does not resolve the discrepancy — this is a genuine methodological gap between the theory's conditions and the evidence presented.

2. **Main-text experimental comparison does not adequately support the paper's central performance claim (lines 31, 249–255, Table 1).** The paper claims that "our methods substantially outperform existing state-of-the-art algorithms" (line 31). In the main text, this claim is supported only by comparisons against gSeg and kerSeg — generic change point detection methods that are not designed for multilayer networks, are not designed for the RDPG model, and have no mechanism to exploit tensor structure. Their poor performance relative to CPDmrdpg is expected and does not meaningfully benchmark the method. The paper states (lines 255) that comparisons to methods actually designed for the problem class (Wang et al., 2025; Li et al., 2024) are deferred to Appendix G.1. A reader should not need to consult an appendix to verify the paper's central empirical claim against reasonable, model-aware baselines.

### Minor

1. **No ablation isolating Stage II's contribution (Section 4.1).** The paper claims Stage II "yield[s] provably improved localization accuracy" (line 87, referring to the log-factor improvement in the theoretical rate). However, no experiment compares Stage I alone against Stage I+II. Without this ablation, the practical value of the computationally heavier Stage II (involving TH-PCA) remains unquantified in the experiments.

2. **Confidence interval centering inconsistency in Table 4 (lines 332–337).** In Table 4, the 95% CIs for the 2005 (time point 20) and 2013 (time point 28) entries are reported as (17.97, 18.05) and (25.99, 26.06) respectively — centered at approximately 18.01 and 26.03, not at the estimated change points (20 and 28). The first two rows (1991, 1999) are correctly centered. This may be a parser-induced table misalignment, but if the numbers are as reported, the CI formula (Step 4, Section 3.1) should center intervals on \(\hat{\eta}_k\), making this a mathematical inconsistency that needs clarification.

3. **Missing variability measures in Table 1 (lines 275–297).** Table 1 reports means over 100 Monte Carlo trials but provides no standard deviations, standard errors, or any other measure of dispersion. For a stochastic data generation process, this makes it impossible to assess whether the method's performance is stable or occasionally catastrophic.

4. **DDM simulation uses two sets of latent positions without comment (line 259).** The Dirichlet distribution model generates \(\{X_i\}_{i=1}^n \cup \{Y_i\}_{i=1}^n\) i.i.d. and computes edge probabilities as \(\mathbf{P}_{i,j,l}(t) = X_i^\top W_{(l)}(t) Y_j\). This uses two independent sets of latent positions (one for rows, one for columns), while the model definition (Definition 1) uses a single set \(\{X_i\}\) with \(\mathbf{P}_{i,j,l} = X_i^\top W_{(l)} X_j\). The paper does not discuss this discrepancy or its effect on the validity of the theoretical assumptions under which the method is evaluated.

### Trivial

1. **Threshold sensitivity analysis checks only one side of the theoretical interval (line 253).** The threshold \(\tau\) is set to \(c_{\tau,1} n\sqrt{L}\log^{3/2}(T)\) with \(c_{\tau,1} = 0.1\), and sensitivity is checked for \(c_{\tau,1} \in \{0.05, \dots, 0.25\}\). Theorem 1 requires \(\tau\) to lie in an interval \((c_{\tau,1} n\sqrt{L}\log^{3/2}(T),\; c_{\tau,2}\kappa^2\Delta)\). Varying \(c_{\tau,1}\) only checks the lower bound; the upper bound is never probed.

## Nice-to-Haves

- **Vary time horizon T in simulations.** All experiments use T=200. Showing that localization error and CI coverage improve as T grows (e.g., T ∈ {50, 100, 200, 500}) would directly support the asymptotic theory.
- **Break down CI coverage by scenario.** Table 2 pools coverage across scenarios. Scenario 3 (model violation) has substantially worse coverage (76.67% vs. 95% target) at n=100. A per-scenario breakdown would help readers assess when the CI procedure is trustworthy.
- **Discuss rank selection in practice.** The method requires Tucker ranks as inputs; conservative overestimates are used. Guidance on rank selection when the true dimension d is unknown would strengthen practical applicability.

## Removed Points

These points are flagged to be removed; treat them with caution:

- **Criticism that Δ = Θ(T) assumption limits practical relevance:** The paper explicitly acknowledges this limitation in Section 5 (line 349: "the assumption Δ = Θ(T) precludes frequent change points") and points to a relaxation path. The authors are aware of the restriction; flagging it as an unaddressed weakness is redundant.
- **Criticism that T=200 is small:** A generic "larger would be better" point not specific to this paper. The asymptotic theory allows parameters to diverge with T; T=200 is a standard simulation choice.
- **Speculation about rank overestimation introducing noise:** The paper states it follows Wang et al. (2025) for robustness and includes a sensitivity check (r ∈ {10, 15, 20}). No evidence of noise issues is identified.
- **Formatting artifact in CUSUM definition:** The garbled notation in Definition 4's piecewise function is a parser artifact, not an author error.

## Novel Insights

The most striking observation from cross-referencing the reviews is the disconnect between the paper's genuinely strong theoretical contribution (first limiting distribution for change point estimators in network data, novel formulation of offline multilayer detection) and the relative weakness of its main-text experimental validation. The harsh critic identifies that the core empirical claim rests on comparisons against straw-man baselines (gSeg and kerSeg) while the informative comparisons are appendix-only. This tension is not uncommon — strong theory papers often under-invest in evaluation — but it is more pronounced here because the paper itself frames the experiments as "extensive" and claims "substantial" outperformance. A second notable insight is the four-sequence independence gap: the paper is unusually honest about the discrepancy (line 89) but does not bridge it, leaving a hole that a careful reader cannot fill from the main text.

## Suggestions

1. **Clarify the four-sequence issue.** Either explain how the odd-even split with two sequences satisfies (or approximately satisfies) the theoretical independence requirements, or state explicitly that the practical implementation is a heuristic and adjust the claim strength accordingly.
2. **Move key competitor comparisons to the main text.** At minimum, summarize the results against Wang et al. (2025) and Li et al. (2024) in a short table or paragraph rather than deferring entirely to the appendix.
3. **Add a Stage I vs. Stage I+II ablation.** A simple experiment comparing the two-stage system against Stage I alone would directly quantify the practical benefit of the TH-PCA refinement.
4. **Resolve the Table 4 CI inconsistency.** Verify whether the reported intervals are correct, and if they are, explain why the last two CIs are not centered on the estimated time points. If the issue is a formatting artifact, ensure the published version is unambiguous.

## Score and Decision

MY FINAL SCORE: <score>6.0</score>
MY FINAL DECISION: <decision>Accept</decision>