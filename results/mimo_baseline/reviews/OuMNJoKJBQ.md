## Summary

This paper investigates why current LLM safety alignment methods are vulnerable to jailbreak attacks, proposing that they rely on shallow refusal heuristics rather than deep reasoning. Through causal intervention experiments (deactivating reasoning-critical neurons), the authors demonstrate that alignment behavior is largely independent of reasoning capabilities. They then construct a Chain-of-Thought safety fine-tuning dataset and propose Alignment-Weighted DPO (AW-DPO), which decomposes responses into reasoning and response segments and assigns distinct preference weights to each, yielding more fine-grained preference optimization.

## Strengths

- **Insightful causal intervention analysis (Section 3):** The linear probing and neuron deactivation experiments provide compelling empirical evidence that safety alignment in current LLMs does not depend on deep reasoning capabilities. This diagnostic contribution—showing reasoning task accuracy drops to chance after deactivating reasoning-critical heads while alignment accuracy remains near 100%—is well-designed and informative for the community.

- **Comprehensive and multi-faceted evaluation:** The paper evaluates across four model families/sizes (Llama-2-7B, Llama-3.2-3B, Llama-3.1-8B, Mistral-7B), 20 jailbreak attack types organized into categories, and compares against numerous baselines including recent advanced methods (SAFECHAIN, Representation Rerouting, STAIR). The transferability experiments (Table 3) and the prefix attack robustness test (Section 5.7) further strengthen the evaluation.

- **Practical dataset contribution:** The construction and planned release of a CoT safety alignment dataset that balances both safety and utility examples is a meaningful contribution, especially given that many prior CoT alignment works do not release their datasets.

- **Thorough ablation studies:** Sensitivity analysis on the scaling factor α (Table 4) and learning rate (Table 5) provides useful practical guidance, showing robustness to α but expected sensitivity to learning rate.

## Weaknesses

### Fatal

None.

### Major

- **Logical gap between diagnosis and treatment:** The causal intervention demonstrates that current alignment does *not* rely on reasoning. The proposed remedy is to *add* reasoning to alignment. However, the paper does not adequately bridge this gap: if alignment is independent of reasoning, why would forcing the model to reason during refusal improve alignment robustness? The paper needs a clearer argument for why reasoning-augmented alignment addresses the identified vulnerability (shallow pattern matching) rather than merely adding a surface-level improvement.

- **Marginal and statistically unvalidated improvements of AW-DPO over standard DPO:** The differences between DPO and AW-DPO are often very small when ASR is already low: Llama-3.2-3B (1.04% vs 0.58%), Llama-3.1-8B (1.00% vs 0.81%). On Mistral-7B, DPO has a standard deviation of ±8.75 on multilingual attacks, making the DPO vs AW-DPO comparison unreliable. No multiple-seed runs or statistical significance tests are provided, making it impossible to determine whether these differences are meaningful or within noise.

- **Unvalidated LLM-as-judge for alignment weights:** The entire AW-DPO pipeline relies on an LLM judge to score harmfulness of reasoning traces and responses, which directly determines the alignment weights. The paper provides no validation of the judge's reliability, inter-rater consistency, or sensitivity to judge choice. If the judge is noisy or biased, the weighting mechanism could be ineffective or counterproductive.

### Minor

- **Comparison with STAIR-DPO-3 is incomplete:** The authors dismiss STAIR-DPO-3 as more expensive (3 rounds of training), but it achieves significantly higher utility (73.34% vs 58.27%) with comparable safety (1.13% vs 0.81% ASR). The trade-off between training cost and quality deserves more nuanced discussion.

- **No comparison against other weighted/modulated DPO variants:** Methods like IPO, KTO, SimPO, and other DPO modifications have been proposed. Comparing against these would help situate AW-DPO's contribution more precisely.

- **The 15% error case motivation is not directly validated:** The paper claims AW-DPO targets the ~15% of failure cases involving reasoning-answer mismatches (Figure 3a), but does not show that AW-DPO specifically improves on these cases versus standard DPO. A targeted evaluation on these specific failure modes would strengthen the argument.

### Trivial

Minor table formatting inconsistencies (likely parser artifacts).

## Nice-to-Haves

- A qualitative analysis of AW-DPO training examples showing how the alignment weights shift attention to the problematic component, with before/after examples.
- Analysis of whether AW-DPO's improvements come from better reasoning traces, better final responses, or both.
- Sensitivity analysis to the choice of LLM judge.

## Novel Insights

The causal intervention experiment revealing that deactivating reasoning-critical neurons leaves alignment behavior intact while degrading reasoning performance is genuinely novel and provides a clear, interpretable explanation for why current alignment methods are brittle against sophisticated jailbreak attacks. The decomposition of unsafe responses into reasoning-answer consistency categories (correct reasoning + unsafe answer, incorrect reasoning + safe answer) is a useful diagnostic framework, though the proposed method's effectiveness at addressing these specific categories remains under-validated.

## Suggestions

- Add multiple random seeds and statistical significance tests for all AW-DPO vs DPO comparisons, especially when ASR values are very low.
- Validate the LLM judge by comparing its scores against human annotations on a subset of examples.
- Provide a clearer causal argument for why reasoning augmentation improves alignment, given that the paper's own experiments show the two are independent.
- Add a targeted evaluation showing AW-DPO specifically reduces the 15% reasoning-answer mismatch failure cases.

## Score and Decision

The paper presents an interesting diagnostic (causal intervention) and a reasonable method (AW-DPO), with comprehensive evaluation across models and attack types. However, the core AW-DPO improvements over standard DPO are marginal and not statistically validated, the LLM judge used for weighting is unvalidated, and there is a logical gap between the paper's own diagnosis (alignment doesn't use reasoning) and its treatment (add reasoning to alignment). These issues prevent confident acceptance.

MY FINAL SCORE: <score>4</score>
MY FINAL DECISION: <decision>Reject</decision>