## Summary

This paper conducts the first systematic study of how reasoning data—varying in diversity, scale, and quality—affects LLM performance when introduced at different training stages (pretraining vs. SFT). Using 8B hybrid Mamba2+attention models pretrained from scratch on 1T tokens, the authors demonstrate that front-loading reasoning data into pretraining creates durable advantages that SFT cannot replicate, and uncover an asymmetric allocation principle: diversity and scale matter most in pretraining while quality dominates in SFT.

## Strengths

- **Well-structured experimental design with controlled variables.** The paper maintains a fixed reasoning token budget (80B tokens) across pretraining experiments and uses a fully crossed design of 4 pretrained models × 3 SFT datasets = 12 combinations, enabling clean comparisons across training phases. The three-phase evaluation pipeline (pretraining → SFT → RL) provides a comprehensive view of how early choices propagate through the full training stack.

- **Actionable, practically useful findings.** The asymmetric principle (diversity in pretraining, quality in SFT) and the demonstration that naive SFT scaling is harmful provide concrete, implementable guidance for practitioners. The finding that high-quality pretraining data has latent effects only activated after SFT (Table 4: M_LMQ gains +4.25% over M_LDQ post-SFT despite minimal pretraining difference) is a genuinely interesting empirical observation.

- **Thorough ablation studies.** The paper systematically ablates reasoning data ratio (Table 6-7), SFT scaling strategies (Table 8), and the "catch-up" hypothesis (Table 4), each isolating a specific variable. The catch-up experiment showing that doubling SFT epochs still fails to match even the weakest reasoning-pretrained model is compelling evidence.

## Weaknesses

### Fatal
None.

### Major

- **Critical confound between data quality and data scale.** The high-quality dataset D_SHQ contains 1.2M samples while D_LDQ contains 268M samples—a ~223× difference. When D_SHQ is used in pretraining, it must be repeated extensively to fill 80B reasoning tokens, which could cause severe overfitting on a small dataset. This makes it impossible to disentangle whether the weaker performance of M_SHQ stems from lower quality, lower diversity, or simply excessive repetition. The paper's central claim that "diversity matters more than quality in pretraining" is undermined by this confound. A fair comparison would require matching dataset sizes or controlling for repetition rate.

- **RL evaluation is only conducted on two extreme models.** Table 3 compares only M_base and M_LMQ after RL, omitting M_SHQ and M_LDQ. Since the paper's headline claim (+19% gain) comes from this comparison, and since the full matrix of 12 SFT models exists, the selective RL evaluation weakens the strongest result. The 19% figure is also specific to expert-level reasoning benchmarks after RL, while the pretraining-only gains (Table 1) are a more modest ~8%—the paper could be more transparent about which number it emphasizes.

- **Single architecture and model scale for main results.** All main experiments use an 8B hybrid Mamba2+attention model. While a 1.2B Transformer result is mentioned in the appendix, the generalizability of findings to standard dense Transformers at larger scales (e.g., 70B+) remains unestablished. Given that the paper claims to provide "a principled guide for strategically allocating data across the entire training pipeline," the narrow architectural scope limits the strength of this guidance.

### Minor

- **No cost-efficiency analysis.** The paper does not discuss whether the compute spent on reasoning-enriched pretraining is more efficient than using that compute for additional general pretraining tokens followed by more intensive SFT. The 80B reasoning tokens represent a significant portion of the 1T token budget; understanding the compute-performance Pareto frontier would strengthen the practical contribution.

- **SFT evaluation benchmarks differ from pretraining benchmarks.** The pretraining evaluation uses standard benchmarks (ARC, HellaSwag, HumanEval, etc.) while SFT evaluation uses different, harder benchmarks (AIME, GPQA, LiveCodeBench). While this is partially justified by the shift in evaluation focus, it makes cross-phase comparisons indirect and complicates interpretation of claims like "the advantage is amplified post-SFT."

- **The "catch-up" test is limited in scale.** Doubling SFT epochs (Table 4) is a relatively modest intervention. The claim that "SFT cannot compensate for a weak foundation" would be stronger if tested with substantially more SFT data (e.g., 5-10× more high-quality samples), not just 2× epochs on the same data.

### Trivial
None.

## Nice-to-Haves

- A comparison of the total compute cost of each strategy (pretraining with reasoning data + standard SFT vs. standard pretraining + heavy SFT) would make the findings more actionable for practitioners with fixed compute budgets.
- Evaluating general capabilities (knowledge, multilingual, instruction-following) after RL to ensure reasoning front-loading doesn't degrade other abilities at the final stage.

## Novel Insights

The latent effect of high-quality pretraining data is a genuinely novel observation: M_LMQ shows only marginal improvement over M_LDQ at the pretraining stage, but after SFT with the same high-quality data, it reveals a +4.25% advantage. This suggests that pretraining can instill dormant capabilities that are only activated by alignment—a finding that has implications for how we think about the interaction between training phases and could motivate new research into phase-aware data curation. The asymmetric allocation principle (diversity for pretraining, quality for SFT) is also a useful empirical contribution, though it is somewhat confounded by the scale differences between the datasets used.

## Suggestions

- Address the scale-quality confound by either (a) subsampling D_LDQ to match D_SHQ's size, or (b) upsampling D_SHQ with controlled augmentation, then re-running the key pretraining comparison.
- Run RL on the full matrix of SFT models (or at least M_SHQ and M_LDQ in addition to M_base and M_LMQ) to validate that the +19% claim generalizes across pretraining conditions.
- Include a compute-normalized comparison showing performance as a function of total training FLOPs for each strategy.

## Score and Decision

This paper addresses an important and underexplored question with a well-designed experimental framework. The core findings—front-loading reasoning, the asymmetric principle, and the latent quality effect—are practically useful and well-supported by the data. However, the critical confound between dataset scale and quality in the pretraining comparison, the selective RL evaluation, and the single-architecture scope limit the strength of the conclusions. The paper is a solid empirical contribution that would benefit from addressing the major confounds before the claims can be fully trusted.

MY FINAL SCORE: <score>6.0</score>
MY FINAL DECISION: Accept