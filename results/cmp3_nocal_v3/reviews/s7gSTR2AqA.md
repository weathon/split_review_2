## Summary

This paper adapts cognitive science frameworks — the Information Bottleneck (IB) principle and iterated language learning (ILL) — to study whether LLMs develop human-like, efficient color categorization systems. The authors conduct two main experiments: (1) an English color-naming evaluation across 39 models, showing that larger instruction-tuned models best approximate English naming and IB-efficiency; and (2) an Iterated In-Context Language Learning (IICLL) paradigm where models iteratively transmit pseudo-color-term systems, finding that Gemini 2.0 converges to near-optimal IB-efficient systems resembling human languages, while other strong models converge to lower-complexity but still increasingly efficient solutions.

## Strengths

- **Theoretically grounded experimental design.** The paper anchors its experiments in the IB framework (Zaslavsky et al., 2018), which provides a principled normative standard for evaluating category systems, and the iterated learning paradigm (Griffiths & Kalish, 2007), which offers a well-motivated method for revealing inductive biases. This gives the study a foundation that goes beyond ad-hoc prompting evaluations.

- **Large-scale model comparison (39 models, 6 families).** The English color-naming study systematically varies model size, instruction-tuning, and modality within families. The finding that some models (Olmo 2, Qwen 2.5 VL) produce systems resembling low-resource WCS languages rather than English is a genuinely non-obvious result.

- **The rotation analysis (Section 4.2, Appendix H) is a meaningful control.** Showing that hue-rotated versions of Gemini's emergent systems have degraded efficiency and alignment provides nontrivial evidence that the observed structure is non-arbitrary and specifically IB-efficient, not a random partition artifact.

- **The core Gemini 2.0 IICLL result is striking and novel.** That Gemini can iteratively construct near-optimal IB-efficient color category systems from pseudo-terms, with no indication that the stimuli are colors, is a genuine empirical finding that extends our understanding of emergent properties in LLMs.

## Weaknesses

### Fatal
None.

### Major

1. **The IICLL paradigm confounds in-context learning ability with inductive bias, limiting the strength of the central claim.** The paper's headline conclusion — that LLMs exhibit a "human-like inductive bias toward IB-efficiency" beyond mimicking training data — rests primarily on the IICLL experiment. However, across the four models tested, only Gemini 2.0 succeeds at capturing the full complexity range; the other three models converge to low-complexity solutions. The paper acknowledges that "the IICLL task requires very strong in-context learning" and that for the k=14 condition "most of the LLMs immediately converge to low-complexity solutions" (Section 4.2). This creates a confound: when a model fails to track 84 in-context examples, its trajectory may reflect task difficulty rather than revealing any genuine inductive bias. A model that falls back to a trivial partition will mechanically appear to have low complexity (near the low-complexity end of the IB curve), making the efficiency metric `ε` improve as diversity collapses. The paper does not cleanly separate "inductive bias toward IB-efficiency" from "ability to handle a difficult ICL task" for the non-Gemini models. While the paper presents evidence that all models improve over generations on efficiency loss and IB-alignment (Figure 4), the confound weakens the inference that these trajectories specifically reveal a bias toward the IB bound. This is a structural issue because it bears directly on the paper's central contribution claim.

2. **The paper's broad claims about "LLMs" overreach the evidence.** The abstract and discussion state that "LLMs iteratively restructure initially random systems towards greater IB-efficiency" and that this demonstrates alignment with "the same fundamental principle that underlies semantic efficiency in humans." The rotation analysis and feature-based clustering baselines provide strong evidence specifically for Gemini 2.0, but the paper itself notes these controls are "less conclusive for the other models" (Section 4.2). The evidence supports a narrower conclusion: Gemini 2.0 (and to a lesser degree, Gemma 3 27B, Qwen 2.5 32B, and Llama 3.3 70B, all at lower complexity ranges) shows this pattern. The paper should more clearly delimit which claims are supported by which models rather than using "LLMs" as a blanket term.

3. **The Shepard circles experiment (Section 4.3) does not provide quantitative support for domain generality.** This section tests only one model (Gemini), one condition (k=4 labels), with no IB-efficiency analysis, no rotation control, and no quantitative evaluation — only four example chains shown qualitatively. The paper accurately describes it as "initial evidence" but nonetheless allows this result to appear in the abstract's list of contributions ("suggesting that our result could potentially apply also in other domains"). As presented, this section does not carry evidential weight for the paper's central claims and would be more appropriate as a discussion of future work or removed from the contribution summary.

### Minor

4. **No formal statistical tests for key comparisons.** Figures 3 and 4 show trajectories and confidence intervals, but the paper does not report hypothesis tests for its main claims (e.g., whether the improvement in efficiency loss from generation 0 to generation 12 is significant across chains, or whether Gemini's final systems are significantly different from the other models' in IB-alignment). The rotation analysis is described as showing a "significant decrease" but no test statistic or p-value is reported.

5. **The paper does not discuss prompt sensitivity of the IICLL results.** The IICLL paradigm uses specific prompt instructions and constrained generation formats. Since the prompt directly determines what the model treats as "features" versus "labels," variations in prompt wording could affect the results. This is especially relevant for the IICLL experiment where the prompt format influences how the model interprets the task.

6. **The theoretical link between IICLL trajectories and "inductive bias" in LLMs is not fully justified.** The paper invokes the Bayesian IL framework (Griffiths & Kalish, 2007), under which iterated learning converges to the learner's prior. However, LLMs are not Bayesian agents with well-defined priors and likelihoods; they are frozen models processing prompts. While the I-ICL literature (Zhu & Griffiths, 2024) provides some precedent, the paper would benefit from a more explicit discussion of whether IICLL trajectories in LLMs can be interpreted as revealing inductive biases in any theoretically grounded sense, as opposed to reflecting prompt-dependent behavioral tendencies.

### Trivial
None.

## Nice-to-Haves

- Varying the number of in-context examples systematically (e.g., 10, 25, 50, 84) for the non-Gemini models could help disentangle ICL ability from the efficiency bias. If these models produce higher-complexity but still IB-efficient systems when the task is easier, that would strengthen the claim.
- Adding statistical tests (e.g., permutation tests) for the main comparisons and the rotation analysis would help quantify the reliability of the observed effects.
- Testing prompt sensitivity (e.g., varying instruction wording, example formatting) would improve robustness.

## Removed Points

These points from the harsh critic review are removed or demoted with justification:

- **Issue 4 (IB metric assumes human perceptual geometry):** Removed as a standalone weakness. The IB metric evaluates category systems as partitions of the color space — the fact that it uses CIELAB-based perceptual geometry is appropriate for the claim being made (that LLM systems are efficient *for human communication*). The paper explicitly acknowledges that LLMs struggle with CIELAB inputs (Section 4.1) and the IICLL experiment (where models build systems without English labels) partially addresses the concern about data memorization. This is not a weakness of the paper's methodology as stated; it is a known property of the evaluation framework inherited from prior work.

- **"No analysis of training data confound for English naming":** The paper explicitly discusses this confound and positions the IICLL experiment as its solution (lines 121, 125, 163: "is this behavior merely a reflection of imitating patterns in the models' training data, or does it signify a more intrinsic LLM inductive bias..."). This criticism misunderstands what the paper already does.

- **"The abstract treats Shepard circles as a contribution":** Partially kept — the paper's abstract does reference this result, and the reviewer's concern about overreach is valid. However, the paper appropriately hedges with "preliminary" and "potentially" language. Demoted to Minor weakness #3 above rather than a separate critical issue.

- **Claims about missing appendices, proofs, or references:** These are parser artifacts and are removed per instructions.

- **Various formatting/style nitpicks:** Removed.

- **Criticism that IICLL chains being averaged could cause artifacts:** The reviewer speculates this could be an issue ("is this a genuine approach toward the bound, or an artifact of averaging trajectories that start high and then collapse?") without evidence from the paper. The paper shows individual chain data in Figure 3. This is speculation, not a verified weakness.

- **"The paper does not discuss the training data confound for the English naming task":** This is factually wrong — the paper explicitly positions IICLL as addressing this very confound (Abstract, lines 121, 163). Removed.

## Novel Insights

The harsh critic's review surfaces a genuinely important insight that goes beyond the paper's own framing: the IICLL paradigm for LLMs is structurally asymmetric — it tests both the model's "inductive bias" and its in-context learning capacity simultaneously, and these two factors cannot be cleanly separated without additional controls. This insight suggests that the paper's strongest result (Gemini 2.0) may be as much about frontier ICL capability as about any general "human-like" inductive bias present across LLMs. The review also correctly identifies that the evidence structure is hierarchical: the English naming study supports a broad claim (many models vary in alignment), but the IICLL evidence pyramid narrows to a single model at its peak, while the paper's language often generalizes from that peak downward.

## Suggestions

1. Narrow the paper's central claim to accurately reflect the evidence structure. The strongest supported claim is: "Gemini 2.0 can develop IB-efficient color category systems via iterated in-context learning with pseudo-terms, suggesting that frontier models may have learned structural regularities from training data that mirror human efficiency principles." Broader claims about "LLMs" should be qualified by which models provide evidence for which sub-claims.

2. Add a control experiment that varies ICL difficulty for the non-Gemini models (e.g., fewer in-context examples per generation) to test whether their low-complexity convergence reflects ICL failure or a genuinely different inductive bias.

3. Either remove the Shepard circles section or promote it to include quantitative analysis (IB evaluation, rotation control, multi-model comparison). In its current form it does not add evidential weight.

4. Add statistical tests (e.g., permutation tests comparing final-generation metrics against initial random systems) for the key IICLL comparisons.

## Score and Decision

<score>6.0</score>
<decision>Borderline Accept</decision>