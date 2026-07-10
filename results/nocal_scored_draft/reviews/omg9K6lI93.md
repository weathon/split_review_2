Now I have all the evidence I need. Let me compile the final review.

## Summary

The paper investigates whether translating benchmarks into Arabic (a lower-resource language) can mask data contamination in LLM evaluation. It fine-tunes four models on varying proportions (0%, 10%, 50%, 100%) of Arabic-translated test data from MMLU, XQuAD, and MLQA, then evaluates on the original English benchmarks, using a choice-reordering extension of TS-Guessing to probe memorization. The core finding — that models benefit from exposure to translated contaminated data (MMLU accuracy increases) — is empirically demonstrated, but the paper's central narrative that translation "conceals" contamination and creates a "dangerous blind spot" is not adequately supported by the evidence presented.

## Strengths

- **Novel research question.** The paper asks a genuinely underexplored question: whether translating benchmarks into lower-resource languages can mask contamination during evaluation. This is timely and relevant as multilingual LLM evaluation grows.
- **Well-structured experimental design.** Varying contamination proportions (0%, 10%, 50%, 100%) across multiple models (4) and dataset types (MCQ and extractive QA) provides a reasonable basis for observing dose-response relationships.
- **Thoughtful methodological extension.** The choice-reordering extension to TS-Guessing for MCQ benchmarks — masking one incorrect choice after shuffling and checking whether the model recalls the pre-shuffle index-letter — is a clever probe for detecting surface-level memorization patterns.

## Weaknesses

### Major

- **Internal inconsistency in the masking narrative.** Section 4.1 acknowledges MMLU's "generally monotonic increase" with contamination (e.g., Mistral: 0.580→0.690, LLaMA: 0.381→0.431 at 10%→100%), and Section 4.3 reiterates this pattern. Yet Section 4.2 claims "approximately equal performance on all evaluated benchmarks" and a "near-flat trend" as evidence that translation is masking contamination. The MMLU results in Table 2 clearly show large, non-flat increases for the paper's primary benchmark (Mistral-7B: +19.6% relative from 0% to 100%). This direct contradiction between the data and a key supporting argument for the masking claim weakens the paper's central narrative.

- **Missing empirical verification of detection failure.** The paper claims translation "evades standard detection tools" (Conclusion) and "conceals traditional contamination signals" (Abstract), but never runs any of the detection methods it surveys in Section 2.3 (Min-K% Prob, guided prompting, n-gram search) on the Arabic data to verify this. The paper reviews these methods in detail and could have tested whether they fail on translated data. Without this experiment, the central "blind spot" claim — the paper's main contribution — remains an untested assertion rather than a demonstrated finding.

- **TS-Guessing results do not support the narrative.** Table 3 shows that TS-Guessing detects almost no contamination even where MMLU accuracy proves contamination is occurring. Mistral's MMLU index-recall rate (IDR) is 0.000 at every contamination level. Gemma's IDR *decreases* from 0.350 to 0.005 as contamination increases — the opposite of what a contamination probe should show. XQuAD EM/ROUGE-L values are below 0.02 for most models. The probe appears to fail as a contamination signal, which the paper does not adequately address. If the probe is meant to "disentangle genuine reasoning from contaminated recall" (Abstract), its inability to detect known contamination undermines its utility.

### Minor

- **TACD overclaimed.** The Translation-Aware Contamination Detection framework is presented as a contribution in the abstract, introduction, and conclusion, but is explicitly a "forward-looking blueprint rather than a complete implementation" (line 252) with no experiments, baselines, or validation. This overclaims relative to what is delivered.

- **No uncertainty quantification.** No confidence intervals, error bars, or significance tests are reported anywhere. Given that non-monotonic XQuAD/MLQA patterns are central to the analysis, the reader cannot assess whether these reflect meaningful trends or variance.

- **Embedding claim lacks quantitative evidence.** The paper states Arabic→English translations have "high cosine similarity" to English originals (Section 4.3) but reports no actual similarity values, baseline comparisons, or the referenced figure's data. This leaves a proposed mechanistic explanation on thin evidence.

- **Generalization gap between fine-tuning and pre-training.** The paper studies contamination through explicit fine-tuning on translated test sets but frames this as revealing a "dangerous blind spot" in LLM evaluation generally, without discussing how fine-tuning on pure test-set data differs from incidental contamination during massive-scale pre-training.

### Trivial

None.

## Nice-to-Haves

- Run at least one existing detection method (e.g., Min-K% Prob) on the Arabic training data and compare detection rates against English data to directly test whether translation conceals contamination signals.
- Add bootstrap confidence intervals to quantify uncertainty around non-monotonic XQuAD/MLQA trends.
- Report actual cosine similarity values with baseline comparisons for the embedding analysis.
- Reconcile the MMLU upward trends with the "masking" narrative explicitly, rather than claiming flatness.
- Reframe TACD from a claimed contribution to a future-work discussion.

## Removed Points

These points from the harsh critic input were filtered:
- "Section 2 is too long (40%)" — removed as a style nitpick per Hard Rules.
- "The paper's central claim is contradicted by its own data" as a fatal flaw — reframed as an internal inconsistency (Major) because the core empirical finding (contamination persists through translation) *is* supported by the MMLU data; the inconsistency is in a supporting argument about "near-flat" trends.
- "The fine-tuning setup doesn't model real contamination" as a severe gap — the paper is transparent about its deliberate contamination study design; downgraded to a minor scope note.

## Novel Insights

None beyond the paper's own contributions. The reviews validate the research question and experimental design but consistently identify gaps in evidential support for the core claims.

## Suggestions

1. **Fix the internal inconsistency.** Acknowledge the MMLU increases explicitly in Section 4.2 and reframe the "masking" narrative around what the data actually shows: translation preserves semantic content (contamination works), but detection methods need separate verification.
2. **Run a detection method on the Arabic data.** This single experiment would directly test whether the claimed "blind spot" exists, and would substantially strengthen the paper regardless of outcome.
3. **Downscope the contribution claims** to match what is demonstrated: an empirical study showing contamination effects persist through translation, rather than a demonstrated detection failure or a validated framework.

## Score and Decision

The paper identifies a genuine and timely research question and designs reasonable experiments. However, it suffers from a significant internal inconsistency (claiming "near-flat" trends for MMLU when clear increases are visible), fails to empirically verify its central claim about detection failure, and presents a probe (TS-Guessing) that does not detect the contamination the paper knows is present. The TACD framework is overclaimed relative to its implementation. These problems collectively undermine the paper's main contribution narrative. The empirical finding that contamination through translation affects performance is real but modest relative to the claims made.

MY FINAL SCORE: <score>4</score>
MY FINAL DECISION: <decision>Reject</decision>