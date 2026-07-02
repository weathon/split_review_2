## Summary
# Final Review Report

## Summary

This paper investigates whether translating standard English LLM benchmarks (MMLU, XQuAD, MLQA) into Arabic masks or eliminates data contamination effects. The authors fine-tune four open-weight instruction models on varying proportions of Arabic-translated benchmark data and evaluate on the original English benchmarks, using an extended TS-Guessing method with choice-reordering to distinguish genuine reasoning from memorization. The central finding is that Arabic translation obscures surface-level contamination signals (exact string matches, n-gram overlap) while preserving semantic leakage—models still benefit from contaminated data, particularly those with stronger Arabic capabilities. Based on this finding, the authors outline a Translation-Aware Contamination Detection (TACD) framework as a conceptual blueprint.

The paper addresses a timely and underexplored question: whether English-centric contamination detection is sufficient for multilingual evaluation. The experimental design (four models × three datasets × four contamination levels) provides reasonable breadth. The TS-Guessing extension for multiple-choice tasks is a sensible methodological contribution.

However, the paper has several significant weaknesses that limit its conclusions. (1) A critical experimental confound: the English evaluation data is included in the training set for all conditions, meaning the study measures additional benefit from Arabic contamination on top of already-present English contamination—not contamination detection per se. (2) The claim that performance is "approximately equal" across contamination levels (Section 4.2) contradicts the paper's own Table 2, which shows substantial MMLU gains (up to +0.113 for Mistral). (3) All results lack variance reporting (single-run, no confidence intervals), making it impossible to assess statistical reliability. (4) The TACD framework is presented as a contribution but has zero experimental validation. (5) The embedding analysis central to the mechanistic explanation is referenced but not shown.

Due to Retrieval-Disabled Mode in this review run, novelty and literature comparison conclusions are explicitly deferred for manual verification.

## Strengths
1. **Timely and important research question.** The paper asks whether English-centric contamination detection is sufficient for multilingual evaluation—a question that becomes increasingly important as LLM evaluation expands to non-English languages. The finding that translation can mask but not eliminate contamination has practical implications for benchmark design and evaluation pipelines.

2. **Well-scoped experimental design.** Testing four diverse open-weight models (varying in size from 1B to 7B parameters, from different families) across three datasets (multiple-choice QA, extractive QA) with four contamination levels provides reasonable breadth. The use of parameter-efficient fine-tuning (LoRA/PEFT) with identical hyperparameters across conditions helps ensure fair comparisons within the study.

3. **Creative methodological extension.** The choice-reordering variant of TS-Guessing for MCQ tasks is a thoughtful adaptation that provides an additional signal (Index-recall rate) beyond standard accuracy metrics. The intuition—that models recalling pre-shuffle letter indices reveal memorization rather than reasoning—is sound and could be useful for the broader contamination detection toolkit.

4. **Honest acknowledgment of limitations.** Section 5.3 transparently admits that TACD is a "forward-looking blueprint rather than a complete implementation" and discusses the resource requirements and potential noise introduced by translation. This honesty about scope boundaries is commendable.

5. **Clear and engaging writing voice.** The paper is generally well-written with clear organization and accessible explanations of complex contamination concepts. The narrative arc from problem to gap to method to findings is easy to follow, despite some structural issues noted in the weaknesses.

## Weaknesses
### W1. Critical experimental confound: English evaluation data included in training (major)

**Evidence:** The training data is defined as $D_{\text{train}}^d(p) = D_{\text{EN}}^d \cup D_{\text{AR}}^d(p)$, where $D_{\text{EN}}^d$ is the English split (MMLU test items, XQuAD/MLQA English QA). The models are then evaluated on the *same* English benchmarks. This means that for all conditions including p=0 (the "clean" baseline), the model has already seen the English evaluation examples during training.

**Risk:** The paper attributes performance gains at p>0 to additional contamination from Arabic translation. But the English evaluation data is already present in every condition. The observed gains may partially reflect the model already having memorized the English evaluation data, with Arabic translation providing marginal additional benefit. The core claim that "translation conceals contamination" is weakened because the study never established a contamination-free baseline to begin with.

**Required action (Must):** Either (a) use a held-out English test set disjoint from $D_{\text{EN}}^d$, or (b) explicitly reframe the experiment as measuring the *additional* effect of cross-lingual contamination on top of already-present English benchmark exposure, and adjust all claims accordingly.

### W2. Internal contradiction: Section 4.2 claims flat performance while Table 2 shows clear gains (major)

**Evidence:** Section 4.1 reports that MMLU rises monotonically (e.g., Mistral: 0.577→0.690, +19.6% relative). Section 4.2 states "Across contamination levels p∈{10,50,100}%, the models exhibit approximately equal performance on all evaluated benchmarks" and "scores remain broadly stable as p increases."

**Contradiction:** Table 2 shows MMLU gains of +0.113 (Mistral), +0.064 (Gemma), +0.099 (LLaMA), and +0.028 (Qwen) from 0% to 100%. XQuAD for LLaMA goes from 0.364 to 0.569 (+56% relative). These are substantial, not flat. The narrative claim of "near-flat" or "approximately equal" performance is directly contradicted by the paper's own evidence.

**Required action (Must):** Revise Section 4.2 to acknowledge that standard evaluation metrics do show clear contamination effects. Clarify that the "flatness" refers specifically to the TS-Guessing metrics (Table 3) and that the evaluation metrics (Table 2) actually reveal contamination-driven gains. This revision is publication-critical because the paper's central thesis rests on this interpretation.

### W3. No variance reporting or statistical significance (major)

**Evidence:** All 12 model×dataset conditions in Tables 2 and 3 report single-run point estimates without standard deviations, confidence intervals, or significance tests. The TS-Guessing IDR values for Mistral are exactly 0.000 across all contamination levels—an implausible result that could indicate either a genuine null effect or a degenerate probe configuration.

**Risk:** Without multi-seed variance, readers cannot assess whether the observed patterns (especially the non-monotonic MLQA trends and the small MMLU gains for Qwen of only +0.028) are meaningful or within noise. The "flatness" interpretation in Section 4.2 could simply reflect high evaluation variance masking real differences.

**Required action (Must):** Report all metrics as mean±std over ≥3 fine-tuning seeds. For key comparisons (0% vs 100% contamination), include a paired significance test or effect size with confidence intervals.

### W4. Unsupported embedding analysis (major)

**Evidence:** Section 4.3 states "The embedding figure shows that Arabic→English translations remain close to their English originals in representation space, with high cosine similarity" and provides the equation $s = \cos(\mathbf{e}^{ar \rightarrow en}, \mathbf{e}^{en})$. However, no embedding figure appears in the manuscript, and no quantitative similarity values, layer breakdowns, or baselines are reported.

**Risk:** The embedding analysis is the mechanistic foundation for the claim that "translation ≠ decontamination." Without supporting data, this explanation is speculative rather than evidenced. The paper's interpretation that semantic similarity explains contamination persistence is plausible but unverified within this manuscript.

**Required action (Must):** Either include the embedding analysis as a proper figure/table with quantitative results (mean cosine similarity, standard deviations, comparison to random baselines), or downgrade the mechanistic claim to a hypothesis requiring future verification.

### W5. TACD framework presented as contribution but not implemented (moderate)

**Evidence:** The abstract states "To address this, we propose a Translation-Aware Contamination Detection framework." The introduction and conclusion similarly present TACD as part of the paper's contribution. Yet Section 5.3 admits "we offer TACD as a forward-looking blueprint rather than a complete implementation."

**Risk:** Including an unimplemented framework as a claimed contribution inflates the paper's apparent scope. The paper's actual scientific contribution is the empirical finding that translation masks contamination while preserving leakage. Labeling TACD as a separate contribution risks reviewer criticism for overclaiming.

**Required action (Must):** Clearly separate the empirical contribution (the finding) from the conceptual proposal (TACD). Relabel Section 5 as "Toward Translation-Aware Contamination Detection: A Proposal" and adjust the abstract and conclusion to avoid implying TACD is a completed contribution.

### W6. Related work section reads as a catalog rather than a structured analysis (minor)

**Evidence:** Section 2 discusses contamination forms, challenges, and detection methods in a paper-by-paper chronological listing style (Sainz 2023 on forms → Li 2023 on Common Crawl → Marone & Van Durme 2023 on Bloom filters → Golchin & Surdeanu 2023a/2023b on guided prompts → Shi et al. 2023 on Min-K% Prob).

**Risk:** The related work does not synthesize methods along comparative axes (e.g., corpus-level vs. model-level detection, required resources, coverage, limitations). This makes it harder for readers to understand where the paper's TS-Guessing extension fits in the landscape.

**Required action (Nice-to-have):** Reorganize Section 2.3 by comparison axes: (i) corpus-level search methods, (ii) model-level probing methods, (iii) hybrid approaches. For each category, state the common limitation regarding cross-lingual contamination that motivates the current study.

### W7. Conclusion introduces untested broad recommendations (minor)

**Evidence:** The conclusion's second paragraph calls for "community-driven efforts to produce and maintain clean pretraining datasets" and "transparent reporting from model developers"—recommendations that have no direct connection to the experiments conducted.

**Risk:** Broad policy recommendations in the conclusion, while not incorrect, dilute the paper's specific empirical contribution and may appear as padding.

**Required action (Nice-to-have):** Replace broad calls with specific, experiment-grounded next steps (e.g., "replicate this analysis for French and Chinese," "develop a validated TACD implementation for the XQuAD benchmark"), and move general recommendations to a broader impacts statement if needed.

## Score
**Final Score: 5/10**

**Rationale:** The paper addresses a timely and important question (multilingual contamination detection) with a reasonably broad experimental design. The core finding—that translation can mask contamination while preserving semantic leakage—has genuine scientific value for the LLM evaluation community. The TS-Guessing extension for MCQ tasks is a thoughtful methodological adaptation.

However, the score is limited by several serious weaknesses that affect the reliability of the central claims:

1. **Experimental confound (W1):** Including English evaluation data in all training conditions means the study never establishes a true contamination-free baseline. This fundamentally weakens the claim about "translation concealing contamination."

2. **Internal contradiction (W2):** Section 4.2 claims flat performance while Table 2 shows substantial gains, creating a direct factual inconsistency that undermines the paper's core thesis.

3. **Missing variance (W3):** Without any statistical reliability indicators, key patterns (especially the claimed "flatness" and the non-monotonic MLQA trends) cannot be distinguished from noise.

4. **Unsupported mechanism (W4):** The embedding analysis central to the explanation is referenced but not shown, leaving the mechanistic interpretation unsubstantiated.

5. **Scope inflation (W5):** TACD is presented as a contribution but is entirely conceptual, inflating the paper's apparent scope beyond what was actually delivered.

**Bottom line:** The paper has promising intuition and a well-motivated research question, but the experimental design confound and internal contradiction prevent the current version from supporting its central claims. With major revisions—particularly a redesigned experiment with held-out evaluation data, proper variance reporting, and careful claim calibration—this work could make a solid contribution. As is, the paper requires substantial strengthening before it meets the bar for publication.

**External literature verification:** Due to Retrieval-Disabled Mode in this review run, novelty and literature comparison conclusions are intentionally deferred. A manual literature search is required to verify whether similar multilingual contamination findings exist and to properly position the paper's novelty relative to prior work.