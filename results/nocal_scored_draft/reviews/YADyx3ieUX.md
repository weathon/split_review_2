The favorability scores confirm that the strengths are strong and the weaknesses are minor. Let me now produce the final review.

## Summary

This position paper argues that the "black box" characterization of neural networks rests on an unjustified assumption: that causal continuity across a system (A causes B through some causal chain) necessarily implies *correlative* continuity (the existence of intermediate features that meaningfully correlate with the output feature). The paper provides a compelling counterexample (a clay/wobble scenario where causation runs continuously but no intermediate feature-level correlate of the wobble exists), draws a clean philosophical distinction, and applies this to a recent "subliminal owls" study and three general consequences for interpretability discourse.

## Strengths

- **A genuinely non-obvious philosophical distinction is drawn clearly.** The paper carefully distinguishes causal continuity from correlative continuity (Section 2). This distinction is real, usefully applied to a domain where it has been overlooked, and articulated with precision. The paper shows that while these two types of continuity typically coincide, their co-occurrence is contingent, not necessary.

- **The clay/wobble counterexample (Section 2.2) is compelling within its own domain.** It provides an intuitive physical case where a distal wobble causes a later wobble, but the stationary clay at t₂ has no feature-level correlate of the oscillation frequency — only a holistic state that carries the causation forward. This cleanly demonstrates that correlative continuity is not a conceptually required consequence of causal continuity.

- **The paper is clearly written and logically structured.** The prose is accessible, the argument flows from abstract philosophical claim → concrete counterexample → application to neural networks → consequences, and the writing makes a subtle conceptual argument approachable for an ICLR audience without oversimplifying.

## Weaknesses

### Fatal

None.

### Major

None.

### Minor

- **Rhetorical overreach in the conclusion.** The paper's core argument is a deflationary philosophical point: the assumption that causal continuity implies correlative continuity is a fallacy, so we should not assume intermediate features must exist. The closing language ("this ubiquitous box is mere myth," "opacity... is no opacity at all," line 171) reads as claiming a stronger positive result — that intermediate features *do not exist* in neural networks. The paper's own caveats (line 133: "cannot be assumed in advance"; line 153: "nothing in the above argumentation guarantees that this is the correct explanation") are in tension with this framing. The paper would be more credible if it consistently presented itself as making a methodological caution about an unjustified assumption rather than a positive ontological discovery about neural network architecture.

- **The ontological-vs-epistemic distinction is applied to neural networks without sufficient justification.** The paper convincingly argues that the absence of correlatively continuous features in the clay is an ontological limit, not an epistemic one (line 129). But when this framing carries into the neural network discussion (Section 3), the paper does not provide analogous justification for why the limit would be ontological rather than epistemic there. For neural networks — which have richly structured, high-dimensional internal representations — the question of whether features are absent (ontological) or merely undiscovered (epistemic) is substantive, and the paper's core argument about an assumption being a fallacy does not by itself answer it.

### Trivial

- **The presentation of the owls example (Section 3.1) oscillates between declarative assertion and hedging.** The paper states "There is no feature of the set that 'means' 'owl'" (line 151) as if settled, but immediately acknowledges "nothing in the above argumentation guarantees that this is the correct explanation" (line 153) and Footnote 15 concedes that a rigorous demonstration "would require a paper of its own." This fluctuation risks misleading readers about what the argument establishes. Making the hedging more prominent in the main text would better align presentation with substance.

## Nice-to-Haves

- The paper could sharpen what "meaningfully correlate" means in operational terms for neural networks. The definition (line 77: features that "meaningfully correlate" with the target feature) is clear enough for the clay example, but operationalizing it for neural network representations (e.g., does a logit lens probe count? a circuit found by activation patching?) would strengthen the paper's relevance to technical audiences.

- The paper could more explicitly acknowledge that some types of neural network behaviors may be fully amenable to feature-level analysis, while others may not be — and that distinguishing these is itself an important research question.

## Removed Points

These points are flagged to be removed; treat them with caution:

- Removed criticism about the central analogy not being adequately defended: The paper does not claim neural networks ARE like clay. It makes a logical argument: the assumption of universal correlative continuity is false (shown by the clay counterexample), therefore we should not assume it holds in neural networks. The paper explicitly acknowledges the clay is "a special case" (line 119) and that the degree of correlative continuity "will not be binary" (line 131). The critic's framing mischaracterizes the paper's inferential structure.

- Removed criticism about missing engagement with mechanistic interpretability literature: Per hard rule, do not mention missing related works.

- Removed criticism about Section 1.2 being thin on technical literature: Generic scope-creep criticism of a position paper's literature review that does not anchor to a specific concrete problem.

- Removed criticism about Section 3.2 conceding trust implications may be unchanged: The section is honestly delineating the implications of the argument, not undermining it.

- Removed strength about the paper not over-reaching in its philosophical core: This conflicts with a verified weakness about rhetorical overreach in the conclusion.

## Novel Insights

None beyond the paper's own contributions. The review's main observation — that the paper's rhetorical framing sometimes outruns what its argument strictly supports — is a common pattern in position papers and not a novel insight specific to this paper.

## Suggestions

- Recast the concluding section (3.3) to more carefully distinguish between the deflationary claim ("we cannot assume intermediate features must exist") and the stronger claim ("intermediate features do not exist") which the argument does not support.

- Add a discussion of how the ontological-vs-epistemic distinction applies to neural networks specifically. For the clay example the case is intuitive; for neural networks it requires additional justification given their structured, high-dimensional representations.

- Move the key hedging about the owls example from Footnote 15 into the main text to prevent misinterpretation.

## Score and Decision

The paper makes a genuine and non-trivial conceptual contribution: it identifies a subtle fallacy embedded in how we talk about neural network opacity and provides a clean counterexample to demonstrate it. The weaknesses are about rhetorical presentation and insufficiently-justified extension to neural networks, not about the core philosophical argument being wrong or irrelevant. For a position paper at ICLR, this is a solid contribution that warrants publication with minor revisions to align the rhetoric with what the argument actually supports.

MY FINAL SCORE: <score>8</score>
MY FINAL DECISION: <decision>Accept</decision>