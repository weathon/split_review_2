## Summary

This paper investigates whether Large Reasoning Models (LRMs)—specifically DeepSeek-R1 and o1—benefit from discrete prompt optimization, using event extraction (EE) as a case study. The authors employ a Monte Carlo Tree Search (MCTS) framework to refine both task instructions and event guidelines, and compare LRMs with standard LLMs (GPT-4o, GPT-4.5) in two roles: as task models and as prompt optimizers. The main findings are that LRMs benefit more from prompt optimization than LLMs, serve as more effective and stable optimizers, and that these advantages generalize to symbolic reasoning and biomedical NER tasks.

## Strengths

- **First systematic study of prompt optimization for LRMs**: The paper addresses a timely and practically relevant question—whether reasoning-intensive models still require careful prompt engineering—and provides clear evidence that they do, while also showing that they are themselves superior optimizers. The research question is well motivated and the case for studying it on event extraction (a structured, schema-constrained task) is convincing.

- **Comprehensive experimental design**: The paper evaluates four models in two roles across varying training set sizes (low/medium), shallow and full MCTS depths, and multiple metrics (TI, TC, AI, AC). The inclusion of both zero-shot baselines and ablation-style comparisons (e.g., each model as its own optimizer) allows for clean attribution of gains. The additional experiments on Geometric Shapes and NCBI Disease NER strengthen the generality claims.

- **Rich qualitative and quantitative analysis**: Beyond aggregate scores, the paper provides a survival plot for prompt quality, a prompt-length vs. performance analysis, and a fine-grained error breakdown. These analyses yield actionable insights—e.g., DeepSeek-R1 achieves top performance with the shortest prompts, and LRM-optimized prompts add concrete extraction rules and exception handling that LLMs largely miss. The convergence analysis (Figure 4) further demonstrates stability advantages.

- **Reproducibility and transparency**: The methodology is described in sufficient detail (MCTS formulation, batch prompting, error extraction via a Python interpreter, etc.), and hyperparameter settings are deferred to the appendix. The use of a fixed development set and reporting on both dev and test sets increase confidence in the reported gains.

## Weaknesses

### Fatal
None.

### Major

1. **Limited novelty of the optimization framework**: The MCTS-based prompt optimization framework is adapted directly from PromptAgent (Wang et al., 2024b) with no substantive modifications. The paper’s core contribution is the application of this existing framework to LRMs and the empirical findings. While this application is valuable, it does not introduce new algorithmic ideas. The contribution therefore lies primarily in the empirical study, which is still significant, but the paper would be stronger with a more detailed justification of why the existing method is appropriate for LRMs or with some adaptation specific to reasoning models.

2. **Low absolute performance raises questions about the adequacy of the EE setup**: Even after full MCTS optimization on ACE_med, the best argument classification F1 score is 44.26 (DeepSeek-R1 optimizer + DeepSeek-R1 task model on dev). While this is a substantial relative improvement over the ~16% no-optimization baseline, the absolute scores remain low, suggesting that either the zero-shot paradigm is inherently limited for EE or the downsampling to 10 event types and small training sets (15 or 120 examples) creates an artificially difficult setting. The paper could discuss whether the findings would hold with larger training sets or with more standard supervised fine-tuning as a baseline.

3. **Quantization of DeepSeek-R1**: The authors state that DeepSeek-R1 was quantized to 2.5 bits using UnSloth, citing minimal degradation. However, no direct evidence or benchmark is provided to demonstrate that the quantized model performs similarly to the full-precision version on event extraction or the auxiliary tasks. This is a potential confound because the paper’s conclusions hinge on comparing LRM vs LLM capabilities. If quantization disproportionately harms LRM performance, then the reported gains might be lower than what a full-precision LRM would achieve, but conversely their superiority might be even larger. The lack of validation is a concern.

4. **Limited generality validation for cross-model optimization**: In the generalization experiments (Geometric Shapes, NCBI), only the same-model optimizer setting is tested (e.g., DeepSeek-R1 optimizing DeepSeek-R1). The paper does not show whether LRM-optimized prompts also benefit LLM task models on these tasks, which would strengthen the claim that LRMs are broadly superior optimizers. Given the extensive cross-model analysis on EE, this omission is noticeable.

### Minor

- The paper uses only two LRMs (DeepSeek-R1 and o1) and two LLMs (GPT-4o, GPT-4.5). While this is a reasonable starting point, the conclusions about LRMs vs LLMs would be more robust with additional models (e.g., Gemini models, Llama-based reasoning models). The variance across models may partially reflect differences in training data or API behavior rather than reasoning capability per se.

- The error analysis (Figure 5c) categorizes errors into types, but the categories are somewhat ad hoc (e.g., “Index Events”, “Confirmation”). The paper does not define these categories precisely, nor does it quantify inter-annotator agreement if human annotation was used. A table with examples for each category would improve clarity.

### Trivial

- In Table 1, some “No Opt.” baseline values differ across sections (e.g., GPT-4o shows 12.68 for depth 1 on ACE_low but 26.30 for depth 1 on ACE_med). The large jump for GPT-4o between ACE_low and ACE_med baselines (12.68 → 26.30) is not explained—it may be due to the different training sets used for optimization, but the “No Opt.” condition presumably does not use any training data and should be consistent. This appears to be an inconsistency or omission.

## Nice-to-Haves

- A human evaluation of prompt quality (e.g., annotator ratings of clarity, completeness) would complement the automatic F1-based evaluation and better characterize what makes LRM-optimized prompts more effective.
- An analysis of the computational cost (API calls, tokens) of using LRMs as optimizers vs. LLMs would be useful for practitioners deciding whether the performance gains justify the higher cost.
- A brief discussion of why prompt length correlates differently with performance for different models (DeepSeek-R1 peaks at short prompts while o1 prefers longer ones) could be explored further.

## Novel Insights

The paper provides a clear empirical demonstration that strong reasoning ability does not eliminate the need for careful instruction design; in fact, LRMs are both more responsive to and more capable of generating high-quality prompts. The observation that DeepSeek-R1, despite being a reasoning model, achieves top performance with the shortest prompts (Figure 5b) is particularly interesting, as it suggests that concise, rule-focused instructions are more effective than verbose elaborations for this model. The survival plot (Figure 5a) further reveals that LRMs not only achieve higher peaks but also produce a larger proportion of usable prompts—a robustness property that has practical implications for automated prompt tuning in production settings. The error analysis (Figure 5c) offers a concrete mechanism: LRM-optimized prompts reduce argument span overprediction and hallucinations by adding precise extraction rules and exception cases, while LLM-optimized prompts tend to add generic formatting instructions.

## Suggestions

- Validate the quantized DeepSeek-R1 by comparing its no-optimization score with the full-precision model on a small sample of the development set, and report the difference. This would directly address the quantization concern.
- For the generalization experiments, include at least one cross-model optimization condition (e.g., an LRM-optimized prompt evaluated on an LLM task model) to test whether the superiority of LRM optimizers holds beyond same-model settings.

## Score and Decision

The paper presents a well-executed, systematic empirical study on a timely question. Its main contributions are solid empirical findings rather than novel methodology. The evidence is convincing, the analyses are thorough, and the claims are appropriately scoped. However, the modest absolute performance, the use of quantized models without validation, and the limited novelty of the optimization framework prevent it from being a top-tier contribution. It is a valuable addition to the literature and meets the acceptance threshold for a venue like ICLR.

MY FINAL SCORE: 6.0score  
MY FINAL DECISION: Accept