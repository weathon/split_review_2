## Summary

This paper proposes a hierarchical attention model for code embeddings in reinforcement learning (RL) settings, combining token-level, function-level, and module-level attention mechanisms with graph-structured dependencies. The method integrates transformer-based sequential processing with graph attention networks operating on abstract syntax trees and code dependency graphs, producing state representations that are end-to-end optimized for RL policy learning. The authors evaluate their approach on code completion, program repair, and algorithmic problem solving tasks, reporting improvements over several baseline methods.

## Strengths

- The paper addresses an important and underexplored problem: learning hierarchical code representations specifically optimized for reinforcement learning objectives, rather than using pre-trained embeddings in isolation.
- The multi-level attention architecture (token, function, module) is well-motivated by the natural hierarchical structure of code, and the integration of both sequential (transformer) and structural (GAT) attention mechanisms is a sensible design choice.
- The ablation study (Table 2) provides clear evidence that each component of the model contributes positively to overall performance, with token-level attention being the most impactful.

## Weaknesses

### Fatal

- **The paper lacks any comparison to state-of-the-art code models such as CodeLlama, StarCoder, or GPT-based code models.** Given that large language models (LLMs) for code have achieved remarkable results on code completion, repair, and generation tasks, the absence of these baselines makes it impossible to assess whether the proposed method offers any meaningful advantage over current practice. The strongest baseline (CodeBERT) is a 2020 model that is now several generations behind.

- **The experimental setup is fundamentally flawed for evaluating RL state representations.** The paper describes tasks (code completion, program repair, algorithmic problem solving) that are standard supervised learning or generation benchmarks, not RL environments. There is no description of the MDP formulation, reward function design, action space details, or environment dynamics that would make these tasks RL problems. The "RL agent" appears to be a wrapper around what is essentially a supervised learning or generation task, raising serious questions about whether the RL framing adds any value or whether the results simply reflect standard supervised fine-tuning.

- **The paper does not release code, data, or model checkpoints, making the results completely irreproducible.** Given the complexity of the proposed architecture and the lack of implementation details (e.g., how ASTs are constructed, how CDGs are built, how the RL environment is implemented), independent verification is impossible.

### Major

- **The writing quality is extremely poor, with numerous nonsensical sentences, grammatical errors, and unclear technical descriptions.** Examples include: "exciting results with Neural Investigations," "Sequential or Tele-centric analysis yet, usually these techniques are restricted to either sequential or structural aspects Peps by itself," "The hierarchical cherry-picking of the code embedding system," and "We use LLM polish writing based on our original paper." This level of writing is unacceptable for a top-tier venue and suggests the paper may not have been carefully prepared.

- **The paper claims to use "Proximal Policy Optimization (PPO)" but provides no details about the policy network architecture, action space, reward shaping, or environment implementation.** Without these details, the RL claims cannot be evaluated.

- **The scalability analysis (Figure 3) is presented with vague "Baseline 1" and "Baseline 2" labels that are never defined.** This makes the comparison meaningless.

- **The paper cites several references that appear to be fabricated or do not exist in the form described.** For example, "Gomez et al., 2025" is cited with a URL "ngruver.github.io" which is not a valid publication venue, and several references have suspicious formatting or incomplete bibliographic information.

### Minor

- The paper claims "6.6% absolute improvement in code completion BLEU score" but the table shows 72.9 vs 68.4 (CodeBERT), which is a 4.5 point difference, not 6.6.
- The t-SNE analysis and nearest neighbor analysis are mentioned but no actual visualizations or quantitative results are presented.
- The paper states "All metrics were computed on held-out test sets not seen during training" but does not specify how the datasets were split.

### Trivial

- The paper uses inconsistent formatting for equations and citations throughout.
- Figure 1 is described in the caption but the actual figure appears to be a placeholder or low-quality rendering.

## Nice-to-Haves

- A comparison with modern code LLMs (CodeLlama, StarCoder, GPT-4) would be essential to establish the practical value of the approach.
- Open-sourcing the code, environments, and trained models would greatly increase the paper's impact and credibility.
- A clearer explanation of why the RL formulation is necessary rather than using supervised learning would help motivate the work.

## Novel Insights

None beyond the paper's own contributions. The idea of hierarchical attention for code is not new (e.g., SG-Trans, CodeBERT, various AST-based methods), and the specific combination of transformer + GAT with multi-level attention is an incremental engineering contribution rather than a conceptual breakthrough. The paper does not provide theoretical analysis or insights into why the hierarchical approach works better than alternatives.

## Suggestions

- The authors should either significantly improve the writing quality or have the paper professionally edited before resubmission.
- The experimental setup needs to be completely rethought: either properly formulate the tasks as RL problems with clear MDP definitions, or reframe the work as a supervised representation learning method.
- Modern code LLM baselines must be included for the results to be meaningful.
- Code and data should be released to enable reproducibility.

## Score and Decision

The paper has fundamental flaws that invalidate its core claims: the experimental setup is not properly described as RL, the baselines are outdated, the writing is extremely poor, and the results cannot be reproduced. The contribution is incremental and not convincingly demonstrated.

MY FINAL SCORE: <score>3</score>
MY FINAL DECISION: <decision>Reject</decision>