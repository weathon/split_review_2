## Summary
This paper argues that the characterization of neural networks as "black boxes" with hidden, inaccessible internal causes is based on a fallacy—the assumption that causal continuity necessarily implies correlative continuity. The author contends that in complex nonlinear systems, including neural networks, there can be genuine causal continuity without there existing individuable intermediate features that correlate with the output features we seek to explain. The paper uses a clay potter's wheel example to illustrate this point and discusses consequences for understanding subliminal learning in LLMs, trust in AI, and the language of opacity in the field.

## Strengths
- The paper identifies and challenges a genuinely subtle philosophical assumption that underlies much of the discourse on explainable AI—the conflation of causal continuity with correlative continuity. This is a novel and potentially important conceptual contribution.
- The clay potter's wheel example is well-chosen and effectively illustrates the distinction between causal continuity and correlative continuity in an intuitive, non-technical way.
- The paper engages seriously with the philosophical literature on causation and explanation while remaining accessible to a machine learning audience, and it correctly identifies that the "black box" framing has real consequences for how researchers approach interpretability problems.

## Weaknesses

### Fatal
None.

### Major
- **The paper's central claim is not well-supported for neural networks specifically.** The clay example demonstrates that correlative discontinuity is *possible* in some physical systems, but the paper does not provide any argument that neural networks are the *kind* of system where this phenomenon occurs. Neural networks have highly structured, differentiated internal representations (features, circuits, attention heads) that are precisely the kind of thing that could serve as intermediate correlates. The paper acknowledges this difference (Section 2.3) but does not bridge the gap between the clay example and neural networks. The "secret owls" example is presented as a candidate case, but the paper explicitly admits (footnote 15) that demonstrating correlative discontinuity in that case "would require a paper of its own."

- **The paper conflates two different senses of "correlative continuity."** The clay example shows that there is no *single, simple feature* of the still clay that corresponds to the wobble frequency. But this does not show that there is no *complex, distributed, or holistic* feature that correlates. The paper's own language ("the overall form of the clay," "the whole of its state") suggests that the entire system state *does* carry the relevant information. The question is whether neural network internal states are more like the clay (where only the whole state matters) or more like systems where individual components carry meaningful correlates. The paper does not address this.

- **The practical implications for XAI research are unclear.** Even if the philosophical point is accepted, it is not obvious what changes in practice. Researchers already use methods like probing, activation patching, and circuit analysis to find *distributed* representations and *interactions* between features, not just simple one-to-one correlates. The paper does not engage with the actual technical literature on mechanistic interpretability to show how its argument would change research practice.

### Minor
- The paper's treatment of the "secret owls" example is somewhat superficial. The Cloud et al. study is from 2025 and appears to be a real paper, but the description here is too brief to fully evaluate whether the correlative discontinuity interpretation is indeed the most plausible one.
- The discussion of trust (Section 3.2) is too cautious and does not reach a clear conclusion. The paper says the implications "will depend on the details" but does not provide any analysis of what those details might be.

### Trivial
- The paper could benefit from more explicit engagement with the mechanistic interpretability literature, which already operates under the assumption that features can be distributed and non-obvious.

## Nice-to-Haves
- A more detailed analysis of the "secret owls" case, perhaps with a sketch of how one would test whether correlative discontinuity holds.
- A discussion of how the argument relates to specific XAI methods (e.g., does it affect the validity of Shapley values, integrated gradients, or activation patching?).
- A more concrete proposal for how the language of opacity should be revised in practice.

## Novel Insights
The paper's core insight—that the assumption of correlative continuity is a contingent empirical fact about most systems rather than a necessary truth—is genuinely novel and philosophically interesting. The distinction between epistemic opacity (we cannot find the intermediate causes) and ontological opacity (there are no intermediate causes to find) is worth making, even if the paper does not fully establish that neural networks fall into the latter category. The paper also correctly identifies that the "black box" metaphor carries implicit commitments that may not be warranted.

## Suggestions
- Provide a more rigorous argument for why neural networks specifically might exhibit correlative discontinuity, perhaps by identifying properties they share with the clay example (e.g., high-dimensional nonlinear dynamics, lack of modular decomposition for certain features).
- Engage with the mechanistic interpretability literature to show how the argument either challenges or is consistent with existing approaches to understanding neural network internals.
- Clarify what "feature individuation" means in the context of neural networks—is the claim that there is no *single neuron or attention head* that correlates, or that there is no *distributed representation* that correlates? The latter would be a much stronger and harder-to-defend claim.

## Score and Decision
The paper makes a genuinely interesting philosophical point, but it does not adequately connect this point to the specific case of neural networks. The central claim—that the "black box" framing is based on a fallacy—is not well-supported for the domain it targets. The paper is more a philosophical essay than a contribution to machine learning research, and while it raises worthwhile questions, it does not provide sufficient evidence or argument to change how researchers should think about or approach neural network interpretability.

MY FINAL SCORE: <score>4</score>
MY FINAL DECISION: <decision>Reject</decision>