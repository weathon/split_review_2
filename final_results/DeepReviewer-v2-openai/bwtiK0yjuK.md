## Summary
This paper studies offline change point localization and inference in Dynamic Multilayer Random Dot Product Graphs (D-MRDPGs). The authors propose a two-stage algorithm combining seeded binary segmentation with low-rank tensor estimation (TH-PCA), establish consistency for the estimated number and locations of change points, derive limiting distributions for refined estimators, and construct data-driven confidence intervals. Numerical experiments on synthetic data and a real agricultural trade network demonstrate advantages over general-purpose graph change-point detection methods.

**Core contributions:** (C1) First offline detection algorithm for D-MRDPGs with consistency guarantees; (C2) first limiting distribution results for change point estimators in a network model; (C3) an empirical methodology that outperforms generic alternatives on benchmark scenarios.

**Key limitations identified:** (i) The theoretical assumption Δ = Θ(T) restricts applicability to well-separated change points and is violated in the real data example (T=35); (ii) Confidence interval coverage degrades substantially under model violations (76.7% in Scenario 3 vs. nominal 95%); (iii) Baseline comparisons are asymmetric (general-purpose vs. model-specific), missing an adapted single-layer SOTA baseline; (iv) The "first" claims require external literature verification that is unavailable in this run. Novelty assessment is deferred pending external literature validation.

**Overall assessment:** The paper addresses a well-motivated problem with a technically sound algorithmic framework. The theoretical analysis is rigorous, and the empirical results are promising. However, the strength of the contribution claims is somewhat diluted by restrictive assumptions, missing competitive baselines, and overclaiming relative to the scope of evidence. The paper would benefit from scoping adjustments, additional baselines, and a more measured presentation of novelty.

## Strengths
**1. Well-motivated and timely problem.** Offline change point detection in multilayer networks is a relevant problem with clear applications (trade networks, transportation, social systems). The paper correctly identifies the gap between single-layer offline methods and multilayer online methods, and targets an underexplored setting.

**2. Technically rigorous theoretical framework.** The paper provides a complete theoretical treatment: consistency of change point number and location (Theorem 1), limiting distributions of refined estimators (Theorem 2), and a data-driven confidence interval procedure. The proof technique extends the single-layer theory of Wang et al. (2021) to tensors via TH-PCA, which is a non-trivial generalization. The two-regime analysis (vanishing vs. non-vanishing jumps) is thorough.

**3. Clean algorithmic design.** The two-stage pipeline (coarse detection via seeded binary segmentation → refinement via TH-PCA-based scan statistics) is computationally well-motivated, with overall complexity $O(T n^2 L r \log^2(T \vee n))$. The use of four independent tensor sequences for theoretical analysis and the odd-even splitting practical implementation is a principled approach to decorrelation.

**4. Comprehensive simulation study.** The paper evaluates four scenarios covering two generative models (DDM and MSBM), including two scenarios that violate Model 1 (Scenarios 2 and 3), demonstrating robustness to model misspecification. Sensitivity analysis for tuning parameters is provided.

**5. Real data demonstration with interpretable results.** The agricultural trade network analysis yields change points (1991, 1999, 2005, 2013) that align with documented geopolitical and policy events, enhancing the practical relevance of the work.

**6. Honest limitations discussion.** Section 5 acknowledges the Δ = Θ(T) limitation and the vanishing-jump restriction, which sets realistic expectations about the scope of the current theory.

## Weaknesses
### W1. Restrictive spacing assumption limits practical applicability (Major)
**Evidence:** Model 1(i) assumes $\Delta = \Theta(T)$, meaning the minimum spacing between change points scales with the total horizon. (Page 2 - Model 1). The paper acknowledges this limitation in Section 5 and Appendix G.1 without providing relaxed theoretical guarantees.

**Impact:** This assumption bounds the number of change points $K$ — effectively requiring that changes are sparse and well-separated. In many practical network settings (financial networks, social media, communication streams), changes can occur at frequencies much higher than $O(T)$. The real data example (T=35, spacing ~6-8) directly violates this assumption, but the method is applied without theoretical justification.

**Repair:** (a) Explicitly state what conditions on $\Delta$ are sufficient for each theoretical result; (b) add a remark in the real data section acknowledging that the theoretical guarantees do not directly apply; (c) provide a finite-sample simulation with $\Delta = o(T)$ to characterize the breakdown point.

### W2. Confidence interval coverage degrades significantly under model violations (Major)
**Evidence:** Table 2 (Page 8) shows that in Scenario 3 (community-size changes), the 95% CI achieves only 76.67% coverage for n=100 and 95.33% for n=150 — well below nominal for n=100. The paper attributes this to "violations of Model 1 and relatively small, layer-specific changes."

**Impact:** Users cannot trust the nominal coverage level when the data generating process deviates from Model 1. Since real-world networks rarely satisfy exact model assumptions, this substantially limits the practical utility of the inference procedure. No diagnostic tool is provided to alert users when coverage degradation is likely.

**Repair:** (a) Add a model-diagnostic step (e.g., test whether the tensor rank structure is stable across segments); (b) provide a bootstrap-based calibration for CIs that adjusts for model misspecification; (c) add a clear warning in Section 3.1 about when CIs are reliable.

### W3. Asymmetric baseline comparison inflates "superior performance" claim (Major)
**Evidence:** The only baselines (gSeg, kerSeg) are general-purpose graph change point methods not designed for the D-MRDPG setting (Page 7 - Section 4.1). The paper claims "our methods substantially outperform existing state-of-the-art algorithms" (Section 1.1) but the comparison is fundamentally asymmetric: CPDmrdpg exploits known tensor structure while baselines are model-agnostic.

**Impact:** The reported performance advantage is expected and does not establish that the method improves upon *the state of the art for this specific problem* — because no prior offline multilayer method exists for this problem by the paper's own premise. Missing: (a) an adapted baseline that applies single-layer offline RDPG detection per layer and aggregates results; (b) comparison against the online D-MRDPG method (Wang et al., 2025) adapted to offline post-processing.

**Repair:** Add the adapted single-layer baseline. Rephrase the contribution claim from "substantially outperform existing state-of-the-art" to "substantially outperform general-purpose graph change point detection methods, demonstrating the value of model-specific design."

### W4. Strong "first" claims require external literature verification (Major)
**Evidence:** The paper states "to the best of our knowledge, this is the first result of its kind in the context of dynamic network data" (Abstract and Section 1.1) regarding both offline detection in multilayer networks and limiting distributions.

**Impact:** External literature verification is unavailable in this run (Retrieval-Disabled Mode). While the claims may be accurate, the current manuscript-level evidence alone cannot verify them. If comparable results exist for related network models (e.g., offline detection with inference in stochastic block models), the "first" framing could be contested.

**Repair:** Add tighter scope qualifiers: "first for the D-MRDPG model" and "first limiting distribution results for change point estimators in a network model." This is partially done but the Abstract still uses the broader phrasing. Marked for deferred manual verification.

### W5. Definition 5 (refined scan statistics) is corrupted and unreproducible (Major)
**Evidence:** The expression in Definition 5 (Page 3) contains garbled LaTeX: "$\hat{D}_{b_k}^{s_k, e_k}(t) = |\tilde{\mathbf{P}}^{s_k, e_k}(b_k) / \tilde{\mathbf{P}}^{s_k, e_k}(b_k)|_{\mathbb{F}}, \tilde{\mathbf{A}}^{s_k, e_k}(t)|$" — a forward slash between tensors and misplaced subscript.

**Impact:** Without a correct formula, the Stage II refinement step cannot be reproduced from the main text alone. Readers must infer the intended definition from the algorithm description, which is not acceptable for a technical paper.

**Repair:** Provide a corrected definition with unambiguous notation (see annotation for the Mentor Revised Version).

### W6. Domain mismatch in limiting distribution: $\mathbb{Z}$ vs $\mathbb{R}$ (Major)
**Evidence:** Theorem 2 (Page 6) states the arg min over $r \in \mathbb{R}$ but the Brownian motions $\mathbb{B}_1(r), \mathbb{B}_2(r)$ are defined "for $r \in \mathbb{Z}$" in the problem statement. The CI construction (Step 3, Section 3.1) discretizes over a continuous grid, which is consistent with the $\mathbb{R}$ interpretation but inconsistent with the $\mathbb{Z}$ qualifier.

**Impact:** This inconsistency affects the theoretical validity of the limiting distribution and the interpretation of the arg min. If the arg min is over integers, the process is a random walk; if over reals, the continuous Brownian approximation is valid. The current mixed presentation is mathematically ambiguous.

**Repair:** Clarify whether the arg min is over $\mathbb{Z}$ (with Brownian motions evaluated at integer points) or over $\mathbb{R}$ (remove "for $r \in \mathbb{Z}$"). My recommendation: keep the real-valued arg min and remove the $\mathbb{Z}$ constraint, as the CI procedure is consistent with the real-valued formulation.

### W7. Introduction lacks storyline coherence and gap identification (Minor)
**Evidence:** The first introductory paragraph (Page 1) provides general background on multilayer networks and change points without stating the precise research gap. The literature survey paragraph (Page 1) reads as a citation listing rather than a critical comparison organized by methodology axes.

**Impact:** Readers without prior expertise in network change point detection may not understand why offline multilayer detection requires new methodology beyond combining existing tools.

**Repair:** Restructure as: (1) concrete stakes and motivation → (2) what prior methods can and cannot do → (3) the specific technical challenge of offline multilayer detection → (4) proposed approach and contributions. See annotation for detailed Mentor Revised Version.

### W8. Real-data analysis runs outside theoretical guarantees (Minor)
**Evidence:** The agricultural trade network has T = 35 with detected change point spacings of 6-8 years (Page 9, Table 3). The Δ = Θ(T) assumption requires spacing proportional to T, which is clearly violated. The paper does not discuss this mismatch.

**Impact:** The method is applied in a regime where the core theoretical guarantees do not hold. While the results appear reasonable, this weakens the paper's overall credibility.

**Repair:** Add an explicit caveat in Section 4.2 acknowledging the regime mismatch and citing the relevant robustness experiments from Appendix G.1.

### W9. Missing ablation analysis (Minor)
**Evidence:** The method has two stages and depends on multiple design choices (seeded interval parameters, CUSUM threshold τ, TH-PCA input ranks). While the authors vary τ and ranks for sensitivity (Page 7), there is no ablation that isolates the contribution of Stage II (low-rank refinement) vs. Stage I alone.

**Impact:** Readers cannot determine how much of the performance gain is due to the tensor refinement vs. the seeded binary segmentation front-end. The paper claims Stage II "yields provably improved localization accuracy" (Page 3) but does not empirically quantify this improvement.

**Repair:** Add a "Stage I only" baseline that uses seeded binary segmentation without TH-PCA refinement to quantify the marginal benefit of Stage II.

### W10. Novelty/comparison conclusions require external retrieval (Deferred)
As per the runtime setup, external paper search is disabled. Therefore, all novelty claims (particularly the "first" claims) and the position of this work relative to existing offline network change point methods cannot be fully verified in this review. These conclusions are marked for deferred manual verification. The authors should ensure that the strongest directly comparable prior methods (e.g., single-layer offline RDPG detection, SBM offline detection, related tensor-based change point methods) are cited and explicitly compared.

## Score
**Final Score: 6/10**

**Scoring rationale:** The score emphasizes research value/novelty as primary dimensions and validity/soundness as secondary.

**Research value (7/10):** The problem of offline change point detection in multilayer networks is relevant and timely. The paper makes a meaningful theoretical contribution by extending consistency and distributional results from the single-layer to the multilayer tensor setting. However, the practical value is somewhat limited by the Δ = Θ(T) assumption, which restricts applicability to well-separated changes, and by the absence of competitive baselines designed for the same setting, making it difficult to calibrate the actual improvement over the state of the art.

**Novelty (6/10 — deferred manual verification required):** The "first offline detection in multilayer networks" and "first limiting distributions in network change point analysis" claims are potentially strong but cannot be fully verified without external literature retrieval (disabled in this run). The methodological combination of seeded binary segmentation with TH-PCA-based tensor refinement is novel, though it builds directly on existing components (Wang et al., 2021; Kovács et al., 2023; Han et al., 2022). The distributional theory appears to be genuinely new for network models.

**Validity/soundness (7/10):** The theoretical framework is rigorous, with clear assumptions and matching guarantees. The proofs are deferred to the appendix (standard practice). The simulation design is comprehensive, with 100 Monte Carlo trials across four scenarios and two generative models. The main validity concerns are: (1) the CI coverage degradation under model violations (76.7% in Scenario 3) is not adequately discussed or diagnosed; (2) the Definition 5 garbled formula undermines reproducibility; (3) the mismatch between the ℤ and ℝ formulations of the arg min in Theorem 2 creates mathematical ambiguity.

**Reproducibility (5/10):** The algorithm description is clear but two issues hinder full reproducibility: (i) Definition 5 is garbled; (ii) the TH-PCA truncation step (Algorithm 2 in Appendix D) is not described in the main text. The simulation details are thorough and should be reproducible.

**Evidence sufficiency (7/10):** The paper provides extensive simulation evidence but the baseline comparison asymmetry weakens the empirical claims. The real-data analysis is illustrative but runs outside the theoretical guarantees.

**Strengths vs. weaknesses balance:** The paper's technical contributions are solid and the problem is important. However, the strength of the claims ("first," "substantially outperform") outpaces the current evidence, especially given the restrictive assumptions and asymmetric baselines. With targeted revisions (additional baselines, scoped claims, corrected definitions, CI diagnostics), the paper could become a strong contribution to the network change point literature.

**Post-Revision Target:** [7, 8]/10 — achievable if the major weaknesses (W1-W6) are addressed with the recommended repairs.