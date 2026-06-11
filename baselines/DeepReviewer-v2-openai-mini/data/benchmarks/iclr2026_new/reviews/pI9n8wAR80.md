## Summary
This paper addresses the problem of Long-Tailed Semi-Supervised Learning (LTSSL), where class imbalance in labeled data and distribution mismatch with unlabeled data create a confirmation bias cycle that marginalizes tail classes. The authors identify two limitations in existing Logit Adjustment (LA) methods: (1) frequency-based class distribution estimation overestimates head class prevalence due to sample redundancy, causing over-suppression; (2) the overall adjustment strength τ is treated as a fixed hyperparameter, ignoring its dependency on the estimated class distribution.

To address these issues, the paper proposes Co-Calibrated Logit Adjustment (CoLA) with two novel components: De-Duplicated Distribution Estimation (DDDE), which uses the effective rank of feature representations to estimate class frequencies while mitigating sample redundancy, and Logit Meta-Calibration (LMC), which meta-learns the optimal overall adjustment strength τ on a proxy validation set resampled to match the estimated distribution. The method is supported by a theoretical generalization bound and convexity analysis.

Empirically, CoLA is evaluated on CIFAR-10/100-LT, STL-10-LT, and SIN-127 across multiple distribution scenarios (consistent, uniform, reversed, middle, head-tail, unknown). Results show consistent improvements over existing LA-based methods, particularly on the more challenging CIFAR-100-LT and STL-10-LT benchmarks. Ablation studies validate the contribution of both DDDE and LMC components, and distribution estimation accuracy is improved over frequency-based alternatives.

**Novelty verdict (deferred):** Due to external literature verification being unavailable in this run, novelty and comparison conclusions are marked as deferred manual verification. Preliminary assessment suggests the core contribution — co-adapting class-wise and overall LA components via erank-based distribution estimation and meta-learned τ — is a reasonable incremental improvement, but the degree of overlap with existing effective-number-based methods (e.g., Cui et al. 2019) and meta-learning approaches for hyperparameter selection requires external literature cross-checking.

## Strengths
1. **Clear problem formulation and motivation.** The paper clearly identifies two concrete limitations in existing LA-based LTSSL methods — sample-redundancy-induced over-suppression and fixed overall adjustment strength — and directly maps each to a proposed solution component (DDDE and LMC). The two-fold dilemma is well-articulated with visual support (Figure 1).

2. **Technically sound core idea.** The use of effective rank (erank) to estimate sample redundancy and derive a de-duplicated class distribution is a principled extension of the effective number concept (Cui et al., 2019) to the LTSSL setting. The meta-learning approach for τ is a natural way to avoid manual hyperparameter tuning when the class distribution changes.

3. **Comprehensive experimental evaluation.** The paper evaluates across 4 datasets and 6 different distribution scenarios (consistent, uniform, reversed, middle, head-tail, unknown), which is substantially more thorough than many prior LTSSL works that evaluate only on consistent or uniform distributions. Results consistently favor CoLA, especially on the more challenging CIFAR-100-LT and STL-10-LT datasets.

4. **Theoretical grounding effort.** The generalization bound (Proposition 1) provides a formal connection between DDDE estimation accuracy and the reliability of the meta-learned τ, even if the bound itself is standard. The convexity analysis (Appendix F) further justifies gradient-based optimization for τ.

5. **Ablation and analysis.** Ablation studies (Table 4) separate the contributions of DDDE and LMC, and Table 5 directly measures distribution estimation accuracy (L2 distance), showing DDDE outperforms frequency-based alternatives (MCA, NWGMA). Figure 2 provides temporal analysis of pseudo-label accuracy.

6. **Reproducibility-friendly details.** The paper includes the proxy set construction procedure, the warm-up phase design, and references to Appendices for implementation details and time complexity, which aid reproducibility.

## Weaknesses
### W1. Statistical significance of results is not established (Major)

Table 1 and Table 2 report mean accuracy with standard deviations, but many of CoLA's gains over the second-best method fall within overlapping standard deviation ranges. For example, on CIFAR-10-LT consistent, CoLA (81.87±2.70) trails CPE (82.59±3.18); on CIFAR-10-LT uniform, CoLA (83.66±1.29) vs Meta-Expert (83.12±1.09) — a 0.54% difference with overlapping error bars. No paired significance tests (t-test, Wilcoxon, or confidence intervals of differences) are reported. This makes it difficult to determine whether improvements are reproducible or within random variation.

**Required action:** Add statistical significance analysis (p-values or bootstrap confidence intervals) comparing CoLA against the best competitor for each setting. Report the proportion of independent runs where CoLA outperforms each baseline.

### W2. Singular value range mismatch in DDDE computation (Major)

The erank computation (Eq. 2) sums over $i=1$ to $m_y$ singular values, but for a $d \times m_y$ feature matrix $\mathbf{Z}_y$, the number of singular values is $\min(d, m_y)$. When $m_y > d$ (more high-confidence pseudo-labeled samples than feature dimensions), there are at most $d$ positive singular values, making the sum over $m_y$ ill-defined due to zero singular values ($\log 0$). This technical inconsistency could cause implementation issues.

**Required action:** Clarify that erank is computed over the $r = \text{rank}(\mathbf{Z}_y) \leq \min(d, m_y)$ positive singular values only, and adjust the sum limit in Eq. (2) accordingly. Report typical values of $d$, $m_y$, and $r$ in practice.

### W3. Inconsistency between linear and log LA formulations (Major)

Equation (1) (post-hoc LA for pseudo-label generation) uses the standard logarithmic term $-\tau \cdot \log \hat{P}_{\gamma_u}(y)$, while Equation (4) (LMC meta-learning objective) uses a linear term $-\tau \cdot \mathbf{p}$. The paper states this "deviates from the original post-hoc LA" and cites (Mor & Carmon, 2025), but it is unclear whether the linear form replaces the log form in both training and inference, or only during meta-learning. If the learned $\tau^*$ is applied with the original log form, the optimality guarantee from the convexity analysis no longer holds because the objective function changes. If the linear form replaces the log form entirely, this is a substantial modification to standard LA that should be explicitly stated and empirically compared.

**Required action:** Clarify which LA formulation is used for pseudo-label generation after meta-learning. If the linear form replaces the log form, add an ablation comparing linear vs log LA. If the log form is retained, explain how the optimal $\tau^*$ transfers between the two formulations.

### W4. Generalization bound is standard and overclaimed (Major)

Proposition 1 presents a PAC-style bound that follows directly from importance-weighting and Rademacher complexity arguments common in domain adaptation literature. The bound is parameterized by the Rademacher complexity $\mathfrak{N}_V(\mathcal{H}_\tau)$ of a one-parameter classifier family, which is likely $O(1/\sqrt{V})$ — making the bound vacuous for selecting $\tau$. The paper acknowledges this by deferring analysis to Appendices, but the main text presents it as a key theoretical contribution ("Supported by a theoretical generalization bound"). The convexity analysis (Appendix F) is more directly useful but is deferred.

**Required action:** Calibrate the claims about the theoretical contribution in the main text. State clearly that the bound provides qualitative insight (linking DDDE accuracy to generalization) but is not tight enough to guide $\tau$ selection. Move the convexity analysis to the main text or prominently reference it as the actionable theoretical result.

### W5. Fixed-τ ablation uses insufficient grid (Minor)

The ablation study (Table 4) tests only three fixed τ values (1, 2, 4). The optimal τ could be any value in $[0.5, 5.0]$, and a coarser grid with only three points may underrepresent the best possible fixed-τ baseline, potentially overstating the advantage of adaptive τ. For example, if τ=1.5 outperforms τ=1 and τ=2, this would be missed entirely.

**Required action:** Extend the fixed-τ grid to at least 6 values (e.g., 0.5, 1.0, 1.5, 2.0, 3.0, 4.0) and report the best fixed-τ performance for each setting individually.

### W6. SIN-127 comparison is incomplete and selective (Minor)

Table 3 on SIN-127 omits several key baselines that appear in the CIFAR tables (CPE, Meta-Expert, ADSH, RDA). On the 32×32 setting, CoLA (24.18%) is virtually tied with ABC (23.66%) but the text claims "CoLA outperforms the other methods." The selective baseline reporting weakens the scalability claim.

**Required action:** Include all baselines from the CIFAR experiments that are applicable to SIN-127, or explicitly state why they are excluded. Tone down the claim to "competitive or superior" and acknowledge the tie on 32×32.

### W7. Missing limitations and failure case analysis (Minor)

The conclusion does not discuss limitations of CoLA. Key potential failure modes include: (1) DDDE relies on initial pseudo-label quality during warm-up — if the model is poorly calibrated, the erank estimates may be unreliable; (2) the meta-learning procedure adds computational overhead from the warm-up phase; (3) Assumption 3 (shared class-conditional distribution) is standard but may not hold in practice.

**Required action:** Add a dedicated limitations paragraph in the conclusion discussing these failure modes and possible mitigation strategies.

### W8. Title could better convey the specific contribution (Minor)

The title "CoLA: Co-Calibrated Logit Adjustment for Long-Tailed Semi-Supervised Learning" identifies the method and domain but does not communicate what problem it solves or what advantage it offers. A more informative title would signal the adaptive nature of the approach.

**Required action:** Consider a title like "CoLA: Co-Adapting Class-Wise and Overall Logit Adjustment for Long-Tailed Semi-Supervised Learning" to better reflect the paper's core contribution.

### W9. Notation ambiguity in distribution definitions (Minor)

The middle and head-tail distribution definitions use $K^{(K+1) \bmod 2}$, which may be a PDF extraction artifact. For $K=10$, this evaluates to $10^1 = 10$, making $k_{\min}=10$ for the middle distribution — which is the last class, not a middle class. This makes it impossible for readers to reconstruct the exact experimental setup.

**Required action:** Verify and clarify the intended notation. If the current expression is correct, provide an explicit example for a specific $K$ value (e.g., CIFAR-100 where $K=100$).

## Score
**Final Score: 6/10**

**Score rationale:** The paper addresses a well-motivated problem (LTSSL with distribution mismatch) and proposes a technically sound two-component solution (DDDE + LMC) with thorough multi-distribution evaluation. However, the score is constrained by: (1) the theoretical contribution is standard and overclaimed in presentation; (2) the DDDE formula has a singular-value range issue that could affect reproducibility; (3) the linear-vs-log LA inconsistency is not adequately justified; (4) statistical significance of the reported gains is not established, with several comparisons falling within overlapping standard deviations; and (5) novelty assessment is deferred due to external literature being unavailable in this run, but the approach appears to be an incremental improvement over existing LA-based methods rather than a paradigm shift. The paper has clear strengths in problem formulation and experimental breadth, but the methodological concerns and unverified statistical reliability prevent a higher score.