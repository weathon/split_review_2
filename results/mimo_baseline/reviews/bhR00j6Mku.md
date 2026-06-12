## Summary

This paper presents the first systematic study of benchmark contamination detection in Large Reasoning Models (LRMs), identifying two contamination scenarios: (I) SFT contamination during base-to-LRM transition that is initially detectable but can be concealed through subsequent GRPO training, with theoretical and empirical evidence that PPO-style importance sampling/clipping is the root cause; and (II) extensive SFT contamination with CoT applied to advanced LRMs, which yields significant performance inflation while leaving detection methods performing near random guessing. The paper evaluates 10 representative detection methods across 6 reasoning benchmarks and proposes a theoretical framework explaining the concealment mechanism.

## Strengths

- **Novel and important research question.** This is the first systematic study of contamination detection fragility in LRMs, a topic of immediate practical importance given the competitive pressure on LRM leaderboards. The two-stage framing (pre-LRM and post-LRM) is well-motivated and cleanly separates distinct failure modes of detection methods.

- **Strong theoretical contribution with clean empirical validation.** The theoretical analysis isolating PPO-style clipping as the root cause of concealment is well-constructed. The ablation comparing RAFT (no concealment) vs. RAFT++ and GRPO (concealment) with and without clipping (Tables 2–3) provides clean evidence that directly validates the theory. The finding that removing clipping from GRPO/RAFT++ eliminates concealment is a sharp, falsifiable prediction confirmed empirically.

- **Comprehensive experimental design.** The paper evaluates 10 detection methods spanning four categories (generation-based, perturbation-based, reference-based, reference-free), uses multiple base models (Qwen2.5-7B-Instruct, Llama-3.1-8B-Instruct), four advanced LRMs (DeepSeek-R1-Distill variants and OpenThinker), and six reasoning benchmarks. The controlled experiment ruling out "forgetting" as an alternative explanation (additional clean SFT still detects contamination, clean+contaminated RL still conceals) strengthens the causal claim.

- **Clear practical implications.** The paper convincingly demonstrates that LRMs present a fundamentally different contamination landscape than standard LLMs: RL algorithms commonly used to train LRMs can inherently conceal SFT contamination, and CoT contamination on advanced LRMs generalizes to unseen questions rather than memorizing specific sequences.

## Weaknesses

### Fatal
None.

### Major

- **Limited sample sizes for some benchmarks raise variance concerns.** AIME24 and AIME25 each have only ~30 questions, meaning the member/non-member splits yield ~15 samples each. While this is a consequence of the benchmark size rather than a design choice, it means the reported AUROCs for these specific benchmarks may have substantial variance, potentially affecting the reliability of per-benchmark conclusions. The paper would benefit from reporting confidence intervals or performing bootstrap analysis, particularly for the AIME datasets.

- **Stage II analysis lacks depth on why generalization occurs.** The paper observes that contaminated LRMs show increased confidence on both members and non-members (Figure 4) and attributes this to LRMs "internalizing underlying knowledge and reasoning processes" rather than memorizing. However, this explanation is not fully developed or empirically tested. For instance, if contamination teaches generalizable reasoning patterns, one would expect the effect to be proportional to the difficulty/novelty of non-member questions—the paper does not examine whether detection improves for out-of-distribution questions that are sufficiently different from the contaminated set.

### Minor

- **The GRPO concealment experiment uses relatively few RL steps (64–156).** While the paper argues that even this limited training causes substantial concealment, and notes that practical models use far more steps, the relationship between concealment and training steps beyond 156 is extrapolated rather than demonstrated. A longer training run would strengthen the practical implications.

- **Only one detection metric is ablated for the theoretical validation.** Table 3 only reports the Loss detector for the RAFT/RAFT++/GRPO ablation. Showing that other detection methods (Min-K%, Max-K%, LiRA) exhibit the same pattern with clipping ablation would strengthen the claim that the mechanism is detector-agnostic rather than specific to loss-based methods.

### Trivial
None.

## Nice-to-Haves

- Reporting AUROC confidence intervals across bootstrap resamples, especially for low-sample-size benchmarks like AIME.
- Ablating the concealment effect as a function of contamination strength (e.g., fraction of benchmark contaminated) to characterize the boundary conditions.
- Examining whether contamination detection methods designed specifically for generation diversity (rather than memorization) could partially mitigate Stage II failure.

## Novel Insights

The paper's key novel insight is that the PPO-style clipping mechanism—widely treated as a mere training stabilizer—has the side effect of suppressing contamination signals by selectively damping the influence of off-policy (non-member) trajectories whose success would otherwise create distinguishable loss differences. This is a structural property of the optimization objective rather than an emergent property of memorization, meaning it applies broadly across algorithms using similar objectives. The second insight that CoT contamination on LRMs does not fit the memorization framework (LRMs generalize contamination knowledge to unseen questions, raising confidence uniformly) challenges the foundational assumption underlying most existing detection methods and suggests the field needs fundamentally different detection paradigms for reasoning models.

## Suggestions

- Add bootstrap confidence intervals for all AUROC tables to clarify the statistical reliability of results, especially for small benchmarks.
- Extend the clipping ablation study (Table 3) to additional detection methods to confirm the mechanism is broadly applicable.
- Investigate whether detection performance for Stage II improves when non-members are drawn from distributions more distant from the training data, to establish boundaries of the generalization effect.

## Score and Decision

This paper makes a strong and timely contribution by identifying a fundamental vulnerability in LRM evaluation. The combination of comprehensive empirical evaluation, a clean theoretical framework isolating PPO clipping as the concealment mechanism, and falsifiable predictions validated through ablation studies is compelling. The practical implications for leaderboard integrity and the call for new detection paradigms are well-justified by the evidence. The major weakness regarding small sample sizes is a practical constraint rather than a fundamental flaw, and the core findings are robust across multiple models and benchmarks.

MY FINAL SCORE: <score>7.5</score>
MY FINAL DECISION: Accept