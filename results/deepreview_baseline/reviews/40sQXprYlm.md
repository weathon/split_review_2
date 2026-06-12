##Summary

This paper introduces Distributed Neural Architectures (DNA), where each token can follow its own learned path through a collection of modules (transformer, MLP, attention, etc.) via end-to-end trained routers. The architecture generalizes mixture-of-experts, mixture-of-depths, and parameter sharing. The authors train DNA models in vision (ImageNet) and language (FineWeb-Edu) domains, showing they are competitive with dense baselines, can learn to allocate compute efficiently, and exhibit emergent interpretable structures such as power-law path distributions and module specialization.

## Strengths

- **Novel and ambitious architecture**: The idea of fully flexible, token-dependent routing through arbitrary module sequences is a natural and interesting generalization of existing conditional computation methods. The paper is among the first to explore this at scale in both vision and language.
- **Comprehensive empirical study**: The authors train multiple DNA variants (top-1, top-2, with skip) in two domains, compare to dense baselines, and provide extensive analysis of routing patterns, compute allocation, parameter sharing, and interpretability.
- **Rich qualitative analysis**: The visualizations of path distributions, module flow, and reconstructed images/tokens offer valuable insights into how the model organizes computation. The observation that path distributions follow a power-law even in random models is intriguing.
- **Clear framing of limitations**: The paper honestly states it is not focused on beating SOTA but on demonstrating feasibility and analyzing emergent structure, which sets appropriate expectations.

## Weaknesses

### Fatal
None.

### Major

1. **Marginal performance gains over simpler baselines**: The DNA models are competitive but not clearly superior. In vision, top-1 DNA (79.1%) and top-2 DNA (78.8%) are slightly worse than ViT-small (79.8%). In language, top-1 DNA underperforms GPT-2 medium on most benchmarks, and top-2 DNA shows only small improvements on some tasks. The complexity of DNA is hard to justify when a standard transformer with the same active parameter count performs similarly or better.

2. **Efficiency gains come with significant performance degradation**: The models trained with explicit skip targets (25% skip in vision, 30% skip in language) show notable drops in accuracy/loss. For example, top-2 DNA with 30% skip in language has perplexity 52.6 vs. 31.5 for the non-skip version, and downstream scores drop substantially. The trade-off is not compared to simpler efficiency methods (pruning, distillation, early exit), making it unclear whether DNA offers a favorable cost-performance frontier.

3. **Lack of comparison to existing conditional computation methods**: The paper compares only to dense baselines. Given that DNA is presented as a generalization of MoE, MoD, and layer-skip, it is essential to compare against these methods under controlled settings (e.g., same parameter count, compute budget). Without such comparisons, the added value of the full flexibility remains unclear.

4. **Qualitative analysis is not rigorously validated**: The interpretability claims (e.g., path specialization, grouping of similar tokens) are supported by a few hand-picked examples. More quantitative evaluation (e.g., clustering metrics, probing tasks, or human evaluation) would strengthen the conclusions. The power-law observation is noted but not analyzed in depth (e.g., how it changes with training, model size, or task).

5. **Language experiments are underpowered**: The language models are trained on only 21B tokens and are described as "vastly underparametrized." This limits the generality of the findings. The conclusion that parameter sharing in language is "random" may be an artifact of insufficient training or model scale.

### Minor

- The naming "top-1 DNA" and "top-2 DNA" could be confused with top-k routing; the paper uses k=1 or 2, which is clear but the terminology is slightly overloaded.
- The flow diagrams (Figures 2 and 6 bottom) are visually dense and hard to interpret; the key message (dense backbone followed by sparse routing) could be conveyed more clearly.
- The compute efficiency mechanism (identity modules with bias trick) is a form of explicit regularization, not purely emergent from the architecture. The paper could clarify this distinction.

### Trivial

- Some figure captions are duplicated in the text (e.g., Figure 1 caption appears three times), likely a formatting artifact.

## Nice-to-Haves

- Comparison to MoE, MoD, or layer-skip baselines with matched compute/parameters.
- Quantitative evaluation of interpretability (e.g., path consistency across similar inputs, probing classifiers for module specialization).
- Ablation on the number of modules, routers, and backbone layers to understand design choices.
- Scaling experiments to larger models and datasets to see if DNA's benefits grow with scale.

## Novel Insights

Beyond the paper's own contributions, the observation that path distributions follow a power-law even in randomly initialized DNA models is noteworthy. It suggests that the routing architecture itself induces a heavy-tailed usage pattern, which training then refines. This could be a fundamental property of such flexible routing systems and may inform future design of sparse or modular networks.

## Suggestions

- Add controlled comparisons to MoE and MoD baselines to isolate the benefit of full routing flexibility.
- Provide quantitative metrics for interpretability (e.g., clustering purity of paths, correlation with human-annotated concepts).
- Report the performance-efficiency trade-off more systematically, including Pareto curves comparing DNA to other efficiency methods.
- Consider training larger language models for more tokens to see if the observed "random" parameter sharing becomes structured.

## Score and Decision

The paper presents a novel and interesting architecture with thorough qualitative analysis, but the empirical results do not convincingly demonstrate that the added complexity is worthwhile. The performance is on par with simpler baselines, and the efficiency gains come with significant degradation. The lack of comparison to existing conditional computation methods weakens the contribution. While the work is exploratory and well-executed, it does not yet provide sufficient evidence of practical value or scientific insight to warrant acceptance at a top venue.

MY FINAL SCORE: <score>4</score>
MY FINAL DECISION: <decision>Reject</decision>