## Summary
# Final Review Report

## Summary

This paper proposes **Copy-Paste**, a generation paradigm for Retrieval-Augmented Generation (RAG) that mitigates contextual faithfulness hallucinations by maximizing lexical copying from the provided context. The core idea is that verbatim reuse of contextual fragments eliminates the semantic transformation gap where hallucinations originate, and copied spans inherently serve as attribution evidence. The approach is instantiated through a two-stage pipeline: (1) **Copy-Paste-Prompting**, comprising three prompting variants (CP-Order, CP-Link, CP-Refine) that generate high-copying responses via hard/soft constraints, and (2) **CopyPasteLLM**, which internalizes high-copying preferences through Direct Preference Optimization (DPO) using automatically constructed preference pairs from only 365 query-context samples. Additionally, the paper introduces **Context-Parameter Copying Capturing**, a token-level interpretability method extending Knowledge Token Capturing to full Chain-of-Thought analysis.

Experiments on FaithEval, ConFiQA, and PubMedQA demonstrate that CopyPasteLLM achieves 12.2%-24.5% accuracy improvements over strong baselines on counterfactual settings while requiring 50× less training data than Context-DPO. Mechanistic analysis suggests the method works by recalibrating internal confidence in parametric knowledge rather than enhancing contextual representations.

**Strengths**: The paper addresses an important problem (contextual faithfulness in RAG), proposes a clean and intuitive solution (copy-paste as a proxy for faithfulness), demonstrates impressive data efficiency (365 samples), and provides an interpretability analysis probing the underlying mechanism. The automated preference data construction pipeline is a practical contribution.

**Weaknesses**: (1) The foundational hypothesis (copying reduces hallucination) rests on a correlational observation without controlled causal evidence. (2) Statistical variance and significance testing are absent from all experimental results. (3) The comparison against GPT-4o lacks necessary experimental context. (4) The Context-Parameter Copying Capturing method's attribution mechanism conflates lexical overlap with genuine knowledge source identification. (5) Novelty positioning relative to prior work is asserted rather than systematically demonstrated, and the related-work section lacks a structured comparison matrix. External literature verification was unavailable in this run; novelty/comparison conclusions require manual verification.

## Strengths
1. **Important problem, clean intuition.** The paper tackles contextual faithfulness hallucinations in RAG — a practically significant issue, especially in high-stakes domains like medicine. The Copy-Paste paradigm is conceptually elegant: rather than asking models to paraphrase or reason about retrieved content, it encourages direct lexical reuse, which provides a natural faithfulness guarantee and built-in attribution. This simplicity is a genuine strength.

2. **Impressive data efficiency.** CopyPasteLLM achieves strong results (12.2%-24.5% improvements on FaithEval) using only 365 training samples, compared to 18,000 for Context-DPO and 32,580 for Parmomute. The automated preference data construction pipeline that converts prompting-based high-copying responses into structured DPO preference pairs is practically valuable and may reduce the annotation burden for deployment.

3. **Interpretability contribution.** The Context-Parameter Copying Capturing algorithm extends Knowledge Token Capturing to full Chain-of-Thought analysis, enabling position-aware assessment of contextual vs. parametric knowledge usage. The visualization (Figures 3 and 4) provides an intuitive demonstration that DPO training suppresses parametric knowledge confidence rather than enhancing contextual representations — a non-obvious mechanistic insight that strengthens the paper's scientific contribution.

4. **Thorough empirical scope.** The paper evaluates across multiple datasets (FaithEval, ConFiQA with three sub-settings, PubMedQA, RAGTruth), multiple base models (Llama-3-8B, Mistral-7B-v0.2, Llama-3.1-8B, Qwen2.5-72B, DeepSeek-V3), and both counterfactual and non-counterfactual settings. The consistency of the improvement across models and datasets supports the robustness of the approach.

5. **Reproducibility orientation.** The paper provides public code, detailed algorithm descriptions (Algorithms 1, 2, 4), prompting templates (Appendix L), and hyperparameter specifications (Appendix D). This commitment to reproducibility is commendable.

6. **Clear writing and structure.** The paper is generally well-organized, with clear section transitions, explicit research questions (RQ1-RQ3), and helpful visual illustrations (Figures 1 and 2) that make the pipeline easy to follow.

## Weaknesses
### W1. Correlational foundation without causal identification [Major]

The paper's central motivation — that high copying degree reduces hallucinations — is supported only by a correlational analysis on RAGTruth (Section 2.2). The observed inverse correlation between copying degree and hallucination density across six models admits several plausible confounders: (a) model capability (better models both hallucinate less and copy more), (b) task difficulty (easy questions permit more copying and inherently carry lower hallucination risk), and (c) reverse causality (models that hallucinate less may simply understand the context better, making copying a byproduct rather than a cause). The paper does not control for these confounders, nor does it present an intervention experiment that manipulates copying degree while holding other factors fixed. This weakens the logical foundation for the entire Copy-Paste paradigm. The hypothesis should be presented as correlational motivation rather than causal evidence.

**Required action**: Add a controlled analysis (e.g., per-model partial correlation controlling for question difficulty, or an intervention where prompting is used to vary copying degree on the same model and questions) and explicitly discuss confounders. At minimum, revise the abstract and introduction to avoid causal framing of what is fundamentally a correlational observation.

### W2. Missing statistical variance and significance testing [Major]

All experimental results in Tables 1, 2, and 3 are reported as point estimates without standard deviations, confidence intervals, or significance tests. Given that many metrics involve LLM-based evaluation (MiniCheck, AlignScore) that can have high variance, and that some differences are small (e.g., ~2-5 MiniCheck points), the statistical reliability of the claimed improvements is unknown. The narrative confidently states superiority over baselines, but no hypothesis test is provided.

**Required action**: Report standard deviations over at least 3 runs or bootstrap confidence intervals. Add paired significance tests (e.g., McNemar's test for hallucination detection or paired permutation test) for key comparisons, particularly the headline results on FaithEval.

### W3. Uncontrolled GPT-4o comparison [Major]

The paper highlights that CopyPasteLLM achieves 92.8% on FaithEval, "remarkably outperforming GPT-4o's reported 47.5% on this challenging subset" (Section 4.1.2). However, the experimental conditions for the GPT-4o comparison are not specified: was GPT-4o evaluated on the same test subset with the same context and prompt? Was it zero-shot without fine-tuning? Comparing a fine-tuned 8B model against an untuned API model on potentially different subsets is not a fair or informative comparison. This risks misleading readers about the method's relative strength.

**Required action**: Either provide the exact GPT-4o evaluation protocol (prompt, context, subset) and confirm comparability, or reframe the comparison as a reference point with explicit caveats about protocol differences.

### W4. Context-Parameter Copying Capturing conflates lexical overlap with knowledge source [Major]

The interpretability method (Section 3.3) classifies any token appearing in the context as "contextual knowledge" and tokens preferred in a context-free run as "parametric knowledge." This lexical-overlap definition cannot distinguish between a token the model genuinely derived from context and one that coincidentally appears in both the context and the model's parametric knowledge — which is the common case for factual knowledge. The "context-free run" proxy also changes the model's generation distribution beyond just knowledge sourcing (it may use different reasoning paths entirely). The central mechanistic claim — that CopyPasteLLM "recalibrates parametric knowledge confidence" — rests on a measurement tool with limited discriminative power.

**Required action**: Explicitly acknowledge this limitation in the main text (currently absent). Use counterfactual datasets where context contradicts parametric knowledge (as in FaithEval) as cleaner testbeds for knowledge source attribution. Frame the method as providing a relative difference measure rather than absolute source attribution.

### W5. Novelty positioning and related-work comparison are asserted rather than demonstrated [Moderate]

The Related Work section (Section 5) surveys three research directions but does not provide a structured comparison matrix showing how Copy-Paste differs from each approach across specific axes (faithfulness mechanism, attribution mechanism, data efficiency, generality). The differentiation from strong baselines (Context-DPO, CoCoLex, Canoe) is mentioned only in passing in the experiment section. Without explicit comparison, readers cannot assess the paper's novelty increment over existing work. (External literature verification was unavailable in this run; a manual novelty assessment is required.)

**Required action**: Add a comparison table (either in Related Work or an appendix) with columns for Approach, Faithfulness Mechanism, Attribution Evidence, Training Data Requirement, and Key Limitation. Explicitly position Copy-Paste's advantages on each axis.

### W6. Task formulation lacks formal trade-off operationalization [Moderate]

Section 2.1 defines the Copy-Paste task as maximizing lexical reuse while balancing faithfulness, query relevance, and fluency. However, this trade-off is described only in prose — there is no formal objective function, constraint specification, or Pareto-front characterization. How is an optimal answer defined when κ, relevance, and fluency compete? Without operationalization, the claimed "balance" is not verifiable.

**Required action**: Either specify a composite objective with explicit weights or thresholds, or clearly state that the system generates a Pareto front and all dimensions are evaluated separately.

### W7. Preference construction pipeline lacks judge validation [Moderate]

The Elo-style LLM-as-Judge tournament (Section 3.2) is a critical component of preference data construction, but the main text does not specify the judge model, prompt, or validation of judge reliability. LLM-as-Judge evaluation is known to have systematic biases (position, verbosity, self-enhancement). Without validation, the quality of the preference pairs that drive DPO training is unknown.

**Required action**: Specify the judge model, provide prompt template reference, and report judge reliability (e.g., agreement with human annotations on a held-out subset).

### W8. Copy-Paste-Prompting implementation details are underspecified [Minor]

The three prompting variants (CP-Order, CP-Link, CP-Refine) are described at a high level, but critical operational details are not in the main text: (a) how are "relevant context sentences" selected? (b) what is the composite copy score threshold for CP-Refine's stopping criterion? (c) which LLM generates the reviewer feedback? These are referenced to the appendix, but at least the selection mechanism and threshold should be stated.

**Required action**: Add one sentence per variant with the key implementation parameter (e.g., "using embedding similarity with threshold 0.7" or "until κ + 2·δ exceeds 0.85").

### W9. Conclusion overclaims beyond evidence [Minor]

The conclusion states "The copy-paste paradigm provides an elegant solution to RAG attribution challenges, where copied content serves as inherent faithfulness evidence." The "elegant solution" framing is subjective, and the claim that copied content "serves as inherent faithfulness evidence" is a design rationale rather than a validated outcome — no human evaluation studies user trust or verifiability.

**Required action**: Replace subjective and over-reaching language with evidence-bounded claims. Frame the attribution benefit as a design property rather than a validated outcome.

### W10. Reproducibility dependencies on appendix [Minor]

Several critical experimental details (preference construction algorithm, prompting templates, hyperparameters, dataset splits) are deferred entirely to the appendix. While the reproducibility statement is thorough, the main text's reliance on appendices for basic methodological details may slow understanding.

**Required action**: Keep the appendix structure but add brief inline summaries or references that allow a reader to understand the key design decisions without cross-referencing.

## Score
**Final Score: 7/10**

**Scoring rationale**: This score prioritizes research value and novelty as primary dimensions, consistent with the scoring policy.

The paper's strengths are substantial: it addresses an important practical problem (RAG faithfulness), proposes a clean and intuitive solution, achieves impressive empirical results with remarkable data efficiency, and provides mechanistic interpretability analysis. The automated preference construction pipeline is a practical engineering contribution.

However, several significant weaknesses prevent a higher score. The foundational hypothesis linking copying degree to hallucination reduction is supported only by correlational evidence without causal identification (W1). The experimental results lack statistical variance and significance testing (W2), which is a serious methodological gap for a paper making strong comparative claims. The headline GPT-4o comparison is not adequately controlled (W3). The interpretability method's attribution mechanism has limited discriminative power (W4). The novelty positioning relative to prior work relies on assertion rather than systematic comparison (W5), and external literature verification was unavailable in this run, making full novelty assessment infeasible. These issues are fixable with additional analysis, controlled experiments, and more careful claim bounding, which is why the score remains in the "accept with revisions" range rather than lower.

**The paper would benefit most from addressing W1 (causal evidence for the core hypothesis), W2 (statistical rigor), and W5 (structured novelty positioning) before any resubmission.**