---
job_id: 799bc561-abb8-4ead-9b50-4d15e5235677
agent_id: ICLR_main_2026_2
status: COMPLETED
filename: Rd0yhdfueL.pdf
paper: Bhav-Net: Knowledge Transfer for Cross-Lingual Antonym vs Synonym Distinction via Dual-Space Graph Transformers
main_score_norm: 0.4
desk_reject: false
---
# Desk Rejection Assessment:
## Paper Length
Pass ✅.

## Topic Compatibility
Pass ✅. The paper is clearly within ICLR scope, touching multilingual representation learning, transfer learning, and graph-based learning for lexical semantic relation classification.

## Minimum Quality
Pass ✅. The paper contains the expected scientific sections and a complete methodological/experimental narrative, although there are substantial issues in rigor, specification, and evaluation that weaken the work and will be reflected in the full review rather than treated as desk-reject defects.

## Prompt Injection and Hidden Manipulation Detection
Pass ✅. I did not find any hidden prompts, suspicious reviewer-directed instructions, or other manipulative content in the provided paper text.

# Expected Review Outcome:
## Summary
This paper studies multilingual antonym-vs-synonym distinction across eight languages and proposes Bhav-Net, a dual-space architecture that maps word pairs into separate synonym and antonym spaces, then performs graph-based reasoning over pair nodes using TransformerConv layers. The method combines language-specific BERT encoders, dual projection heads, graph construction over batches, and a margin-based auxiliary loss, with experiments on English and seven additional languages built from WordNet/ConceptNet.

## Strengths
The paper addresses a real and nontrivial problem. Antonymy and synonymy are notoriously difficult to separate using standard distributional similarity alone, and extending this to a multilingual setting is worthwhile.

The idea of using two relation-specific spaces is intuitively sensible for this task. Even though the exact formulation raises issues that I discuss below, the high-level inductive bias is aligned with the semantic asymmetry between synonymy and antonymy.

The paper is easy to follow at a high level. The method decomposition into encoder, dual projections, graph reasoning, and auxiliary loss is straightforward, and **Figure 1** does help the reader understand the intended training pipeline from per-language encoding to fused graph features and final prediction. In particular, the figure is useful for seeing that the graph stage is not applied to token graphs or lexical knowledge graphs, but to a graph whose nodes are word pairs. That design choice is important for interpreting what the graph module can and cannot actually contribute.

The multilingual dataset statistics in **Table 1** are useful and transparent. The paper makes clear that the non-English datasets are much smaller and uneven across languages, which is important context for interpreting the reported language-wise differences.

The English numbers in **Table 2** and the language breakdown in **Table 3** suggest that a dual-encoder variant can improve over a plain BERT baseline in several languages, at least in the reported setup. The gains are not huge, but they are directionally consistent in most rows of Table 3.

## Weaknesses
1. **The central “knowledge transfer” claim is not actually substantiated by the method as written.**  
   The title, abstract, and Introduction repeatedly frame the contribution as knowledge transfer from “complex multilingual models” into “simpler graph-based architectures.” However, the actual method in Sections 3.1 to 3.4 does not describe any teacher-student distillation objective, frozen-teacher supervision, feature matching, logit matching, or layer-wise transfer mechanism. Instead, the model simply uses language-specific BERT encoders inside the architecture itself, see Equations (1)-(2) and Algorithm 1, lines 2 and 7 on **Page 6**. This is not the same thing as transferring knowledge into a simpler student. It reads more like “using pretrained encoders as front ends,” which is standard.  
   This matters because a large part of the paper’s claimed novelty and significance rests on efficient transfer. Without a concrete transfer mechanism and without a comparison to a teacher model or distillation baseline, the title/abstract framing is materially overstated.

2. **The mathematical formulation is internally inconsistent about what the antonym space is supposed to do.**  
   In Section 3.2 on **Page 4**, the text says antonyms should be “similar in an oppositional space,” and Equation (8) explicitly defines an antonym-space similarity. This suggests antonym pairs should have high similarity in the antonym space. But the actual margin loss in Equation (16b) on **Page 6** does the opposite:
   \[
   \mathcal{L}_{\text{ant}} = \max\left(0,\tanh(\langle \mathbf{a}_1^{(\ell)}, \mathbf{a}_2^{(\ell)}\rangle)-m_{\text{ant}}\right),
   \]
   with \(m_{\text{ant}}=0.2\), and the text immediately below says “for antonym pairs, similarity in antonym space should be below \(m_{\text{ant}}\).”  
   That directly contradicts the conceptual motivation in Section 3.2. Either the antonym space is meant to pull antonyms together, or it is meant to push them apart; the paper currently says both. This is not a cosmetic issue, because it affects the semantics of the representation, the interpretation of Table 3, and the plausibility of the claimed “dual-space” advantage.

3. **Several core components are underspecified to the point that the method is not reproducible from the main paper.**  
   The graph construction in Section 3.3 on **Page 5** is too vague. The paper says edges are added based on word overlap, semantic similarity above threshold \(\tau\), and transitivity constraints, but does not define:
   - how \(\tau\) is selected,
   - whether similarity for edge creation uses Equations (7)-(8), raw dot products, or something else,
   - whether the graph is recomputed every batch,
   - how transitive weighted edges are parameterized,
   - whether edge types or weights are passed into TransformerConv,
   - what happens for isolated nodes,
   - whether the graph is language-specific or mixed across languages.
   
   Likewise, Equation (11) writes
   \[
   \mathbf{X}^{(l)}=\text{Dropout}(\text{ReLU}(\text{TransformerConv}(\mathbf{X}^{(l-1)},\mathcal{E}))),
   \]
   but \(\mathbf{X}^{(0)}=\mathbf{x}_{\text{fused}}\) in Equation (10) is defined as if it were a single fused vector, while the graph layer requires a node-feature matrix. The notation conflates per-pair features with batch-level graph features.  
   This matters because the graph module is one of the main advertised contributions, yet the exact learning object is unclear.

4. **The pooling/classification design appears conceptually mismatched to the stated task.**  
   Equation (13) on **Page 5** applies global mean pooling over all nodes:
   \[
   \mathbf{x}_{\text{pool}} = \frac{1}{|V|}\sum_{i \in V}\mathbf{x}_i^{(L)}.
   \]
   Then Equation (14) predicts a single \(\hat y\) from that pooled vector. But the task is defined as binary classification over word pairs, not graph-level classification. If each node is a word pair, global mean pooling over the entire batch graph would normally yield one prediction for the whole graph or batch, not one label per pair. Algorithm 1, line 12 on **Page 6**, similarly uses one \(x_{pool}\) and one \(\hat y\). Yet Equation (15) defines BCE over \(N\) examples.  
   This is a serious formulation issue. Either the model is node-level classification, in which case global mean pooling is inappropriate for the main prediction target, or the paper is doing graph-level classification, which does not match the dataset/task. As written, the training objective and architecture do not line up.

5. **The empirical evaluation is too weak to support the strength of the claims, especially outside English.**  
   The only real baseline comparison in **Table 2** is on English. For the multilingual setting, the paper reports only Bhav-Net’s average precision/recall/F1/accuracy and then a separate **Table 3** with “Bert F1-Score” versus “Dual encoder F1-Score.” This is not enough to justify claims of “competitive results against state-of-the-art baselines” in the abstract. There are no multilingual baseline rows in Table 2, no statistical variance, and no paired significance tests.  
   The non-English claims therefore rest on an internal comparison to an underspecified BERT baseline rather than on a convincing competitive evaluation. That is a major gap because the multilingual setting is one of the main stated contributions.

6. **The reported tables leave important ambiguities and raise questions about fairness of comparison.**  
   In **Table 2**, Bhav-Net is compared against AntSynNET, ICE-NET, Distiller, and a SimCSE-based model on English POS-specific F1, but the paper does not clearly state whether those numbers are taken directly from prior work, reproduced under the same split, or reimplemented with the same encoder backbone. This matters because the proposed system uses BERT-based encoders plus graph processing, while some baselines come from different modeling eras and data assumptions.  
   Also, the “Cross-Lingual Average” columns in Table 2 provide Bhav-Net numbers only, with dashes for all baselines. That makes the layout visually suggest a broader comparison than what is actually available. The table is not wrong, but it overstates evidential density.  
   In **Table 3**, the “Bert F1-Score” versus “Dual encoder F1-Score” comparison does not isolate the graph transformer or margin loss, so it does not really validate the contribution of the full Bhav-Net architecture.

7. **The paper promises ablation variants but does not report actual ablation results.**  
   Section 4.2 on **Page 7** lists three ablation variants, “Single-Space,” “No Graph,” and “No Contrastive,” which are exactly the right experiments for this paper. But no ablation table or figure is actually presented in the results section. Later, Section 5.2 on **Page 9** states that “the graph transformer adds 2-4% absolute F1,” yet there is no supporting table in the main paper showing this.  
   This matters a lot. Without these ablations, one cannot tell whether the gains in Table 3 come from the dual-space idea, from stronger encoders, from graph construction, or from the auxiliary margin loss.

8. **The dataset creation protocol for the multilingual data is not sufficiently described, and this is especially problematic for lexical semantic relation tasks.**  
   On **Pages 6-7**, the paper says the seven multilingual datasets are built from WordNet and ConceptNet with “manual verification,” “cross-linguistic consistency” checks, and balanced sampling. But there is no description of:
   - exact extraction rules,
   - deduplication,
   - train/validation/test split strategy,
   - whether lexical forms overlap across splits,
   - whether inflectional or derivational variants appear in both train and test,
   - whether translated cognates or near-duplicates create leakage,
   - how many examples were manually checked,
   - whether annotations were done by one person or multiple annotators.
   
   For relation classification over lexical pairs, lexical memorization and split leakage are well-known concerns. If the same head or tail words recur heavily across splits, results can be inflated. The paper does not give enough information to rule that out.

9. **The cross-lingual generalization claim is only weakly tested.**  
   The paper asks, in the Introduction, how antonym-synonym modeling generalizes across languages, and Section 5.1 on **Page 9** further claims that “models trained on high-resource languages can provide meaningful initialization for low-resource languages.” But there is no explicit experimental protocol in the main paper showing zero-shot transfer, few-shot transfer, joint multilingual training, or source-to-target transfer matrices.  
   What is reported instead appears to be per-language training with language-specific encoders. That is multilingual coverage, but not strong evidence of cross-lingual transfer or generalization in the usual sense. The terminology here is too loose.

10. **The positioning relative to related work is incomplete and occasionally imprecise.**  
   Section 2 discusses prior work, but the framing “existing multilingual approaches typically treat all semantic relationships uniformly” is too broad without direct evidence. There is also a placeholder-like citation, “The work of ? demonstrated...” in Section 2.1 on **Page 2**, which suggests an unresolved gap in the literature review. More importantly, the paper does not sufficiently engage with work on semantic relation classification using pretrained language models beyond the few cited lexical-semantics papers.  
   This matters because the contribution may be more incremental than the paper acknowledges, especially if the main novelty is combining standard components, BERT encoders, MLP projections, cosine similarities, graph transformer layers, and a margin loss, in a relation-classification setting.

11. **Some claims in the discussion are stronger than the evidence supports.**  
   Section 5.2 on **Page 9** states that performance variation stems “primarily from embedding model quality rather than architectural limitations.” That is a strong causal claim. But the paper does not present controlled experiments varying only encoder quality while holding everything else fixed. Since dataset size, lexical coverage, relation quality, and split difficulty vary substantially across languages in **Table 1**, that conclusion is premature.  
   Similarly, the conclusion’s claim that the method achieves “state-of-the-art performance” is only clearly supported for the reported English benchmark table, not for the multilingual setting.

12. **The figure supports the pipeline narrative, but also exposes a mismatch between the claimed contribution and the actual algorithmic content.**  
   **Figure 1** is useful, but it also makes clear that the training loop is just standard supervised optimization of parameters \(\Theta\) with BERT encoders in the loop. There is no visible teacher-student transfer path, no teacher logits, and no distilled objective. In other words, the figure undermines the title’s “knowledge transfer” framing as much as it supports the architecture description. That is a notable disconnect between presentation and substance.

## Questions
1. The biggest issue for me is the exact semantics of the antonym space. Should antonym pairs have **high** similarity in the antonym space, as suggested in Section 3.2, or **low** similarity, as enforced by Equation (16b)? Please clarify the intended geometry and, if Equation (16b) is correct, explain why the conceptual description in Section 3.2 is not contradictory.

2. What is the precise prediction granularity of the graph module? Are you doing node-level classification for each word pair, or graph-level classification for a batch graph? Please reconcile Equations (13)-(15) and Algorithm 1 with the task definition. A corrected mathematical statement of the model would materially increase my confidence.

3. Please provide the exact multilingual dataset construction and split protocol. In particular:
   - how were train/validation/test sets created,
   - were splits made by pair or by vocabulary item,
   - how did you prevent lexical overlap leakage,
   - how much manual verification was performed,
   - and what annotation guidelines were used?

4. Can you report the missing ablations promised in Section 4.2, especially:
   - BERT only,
   - dual-space without graph,
   - graph without margin loss,
   - and single-space vs dual-space?
   A compact table would substantially strengthen the paper.

5. What exactly is the “Bert F1-Score” baseline in **Table 3**? Is it the same encoder backbone with a linear or MLP classifier over concatenated pair features, and is it trained with the same data and same splits as Bhav-Net? Without that clarification, Table 3 is hard to interpret.

6. The paper makes repeated claims about knowledge transfer and cross-lingual initialization benefits. Can you provide explicit transfer experiments, for example source-language pretraining followed by low-resource target fine-tuning, or teacher-student distillation results against a multilingual teacher? This would help align the empirical evidence with the paper’s stated contributions.

7. For the graph construction in Section 3.3, please specify the exact edge function. A formal definition such as
   \[
   A_{ij} = \mathbf{1}[\text{overlap}(i,j)] \lor \mathbf{1}[\text{sim}_{\text{syn}}(i,j)>\tau_{\text{syn}}] \lor \mathbf{1}[\text{sim}_{\text{ant}}(i,j)>\tau_{\text{ant}}],
   \]
   plus any transitivity-based reweighting, would make the method much clearer.

## Flag For Ethics Review
- No ethics review needed.

## Details Of Ethics Concerns
No major ethics concerns are apparent from the submission. The work is on lexical semantic relation classification using standard lexical resources and pretrained language models.

## Soundness Rating
2: fair. The core intuition is plausible, but the technical formulation contains important inconsistencies, and the empirical evidence does not adequately support several central claims.

## Presentation Rating
2: fair. The paper is readable at a high level, but there are substantial clarity issues in the mathematical formulation, experimental protocol, and claim-to-evidence alignment.

## Contribution Rating
2: fair. The problem is relevant, but the current paper does not convincingly establish a strong methodological or empirical advance beyond combining familiar components.

## Overall Rating
4: Marginally below the acceptance threshold. But would not mind if paper is accepted.  
The paper tackles an interesting multilingual lexical semantics problem and has a reasonable high-level modeling idea, but too many central pieces are either underspecified or internally inconsistent, and the evaluation is not strong enough to support the broader claims about knowledge transfer and cross-lingual generalization.

## Reviewer Confidence
4: confident. I am confident in the assessment, especially regarding the lexical-semantics framing, the claim-evidence mismatch, and the mathematical inconsistencies in the model description, although some implementation details are missing from the paper and could in principle resolve part of the confusion.