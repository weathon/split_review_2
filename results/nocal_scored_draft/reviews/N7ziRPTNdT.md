Good. The analysis confirms that within Fig. 6 the comparison is controlled (same VAE, with vs. without replay/search). The critic's Issue 4 about supervision asymmetry is partially overblown — I'll keep a weakened version. Let me now produce the final review.

## Summary

This paper provides a theoretical and empirical analysis of whether generative (decoder-based) or non-generative (encoder-based) methods can achieve compositional generalization. The core theoretical contribution (Theorem 3.2) shows that when the observed dimension is large relative to the latent dimension (d_x ≥ d_z³), the Jacobian and Hessian of inverse generators in the function class G_int can be arbitrary — the structural constraints that enable compositional generalization are manifold-dependent and cannot be straightforwardly enforced on encoders. By contrast, the same constraints are axis-aligned and globally enforceable on decoders. Empirically, the paper shows that standard non-generative methods often fail on compositional generalization in controlled photorealistic datasets (PUG), while adding generative replay and gradient-based search to the same encoder-decoder models yields significant improvements.

## Strengths

- **A clear and meaningful theoretical result (Theorem 3.2, Sec. 3.1).** The paper proves that when d_x ≥ d_z³, the Jacobian and Hessian of inverse generators in G_int can be arbitrary — there is no required structure at individual points. This is a genuine mathematical finding that formalizes an intuition discussed informally in the literature. [favorability: 1.00]

- **Clean conceptual contrast between the decoder and encoder cases (Eqs. 3.1/3.4, Fig. 3).** The paper crisply distinguishes axis-aligned, globally applicable decoder constraints (F_int) from manifold-dependent, data-ill-posed encoder constraints (G_int). The geometric intuition in Fig. 3 — latent space extends "Cartesian" while the data manifold has curved unknown boundaries — is genuinely illuminating. [favorability: 0.88]

- **The PUG-Object result supports the theory predictively.** The special case n=0 (Sec. 3.1) predicts that when concepts do not interact, G_int becomes more structured and non-generative methods should find compositional generalization easier. The experiments (Fig. 5C) confirm this — all methods achieve near-perfect OOD accuracy on PUG-Objects. This is a successful *prediction* from the theory, which is stronger evidence than a post-hoc explanation. [favorability: 1.00]

- **The search and replay mechanisms (Sec. 4) are well-motivated.** Gradient-based search initialized by an encoder and generative replay flow naturally from the theoretical analysis rather than being ad-hoc additions. [favorability: 1.00]

## Weaknesses

### Fatal
None.

### Major
- **The experiments do not directly test the infeasibility claim.** The theory argues that *constraining an encoder to G_int is infeasible* (Sec. 3). The experiments test whether *standard off-the-shelf non-generative methods (without explicit G_int constraints)* fail on compositional generalization (Sec. 5). These are related but different claims. A skeptical reader could say: "You haven't shown non-generative methods *cannot* work with appropriate constraints; you've shown that the specific methods you tried don't work well." The paper would be substantially strengthened by attempting to construct encoders that approximate G_int constraints (e.g., regularizing toward Eq. 3.4 using an estimate of the tangent space) and demonstrating their failure directly. [favorability: 0.11]

### Minor
- **Framing mismatch between title/abstract and what is actually proven.** The title "Generation is Required for Data-Efficient Perception" and abstract framing imply a broad claim. The theory is conditioned on f ∈ F_int (Eq. 2.7) — the largest function class shown to enable OOD identifiability, but not proven to cover all natural image generators. The paper acknowledges this limitation in Sec. 7, but the title and abstract do not carry this qualifier. [favorability: 0.50]

- **The "data efficiency" framing is not empirically tested.** The introduction frames the paper around human-level "data efficiency" (children encountering concepts "only a handful of times," line 27), but the experiments do not vary the amount of training data. What is actually shown is that generative methods improve OOD generalization *without requiring additional data* — a legitimate but different claim. [favorability: 0.41]

- **No reporting of variance or confidence intervals.** The paper reports "the best-performing combination of slot encoder and fine-tuning choice" (line 213) without error bars or standard deviations. With multiple architectures, fine-tuning choices, and random seeds, selecting the best risks inflating reported performance. This is a meaningful gap for a paper making comparative claims. [favorability: 0.54]

### Trivial
None.

## Nice-to-Haves

- **Direct test of the infeasibility claim:** Attempt to construct an encoder regularized toward G_int constraints (e.g., via Eq. 3.4 with tangent space estimation) and demonstrate its failure, to directly bridge theory and experiments.
- **Data-scaling experiment:** Varying ID dataset size would directly substantiate the "data efficiency" language in the title and abstract.
- **Error bars:** Reporting variance across runs for the key experimental figures.
- **Computational cost discussion:** The per-image gradient-based search procedure has implications for real-time perception that could be discussed.

## Removed Points

*(These points appeared in the sourcereview but were removed per filtering rules. Treat with caution.)*

- **"The 'unstructured decoder' control is deferred to Appendix C":** Removed because the parser strips appendices; the original submission contains this material.
- **"Why SigLIP2 pretraining helps (scale vs. objective)":** Removed as speculative — the paper is not required to ablate every factor.
- **"The generative method starts from the same pretrained encoder (Issue 4b)":** Weakened and partially removed because this is by design — the controlled comparison is VAE-without-replay vs. VAE-with-replay (same encoder), which is fair.
- **"The n=0 special case is underspecified":** The paper explains the unknown sparsity pattern; this is adequately addressed.
- **"The non-generative SigLIP2 supervised already achieves 80% undercuts the failure claim":** The paper's headline comparison is VAE w/o replay vs. VAE w/ replay (controlled), not SigLIP2 supervised vs. VAE generative. However, a softened version of the concern is kept: the strongest non-generative baseline (SigLIP2 supervised) achieves ~80% OOD accuracy, which modestly undercuts the framing that "non-generative methods fail."

## Novel Insights

The strongest signal from the review process is that the paper's theoretical contribution (Theorem 3.2 + Eq. 3.4) is genuinely novel and well-supported, but the paper consistently overframes its results. The theory proves an infeasibility result about a specific function class (F_int/G_int), but the title, abstract, and conclusions paint with a broader brush. The experiments provide directional support for the theory but do not directly test the infeasibility claim — they test standard methods rather than attempting (and failing) to constrain encoders to G_int. This gap between what the theory proves and what the experiments test is the paper's central unresolved tension. Fixing it would require either tighter experiments or more careful framing.

## Suggestions

1. Adjust the title and abstract to reflect the conditionality of the theoretical results on the F_int function class.
2. Add error bars or variance reporting to Figs. 5 and 6.
3. Either run a data-scaling experiment or replace the "data efficiency" framing with "compositional generalization without additional data."
4. Consider a targeted experiment that attempts to explicitly regularize an encoder toward G_int constraints (Eq. 3.4) to directly support the infeasibility claim.

## Score and Decision

This is a solid paper with a meaningful theoretical contribution. Theorem 3.2 and the G_int manifold-dependence analysis are genuine advances. The experiments are well-designed for what they test, and the PUG-Object n=0 prediction provides strong confirmatory evidence. The major weakness — that experiments test standard methods rather than directly testing the infeasibility claim — is significant but does not invalidate the core theory. The paper would be stronger with revisions to align its framing with its actual contributions and to tighten the experiment-theory connection.

MY FINAL SCORE: <score>7.0</score>
MY FINAL DECISION: <decision>Accept</decision>