## Summary
This paper argues that characterizing neural networks as "black boxes" rests on a flawed assumption: that causal continuity across a system necessarily implies correlative continuity (i.e., that intermediary features must exist that correlate with distal causes and effects). Using an analogy of a potter's clay that retains a wobble across a pause, the author contends that in some nonlinear systems, causal continuity can hold without individuable intermediate correlating features. The paper applies this to the "secret owls" LLM subliminal learning study and discusses consequences for XAI, trust, and the language of opacity.

## Strengths
- The philosophical argument is genuinely interesting and clearly structured. The distinction between epistemic and ontological limits of explainability—that "hidden" features may not exist rather than merely eluding us—is a provocative reframing worth engaging with.
- The connection to the Cloud et al. "secret owls" subliminal learning study is clever and timely, providing a concrete case where the absence of semantically relevant intermediate features in training data is striking and demands explanation.
- The paper is well-organized and clearly written, with careful attention to defining desiderata for counterexamples (Section 2.1) and honest acknowledgment of the clay example's limitations as a special case.

## Weaknesses
### Fatal
None.

### Major
- **Insufficient engagement with empirical interpretability literature.** The paper's central thesis—that intermediate features correlating with output features may simply not exist—is directly contradicted by a large body of mechanistic interpretability work that has found specific, well-characterized intermediate features (e.g., circuits in vision transformers, induction heads in language models, feature visualization). The paper does not engage with this literature at all, which is a serious omission. If the claim is that this applies only to *some* cases, the paper needs to characterize which cases and how the empirical findings relate.
- **The clay-to-neural-network analogy is too loose.** Neural networks have discrete, enumerable intermediate states with fully known computational structure (weights, architecture, activation functions). Unlike clay, every intermediate activation is deterministically computed and its relationship to the output is, in principle, traceable through a known function. The paper does not adequately address why neural networks are relevantly similar to the clay case rather than to the many physical systems where intermediate causes *are* individuable. The author acknowledges this gap (footnote 15) but does not resolve it.
- **Equivocation on "feature" and "correlate."** The argument depends on a particular notion of "correlative continuity" that requires intermediate features to be the same *kind* of thing as the target feature, or to admit simple one-to-one mapping. But in the clay example, the shape of the clay at t2 is a specific, individuable state that deterministically produces a specific wobble frequency at t3. The paper dismisses this as merely "the overall form" without adequately arguing why shape doesn't count as a correlative feature. This definitional looseness weakens the core argument.

### Minor
- The paper's practical recommendations (Section 3) are somewhat vague. Claiming that "opacity" language should be revised without providing clear guidance on when ontological versus epistemic opacity applies limits the actionable value.
- The discussion of trust (Section 3.2) acknowledges that reframing opacity as ontological rather than epistemic may not change trust outcomes, somewhat undercutting the significance claim.

### Trivial
None.

## Nice-to-Haves
- A concrete neural network example (even a small one) demonstrating correlative discontinuity empirically would dramatically strengthen the paper.
- Discussion of how the paper's framework relates to the lottery ticket hypothesis, feature visualization, or circuit-level interpretability findings.

## Novel Insights
The paper's genuinely novel contribution is the philosophical argument that the "black box" metaphor in XAI may rest on a fallacious assumption—that causal continuity necessarily entails correlative continuity—and that what is perceived as "hidden" complexity in neural networks may, in some cases, reflect an ontological absence of individuable intermediate features rather than an epistemic limitation. This is a thought-provoking reframing, though its applicability to neural networks specifically remains underdeveloped.

## Suggestions
- Engage directly with the mechanistic interpretability literature (e.g., Olah et al.'s circuits work, Nanda et al.'s mechanistic interpretability) to address cases where intermediate features have been found, and characterize precisely when and why the author expects correlative discontinuity to hold in neural networks.
- Tighten the clay analogy by explicitly comparing the structural properties of clay (homogeneous, continuous, high-dimensional) with those of neural network layers (discrete, structured, known computation), and explain why the analogy holds despite these differences.

## Score and Decision
The paper makes an interesting philosophical argument about causation and neural network opacity, but it significantly underengages with the empirical interpretability literature that bears directly on its central thesis. The analogy from clay to neural networks is too loose, and the key terms ("feature," "correlate") are not sufficiently precise to make the argument fully convincing for an ML audience. As a philosophy paper it has merit; as an ICLR contribution, it needs much more empirical grounding and engagement with existing interpretability findings.

MY FINAL SCORE: <score>4</score>
MY FINAL DECISION: <decision>Reject</decision>