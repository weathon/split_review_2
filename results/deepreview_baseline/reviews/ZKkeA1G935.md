## Summary
This paper studies whether large language models (LLMs) can mitigate catastrophic forgetting in graph continual learning (GCL). It first identifies a critical flaw in existing GCL evaluation setups—local testing causes task ID leakage, degrading class-incremental learning into task-incremental learning. It then introduces LLM4GCL, a benchmark that evaluates 9 LLM-based and GLM-based methods across 7 text-attributed graphs under a more realistic global testing regime. Finally, it proposes SimGCL, a simple method that combines graph-prompted instruction tuning with training-free prototype classification, achieving substantial improvements over prior GNN-based and LLM-based baselines.

## Strengths
- **Exposes a significant evaluation flaw in GCL.** The paper convincingly demonstrates that the widely used local testing setup allows models to infer task IDs trivially (e.g., via mean pooling), which invalidates reported forgetting ratios and inflates accuracy. This is an important contribution that should raise methodological standards in the field.
- **Provides the first systematic benchmark for LLMs in GCL.** The benchmark includes diverse datasets (citation, web, e-commerce), multiple LLM and GLM backbones, and both NCIL and FSNCIL settings, offering a solid foundation for future research.
- **SimGCL is simple, efficient, and effective.** The method uses only first-session instruction tuning with LoRA and prototype-based classification in subsequent sessions, making it both computationally efficient and resistant to catastrophic forgetting. It achieves 20%+ absolute gains over the best GNN baseline on several datasets.
- **Clear experimental insights.** The paper provides well-structured observations (e.g., GNN limitations, LLM generalization advantage, prototype method benefits, scaling trends) that are supported by results and help the community understand the landscape.

## Weaknesses
### Fatal
None.

### Major
- **SimGCL underperforms SimpleCIL on Arxiv-23 in NCIL** (Table 2: SimGCL 38.7/13.6 vs SimpleCIL 52.4/38.8) and **underperforms SimpleCIL on several FSNCIL metrics** (e.g., Arxiv-23 and Arxiv final accuracy). This inconsistency weakens the claim that SimGCL “consistently overperforms” all baselines. The paper attributes this to dataset sparsity and overfitting, but the phenomenon deserves a deeper explanation or a robustness analysis.
- **Limited novelty of the SimGCL design.** The combination of instruction tuning (with graph prompts) followed by frozen prototypes closely mirrors SimpleCIL (Zhou et al., 2025) from vision, with the main addition being graph-aware prompting. While effective, the technical contribution is incremental relative to existing prototype-based continual learning with pretrained models.

### Minor
- The paper focuses exclusively on the rehearsal-free constraint. A brief discussion of how rehearsal-based methods compare or whether SimGCL could incorporate replay would strengthen the contextualization.
- The evaluation does not include computational cost comparisons (e.g., training time, memory) between LLM-based methods and GNN methods. Given that LLMs are much larger, a cost-benefit analysis would be useful.
- Some observations (e.g., Obs. 4 on dense graph structures) are based on only a few datasets and could be speculative.

### Trivial
- The observation numbering jumps from 6 to 8 (missing 5 and 7 in the text) – appears to be a typographical artifact.

## Nice-to-Haves
- Provide per-task accuracy curves for all baselines (not just SimGCL and SimpleCIL) to show forgetting dynamics.
- Include a variant of SimGCL that uses a small rehearsal buffer to see if performance on Arxiv-23 improves.
- Analyze the effect of different prompt designs (e.g., without neighbor information) to isolate the contribution of graph structure.

## Novel Insights
The key insight beyond the paper’s own contributions is that **the primary bottleneck in GCL is not the continual learning algorithm but the representational quality of the backbone**. GNNs trained from scratch suffer severe forgetting because their limited capacity cannot maintain discriminative features across sessions. LLMs, even with simple prototype matching, outperform sophisticated GCL methods because they start from a rich semantic space. This suggests that future GCL research should focus on leveraging strong pretrained backbones rather than designing complex regularization or replay mechanisms. The paper’s demonstration that task ID leakage invalidates prior evaluations also serves as a caution that progress in GCL may be overestimated.

## Suggestions
1. Address the inconsistency on Arxiv-23 explicitly, either by adding a post-hoc explanation (e.g., ablation on prompt quality, prototype collapse analysis) or by adjusting the claim to note that SimGCL excels on denser graphs.
2. Include a small table comparing the training/inference time and GPU memory of SimGCL vs. GNN baselines to contextualize the efficiency claim.
3. Add a discussion on whether the local testing flaw extends to graph-level or edge-level continual learning, to broaden the impact.

## Score and Decision
MY FINAL SCORE: <score>8</score>
MY FINAL DECISION: <decision>Accept</decision>