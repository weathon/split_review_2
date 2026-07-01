## Summary

The paper identifies and formalizes the “copy-paste artifact” in identity-consistent (ID-consistent) image generation—where models replicate the reference face rather than synthesizing the identity with natural variations. To address this, the authors contribute: (1) **MultiID-2M**, a large-scale paired multi-person dataset (500k group photos with multiple references per identity plus 1.5M unpaired images); (2) **MultiID-Bench**, a benchmark with a copy-paste metric and standardized evaluation; and (3) **WithAnyone**, a diffusion model built on FLUX that uses paired training, a ground-truth-aligned ID loss, and an InfoNCE contrastive loss with extended negatives to reduce copy-paste while maintaining high identity fidelity. Experiments show that WithAnyone achieves a favorable balance, breaking the typical trade-off between similarity and artifacts, and outperforms many existing methods both quantitatively and in user studies.

## Strengths

- **Clear problem formulation and metric**: The paper clearly identifies the copy-paste artifact, which is often overlooked in ID generation. The proposed copy-paste metric \(\mathcal{M}_\text{CP}\) and the use of Sim(GT) as the primary similarity metric are principled ways to quantify this problem, moving beyond the common practice of only reporting Sim(Ref) that inadvertently rewards copying.
- **Significant dataset and benchmark contributions**: MultiID-2M is a large-scale, open-source dataset with paired multi-person references—a scarce resource that enables training strategies beyond reconstruction. MultiID-Bench provides a standardized evaluation protocol with diverse metrics (ID similarity, copy-paste, identity blending, CLIP scores, aesthetics) that will benefit future research.
- **Sound training design to mitigate copy-paste**: The four-phase training pipeline (reconstruction→caption→paired tuning→quality tuning) and the combination of ground-truth-aligned ID loss and contrastive loss with extended negatives are well motivated by the problem analysis. Ablations confirm the importance of each component.
- **Comprehensive evaluation**: The paper compares against 12+ baselines spanning general customization models, face customization models, and VLMs, on both single- and multi-person subsets. Qualitative examples clearly illustrate the copy-paste issue and the improved controllability of WithAnyone.
- **Open-source release**: Code, models, and datasets are publicly released, supporting reproducibility and extending the contribution to the community.

## Weaknesses

### Fatal
None.

### Major
1. **Ethical and licensing concerns with the dataset**: MultiID-2M is constructed by scraping web images of celebrities under Creative Commons filters. Although the authors provide an ethics statement and anonymization (no personal names in training), the use of real people’s faces—even of public figures—raises privacy and consent questions that may be sensitive for the ICLR community. The dataset construction pipeline and the release terms should be scrutinized, and the paper would benefit from a clearer discussion of how the dataset complies with emerging norms on face data.

2. **Limited evidence that the trade-off is truly “broken”**: The paper claims that WithAnyone breaks the long-standing trade-off between identity similarity and copy-paste artifacts. While Fig. 5 shows WithAnyone deviating from the regression curve, the quantitative results (Table 1) show that on Sim(GT) WithAnyone (0.460) is slightly below InstantID (0.464) and UMO (0.458) on the single-person subset. The improvement in copy-paste is substantial, but the claim of “breaking” the trade-off may be overstated—it is more accurate to say WithAnyone achieves a better Pareto point. The paper should soften this claim or provide statistical significance tests.

3. **Moderate performance on multi-person subsets**: In the 2-person and 3-4 person subsets (Table 2), WithAnyone’s Sim(GT) is competitive but not clearly state-of-the-art (e.g., GPT-4o and DreamID sometimes score higher). The copy-paste metric is also not consistently lowest (e.g., on 2-people subset, OmniGen2, UNO, GPT have lower CP). The paper should discuss why these cases are harder and what limits the model’s advantage in multi-ID settings.

### Minor
1. **User study sample size**: The user study uses only 10 participants and 230 groups, which may limit statistical power. While the results are broadly consistent with automatic metrics, the paper should acknowledge this limitation more explicitly.

2. **Copy-paste metric’s sensitivity**: The metric \(\mathcal{M}_\text{CP}\) is defined with a normalization by \(\max(\theta_\mathbf{tr},\varepsilon)\). When the ground-truth and reference embeddings are very close (small \(\theta_\mathbf{tr}\)), the metric can be unstable. The threshold \(\varepsilon\) is not discussed. A sensitivity analysis would strengthen the metric’s credibility.

3. **Ablation on multi-ID setting**: Ablations (Table 3 and Fig. 7) are performed only on the single-person subset. It would be informative to see how each component affects multi-person generation, where copy-paste is most problematic.

### Trivial
- None.

## Nice-to-Haves
- Provide a version of the dataset that uses synthetic or consent-collected faces (e.g., from volunteer studies) to entirely sidestep privacy concerns, though this is a large additional effort.
- Analysis of how the extended negative pool size (4096 vs. batch size) affects the contrastive loss; the paper ablates to 63 negatives but does not investigate other sizes.
- A breakdown of copy-paste artifacts by expression/pose change (e.g., when the prompt requires a smile vs. neutral) to further demonstrate controllability.

## Novel Insights
The paper’s central insight—that excessive identity similarity in generative models is often achieved via trivial copy-paste rather than genuine identity preservation, and that this can be quantified by comparing generated-to-reference vs. generated-to-ground-truth embeddings—is a valuable conceptual clarification for the field. The idea that paired multi-person data is essential to break this shortcut, and that reconstruction-only training inherently exacerbates it, is clearly articulated and empirically validated. The ground-truth-aligned ID loss (using GT landmarks to avoid noisy extraction from generated images) is a practical technical contribution that can be adopted by other methods.

## Suggestions
- Moderate the claim about “breaking the trade-off” to “achieving a better Pareto point” or “substantially shifting the Pareto frontier” to be more precise.
- Provide a more thorough discussion of the dataset’s limitations (e.g., potential cluster noise, bias toward celebrities, geographic/nationality distribution) and how these affect the model’s generalization.
- Include an analysis of the copy-paste metric’s robustness to small \(\theta_\mathbf{tr}\) and set \(\varepsilon\) explicitly.
- Consider releasing a small-scale validation set with human-verified pairings to further benchmark the dataset quality.

## Score and Decision

**Score**: 8  
**Decision**: Accept

**Rationale**: The paper makes three significant contributions—a large-scale paired dataset, a comprehensive benchmark with a novel copy-paste metric, and a model that demonstrably reduces copy-paste while preserving high identity fidelity. The problem is well-motivated, the experiments are thorough, and the release of open-source assets ensures broad impact. The weaknesses (dataset ethics, moderate overclaim, minor evaluation gaps) are addressable and do not invalidate the core contributions. This work advances the state of the art in ID-consistent generation and provides valuable resources for the community.

MY FINAL SCORE: 8<score>8</score>
MY FINAL DECISION: Accept<decision>Accept</decision>