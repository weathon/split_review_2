Now I have all the information I need. Let me compile the final review.

## Summary

This paper investigates whether translating evaluation benchmarks into Arabic conceals or eliminates data contamination in LLMs. The authors fine-tune four open-weight models on varying proportions (0%, 10%, 50%, 100%) of Arabic-translated MMLU, XQuAD, and MLQA data, then evaluate on the original English benchmarks and probe memorization with a choice-reordering extension of TS-Guessing. The paper finds that models show performance gains from Arabic-translated contamination while standard detection signals remain weak, arguing that translation creates a blind spot in current contamination detection.

## Strengths

- **Well-motivated and practically important research question.** Whether translating evaluation benchmarks into another language masks or eliminates data contamination is genuinely underexplored. The paper identifies this gap clearly (Section 1, Section 2.4) and addresses a timely concern for multilingual evaluation practices.
- **Systematic contamination conditions.** Varying proportions of Arabic-translated data (0%, 10%, 50%, 100%) across three datasets (MMLU, XQuAD, MLQA) and four models provides a principled dose-response design, stronger than a binary contaminated/not-contaminated comparison.
- **Choice-reordering extension to TS-Guessing (Section 3.3).** Adding choice shuffling to probe index-pattern memorization is a sensible methodological addition for the MMLU setting, and the procedure is clearly described.

## Weaknesses

### Major

**1. The experimental design cannot isolate contamination from the effect of additional training data.** The training set for all conditions (including p=0) already includes D_EN, described as "English test items" / "English QA" from the evaluation benchmarks themselves (line 132). The p>0 conditions add Arabic-translated test data on top. This means: (1) there is no clean baseline — all models are already contaminated with English test data; (2) gains from p=0 to p>0 could reflect simply having more training data (English + Arabic vs. English only), improved Arabic language ability that transfers cross-lingually, or exposure to more varied surface forms — not necessarily contamination through translation in the sense the paper argues. A non-benchmark Arabic control (e.g., Arabic Wikipedia text of matched size) is needed to attribute observed effects specifically to contamination rather than to general Arabic data exposure.

**2. Section 4.2's central interpretive claim does not match the reported data.** The paper states that "across contamination levels p ∈ {10, 50, 100}%, the models exhibit approximately equal performance on all evaluated benchmarks" and that "scores remain broadly stable as p increases." Table 2 tells a different story. For example, from p=10 to p=100: Mistral MMLU rises from 0.580 to 0.690 (+19%), Mistral XQuAD falls from 0.455 to 0.114 (-75%), Qwen MLQA falls from 0.409 to 0.153 (-63%). These are substantial, often large changes that contradict the "broadly stable" characterization. Since the paper's core narrative — that translation conceals contamination signals by compressing performance differences — is built on this characterization, the mismatch between claim and evidence undermines the paper's main conclusion.

### Minor

**3. The TS-Guessing probe results are weak and do not cleanly support the "masked contamination" narrative.** XQuAD EM values are essentially zero across all conditions (≤0.017 for all models except Mistral at 0.074–0.113). MMLU IDR values are erratic and non-monotonic (e.g., LLaMA: 0.287→0.643→0.410; Gemma: 0.350→0.029→0.005). The paper interprets weak/erratic probes as evidence that translation "masks" contamination, but a simpler alternative explanation — that TS-Guessing is simply not sensitive enough in this setting, or that the observed performance gains stem from non-contamination mechanisms (more data, better Arabic→English transfer) — is not ruled out.

**4. No error bars, confidence intervals, or statistical tests are reported anywhere.** With single-run results and many non-monotonic patterns (e.g., "peak-at-10%" in MLQA), the reader cannot distinguish signal from noise. Multiple seeds and variance reporting are needed, especially given that LoRA fine-tuning on these model sizes is relatively cheap.

**5. The provenance and quality of the Arabic translations are not described.** The paper says "Arabic translations" for MMLU and "Arabic split" for XQuAD/MLQA (lines 132–142), but does not state whether translations were machine- or human-generated, by whom, or whether they were validated. Translation quality and artifacts directly affect the paper's core claims about contamination through translation.

**6. The TACD framework (Section 5) is presented as a contribution in the abstract but is explicitly described as a "forward-looking blueprint rather than a complete implementation" (line 252) with no experiments, validation, or empirical support.** The abstract should scope this as a proposed future direction rather than as something the paper "proposes" as a completed framework.

### Trivial

None.

## Nice-to-Haves

- A non-benchmark Arabic control (e.g., matched-size Arabic Wikipedia fine-tuning) would substantially strengthen the causal claims about contamination versus general Arabic data effects.
- Checking whether the base pre-trained models (Llama-3.2-1B, Mistral-7B, etc.) were already exposed to Arabic MMLU/XQuAD/MLQA data during pretraining would help disentangle fine-tuning effects from prior exposure.

## Removed Points

These points were identified by the harsh critic but are removed from the main review for the following reasons:

- **"Internal contradiction between Section 4.1 and Section 4.2"** — Removed because these sections discuss different scopes (Section 4.1: MMLU from 0→100%; Section 4.2: all benchmarks from 10→100%). They are not directly contradictory. The real problem — that Section 4.2's "broadly stable" claim doesn't match Table 2 — is retained as Major weakness #2.
- **"TACD is not a contribution" framed as fatal** — Downgraded to Minor (#6) because the paper is upfront that TACD is a blueprint, and many papers propose future directions. The issue is mainly about the abstract's framing.
- **The p=0 baseline being "already contaminated" frames as invalidating the paper** — Reframed as Major weakness #1 (design confound) rather than a fatal flaw. The paper can still compare p=0 vs p>0 conditions to study the effect of adding Arabic contamination; the limitation is the inability to fully attribute gains to contamination vs. more Arabic data.
- **Missing embedding figure reference** — This is a parser artifact (embedded images lose their figure numbers in plain-text extraction).
- **Formatting nitpicks and complaints about missing appendix content** — Appendix sections were stripped by the PDF parser; they exist in the original submission.
- **Speculative claims about model providers not releasing data** — These are about cited works, not about the paper under review.
- **Generic "no related work" mentions** — Cannot verify without external sources.

## Novel Insights

The harsh critic correctly identifies that the paper's experimental design has a subtle but important confound: training on English test items in all conditions makes it impossible to fully separate contamination effects from general training data effects. However, the critic's framing of this as a fatal flaw that "invalidates the paper" overstates the case — the paper still provides partial evidence that adding Arabic-translated test data produces performance changes that standard probes fail to detect, which is a useful observation even if the design is not perfectly controlled. The more serious and specific problem is that Section 4.2's interpretive overreach (claiming "broadly stable" scores that the data does not support) undermines the paper's narrative more than any single design limitation — this is a factual error about what the data shows, not a judgment call.

## Suggestions

1. Add a non-benchmark Arabic control condition (e.g., matched-size Arabic Wikipedia fine-tuning) to separate contamination effects from general Arabic data effects.
2. Remove or substantially qualify the "broadly stable" / "approximately equal" claim in Section 4.2, and honestly characterize the substantial variation observed in Table 2.
3. Report results with multiple random seeds and provide variance estimates.
4. Clearly state the translation methodology for all datasets (source, quality, validation procedure).
5. Scope TACD as a future direction in the abstract, consistent with its treatment in Section 5.

## Anchors Used for Calibration

| Anchor | Path | Avg Score | Round | Itemized | Comparison |
|--------|------|-----------|-------|----------|------------|
| Evading Data Contamination Detection | Nk1MegaPuG | 4.25 | R1, R2 | Yes | Topic-wise closest; our weaknesses are less severe (most negative -0.64 vs -3.49), strengths comparable → our paper stronger |
| How much can we Forget | Nsms7NeU2x | 6.75 | R1 | Yes | Much stronger paper with extensive experiments + theory → our paper clearly below |
| To the Cutoff... and Beyond | m2NVG4Htxs | 6.75 | R1 | No | Stronger methodology and more convincing evidence → our paper below |
| Benchmark Inflation | rAylWUIKtu | 4.25 | R1, R2 | Yes | Comparable weakness severity but narrower scope → our paper slightly stronger |
| Elephants Never Forget | lwtaEhDx9x | 4.75 | R2 | Yes | Worse weaknesses (-4.16) but stronger strengths → comparable overall |
| Crosslingual Capabilities | BCyAlMoyx5 | 5.67 | R2 | Yes | Included despite high variance (8,6,3); had very negative weaknesses (-5.69) |
| Clever Hans (Leaving the barn door...) | PtnttTKgQw | 5.00 | R2 | Yes | Strong weaknesses (-4.42); our paper has less severe weaknesses → similar tier |

**Round 1 bracket**: The paper sits between Nk1MegaPuG (4.25) and Nsms7NeU2x (6.75). Given our -0.64-weighted confound weakness vs. the -3.49 and -2.15 weaknesses in the 4.25 anchor, the paper is stronger than 4.25 but lacks the extensive experiments and theoretical grounding of the 6.75 anchor.

**Round 2 narrowing**: Compared against lwtaEhDx9x (4.75) and PtnttTKgQw (5.00), our paper has less severe weaknesses than either — our most negative item is -0.64 vs. -4.16 and -4.42 respectively. However, our strengths are also less exceptional. This places the paper in the upper 4s to low 5s range.

**Final score placement**: The -0.64 weight on the design confound is a clear signal that this weakness materially harms the paper's score. Combined with the Section 4.2 interpretive overreach (weight 2.29, still in the mildly harmful range), the paper has two clear issues that prevent it from reaching the 5+ range. At the same time, the topic is genuinely novel and the systematic design across 3 datasets × 4 models is a strength. The closest calibrated anchor is PtnttTKgQw (5.00) but our paper's negative-weight weakness is less severe — placing it slightly below that point due to the unresolved interpretive overreach.

MY FINAL SCORE: <score>4.5</score>
MY FINAL DECISION: <decision>Reject</decision>