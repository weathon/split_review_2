Now I'll write the final consolidated review.

## Summary
This paper presents a theoretical and empirical analysis arguing that generative (decoder-based) approaches have a principled advantage over non-generative (encoder-based) approaches for compositional generalization in visual perception. The core theoretical result (Theorem 3.2) shows that when the image dimension far exceeds the latent dimension, constraining an encoder to the inverse function class that enables compositional generalization is infeasible because the constraints depend on the unknown geometry of OOD regions, whereas constraining a decoder to the corresponding generator class is straightforward since the constraints are coordinate-aligned and data-independent. Experiments on PUG photorealistic datasets confirm that non-generative methods often fail at compositional generalization without large-scale pretraining, while generative methods using search and replay improve OOD performance.

## Strengths
- **Theorem 3.2 is a genuine theoretical contribution.** The result that when $d_x \geq d_z^3$, the Jacobian and Hessian of any inverse $g \in \mathcal{G}_{\text{int}}$ can be essentially arbitrary at a point formally establishes why constraining encoders to guarantee compositional generalization is fundamentally harder than constraining decoders. The contrast between the coordinate-aligned constraints for decoders (Eq. 3.1) versus the manifold-dependent constraints for encoders (Eq. 3.4) is clearly articulated and genuinely illuminating.
- **The empirical comparison is well-controlled.** The setup uses the same autoencoder: the non-generative baseline evaluates the VAE encoder directly on OOD data, while the generative variants invert the same decoder via search and/or replay. This cleanly isolates the benefit of the generative inference strategy. The differences (e.g., from-scratch ViT-S/36 on PUG-Background showing ~15-20% non-generative vs. ~60-70% generative) are striking.
- **Honest treatment of the n=0 special case.** The paper explicitly notes (Sec. 3.1, Sec. 5.2) that when concepts do not interact (PUG-Object), the inverse class is more structured and non-generative methods succeed. This demonstrates that the theory correctly predicts where the asymmetry will and will not matter.
- **Connection to causal vs. anti-causal learning (Sec. 6).** The paper connects its results to the broader causal learning literature, providing a formal justification for the heuristic that generalization is easier in the causal direction.

## Weaknesses

### Fatal
None.

### Major
- **Framing overclaims relative to what is theoretically established.** The title "Generation Is Required for Data-Efficient Perception" and the abstract's claim that "such inductive biases cannot be enforced on an encoder through practical means such as regularization or architectural constraints" suggest an unconditional result. However, the theory is conditional on the ground-truth generator belonging to the specific parametric class $\mathcal{F}_{\text{int}}$ (Eq. 2.7). The paper acknowledges this in Sec. 7, but the title and abstract do not carry this caveat. Moreover, the experiments show that non-generative methods with large-scale pretraining (SigLIP2) achieve ~80% OOD accuracy on PUG-Background, which is compatible with the theory (which is about guarantees, not impossibility) but contradicts the unconditional framing. The paper's actual contribution — that within $\mathcal{F}_{\text{int}}$, decoders can be constrained to *guarantee* compositional generalization while encoders cannot — is valuable and does not need the stronger claim. This is the most significant weakness and should be addressed by softening the title and abstract.

### Minor
- **All experiments use a single dataset family.** While PUG offers photorealistic controllability, it is one family of synthetic scenes with a limited concept vocabulary (10 backgrounds, 32 animals). The paper acknowledges this in Sec. 7, but the scope of empirical evidence remains narrow for the motivating question about human-level visual perception.
- **The search method's practical cost is uncharacterized.** Gradient-based search (Sec. 4.1) requires optimizing Eq. 4.3 for each OOD image at inference time. The paper mentions that "many gradient steps are required" can lead to "slow or suboptimal convergence" (line 165) but provides no analysis of how many steps are needed, how often optimization succeeds, or sensitivity to hyperparameters. Since search is one of only two OOD inversion strategies (and replay cannot be applied to PUG-Texture), this gap weakens the practical case the paper tries to make.
- **Theory-experiment alignment gap.** The theory concerns *guaranteeing* compositional generalization (requiring exact membership in $\mathcal{F}_{\text{int}}$ or $\mathcal{G}_{\text{int}}$), but the experiments use a "regularized cross-attention Transformer" that only *approximately* enforces the $\mathcal{F}_{\text{int}}$ constraint (Sec. 5.1). The generative methods achieve good but not perfect OOD accuracy. The paper would benefit from explicitly clarifying the distinction between the theoretical guarantee and the empirical demonstration throughout.
- **Bar charts lack quantitative labels.** Figs. 5 and 6 report results only through bar charts without numerical values. Exact numbers (or a supplementary table) are needed to assess the magnitude of improvements precisely.

### Trivial
None.

## Nice-to-Haves
- Characterize search convergence behavior (typical number of gradient steps, failure cases, sensitivity to initialization) to make the practical feasibility clearer.
- Include a failure analysis: when generative methods do not achieve 100% OOD accuracy, what mistakes do they make? Do errors correlate with certain concept combinations?
- Discuss why the decoder trained on $\mathcal{X}_{\text{ID}}$ should be a good model of $\mathcal{X}_{\text{OOD}}$ — the identifiability result (Eq. 2.5) helps but depends on the decoder being exactly in $\mathcal{F}_{\text{int}}$ and exactly matching ID, both of which are approximate in practice.
- A controlled comparison with a larger non-generative architecture trained from scratch would help distinguish whether the generative advantage is due to architectural inductive bias or simply having more total parameters.

## Removed Points
These points from the input review were removed after verification against the paper:

1. **"Straw-mannish framing of the debate"** — the paper defines the generative and non-generative views clearly with citations; this is a reasonable framing for the paper's scope.
2. **"Lemma 3.1 is a warm-up"** — this describes the lemma's role, not a flaw; the paper explicitly frames it as a warm-up.
3. **"Eq. 2.1 implicitly assumes slot-structured latents"** — this is a standard assumption in the compositional generalization literature, inherited from prior work (Brady et al., 2025), and is clearly stated.
4. **"MSE landscape for OOD may be poorly behaved"** — speculative; the paper's search method is a well-motivated approach and the challenge of initialization is already discussed.
5. **"SigLIP2 at ~80% shows difficulty is about model capacity/scale"** — this is fully compatible with the theory (which concerns guarantees, not impossibility); already addressed in the Major weakness about overclaiming.
6. **Various formatting nitpicks** — parser artifacts, not author errors.

## Novel Insights
The harsh review's key insight is that the paper's strongest claim runs ahead of what the evidence supports: "Generation Is Required" is not what is shown. What is shown is that, under the $\mathcal{F}_{\text{int}}$ assumption, generation provides a principled way to *guarantee* compositional generalization while non-generative methods need large-scale data to achieve it without guarantees. This distinction between guarantee (theory) and practical success (experiments) is blurred in the current framing and should be clarified. Additionally, the paper would benefit from explicitly confronting the fact that large-scale pretrained non-generative encoders (SigLIP2 at ~80%) can succeed in practice, which does not contradict the theory but does contradict the more absolutist framing.

## Suggestions
- **Revise the title and abstract** to reflect what is actually shown: that generation provides a principled *guarantee* for compositional generalization under the $\mathcal{F}_{\text{int}}$ assumption, while non-generative methods cannot be similarly guaranteed. Replace "required" language with "provides a principled path to guarantee."
- **Add a quantitative table** reporting the exact OOD accuracy values from Figs. 5 and 6.
- **Include a brief characterization** of search costs (typical number of gradient steps, convergence behavior, failure modes).
- **Explicitly clarify** throughout the paper that the theory concerns *guarantees* while the experiments demonstrate *practical benefits* — these are related but distinct claims.

## Score and Decision

**Calibration anchors used across all rounds:**

| Path | Avg Score | Round | Comparison |
|------|-----------|-------|------------|
| `gwZ90hFSL2.md` | 1.00 | R1 (bracket) | Unrelated topic; our paper is far stronger |
| `Uj0h13lVrR.md` | 1.00 | R1 (bracket) | Unrelated topic; our paper is far stronger |
| `hv8l922Ad7.md` | 3.40 | R1 (bracket) | Reject-level disentanglement paper; our paper has stronger theory and experiments |
| `AxYTFpdlvj.md` | 2.00 | R1 (bracket) | Graph decoding; unrelated |
| `Hxm0hOxph2.md` | 5.25 | R1 (bracket) | Compositional generalization theory with very strong assumptions; our paper has more realistic experiments and cleaner theory |
| `7VPTUWkiDQ.md` | 7.33 | R1 (bracket) | Most similar anchor: object-centric compositional generalization with identifiability theory on synthetic data. Our paper has more realistic experiments (PUG vs. simple synthetic) but somewhat more incremental theory over prior work |
| `hrqNOxpItr.md` | 8.00 | R1 (bracket) | Strong identifiability theory paper; our paper is comparable in theoretical rigor but narrower in scope |
| `cCl10IU836.md` | 7.00 | R2 (narrow) | "Interaction Asymmetry" — extremely closely related theoretical framing; our paper extends to the encoder asymmetry analysis |
| `s1zO0YBEF8.md` | 6.50 | R2 (narrow) | "Dynamics of Concept Learning" — theory with overclaiming concerns, accepted; comparable quality to our paper |
| `H98CVcX1eh.md` | 6.50 | R2 (narrow) | "Discovering modular solutions" — theory + experiments, accepted; comparable profile |

**Round 1 bracket:** 5.5–7.5 (plausible range after initial bracketing).

**Round 2 narrowing:** The closest anchors (Interaction Asymmetry at 7.00, Provable Compositional Generalization at 7.33) are slightly stronger in terms of theoretical novelty, while our paper has better experiments. The overclaiming in framing is a real weakness that prevents reaching the 7+ level. The 6.5 anchors (Dynamics of Concept Learning, Discovering modular solutions) are the closest quality matches.

**Final score: 6.5** — borderline accept. The paper makes a genuine theoretical contribution with carefully controlled experiments, but the framing overclaims relative to what is actually proven, and the empirical evidence is limited to one dataset family.

MY FINAL SCORE: <score>6.5</score>
MY FINAL DECISION: <decision>Accept</decision>