Now I have sufficient context. Let me compile the final review.

**Calibration Summary:**

| Anchor | Avg Score | Round | Itemized? | Comparison to Paper Under Review |
|--------|-----------|-------|-----------|----------------------------------|
| 7VPTUWkiDQ.md (Brady et al.) | 7.33 | R1 | Yes | The paper this work builds on. Stronger theory-experiment link but only synthetic experiments. My paper uses photorealistic data but lacks statistical rigor. |
| s1zO0YBEF8.md (Dynamics of Concept Learning) | 6.50 | R1 | Yes | Theory + diffusion experiments, but SIM task criticized as poor proxy. My paper has cleaner theory-experiment alignment. |
| 7QGyDi9VsO.md (Next State Prediction) | 5.00 | R1 | Yes | Distributed vs slot-based comparison, but claim-evidence issues and weak baselines. My paper has stronger theory. |
| hKMPz3wkPV.md (Formal Theory of Compositionality) | 6.75 | R1 | Yes | Pure theory paper with definitional issues. My paper has both theory and experiments. |
| HYyRwm367m.md (Neural LoTM) | 6.50 | R2 | Yes | Good experiments but synthetic-only and novelty concerns. My paper has stronger theory. |
| UVSKuh9eK5.md (CLIP Compositional Generalization) | 5.67 | R2 | Yes | Empirical study on CLIP, somewhat messy evaluation. My paper has clearer claims. |
| pBxeZ6pVUD.md (Grounded OCL) | 6.00 | R2 | Yes | Solid but incremental slot attention variant. My paper has more novel theoretical contribution. |

**Round 1 bracket:** 5.5–7.5 (appropriate given the topic similarity with Brady et al. at 7.33 and the reject papers around 5.0)

**Narrowing assessment:** Comparing item weights with the Brady anchor (7VPTUWkiDQ.md, avg 7.33): Brady's worst weakness is weight 2.31 (synthetic-only experiments); my paper's worst is weight 1.93 (no statistical reporting). My strengths are marginally higher (8.50–10.13 vs 7.87–9.91) and I use photorealistic PUG data, which directly addresses Brady's core weakness. However, the statistical reporting gap and multiple moderately damaging weaknesses (3.45, 3.64, 3.84) place this paper below Brady's 7.33. Comparing with the Grounded OCL paper (pBxeZ6pVUD.md, avg 6.00): my theory is more novel and my experiments are on photorealistic data, placing me slightly above 6.00.

**Final Score:** 6.0

---

## Summary

This paper investigates whether generative (decoder-based) approaches are necessary for data-efficient compositional generalization in visual perception. Theoretically, it formalizes the constraints needed for compositional generalization in both generative and non-generative methods, proving (Theorem 3.2) that enforcing such constraints on an encoder is generally infeasible when the ambient data dimension substantially exceeds the latent dimension, while constraining a decoder is straightforward. Empirically, it evaluates non-generative methods (pretrained encoders) on photorealistic PUG datasets, finding they often fail to generalize compositionally unless trained at web-scale. By contrast, adding gradient-based search and generative replay to an autoencoder yields significant OOD improvements without additional data.

## Strengths

- **The paper formalizes generative and non-generative approaches on a common theoretical footing (Eqs. 2.5/2.6).** This framing cleanly separates the two paradigms as different paths to the same identifiability condition, rather than treating them as incomparable. [weight=10.13]
- **Theorem 3.2 provides a concrete structural asymmetry result.** It shows that when d_x ≥ d_z³, the Jacobian and Hessian of inverse functions in G_int can be arbitrary, while forward functions in F_int remain structured — a formal argument for why constraining an encoder is harder than constraining a decoder. [weight=8.50]
- **The experimental design cleanly distinguishes interaction regimes (PUG-Background n>0, PUG-Texture, PUG-Object n=0).** The finding that all non-generative methods succeed on PUG-Object while failing on PUG-Background validates the theory's prediction about the n=0 special case. [weight=10.12]
- **Search and replay produce consistent improvements across all base encoder architectures on PUG-Background.** This robustness across architectures (from-scratch ViT through SigLIP2) strengthens the empirical case. [weight=9.24]
- **The paper connects a theoretical identifiability result to practical algorithmic techniques (gradient-based search and generative replay),** effectively bridging theory and practice. [weight=9.69]

## Weaknesses

### Fatal
None.

### Major

- **No statistical reporting on empirical results.** All OOD accuracies are reported as point estimates without error bars, confidence intervals, or multiple-seed variation. The procedure of reporting "the OOD accuracy obtained with the best-performing combination of slot encoder and fine-tuning choice" for each base encoder (Sec. 5.2) is described without clarifying whether selection was done on a held-out validation set or how many configurations were tried. This makes it difficult to assess whether the reported advantages reflect genuine improvement versus configuration selection luck. [weight=1.93]

- **The paper's central theoretical condition (d_x ≥ d_z³ from Theorem 3.2) is not verified for the experiments, and the latent dimension d_z used in the autoencoder is never stated.** For the theorem to formally apply to the experiments, the ground-truth latent dimension must satisfy d_z ≤ d_x^(1/3) — e.g., ≤∼53 for 224×224 images, ≤∼58 for 256×256. While the qualitative insight (d_x ≫ d_z) clearly holds for images, stating d_z and explicitly discussing the connection would strengthen the theory-experiment link. [weight=4.75]

### Minor

- **The decoder constraint is only approximate (regularized cross-attention Transformer, cited from Brady et al. 2025), while the theoretical guarantees require exact membership in F_int.** The paper acknowledges this approximation but does not discuss how close the approximation is or whether the guarantees degrade gracefully. Results with unstructured decoders are deferred to the appendix. [weight=5.66]
- **The title "Generation is Required for Data-Efficient Perception" overstates what the evidence supports.** Non-generative methods (SigLIP2) achieve ∼80% OOD accuracy on PUG-Background, and all methods achieve near-perfect performance on PUG-Object. The results show that generation enables more data-efficient compositional generalization, not that it is strictly required. A reframed title would better match the evidence. [weight=3.84]
- **The computational cost of search and replay is not discussed.** Gradient-based search requires iterative optimization per OOD test image (could be orders of magnitude slower than a single feedforward pass), and generative replay requires training a second encoder on synthesized data. The paper describes these as "efficient" but provides no wall-clock time, FLOPs, or gradient step counts. [weight=3.64]
- **The comparison between "non-generative" and "generative" methods uses the same autoencoder (VAE) in both cases**, differing only in whether the decoder is used for OOD inference via search/replay. This is a valid comparison of inference strategies but does not test whether a purely feedforward architecture (no decoder at all) would fare differently. [weight=3.45]
- **The paper does not explain why the cubic threshold (d_x ≥ d_z³) appears in Theorem 3.2** — whether this is sharp or simply a sufficient condition for the proof technique. While the full proof is in the appendix, a brief intuition in the main text would help readers assess how restrictive this condition is. [weight=6.39]

### Trivial
None.

## Nice-to-Haves
- Quantify the computational overhead of search (gradient steps per OOD image, convergence criteria) and replay (number of generated images, training cost).
- Add a discussion of how close the regularized cross-attention decoder is to F_int (e.g., sensitivity to regularization weight, ID vs. OOD tradeoffs).
- Report the latent dimension used in the autoencoder and verify whether d_x ≥ d_z³ holds.

## Removed Points
These points are flagged to be removed, treat them with caution:
- **"The VAE baseline labeled 'non-generative' already has a generative decoder, making the comparison asymmetric."** — The paper defines 'generative' vs 'non-generative' by whether representations are obtained by inverting a decoder on OOD data (Sec. 2), not by whether a decoder exists. The definition is explicit: "the difference between the generative and non-generative approaches is not whether an encoder or decoder is used" (line 53). This criticism misreads the paper's definition and is factually incorrect.
- **"The human analogy is ornamental rather than supported by the evidence."** — Subjective framing critique of introduction motivation. The analogy is used as standard motivational context, not as evidence.
- **"PUG datasets...web-scale pretraining data likely contains similar images" / contamination concern.** — Speculative; the paper states PUG datasets were not in the pretraining set. Critic questions whether pretraining provides compositional experience, which is exactly the paper's point (pretraining helps at the cost of data efficiency).
- **"The cubic condition is asserted but not derived."** — The proof is in the appendix, which the parser strips from all papers. This is a parser artifact, not an author omission.
- **Section-by-section commentary** that raises preferences rather than identifying specific flaws.

## Novel Insights
None beyond the paper's own contributions. The theoretical analysis of the F_int vs G_int asymmetry (Theorem 3.2), the connection to practical search/replay algorithms, and the experimental validation on PUG datasets constitute the paper's primary contribution.

## Suggestions
1. Add statistical reporting: 3–5 random seeds with standard deviations, clarify hyperparameter selection (held-out validation set, number of configurations tried).
2. State the latent dimension d_z used in experiments and discuss the d_x ≥ d_z³ condition.
3. Report the computational overhead of search (gradient steps per OOD image) and replay (# generated images, training cost).
4. Reframe the title to match the empirical scope (e.g., "Generation Enables More Data-Efficient Compositional Generalization").

## Score and Decision

MY FINAL SCORE: <score>6.0</score>
MY FINAL DECISION: <decision>Accept</decision>