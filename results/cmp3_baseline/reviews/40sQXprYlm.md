## Summary

The paper introduces **Distributed Neural Architectures (DNAs)**, a family of models in which each token (or image patch) follows its own learned path through a collection of computational modules (transformers, MLPs, attention blocks) and routers. This framework generalises Mixture-of-Experts, Mixture-of-Depths, weight sharing, and early-exit mechanisms. DNAs are trained end-to-end on ImageNet (vision) and FineWeb-edu (language) and achieve performance competitive with dense baselines (ViT-small and GPT-2 medium). The authors further demonstrate that DNAs can learn to skip computation (via identity modules) in an input-dependent manner, and that the emergent routing paths exhibit interpretable specialization—e.g., some paths focus on object boundaries, others on background, and rare paths capture specific concepts like brass instruments or puzzle pieces.

## Strengths

- **Original conceptual framework.** DNA unifies several strands of conditional computation (MoE, MoD, parameter sharing, layer skipping) into a single, end-to-end learnable architecture. This perspective is novel and provides a principled way to study emergent connectivity.
- **Thorough two-domain validation.** The same ideas are tested on both vision and language tasks at non-trivial scales (ViT-small and GPT-2 medium), demonstrating the generality of the approach. The fact that a single recipe works in both domains is a positive signal.
- **Interpretability analysis.** The paper does more than report numbers; it provides insightful visualisations (e.g., path heatmaps, class activation–style reconstructions, clustering of patches/tokens that share the same path). The observation that paths follow a power-law distribution and that rare paths capture semantically specific content is genuinely interesting and opens avenues for future analysis.
- **Compute efficiency is learned, not hand-designed.** The use of identity modules with a bias-based skip incentive (inspired by DeepSeek) allows the model to automatically allocate less compute to simpler inputs. The resulting compute distribution is shown to be roughly Gaussian and correlates plausibly with visual/textual complexity.

## Weaknesses

### Fatal
None.

### Major

1. **Modest empirical gains relative to baselines.**  
   - Vision: Top-1 DNA achieves 79.1% vs ViT’s 79.8%; Top-2 DNA achieves 78.8%. These differences are small, but the paper does not provide confidence intervals or statistical tests.  
   - Language: Top-1 DNA’s loss (2.754) is slightly worse than GPT-2 medium (2.720); only the (larger) Top-2 DNA marginally improves (2.674). On downstream tasks the differences are often within 1–2 points, which may be noise.  
   - The paper explicitly states it is not aiming to beat SOTA, which is acceptable for a feasibility study, but the results do not yet present a clear *empirical advantage* that would compel adoption.

2. **Limited comparison to other efficient architectures.**  
   - The baselines are standard dense ViT-small and GPT-2 medium. No comparisons are made to MoE transformers, Mixture-of-Depths, or layer-skip methods of comparable size and compute budget. Without such comparisons, it is difficult to assess whether the DNA approach offers a better accuracy–efficiency trade-off than existing conditional computing methods.  
   - The “30% skip” models in Table 3 do include a GPT-2 with 30% shallower layers, but this is a single, coarse baseline. A more systematic ablation (e.g., comparing to a MoE with the same total parameters) would strengthen the paper.

3. **Scalability concerns are not addressed.**  
   - The largest models have ~600M parameters, far below the scale at which conditional computing typically shows significant advantages (e.g., >1B parameters). The paper’s findings about power-law path distributions and specialization might change at larger scales, and the computational overhead of the routing mechanism (which adds extra parameters and inference cost) is not thoroughly quantified.  
   - The authors leave infrastructure co-design for distributed execution to future work, which is honest but limits the immediate practical value.

4. **Interpretability analysis is entirely qualitative.**  
   - The clustering of patches/tokens by path is compelling, but no quantitative metric (e.g., purity, NMI, or a human evaluation) is provided to confirm that the groups are indeed semantically coherent.  
   - The reconstruction visualizations (Figure 4) are intriguing, but the claim that early steps capture texture/edges and later steps capture large-scale features is based on visual inspection of a few examples. A controlled experiment (e.g., layer-wise probing or concept activation vectors) would lend rigor.

### Minor

- The paper uses the term “distributed” in the sense of distributed computation across modules, not distributed training. The terminology could cause confusion and is not clearly disambiguated.
- The routing probabilities are used to weight the module outputs (Eq. 1), but the top-k selection is based on biased logits (Eq. 2). The interaction between the softmax probabilities and the biases for identity modules is not fully explained.
- The finding that random models also exhibit power-law path distributions (Figure 1 caption) is interesting but not analyzed; it suggests the distribution might be a property of the routing structure rather than learned specialization, which weakens the claim of “emergent” power-law.

### Trivial

- Some sub-figure references in the text are slightly garbled (e.g., “Figs. 3, 4, 13, 8” in the introduction). This is a minor copy-editing issue.

## Nice-to-Haves

- A quantitative metric to measure the quality of the emergent clustering (e.g., intra-cluster vs. inter-cluster similarity of token embeddings).
- Ablation studies that vary the number of modules, routers, and the backbone length to understand their effect on performance and compute usage.
- Analysis of the *training* dynamics—how do paths gradually specialise over the course of training?
- A discussion of the inference cost overhead of the routers (additional forward passes for a linear classifier per step).

## Novel Insights

- The observation that paths through the network follow a power-law distribution, with rare paths capturing highly specific semantic concepts, is a fresh perspective on how conditional computation organises itself.  
- The idea that the same framework can *simultaneously* learn to skip layers, share parameters, and route tokens to specialised modules in a data-dependent way, without explicit architectural constraints beyond the proto-architecture, is a valuable demonstration of the flexibility of learned routing.  
- The finding that parameter sharing in the language domain appears random (unlike vision) suggests that inductive biases or auxiliary losses may be needed to encourage meaningful weight sharing in text, which is a non-obvious and actionable insight.

## Suggestions

1. **Add controlled comparisons to MoE/MoD baselines** with matched parameter counts and compute budgets. Even a small-scale comparison (e.g., 300M–600M) would help position DNAs relative to existing conditional computing methods.  
2. **Quantify the interpretability claims.** Use a metric (e.g., silhouette score on path groups or a human evaluation of path-cluster coherence) to support the claim that paths specialise semantically.  
3. **Report variance** (e.g., standard deviation over multiple seeds) for the main accuracy/loss numbers to establish whether the small gaps to baselines are significant.  
4. **Provide a more detailed efficiency analysis** – measure actual FLOPs per token/sequence rather than just active parameter counts, and compare the overhead of the routers.  
5. **Discuss the “distributed” terminology** more precisely to avoid confusion with distributed computing.

## Score and Decision

The paper introduces a conceptually novel and flexible architecture for conditional computation, demonstrates its feasibility across two domains, and provides an interesting qualitative analysis of the emergent paths. However, the empirical gains over simple dense baselines are modest, the lack of comparisons to other conditional computing methods weakens the evaluation, and the interpretability results are not quantitatively validated. Given the stated goal of the paper (feasibility and analysis, not SOTA), the contribution is solid but the impact is currently limited.  

I recommend a **borderline accept** with the expectation that the above concerns can be addressed in a rebuttal or future work.

MY FINAL SCORE: <score>6</score>  
MY FINAL DECISION: <decision>Accept</decision>