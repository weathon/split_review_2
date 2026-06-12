## Summary
This paper introduces VisualPRM400K, a ~400K-sample multimodal process supervision dataset constructed via Monte Carlo sampling; VisualPRM, an 8B-parameter Process Reward Model trained on this data; and VisualProcessBench, a human-annotated benchmark for evaluating step-level error detection in multimodal reasoning. Under Best-of-N evaluation, VisualPRM consistently improves multimodal reasoning across four model families (MiniCPM, Qwen, InternVL) and multiple scales (7B–78B), with gains of 3.7–8.4 points averaged over seven benchmarks, outperforming Outcome Reward Models and Self-Consistency.

## Strengths
- **Comprehensive and convincing experimental evaluation.** The paper evaluates on 7 multimodal reasoning benchmarks, across 6 policy models spanning 3 model families and scales from 7B to 78B parameters. The consistent improvements (e.g., InternVL2.5-8B +8.4, MiniCPM-V2.6 +8.0, InternVL2.5-78B +5.9) are substantial and robust across settings. Ablations systematically compare PRM vs. ORM vs. Self-Consistency at N ∈ {8, 16, 32, 64, 128}, value-based vs. advantage-based modeling, and different score aggregation methods.

- **Useful community infrastructure.** The paper delivers three resources: (1) a large-scale training dataset (VisualPRM400K with ~2M annotated steps), (2) a carefully constructed benchmark (VisualProcessBench with 26,950 human-annotated step labels from expert annotators with quality control), and (3) a trained model (VisualPRM). The benchmark design requiring detection of *all* erroneous steps (not just the first) is well-motivated by model reflection capabilities and represents a meaningful improvement over prior benchmark designs.

- **Strong practical value for test-time scaling.** The paper convincingly demonstrates that open-source MLLMs perform poorly as critic models (often scoring near random guessing on VisualProcessBench), and that a dedicated PRM fills this gap effectively. The additional text-only results on GSM8K, MATH-500, and GPQA-Diamond (Table 5) demonstrate unexpected transfer, strengthening the case for the model's utility.

## Weaknesses
### Fatal
None.

### Major
- **Limited methodological novelty.** The core data construction pipeline (Monte Carlo sampling to estimate step-level expected accuracy) follows MathShepherd (Wang et al., 2023a) closely, and the PRM training formulation as multi-turn chat is straightforward. The paper itself acknowledges in the Limitations: "our exploration of training and modeling strategies for multimodal PRMs is limited." The primary novelty lies in the multimodal adaptation and scaling, which is valuable but modest in terms of algorithmic contribution.

- **Homogeneous training data generation.** All solutions in VisualPRM400K are generated using InternVL2.5 series models, which could bias the PRM toward reasoning patterns specific to that model family. In contrast, the benchmark correctly uses five diverse models for solution generation. This asymmetry is not discussed or analyzed.

- **Noisy automatic annotations.** With only 16 Monte Carlo continuations per step, the expected accuracy estimates are coarse-grained (only 17 possible values). The paper acknowledges ~10% incorrect steps in the training data but does not deeply analyze the impact of annotation noise on PRM quality or compare against higher-quality annotations (e.g., human-labeled subsets).

### Minor
- **Inference cost not quantified.** The paper notes that MLLM-as-a-judge is slow due to autoregressive step evaluation, but provides no quantitative latency comparison. BoN with N=8 requires 8 policy model forward passes, which is a significant cost; a cost-performance analysis would strengthen the practical guidance.

- **Qwen2.5-VL-72B result partially undermines a key claim.** Table 3 shows Qwen2.5-VL-72B achieves 60.5 F1 on VisualProcessBench, very close to VisualPRM's 62.0, which somewhat weakens the claim that "existing open-source MLLMs struggle to accurately assess step correctness." The paper should acknowledge this.

- **Score aggregation detail.** Section 3.2 states step scores are averaged for response score, but Table 4 shows min aggregation sometimes performs comparably. The chosen default (average) is justified but the near-parity deserves comment.

### Trivial
None.

## Nice-to-Haves
- A cost-performance Pareto analysis showing accuracy vs. total inference FLOPs for BoN at different N values.
- Analysis of PRM performance when the policy model family differs from the InternVL2.5 models used to generate training data.
- Comparison with a PRM trained on a subsample of higher-quality (e.g., human-verified) annotations to isolate the effect of annotation noise.

## Novel Insights
The paper surfaces a practically important observation: even strong MLLMs like InternVL2.5-78B are poor at step-level error detection when used as zero-shot critics, tending to assign positive labels indiscriminately (InternVL2.5-8B achieves 76.8 F1 on correct steps but only 19.2 on incorrect steps). This is a genuine finding that motivates dedicated PRM training for the multimodal setting. The additional finding that a multimodal PRM transfers to text-only reasoning benchmarks is also noteworthy and somewhat surprising.

## Suggestions
- Add a quantitative latency and compute comparison between VisualPRM and MLLM-as-a-judge to make the efficiency argument concrete.
- Discuss the impact of training data homogeneity (InternVL2.5-only generation) and ideally experiment with mixed-policy training data.
- Increase Monte Carlo sampling budget or analyze how PRM quality scales with the number of continuations per step.

## Score and Decision

The paper makes a solid practical contribution through its dataset, benchmark, and model, with strong and comprehensive experimental results across many settings. The VisualProcessBench benchmark in particular is a valuable community resource. However, the methodological novelty is moderate—the core ideas are straightforward adaptations of existing techniques (MathShepherd-style MC sampling, standard PRM training) to the multimodal setting. The paper's own limitation statement is refreshingly honest about this. Given the clear utility of the resources and the strong empirical validation, balanced against the limited algorithmic novelty, this falls in the borderline accept range.

MY FINAL SCORE: <score>6</score>
MY FINAL DECISION: <decision>Accept</decision>