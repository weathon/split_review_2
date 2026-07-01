## Summary

This paper investigates why the "counterintuitive phenomenon" of likelihood-based anomaly detection—where deep generative models assign higher likelihood to anomalous/OOD data than to in-distribution data—is rare in tabular settings. It proposes a domain-agnostic definition of the phenomenon based on relative model performance (the generative model underperforms compared to baselines by a significant margin), benchmarks a normalizing-flow-based likelihood test (NF-SLT with NICE) against 12 baselines across all 47 tabular and 10 CV/NLP embedding datasets from ADBench, and provides theoretical and empirical analyses linking the rarity of the phenomenon to lower dimensionality and weaker feature correlations in tabular data.

## Strengths

- **Extensive and unbiased benchmark evaluation.** The paper evaluates on all 47 tabular datasets and 10 embedding datasets from ADBench without cherry-picking, comparing against 12 baselines (6 shallow + 6 deep) under a consistent protocol. Table 1 provides a comprehensive, reproducible picture: NF-SLT achieves the highest average AUROC (0.8575), lowest average rank (3.43), and a fail ratio of only 0.02. This is the most thorough empirical investigation of likelihood-based tabular anomaly detection I am aware of.

- **The ID / d-Ratio analysis (Section 5.2) is a clean and original empirical framework.** The paper measures feature correlation indirectly via the ratio of intrinsic dimension to ambient dimension (d-Ratio), using a toy autoregressive Gaussian model (Eq. 5, Figure 1 left/center) to show that stronger correlation reduces estimated ID. The comparison of real tabular and image datasets (Figure 1 right, Table 4) makes the point visually and quantitatively: image datasets cluster far from the identity line (d-Ratio ~1%), tabular datasets cluster near it. This is a genuine empirical finding that could inform future work on domain differences in generative modeling.

- **The theoretical derivation connecting dimensionality to likelihood gap (Theorem 5.4) is conceptually valuable.** Even under a strong independence assumption, showing that the lower bound of the expected likelihood gap scales negatively with dimension provides a plausible mechanism for why high-dimensional settings are more prone to likelihood inversion. The extension to AUROC upper bounds (Corollary 5.6) gives the theory practical relevance. While the assumptions are strong, the framework offers a structured way to reason about the problem.

## Weaknesses

### Fatal
None.

### Major

- **The definition of the "counterintuitive phenomenon" (Definition 3.3) does not align with the phenomenon the title and abstract invoke, creating a gap between the research question and the evidence provided.**  
  The original observation in the image domain (Nalisnick et al., 2019a) was a *likelihood-assignment* phenomenon: a model trained on CIFAR-10 assigned *higher* likelihood to SVHN than to CIFAR-10. The quantity of interest is whether anomalies systematically get higher likelihood than normal data (AUROC < 0.5). Definition 3.3 replaces this with a *relative model-performance* criterion: the phenomenon occurs when most comparison models beat the generative model by a margin γ.  

  These are not equivalent. NF-SLT could have AUROC = 0.86 (no inversion, strong performance) yet qualify as "counterintuitive" under Definition 3.3 if all baselines had AUROC = 0.96. Conversely, a model could have AUROC = 0.4 (genuine likelihood inversion) but Definition 3.3 would *not* classify it as counterintuitive if all baselines were also below 0.4.  

  The paper's headline empirical claim—"the counterintuitive phenomenon is rare in tabular anomaly detection"—follows mechanically from the definition + results: NF-SLT outperforms baselines (Table 1), so by Condition 1 of Definition 3.3 the phenomenon cannot occur. This is a restatement of the performance table rather than an independent empirical discovery. The paper dismisses the simpler "likelihood inversion" criterion by arguing it would "consider any result outside 100% AUROC as counterintuitive" (lines 25–26)—a straw man, since the natural threshold is AUROC < 0.5, not AUROC < 1.0.  

  The paper's "why" analysis (Sections 5.1–5.2) is valuable and partially independent of this issue, but the paper should have answered the title's question directly by checking whether likelihood inversion (AUROC < 0.5) occurs on any of the 47 datasets. This is not reported.

### Minor

- **No direct evidence about whether likelihood inversion (AUROC < 0.5) occurs for any individual tabular dataset.**  
  The paper reports only average AUROC across 47 datasets (Table 1 top). Per-dataset AUROC values, likelihood histograms for normal vs. anomalous test data, or even a simple count of datasets where AUROC < 0.5 would directly answer the question posed in the title. Without this, readers cannot verify whether the original form of the phenomenon occurs even if the paper's own definition says it does not.

- **The experimental protocol differs from the setting where the image-domain phenomenon was originally observed, and this confound is not discussed.**  
  The paper uses the semi-supervised protocol of Zong et al. (2018): train on 50% of normal data only. The original image-domain phenomenon (Nalisnick et al., 2019a) was observed in an unsupervised setting: train on the full multi-class CIFAR-10 dataset. These are different tasks, and the protocol difference alone could explain the absence of the phenomenon in the tabular experiments. The paper should acknowledge this and ideally add an unsupervised experiment to control for it.

- **Theorem 5.4 assumes independent features (P = ∏ p_i, Q = ∏ q_i), which is violated by both image and tabular data, yet the paper does not discuss how this assumption impacts the conclusion for tabular data.**  
  The paper notes the assumption limitation for raw image experiments (line 164: "independence between pixels is not guaranteed, so the theorem…cannot be applied") but does not acknowledge that the same issue applies to tabular data. Section 5.2 itself shows that tabular data has non-trivial feature correlation (d-Ratio < 1.0 for most datasets). The theorem provides intuition but its quantitative claims (linear dependence on d) rest on an assumption the paper's own empirical analysis contradicts.

- **The claim in Section 5.1 that "AUROC increases as the dimensionality decreases" is overstated for one of the three reported cases.**  
  In Table 2, CIFAR-10/SVHN gives: 0.3311 (1024) → 0.2924 (512) → 0.2984 (256) → 0.3143 (30). The trend is non-monotonic, and the net change from 1024 to 30 dimensions is a *decrease* (0.3311 → 0.3143). The other two cases (CIFAR-100/SVHN, CelebA/SVHN) do show a clear monotonic increase. The paper should qualify this claim.

### Trivial
None.

## Nice-to-Haves

- Show likelihood histograms for normal vs. anomalous test data on a few representative datasets to make the empirical claim concrete.
- Add an unsupervised AD experiment (train on all data, normal + anomaly mixed) to control for the protocol confound with the image-domain setting.
- Run per-dataset hyperparameter selection (validation split) instead of global hyperparameter selection across all datasets.
- Discuss how feature correlation could affect Theorem 5.4's bound, even as a qualitative argument.

## Removed Points

- **β and γ not stated in main text**: The reviewer noted that Definition 3.3's parameters β and γ are never assigned numeric values in the main text. The paper states the rigorous formulation with specific values is in Appendix B. Per the Hard Rules, this weakness about appendix content (stripped by the parser) is removed. The values exist in the original submission.

- **Criticism that the definition treats the phenomenon as a model property rather than a likelihood property**: Partially subsumed into the Major weakness above, but the reviewer's framing of this as a "structural flaw" was too harsh. The paper explicitly motivates its definitional choice (arguing the simple likelihood-inversion criterion is inadequate), which is a defensible methodological position even if it creates the mismatch identified above.

- **Formatting/presentation nitpicks** from the Section-by-Section Notes: These are parser artifacts and/or minor points that do not affect the paper's contribution.

## Novel Insights

None beyond the paper's own contributions. The harsh critic's main cross-cutting insight—that the paper's definitional choice creates a gap between the stated research question and the evidence provided—is accurate but is essentially the paper's own limitation stated more directly. The paper's own ID/d-Ratio analysis remains the most genuinely novel empirical contribution.

## Suggestions

1. **Re-center the empirical analysis.** The paper should directly answer whether likelihood inversion (AUROC < 0.5) occurs on any of the 47 tabular datasets. Report per-dataset AUROC values and/or the count of datasets where NF-SLT's AUROC < 0.5. This is a direct, unambiguous test that would settle the question in the title. The current Definition 3.3 can be retained as a *secondary* robustness check, but it should not be the primary lens.

2. **Acknowledge the protocol confound.** Add a brief discussion of the difference between semi-supervised tabular AD (Zong et al., 2018) and unsupervised image OOD detection (Nalisnick et al., 2019a), and ideally include one additional experiment in the unsupervised setting to control for it.

3. **Qualify the claim about AUROC increasing with decreasing dimension** (Table 2, CIFAR-10/SVHN case) to reflect the non-monotonic trend.

4. **Discuss the independence assumption** of Theorem 5.4 more honestly. A paragraph noting that real tabular data also has correlations (as Section 5.2 shows) and explaining why the theorem's insight is still directionally relevant would strengthen the paper.

## Score and Decision

MY FINAL SCORE: <score>6</score>
MY FINAL DECISION: <decision>Accept</decision>