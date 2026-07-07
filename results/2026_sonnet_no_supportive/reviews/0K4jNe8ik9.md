Based on my paper reading and calibration, I have sufficient information to write the final review.

**Round 1 bracket established:** 2–3, based on comparison with similar EEG classification papers (UniEEG avg 2.0, FSL-MIC avg 2.2, Seizure cross-patient classification avg 3.0). The unresolved data leakage concern and incremental contribution align this paper with the reject range.

---

## Summary
DGNet proposes a multi-head SimCLR-based self-supervised learning framework for EEG Alzheimer's disease (AD) classification. The model decomposes EEG into five canonical frequency bands (δ, θ, α, β, γ), assigns independent CNN encoders and projection heads per band, and uses an adaptive NT-Xent loss with per-band learnable temperatures. Evaluated on a public 88-subject dataset using LOSO cross-validation against prior dementia EEG methods, it reports 92.90% accuracy, claimed as state-of-the-art.

## Strengths
- **Neurophysiologically grounded architecture**: The five-band decomposition directly targets the known AD spectral signature (delta/theta elevation, alpha/beta/gamma reduction) documented in cited literature (Section 1, Moretti et al. 2004, Benwell et al. 2020, Traikapi & Konstantinou 2021), providing stronger inductive-bias motivation than most EEG papers offer.
- **Ablation study demonstrates clear component contributions (Table 3)**: The progression from training-from-scratch (63.35%) through SSL (79.55%) to adaptive temperature (86.53%) and full model (92.90%) demonstrates that each major component contributes positively, with the total gap large enough to be meaningful.
- **LOSO cross-validation is the appropriate evaluation framework**: The paper correctly employs Leave-One-Subject-Out evaluation and explains why it is stricter than k-fold for inter-subject generalization in EEG (Section 3.4).

## Weaknesses

### Fatal
- **Pre-training data leakage with LOSO (unaddressed)**: Section 3 explicitly states that SSL pre-training uses "unlabeled EEG data" from the same 88-subject pool, while LOSO is applied only during the linear evaluation stage. The paper never specifies whether pre-training is re-run per fold with the test subject excluded, or whether a single shared encoder is trained once on all 88 subjects. If the encoder was pre-trained on all subjects (including each fold's held-out subject), the LOSO independence assumption is violated: the encoder has already seen the test subject's EEG, making the 92.90% accuracy an in-distribution measurement rather than true generalization. Running per-fold pre-training 88× would be expensive and is not mentioned. This omission is the most critical flaw: without resolution, the headline accuracy and the "state-of-the-art" claim in Table 2 cannot be accepted at face value.

### Major
- **No variance for the primary comparison**: DGNet reports 92.90% as a single point estimate with no standard deviation across LOSO folds. The closest competitor in Table 2, BI-MCGNN, reports 91.25±0.38. The ~1.65 pp gap may not be statistically significant; the "state-of-the-art" claim is unsupported without overlapping confidence intervals.
- **Segment-level vs. subject-level accuracy unspecified**: Section 3.3 describes 30-second segmentation of ~13.5-minute recordings (~27 segments/subject), but the paper never states whether the reported 92.90% is segment-level or subject-level (e.g., majority-vote). This ambiguity makes comparisons in Table 2 unreliable, since prior works may aggregate predictions at the subject level.

### Minor
- **Table 1 framing is misleading**: The 12 baselines in Table 1 (ATCNet, BIOT, Deep4Net, EEGNet, FBCNet, Labram, S-JEPA, etc.) are designed for motor imagery, seizure detection, or general BCI—not resting-state dementia EEG. Their low performance (39–74%) reflects domain mismatch. Section 4.1 frames this as the primary performance evidence ("significantly outperforming all comparison models"), when Table 2 (domain-matched prior work) is the only clinically meaningful comparison. The framing overstates the significance of Table 1.
- **Ablation table structure is ambiguous (Table 3)**: The "Multi-head (5 heads)" row achieves 79.55%, yet "constant temperature (τ=0.1)" achieves 86.53%—a ~7 pp difference that is not explained. If constant temperature is simply the full multi-head model without adaptive temperature, these two rows should differ by only one factor. Section 4.3 does not clarify what other components are active or absent in each row, making individual attribution ambiguous.
- **FTD class excluded without justification**: The dataset contains three groups (AD=36, FTD=23, CN=29), but only binary AD vs. CN is evaluated. No explanation is provided for excluding FTD, which shares overlapping spectral signatures with AD. A 3-class experiment would be more clinically realistic and the exclusion weakens the clinical impact claim.

### Trivial
- **Numeric discrepancy between text and figure**: Section 2.1 states "the first hidden layer contains 512 nodes," while Figure 1 caption reads "612 and 256 units." One of these is incorrect.

## Nice-to-Haves
- Report mean ± standard deviation across LOSO folds for all metrics in Tables 1 and 2 to enable proper statistical comparison.
- Explicitly state whether 92.90% is segment-level or subject-level accuracy.
- Rebuild Table 3 as strict single-factor ablations from the full model (one component removed at a time, all others intact) to enable clean attribution.
- Address or at minimum discuss the FTD group—even as an out-of-distribution test.
- Clarify how the temperature range [0.05, 0.5] is enforced (clipping, sigmoid scaling, etc.) for reproducibility.

## Removed Points
*These points are flagged to be removed; treat them with caution.*

- **Strength: "addresses an important problem"** — generic, not grounded in specific paper evidence; removed.
- **Table 1 baselines as "unfair comparison"**: The harsh critic frames this as primarily a fairness issue. The real concern is the misleading framing in Section 4.1, not comparison unfairness per se (these baselines are disadvantaged, not the author's method), so this is retained only as a framing/presentation concern in Minor.
- **Temperature range enforcement**: Demoted below trivial as a minor reproducibility detail; the paper does report the range values.
- **Abstract's "multi-head approaches" scope caveat**: Noted but not a structural weakness; appropriately hedged by the authors.

## Novel Insights
The per-band adaptive temperature mechanism is a domain-tailored extension of SimCLR that explicitly accounts for the heterogeneous learning difficulty across EEG frequency bands—a biologically motivated design choice that goes beyond standard contrastive learning. If the data leakage concern is resolved and the performance holds under clean LOSO evaluation, this would constitute concrete evidence that neurophysiologically motivated inductive biases (frequency-band separation) can meaningfully improve SSL representations for disease EEG classification.

## Suggestions
1. **Explicitly document pre-training protocol w.r.t. LOSO**: State in Section 3 whether SSL pre-training is performed once globally or re-run per fold with the test subject excluded. If global, re-run with proper exclusion and report corrected metrics.
2. **Report mean ± std across folds**: Add standard deviations to all metrics in Tables 1 and 2 to support statistical claims.
3. **Clarify evaluation granularity**: Specify segment-level vs. subject-level accuracy in Section 4 (and report both if possible).
4. **Fix the 512/612 node discrepancy** between Section 2.1 and Figure 1.
5. **Restructure ablation**: Present Table 3 as strict single-factor ablations from the full model.

---

## Score and Decision

**Anchor papers retrieved:**

| Path | Avg Score | Round | Comparison |
|------|-----------|-------|------------|
| TkbjqexD8w (EEG seizure cross-patient) | 3.00 | R1 | Similar EEG classification with cross-patient evaluation, rejected; paper under review has similar scope but additional data leakage concern |
| 6uReXuDWrw (UniEEG) | 2.00 | R1/R2 | EEG pretraining with broader dataset; rejected; paper under review is narrower scope but has targeted dementia motivation |
| PcE0yAGAGW (FSL-MIC EEG) | 2.20 | R1/R2 | EEG few-shot classification, small dataset; rejected |
| g3PuaFh5vV (Neural Decoding source space) | 2.50 | R1 | EEG cross-subject decoding; rejected |
| p30YulvDbj (Single-channel EEG MDD) | 2.00 | R2 | EEG medical classification; rejected |
| 04RGjODVj3 (Resting-EEG → motor imagery) | 3.00 | R2 | EEG LOSO cross-subject; rejected |
| ul6EYKM1Kv (EEG-saliency contrastive) | 4.50 | R1 | EEG+contrastive learning but richer contribution |
| YKfJFTiRz8 (EEG-DisGCMAE) | 5.00 | R1 | More substantial pretraining contribution over multiple datasets |
| dhLIno8FmH (EEG image decoding) | 6.75 | R1 | Strong self-supervised EEG paper; substantially more rigorous evaluation |
| IAFStwZPNu (Speech decoding SSL) | 5.67 | R1 | Larger scale, stronger methodological rigor |

**Round 1 bracket:** 2–3. The paper's unresolved data leakage issue, incremental architecture (SimCLR + frequency decomposition on a 88-subject dataset), and absence of variance reporting align it with papers in the 2–3 reject range. It is more motivated than the score-2 papers (which often lack even a clear contribution) but does not reach score-4 borderline territory due to the potentially fatal methodological gap.

**Narrowing:** The paper is above the score-2 band (it has clear neurophysiological motivation, ablation study, and a coherent architecture), but the data leakage concern, if confirmed, directly invalidates the headline result. The paper sits at **3.0** — a clear reject, principally due to the unresolved pre-training/LOSO interaction, insufficient statistical reporting for the primary claim, and ambiguous evaluation level.

MY FINAL SCORE: <score>3</score>
MY FINAL DECISION: <decision>Reject</decision>