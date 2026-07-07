Now I have all the calibration data I need. Let me produce the final review.

## Summary

This paper empirically studies when reasoning data should be injected during LLM training (pretraining vs. SFT) and what data properties (diversity, quality, scale) matter most at each phase. Training 8B models from scratch for 1T tokens with a fully crossed design across multiple pretraining conditions, SFT recipes, and RL, the paper finds that front-loading reasoning data into pretraining creates durable advantages that post-training cannot fully recover. It also proposes an "asymmetric principle": diversity and scale matter more in pretraining, while quality dominates in SFT.

## Strengths

1. **Important and timely research question (Section 1).** The paper investigates whether the timing of reasoning-data injection matters, which is both scientifically interesting and practically urgent given the industry trend toward reasoning-focused models. The community has largely treated reasoning as a post-training skill, and this paper challenges that framing directly.

2. **Substantial experimental infrastructure (Sections 2–3).** Training 8B models from scratch for 1T tokens with a fully crossed design across 4 pretraining conditions, multiple SFT conditions, and evaluation through RL represents a major compute investment. The control of total reasoning token budget (80B) across all pretraining conditions is a clean design choice that enables fair comparison.

3. **The catch-up experiment is clean and convincing (Table 4, Section 5).** Testing whether 2× SFT epochs on the baseline allows it to match reasoning-pretrained models is a direct and rigorous test of the paper's central thesis. The finding that even 2× SFT on M_base fails to match M_SHQ+SFT_SHQ (+3.32% gap) is the single strongest piece of evidence in the paper.

4. **Evaluation through to RL (Table 3).** Showing that the advantage persists and widens through GRPO-based RL (a 18.74 percentage-point gap) strengthens the central claim that pretraining choices dictate the final performance ceiling.

## Weaknesses

### Major

1. **"Latent effect" claim is structurally confounded by data overlap (Section 5, Table 4).** The paper claims that high-quality pretraining data (D_SHQ added to D_LDQ, creating D_LMQ) has a "latent effect" unlocked by SFT. The evidence: M_LMQ barely outperforms M_LDQ at pretraining (64.07 vs 64.09) but outperforms it after SFT on D_SHQ (50.95 vs 46.70, +4.25). The problem: M_LMQ already contains D_SHQ in its pretraining mix. When both models are SFT'd on D_SHQ, M_LMQ sees D_SHQ for the second time while M_LDQ sees it for the first time. The "latent effect" is indistinguishable from a repetition benefit — more total exposure to the same examples. The paper acknowledges that small datasets are "repeated" during pretraining (Section 2.3) but does not discuss how this confounds the latent-effect interpretation. A proper test would require a control where the additional pretraining data is equally high-quality but *different* from the SFT data.

2. **Diversity and scale are not disentangled in the pretraining comparison (Sections 2.2, 4).** The paper's asymmetric principle claims "diversity matters in pretraining." The evidence compares M_LDQ (diverse, 268M unique samples) vs M_SHQ (narrow, 1.2M samples). These differ on *both* diversity and scale — M_SHQ's 1.2M samples are repeated ~67× during pretraining to reach the 80B token budget, while M_LDQ's 268M samples have minimal repetition. The poor performance of M_SHQ could reflect overfitting from extreme repetition rather than a failure of "narrow but high-quality" data. The paper's attribution of the advantage to *diversity specifically* is not fully supported by the current design. This does not invalidate the overall finding that D_LDQ-style data works better in pretraining, but it means the attribution to the specific factor of diversity is confounded.

### Minor

3. **Headline percentage figures are ambiguous and the "11% diversity gain" is overattributed (Abstract, Section 1).** All "% gain" figures in the abstract ("19%," "11%," "15%," "-5%") are absolute percentage-point differences presented simply as "%" (e.g., 37.9→56.7 is called a "19% gain" rather than "19 percentage point gain"). Additionally, the "11% gain with diverse corpus" claim in the abstract attributes the full M_LDQ vs M_base gap (64.09 vs 52.70) to *diversity specifically*, but M_LDQ differs from M_base in having reasoning data at all, not just in diversity. The proper isolation (M_LDQ vs M_SHQ, 64.09 vs 54.98) yields ~9%, not 11%. The paper body is more careful (Section 5 correctly uses the 9.09% figure for diversity), but the abstract and introduction overclaim.

4. **No variance or significance estimates (Tables 1–8).** All results are single numbers without error bars, confidence intervals, or multiple-seed runs. While multiple seeds are expensive at this scale, the lack of any uncertainty information makes it impossible to assess whether fine-grained differences are meaningful or noise. The paper's "latent effect" finding in particular hinges on a pretraining difference that is essentially zero (64.07 vs 64.09) being interpreted as a null result, which requires variance information to support.

5. **SFT protocol uses substantially different repetition rates across conditions (Section 3.1).** SFT uses "4.8M reasoning samples." For D_SHQ (1.2M unique samples) this is ~4 epochs; for D_LDQ (268M samples) this is a tiny fraction of an epoch. This differential repetition in SFT is not discussed as a potential confound in the quality vs. diversity comparison at the SFT stage.

6. **Data quality is asserted but never directly measured (Section 2.2).** The paper's central axis is "quality vs. diversity," but quality is proxied by data source provenance and answer length rather than quantified directly. There are no metrics (reward model scores, human ratings, factuality measures) that characterize what makes D_SHQ higher quality than D_LDQ. This weakens the precision of the "quality governs SFT" claim.

### Trivial

7. The 600B/400B two-stage pretraining schedule means reasoning data is introduced only in the last 40% of training, which is somewhat at odds with the "front-loading" rhetoric (Section 2.3). This does not invalidate the comparisons (all models follow the same schedule) but the framing could be more precise.

## Nice-to-Haves

- Add an explicit control for the latent-effect confound: SFT a model on a different high-quality dataset to rule out the repetition-benefit explanation.
- Add a "diverse but small" pretraining condition (e.g., sample 1.2M from D_LDQ) and a "narrow but large" condition to disentangle diversity from scale/repetition rate.
- Replace "% gain" with "percentage point gain" or "absolute improvement" throughout to avoid ambiguity.
- Report bootstrapped confidence intervals or at minimum add a limitations paragraph discussing the lack of variance estimates.

## Removed Points

The following points from the input review were removed for the stated reasons:

- *"First systematic study" claim repeated 3 times* — REMOVED as a minor style observation that does not constitute a substantive weakness. The paper acknowledges related work and the claim is directionally accurate.
- *"Criticism about the 11% gain being based on M_LDQ vs M_base comparison" framing as fatal* — DEMOTED to Minor. The paper body correctly handles this distinction (Section 5 uses the M_LDQ vs M_SHQ comparison for diversity isolation). Only the abstract/intro oversimplify.
- *"Evaluation benchmarks shift between phases"* — REMOVED. The paper explicitly acknowledges this design choice ("unlike in base model evaluations"). Using harder benchmarks for SFT/RL models is standard practice; this is not a flaw but a design decision.
- *"SFT scaling finding based on one comparison"* — WEAKENED and subsumed into the general point about confounds. It's one data point in an ablation section, not the paper's main claim.
- *Speculative comments about "the appendix may specify X"* — REMOVED per hard rules about speculative fatal claims.
- *Generic strengths about "importance of the problem"* — REMOVED per rules about generic strengths. The retained strengths are specific and evidence-grounded.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. **Disentangle the latent-effect confound.** Add a control experiment where a different high-quality dataset (not D_SHQ) is used for SFT, to rule out the repetition-benefit explanation for M_LMQ's post-SFT advantage over M_LDQ.

2. **Calibrate the diversity claim.** Acknowledge that the "diversity matters in pretraining" finding is confounded with dataset scale and repetition rate. Replace "diversity" with "diversity and scale" consistently, including in the abstract.

3. **Clarify percentage notation.** Replace "19% gain" with "19 percentage point gain" or "19% absolute improvement" throughout the abstract and introduction to avoid ambiguity.

4. **Add a limitations section.** Explicitly discuss the confounds identified above and the lack of variance estimates as limitations of the current study.

## Score and Decision

**Round 1 bracket: [5.5, 7.0]**

**Calibration anchors used:**
| Path | Avg Score | Round | Itemized? | Comparison |
|------|-----------|-------|-----------|------------|
| /home/.../KIPJKST4gw.md | 7.25 | R1 | Yes | Very similar: same research question framing (training stage timing), comparable systematic methodology. The current paper has cleaner token-budget control but more confounded sub-claims. |
| /home/.../3OyaXFQuDl.md | 7.00 | R2 | Yes | Different topic but similar rigor. Current paper is less methodologically tight on sub-claims. |
| /home/.../1hQKHHUsMx.md | 6.75 | R1 | Yes | Different methodology (influence functions). Current paper has more direct experimental evidence. |
| /home/.../S6cBH99BhB.md | 6.50 | R2 | Yes | Comparable: both are systematic studies with some methodological issues. Current paper has a stronger experimental design but similar confound issues. |
| /home/.../oqsQbn4XfT.md | 5.80 | R3 | Yes | Similar topic area (diversity in pre-training/SFT). Current paper has cleaner design and more comprehensive evaluation. |
| /home/.../GtpubstM1D.md | 5.71 | R1 | Yes | Related domain. Current paper has better-controlled experiments. |
| /home/.../8uXkyWFVum.md | 4.20 | R1 | Yes | Similar topic (pre-training/fine-tuning relationship) but at much smaller scale (1B). Current paper is clearly stronger. |

**Score placement rationale:** The paper's core contribution — that front-loading reasoning data into pretraining creates durable advantages — is well-supported and important. The catch-up experiment (Table 4) and RL results (Table 3) are clean and convincing. However, two structural confounds prevent the paper from reaching the 7+ range: the "latent effect" claim is confounded by data overlap, and the "diversity matters in pretraining" claim is confounded with scale/repetition rate. These issues are fixable through claim calibration rather than new experiments. The paper sits between S6cBH99BhB (6.50) — comparable systematic study with methodological caveats — and KIPJKST4gw (7.25) — similar topic with cleaner sub-claims. Its core evidence is stronger than the 5.80–6.25 anchors but the confounds prevent it from reaching 7+.

The paper would benefit from a version that calibrates claims to what the evidence actually supports. The central finding is robust and valuable; it does not need the overreaching sub-claims.

MY FINAL SCORE: <score>6.5</score>
MY FINAL DECISION: <decision>Accept</decision>