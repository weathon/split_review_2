Now I've read the full paper. Let me draft the review based on my verified findings.Now let me run Round 1 calibration — bracketing across score bands:Let me read the most relevant anchors in detail to calibrate:Now I have sufficient calibration data. Let me form my bracket and write the final review.

**Round 1 Bracket:** Based on the anchors:
- The paper is clearly above the 3.5-5.5 rejected papers (e.g., "Learning Identifiable Concepts" at 4.25, "Provable Length and Compositional Generalization" at 5.25)
- It is comparable to "Provable Compositional Generalization for Object-Centric Learning" (7.33, accepted) — the Brady et al. paper this work builds on — and "Dynamics of Concept Learning" (6.50, accepted)
- It has a clean theoretical insight and confirmatory experiments but overclaims and has narrower experimental scope than the strongest 8.0 papers like "Cross-Entropy Is All You Need"

**Initial bracket: 6.0–7.5**

Now let me write the final consolidated review:

---

## Summary
This paper investigates whether generative (decoder-based) or non-generative (encoder-based) approaches are better suited for compositional generalization in visual perception. The key theoretical contribution (Theorem 3.2) demonstrates an asymmetry: constraining a decoder to the function class $\mathcal{F}_{\text{int}}$ requires enforcing block-diagonal derivative structure that is coordinate-aligned and data-independent (Eqs. 3.1–3.2), while constraining an encoder to $\mathcal{G}_{\text{int}}$ requires enforcing structure relative to the unknown data manifold tangent space (Eq. 3.4), which is infeasible in practice. Experiments on PUG datasets confirm that non-generative methods fail OOD without large-scale pretraining, while generative methods with gradient-based search and replay improve OOD performance.

## Strengths

- **Genuine structural insight in the decoder/encoder asymmetry (Theorem 3.2, Sec. 3).** The paper proves that when $d_x \geq d_z^3$, the Jacobian and Hessian of inverse generators are essentially unconstrained in ambient space. The remaining structure (Eq. 3.4) persists only on the data manifold's tangent space, which is unknown for OOD regions. In contrast, decoder constraints (Eq. 3.1–3.2) are coordinate-aligned and can be enforced universally. This is a clean, non-trivial mathematical result that formalizes an informal conjecture from the causal/anti-causal learning literature (Kilbertus et al., 2018).

- **Theory-confirming experimental design, particularly the PUG-Object control (Fig. 5C, Sec. 5.2).** When $n=0$ (concepts do not interact), $\mathcal{G}_{\text{int}}$ is more constrained, and all models achieve near-perfect OOD accuracy — exactly as predicted by Sec. 3.1. The contrast with PUG-Background (Fig. 5A), where interacting concepts break non-generative methods trained from scratch, provides a clean confirmation of the theory's predictions. This is notably better than papers where theory and experiments are decoupled.

- **Coherent unification across literatures (Secs. 1, 6).** The paper connects cognitive science (analysis-by-synthesis), causality (causal vs. anti-causal learning), and identifiability theory into a single formal story. The connection to Kilbertus et al. (2018) — this paper provides a formal justification for their informal conjecture — is well-drawn and adds intellectual value.

- **Practical search and replay mechanisms with consistent empirical gains (Sec. 4, Fig. 6).** The System 1/System 2 framing (encoder for initialization, decoder inversion for refinement) is clean, and Fig. 6 shows consistent improvements across all base encoders for both search and replay.

## Weaknesses

### Fatal
None

### Major

- **Title and abstract overclaim relative to theoretical evidence.** The title states "Generation Is Required" but Theorem 3.2 proves only that derivative-based constraints on encoders are vacuous when $d_x \gg d_z$. The transition from this to "constraining an encoder is infeasible" (lines 122–125) is an informal argument, not a theorem. The paper's own Discussion acknowledges: "these results may, in principle, fail to generalize to function classes associated with other settings, where non-generative strategies may be effective" (line 231). This caveat does not propagate to the title or abstract. What has been shown is that for $\mathcal{F}_{\text{int}}$, one natural class of encoder constraints fails — not that all possible encoder-side approaches fail. The gap between "we cannot find a practical way for this function class" and "generation is required" is meaningful.

- **The pretraining confound weakens the data-efficiency narrative.** The paper frames the question around data efficiency (title, abstract, Sec. 1), but generative methods in Fig. 6 also use pretrained base encoders. The from-scratch generative model with replay achieves roughly 40–50% on PUG-Background vs. ~15% for non-generative from scratch — but this is far below ~80% for the SigLIP2 non-generative model. This means generation provides a structural improvement over matched baselines but does not substitute for large-scale pretraining. The claim that generation enables "data-efficient" perception is not cleanly tested by the experimental design as presented.

### Minor

- **Narrow experimental scope relative to framing.** The PUG datasets feature at most two animals + one background (10 backgrounds, 32 animal types, ~20,000 images). Real-world compositionality involves many more interacting factors. The Introduction invokes "human-level visual perception" and children's learning (line 27), setting expectations the experiments cannot meet. The paper acknowledges this limitation (line 231), but the framing gap is notable.

- **Replay has a significant practical limitation (line 219).** Replay cannot be applied on PUG-Texture because slots must align with axes of compositional variation. In realistic settings where compositional structure is not known a priori, constructing the replay distribution is unclear. This narrows the practical applicability of one of the two proposed methods.

- **Missing computational cost analysis for search.** The paper argues encoder constraints are impractical but does not report the computational cost of its own decoder-inversion alternative — how many gradient steps, convergence rates, or wall-clock overhead per image. This information is needed to fully evaluate the practical tradeoff.

### Trivial
None

## Nice-to-Haves

- A controlled data-efficiency experiment: train both generative and non-generative methods from scratch on datasets of varying size and plot OOD accuracy as a function of training data, directly testing the data-efficiency claim.
- Train encoders with an explicit regularizer attempting to enforce Eq. 3.4 using estimated tangent spaces from ID data, to directly test the theoretical prediction that this fails.
- Surface Appendix C results on unstructured decoders in the main text to strengthen the case that the $\mathcal{F}_{\text{int}}$ constraint is necessary for decoder-side gains.
- Brief analysis of search failure modes (non-convex loss landscape, poor initialization) and convergence properties.

## Removed Points
*These points are flagged to be removed; treat them with caution.*

- **"The comparison is structurally asymmetric" (generative gets encoder+decoder+search vs. encoder alone):** This is the paper's entire thesis — the extra structured decoder machinery *is* the contribution. The theory argues this structural advantage is necessary, so the asymmetry is the point, not a confound. The relevant comparison is whether non-generative methods with comparable *unstructured* extra computation (e.g., self-training) would close the gap, but this is a nice-to-have, not a weakness of the current design.

- **"The definition of compositional generalization (Eq. 2.4) assumes individual slot values are fully observed":** This is a clearly stated assumption in the formal setup, scoping the problem appropriately. It is not a weakness but a modeling choice.

- **Demands for variance reporting across runs:** The performance gaps are large (e.g., ~15% vs ~80% in Fig. 5A), making variance unlikely to affect conclusions. This is a standard practice nitpick.

- **Criticism about the connection between $\mathcal{F}_{\text{int}}$ and the actual decoder architecture being "under-specified":** The paper describes the cross-attention Transformer decoder with attention weight regularization (Sec. 5.1, line 207) and references Brady et al. (2025) and Appendix C for details, including results with unstructured decoders. This is adequately addressed given space constraints.

## Novel Insights
The core novel insight is the formal demonstration that the structural asymmetry between generators and their inverses maps precisely onto the causal/anti-causal distinction: decoder constraints are coordinate-aligned and data-independent, while encoder constraints are manifold-dependent and therefore infeasible for OOD regions. The PUG-Object experiment ($n=0$ case) serves as an elegant "control condition" — when concept interactions vanish, the encoder-side structure becomes more tractable and all methods succeed, confirming the theory's prediction that the difficulty scales with interaction degree.

## Suggestions
- Soften the title to something like "Generation Has a Principled Structural Advantage for Data-Efficient Perception" to align claims with the evidence.
- Add a from-scratch data-efficiency curve comparing generative vs. non-generative methods at varying dataset sizes to directly test the data-efficiency claim.
- Report gradient-step count and wall-clock time for search to complete the practical feasibility argument.
- Surface the unstructured decoder results from Appendix C in the main text — if unstructured decoders degrade OOD performance, this directly supports the theory.

## Score and Decision

**Calibration anchors (all rounds):**

| Paper | Path | Avg Score | Round | Comparison |
|---|---|---|---|---|
| Provable Compositional Generalization for Object-Centric Learning | 7VPTUWkiDQ | 7.33 | R1 | Most directly relevant — the Brady et al. (2025) paper this submission builds on. The paper under review extends it with a novel encoder/decoder asymmetry insight and photorealistic experiments, but overclaims relative to evidence. Roughly comparable in quality. |
| Dynamics of Concept Learning and Compositional Generalization | s1zO0YBEF8 | 6.50 | R1 | Related topic but weaker theoretical contribution. The paper under review has a cleaner, more impactful insight and more practical methods. Should score at least as high. |
| Discovering modular solutions that generalize compositionally | H98CVcX1eh | 6.50 | R1 | Comparable scope in the compositional generalization space. The paper under review has a stronger theoretical contribution. |
| Cross-Entropy Is All You Need To Invert the Data Generating Process | hrqNOxpItr | 8.00 | R1 | Stronger empirical validation across multiple scales (synthetic → DisLib → ImageNet). The paper under review has narrower experiments and overclaims more. Below this level. |
| Identifying Representations for Intervention Extrapolation | 3cuJwmPxXj | 8.00 | R1 | Clean identifiability theory with strong practical implications and broader experimental scope. The paper under review is somewhat below this level. |
| On Provable Length and Compositional Generalization | Hxm0hOxph2 | 5.25 | R1 | Solid theory but rejected. The paper under review has a more insightful and practically relevant contribution. Above this level. |
| Learning Identifiable Concepts for Compositional Image Generation | 0BBzwpLVpm | 4.25 | R1 | Weaker theory, limited baselines, rejected. The paper under review is substantially stronger. |
| On the Identifiability of Nonlinear Representation Learning with General Noise | 7oT1X8xjIk | 5.80 | R1 | Identifiability theory paper that was rejected despite interesting results. The paper under review has stronger practical implications and cleaner experiments. |
| Correcting Flaws in Common Disentanglement Metrics | hv8l922Ad7 | 3.40 | R1 | Weak contribution, rejected. Far below the paper under review. |
| Do Generative Models Learn Rare Generative Factors? | Eg32tDGgF5 | 3.00 | R1 | Empirical study without theoretical depth, rejected. Far below. |
| Generator Matching | RuP17cJtZo | 8.00 | R1 | Different topic (generative modeling frameworks). Not directly comparable but illustrates the quality bar for score 8. |
| Strong Model Collapse | et5l9qPUhm | 8.00 | R1 | Different topic. Clean theory paper at score 8. |

**Round 1 bracket:** 6.0–7.5

**Narrowing:** The paper extends Brady et al. (7.33) with a genuinely novel asymmetry insight and photorealistic experiments, but overclaims ("required" rather than "has structural advantage") and has a confounded data-efficiency narrative. The theoretical contribution is clean and the PUG-Object control experiment is elegant. Compared to Brady et al. (7.33), the insight is novel and important, but the overclaiming and experimental limitations pull it slightly below. Compared to the 6.50 papers, this has a stronger theoretical contribution and more practical methods. The paper sits around 7.0 — a solid contribution with overclaimed framing.

**Final score: 7.0**

The paper makes a genuine and insightful theoretical contribution (the decoder/encoder asymmetry for compositional generalization) that is confirmed by well-designed controlled experiments, connects multiple research communities, and offers practical methods. The overclaiming in the title/abstract and the confounded data-efficiency narrative are real weaknesses but do not undermine the core contribution. This is above the acceptance threshold.

MY FINAL SCORE: <score>7.0</score>
MY FINAL DECISION: <decision>Accept</decision>