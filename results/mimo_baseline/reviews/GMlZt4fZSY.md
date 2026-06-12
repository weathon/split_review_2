## Summary

This paper presents MobileLLM-R1, a series of sub-billion-parameter reasoning models trained on 4.2T tokens (~2T unique tokens resampled) from curated open-source data. The key technical contributions are: (1) a leave-one-out analysis using capability-probing datasets to identify which pre-training corpora benefit reasoning across code, math, and knowledge domains; (2) cross-capability influence-based data mixing to optimize token allocation without benchmark access; and (3) an iterative mid-training co-evolution strategy that uses positive-influence rejection sampling until convergence. MobileLLM-R1-950M achieves AIME 15.5 and matches Qwen3-0.6B while using only 11.7% of its training tokens, substantially outperforming all other fully open-source sub-billion models.

## Strengths

- **Compelling efficiency results**: MobileLLM-R1-950M matches Qwen3-0.6B across multiple reasoning benchmarks (MATH, AIME, LiveCodeBench) with only 4.2T tokens vs. Qwen3's 36T—a 8.6× data efficiency improvement. Compared to fully open-source baselines, the gains are dramatic: 5× higher MATH accuracy than OLMo-1.24B, and 2× higher than SmolLM2-1.7B despite having fewer parameters.

- **Principled and well-ablated data methodology**: The leave-one-out analysis (Figure 3) concretely demonstrates cross-domain dataset contributions—e.g., FineWeb-Edu removal causes the largest degradation across all three capabilities, and StarCoder benefits math more than OpenWebMath benefits code. The influence-based mixing (Eq. 4-5) provides a principled closed-form alternative to heuristic allocation, and Figure 4 shows consistent perplexity improvements on held-out benchmarks not used during training.

- **Novel convergence observation in mid-training**: The iterative data-model co-evolution (Section 3) reveals that influence scores converge toward zero/negative (Figure 5), providing a natural termination criterion indicating dataset exhaustion. Figure 6 demonstrates that subsampled mid-training data outperforms the original throughout training, confirming the compression mechanism works.

- **Rigorous controlled comparisons**: Table 2 provides a fair comparison by fine-tuning all baselines on identical reasoning SFT data, isolating the contribution of better pre-training/mid-training. Table 1 thoroughly ablates the post-training pipeline, showing that staged instruction-then-reasoning training outperforms joint training.

- **Full transparency and reproducibility**: Complete dataset lists, training configurations, and model/code release provide exceptional value to the community, particularly given the growing importance of understanding efficient training recipes for small models.

## Weaknesses

### Fatal
None.

### Major

- **Benchmark-free claim needs stronger verification**: The paper claims no benchmark data is used during training or mixture construction, but the capability-probing datasets are curated via hierarchical rejection sampling from corpora (FineWeb-Edu, OpenWebMath, etc.) that plausibly contain benchmark content. Given that GSM8K, MATH, and HumanEval problems circulate widely on the web, a more explicit verification of leakage-free probing datasets would strengthen the core claim. The authors should describe how they ensure probing dataset content doesn't overlap with evaluation benchmarks.

- **Insufficient comparison with other data mixing baselines**: Figure 4 compares influence-based mixing only against uniform sampling. The methodology builds on AutoMixer (Chang et al., 2025), but lacks comparison with other established approaches like DoReMi, temperature-based domain sampling, or simple loss-based weighting. This makes it hard to isolate the specific contribution of cross-capability influence scoring versus simpler alternatives.

- **Partial confounding from post-training data**: While Table 2's controlled comparison is valuable, the strongest final results (Figure 9) use OpenMathReasoning, OpenScienceReasoning-2, and OpenCodeReasoning-2—large-scale, high-quality SFT corpora that partially obscure how much of the reasoning capability comes from pre-training curation versus post-training data quality. The ablation in Table 1 shows that SFT data choice causes large swings (MATH 16.2–60.0), suggesting post-training dominates the final numbers.

### Minor

- **Resampling strategy underspecified**: The paper states ~2T unique tokens are resampled to 4.2T, but the exact resampling ratios, whether they differ from the influence-based mixing ratios, and why 4.2T was chosen as the total budget are not fully explained.

- **Scaling generalizability unclear**: All experiments are at sub-billion scale. A brief discussion of whether the data curation insights transfer to larger models would broaden the paper's impact claims.

### Trivial
- Some table entries in Figure 8 appear garbled (likely parser artifact), making direct verification of certain numbers difficult.

## Nice-to-Haves

- A comparison of MobileLLM-R1's data mixture against OLMo-2 and SmolLM's published mixtures at the same model scale, to quantify the gains from mixture optimization alone.
- Analysis of whether the cross-capability influence insight (e.g., StarCoder benefiting math) holds at larger scales or changes qualitatively.

## Novel Insights

The finding that code data (StarCoder) transfers more effectively to math than math data transfers to code (Section 2.1.2) challenges the conventional wisdom from Lewkowycz et al. (2022) about mathematical data disproportionately benefiting code. Combined with the observation that web data serves as "glue" binding heterogeneous domains (FineWeb-Edu having the largest cross-domain impact), these findings provide actionable insights for designing efficient data mixtures for small models. The convergence-of-influence observation—that iterative co-evolution naturally terminates as samples reach zero or negative influence, indicating dataset exhaustion—offers a practical and principled stopping criterion that could inform mid-training protocols broadly.

## Suggestions

- Add a contamination analysis for capability-probing datasets by checking overlap with held-out evaluation benchmarks using n-gram or embedding-based matching.
- Include comparison with at least one non-influence-based data mixing baseline (e.g., DoReMi or temperature scaling) to establish the incremental value of cross-capability influence scoring.
- Clarify the relationship between the influence-based mixing ratios and the actual resampling applied for the 4.2T training run.

## Score and Decision

This paper makes a valuable and well-supported contribution to training efficient small reasoning models. The data-centric methodology is principled, the experiments are thorough with controlled ablations, and the efficiency gains over both fully open-source and partially open-source baselines are substantial and practically meaningful. The core claim—that strong reasoning can emerge from ~2T carefully curated tokens rather than 10T+—is well-supported and important for the community. While the benchmark-free claim and insufficient comparison with alternative mixing strategies are notable gaps, they do not invalidate the paper's contributions.

MY FINAL SCORE: <score>7.0</score>
MY FINAL DECISION: <decision>Accept</decision>