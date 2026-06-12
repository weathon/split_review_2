## Summary

This paper proposes a self-evolution framework where a single language model acts as both generator and verifier to construct preference data for fine-tuning without external supervision. The authors introduce thresholded majority voting to extract reliable signals from noisy self-verification and explore both single-turn (SimpleGV) and multi-turn (RevisionGV) generator-verifier games. Experiments on logical reasoning (Knights and Knaves) and mathematical reasoning benchmarks (GSM8K, MATH, TabMWP) show consistent improvements over base models, with accuracy on KK rising from 31.0% to 44.8% through curriculum learning, and demonstrate emergent easy-to-hard generalization.

## Strengths

- **Clean and well-motivated framework**: The paper systematically studies a fundamental question—whether a single model can self-improve without external supervision—and provides a clear, principled approach through generator-verifier games. The thresholded majority voting method is a simple yet effective solution to the noisy self-verification problem.

- **Comprehensive experimental analysis**: The paper goes beyond simple accuracy reporting to examine multiple dimensions: model size scaling (1B, 4B, 12B), data size effects (5K-40K samples), iterative training, curriculum learning, and cost-performance trade-offs. This thorough characterization provides practical insights for practitioners.

- **Demonstration of easy-to-hard generalization**: The finding that models trained only on easier KK instances (2-3 people) generalize effectively to harder ones (4-8 people) is a notable and non-trivial result. This suggests the method captures genuine reasoning improvements rather than just memorization.

- **Competitive results without external signals**: SimpleGV achieves performance competitive with methods that use online RL, external environments, or supervised rewards, despite being fully offline and requiring no external labels. For example, on GSM8K with Qwen2.5-7B, SimpleGV (90.6%) outperforms INTUITOR (87.3%), AZR (84.0%), and GRPO (82.9%).

## Weaknesses

### Fatal
None.

### Major
- **Limited comparison to self-consistency baselines**: The paper does not compare against simple self-consistency or majority voting at inference time, which is a standard baseline for improving reasoning without training. The gains from SimpleGV could partially reflect the benefit of ensembling multiple generations rather than genuine self-evolution. A comparison showing that training with GV-generated data outperforms inference-time majority voting with the same compute budget would strengthen the claims.

- **No ablation on the necessity of DPO training**: The paper does not include a baseline where the model simply uses the verifier at inference time (e.g., generating multiple candidates and selecting the one the verifier judges best) without any fine-tuning. This would isolate whether the improvements come from the training signal or from the verifier's selection ability.

- **Potential data contamination concerns**: The paper uses OpenThoughts3 for training on mathematical reasoning tasks, but OpenThoughts3 may contain problems that overlap with the evaluation benchmarks (GSM8K, MATH, TabMWP). The paper does not discuss deduplication or contamination analysis, which is critical for self-evolution claims where the model generates its own training data from prompts that may resemble test problems.

### Minor
- **The cost analysis (Figure 5) is somewhat superficial**: While the paper notes that scaling verifier computation is more cost-effective than scaling generator computation, it does not provide a concrete cost model or practical recommendations for practitioners. A simple table showing total FLOPs or inference calls for different configurations would be more actionable.

- **The 1B model results are weak and somewhat undermine the generality claim**: For the 1B model, SimpleGV barely improves over the base (7.8% → 8.4%), and RevisionGV actually performs worse than SimpleGV. The paper acknowledges this but does not explore why or what conditions are necessary for self-evolution to work.

### Trivial
- The paper uses "gamma-34b-it" in Table 2 instead of "gemma-3-4b-it" (likely a typo from the parser).

## Nice-to-Haves

- An analysis of what types of errors the verifier makes (false positives vs. false negatives) and how thresholding affects each type would deepen understanding of the method.
- A comparison with supervised fine-tuning on the same amount of ground-truth data would help quantify the gap between self-evolution and supervised methods.
- Discussion of whether the method works for non-reasoning tasks (e.g., summarization, creative writing) would broaden the impact.

## Novel Insights

Beyond the paper's own contributions, a genuinely novel observation is that **self-verification accuracy improves after training on self-generated preference data** (Figure 2), demonstrating a co-evolution dynamic where better generation leads to better verification and vice versa. This suggests that the generator and verifier roles are not independent but mutually reinforcing, which has implications for understanding how self-supervised reasoning improvement might work in principle. The paper also provides empirical evidence that **easy-to-hard generalization emerges naturally from self-evolution without explicit curriculum design**, which is a non-obvious finding given that the model only sees easier instances during training.

## Suggestions

- Add a baseline comparing SimpleGV against inference-time self-consistency (majority voting) with the same number of generations to isolate the effect of training.
- Include a deduplication analysis between OpenThoughts3 training prompts and evaluation benchmarks, or use a training set with guaranteed non-overlap.
- Provide a concrete cost comparison (e.g., total inference FLOPs or API calls) for different configurations in Figure 5 to make the cost-performance trade-off actionable.

## Score and Decision

The paper makes a solid contribution by systematically studying a simple yet effective self-evolution framework, providing thorough experimental analysis across multiple dimensions, and demonstrating non-trivial findings like easy-to-hard generalization. The weaknesses (missing baselines and contamination concerns) are addressable and do not invalidate the core claims. The work is well within the scope of ICLR and provides value to the community studying self-improvement and reasoning in language models.

MY FINAL SCORE: <score>6</score>
MY FINAL DECISION: <decision>Accept</decision>