## Summary

This paper proposes PIRN, a framework for few-shot multimodal anomaly detection using a prototype-driven reconstruction approach. It introduces three core innovations: Balanced Prototype Assignment (BPA) using optimal transport to prevent codebook collapse, Adaptive Prototype Refinement (APR) that dynamically updates prototypes during inference to cover unseen normal variations, and Multimodal Normality Communication (MNC) that exchanges high-level normal cues across RGB and surface-normal modalities. Experiments on MVTec 3D-AD, Eyecandies, and Real-IAD D3 show consistent improvements over existing methods, especially under limited training data.

## Strengths

- **Addresses a practical and underexplored problem:** Few-shot multimodal anomaly detection is a realistic industrial scenario, and the paper identifies clear limitations of existing cross-modal alignment and memory-based methods in this setting.
- **Sound technical contributions with good motivation:** The three components (BPA, APR, MNC) each target a specific failure mode of prototype-based reconstruction in few-shot settings, and the ablation studies confirm their individual contributions.
- **Strong experimental results:** PIRN achieves substantial gains over strong baselines across multiple datasets and shots settings (e.g., +3.9 AUROC_I on MVTec-3D-AD at 5-shot, +4.0 on Eyecandies at 10-shot). The method also demonstrates favorable computational efficiency (85% fewer FLOPs than FIND).
- **Comprehensive evaluation:** The paper includes experiments on three datasets, ablation studies on each component, analysis of codebook size and decoder depth, modality ablation, and a visualization of feature displacement via BPA routing. The additional results on Real-IAD D3 show convincing localization performance.

## Weaknesses

### Major
- **Missing statistical significance / error bars:** The paper reports results from a single run without standard deviations or confidence intervals. This is particularly important in few-shot settings where the choice of training samples can introduce high variance. The results would be considerably strengthened by reporting means and variances over multiple random seeds.
- **Ablation baseline is overly weak:** The base model "w/o all modules" (AUROC_I 0.828) excludes all three proposed components but it is not clear what reconstruction mechanism is used. Comparing against a stronger baseline that uses a standard prototype codebook with softmax assignment (the most common approach) would better demonstrate the specific benefit of BPA over a natural alternative, rather than leaving the baseline underspecified.
- **Limited validation of APR robustness to anomalies:** The paper argues that anomalous tokens are diffused across prototypes in the OT assignment, thus having minimal influence on prototype updates. However, no quantitative analysis or sensitivity test is provided to verify this claim under varying anomaly severity. A controlled experiment measuring how much the prototypes drift when anomalies are present would strengthen the safety argument.

### Minor
- **Frozen encoder limits domain adaptation:** The ViT encoder is frozen with DINOv2 weights. While this is common practice, it means that the features are not adapted to the specific target domain. A discussion of this limitation and whether fine-tuning the encoder would further improve performance is missing.
- **Surface normal map generation requires 3D point clouds:** The method relies on surface normal maps derived from 3D data, which may not be available in all multimodal settings. The paper acknowledges this implicitly by focusing on the MAD benchmark, but it is a constraint worth noting explicitly.

## Nice-to-Haves
- Add error bars over multiple runs (e.g., 3-5 seeds) to demonstrate statistical reliability of the reported improvements.
- Compare against a stronger ablation baseline that uses softmax-based prototype assignment (without balanced OT) to isolate the benefit of BPA more clearly.
- Provide a quantitative analysis of how much the prototypes change when the input contains anomalies (e.g., measure prototype drift as a function of anomaly proportion) to validate the robustness claim of APR.

## Novel Insights
Beyond the paper's own contributions, a key insight is that in few-shot multimodal anomaly detection, *prototype-level* cross-modal communication is more robust than dense patch-to-patch alignment. By exchanging only high-level normal prototypes rather than per-pixel features, the model avoids overfitting to spurious cross-modal correlations that arise from limited training data. Additionally, the use of balanced optimal transport to enforce uniform prototype utilization provides a principled way to maintain codebook diversity without requiring large memory banks. 

## Suggestions
- Report results over multiple random seeds and include standard deviations.
- Clarify the architecture of the baseline in Table 2 (row 1) and consider adding a comparison with softmax-based prototype assignment.
- Add a figure or quantitative analysis showing how much the prototypes shift when anomalous patches are present, to empirically validate the safety of APR.

## Score and Decision

**Score:** 6  
**Decision:** Accept  

MY FINAL SCORE: <score>6</score>  
MY FINAL DECISION: <decision>Accept</decision>