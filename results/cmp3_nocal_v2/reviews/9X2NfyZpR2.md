## Summary

This paper introduces TbLTA, the first dense long-term action anticipation (LTA) framework trained exclusively from video transcripts (ordered action lists without timestamps or durations). It uses a temporal alignment module (ATBA) to generate pseudo-labels, a CTC loss for global transcript consistency, cross-modal attention to ground video features with text, and a CRF-based decoder for coherent future predictions. On Breakfast, the deterministic variant (29.03 MoC) slightly exceeds the best fully-supervised method ActFusion (28.45), establishing a new weakly-supervised baseline. Ablations confirm each component contributes meaningfully.

## Strengths

- **First weakly-supervised dense LTA using only transcripts.** The paper correctly identifies that prior work (including Zhang et al. 2021) still uses some form of frame-level annotation. TbLTA requires only ordered action lists — a genuinely novel and practically valuable framing for scaling anticipation to domains where dense labeling is infeasible (lines 31–35, abstract).

- **Competitive deterministic results on Breakfast.** The deterministic variant achieves 29.03 MoC (Table 1), exceeding ActFusion (28.45) and substantially outperforming the only prior weakly-supervised baseline WS-DA (15.65). The gains are concentrated at the 30% observation setting, where TbLTA leads across all anticipation horizons. This is a non-trivial outcome for a method using zero frame-level annotations.

- **Clean ablation study.** Table 4 systematically isolates each component (CTC, cross-attention, CRF, duration loss). Degradations are meaningful and interpretable — removing cross-attention costs ~5.7 points on Breakfast, removing CRF costs ~4.1 points — confirming the architecture is genuinely compositional rather than relying on a single mechanism.

## Weaknesses

### Fatal
None.

### Major
None.

### Minor

- **Stochastic Top1 metric presented without sufficient clarification.** The paper states (line 227): "we also report stochastic results, where TbLTA achieves substantially higher accuracy by capturing multiple plausible futures." The Top1 column in Table 1 shows dramatically higher numbers (Breakfast Avg 37.15 vs deterministic 29.03). However, Top1 is an oracle metric that selects the single best sample from multiple stochastic draws using knowledge of the ground truth — it does not reflect deployable performance. The honest comparison (Mean stochastic vs deterministic) tells a different story: on 50Salads the Mean (19.11) is *worse* than deterministic (20.92), and on Breakfast the Mean (29.37) is essentially tied with deterministic (29.03). The Top1 metric follows the field convention (Abu Farha & Gall 2019) and the table visually separates deterministic/probabilistic results, but the main-text phrasing conflates the oracle Top1 with the stochastic framework as a whole and should be reworded to avoid misleading readers.

- **Limited weakly-supervised baseline comparison.** The only prior weakly-supervised LTA baseline is WS-DA (Zhang et al. 2021), reported at a single configuration (Obs 30%, no horizon breakdown). While the paper correctly notes that WS-DA uses a different (semi-weakly) supervision regime, the comparison lacks depth. The paper also cites Kim et al. (2024) for language-based anticipation without time annotations, but this work predicts symbolic action sequences rather than dense frame-level labels, so the tasks are not directly comparable. The thinness of the weakly-supervised comparison is understandable given the scarcity of prior methods, but the evaluative evidence would be stronger with at least one adapted baseline (e.g., a weakly-supervised TAS method with an anticipation decoder added).

- **EGTEA evaluation is thin.** Table 2 reports only aggregated mAP across observation horizons, with only two baselines (Timeception, Anticipatr). No per-horizon breakdown is given, no variance information, and contemporary methods (ActFusion, FUTR) evaluated on the other datasets are absent. The claim that TbLTA is "competitive on rare classes" rests on a single number (60.11 vs 59.70) without significance testing. This weakens the paper's generalizability claims from the EGTEA benchmark.

- **No variance or significance information.** Results are averaged over dataset splits but reported without standard deviations or confidence intervals. Given that some headline comparisons are close (TbLTA 29.03 vs ActFusion 28.45 on Breakfast), this information is needed to assess whether differences are meaningful.

- **No inference-time analysis.** Model size, inference speed, and the number of stochastic samples used for Mean/Top1 are not reported. For a method claiming scalability benefits, these are relevant omissions.

### Trivial

- **Abstract slightly overstates the gap.** The abstract claims LTA has been tackled "exclusively in a fully supervised manner," but the introduction (line 15) and related work (lines 70–76) discuss Zhang et al. (2021) as a semi-weakly supervised predecessor. The claim is broadly true if qualified as "exclusively with human frame-level annotations" (which Zhang et al. also uses), but as written it is a mild overstatement.

- **Notational inconsistency in CTC loss.** The segmentation head output is defined as π = [π₁, ..., π_{αT}] (line 160, length = observed portion), but the CTC sum in Eq. 4 runs over t=1 to T (full video). The notation should be consistent — π should be length T if CTC is applied to the full video, as the text describes.

- **Ablation table formatting duplication.** Table 4 appears twice (lines 250–257 and 262–269 are identical). The data is present, but this is a layout artifact.

## Nice-to-Haves

- Add variance reporting (standard deviations or confidence intervals) to the main results.
- Report inference-time cost (model size, speed, number of stochastic samples).
- Provide a per-horizon breakdown for EGTEA.
- Deepen the analysis of why Breakfast outperforms 50Salads (e.g., binning by video length or transition density).
- Adapt a weakly-supervised TAS method (e.g., Xu & Zheng 2024) as an additional LTA baseline to broaden the comparison.

## Removed Points

These points were raised in the input review but are removed with justification:

- **"The comparison against weakly-supervised baselines is incomplete (Evidential)"** — downgraded from the critic's framing as a critical/evidential issue to Minor above. The paper compares against the only prior weakly-supervised LTA method (WS-DA). Additional baselines would strengthen the paper but the comparison is not incomplete in a way that undermines the results.
- **"EGTEA evaluation is too thin to support the paper's claims (Evidential)"** — downgraded from critical to Minor. The main contribution (first transcript-only LTA) is supported by Breakfast and 50Salads results; EGTEA is a secondary dataset. The evaluation is thin but not fatal.
- **"EGTEA verb-only evaluation should be acknowledged"** — the paper already acknowledges this explicitly (line 194: "restricting evaluation to verb prediction"). Not a weakness.
- **"Table 3 (IAS) referenced but not in main paper"** — this table may exist in the supplementary material, which the parser strips. Per hard rules, missing supplementary references are not author errors.
- **"Maté & Dimecicoli relationship unclear"** — the paper clearly states it borrows the CRF mechanism: "we apply a Conditional Random Field (CRF), inspired by TCCA (Maté & Damiccoli, 2024)" (line 140).
- **"WS-DA lacks context / not specified if re-implemented"** — speculative; the paper cites existing numbers. Not a valid weakness.
- **"Duration prediction not analyzed"** — a nice-to-have, not a weakness.
- **Formatting artifacts** (table duplication, etc.) — these are parser artifacts, not author errors.

## Novel Insights

The reviews surface the key tension: the paper's core contribution (first transcript-only dense LTA) is genuine and well-supported by the deterministic Breakfast results, but the Top1 stochastic framing introduces ambiguity about how much the stochastic variant actually adds. The Mean stochastic results are not clearly better than deterministic, suggesting the stochastic model's real value may be in uncertainty quantification rather than accuracy gains. This tension is worth the authors addressing explicitly in revision.

## Suggestions

1. Reframe the "substantially higher accuracy" claim about stochastic results to refer specifically to the Top1 (oracle) metric, and clearly explain what Top1 means early in the paper.
2. Add standard deviations or confidence intervals to Table 1, especially for the closely-matched comparisons.
3. Include a per-horizon breakdown for EGTEA or recalibrate the claims made from it.
4. Report the number of stochastic samples used and inference speed.
5. Fix the notational inconsistency in the CTC loss definition (π length vs summation range).

MY FINAL SCORE: <score>7.0</score>
MY FINAL DECISION: <decision>Accept</decision>