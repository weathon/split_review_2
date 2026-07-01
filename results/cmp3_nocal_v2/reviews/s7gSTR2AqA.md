## Summary

This paper investigates whether LLMs exhibit a human-like inductive bias toward Information Bottleneck (IB) efficiency in categorization. It first conducts an English color-naming study across 39 models, finding that larger instruction-tuned models better align with English and achieve near-optimal IB tradeoffs. It then introduces Iterated In-Context Language Learning (IICLL), an experimental paradigm that simulates cultural evolution of artificial color-naming systems by passing in-context exemplars across generations. Using IICLL, the paper finds that four instruction-tuned LLMs restructure initially random category systems toward greater IB-efficiency, with Gemini 2.0 covering the full complexity range seen across human languages. A preliminary Shepard circles experiment suggests potential domain generality. The work is grounded in the Information Bottleneck principle and iterated learning theory from cognitive science.

## Strengths

- **Strong theoretical scaffolding.** The paper grounds its investigation in two well-established cognitive science frameworks — the Information Bottleneck principle (Zaslavsky et al., 2018) and iterated language learning (Griffiths & Kalish, 2007; Kirby et al., 2008). These frameworks provide concrete quantitative predictions (the complexity-accuracy tradeoff curve) and a formal link between observed category systems and underlying inductive biases. This is rare in LLM evaluation work and genuinely sharpens the questions being asked.

- **Large-scale model comparison.** Testing 39 models across 6 families (Gemini, Gemma, Llama, Qwen, Olmo, GPT-2) with both base and instruction-tuned variants gives the English naming study substantial breadth. The finding that models vary widely in their alignment with English — and that smaller/base models often fail entirely — is a meaningful empirical contribution.

- **The IICLL paradigm is a clever experimental design.** Adapting iterated in-context learning (Zhu & Griffiths, 2024) to simulate cultural evolution of *language* systems is a genuine methodological contribution. It allows direct comparison with human iterated learning data (Xu et al., 2013) and addresses whether LLMs can acquire category structure beyond memorization of their training data.

- **Rotation analysis as a control.** The rotation analysis (Section 4.2, referencing Regier et al., 2007) — rotating the color-label mapping along the hue dimension and measuring the drop in efficiency/alignment — is exactly the kind of control needed to show that emergent systems are non-trivially structured. Showing a significant drop for Gemini strengthens the case that the IICLL results reflect structured learning, not artifacts.

## Weaknesses

### Fatal
None.

### Major

1. **The IICLL paradigm does not fully separate "inductive bias toward IB-efficiency" from training-data retrieval.** The paper's central claim (abstract, lines 9, 23; Section 4.2) is that LLMs are "not merely mimicking patterns in their training data but are actually guided by a human-like inductive bias toward IB-efficiency." The IICLL experiment uses pseudo terms and describes stimuli as having "features" rather than as colors, which is a reasonable step. However, the stimuli are still the WCS 330-color grid — a well-known structure deeply embedded in the color categorization literature present in training data. When LLMs see this grid and are asked to assign pseudo-labels based on exemplars, their inference is unavoidably shaped by training on color language, color perception descriptions, and color categorization patterns from human languages. The convergence toward IB-efficient solutions is equally well-explained by the hypothesis that the models' training data contains efficient human color systems, and the IICLL procedure surfaces this prior knowledge. The paper does not provide a control that would cleanly distinguish a "bias" account from a "knowledge retrieval" account. The Shepard circles experiment was designed to address this, but it does not compute IB-efficiency (the paper explicitly states this is future work, line 159). This limitation directly affects how strongly the paper's headline claim can be stated.

2. **Structural asymmetry between human ILL and LLM IICLL undercuts the direct comparison.** In the human experiment (Xu et al., 2013), participants learned pseudo-words during a training phase and then recalled/applied them from memory to the full grid — a genuine compression task driven by memory constraints. In the LLM IICLL paradigm, all exemplars are presented *in-context*; the model never needs to compress, only to pattern-match. The IB-efficiency of human color systems is thought to arise in part from pressure to compress under memory and communication constraints, but the IICLL procedure removes that pressure. While iterated learning theory (Griffiths & Kalish, 2007) does not strictly require memory constraints for convergence to the prior, the specific human experiment being replicated does involve them. The paper's central comparison (Figures 3, 4) is presented as though both experiments measure the same underlying bias, but the mechanisms may be different. The Discussion (line 169) touches on communication pressure as future work but does not acknowledge this specific asymmetry.

### Minor

3. **ICL capacity confound.** The paper attributes Gemini's broader complexity range to its "strongest in-context capabilities" (line 143). But this makes it unclear whether the model's behavior reflects an IB-efficiency bias or simply better few-shot learning capacity. A model with limited ICL that produces simpler systems may not have a weaker "bias toward IB-efficiency" — it may simply not be able to maintain 84 exemplars (the k=14 condition) in its effective processing window. The paper acknowledges this factor but does not control for it.

4. **No formal statistical tests on key comparisons.** The paper reports 95% confidence intervals (Figure 4) and states that Gemini's rotation analysis results are "significant" (line 145), but does not report p-values, effect sizes, or formal tests comparing (e.g.) whether Gemini's final-generation systems are significantly more IB-aligned than the other models' systems, or whether convergence rates differ across models. These may exist in the stripped appendix, but their absence from the main text weakens the comparative claims.

5. **How LLM outputs are mapped to the IB framework's stochastic encoder is not explained in the main text.** The IB model (Eq. 1) requires a stochastic encoder q(w|m), but LLM outputs are deterministic category assignments (one label per color chip). The paper states that the IB color naming model from Zaslavsky et al. (2018) is used "as part of our evaluation" (line 63), but does not explain how the mapping from discrete responses to the quantities in Eq. (1) is performed. For a paper whose evaluation hinges on this framework, this is a notable gap in the main text (it may be in the stripped appendix).

6. **Number of IICLL chains/initializations is not reported in the main text.** Figure 4 shows averages and confidence intervals across "initializations and conditions" (caption, line 135), but the paper never states how many chains were run per condition, whether chains were independently initialized, or how the confidence intervals are computed. This is essential for evaluating the reliability of the results.

7. **The interesting trajectory dynamics are noted but not analyzed.** The paper observes that IICLL trajectories "initially climb in complexity towards the IB bound before slowly evolving downwards alongside it" (line 143), but offers no analysis of why this occurs or connection to theoretical predictions from iterated learning theory (Griffiths & Kalish, 2007). Understanding this dynamic could provide insight into the mechanisms driving convergence.

8. **Non-English but human-like systems are underexplored.** The finding that some models (Olmo 2 32B, Qwen 2.5 VL 7B) produce systems resembling low-resource WCS languages rather than English (line 105) is interesting but not analyzed. If models produce *non-English* but still human-like systems, this could strengthen the claim of a general human-aligned bias, but the paper does not develop this point.

### Trivial

- The pseudo-words used in IICLL are not listed or described; their phonological properties and potential biases from training data cannot be assessed.
- The NID-based alignment metric is defined, but actual alignment values are only shown visually in plots rather than in a table, making precise comparison harder.

## Nice-to-Haves

- Running the IICLL experiment in a domain where the model has minimal training data priors about human categorization (and computing IB-efficiency there) would substantially strengthen the inductive bias claim.
- A control that reduces the number of in-context exemplars to match human memory load, or tests whether results change without exemplars in context, would help address the memory-asymmetry issue.
- Reporting formal statistical comparisons (p-values, effect sizes) for the key results would strengthen the paper's claims.

## Removed Points

These points were raised in the input review but are removed after filtering:

- **Shepard circles don't test IB-efficiency (critic Issue 3).** The paper explicitly states this experiment is "preliminary" and that testing IB-efficiency for Shepard circles is "an important direction for future work" (line 159). The abstract uses "potentially" as a qualifier. The paper is appropriately cautious; the critic overstates this as a weakness.
- **Abstract implies IB-efficiency emergence is surprising (Section-by-Section note on line 9).** This is a matter of framing interpretation, not a concrete or verifiable weakness. The paper explicitly notes LLMs are not trained for the IB objective, making the question non-trivial regardless of expectations.
- **Prompts deferred to Appendix J (Section 3 note).** This is a standard practice for LLM papers; the main text appropriately summarizes the approach. Not a weakness.
- **Model details deferred to Appendix D.** Same as above — standard practice.
- **Trajectory dynamics not connected to theory (Section 4.2 note).** This is partially valid (included as Minor #7 above), but the critic's framing implied it was a major omission; the paper's observation is already informative without full theoretical analysis.
- **Missing related work / citation concerns.** Removed per instructions — these cannot be verified without external sources.

## Novel Insights

None beyond the paper's own contributions. The input review largely recapitulated the paper's findings and identified genuine evidential gaps but did not contribute a new framing or synthesis that the paper itself does not offer.

## Suggestions

1. **Qualify the central claim more carefully.** The paper should present the IICLL results as "consistent with the hypothesis that LLMs have a bias toward IB-efficiency" rather than as a definitive demonstration. Acknowledge explicitly that the design cannot fully separate inductive bias from training-data retrieval, and reframe the "not merely mimicking" language accordingly.

2. **Add a dedicated subsection explaining how the IB framework is applied to LLM outputs** (the q(w|m) mapping) in the main text, not just in the appendix.

3. **Report the number of IICLL chains and the statistical testing procedures** in the main text.

4. **Analyze the non-English human-like systems** (Olmo 2, Qwen VL) to see if they strengthen the case for human-aligned bias rather than English-specific memorization.

## Score and Decision

This is a well-motivated paper with a strong theoretical foundation, a genuinely clever experimental paradigm (IICLL), and an impressive empirical scope (39 models). The finding that LLMs converge toward IB-efficient solutions from random starts using pseudo terms is novel and interesting. However, the paper's central claim — that LLMs exhibit a "human-like inductive bias toward IB-efficiency" separable from training data retrieval — is broader than the current evidence supports. The key confounds (training data priors, ICL capacity, memory asymmetry) are real and acknowledged only partially. The paper would be strengthened by more careful qualification of its claims or additional controls. The contribution is real and the framework is valuable; I recommend acceptance with the expectation that the claims will be calibrated to match the evidence.

MY FINAL SCORE: <score>7.0</score>
MY FINAL DECISION: <decision>Accept</decision>