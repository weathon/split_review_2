## Summary

This paper introduces Distributed Neural Architectures (DNA), a framework where tokens follow individual paths through a collection of computational modules (transformers, MLPs, attention) and routers, with connectivity learned end-to-end. The authors demonstrate that DNA models are competitive with dense baselines in both vision (ImageNet) and language (FineWeb-Edu) domains, can learn to allocate compute efficiently, and exhibit interpretable emergent specialization of paths and modules.

## Strengths

- **Novel and ambitious framework**: The paper proposes a genuinely flexible architecture that generalizes multiple conditional computing approaches (MoE, MoD, parameter sharing, early exit) into a unified framework where token paths are learned end-to-end. This is a conceptually interesting direction that could influence future architecture design.

- **Comprehensive empirical validation across two domains**: The authors demonstrate feasibility in both vision (ImageNet classification) and language (autoregressive language modeling), showing competitive performance against dense baselines in both settings. This cross-domain validation strengthens the claim that DNAs are a general approach.

- **Rich interpretability analysis**: The paper provides extensive analysis of emergent patterns, including path distributions following power laws, interpretable routing decisions (e.g., boundary patches in vision, punctuation/verb grouping in language), and reconstruction-based visualization of routing decisions. The analysis of compute allocation (Fig. 5) showing that boundary-heavy images require more compute is particularly insightful.

- **Honest and nuanced presentation**: The authors clearly state limitations (e.g., "not focused on beating SOTA", models are "way too small" for language), report both successes and failures (e.g., parameter sharing in language being random rather than meaningful), and provide a balanced discussion.

## Weaknesses

### Fatal
None.

### Major
- **Limited scale and compute budget**: The language models are trained on only 21B tokens (compared to typical 100B+ for models of this size), and the authors acknowledge models are "vastly underparametrized" for the dataset. The vision models are at ViT-Small scale. While the paper's goal is feasibility demonstration, the limited scale raises questions about whether the observed phenomena (power-law paths, interpretable routing) persist at practical model sizes where conditional computation matters most.

- **No systematic comparison to existing conditional computation methods**: The paper claims DNAs generalize MoE, MoD, parameter sharing, etc., but provides no direct comparison to these methods as baselines. For example, how does DNA compare to a standard MoE transformer with the same parameter count and compute budget? Without such comparisons, it's unclear whether the DNA framework offers practical advantages over simpler, well-understood conditional computation approaches.

- **Limited evidence for the "distributed" claim**: The paper's analysis shows that routing patterns are interpretable and follow power laws, but the claim that computation is truly "distributed" (as opposed to hierarchical with learned skipping) is not strongly supported. The flow diagrams (Fig. 2, 6) show that most tokens still pass through a dense backbone before becoming sparse, and the effective number of compute nodes per step is relatively small (1-2.5). The architecture may be better described as "learned sparse routing" rather than truly distributed computation.

### Minor

- **No ablation studies on key design choices**: The paper makes several empirical design choices (backbone layers, identity modules with bias trick, specific routing formulation in Eq. 1) without ablation studies to justify them. For example, how critical is the backbone? How does performance change with different numbers of modules or routers?

- **Missing analysis of training efficiency**: The paper focuses on inference efficiency but does not discuss training cost. DNA models have more total parameters than baselines (e.g., 34M vs 22M for vision), and the routing mechanism likely adds training overhead. A discussion of training compute/memory would help contextualize the approach.

- **The "distributed" framing may be overstated**: The paper claims DNAs are "not feed-forward" and allow "information to flow between any pair of computing modules," but the actual implementation uses a sequential step structure with routers at each step, and the flow diagrams show largely feed-forward patterns with limited branching. The term "distributed" in the title may overclaim relative to what is demonstrated.

### Trivial

- The paper uses "distributed" in a non-standard way that could be confused with distributed training/systems. A brief clarification early on would help.

## Nice-to-Haves

- A direct comparison to standard MoE or MoD baselines with matched compute budgets would significantly strengthen the paper's claims about the advantages of the DNA framework.
- Ablation studies on key design choices (number of backbone layers, number of modules, identity module bias hyperparameters) would help understand what drives performance.
- Analysis of scaling behavior: does the DNA advantage grow or shrink with model size?

## Novel Insights

The paper's most novel insight is that when tokens are allowed to learn their own paths through a network, the resulting path distribution follows a power law, and the emergent routing patterns are interpretable (e.g., boundary patches in vision, punctuation/verb grouping in language). The finding that compute allocation correlates with visual complexity (boundary-heavy images requiring more compute) is a clean and intuitive result. The observation that parameter sharing emerges without explicit incentivization, but is meaningful in vision yet random in language, is a nuanced finding that suggests domain-specific dynamics.

## Suggestions

1. Add direct comparisons to standard conditional computation baselines (MoE, MoD) with matched compute budgets to demonstrate the practical advantages of the DNA framework.
2. Include ablation studies on key design choices: number of backbone layers, number of modules, the effect of the identity module bias hyperparameters.
3. Report training compute/memory costs to contextualize the inference efficiency gains.
4. Consider scaling experiments to verify whether the observed phenomena (power-law paths, interpretable routing) persist at larger model sizes.

## Score and Decision

The paper presents a novel and ambitious framework with thorough empirical validation across two domains and rich interpretability analysis. The main limitations are the lack of comparison to existing conditional computation baselines and the relatively small scale of experiments, which prevent strong conclusions about practical advantages. However, the paper's stated goal is feasibility demonstration and analysis, not SOTA, and it succeeds at this. The work is original, well-executed within its scope, and provides valuable insights. I recommend borderline accept.

MY FINAL SCORE: 6.0score</score>
MY FINAL DECISION: Accept</decision>