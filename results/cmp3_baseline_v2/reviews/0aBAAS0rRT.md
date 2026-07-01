## Summary
The paper proposes SigMap, a multimodal foundation model for wireless localization that introduces two key innovations: (1) a cycle-adaptive masking strategy for self-supervised pre-training on CSI data that disrupts periodic shortcuts, and (2) a “map-as-prompt” framework that encodes 3D geographic information via graph neural networks into lightweight soft prompts for parameter-efficient cross-scenario adaptation. Experiments on simulated DeepMIMO and WAIR-D datasets show strong performance on single-BS and multi-BS localization tasks, outperforming several baselines.

## Strengths
- **Novel problem framing and approach**: The idea of using 3D map information as soft prompts for wireless localization is creative and addresses a real limitation of existing data-driven methods that ignore environmental geometry.
- **Cycle-adaptive masking is well motivated**: The paper correctly identifies that periodic patterns in CSI can be exploited as shortcuts by standard masked autoencoders, and the proposed adaptive masking strategy is a principled solution to force learning of global signal representations.
- **Strong empirical results**: SigMap achieves substantial improvements over baselines (e.g., 34.4% MAE reduction in single-BS NLoS, 14.7% in multi-BS) and demonstrates good few-shot generalization to unseen environments with minimal parameter updates (0.7% of total parameters).
- **Parameter efficiency is clearly demonstrated**: The fine-tuning stage updates only 0.085M parameters and completes in 30 minutes, making the approach practical for deployment.

## Weaknesses
### Fatal
None.

### Major
1. **Overclaim of zero-shot generalization**: The abstract states “strong zero-shot generalization in unseen environments,” yet Section 4.5 explicitly fine-tunes the task heads on ~100 target samples per scenario. This is few-shot, not zero-shot. The claim is misleading and should be corrected to “few-shot” or “minimal fine-tuning” throughout the paper.
2. **Insufficient detail on cycle-adaptive masking**: The periodicity detection algorithm (e.g., how \(d_{\text{final}}\) is computed from cross-correlation) is not described. Equation (6) defines the mask pattern but omits the detection procedure, making the method difficult to reproduce. The paper should provide the full algorithm or a clear reference.
3. **Modest advantage of 3D over 2D map prompts**: Table 4 shows that using a 2-D bird’s-eye view only degrades MAE by 8% relative to the full 3-D mesh. This suggests that most of the benefit comes from topological/LoS cues rather than 3D geometry, weakening the claim that 3D map integration is a key innovation. The paper acknowledges this but does not sufficiently discuss the implications.

### Minor
- **No real-world validation**: All experiments use simulated data (DeepMIMO, WAIR-D). While this is common in the field, the paper would benefit from a discussion of potential sim-to-real gaps.
- **Missing error bars or statistical significance**: Results are averaged over 5 runs but no standard deviations are reported, making it hard to assess the variability of the improvements.
- **Inconsistent naming**: The method is called “SigMap” in the abstract and “SIGMAP” in tables and figures.
- **NLoS-aware attention mechanism is vague**: Equation (11) is presented as a key component but the paper does not explain how \(\mathbf{W}_{\text{NLoS}}\) is learned or how it explicitly models multipath propagation.

### Trivial
None.

## Nice-to-Haves
- Include standard deviations or confidence intervals for all main results.
- Compare with additional foundation-model-based baselines (e.g., WirelessGPT, LWM) to better contextualize the contribution.
- Release code and pre-trained models to facilitate reproducibility and future research.

## Novel Insights
None beyond the paper’s own contributions.

## Suggestions
- Correct the zero-shot claim to few-shot or minimal fine-tuning, and adjust the abstract and introduction accordingly.
- Provide a detailed description of the periodicity detection algorithm used in cycle-adaptive masking (e.g., pseudo-code or explicit equations).
- Discuss the implications of the small gap between 2-D and 3-D map prompts, and clarify what specific 3D information is most valuable.
- Add error bars to all tables and consider a real-world dataset or a discussion of sim-to-real challenges.

## Score and Decision
**Score**: 4  
**Decision**: Reject  

The paper presents a novel and well-motivated approach with strong empirical results on simulated data. However, the major overclaim of zero-shot generalization and the lack of detail on the core masking algorithm undermine the paper’s credibility and reproducibility. These issues must be fully resolved before the paper can be accepted.

MY FINAL SCORE: <score>4</score>  
MY FINAL DECISION: <decision>Reject</decision>