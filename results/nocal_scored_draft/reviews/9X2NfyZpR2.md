Now I have the favorability signals. The two heaviest negatives (overclaiming at 0.01, missing variance at 0.00) are real concerns, but the strongest positives (problem identification, architecture, ablation, Breakfast result at 1.00) are also well-grounded. The paper's core technical contribution is genuine. Here is my final review:

---

## Summary

This paper introduces TbLTA, the first framework for dense long-term action anticipation (LTA) trained solely from video transcripts — ordered action lists without timing or boundary information. The architecture combines temporal alignment (ATBA) to generate soft pseudo-labels, cross-modal attention to ground video features in transcript semantics, CTC loss for global alignment, and a CRF for sequence-level coherence. Evaluated on Breakfast, 50Salads, and EGTEA, the method establishes the first transcript-only LTA benchmark and achieves a striking result on Breakfast at 30% observation where it outperforms all fully-supervised baselines.

## Strengths

- **Addresses a genuinely under-explored and important problem.** Prior LTA work requires dense frame-level annotations or at least some temporally-localized labels (Zhang et al., 2021). Moving to transcript-only supervision is a meaningful step toward scalability, and the paper correctly identifies this gap.

- **Architecture is modular, well-motivated, and validated.** Each component serves a clear purpose in the weakly-supervised setting: ATBA preserves boundary uncertainty, localized cross-modal attention grounds text in the correct video segments, CTC enables alignment without boundary annotations, and the CRF enforces sequence coherence. The ablation study (Table 4) demonstrates positive contributions from most components.

- **Genuinely strong result on Breakfast at 30% observation.** TbLTA's deterministic model achieves 40.28, 35.76, 31.67, and 28.79 at the four prediction horizons — outperforming all fully-supervised baselines including ActFusion (35.79, 31.76, 29.64, 28.78). This is a noteworthy demonstration that transcript supervision can, in some settings, exceed dense supervision.

- **Thorough ablation and clear architecture figure.** The paper systematically evaluates each loss component and module, providing clear evidence for design decisions.

## Weaknesses

### Major

- **Overclaimed generalization relative to evidence.** The abstract claims transcript supervision offers "a very robust and less costly alternative to its fully supervised counterpart" and the conclusion states results are "competitive with, and in certain settings even superior to, fully supervised methods." This framing is misleading when viewed across all datasets: on 50Salads, TbLTA's deterministic results are far below every fully-supervised baseline at every horizon (e.g., 24.90 vs 39.55 for FUTR at Obs 20%/10%); on EGTEA, TbLTA trails Anticipatr by ~11 mAP points on All and Freq. The strong Breakfast Obs 30% result is the exception, not the rule. The paper's core contribution — being the *first* transcript-only LTA system — is valuable on its own and should be framed with appropriate scope, acknowledging clear trade-offs rather than asserting general competitiveness with full supervision.

### Minor

- **The weakly-supervised comparison is limited to a single baseline (WS-DA, Zhang et al., 2021) at one setting (Obs 30%, 10% horizon).** While being the first transcript-only LTA system partially justifies limited baselines, the paper would be strengthened by simpler transcript-based pipelines (e.g., using ATBA pseudo-labels to train an off-the-shelf fully-supervised LTA model) to help the reader assess whether TbLTA's architectural choices are necessary or whether pseudo-label quality is the main bottleneck.

- **No variance or error bars reported.** Despite averaging over 4 splits (Breakfast) and 5 splits (50Salads), only point estimates are given. Some claimed advantages are extremely small (e.g., 28.79 vs 28.78 on Breakfast Obs 30%/50%), making statistical significance impossible to assess. This is essential for any comparative evaluation.

- **The stochastic protocol is not explained in the main text.** It is referenced only to the supplementary material and prior work (Abu Farha & Gall, 2019). The source of stochasticity — whether from CRF sampling, the parallel decoder, or a separate mechanism — is not described. Since the deterministic and stochastic Top1 results differ substantially (e.g., 29.03 vs 37.15 average on Breakfast), the comparison is uninterpretable from the main paper alone.

### Trivial

- The abstract states LTA has been tackled "exclusively in a fully supervised manner," but the introduction cites Zhang et al. (2021) as a prior (semi-)weakly-supervised attempt. The paper later correctly distinguishes its setting, but the abstract is slightly overbroad.

## Nice-to-Haves

- A baseline using ATBA pseudo-labels with an off-the-shelf LTA model would help quantify the value of TbLTA's specific architectural components.
- Computational cost (training time, inference speed) would contextualize the scalability motivation.

## Removed Points

- *Duration loss circularity:* The harsh critic flagged the self-supervised duration loss as "circular." This is a standard bootstrapping approach in weakly-supervised learning; the paper explicitly states it is trained "without any temporal ground truth." Not a genuine flaw.
- *Training on future frames:* The critic noted the encoder sees future frames during training. This follows standard practice in the LTA literature (Gong et al., 2024, which the paper cites) and does not constitute a weakness.
- *CRF short-horizon understatement:* The paper acknowledges the short-horizon tradeoff and provides all values in Table 4. The characterization is reasonable and the data is transparent.
- *EGTEA baseline count:* EGTEA is an additional benchmark; the main evaluation on Breakfast and 50Salads has dense supervised baselines fully reported.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. Reframe the abstract and conclusions to present TbLTA as the first demonstration that transcript-only LTA is feasible, with competitive results on some benchmarks and clear gaps on others — not as a general competitive alternative to full supervision.
2. Add standard deviations or error bars to multi-split results.
3. Include a simple baseline: train a fully-supervised LTA model on ATBA pseudo-labels to isolate the effect of architectural choices from pseudo-label quality.
4. Briefly explain the stochastic protocol mechanism in the main paper so the deterministic vs. stochastic comparison is interpretable without the supplementary.

## Score and Decision

The paper makes a genuine contribution as the first transcript-only LTA framework with a well-designed architecture and a compelling result on Breakfast at 30% observation. However, the central weakness is the substantial mismatch between the framing (claiming general competitiveness with full supervision) and the evidence (strong on one dataset/setting, weak on others). This overclaiming, combined with missing variance reporting and an underspecified stochastic protocol, prevents acceptance in the current form. With honest reframing and the additions noted above, the paper's core contribution would be solid.

MY FINAL SCORE: <score>6</score>
MY FINAL DECISION: <decision>Borderline Accept</decision>