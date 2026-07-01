## Summary

This paper proposes TbLTA, the first weakly-supervised framework for dense long-term action anticipation (LTA) that uses only video transcripts (ordered action lists without timings or durations) as supervision. The method combines a temporal alignment module (ATBA) to generate pseudo-labels, a cross-modal attention mechanism for grounding video features with transcript semantics, and an encoder-decoder architecture trained with CTC, CRF, and duration losses. Results on Breakfast, 50Salads, and EGTEA establish a transcript-only baseline, with the deterministic model achieving competitive performance against fully supervised methods on Breakfast (29.03% avg MoC at 30% observation vs. 28.45% for ActFusion).

## Strengths

1. **First transcript-only weakly-supervised framing for dense LTA.** The paper correctly identifies that prior LTA work requires dense frame-level annotations, and that prior weakly-supervised attempts (Zhang et al., 2021) still need frame-level labels for the observed segment. Using only ordered action lists is a genuine and well-motivated step toward scalability.

2. **Competitive results on Breakfast at 30% observation.** Under the deterministic protocol, TbLTA achieves 29.03% average MoC on Breakfast, matching the fully supervised ActFusion (28.45%) and surpassing most other supervised methods (Table 1). Given that TbLTA sees no frame-level labels, this is an interesting result that suggests transcript-level supervision can capture procedural structure effectively.

3. **Systematic ablation study.** The ablation in Table 4 systematically removes CRF, cross-attention, and duration loss, showing measurable degradation in each case across both Breakfast and 50Salads. The cross-attention ablation additionally compares against a simpler unconstrained variant, providing finer-grained analysis than a simple presence/absence test.

4. **Novel cross-modal attention design.** The gated residual cross-attention mechanism (Eqs. 1–2) with transcript-derived binary masks is technically well-specified and provides a concrete architectural contribution beyond the problem framing.

## Weaknesses

### Fatal
None.

### Major
None.

### Minor

1. **EGTEA evaluation clarity.** Table 2 reports TbLTA against Timeception and Anticipatr on EGTEA, with TbLTA evaluated under a verb-only (19-class) protocol as stated at line 194. The paper does not clarify whether the baseline numbers reflect the same verb-only protocol or the full 106-class verb-noun task. Since verb-only prediction is substantially easier, this omission makes the EGTEA comparison difficult to interpret. The paper's EGTEA claims are modest ("supervised models retain a clear edge overall" and "competitive on rare classes"), but transparency about the comparison is still needed.

2. **Stochastic results are underspecified in the main paper.** Table 1 reports TbLTA\* - Mean and TbLTA\* - Top1 with a footnote saying "\* means stochastic protocol" and a reference to the supplementary material. The main text does not explain what "Mean" and "Top1" refer to, how many samples are drawn, or why the gap between deterministic and Top1 results is so large (e.g., ~10 points on Breakfast at Obs 20%). While details may exist in the supplementary material, the main paper should briefly define the inference protocol.

3. **No variance or per-split results reported.** Results are averaged over 4 (Breakfast) and 5 (50Salads) standard splits but no standard deviations, confidence intervals, or per-split ranges are given. Several comparative claims involve close margins (e.g., TbLTA 29.03 vs. ActFusion 28.45 on Breakfast), and the ablation shows cross-over patterns (e.g., w/o CRF outperforming the full model at short horizons on Breakfast at Obs 20%/10%: 39.7 vs 37.2). Without variance, it is difficult to assess whether differences are systematic or within the noise floor. (This is common practice in the LTA literature, but reporting variance would substantially strengthen the evidence.)

4. **Limited comparison with the only prior weakly-supervised LTA method.** WS-DA (Zhang et al., 2021) is cited with only two data points (one per dataset, both at Obs 30%), with no other horizons reported. The paper also notes that WS-DA is not fully weakly supervised (it uses frame-level labels for the observed segment). The claim of "consistently surpassing prior weakly-supervised baselines" (line 227) rests on a thin comparison. The paper would be better served by emphasizing the new benchmark it establishes rather than positioning as "surpassing" prior methods.

5. **The "stochastic variant" claim in related work is not reflected in the methodology.** The related work (lines 94–96) states "we propose a stochastic variant" of a CRF-based LTA approach, but the method section describes the CRF as a loss function (negative log-likelihood), not as a generative sampling mechanism. The stochastic results appear to come from adopting the "stochastic protocol of Abu Farha & Gall (2019)" (line 223) rather than from the CRF design. This creates a disconnect between the claim and the actual method.

6. **Inference-time horizon determination is not addressed.** The problem definition (line 114) defines observation and prediction lengths as fractions α and β of total frames T. At inference, only X_obs is available and T is unknown. The paper does not explain how the model determines how many future frames to predict at inference time. The decoder uses EOS termination, but how this maps to the βT frame-count evaluation protocol is unclear.

### Trivial
None.

## Nice-to-Haves
- Analyze ATBA pseudo-label quality (e.g., frame-level agreement with ground-truth labels, which are available for evaluation), to directly validate whether the weak supervision is working as intended.
- Report per-split results or variance alongside the averages.
- More systematic qualitative analysis (failure cases, error patterns across classes).
- Specify the numerical values of γ₁, γ₂, γ₃ in the main paper.
- Ablate ATBA against a simpler alignment baseline (e.g., uniform assignment, CTC-only).

## Removed Points
These points from the input review were removed with justification:
- **"Missing hyperparameters γ₁, γ₂, γ₃"**: The paper states "More details in the supplementary material" — these likely exist in the stripped appendix. Removed per rule against appendix-based criticisms.
- **"Duration loss circularity"**: The paper explicitly acknowledges this is a "weak duration prior" (line 283) and the ablation shows it helps. The concern is overblown; this approach is standard for weakly-supervised settings.
- **"Insufficient qualitative results"**: Subjective opinion; moved to Nice-to-Haves.
- **"Incomparable EGTEA evaluation" framed as a structural/fatal flaw**: The concern is speculation (baseline numbers may or may not be from the verb-only protocol) and conditional. Demoted to a Minor clarity issue about transparency, not a fatal flaw.

## Novel Insights

The most interesting observation emerging from the review is the framing asymmetry: the paper claims to "surpass" prior weakly-supervised baselines while simultaneously acknowledging that those baselines (Zhang et al., 2021) use *less* weak supervision (frame-level labels for the observed segment). The more honest and scientifically impactful framing would be to position the work as establishing the first transcript-only benchmark for LTA, letting the absolute performance speak for itself rather than constructing a thin head-to-head comparison. This is a genuine insight about how the paper's narrative could be improved without changing any experiments.

## Suggestions

1. **Clarify the EGTEA baseline comparison.** State explicitly in Table 2 whether Timeception and Anticipatr numbers are under the same verb-only (19-class) protocol. If they are, state this. If not, note the difference and adjust claims accordingly.
2. **Briefly define the stochastic protocol in the main paper.** Explain what Mean and Top1 mean, how many samples are drawn, and why the deterministic/stochastic gap exists.
3. **Add variance to the main tables.** Report standard deviations or per-split ranges alongside the averages. This is a straightforward addition from the existing splits.
4. **Explain how the anticipation horizon β is determined at inference.** Since total video length T is unknown during inference, clarify how the model knows how many future frames to predict.
5. **Frame the WS-DA comparison more carefully.** Acknowledge that the only prior weakly-supervised LTA method provides very limited points of comparison and that the main contribution is establishing a new transcript-only benchmark, not "surpassing" prior methods.

## Score and Decision

**Calibration anchors:**

| Paper | Avg Score | Round | Comparison |
|---|---|---|---|
| Actions-to-Action (dl34rOnbqJ) | 4.40 | R1 (3.5–5.5) | Less novel framing, smaller improvements. TbLTA is stronger. |
| Weakly Supervised Skill (HCoSsULNxG) | 4.75 | R2 (4.5–6.5) | Similar evaluation gaps, less competitive results. TbLTA is stronger. |
| Language Repository (O8FkMqNF1M) | 5.50 | R2 (5.0–6.0) | Comparable contribution level, similar borderline issues. |
| Video Active Perception (KtqZrNjvjd) | 5.80 | R2 (5.0–6.0) | Interesting idea but fairness concerns. Comparable overall. |
| Weakly Sup. VidSGG (GQgPj1H4pO) | 6.00 | R1 (5.5–7.5) | Better evaluation clarity. TbLTA has stronger problem novelty. |
| LASER (HEXtydywnE) | 6.00 | R1 (5.5–7.5) | Better presentation, similar weak supervision framing. |
| AntGPT (Bb21JPnhhr) | 6.25 | R2 (4.5–6.5) | SOTA on multiple LTA benchmarks. TbLTA has weaker evaluation. |

**Round 1 bracket:** 4.5–6.5 (after comparing to strong rejects, scores 3.5–5.5, and scores 5.5–7.5 anchors)

**Round 2 narrowing:** 5.0–6.0 (after comparing to AntGPT at 6.25 and the Weakly Supervised Skill paper at 4.75)

**Final score determination:** The paper has a genuinely novel problem framing (first transcript-only weakly-supervised LTA) and competitive results on Breakfast. However, the evaluation has several clarity issues (EGTEA comparison, underspecified stochastic protocol, missing variance) and a thin WS-DA comparison. These are all fixable, but in the current form the evidence is not as decisive as it could be. The paper is borderline — real contribution but notable evaluation gaps.

MY FINAL SCORE: <score>5.5</score>
MY FINAL DECISION: <decision>Reject</decision>