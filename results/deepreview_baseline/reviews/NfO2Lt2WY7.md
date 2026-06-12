## Summary

This paper conducts a systematic ablation of the GRPO loss function for LLM reasoning post-training. It identifies that negative feedback and group-relative advantage estimation are essential for stable learning, while PPO-style clipping is unnecessary. Based on these findings, the authors propose RGR (REINFORCE with Group Relative Advantage), a simplified method that removes clipping and policy ratios. Experiments on small models (0.5B–1.5B) across several math benchmarks show that RGR roughly matches or slightly outperforms GRPO.

## Strengths

- **Clean ablation design**: Isolating the roles of negative feedback, advantage estimation, and PPO clipping is a principled way to interrogate GRPO’s complexity. The comparisons (positive-only GRPO, REINFORCE, RAFT) directly test each hypothesis.
- **Important practical question**: Determining which components of GRPO are truly necessary has significant implications for training efficiency and interpretability. The paper addresses a timely topic that many practitioners care about.
- **Reproducibility-oriented presentation**: The description of experimental setups (LoRA rank, group size, reward signals, number of generations) is detailed, making it possible to reproduce the core comparisons.

## Weaknesses

### Major

- **Experiment scale is too small to support the claimed generality**: All training is done on models with ≤1.5B parameters, only 1,800 training examples from GSM8K, and roughly 70 training steps. It is unclear whether the conclusions (e.g., “PPO clipping is unnecessary”) hold for larger, more capable models (e.g., 7B, 70B) trained for thousands of steps on multi-task data. The paper’s title and conclusions make a general statement about “teaching LLMs to reason,” but the evidence is restricted to a narrow regime.
- **Observed improvements are modest and lack statistical rigor**: RGR outperforms GRPO in 17 of 27 benchmark comparisons, but the margins are often 1–3 percentage points. No confidence intervals, standard deviations across multiple runs, or significance tests are provided. Without this, it is impossible to determine whether the advantage is real or due to noise. Several comparisons show GRPO surpassing RGR (e.g., Llama3.2 1B on CMATH, Gaokao2024-STEM).
- **No analysis of computational cost**: One of the motivations for simplification is efficiency, yet the paper does not measure or compare training time, memory usage, or token throughput between GRPO and RGR. This is a missed opportunity to quantify a practical benefit.
- **Scope limited to math reasoning**: The paper evaluates only mathematical benchmarks (including STEM). While math is a relevant testbed, the title and framing imply broader applicability to “reasoning” in general. Without evidence on non‑math reasoning tasks (e.g., logical deduction, code generation, multi‑hop QA), the claim remains under‑supported.

### Minor

- **Naming inconsistency**: The proposed method is called RGR in the abstract and main text, but also “RGRA” (e.g., in Section 4 discussion). This can confuse readers.
- **Anecdotal evidence for reasoning emergence**: Figure 2 shows one qualitative example; a more systematic quantification of reasoning trace quality across methods would strengthen the argument about “emergence of reasoning behaviors.”

### Trivial

- The paper provides a code link in the reproducibility statement, which is good practice.

## Nice-to-Haves

- Include error bars or multiple seeds for all benchmark results to assess variability.
- Report wall-clock training time and memory usage for GRPO vs. RGR.
- Extend the analysis to at least one non‑math reasoning benchmark (e.g., ARC-Challenge, BBH).
- Show results with a larger model (e.g., 7B) on a subset of tasks to test scaling.

## Novel Insights

The paper confirms that, at least for small‑scale LLM post‑training, PPO’s clipping mechanism—designed to control policy updates in standard RL—is not needed when initializing from a strong instruction‑tuned policy and using group‑relative advantage. This aligns with earlier observations by Ahmadian et al. (2024) and provides a direct ablation within the GRPO framework. The finding that discarding negative feedback leads to catastrophic reward hacking (collapse) is also clearly demonstrated.

## Suggestions

- **Temper the claims**: Rephrase conclusions to explicitly acknowledge the small‑model, limited‑training regime, e.g., “for small LLMs and limited fine-tuning steps, PPO clipping is unnecessary.” Avoid general statements about “LLMs” without qualification.
- **Add statistical rigor**: Run each experiment with at least 3 random seeds and report mean and standard deviation. Use a simple test (e.g., paired bootstrap) to quantify whether RGR is significantly better than GRPO on each benchmark.
- **Include a computational comparison**: Measure tokens per second during training and peak GPU memory. This would directly support the “simpler and more efficient” claim.
- **Discuss limitations**: Explicitly state that the findings may not transfer to larger models, longer training, or non‑math domains, and that this is a limitation of the current study.

## Score and Decision

The paper addresses a well‑motivated research question and presents a clear ablation. However, the experimental evidence is limited to small models, few training steps, and a single domain (math). The improvements over GRPO are modest and not accompanied by any statistical grounding. The strong title and general claims are not supported by the narrow scope of the experiments. Given these concerns, the paper does not meet the bar for acceptance at ICLR.

MY FINAL SCORE: <score>4.0</score>  
MY FINAL DECISION: <decision>Reject</decision>