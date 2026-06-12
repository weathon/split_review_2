## Summary

This paper investigates whether generative (decoder-based) or non-generative (encoder-based) methods are better suited for achieving compositional generalization, a key component of data-efficient visual perception. The authors provide a theoretical analysis showing that enforcing the inductive biases needed to guarantee out-of-domain identifiability on an encoder is generally infeasible when the image dimension exceeds the latent dimension, whereas the same constraints on a decoder can be imposed straightforwardly via architecture or regularization. They propose using gradient-based search and generative replay to invert a learned decoder on out-of-domain images, and empirically demonstrate on photorealistic PUG datasets that generative methods significantly outperform non-generative approaches—which often require large-scale pretraining—while also improving upon their own baselines through search and replay.

## Strengths

- **Theoretical clarity and novelty.** The paper formalizes the distinction between generative and non-generative perception in terms of identifiability conditions and provides a precise theoretical characterization of why non-generative methods are fundamentally limited in their ability to guarantee compositional generalization. The key insight—that the required constraints on encoders depend on the unknown geometry of the out-of-domain data manifold, while decoder constraints are axis-aligned and data-independent—is novel and well-supported.

- **Sound experimental design.** The experiments on PUG datasets are carefully constructed with controlled in-domain/out-of-domain splits, multiple encoder architectures (including large-scale pretrained models), and both supervised and unsupervised training regimes. The ablation of search, replay, and their combination provides clear evidence for the value of generative inversion.

- **Clear connection to causal learning.** The paper ties its findings to the causal-versus-anticausal learning heuristic (Janzing and Schölkopf, 2010; Kilbertus et al., 2018) and provides a formal justification for why the generative (causal) direction is more amenable to out-of-domain generalization.

## Weaknesses

### Fatal
None.

### Major

1. **Overstated title and core claim.** The title claims “Generation Is Required for Data-Efficient Perception,” but the experiments show that non-generative methods with large-scale pretraining (e.g., SigLIP2) can still achieve reasonably high OOD accuracy (≈80% on PUG-Background). The generative methods in Figure 6 also rely on the same large-scale pretrained encoders as their base. The paper does not convincingly demonstrate that generation is *required* rather than *beneficial*; a more measured claim would better reflect the evidence.

2. **Generality of the theoretical assumptions.** The theory assumes generators belong to the function class F_int (polynomial interactions up to degree n). While the authors acknowledge this limitation, it is significant: many real-world visual phenomena involve non-polynomial interactions (e.g., lighting, shadows, occlusion boundaries), and it is unclear whether the guarantees extend beyond this class. The paper would be strengthened by a discussion of how robust the findings are to deviations from F_int.

3. **Limited experimental complexity.** The PUG datasets, while photorealistic, involve only simple visual concepts (animals, backgrounds, textures) in controlled settings. The paper does not demonstrate compositional generalization on more realistic or diverse benchmarks (e.g., CLEVR, 3D scenes, or in-the-wild images). This limits the strength of the empirical conclusions about “human-level visual perception.”

### Minor

- The distinction between “generative” and “non-generative” is somewhat non-standard. The paper defines “generative” narrowly as “obtaining representations by inverting a learned decoder,” which excludes pure generative models (e.g., diffusion models) that are not decoder-inversion based. This could confuse readers and should be clarified earlier.

- The non-generative methods in Figure 5 are evaluated as standalone encoders, while the generative methods in Figure 6 combine the same encoder with a decoder and search/replay. This asymmetry is acknowledged but makes the comparison less direct; a fairer baseline would be to also give the non-generative methods access to the same decoder for classification (e.g., by using the decoder’s reconstructions).

### Trivial
None.

## Nice-to-Haves

- Include experiments on a dataset with multiple object types and more complex interactions (e.g., CLEVR or a subset of 3D-Objects) to test the scalability of the approach.
- Compare with alternative generative approaches, such as diffusion model inversion, to see if the advantages are specific to the proposed autoencoder framework.

## Novel Insights

The paper’s core theoretical contribution—that the inductive biases needed for OOD identifiability are geometrically incompatible with encoder architectures in high-dimensional ambient spaces—is genuinely novel and provides a principled explanation for the empirical success of generative replay and search methods. This result bridges causal reasoning (the causal direction being simpler) with representation learning in a formal way. The practical demonstration that generative replay (offline) and gradient-based search (online) can be combined to improve OOD performance even when the decoder is imperfect is also a valuable insight.

## Suggestions

1. **Tone down the title and central claim.** Consider changing “Generation Is Required” to something like “Generation Improves Data-Efficient Perception” or “Why Generation Helps Data-Efficient Perception.” The current title overreaches the evidence.

2. **Add a discussion on the robustness of the theory.** Acknowledge more explicitly what happens when the ground-truth generator does not belong to F_int, and discuss whether the practical benefits of generation persist in that regime.

3. **Include a more direct comparison.** Evaluate non-generative methods that also use the decoder (e.g., by using the decoder’s reconstruction loss as a regularizer or by reclassifying via the decoder) to isolate the benefit of generative inversion.

## Score and Decision

**Score:** 7.5 — The paper makes a solid theoretical contribution, is well-written, and the experiments are carefully executed. The main weaknesses are the overstated title and limited experimental scope, which prevent it from being a strong accept. The work is above the ICLR median and brings valuable insights to the community.

**Decision:** Accept

MY FINAL SCORE: <score>7.5</score>
MY FINAL DECISION: <decision>Accept</decision>