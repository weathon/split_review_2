## Summary

This paper addresses noisy correspondence (NC) in multi-view clustering (MVC), identifying two critical failure modes: category-level mismatch (same-class samples wrongly treated as negatives) and sample-level mismatch (misaligned or unalignable cross-view pairs). The authors propose CorreGen, a generative framework that models latent cross-view correspondences via maximum likelihood estimation and solves it with an Expectation-Maximization algorithm. The E-step uses optimal transport with GMM-guided marginals and virtual samples to infer soft correspondences; the M-step updates the embedding network under the inferred correspondences. Extensive experiments on multiple datasets with varying noise levels show that CorreGen substantially outperforms existing robust MVC methods, with particularly large gains on the real-world noisy UMPC-Food101 dataset. The paper also proves that InfoNCE is a special case of the proposed formulation.

## Strengths

- **Well-motivated problem formalization.** The paper provides clear definitions of two types of noisy correspondence (category-level and sample-level) that arise in realistic web-collected multi-view data. These definitions are absent from prior work and provide a useful conceptual framework for future research.
- **Principled generative formulation.** Moving from discriminative contrastive objectives to a maximum likelihood estimation over latent correspondences is a theoretically grounded departure that reduces reliance on potentially noisy pre-defined positive/negative pairs. The connection to InfoNCE (Proposition 2) unifies the approach with standard practice.
- **Elegant EM solution with practical components.** The E-step combines optimal transport with GMM-guided marginals and virtual samples to handle both category-level and sample-level noise in a unified manner. The use of entropy-regularized transport (Proposition 1) makes the solution computationally tractable via Sinkhorn iterations.
- **Strong empirical performance.** Experiments across four datasets under multiple noise configurations show consistent and often large improvements over seven recent baselines. The 13+ point absolute accuracy gain on UMPC-Food101 at 0% MR (49.77 vs. 36.20) is particularly compelling for a real-world noisy dataset. The method maintains good performance even at 80% sample-level mismatch.
- **Visual evidence of correspondence recovery.** Figure 3 shows that the estimated posterior distributions progressively approximate the ground-truth block-diagonal structure, directly validating the method's ability to uncover latent category-level correspondences.

## Weaknesses

### Fatal

None.

### Major

1. **The GMM-guided marginal estimation is a heuristic that breaks the exact EM derivation.** In Eq. (9), the posterior requires the model's own marginal \(p(\mathbf{x}_i^{(v_1)}; \theta)\), but the paper replaces it with an externally estimated GMM marginal that is not consistent with the model's joint distribution. While this design choice is pragmatic, it means the algorithm is not a strict EM procedure. The paper should discuss this discrepancy and justify why it works—for example, as a form of amortized or variational approximation. Without such discussion, the theoretical grounding is somewhat overstated.

2. **The method's reliance on a base model (DIVIDE) limits clarity of contribution.** The paper states "We implement it on top of DIVIDE as the base model," but it is not entirely clear which components are inherited from DIVIDE and which are new. The ablation study (Appendix F, stripped) presumably addresses component contributions, but the main paper should at least mention the key dependencies. More critically, if CorreGen requires a specific base architecture, its generality is reduced.

### Minor

- The experimental results in Table 1 contain a formatting artifact: the "Ours" row appears twice (once underlined, once bold) with identical numbers. While this is likely a LaTeX duplication error, it creates confusion. The paper should ensure a single clean row for the proposed method.
- The dataset name "UMPC-Food101" appears to be a typo for the standard "UPMC-Food101" dataset. While the reference (Wang et al., 2015) is correct, using the wrong name could cause reproducibility issues.
- The paper claims "10% accuracy improvements on the challenging UMPC-Food101 dataset" in the introduction. At 0% MR the improvement is 13.57 absolute percentage points, which is much larger than 10%. It is unclear whether this refers to a different experimental condition (e.g., a specific noise level). The claim should be precisely specified.

### Trivial

- The paper uses "alignable mispaired" and "unaligned mispaired" in Definition 2; the phrasing "unaligned mispaired" is slightly awkward ("unpaired mispaired" might be clearer). This does not affect substance.

## Nice-to-Haves

- An analysis of computational complexity, including the cost of Sinkhorn iterations in the E-step and how it scales with batch size and number of views. The paper uses batch size 512 for realignment; it would be helpful to know whether the method scales to larger mini-batches or full datasets.
- A discussion of sensitivity to the virtual sample marginal \(\rho\). How should practitioners set this hyperparameter when the true noise ratio is unknown?

## Novel Insights

The paper offers a genuinely novel perspective by reframing noisy correspondence learning in MVC as a generative latent variable problem, rather than a discriminative reweighting or realignment task. The key insight is that cross-view correspondences can be treated as unobserved latent variables and inferred via an EM-like procedure, where the E-step jointly handles category-level semantics (through many-to-many OT with GMM-derived marginals) and sample-level noise (through virtual samples). This formulation is principled and the empirical results demonstrate that it captures semantic correspondences beyond simple instance alignment, as visualized in Figure 3. The proof that InfoNCE is a special case of the M-step under degenerate conditions also provides a theoretical link between generative and contrastive approaches.

## Suggestions

1. Clarify the relationship between the model's own marginals (which would be derived from Eq. 17) and the externally estimated GMM marginals used in the E-step. If this is an approximation or a variational bound, state it explicitly and discuss the implications.
2. Specify which parts of the method are architecture-agnostic and which depend on the DIVIDE base model. If possible, demonstrate the method on a different base MVC framework to show generality.
3. Fix the dataset name (UPMC-Food101) and the duplicated row in Table 1.
4. Provide guidance on setting the virtual sample marginal \(\rho\), e.g., using a held-out validation set or cross-validation.

## Score and Decision

The paper presents a well-motivated, theoretically grounded, and empirically strong approach to a practically important problem. The weaknesses are not fatal—the GMM heuristic is a practical choice that works well, and the base-model dependency is common in this line of work. The improvements on real-world noisy data are substantial, and the method's ability to recover latent correspondences is convincingly demonstrated. The paper merits acceptance at ICLR.

MY FINAL SCORE: <score>7.0</score>
MY FINAL DECISION: <decision>Accept</decision>