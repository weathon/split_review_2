## Summary

This paper formalizes the All-Day Multi-Scenes Lifelong Vision-and-Language Navigation (AML-VLN) problem, where agents must continually adapt across diverse scenes and environmental conditions (normal, low-light, overexposed, scattering) without catastrophic forgetting. The authors propose Tucker Adaptation (TuKA), a parameter-efficient fine-tuning method that represents multi-hierarchical navigation knowledge as a high-order tensor and uses Tucker decomposition to decouple shared and task-specific knowledge. They further introduce a Decoupled Knowledge Incremental Learning (DKIL) strategy and build the AllDayWalker agent, which consistently outperforms state-of-the-art baselines on a newly constructed benchmark with 24 navigation scenarios.

## Strengths

- **Novel problem formalization**: The paper formalizes the AML-VLN problem, which is a practical and underexplored setting that combines lifelong learning with multi-scene and multi-environment navigation. This is a timely contribution given the growing interest in deploying VLN agents in real-world, dynamic conditions.

- **Technically sound and principled approach**: The use of Tucker decomposition to represent multi-hierarchical knowledge (scene, environment, shared skills) as a high-order tensor is a principled and mathematically grounded extension beyond existing 2D matrix-based adapters like LoRA. The decoupling into shared core tensor, encoder/decoder, and separate scene/environment expert factor matrices is well-motivated and aligns naturally with the problem structure.

- **Strong empirical results**: The proposed AllDayWalker consistently and significantly outperforms a comprehensive set of 12 baselines (including recent methods like BranchLoRA, SD-LoRA, HydraLoRA) across all metrics (SR, SPL, OSR) and their forgetting rates. The improvements are substantial (e.g., 65% average SR vs. 52% for the best baseline SD-LoRA, and 11% F-SR vs. 18% for SD-LoRA). The generalization experiments to unseen scenarios also show large margins (55% vs. 40%).

- **Comprehensive evaluation**: The paper constructs a new benchmark with 24 tasks spanning simulation and real-world scenes across four environmental conditions, evaluates against 12 baselines, and includes extensive ablation studies (tensor order, shared components, scaling to more tasks, generalization). The inclusion of real-world deployment further strengthens the practical relevance.

## Weaknesses

### Fatal
None.

### Major
1. **Potential confounding in the comparison of trainable parameters**: The paper states that to keep trainable parameters comparable, LoRA uses rank r=6, MoE-LoRA uses r=16 with K=8 experts, and MoE-LoRA shared A uses r=32 with K=8 experts. However, the TuKA method uses r1=r2=8, r3=64, r4=64 with M=7, N=4 experts. The total number of trainable parameters in TuKA appears to be significantly larger than the baselines (e.g., the core tensor alone is 8×8×64×64 = 262,144 parameters per layer, plus factor matrices). The paper should provide a clear parameter count comparison per layer and total to ensure the comparison is fair. If TuKA uses substantially more parameters, the performance gains may be partially attributable to capacity rather than the tensor decomposition structure.

2. **Limited analysis of the expert search mechanism**: The task-specific expert search during inference (Section 3.4) relies on CLIP vision features and cosine similarity matching. However, the paper does not report the accuracy of this expert retrieval mechanism. If the expert selection is incorrect, the agent would use mismatched scene/environment experts, potentially degrading performance. The paper should provide retrieval accuracy or ablation showing performance with oracle expert selection vs. the proposed retrieval method.

3. **The forgetting rate metric definition may be problematic**: The forgetting rate F-SR_t is defined as (M-SR_t - SR_t) / M-SR_t, where M-SR_t is the performance when training on tasks 1 through t jointly. However, in a lifelong learning setting, joint training on all tasks up to t is not a valid upper bound because it violates the sequential learning constraint (it has access to all data simultaneously). A more standard forgetting metric would compare performance on task t after learning all tasks vs. performance on task t immediately after learning it. The current definition may overstate or understate forgetting.

### Minor

1. **The forgetting rate metric definition may be problematic**: The forgetting rate F-SR_t is defined as (M-SR_t - SR_t) / M-SR_t, where M-SR_t is the performance when training on tasks 1 through t jointly. However, in a lifelong learning setting, joint training on all tasks up to t is not a valid upper bound because it violates the sequential learning constraint (it has access to all data simultaneously). A more standard forgetting metric would compare performance on task t after learning all tasks vs. performance on task t immediately after learning it. The current definition may overstate or understate forgetting.

2. **Limited analysis of the expert search mechanism**: The task-specific expert search during inference (Section 3.4) relies on CLIP vision features and cosine similarity matching. However, the paper does not report the accuracy of this expert retrieval mechanism. If the expert selection is incorrect, the agent would use mismatched scene/environment experts, potentially degrading performance. The paper should provide retrieval accuracy or ablation showing performance with oracle expert selection vs. the proposed retrieval method.

3. **The forgetting rate metric definition may be problematic**: The forgetting rate F-SR_t is defined as (M-SR_t - SR_t) / M-SR_t, where M-SR_t is the performance when training on tasks 1 through t jointly. However, in a lifelong learning setting, joint training on all tasks up to t is not a valid upper bound because it violates the sequential learning constraint (it has access to all data simultaneously). A more standard forgetting metric would compare performance on task t after learning all tasks vs. performance on task t immediately after learning it. The current definition may overstate or understate forgetting.

### Minor

1. **Limited analysis of the expert search mechanism**: The task-specific expert search during inference (Section 3.4) relies on CLIP vision features and cosine similarity matching. However, the paper does not report the accuracy of this expert retrieval mechanism. If the expert selection is incorrect, the agent would use mismatched scene/environment experts, potentially degrading performance. The paper should provide retrieval accuracy or ablation showing performance with oracle expert selection vs. the proposed retrieval method.

2. **The forgetting rate metric definition may be problematic**: The forgetting rate F-SR_t is defined as (M-SR_t - SR_t) / M-SR_t, where M-SR_t is the performance when training on tasks 1 through t jointly. However, in a lifelong learning setting, joint training on all tasks up to t is not a valid upper bound because it violates the sequential learning constraint (it has access to all data simultaneously). A more standard forgetting metric would compare performance on task t after learning all tasks vs. performance on task t immediately after learning it. The current definition may overstate or understate forgetting.

3. **Limited analysis of the expert search mechanism**: The task-specific expert search during inference (Section 3.4) relies on CLIP vision features and cosine similarity matching. However, the paper does not report the accuracy of this expert retrieval mechanism. If the expert selection is incorrect, the agent would use mismatched scene/environment experts, potentially degrading performance. The paper should provide retrieval accuracy or ablation showing performance with oracle expert selection vs. the proposed retrieval method.

### Trivial

- The paper uses "AlldayWalker" and "AllDayWalker" inconsistently in the text.
- Figure 7 caption mentions "BaseModel, Recall, Task2Vec, CLIP" but these are not the methods compared in the main tables; the radar chart appears to show different methods than those in Tables 1-2.

## Nice-to-Haves

- An analysis of the computational overhead (training time, inference time, memory usage) of TuKA compared to baselines would be valuable for practitioners.
- A study on the sensitivity of the rank parameters (r1, r2, r3, r4) and the number of experts (M, N) would help understand the robustness of the method.
- The paper could benefit from a more detailed discussion of failure cases or scenarios where AllDayWalker still struggles.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. Provide a clear parameter count comparison (per layer and total) between TuKA and all baselines to ensure fair comparison.
2. Report the accuracy of the expert retrieval mechanism (scene and environment expert selection) and provide an ablation study comparing oracle expert selection vs. the proposed retrieval method.
3. Clarify the forgetting rate metric definition and consider using a more standard lifelong learning metric (e.g., average forgetting, or comparing performance after sequential learning vs. after single-task learning).
4. Add an analysis of computational overhead (training time, inference time, memory) for TuKA vs. baselines.

## Score and Decision

The paper makes a solid contribution by formalizing a practical lifelong VLN problem, proposing a principled tensor-based adaptation method, and demonstrating strong empirical results. The main concerns are around the fairness of parameter count comparison and the clarity of the forgetting rate metric. However, these are addressable and do not invalidate the core contribution. The paper is well-written, the method is novel and technically sound, and the experiments are comprehensive.

MY FINAL SCORE: <score>8</score>
MY FINAL DECISION: <decision>Accept</decision>