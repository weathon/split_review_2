## Summary
The paper proposes a new mechanistic interpretability method for gated neurons (SwiGLU, GeGLU) based on cosine similarities between their input, gate, and output weight vectors. Using this weight-based lens, it defines a taxonomy of read-write (RW) functionalities (e.g., strengthening, weakening, conditional) and discovers a small class—“weakening” neurons—that activate very often, have outsized influence on model behavior, and whose effect partly arises from negative gate values, challenging the common view that negative Swish values are only a training artefact.

## Strengths
- **Novel perspective on gated neurons.** While weight cosine similarities have been computed before (e.g., Gurnee et al. 2024), this paper is the first to systematically interpret them as “read-write” functionality for gated activation functions, leading to a clear taxonomy.
- **Discovery of weakening neurons and their surprising properties.** The finding that a tiny class of neurons (weakening) has disproportionately large effects on attribute rate and output entropy is genuinely unexpected and opens new research questions.
- **Universality across many LLMs.** The pattern of strengthening-dominant early layers and weakening-dominant late layers is shown to hold across 12 models of different families and sizes, giving the empirical finding strong generality.
- **Conditional ablation method.** The idea to ablate only activations satisfying specific sign conditions on gate and input is elegant and reveals that negative gate values (Swish < 0) are mechanistically important—a concrete contribution to interpretability methodology.
- **Clear exposition.** The paper is well structured, the taxonomy is explained intuitively, and the key figures (especially the layer-wise cosine trend and the ablation results) vividly convey the main insights.

## Weaknesses
### Major
- **Limited experimental scope for causal claims.** All ablation experiments (Sections 6–8) are performed on a single model (OLMo-7B) with one dataset subset (20M Dolma tokens). While the authors cite resource constraints, the claim that “weakening neurons have the highest effect on metrics” needs to be validated on at least one other model to rule out model-specific artifacts. The universal weight-pattern results (Section 5) do not automatically guarantee universal behavioral importance.
- **The preprocessing step (multiplying win and wout by sign of cos(wgate, win)) is not fully justified in the main text.** The argument that it “does not change model behavior” may be formally correct, but it changes the geometric relationship between the weight vectors and thus directly affects the cosine-based classification. Without seeing the Appendix (Section C), the reader cannot assess whether this step might artificially create or destroy certain categories.
- **Arbitrariness of threshold-based classification.** The taxonomy uses a fixed threshold τ=±0.5 to assign categories. While the paper also shows continuous distributions, all quantitative breakdowns (Fig. 1b) and ablation experiments rely on the thresholded categories. The results may be sensitive to the choice of threshold; a sensitivity analysis is missing.

### Minor
- **The case study of a weakening neuron (Section 8) is inconclusive.** The interpretation is described as “much harder to interpret” and the most interpretable examples come from the negative-gate case, but the overall qualitative analysis does not convincingly demonstrate that the RW perspective yields new understanding beyond existing methods (projection to vocab space, activation maximization).
- **The term “read-write functionality” is somewhat overloaded.** The paper uses “read” for the dot products with gate/input weights and “write” for the output weight direction, but does not address how multiple neurons interact (superposition). The limitation is acknowledged, but the strong claims about “understanding mechanisms” should be tempered.
- **Absence of any counterfactual tests on the importance of the gate weight itself.** The method symmetrically treats wgate and win for reading, but the gating mechanism is the distinguishing feature of SwiGLU. An ablation study that compares the effect of removing wgate vs. win would strengthen the argument that the taxonomy captures meaningful behavior.

### Trivial
- The y-axis label in Figure 1(a) is cut off (“cos(w\_in, w\_out)” vs. full notation used in text).

## Nice-to-Haves
- Validate the ablation results on at least one other model (e.g., Llama-3.2-3B) to confirm that weakening neurons are consistently influential.
- Provide a sensitivity analysis of the classification to the cosine threshold (±0.5 or other values).
- Show random baselines for the attribute rate metric in the same plot to help gauge effect size.

## Novel Insights
The paper’s most novel insight is that negative Swish gate values, long assumed to be only a byproduct of smooth activation design, have measurable mechanistic effects on model output—specifically, they can flip a “weakening” neuron into a “strengthening” neuron, sharpening the output distribution. This reframes Swish as a functional component, not just a training convenience, and suggests that interpretability work on gated models must account for negative activations. Additionally, the empirical regularity that the median cos(win, wout) transitions from positive to negative across layers across many independently trained models is striking and suggests a fundamental architectural constraint or training dynamic.

## Suggestions
- Perform ablation experiments on a second model (e.g., Llama-3.2-3B) on a similarly sized dataset to confirm the outsize influence of weakening neurons.
- Include a verifiable justification of the preprocessing sign-flip step in the main paper, or perform a control experiment without it.
- Show how the classification changes if the threshold τ is varied (e.g., τ=0.3, 0.7) to demonstrate robustness.

## Score and Decision
**Score:** 6  
**Decision:** Accept  

The paper presents a fresh weight-based lens for analyzing gated neurons, discovers a surprising class of weakening neurons with outsized influence, and demonstrates (for the first time) that negative Swish values have functional importance. The empirical patterns are robust across many models. The main weakness is the limited scope of the causal ablation experiments (one model), which prevents full confidence in the universality of the behavioral claims, but the weight-based observations are already valuable. Overall, the paper makes a solid contribution that will likely inspire further work.

MY FINAL SCORE: <score>6</score>  
MY FINAL DECISION: <decision>Accept</decision>