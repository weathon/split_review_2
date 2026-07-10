## Summary

This paper conducts the first systematic study of how reasoning data (varying in scale, diversity, and quality) affects LLM performance when introduced at different training stages—pretraining vs. SFT. The authors pretrain four 8B models from scratch for 1T tokens each (one baseline without reasoning data, three with different reasoning corpora), then fine-tune each on three SFT variants (12 SFT models), and apply RL to two extremes. The central findings are: (1) front-loading reasoning data into pretraining creates a durable advantage that SFT alone cannot reproduce, (2) the optimal data strategy is asymmetric—diversity matters in pretraining while quality dominates in SFT, and (3) naively scaling SFT data can be actively harmful.

## Strengths

- **Large-scale, carefully controlled experimental design.** Pretraining four 8B models from scratch for 1T tokens each with a crossed design (4 pretraining variants × 3 SFT datasets = 12 SFT models, plus RL) is a substantial, systematic effort that goes well beyond prior work. The total token budget is fixed at 1T across all conditions, providing a clean controlled comparison.

- **The asymmetric principle—diversity in pretraining, quality in SFT—is a crisp, actionable finding.** This directly informs data allocation decisions for practitioners and is well-supported by the data: Table 1 shows diversity drives pretraining gains (+28% math for M_LDQ over baseline), while Table 5 shows high-quality SFT data (D_SHQ) dramatically outperforms diverse but mixed-quality SFT data.

- **The "catch-up" test (Table 4) is well-designed and produces a clear result.** Doubling SFT epochs on the baseline still fails to match even the weakest reasoning-pretrained model (+3.32% gap), cleanly refuting the hypothesis that intensive SFT can compensate for a weak pretraining foundation.

- **The SFT scaling analysis (Table 8) is striking and practically important.** Naively doubling mixed-quality SFT data hurts math reasoning (−4.92%), while a marginal (0.4%) addition of high-quality long-CoT data yields consistent gains. This provides a clear warning against quantity-driven SFT scaling.

## Weaknesses

### Major
None.

### Minor

- **The RL-phase evidence for the compounding-advantage claim is thin.** Only 2 models (M_base+SFT_SHQ and M_LMQ+SFT_SHQ) undergo RL, so the headline 18.57% RL gap rests on a single comparison. The paper acknowledges these as "extreme pretraining backbones" (line 193), but the broader claim that "pretraining strategy dictates final accuracy on expert-level tasks" would be substantially stronger with at least one more RL condition (e.g., M_LDQ+SFT_SHQ+RL). This is the paper's strongest quantitative claim, and it currently rests on the narrowest evidence base.

- **No statistical uncertainty is reported.** While the largest effects (28% math gain, 18.57% RL gap) are convincing without confidence intervals, several important claims rely on smaller differences: the +4.25% "latent effect" (M_LMQ vs M_LDQ post-SFT, Table 4) and the reasoning/instruction-following trade-offs in Table 7. Without any measure of variability (including evaluation-level variance, which the paper already has via multiple eval runs for several benchmarks), the reader cannot assess whether these smaller effects are robust or reflect noise from single-seed runs.

- **The 4.8M SFT sample selection procedure is underspecified.** The paper states (line 124) that each model is finetuned on 4.8M reasoning samples from D_res. For D_SHQ (1.2M samples), this means ≈4 epochs; for D_LDQ (268M samples), it means sub-sampling 1.8% of the data. The paper does not describe how the 4.8M samples are selected from larger datasets (random? stratified?), nor whether the SFT results are stable under different subsamples. This is easily clarified but the omission is a reproducibility gap for the core SFT comparisons.

### Trivial

- **The baseline comparison frames the advantage as purely about reasoning data** when it is actually a trade-off: reasoning-augmented models see 920B D_base + 80B D_res vs. M_base's 1T D_base. The total token budget is controlled, so this is a valid trade-off argument, but the paper could state more explicitly that the advantage partially reflects 80B tokens of problem-solving data being more valuable than 80B tokens of additional general web text.

## Nice-to-Haves

- The paper's phrasing "from the start" (line 154) is slightly imprecise—reasoning data is introduced at 600B tokens (60% through pretraining), not token 0. The experimental design is clearly described in Section 2.3, so this does not mislead, but using "during pretraining" (as the abstract mostly does) is more precise than "from the start."
- The D_SHQ vs. D_LDQ comparison for the SFT quality claim varies not just quality but also domain composition (71% math vs. 56% math), dataset size, and source, creating a confound that could be explicitly discussed.

## Removed Points

These points are flagged to be removed; treat them with caution:

- **"Front-loading" overclaim (Issue 4 from Harsh Critic):** The critic argues that introducing reasoning data only in the last 40% of pretraining does not constitute "front-loading" and that the paper overclaims. This is removed because the paper's central contrast is between introducing reasoning data during any part of pretraining versus only during post-training—a distinction the paper clearly defines and a valid comparison. The abstract accurately says "adding reasoning data earlier during pre-training" (relative to post-training), and Section 2.3 transparently describes the exact schedule. The phrase "from the start" on line 154 is mildly imprecise but does not mislead about the overall claim.
- **1.2B scaling experiment not discussed in main text:** The critic flags this as a missing discussion, but the appendix is stripped by the parser. Per review rules, this is a parser artifact.
- **Missing related works / data availability / model existence concerns:** Removed per hard rules (cited entities are assumed to exist; missing related works cannot be verified by the reviewer).

## Novel Insights

Beyond the paper's own contributions, the reviews do not surface novel insights not already present in the paper.

## Suggestions

1. **Expand the RL comparison.** Even adding one more condition (e.g., M_LDQ+SFT_SHQ+RL) would substantially strengthen the compounding-advantage claim and turn it from a single data point into a pattern.
2. **Specify the 4.8M SFT sampling procedure.** Describe how samples are selected from larger datasets (D_LDQ, D_LMQ) and report whether key SFT results are stable under different subsamples.
3. **Report evaluation-level variance.** The paper already averages 16 runs for AIME tasks and 4 runs for several other benchmarks (line 148). Reporting standard errors or per-run ranges would help readers assess the robustness of smaller effects (the +4.25% latent effect, the trade-offs in Table 7).

## Score and Decision

**Calibration anchors used (all rounds):**

| Path | Avg Score | Round | Itemized? | Comparison to this paper |
|------|-----------|-------|-----------|--------------------------|
| KIPJKST4gw (code data training stage) | 7.25 | 1, 2 | Yes | Most topically similar. This paper has better-controlled experiments (fixed token budget vs. unfixed in anchor) and uniformly higher favorability on weaknesses. |
| 1hQKHHUsMx (pretraining data reliance for reasoning) | 6.75 | 1 | Yes | Different methodology (interpretability vs. training recipe). Broader but less controlled. |
| NGKQoaqLpo (knowledge pollution in LLMs) | 7.50 | 2 | Yes | Our weaknesses are less severe (lowest favorability 5.69 vs. -5.78 in anchor). |
| f4gF6AIHRy (data selection via submodular) | 8.00 | 1, 2 | No | Different topic, higher bar. Our paper lacks the unanimous 8s that anchor achieved. |
| jOmk0uS1hl (test task confound) | 8.00 | 1 | No | Different topic (evaluation methodology), different contribution type. |

**Bracketing:** Round 1 placed the paper above the 7.25 anchor (better-controlled experiments, fewer severe weaknesses) but below the 8.00 anchors (which have unanimous 8s and no harmful weaknesses). **Round 2 narrowed to ~7.5** by comparison with NGKQoaqLpo (7.50): our paper has uniformly higher favorability on weaknesses (5.69–7.81 vs. that anchor's -5.78 to 6.20) and stronger, more directly actionable findings.

**Final score: 7.5.** The paper makes a significant empirical contribution with a well-designed large-scale study and clear, practically useful findings. The weaknesses (thin RL evidence, missing variance estimates, underspecified SFT sampling) are real but addressable and do not undermine the core contributions.

MY FINAL SCORE: <score>7.5</score>
MY FINAL DECISION: <decision>Accept</decision>