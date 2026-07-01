## Summary

This paper introduces *persona vectors*—linear directions in LLM activation space corresponding to personality traits—extracted via an automated pipeline from natural-language trait descriptions. The authors demonstrate that these vectors enable monitoring of persona shifts during deployment and finetuning, mitigation of unwanted shifts via inference-time or preventative steering during training, and pre-finetuning data screening to flag problematic samples. Experiments across two 7-8B models and three negative traits (evil, sycophancy, hallucination) show strong correlations between activation shifts along persona vectors and behavioral trait expression.

## Strengths

- **Timely and important problem.** Unintended persona shifts in LLMs have caused real-world incidents (Bing, Grok, GPT-4o sycophancy). The paper directly addresses a pressing safety concern with practical tools.
- **Comprehensive application suite.** The paper demonstrates four distinct use cases (monitoring, inference-time steering, preventative steering, data screening) from a single extracted vector, showing broad utility.
- **Preventative steering is a novel and well-motivated contribution.** Steering *toward* the undesired direction during training to counteract drift, while steering *against* it at inference, is a clever inversion of standard practice. The case study on hallucination during fact acquisition convincingly shows that preventative steering preserves capabilities better than inference-time steering.
- **Thorough empirical validation.** Experiments span two model families (Qwen2.5-7B, Llama-3.1-8B), multiple traits, and multiple dataset types (explicit trait-eliciting, emergent misalignment-like). Correlations are consistently high (r=0.76–0.97) and statistically significant.
- **Pre-finetuning data screening is practically valuable.** The projection difference metric predicts post-finetuning trait expression before training, and sample-level detection separates trait-inducing from benign data. This could enable proactive safety filtering.

## Weaknesses

### Fatal
None.

### Major
- **Incremental methodological novelty.** The core technique (contrastive pairs → difference of means in activation space) is well-established in prior work on activation steering (Turner et al., Zou et al., Wu et al.). The automated pipeline using an LLM to generate artifacts is a practical engineering contribution but not a deep methodological advance. The paper would benefit from clearer articulation of what is new beyond systematization.
- **Heavy reliance on LLM-based evaluation.** Both extraction (Claude 3.7 Sonnet) and evaluation (GPT-4.1-mini) depend on LLM judges. While the authors validate against human evaluators in the appendix, the core results are mediated by a black-box judge that may share biases with the target models. This is a significant concern for reproducibility and objectivity, especially for traits like "evil" where judge calibration is critical.

### Minor
- **Monitoring correlation is driven by coarse prompt differences.** The strong correlations (r=0.75–0.83) in Section 3.3 arise primarily from distinguishing between clearly different system prompts (trait-encouraging vs. trait-discouraging). Within-prompt-type correlations are more modest, limiting the method's utility for detecting subtle deployment-time shifts. The paper acknowledges this but does not fully discuss implications for real-world monitoring.
- **Preventative steering does not fully eliminate shifts for explicit trait-eliciting datasets.** The method reduces but does not eliminate trait expression for datasets intentionally designed to induce a trait (e.g., Evil II). Multi-layer steering helps, but the claim of "avoiding" shifts is somewhat overstated.
- **Data screening cost.** The projection difference metric requires generating base model responses for all training samples, which is expensive for large datasets. The approximations in Appendix K are acknowledged but not thoroughly evaluated against the full method.

### Trivial
- The paper focuses on three negative traits; positive traits are relegated to the appendix. While justified by safety concerns, the generality claim is slightly weakened.

## Nice-to-Haves
- A deeper analysis of *why* preventative steering works: does it change the loss landscape, or simply shift the initialization? Ablation studies on the steering coefficient schedule during training would strengthen the mechanistic understanding.
- Comparison of data screening against simpler baselines (e.g., perplexity-based filtering, keyword matching) to contextualize the added value of activation-based screening.
- Evaluation on larger models (e.g., 70B) to test scalability of the approach.

## Novel Insights

None beyond the paper's own contributions. The key insight—that finetuning-induced persona shifts are mediated by linear directions and can be counteracted by steering during training—is a useful synthesis of existing ideas (activation steering + training-time intervention) rather than a fundamentally new discovery.

## Suggestions
- Provide a more detailed comparison of the automated pipeline with the closest prior work (Wu et al. 2025) to clarify the specific novelties.
- Report within-prompt-type correlations for monitoring (as done in Appendix E.2) more prominently, and discuss the practical limitations for deployment monitoring.
- Consider evaluating on a held-out set of traits not seen during pipeline development to better assess generality.

## Score and Decision

**Score:** 6.5  
**Decision:** Accept

The paper is a solid, well-executed contribution to an important problem. It systematizes and extends existing activation steering techniques into a practical toolkit for LLM safety. While the methodological novelty is moderate, the thorough empirical validation, the novel preventative steering method, and the pre-finetuning data screening application provide sufficient value for acceptance. The reliance on LLM judges and the incremental nature of the core technique prevent a higher score.

MY FINAL SCORE: <score>6.5</score>
MY FINAL DECISION: <decision>Accept</decision>