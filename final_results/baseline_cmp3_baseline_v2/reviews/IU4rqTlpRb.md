## Summary

This paper investigates why machine unlearned models recover forgotten information when fine-tuned on benign data—a phenomenon called *benign relearning*. Through controlled experiments on TOFU and BLUR benchmarks, the authors show that **syntactic similarity** (surface-level structural overlap) is a stronger and more consistent driver of relearning than topical relevance, which prior work had emphasized. They further demonstrate that unlearning disproportionately suppresses template/token patterns rather than the actual keywords, and propose **syntactic diversification**—paraphrasing forget queries into heterogeneous syntactic forms—to break this structural rigidity. The approach improves forgetting, model utility, and robustness against benign relearning.

## Strengths

- **Clear, well-motivated research question.** The paper identifies a real and practically important vulnerability in machine unlearning—benign relearning—and provides a rigorous analysis that challenges the prevailing topical-relevance account.
- **Controlled experimental design.** The construction of syntactically similar vs. topically relevant relearn sets on TOFU is clean, and the authors carefully correct for confounds in prior evaluations (e.g., unequal training budgets and non-monotonic recovery curves) before drawing conclusions.
- **Evidence for the mechanism.** The representation similarity, gradient similarity, and loss-ratio analyses (Figures 5 and 6) convincingly show *why* syntactic overlap drives recovery, and the template-vs-keyword suppression story is both intuitive and well-supported.
- **Practical and effective remedy.** Syntactic diversification is simple, uses off-the-shelf LLMs, and yields substantial improvements in relearning robustness while also reducing utility degradation. The ablation on unlearning steps (Figure 8) is particularly compelling.

## Weaknesses

### Fatal
None.

### Major
1. **Generality of the syntactic similarity measure.** The paper relies entirely on Levenshtein distance to quantify syntactic similarity. While this captures surface-level edit distance, it does not reflect higher-order syntactic structures (e.g., parse trees, dependency relations) that could also matter. The Appendix mentions alternatives but does not evaluate them. The claim that syntax is the "primary driver" might be nuanced if other structural metrics correlate differently across benchmarks.
2. **Limited diversity of benchmarks for the core claim.** The controlled comparison of topical vs. syntactic relearning is conducted only on TOFU (synthetic biographical QA). While the authors revisit BLUR benchmarks to show that syntactic similarity explains prior results, the controlled experiment does not include benchmarks like WMDP, WHP, or RWKU in the same fashion. It would strengthen the paper to show that syntactic similarity is also decisive on these more diverse datasets under comparable control.
3. **Dependence on an external paraphrase model (GPT-4o).** The syntactic diversification method requires a high-quality paraphrasing LLM and a manual filtering step (with a similarity threshold). This may not be reproducible or cost-effective for every practitioner, and the paper does not analyze sensitivity to the choice of paraphrasing model or threshold. Minor changes in paraphrase quality could affect unlearning robustness.

### Minor
- The keyword-based “Relearn Success Rate” is a binary metric (exact author name appears). This could miss partial recoveries. ROUGE-L is used elsewhere, but the main TOFU experiments use only the binary metric. A continuous metric would provide finer-grained signal.
- The loss-ratio analysis is performed only for GA, not for NPO or SCRUB. It would be useful to see whether the same template-keyword imbalance occurs across methods.

### Trivial
- Figure 3 markers (stars and squares) are small and somewhat hard to distinguish in print. This does not affect the argument.

## Nice-to-Haves
- An experiment that applies diversification to *multiple* unlearning methods (beyond GA) would further demonstrate the generality of the remedy.
- A discussion of possible failure modes of diversification (e.g., if paraphrasing inadvertently removes essential constraints needed for forgetting) would strengthen the paper.
- Providing the paraphrasing prompts used for GPT-4o would aid reproducibility.

## Novel Insights

Beyond the paper’s own contributions, the key insight is that **unlearning mechanisms disproportionately suppress surface-level template patterns rather than the actual factual content (keywords).** This asymmetry creates a structural vulnerability: any fine-tuning data that shares the same syntactic scaffolding can rapidly restore the template, after which the keywords naturally reappear. This view reframes benign relearning not as a semantic memory phenomenon, but as a consequence of how gradient-based unlearning interacts with rigid input/output formats. The corollary—that breaking syntactic homogeneity in the forget set forces the optimization to target the real content—is a genuinely useful design principle for robust unlearning.

## Suggestions
- In the main controlled experiment, include a continuous metric (e.g., ROUGE-L or probability of the target keyword) alongside the binary Relearn Success Rate. This would provide a more complete picture of recovery strength.
- For the diversification procedure, analyze sensitivity to the similarity filtering threshold (e.g., vary the threshold and report the trade-off between diversity and semantic preservation).
- Test diversification on at least one additional dataset (e.g., a WMDP subset) to demonstrate transferability beyond TOFU.

## Score and Decision

**Score: 8**

**Decision: Accept**

The paper makes a clear, well-supported, and practically important contribution to the understanding of machine unlearning failures. It corrects a misconception in the literature (topical relevance as the primary driver), provides mechanistic insight, and offers a simple yet effective remedy. The empirical work is thorough and the reasoning is sound. While there are minor limitations regarding the generality of the syntactic metric and the dependence on GPT-4o, these do not undermine the core contributions. The paper merits acceptance.

MY FINAL SCORE: <score>8</score>  
MY FINAL DECISION: <decision>Accept</decision>