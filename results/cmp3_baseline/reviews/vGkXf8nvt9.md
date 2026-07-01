## Summary

The paper proposes *Forget-to-Focus (F2F)*, a two-stage protocol that first applies machine unlearning (e.g., gradient ascent on a “forget set” with optional retention) to a pretrained LLM, then fine-tunes on a domain-specific dataset. Experiments across coding, mathematics, and medical domains with models from 0.6B to 72B parameters show that F2F consistently outperforms standard fine-tuning, DAPT, and LoRA baselines. The authors also analyze representational geometry via CKA and SVCCA to argue that unlearning reshapes internal representations away from generalist features.

## Strengths

- **Novel framing of unlearning for domain adaptation.** Repurposing machine unlearning—traditionally a privacy tool—as a preparatory step for fine-tuning is a creative and underexplored idea. The paper clearly motivates why suppressing irrelevant pretraining knowledge could reduce negative transfer.
- **Extensive empirical scope.** Experiments cover three diverse domains (coding, math, medical), multiple model families (Qwen, LLaMA, Gemma) and scales (0.6B–72B), and several unlearning variants (GA+GD, GA-only, NPO, GA+KL). The consistent performance gains across settings strengthen the claim.
- **Representational analysis.** The use of CKA and SVCCA to measure representational drift provides a mechanistic window into how unlearning alters internal representations, going beyond surface-level accuracy comparisons.

## Weaknesses

### Major

1. **Uncontrolled training budget.** The F2F pipeline adds an unlearning phase before fine-tuning, meaning it uses strictly more gradient steps than standard fine-tuning. The paper does not control for total compute: e.g., fine-tuning the baseline for more epochs or with a larger learning rate might close the gap. Without such a control, the observed gains could be attributed to additional training rather than to the unlearning intervention itself.

2. **Baseline hyperparameter tuning is not reported.** The paper uses a uniform learning rate (2e-5) for fine-tuning across all models and methods. It is unclear whether the baselines (SFT, DAPT, LoRA) were individually tuned. If the baselines are suboptimal, the reported improvements from F2F may be inflated. A fair comparison requires reporting that baselines were tuned or at least that the same search procedure was applied.

3. **Forget set is small and not clearly representative of pretraining knowledge.** The forget set is drawn from BookCorpus (100–1000 samples), which is a tiny fraction of the massive pretraining corpora used for modern LLMs. The paper does not demonstrate that this small set actually captures “irrelevant general knowledge” that interferes with domain specialization. The gains might instead come from a regularization effect or from the model simply seeing additional data. An ablation using a random set of the same size (without unlearning) would help isolate the effect.

4. **Missing F2F results in Table 2.** Section 4.2 is titled “F2F w/ Fine-Tuning Variants” but Table 2 only shows baseline fine-tuning methods (SFT, LoRA, CurlLoRA, DAPT) without any F2F column. This makes the section’s purpose unclear and fails to directly support the paper’s main claim. The reader cannot see how F2F compares to these variants in the medical domain from that table.

5. **Figure 3 is poorly described.** The figure caption and text do not clearly explain what the bars represent (e.g., are they after unlearning only, or after unlearning + tuning?). The legend mentions “Tuning” and “Unlearning” but the mapping to the bars is ambiguous. This obscures the key comparison between unlearning variants.

### Minor

- The theoretical proposition (Section 2) is derived for convex linear models and does not directly apply to non-convex LLM training. While it provides intuition, the paper does not bridge this gap or validate the assumptions (e.g., orthogonal subspace decomposition) in practice.
- The paper claims “first comprehensive study” but does not discuss prior work on active forgetting during pretraining (Chen et al. 2023a) in sufficient depth to differentiate the contribution. The novelty is still clear, but the positioning could be sharper.

### Trivial

- Some table formatting issues (e.g., Table 1 has an extra empty column) and figure axis labels are hard to read, but these do not affect the scientific content.

## Nice-to-Haves

- A controlled experiment where the baseline fine-tuning is given the same number of total gradient steps as F2F (unlearning + fine-tuning) would directly address the training-budget concern.
- An ablation using a random forget set (without gradient ascent) would help confirm that the unlearning operation itself, not just exposure to additional data, drives the improvements.
- Reporting calibration metrics (e.g., expected calibration error) for all domains, not just medical QA, would strengthen the claim about improved calibration.

## Novel Insights

None beyond the paper’s own contributions.

## Suggestions

- Add a compute-controlled baseline: fine-tune the base model for the same total number of steps as the F2F pipeline (unlearning steps + fine-tuning steps) and report the results.
- Perform an ablation where the “forget set” is replaced by a random set of the same size but without gradient ascent (i.e., standard fine-tuning on that set) to isolate the effect of unlearning.
- Clarify Figure 3: ensure the legend and axis labels unambiguously indicate whether the bars show performance after unlearning only or after unlearning + tuning.
- Include F2F results in Table 2 or restructure Section 4.2 to directly compare F2F with fine-tuning variants.

## Score and Decision

**Score:** 4.0  
**Decision:** Reject

MY FINAL SCORE: <score>4.0</score>
MY FINAL DECISION: <decision>Reject</decision>