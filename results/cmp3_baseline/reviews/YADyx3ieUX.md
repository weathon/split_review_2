## Summary

This is a philosophical critique of the "black box" metaphor for neural networks. The author argues that the common assumption that causal continuity in a system requires "correlative continuity" (i.e., the existence of individuable intermediate features that correspond to the distal cause and effect) is a fallacy. Using a clay-wobble example and the "secret owls" LLM study (Cloud et al., 2025), the paper contends that in some complex, nonlinear systems, intermediate causal features may not exist even in principle; consequently, neural network opacity is not about hidden information but about the absence of such features. The paper discusses conceptual consequences for explainable AI, trust, and the language of opacity.

## Strengths

- **Clear, well-structured philosophical argument.** The paper is lucidly written, with a careful progression from the clay counterexample to neural network contexts. The logical steps are easy to follow, even for readers not steeped in philosophy of causation.
- **Identifies a genuine, often-implicit assumption.** Many discussions of black-box AI tacitly assume that there *must* be some intermediate internal features that correspond to output features, even if they are incomprehensible. The paper usefully challenges this assumption and makes the case that it should not be taken for granted.
- **Engages with a striking recent empirical finding.** The "subliminal learning" (secret owls) study provides a concrete, provocative case that seems to exemplify the kind of causal discontinuity the author describes. Using this example anchors the abstract argument in real experimental results.

## Weaknesses

### Fatal

- **The core argument does not convincingly transfer from the clay example to neural networks, and the central conclusion ("the box is a myth") is not adequately supported.** The clay example relies on the near-homogeneity of a lump of clay at rest: there genuinely are no discernible subfeatures that "encode" the oscillation frequency. But neural networks, by construction, have richly structured intermediate representations (activations over many neurons). Even if individual features are not easily interpretable, there is strong empirical (and theoretical) reason to believe that *some* pattern of activations correlates with output features—this is precisely what mechanistic interpretability methods attempt to recover. The paper asserts that "in at least some of these cases the putatively hidden elements ... do not exist" (Section 3), but provides no proof that neural network internal states lack such features. The "secret owls" example is offered as a candidate, yet the author repeatedly admits ("nothing in the above argumentation guarantees that this is the *correct* explanation"). Without a concrete demonstration that a neural network's intermediate activations indeed contain no correlative features for a given output, the argument remains a suggestive philosophical possibility rather than a substantiated claim.

### Major

- **The definition of "correlative continuity" is too vague to sustain the argument.** The paper requires that intermediate features "meaningfully correlate" or "intelligibly correspond" to the distal cause and effect (Section 2). But what counts as "meaningful" or "intelligible"? If the requirement is that features be human-interpretable, then the paper merely restates the known difficulty of interpretability. If the requirement is ontological (that no subset of the system state correlates at all with the output feature), then the burden of proof is enormous and unfulfilled. The clay example may satisfy the ontological claim, but no evidence is given that any neural network state does.
- **The paper does not engage with the extensive mechanistic interpretability literature.** There is a large body of work showing that features in neural networks can often be identified (e.g., neurons or directions in activation space that correspond to specific concepts). The paper cites only a few review papers. A thorough discussion of why these findings are not evidence for correlative continuity, or how the author's thesis accommodates them, is missing.
- **The practical implications are underdeveloped.** The section on trust (3.2) notes that the removal of the "box" may or may not affect existing trust arguments, but essentially punts on the issue. The section on language (3.3) argues for conceptual revision but offers no concrete guidance for researchers or practitioners. The paper's contribution is primarily negative (critique) without a positive framework for how to analyze neural network behavior in light of its thesis.

### Minor

- The claim that the earlier wobble is "distally causally responsible" for the later wobble in the clay example is plausible but not formally justified; the example relies on intuition. A more rigorous causal model would strengthen the case.
- The paper occasionally conflates "causation" and "explanation" despite stating that it aims to remain neutral on the relationship between them. Some readers may find the ambiguity problematic.

### Trivial

- The "secret owls" paper is from the future (2025) relative to the review process; this does not affect the evaluation, but it is worth noting that the example cannot be independently verified at the time of review.

## Nice-to-Haves

- A concrete experiment or simulation demonstrating a neural network case where mechanistic interpretability methods fail *not because of complexity but because there is nothing to find* would dramatically strengthen the argument. Even a toy network designed to exhibit such holism would be valuable.
- A deeper discussion of how this thesis interacts with existing causal abstraction or intervention-based interpretability methods would help situate the contribution within the XAI community.

## Novel Insights

The paper's genuinely novel insight is that the "black box" metaphor carries an unwarranted ontological commitment: it presupposes hidden *features* that are merely inaccessible. The clay example provides an intuitive case where the metaphor fails, and the author correctly notes that such failures could occur in neural networks as well. This is a useful conceptual warning against reifying hidden representations as "encoded" causes. Beyond this cautionary note, the paper does not produce a new method, result, or framework that moves the field forward empirically or theoretically.

## Suggestions

- Strengthen the argument by focusing on a single, well-defined neural network task (e.g., the owls scenario) and attempt to show either by analysis or by construction that no intermediate feature set correlates with the target output. Without such demonstration, the paper remains a philosophical possibility rather than an actionable critique.
- Clarify the definition of "correlative continuity" and distinguish between "ontological absence" and "epistemic inaccessibility" more sharply. Acknowledging that even in the clay example a god could predict the wobble from the t2 state (just not identify a *feature*) would help clarify what is being denied.
- Engage with specific interpretability works (e.g., probing, activation patching, sparse autoencoders) to explain why their successes are compatible with the thesis or why they are misleading.

## Score and Decision

Score: 4 — borderline reject.

The paper is thought-provoking and well-written, but its central thesis is insufficiently supported for a top empirical ML venue. The argument does not convincingly demonstrate that neural networks ever lack correlative intermediate features, and the consequences drawn are too tentative to guide research or practice. The contribution is primarily conceptual critique, which may be better suited to a workshop or a philosophy-of-science journal.

MY FINAL SCORE: <score>4</score>  
MY FINAL DECISION: Reject