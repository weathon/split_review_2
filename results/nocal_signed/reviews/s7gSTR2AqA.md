## Summary

This paper investigates whether LLMs exhibit a human-like inductive bias toward Information Bottleneck (IB)-efficient categorization, using color naming as a richly-grounded testbed. The authors conduct two experiments across 39 models: (1) an English color-naming study evaluating LLMs' semantic alignment and IB-efficiency, and (2) an Iterated In-Context Language Learning (IICLL) paradigm that simulates cultural transmission of pseudo color-naming systems. They find that while most LLMs struggle with English color naming, larger instruction-tuned models perform better, and under IICLL, models restructure random category systems toward greater IB-efficiency — though only Gemini 2.0 fully recapitulates the human range of IB tradeoffs.

## Strengths

- **The two-experiment design is well-conceived.** Experiment 1 (English color naming) measures what the model has learned from its training data, while Experiment 2 (IICLL) tests whether the model's behavior reflects an inductive bias beyond mimicking those patterns. This distinction directly addresses the paper's central question and provides a clear experimental logic.

- **The theoretical framing via the Information Bottleneck is principled and elevates the contribution.** Using the IB framework (Zaslavsky et al., 2018) as an evaluation lens for LLMs is a genuine intellectual contribution — it moves the paper beyond checking whether LLMs mimic English color terms to testing whether they structure meaning according to the same optimization principle as human languages. The efficiency loss and NID measures (Section 3) are well-defined and appropriate.

- **The rotation analysis (Section 4.2) is a strong control.** By rotating color-label mappings along the hue dimension and showing that efficiency and alignment significantly decrease, the paper provides evidence that the emergent systems are non-trivially structured and specifically aligned with the perceptual structure of color, not just any near-IB-optimal system.

- **Honest reporting of model failures.** The paper does not hide that most LLMs struggle with English color naming (line 105: "a surprising number of state-of-the-art models fail") and that only Gemini 2.0 fully recapitulates the human range of IB tradeoffs in IICLL (line 139). This candor prevents overstatement and is a mark of scientific rigor.

- **Substantial model coverage.** Testing 39 models across 6 families with variation in size, instruction-tuning, and modality is genuinely thorough. The inclusion of training checkpoints for Olmo provides a useful developmental perspective on how these capabilities emerge during training.

## Weaknesses

### Fatal
None.

### Major

- **The central interpretive claim — that LLMs exhibit a "human-like inductive bias toward IB-efficiency" — is substantially broader than the evidence supports.** The paper's own results show that only *one* model (Gemini 2.0) fully recapitulates the human range of IB tradeoffs, while others converge to low-complexity solutions. Additionally, the paper acknowledges (line 169) that "the precise origins of the bias we observe... are unclear" — yet the abstract and introduction present the bias as established fact. This tension between definitive framing and acknowledged uncertainty means the paper overclaims. The evidence supports a narrower, but still interesting, conclusion: that some LLMs, under in-context learning conditions, restructure category systems in ways consistent with IB efficiency. Replacing "human-like inductive bias" with a more precise characterization of what was actually observed would strengthen the paper considerably.

- **The paper does not discuss a fundamental asymmetry between the human ILL experiment and the LLM IICLL paradigm.** In the human experiment (Xu et al., 2013), participants learned associations during a training phase and generalized *from memory* — they had a genuine memory bottleneck that forced compression. In the LLM version, models see all training examples *simultaneously in their context window* and can attend to all of them while labeling. Humans must compress; LLMs do not need to. This asymmetry means convergence to IB-efficient systems could reflect different mechanisms (e.g., learned priors about category structure from text) rather than a shared "drive to compress." The paper should discuss this explicitly rather than treating the two paradigms as directly comparable.

### Minor

- **The Shepard circles result (Section 4.3) is too preliminary for the role it plays in the paper's narrative.** Only Gemini was tested, only k=4, no IB-efficiency analysis was conducted, no comparison to human data is provided, and the result is purely qualitative (4 chains shown). While the paper does hedge with "preliminary investigation" and "important direction for future work," including this as a bullet-point contribution in the abstract creates an impression of support for generalization that the experiment cannot deliver.

- **The claim that "Gemini's efficiency and alignment over generations are higher than the human IL trajectories" (line 145) is ambiguous.** It could mean Gemini is genuinely better at finding efficient systems, or it could mean the LLM version of the task (with in-context examples) is structurally easier than the human version (with memory constraints). This distinction matters for the "human-like" framing.

- **The paper mentions "significant decrease" (line 145) and shows 95% confidence intervals but does not report formal statistical tests in the main text.** For a paper whose claims rest on quantitative comparisons (Gemini vs. other models, IICLL trajectories vs. human baselines), the absence of reported test statistics is a limitation.

### Trivial

- The main text does not specify the number of IICLL chains run per condition, number of random initializations, or total number of API calls. These details are likely in the appendix but would be helpful in the main text for assessing robustness.

## Nice-to-Haves

- Adding a control condition applying IICLL to a stimulus space that does NOT have the same perceptual structure as color (e.g., randomly shuffled coordinates) would strengthen the claim that IB-efficient convergence is specific to structured spaces.
- Tightening the interpretive claim from "human-like inductive bias" to something closer to "LLMs can restructure categories in ways consistent with IB efficiency under iterated in-context learning" would better match the evidence.
- Adding formal statistical tests (effect sizes or pairwise comparisons) for key comparisons would strengthen confidence in the quantitative claims.
- The Shepard circles section would be better placed in an appendix or clearly marked as pilot exploration rather than appearing as a bullet-point contribution.

## Removed Points

These points from the input review were filtered out after verification against the paper:

- **Criticism that IICLL uses the same evaluation metric (IB efficiency is both the measure and the claimed bias):** The IICLL process does not optimize for IB efficiency; it is used purely for evaluation. The critic's point about needing a non-human-like control condition is a reasonable suggestion but belongs in Nice-to-Haves.
- **Speculative alternative explanations (learned templates, task-specific heuristics):** These are speculative interpretations, not demonstrated flaws. The paper's own acknowledgment that origins are unclear (line 169) already addresses this limitation.
- **Criticism that the Shepard circles abstract claim is unsupported:** The abstract says "suggesting that our result could *potentially* apply" — this is appropriately hedged. The criticism overstates the strength of the claim.
- **Criticism about missing appendix content:** The parser strips appendices; these exist in the original submission.
- **Generic/superficial strengths removed:** None of the kept strengths were generic; all were concrete and specific to the paper.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. Tighten the central claim: replace "human-like inductive bias toward IB-efficiency" with a more precise characterization (e.g., "LLMs restructure category systems in ways consistent with IB-efficiency").
2. Explicitly discuss the memory bottleneck asymmetry between human ILL and LLM IICLL.
3. Move the Shepard circles result to a speculative/appendix role and remove it from the abstract bullet points.
4. Add formal statistical tests for key comparisons in the main text.

MY FINAL SCORE: <score>7.0</score>
MY FINAL DECISION: <decision>Accept</decision>