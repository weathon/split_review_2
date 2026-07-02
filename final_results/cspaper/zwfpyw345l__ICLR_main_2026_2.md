---
job_id: 5cd57772-6084-402b-bdd0-e9789e5ca63a
agent_id: ICLR_main_2026_2
status: COMPLETED
filename: zwfpyw345l.pdf
paper: 
main_score_norm: 0.2
desk_reject: false
note: desk_rejection_enabled=false rerun
---
# Preliminary Observations:
N/A

# Expected Review Outcome:
## Summary
This paper proposes a hierarchical code state representation for reinforcement learning, combining token-level transformer attention, function-level AST attention, and module-level graph attention over a code dependency graph. The final representation is trained end-to-end with an RL objective and evaluated on three code-related tasks, code completion, program repair, and algorithmic problem solving, with comparisons to sequence, tree, pretrained, and graph-based baselines plus an ablation study.

## Strengths
The paper addresses a topic that is in scope for ICLR and potentially interesting, namely representation learning for RL over structured code states. The high-level motivation, that code has meaningful hierarchical structure and that RL agents may benefit from state encodings that reflect token, function, and module levels, is reasonable.

The architecture sketch in **Figure 1** is one of the clearer parts of the paper. It conveys the intended flow from token-level attention to function- and module-level aggregation, with a dependency-graph branch feeding into the final state representation. Even though the exact implementation remains underspecified in the text, the figure helps the reader understand the authors’ intended modular decomposition.

The empirical section at least attempts breadth: the paper reports multi-task comparisons in **Table 1**, an ablation in **Table 2**, training dynamics in **Figure 2**, and a scalability plot in **Figure 3**. The inclusion of an ablation is good practice, and **Table 2** does suggest that the authors are trying to isolate the contribution of token-, function-, and module-level attention, as well as CDG edges.

## Weaknesses
I have substantial concerns about soundness, clarity, novelty positioning, and empirical validity. The main issue is not that the paper is “rough around the edges”; it is that many central claims are currently unsupported or even not well-defined enough to evaluate.

1. **The method is underspecified to a degree that prevents reproducibility or even a precise understanding of what is being trained.**  
   Section 4 introduces several attention formulas, but the actual model is not concretely defined. For example, in **Equation (5)** on **Page 4**, the state is the concatenation
   \[
   \mathbf{s} = [\mathbf{h}_{\mathrm{CLS}} \| \mathbf{f}_{\text{main}} \| \mathbf{m}_{\text{root}} \| \mathbf{g}_{\mathrm{CDG}}],
   \]
   but the paper never defines how \(\mathbf{f}_{\text{main}}\), \(\mathbf{m}_{\text{root}}\), or \(\mathbf{g}_{\mathrm{CDG}}\) are actually computed in the multi-layer architecture. Is there a pooling operator over AST nodes? How are multiple functions/modules handled when there is no unique “main” or “root” in the dataset? How is the CDG readout formed, mean pooling, attention pooling, virtual node, or something else? These are not cosmetic omissions. They determine the actual state representation that the RL algorithm sees.

2. **Several equations are mathematically incomplete or ambiguous.**  
   This is a major issue because the paper’s contribution is methodological. A few concrete examples:
   - In **Equation (1)** on **Page 3**, \(\alpha_{ij}\) is written as a softmax of a scalar compatibility term, but the normalization axis is not specified. Presumably softmax is over \(j\) for each fixed \(i\), but that should be stated.
   - In **Equation (2)**, the AST attention weight \(\beta_{uv}\) again uses softmax, but over which neighbor set, all \(v \in \mathcal{N}(u)\), all AST nodes in a function, or something else? This matters because the aggregation rule is otherwise undefined.
   - **Equations (4)** and **(7)** both appear to define module/CDG attention, but the relationship between them is unclear. Is **Equation (4)** replaced by the multi-head variant in **Equation (7)**, or are both used? If both are used, where? At present, Section 4.2 and Section 4.4 look partially redundant and internally inconsistent.
   - In **Equation (6)**, the policy gradient is presented as
     \[
     \nabla_\theta \mathcal{J}(\theta)=\mathbb{E}[\nabla_\theta \log \pi_\theta(a|s) Q^\pi(s,a)],
     \]
     but the implementation section on **Page 5** states PPO is used. PPO does not optimize this bare objective directly; it uses a clipped surrogate and typically a value loss and entropy bonus. If the claimed end-to-end RL objective is central, the actual optimization objective should be stated. Otherwise the training story is misleading.
   - In **Equation (8)**, dynamic edge updates are defined, but the paper never specifies initial edge features \(\mathbf{e}_{uv}^{(0)}\), which edges receive updates, or how this interacts with the edge-type-specific attentions in earlier equations.

3. **The RL problem formulation is not credible as written, because the states, actions, rewards, and episodes are not concretely defined for the three tasks.**  
   This is especially problematic in **Section 5.1** and **Section 5.5**. “Code completion,” “program repair,” and “algorithmic problem solving” are extremely different problems. Yet the paper compresses all three into generic statements like “actions correspond to valid code modifications or additions” and later says the action space includes “insert/replace/delete” and also “complexity raising functions, name changes of variables.” This is far too vague.  
   For RL, one needs to know:
   - what constitutes one state transition,
   - whether rewards are dense or sparse,
   - when an episode terminates,
   - whether actions are token-level, AST-level, or mixed,
   - how invalid actions are masked,
   - how the MDP differs across datasets and languages.
   
   Without this, the central claim, that the proposed encoder improves RL state representation, cannot be meaningfully assessed. Right now the RL framing reads more like a thin wrapper around standard code prediction/generation tasks than a properly specified sequential decision problem.

4. **The experimental setup is too weakly described to trust the reported numbers in Table 1.**  
   **Table 1** on **Page 7** reports exact BLEU, success rate, pass rate, and average reward values for six models across three tasks. However, there is no information about:
   - number of random seeds,
   - variance or standard deviation,
   - confidence intervals,
   - train/validation/test splits for each dataset as actually used,
   - whether models were pretrained or trained from scratch,
   - whether CodeBERT was allowed to use its pretrained weights while other baselines were not,
   - task-specific hyperparameters,
   - budget parity in terms of parameters, updates, and wall-clock.
   
   The paper says significance was tested via paired \(t\)-tests in **Section 5.4**, but there are no error bars, no p-values in any table, and no indication of what was paired across runs. As a result, the apparent margins in **Table 1** are difficult to interpret scientifically.

5. **Key baselines are either poorly justified or unfairly compared.**  
   The baseline section on **Page 5** includes Sequence Transformer, Tree-LSTM, CodeBERT, GNN-CDG, and Flat-GAT. This is not enough for the claimed contribution. Since the method is explicitly hierarchical and hybrid graph-sequential, the most relevant comparisons should include stronger hierarchical code models or stronger graph-transformer hybrids, not mostly older or generic baselines. The paper cites prior hierarchical code representation works in Sections 2.1 and 2.2, but does not compare against them experimentally.  
   More importantly, the fairness claim “all baselines were adapted to output state representations of comparable dimensionality (768-D) and trained with identical RL algorithms” is not sufficient. Equal dimensionality does not imply comparable capacity or optimization fairness. In particular, comparing a pretrained model like CodeBERT to non-pretrained baselines, while not explaining initialization and fine-tuning protocol carefully, leaves a large ambiguity.

6. **The results section over-claims based on thin evidence.**  
   The text around **Table 1** claims “consistent superiority” and specific semantic advantages, but the evidence shown is only task-level aggregate metrics. There is no per-dataset breakdown beyond one scalar per task, no analysis of failure modes by bug type, no robustness to program length except a later qualitative curve, and no evidence tying improvements to hierarchy rather than simply increased model complexity.  
   **Table 2** is directionally useful, but it is only reported for one task, program repair. If the paper’s thesis is that hierarchical multi-level attention is generally important for code RL, a single-task ablation is not enough. The largest drop there is from removing token-level attention, \(-6.2\%\), while removing CDG edges costs only \(-1.9\%\). That weakens, rather than strengthens, the paper’s narrative that the structural graph augmentation is a major driver.

7. **The figure-based evidence is not strong enough to support the stated conclusions.**  
   - **Figure 2** on **Page 7** shows learning curves for cumulative reward, and the proposed model is above the others. But the figure lacks variance bands, seed count, and even task labeling in the caption beyond a vague reference in the text. Given how noisy RL training typically is, a single mean-looking curve is not enough to establish “faster convergence” or better sample efficiency.
   - **Figure 3** on **Page 8** is more troubling. The y-axis is “Prediction Error (%)” versus code complexity, but the curves increase with complexity and seem capped near 20 for some methods. The paper then concludes memory is linear for the proposed model and quadratic for sequence transformers. **Figure 3** does not show memory at all, only prediction error. So the memory-scaling claim is unsupported by the displayed figure. This is a concrete mismatch between figure evidence and textual claim.
   - In **Figure 1**, while the architecture is readable at a high level, it also exposes the paper’s underspecification: there is a “Graph Attention Aggregator” box that does not correspond cleanly to one uniquely defined block in the equations, which split functionality across module-level attention, CDG attention, and dynamic edge learning.

8. **The representation-quality analysis is asserted but not presented.**  
   In **Section 5.4**, the paper lists t-SNE visualization, nearest neighbor analysis, and attention head diversity as representation metrics. In **Section 6.4**, it says “t-SNE visualizations of the learned state representations are shown here,” but there is no corresponding figure or quantitative summary in the paper text. This is not a minor omission. The paper explicitly advertises representation learning benefits, yet the representation analysis is mostly verbal and unsupported by actual presented evidence.

9. **The writing and exposition are substantially below ICLR standards, and this materially affects scientific evaluation.**  
   I am ignoring obvious OCR artifacts, but even beyond those, many passages are genuinely hard to parse and appear conceptually unstable. Examples include the task descriptions, the explanation of Section 4.2, and the discussion section on **Page 9**. This is not about style policing. Here, unclear exposition translates directly into uncertainty about what the method is, what assumptions it makes, and what was actually evaluated. When a paper proposes a new architecture and training setup, precision is not optional.

10. **Novelty and positioning are not convincingly established.**  
    The paper’s main idea, hierarchical attention over code structure combined with graph-based dependencies and optimized for a downstream task, is close in spirit to multiple existing strands of work that the paper itself partially cites, including hierarchical code representation, graph attention for code, and RL-guided code modeling. The paper does not sharply articulate what is genuinely new beyond assembling token/function/module attention plus CDG edges in an RL setting. That could still be acceptable if the empirical evidence were strong, but currently the evidence is not strong enough to elevate what looks like an incremental combination.

11. **Some claims are unsupported or internally inconsistent.**  
    A few examples:
    - The abstract and introduction emphasize that existing methods do not capture local and global code features well, but there is no direct analysis separating local versus global dependencies.
    - Section 4.5 says “the relative balance between these pathways is learned,” but no gating variable, mixture coefficient, or balancing loss is ever defined.
    - The conclusion on **Page 9** claims a “major breakthrough,” which is not warranted by the evidence in the paper.

Overall, the paper has a plausible high-level idea, but the current manuscript does not provide a sufficiently precise method description or a sufficiently reliable empirical evaluation to support its claims.

## Questions
1. Please provide a precise MDP definition for each of the three tasks in **Section 5.1**: what is the state, what are the actions, how are invalid actions handled, what is the reward at each step, and what is the episode termination condition? A task-by-task table would help substantially.

2. What is the exact PPO objective used in training? Since **Equation (6)** gives a vanilla policy-gradient form, please specify the actual clipped surrogate, value loss, entropy bonus, and how gradients flow into the encoder.

3. How exactly are the representations in **Equation (5)** computed? In particular, how are \(\mathbf{f}_{\text{main}}\), \(\mathbf{m}_{\text{root}}\), and \(\mathbf{g}_{\mathrm{CDG}}\) derived for code samples with multiple functions/modules or without a clear root/main function?

4. Please clarify the relationship between **Equations (4)** and **(7)**. Are these two alternative definitions of CDG attention, or are both used in different layers? If both are used, please state the full forward pass explicitly.

5. For **Table 1** and **Figure 2**, how many random seeds were used, and can you report mean \(\pm\) standard deviation or confidence intervals? This would significantly increase confidence in the empirical claims.

6. Can you provide stronger, more directly relevant baselines for hierarchical code representation, or explain why they were omitted? This is important for assessing whether the gains come from hierarchy specifically, rather than from a larger or more tuned architecture.

7. The claim on **Page 8** that memory usage scales linearly for the proposed model and quadratically for sequence transformers is not supported by **Figure 3** as presented. Do you have a runtime/memory table or plot that directly substantiates this claim?

8. Since **Table 2** shows the smallest drop when removing CDG edges, can you explain more carefully what unique value the graph component adds, beyond token-level modeling? A per-task ablation, not just program repair, would help.

## Flag For Ethics Review
- No ethics review needed.

## Details Of Ethics Concerns
None.

## Soundness Rating
1: poor. The central technical and empirical claims are not adequately supported because the method and RL formulation are underspecified, several equations are ambiguous, and the experiments lack the detail and statistical evidence needed for validation.

## Presentation Rating
1: poor. The paper has serious exposition problems that go beyond style and make it difficult to determine the exact method, assumptions, and evaluation protocol.

## Contribution Rating
1: poor. The high-level idea is relevant, but the paper does not clearly establish a distinct contribution relative to prior hierarchical/graph code representation work, and the evidence is not strong enough to make the contribution convincing.

## Overall Rating
2: Reject, not good enough. The topic is relevant and the core intuition is reasonable, but the current paper falls well short of ICLR standards on specification, clarity, and evidential support. The work would need a much more precise methodological description, a properly defined RL formulation, stronger and fairer baselines, and statistically credible experiments before it can be evaluated positively.

## Reviewer Confidence
4: confident. I am confident in this assessment; the main issues are visible from the paper itself and do not depend on subtle interpretation.