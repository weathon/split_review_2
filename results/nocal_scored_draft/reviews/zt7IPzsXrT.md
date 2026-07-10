## Summary

This paper proposes ScaPre, a closed-form framework for large-scale concept unlearning in text-to-image diffusion models. It combines a conflict-aware stable design (spectral trace regularizer + geometry alignment via Bures distance) with an Informax Decoupler that uses mutual information to confine updates to concept-relevant parameters. The method solves its core optimization via a Sylvester equation and handles the non-quadratic geometry alignment term through a separate proximal refinement.

## Strengths

- **The ImageNet-Confuse5 benchmark (Table 4) is the strongest evidence for precision.** It directly tests disentanglement by constructing groups of visually similar concepts (e.g., dog breeds) where some are targets and others must be preserved. ScaPre achieves 5.8% Unlearn Acc while keeping 76.3% Preserve Acc. By contrast, UCE (2.9% unlearn, 5.6% preserve) destroys everything, making its good unlearning number meaningless. This cleanly validates the central precision thesis.

- **The scalability comparison on ImageNet-Diversi50 (Table 3) shows ScaPre occupies a unique region.** No other method simultaneously achieves low residual accuracy (3.9%) without generative collapse (CLIP 29.41). UCE/RECE collapse generatively (CLIP 22.23/21.78) while training-based methods barely unlearn (~78% accuracy). This is the paper's most practically significant result.

- **The closed-form core via the Sylvester equation (Eq. 9–10) is well-motivated.** Avoiding iterative fine-tuning for the quadratic part of the objective is architecturally appealing, and the derivation is clearly presented.

## Weaknesses

### Fatal
None.

### Major
- **Runtime contradiction between text and Figure 3.** The contribution bullet and Section 5.5 state "completing the unlearning of 50 concepts within only **120 seconds**," yet Figure 3's data table reports ScaPre at ~1.5 hours — a 45× discrepancy. Since efficiency ("Lightweight Design") is a headline contribution claim, the authors must clarify what the 120 seconds covers (unlearning computation only?) vs. what the 1.5 hours covers (including evaluation?), and ensure consistency across the paper.

### Minor
- **The Informax Decoupler (Section 4.2) is underspecified in the main text.** Key details are not given: what "input feature s" indexes over (tokens? images? denoising steps?), how the adaptive threshold τ_i is set, the number of samples K, and what constitutes "neutral inputs" (y=0). These may be in the appendix, but the main text alone is insufficient for implementation.
- **The "no additional data" claim needs qualification.** The Informax Decoupler requires both target-concept inputs and neutral inputs to compute mutual information. If these are already available from the concept-embedding set (i.e., no external data is needed), that should be stated explicitly rather than claimed as "requiring no additional data."
- **The UQ metric is relative and table-dependent.** It is normalized using the mean and std of the methods being compared per-table, making values incomparable across different tables and sensitive to which baselines are included. The paper does report raw Avg Acc and CLIP scores alongside UQ, so this does not invalidate results, but claims of superiority should be grounded primarily in the absolute metrics.
- **The "×5 more concepts" claim is imprecise.** The abstract states the method "can forget up to ×5 more concepts than the best baseline within the limits of acceptable generative quality," but "acceptable generative quality" is not quantitatively defined. Without a fixed criterion this claim is rhetorical rather than precise.
- **Notation inconsistency:** Section 5.4 defines the holistic indicator as "CLIP_π" but Table 2 uses "CLIP_x" for the same column.
- **No discussion of failure cases or limitations.** The paper presents only positive results and does not analyze scenarios where ScaPre might struggle (e.g., highly overlapping concept embeddings, scaling beyond 50 concepts, sensitivity to β or the threshold parameters).

### Trivial
None.

## Nice-to-Haves
- Include a brief summary of key ablation results (per-component contribution) in the main text, rather than only in the appendix.
- Report unlearning computation time and evaluation/generation time separately for all methods to avoid ambiguity.

## Removed Points
These points are flagged to be removed; treat them with caution:
- Criticism that geometry alignment is "incompatible with closed-form" — the paper explicitly acknowledges this (Section 4.3, line 131) and handles it via a separate proximal refinement; this is transparent, not a flaw.
- Missing related work mentions — cannot be verified without external sources.
- Formatting/style nitpicks and parser artifacts.
- Speculative claims about the Informax Decoupler being computationally non-trivial — not supported by evidence.
- Generic criticisms about evaluation rigor, baseline fairness, or evidence strength that lacked a specific anchor in the paper.
- Missing appendix content or absent references — these sections are parser-stripped.
- Ablation visibility concern — the paper directs to the appendix, which is standard practice for the main text.

## Novel Insights
None beyond the paper's own contributions.

## Suggestions
1. Resolve the runtime contradiction definitively: report unlearning computation time and evaluation time separately for all methods, and ensure the 120-second claim is correctly scoped and consistent with Figure 3.
2. Define what threshold(s) constitute "acceptable generative quality" when making the ×5 claim, or replace the claim with a precise quantitative statement.
3. Add a brief limitations paragraph discussing scenarios where ScaPre may struggle and parameter sensitivity.
4. Fix the CLIP_π / CLIP_x notation inconsistency between text and Table 2.

MY FINAL SCORE: <score>6</score>
MY FINAL DECISION: <decision>Borderline Accept</decision>