## Summary

This paper argues that the “black box” characterization of neural networks is grounded in a fallacy—the assumption that causal continuity across a system necessarily implies correlative continuity (i.e., that for any distally caused output feature there must be an intermediate feature that correlates with it). Using an analogy of a clay wobble on a potter’s wheel and a recent “subliminal learning” LLM study, the author contends that in complex nonlinear systems, causation can run continuously without any individuable intermediate correlating features. This reframes opacity as ontological rather than epistemic, with consequences for how we think about explainability, trust, and the language used to describe deep learning systems.

## Strengths

- The paper raises a genuinely foundational question about the conceptual basis of “opacity” in neural networks, going beyond typical technical discussions of interpretability.
- The writing is clear, well-structured, and philosophically sophisticated, making a potentially subtle distinction (causal vs. correlative continuity) accessible.
- The “secret owls” example from the recent Cloud et al. 2025 study is an intriguing and timely case that helps ground the abstract argument in a concrete ML scenario.
- The paper engages thoughtfully with related philosophical issues (Wittgenstein, causation, explanation) without overreaching, and the three consequences section shows an attempt to connect the argument to practical concerns (trust, language).

## Weaknesses

### Fatal
None.

### Major

1. **The core analogy (clay wobble) does not convincingly establish the claimed ontological claim.**  
   The clay at \(t_2\) (at rest) does have physical properties—density distribution, shape, elasticity—that determine its oscillation frequency at \(t_3\). While no single “feature” maps one-to-one onto the frequency, the overall form is itself a collection of features; the paper’s assertion that “there is no feature… that correlates” conflates “no simple, easily decomposable feature” with “no feature at all.” The black-box metaphor in ML does not demand a single neat correlate; it typically describes the practical difficulty of tracing causation, not a metaphysical claim that no internal structure exists. The argument attacks a stronger version of the opacity thesis than many researchers actually hold.

2. **Lack of engagement with the mechanistic interpretability literature.**  
   The paper does not discuss or address existing efforts that *do* find identifiable features in intermediate representations (e.g., activation patching, probing, feature visualization, superposition analysis). This omission weakens the claim that the black box is a “myth” for neural networks specifically. Even if the clay example works, the extension to neural networks is asserted rather than demonstrated; the paper does not provide evidence that no correlative features exist in, say, the hidden states of the LLM in the owls example.

3. **The “secret owls” example is not rigorously analyzed.**  
   The paper acknowledges that a full demonstration would require its own paper, but this leaves the central ML case study largely unsupported. Without a detailed argument that the training data truly lacks any statistical or structural correlate of the owl preference (e.g., distributional signatures, patterns in the digit sequences that relate to the teacher model’s behavior), the conclusion that no correlative feature exists is speculative. The example could instead be explained by existing concepts like dataset artefacts or latent causal structure that is merely opaque in practice, not in principle.

### Minor

- The paper’s claim that “an omniscient god could not identify a feature” in the intermediate state is rhetorically strong but philosophically slippery: an omniscient being with full knowledge of the system’s dynamics *could* predict the output from the state, which suggests that the state *does* contain the relevant information—just not in a human-friendly, decomposable form. The argument risks sliding between “no decompositional feature” and “no information.”

- The discussion of trust (Section 3.2) is too brief and does not draw concrete implications that would distinguish the author’s view from standard debates about post-hoc interpretability.

### Trivial

- None.

## Nice-to-Haves

- A more thorough philosophical defense of why the “overall state” is not itself a feature (or set of features) could strengthen the ontological claim.
- A concrete analysis of the Cloud et al. data—e.g., showing that standard attribution methods fail to find any input-token correlate for the owl behavior—would make the paper much more compelling to an ML audience.
- Discussion of how the argument relates to specific XAI methods (e.g., SHAP, integrated gradients) and whether they implicitly assume correlative continuity would be valuable.

## Novel Insights

The paper’s central insight—that the search for intermediate causal correlates may be ontologically fruitless in nonlinear systems, not merely epistemically hard—is a worthwhile conceptual point that is often glossed over in the explainable AI literature. However, the insight is not new in philosophy of science (e.g., discussions of emergence, holism, or “causal thickness”), and its application to neural networks is not sufficiently developed to constitute a major advance for the ML community. The paper does not go beyond the analogy to provide a crisp criterion for when correlative continuity holds or fails in a network, nor does it propose any new methodology.

## Suggestions

- Substantially deepen the analysis of the owls example. Demonstrate, even in a small-scale controlled experiment, that no correlative feature can be found in the training data despite clear causal continuity.
- Engage with at least one prominent existing interpretability method and show how it implicitly relies on the correlative-continuity assumption that the author argues is fallacious.
- Clarify the target of the critique: many researchers use “black box” merely as a shorthand for practical difficulty, not a metaphysical claim. The paper should more carefully distinguish the version of the opacity thesis it is attacking from weaker, more common versions.

## Score and Decision

This is a well-written philosophical position paper that raises a legitimate conceptual concern, but it lacks the empirical or analytical depth to support its strong claim that “the box is a myth” in the context of neural networks. The core argument relies on an analogy with clay that does not fully transfer, and the paper does not engage with the technical interpretability literature that would be necessary to persuade an ML audience. The contribution is more suggestive than definitive, and the paper is unlikely to substantially change how researchers approach explainability.

MY FINAL SCORE: 4.0<score>4.0</score>
MY FINAL DECISION: Reject<decision>Reject</decision>