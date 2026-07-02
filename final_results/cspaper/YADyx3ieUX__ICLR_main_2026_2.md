---
job_id: 0827cb28-ef52-40ff-a7be-90e9c48239fd
agent_id: ICLR_main_2026_2
status: COMPLETED
filename: YADyx3ieUX.pdf
paper: 
main_score_norm: 0.2
desk_reject: false
note: desk_rejection_enabled=false rerun
---
# Preliminary Observations:
The submission is primarily a conceptual/philosophical position paper about opacity, causation, and explanation in neural networks. It touches interpretability and causal reasoning, so it is not completely out of scope, but it does not present a machine learning method, benchmark, experiment, quantitative evaluation, figure, or table, which makes its fit to the ICLR main track relatively weak.

# Expected Review Outcome:
## Summary
This paper argues against a common way of understanding neural networks as “black boxes.” The central claim is that people often assume that if an output feature is causally produced by some earlier feature, then there must exist an intermediate feature in the system that can, at least in principle, be individuated as a correlate of that output; the paper argues this assumption is false. Using a potter’s clay analogy and a discussion of “subliminal learning” in LLMs from Cloud et al. (2025), the paper claims that in some neural-network cases the relevant internal correlates are not hidden but simply do not exist, and that this should reshape how we think about explainability, trust, and opacity in AI.

## Strengths
The paper has a clear, identifiable thesis, and it is not a generic “XAI is hard” essay. The target assumption, that causal continuity requires what the paper calls “correlative continuity,” is stated repeatedly and is easy to track across Sections 2 and 3.

The writing is generally readable and the examples are memorable. In particular, the contrast between the “secret owls” case on Pages 3 to 4 and the clay-wobble case in Section 2.2 on Pages 5 to 6 gives the manuscript a concrete argumentative backbone, rather than leaving it at the level of slogans about opacity.

The paper is also trying to contribute something broader than a narrow technical tweak. If the argument were made convincingly, it could matter for how interpretability claims are framed, especially in discussions that casually move from “we cannot identify the internal cause” to “there must be a hidden internal representation.” That is at least a meaningful conceptual target for the ICLR community.

I also appreciate that the manuscript does not claim to solve interpretability. Instead, it tries to reframe what kind of explanatory demand is legitimate. That is a more disciplined ambition than many purely conceptual submissions.

## Weaknesses
1. **The core claim is asserted far more strongly than it is established, especially when moved from the clay analogy to neural networks.**  
   The manuscript’s main argumentative work happens in Section 2.2, Pages 5 to 6, via the potter’s clay example. But this is an analogy, not an analysis of neural networks. The conclusion drawn on Page 8, namely that in some neural-network cases “the putatively hidden elements... do not exist,” is much stronger than what the clay story supports. At most, the example suggests that some systems may resist simple feature-level decomposition under a chosen explanatory vocabulary. It does **not** show that neural networks, which have explicit parameterized internal states, learned activations, and analyzable computational graphs, lack individuable intermediate correlates in the relevant sense. This matters because the whole paper is pitched as a claim about “neural network behavior,” not just about a philosophical possibility result.

2. **The key concepts are underdefined, and the formal notation gives an impression of precision that the paper does not actually supply.**  
   Across Pages 2 to 8, the paper uses notation such as \(f_j(x_i)\), \(f_j(y_i)\), and \(f_m(z_k)\), and repeatedly contrasts “causal continuity” with “correlative continuity.” But there is no formal definition of:
   - what counts as a “feature,”
   - what makes a feature “meaningfully” correlated,
   - what level of granularity is allowed for individuating an intermediate state,
   - whether “correlative continuity” means linear decodability, semantic interpretability, causal mediation, invariance under intervention, or something else.
   
   This is not a minor stylistic complaint. The paper’s strongest claims depend exactly on these distinctions. For example, on Page 6 the paper says that “nothing more fine-grained than ‘the state of the clay’ can be picked out at \(t_2\),” and on Page 7 it upgrades this to an ontological claim that “there are no individual features in the intermediary system-state... that are causes of the output feature.” Without a precise criterion for admissible feature maps \(f_j\), these claims are not checkable. If \(f\) can be arbitrarily rich, then the “no feature exists” claim is extremely hard to defend. If \(f\) is restricted to human-semantic or sparse concepts, that is a very different and much weaker thesis, but the paper does not clearly choose.

3. **The manuscript repeatedly jumps from epistemic difficulty to ontological impossibility without adequate argument.**  
   The boldest version appears in Section 2.3, Page 7: “The absence of such individuation... is not an epistemic limit, it is an ontological limit.” That is a major philosophical and scientific claim. Yet the support given is basically: the clay example feels like a case where no intermediate wobble-like feature is available. That is nowhere near enough to justify an ontological conclusion, especially when the paper itself acknowledges on Page 7 that many systems admit “varying degrees of relevant feature differentiation.” The leap from “we do not have a satisfying intermediate representation” to “there is none, even in principle” is exactly the sort of move that should require either a formal impossibility argument or an empirically grounded analysis of a class of models. The paper offers neither.

4. **The use of the Cloud et al. “secret owls” example is speculative and does not rule out more mundane explanations.**  
   Section 3.1 on Page 8 treats the owl-transmission case as a strong candidate for “discontinuous correlation.” But the paper itself admits, “nothing in the above argumentation guarantees that this is the correct explanation.” That concession is honest, but it also undercuts the force of the example. There is no analysis of alternative possibilities such as:
   - subtle statistical regularities in the number sequences,
   - distributional artifacts inherited from teacher sampling,
   - inductive biases of the student model that map these regularities into downstream traits,
   - representational structures that are not human-semantic but are still decodable or mechanistically traceable.
   
   In other words, the example is used rhetorically as though it points toward the paper’s thesis, but the paper does not actually investigate the internal representations of the student model or the training set structure. For a main-track ML venue, that is too thin.

5. **The paper does not engage the interpretability literature that most directly challenges its thesis.**  
   The manuscript cites broad XAI surveys such as Dwivedi et al. (2023) and Minh et al. (2022), but it does not seriously engage work aimed at recovering internal mechanisms, circuits, disentangled subspaces, or logic-level approximations of neural behavior. That gap matters because the paper’s main target is exactly the assumption that there must be intermediate correlates. If there is a live research program attempting to identify such correlates in practice, then the paper needs to explain whether:
   - those works are chasing something incoherent,
   - those works succeed only for some feature classes,
   - or those works produce useful approximations without answering the ontological question.
   
   As written, the submission mostly argues against a diffuse metaphor of “black-box opacity,” rather than against the strongest current versions of mechanistic interpretability and model analysis. The literature positioning is also incomplete on the philosophical side: there is no engagement with more systematic taxonomies of opacity in machine learning, which would be important for sharpening exactly which notion of opacity is being rejected.

6. **The analogy to homogeneous clay is a poor stand-in for modern neural networks.**  
   On Page 7, the paper explicitly emphasizes that the clay case is useful because the medium is relatively homogeneous. But this is also precisely why the analogy becomes weak for neural networks. A trained neural network is not just a “holistic form” in the same way as a lump of clay. It has:
   - structured layers,
   - explicit units and attention heads,
   - known computational topology,
   - parameter tensors that can be intervened on,
   - activations that can be decoded, ablated, and causally tested.
   
   So even if one accepts the clay case, it does not follow that the right explanatory unit for a neural network is equally holistic. The paper needs to explain why the presence of a structured computational graph does not already undermine the analogy. Right now, the transfer from clay dynamics to learned representations feels hand-wavy.

7. **The paper frames strong claims about explanation being “complete and without remainder,” but does not provide criteria for explanatory adequacy.**  
   The abstract already states that explanations can be “intrinsically partial, yet complete and without remainder.” This is catchy, but scientifically slippery. Complete with respect to what explanatory task? Local counterfactual explanation? Mechanistic mediation? Predictive sufficiency? Human interpretability? Regulatory accountability? The problem resurfaces on Page 8, where the manuscript says “The explanation is complete” for the owl case once one cites the dataset as the vehicle of causation. That is not obviously an explanation in the sense relevant to ML interpretability. It may identify a causal dependence at a coarse grain, but it does not answer the practical question that motivates much of XAI: what internal computation or learned structure made the behavior arise? Declaring completeness here feels like moving the goalposts.

8. **The manuscript is not methodologically matched to ICLR standards.**  
   This is the blunt part. The paper is written as a conceptual position paper, not as ML research in the usual sense. There are no experiments, no case studies on actual models beyond discussion of another paper, no formal results, no benchmarks, no figures, no tables, and no reproducibility content. A conceptual paper can still be publishable at ICLR if it is exceptionally sharp and deeply anchored in current ML practice. Here, however, the paper’s conceptual claims outpace its scientific grounding. For the main track, that is a serious limitation.

9. **Some claims about current consensus and the nature of opacity are overstated.**  
   On Page 2 the paper states that neural networks are “uniquely opaque” in an “in-principle” sense; on Page 3 it says there is “near consensus” about opacity with respect to causal antecedents of output features. These are broad sociological and conceptual claims, but the manuscript does not defend them carefully. In current ML research, there is a wide spectrum of positions ranging from local feature attribution, to concept bottlenecks, to circuit analysis, to causal abstraction. Treating the field as if it broadly shares a single background assumption makes the target easier than it should be.

10. **The paper would benefit from much more disciplined separation between causal claims and explanatory claims.**  
    The manuscript explicitly notes in Footnote 8 on Page 4 that the relation between causation and explanation is controversial, but then it proceeds as if distal causation plus holistic state description can settle explanatory adequacy. This is precisely where more precision is needed. If the claim is only that distal causal dependence can exist without neatly individuable intermediate semantic features, that is plausible. If the claim is that this makes the black-box metaphor a “myth,” that is much less plausible. The paper currently slides between these levels.

## Questions
1. Can the authors provide a precise definition of “correlative continuity”? In particular, what is the admissible class of intermediate features \(f_j\)? Are these intended to be human-semantic features, sparse latent variables, linear probes, arbitrary measurable functions of the system state, or causally isolatable mediators? My assessment would improve substantially if this were pinned down formally.

2. What concrete prediction does the thesis make for neural-network analysis that differs from standard mechanistic interpretability? For example, is there a testable criterion under which one should expect that no intermediate representation of a target behavior can be individuated, even in principle?

3. For the Cloud et al. case discussed in Section 3.1, what evidence would distinguish the paper’s preferred explanation from a more standard view in which some non-semantic but still structured correlates do exist in the training data or learned parameters? Right now the argument seems underdetermined by the example.

4. Can the authors engage more directly with interpretability work that tries to recover internal circuits, concepts, or subspaces in real models? Even if the authors disagree with those programs, a serious confrontation with them is necessary, since they are the strongest empirical counterpressure to the paper’s thesis.

5. The clay example on Pages 5 to 7 is doing nearly all the heavy lifting. Can the authors offer at least one neural-network-specific case study, even qualitative, where they analyze the internal state and argue why the best interpretation is genuinely “no individuable correlate exists,” rather than merely “we have not found one yet”?

6. The manuscript often says the resulting explanation is “complete.” Complete for which notion of explanation? Please clarify whether completeness is meant in a causal, predictive, semantic, mechanistic, or normative sense.

## Flag For Ethics Review
- No ethics review needed.

## Details Of Ethics Concerns
No specific ethics concerns beyond standard downstream interpretability/trust discussions are raised by the submission itself.

## Soundness Rating
1: poor. The central claims are not adequately supported by formal argument, empirical evidence, or ML-specific analysis, and several strong ontological conclusions go well beyond what the provided examples justify.

## Presentation Rating
2: fair. The prose is readable and the argumentative structure is easy to follow, but the conceptual vocabulary is underdefined, the literature positioning is incomplete, and the paper does not present the level of scientific grounding expected for ICLR.

## Contribution Rating
1: poor. The paper has an interesting conceptual intuition, but in its current form it does not make a sufficiently substantiated or well-positioned contribution to machine learning research.

## Overall Rating
2: Reject, not good enough. The paper raises an interesting philosophical challenge to how “black box” language is used in ML, but the submission is too speculative and insufficiently grounded in neural-network analysis to meet ICLR main-track standards.

## Reviewer Confidence
4: confident. I am confident in the assessment of the paper’s positioning relative to interpretability/XAI work and in the judgment that the claims are under-supported for an ML venue, though the paper’s philosophical background is broader than my core technical specialization.