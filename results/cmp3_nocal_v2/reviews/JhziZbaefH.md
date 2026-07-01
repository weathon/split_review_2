## Summary

This paper proposes OML, a brain-inspired hierarchical neural architecture for online multimodal learning. The network features modular ascending/descending/lateral pathways, a reference extraction mechanism (using coefficient of variation across repeated exposures to identify which feature dimensions a word refers to), and conflict detection with human-in-the-loop question-asking. The method is evaluated on small fruit-image datasets (Fruits, HomeF) with Chinese audio, in both close (random) and open (sequential) environments, showing consistent improvement over existing online methods (ART, AEN) and competitive results against offline methods that are not designed for continual learning.

## Strengths

1. **The reference extraction idea is genuinely novel and well-motivated.** The coefficient-of-variation approach in Section 3.4 — using the observation that dimensions a word refers to should have shrinking variance across repeated exposures — is a clean statistical intuition that is clearly grounded in the problem. The paper illustrates this concretely with the "red" example (onions vs. apples), where color features stabilize while shape features vary.

2. **The architecture designs for online multimodal learning are non-trivial and contribute beyond existing methods.** The hierarchical modular structure with ascending, descending, and lateral pathways (Section 3, Figures 2–3) provides a mechanistic architecture for continual multimodal binding that goes beyond the simpler ART-based approaches. The modal extension experiment (Table 3, adding a taste channel) demonstrates a genuinely useful capability — reusing a trained network with a new modality — that only one prior method (AEN) supports.

3. **Consistent empirical improvement over online baselines across all settings.** In all four datasets and both close/open environments, OML outperforms the other online methods (ART, AEN). The margins are modest (roughly 3–5 points in the open environment) but consistent across all 16 comparisons in Tables 1–3, which suggests a reliable advantage rather than noise.

## Weaknesses

### Fatal
None.

### Major

1. **The human-in-the-loop capability — listed as a core contribution — is not empirically evaluated.** Attribute (2) in the introduction states the model "can detect conflict between the current input and the learned ones. If a conflict occurs, it can ask the user appropriate questions and conduct learning based on user's answer." Yet the experiments bypass the human entirely: "if the question posed to the user by OLM remains unanswered for a certain period of time, we set the answer to be positive" (Section 4, final paragraph). The only evidence offered is a single unsupported claim: "when we randomly add 10% of word-image or word-taste data pairs with incorrect matches, OML is able to detect all conflicts and raise appropriate questions" (Section 4.1, point 3). No methodology, detection rates, false positive rates, or question-quality measures are provided. This contribution is effectively unvalidated.

2. **No ablation study.** The proposed architecture combines multiple novel components — the frequency-based activation (Eq. 1), Fourier-transformed routing at MANs (Eq. 6), lateral connections between FNs, reference extraction (Eq. 7), and conflict detection with question-asking. Without ablation experiments that remove or simplify individual components, it is impossible to determine which design choices drive the observed performance. This is a significant gap for a systems paper with a multi-component architecture.

### Minor

3. **Reference extraction is evaluated only indirectly, with no direct measurement of whether the mechanism correctly identifies referring dimensions.** Table 2 evaluates the downstream retrieval task, not the reference extraction itself. The paper generously scores baselines as "correct" even when they return irrelevant features (Section 4.1, point 2: "they return all features (shape and color)... we count this as a correct result for them"). While this generosity actually makes OML's win harder (not easier), a direct evaluation — precision/recall of dimension selection — would be far more informative. An ablation comparing OML with and without reference extraction would also clarify how much the mechanism contributes.

4. **No variance or statistical significance reporting.** Across all three tables, not a single standard deviation, confidence interval, or significance test is reported. Given the small custom datasets and modest margins over the closest competitor (e.g., 3–4 points), the reader cannot assess whether the reported differences are reliable or within noise.

5. **Missing dataset statistics.** The paper describes the datasets only by name and source (Fruits from Xing et al. 2019; HomeF from Lai et al. 2011). Number of classes, samples per class, total images/audio clips, and the size of the added color-word vocabulary for E-Fruits/E-HomeF are all absent, making it difficult to assess the scale and difficulty of the evaluation.

6. **Several design choices are opaque and lack justification.** (a) The parameter *T* in Eq. (1) is described as not affecting the algorithm, raising the question of why it appears in the activation function. (b) The Fourier transform in Eq. (6) and frequency-based routing (λ parameter) are central to how signals find correct pathways, but no ablation or analysis clarifies whether this complexity is warranted over simpler attention or gating mechanisms. (c) The "X channel" appears in Figure 2 and is mentioned once (Section 3) as receiving descending pathways but its purpose is never defined. (d) The learning rules in Section 3.5 are described only for the two-modality (vision+audition) case; generalizing beyond this is left unspecified.

### Trivial
- The claim that all designs make the method "learn like the way humans do" (Abstract) is an overstatement unsupported by experiments on a handful of fruit categories with two modalities.
- No discussion of limitations or failure cases in the conclusion.

## Nice-to-Haves
- **Standard multimodal benchmarks.** While the custom datasets are appropriate for online learning (where standard benchmarks like MS-COCO assume offline training), evaluation on a benchmark that supports continual learning protocols would improve generality.
- **Sensitivity analysis** for key hyperparameters (θ threshold, *r* threshold for reference extraction, ϑ probability threshold).
- **Discussion of scaling behavior** with vocabulary size and number of conflicting concepts.

## Removed Points
These points were raised in the input review but are not included as weaknesses after verification:
- **"Open-environment comparison against offline methods is structurally unfair."** The paper clearly labels offline vs. online methods, and it is standard practice in continual learning work to include offline baselines to demonstrate catastrophic forgetting. The reader can see the comparison against online methods in the same tables. The margins against online methods (3–5 points) are visible and not inflated by the offline inclusion.
- **"Reference extraction evaluation inflates baseline accuracy and makes OML look better."** The paper explicitly states that baselines returning ALL features (shape + color) are counted as correct. This generosity toward baselines makes OML's superior performance *more* convincing, not less. The underlying point about missing direct evaluation/ablation is kept as Minor weakness #3.
- **"No evaluation on standard multimodal benchmarks."** Standard benchmarks (MS-COCO, Flickr30K) are designed for offline training and do not typically support the online continual-learning protocols that are the paper's focus. This is scope creep.
- **Typos (e.g., "OLM" instead of "OML") and formatting issues.** These are parser artifacts or minor errors that do not affect evaluation.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. **Evaluate the human-in-the-loop component.** Even a basic simulated-user experiment would transform this weakness: inject incorrect or conflicting data at known rates, report conflict detection true positive rate / false positive rate, and evaluate whether the generated questions target the correct source of conflict. Without this, attribute (2) remains an unsupported claim.

2. **Add an ablation study.** The architecture has several novel components (frequency-based activation, Fourier routing, lateral connections, reference extraction, conflict detection). Ablating each component (or at minimum: removing reference extraction, replacing Fourier routing with a simpler gating mechanism) would clarify which designs drive performance.

3. **Directly evaluate reference extraction.** Report whether the mechanism correctly identifies the referring feature dimensions (e.g., precision and recall of dimension selection). This is a stronger signal than the current indirect downstream evaluation.

4. **Report variance.** Even basic bootstrapped confidence intervals or standard deviations across runs would substantially improve credibility, especially given the modest margins over AEN.

5. **Provide dataset statistics.** Include class counts, sample counts, and vocabulary sizes for all datasets.

## Score and Decision

**Score:** 4.0 — The paper proposes a genuinely novel architecture and an interesting reference extraction mechanism, with consistent empirical improvements over online baselines. However, one of its two stated core contributions (human-in-the-loop interaction) is not evaluated, the multi-component architecture lacks any ablation analysis, and several design choices are opaque without justification. These gaps prevent the paper from being accepted in its current form.

MY FINAL SCORE: <score>4.0</score>
MY FINAL DECISION: <decision>Reject</decision>