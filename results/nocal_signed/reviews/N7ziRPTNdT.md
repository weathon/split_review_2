Now let me write the final consolidated review.

## Summary

This paper presents a theoretical and empirical analysis of why generative (decoder-inversion) approaches are fundamentally better positioned for compositional generalization than non-generative (encoder-only) approaches. The central theoretical contribution (Theorem 3.2) proves that when the ambient image dimension is much larger than the latent dimension ($d_x \geq d_z^3$), constraining an encoder to the function class $\mathcal{G}_{\text{int}}$ that guarantees compositional generalization is infeasible because the required constraints depend on the unknown geometry of out-of-domain regions. In contrast, the corresponding constraints on decoders ($\mathcal{F}_{\text{int}}$) are axis-aligned and globally applicable. Experiments on PUG datasets show that non-generative methods often fail at compositional generalization while generative methods leveraging gradient-based search and generative replay achieve significant improvements.

## Strengths

- **Theorem 3.2 is a central and nontrivial theoretical contribution.** It establishes that when $d_x \geq d_z^3$, the first- and second-order derivatives of $g \in \mathcal{G}_{\text{int}}$ at any point can be essentially arbitrary (any matrix $A$, any symmetric matrices $B_l$). This cleanly proves that $\mathcal{G}_{\text{int}}$ has no local, point-wise signature in high-dimensional ambient space, meaning one cannot regularize an encoder to belong to $\mathcal{G}_{\text{int}}$ by imposing constraints on its derivatives at observed points. This is a crisp theoretical asymmetry with the decoder case, where the $\mathcal{F}_{\text{int}}$ constraint is axis-aligned and globally applicable.

- **The contrast between in-principle possibility and in-practice infeasibility is clearly articulated.** Section 2 correctly notes that both approaches *can* guarantee compositional generalization in theory (by constraining to $\mathcal{F}_{\text{int}}$ or $\mathcal{G}_{\text{int}}$), and then convincingly argues why the latter constraint cannot be realized practically. This framing avoids straw-man arguments.

- **The experimental design cleanly separates the two approaches.** The "w/o replay" baseline in Fig. 6 *is* the non-generative approach (encoder on OOD), while "with replay" and "with replay + search" add generative inference on top of the *same* trained model. This isolates the effect of the generative decoding step from confounders such as architecture, training data, and supervision. The finding that replay and search consistently improve OOD accuracy across all six base encoders (Fig. 6) is compelling.

- **The PUG-Object ($n=0$) experiment acts as an important boundary condition.** The result that all methods succeed when concepts do not interact is consistent with the theory (Sec. 3.1, special case of $n=0$) and demonstrates that the paper does not claim non-generative methods *never* work — it claims they fail precisely when the inverse structure is least constrained. This honesty strengthens the paper.

## Weaknesses

### Fatal
None.

### Major

- **Evidential gap between theory and experiments.** The core theoretical claim is that *constraining* an encoder to $\mathcal{G}_{\text{int}}$ is infeasible. However, the experiments do not attempt to constrain an encoder — they train unconstrained encoders and observe whether they *happen* to generalize. The paper acknowledges this ("whether compositional generalization occurs depends on whether the optimization process happens to avoid converging to such a solution," Sec. 3 takeaways), but the experiments demonstrate something different: unconstrained encoders often fail, and generative search/replay helps. This is consistent with the theory but does not directly demonstrate the infeasibility of constraining encoders. A direct test (e.g., attempting to enforce Eq. (3.4) via regularization and showing it fails because it requires knowledge of $\mathcal{X}_{\text{OOD}}$) would close this gap. This gap does not invalidate the paper — the theory stands on its own — but it weakens the link between the paper's strongest theoretical claim and its empirical demonstration.

### Minor

- **No uncertainty estimates are reported.** Fig. 5 and Fig. 6 show point estimates only, with no error bars, confidence intervals, or measures of statistical significance. Given the moderate dataset size (~20K images), it is unclear whether performance differences (especially the modest gains from "with replay" vs. "with replay + search" for some model-dataset combinations) are robust.

- **Generative methods are only evaluated on unsupervised VAEs** (Fig. 6), not on the supervised models from Fig. 5. It remains unclear whether search/replay would also benefit supervised encoders, or whether the benefits are specific to unsupervised representations. This limits the generality of the empirical comparison.

- **Replay is inapplicable on PUG-Texture.** The paper acknowledges this (slots capture objects/backgrounds and cannot be trivially recomposed for animal-texture combinations), meaning one of the two generative strategies is unavailable for one of the three splits. The split where replay does work (PUG-Background) involves the conceptually simplest manipulation (changing backgrounds). This limits the breadth of the generative demonstration.

- **The computational cost of gradient-based search is not discussed.** No estimates are given for the number of gradient steps required, wall-clock time per image, or whether convergence is reliably achieved. Since the paper presents search as a practical strategy, some practical cost characterization would be helpful.

- **The $d_x \geq d_z^3$ condition in Theorem 3.2 is stated but not contextualized** with experimental parameters. For the PUG datasets, what are $d_x$ (image dimension) and $d_z$ (latent dimension)? The paper asserts this is the "more practical case" without connecting the theoretical condition to the specific evaluation setup, which would help readers assess whether the theory applies to the experiments.

- **The role of the decoder architecture is not discussed in the main text.** The paper uses a regularized cross-attention Transformer designed to approximately match $\mathcal{F}_{\text{int}}$ and mentions that results with "unstructured decoders" are in Appendix C (removed by parser). Since the theoretical argument is that $\mathcal{F}_{\text{int}}$ constraints are straightforward to enforce, it matters whether the generative gains depend on this specific structured decoder or persist with unstructured alternatives.

### Trivial
None.

## Nice-to-Haves
- A small-scale direct test of the encoder-constraining infeasibility claim (attempting to enforce Eq. (3.4) via regularization on ID data and showing it fails to transfer OOD)
- Statistical significance reporting for experimental results
- Concrete estimates of the computational cost of gradient-based search
- Contextualization of the $d_x \geq d_z^3$ condition with experimental parameters

## Removed Points
These points from the input review were removed with justification:

- **"Conflation of having a decoder vs. inverting a decoder"**: REMOVED because the paper explicitly addresses this. Line 53 states: "We emphasize that the difference between the generative and non-generative approaches is not whether an encoder or decoder is used." The paper also clarifies in Sec. 5.1 that the VAE case is "non-generative since the encoder is only constructed to invert the decoder on X_ID, and not on X_OOD." The criticism is factually incorrect.
- **"Human-level perception framing overstates results"**: REMOVED. The paper uses "human-level visual perception" as motivation/framing, not as a claimed experimental result. The limitations section (Sec. 7) explicitly acknowledges scope.
- **"SigLIP2 achieving ~80% shows non-generative methods don't fail"**: REMOVED. The paper claims methods "frequently fail" (not "always fail") and acknowledges that large-scale pretraining improves performance. Fig. 5 shows most models perform poorly; SigLIP2 is the exception.
- **"Search and replay are not new"**: REMOVED. The paper explicitly cites prior work; novelty lies in the theoretical connection, not the algorithms.
- **"Missing comparison with diffusion-based classifiers"**: REMOVED. Scope creep — the paper's generative approach is about inverting a learned decoder, not about diffusion models.
- **"Proof in removed appendix cannot be verified"**: REMOVED per instructions — the appendix was stripped by the parser, not omitted by the authors.
- **"Smoothness could compensate"**: REMOVED. Theorem 3.2 directly addresses this; derivatives can be arbitrary at a point, so smoothness alone cannot compensate.
- **"Diffeomorphism assumption is strong"**: REMOVED. This is a standard assumption in nonlinear ICA, and the paper is transparent about its modeling assumptions.

## Novel Insights
None beyond the paper's own contributions.

## Suggestions
- Add error bars or confidence intervals to all experimental figures.
- Extend the generative evaluation to include supervised models to test whether search/replay benefits generalize beyond unsupervised VAEs.
- Provide concrete estimates of the computational cost of gradient-based search (number of steps, wall-clock time).
- Contextualize the $d_x \geq d_z^3$ condition with the experimental parameters of the PUG datasets.
- If possible, include a small-scale direct test of the encoder-constraining infeasibility claim (e.g., attempting to regularize an encoder toward Eq. (3.4) using ID data and showing it fails to transfer OOD).

MY FINAL SCORE: <score>7.5</score>
MY FINAL DECISION: <decision>Accept</decision>