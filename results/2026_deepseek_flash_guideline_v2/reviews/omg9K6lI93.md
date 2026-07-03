Now I have a thorough understanding of the paper. Let me write the final consolidated review.

## Summary

This paper investigates whether translating LLM benchmark data into Arabic "masks" data contamination — making it harder to detect via standard English-only evaluation while models still benefit from the exposed data. The authors fine-tune four open-weight models on English test items combined with varying proportions (0%, 10%, 50%, 100%) of Arabic-translated versions of those same test items, then evaluate on English benchmarks. They extend TS-Guessing with a choice-reordering strategy (index-recall rate / IDR metric) to probe memorization, and propose a Translation-Aware Contamination Detection (TACD) framework as a non-implemented blueprint.

## Strengths

- **First systematic study of translation as a contamination mask in a multilingual context.** The paper identifies a genuine blind spot: prior contamination detection research focuses overwhelmingly on English, and the question of whether multilingual translation obscures contamination signals is timely and practically significant. The core observation — that TS-Guessing detects memorization signals (e.g., IDR of 0.643 for LLaMA at 50% contamination) even when English evaluation scores change relatively little — is concrete and relevant.

- **Methodological extension of TS-Guessing with choice-reordering.** The choice-reordering strategy and the Index-recall rate (IDR) metric (Section 3.3–3.4) are concrete, reusable contributions for contamination detection in any multiple-choice benchmark, not just Arabic. The idea of measuring whether the model reproduces the pre-shuffle answer letter after re-ordering is a stronger contamination signal than content-based overlap alone.

- **Well-controlled experimental design.** The setup systematically varies four models (1B–7B scale), three datasets (MMLU, XQuAD, MLQA), and four contamination proportions with identical LoRA/PEFT hyperparameters, optimizer, and batch policy. This enables attribution of observed effects to contamination rather than confounds and allows cross-comparison across task formats.

- **Honest framing of TACD.** The paper explicitly acknowledges the proposed framework is "a forward-looking blueprint rather than a complete implementation" and discusses its resource requirements and the noise introduced by translation (Section 5.3). This candor separates the paper's self-contained empirical contribution from its aspirational proposal.

- **Nuanced non-monotonic findings in extractive QA.** The "peak-at-10%" pattern in MLQA (Section 4.1) is a non-trivial observation: small amounts of cross-lingual overlap can aid surface-form familiarity, but heavier contamination overfits to distributional quirks that do not transfer well. This goes beyond the simplistic "more contamination = better score" narrative.

## Weaknesses

### Fatal
None.

### Major

1. **The p=0 baseline already includes direct English test items, so the experiment never measures against a truly clean condition.** The training set is D_train^d(p) = D_EN^d ∪ D_AR^d(p), where D_EN^d is explicitly described as "MMLU: English test items formatted as MCQ" and "XQuAD/MLQA: English QA" (Section 3.1, lines 130–142). Every condition — including p=0 — fine-tunes directly on the English test data. The comparison is therefore "model contaminated with English test items" vs. "model additionally exposed to Arabic translations of the same items." The paper's motivating question — whether translation can act as a "natural barrier" to contamination — cannot be properly answered without a condition that has no test-set exposure at all. This limits the interpretability of the paper's central claims about "concealment."

2. **The claim of "approximately equal performance" across contamination levels (Section 4.2) is contradicted by the paper's own Table 2.** The paper states that "models exhibit approximately equal performance on all evaluated benchmarks" for p ∈ {10,50,100}%, but Table 2 shows clear, often large, changes. Examples from p=10 to p=100: Mistral MMLU 0.580→0.690 (+19%); LLaMA MMLU 0.381→0.431 (+13%); Mistral XQuAD 0.455→0.114 (collapse); LLaMA XQuAD 0.459→0.569 (+24%). These are not "approximately equal." The paper's central interpretive claim about "masking" is based on a factual inaccuracy about its own data.

3. **Missing same-language control condition.** The paper's narrative that *translation specifically* conceals contamination requires a control where additional data is provided in English (e.g., paraphrased versions of test items) at the same proportions. Without this, the observed patterns across p could be attributed to data quality differences, models' weaker Arabic capabilities, or simple diminishing returns from adding more data on top of already-saturated English contamination. The paper cannot distinguish the claim "translation masks contamination" from the claim "any additional semantically related data yields small, inconsistent improvements on top of direct English contamination."

4. **The TS-Guessing evidence is inconsistent and does not clearly support the concealment narrative.** Across MMLU (IDR), results are erratic: Gemma drops from 0.350→0.029→0.005 as contamination increases; LLaMA jumps 0.287→0.643→0.410 (non-monotonic); Mistral is near zero throughout (Table 3a). For XQuAD, EM and RL-F1 are negligible for all models (<0.02 for three of four models). The paper interprets these as supporting translation's "masking" effect, but an equally plausible reading is that the probe is not reliably detecting memorization in this setting. The paper does not address why probe scores collapse or are near zero for most models while still claiming they support its central claim.

### Minor

5. **No variance or statistical significance reported.** Tables 2 and 3 present single-run point estimates without error bars, confidence intervals, or significance tests. With only one seed per condition, it is impossible to assess whether any observed difference (e.g., Mistral MMLU 0.580→0.690) is reliable.

6. **Arabic proficiency is claimed as a factor but never measured.** The abstract and conclusion state that models with "stronger Arabic capabilities" benefit more from Arabic-translated contamination, but no Arabic proficiency evaluation is conducted. This claim is unsupported by the evidence presented.

7. **Fine-tuning on test data vs. naturalistic pretraining contamination is not discussed.** The paper fine-tunes directly on test items — a much stronger and more direct form of exposure than the incidental overlap that occurs during web-scale pretraining. Whether the findings generalize to real-world contamination scenarios is unclear and the paper does not address this distinction.

### Trivial
None.

## Nice-to-Haves
- A truly clean baseline (no English or Arabic test data in training) would directly test whether translation masks contamination relative to a clean state.
- An English-paraphrase control condition would isolate whether any masking effect is translation-specific or general to surface-form variation.
- Variance estimates (multiple seeds or bootstrapping) would strengthen claims about trends.
- Arabic proficiency measurements would support the claim about Arabic capability correlating with contamination effects.

## Removed Points
These points from the inputs were filtered and moved here:
- "The paper does not cite or compare against any existing work on multilingual contamination" — removed per the rule that missing related works cannot be confirmed without external sources.
- "Section 2 is too long" — removed as a formatting/style observation with no substantive content.
- "Table 1 reporting Min-K% Prob results with no indication of whether these are the authors' own calculations" — removed as a minor reproducibility concern not central to the paper's claims.
- Critic's claim that the paper "downplays" erratic XQuAD/MLQA patterns — the paper's Section 4.1 discusses these patterns in detail; the criticism is inaccurate.
- Strength Finder's claim that "English evaluation scores remain stable" — this overstates the flatness and conflicts with verified weaknesses showing MMLU increases; removed as unsupported.

## Novel Insights
The harsh critic's most penetrating observation is that the experimental design never establishes a clean baseline, which means the paper's central claim about translation "concealing" contamination is grounded in a comparison between "English-contaminated" and "English+Arabic-contaminated" models rather than between "clean" and "contaminated-via-translation" models. This is a genuine structural limitation that careful readers should attend to. However, this is a limitation that a competent reviewer would identify from the paper itself; it is not a discovery that emerges uniquely from the reviews.

## Suggestions

- **Redesign the experiment with a truly clean baseline.** Train a model without any test-set exposure (neither English nor Arabic) as p=0, then compare against conditions with only Arabic-translated test items. This would directly test whether translation masks contamination relative to a clean state.
- **Add an English-paraphrase control condition** at the same proportions to isolate whether any masking effect is specific to translation or general to surface-form variation.
- **Correct the "approximately equal performance" claim** (Section 4.2) to accurately reflect the patterns in Table 2. Clearly acknowledge which benchmarks show changes and which do not.
- **Report variance estimates** (e.g., 3 seeds with error bars) to establish reliability of trends.
- **Qualify the TS-Guessing interpretation** to honestly reflect that most probe scores are near zero or erratic, and discuss the possibility that the probe is insensitive in this setting rather than assuming the results support concealment.
- **Evaluate Arabic proficiency** of all models or remove the claim that stronger Arabic capabilities lead to greater contamination benefits.

## Score and Decision

Given the constraints with the calibration tool, I reason as follows. The paper tackles a genuinely important and underexplored problem — multilingual contamination detection — and contributes a useful methodological extension (IDR metric). These are real strengths. However, the experimental design has a structural limitation (no clean baseline), the paper's central interpretive claim ("approximately equal performance") contradicts its own data, the TS-Guessing evidence is inconsistent, and the missing same-language control prevents attribution of effects to translation specifically. Collectively, these weaknesses mean the empirical contribution does not anchor the headline claims. The paper reads more like a promising research direction with preliminary findings than a completed empirical study that supports its conclusions. On the ICLR scale, this falls in the borderline reject range: the idea and framing have merit, but the evidence as presented does not convincingly support the claims.

MY FINAL SCORE: <score>4.0</score>
MY FINAL DECISION: <decision>Reject</decision>