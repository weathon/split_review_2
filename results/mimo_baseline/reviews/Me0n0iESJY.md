## Summary

This paper introduces OptMerge, a model merging benchmark and method for Multimodal Large Language Models (MLLMs). The benchmark covers five capability domains (VQA, Geometry, Chart, OCR, Grounding) with both LoRA and full fine-tuning across InternVL2.5 and Qwen2-VL architectures, and extends to modality merging (vision, audio, video). The proposed method improves upon WUDI Merging by applying low-rank approximation to denoise task vectors and stabilizing the merged vector optimization through better initialization and optimizer choices.

## Strengths

- **Well-designed benchmark filling a clear gap**: The paper provides the first standardized benchmark for MLLM model merging with fine-grained capability categorization, covering 5 task domains with ≥100K training samples each, two model families, and both LoRA and full fine-tuning settings. This is a genuinely valuable community resource.

- **Practical method with principled motivation**: OptMerge addresses real failure modes of prior optimization-based merging (task vector noise, norm explosion during optimization). The ablation study (Table 4) cleanly isolates each component's contribution: SGD + initialization yields a 4.43% improvement for LoRA merging, and low-rank approximation provides additional gains. The norm trajectory visualization (Figure 4) convincingly demonstrates the stability benefit.

- **Theoretical contribution**: Theorem 3.1 provides the first formal bound connecting fine-tuning hyperparameters (learning rate η, iterations T) to merging quality through cross-task interference (O(δηT)) and curvature (O(η²T²)) terms, offering a principled explanation for the empirical observation that excessive fine-tuning degrades merging.

- **Comprehensive evaluation scope**: The paper evaluates 10 merging methods, tests on real HuggingFace community models (Table 6), examines 3 model scales (1B, 7B, 32B), and includes modality merging experiments. The practical demonstration with community-released checkpoints strengthens the paper's relevance.

- **Computational efficiency**: Table 7 shows OptMerge achieves 0.22h/2.62GB vs. 25.38h/240GB for InternVL2.5, making it practically deployable.

- **The finding that merged models can match or exceed mixture training** (Tables 2-3) is a significant and practically useful result.

## Weaknesses

### Fatal

None.

### Major

- **Marginal gains on InternVL2.5 full fine-tuning**: In Table 2, OptMerge achieves 57.44 avg vs. WUDI's 57.00 (0.44% improvement) and actually falls below mixture training (57.66). The headline "2.48% average improvement" conflates gains across different settings rather than representing consistent improvement on any single benchmark. The method's advantage is most clear for LoRA merging (Qwen2-VL) where it achieves 63.30 vs. 63.65 for WUDI — wait, actually WUDI achieves 63.65 there, so OptMerge is *lower*. Looking more carefully, for InternVL2.5 OptMerge is +0.44% over WUDI, while for Qwen2-VL it is −0.35%. The 2.48% figure appears to be an average of specific component ablations rather than end-to-end improvements. This inconsistency weakens the main claims.

- **Iso-C baseline is broken for LoRA merging**: Iso-C achieves only 26.69 on Qwen2-VL (Table 3) compared to 54.78 on InternVL2.5, likely because applying isotropic merging to already low-rank LoRA vectors is inappropriate. This inflated gap makes the average comparison misleading. The paper acknowledges this but still reports averages that include this broken baseline.

- **Modality merging evaluation is limited and OptMerge isn't the best**: Table 5 shows only 2 datasets (MUSIC-AVQA and AVQA). TSV Merging achieves 67.34 vs. OptMerge's 67.00, meaning the proposed method is not actually the best for this setting. For a paper that claims modality merging as a key contribution (Figure 1, title), this limited and sub-optimal result is a concern.

- **Significant rank size sensitivity**: Table 8 shows Grounding performance dropping from 73.96 (10%) to 56.19 (50%), and overall average declining from 57.43 (20%) to 52.98 (50%). The method's claim of robustness is restricted to 10-30%, and even within that range there is meaningful variation. The choice of k = rank/n_tasks (used without justification) and the sensitivity to this choice warrant more discussion.

### Minor

- **No variance/error bars**: All results are reported as single runs. Given the optimization procedure (300 iterations of Adam/SGD) and hyperparameter search over λ, understanding result stability is important.

- **Limited λ search**: Only 6 values in [0.1, 1.5] are searched. A finer grid or per-task λ might change relative rankings of methods.

- **Modality complementarity analysis is shallow**: Table 5 shows merged modalities beat individuals, but pairwise analysis (vision+audio, vision+video, audio+video) would better characterize complementarity.

- **Table 9 (32B) is a partial evaluation**: Only 5 methods are compared and individual expert models sometimes outperform OptMerge on specific tasks (e.g., Individual Geometry on MATH-Vision: 80.34 vs. 80.01).

### Trivial

Minor table header inconsistencies (e.g., "CharQVA" in Table 6).

## Nice-to-Haves

- Per-task breakdown showing which capabilities benefit most vs. suffer most from merging
- Pairwise modality merge analysis to isolate where complementarity arises
- Automatic rank selection to reduce hyperparameter sensitivity
- Discussion of failure cases where merging fails catastrophically

## Novel Insights

The theoretical analysis in Theorem 3.1 is genuinely novel — connecting fine-tuning dynamics (learning rate × iterations) to merging quality through formal bounds on cross-task interference and curvature terms provides the community with actionable guidance for selecting models suitable for merging. The practical observation that task vectors require denoising (via SVD truncation) before optimization, and that the merged vector must be initialized with the mean of task vectors to prevent norm explosion (Figure 3-4), are valuable design insights for optimization-based merging methods.

## Suggestions

- Provide error bars or at least report variance across multiple runs
- Expand modality merging evaluation to more datasets and report pairwise modality merges
- Justify the rank selection heuristic (k = rank/n_tasks) more rigorously or propose automatic selection
- Disaggregate the "2.48% improvement" claim to show per-setting gains transparently

## Score and Decision

The benchmark contribution is the paper's strongest asset — it provides a well-structured, publicly available evaluation framework that the community genuinely needs. The method (OptMerge) is technically sound with clear ablation support, but its improvements are inconsistent across settings (sometimes better, sometimes worse than WUDI Merging). The modality merging claim is underdeveloped and the method isn't actually the best there. The theoretical analysis adds novelty. Overall, this is a solid benchmark paper with a competent but not transformative method, placing it at the borderline.

MY FINAL SCORE: <score>6</score>
MY FINAL DECISION: Accept