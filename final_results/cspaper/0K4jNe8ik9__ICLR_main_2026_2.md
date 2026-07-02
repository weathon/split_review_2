---
job_id: abc66be4-fd89-41d2-bca2-6280ccd90a00
agent_id: ICLR_main_2026_2
status: COMPLETED
filename: 0K4jNe8ik9.pdf
paper: DGNet: Self-Supervised Delta2Gamma Multi-Band EEG Representation Learning for Dementia Classification
main_score_norm: 0.4
desk_reject: false
---
# Desk Rejection Assessment:
## Paper Length
Pass ✅.

## Topic Compatibility
Pass ✅. The paper is clearly within ICLR scope, focusing on self-supervised representation learning for EEG and a healthcare application.

## Minimum Quality
Pass ✅. The submission contains the necessary components, including abstract, introduction, method, experiments, results, and conclusion. While I found substantial issues in novelty, clarity, mathematical specification, and experimental rigor, they do not rise to the level of an automatic desk rejection.

## Prompt Injection and Hidden Manipulation Detection
Pass ✅. I did not detect hidden prompts, manipulative instructions, or other obvious attempts to influence automated reviewing within the provided paper content.

# Expected Review Outcome:
## Summary
This paper proposes DGNet, a self-supervised EEG representation learning framework for dementia classification based on a multi-band SimCLR-style setup. The method decomposes EEG into five canonical frequency bands, processes each band with an independent CNN encoder and projection head, and trains the model with an adaptive temperature contrastive objective before evaluating the learned representation on AD vs CN classification with LOSO cross-validation. The paper reports strong performance on a public dementia EEG dataset and includes comparisons against a range of EEG baselines and several ablations.

## Strengths
The paper tackles an important application area. EEG-based dementia screening is clinically meaningful, and the focus on learning with limited labels is well motivated for this setting.

The central inductive bias, separating EEG into canonical bands and learning band-specific representations, is intuitively aligned with established neurophysiology. Even if the ingredients are familiar, the paper makes a reasonable attempt to tailor a generic contrastive-learning framework to the structure of EEG.

The empirical gains reported in **Table 3** are large relative to the authors’ own ablations. In particular, the jump from the scratch model (63.35% accuracy) to the full adaptive 5-band-head model (92.90%), and the gap between the single-head and adaptive multi-band variants, suggest that the chosen representation design may indeed matter on this dataset, assuming the evaluation is fully sound.

**Figure 1** is helpful at a high level. It makes the two-stage pipeline easy to follow, namely SSL pretraining on unlabeled EEG followed by downstream classification. For readers less familiar with EEG SSL, this figure gives a quick mental model of the intended training flow.

The augmentation section is more concrete than in many applied SSL papers. **Figure 4** gives examples of Gaussian noise, amplitude scaling, masking, and channel dropout, which helps the reader understand what invariances the method is trying to impose.

## Weaknesses
1. **The main novelty is limited and the paper does not position itself sharply enough against prior SSL-for-EEG work.**  
   The proposed recipe is, in essence, bandpass decomposition plus per-band CNN encoders plus SimCLR-style projection heads plus adaptive temperature, with the adaptive temperature mechanism itself attributed to prior work in **Section 2.3** and the conclusion. The paper repeatedly describes the method as highly innovative, but the actual technical difference from standard EEG pipelines is modest. The problem is not that simple ideas are invalid, it is that the paper does not convincingly isolate what is scientifically new beyond combining known ingredients in a task-specific way. This matters because ICLR expects either a clear algorithmic advance, a deeper representation-learning insight, or unusually strong evidence that a practical combination reveals something generalizable. Right now, the paper mostly demonstrates a domain-specific composition of standard components.

2. **There is a serious inconsistency between the architectural description and the actual frequency-band processing pipeline.**  
   On **Page 4, Section 2.1**, the paper first states that the input signal is split into five bands “using parallel 1-dimensional depthwise convolution,” but immediately after that it says “First, the signal is decomposed into five canonical frequency bands using bandpass filters.” These are not the same thing. If the bands are produced by fixed preprocessing filters, the frequency extractor is not a learnable depthwise-convolution band separator. If the bands are produced by learned depthwise convolutions, then the canonical band interpretation is weaker and the filter design needs to be specified. **Figure 2** visually suggests a learnable frequency-band extractor, while the text also claims bandpass filtering. This ambiguity affects reproducibility and scientific interpretation, because fixed physiologically defined bands and learned per-channel temporal filters imply different inductive biases, different parameterizations, and different claims about what the model is learning.

3. **The mathematical formulation in Section 2.3 is underspecified and, as written, not internally consistent with NT-Xent.**  
   **Equation (1)** defines an adaptive loss using only the positive similarity term and the hardest negative via a max operator, plus regularization on temperatures. This is quite different from the softmax-based contrastive objective used in SimCLR. Then **Equation (2)** is presented as “NT-Xent,” but its denominator includes only negative samples, whereas the standard InfoNCE / NT-Xent form includes the positive in the normalized partition or, depending on notation, all paired examples except the anchor itself. Moreover, the paper says the implementation computes independent losses for each band and combines them through a weighted average, yet the earlier sentence says “The final loss is defined as \( \ell = \sum_{b=1}^B \ell_b \),” and **Equation (1)** already sums over \(b\) inside \( \ell_i \). The indexing of \( \ell \), \( \ell_i \), and \( \ell_b \) is therefore confusing and possibly duplicated. Also, the paper never specifies how the learnable temperatures are parameterized to remain positive, how they are initialized, whether they are per-instance or per-head parameters in practice, or how gradients are stabilized. These are not cosmetic details; they are core to the claimed contribution.

4. **The downstream evaluation protocol is described inconsistently, which makes it hard to trust the reported numbers.**  
   In **Figure 1(b)** and the caption, the paper says linear evaluation is performed with a frozen encoder, but the same caption also says “the entire model is intentionally retrained using labeled data,” which sounds like fine-tuning. On **Page 5**, the “Downstream Task” section states that two approaches were considered: frozen encoder and updating all parameters, and then incorrectly says the second approach is “known as linear evaluation,” which is not standard terminology. In **Section 3** on **Page 7**, the paper says the linear evaluation stage used LOSO with the pretrained encoder weights kept frozen. So which results in **Tables 1-3** correspond to frozen linear evaluation, and were any full fine-tuning results also run? This confusion matters because the reported gains could differ substantially between linear probing and end-to-end fine-tuning, and the paper’s claims about representation quality depend on that distinction.

5. **The experimental protocol leaves open a substantial risk of leakage or over-optimistic model selection.**  
   The paper states in **Section 3** that LOSO cross-validation is used and that “early stopping” is applied if no performance improvement is observed for 10 epochs. However, it is never explained what validation set is used inside each LOSO fold for early stopping and hyperparameter/model selection. If the held-out subject is used for early stopping, that would contaminate the test protocol. If a validation split is carved from the training subjects, that should be stated explicitly. Similarly, the SSL pretraining stage is said to use unlabeled EEG data, but it is not made clear whether pretraining is performed separately within each LOSO fold using only training-subject unlabeled data, or once using all subjects including the held-out subject. In a subject-generalization setting, this is crucial. Without a clean fold-specific pretraining and validation description, the reported **92.90%** in **Tables 1 and 2** is difficult to interpret.

6. **The comparison to baselines in Table 1 is not convincingly fair.**  
   **Table 1** compares the proposed model to a heterogeneous collection of architectures, many originally designed for motor imagery, epilepsy, ERP, or generic EEG tasks. The appendix **Table 4** confirms this mismatch in application domains. That alone is not fatal, but the paper provides too little detail on how each baseline was adapted to this dataset, how input formatting was standardized, whether the same preprocessing and segmentation were used, and whether hyperparameters were tuned comparably. The statement that “for the SSL models, fine-tuning was performed when pretrained weights were available” is not enough to establish fairness. On a small 88-subject dataset, baseline sensitivity to training choices can be large. The extremely low numbers for several strong EEG architectures in **Table 1** such as EEGNet, EEGConformer, BIOT, and S-JEPA raise the question of whether the implementations and tuning were competitive. This matters because the paper’s headline claim of superiority rests heavily on this table.

7. **The paper does not report uncertainty estimates for the main result despite using LOSO and a small subject count.**  
   In **Table 2**, most prior methods are listed as single numbers, one includes mean ± std, and the proposed method is again a single number. With only 88 participants, subject-level variability matters. The paper should report fold-wise mean and dispersion, or at least subject-level confidence intervals, for accuracy and F1. Otherwise a performance difference such as 92.90 vs 91.25 may not be statistically meaningful. This is especially important because the paper repeatedly claims clear superiority.

8. **The ablations are helpful but still not sufficient to establish the mechanism of improvement.**  
   **Table 3** compares adaptive 5-band heads, scratch training, single-head, no augmentation, “Multi-head (5 heads),” constant temperature, and no regularization. However, the definitions are muddled. It is not obvious what the difference is between “Adaptive 5 band heads” and “Multi-head (5 heads)” other than adaptive temperatures, and the terminology overlaps confusingly with the earlier architecture description. More importantly, there is no ablation on the band decomposition itself, such as fixed bandpass preprocessing with a shared encoder, learned band extractor versus fixed filters, varying the number of bands, or removing individual bands to assess which frequencies actually drive the dementia signal. Since the entire motivation is neurophysiological band specificity, the absence of per-band analysis is a missed opportunity.

9. **Some figures are more decorative than evidential, and a few even amplify confusion.**  
   **Figure 3** is labeled “Spectrogram visualization of embeddings from the encoder,” but the paper does not explain how an embedding becomes a spectrogram, what exactly the axes correspond to after encoding, or what scientific takeaway the reader should draw from the image. It currently functions more as a visual placeholder than evidence. Similarly, **Figure 6** in the supplement shows mean ± std bars for several metrics across “5 band heads”, “5 heads”, and “1 head”, but the main paper does not integrate this analysis or explain the experimental repetition protocol that produced those standard deviations. By contrast, **Figure 4** is useful because it concretely shows augmentations, whereas **Figure 3** and **Figure 6** need stronger interpretation.

10. **The writing overstates conclusions and sometimes weakens precision.**  
   Examples include phrases such as “perfectly aligns,” “clearly demonstrate the superiority,” and “highly effective” in the absence of careful caveats about the small dataset and the potential evaluation ambiguities noted above. There are also places where terminology is used imprecisely, for example calling full end-to-end updating “linear evaluation,” or describing parameter counts in **Table 4** as “essential hyperparameters.” These issues do not make the paper unreadable, but they reduce confidence in the precision of the technical presentation.

11. **The task setup and scope are narrower than the paper’s framing suggests.**  
   The dataset described in **Section 3.1** contains AD, FTD, and CN participants, but the reported task in **Tables 1-3** is AD vs CN only. The paper does not explain why FTD is excluded from the main task, nor whether unlabeled FTD data is used during pretraining. This matters because a method presented as a dementia representation learner would be more convincing if evaluated in a multiclass dementia setting, or at least if the inclusion/exclusion logic were clearly justified. Otherwise the framing appears broader than the evidence.

## Questions
1. Please clarify the exact band-generation pipeline. Are the five frequency bands obtained by fixed signal-processing bandpass filters before the network, or by learned depthwise 1D convolutions inside the model, or both? If both are used, what is the role of each, and what are the exact tensor shapes after each stage? A revised description aligned with **Figure 2** would materially improve confidence.

2. Please provide a precise training objective that matches the implementation. In particular:
   - What is the exact loss minimized over a batch?
   - Is **Equation (1)** the actual training loss, or a conceptual summary?
   - How are the adaptive temperatures parameterized, constrained to be positive, and initialized?
   - Is the final loss a sum over heads, a mean over heads, or a weighted average over heads?
   - Why is the denominator in **Equation (2)** written without the positive term?

3. Please clarify the evaluation protocol under LOSO. For each fold:
   - Is SSL pretraining performed using only training-subject unlabeled data?
   - What validation set is used for early stopping and model selection?
   - Are the reported **Tables 1-3** from frozen linear evaluation only, or from fine-tuning, or from both?
   A clean fold diagram would help.

4. Can you report variability across LOSO folds, for example mean ± std or confidence intervals for the main metrics in **Tables 2 and 3**? This would help determine whether the gains over prior work are robust.

5. Can you add stronger ablations directly tied to the main scientific claim, for example:
   - shared encoder across bands vs independent encoders,
   - fixed bandpass preprocessing vs learned filters,
   - removing one band at a time,
   - different numbers of bands,
   - adaptive temperature per band vs one global adaptive temperature?
   These results would substantially strengthen the paper.

6. Please explain the baseline training details behind **Table 1** more carefully. Were all baselines trained with the same segmentation, preprocessing, optimizer family, and comparable tuning budget? For the SSL baselines, what exactly was pretrained and what exactly was fine-tuned?

7. Why is the FTD group excluded from the main classification task despite being present in **Section 3.1**? Was FTD used in pretraining, and if so, how should readers interpret the transfer setting?

## Flag For Ethics Review
- No ethics review needed.

## Details Of Ethics Concerns
No major ethics concerns are evident from the paper itself. The work uses a clinical EEG dataset for dementia-related classification, but the manuscript does not raise immediate issues requiring specialized ethics escalation beyond standard concerns already common to medical ML.

## Soundness Rating
2: fair. The idea is plausible and some experiments are relevant, but the core mathematical specification, evaluation protocol, and fairness of baseline comparisons are not documented with enough precision to fully support the central claims.

## Presentation Rating
2: fair. The paper is readable at a high level and some figures help, but there are important inconsistencies in terminology, equations, and the description of the training/evaluation pipeline.

## Contribution Rating
2: fair. The paper addresses a meaningful problem and reports strong empirical results, but the methodological advance over existing EEG SSL practice appears limited and the evidence is not yet strong enough for a clearer positive assessment.

## Overall Rating
4: Marginally below the acceptance threshold. But would not mind if paper is accepted. The application is important and the empirical results are potentially interesting, but there are too many unresolved issues around novelty, objective specification, protocol clarity, and baseline fairness for me to support acceptance in the current form.

## Reviewer Confidence
4: confident. I am confident in the assessment, though not absolutely certain. The paper is in an area I know well, and I checked the method and experimental claims carefully, but some ambiguities in the manuscript prevent complete verification.