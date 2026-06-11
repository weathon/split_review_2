## Summary
This paper proposes CorreGen, a generative framework for multi-view clustering (MVC) under noisy correspondence (NC). Unlike discriminative contrastive MVC methods that rely on pre-defined positive/negative cross-view pairs, CorreGen formulates correspondence learning as maximum likelihood estimation over latent cross-view correspondences. The framework uses an Expectation-Maximization (EM) procedure: the E-step infers soft correspondence distributions via optimal transport with GMM-guided marginal probabilities and a virtual sample mechanism to handle unalignable noise; the M-step updates the embedding network to maximize expected log-likelihood guided by the inferred correspondences. The paper identifies two NC types—category-level mismatch (same-class samples treated as negatives) and sample-level mismatch (misaligned/unpaired samples)—and argues that prior discriminative approaches fail to address both simultaneously. Experiments on Scene15, Caltech101, LandUse21, and UMPC-Food101 under controlled mismatch ratios (MR) and corruption ratios (CR) show consistent improvements over seven baselines including DCP, DIVIDE, and CANDY. On the real-world noisy dataset UMPC-Food101, CorreGen achieves up to 10%+ absolute accuracy gains. A posterior distribution visualization on Caltech101 demonstrates that the estimated correspondences progressively approach ground-truth category-level block structure during training.

## Strengths
**1. Well-motivated problem formulation.** The paper clearly identifies and formalizes two types of NC (category-level and sample-level mismatch) that are realistic in web-collected multi-view data but under-explored in prior MVC literature. This taxonomy provides a clean conceptual framework for understanding limitations of existing methods and motivating the proposed generative approach.

**2. Principled methodological framework.** Shifting from discriminative contrastive objectives to a generative maximum likelihood formulation with latent correspondences is a conceptually elegant move. The EM derivation is technically sound, and the connection to InfoNCE as a special case (Proposition 2) provides theoretical grounding. The use of optimal transport with GMM-guided marginals to capture many-to-many cross-view correspondences is a novel algorithmic contribution.

**3. Strong empirical results.** The experimental evaluation is thorough, covering four datasets with multiple MR/CR combinations. CorreGen consistently outperforms seven baselines across most settings, with particularly notable gains on the real-world noisy dataset UMPC-Food101 (10%+ absolute ACC improvements). The posterior distribution visualization provides useful qualitative evidence that the E-step progressively uncovers meaningful correspondences.

**4. Code release.** The authors commit to releasing the code, which supports reproducibility and further research.

## Weaknesses
**W1. Notational error in Eq. (3) and insufficient derivation from Eq. (2).** The summation indices in Eq. (3) are inconsistent: $\sum_{v_i}^N$ appears to be a typo for $\sum_{i=1}^N$. More importantly, the derivation from per-view marginal log-likelihood (Eq. 2) to the pairwise joint distribution objective (Eq. 3) is presented as a direct algebraic manipulation, but it actually requires additional assumptions (e.g., that latent correspondences exist and are independent across view pairs) that are not stated. This weakens the theoretical rigor of the foundational objective. *(Severity: Major, Fixability: Easy — correct the index notation and add an intermediate derivation step.)*

**W2. EM derivation uses an OT-based posterior approximation without acknowledging the approximation gap.** The paper presents Eq. (8) as a standard EM objective but then in the E-step (Section 3.2.1) replaces the exact posterior $p(\mathbf{x}_j^{(v_2)}; \mathbf{x}_i^{(v_1)}, \theta(t))$ with an entropy-regularized OT solution $\mathbf{P}^*$. The paper does not discuss how this approximation affects the EM convergence guarantees or under what conditions the surrogate posterior is close to the true posterior. This is a significant theoretical gap: the framework is presented as "elegantly solved via EM," but the E-step computes only an approximation. *(Severity: Major, Fixability: Moderate — add a paragraph acknowledging the approximation, discussing the role of the entropy regularization parameter $\lambda$, and providing conditions for approximation quality.)*

**W3. GMM marginal estimation uses a heuristic that does not produce proper probabilities.** The marginal probability estimate in Eq. (13)-(14) is a hand-designed function that does not guarantee $\sum_i p(\mathbf{x}_i^{(v)}; \theta) = 1$. While the OT step subsequently treats these as marginal constraints, the paper does not clarify whether or how the vector $\mathbf{p}^{(v)}$ is normalized to sum to 1. Additionally, the GMM is fitted to the embedding space that is being learned, creating a circular dependency that is only briefly acknowledged with "momentum update to stabilize training" but not analyzed. Key GMM hyperparameters (number of components, covariance type, fitting frequency) are not reported, which harms reproducibility. *(Severity: Major, Fixability: Moderate — normalize marginals, document GMM hyperparameters, and discuss the circular dependency.)*

**W4. Missing statistical significance for experimental results.** Table 1 reports results as means over 5 seeds but omits standard deviations, confidence intervals, or significance tests. Many comparisons show small margins (e.g., Caltech101 NMI: Ours 84.45 vs CANDY 84.06 at 0% MR) that could be within one standard deviation. Without variance information, the reader cannot assess whether the claimed improvements are statistically reliable. *(Severity: Major, Fixability: Easy — add standard deviations or confidence intervals to tables.)*

**W5. Numerical stability and complexity concerns in the M-step objective.** The posterior computation $Q_{ij} = P_{ij}^* / p_i^{(v_1)}$ can be numerically unstable when $p_i^{(v_1)}$ is very small (for outlier samples). Furthermore, the denominator in Eq. (18) is a double sum over all $N^2$ pairs, requiring $O(N^2)$ computation per forward pass, which is prohibitive for large datasets. The paper does not address either of these practical concerns. *(Severity: Major, Fixability: Moderate — add epsilon smoothing for division, discuss mini-batch approximation or importance sampling for the normalization.)*

**W6. Posterior visualization uses a limited setting and lacks quantitative metrics.** The correspondence quality analysis (Section 4.3) is conducted only under MR=0.2, CR=0.0 (no corruption) on a single mini-batch from Caltech101. The paper claims "effectively alleviating category-level mismatches" based solely on visual inspection of heatmaps without quantitative metrics (e.g., block-structure alignment score, correspondence precision/recall). Higher-noise conditions and comparisons with baseline methods would strengthen this analysis. *(Severity: Major, Fixability: Moderate — add correspondence precision metrics, test under higher MR/CR, and compare with baseline methods' posterior estimates.)*

**W7. Conclusion lacks limitations discussion.** The conclusion does not acknowledge any limitations of the proposed approach, such as the Gaussian assumption for marginal estimation, sensitivity to the noise ratio hyperparameter $\rho$, or computational overhead of the OT-based E-step. Including limitations is a standard expectation for rigorous scientific writing and improves the paper's credibility. *(Severity: Minor, Fixability: Easy — add one paragraph discussing limitations.)*

**W8. Related work section reads as a literature list.** The Robust Multi-view Clustering and Noisy Correspondence Learning subsections provide a reasonable survey but do not organize methods along comparison axes that directly motivate CorreGen. A structured comparison table or explicit contrast dimensions (e.g., assumption, supervision, noise type handled) would better position the contribution. *(Severity: Minor, Fixability: Easy — add a comparative summary table.)*

## Score
**Final Score: 6/10**

**Rationale:** The paper proposes a conceptually interesting generative framework (CorreGen) for robust multi-view clustering under noisy correspondence. The problem formulation and EM-based solution are principled, and the empirical results show consistent improvements over strong baselines. However, the manuscript has several significant weaknesses that prevent a higher score:

- **Theoretical rigor gap (W1, W2):** The EM derivation uses an OT-based posterior approximation without discussing the approximation gap or its impact on convergence guarantees. The foundational objective derivation in Eq. (2)-(3) contains a notational error and lacks intermediate steps.
- **Methodological clarity issues (W3, W5):** Key components (GMM marginal estimation, M-step normalization) have unresolved numerical and probabilistic concerns that affect reproducibility.
- **Statistical evidence (W4):** Missing variance reporting undermines confidence in the empirical comparisons.
- **Limited analysis depth (W6):** The qualitative posterior analysis lacks quantitative rigor and broader validation.
- **Novelty verification deferred:** External literature comparison was not available in this run; novelty claims regarding the generative formulation and InfoNCE unification should be manually verified against related work on variational EM for contrastive learning.

The paper has clear strengths: a well-motivated problem taxonomy, an elegant EM+OT framework design, and strong reported empirical gains on the challenging UMPC-Food101 dataset. With revisions addressing the theoretical gaps, statistical reporting, and methodological clarity, the paper could reach a higher score.

---

### ASCII Diagrams

```text
ASCII Diagram A — Paper Structure & Evidence Map

[Problem: Noisy Correspondence in MVC]
    |
    +--> [Claim C1: NC taxonomy (category-level + sample-level)]
    |        |-- Evidence: Formal definitions (Def 1, 2)
    |        |-- Gap: Oracle labels required; not directly observable in unsupervised setting
    |        |-- Verdict: Conceptually useful but operationally aspirational
    |
    +--> [Claim C2: Generative MLE formulation + EM solution]
    |        |-- Evidence: Eq. (2)--(8), Proposition 1, Proposition 2
    |        |-- Gap: OT-based E-step approximates posterior; InfoNCE link follows known variational principles
    |        |-- Verdict: Theoretically interesting but OT approximation gap unacknowledged
    |
    +--> [Claim C3: Strong robustness on real-world NC]
             |-- Evidence: Tables 1, 2; Fig. 3
             |-- Gap: No standard deviations; posterior analysis only under clean setting
             |-- Verdict: Promising but statistically under-supported
             |-- Risk: Small margins on Caltech101 may be within noise range
```

```text
ASCII Diagram B — Revision Strategy Roadmap

[W1: Eq(3) index error + missing derivation]
    --> Fix notation & add intermediate step
    --> Expected gain: theoretical rigor restored
    
[W2: OT approximation gap in EM]
    --> Add paragraph on surrogate posterior, discuss lambda role
    --> Expected gain: honest framing of EM approximation
    
[W3: GMM marginals not proper probabilities]
    --> Normalize p^{(v)}, report GMM hyperparameters, discuss circular dependency
    --> Expected gain: reproducibility + mathematical correctness
    
[W4: Missing variance/statistics]
    --> Add std or CI to Tables 1, 2
    --> Expected gain: statistical credibility

[W5: Numerical stability + O(N^2) cost]
    --> Add epsilon smoothing + mini-batch discussion
    --> Expected gain: practical feasibility acknowledgment

[W6: Limited posterior analysis]
    --> Add quantitative metrics, test under higher noise
    --> Expected gain: stronger evidence for category-level mismatch handling

[W7: Missing limitations]
    --> Add limitations paragraph to conclusion
    --> Expected gain: scientific completeness

Priority Order: W1+W2 (theoretical) -> W4 (evidence) -> W3+W5 (reproducibility) -> W6+W7 (depth)
```

```text
ASCII Diagram C — Related-Work Taxonomy Tree (Layered)

Related Work: Robust MVC under Imperfections
|
+-- Branch 1: Incomplete Multi-view Problem (IMP)
|   +-- Leaf 1.1: Anchor-based completion [Liu+ 2024]
|   +-- Leaf 1.2: Subspace learning [Zhang+ 2024]
|   +-- Leaf 1.3: Diffusion-based imputation [Zhang+ 2025]
|
+-- Branch 2: Partially View-aligned Problem (PVP)
|   +-- Leaf 2.1: Variational contrastive realignment [He+ 2024]
|   +-- Leaf 2.2: Multi-stage iterative alignment [Yan+ 2025]
|
+-- Branch 3: Noisy Correspondence (NC)
|   +-- Leaf 3.1: Reweighting-based [Huang+ 2021, Yang+ 2024]
|   |   -- Strategy: down-weight mismatched pairs via robust loss
|   |   -- Limitation: cannot repair alignment; misses category-level
|   +-- Leaf 3.2: Realignment-based [Lin+ 2024]
|   |   -- Strategy: reassign each sample to plausible counterpart
|   |   -- Limitation: instance-level only; no unalignable handling
|   +-- Leaf 3.3: Generative correspondence (Ours: CorreGen)
|       -- Strategy: MLE over latent correspondences via EM+OT
|       -- Differentiator: many-to-many probabilistic assignments,
|          GMM-guided marginals, virtual sample for unalignable noise
|       -- Novelty risk: OT+EM for MVC is new, but generative formulation
|          of correspondences shares high-level idea with variational
|          methods; InfoNCE connection is known variational property.
|          Manual verification of overlap with [Sun+ 2024, 2025] needed.
|
Note: NC problem studied here differs from PVP in that (i) misalignments
are unobserved without verification labels, (ii) NC includes both category-
level and unalignable samples, not just instance-level permutation.
```

---

**Novelty & Retrieval Note:** External paper search was unavailable in this run (Retrieval-Disabled Mode). All novelty/comparison conclusions above are based solely on manuscript content and should be verified against the literature before final acceptance. The OT-EM combination for MVC appears technically novel, but the generative formulation of correspondences via variational methods has conceptual parallels with existing work that could not be assessed here. Key comparisons to verify: (1) overlap with ROLL [Sun+ 2025] and other NC-MVC methods; (2) whether the InfoNCE-as-special-case claim is already established in variational InfoNCE literature; (3) whether OT-based cross-view alignment has been applied to clustering in prior work beyond the cited [Deng+ 2025, Fu+ 2025].