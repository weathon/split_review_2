## Summary

This paper presents a dual-encoder language-based audio retrieval system enhanced with three techniques: (1) soft-label distillation from an ensemble of pretrained retrieval models to capture non-binary audio-text correspondences, (2) LLM-driven caption augmentation via back-translation and caption mixing, and (3) cluster-guided auxiliary classification to improve alignment between audio and text representations. On the CLOTHO dataset, the authors show that distillation and LLM augmentation consistently improve retrieval performance across backbones, while cluster-guided classification yields mixed and sometimes negative gains. The best weighted ensemble achieves mAP@16 of 48.83 on the development test split.

## Strengths

- **Clear and well-motivated problem framing**: The paper correctly identifies that standard contrastive learning makes a binary correspondence assumption that is violated in realistic audio-caption datasets, and proposes targeted remedies (distillation, augmentation, clustering) that are each intuitively motivated.
- **Systematic ablation with multiple backbones**: The use of three different audio encoders (PaSST, EAT, BEATs) and five System IDs allows readers to assess the contribution of each component across different architectures, increasing the reliability of the conclusions.
- **Strong baseline improvements from distillation and LLM augmentation**: Comparing SID1 (baseline) to SID2 (+distillation) and SID3 (+augmentation), the gains are substantial and consistent across all three audio models (e.g., PaSST mAP@16 from 42.08 to 46.62 to 46.41), demonstrating clear value in these techniques.
- **Competitive final performance**: The weighted ensemble achieves state-of-the-art-level results on CLOTHO, and the ablation methodology makes it easy to attribute which components drive the gains.

## Weaknesses

### Fatal
None.

### Major

1. **The cluster-guided classification component shows marginal and inconsistent gains, undermining its claimed role as a core contribution.** When comparing SID3 (distillation + augmentation) to SID4 (adds cluster labels from finetuned model) and SID5 (adds cluster labels from BERTopic), the results are mixed at best. For PaSST, mAP@16 drops from 46.41 (SID3) to 46.39 (SID4) and rises only infinitesimally to 46.50 (SID5). For EAT, performance *decreases* from 46.05 to 45.34 in both cluster variants. The paper’s abstract claims “consistent improvements under high correspondence ambiguity,” but no experiment defines or measures high-ambiguity subsets, and the main results table shows no reliable improvement. The cluster component is presented as a key innovation, yet it either hurts or gives negligible benefits.

2. **The method for assigning cluster labels to audio samples is ambiguous and may be invalid.** Each audio recording in CLOTHO has five captions, which could belong to different clusters. The paper states that the audio encoder’s classification head “predicts the cluster label of the corresponding caption” but does not specify how a single cluster label is chosen for an audio sample that has multiple captions (e.g., majority vote, random selection, or using a derived audio-cluster mapping). This ambiguity makes the auxiliary classification loss ill-defined and the results uninterpretable. A clearer description or justification is essential.

3. **No statistical significance or variance estimates are reported.** The differences between SID3, SID4, and SID5 are often within fractions of a percentage point (e.g., 46.41 vs 46.39 vs 46.50 for PaSST). Without error bars or multiple runs, it is impossible to know whether these differences are meaningful or just noise. Given that the conclusion about cluster guidance hinges on these small numbers, the lack of variance reporting is a serious omission.

4. **Limited evaluation scope.** All main results are on the CLOTHO development test split only. The system is pretrained on AudioCaps and WavCaps, but no evaluation is performed on the AudioCaps test set or any other dataset to demonstrate generalizability. A single-domain evaluation weakens the significance of the claims, especially because the cluster-based method is dataset-specific (clustering is performed on CLOTHO captions).

5. **Reproducibility limitations from proprietary components.** The LLM augmentation uses GPT-4o, a closed model whose outputs may change over time and are not available offline. The paper acknowledges this as a limitation, but it remains a concern for a method that relies on augmentation as a core building block. Similarly, the exact checkpoints and configurations of the pretrained ensemble models used for distillation are not fully specified (e.g., which epoch of BEATs.iter3.plus_AS2M, which PaSST variant), making it difficult to reproduce the teacher ensemble.

### Minor

- The ensemble weighting procedure in Table 3 is described only briefly and appears to use a two-stage grid search on the validation set. The weights for E1–E4 vary considerably, but no justification is given for why these specific weights are optimal.
- The paper mentions “one-word random deletion or synonym replacement with 0.8 probability” as augmentation during finetuning, but this is not described in the Method section and is not listed as a component in the SID configurations.

### Trivial

- Figure 1’s caption is garbled in the parsed text, but this is clearly a parsing artifact and does not affect evaluation.

## Nice-to-Haves

- Report results with confidence intervals or standard deviations over multiple random seeds to assess the reliability of the cluster guidance results.
- Provide an evaluation on the AudioCaps test set to demonstrate generalization beyond CLOTHO.
- Clarify how cluster labels are assigned to audio samples with multiple captions, and consider alternative multi-label approaches.
- Release the exact checkpoints and code for the teacher ensemble and the augmentation pipeline to improve reproducibility.

## Novel Insights

None beyond the paper’s own contributions. The paper demonstrates that well-known techniques—soft-label distillation, LLM-based back-translation and caption mixing, and clustering-based auxiliary tasks—can be combined to improve audio retrieval performance; however, the cluster component does not provide reliable gains and the overall engineering contribution is largely an application of prior ideas (especially the DCASE 2024 Task 8 method) to the same dataset. The most informative result is the clear benefit of distillation and augmentation, which is consistent with prior work.

## Suggestions

- **Strengthen the evidence for cluster guidance**: Either provide a dedicated experiment on subsets with high correspondence ambiguity (e.g., by measuring caption-caption similarity or audio-audio similarity) showing consistent improvement, or honestly downgrade the claimed contribution of clustering to a minor ablation component.
- **Add statistical rigor**: Run each experiment at least 3 times and report mean ± std. This is especially important for evaluating the small differences between SID3–SID5.
- **Clarify the cluster-label assignment procedure**: Explain how each audio sample (which has multiple captions) is assigned a single cluster label for the auxiliary classification loss. If no such procedure exists, the method as described is incomplete.
- **Evaluate on a held-out dataset**: Include results on AudioCaps test set to show that the improvements are not overfitted to CLOTHO’s specific caption distribution.
- **Reduce reliance on proprietary LLMs**: Consider providing an alternative augmentation pipeline using an open-source LLM (e.g., Llama) to ensure long-term reproducibility.

## Score and Decision

MY FINAL SCORE: 4.5
MY FINAL DECISION: Reject