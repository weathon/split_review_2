Now I have sufficient calibration information. Let me compile the final review.

**Bracket from Round 1:** The paper sits above the 4.20-5.71 band (Amuro and Char, Advancing Mathematical Reasoning) in scope and novelty, but below the 7.00-7.25 band (Smaller/Weaker/Better, At Which Training Stage) due to addressable overclaiming and the confound issue. This places it in the 5.5-7.0 range.

**Round 2 narrowing:** Comparing weighted items against the closest anchor "At Which Training Stage Does Code Data Help LLMs Reasoning?" (7.25): that paper's strengths peak at weight 10.39 (comparable to our paper's 10.43) and its most damaging weakness is weight -1.26 (a reviewer's point about a confound). Our paper's most damaging criticisms (2.40, 2.63 for the major weaknesses) are more damaging, but our paper also has stronger scope (full pretraining from scratch at 8B scale, three training stages, multiple data dimensions). The paper under review sits slightly below 7.25, around 6.0, given the overclaiming and the confound that needs resolution.

Let me finalize at **6.0** — borderline accept.

Now let me produce the final review in the specified format.

Here are the anchor papers used across rounds:

**Round 1:**
1. `/home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/8QTpYC4smR.md` - avg 1.00 - Survey paper, not comparable
2. `/home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/SaOxhcDCM3.md` - avg 3.20 - Self-consuming training loop, not directly comparable
3. `/home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/506Sxc0Adp.md` - avg 4.00 - Diversity coefficient paper, somewhat comparable on data quality
4. `/home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/GtpubstM1D.md` - avg 5.71 - Advancing Mathematical Reasoning [itemized] - Most comparable on topic but less scope
5. `/home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/1hQKHHUsMx.md` - avg 6.75 - What Kind of Pretraining Data [itemized] - Related but different methodology
6. `/home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/f4gF6AIHRy.md` - avg 8.00 - Combatting Dimensional Collapse - Higher quality but different focus

**Round 1 (continued):**
- `/home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/8uXkyWFVum.md` - avg 4.20 - Amuro and Char [itemized] - Less scope, 1B model
- `/home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/cijO0f8u35.md` - avg 5.25 - Scaling Relationship [itemized] - Narrower focus

**Round 2:**
- `/home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/KIPJKST4gw.md` - avg 7.25 - At Which Training Stage Does Code Data Help [itemized] - Most structurally similar in research question
- `/home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/3OyaXFQuDl.md` - avg 7.00 - Smaller, Weaker, Yet Better [itemized] - Data strategy for reasoning
- `/home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/UNxCphTxWp.md` - avg 6.00 - Programming Every Example
- `/home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/oqsQbn4XfT.md` - avg 5.80 - On the Diversity of Synthetic Data

Now let me produce the final review.## Summary

This paper presents a systematic study of how reasoning data (varying in scale, diversity, and quality) affects LLM performance when introduced at different training stages — pretraining, SFT, and RL. The authors train 8B hybrid Mamba2+Attention models from scratch for 1T tokens across multiple data conditions, tracing effects through all three stages. Key findings include: (1) front-loading reasoning data into pretraining creates durable advantages over later injection, (2) an asymmetric allocation principle where diversity drives pretraining effectiveness while quality governs SFT, (3) a "latent effect" where high-quality pretraining data shows gains only after SFT, and (4) naive SFT scaling with mixed-quality data harms math reasoning.

## Strengths

- **Fully-crossed experimental design across the entire training pipeline (pretraining → SFT → RL).** Unlike prior work that studies reasoning data only in post-training, this paper traces the effect of reasoning data injection through all three stages by training 4 pretrained variants × multiple SFT recipes × RL for key comparisons (Section 2.3, Tables 1-8). This allows testing whether early advantages persist, amplify, or wash out — a level of experimental control rare in the literature given the compute investment (1T tokens, 8B model from scratch).

- **The asymmetric allocation finding (diversity drives pretraining, quality drives SFT) is novel and practically actionable.** This result is empirically well-motivated by the comparison between Tables 4 and 5, where the rank ordering of data properties flips across phases. It provides a clear, actionable blueprint for data strategy that is more nuanced than simplistic "more is better" approaches.

- **Counterintuitive results that challenge conventional wisdom.** (a) Naive SFT scaling harms math reasoning (Table 8: −5% in MATH when doubling mixed-quality SFT data). (b) The "latent effect" where ℳ_LMQ and ℳ_LDQ are nearly tied at pretraining (64.07 vs 64.09) but diverge +4.25% after SFT (Table 4). These are genuinely interesting, non-obvious findings that would be worth publishing even if the headline claims were weaker.

- **Systematic large-scale pretraining with controlled token budgets.** The paper controls for total reasoning tokens (80B) across all conditions and varies reasoning proportion (10%, 20%, 40%) to test sensitivity (Table 6). The use of a 1.2B transformer as an architecture check further strengthens the robustness of the approach.

## Weaknesses

### Fatal
None.

### Major

- **The diversity vs. quality comparison in pretraining is confounded with data repetition.** The key comparison underlying the diversity claim — 𝒟_SHQ (1.2M samples, high-quality, narrow) vs. 𝒟_LDQ (268M samples, lower quality, broad) — differs along three axes simultaneously: diversity, quality, and repetition frequency. As the paper states, "When a reasoning dataset is small, it is repeated so that the model still observes the same total volume of reasoning tokens" (line 93). To reach the 80B reasoning token budget, 𝒟_SHQ is repeated ~200× while 𝒟_LDQ is seen once. The claimed diversity advantage (+9.09% in Table 1, "11% average gain" in abstract) could partly reflect detrimental effects of extreme repetition (overfitting, loss of training signal diversity) rather than diversity per se. A controlled experiment subsampling 𝒟_LDQ to match 𝒟_SHQ's size would be needed to decouple these factors. This does not invalidate the paper's broader findings about front-loading being beneficial, but it weakens the specific claim about *which property* of pretraining data drives the gain.

- **The "catch-up" hypothesis is tested too narrowly to support the strong conclusion drawn.** The paper claims that "SFT cannot compensate for a weak foundation" (line 37) and that the catch-up hypothesis is "prove[n]... false" (line 213). The evidence comes from a single intervention: doubling SFT epochs for ℳ_base on 𝒟_SHQ (Table 4), which improves the baseline by 4.09% but still falls short of ℳ_SHQ+SFT_SHQ by 3.32%. A meaningful catch-up test would explore other plausible intensifications: more SFT data, different SFT recipes, per-model hyperparameter tuning, or longer training. The claim that SFT *categorically* cannot compensate for weak pretraining goes beyond what a single intervention can demonstrate. The paper's own contribution does not depend on this being a universal impossibility — it only needs to show the gap is large and not trivially closed.

### Minor

- **The "19% average gain" headline is imprecisely reported.** The abstract says "front-loading reasoning data into pretraining is critical (19% average gain)." Tracing this to Table 3: ℳ_base+SFT_SHQ+RL = 37.92, ℳ_LMQ+SFT_SHQ+RL = 56.66, giving 18.74 **absolute percentage points** (~49% relative) from one specific pipeline configuration. The paper should clearly distinguish absolute vs. relative gains and specify which comparison produces this figure, rather than presenting it as a general result of front-loading.

- **"Front-loading" overstates the timing of reasoning data injection.** Reasoning data is introduced at token 600B out of 1T (line 93), i.e., in the last 40% of pretraining after 600B tokens of pure base corpus. While the paper describes this schedule, the "front-loading" rhetoric in the abstract and introduction implies introduction from the start of pretraining. A more precise description would be "mid-training injection" or "early-in-pipeline injection."

- **The answer-length proxy for data quality (𝒟_ALF) uses an unvalidated heuristic.** The dataset filters for answers exceeding 4096 tokens (line 87) on the principle that longer responses imply more complex CoT reasoning. This heuristic is reasonable but unvalidated — longer answers could reflect verbosity, repetition, or irrelevant content rather than genuine reasoning depth. The paper should acknowledge this limitation explicitly.

- **Base model evaluations (Table 1) report single numbers without variance information.** Given n=1 per pretraining condition due to computational cost, the robustness of some tight comparisons (e.g., ℳ_LDQ vs ℳ_LMQ at 64.07 vs 64.09) is uncertain. This should be acknowledged as a limitation.

### Trivial
None.

## Nice-to-Haves

- A controlled experiment subsampling 𝒟_LDQ to match 𝒟_SHQ's size (~1.2M), controlling for repetition frequency, would cleanly decouple diversity from repetition.
- A brief discussion of data contamination risk for widely-used evaluation benchmarks (GSM8K, MATH, MMLU, HumanEval) would strengthen the paper.
- A rough estimate of total compute (GPU-hours or FLOPs) would help readers assess feasibility.

## Removed Points

These points are flagged to be removed; treat them with caution:
- Criticism about the 1.2B transformer experiment being unverifiable due to missing appendix: Removed per hard rule — appendix content is stripped by the parser and exists in the original submission. The paper explicitly states these results are in Table 14.
- Criticism about data contamination not being discussed: Removed — this is a constructive suggestion, not a weakness that undermines the paper's claims.
- Criticism about no compute budget discussion: Removed — this is a minor suggestion, not a core weakness.
- "Variance across ℳ_res models" criticism: Removed — the paper defines ℳ_res as an average (line 102) and reports individual model scores in all tables, allowing readers to see the spread (e.g., Table 1: SHQ=54.98, LDQ=64.09, LMQ=64.07).
- The harsh critic's proposed ideal experiment (subsampling 𝒟_LDQ): This is a constructive suggestion already subsumed by the first Major weakness above. It does not need to be listed separately.

## Novel Insights

None beyond the paper's own contributions. The reviews converge on the paper's genuine strengths (experimental scope, asymmetric allocation finding, counterintuitive results) while identifying real but addressable overclaiming issues. The key insight from the review process is that the paper's core findings are supported by the data but would be strengthened by more careful calibration of claims to evidence, particularly around the diversity/repetition confound and the catch-up hypothesis.

## Suggestions

1. **Decouple diversity from repetition:** Conduct a controlled experiment subsampling 𝒟_LDQ to match 𝒟_SHQ's size, controlling for repetition frequency. If the diversity advantage persists, the claim is vastly stronger. If it disappears, the paper's main finding was about repetition effects rather than diversity.
2. **Calibrate the catch-up claim:** Replace "SFT cannot compensate for a weak foundation" with "the specific SFT intensification tested (2× epochs on the same data) cannot close this gap." The paper's contribution does not require a universal impossibility claim.
3. **Report gains precisely:** Distinguish absolute percentage points from relative improvements (e.g., "18.7 percentage points, corresponding to ~49% relative improvement").
4. **Clarify timing terminology:** Replace "front-loading" with more precise phrasing like "early-in-pipeline injection" or "pretraining-stage injection" to avoid implying training from token 1.
5. **Acknowledge the answer-length heuristic limitation** and discuss potential confounds.

## Score and Decision

### Calibration Anchors

**Round 1 (Bracketing):**
| Anchor | Path | Avg Score | Itemized | Comparison |
|--------|------|-----------|----------|------------|
| Survey paper | 8QTpYC4smR.md | 1.00 | No | Not comparable (general survey) |
| Self-consuming loop | SaOxhcDCM3.md | 3.20 | No | Different topic |
| Diversity coefficient | 506Sxc0Adp.md | 4.00 | No | Somewhat comparable on data quality framing |
| Amuro and Char | 8uXkyWFVum.md | 4.20 | Yes | Less scope (1B model, continued PT only); current paper stronger |
| Scaling Relationship | cijO0f8u35.md | 5.25 | Yes | Narrower (GSM8K only); current paper broader and more novel |
| Advancing Math Reasoning | GtpubstM1D.md | 5.71 | Yes | Most similar topic but does CPT not full PT; split reviews |
| On Diversity of Synthetic Data | oqsQbn4XfT.md | 5.80 | No | Related data diversity topic; current paper has stronger experiments |
| What Kind of Pretraining Data | 1hQKHHUsMx.md | 6.75 | Yes | Different methodology (influence functions); current paper does direct training |
| Combatting Dimensional Collapse | f4gF6AIHRy.md | 8.00 | No | Cleaner paper but different focus |

**Round 2 (Narrowing):**
| Anchor | Path | Avg Score | Itemized | Comparison |
|--------|------|-----------|----------|------------|
| Programming Every Example | UNxCphTxWp.md | 6.00 | No | Different approach to data quality |
| RLSF | vf8iou7FNF.md | 5.75 | No | RL-focused, different contribution |
| Smaller, Weaker, Yet Better | 3OyaXFQuDl.md | 7.00 | Yes | Cleaner experiments but narrower scope; current paper broader |
| **At Which Training Stage Does Code Data Help** | KIPJKST4gw.md | **7.25** | **Yes** | **Most structurally similar RQ (at which stage does X data help); the current paper has stronger scope (full PT, 8B, 3 stages) but the anchor has fewer overclaiming issues** |
| Predicting Emergent Abilities | lDbjooxLkD.md | 6.00 | No | Different focus |

**Weighted-item comparison:** The current paper's strengths (peak weight 10.43 for experimental scope) are on par with the strongest anchors (peak 10.39 for "At Which Training Stage"). However, the current paper's major weaknesses have weights 2.40 and 2.63 — more damaging than the most damaging weakness in "At Which Training Stage" (weight -1.26 for a reviewer's confound concern, which was a single reviewer's point that others did not echo). The current paper's weaknesses are more broadly agreed upon. This places the paper slightly below the 7.25 anchor.

### Final Score and Decision

**Bracket from Round 1:** 5.5–7.0 (above Amuro and Char at 4.20 and Scaling Relationship at 5.25; clearly below the 7.00–8.00 band).

**Round 2 narrowing:** Comparison with "At Which Training Stage Does Code Data Help" (7.25) confirms the paper sits below this level due to the confound and overclaiming issues, but above the 5.71 anchor (Advancing Mathematical Reasoning) due to broader scope (full pretraining vs. CPT, 3 training stages vs. 2, more novel findings). This yields a final score of **6.0**.

This paper presents genuinely impressive experimental scope and interesting findings that challenge conventional wisdom. The core contributions — the asymmetric allocation principle, the latent effect of high-quality pretraining data, and the finding that naive SFT scaling harms math reasoning — are well-supported by the data and practically valuable. However, the paper systematically overclaims relative to its evidence: the diversity claim is confounded with data repetition, and the catch-up claim rests on a single intervention tested too narrowly. These are addressable in revision and do not threaten the paper's core findings, but they prevent the paper from achieving the highest tier at this stage.

MY FINAL SCORE: <score>6.0</score>
MY FINAL DECISION: <decision>Borderline Accept</decision>