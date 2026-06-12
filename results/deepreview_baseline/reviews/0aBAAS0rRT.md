## Summary

This paper proposes SigMap, a multimodal foundation model for wireless localization that combines a cycle-adaptive masked autoencoding pretraining strategy with a map-conditioned prompt tuning mechanism. The model is pretrained self-supervisedly on CSI data and then adapted by injecting geographic information (3D building meshes) as soft prompts via a GNN, enabling parameter-efficient fine-tuning. Experiments on DeepMIMO and WAIR-D benchmarks report strong localization accuracy in single-BS and multi-BS settings and improved cross-scenario generalization.

## Strengths

- **Clear and well-motivated problem framing.** The paper identifies two genuine challenges in existing wireless localization methods: learning shortcuts caused by periodic CSI structures and the shallow integration of geographic information. These are practical obstacles in deploying learned models across diverse environments.
- **Effective architectural design.** The cycle-adaptive masking strategy is a thoughtful way to force the model to learn global signal representations rather than exploiting local periodic patterns. The geographic prompt tuning via GNN is a sensible and parameter-efficient way to inject environmental constraints.
- **Strong empirical performance.** On the chosen benchmarks, SigMap achieves substantial improvements over the baselines included (OMP, CNN, SWiT, LWLM), especially in NLoS scenarios and under multi-BS collaboration. The ablation studies isolate the contributions of the map prompt and the adaptive masking.
- **Practical efficiency.** Only 0.7% of parameters are updated during fine-tuning, and the total fine-tuning time is 30 minutes, which is appealing for deployment.
- **Good generalization results.** The model transfers reasonably to unseen ray-tracing scenarios (DeepMIMO O2, WAIR-D) with minimal fine-tuning, demonstrating the potential of the prompt-based adaptation.

## Weaknesses

### Fatal

- **Misleading claim of zero-shot generalization.** The abstract states “strong zero-shot generalization in unseen environments,” yet the experimental setup (Section 4.5) fine-tunes the task head on target data (≈100 samples per scenario). This is few-shot, not zero-shot. The difference is critical because adapting the output head is not a trivial operation and requires labeled data. This overstatement invalidates the advertised property of the model.

### Major

- **Missing critical baselines that undermine the claimed contributions.** The paper does not ablate the self-supervised pretraining itself. Without a comparison to a *randomly initialized backbone (no pretraining)* that still uses the same map prompt and fine-tuning, it is impossible to attribute the gains to the cycle-adaptive masking or to the SSL pretraining stage. The observed improvements could stem almost entirely from the map prompt and task-specific heads, rendering the self-supervised component unnecessary.
- **Inadequate comparison with state-of-the-art SSL-based localization methods.** The related work lists CrowdBERT and signal-guided MAE as relevant SSL approaches but does not include them in the experiments. The paper criticizes such methods but provides no evidence that SigMap outperforms them. Given that the core claim is advancing SSL-based localization, this omission is a serious gap.
- **Insufficient algorithmic detail for reproducibility.** The cycle-adaptive masking procedure (Equation 6 and surrounding text) lacks a concrete description of how `d_final` (the periodicity shift) is computed from cross-correlation. The exact steps for generating the mask pattern, the role of the threshold, and whether the detection is performed per-sample or per-batch are not specified. This makes the core technical contribution unreproducible without guesswork.
- **Single dataset for main results.** All primary localization tables (Tables 1, 2, 3) are derived from DeepMIMO O1_3p5 only. The generalization experiments use O2 and WAIR-D, but the main conclusions rest on a single simulated urban scenario. A stronger evaluation would include multiple datasets (e.g., indoor, suburban, different frequency bands) to support the claim of state-of-the-art performance.

### Minor

- **Overselling the “foundation model” label.** The model is pretrained on a single simulated scenario (DeepMIMO O1_3p5). Foundation models in vision, language, and even wireless (e.g., LWLM) are typically pretrained on large, diverse corpora. Calling this a foundation model overstates the breadth of its pretraining.
- **Inconsistencies in naming (SigMap vs SIGMAP) and missing explanation of the “NLoS-aware attention” mechanism** (Equation 11) that appears only in the experimental section without being part of the methodology description.
- **The radar chart (Figure 5) uses metrics not defined in the paper** (e.g., “oss_scenario”, “AoA”, “ToA”), making it hard to interpret.

### Trivial

- Minor formatting issues (repeated figure captions) – ignored per review guidelines.

## Nice-to-Haves

- Evaluate the model on real-world CSI measurements to validate simulation-to-reality transfer.
- Provide an ablation where the SSL pretraining is replaced with a randomly initialized backbone (same architecture) to quantify the benefit of the self-supervised phase.
- Release code and pretrained weights to facilitate reproducibility and future comparisons.

## Novel Insights

None beyond the paper’s own contributions.

## Suggestions

1. **Correct the “zero-shot” claim.** Rename the generalization experiment to “few-shot adaptation” or “prompt-based fine-tuning” and state the number of labeled samples used explicitly in the abstract and conclusion.
2. **Add a no-pretraining baseline.** Compare SigMap (with map prompt) against a version where the backbone is randomly initialized and fine-tuned with the same data. This will demonstrate whether SSL pretraining adds value beyond the map prompt.
3. **Include comparisons with CrowdBERT, signal-guided MAE, or other SSL localization methods** to substantiate the claim of advancing SSL-based localization.
4. **Provide full algorithmic details of the cycle-adaptive masking** (cross-correlation computation, periodicity detection, mask generation) in the main text or appendix so that the method is reproducible.
5. **Diversify the evaluation** by adding at least one additional dataset (e.g., an indoor dataset or a different DeepMIMO scenario) to the main results table.

## Score and Decision

The paper has well-motivated ideas and shows promising results on the benchmarks tested. However, the fatal misrepresentation of zero-shot performance and the major gaps in experimental validation (missing no-pretraining baseline, lack of comparison with key SSL methods) significantly undermine the reliability of the claimed contributions. The core self-supervised component is not convincingly shown to be necessary or beneficial beyond the map prompt. These issues weigh heavily against acceptance.

MY FINAL SCORE: <score>3</score>
MY FINAL DECISION: <decision>Reject</decision>