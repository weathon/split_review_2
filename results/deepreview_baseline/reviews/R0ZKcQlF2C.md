## Summary
The paper introduces ARENABENCHER, a framework for automatically evolving benchmarks by generating harder, yet aligned, test cases that expose shared weaknesses across multiple models. It extracts the core ability of each original test case, generates candidate rewrites, uses aggregated loss from a sampled subset of models to select candidates that degrade performance consistently, and iteratively refines generation via in-context demonstrations. Experiments on GSM8K, CommonsenseQA, and a safety dataset show that the updated benchmarks increase difficulty while maintaining alignment and fairness.

## Strengths
- **Relevant and timely problem**: The issue of data leakage in static benchmarks is real and important; an automated method to refresh benchmarks is of clear interest to the community.
- **Multi-model feedback design**: Using feedback from multiple models (rather than a single model) to select test cases is a sensible strategy to reduce model-specific bias, and the √K sampling heuristic is practical.
- **Ability-aware generation**: Explicitly extracting and conditioning on the core ability of each test case provides a principled way to steer generation toward tasks that preserve the original evaluation intent.
- **Clear and well-structured description**: The framework is presented in a modular, step-by-step manner (target extraction, candidate generation/verification, multi-model scoring, iterative refinement, final selection) that is easy to follow.

## Weaknesses

### Major
- **No comparison against any baseline**: The paper evaluates ARENABENCHER only against its own single-model variant (m=1). There are no comparisons to prior benchmark augmentation methods (e.g., MATH-Perturb, ARST, simple paraphrasing or numerical perturbation). Without such baselines, it is impossible to know whether the proposed framework is genuinely better than simpler alternatives or whether the observed difficulty increase is merely due to making queries harder in a naive way.
- **Very small and non-diverse model pool**: The evaluation uses only 6 open-source models (1B–7B), all from three families (LLaMA, Qwen, Mistral). This does not constitute a “diverse” pool; the claim that multi-model feedback mitigates bias is not convincingly demonstrated. The behavior on larger or closed-source models (e.g., GPT-4) is untested, and the generalizability of the method to a truly diverse model population is unclear.
- **Separability actually decreases**: The claimed “improvement in model separability” is contradicted by the reported numbers (e.g., GSM8K: Ori 15.2 → ARENABENCHER₃ 12.2; Harmful Behaviors: 17.1 → 14.5; CSQA: 8.5 → 7.2). The paper tries to explain this away (“slight variation … expected”), but the direction is consistently downward. This weakens one of the core claims.
- **Reliance on LLM-as-a-judge for alignment and correctness without sufficient validation**: The verifier and judge are GPT-4o, which itself may have biases. The human annotation covers only 100 samples from one domain (GSM8K). The failure case shown (Figure 2) reveals a clear failure where the updated query is unsolvable and misaligned—yet such cases are presumably scored as “Valid” by the automated verifier. This raises concerns about the reliability of the verification pipeline.
- **No analysis of what makes a “good” update beyond metrics**: There is no qualitative analysis of the generated test cases (except the one failure), no study of the diversity of failure modes uncovered, and no investigation of whether the updated benchmarks actually test the same skills in a meaningful sense (e.g., via probing or representational analysis).

### Minor
- **Cost and scalability not discussed**: The framework calls GPT-4o for generation and verification and requires running multiple models on many candidates. The paper provides no discussion of computational cost, latency, or feasibility for evolving large benchmarks (e.g., MMLU with thousands of questions). The “scalable path” claim is unsupported.
- **In-context demonstration benefit not ablated**: The iterative refinement with in-context demonstrations is a key component, but there is no ablation comparing ARENABENCHER with and without this mechanism. It is unclear whether the benefit comes from multi-model feedback, iterative refinement, or just the initial candidate generation.
- **Dataset sizes and selection not reported**: The paper does not specify how many test cases were updated from each benchmark (e.g., the full GSM8K, a subset). This makes it hard to assess statistical reliability and comparability across domains.
- **Fairness metric interpretation**: The fairness metric normalizes deviation of per-model failure counts. If all models fail on many queries, deviation is low and fairness is high, but that does not necessarily indicate unbiasedness—the queries might be uniformly too hard. The metric should be interpreted with caution.

### Trivial
- Figure 2 is duplicated in the paper (appears twice with identical caption).
- The framework name “ARENABENCHER” is a bit unwieldy but not a substantive issue.

## Nice-to-Haves
- Compare against at least two strong baselines (e.g., simple numerical/value substitution, paraphrase-based augmentation, and a state-of-the-art perturbation method like MATH-Perturb or ARST).
- Include an ablation where the multi-model feedback is replaced by random selection to understand the contribution of the loss-based selection.
- Report the number of test cases updated and the coverage of the original benchmark.
- Provide a small qualitative taxonomy of failure modes uncovered by the updated test cases.
- Discuss the cost of the pipeline (number of GPT-4o calls, total inference time) and how it scales with benchmark size.

## Novel Insights
The combination of multi-model aggregated loss as a selection signal with ability-preserving generation conditioned on extracted task descriptions is a sensible design. The in-context demonstration loop that reuses top candidates to steer future generation is a clever way to create a curriculum of difficulty. However, the empirical evaluation is too limited to support the strong claims, and the absence of baselines prevents isolating what portion of the benefit is truly novel.

## Suggestions
1. **Add baselines**: Compare against simple numerical perturbation (e.g., replace numbers in math problems) and a paraphrasing-based method (e.g., LLM paraphrase without feedback). This is essential to show that the multi-model feedback and ability extraction add value.
2. **Separability analysis**: The decrease in separability should be explained honestly. If increased difficulty compresses scores, then separability is not a strength; the paper should either reframe the goal or show that under appropriate analysis (e.g., per-difficulty-level separability) the metric is still meaningful.
3. **Strengthen human evaluation**: Increase the number of annotated samples (e.g., 200–300) and include samples from all three domains. Evaluate not just alignment/correctness but also whether the updated query tests a similar reasoning process.
4. **Ablate iterative refinement**: Show a comparison with and without the in-context demonstration loop to justify its inclusion.
5. **Address the failure case**: Discuss how the verification pipeline could be improved (e.g., using a structured verifier or multiple judges) and report the overall failure rate beyond the 5% misaligned / 4% incorrect from human eval.

## Score and Decision
The paper addresses an important problem and proposes a clean framework. However, the evaluation is critically incomplete: no baselines, a small and homogeneous model pool, decreasing separability, and insufficient validation of the automated verification. The current evidence does not convincingly demonstrate that ARENABENCHER is better than simpler alternatives. The core ideas have potential, but the paper, in its present form, does not meet the standard for acceptance.

MY FINAL SCORE: <score>4</score>
MY FINAL DECISION: <decision>Reject</decision>