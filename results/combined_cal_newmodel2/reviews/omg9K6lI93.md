Now let me construct the final review.

## Summary

This paper investigates whether translating benchmarks into Arabic can create a blind spot for data contamination detection. The authors fine-tune four open-weight LLMs on mixtures of English and Arabic-translated benchmark data (MMLU, XQuAD, MLQA) at varying contamination proportions, evaluate on English originals, and use a TS-Guessing probe to detect memorization. They find that MMLU accuracy increases with contamination while the TS-Guessing probe shows flat results, which they interpret as translation masking contamination. They also propose a TACD framework.

## Strengths

- **The research question is well-motivated and addresses a genuine gap.** The paper correctly identifies that prior contamination work has been overwhelmingly English-centric (Section 2), and the concern that translation could conceal contamination signals is important and timely. [favorability=7.93]

- **The experimental design is conceptually clean.** Fine-tuning on controlled mixtures of English and Arabic-translated data (p ∈ {0, 10%, 50%, 100%}) creates a setting where ground-truth contamination is known, unlike typical post-hoc contamination studies. [favorability=11.07]

- **The TS-Guessing extension with choice-reordering (Section 3.3) for MCQ settings** is a sensible methodological addition that could be useful beyond this paper. [favorability=9.35]

## Weaknesses

### Fatal
None.

### Major

1. **No calibration of the TS-Guessing probe.** The paper's central interpretive claim — that translation "masks" contamination — rests on the flatness of TS-Guessing scores across contamination levels (Table 3). However, the TS-Guessing results are largely near-zero (e.g., Mistral IDR = 0.000 at all levels; XQuAD EM/RL-F1 scores near 0.000 across all models). The paper interprets this flatness as evidence of masking, but this requires assuming the probe would detect contamination in a same-language setting with these exact models and data. No such calibration experiment is presented. Without it, the flat scores could equally indicate that the probe is simply insensitive or that little contamination is actually occurring through translation. [favorability=-0.83]

2. **Plausible alternative explanations for the MMLU accuracy gains are not controlled for.** Table 2 shows MMLU accuracy rising monotonically with contamination, which the paper interprets as "contamination-driven memorization" (Section 4.1). However, the EN+AR100 condition has roughly twice the training data as EN-only. The gains could reflect more total training data, cross-lingual transfer, or genuine learning of underlying knowledge. No ablation with equal-sized non-benchmark Arabic data is included to distinguish these. [favorability=-0.30]

3. **A key mechanistic claim is presented without supporting evidence.** Section 4.3 states: "The embedding figure shows that Arabic→English translations remain close to their English originals in representation space, with high cosine similarity." No figure, quantitative similarity values, experimental setup, model identity, or layer information is provided. This claim is central to the explanation of why translation preserves contamination, but the reader cannot evaluate it. [favorability=-0.56]

### Minor

4. **The claim that translation "evades standard detection tools" is broader than the evidence supports.** The abstract and conclusion assert that Arabic translations "evade standard detection tools," but the paper only tests one detection method (TS-Guessing). Other methods discussed in the literature review (Min-K% Prob, guided prompting, Bloom-filter matching) are never applied to the Arabic-translated data. This claim requires at least a demonstration on one additional detector to be substantiated. [favorability=-0.15]

5. **The experimental design simulates intentional fine-tuning leakage, not incidental pretraining contamination.** The paper fine-tunes models on Arabic translations of exact test sets, which is closer to deliberate data leakage during supervised fine-tuning than to the incidental inclusion of benchmark data in pretraining corpora that the contamination literature typically addresses. The framing in the abstract (threatening "validity of LLM evaluation") implies broader applicability, but the gap between these scenarios is not discussed as a limitation. [favorability=3.00]

### Trivial
None.

## Nice-to-Haves

1. **Calibrate the TS-Guessing probe** by running it in a same-language (English→English) contamination setting with the same models. If the probe detects memorization in English but fails when Arabic translation is introduced, this would directly demonstrate the claimed masking effect.

2. **Add a data-quantity control:** fine-tune on an equal amount of non-benchmark Arabic text to distinguish contamination effects from general cross-lingual transfer or data quantity benefits.

3. **Run at least one existing contamination detector** (e.g., Min-K% Prob) on both the English and Arabic training data to directly substantiate claims about standard tools' blind spots.

4. **Either include the embedding analysis** with full experimental details (model, layer, similarity values) or remove the claim.

## Removed Points

- **"Structural contradiction" framing of Weakness 1** — Removed because the paper does not claim TS-Guessing detects contamination; it claims translation masks contamination. The paper's logic (MMLU gains → contamination is real; TS-Guessing flatness → masking) is coherent. The valid calibration concern is retained.

- **Section-by-section notes about literature review length, organization, and writing style** — Removed as subjective/style nitpicks that do not rise to weaknesses.

- **Criticism about single-run experiments with no variance estimates** — Removed per soft rules; single-run fine-tuning evaluation is standard practice in this setting.

- **Criticism about non-monotonic XQuAD/MLQA patterns undercutting core claims** — Removed because the paper explicitly discusses these patterns (Section 4.1) and does not claim a unified contamination effect across all benchmarks.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

The paper's core question is important, and the experimental concept is well-structured. To make the evidence match the claims, the most impactful changes would be: (1) calibrate TS-Guessing with a same-language condition, (2) add a data-quantity control with non-benchmark Arabic data, (3) demonstrate at least one existing detector failing on Arabic while succeeding on English, and (4) either include or remove the embedding analysis. These tighten the paper substantially without expanding its scope.

## Score and Decision

**Bracket analysis (Round 1):** The most topically similar anchors in the corpus are "Evading Data Contamination Detection for Language Models is (too) Easy" (avg 4.25, Reject), "Benchmark Inflation: Revealing LLM Performance Gaps Using Retro-Holdouts" (avg 4.25, Reject), and "Elephants Never Forget: Testing Language Models for Memorization of Tabular Data" (avg 4.75, Reject). These anchor scores place the plausible range for this paper between 4.0 and 5.5. A higher-scoring anchor like "To the Cutoff... and Beyond?" (6.75, Accept) has substantially stronger empirical methodology and rigorous controls that this paper lacks. A lower-scoring anchor like the 1.0–1.4 papers are survey-level works with minimal empirical content, which this paper exceeds.

**Narrowing (Round 2):** Comparing item-level favorability, the "Evading" anchor (4.25) had its most damaging weaknesses at -4.37 (lack of novelty/depth) and -3.44 (contribution not significant). Our paper's most damaging weakness is -0.83 (TS-Guessing calibration), substantially less severe. However, the "Evading" paper actually implements and demonstrates an evasion technique, while our paper leaves central claims unsupported by the experiments. The "Elephants Never Forget" anchor (4.75) had a similar structural weakness (lack of probe validity evidence rated -2.32) and received a Reject decision despite its strengths. Our paper shares the same fundamental gap: the primary detection probe is not validated.

**Final calibration:** The paper has a genuinely novel and well-motivated research question with a clean experimental design concept, placing it above the 4.0 floor. However, three major evidence gaps — no probe calibration, no data-quantity control, and an unsupported embedding claim — prevent the experiments from substantiating the central conclusions. The claims in the abstract and conclusion (that translation "evades standard detection tools" and that "contaminated knowledge continues to influence model behavior") require at least one of these gaps to be closed. In its current state, the paper reads as a preliminary investigation whose evidence does not match the strength of its claims.

MY FINAL SCORE: <score>5.0</score>
MY FINAL DECISION: <decision>Reject</decision>