---
job_id: bc5f796b-be0d-42fb-b902-6ac46a2deb8f
agent_id: ICLR_main_2026_2
status: COMPLETED
filename: m7gNW26Zih.pdf
paper: LLM-Augmented Soft-Label Distillation and Cluster-Guided Alignment for Language-Based Audio Retrieval
main_score_norm: 0.4
desk_reject: false
---
# Desk Rejection Assessment:
## Paper Length
Pass ✅.

## Topic Compatibility
Pass ✅. The paper is clearly within ICLR scope: cross-modal representation learning, metric learning, and retrieval for audio-language data using dual encoders, distillation, and auxiliary supervision.

## Minimum Quality
Pass ✅. The paper includes an abstract, introduction, method, experiments, quantitative results, and conclusion, and it is written in English. While there are important concerns about novelty, experimental depth, and some methodological clarity, these do not rise to the level of an immediate desk rejection based on the provided text alone.

## Prompt Injection and Hidden Manipulation Detection
Pass ✅. I did not detect hidden prompts, manipulative instructions to automated reviewers, or other obvious integrity issues in the provided paper text and figure content.

# Expected Review Outcome:
## Summary
This paper studies language-based audio retrieval using a dual-encoder framework on CLOTHO, augmented with three ingredients: soft-label distillation from an ensemble of pretrained retrieval teachers, LLM-based caption augmentation including back-translation and mixed-audio caption generation, and a cluster-guided auxiliary classification objective on pseudo-topic labels. The empirical study compares several audio backbones and system variants, and reports that distillation provides the strongest gains, while augmentation and cluster guidance offer smaller and more mixed improvements.

## Strengths
The paper addresses a real issue in language-based audio retrieval, namely that audio-caption relevance is often not strictly binary. The distillation formulation in Section 2.2 is well aligned with that motivation, and Equations (5)-(9) make the intended teacher-softened supervision reasonably easy to follow.

The empirical gains from distillation are non-trivial. In **Table 2**, moving from SID 1 to SID 2 improves PaSST from 42.08 to 46.62 mAP@16, EAT from 40.41 to 45.35, and BEATs from 38.12 to 43.89. This consistency across three different audio backbones is the strongest piece of evidence in the paper, and it supports the claim that soft targets are useful for ambiguous audio-text correspondence.

The paper evaluates multiple audio encoders rather than presenting a single-backbone story. That breadth is valuable because it shows that the main conclusions are not tied to one architecture.

**Figure 1** is helpful at a high level. It conveys the intended training pipeline, namely initial contrastive supervision, distillation from a pretrained system, and a later re-finetuning stage with cluster-guided auxiliary classification. In particular, the figure makes the two additional losses, \(L_{\text{dist}}\) and \(L_{\text{cls}}^{a}, L_{\text{cls}}^{c}\), visually explicit, which improves accessibility relative to the text alone.

The paper is also reasonably transparent about the practical outcome of cluster supervision. The abstract and results section do not oversell it, and the numbers in **Table 2** indeed show mixed gains, which is a more honest presentation than claiming universal improvement.

## Weaknesses
1. **The paper’s main contribution is too incremental and insufficiently differentiated from existing retrieval-system engineering.**  
   The three main components are all adaptations of already familiar ideas: soft-label distillation from prior retrieval systems, LLM-based caption augmentation, and pseudo-label clustering with auxiliary classification. The paper does not convincingly articulate what is fundamentally new beyond combining these ingredients in one system. This matters because for ICLR, a systems paper built from standard parts needs either unusually strong empirical evidence, a sharper conceptual framing, or a clearer methodological insight. Here, the paper mainly reads as a competition-style recipe. The introduction on **Page 1** claims contributions such as “soft-label distillation,” “LLM-based augmentation pipeline,” and “cluster-guided auxiliary heads,” but none is framed against prior methods in enough depth to clarify what technical gap is actually being closed.

2. **Positioning against prior work is weak, especially around non-binary relevance and LLM augmentation.**  
   The paper motivates soft labels as a way to address non-binary audio-caption correspondence, but it does not sufficiently situate itself relative to prior work that directly studies graded relevance or caption-similarity-based soft targets for text-based audio retrieval. That omission matters because the paper’s core narrative is not just “distillation helps,” but “distillation helps because relevance is non-binary.” If that conceptual claim is central, the related literature around graded relevance should be discussed explicitly and compared more carefully. Similarly, the augmentation story would be stronger if it were positioned against earlier GPT-based caption augmentation for audio retrieval, rather than presented as if this were largely new in spirit.

3. **The experimental evidence does not isolate which proposed components are actually responsible for improvement.**  
   The strongest gains come from distillation alone, as shown in **Table 2**. By contrast, augmentation and clustering produce very small, inconsistent, and often negligible changes. For example, with PaSST, SID 2 gives 46.62 mAP@16, SID 3 gives 46.41, SID 4 gives 46.39, and SID 5 gives 46.50. For EAT, SID 3 improves slightly over SID 2, but SID 4 and SID 5 do not. For BEATs, the pattern is similarly mixed. This matters because the title and abstract emphasize all three ingredients, but the actual table suggests that one ingredient carries the paper and the other two are at best weak auxiliary tweaks. The authors should not bury this under ensemble results. A more honest reading of **Table 2** is that distillation is useful, while the case for augmentation and cluster-guided alignment remains under-supported.

4. **The cluster-guided classification module is underspecified and empirically unconvincing.**  
   Section 2.3 describes clustering captions and training classification heads on both text and audio encoders, but key details are missing or vague. The paper does not report the number of clusters obtained, the fraction of outliers before reassignment, cluster size distribution, or any quality measure of the pseudo-labels. These are not cosmetic details. If the auxiliary objective depends entirely on noisy pseudo-topics, then the usefulness of Equation (10) depends on whether those topics are stable and semantically meaningful. Without such evidence, the reader cannot judge whether the weak gains in **Table 2** come from an inherently weak idea or from poor pseudo-label quality. The claim in the abstract that “ablations indicate consistent improvements under high correspondence ambiguity” is also not supported by any dedicated table or figure in the main paper.

5. **The LLM augmentation pipeline is not reproducible enough from the main paper.**  
   Section 2.4 says the authors use GPT-4o for back-translation and “intelligently merge” captions for mixed audio, but gives no prompt templates, no language sampling policy, no filtering criteria, no examples of failed generations, and no validation that generated mixed captions remain faithful to the mixed audio. Even the simpler augmentation in Section 3.4, “one-word random deletion or synonym replacement with 0.8 probability,” is not properly specified. Is 0.8 applied per caption, per token, or per augmentation attempt? How are synonyms selected, and how is semantic drift controlled? This matters because augmentation quality is central to the paper’s claims, yet the description is far too coarse to reproduce or evaluate scientifically.

6. **There is a methodological concern around teacher construction and potential circularity that is not addressed clearly enough.**  
   In Section 2.2 and Section 3.4, the teachers are an ensemble of pretrained models, and the student backbones seem to overlap with those model families. The paper does not clearly specify whether each student is distilled from a teacher ensemble including a model of the same architecture trained on overlapping data, whether teachers are frozen before CLOTHO finetuning, and whether the teacher ensemble includes models later used in the final evaluation ensemble. None of this is necessarily invalid, but it should be spelled out, because otherwise it is hard to assess whether the gains reflect true transfer of complementary soft structure or just iterative self-training with closely related models.

7. **The mathematical formulation is serviceable but not fully careful, and some notation/definition choices are confusing.**  
   In Section 2.1, Equations (2) and (3) define \(q_a(a_i \mid c_j)\) and \(q_c(c_j \mid a_i)\), but the notation is backwards relative to usual retrieval convention. For Equation (2), the denominator sums over audio index \(k\), so this is better interpreted as a distribution over audios conditioned on caption \(c_j\). For Equation (3), the denominator sums over captions \(l\), so it is a distribution over captions conditioned on audio \(a_i\). This is not fatal, but the notation should be made explicit because later cross-entropy expressions in Equations (4) and (8) rely on these distributions. More importantly, the paper says \(p_a\) and \(p_c\) “assign a probability of 1 to the positive pair and 0 to negative pairs,” but with five captions per audio in CLOTHO the notion of the “positive pair” is not as trivial as in one-to-one settings, and the batch construction is not described well enough to tell how multiple positives are handled. If the batch contains different captions of the same audio, the effective target distribution is not simply one-hot. That ambiguity directly affects the meaning of the supervised term \(L_{\text{sup}}\).

8. **Equation (10) introduces auxiliary classification losses without defining them precisely enough.**  
   The paper never formally states whether \(L_{\text{cls}}^a\) and \(L_{\text{cls}}^c\) are standard cross-entropy losses, whether class imbalance is handled, and whether pseudo-label confidence is used to weight examples. Since HDBSCAN/BERTopic topic assignments are usually highly imbalanced and include uncertain points, treating all pseudo-labels equally may be problematic. This is an important omission because the success or failure of the auxiliary objective hinges on the pseudo-label noise model.

9. **The paper over-relies on a single benchmark and does not evaluate generalization claims strongly enough.**  
   The entire main evaluation is on the CLOTHO development test split, with the final evaluation number reported only briefly. There is no second benchmark, no cross-dataset transfer test, and no robustness analysis beyond the narrative claim of “high correspondence ambiguity.” This matters because the paper repeatedly argues that the method improves robustness and generalization. Those are broader claims than “works a bit better on CLOTHO dev test,” and the current evidence is too narrow to support them.

10. **The ensemble results are practically stronger than the single-model story, but scientifically weaker.**  
    The paper highlights the ensemble reaching 48.83 mAP@16 in **Table 2**, with the weighting details in **Table 3**. However, the ensemble construction is essentially validation-set grid search over many system/model combinations. This may be fine for a challenge submission, but it does not add much scientific understanding. **Table 3** lists hand-tuned or grid-searched coefficients, yet there is no analysis of why these weights make sense, which systems are complementary, or how sensitive performance is to the weighting strategy. As a result, the ensemble section reads more like scoreboard optimization than a research contribution.

11. **The paper lacks key diagnostic analyses that would substantiate its central hypotheses.**  
    For distillation, I would expect at least one analysis of teacher-target entropy or temperature sensitivity beyond fixing \(\tau=0.05\). For clustering, I would expect topic examples or a visualization of cluster purity. For augmentation, I would expect qualitative examples and failure cases. **Figure 1** is only a pipeline diagram; there are no qualitative figures showing the nature of augmented captions, mixed-audio captions, or cluster assignments. This is a missed opportunity because the claimed benefits are semantic in nature, and semantic claims benefit from qualitative inspection.

12. **Presentation is adequate but still leaves important ambiguities in the training setup.**  
    Section 3.4 states that initial pretraining is conducted on “a mix of CLOTHO development training split, AudioCaps, and WavCaps datasets,” while subsequent finetuning and re-finetuning are only on CLOTHO. However, the sampling strategy across datasets is not specified, nor is the total number of training pairs after augmentation. Since the batch sizes differ substantially by backbone, optimization comparability is also murky. These omissions make it difficult to interpret whether gains arise from the proposed objectives or from hidden differences in data exposure and optimization dynamics.

## Questions
1. The central empirical result seems to be distillation, not augmentation or clustering. Can the authors provide a sharper decomposition of gains, ideally with variance across runs, to show whether the SID 2 to SID 3/4/5 differences in **Table 2** are statistically meaningful or mostly noise?

2. Please clarify the construction of positives in Equation (4). In CLOTHO, each audio has multiple captions. Within a batch, if multiple captions correspond to the same audio, is \(p_c\) or \(p_a\) still one-hot? If not, please define the exact target distribution used for \(L_{\text{sup}}\).

3. For Equations (6)-(8), are the teacher models frozen after pretraining, after CLOTHO finetuning, or at some other stage? Does each student receive soft labels from an ensemble that includes a teacher with the same backbone family? A precise protocol would help assess whether the method is distillation, self-training, or a hybrid.

4. For the cluster-guided objective in Equation (10), what is the number of clusters for the “Finetuned” and “BERTopic/e5-large-v2” settings, and what fraction of samples were initially assigned as outliers by HDBSCAN? Please also report cluster-size imbalance. Without this, it is difficult to interpret the weak/mixed results.

5. The paper claims consistent improvements “under high correspondence ambiguity,” but I could not find a dedicated main-paper table supporting that statement. Can the authors provide an explicit ambiguity-stratified analysis in the main paper, for example partitioning queries by teacher-target entropy or by semantic overlap with nearest non-matching captions?

6. For the augmentation pipeline, please provide concrete prompt templates and a few qualitative examples of back-translated and mixed captions. How often does the LLM mix produce captions that mention events not perceptually grounded in the mixed audio?

7. How sensitive are results to the temperature \(\tau\) in Equations (2), (3), (6), and (7), and to the loss weight \(\lambda_2=0.05\) in Equation (10)? Right now these values are fixed without justification.

8. For **Table 3**, can the authors give a more informative analysis of ensemble complementarity? For instance, what is the pairwise disagreement or error correlation among systems/backbones that justifies the specific weighting patterns?

## Flag For Ethics Review
- Yes, Legal compliance (e.g., GDPR, copyright, terms of use)  
- Yes, Responsible research practice (e.g., human subjects, data release)

## Details Of Ethics Concerns
The main issue is limited transparency around the use of proprietary LLMs in the augmentation pipeline described in **Section 2.4** and acknowledged again in the limitations on **Page 7**. Because GPT-4o is used to generate training captions, the paper should clarify terms-of-use compatibility, whether any dataset text was transmitted to an external service, and whether redistribution of generated captions is permissible. This is not an accusation of wrongdoing, but it should be disclosed more carefully for reproducibility and compliance reasons.

A second concern is responsible reporting of synthetic data generation. The paper creates 50,000 mixed-audio caption pairs using GPT-4o, but does not discuss quality control, hallucination screening, or whether these synthetic captions will be released. Given that these synthetic labels influence retrieval behavior, some discussion of filtering and auditing would be appropriate.

## Soundness Rating
2: fair. The main empirical claim, that distillation helps, is supported, but several methodological details are under-specified and the evidence for the full three-part contribution is not strong enough.

## Presentation Rating
2: fair. The paper is readable and the high-level flow is understandable, especially with **Figure 1**, but important details of losses, pseudo-label construction, augmentation, and experimental protocol are missing or unclear.

## Contribution Rating
2: fair. The paper tackles a relevant problem and distillation seems useful, but the overall contribution is too incremental and the added components beyond distillation are not convincingly validated.

## Overall Rating
4: Marginally below the acceptance threshold. But would not mind if paper is accepted.  
My hesitation is not that the paper is unsound in a catastrophic sense, but that the main-paper evidence supports only part of the claimed contribution. Distillation looks useful, yet augmentation and cluster-guided alignment are weakly justified, the novelty is limited, and the paper reads more like a practical system assembly than a sufficiently sharp ICLR contribution.

## Reviewer Confidence
4: confident. I am confident in this assessment, though not absolutely certain. The paper is in an area I know reasonably well, and I checked the main equations, tables, and claims carefully.