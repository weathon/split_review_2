## Summary

This paper proposes a self-evolution framework where a single language model acts as both generator and verifier, using thresholded majority voting to construct reliable preference pairs for DPO training without external supervision. The authors systematically study single-turn verification (SimpleGV), multi-turn revision (RevisionGV), iterative training, and curriculum learning, reporting improvements on synthetic logical reasoning (Knights and Knaves) and modest gains on mathematical reasoning benchmarks. The key finding is that training on easier instances can generalize to harder ones, demonstrating easy-to-hard generalization.

## Strengths

- **Simple and general framework:** The generator-verifier game formulation is intuitive, requires no external labels, environments, or task-specific reward models, and can be applied to free-form text outputs.
- **Systematic empirical study:** The paper explores multiple variants (SimpleGV, RevisionGV, iterative training, curriculum learning) with controlled experiments, providing clear ablation of each component.
- **Easy-to-hard generalization:** Demonstrating that models trained only on easier KK instances (2–3 people) transfer effectively to harder instances (4–8 people) is the most compelling result, with clear practical relevance.
- **Cost-performance analysis:** The paper provides a practical analysis of computational trade-offs, showing that moderate configurations already achieve strong results at reasonable cost and that scaling verifier compute is often more efficient than scaling generator compute.

## Weaknesses

### Fatal
None.

### Major
1. **Modest improvements on standard benchmarks:** On real-world math reasoning tasks (GSM8K, MATH500, MATHHard), the absolute gains over the base model are typically 1–2%, and on GSM8K for gemma-3-4b-it there is a slight decrease (89.2 → 89.0). The paper’s central claims are primarily supported by the synthetic KK dataset, which limits the impact of the proposed method on realistic tasks.
2. **Easy-to-hard generalization is only validated on KK:** While this is a notable finding, the paper does not demonstrate similar transfer on math benchmarks (e.g., training on simpler GSM8K problems and testing on harder MATH problems). Without such evidence, the claim of “emergent easy-to-hard generalization” remains unsubstantiated beyond a single synthetic domain.
3. **Limited comparison with recent self-evolution methods:** The paper compares against INTUITOR, Absolute Zero, and GRPO, but does not include more recent and closely related methods such as R-Zero (Huang et al., 2025) or TTRL (Zuo et al., 2025) on the same benchmarks. This makes it difficult to assess the relative effectiveness of the proposed approach compared to the current state-of-the-art in self-evolution.

### Minor
1. **Instruction-tuned base models:** The paper uses instruction-tuned variants, which already incorporate supervised signals. The claim of “without external supervision” is therefore nuanced, as the base models have undergone instruction tuning that may include preference data or human feedback.
2. **Threshold sensitivity:** Performance depends on the threshold $\tau$, which requires some tuning. While the paper notes that thresholds 0.6–0.7 work well, the need for task-specific calibration weakens the claim of full autonomy.

### Trivial
- Table 1 uses asterisks to denote results from original reports but does not include a clear footnote explaining this convention.
- Some figures (e.g., Figure 4) have small font sizes that make it hard to read the exact values.

## Nice-to-Haves
- Release of the code and generated preference datasets would improve reproducibility and facilitate adoption.
- Extending the easy-to-hard experiments to mathematical benchmarks (e.g., training on GSM8K, testing on MATH) would greatly strengthen the generality claim.
- Analysis of failure cases (e.g., why 1B models do not benefit from RevisionGV) could provide deeper insights into the conditions required for self-evolution.

## Novel Insights

The paper shows that a simple thresholded majority voting scheme can extract reliable preference signals from noisy self-verification, and that multi-turn revision (RevisionGV) consistently outperforms single-turn selection. The most interesting insight is that self-evolution on easy problems yields strong generalization to harder problems, suggesting that the model’s latent reasoning structure can be bootstrapped from simpler tasks without seeing complex examples. However, this insight is only confirmed in the synthetic KK domain.

## Suggestions
- Include comparisons with R-Zero and TTRL on the MATH and GSM8K benchmarks to better contextualize the results.
- Evaluate easy-to-hard generalization on a mathematical reasoning benchmark (e.g., train on GSM8K, test on MATH500 or MATHHard) to support the claimed insight.
- Provide a more detailed analysis of why RevisionGV fails for the 1B model while SimpleGV succeeds; this could inform the applicability of the method to smaller models.

## Score and Decision
Score: 6

MY FINAL SCORE: 6</score>
MY FINAL DECISION: Accept</decision>