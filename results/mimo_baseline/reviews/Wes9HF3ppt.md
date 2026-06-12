## Summary
The paper introduces Insertion Language Models (ILMs), which generate sequences by jointly predicting a token and its insertion position at each step, enabling arbitrary-order generation of variable-length sequences. The authors propose a denoising training objective that approximates insertion distributions using normalized token counts, and demonstrate on planning tasks (star graphs, zebra puzzles) and text generation/infilling that ILMs overcome specific failure modes of autoregressive models (ARMs) and masked diffusion models (MDMs).

## Strengths
- **Compelling problem identification and motivation.** The paper clearly articulates limitations of both ARMs (fixed left-to-right order, poor planning) and MDMs (simultaneous unmasking causing incoherence, fixed-length mask constraint preventing arbitrary infilling). The chef/dessert example and Figure 1 effectively illustrate these failure modes.

- **Dramatic improvements on planning tasks.** On star graphs with variable arm lengths, ILMs achieve 99–100% sequence accuracy while MDMs drop to 21–36% and standard ARMs to 23–32% (Table 1). On zebra puzzles, ILMs reach 90% vs. 82.6% (MDM) and 81.2% (ARM). These are clean, convincing demonstrations of the method's core advantage.

- **Principled training methodology.** The paper carefully explains why naive trajectory-based training has high variance (Appendix D) and proposes a practical approximation using normalized counts of dropped tokens as insertion distribution targets. The training procedure is well-specified with clear algorithms (Algorithms 1 and 2) and a helpful diagram (Figure 2).

- **Comprehensive and multi-faceted evaluation.** The paper evaluates on synthetic planning tasks, unconditional text generation (using both NLL under Llama 3.2 3B and Prometheus LLM judge), and infilling, across two datasets with different characteristics (LM1B and TinyStories). The inclusion of the Insertion Transformer baseline is also valuable.

- **Honest discussion of limitations.** The authors transparently acknowledge that ILMs are slightly worse than ARMs on text NLL, cannot cache hidden states, and use a biased training objective.

## Weaknesses
### Fatal
None.

### Major
- **Scale of experiments limits the strength of text generation claims.** All text experiments use ~85M parameter models on medium-sized corpora (LM1B, TinyStories). On standard text generation, ILMs are still worse than ARMs in NLL (2.14 vs. 2.11 on Stories; 4.67 vs. 3.94 on LM1B). While the authors attribute this to training token efficiency, the gap is non-trivial on LM1B (~19% relative increase), and without larger-scale experiments it is unclear whether this gap persists, narrows, or widens with scale.

- **MDM baseline may be suboptimal.** The MDM uses tau-leaping sampling, which the paper's own related work section acknowledges leads to simultaneous unmasking and incoherence. More competitive MDM inference strategies (greedy unmasking, top-k sequential unmasking from Gong et al., 2024; Zheng et al., 2024) are mentioned but not compared against. This makes the MDM vs. ILM comparison on text generation less decisive.

- **Insufficient analysis of the biased training objective.** The paper admits the training objective is biased but does not quantify or analyze the impact of this bias. How does the quality of the learned insertion distribution degrade as a function of sequence length or vocabulary size? Are there systematic failure modes introduced by this approximation? This is a core methodological choice that deserves deeper analysis.

### Minor
- **Inference cost analysis is incomplete.** Figure 6 shows ILMs take ~2x the per-token generation time of ARMs on the Stories dataset, but no wall-clock comparison is provided for the planning tasks. Since each ILM step requires a full forward pass over the growing sequence (no KV caching), the cost scales quadratically with sequence length, which could be significant for longer sequences.

- **Infilling evaluation is limited.** The infilling comparison only includes MDMs (not ARMs with fill-in-the-middle training), and the evaluation metrics (percentage change in NLL) are somewhat indirect. A more direct evaluation of infilling quality (e.g., human evaluation or task-specific metrics) would strengthen this claim.

- **The LLM judge results (Figure 5) show modest differences.** While ILMs outperform MDMs on several metrics, the differences between ILMs and ARMs are small and inconsistent across metrics and datasets, making it hard to draw strong conclusions about text generation quality.

### Trivial
None.

## Nice-to-Haves
- A comparison against MDMs with sequential (greedy or top-k) unmasking at inference time, to isolate the benefit of the ILM training objective from the benefit of sequential generation.
- Analysis of how the number of insertion steps scales with sequence length and how this affects both quality and computational cost.
- Experiments on a larger dataset or with larger models to assess scalability.

## Novel Insights
The paper's most novel insight is that dropping tokens entirely (rather than masking them) and learning to predict their insertion positions enables both out-of-order generation and variable-length sequence modeling within a unified framework. The demonstration that MDMs' reliance on absolute token positions causes them to fail on variable-length planning tasks (star graphs), while ILMs' use of relative positions allows them to succeed, is a genuinely useful finding for the community. The connection between MDMs and ILMs—viewing ILMs as MDMs where masks are removed and generation is strictly sequential—provides a clean conceptual framework.

## Suggestions
- Compare against MDMs with sequential unmasking inference strategies to make the comparison fairer and to isolate the contribution of the training objective vs. the inference procedure.
- Provide a more thorough analysis of the biased training objective, including ablations on how the approximation quality degrades with sequence length.
- Include wall-clock time comparisons for the planning tasks to give a complete picture of the efficiency-accuracy tradeoff.

## Score and Decision
The paper makes a genuine contribution by introducing a practical training framework for insertion-based language models and demonstrating clear advantages on tasks requiring out-of-order generation. The synthetic experiments are compelling and well-designed. However, the text generation results don't clearly surpass ARMs, the MDM baseline may be suboptimal, the biased training objective lacks thorough analysis, and the experiments are at a limited scale. These factors place the paper at the borderline.

MY FINAL SCORE: <score>6</score>
MY FINAL DECISION: Accept