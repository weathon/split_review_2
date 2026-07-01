## Summary

The paper proposes Critique-RL, a two-stage reinforcement learning method for training a separate critique model that assesses and generates feedback for an actor model's responses, without requiring a stronger supervisor. The first stage optimizes discriminability (whether the critique correctly judges the original response's correctness) using a direct rule-based reward. The second stage optimizes helpfulness (constructive feedback that improves actor refinement) while preserving discriminability through regularization. Experiments on math reasoning tasks (MATH, GSM8K, AQuA) and out-of-domain sets (SVAMP, TheoremQA) show consistent gains over baselines (SFT, STaR, Retroformer, CTRL), with Qwen2.5-7B achieving up to 12.66% improvement in refined accuracy on MATH.

## Strengths

- **Clear identification of a key failure mode.** The paper convincingly demonstrates via training dynamics (Figure 3) that optimizing critique models solely with indirect rewards from actor refinement leads to either overly conservative or overly aggressive critics, because discriminability is not directly optimized. This is a well-motivated and empirically supported finding.
- **Novel and sound two-stage RL approach.** The separation of discriminability (Stage I) and helpfulness (Stage II) optimization, with explicit regularization to prevent regression, is a principled solution to the identified problem. The algorithm (Algorithm 1) is clearly explained and the rewards are well-defined.
- **Strong empirical results.** Critique-RL consistently outperforms all baselines across multiple model scales (3B, 7B), in-domain tasks, and out-of-domain tasks, often by large margins (e.g., +12% accuracy on GSM8K for 7B). The improvements in discriminability (Acc@Dis) are particularly notable.
- **Thorough ablation and analysis.** The paper systematically ablates each stage and reward component (Table 3), validating the necessity of both stages and the discrimination regularization. Additional analyses (oracle verifier, inference compute scaling, iterative improvement) further demonstrate robustness and efficiency.
- **Scalable oversight without stronger supervisors.** The method does not rely on a stronger model or human annotation for critique training, addressing a significant practical bottleneck in scalable oversight.

## Weaknesses

### Fatal
None.

### Major
- **Limited task scope in main experiments.** All in-domain and out-of-domain tasks are math reasoning (MATH, GSM8K, AQuA, SVAMP, TheoremQA). While the paper mentions summarization experiments in the appendix, the main paper does not demonstrate effectiveness on open-ended or qualitative tasks, which limits the generalizability claims. The reliance on a rule-based oracle verifier for rewards further restricts applicability to tasks with verifiable ground-truth answers.

### Minor
- **Comparison with common refinement methods not in main paper.** The paper relegates comparisons with Self-Refine, SuperCorrect, and Critic-CoT to the appendix. These are natural baselines for critique-based refinement, and their absence from the main results weakens the empirical positioning of the method. The main paper should at least summarize this comparison.
- **Training dynamics shown only for 3B model on one dataset.** Figure 3 uses Qwen2.5-3B on GSM8K. While illustrative, the reader cannot assess whether the same optimization challenges appear for larger models or other datasets. For a claim about "insufficient for training satisfactory critique models," broader evidence would be stronger.

### Trivial
- The notation in Algorithm 1 uses `r_{\text{oracle}}` but `r_{\text{oracle}}` is not formally defined in the algorithm description; it is clear from context.

## Nice-to-Haves
- Including the comparison with Self-Refine, Critic-CoT, etc., in the main paper would strengthen the evaluation.
- A small-scale experiment on a non-math task (e.g., summarization or code) in the main paper would better support the claim of generalizability.
- Discussion of how to apply the method when no rule-based oracle verifier exists (e.g., using a reward model) would broaden the impact.

## Novel Insights

Beyond the paper's own contributions, the key insight is that training a critique model through RL must explicitly decouple and jointly optimize two distinct capabilities: discriminability (assessing correctness) and helpfulness (providing actionable feedback). The paper shows that optimizing only the latter via indirect actor outcomes leads to degenerate behavior (overly conservative or aggressive critiques), and that direct discriminability rewards plus careful regularization are necessary. This insight may generalize beyond critique models to other forms of automated feedback or process supervision.

## Suggestions

- Move the comparison with Self-Refine, SuperCorrect, and Critic-CoT from the appendix to the main paper, or at least summarize the results in a sentence or table.
- Add a brief discussion on how the method could be extended to tasks where a rule-based oracle verifier is unavailable, e.g., using a learned reward model or human feedback in the loop.
- Consider showing training dynamics for the 7B model, or at least note that similar patterns were observed.

## Score and Decision

MY FINAL SCORE: <score>8.0</score>
MY FINAL DECISION: <decision>Accept</decision>