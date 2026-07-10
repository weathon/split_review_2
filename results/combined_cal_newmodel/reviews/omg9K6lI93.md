## Summary

This paper investigates whether translating benchmarks into Arabic can mask data contamination in LLM evaluation. The authors fine-tune four open-weight instruction models (1B–7B parameters) on varying proportions (0%, 10%, 50%, 100%) of Arabic-translated test data from MMLU, XQuAD, and MLQA, then evaluate on the original English benchmarks. They extend the TS-Guessing memorization probe with a choice-reordering strategy for multiple-choice questions. The paper reports that models benefit from exposure to translated contaminated data while TS-Guessing signals remain low (suggesting translation obscures detectable contamination), and proposes a conceptual Translation-Aware Contamination Detection (TACD) framework.

## Strengths

- **Choice-reordering extension to TS-Guessing (Section 3.3, Figure 1) is a sensible adaptation for the MCQ setting.** Shuffling choices before masking tests whether the model recalls index-position associations rather than reasoning about content—a clean operationalization of one form of memorization. This methodological contribution is concrete and specific to the paper.
- **The paper is clearly written and easy to follow.** The methodology section describes the training conditions, datasets, and probe design concisely, and the research question (whether translation can mask contamination) is well-motivated by the existing literature's English-centric focus (Section 2.3).

## Weaknesses

### Major

- **Unsupported claim about "stronger Arabic capabilities."** The abstract and introduction state that models benefit from contaminated data "particularly those with stronger Arabic capabilities." The paper provides zero evidence for this claim: no Arabic benchmark evaluation, no Arabic proficiency metric, and no correlation analysis between Arabic ability and contamination benefit. The four models (Llama-3.2-1B-Instruct, Mistral-7B-Instruct-v0.2, Gemma-3-1B-it, Qwen3-1.7B) are never evaluated on Arabic tasks, and differences in their Arabic capabilities are simply assumed. This claim should either be supported with explicit evidence or removed.

- **The TS-Guessing probe results cannot support the paper's core "masking" interpretation without a same-language baseline.** The TS-Guessing scores (Table 3) are near-floor across most conditions (XQuAD EM: 0.000–0.103; MMLU IDR for Mistral: 0.000–0.001; Gemma's IDR decreases from 0.350 to 0.005 as contamination increases). The paper interprets this flatness as evidence that translation "masks" contamination signals. However, without a baseline condition (fine-tuning on English test data and running TS-Guessing to show what unmasked contamination signals look like), this interpretation is indistinguishable from "the TS-Guessing probe does not detect memorization through this mechanism" or simply "the models did not memorize in a way TS-Guessing captures." A same-language baseline is necessary to validate the causal claim that translation specifically (rather than properties of the probe or the training setup) is responsible for the absence of detection signals.

- **The experimental design conflates contamination effects with cross-lingual transfer and increased training data.** The training set adds Arabic-translated test data on top of the English data, meaning the p=0 condition has strictly less data than p>0 conditions. Performance gains (e.g., Mistral MMLU: 0.577→0.690; LLaMA XQuAD: 0.364→0.569) could partially reflect (a) simply having more training examples, or (b) cross-lingual transfer learning from Arabic QA data to English QA on similar topics. Without a control condition (e.g., fine-tuning on an equivalent volume of non-benchmark Arabic data), the paper cannot isolate contamination-driven memorization from these alternative mechanisms. The paper assumes any performance increase from adding Arabic-translated test data is contamination-driven, but this conflates memorization with transfer learning.

- **The TACD framework (Section 5) is presented as a contribution but has no implementation or evaluation.** The paper itself describes it as a "forward-looking blueprint" (line 252) and acknowledges that deploying it "would require shared infrastructure and community resources." While future-outlook sections are reasonable, presenting an unimplemented, unevaluated framework as a contribution in the abstract overstates what has been delivered.

### Minor

- **No statistical variance or significance is reported.** Every result in Tables 2 and 3 is a single point estimate without error bars, confidence intervals, or replication across seeds. Given that fine-tuning small models with different random seeds can produce substantial variance, the reader cannot assess whether observed differences (e.g., Mistral MMLU: 0.577→0.580 at 10%) are meaningful or noise. This is especially problematic for the TS-Guessing results where the differences being interpreted are in the 0.001–0.01 range.

- **Section 4.2 contains an internal contradiction in its characterization of the results.** The text claims that "across contamination levels p ∈ {10, 50, 100}%, the models exhibit approximately equal performance on all evaluated benchmarks" and that "scores remain broadly stable as p increases." Yet Table 2 shows substantial variation (Mistral MMLU rises 0.577→0.690, +20% relative; LLaMA XQuAD rises 0.364→0.569, +56%; Mistral XQuAD collapses 0.455→0.114). The exposition appears to conflate evaluation metric trends (Table 2) with TS-Guessing probe metrics (Table 3), creating confusion about what exactly is being claimed as "masked."

### Trivial

None.

## Nice-to-Haves

1. **Add a same-language (English) baseline** for TS-Guessing: fine-tune on English copies of the test set and probe with TS-Guessing. This would show what unmasked contamination signals look like and allow the paper to substantiate the "masking" interpretation.
2. **Add a non-benchmark Arabic control condition**: fine-tune on an equivalent volume of Arabic data unrelated to the benchmarks (e.g., Arabic Wikipedia) to separate contamination effects from general cross-lingual transfer or increased training data.
3. **Report variance estimates** from multiple random seeds (3+) for all experiments.
4. **Substantiate or remove the Arabic-capabilities claim**: either evaluate Arabic proficiency explicitly and correlate it with contamination benefit, or remove the claim entirely.

## Removed Points

The following criticisms from the input review were removed:

- **"Experimental design does not test what the paper claims" (Issue 1 in its strongest form):** The critic argued the paper tests cross-lingual transfer rather than contamination. However, training on Arabic-translated test items and evaluating on the original English items is a valid contamination scenario (the model sees the test content in a different surface form). The criticism was moderated to focus on the specific confounds (more training data, lack of controls) rather than dismissing the experimental design entirely.
- **"Section-by-section notes" about translation quality, use of instruction-tuned vs base models, and dataset selection:** These are scope-creep criticisms that demand the paper address problems outside its stated scope or make methodological choices that are not standard requirements.
- **Strength 1 ("research question is well-motivated and timely"):** Removed as generic per filtering rules. The strength lacked concrete specificity to this paper.

## Novel Insights

None beyond the paper's own contributions. The paper identifies an underexplored dimension (multilingual contamination via translation) and presents preliminary evidence that standard English-only contamination probes may not detect memorization when benchmarks are translated. However, the reviews do not surface any novel framing or interpretation that the paper itself does not already present.

## Suggestions

1. The paper's core claim is that translation "masks" contamination. To demonstrate this convincingly, the most impactful addition would be a same-language English baseline where models are fine-tuned on English test data and probed with TS-Guessing. If TS-Guessing detects contamination strongly in the English condition but not in the Arabic condition (while evaluation scores rise in both), that would directly support the masking thesis.
2. Add a non-benchmark control condition to rule out the "more training data" confound.
3. Either substantiate the Arabic-capabilities claim with evidence (Arabic benchmarks, proficiency metrics, correlation analysis) or remove it. As written, this claim is unsupported and undermines trust in the paper's conclusions.
4. Report all results with variance estimates from multiple runs.

**Calibration Report**

All anchor papers retrieved across rounds:

| Anchor | Path | Avg Score | Round | Itemized | Comparison |
|--------|------|-----------|-------|----------|------------|
| Evading Data Contamination Detection | Nk1MegaPuG.md | 4.25 | R1 | Yes | Very similar topic (evading detection); had far more severe weaknesses (items at -5.52, -4.59 favorability) vs our paper's worst at -1.58 |
| Elephants Never Forget | lwtaEhDx9x.md | 4.75 | R1 | Yes | Similar topic (memorization testing); had severe weaknesses at -4.10 and -4.31, broader methodological contribution |
| Correlation Analysis of MT Metrics | MyotJECv0D.md | 2.50 | R1 | No | Lower quality, less related |
| How Much Can We Forget | Nsms7NeU2x.md | 6.75 | R2 | Yes | More rigorous experimental design; our paper is notably less thorough |
| To the Cutoff and Beyond | m2NVG4Htxs.md | 6.75 | R2 | Yes | Stronger methodology; our paper has less comprehensive evaluation |
| Understanding Memorisation Dynamics | ILStlRb1Sp.md | 5.00 | R2/N | Yes | Systematic experimental design on limited setting; worst item at -2.18; mixed reviews |
| Generalization vs Memorization | IQxBDLmVpT.md | 5.00 | R2 | No | Similar thematic area; strong methodological contribution |

**Round-1 bracket:** The paper sits between the 4.25 anchor ("Evading Data Contamination Detection") and the 5.00 anchors ("Understanding Memorisation Dynamics" at 5.00, "Generalization vs Memorization" at 5.00). Compared to the 4.25 anchor, our paper has notably less severe negative items (-1.58 vs -5.52 worst), cleaner presentation, and a more novel research question. Compared to the 5.00 anchors, our paper has comparable worst-item severity but less systematic experimental design and missing critical baselines.

**Final placement:** The paper's worst items (Arabic-capabilities claim at -1.58, TACD blueprint at -1.52, missing baseline at -0.08) are less severe than the 4.25 anchor's worst items (-5.52), favoring a score above 4.25. However, the 5.00 anchors had stronger experimental evidence or methodological rigor. The paper's central interpretive claim (that translation "masks" contamination) requires a baseline the paper does not provide, and the unsupported Arabic-capabilities claim undermines a stated contribution. At the same time, the research question is genuinely novel and timely, the TS-Guessing extension is a reasonable contribution, and the paper is clearly presented. The score is calibrated at 4.5, reflecting a paper with a worthwhile research direction and clean exposition but whose experimental execution is insufficient to support its headline claims.

## Score and Decision

MY FINAL SCORE: <score>4.5</score>
MY FINAL DECISION: <decision>Reject</decision>