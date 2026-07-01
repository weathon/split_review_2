Now I've read the full paper. Let me verify a few more specific points before drafting.Now I have thoroughly read the paper. Let me draft the review.Now let me run calibration Round 1 to bracket the score.Let me read a few key anchors to calibrate the score range.Now I have good calibration anchors. Let me form my initial bracket.

**Round 1 Bracket Assessment:**

Comparing DGNet to the anchors:
- It's clearly above strong-reject territory (score < 1.5) — it's a real paper with a real method.
- It's comparable to TkbjqexD8w (3.0, EEG seizure classification with limited novelty, single dataset) and 6uReXuDWrw (2.0, EEG pretraining with poor writing and limited novelty). DGNet has a clearer method but has a likely data leakage issue.
- It's clearly below YKfJFTiRz8 (5.0, EEG graph contrastive) which had much more technical depth.
- It's far below the accepted papers dhLIno8FmH (6.75) and NPNUHgHF2w (6.75) which had thorough analysis and multiple datasets.

**Initial bracket: 2.5 – 4.0**

Let me do a narrowing pass to pin down the final score.Now I have sufficient calibration data. Let me write the final review.

## Summary
DGNet proposes a multi-head SimCLR-based self-supervised learning framework for EEG-based Alzheimer's disease (AD) vs. cognitively normal (CN) classification. It decomposes EEG signals into five canonical frequency bands (delta through gamma), applies independent CNN encoders and contrastive projection heads per band, and uses adaptive temperature scaling borrowed from Wang et al. (2024). Evaluated on a 65-subject dataset with Leave-One-Subject-Out (LOSO) cross-validation, it reports 92.90% accuracy.

## Strengths
- **Neurophysiologically motivated multi-band decomposition.** Decomposing EEG into five canonical frequency bands for independent contrastive learning is well-grounded in the known spectral signatures of AD (increased delta/theta, decreased alpha/beta/gamma power). The paper correctly cites the relevant neuroscience literature (Section 1, Moretti et al., 2004; Benwell et al., 2020; Traikapi & Konstantinou, 2021) and designs the architecture to preserve band-specific information.
- **Systematic ablation study.** Table 3 quantifies the contribution of each component: SSL (+29.55% over training from scratch), multi-head (+6.03% over single-head), augmentation, adaptive temperature, and regularization. This provides concrete evidence for the value of each design choice.
- **Appropriate choice of LOSO protocol.** The paper recognizes that LOSO cross-validation is the correct evaluation standard for EEG classification to test generalization to unseen subjects (Section 3.4), which is stronger than random train/test splits.

## Weaknesses

### Fatal
None confirmed as absolutely fatal from the paper alone, but the data leakage concern below is severe enough to potentially invalidate results.

### Major

- **Probable data leakage between SSL pre-training and LOSO evaluation.** Section 3 states: *"During the pre-training stage, the model was trained using the AdamW optimizer... In the subsequent linear evaluation stage, Leave-One-Subject-Out (LOSO) cross-validation was used, and classification was performed with the pre-trained encoder weights kept frozen."* This clearly implies pre-training is performed once on ALL subjects, with LOSO applied only to the downstream classifier. If so, the encoder has already seen every test subject's EEG during contrastive pre-training. Even without labels, contrastive learning captures subject-specific distributional patterns that inflate downstream classification. For valid LOSO evaluation, pre-training must exclude the test subject in each of 65 folds—a requirement nowhere mentioned in the paper. Ironically, Section 3.4 describes LOSO as *"preventing data leakage between subjects and ensuring complete independence between the training and validation sets."* If the leakage exists, all reported results and comparisons to prior work in Table 2 are invalidated.

- **No variance reporting on a 65-subject dataset.** With only 65 subjects (36 AD, 29 CN), individual LOSO fold results will vary substantially. The paper reports only point estimates (92.90% accuracy, 92.85% F1). The closest competitor, BI-MCGNN, reports 91.25 ± 0.38 (Table 2). Without standard deviations or confidence intervals for DGNet, the claimed 1.65 percentage point improvement cannot be assessed for statistical significance. This omission seriously undermines the SOTA claim.

- **Misleading "linear evaluation" terminology and non-linear classifier.** Section 2.1 describes two approaches: (1) frozen encoder + classifier, and (2) *"known as linear evaluation, all parameters of the model including those of the encoder are updated."* Approach 2 is fine-tuning, not linear evaluation—this is a basic terminological error. Section 3 says the frozen encoder approach was used, but the "classifier" is a 3-layer MLP with 512→256→output dimensions, dropout (0.3, 0.2), batch normalization, and ReLU (Section 2.1). This is not a linear classifier. True linear evaluation uses a single linear layer. The MLP's substantial capacity could compensate for poor encoder quality, making the evaluation less informative about what the SSL representations actually learned.

### Minor

- **Unclear architecture description for frequency band extractor.** Section 2.1 first describes *"five parallel 1-dimensional convolution layers"* with depthwise convolutions (groups=C), then separately states *"the signal is decomposed into five canonical frequency bands using bandpass filters."* Figure 2 shows both "1D depthwise convolutions" and "bandpass filters." Whether these are sequential, parallel, or alternative descriptions of the same operation is unclear, hindering reproducibility.

- **FTD subjects excluded without justification.** Section 3.1 describes 23 FTD subjects in the dataset, but only AD vs. CN classification is evaluated. No reason is given for this exclusion, and no multi-class evaluation is attempted, limiting the practical significance of the contribution.

- **Table 1 baselines largely from different EEG domains.** Most compared models (EEGNet, ATCNet, FBCNet, SPARCNet, EEGConformer) were designed for motor imagery or seizure detection, not dementia classification. A task-specific model will naturally outperform generic models applied without domain adaptation. Table 2 provides more meaningful comparisons with dementia-specific methods.

### Trivial
None.

## Nice-to-Haves
- Report per-fold LOSO statistics (mean ± std) and perform paired statistical significance tests against BI-MCGNN.
- Include t-SNE/UMAP visualization of learned representations and analyze which frequency bands contribute most to classification, validating the neurophysiological motivation.
- Provide a 2×2 ablation (±adaptive temperature × ±regularization) to characterize the interaction between these two components, which together account for most of the jump from 79.55% to 92.90%.
- Evaluate on FTD subjects for three-class classification (AD vs. FTD vs. CN).
- Replace the MLP classifier with a single linear layer for proper linear evaluation, or clearly label the current setup as "MLP probing."

## Removed Points
*These points are flagged to be removed; treat them with caution.*

- **"Adaptive temperature and regularization presented without clear novelty attribution"**: Section 2.3 explicitly cites Wang et al. (2024) for both adaptive temperature and regularization, and Section 5 again credits the "Adaptive Multi-head Contrastive Learning (AMCL) strategy (Wang et al., 2024)." Attribution exists; the reviewer overstated this concern.
- **"Introduction is excessively long"**: Removed as a style/formatting nitpick.
- **"Table 1 rounds results to 93% vs 92.90% elsewhere"**: Removed as a trivial formatting inconsistency.
- **"Relative performance improvement reporting (31.5%) is misleading"**: While unusual phrasing, this is a presentation preference, not a substantive flaw.
- **"Missing limitations section"**: Removed as a structural style preference.
- **"Missing analysis (t-SNE, band contribution, error analysis)"**: Moved to nice-to-have. The paper does include Figure 3 (spectrogram visualization of encoder embeddings), though more comprehensive analysis would strengthen the paper.

## Novel Insights
None beyond the paper's own contributions. The multi-band contrastive learning idea is a reasonable architectural choice, but the execution and evaluation are insufficiently rigorous to yield novel empirical findings about EEG representation learning or AD biomarkers.

## Suggestions
- **Critical**: For each LOSO fold, re-run pre-training excluding the held-out subject (65 separate pre-training runs) to eliminate data leakage concerns. If this was already done, state it explicitly with language like "pre-training was independently repeated for each LOSO fold."
- Report mean ± std across LOSO folds and perform paired statistical tests against BI-MCGNN.
- Clarify the frequency band extractor architecture: explicitly state whether bandpass filtering and depthwise convolutions are the same operation, sequential, or alternatives.
- Fix the terminology: rename the evaluation protocol accurately (e.g., "frozen-encoder MLP probing" rather than "linear evaluation"), and correct the mislabeling of fine-tuning as "linear evaluation."
- Attempt three-class classification (AD vs. FTD vs. CN) to demonstrate broader clinical utility.

## Score and Decision

### Anchor Papers (all rounds)

| Paper | Avg Score | Round | Comparison to DGNet |
|---|---|---|---|
| 5lUdTogEL3 (Clothing-Irrelevant ReID) | 1.0 | R1 | Fundamentally flawed; DGNet is substantially better |
| nSDOkm0SKo (Financial Markets NN) | 1.0 | R1 | Not a serious ML paper; DGNet is better |
| P49gSPmrvN (Scientific Discourse UMAP) | 1.0 | R1 | Not a serious ML paper; DGNet is better |
| PcE0yAGAGW (FSL-MIC EEG) | 2.2 | R1, R2 | Similar limited novelty in EEG classification; DGNet has better ablation but worse evaluation concern |
| 6uReXuDWrw (UniEEG) | 2.0 | R1 | Poor writing and limited novelty; DGNet is slightly better written but has similar novelty issues |
| g3PuaFh5vV (Brain Space Neural Decoding) | 2.5 | R1 | More novel idea but similar quality issues; comparable to DGNet |
| TkbjqexD8w (Seizure Classification) | 3.0 | R1, R2 | Most comparable—limited novelty EEG SSL, single dataset, reject; DGNet has more serious evaluation flaw but slightly better ablation |
| wJ6Bx1IYrQ (EEGPT) | 4.0 | R2 | More ambitious foundation model scope, multiple datasets; DGNet is clearly less technically deep |
| 2og3oWsC5n (TaKF+ EEG tuning) | 4.0 | R2 | Comprehensive multi-task evaluation; DGNet has narrower scope and weaker evaluation |
| ejVuTFFkl6 (EEG-ImageNet) | 4.25 | R2 | Dataset contribution with benchmarks; more substantial contribution than DGNet |
| YKfJFTiRz8 (EEG-DisGCMAE) | 5.0 | R1 | Much more technical depth; DGNet is clearly weaker |
| dhLIno8FmH (EEG Image Decoding) | 6.75 | R1 | Accepted; thorough analysis and biological plausibility; far above DGNet |
| NPNUHgHF2w (CBraMod) | 6.75 | R1 | Accepted EEG foundation model; far above DGNet |
| agPpmEgf8C (Predictive Aux RL) | 8.0 | R1 | Accepted; thorough neuroscience+RL work; incomparable quality level |

**Round 1 bracket**: 2.5–4.0
**Round 2 narrowing**: The most comparable paper is TkbjqexD8w (avg 3.0)—similar profile of limited novelty in EEG representation learning with single-dataset evaluation. DGNet has a more serious evaluation concern (probable data leakage) but a slightly more thorough ablation. Papers at 4.0 (EEGPT, TaKF+) are clearly more technically ambitious and better evaluated. DGNet sits at or slightly below the 3.0 anchor.

The paper has a reasonable core idea (multi-band contrastive EEG learning) but is undermined by a probable data leakage issue that the text itself reveals, no variance reporting on a very small dataset, terminological confusion about linear evaluation, and limited novelty given the heavy reliance on borrowed components (SimCLR framework, adaptive temperature from Wang et al., 2024). The claimed SOTA improvement of 1.65% over BI-MCGNN cannot be verified as meaningful without statistical testing.

MY FINAL SCORE: <score>3.0</score>
MY FINAL DECISION: <decision>Reject</decision>