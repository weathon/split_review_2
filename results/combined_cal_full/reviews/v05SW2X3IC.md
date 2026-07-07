## Summary

This paper instantiates a learnable Gray-Wyner network — a three-channel codec with one common and two private channels — for multi-task vision compression. It extends prior "coding for humans and machines" work (which used only two channels) to settings where two vision tasks share common information but also have private information. The authors derive a β-parameterized Lagrangian objective that controls the transmit-receive rate tradeoff (β=1 for transmit, β=2 for receive, β=3/2 for equal weighting), and validate their method on synthetic data, colored MNIST, Cityscapes (segmentation + depth), and COCO (detection + keypoint).

## Strengths

- **First to bridge Gray-Wyner theory to learned multi-task codecs.** The paper correctly observes that two vision tasks with shared-but-not-identical information needs call for a three-channel architecture (common + two private channels), and grounds this architecture in the information-theoretic Gray-Wyner rate region. This is a genuine and well-motivated extension over prior two-channel "coding for humans and machines" work. (Evidence: Section 2.1, Figure 1, line 17)

- **Clean, theoretically grounded objective for the transmit-receive tradeoff.** The derivation from Theorem 2 to the Lagrangian in Eq. 12, where β=1 optimizes for transmit rate and β=2 for receive rate, is sound. The fact that β cleanly parameterizes the tradeoff and β=3/2 equally weights both is a satisfying theoretical result with direct practical utility. (Evidence: Theorem 2, Eqs. 9-12, line 157)

- **Well-designed diagnostic experiments.** The synthetic linear regression dataset (Section 4.1, known entropies: H(X₁,X₂)=3.3 bits, I(X₁;X₂)=1.32 bits) and the colored MNIST edge cases (Section 4.2, three PMFs with known mutual information: full, zero, and partial) are exactly the right kind of controlled experiments for validating that the method separates common information as intended. The results in Figures 3 and 4 confirm the method responds correctly to the information-theoretic structure. (Evidence: lines 209-235, Figures 3-4)

## Weaknesses

### Fatal
None.

### Major

1. **No comparison against prior multi-task codecs.** The paper cites Chamain et al. (2021), Feng et al. (2022), and Guo et al. (2024) as "multitask learnable codecs" that "propose one or more common channels to perform several tasks" (line 37). These are the most directly relevant baselines, yet none appear in the experimental evaluation. The paper's defense — "their rate is optimal only when all the tasks involved are performed jointly" — characterizes a design difference but does not justify their absence. Without such comparisons, readers cannot assess whether the three-channel Gray-Wyner architecture offers practical advantages over existing multi-common-channel alternatives. This is the single biggest gap in the evaluation.

2. **Headline claim framed against the weakest baseline.** The conclusion states "our codecs achieved, on average, a BD-rate advantage of -81.58% in transmit rate, against single-task codecs" (line 275). This number is computed against the Independent baseline (no common channel), which is *designed* to be transmit-inefficient. Against Joint (one shared channel) — the more informative baseline — the proposed method needs *more* rate (23.32% more on Cityscapes, 13.16% more on COCO, Figure 5). The paper shows this honestly in the figures but frames the headline result against the baseline that makes the method look best, inflating the perceived improvement. The abstract's claim ("consistently outperforms independent coding") is true but sets a low bar.

### Minor

3. **The common channel combining mechanism (Eq. 14) has a potentially brittle design.** The core mechanism for producing Y₀ uses a hard "match-or-zero" rule: elements that match between the two branches are averaged; elements that disagree are set to zero. This means the common channel can only contain information that both branches independently extract and quantize to the *same discrete index*. If two views of the same information quantize to nearby but non-identical indices (common with noisy inputs or slightly different transforms), that information is lost from Y₀. The paper acknowledges that tuning the auxiliary loss coefficient γ (Eq. 15) is delicate, with small γ producing no matches and large γ producing degenerate distributions (lines 179-181). While γ=1 works in practice, this is a potential fragility the paper does not ablate against alternatives (e.g., learned convex combinations, gated mechanisms, or projection-based merging).

4. **No error bars or variance estimates for BD-rate results.** The BD-rates in Figures 4 and 5 are reported as point estimates with no measure of variability across random seeds. Given the known variance in training learned codecs, some quantification of uncertainty would significantly strengthen the experimental claims.

5. **Receive-rate tradeoff incompletely demonstrated for real tasks.** Figure 5 shows the Proposed (Receive) method has higher BD-rates (51.97%, 42.7%) than Proposed (Transmit) (23.32%, 13.16%) when both are measured against Joint, but does not provide a receive-rate-centric view where the β=2 model would be expected to outperform β=1. Without this, the transmit-receive tradeoff is harder to verify empirically for the real-task experiments.

### Trivial
None.

## Nice-to-Haves
- Report individual channel rates (R₀, R₁, R₂) for the real-task experiments (Cityscapes, COCO) to directly demonstrate how information is allocated across channels, as is done for the synthetic data.
- Compare against the prior multi-task codecs (Chamain et al., Feng et al., Guo et al.) on the same Cityscapes and COCO task pairs.
- Ablate the mask-based combining mechanism (Eq. 14) against alternatives such as learned convex combinations or projection-based merging.
- Note in the main paper that jointly training the task models with the codec could yield different rate-distortion tradeoffs.

## Removed Points
These points are flagged to be removed, treat them with caution:
- **"Theorem 1 practical value unclear" (removed):** Information-theoretic bounds routinely serve as conceptual guides rather than computable quantities. This is standard practice, not a weakness specific to this paper.
- **"Entropy model description under-specified" (removed):** The paper describes the conditioning mechanism and references Appendix D for full architectural diagrams, which is standard for conference papers.
- **"Frozen pre-trained task models concern" (removed):** The reviewer acknowledges this is a reasonable design choice. The suggestion to explore joint training is a nice-to-have.
- **"Scalability to more than 2 tasks" (removed):** The paper explicitly addresses this as future work (line 279). Scope creep.
- **"Three experiments count confusing" (removed):** The paper describes three CV experiments (colored MNIST, Cityscapes, COCO). This count is accurate.

## Novel Insights
The most interesting observation from the reviews is the tension between the paper's hard "match-or-zero" combining mechanism for Y₀ (Eq. 14) and the information-theoretic goal of separating common from private information. This design forces the common channel to only capture information that both branches quantize to identical discrete indices, which is a strong constraint. The auxiliary loss (Eq. 15) attempts to encourage matching, but the acknowledged brittleness of γ tuning (lines 179-181) suggests this is a genuine engineering challenge. None beyond the paper's own contributions.

## Suggestions

1. **Add comparisons against prior multi-task codecs.** Comparing against Chamain et al., Feng et al., and Guo et al. on the same Cityscapes and COCO task pairs would directly answer the most obvious question: does the three-channel architecture offer practical advantages over existing multi-common-channel alternatives? If it matches or beats them, the contribution is clearly significant.

2. **Reframe headline claims honestly.** The abstract and conclusion should state that the key novelty is the controllable transmit-receive tradeoff via β, with performance lying between Joint (transmit-optimal, 13-23% less rate) and Independent (receive-optimal, 77-144% more rate). The -81.58% number should be contextualized as "against the Independent baseline."

3. **Report individual channel rates (R₀, R₁, R₂) for real tasks** to directly demonstrate how the method allocates information across channels, as done for synthetic data (Figure 3a).

4. **Add variance estimates** (e.g., across random seeds) for BD-rate results.

## Score and Decision

MY FINAL SCORE: <score>5.5</score>
MY FINAL DECISION: <decision>Accept</decision>