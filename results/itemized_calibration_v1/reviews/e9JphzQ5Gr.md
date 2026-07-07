Now I have all the information needed. Let me produce the final consolidated review.

## Summary

This paper proposes CaPT (CLIP as a Prior Teacher), an asymmetric-modalities co-training framework that integrates CLIP into semi-supervised learning. CaPT jointly trains a fully fine-tuned unimodal network (UPM) and a parameter-efficiently fine-tuned multimodal CLIP model (MPM), using co-pseudo labels with entropy-based weighting to combine their predictions. A theoretical bound on pseudo-label error under a prototype-based Gaussian mixture model is presented as motivation. Empirically, CaPT achieves strong results across USB benchmarks, ImageNet, extreme low-label settings (e.g., +21.38% on CIFAR-100 with 1 label/class), and six fine-grained datasets, with modest computational overhead (~8% memory, ~11% training time over FreeMatch).

## Strengths

1. **Empirically strong in the extreme low-label regime.** On CIFAR-100 with one label per class (Table 3), CaPT achieves 82.51% vs. 61.13% (FreeMatch) and 60.49% (RegMixMatch). A 21+ point improvement on a 100-class dataset with one sample per class is genuinely striking and not incremental.

2. **Efficient integration with practical overhead.** Table 4 shows CaPT adds only ~8% memory and ~11% training time over FreeMatch while improving accuracy by ~6 points. The PEFT design (CLIP adapters + frozen encoders + feature-level Mixup) is sensibly engineered to avoid the cost of fully fine-tuning CLIP or re-encoding at high resolution.

3. **Clean ablation design.** The variants in Table 6 (CaPT-Ada, CaPT-Deb, CaPT-Uni, only UPM, only MPM, w/o feat aug., equal weights) are well-conceived and isolate the contribution of each design choice. The fact that CaPT-Uni (unidirectional) underperforms the full bidirectional version supports the claim that mutual learning matters.

4. **Broad evaluation scope.** The paper covers USB benchmarks (Table 1), ImageNet (Table 2), extreme low-label (Table 3), and six fine-grained datasets (Table 5). This breadth strengthens the case that the framework generalizes.

5. **Useful problem diagnosis.** The empirical demonstration in Figure 1 that SSL gains from unlabeled data collapse when labeled data quality/quantity is poor is a genuinely informative observation.

## Weaknesses

### Major

None.

### Minor

1. **The theoretical bound (Theorem 1.1) is overclaimed as a central contribution.** The paper advertises "theoretically establish[ing] the label dependency that constrains SSL" as contribution #1. However, Theorem 1.1 bounds pseudo-label error for a *nearest-prototype classifier* under a *prototype-based Gaussian mixture model* — a setup that does not reflect modern SSL methods (deep networks, confidence thresholds, consistency regularization). The bound contains a 2^{d/2} term that is astronomically large for realistic image dimensions (e.g., 224×224×3), rendering the bound vacuous. Moreover, the theorem neither motivates nor predicts the behavior of CaPT's specific co-pseudo-label mechanism; it formalizes the intuition that "poor labeled data leads to worse pseudo-labels," which is well-known. The paper would be stronger if it treated this as an illustrative motivation rather than a central theoretical contribution.

2. **On STL-10, CaPT's reported accuracy (unimodal network) underperforms CLIP alone, and this is not discussed.** In Table 1, on STL-10 with 4 labels/class: CaPT achieves 96.07% while Adapter-tuned CLIP achieves 96.86% and zero-shot CLIP achieves 97.18%. With 10 labels/class: CaPT 96.34% vs. Adapter-tuned CLIP 97.15%. The paper reports CaPT's final performance using the fully fine-tuned unimodal network, so this comparison is apples-to-oranges in a strict sense — CaPT is an SSL method for training the unimodal network, not a CLIP fine-tuning method. However, the fact that the co-trained unimodal network does not match CLIP alone on STL-10 — where CLIP's zero-shot performance is already near-saturated at 97.18% — deserves explicit acknowledgment and analysis. This would reveal an informative boundary condition of the method.

3. **The paper does not explicitly describe a supervised loss on labeled data in the method section.** Sections 3.1–3.3 describe the pipeline exclusively for *unlabeled* data. No equation for a supervised cross-entropy loss on labeled data appears in the method section. The paper states that UPM "follows common practices (Sohn et al., 2020)," which *implies* a supervised loss is included, but this is not stated explicitly. For completeness and reproducibility, the full training objective should be described in the main text.

4. **Missing simple CLIP+SSL hybrid baselines.** The headline improvements compare CaPT (CLIP + backbone) against methods without CLIP. The paper does include an "Adapter-tuned CLIP" row (Table 1) and ablation variants (CaPT-Ada, CaPT-Deb) that partially address this. However, simpler CLIP+SSL hybrids — e.g., using CLIP's adapter-tuned predictions to initialize FreeMatch's pseudo labels, or adding a consistency loss between CLIP's predictions and the backbone's predictions without the co-training loop — would help isolate what the co-training *framework* specifically contributes beyond "just having CLIP." Without these, it is unclear how much of the gain comes from the carefully designed co-training versus the brute-force addition of a strong pretrained model.

5. **The benefit of bidirectional co-training is modest on the main datasets.** In Table 6, CaPT-Uni (unidirectional CLIP→vision model flow) drops only 0.88% on CIFAR-100 and 1.49% on EuroSAT compared to the full bidirectional CaPT. The paper's claim that bidirectional exchange is "crucial" overstates what the evidence supports; the data more accurately show a small but consistent benefit.

6. **No standard deviations reported for several key tables.** Table 2 (ImageNet), Table 3 (extreme low-label), and Table 5 (fine-grained) report single numbers without variance estimates, while Table 1 reports means and stds from 3 runs. Consistency in reporting variance would strengthen the reliability of the claims, especially given the paper's strong claims about reducing label dependency.

7. **The confidence threshold mechanism is underspecified in the two-model setting.** Line 196 states that pseudo labels are retained only if confidence exceeds a threshold, and line 206 says the adaptive threshold from FreeMatch is used. But in a two-model system, it is unclear whose learning state determines the threshold and how the two models' potentially different confidence levels are reconciled.

### Trivial

- CaPT underperforms baselines on FGVCAircraft (Table 5). The paper relegates this to Appendix N; a brief note in the main text would be appropriate.
- The paper previews CaPT's own results in Figure 1a before describing the method, giving the reader no basis to interpret the gains at that point.

## Nice-to-Haves

- Adding a direct comparison against a simple CLIP+SSL hybrid (e.g., CLIP adapter-tuned predictions used to initialize FreeMatch's pseudo labels) would substantially strengthen the claim that the co-training framework itself drives the gains.
- A quantitative measure of representation diversity (e.g., CKA similarity, prediction disagreement rate) between the two co-trained models would strengthen the "pattern-homogeneity bottleneck" argument, which is currently supported only by qualitative attention maps (Figure 3).
- A discussion of boundary conditions where CLIP's prior is weak (specialized domains, fine-grained classes with low zero-shot performance) would characterize important limitations.

## Removed Points

These points from the input review were removed or demoted based on filtering rules:

- **"STL-10: serious unresolved discrepancy that undermines the core claim"** → Demoted to Minor #2. The comparison is between different models (UPM accuracy vs. CLIP accuracy). CaPT's contribution is improving SSL for the unimodal network, not improving CLIP. CaPT still substantially outperforms all SSL baselines on STL-10 (96.07% vs. 89.89%). The lack of discussion is worth noting, but the framing as a "serious unresolved discrepancy" is overstated given the paper's reported metric choice.
- **"Comparison is asymmetric"** → Partially retained as Minor #4. The paper does include Adapter-tuned CLIP baselines and ablation variants that address the concern, so the criticism was weakened to "missing simple CLIP+SSL hybrid baselines."
- **"Missing related work on CLIP+SSL hybrids"** → Removed per hard rules (cannot verify external sources or claim missing citations).
- **Various formatting, grammar, appendix-missing, and reproducibility nitpicks** → Removed per hard rules (parser artifacts, appendix stripped, hyperparameter disclosure not required for acceptance).
- **"Figure 1a previews results before describing method"** → Demoted to Trivial.
- **"CaPT-Uni drop is small; bidirectional claim overstated"** → Retained as Minor #5 but reframed more precisely.

## Novel Insights

The most informative observation to emerge from the review is the tension between the claimed contribution ("bidirectional asymmetric-modalities co-training enables richer information exchange") and the empirical evidence: CaPT-Uni (unidirectional flow) loses only 0.88% on CIFAR-100, suggesting the primary value of CaPT may come from CLIP acting as a one-way teacher rather than genuine mutual learning. The authors should either present stronger evidence for the bidirectional benefit or recalibrate their claims. Additionally, the STL-10 case (where CLIP's zero-shot accuracy is already near-saturated at 97.18%) hints that CaPT's advantage is largest precisely when the baseline SSL methods struggle most — i.e., when CLIP's prior is strong and the unimodal network's learning is weak.

## Suggestions

1. Add explicit description of the supervised loss on labeled data to Section 3.
2. Add a brief discussion of the STL-10 case where CaPT's unimodal network does not match CLIP alone, noting this as a boundary condition.
3. Add variance estimates to Tables 2, 3, and 5.
4. Clarify whose learning state determines the adaptive confidence threshold in the two-model system.
5. Either add simple CLIP+SSL hybrid baselines or temper the claims about the framework's novelty relative to "having CLIP."
6. Note the FGVCAircraft underperformance briefly in the main text.
7. Treat Theorem 1.1 as instructive motivation in the narrative rather than a central theoretical contribution.

## Score and Decision

**Calibration anchors**: All retrieved anchors from the corpus are listed below.

| File | Avg Score | Round | Itemized? | Comparison to CaPT |
|------|-----------|-------|-----------|-------------------|
| `25kAzqzTrz` (FixMatch theory) | 8.00 | Bracket | Yes | Stronger theory, less applied contribution. CaPT is below this. |
| `dnqPvUjyRI` (SemiReward) | 6.00 | Narrow | Yes | Comparable SSL framework paper. CaPT has more dramatic gains in extreme regimes but weaker theory. |
| `97D725GJtQ` (SemiCLIP) | 5.80 | Both | Yes | Similar CLIP+SSL topic. CaPT has stronger results and broader evaluation. |
| `ptCIlV24YZ` (Image Clustering) | 5.80 | Narrow | Yes | Uses CLIP features. CaPT has more methodological novelty. |
| `1rgMkDWfYV` (CLIP + noisy labels) | 4.50 | Bracket | Yes | Key weakness was unfair comparison concern and inferior SOTA results. CaPT addresses comparison better and has stronger results. |
| `FwkYeLovHk` (Weak-to-strong CLIP) | 3.33 | Bracket | Yes | Setting concerns, limited novelty. CaPT is clearly stronger. |

**Bracket**: 5.5–6.5 (determined by comparing against anchors in Rounds 1 and 2).

**Final placement**: CaPT sits at 6.0. The shared heavy-weight positive items with higher-scoring anchors include "strong empirical results surpassing SOTA" and "broad experimental evaluation." The missing heavy-weight positive items include "rigorous theoretical analysis" and "novel methodological contributions clearly beyond engineering." The weaknesses (weak theory, missing CLIP+SSL hybrid baselines, presentation gaps) are real but addressable and do not invalidate the core empirical contribution.

MY FINAL SCORE: <score>6.0</score>
MY FINAL DECISION: <decision>Accept</decision>