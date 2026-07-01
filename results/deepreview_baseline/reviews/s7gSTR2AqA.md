## Summary

This paper investigates whether large language models (LLMs) exhibit a human-like inductive bias toward Information Bottleneck (IB) efficiency in semantic categorization, using color naming as a testbed. The authors conduct two experiments: (1) an English color-naming study across 39 LLMs, finding that larger instruction-tuned models achieve better alignment with human English naming and IB efficiency; (2) an Iterated In-Context Language Learning (IICLL) paradigm that simulates cultural transmission, showing that LLMs restructure initially random category systems toward greater IB efficiency and human alignment. Gemini 2.0 recapitulates the full range of near-optimal IB tradeoffs observed across human languages, while other models converge to lower-complexity solutions. Preliminary results on Shepard circles suggest the bias may generalize beyond color.

## Strengths

- **Novel theoretical framing**: The paper combines the Information Bottleneck principle with iterated learning to study LLM categorization biases, providing a principled, cognitively-motivated lens that goes beyond simple accuracy comparisons.
- **Large-scale systematic evaluation**: Testing 39 models across 6 families with varying size, instruction-tuning, and modality offers a comprehensive picture of how model properties affect color naming behavior.
- **Methodological contribution (IICLL)**: The IICLL paradigm adapts human iterated language learning experiments to LLMs in a way that enables direct comparison of inductive biases, and is likely to be useful for future work on cultural evolution in LLMs.
- **Key empirical finding**: The demonstration that Gemini 2.0 can evolve human-like, IB-efficient category systems from random initializations—and that this is not merely mimicking training data—is striking and supports the paper's central claim.
- **Clear presentation**: The figures (especially the information plane plots and the IICLL trajectories) effectively communicate the main results, and the writing is well-structured.

## Weaknesses

### Fatal
None.

### Major
- **Confound in IICLL interpretation**: The IICLL experiment uses pseudo terms and does not mention color, but the models may still leverage pre-trained internal representations of color similarity (e.g., from text describing colors or from multimodal training). The claim that the bias is "not merely mimicking patterns in training data" is partially supported, but the experiment does not fully disentangle whether the observed IB-efficiency emerges from an inherent inductive bias or from the model's pre-existing knowledge of color structure that is itself IB-efficient. A control using a domain where the model has no pre-trained knowledge (beyond the Shepard circles pilot) would strengthen this claim.
- **Preliminary Shepard circles results**: The Shepard circles experiment is limited to one model (Gemini), one condition (k=4), and lacks quantitative IB analysis. The paper uses this to suggest domain generality, but the evidence is too thin to support that claim. This section feels like a placeholder rather than a completed analysis.
- **Limited disentanglement of bias source**: The paper shows that instruction-tuning and model size correlate with better performance, but does not investigate *why* this bias emerges. The Olmo checkpoint analysis is a step in this direction but only covers one model family. The origins of the IB-efficiency bias in LLMs remain largely unexplained.

### Minor
- **Dependence on a specific IB model**: The evaluation relies on the Gaussian perceptual noise model from Zaslavsky et al. (2018). While well-motivated, the results are contingent on this particular formalization of efficiency. Alternative definitions of optimal compression might yield different conclusions.
- **Comparison to human IL data**: The human iterated learning data from Xu et al. (2013) involved different experimental conditions (e.g., human participants with limited training, different chain lengths). The IICLL paradigm is not a perfect replication, and the paper could more explicitly discuss how these differences might affect the comparison.
- **English-centric focus**: The English naming study is thorough, but the paper's claims about "human-aligned" categorization are based primarily on English and WCS languages. The IICLL results show alignment to WCS, but the analysis of which specific languages the LLM systems resemble is qualitative (Appendix I). A more quantitative cross-linguistic comparison would strengthen the claims.

### Trivial
None.

## Nice-to-Haves

- A control experiment where IICLL is run on a domain with no plausible pre-trained structure (e.g., random feature spaces) to more cleanly isolate the inductive bias.
- An analysis of how the IB-efficiency bias scales with model size within a single family, controlling for instruction-tuning.
- A discussion of potential ethical implications of LLMs inheriting human-like categorization biases (e.g., reinforcing cultural biases in color naming or other domains).

## Novel Insights

The paper's core insight is that IB-efficiency—a principle that explains human semantic systems—can emerge in LLMs through cultural transmission alone, without explicit training for that objective. This suggests that optimal compression may be a general property of intelligent systems that process structured information, not just a human-specific phenomenon. The finding that only the most capable in-context learner (Gemini 2.0) recapitulates the full human range of complexity-accuracy tradeoffs, while other models collapse to low-complexity solutions, provides a nuanced picture of how model capabilities interact with this bias.

## Suggestions

- Strengthen the Shepard circles analysis by including quantitative IB evaluation, multiple models, and more category sizes, or remove it and frame the paper as focused on color.
- Add a control experiment where IICLL is run with stimuli that have no natural perceptual structure (e.g., random feature vectors) to test whether the bias is truly domain-general or specific to domains where the model has pre-trained knowledge.
- Discuss more explicitly the possibility that the IB-efficiency bias in LLMs is inherited from human language data (which is itself IB-efficient) rather than being an emergent property of the learning algorithm.

## Score and Decision

The paper makes a solid contribution by bridging cognitive science and LLM research with a principled framework and a novel experimental paradigm. The main claims are well-supported for the color domain, though the interpretation of the bias source and the generality beyond color are less conclusive. The weaknesses are not fatal and can be addressed in future work. I recommend acceptance.

MY FINAL SCORE: <score>7.5</score>
MY FINAL DECISION: <decision>Accept</decision>