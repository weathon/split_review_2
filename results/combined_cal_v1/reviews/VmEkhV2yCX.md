I have all the information I need. Let me compose the final consolidated review.

## Summary

This paper conducts the first systematic empirical study of how reasoning data (QA-formatted, SFT-style data) affects LLM performance when introduced at different training stages. The authors train 8B-parameter models from scratch for 1T tokens across four pretraining conditions (baseline without reasoning data, small high-quality, large diverse, and mixed) and three SFT conditions, plus RL. The central finding is an asymmetric allocation principle: pretraining benefits most from diverse, large-scale reasoning data, while SFT is dominated by data quality. The paper provides evidence that front-loading reasoning data into pretraining creates durable advantages that persist through SFT and RL, and that the baseline cannot "catch up" even with doubled SFT epochs.

## Strengths

- **Large-scale controlled study at significant computational cost.** Training 8B models from scratch for 1T tokens across multiple conditions (4 pretraining variants × 3 SFT conditions, plus scaling ablations and RL) goes well beyond the typical practice of studying data effects only at the post-training stage. The scale of this effort alone makes it a valuable contribution.

- **The asymmetric finding (diversity in pretraining, quality in SFT) is practically actionable and non-obvious.** The paper provides an explicit heuristic — "prioritize diversity in pretraining, quality in SFT" — that is supported by multiple comparisons and could directly inform data allocation decisions in production pipelines. The contrast between Table 1 (where M_LDQ at 64.09 far exceeds M_SHQ at 54.98 in pretraining) and Table 5 (where SFT_SHQ dominates SFT_LDQ after fine-tuning) cleanly illustrates the asymmetry.

- **The catch-up experiment is well-controlled and informative.** Table 4 shows that doubling SFT epochs on the baseline (M_base + SFT_SHQ 2× epochs: 34.01) still cannot match even the weakest reasoning-pretrained model (M_SHQ + SFT_SHQ: 37.33). This directly addresses a central debate in the field and provides the cleanest evidence in the paper.

- **Well-framed research questions.** The four questions in Section 1 (catch-up, overfitting, diversity vs. quality, complexity during pretraining) cleanly articulate gaps in the current literature and directly motivate the experimental design.

- **The scaling and ratio sensitivity experiments (Tables 6, 7) add depth.** The finding that increasing the reasoning ratio from 20% to 40% during pretraining improves reasoning benchmarks while modestly reducing instruction-following metrics provides useful nuance about the trade-offs involved.

## Weaknesses

### Fatal
None.

### Major

1. **Data repetition confounds the diversity/quality comparison in pretraining.** To reach the fixed 80B reasoning token budget, D_SHQ (1.2M samples) must be repeated thousands of times while D_LDQ (268M samples) is used roughly once (Section 2.3: "When a reasoning dataset is small, it is repeated so that the model still observes the same total volume of reasoning tokens"). The paper attributes the large gap between M_SHQ (54.98) and M_LDQ (64.09) — a 22.96-point difference in MATH_PT AVG — to "scale and diversity," but extreme repetition could introduce overfitting, memorization artifacts, or saturation effects that independently suppress M_SHQ's performance. Without a control that varies the repetition ratio independently of dataset content, the diversity explanation is confounded. **This is the most significant methodological concern in the paper.**

2. **The RL evidence for the paper's strongest claim is limited to a single comparison.** Table 3 reports only M_base + SFT_SHQ + RL vs. M_LMQ + SFT_SHQ + RL — described as "our two extreme pretraining backbones." The paper states that "pretraining strategy dictates final accuracy on expert-level tasks" and that gains "compound through RL," but this rests on one data point. Other intermediate conditions (e.g., M_LDQ + SFT_SHQ + RL, M_SHQ + SFT_SHQ + RL) are not evaluated under RL, so it is unclear whether the pattern is monotonic or specific to the extreme comparison. This weakens the paper's strongest causal claim.

### Minor

3. **The "latent effect" claim relies on a confounded comparison.** M_LMQ (269.2M samples = D_LDQ ∪ D_SHQ) outperforms M_LDQ (268M samples) by +4.25% after SFT (Table 4: 50.95 vs. 46.70). The paper attributes this to "high-quality pretraining data having latent effects, activated only after SFT." However, the improvement could also come from the 1.2M additional training samples (even a marginal quantity increase of 0.4%) or from the different domain composition of D_SHQ (71% math vs. 56% in D_LDQ). The evidence supports a correlation but not the specific causal mechanism claimed.

4. **The "naive scaling is harmful" claim is based on a single data point.** Table 8 shows M_LDQ + SFT_2×LDQ drops math performance by 4.92% relative to M_LDQ + SFT_LDQ. The paper frames this as a general principle ("naively scaling SFT data can be detrimental"), but it tests only one base model (M_LDQ) with one scaling strategy. It is unclear whether the harm generalizes across different base models or scaling regimes.

5. **The baseline model's pretraining corpus already contains math and code data.** D_base is described as containing "mathematics, and code sources" (Section 2.2). The paper's framing of "reasoning data vs. no reasoning data" in pretraining masks that the actual comparison is between QA-formatted reasoning data and the same domains in raw-text format. This does not invalidate the results but the framing could be more precise about what distinguishes D_res from D_base beyond the format.

6. **The optimization framing (Eq. 2) does not match the experimental design.** The paper sets up a budget-constrained optimization problem (B = |D_res^PT| + |D_res^SFT|) but never varies the split ratio between pretraining and SFT reasoning data. The experiments use fixed budgets (80B reasoning tokens in pretraining, 4.8M samples in SFT) with no experiment testing the trade-off between the two phases. The formalization is conceptually useful but not operationalized.

### Trivial

7. **No uncertainty quantification.** None of the tables report standard errors, confidence intervals, or significance tests. While single-run large-scale training is the norm for this type of work, it limits the ability to assess whether fine-grained differences (e.g., the +4.25% "latent" gain) are reliable.

## Nice-to-Haves

- Run a control experiment that varies the repetition ratio (or reduces the token budget for D_SHQ) to disentangle data diversity from repetition effects.
- Add at least 2-3 more RL comparisons (e.g., M_LDQ + SFT_SHQ + RL, M_SHQ + SFT_SHQ + RL) to test whether the RL advantage is monotonic across pretraining conditions.
- For the latent effect, add a control: compare adding 1.2M random samples from D_LDQ to D_LDQ vs. adding 1.2M samples from D_SHQ.
- Acknowledge that D_base contains math/code content in the paper's framing, and clarify that the comparison is about QA-formatted reasoning data vs. raw text in the same domains, not "reasoning vs. no reasoning."

## Removed Points

These points are flagged to be removed, treat them with caution:

- **"Evaluation metrics shift between phases, making headline percentages misleading"** — REMOVED. The paper explicitly explains the different metric sets in Section 3.2: "To evaluate the reasoning ability of different SFT models, we focus on reasoning centric benchmarks unlike in base model evaluations." This is by design and transparently communicated.

- **"The paper never explains why the same benchmarks are not used across both phases"** — REMOVED. The paper does explain this in Section 3.2, as noted above.

- **"The GPR/INS results undermine the narrative"** — REMOVED. This claim is factually incorrect. In Table 4, MATH gains from M_base + SFT_SHQ (42.79) to M_LMQ + SFT_SHQ (64.67) are +21.88, exceeding INS gains from 30.59 to 49.82 (+19.23). The largest relative gains are in MATH and CODE, not INS.

- **"No statistical significance or variance information"** — Demoted to Trivial (the reviewer called it a "serious gap"). Single-run large-scale pretraining papers rarely report uncertainty quantification; it is a nice-to-have, not a fatal omission.

- **"The D_ALF experiment is under-analyzed"** — REMOVED. The ALF ablation serves its purpose as a targeted experiment on reasoning complexity. Deeper analysis would be a useful extension but the current treatment is adequate for an ablation.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. Add a control experiment that decouples data repetition from data content to address the most significant confound. For example, train M_SHQ on a reduced token budget (fewer repetitions) to see if the gap to M_LDQ narrows.
2. Evaluate at least 2-3 additional pretraining backbones under RL to strengthen the "compounding returns" claim.
3. Add a control for the latent effect experiment: compare adding 1.2M random D_LDQ samples to D_LDQ vs. adding 1.2M D_SHQ samples.
4. Soften causal language around the "latent effect" and "naive scaling is harmful" claims, or add experiments that directly test the proposed mechanisms.
5. Clarify the framing in the introduction to acknowledge that the baseline does see math/code tokens in raw-text format, and that the intervention is about QA-formatted reasoning data specifically.

## Score and Decision

**Bracket determination (Round 1):** I compared this paper against four anchors: GtpubstM1D (5.71, on mathematical reasoning data across training stages), 8uXkyWFVum (4.20, on pre-training/fine-tuning relationships), 1hQKHHUsMx (6.75, on pretraining data influence in reasoning), and 5HCnKDeTws (6.75, on scaling in finetuning). The paper under review is clearly stronger than 8uXkyWFVum (4.20) — that paper used only a 1B model and its conclusions were limited. The paper is comparable to GtpubstM1D (5.71) but has broader domain coverage (math, science, code vs. math only) and cleaner experimental design, though GtpubstM1D's model release adds value. The paper is in a similar tier to 1hQKHHUsMx (6.75) and 5HCnKDeTws (6.75) in terms of experimental rigor and practical significance, though it carries more methodological confounds than those works. Initial bracket: **5.5–7.0**.

**Narrowing:** The paper's strongest weighted items (catch-up experiment at +5.44, large-scale study at +5.13, asymmetric finding at +4.89) compare favorably to the top-weighted items in the 6.0–7.0 anchors. Its main negative items (limited RL evidence at -4.48, naive scaling overclaim at -4.92) are moderate concerns that weigh against an "accept" level (8.0+) but don't pull it below the 6.0 threshold. The data repetition confound at -1.14 is a genuine concern but not fatal.

**Final score: 6.5** — a borderline accept / solid accept. The paper's core findings (asymmetric allocation principle, front-loading advantage) are important, novel, and practically useful. The data repetition confound is the most significant issue, but it is addressable and does not undermine the main directional finding. The paper would benefit from additional RL comparisons and more tempered causal claims, but its contribution is clear and its empirical scope is impressive.

MY FINAL SCORE: <score>6.5</score>
MY FINAL DECISION: <decision>Accept</decision>