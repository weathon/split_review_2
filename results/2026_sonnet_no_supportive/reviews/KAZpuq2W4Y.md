## Summary
HOMIL proposes to extend attention-based MIL for whole-slide image classification by incorporating second-order statistics (a covariance matrix of cluster features) alongside the standard first-order attention-weighted mean. Adaptive DBSCAN clustering is used to compress ~10,000–15,000 patches per slide down to ~16–18% of that count, simultaneously improving computational efficiency and providing variable-granularity representation. The method is evaluated on CAMELYON16 and TCGA-NSCLC with nine baselines.

## Strengths
- **Clear and principled statistical framing**: The reinterpretation of ABMIL as a first-order moment estimator (Section 3.1, Eq. 2) and the natural extension to second-order statistics is well-motivated and clearly written. The connection between attention weights and a probability distribution over instances is precise.
- **Ablation confirms both components contribute (Table 3)**: On CAMELYON16, removing either clustering (CM) or second-order moments (SOM) degrades all three metrics; removing both (i.e., ABMIL) yields the lowest scores. The full model improves ACC by ~2.26% over ABMIL.
- **Efficiency story is internally consistent and strong**: Clustering reduces patch count to 16–18% of original; reported total runtimes (310s HOMIL vs. 7200s MambaMIL and 10800s HMIL on CAMELYON16) are compelling and include the clustering overhead. HOMIL is also faster than ABMIL (455s).

## Weaknesses

### Fatal
None.

### Major
- **Mislabeled "attention-weighted covariance" vs. actual implementation (Section 4.3.3)**: The paper repeatedly calls its second-order representation an "attention-weighted covariance matrix" (abstract, Section 4.1 item 3, Section 4.3.3 step 2 header). However, the actual formula (Section 4.3.3 step 2) is: **C = Σ_k g̃_k g̃_k^T**, where attention weights *a_k* do not appear in the sum. Only the centering vector **v^(1)** uses attention weights; the outer-product accumulation is uniform. This is a sample covariance with a non-standard mean — not an attention-weighted covariance. The distinction matters because the stated motivation is that *important clusters contribute more to the covariance*; the implementation does not enforce this. This gap between description and formula is neither acknowledged nor ablated anywhere in the paper.

- **Marginal TCGA-NSCLC gains without significance testing (Table 2)**: On TCGA-NSCLC (the harder, larger dataset), HOMIL's improvement over the next-best method HMIL is +0.35% ACC (SEs: 2.47% vs. 1.45%) and +0.10% F1 (SEs: 2.62% vs. 1.47%). These differences are well within reported standard error overlap. No statistical significance test is reported anywhere. The abstract claims the method "significantly improves the state-of-the-art," but this claim is unsubstantiated on the harder dataset.

### Minor
- **DBSCAN adaptivity claim unverified (abstract, Section 4.2)**: The central motivation for choosing DBSCAN — that it "adaptively forms large clusters for abundant normal tissues and small clusters for rare pathological regions" — is asserted repeatedly but never empirically validated. No cluster-size distributions per tissue type, no visualization, no comparison with a fixed-granularity alternative (e.g., k-means) are provided. The efficiency gains from clustering are real and documented; the diagnostic-selectivity claim is not.

- **Covariance compression is ad-hoc with no alternatives tested (Section 4.3.3)**: Compressing a 512×512 covariance matrix to a 512-d vector via row-wise 1D convolution (T=4 kernels, m=64) followed by double max-pooling is an extreme reduction with no stated rationale for why this preserves the pairwise correlation structure that motivated computing the covariance in the first place. No ablation compares against simpler alternatives (diagonal extraction, learned linear projection, PCA on the covariance).

- **Ablation not replicated on TCGA-NSCLC (Section 5.4)**: Table 3 ablation is conducted only on CAMELYON16. On TCGA-NSCLC — where HOMIL's margins are smallest and most questionable — no ablation is reported, so the contribution of SOM on that dataset remains unknown.

### Trivial
None.

## Nice-to-Haves
- Visualize covariance structure differences between slide classes (e.g., PCA of cluster covariance matrices for cancerous vs. non-cancerous slides) to directly demonstrate that the second-order statistics carry class-discriminative information.
- Either implement the attention-weighted outer product C = Σ_k a_k g̃_k g̃_k^T and ablate it against the current uniform version, or explicitly state that only the centering uses attention weights and justify the design choice.
- Add statistical significance tests (or at minimum a discussion of SE overlaps) in Tables 1–2.
- Replicate ablation on TCGA-NSCLC.
- Compare against simpler second-order baselines (bilinear pooling, global covariance pooling from computer vision) to establish whether DBSCAN + 1D convolution compression is genuinely necessary.

## Removed Points
*These points are flagged to be removed; treat them with caution.*

- **Computational time accounting asymmetry**: The reviewer notes DBSCAN's O(n²) worst-case complexity. Removed because actual measured runtimes are reported in the paper and speak for themselves.
- **Conflation of intra-patch vs. across-patch covariance (Section 3.2)**: The framing in Section 3.2 is slightly imprecise, but the actual computation throughout Section 4 is clearly cross-patch statistics. Not a substantive error.

## Novel Insights
The "attention-weighted covariance" naming issue surfaces a genuinely interesting design decision that the paper leaves unresolved: attention-weighting the centering step (as done) biases the deviations toward attention-highlighted clusters, but uniform accumulation means rare low-attention clusters contribute equally to spread. Whether attention-proportional outer-product accumulation (C = Σ_k a_k g̃_k g̃_k^T) is empirically better or worse is an open question the paper is positioned to answer but does not. For imbalanced slides with sparse pathological foci — the paper's core use case — this choice could meaningfully affect what the covariance encodes.

## Suggestions
- Clarify Section 4.3.3: either add a_k weights to the outer-product accumulation and ablate both variants, or explicitly state the accumulation is unweighted with a justification.
- Soften "significantly improves the state-of-the-art" language in abstract/conclusion to match the actual evidence, particularly on TCGA-NSCLC.
- Add a TCGA-NSCLC ablation table matching Table 3.

---

## Score and Decision

**Anchor papers reviewed:**

| Path | Avg Score | Round | Comparison |
|------|-----------|-------|-----------|
| 0yVP49SDg0 (Mamba-HMIL) | 3.25 | R1 | WSI MIL paper, rejected; weaker motivation and more components than HOMIL, but similar class |
| MOCEoNsjEx (Pg-GAT) | 3.00 | R1 | Graph WSI MIL, rejected; marginal results with weakly-motivated components |
| jHdsZCOouv (SHAP-CAT) | 3.40 | R1 | Multimodal WSI, rejected; also incremental but similar evidence quality |
| lo9HMoGNwQ (SMIL) | 4.50 | R2 | Sequential MIL for medical imaging, rejected; sound but incremental, similar profile |
| 6xrDPHhwD3 (MFC) | 6.00 | R1 | WSI MIL with multiple novel modules, accepted; more comprehensive though also has inconsistencies |
| AZW3qlCGTe | 5.67 | R1 | Instance classification with set labels; relevant to MIL space |
| trj2Jq8riA | 5.67 | R1 | WSI survival analysis with VL; strong conceptual contribution |
| oW7T3p5wE1 (SEC) | 5.00 | R2 | Token clustering paper, rejected; comparable efficiency + clustering claims |
| SPu6k4OZkj | 5.25 | R2 | Novel clustering algorithm, rejected; uneven reviews |

**Round 1 bracket**: 3.5–5.5 — HOMIL's idea is sound and better motivated than the rejected WSI MIL papers (3.0–3.4), but the verified technical inconsistency in the central contribution (attention-weighted covariance) and the lack of support for the headline TCGA-NSCLC claims pull it below borderline accept.

**Round 2 narrowing**: Comparing to the 4.5 (SMIL, rejected) and 6.0 (MFC, accepted) anchors more carefully: SMIL was rejected for being incremental with sound-but-limited experiments — HOMIL has a similar profile with the additional problem of a formula/description inconsistency. MFC was accepted despite inconsistencies between abstract and body because its technical components are more developed and its experimental support broader. HOMIL's single-dataset ablation, unverified DBSCAN claims, and marginal TCGA-NSCLC gains align it closer to the 4–5 range. The "attention-weighted covariance" mismatch is the clearest differentiator — it weakens the central claimed design choice.

**Final score**: **4.0** (borderline reject)

MY FINAL SCORE: <score>4.0</score>
MY FINAL DECISION: <decision>Reject</decision>