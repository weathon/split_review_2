## Summary

This paper investigates whether generative (decoder-based) or non-generative (encoder-based) approaches are necessary for compositional generalization, a key component of data-efficient visual perception. The authors provide theoretical results showing that enforcing the inductive biases required for out-of-domain (OOD) identifiability on encoders is generally infeasible because the constraints depend on the unknown geometry of OOD regions of the data manifold, whereas for decoders the constraints are global and can be enforced via architecture or regularization. Empirically, they demonstrate on photorealistic PUG datasets that non-generative methods often fail at compositional generalization unless they have large-scale pretraining, while generative methods using gradient-based search and generative replay achieve substantial OOD improvements without additional data.

## Strengths

- **Novel theoretical analysis of the asymmetry between generative and non-generative approaches.** The paper formalizes the function classes \(\mathcal{F}_{\text{int}}\) and \(\mathcal{G}_{\text{int}}\) and proves that constraining an encoder to \(\mathcal{G}_{\text{int}}\) is generally infeasible in high-dimensional ambient spaces because the required constraints depend on the unknown OOD manifold geometry (Theorem 3.2), while constraining a decoder to \(\mathcal{F}_{\text{int}}\) is straightforward. This provides a principled explanation for why non-generative methods struggle with compositional generalization.

- **Clear and well-motivated problem setup.** The paper defines perception as inverting a ground-truth generator, formalizes compositional generalization in terms of OOD identifiability, and precisely characterizes the difference between generative and non-generative approaches. This framework is rigorous and connects to prior work on identifiability and causal learning.

- **Empirical validation on photorealistic data with controlled OOD splits.** The experiments use PUG datasets, which allow explicit control over in-domain and out-of-domain concept combinations. The results show that non-generative methods (even with large-scale pretraining like SigLIP2) fail on PUG-Background and PUG-Texture, while generative methods with search and replay consistently improve OOD accuracy across all base encoders. The special case of non-interacting concepts (PUG-Object) confirms the theory that when \(\mathcal{G}_{\text{int}}\) is more structured, non-generative methods can succeed.

- **Practical methods for inverting decoders OOD.** The paper proposes gradient-based search (online) and generative replay (offline) as efficient ways to invert a learned decoder for OOD images, and shows that these methods yield significant gains. The combination of a fast encoder initialization with slower optimization is well-motivated and effective.

## Weaknesses

### Fatal
None.

### Major
- **The theoretical results rely on the assumption that the ground-truth generator belongs to \(\mathcal{F}_{\text{int}}\).** While \(\mathcal{F}_{\text{int}}\) is the largest function class known to enable OOD identifiability, it is not clear that all real-world visual data can be modeled by such functions. The paper acknowledges this limitation, but it weakens the claim that generation is *required* for data-efficient perception in general. The results are conditional on this function class.

- **The empirical evaluation is limited to PUG datasets, which are photorealistic but still synthetic and relatively simple (10 backgrounds, 32 animals, limited interactions).** The paper does not demonstrate that the proposed generative methods scale to more complex, real-world images with many concepts, occlusions, and diverse interactions. The claim that generation is required for data-efficient perception would be stronger with evidence on more realistic benchmarks.

- **The comparison between generative and non-generative methods is not entirely symmetric.** The generative methods use the same encoder as the non-generative methods plus a decoder and search/replay. The improvement could partly come from the additional decoder capacity or the search/replay procedure rather than the generative nature per se. The paper argues that the decoder is constrained to \(\mathcal{F}_{\text{int}}\), but the non-generative methods do not have access to such a decoder. A more direct comparison would be to also give non-generative methods access to a decoder (e.g., via an autoencoder) but without the generative inversion step.

### Minor
- **The paper does not report computational costs.** Gradient-based search and generative replay may be computationally expensive, especially for large images or many OOD samples. The paper claims these methods are efficient but provides no runtime or iteration count comparisons.

- **The generative methods rely on a specific decoder architecture (regularized cross-attention Transformer) that is designed to approximate \(\mathcal{F}_{\text{int}}\).** It is unclear how to design such decoders for more complex data or whether the regularization is sufficient to guarantee the required structure. The paper briefly mentions results with unstructured decoders in the appendix but does not discuss them in the main text.

### Trivial
None.

## Nice-to-Haves

- An analysis of how the required number of search steps or replay samples scales with image complexity and OOD difficulty.
- Experiments on more complex datasets (e.g., CLEVR, ObjectsRoom, or real-world images with controlled concept combinations) to test the generality of the findings.
- A comparison with other generative approaches such as diffusion models or normalizing flows for the decoder.

## Novel Insights

The paper provides a theoretical explanation for why non-generative methods struggle with compositional generalization: the constraints needed for OOD identifiability on encoders depend on the unknown geometry of OOD regions of the data manifold, making them infeasible to enforce in practice. In contrast, for decoders the constraints are global and can be enforced via architecture or regularization. This insight goes beyond prior empirical observations that non-generative methods fail on compositional tasks, and it formalizes the intuition from causal learning that the causal direction (generator) is simpler than the anti-causal direction (inverse). The paper also shows that even when non-generative methods succeed with large-scale pretraining, generative methods can achieve comparable or better OOD performance without additional data, highlighting the data-efficiency advantage.

## Suggestions

- Clarify the scope of the claim "generation is required." The paper shows that generation is required for *guaranteed* compositional generalization under the \(\mathcal{F}_{\text{int}}\) assumption, but non-generative methods can still achieve OOD generalization with sufficient data. Consider softening the title or adding a qualifier.
- Include a discussion of the computational cost of search and replay, and provide guidelines for when each method is preferable.
- Add experiments with unstructured decoders in the main text to show that the decoder architecture matters for the generative advantage.

## Score and Decision

MY FINAL SCORE: <score>8</score>
MY FINAL DECISION: <decision>Accept</decision>