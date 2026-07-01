## Summary

This position paper argues that the "black box" metaphor for neural networks rests on an unwarranted philosophical assumption: that causal continuity (a past feature causing a present feature) necessarily implies *correlative* continuity (the existence of an individuable intermediate feature that correlates with the output). It offers a counterexample — a lump of clay whose past wobble causes a future wobble without any individuable "wobble feature" in the intermediate state — to show this necessity is false. The paper draws consequences for the "Secret Owls" phenomenon (Cloud et al., 2025), discussions of trust in AI, and the language of opacity more broadly.

---

## Strengths

- **Identifies a genuinely underexamined philosophical assumption.** The paper rightly calls attention to the fact that the "black box" metaphor carries an implicit ontological commitment — that there *must be* hidden intermediate features — and shows that this commitment is not forced by the causal structure of the system. Section 1.1 carefully distinguishes what-questions from why-questions, and Section 2 draws a clean conceptual distinction between causal continuity and correlative continuity.
- **The clay/wobble thought experiment (Section 2.2) is well-constructed.** It provides an intuitive case where causal continuity between a t₁ feature and a t₃ feature is unequivocal, yet there is no individuable feature at t₂ that non-trivially correlates with the t₃ wobble. As a philosophical device demonstrating that correlative continuity is not a necessary consequence of causal continuity, it is effective.
- **The paper is clearly written, logically structured, and well-situated in the relevant literature.** It engages with Chesterman (2021), Zerilli (2022), Dwivedi et al. (2023), Zednik (2021), Cloud et al. (2025), and others, and its core distinctions are properly contextualized.

---

## Weaknesses

### Fatal

None.

### Major

- **The paper's own concessions substantially limit its practical significance.** The paper explicitly states that phenomena defying correlative continuity "are rare" (line 99), that the clay example is "something of a special case" (line 119), and that reframing opacity as ontological rather than epistemic "may make no ultimate difference to the trust we do, or should, have in a system" (line 165). These are not minor hedging statements — they undermine the paper's central rhetorical framing as a debunking of a "myth." If the counterexamples are rare, and if correcting the fallacy changes little in practice, the paper's contribution is a narrow conceptual clarification rather than the revolutionary correction its title and framing suggest. The paper is internally consistent but its self-imposed bounds drain it of much of its intended force.

- **The paper does not adequately bridge the gap from the clay counterexample to neural networks.** The clay example works *because* the clay is largely homogeneous (line 131: "A lump of clay is largely homogeneous"). Neural networks are characterized by rich, high-dimensional internal differentiation: layer activations with thousands of dimensions, attention patterns with specific head specializations, weight matrices with organized sparsity. The paper acknowledges this difference (line 131: "If the brain were as homogeneous as clay, most efforts in cognitive neuroscience would never have progressed at all") but does not provide positive reasons to think that neural networks pattern with the homogeneous clay case rather than with the typical case where correlative continuity holds. The argument shows that correlative discontinuity is *possible*; it does not show it is *likely* for neural networks. More is needed to motivate the paper's central claim — that the "black box" framing is a "myth" — rather than the weaker conclusion that we should remain open to the possibility.

### Minor

- **The concept of "feature" is never adequately defined, and the argument's force depends on this.** The paper claims there is "no feature, or collection of features" in the intermediate state that correlates with the output, while conceding that the holistic form has structure and that properties of this structure are causally implicated (line 115). The question is: why doesn't the holistic form count as a "feature"? The paper appears to operate with an implicit constraint that features must be simple, nameable, easily individuable properties — but this is a definitional stipulation that does much of the argument's work. In neural network interpretability, the question is precisely whether complex, distributed patterns in intermediate activations are discoverable and interpretable at some level of analysis, not whether they reduce to simple labels like "wobble frequency."

- **The application to the "Secret Owls" case makes an empirical claim not settled by philosophical argument alone.** The paper states that "there is no finer-grained analysis of the data set's features available, to either humans or gods" (line 151). But whether the training data (lists of three-digit numbers) contains statistical structure that correlates with the owl disposition is an empirical question about Cloud et al.'s data, not a conceptual one. The paper partially hedges this in footnote 15 ("The experimental details in Cloud et al. are amenable to a rigorous demonstration… but to develop this argument effectively would require a paper of its own"), but the main text still asserts the stronger claim.

### Trivial

None.

---

## Nice-to-Haves

- The paper would benefit from engagement with mechanistic interpretability work (e.g., superposition, sparse autoencoders) that actively finds features in intermediate representations. Addressing this would force clarity on whether the claim is about *all* NN behaviors or only some, and under what conditions.
- A more modest framing — "a cautionary note about implicit assumptions" rather than "the myth of the box" — would better match what the argument actually supports and would strengthen the paper by preempting overclaim concerns.

---

## Removed Points

These points from the input review were removed (with brief justification):

1. **"Mischaracterizes the black box claim it targets"** — The paper explicitly engages with the Chesterman/Zerilli distinction between natural and complex opacity (Section 1.1). Whether the paper accurately represents the consensus is debatable, but it is not a clear mischaracterization. Removed.
2. **"Central analogy doesn't support the paper's conclusion"** (in the strong form) — This misreads the paper's argument structure. The paper uses the clay to disprove a *necessity* claim (modus tollens), not as a direct analogy. The criticism that the paper needs a positive bridge to NNs is kept as a Major weakness above; the claim that the analogy "doesn't work" is removed.
3. **"The Secret Owls case is question-begging"** (strong form) — The paper qualifies its claim (footnote 15, line 153: "nothing in the above argumentation guarantees that this is the *correct* explanation"). The weaker version — that the paper makes an empirical claim by philosophical argument — is kept as a Minor weakness.
4. **"Lacks engagement with mechanistic interpretability literature"** — Per policy, missing related works are not noted.

---

## Novel Insights

None beyond the paper's own contributions. The harsh critic's insights largely rephrase or push back on the paper's claims rather than adding new observations.

---

## Suggestions

1. **Reframe the contribution as a cautionary clarification rather than a debunking.** The paper's strongest form is: "We should not assume, for any given case of neural network opacity, that there exist intermediate individuable features. This assumption is not guaranteed by the causal structure of the system." The current title ("Myth of the Box") and framing ("fallacy") overreach relative to what the argument supports.
2. **Address the homogeneity gap explicitly.** Acknowledge that the clay example works because of homogeneity, and discuss what would need to be true about neural network computation for correlative discontinuity to arise there. This could be treated as an open empirical question.
3. **Clarify the definition of "feature."** Specify the criteria for what counts as an individuable feature versus a holistic property, or at least acknowledge the definitional dependence and how it interacts with the argument.
4. **Soften the empirical claim about Secret Owls.** Present it as a hypothesis or candidate explanation, not as an established implication of the philosophical argument.

---

## Score and Decision

**Calibration round 1 bracket:** 4.5–5.5

**Anchors retrieved:**
- *What Does it Mean for a Neural Network to Learn a "World Model"?* — avg 4.75, reject. Most similar paper: purely conceptual analysis with no experiments. The current paper has a tighter argument but similar issues about practical significance. (Round 1, band 2)
- *A Principled Evaluation Framework for Neuron Explanations* — avg 5.00, reject. Stronger empirical grounding but also a primarily conceptual contribution. (Round 1, band 3)
- *Is This the Subspace You Are Looking for?* — avg 6.33, accept. Clear formal definitions + experimental demonstrations + focused methodological target. Stronger than the current paper on all dimensions. (Round 2, band 2)
- *On the (un)interpretability of Ensembles* — avg 5.60, reject. Formal complexity analysis with a clear negative result. Comparable level of abstraction but more rigorous. (Round 2, band 2)
- *Deep Concept Removal* — avg 4.00, reject. Method paper with experiments; less relevant conceptually. (Round 1, band 1)
- *Complexity of Formal Explainability for Sequential Models* — avg 5.80, reject. Formal complexity results, stronger technical contribution. (Round 2, band 2)

**Narrowing:** The "World Model" paper (4.75) is the closest conceptual analogue and was rejected. The current paper is slightly stronger in execution (tighter argument, cleaner counterexample) but similarly limited by abstractness and lack of clear practical consequences. The "Subspace" paper (6.33, accepted) shows what a stronger conceptual critique paper looks like: formal definitions + empirical demonstrations. The current paper falls short of that bar. Final score anchored at 5.0.

The paper makes a genuine conceptual contribution — the distinction between causal and correlative continuity is worth drawing, and the clay counterexample is well-constructed. However, the practical significance is heavily qualified by the paper's own concessions, and the central gap between the counterexample and neural networks is not adequately addressed. The rhetorical framing overreaches relative to the argument. The contribution is real but narrow, insufficient for acceptance at a top venue.

MY FINAL SCORE: <score>5.0</score>
MY FINAL DECISION: <decision>Reject</decision>