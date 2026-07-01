## Summary

This paper proposes CorreGen, a generative framework for multi-view clustering (MVC) under noisy correspondence (NC). The key idea is to formulate NC as maximum likelihood estimation over latent cross-view correspondences, solved via an EM algorithm. The E-step infers soft correspondences using Optimal Transport with GMM-guided marginals and a virtual sample mechanism to handle outliers; the M-step updates the embedding network to maximize the expected log-likelihood. The paper identifies two forms of NC—category-level mismatch and sample-level mismatch—and provides theoretical connections to InfoNCE as a special case. Experiments on four datasets with varying noise levels show consistent improvements over seven baselines.

## Strengths

1. **Principled generative reframing of noisy correspondence (Sections 3.1–3.2).** Moving from a discriminative contrastive objective to a maximum-likelihood formulation over latent correspondences is a well-motivated departure from prior reweighting/realignment approaches. The EM derivation (Eqs. 5–8) is technically sound, and Proposition 2 (InfoNCE as a special case) grounds the method theoretically.

2. **Elegant handling of unalignable samples via virtual samples (Section 3.2.1, Eqs. 12–16).** Augmenting the Optimal Transport coupling with a virtual sample that absorbs outlier probability mass addresses a genuine gap—prior methods (both reweighting and realignment) assume every sample has a valid counterpart somewhere. This is a clean conceptual innovation.

3. **Consistent and often substantial empirical gains across almost all settings (Tables 1, 2).** CorreGen outperforms all seven baselines on ACC, NMI, and ARI across four datasets under multiple noise configurations. The improvements on UMPC-Food101 (a realistic web-crawled dataset) are particularly large and compelling.

4. **Posterior distribution visualization (Fig. 3)** provides direct evidence that the E-step progressively recovers category-level block structure from initially noisy correspondences, supporting the claim that the method learns meaningful latent alignments.

## Weaknesses

### Fatal
None.

### Major

1. **No variance estimates for any result (Tables 1, 2).** The paper reports "the mean of five individual runs" but omits standard deviations entirely. Several key comparisons are close enough that variance could affect interpretation. For example, on LandUse21 at 0% MR, CorreGen (32.87 ACC) leads DIVIDE (32.50 ACC) by only 0.37 points. The absence of variance is an evidential gap that prevents readers from assessing which results are statistically robust and which may reflect run-to-run noise. This is a basic standard for empirical claims and should be addressed.

### Minor

2. **The ρ (noise ratio) hyperparameter is not explained in the main text (Section 3.2.1).** The virtual sample mechanism introduces ρ, which determines the probability mass allocated to outliers. In the unsupervised setting the paper targets, the true noise ratio is unknown. The main text does not state how ρ is set—whether it is tuned on a validation set, set to the true synthetic noise ratio (which would give CorreGen an oracle advantage over baselines), or treated as a tunable parameter. The paper references Appendix C for implementation details and Appendix E for hyperparameter analysis, but the main text should at least clarify the basic approach. **If ρ is set to the true MR/CR values used to generate synthetic noise, the comparisons on synthetic-noise experiments would be unfair to baselines that lack this oracle information.**

3. **The claim that CorreGen "consistently achieves the best performance" (Section 4.2) is overstated.** On Scene15 at 80% MR, CANDY achieves ACC 42.27 vs. CorreGen's 40.96—a counterexample to the "consistently best" claim. While CorreGen leads on NMI and ARI for this setting, and dominates most other comparisons, the blanket statement should be qualified. (This does not undermine the overall strong empirical trend, but precision matters.)

4. **The GMM-guided marginal estimation (Eqs. 13–14) is a heuristic construction, not a proper probabilistic posterior.** Eq. 13 applies a curve-shaping transformation ($\frac{m^{d_i}-1}{m-1}$) with arbitrary hyperparameters ($\epsilon=0.1, m=10$) to a kernelized Mahalanobis distance, then multiplies by cluster proportion. This is not a standard GMM posterior $\frac{\pi_c \mathcal{N}(\mathbf{z}_i; \boldsymbol{\mu}_c, \boldsymbol{\Sigma}_c)}{\sum_k \pi_k \mathcal{N}(\mathbf{z}_i; \boldsymbol{\mu}_k, \boldsymbol{\Sigma}_k)}$. The paper's description as "GMM-guided" is accurate in that GMM is used to obtain cluster parameters, but the marginal construction is heuristic. This adds tuning complexity (two shaping parameters) and somewhat undercuts the "principled" framing of the overall approach.

5. **The category-level mismatch claim is not directly tested.** The paper identifies two types of NC, but the experiments (Tables 1, 2) vary only sample-level mismatch (MR and CR). The paper acknowledges this (Section 4.2: "category-level mismatch is an intrinsic challenge rather than one that can be explicitly specified") and provides the posterior visualization (Fig. 3) as indirect evidence. However, the 0% MR results—where no sample-level mismatch exists—could reflect the generative objective being a generally better learning objective rather than specifically addressing category-level mismatch. The framing would be strengthened by a clearer statement of what evidence does and does not support the category-level claim.

### Trivial
None.

## Nice-to-Haves

- **Computational cost discussion.** The E-step solves an OT problem on an $(N+1)\times(N+1)$ matrix via Sinkhorn iterations; the M-step denominator sums over all $N^2$ pairs. Reporting wall-clock time, EM iteration counts, and how these scale would aid reproducibility.
- **Ablation of the base model.** CorreGen is implemented on top of DIVIDE. An ablation that applies the EM training to a simpler backbone would clarify how much of the gain comes from the generative objective vs. the base model quality.
- **Sensitivity of the entropy regularization coefficient λ** in the OT formulation (Proposition 1) is not discussed in the main text (it may be in Appendix E).

## Removed Points

- **Missing standard deviations:** This was kept (it is the sole Major weakness).
- **CorreGen "loses" on Scene15 80% MR:** The reviewer framed this as a loss, but CorreGen wins on NMI (41.74 vs. 36.08) and ARI (24.74 vs. 20.74) for that setting. The ACC-only framing was misleading; the criticism about the "consistently best" overclaim (Weakness 3 above) is the accurate version of this concern.
- **Cross-modal retrieval citation context for the 20% noise ratio claim:** This is a minor nitpick that does not affect the paper's substance.
- **Transition from Eq. 2 to Eq. 3 being glossed over:** This is a presentation suggestion, not a substantive weakness.
- **E-step bootstrapping risk (GMM marginals propagating errors early in training):** Speculative concern not evidenced in the paper.
- **Duplicate "Ours" rows in table formatting:** This is a formatting artifact/parser issue, not a content problem.
- **Base model ablation concern:** The comparison against DIVIDE directly shows the added value. A separate ablation would be informative but is not a weakness of the current experimental design.

## Novel Insights

None beyond the paper's own contributions. The harsh review's main insight—that the GMM-guided marginal is heuristic rather than truly probabilistic—is specific and correct but concerns a component the paper already describes transparently (Eqs. 13–14 are presented as stated, not misrepresented). The review correctly identifies the missing variance estimates and unclear ρ setting as the two main evidential gaps.

## Suggestions

1. **Report standard deviations** for all metrics in Tables 1 and 2. This is the single most impactful fix.
2. **Clarify how ρ is set** in the main text. If it is set to the true MR/CR for synthetic experiments, state this explicitly and discuss how it would be estimated in a fully unsupervised setting; ideally, evaluate with a fixed default or estimated ρ.
3. **Qualify the "consistently best" claim** in Section 4.2 to reflect that CorreGen leads on most (but not all) comparisons.
4. **Add a brief note** that the GMM marginal in Eq. 13 is a heuristic construction designed to amplify confidence differences, rather than a strict probabilistic posterior—this preempts confusion and is more accurate than leaving readers to assume standard GMM posteriors are being used.
5. **Include runtime or convergence information** to help readers assess practical applicability.

## Score and Decision

MY FINAL SCORE: <score>7.0</score>
MY FINAL DECISION: <decision>Accept</decision>