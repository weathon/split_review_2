Now let me read the remaining sections to ensure I have full coverage of the paper:Now I have a thorough understanding of the paper. Let me submit my draft review.Now let me run Round 1 calibration — bracketing across score ranges:Let me read the most relevant anchor papers for calibration. The paper KIPJKST4gw (score 7.25) is extremely close in topic — "At Which Training Stage Does Code Data Help LLMs Reasoning?" — and 8uXkyWFVum (score 4.20) is also very similar — "Analyzing the Relationship between Pre-Training and Fine-Tuning."Now let me read the most relevant anchor more carefully — EVa5OIYBoG (3.67) on post-training study, and examine the 6-7 range more carefully:Now I have enough calibration data to finalize my review. Let me summarize the anchors and form my final assessment.

**Round 1 Bracket:**
- The paper is clearly above the reject range (1-3.5): it has genuine computational investment and useful findings
- It's stronger than **8uXkyWFVum** (4.20, "Amuro & Char"): larger scale (8B vs 1B), more comprehensive experiments, more actionable findings
- It's comparable to **GtpubstM1D** (5.71, "Advancing Mathematical Reasoning"): both study PT vs post-training data allocation with useful but methodologically imperfect findings
- It's weaker than **KIPJKST4gw** (7.25, "At Which Training Stage Does Code Data Help"): despite smaller scale, that paper had a cleaner experimental design without the repetition confound
- It's clearly below the 8.0 papers (e.g., "Synthetic continued pretraining"): those have cleaner methodology and stronger evidence

**Initial bracket: 5.0 to 6.5**

The data repetition confound specifically affects the "diversity > quality in pretraining" headline claim but does NOT invalidate the front-loading finding, the latent effect, or the SFT quality finding. The overclaiming is pervasive but correctable. The narrow RL evidence is a gap but not fatal.

---

## Summary
This paper systematically investigates how reasoning data should be allocated across pretraining and post-training (SFT, RL) stages of LLM development. Using four 8B-parameter hybrid Mamba-attention models pretrained from scratch on 1T tokens with varying reasoning data compositions, the authors report that front-loading reasoning data into pretraining provides durable advantages (+8.35% average, Table 1; +9.3% post-SFT, Table 2), and propose an "asymmetric principle" where pretraining benefits from diversity/scale while SFT benefits from quality.

## Strengths
- **Substantial and rare computational investment**: Four 8B models pretrained from scratch on 1T tokens each, then crossed with three SFT recipes producing 12 SFT models (Section 2.3, Section 3.1). This full-factorial PT × SFT design is expensive and uncommon, enabling findings (e.g., the latent effect, Table 4) that could not emerge from cheaper experiments.
- **The "latent effect" of high-quality pretraining data is a genuinely novel observation**: M_LMQ shows minimal immediate benefit over M_LDQ at the pretraining stage (64.07 vs 64.09, Table 1) but reveals a +4.25% advantage after SFT (50.95 vs 46.70, Table 4). This suggests pretraining can instill capabilities that only manifest during alignment—a non-obvious and practically important finding.
- **SFT quality dominance is well-supported**: Table 5 shows M_res + SFT_SHQ achieves 44.99 average vs. 31.54 for M_res + SFT_LDQ, providing clear evidence that SFT is sensitive to data quality rather than scale, across math (+26.38%), science (+19.71%), and code (+18.78%) domains.
- **Actionable SFT scaling insight**: Table 8 demonstrates that doubling mixed-quality SFT data yields a 4.92% math regression while adding 0.4% high-quality data (D_ALF') improves performance, providing a concrete and practical finding for practitioners.

## Weaknesses

### Fatal
None

### Major
1. **The diversity-vs-quality comparison in pretraining is confounded by data repetition.** D_SHQ contains only 1.2M samples (~1.2B unique tokens at ~1000 tokens/sample), which must be repeated ~67 times to fill the 80B reasoning token budget. D_LDQ (268M samples) fills this budget with minimal or no repetition. Section 2.3 acknowledges repetition ("when a reasoning dataset is small, it is repeated") but does not discuss or control for this confound. The well-documented degradation from excessive data repetition means M_SHQ's underperformance (54.98 vs 64.09, Table 1) may reflect repetition artifacts rather than the claimed superiority of diversity over quality. This directly undermines the headline "asymmetric principle" as stated—the paper cannot cleanly attribute M_SHQ's worse pretraining performance to lack of diversity vs. harmful repetition.

2. **The catch-up hypothesis test is asymmetrically scaled and overclaimed.** The test (Table 4) doubles SFT epochs from 4.8M to 9.6M samples (~9.6B tokens), while reasoning-pretrained models received ~80B reasoning tokens during pretraining—nearly an order of magnitude more. Showing that ~10B additional SFT tokens cannot compensate for ~80B pretraining tokens is unsurprising and does not test the interesting version of the hypothesis. Yet the paper uses strong causal language: "proves this hypothesis false" (Section 5), "conclusive evidence" (Section 4), and "refutes" (Section 1). These claims are not warranted for this narrow test.

3. **RL evidence is too thin to support the "compounding returns" claim.** Table 3 compares only M_base + SFT_SHQ + RL vs. M_LMQ + SFT_SHQ + RL—the two most extreme configurations in the design space. No RL results are shown for M_SHQ or M_LDQ, nor for other SFT recipes. The headline "19% average gain" and "compounding returns" claims rest on a single comparison, not systematic evidence.

### Minor
1. **The mathematical formalization is misleading.** Equation 2 presents a budget constraint B = |D_res^PT| + |D_res^SFT| suggesting a shared allocation trade-off between pretraining and SFT reasoning data. In practice, the PT budget (80B tokens) and SFT budget (4.8M samples) are set independently with no experiment shifting reasoning tokens between stages. The formalization implies a controlled trade-off that the experiments do not explore.

2. **IFEval metric confound is undiscussed.** In Table 5, SFT with D_LMQ achieves 56.41 on IFEval vs. 30.59 for SFT with D_SHQ, likely because D_LDQ contains instruction-following-style data that D_SHQ lacks. This confound inflates the "average" scores for diverse SFT and deflates them for high-quality SFT, yet is not acknowledged. Reported averages mix reasoning gains with instruction-format gains.

3. **Single architecture for core findings.** All main experiments use one 8B hybrid Mamba-attention model. While a 1.2B Transformer experiment exists in appendix Table 14, the core findings—especially the asymmetric principle—rest on one configuration. Mamba's different inductive biases for sequential processing could interact with how reasoning patterns are learned during pretraining.

### Trivial
- D_ALF's answer-length threshold (>4096 tokens) as a proxy for reasoning complexity is crude, though it only affects one ablation (Table 8).

## Nice-to-Haves
- A controlled experiment disentangling diversity from repetition: subsample D_LDQ to 1.2M samples and pretrain under identical repetition as D_SHQ to cleanly test the diversity hypothesis.
- A fairer catch-up test: continued pretraining or extended SFT with a reasoning token budget comparable to the 80B used during pretraining.
- RL results for M_SHQ and M_LDQ to substantiate the "compounding" claim beyond a single pair.
- Data contamination analysis between D_LDQ (268M samples including math problems) and evaluation benchmarks (GSM8K, MATH-500).

## Removed Points
*These points are flagged to be removed, treat them with caution:*

- **Variance/error bars for pretraining runs**: The paper reports Pass@1 averages over 16 and 4 runs for evaluation benchmarks (Section 3.2). Running multiple full pretraining replicates at 8B/1T scale exceeds community norms for this type of work. Removed as not standard in the field.
- **Table 2 averaging obscures individual results**: The full breakdown is available in appendix Table 13. This is a presentation choice, not an error. Removed.
- **"Important and underexplored research question" as a strength**: Removed as a generic strength about problem importance rather than specific paper contribution.
- **D_ALF critique as a standalone weakness**: This dataset is only used in one ablation and is not central to the main claims. Demoted to trivial.

## Novel Insights
The latent effect of high-quality pretraining data is the paper's most genuinely novel contribution. The near-identical pretraining performance of M_LMQ and M_LDQ (64.07 vs 64.09) followed by a meaningful +4.25% post-SFT divergence suggests that pretraining can embed latent representational structure that only activates during alignment. This has practical implications: evaluating pretraining data choices solely by immediate benchmark performance may undervalue quality investments whose returns only materialize downstream. This finding is robust to the repetition confound since M_LMQ (269.2M samples) and M_LDQ (268M samples) have comparable data volumes and neither requires significant repetition.

## Suggestions
- **Design a repetition-controlled comparison**: Subsample D_LDQ to match D_SHQ's sample count (1.2M) and pretrain with identical repetition schedules. If the diverse-but-equally-repeated subset still outperforms D_SHQ, the diversity claim is clean.
- **Soften causal language throughout**: Replace "proves," "conclusive evidence," and "refutes" with "suggests," "provides evidence," and "challenges," matching the evidential strength of single-run experiments with known confounds.
- **Extend RL evaluation**: Include at least M_SHQ and M_LDQ + SFT_SHQ + RL to show the pretraining advantage generalizes beyond the extreme comparison.
- **Discuss the IFEval confound explicitly**: Note that IFEval gains for D_LDQ-based SFT likely reflect instruction-format data presence rather than reasoning improvement, and consider reporting reasoning-only averages separately.
- **Reconcile the formalization with the experimental design**: Either remove the budget constraint formalization (Equation 2) or add an experiment that genuinely shifts reasoning tokens between PT and SFT under a fixed total budget.

## Score and Decision

### Calibration Anchors

| Paper | Path | Avg Score | Round | Comparison |
|-------|------|-----------|-------|------------|
| "Systematic Review of LLMs" | 8QTpYC4smR | 1.00 | R1 | Not a research paper; far below |
| "NEMESIS: Jailbreaking LLMs" | 5kMwiMnUip | 1.40 | R1 | Narrow and weak; far below |
| "Cross-Lingual Humanoid Robots" | gwZ90hFSL2 | 1.00 | R1 | Not relevant; far below |
| "Financial Markets Neural Network" | nSDOkm0SKo | 1.00 | R1 | Not relevant; far below |
| "Self-Consuming Training Loop" | SaOxhcDCM3 | 3.20 | R1 | More limited scope; paper under review is stronger |
| "Guardrail Pipeline" | KjxZ4BdUdN | 3.00 | R1 | Different topic, weaker; paper under review is stronger |
| "Re-TASK Framework" | dp1BH2bK4Y | 3.00 | R1 | Different topic, less empirical; paper under review is stronger |
| "Efficiently Deploying LLMs" | BjZP3fTlVg | 3.00 | R1 | Different topic; paper under review is stronger |
| "Pre-Memorization Train Accuracy" | OegBJMucyM | 4.25 | R1 | Different topic; paper under review has larger scale but comparable issues |
| "LokiLM Technical Report" | bppG9srkpR | 3.60 | R1 | Not a proper paper; far below |
| "Post-training Study (Finance)" | EVa5OIYBoG | 3.67 | R1 | Similar topic but narrower and less novel; paper under review is stronger |
| "Amuro & Char: PT vs FT" | 8uXkyWFVum | 4.20 | R1 | Very similar topic, smaller scale (1B), less comprehensive; paper under review is clearly stronger |
| "At Which Stage Does Code Data Help" | KIPJKST4gw | 7.25 | R1 | Very similar question, accepted; cleaner design despite smaller scale; paper under review is weaker due to confound |
| "Pretraining Data for LLM Reasoning" | 1hQKHHUsMx | 6.75 | R1 | Similar topic, accepted; paper under review has larger experiments but more confounds |
| "Multilingual Reasoning Data Proportions" | S6cBH99BhB | 6.50 | R1 | Related topic; paper under review has larger scope but weaker methodology |
| "Advancing Math Reasoning" | GtpubstM1D | 5.71 | R1 | Very similar topic; comparable quality—both have useful findings and methodological concerns |
| "Training on Test Task" | jOmk0uS1hl | 8.00 | R1 | Stronger methodology and cleaner claims; clearly above |
| "Combatting Dimensional Collapse" | f4gF6AIHRy | 8.00 | R1 | Stronger methodology; clearly above |
| "Synthetic Continued Pretraining" | 07yvxWDSla | 8.00 | R1 | Stronger methodology and novel algorithm; clearly above |
| "Knowledge Card" | WbWtOYIzIK | 8.00 | R1 | Different topic, stronger contribution; clearly above |

**Round 1 bracket: 5.0 to 6.5**

The paper is clearly stronger than rejected papers in the 3-4.5 range (Amuro & Char at 4.20, Post-training Finance at 3.67) due to its larger computational scale and more actionable findings. It is comparable to GtpubstM1D (5.71), which also studies pretraining vs. post-training allocation with useful but imperfect methodology. However, it falls below KIPJKST4gw (7.25), which asked a very similar question ("at which training stage?") with a cleaner experimental design and fewer confounds despite smaller scale. The data repetition confound on a headline claim, pervasive overclaiming, and thin RL evidence prevent the paper from reaching the 6.5+ range of accepted papers with similar scope.

**Final calibrated score: 5.5**

The paper makes a genuine and rare computational investment in an important question, yielding several useful findings (front-loading advantage, latent effect, SFT quality dominance). However, the data repetition confound undermining the diversity-vs-quality headline claim is a structural experimental design issue that cannot be resolved by textual revision—it requires new experiments. Combined with pervasive overclaiming ("proves," "refutes," "conclusive") and RL evidence limited to a single extreme comparison, the paper's strongest claims outrun its evidence. The directional findings are likely correct and useful, but the gap between what is claimed and what is demonstrated is too large for acceptance in its current form.

MY FINAL SCORE: <score>5.5</score>
MY FINAL DECISION: <decision>Reject</decision>