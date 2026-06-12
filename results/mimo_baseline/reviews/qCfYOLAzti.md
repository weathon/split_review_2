## Summary

This paper identifies a previously underexplored failure mode in LLM unlearning called the "squeezing effect," where gradient ascent-based methods redistribute probability mass into semantically related paraphrases of the target, yielding spurious unlearning that standard metrics fail to detect. To address this, the authors propose a bootstrapping (BS) framework that incorporates the model's own high-confidence generations ("model beliefs") as auxiliary unlearning targets, instantiated at both the token level (BS-T) and sequence level (BS-S), with theoretical analysis under the AKG learning dynamics framework and experimental validation across TOFU, MUSE, and WMDP benchmarks.

## Strengths

- **Important and well-characterized problem.** The paper convincingly demonstrates that existing metrics (ROUGE, Truth Ratio, etc.) can mask spurious unlearning where models generate semantically equivalent paraphrases. The case studies in §3.1 (e.g., NPO producing "She mainly writes in English" to replace "Hsiao Yun-Hwa typically writes her books in English") are vivid and practically concerning. The empirical verification in §3.2, using beam search to show that high-likelihood regions retain more semantic similarity (Fig. 2a) and that NPO persistently maintains probability mass in these regions (Fig. 2c), provides strong evidence that this is a systematic rather than isolated problem.

- **Elegant and well-motivated solution.** The bootstrapping idea—using the model's own beliefs as forgetting targets—is intuitive, novel, and complementary to existing unlearning objectives. The two-level design (BS-T for token-level belief suppression, BS-S for sequence-level augmentation) addresses both local and global manifestations of the squeezing effect. The framework is flexible, compatible with any base unlearning loss and regularization scheme.

- **Rigorous theoretical grounding.** The analysis in §5 using the AKG learning dynamics framework is well-structured. Theorem 5.2 cleanly shows how BS-T reshapes the residual to spread repulsion across both the target and its high-likelihood neighborhood (Fig. 3), and Theorem 5.3 extends this to off-policy BS-S. This provides genuine mechanistic insight rather than post-hoc rationalization.

- **Comprehensive experimental evaluation.** Experiments span three benchmarks (TOFU, MUSE, WMDP), multiple model scales (1B–8B), and multiple forget settings (1%, 5%, 10%). The introduction of LLM-as-a-judge evaluation (Naturalness and Similarity dimensions) alongside standard metrics is a valuable methodological contribution that better captures the semantic aspects of unlearning success.

## Weaknesses

### Fatal
None.

### Major

- **Modest empirical margins on standard metrics.** While BS-S consistently achieves the best results, the improvements over strong baselines (particularly NPO) are often small. On TOFU Table 1, for Llama 3.2 3B at 10%, BS-S achieves Agg. 0.63 vs. NPO's 0.62; at 8B/10%, it's 0.64 vs. 0.63. On WMDP, the forget scores differ by only 0.01 on Bio and 0.03 on Cyber between BS-S and NPO. No confidence intervals or significance tests are provided, making it difficult to assess whether these differences are statistically meaningful. The paper's strongest case relies on the LLM-as-a-judge evaluation (Fig. 4c), which shows larger gaps on Similarity (4.3 vs. 2.8 for NPO) but involves a custom evaluation the authors designed, raising potential evaluation bias.

- **Computational overhead of BS-S is insufficiently analyzed.** BS-S requires sampling N high-confidence sequences per prompt and potentially resampling during training (on-policy variant). While the paper mentions this adds cost and that N can be adjusted, no systematic analysis of the cost-performance tradeoff is provided. For practical deployment scenarios where unlearning must be applied frequently (e.g., "report then remove" pipelines), this overhead could be significant. The training time comparison mentioned in Appx. F.6 is referenced but its conclusions are not surfaced in the main paper.

### Minor

- **The relationship between BS-T and self-distillation could be explored more.** The paper notes that BS-T "resembles self-distillation" but with the "opposite" purpose. However, the connection and differences could be more precisely delineated—e.g., does temperature tuning in BS-T play a similar role to distillation temperature, and if so, does this suggest a unified framework?

- **The Laaj evaluation framework itself lacks validation.** The paper introduces a custom LLM-as-a-judge evaluation with "Naturalness" and "Similarity" dimensions that becomes central to motivating and evaluating the method. While Laaj is referenced as aligning with human evaluation (Zheng et al., 2023), the specific prompts, rubrics, and reliability of this particular instantiation are not validated against human annotators in this work.

### Trivial
None.

## Nice-to-Haves

- An analysis of how the choice of N (number of sampled sequences in BS-S) and λ_BST interact with model scale and forget percentage would help practitioners.
- A comparison of on-policy vs. off-policy BS-S variants in the main text to clarify the practical tradeoff.
- Confidence intervals over multiple random seeds to substantiate the improvements.

## Novel Insights

The paper's central conceptual contribution is the identification and characterization of the squeezing effect as a fundamental mechanism behind spurious unlearning in GA-based methods. The observation that softmax normalization inherently drives probability mass into semantically proximate high-likelihood regions—and that standard metrics systematically fail to detect this—is a genuinely novel insight that has implications beyond the specific method proposed. The connection drawn between this effect and the model's own internal beliefs (top-k predictions and high-confidence generations) provides a principled framework for thinking about unlearning that shifts the focus from "what to forget" to "where does forgotten knowledge escape to." This reframing is likely to influence future work on both unlearning algorithms and evaluation methodology.

## Suggestions

- Include confidence intervals or standard errors across multiple runs for all reported metrics.
- Provide a concise analysis in the main text comparing BS-S computational cost (time and memory) against baselines, not just in the appendix.
- Validate the LLM-as-a-judge evaluation against human annotations on a subset of examples to establish its reliability for the specific unlearning assessment task.

## Score and Decision

The paper makes a meaningful conceptual contribution by identifying the squeezing effect and spurious unlearning, provides elegant and theoretically grounded solutions, and validates them across multiple benchmarks. The empirical improvements, while consistent, are often modest on standard metrics and lack statistical significance testing. The strongest evidence comes from the custom LLM-as-a-judge evaluation, which needs independent validation. Overall, the paper advances understanding of LLM unlearning failure modes and offers a practical framework, though the incremental nature of the gains tempers enthusiasm.

MY FINAL SCORE: <score>6.0</score>
MY FINAL DECISION: Accept