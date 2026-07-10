Now I have all the information needed. Let me produce the final consolidated review.

## Summary

This paper investigates whether generative (decoder-based) approaches are necessary for compositional generalization in perception. It formalizes the inductive biases required for OOD identifiability in both generative and non-generative settings, provides a theoretical result (Theorem 3.2) showing that constraining encoders to the required function class is generally infeasible when the ambient image dimension is large relative to the latent dimension, proposes two practical decoder-inversion schemes (gradient-based search and generative replay), and evaluates them on the photorealistic PUG datasets. The theoretical core — the structural asymmetry between the function classes F_int (decoder-side, coordinate-aligned) and G_int (encoder-side, manifold-dependent) — is novel and illuminating.

## Strengths

- **Novel theoretical result (Theorem 3.2).** The paper shows that when d_x ≥ d_z³, the Jacobian and Hessian of the inverse generator g can be arbitrary matrices — no exploitable structure exists in the ambient space. The contrast with the decoder side, where constraints in F_int are coordinate-aligned and not manifold-dependent, is clean and well-drawn. This is a genuine insight about the asymmetry between generative and non-generative approaches.

- **Experimental design responsibly connects theory to practice.** The PUG datasets provide explicit control over in-domain vs. out-of-domain compositions while remaining photorealistic. The three splits (Background, Texture, Object) cleanly correspond to different regimes of the theory (n≥1 interactions vs. n=0 non-interacting concepts). The fact that non-generative methods succeed on PUG-Object (where G_int is more structured) but fail on PUG-Background and PUG-Texture is exactly what the theory predicts, providing mutual validation of theory and experiments.

- **Systematic and meaningful empirical gap.** Fig. 5 shows that non-generative methods largely fail on PUG-Background and PUG-Texture unless equipped with massive pretraining (SigLIP2). Fig. 6 shows that generative methods (replay + search) yield meaningful gains on top of the same base encoders, demonstrating that decoder-based inversion adds value beyond what large-scale pretrained encoders already provide.

- **Careful hedging in theoretical claims.** The paper characterizes enforcing constraints on encoders as "generally infeasible with practical approaches" and "suggests" infeasibility, rather than claiming impossibility. This is an honest characterization of what the theory supports.

## Weaknesses

### Major

- **No measures of variance or statistical significance.** Results are reported as single accuracy numbers without error bars, confidence intervals, or multiple-seed results. The "best-performing combination of slot encoder and fine-tuning choice" (Sec. 5.2) is selected post-hoc across multiple configurations, which risks overestimating true performance. For an empirical study whose main evidence consists of bar charts comparing ~6 models across 3 datasets, the absence of uncertainty quantification is a genuine limitation: readers cannot assess how stable the reported patterns are. *(Verified: grep for "variance", "error bar", "standard deviation", "multiple seed" returns no matches in the paper text.)*

- **The experimental comparison conflates "generative vs. non-generative" with "availability of test-time optimization on OOD inputs."** Non-generative methods receive a single forward pass on OOD images. Generative methods additionally receive gradient-based search (Eq. 4.3, test-time optimization on each OOD image) or generative replay (Eq. 4.4, training an encoder on decoder-synthesized OOD data). The paper acknowledges this asymmetry, but a skeptic could attribute the gap to the extra OOD computation rather than to the generative approach per se. The paper would be strengthened by including a non-generative baseline with test-time adaptation (e.g., self-training or confidence-based fine-tuning on OOD inputs) to disentangle these factors. The "System 1 / System 2" framing makes the asymmetric comparison explicit, which is honest, but does not resolve it.

### Minor

- **The "data efficiency" framing in the title is asserted rather than directly tested.** The paper correctly argues that compositional generalization is essential for data efficiency, and the experiments test compositional generalization. However, "data efficiency" classically means achieving strong performance with less training data, which would require varying the amount of ID training data — a dimension not explored. The title "Generation is Required for Data-Efficient Perception" overclaims relative to what the experiments directly demonstrate.

- **The infeasibility claim is an argument from difficulty, not a proof of impossibility.** The paper hedges appropriately ("suggests," "generally infeasible," "tends to be infeasible"), but the title "Generation is Required" is absolute. The analysis shows that constraining an encoder to G_int requires knowledge of OOD manifold geometry — a real insight — but the paper does not discuss potential counter-strategies (e.g., estimating the tangent space from ID data alone, or using self-supervised tasks to implicitly capture manifold geometry).

- **The d_x ≥ d_z³ bound in Theorem 3.2 is not discussed for tightness.** If the actual threshold is much lower (e.g., d_x > d_z), the result is stronger; if it is much higher, it is weaker. The paper does not comment on whether this bound reflects the proof technique or a fundamental property.

### Trivial

None.

## Nice-to-Haves

1. A combined figure showing non-generative and generative results side-by-side for direct comparison (currently Figs. 5 and 6 are separate, requiring cross-referencing).
2. A more thorough discussion of the replay failure mode on PUG-Texture — the paper states replay "cannot be applied" because slots capture objects/backgrounds rather than textures, but does not explore whether alternative slot decompositions could make it feasible.

## Removed Points

These points from the input review were evaluated and removed:

- **"The paper's asymmetric comparison is fatal/structural"** — Demoted from Fatal to Major. The asymmetry is inherent to the paper's central claim (the decoder enables this extra machinery). It is a genuine limitation but not a fatal flaw; the paper's theoretical contribution stands independently.
- **Section-by-section presentation notes (d_x ≥ d_z³ bound discussion, formatting)** — These were absorbed into minor weaknesses or removed per the formatting/trivial filtering rules.
- **"Replay failure mode on PUG-Texture is underexplored"** — Moved to Nice-to-Haves since the paper acknowledges this limitation explicitly.
- **Claims about missing related work** — Removed per meta-reviewer rules (no external sources to confirm).
- **Reproducibility nitpicks about undisclosed hyperparameters** — Removed per meta-reviewer rules about trivial implementation details.

## Novel Insights

The most interesting observation that emerges from reading the harsh critic's review against the paper is that the paper's theoretical contribution (the asymmetry between F_int and G_int) is stronger than its empirical contribution, yet the experiments are what drive the headline claim. The inverse direction is revealing: the PUG-Object results (Fig. 5C) show that non-generative methods *can* succeed when G_int is more structured (n=0), which the paper correctly treats as a special case — but this also suggests that the boundary between "feasible" and "infeasible" may be more nuanced than the title suggests. The theory itself points toward a continuum of difficulty rather than a binary distinction.

## Suggestions

1. **Add error bars and multi-seed results.** This is the highest-priority revision. Without variance estimates, the core empirical claims cannot be properly evaluated.
2. **Include a non-generative baseline with test-time adaptation** (e.g., self-training or test-time fine-tuning on OOD inputs using a self-supervised objective) to control for the asymmetric amount of computation applied to OOD inputs.
3. **Vary the amount of ID training data** to directly test the "data efficiency" claim rather than relying on compositional generalization as a proxy.
4. **Temper the title and headline claims.** "Generation is Required" overstates what the evidence supports; "Generation is Strongly Advantageous" or "Generation Enables Principled Compositional Generalization" would be more accurate.
5. **Discuss whether the d_x ≥ d_z³ bound in Theorem 3.2 is tight** and whether the result holds under weaker conditions.

## Score and Decision

**Calibration details:**

All anchors retrieved across rounds (non-itemized shown for completeness):

| Anchor | Path | Avg Score | Round | Itemized | Comparison |
|--------|------|-----------|-------|----------|------------|
| Brady et al. (Provable Comp. Gen.) | 7VPTUWkiDQ | 7.33 | 1, 2 | Yes | Direct precursor; only synthetic experiments, current paper has more realistic data and broader theory but weaker empirical reporting |
| Interaction Asymmetry | cCl10IU836 | 7.00 | 2 | Yes | Similar theory framework; synthetic-only experiments, current paper adds photorealistic validation and practical search/replay |
| Cross-Entropy Is All You Need | hrqNOxpItr | 8.00 | 1 | Yes | Stronger theory paper with extensive experiments; similar concern about overclaiming relative to assumptions |
| Formal Theory of Compositionality | hKMPz3wkPV | 6.75 | 1, 2 | Yes | Definitional paper rejected due to fundamental technical issues; less relevant |
| Dynamics of Concept Learning | s1zO0YBEF8 | 6.50 | 1 | Yes | Theory+experiments on SIM task; weak connection to practice was a key weakness |
| Provable Length & Comp. Gen. | Hxm0hOxph2 | 5.25 | 1 | Yes | Pure theory with unrealistic assumptions; rejected |
| Unifying Disentangled Rep. | 1UMxtR9Eb9 | 5.80 | 2 | No | Compositional bias framework; less directly relevant |
| CLIP Compositional Gen. | UVSKuh9eK5 | 5.67 | 2 | No | Empirical; different framing |

**Round 1 bracket:** [5.5, 7.5]. The paper is clearly above reject-level theory papers (~5.25) due to its combination of theory and realistic experiments, but below the strongest theory+experiment papers (~8.00) due to evidential gaps in empirical reporting.

**Round 2 narrowing:** The paper's closest comparable anchors are Brady et al. (7.33) and Interaction Asymmetry (7.00). It extends both with more realistic experiments and broader theory (Theorem 3.2). However, both anchors had their primary weaknesses in experimental limitations (synthetic-only data). The current paper addresses that by using photorealistic PUG data, but introduces new evidential weaknesses (no variance/error bars, favorability=-1.77) that those papers did not have. The asymmetric comparison (favorability=2.15) is also a concern unique to this paper. The top strengths (Theorem 3.2 novelty, favorability=14.09; clean theoretical contrast, favorability=13.30) are comparable to the anchors' strongest items. The paper sits slightly below the 7.00-7.33 range due to the empirical reporting issues.

**Final score:** The paper makes a genuine theoretical contribution and the experimental design is thoughtful. However, the absence of variance/error bars and the asymmetric comparison in the main empirical evidence are significant enough to prevent acceptance at the 7+ level. The paper requires major revisions focused on empirical rigor before it can be accepted. Score: **6.5**.

MY FINAL SCORE: <score>6.5</score>
MY FINAL DECISION: <decision>Accept</decision>