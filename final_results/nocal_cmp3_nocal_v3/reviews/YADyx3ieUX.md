Here is my final consolidated review:

---

## Summary

This paper argues that a widespread assumption underlying "black box" discourse in XAI — namely, that causal continuity across a system guarantees correlative continuity (i.e., that if feature A distally causes feature C, there must exist individuable intermediate features in the system that correlate with both A and C) — is not a necessary truth. The paper provides a counterexample from a physical system (a wobbling clay pot, where the wobble at t₁ and t₃ are causally continuous but no individuable feature at t₂ correlates with the wobble frequency beyond "the whole state of the clay"). It then argues that this assumption, found to be non-necessary, underlies the way neural network "opacity" is characterized, and traces three consequences: (1) the "subliminal learning" case of Cloud et al. (2025), where student models inherit teacher dispositions via semantically sterile data, may genuinely lack hidden intermediate features; (2) trust discussions should be reconfigured accordingly; (3) the language of opacity itself should be reconsidered.

## Strengths

- **A genuine counterexample to a widely implicit assumption.** The clay/wobble case (Section 2.2) is the paper's strongest constructive contribution. It succeeds on its own terms: it is a real-world-like case where a distal cause (wobble at t₁) and its effect (wobble at t₃) are linked by a continuous causal process, yet no intermediate feature at t₂ can be individuated as a correlate of the oscillation frequency beyond "the whole state of the clay." This demonstrates that the causal-continuity-entails-correlative-continuity thesis is not a necessary truth, which is a real conceptual observation worth making.

- **Intellectual honesty about limitations.** The paper repeatedly and explicitly concedes that (a) correlative discontinuity is rare (Section 2.3), (b) the clay example is "something of a special case" (line 119), (c) the degree of correlative continuity is feature-dependent and system-dependent (line 133), (d) the owls example is "high-level" causation and falls short of one of its own desiderata (Footnote 14). This candor enables clear evaluation of what the argument does and does not claim.

- **Clear and engaging prose.** The paper structures its argument in a well-signposted way, uses philosophical terminology precisely, and orders its three consequences from concrete to abstract effectively.

## Weaknesses

### Major

None.

### Minor

- **The notion of "feature" is used imprecisely across the argument.** The paper uses "feature" to refer to: (a) a property of a distal cause (the clay's wobble frequency), (b) the absence of an individuable intermediate correlate ("the whole state of the clay"), (c) semantic properties like "owl meaning" in the training data, and (d) activations or parameters in neural networks. The argument's cogency depends on a consistent notion of what counts as a "correlative feature" — i.e., a property of the system at the intermediate state that can be individuated, extracted from the full system state, and identified as a causal correlate of the output feature of interest. Without explicit criteria for what individuability requires, the reader cannot fully evaluate whether the clay case and the neural network case are being judged by the same standard. The paper's central claim — that some intermediate features "do not exist" — would benefit from specifying *what must be true of a system for a feature to exist as a correlate*. This does not invalidate the argument but would sharpen it considerably.

- **The owls example is presented as a stronger illustration than the evidence supports.** The paper states: "There is no feature of the set that 'means' 'owl', that correlates to a disposition toward owl behaviors, or is an 'encoding' of a love of owls" (line 151). This conflates semantic meaning with causal/statistical correlation. The training data has quantifiable statistical properties (n-gram distributions, positional patterns, digit frequencies) that could correlate with the teacher's owl-related tendencies — such correlation does not require the data to "mean" owl. The paper later hedges that this is a "candidate explanation" and not guaranteed (line 153), but the categorical claim ("no feature... correlates") goes further than the hedging allows. The example would be stronger if it acknowledged that the empirical question is whether *any* statistical feature of the training data predicts owl-related outputs, not whether any *semantic* feature "means" owl.

- **The trust section concedes limited practical impact.** The paper honestly notes that "reframing the same limits as ontological rather than epistemic makes no ultimate difference to the trust we do, or should, have in a system" (line 165). This is an honest concession, but it leaves the reader wondering what the argument actually *changes* about practical engagement with neural networks. The paper's significance would be clearer if it could identify concrete downstream consequences beyond linguistic revision.

### Trivial

None.

## Nice-to-Haves

- The paper could more explicitly address the disanalogy between the clay (a largely homogeneous medium) and neural networks (which have rich compositional structure at intermediate layers). The paper acknowledges clay's homogeneity (line 131) but never directly says: "neural networks are not homogeneous like clay, yet the conceptual point still applies because..." Making this step explicit would preempt the central objection likely readers will raise. The key argument is that the *existence of structured components* does not guarantee that, for any given output feature, some component or combination of components constitutes a *correlative feature* of that specific output. Making this reasoning explicit would strengthen the paper.
- The paper could expand Footnote 12's Maxwell's-demon point to clarify that the distinction between "the full state contains predictive information" and "some feature of the state correlates with the output feature" is the crux of its argument, not an evasion.

## Removed Points

- **"The central argument equivocates on what counts as a 'feature,' and this equivocation is fatal."** This criticism misreads the paper. The paper does not claim neural networks are homogeneous like clay, nor does it need to. Its argument structure is: (a) the assumption that causal continuity entails correlative continuity is not a necessary truth (proven by clay counterexample); (b) XAI opacity discourse relies on this assumption; (c) therefore the assumption should be reconsidered in neural network contexts. The paper explicitly says the claim applies to "at least some cases" (line 145), is "feature-dependent, not merely system-dependent" (line 133), and addresses the "omniscient god" objection directly (Footnote 12). The criticism that "an omniscient god could trivially read them off" the activation vectors is exactly the position the paper anticipates and addresses: the existence of activations does not guarantee that any *feature* of that activation vector correlates with the specific output feature of interest in an explanatorily relevant way.

- **"The paper does not engage with mechanistic interpretability."** Per the applicable rule, missing related works are not raised here. (This would be more appropriate as a scope-of-review judgment by someone with full knowledge of the literature.)

- **"The paper's conclusion conflicts with its own stated position on interpretability research."** This is a misunderstanding. The paper does not claim that *no* intermediate features exist; it claims that for *some* output features, there may be no intermediate features that correlate with them. Studying which features do or do not correlate is perfectly consistent with this claim, as the paper states at line 173.

- **"The photic-sneeze example cuts against the paper's argument."** The paper explicitly grants that most systems exhibit correlative continuity and uses the sneeze case as a contrast to show where we *should* expect correlates. This is consistent with the paper's thesis, not a contradiction.

- **"The Section 1.1 framing of in-principle opacity is accepted uncritically."** This is a normal practice for a position paper citing philosophical sources on its framing assumptions. Minor and not central to the argument.

- **Various format/style criticisms, reproducibility nitpicks, and generic "evaluation lacks rigor" concerns.** These are not present in the reviewed paper.

## Novel Insights

None beyond the paper's own contributions. The reviews do not surface a genuinely novel perspective on the paper's thesis that the paper itself does not already contain or imply.

## Suggestions

1. **Define "feature" explicitly.** Specify what criteria a system property must satisfy to count as a "correlative feature" of an output feature (individuability? decomposability? invariance across contexts?). This single clarification would resolve the paper's main vulnerability.
2. **Acknowledge the structural disanalogy between clay and neural networks directly and explain why it does not matter.** A one-paragraph passage saying "Neural networks are not homogeneous like clay, but the existence of structured components does not guarantee that for any given output feature there exists a correlating component" would preempt the most common objection.
3. **Soften the owls claim.** Replace "There is no feature of the set that... correlates to a disposition toward owl behaviors" with the more qualified claim that such correlation is not guaranteed a priori and that correlative discontinuity is a serious candidate explanation worth investigating.
4. **Identify at least one non-linguistic practical consequence.** If the only thing that changes is removing a word ("opacity") from our vocabulary while all methods, goals, and trust considerations remain the same, the argument's significance is limited. Even one concrete implication would help.

## Score and Decision

<score>6</score>
<decision>Borderline Accept</decision>