## Summary
This paper proposes "Forget-to-Focus" (F2F), a two-stage domain adaptation protocol for LLMs that first performs targeted unlearning of general-domain knowledge (using a forget set derived from BookCorpus, optionally with a retain set for stability) and then fine-tunes on domain-specific data. The authors demonstrate across medical, coding, and mathematics domains—using models from 0.6B to 72B parameters—that F2F consistently outperforms standard fine-tuning and parameter-efficient baselines, and they analyze representational shifts via CKA/SVCCA to provide mechanistic evidence for why preparatory unlearning aids specialization.

## Strengths
- **Novel and well-motivated framing**: Repurposing machine unlearning as a preparatory stage for domain adaptation—rather than as a privacy tool—is a genuinely interesting conceptual contribution. The central research question (whether actively removing irrelevant knowledge improves specialization) is clearly stated and well-motivated by prior work on negative transfer.
- **Extensive experimental breadth**: The paper evaluates F2F across three distinct domains (medical, coding, math), five model families (Qwen-3 0.6B, Gemma-2B, LLaMA-3.1 8B, LLaMA-2 13B, Qwen-2 72B), four unlearning methods, multiple fine-tuning strategies (SFT, LoRA, CurlLoRA, DAPT), and three forget-set constructions (BC-Select, BC-Mixed, BC-Cosine). This breadth substantially strengthens the empirical case.
- **Significant empirical gains with representation analysis**: F2F achieves large improvements—e.g., HumanEval pass@1 improves by ~22.6 points on Qwen-0.6B and ~7.4 points on Qwen-72B over the base model. The CKA/SVCCA/Fisher/PCA analyses go beyond accuracy numbers to show that unlearning reshapes representational geometry away from generalist features, providing mechanistic insight.
- **Practical forget-set design ablation**: Comparing BC-Select (curated, no domain overlap), BC-Mixed (80/20 split), and BC-Cosine (cosine-distance-based selection) provides useful practical guidance on how forget-set quality affects downstream performance. The finding that curated forget sets consistently outperform mixed ones is actionable.

## Weaknesses
### Fatal
None.

### Major
- **No error bars or statistical significance testing**: All reported numbers are single-run results. Given the sensitivity of fine-tuning and unlearning to random seeds, data ordering, and initialization, reporting confidence intervals or standard deviations across multiple runs is essential for a paper making strong claims about "consistent" improvements. Without this, it is difficult to judge whether the observed gains are statistically meaningful or within noise.
- **Retain set contaminates the comparison**: The retain set R is described as "a small subset of the fine-tuning data" (1,000 samples). This means F2F exposes the model to domain-relevant data during the unlearning phase, effectively giving it a preview of the target domain before standard fine-tuning begins. A fairer baseline would be standard fine-tuning with the same total domain-data budget, or an ablation showing F2F without any retain set (pure GA, which the paper does include but often performs poorly). The paper does not adequately discuss this confound.
- **Incomplete mechanistic explanation**: The paper claims unlearning removes "irrelevant pretraining knowledge," but it's unclear why forgetting BookCorpus text (narrative fiction and books) would specifically help with code generation on HumanEval/MBPP or medical QA on PubMedQA. BookCorpus is not the source of domain-interfering knowledge for these tasks. The t-SNE in Figure 2 shows separation between BookCorpus and code, but this doesn't explain the mechanism—what specific knowledge is being suppressed that was causing negative transfer? This gap weakens the conceptual contribution.
- **Fragile results for smaller models**: Gemma-2B performance drops to 0.00 after unlearning (before fine-tuning), and several configurations show catastrophic degradation (e.g., LLaMA-8B GA-only HumanEval = 1.20). While the paper notes this, it doesn't provide principled guidance on when F2F is safe to apply, limiting the method's practical utility.

### Minor
- **Missing ablations on critical hyperparameters**: The number of unlearning steps T_u, the ratio λ/σ, and the learning rate are all fixed without ablation. The theoretical analysis suggests these are important (the bound depends on T_u and λ/σ), yet no empirical study supports the chosen values.
- **No compute cost analysis**: F2F adds an entire unlearning training phase before fine-tuning. The paper does not report total training cost, wall-clock time, or whether the performance gains justify the additional compute.
- **Shallow theoretical analysis**: The proposition essentially restates that gradient ascent on a strongly convex function contracts the irrelevant subspace, which is a textbook result. The corollary follows trivially. For non-convex LLM training, these convex surrogates provide limited insight. The theoretical section occupies significant space without commensurate explanatory value.

### Trivial
- Some table entries appear incomplete (e.g., Qwen 72B in Table 1 has missing values in some rows), likely a parser issue.

## Nice-to-Haves
- A comparison with knowledge distillation or task-continual-learning baselines would strengthen the positioning.
- An analysis of what the model "forgets" in embedding space—e.g., probing specific capabilities before and after unlearning—would deepen understanding.
- Reporting the downstream effect on general capabilities (e.g., MMLU or general reasoning benchmarks) after F2F, to quantify any collateral damage.

## Novel Insights
The paper's central insight—that machine unlearning can be repurposed as a preparatory intervention for domain adaptation rather than merely a privacy mechanism—is genuinely novel and potentially impactful. The empirical finding that a curated forget set (BC-Cosine) selected via cosine distance from the domain centroid performs comparably to manually curated sets offers a practical, automatable approach to forget-set construction. The representation geometry analysis (CKA/SVCCA) showing that F2F induces more pronounced representational drift than standard fine-tuning provides the first direct evidence that unlearning reshapes model geometry in ways conducive to specialization, beyond what standard fine-tuning achieves alone.

## Suggestions
- Add error bars from 3+ random seeds for all main results, especially Table 1 and Table 3.
- Add an ablation varying T_u (number of unlearning steps) and λ/σ ratio to validate the theoretical predictions empirically.
- Include a "standard fine-tuning with additional domain data" baseline equal to the retain set size to disentangle the effect of the retain set from the unlearning itself.
- Clarify the mechanism: what specific general knowledge does unlearning BookCorpus suppress that helps with coding/medical tasks? Consider analyzing attention patterns or gradient attribution to identify which knowledge pathways are disrupted.

## Score and Decision
The paper presents a novel and well-motivated idea with extensive experiments across domains, models, and scales. The empirical gains are substantial and the representation analysis adds depth. However, the lack of error bars, the retain-set contamination issue, the incomplete mechanistic explanation, and shallow theoretical analysis temper enthusiasm. These are addressable weaknesses, and the core contribution is valuable enough for a borderline acceptance.

MY FINAL SCORE: <score>6</score>
MY FINAL DECISION: <decision>Accept</decision>