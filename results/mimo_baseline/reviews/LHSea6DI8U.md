## Summary
The paper proposes STBP, a continual spatio-temporal forecasting framework that pairs a general-purpose backbone (featuring frequency-domain processing and linear graph attention) with a scalable contextual pattern bank. The backbone is frozen after initial training to preserve general knowledge, while the pattern bank expands incrementally via parameter addition and interacts with the backbone through prompt-based gating, enabling adaptation to evolving graph structures while mitigating catastrophic forgetting. Extensive experiments on three real-world streaming datasets demonstrate consistent improvements over CSTF baselines.

## Strengths
- **Clear problem decomposition and motivation**: The paper convincingly identifies two gaps in existing CSTF work—limited backbone capacity and weak coupling between continual strategies and backbones—and proposes a principled separation of concerns (stable backbone vs. adaptive pattern bank) that directly addresses them. The four challenges enumerated (distributional drift, dynamic correlations, catastrophic forgetting, incremental strategy) provide a useful organizing framework.
- **Strong empirical results across multiple settings**: STBP achieves substantial MAE reductions of 21.4% and 21.9% on PEMS-Stream and CA-Stream over the best baselines (Table 1). The few-shot results (Table 2) show even larger margins, and the ablation study (Figure 4) cleanly isolates contributions of each component. These results are consistent across three datasets and all metrics/horizons.
- **Scalability with theoretical grounding**: The linear graph attention mechanism (Eq. 9) reduces spatial modeling complexity from O(N²) to O(N), and the efficiency study (Figure 8) empirically validates this, showing the pattern bank adds only linear overhead as nodes grow. This is practically important for real-world deployment.
- **Insightful visualization of learned representations**: The t-SNE analysis of the pattern bank (Figure 3 and Figure 6) provides compelling evidence that the learned parameters autonomously capture both node heterogeneity (distinct clusters) and relevance (similar temporal dynamics within clusters), supporting the paper's central hypothesis.

## Weaknesses
### Fatal
None.

### Major
- **Limited novelty in individual components**: The core technical ingredients—frequency-domain temporal processing (FreNet), linear attention approximation via random feature mapping, and prompt-based parameter expansion—are all established techniques. While their specific combination for CSTF is new, the paper does not deeply analyze why *this particular* combination works better than alternatives, nor does it contrast with other possible designs (e.g., LoRA-style adapters, prototype-based methods, or elastic weight consolidation adapted for GNNs). The contribution reads more as a well-executed engineering combination than a conceptual advance.
- **Narrow evaluation scope**: Only three datasets are used, all from the traffic/air quality domain with similar temporal resolutions (5-min or hourly). The paper's claims about "general" spatio-temporal forecasting are not convincingly supported without evidence on more diverse domains (e.g., energy, epidemic, social dynamics). The conclusion acknowledges this as future work, but the gap weakens the paper's present claims.
- **Incomplete ablation design**: The ablation removes major components (backbone, DLGA) but does not isolate the three pattern bank components (P₀, P₁, P₂) to quantify their individual contributions. Since the prompt-based guidance mechanism is a central contribution, understanding which sub-component drives performance is important. Similarly, FreNet is not individually ablated despite being a core backbone innovation.

### Minor
- **Few-shot framing is misleading**: The few-shot setting (Table 2) only reduces training data for periods τ > 1 to 10%, while the first period uses full data and the backbone is fully trained. This is better described as a "data-scarce incremental" setting rather than "few-shot forecasting," which typically implies extremely limited data from the start.
- **The 2.35% gain on AIR-Stream is modest**: While the traffic dataset improvements are impressive, the AIR-Stream gain over EAC is small, suggesting the advantage may not generalize uniformly. This asymmetry is not discussed.
- **No analysis of backbone freezing trade-offs**: The backbone is frozen after initial training, but no experiments explore whether periodic fine-tuning, selective layer updates, or a scheduled unfreezing strategy could further improve performance. This rigid design choice is not justified beyond the stability argument.

### Trivial
- Figure 4 bar charts are rendered as approximate numerical tables in the parsed version, making precise comparisons difficult, though this is a parsing artifact.

## Nice-to-Haves
- An analysis of how the pattern bank scales with long-term continual learning (many more incremental periods) would strengthen the scalability claims.
- A comparison against continual learning methods from the broader ML community (e.g., EWC, progressive networks) adapted to the spatio-temporal setting would contextualize the contribution better.
- Discussion of failure cases or conditions under which the frozen backbone assumption breaks down.

## Novel Insights
The paper's genuinely novel insight is that separating a *frozen* general-purpose backbone from an *expandable* node-level pattern bank, connected through prompt-based gating, enables an effective stability-plasticity trade-off specifically for graph-growing continual learning scenarios. The empirical finding that a frozen backbone with linear attention alone matches EAC's performance (the "w/o Backbone" variant under online training) suggests that the backbone quality is a critical bottleneck in existing CSTF methods—a finding worth further investigation. The autonomous emergence of meaningful node clusters in the pattern bank without explicit clustering supervision is also noteworthy.

## Suggestions
- Add individual ablations for P₀, P₁, P₂, and FreNet to pinpoint which prompt-guidance and backbone components matter most.
- Include at least one dataset outside traffic/air quality to support the "general" claim.
- Discuss the AIR-Stream performance gap explicitly—what characteristics of this dataset limit the advantage over EAC?
- Rename the few-shot experiment to avoid conflating it with standard few-shot learning paradigms.

## Score and Decision
The paper presents a well-motivated and well-executed framework with strong empirical results on standard benchmarks. The architecture design is clean and the ablations are mostly convincing. However, the novelty is incremental (combination of known techniques), the evaluation is narrow (three similar-domain datasets), and key ablations are missing. The impressive performance gains on traffic datasets are the strongest argument for acceptance, but the limited generalizability evidence and lack of deeper technical novelty temper enthusiasm. This is a solid application paper that advances CSTF, but falls short of a high-impact contribution.

MY FINAL SCORE: <score>6.0</score>
MY FINAL DECISION: <decision>Accept</decision>