## Summary

The paper proposes SigMap, a foundation model for wireless localization that combines (1) a cycle-adaptive masking strategy for self-supervised pre-training on Channel State Information (CSI) data, designed to prevent models from exploiting periodic shortcuts, and (2) a "map-as-prompt" framework that encodes 3D geographic information through a GNN into lightweight soft prompts for parameter-efficient fine-tuning. The model is evaluated on ray-tracing simulated datasets (DeepMIMO and WAIR-D) for single-BS and multi-BS localization tasks, demonstrating improvements over existing baselines.

## Strengths
- **Creative "map-as-prompt" design**: Encoding 3D building geometry and base station positions via Delaunay triangulation + GCN into prompt tokens is a novel and interpretable way to inject environmental constraints into a pre-trained wireless model. The parameter efficiency (only 0.7% of parameters updated) and the ablation on 3D vs. 2D maps (Table 4) clearly demonstrate the value of this design.
- **Cycle-adaptive masking motivation**: The insight that generic masking strategies in existing wireless SSL methods allow models to exploit periodic CSI shortcuts is well-motivated and physically grounded. Table 3 provides direct evidence that the adaptive masking improves over fixed grid or strip masking (0.673 m vs. 0.753–0.770 m MAE).
- **Comprehensive evaluation structure**: The experiments systematically address key questions—main results (Tables 1–2), masking ablation (Table 3), map modality ablation (Table 4), cross-scenario generalization (Table 5), and parameter efficiency (Table 5b). The generalization to unseen scenarios (DeepMIMO O2 and WAIR-D with 100 cities) with few-shot adaptation is a meaningful test.

## Weaknesses
### Fatal
None.

### Major
- **Synthetic-only evaluation**: All experiments use ray-tracing simulated data (DeepMIMO, WAIR-D). There is no real-world deployment or measurement validation. Ray-tracing simplifications (e.g., idealized material properties, simplified diffraction models) may not reflect the noise, hardware impairments, and environmental dynamics of real wireless systems. This significantly limits confidence in the claimed "practical deployability."
- **Limited and narrow baselines**: The comparison includes only OMP, a basic CNN, SWiT, and LWLM. Several relevant wireless localization methods (e.g., fingerprint-based approaches, recent transformer-based localization, methods using propagation models) are absent. This makes it difficult to assess whether the improvements reflect genuine methodological advances or simply reflect stronger pre-training on a larger corpus.
- **Underspecified cycle-adaptive masking**: Equation 6 defines the mask pattern given parameters d_final, j_0, and w, but the paper does not formally specify how these parameters are computed from the cross-correlation analysis. The connection between the "row-wise cross-correlation" mentioned in the text and the concrete mask generation is left implicit, making the method difficult to reproduce.

### Minor
- **Numerical inconsistency**: The text states SigMAP achieves "1.580 m on WAIR-D Scenario-2" but Table 5 shows 1.880 m MAE. The table value is consistent with the claimed 44.3% improvement over LWLM (3.375 m), suggesting the text contains an error.
- **Graph construction choice unexamined**: Delaunay triangulation is used for graph construction without justification or comparison to alternatives (e.g., k-NN graphs, radius-based graphs, or learned edge construction). Given that the graph structure directly determines what spatial relationships the GNN captures, this choice deserves ablation.
- **Single dataset pre-training**: The model is pre-trained solely on DeepMIMO O1_3p5. Training on more diverse ray-tracing scenarios during pre-training could strengthen the foundation model claims and potentially improve downstream generalization further.

### Trivial
- The radar chart (Figure 5) lacks axis labels with concrete values, making it difficult to quantitatively compare methods beyond visual impression.

## Nice-to-Haves
- Real-world measurement experiments, even on a small scale, would substantially strengthen the paper's claims about practical utility.
- Analysis of failure cases—where does the model struggle, and in what types of environments does the geographic prompt provide the least/most benefit?
- Comparison of the learned representations (e.g., via probing or visualization) to understand what the cycle-adaptive masking captures differently from standard masking.

## Novel Insights
The "map-as-prompt" concept—treating 3D environmental geometry as a conditioning signal through lightweight soft prompts rather than as an input feature—is a genuinely useful conceptual contribution that bridges the prompt-tuning paradigm from NLP/vision to the wireless domain. The observation that 2D bird's-eye maps retain most of the topological benefit (only 8% MAE degradation vs. full 3D) is practically useful, suggesting that simpler map representations suffice for many scenarios.

## Suggestions
- Add at least one real-world measurement campaign to validate the synthetic-to-real transfer.
- Expand baselines to include more localization methods, particularly recent transformer-based and diffusion-based approaches.
- Provide detailed pseudocode or formal specification of the cross-correlation detection and mask generation pipeline to enable reproduction.
- Fix the WAIR-D MAE inconsistency between text and table.

## Score and Decision
The paper presents an interesting and well-structured framework with creative ideas (map-as-prompt, cycle-adaptive masking). However, the synthetic-only evaluation, limited baselines, and underspecified technical details weaken the contribution. The work is a solid application paper but falls short of the methodological novelty and experimental rigor expected at ICLR.

MY FINAL SCORE: <score>4.0</score>
MY FINAL DECISION: <decision>Reject</decision>