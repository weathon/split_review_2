## Summary
CORE-3D is a training-free pipeline for open-vocabulary 3D scene understanding that combines: (1) progressive multi-granularity mask generation via SemanticSAM, (2) context-aware CLIP embedding using five complementary crops with weighted aggregation (including a contrastive surroundings crop), and (3) symmetric-balanced volumetric merging for multi-view 3D consistency. The framework is further extended with an LLM/VLM-based object retrieval pipeline for handling relational and orientation queries. Experiments on Replica and ScanNet (segmentation) and SR3D+ (retrieval) show improvements over prior zero-shot and training-based baselines.

## Strengths
- **Clear and consistent quantitative improvements**: On Replica, mIoU improves from 0.27 (BBQ-CLIP) to 0.29 and fmIoU from 0.48 to 0.56; on ScanNet, mIoU goes from 0.34 to 0.36 and mAcc from 0.56 to 0.61. On SR3D+ retrieval, overall A@0.1 jumps from 34.2 (BBQ) to 41.8, a substantial margin.
- **Well-structured ablations**: Tables 3–5 independently validate the progressive granularity strategy, context-aware CLIP embedding, and extension mechanism. Table 3 clearly shows that no single granularity level of SemanticSAM matches the progressive scheme, and Table 4 shows the context-aware embedding strongly outperforms fine-tuned OvSeg.
- **Practical and modular design**: The symmetric-balanced IoV merging criterion to avoid false merges (e.g., cushion on sofa) is well-motivated and the multi-stage retrieval pipeline (query parse → candidate mine → VLM verify → LLM reason) is sensibly decomposed.

## Weaknesses

### Fatal
None.

### Major
- **Critical reproducibility gap in the core contribution**: The context-aware CLIP embedding weights $\{w_\text{mask}, w_\text{bbox}, w_\text{large}, w_\text{huge}, w_\text{sur}\}$ are described as "empirically tuned" but their actual values are never reported anywhere in the paper. This is the key hyperparameter of the central contribution and its omission makes the method unreproducible.
- **LLM/VLM not specified**: The retrieval pipeline relies on external API-accessed VLMs and LLMs, but neither the model names, versions, nor any prompt engineering details appear in the main paper. Since results could vary substantially across models, this is a significant reproducibility and comparability issue.
- **Ablation of 3D merging is absent**: The paper never isolates the contribution of the symmetric-balanced IoV merging step. The ablation tables jump from mask generation to CLIP embedding to extension mechanism without testing the 3D consolidation component separately. Given that multi-view consistency is claimed as a core contribution, its ablation is essential.

### Minor
- The overlap threshold parameters $\gamma$ and $\delta$ for the symmetric IoV criterion are not reported or ablated, leaving one key design choice without justification.
- The ScanNet fmIoU improvement of the full method (0.46) over vanilla SAM (0.42) in Table 3 is modest, suggesting limited gains on this metric from the progressive refinement strategy alone on real-world scenes.
- Table 4 conflates two variables by comparing Context-Aware CLIP against OvSeg: OvSeg is fine-tuned for masked regions but uses the same underlying mask quality, making it unclear whether the gap stems from the embedding strategy or the fine-tuning advantage being inverted.

### Trivial
- Computational cost is only partially characterized (mentions RTX4090 + external APIs) without runtime numbers.

## Nice-to-Haves
- Report actual weight values for the context-aware aggregation and a sensitivity analysis showing how performance changes as weights vary.
- An ablation disabling the 3D merging step to quantify its independent contribution.
- Specify which LLM/VLM APIs are used and report performance variance across at least two different models to assess robustness.

## Novel Insights
The most genuinely novel observation is the surroundings crop with a negative weight in the embedding combination, implementing an implicit contrastive mechanism at inference time without any fine-tuning. This inductive bias—penalizing features dominated by environmental context rather than the object—is a simple but non-obvious extension of multi-crop CLIP inference that could transfer to other open-vocabulary tasks beyond 3D mapping.

## Suggestions
- Include the actual embedding weights in the paper (or a supplementary table) and report sensitivity to weight variation.
- Name the specific LLM/VLM models used in the retrieval pipeline and add an ablation with at least one alternative (e.g., a smaller model) to gauge robustness.
- Add a row to the ablation tables with no 3D merging (projecting 2D masks directly) to demonstrate the value of the symmetric-balanced IoV criterion.

## Score and Decision
The paper presents a well-executed engineering contribution that is clearly evaluated and achieves meaningful quantitative improvements across multiple benchmarks. The ideas are not individually radical, but their combination is carefully designed and ablated (at a high level). However, the omission of the core hyperparameter values (embedding weights) is a significant reproducibility issue for a claimed contribution, and the absence of a 3D merging ablation leaves one of three stated contributions unvalidated. These issues are correctable and do not invalidate the results, but they weigh against acceptance in their current state.

MY FINAL SCORE: <score>5.5</score>
MY FINAL DECISION: <decision>Accept</decision>