## Summary

This paper applies the Information Bottleneck (IB) framework to study whether LLMs exhibit a human-like inductive bias toward efficient, compressed semantic categories. The authors conduct two studies: (1) an English color-naming evaluation of 39 LLMs across 6 families, finding wide variation with larger instruction-tuned models performing best; and (2) an Iterated In-Context Language Learning (IICLL) paradigm that simulates cultural transmission, showing that instruction-tuned LLMs (particularly Gemini 2.0) restructure initially random artificial color-naming systems toward greater IB-efficiency and human-alignment over generations—mirroring results from human iterated language learning experiments.

## Strengths

1. **IB framework provides a principled evaluative lens.** The paper maps LLM color-naming systems onto the information plane and evaluates them against the theoretically optimal IB tradeoff (Figures 2a, 3), giving quantitative meaning to "efficiency" beyond ad-hoc metrics. This connects the results to a substantial body of cognitive science (Zaslavsky et al., 2018, 2019, 2021, 2022; Imel et al., 2025).

2. **IICLL is a well-motivated methodological adaptation.** Extending I-ICL (Zhu & Griffiths, 2024) to iterated language learning with pseudo-labels is a natural way to probe inductive biases in LLMs without relying on patterns present in the training data. The design follows the human ILL paradigm of Xu et al. (2013), enabling a structurally appropriate comparison.

3. **Large-scale evaluation across 39 models and 6 families** enables meaningful comparisons along size, instruction-tuning, and training-stage axes. The finding that many state-of-the-art LLMs struggle with basic English color naming is striking and practically important. The observation that some models produce systems resembling low-resource WCS languages rather than English (line 105) is a nuanced and interesting result.

4. **The rotation analysis (Section 4.2, Appendix H) is a proper control.** Showing that hue-rotated versions of Gemini's emergent systems are significantly less efficient/aligned demonstrates that the IB-efficiency of the IICLL systems is non-trivial.

## Weaknesses

### Fatal
None.

### Major

1. **Overclaimed inference from IICLL to English naming.** The paper claims that the IICLL result shows LLMs "are not merely mimicking patterns in their training data" but exhibit "a human-like inductive bias toward IB-efficiency" (abstract, line 23, discussion line 163). The IICLL experiment demonstrates that LLMs *can* develop IB-efficient novel category systems from random starts with pseudo-labels. This is a genuine and interesting finding. However, it does not logically establish that their English color-naming performance is *caused* by this bias rather than by memorization of training data—these two capacities could coexist. The paper treats the IICLL result as a disproof of the mimicry explanation for English naming, but the logical chain requires an additional link that is not provided (e.g., showing that English systems and IICLL systems share structural properties beyond both being IB-efficient, or that models fail at English naming for languages they haven't seen but succeed via IICLL). **This weakness is not fatal** because the IICLL finding is independently valuable. The paper would be stronger with a more measured framing.

2. **The instruction-tuning confound is not adequately addressed.** The IICLL experiment only tests instruction-tuned models (line 125: "We considered only large, instruction tuned models"), and the English naming results show that instruction-tuned models perform dramatically better than base models (Figure 2c). Instruction-tuned models are explicitly trained via RLHF or similar to produce human-aligned responses. Calling the resulting IICLL behavior an "inductive bias toward IB-efficiency" that "may emerge to support intelligent behavior" (line 167) glosses over a more parsimonious explanation: models trained to imitate human responses will naturally produce human-like (IB-efficient) outputs even in the IICLL paradigm. The discussion (line 169) acknowledges that the origins of the bias are "unclear" but does not specifically discuss this confound. Testing a non-instruction-tuned model in IICLL (even if it performs poorly, the trajectory direction would be informative) would substantially strengthen the argument.

### Minor

1. **Structural differences between IICLL and human ILL are not discussed.** In human ILL (Xu et al., 2013), participants learn color-label associations from memory during a training period and then produce labels. In IICLL, the model is given labeled examples *in the prompt context window* and can attend to them while producing responses. The finding that Gemini achieves higher efficiency and alignment than human IL trajectories (line 145) could partly reflect this structural advantage (external memory store available at inference time vs. human memory consolidation). The paper should discuss this difference and its implications.

2. **"Significant" is asserted without statistical reporting.** The rotation analysis (line 145) states that hue rotations lead to a "significant decrease in efficiency and alignment for Gemini" but does not report any test statistic, p-value, or effect size. Given the small number of IICLL chains, a permutation test or bootstrap confidence interval would be straightforward and important.

3. **No analysis of prompt sensitivity.** The paper uses a single prompt phrasing per condition. LLMs are sensitive to prompt variations; a brief analysis of whether the English naming or IICLL results are stable across different phrasings would strengthen reliability.

4. **Shepard circles result is preliminary and not quantitatively evaluated.** Section 4.3 is appropriately described as preliminary, but categories becoming "increasingly compact" is visually suggestive without quantitative backing. IB-efficiency is not computed for these systems, and comparison to human data is absent. The abstract and discussion slightly overstate the significance of this result.

### Trivial
None.

## Nice-to-Haves
- Provide explicit quantitative comparison between Gemini's IICLL systems and human IL data, with confidence intervals or effect sizes for the difference.
- Report the IB-efficiency of the Shepard circle IICLL systems to move beyond visual inspection.
- Test whether the English color naming results are robust to different prompt phrasings.
- The sRGB input format concern is partially addressed by the image-input experiments (finding that images do not help larger models), but could be acknowledged more explicitly as a remaining limitation.

## Removed Points
The following points from the input review are excluded:

- **sRGB input confound as a "Critical Issue":** The reviewer raised this as a structural weakness, but the paper already addresses it by testing image inputs (finding no improvement for larger models) and CIELAB coordinates (finding worse performance). The concern is partially mitigated, though not fully resolved—it is moved to Nice-to-Haves.
- **"Models cited may not exist"** - speculative and violates hard rules.
- **Missing related works** - violates hard rules; no external confirmation possible.
- **Formatting nitpicks** - parser artifacts, not author errors.
- **Missing appendix content** - parser-stripped sections; the original submission has them.

## Novel Insights
None beyond the paper's own contributions. The review surfaces the observation that IICLL's structural advantage over human ILL (in-context exemplars vs. memory-based learning) is a confound the paper does not address, but this is a weakness rather than a novel insight.

## Suggestions
1. **Reframe the central claim.** Present the IICLL result as evidence that LLMs possess an inductive bias toward IB-efficiency (an interesting finding on its own), rather than using it to argue that English naming performance is "not merely mimicking." The latter claim requires additional evidence.
2. **Acknowledge the instruction-tuning confound explicitly.** Discuss the possibility that the observed bias toward IB-efficiency in IICLL is a byproduct of alignment training toward human-like responses, and consider testing at least one non-instruction-tuned model in IICLL.
3. **Report statistical tests** (permutation or bootstrap) for the rotation analysis significance claim.
4. **Add a prompt sensitivity analysis** for the English naming task.
5. **Discuss the structural differences** between IICLL (in-context exemplars) and human ILL (memory-based) and how this affects the interpretation of the comparison.

## Score and Decision

**Calibration anchors used (all rounds):**

| Path | Avg Score | Comparison |
|------|-----------|------------|
| fN8yLc3eA7.md (Telephone Game) | 6.00 | Most directly comparable: iterated cultural transmission in LLMs. Current paper is more rigorous (39 models, stronger IB grounding) but has framing overreach. |
| HYyRwm367m.md (Neural LoT) | 6.50 | Cognitive science/ML intersection. Comparable rigor; current paper is empirical while NLoTM is architectural. |
| YzXPU3QRnL.md (Larger LLMs ICL) | 5.80 | Similar interdisciplinary framing. Current paper is more novel in methodology and has stronger theoretical grounding. |
| bVTM2QKYuA.md (Representation Geometry) | 6.75 | Strong LLM analysis paper. Current paper is comparable in rigor but addresses a different question. |
| RC5FPYVQaH.md (CB-LLM) | 5.75 | Similar interdisciplinary scope. Current paper has stronger cognitive science connections. |
| 8QTpYC4smR.md (Sys Review of LLMs) | 1.00 | Strong reject anchor; clearly much weaker than current paper. |

**Round 1 bracket:** 5.5–7.0. The paper sits alongside the Telephone Game paper (6.00) and is clearly stronger than reject-level papers (1–3) but has framing issues that prevent it from reaching 7+ territory.

The paper makes solid empirical contributions (large-scale evaluation, IICLL method) with a principled theoretical framework. However, the central narrative overreaches, and the instruction-tuning confound is inadequately addressed. With a more measured framing and additional analyses, this could be a strong contribution.

MY FINAL SCORE: <score>6.0</score>
MY FINAL DECISION: <decision>Accept</decision>