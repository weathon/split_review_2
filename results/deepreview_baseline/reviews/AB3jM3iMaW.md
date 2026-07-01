## Summary

This paper proposes ReaL-TG (Reasoning-Enhanced Learning for Temporal Graphs), a reinforcement learning framework that fine-tunes LLMs to perform explainable link forecasting on real-world temporal graphs. The framework uses GRPO with an F1-based reward to encourage LLMs to self-explore reasoning strategies from graph structure while producing human-readable explanations. The authors also introduce a new evaluation protocol combining penalized MRR (pMRR) with an LLM-as-a-Judge system that assesses reasoning quality across faithfulness, logical consistency, and answer-explanation alignment. Their fine-tuned ReaL-TG-4B model outperforms much larger frontier LLMs (including GPT-5 mini and Llama 3.3 70B) on ranking metrics while producing high-quality explanations.

## Strengths

- **Novel and well-motivated problem framing**: The paper addresses a genuine gap—enabling LLMs to perform explainable link forecasting on real-world temporal graphs without relying on textual attributes that risk data leakage. The anonymized graph setting is practical and avoids the contamination issues present in prior work.

- **Comprehensive evaluation protocol**: The introduction of pMRR to penalize over-generation and the three-criteria LLM-as-a-Judge system for reasoning quality are thoughtful contributions. The human evaluation validating both the judge system and the model's reasoning traces (with high inter-annotator agreement) significantly strengthens the paper's claims.

- **Strong empirical results**: ReaL-TG-4B outperforms much larger models (GPT-5 mini, Llama 3.3 70B) on both seen and unseen graphs across MRR and pMRR, demonstrating that RL fine-tuning on a modest 4B parameter model can yield substantial improvements. The transferability to unseen graphs is particularly impressive.

- **Sound methodology**: The T-CGS algorithm for temporal context graph selection is well-designed, using temporal random walks with recency bias. The GRPO-based RL training with F1 reward is appropriate for the multi-label prediction setting, and the ablation with ReaL-TG-0.6B provides useful insights about base model capacity requirements.

## Weaknesses

### Fatal
None.

### Major
- **Limited evaluation scale and dataset diversity**: The training set uses only 1,000 queries from 4 datasets, and the evaluation set contains 4,246 queries from 6 datasets (all from TGB). While the results are promising, the temporal graphs in TGB are relatively small (hundreds to thousands of nodes). The paper does not demonstrate scalability to larger temporal graphs (e.g., with millions of nodes or interactions), which is critical for real-world applicability. The claim of "real-world" applicability is somewhat undermined by the small graph sizes.

- **Missing comparison with LLM fine-tuning baselines**: The paper compares ReaL-TG-4B against prompted frontier LLMs and traditional TGNNs, but does not compare against standard supervised fine-tuning (SFT) of the same base model (Qwen3-4B) on the same data. Without this ablation, it is unclear whether the improvements come from the RL framework specifically or simply from any fine-tuning on TG data. This is a significant omission for a method paper claiming RL as the key innovation.

- **The LLM-as-a-Judge evaluation uses GPT-4.1 mini as the judge while evaluating models including those from the same family**: The authors acknowledge this concern for GPT-5 mini (which they exclude), but they evaluate Qwen3 models using a GPT-based judge. While the human evaluation on 50 samples shows good alignment, the scale is small, and potential model-specific biases in the judge's assessments across different model families are not systematically addressed.

### Minor
- **The T-CGS algorithm's hyperparameters (α, β, number of hops, top-k nodes) are set to fixed values without sensitivity analysis**: The paper states that |𝒩_q| is set to 100 and the random walk is limited to at most 2 steps, but does not explore how varying these parameters affects performance. Given that T-CGS is a core component, this analysis would strengthen the paper.

- **The paper claims "the first framework that enables LLMs to perform explainable and effective link forecasting on real-world temporal graphs via reinforcement learning"** but concurrent work (TGTalker, cited as Huang et al., 2025b) also explores LLM-based link forecasting on real-world TGs. The novelty lies specifically in the RL training component, which should be more precisely scoped.

### Trivial
- The paper uses "link forecasting" and "link prediction" somewhat interchangeably, though they define "forecasting" as predicting future links. This is a minor inconsistency.

## Nice-to-Haves

- A sensitivity analysis of T-CGS hyperparameters (α, β, number of hops, top-k) would strengthen the paper.
- Comparison with SFT baselines on the same data would isolate the benefit of RL.
- Evaluation on larger temporal graphs (e.g., from the TGB2 benchmark or industrial-scale datasets) would strengthen claims of real-world applicability.
- Analysis of the computational cost of the RL training (number of GRPO steps, wall-clock time, GPU hours) would help practitioners assess feasibility.

## Novel Insights

Beyond the paper's own contributions, a genuinely novel observation is that outcome-based RL (without process-level supervision) can induce LLMs to discover meaningful reasoning strategies for temporal graph structure, even when nodes are anonymized and carry no semantic information. This suggests that LLMs can learn to reason about purely structural, temporal patterns through trial-and-error with a simple F1 reward, which has implications for other structured reasoning tasks where semantic priors are unavailable. The finding that a 0.6B model exhibits reward hacking (claiming the future link was "already seen") while a 4B model does not provides empirical evidence for a capacity threshold below which RL-based self-exploration of reasoning strategies fails, which is valuable for practitioners designing RL fine-tuning pipelines.

## Suggestions

- Add a supervised fine-tuning (SFT) baseline using the same training data to isolate the contribution of the RL framework.
- Include a sensitivity analysis of T-CGS hyperparameters and report computational costs of training.
- Consider evaluating on larger temporal graphs to strengthen claims about real-world applicability.

## Score and Decision

The paper makes a solid contribution to an emerging area (LLMs for temporal graph reasoning) with a well-designed framework, thorough evaluation, and strong empirical results. The main limitations are the missing SFT ablation and the relatively small scale of evaluation graphs. These are addressable but prevent the paper from being a clear accept at the highest level.

MY FINAL SCORE: <score>6.0</score>
MY FINAL DECISION: <decision>Accept</decision>