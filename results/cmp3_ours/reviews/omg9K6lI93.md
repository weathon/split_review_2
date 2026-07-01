Now let me write the final consolidated review.

## Summary

This paper investigates whether translating benchmark data into Arabic can "mask" data contamination in LLM evaluation. The authors fine-tune four open-weight models on English test splits of MMLU, XQuAD, and MLQA augmented with Arabic translations at varying proportions (0%, 10%, 50%, 100%), then evaluate on the original English benchmarks. They use TS-Guessing probes to detect memorization and propose a Translation-Aware Contamination Detection (TACD) framework.

## Strengths

- **Well-motivated research question (Introduction, Section 1).** The question of whether translation conceals contamination in multilingual evaluation is real, timely, and under-explored. The contamination literature is overwhelmingly English-centric.

- **Clean controlled fine-tuning setup (Section 3.1, lines 128–146).** The use of four models, three datasets, graded contamination levels (p ∈ {0, 10%, 50%, 100%}), and consistent LoRA/PEFT infrastructure across all conditions is a reasonable design for isolating the effect of adding Arabic-translated test-set data to the training mixture.

- **Systematic probing methodology (Section 3.3).** Extending TS-Guessing with choice reordering for MMLU and masked-token recovery for extractive QA provides a principled approach to detecting memorization beyond surface-form matching.

## Weaknesses

### Major

1. **Missing same-language (English→English) control condition.** The paper argues that translation specifically "masks" contamination signals, but never compares the Arabic condition to an English→English condition. Without this control, the flat or non-monotonic TS-Guessing scores in Table 3 cannot be attributed to translation. It is possible that LoRA fine-tuning on test-set data does not produce detectable TS-Guessing signals *regardless of language*. The minimal control would be: fine-tune models on p% of the English test set and run the same TS-Guessing probes. If the English condition shows the expected monotonic IDR increase and the Arabic condition does not, the "translation masks contamination" claim would have direct support. Without it, the paper's central conclusion is significantly weakened. (Section 3.1, Section 4.2)

2. **Internal inconsistency in result interpretation.** Section 4.2 states: "Across contamination levels p ∈ {10, 50, 100}%, the models exhibit approximately equal performance on all evaluated benchmarks. This near-flat trend indicates that Arabic→English translation is effectively masking contamination effects… The consolidated results in Tables 2 and 3a show that scores remain broadly stable as p increases." This is contradicted by Table 2, which shows clear and often substantial increases in MMLU (e.g., Mistral: 0.577→0.690, LLaMA: 0.332→0.431, Gemma: 0.220→0.284). The paper's own Section 4.1 (line 189) acknowledges that "MMLU exhibits a generally monotonic increase as contamination rises from 0% → 100%." The paper cannot simultaneously claim that MMLU scores increase monotonically (Section 4.1) and that "scores remain broadly stable" (Section 4.2). This inconsistency makes it unclear what pattern the authors consider the key finding. (Table 2, lines 189–190, lines 201–218)

3. **TS-Guessing probe results do not clearly support the "masking" narrative.** If TS-Guessing were detecting contamination, IDR should increase (or at least be non-decreasing) with contamination level p. The data shows the opposite for several models:
   - **MMLU (Table 3a):** Gemma IDR drops from 0.350 (10%) → 0.029 (50%) → 0.005 (100%); the probe becomes *less* sensitive at higher contamination. Qwen IDR slightly decreases with p (0.261→0.251→0.208). LLaMA IDR is non-monotonic (0.287→0.643→0.410).
   - **XQuAD (Table 3b):** EM and ROUGE-L-F1 are essentially zero for all models and contamination levels (most ≤0.01). Mistral's values (0.10–0.11) are the highest but still very low and slightly *decreasing* with p.
   The paper attributes this to "masking," but this is circular: the probe fails to detect contamination, and the explanation given is that contamination is masked. Without independent evidence (e.g., a same-language control showing the probe works in English), the reader cannot distinguish between (a) translation masks contamination and (b) the probe simply does not work under LoRA fine-tuning. (Table 3, Section 4.2)

### Minor

4. **Unsupported claim about "stronger Arabic capabilities."** The abstract and introduction state that models benefit "particularly those with stronger Arabic capabilities," but the paper provides no measurement, ranking, or citation for which models have stronger Arabic proficiency. This assertion is unsupported. (Abstract, line 17)

5. **No uncertainty quantification.** Tables 2 and 3 report point estimates without variance, confidence intervals, or significance tests across 4 models × 3 datasets × 4 contamination levels = 48 conditions. Many differences are small (e.g., Mistral MMLU 0.577→0.580 for 0%→10%), making it impossible to assess whether they are signal or noise.

6. **Arabic translation source unspecified.** The paper does not state whether the Arabic translations were produced via machine translation or human translation, nor what quality assurance was applied. Translation quality affects both semantic preservation and surface-form divergence, which are central to the claims.

7. **TACD framework is unimplemented.** Section 5 describes TACD as a "forward-looking blueprint rather than a complete implementation" (line 252). The three components are reasonable ideas but are not evaluated or compared to alternatives. This limits the weight of TACD as a contribution.

### Trivial

None.

## Nice-to-Haves

- A same-language (English→English) control condition for the fine-tuning and TS-Guessing experiments. This is the single most impactful addition and would directly test whether translation specifically causes the probe's failure.
- Uncertainty quantification (confidence intervals or significance tests) for the main results.
- Clarification of translation methodology (human vs. machine, quality assurance).
- A controlled pre-training study (or explicit acknowledgment that the paper studies test-set leakage through fine-tuning, not pre-training contamination, and a reframing of the contribution accordingly).

## Removed Points

- **"The experimental setup does not model the contamination phenomenon" (Reviewer's Issue 1).** The reviewer argued that the paper studies fine-tuning on test-set translations, not pre-training contamination, and that this mismatch is fatal. The paper does study a form of data contamination (test-set leakage through fine-tuning), and while the framing could be more precise about the mechanism, this is not a fatal flaw. The finding that translation can mask fine-tuning-based test-set leakage is still meaningful. Demoted from "Fatal" to a point addressed in the Major weakness about framing and now handled as part of the missing control weakness (Major #1) and the nice-to-have section.

- **"The main empirical finding is unsurprising" (Reviewer's Issue 4).** This is an opinion about significance, not a specific weakness. The paper provides controlled empirical evidence for a phenomenon that, while intuitive, had not been systematically documented. Generic significance dismissals are not actionable.

- **Criticism about the literature review being too long (Section-by-Section Notes).** Pure presentation/style preference; does not bear on the paper's technical validity.

- **"The embedding figure is described but not shown."** The figure may have been stripped by the PDF parser; not verifiable as an author omission.

- **"The paper's claim in Section 4.2 is circular" framing.** This is subsumed by the more precise weakness about TS-Guessing results not supporting the narrative (Major #3).

## Novel Insights

The reviews converge on a key structural gap that the paper's own framing does not acknowledge: the central claim that "translation masks contamination" requires a control condition (English→English) to disentangle the effect of translation from the effect of the fine-tuning paradigm itself. Without this control, the flat TS-Guessing scores could reflect a general limitation of the probe under LoRA fine-tuning rather than a translation-specific masking phenomenon. This observation goes beyond any single reviewer's comment and identifies the most critical path toward strengthening the paper.

## Suggestions

1. **Add an English→English control condition.** Fine-tune the same models on p% of the *English* test set and run TS-Guessing probes. If IDR rises monotonically with p in English but not in Arabic, the "translation masks contamination" claim would have a direct empirical foundation.

2. **Resolve the internal inconsistency** between Section 4.1 (which correctly notes MMLU increases with p) and Section 4.2 (which claims results are "broadly stable"). The TS-Guessing results (Table 3) can be described as showing weak or inconsistent signals; the evaluation results (Table 2) should be described as showing model-specific and often substantial increases.

3. **Reframe the contribution** to acknowledge that the paper studies test-set leakage through fine-tuning (not pre-training contamination), and clarify why this form of contamination is worth studying independently.

## Score and Decision

**Anchor comparison:** The most topically similar calibrated paper is "Evading Data Contamination Detection for Language Models is (too) Easy" (avg 4.25, Reject), which implemented a concrete evasion attack against multiple detectors but was criticized for limited technical depth. The current paper has a cleaner experimental design but a weaker link between its central claim and its evidence, primarily due to the missing same-language control. The other similar anchors—"Benchmark Inflation" (4.25), "Elephants Never Forget" (4.75)—all implement and evaluate their proposed methods, whereas this paper's TACD proposal is unimplemented.

**Bracketing:** Round 1 bracket was 3.0–4.5. Round 2 narrowed to 3.0–4.0 by comparing against anchors with similar topics but more complete claim-evidence alignment. The paper's strengths (clean setup, important question) are offset by a fundamental gap (missing control) and internal inconsistencies that weaken the interpretive claims.

**Final assessment:** The paper asks a worthwhile question and provides a clean experimental framework, but the missing control condition prevents the central "translation masks contamination" claim from being supported, and the TS-Guessing evidence is at odds with the paper's own interpretation. These are addressable with additional experiments, but they substantially weaken the paper in its current form.

MY FINAL SCORE: <score>3.5</score>
MY FINAL DECISION: <decision>Reject</decision>