## Summary

This paper investigates whether LLMs exhibit a human-like inductive bias toward Information Bottleneck (IB)-efficient categorization, using color naming as a primary testbed. The authors evaluate 39 LLMs across 6 families on English color naming under the IB framework, then introduce Iterated In-Context Language Learning (IICLL) to simulate cultural transmission of pseudo color-naming systems and probe inductive biases beyond training data mimicry. The key finding is that all tested LLMs move toward IB-efficiency through IICLL, but only Gemini 2.0 recapitulates the full range of near-optimal IB tradeoffs observed across human languages; other SOTA models converge to low-complexity solutions.

## Strengths

- **Principled, theory-driven evaluation framework.** The paper grounds its analysis in the well-established IB framework for semantic systems (Zaslavsky et al., 2018) and iterated learning (Griffiths & Kalish, 2007), avoiding the ad-hoc metrics common in LLM cognition studies. The efficiency loss and NID alignment metrics are directly inherited from a line of work with strong cross-linguistic empirical support.

- **Comprehensive model coverage.** 39 models across 6 families (Gemini, Gemma, Llama, Qwen, Olmo, GPT-2), systematically varying size, instruction-tuning, and modality. This enables meaningful trend identification: larger instruction-tuned models perform better, pre-training alone is insufficient, and instruction-tuning drives the largest improvement.

- **Thoughtful experimental design in IICLL.** The adaptation of iterated learning to LLMs via in-context learning is non-trivial. The use of pseudo terms, avoiding telling the model the stimuli are colors (referring only to "features"), the rotation analysis (Regier et al., 2007), and the feature-based clustering baseline collectively strengthen the claim that emergent systems are non-trivially efficient. The k=14 condition (84 in-context examples) is a genuinely demanding test.

- **Non-obvious and interesting main finding.** The result that only Gemini 2.0 recapitulates the full human range of IB tradeoffs, while other SOTA models converge to low-complexity solutions, is a real empirical contribution. The observation that some models (Olmo 2 32B inst., Qwen 2.5 VL 7B inst.) produce systems resembling low-resource WCS languages rather than English is surprising and worth further investigation.

## Weaknesses

### Fatal
None.

### Major
None.

### Minor

- **The headline framing slightly overstates the generality of the results.** The Discussion (line 167) states that "LLMs are capable of evolving perceptually grounded, human-like semantic systems, guided by the same IB-efficiency principle," and the title reads "ON THE EMERGENCE OF HUMAN-ALIGNED CATEGORIZATION" in LLMs broadly. However, the full human-like range of IB tradeoffs is observed in only one model (Gemini 2.0); the other three tested models converge to low-complexity solutions. The abstract and results section are more balanced (explicitly noting "only a model with strongest in-context capabilities"), but the title and Discussion claim a generality the evidence supports for exactly one model. The paper's own transparency about model differences makes this a framing issue rather than a factual error—recalibrating the title and Discussion would resolve it.

- **The interpretive link between IICLL convergence and inductive biases relies on an unverified assumption.** The paper correctly states (line 67) the Bayesian conditions under which iterated learning chains converge to the agent's prior (Griffiths & Kalish, 2007). However, it provides no evidence that LLMs satisfy these Bayesian assumptions, which would license the interpretation that IICLL systems directly reflect "inductive biases" in the Bayesian sense. This is a known open question in the I-ICL literature (Zhu & Griffiths, 2024) that the paper inherits without explicit discussion. The rotation analysis and clustering baseline partially mitigate this concern but do not bridge the interpretive gap. The paper would benefit from either (a) explicitly acknowledging this limitation or (b) providing an argument or auxiliary experiment showing that the Bayesian interpretation is plausibly satisfied.

- **No formal statistical significance testing.** The paper reports 95% confidence intervals for IICLL results (Figure 4), which is helpful, but conducts no formal statistical tests comparing models to each other, comparing emergent systems to baselines, or assessing whether improvements over generations are significant. Claims about "significant decrease" in the rotation analysis (line 145) are made without reporting a test statistic, p-value, or effect size. For a paper whose central claims depend on comparing models and conditions, the absence of formal inference is a gap.

- **The English alignment metric lacks a chance-level baseline.** Figure 2c shows English-alignment values ranging from ~0.0 to ~0.6, but there is no baseline showing what a random partition of the color grid into k categories would score on NID alignment, or what a simple perceptual clustering baseline (e.g., k-means on CIELAB) would score. This makes it difficult to interpret whether a model scoring 0.4 is doing something nontrivial or is near chance. The IB tradeoff plots (Figure 2a) partially anchor interpretation through the IB bound and human data, but the alignment metric specifically needs a baseline.

- **The Shepard circles experiment is too thin to support the generalization claim.** The paper presents this as "initial evidence" (line 157) and a "preliminary investigation" (line 159), and explicitly notes that IB-efficiency was not computed for this domain. However, only Gemini is tested, only k=4 is used, the analysis is purely qualitative (categories became "increasingly compact"), and no quantitative metric is reported. Even as "initial evidence," the experiment advances the paper's central argument only weakly. The cautious framing in the text is appropriate, but the experiment's presence in the main paper gives it more weight than its substance supports.

- **The CIELAB finding has an alternative explanation not fully engaged with.** The paper frames the result that LLMs struggle with CIELAB inputs as revealing "a key difference between how LLMs represent color and how humans do" (line 119). An equally plausible explanation is that sRGB coordinates are vastly more common in LLM training data than CIELAB coordinates, meaning the difference may reflect training data distribution rather than fundamentally different perceptual representations. The paper should at minimum acknowledge this alternative interpretation.

### Trivial
None.

## Nice-to-Haves

- The Shepard circles experiment could be strengthened by computing IB-efficiency for the emergent systems, testing additional models beyond Gemini, and adding a quantitative compactness metric. If these cannot be added, the experiment could be moved to the appendix with a brief mention in the main text.
- Adding a random partition baseline for the English alignment metric would help readers interpret the alignment range.
- Adding statistical significance tests (e.g., comparing each model's final-generation efficiency loss to its initial value, and comparing Gemini's final efficiency loss to each other model's) would strengthen the comparative claims.

## Removed Points

These points were flagged for removal from the input review; they are listed here for transparency but should be treated with caution:

- **Reproducibility details (prompts not fully specified in main text).** The reviewer noted that the English naming prompt is not fully specified in the main text. The paper explicitly references Appendix J for example prompts and full details. Since the parser strips appendix content from all papers, this is not a valid weakness of the submission as written.
- **Shepard circles labeled as "Critical Issue."** The reviewer raised this as a critical evidential problem, but the paper's own framing ("initial evidence," "preliminary investigation," "An important direction for future work is to test whether this emergent structure also supports greater IB-efficiency") is appropriately cautious. Demoted to Minor above and the substance is preserved.
- **"Should not be accepted as-is" language.** The reviewer's concluding recommendation is based on framing issues that are addressable and do not undermine the paper's core scientific contribution. The paper's evidence base is solid; the main change needed is recalibrating the title and Discussion.

## Novel Insights

The input review's key insight is that the paper's claim structure—"LLMs are capable of evolving human-like semantic systems"—is under tension with the model-specific nature of the strongest evidence (Gemini 2.0 only). This tension is productive: reframing the paper's contribution around the *contrast* between Gemini and other models (rather than claiming a general LLM property) would sharpen the research question and make the result more interesting, not less. The review also correctly identifies that the IICLL-to-inductive-bias interpretive link is stronger than the current evidence supports, and that the paper's evaluation framework could be strengthened with relatively simple additions (baselines, significance tests) without changing any experimental design.

## Suggestions

1. **Recalibrate the title and Discussion** to reflect that the full human-like range of IB tradeoffs was observed in one model (Gemini 2.0), while other models show a partial but meaningful version of the bias. The contrast between models is the paper's most interesting result.
2. **Explicitly acknowledge the Bayesian interpretation gap** for IICLL convergence. Either argue that the analogy is reasonable for LLMs (with supporting reasoning) or reframe the interpretive claim from "inductive bias" to "systematic regularities under transmission pressure."
3. **Add chance-level and clustering baselines** for the English alignment metric to help readers interpret the 0.0–0.6 range.
4. **Add formal statistical tests** for the key comparative claims (model vs. model, generation vs. generation in IICLL, rotation analysis).

## Score and Decision

MY FINAL SCORE: <score>8</score>
MY FINAL DECISION: <decision>Accept</decision>