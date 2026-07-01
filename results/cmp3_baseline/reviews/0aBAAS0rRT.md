## Summary
The paper proposes SigMap, a multimodal foundation model for wireless localization that combines a novel cycle-adaptive masked autoencoding strategy for self-supervised pre-training on Channel State Information (CSI) with a “map-as-prompt” framework that integrates 3D geographic information via lightweight graph neural network–generated soft prompts. Extensive experiments on simulated ray-tracing datasets (DeepMIMO and WAIR-D) demonstrate strong improvements over several baselines in single-BS and multi-BS localization, as well as promising few-shot generalization to unseen environments while updating only a small fraction of model parameters.

## Strengths
- The problem is well-motivated – accurate cross-scenario wireless localization under NLoS conditions remains an important and open challenge for 5G/6G, and the paper clearly identifies two key gaps (inadequate handling of signal periodicity and superficial geographic integration).
- Cycle-adaptive masking is a thoughtful adaptation of masked autoencoding to periodic signals. The idea of dynamically disrupting periodic shortcuts to force learning of global representations is novel and well-justified for CSI data.
- The map-as-prompt mechanism is technically sound: it uses a GNN to encode 3D building meshes and BS positions into soft prompts, allowing parameter-efficient fine-tuning without updating the backbone. This is a practical contribution for deployment.
- The experimental evaluation is comprehensive, covering single-BS, multi-BS, ablation studies on masking and map modalities, and generalization to two completely unseen ray-tracing scenarios. The results consistently show large margins over baselines (e.g., 34.4% MAE improvement over LWLM in single-BS).
- The paper provides a clear analysis of parameter efficiency (only ~0.7% of parameters updated during fine-tuning) and training time, which supports practical deployability.

## Weaknesses
### Major
1. **Misleading claim of “zero-shot” generalization.** The abstract states “exhibiting strong zero-shot generalization in unseen environments,” yet the generalization experiments (Section 4.5) fine-tune downstream task heads on 100 target samples per scenario. This is few-shot, not zero-shot. The distinction is significant – claiming zero-shot when the model receives any labeled data from the target domain overstates the capability and must be corrected.
2. **Evaluation only on simulated ray-tracing data.** Both the pre-training data (DeepMIMO O1_3p5) and the generalization datasets (DeepMIMO O2, WAIR-D) are generated via ray-tracing simulators. No experiments on real-world measured CSI are presented. While simulation is a reasonable starting point, a foundation model intended for practical deployment should demonstrate at least some validation on real channel measurements. The paper’s claims about “cross-scenario” and “practical” impact are weakened without this.

### Minor
1. **Lack of statistical uncertainty in main results.** The paper reports averages over 5 runs but does not provide standard deviations, confidence intervals, or significance tests. Given the reported gains (e.g., MAE differences of a few tens of centimeters), uncertainty quantification would substantially increase confidence.
2. **Cycle-adaptive masking details are insufficiently specified.** The key algorithmic step – computing the periodicity shift \(d_{\text{final}}\) from “row-wise cross-correlation” – is described only at a high level. The main text does not explain how dominant periodicities are detected or how \(w\) (mask width) is chosen, making the method difficult to reproduce without the appendix.
3. **Inconsistency in reported parameter-efficiency percentage.** Section 4.5 claims “updating only 0.4% of parameters,” while Table 5 shows 0.085M / 11.730M ≈ 0.72%. The numbers should be consistent.
4. **Multi-BS fusion head design may scale poorly.** Equation (10) uses separate MLP heads per base station, which could increase parameter count when many BSs are present. While still a small fraction overall, this design choice is not discussed.

### Trivial
- The radar chart (Figure 5) label “oss_scenario” is likely a typo for “loss scenario.”

## Nice-to-Haves
- Validation on a real-world measured CSI dataset (e.g., from an indoor testbed or a city-scale measurement campaign) would significantly strengthen the practical relevance.
- An analysis of what the learned prompts actually encode – e.g., which building vertices or BS locations receive high attention – could improve interpretability.
- Comparison to more recent wireless foundation models (e.g., WirelessGPT) or to a simple LLM-based baseline would help contextualize the approach relative to the LLM-based line of work discussed in the introduction.

## Novel Insights
None beyond the paper’s own contributions.

## Suggestions
- Replace all instances of “zero-shot” with “few-shot” or “low-shot” to accurately reflect the experimental setup. If zero-shot results exist (no fine-tuning on target data at all), present them separately.
- Add standard deviations or error bars to Tables 1–4 and the generalization table.
- Provide a more detailed explanation of the periodicity detection step in the main text (or state that it is fully covered in the appendix).
- Consider adding a small real-world measurement experiment or clearly discuss the limitations of simulated data in the conclusion.
- Unify the parameter-efficiency percentage (0.7% rather than 0.4%) and check for other numeric inconsistencies.

## Score and Decision
The paper presents a solid, well-structured contribution with a clever masking strategy and a practical prompt-based fine-tuning approach. The experimental improvements over baselines are substantial and consistent. However, the two identified major weaknesses – the mischaracterization of zero-shot generalization and the restriction to simulated data – temper the overall impact. With corrections to the claims and ideally some real-world validation, the paper would be a strong addition to the ICLR community.

MY FINAL SCORE: 6.0<score>6.0</score>
MY FINAL DECISION: Accept<decision>Accept</decision>