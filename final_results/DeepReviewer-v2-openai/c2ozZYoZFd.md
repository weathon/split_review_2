## Summary
This paper presents a forensic case study of "Turning Up the Heat: MIN-P Sampling for Creative and Coherent LLM Outputs" (Nguyen et al., 2024), a high-visibility ICLR 2025 Oral paper that introduced `min-p` sampling for LLMs. The current paper re-analyzes the original's four lines of evidence — human evaluations, NLP benchmarks, LLM-as-a-Judge evaluations, and community adoption claims — and argues that none support the claimed superiority of `min-p`. From this case study, the paper distills general lessons for rigorous empirical ML research: controlling for hyperparameter volume, applying correct statistical testing, ensuring data transparency, scrutinizing qualitative summaries, requiring methodological clarity, and watching for selective reporting.

**Overall assessment:** The paper's forensic work is valuable and exposes genuine methodological flaws in a high-profile publication. However, the paper itself exhibits several of the same rigor issues it criticizes — overclaiming the novelty of its methodology, providing insufficient transparency for some of its own evidence, and using logically flawed verification arguments. The "blueprint" contribution is primarily a restatement of existing best practices rather than a novel framework. The paper would benefit from tempering its methodological novelty claims, strengthening the evidence chain for its most serious accusations (selective reporting), and acknowledging the limitations of its own analyses. With these revisions, the paper could serve as a useful teaching case for research methodology in ML.

**Novelty note (Retrieval-Disabled Mode):** External literature verification was unavailable in this run. Novelty claims about the Best-of-N methodology and comparisons to existing reproducibility guidelines are deferred for manual verification.

## Strengths
1. **Timely and relevant topic.** The paper addresses a genuine need for methodological rigor in ML research, and the choice of a high-profile ICLR Oral paper as a case study ensures visibility and impact. The detailed line-by-line deconstruction of the original paper's evidence is a valuable educational exercise.

2. **Comprehensive coverage of evidence lines.** The paper examines all four types of evidence from the original paper, providing a thorough audit trail. The re-analysis of human evaluation data with proper multiple-comparison correction (Bonferroni, IUT) is technically sound and clearly presented in Table 1.

3. **Substantial experimental effort.** The GSM8K sweep across 9 models, 2 stages, 4 samplers, 31 temperatures, and 6 hyperparameters per sampler represents a significant computational investment (~6000 A100-hours). The Best-of-N analysis framework for controlling hyperparameter volume is a practical methodological contribution that could be adopted by future work.

4. **Effective use of data transparency.** The paper demonstrates the value of open data by discovering the omitted basic-sampler scores in the original study's publicly posted data. This finding alone (1/3 of data excluded without justification) is a significant methodological critique.

5. **Clear statistical re-analysis.** The hypothesis testing table (Table 1) with and without Bonferroni correction, plus the IUT analysis, provides a model of how to rigorously re-evaluate published claims. The distinction between "significant in a pooled test" and "consistently outperforms across all settings" is well-articulated.

6. **Identification of selective reporting.** The discovery that the original paper may have selected favorable hyperparameter results for min-p while reporting less favorable ones for top-p (Section 4.3) is the most serious finding and, if verified, raises concerns beyond methodological sloppiness.

## Weaknesses
### W1. Overclaiming methodological novelty (major)

The paper claims to "develop a novel methodology for fairly comparing methods that require extensive hyperparameter tuning" (Page 1 - Introduction, closing paragraph). However, the Best-of-N analysis used in Section 3 is an adaptation of existing resampling approaches (Nakano et al., 2021; Stiennon et al., 2020) applied to a new domain. The adaptation is a straightforward use of subsampling to equalize evaluation budgets, not a new statistical framework. This overclaim undermines the paper's own call for rigor, as it uses the same kind of novelty inflation it criticizes in others. The paper should replace "novel methodology" with "adapted methodology" or "application of" and clearly attribute the original methods.

### W2. Insufficient evidence chain for selective reporting claim (major)

The paper's most serious accusation — that the original authors selectively reported favorable results for min-p and unfavorable ones for top-p (Section 4.3, Page 7) — relies on a Telegram link shared by the first author. Telegram links are not stable, citable sources. The paper does not describe what the link contained (screenshot, spreadsheet, chat message), does not archive the evidence, and does not provide independent verification. For a paper that demands data transparency, this evidence chain is itself opaque. **Required action:** Archive the Telegram communication as an appendix exhibit (screenshot or archived message), or downgrade the claim strength and acknowledge that it is based on personal communication pending independent verification.

### W3. Logically flawed GitHub star verification (major)

Section 5 attempts to verify the original paper's claim of "1.1 million stars" by summing the stars of leading LM repositories (transformers, ollama, llama.cpp, etc.) and noting that they sum to only 453K. This verification attempt is logically flawed: the original claim was that projects *using* min-p collectively have 1.1M stars, not that min-p's own repository or any particular set of repositories has that many stars. Summing stars of unrelated major repositories (some of which may or may not use min-p) is not a valid sanity check. The stronger evidence is that the original authors retracted the claim after acknowledging false positives from searching for the string "min-p." The attempted numerical verification should be removed or corrected.

### W4. Methodological transparency gaps in the current paper's own analyses (major)

Despite demanding full data transparency from others, the current paper has several transparency gaps:

- **Qualitative annotation methodology (Section 2.3, Page 3):** The paper reports manually annotating human evaluators' qualitative responses but provides no information about who annotated, what annotation scheme was used, inter-annotator reliability, or how ambiguous responses were resolved. This is the same type of opaque qualitative analysis the paper criticizes.

- **Numerical discrepancy verification (Section 2.4, Page 4):** The paper claims a 2.0-point error in the original's Table 15 (7.80 vs 5.80) but does not provide the recomputation path. The reader cannot verify whether this is indeed an error or a misunderstanding.

- **Hyperparameter counting methodology (Section 4.2, Page 7):** The paper reports that min-p received ~25 hyperparameter configurations vs ~11 for top-p and ~2 for basic, but does not define how configurations were counted or provide exact numbers.

### W5. Missing experimental reproducibility details (major)

Section 3.1 describes a ~6000 A100-hour experiment but omits critical methodological details: the number of generations per model-sampler-temperature-hyperparameter combination, the method for aggregating Exact Match scores across seeds, and the specification of the two prompt formats. Without these details, the experiment cannot be independently reproduced. These omissions are particularly problematic given that the paper's Lesson 5 calls for "methodological clarity for full reproducibility."

### W6. New human evaluation confounds not acknowledged (major)

Section 2.4 lists six simultaneous methodological changes in the new human evaluation study (implementation, participants, hyperparameters, reading time, text type, rubric), but does not acknowledge that these multiple confounds limit the conclusions that can be drawn. The paper presents the new study as supporting its conclusion ("min-p does not outperform baselines"), but a skeptic could attribute the different outcome to any of the six changes. The analysis should explicitly note this limitation and recommend a controlled replication.

### W7. Reliance on author communication as evidence (moderate)

Section 2.2 relies on "the authors said publicly to ignore this particular low diversity condition" as evidence for the claim that top-p's hyperparameter was poorly chosen. This is an appeal to authority that conflicts with the paper's own emphasis on evidence-based analysis. An independent, principle-based justification (e.g., explaining why p=0.1 severely truncates the distribution) would strengthen the argument.

### W8. Blueprint lessons overlap with existing guidelines (moderate)

The six general lessons in Section 6 are presented as a novel "blueprint" but several overlap substantially with existing reproducibility guidelines (e.g., ML Reproducibility Checklist, ReproGen guidelines). The paper does not position its lessons relative to prior work, making it difficult to assess what is truly new versus a restatement. Acknowledging this overlap and identifying which lessons are operationalized differently would improve the paper's scholarly positioning.

### W9. Crisis-framing citation list is unfocused (minor)

The opening paragraph of the Introduction (Page 1) uses a dense citation wall (19 citations in one sentence) without categorization, narrative arc, or clear connection to the specific methodological issues addressed. This reduces readability and can be perceived as performative rather than substantive.

### W10. One-sided testing choice could be more complete (minor)

The statistical re-analysis uses one-sided t-tests (testing only whether min-p > baseline). While justified by the original paper's directional claim, the analysis could be strengthened by also reporting two-sided tests or equivalence tests (TOST) to show that no sampler is systematically better or worse. This would provide a more complete picture and guard against the appearance of analysis bias.

## Score
**Final Score: 5/10**

**Scoring rationale:** This paper has genuine value as a methodological case study and demonstrates important flaws in a high-profile publication. The forensic work on the human evaluation data, particularly the discovery of omitted data and the correct application of multiple-comparison correction, is a meaningful contribution to research methodology discourse. However, the paper is weakened by several self-undermining issues: it overclaims methodological novelty while using established techniques, it demands transparency from others while providing insufficient detail for some of its own analyses, and it includes a logically flawed verification argument (the GitHub stars calculation). The "blueprint" contribution largely restates existing best practices rather than offering a novel framework. The most serious finding (selective reporting in LLM-as-a-Judge) lacks a sufficiently documented evidence chain. These issues reduce the paper's scientific credibility relative to its stated ambitions.

**Post-Revision Target: 6-7/10** — achievable by addressing the major weaknesses documented above (correcting novelty claims, archiving evidence for selective reporting, fixing the GitHub analysis, adding methodological transparency for the qualitative annotation, and acknowledging confounds in the new human evaluation).

**Novelty note:** External literature verification was unavailable in this run (Retrieval-Disabled Mode). Novelty comparisons to existing reproducibility guidelines and the Best-of-N methodology are deferred for manual verification.