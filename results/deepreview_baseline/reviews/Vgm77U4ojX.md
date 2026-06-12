## Summary

This paper introduces SIGMADOCK, a novel fragment-based SE(3) Riemannian diffusion model for molecular docking. Instead of using torsional angles (which suffer from non-local coupling and gauge ambiguities), the method decomposes ligands into rigid-body fragments via a new reduction scheme (FR3D), and diffuses over their translations and orientations on SE(3) m. By leveraging geometric priors (soft triangulation constraints and a carefully designed equivariant architecture), SIGMADOCK achieves state-of-the-art re-docking performance, surpassing both prior deep learning methods and classical physics-based docking on the PoseBusters and Astex benchmarks under the standard PDBBind(v2020) train-test split.

## Strengths

- **Novel and well-motivated methodological contribution.** The paper clearly identifies the fundamental limitations of torsional diffusion models (non-locality, gauge ambiguity, induced non-product measures) and proposes a principled alternative based on rigid-body fragments. The theoretical justification (Theorem 1, Lemma 1, Theorem 2) cogently supports why operating in SE(3) m offers a simpler learning problem than torsion-space diffusion.

- **Strong empirical results with rigorous experimental design.** SIGMADOCK reports Top-1 PB-valid success rates of 79.9% on PoseBusters and 90.6% on Astex, substantially outperforming existing deep learning methods (reported range 12.7–32.8%) and classical docking. The paper includes careful ablations (fragmentation merging, triangulation conditioning, protein–ligand interactions, sampling heuristic components), robustness analyses (pocket size sensitivity, co-factor stratified performance, sequence-similarity splits), and a fair comparison against methods trained on the same train-test split.

- **Data efficiency and computational practicality.** The model is trained solely on PDBBind(v2020) (~19k complexes) and matches AlphaFold3-level performance with orders of magnitude less training data and 50× faster sampling, demonstrating that principled inductive biases can replace reliance on massive scale. The method does not require a separately trained confidence model or post-hoc minimisation to achieve high validity.

- **Open source and reproducible.** The authors commit to releasing the codebase, which is essential for independent verification and further development.

## Weaknesses

### Fatal

None.

### Major

- **Comparison to AlphaFold3 is not fully contextualised.** AlphaFold3 is a co-folding model that jointly predicts protein and ligand structures under different assumptions (flexible receptor, whole-protein modelling). The paper frames the comparison as "AF3-level performance" on the re-docking task, but this conflates two distinct problem settings. While the raw numbers are informative, the discussion would benefit from a clearer separation of the evaluation protocols and a more nuanced interpretation of what the comparison implies about each method's strengths and limitations.

- **The ranking heuristic is a central component yet under-analysed against learned alternatives.** The paper uses a simple heuristic (pseudo binding energy plus physicochemical checks) to select among sampled poses, and an ablation shows that removing energy scoring hurts performance by ~13%. However, there is no comparison against a learned confidence model (e.g., DiffDock's confidence head). Since ranking is critical to the reported Top-1 numbers, the absence of this comparison weakens the claim that the generative model alone is responsible for the gains, and leaves the reader unsure whether a better ranking scheme could further improve results.

### Minor

- **The stochastic fragmentation reduction (FR3D) could introduce uncontrolled variance.** FR3D performs stochastic merges of adjacent fragments to reduce degrees of freedom. Although the paper provides empirical results that fragmentation merging helps (Ablation C), the stochastic nature of the process means different merges could lead to different performance. No analysis is provided on the sensitivity of the final results to the specific merge trajectory chosen during training or inference.

- **The claimed degrees-of-freedom advantage over torsional models is not fully concretised.** The paper states that fragment models have DoFs between k+6 and 6m, while torsional models have k+6, but the effective number after FR3D reduction is not empirically reported for the dataset. Providing a histogram of fragment counts and effective DoFs across the PDBBind set would make the argument more concrete.

## Nice-to-Haves

- An empirical comparison against DiffDock-L on the PoseBusters set *under the same training setup* (even if DiffDock-L is trained on more data) would strengthen the claim of superiority over existing deep learning methods.
- An analysis of how the stochastic FR3D merge choices affect the training stability and final accuracy across multiple seeds would help assess robustness.

## Novel Insights

Beyond the paper's own contributions, the key insight is that the widely adopted torsional parametrisation for molecular diffusion introduces an ill-conditioned learning problem due to the non-local and ambiguous mapping from torsion updates to Cartesian displacements. By shifting to rigid-body fragments, the forward process factorises over a product of Haar measures on SE(3), and inter-fragment correlations are learned *only* via the score function rather than being baked into the noise kernel. This simple but conceptually important distinction—between induced and factorised noise kernels—provides a design principle that could apply to other structured prediction problems where internal dynamics are separable at coarse granularity.

## Suggestions

- Expand the discussion of the AF3 comparison to clarify the differences in problem setting (co-folding vs. rigid-receptor docking) and explicitly state that the comparison is meant to demonstrate data efficiency rather than claim equivalence as a docking tool.
- Report the distribution of fragment counts and effective degrees of freedom after FR3D across the training set, to quantitatively support the DoF reduction claim.
- Consider benchmarking against a learned confidence model (even one trained on SIGMADOCK's outputs) to isolate the contribution of the ranking heuristic.

## Score and Decision

Score: 8 – This is a strong paper with a novel, theoretically grounded method, careful experimentation, and results that represent a clear step forward in the field of deep learning–based molecular docking. The weaknesses are not fatal and can be addressed in a revised version or discussion.

MY FINAL SCORE: <score>8</score>
MY FINAL DECISION: <decision>Accept</decision>