Now let me verify a few more specific claims from the reviewer.Now I have a thorough understanding of the paper. Let me draft the review before calibration.Now let me run the calibration search — Round 1 bracketing.Let me read a few key anchor papers for calibration, especially the critique/replication papers.Now I have strong calibration anchors. Let me form my bracket.

**Round 1 Bracket Analysis:**

- **Score < 1.5 papers**: Clearly bad (hypothetical scenarios, pure surveys) — the min-p critique paper is vastly better. Eliminated.
- **Score 1.5-3.5**: Papers with major contribution or methodology issues. The min-p paper is clearly above this band.
- **Score 3.5-5.5**: The "Is Memorization Actually Necessary for Generalization?" papers (3.75 and 4.40) are the most directly comparable — they are critique/replication papers that identify methodological errors in prior work. However, those papers were criticized for "minimal contribution" and limited replication scope. The min-p paper is substantially stronger: it introduces novel methodology (hyperparameter equalization), covers 4 lines of evidence, invests ~6000 A100-hours.
- **Score 5.5-7.5**: "On Evaluating Durability of Safeguards" (6.50) is a critique paper that was accepted. The min-p paper has more comprehensive evidence and a novel reusable methodology.
- **Score 7.5-8.5**: "Training on the Test Task" (8.00) and "Never Train from Scratch" (8.00) are strong methodological critique papers with unanimous 8s. Both propose novel, broadly applicable methodologies. The min-p paper has a similar contribution but is narrower (case study of one paper) and has the GSM8K-only limitation.

**Initial bracket: 6.0–8.0**

Now let me write the final review.

---

## Summary
This paper provides a comprehensive re-examination of "Turning Up the Heat: Min-P Sampling" (Nguyen et al., 2024), an ICLR 2025 Oral. Through four independent lines of inquiry—re-analyzing human evaluations, conducting extensive NLP benchmark sweeps, scrutinizing LLM-as-a-Judge evaluations, and verifying community adoption claims—the authors demonstrate that the original paper's evidence does not support min-p's claimed superiority over existing sampling methods. The paper introduces a novel "Best-of-N" hyperparameter volume equalization methodology and extracts general methodological lessons for empirical ML research.

## Strengths

- **Discovery of omitted human evaluation data is concrete and consequential (Section 2.1).** One-third of collected human evaluation scores (the basic sampler condition) were excluded without mention or justification. The authors publicly confirmed this with the original authors. Including the omitted data changes the paper's conclusions—a clear-cut data transparency failure with material impact on the original paper's claims.

- **Statistical re-analysis is methodologically rigorous (Section 2.2, Table 1).** The application of 12 one-sided paired t-tests with Bonferroni correction is well-matched to the original paper's claim of "consistently" outperforming baselines. The result—only 1 of 12 comparisons survives Bonferroni at α=0.05 and 0/12 at α=0.01—directly undermines the original headline conclusion. The Intersection-Union Test for the "consistently outperforms" claim is a particularly appropriate statistical choice.

- **Hyperparameter volume equalization is a genuinely novel and reusable contribution (Section 3, Figs 4-5).** The Best-of-N analysis—subsampling equal numbers of hyperparameters per sampler and plotting maximum performance as a function of sweep size—is an elegant, practical methodology for detecting whether a method's advantage stems from more tuning rather than intrinsic superiority. The investment of ~6000 A100-hours across 9 models, 4 samplers, 31 temperatures, and 3 seeds demonstrates substantial effort and the results are compelling: min-p's advantage converges to zero or turns negative as hyperparameter budgets are equalized.

- **Manual annotation of qualitative responses reveals a concrete contradiction (Section 2.3, Fig 2).** Re-reading evaluators' free-text preferences shows "basic" was actually the most-preferred sampler (21 evaluators vs. 12 for min-p), directly contradicting the original paper's characterization that participants "frequently noted" min-p was preferred.

- **Community adoption debunking is decisive (Section 5).** The finding that claimed 1.1M GitHub stars exceeds the combined stars of all major LM repositories, that the search methodology produced false positives, and that both claims were retracted, is cleanly demonstrated. The observation that 3 of 4 ICLR reviewers cited these retracted numbers as their main justification for endorsement is a sharp commentary on the review process.

- **Selective reporting finding is specific and verifiable (Section 4.3).** The original Table 3(b) reported the higher of two win rates for min-p (52.01 at p=0.05 vs. 50.14 at p=0.01) but the lower of two for top-p (50.07 at p=0.9 vs. 50.43 at p=0.98).

## Weaknesses

### Fatal
None

### Major
- **The most novel methodology (hyperparameter volume equalization) is demonstrated on only one benchmark (Section 3.1).** The original paper evaluated min-p on both GSM8K and GPQA (line 121), but this paper's sweep covers only GSM8K (line 150: "Due to our compute budget, we only evaluated GSM8K CoT"). GSM8K is a math reasoning task, which is arguably not the strongest domain for testing a sampling method whose claimed advantage is in creative generation. The conclusion that "min-p does not outperform other samplers when controlling for hyperparameter volume" is well-supported for GSM8K but not independently verified on other task types. The authors are transparent about this limitation, but it meaningfully bounds the generalizability of their central novel contribution.

### Minor
- **Section 4.2 rests partly on unpublished analysis.** The text explicitly states insights were derived from "closely scrutinizing (ongoing work to publish) the data" (line 189). While the hyperparameter asymmetry (Fig. 6, left) and selective reporting (Section 4.3) are independently verifiable from public data, the "ongoing work to publish" framing weakens this section relative to the other three lines of critique.

- **The "blueprint" framing slightly overpromises relative to the actual novelty of the extracted lessons.** The six lessons in Section 6 (correct for multiple comparisons, report all data, ensure reproducibility, etc.) are individually well-established principles from introductory statistics and experimental design courses. The paper's genuine contribution is the concrete demonstration that these principles were violated with material consequences in a high-profile paper, plus the hyperparameter volume equalization methodology. The gap between the ambitious title/framing and the actual novelty of the codified lessons is a presentation issue, not a substantive flaw.

### Trivial
None

## Nice-to-Haves
- A brief theoretical discussion of min-p's adaptive truncation mechanism and why it might or might not be expected to outperform alternatives would round out the analysis, though this is outside the paper's stated scope as a methodological critique.
- Formalizing the Best-of-N hyperparameter equalization as a standalone protocol with explicit guidance on subsampling strategy, minimum sweep sizes, and interpretation of the resulting curves.
- A power analysis for the human evaluations to distinguish "min-p is indistinguishable from baselines" from "the studies were underpowered to detect small effects."
- Extending the benchmark evaluation to at least one creative generation or open-ended task.

## Removed Points
*These points are flagged to be removed; treat them with caution.*

- **"The paper does not engage with the theoretical mechanism of min-p"** — Demoted from weakness to nice-to-have. The paper explicitly scopes itself as a methodological re-analysis/critique, not a theoretical investigation. Demanding theoretical analysis of min-p's mechanism is scope creep; the paper's stated goal is to test whether the *evidence* supports the *claims*, not to develop a theory of when min-p should work.

- **"The introduction's litany of ML scandals risks adversarial framing"** — Removed as a stylistic/presentation choice. The 13+ citations provide factual context for the paper's motivation and are relevant to framing this as a systemic problem.

- **"Light editing of hyperparameters could disadvantage one sampler"** — Removed as speculative. The paper states edits were to make values "more evenly distributed" (line 133), which is a fairness-motivated choice. No evidence this disadvantaged any specific sampler, and making hyperparameters more evenly distributed is standard practice.

- **"Section 2.4's new human evaluation involved multiple simultaneous methodological changes"** — Removed. Section 2.4 discusses the *original authors'* new human evaluation study, not this paper's methodology. The complexity of the original authors' revised study is their issue; this paper correctly reports on it.

- **"'invalidated by its own data' may overstate the case for LLM-as-a-Judge section"** — Partially valid but minor. Three of four lines of evidence strongly support "invalidated"; the LLM-as-a-Judge section is weaker but still provides corroborating evidence. The abstract's language is aggressive but defensible given the totality of the findings.

## Novel Insights
The hyperparameter volume equalization methodology ("Best-of-N" analysis) is a genuinely novel and practically reusable contribution. The key insight it operationalizes—that a method's apparent superiority can be an artifact of asymmetric hyperparameter search rather than intrinsic quality—has been discussed informally but never, to this paper's credit, formalized into a concrete, visual methodology with clear interpretation. The paper also provides a valuable demonstration of how omitted data, incorrect statistical testing, mischaracterized qualitative feedback, and unsubstantiated claims can compound in a single high-profile publication to create a misleading picture—a case study whose individual components are well-known failure modes but whose comprehensive co-occurrence in a single top-ranked paper is instructive.

## Suggestions
- Extend the Best-of-N hyperparameter equalization analysis to at least one additional benchmark—ideally a creative generation or open-ended task where min-p's advantages are most claimed—even if the sweep is smaller.
- Either complete the "ongoing work to publish" analysis referenced in Section 4.2 or explicitly delineate what conclusions the section can and cannot support with currently available evidence.
- Consider tempering the "blueprint" framing (particularly the title) to better match the paper's actual contribution: a rigorous case study with a novel methodology, rather than a general guide to standard best practices.
- Include a power analysis for the human evaluations to quantify whether the sample sizes were sufficient to detect plausible effect sizes for sampling method differences.

## Score and Decision

### Calibration Anchors (all rounds)

| Paper | Avg Score | Round | Comparison |
|-------|-----------|-------|------------|
| nSDOkm0SKo (Financial Markets NN) | 1.00 | R1 | Clearly worse — hypothetical scenario, no real contribution |
| 8QTpYC4smR (LLM Survey) | 1.00 | R1 | Clearly worse — pure survey, no novel analysis |
| P49gSPmrvN (UMAP Scientific Discourse) | 1.00 | R1 | Clearly worse — minimal contribution |
| 5kMwiMnUip (Jailbreaking LLMs) | 1.40 | R1 | Clearly worse — weak methodology |
| x8mr9zGkpr (Dataset Complexity vs Hyperparameters) | 3.00 | R1 | Worse — limited contribution, basic methodology |
| XWfjugkXzN (Sampling Info Sets) | 1.67 | R1 | Clearly worse |
| u8L1zzGXRq (Drug Response Predictions) | 3.00 | R1 | Worse — benchmarking without novel methodology |
| lZRRfupxYn (Mesoscience Model Generalizability) | 3.00 | R1 | Worse — unclear contribution |
| kiwyQsZIGP (Few-Shot Learning Benchmarks) | 5.00 | R1 | Worse — the min-p paper has stronger evidence and novel methodology |
| **lf8QQ2KMgv (Is Memorization Necessary?) | 3.75** | R1 | **Most comparable: also a critique/replication paper. The min-p paper is substantially stronger — it introduces novel methodology, covers 4 lines of evidence, and invests ~6000 A100-hours vs. being criticized for "minimal contribution."** |
| **GbEmJmnQCz (Is Memorization Necessary? v2) | 4.40** | R1 | **Same paper, slightly higher scoring version. Still weaker than the min-p paper for the same reasons.** |
| esh9JYzmTq (RL Distribution Shift) | 4.67 | R1 | Comparable methodology focus but less impactful findings |
| **fXJCqdUSVG (Durability of LLM Safeguards) | 6.50** | R1 | **Similar in spirit — critique paper evaluating prior claims. The min-p paper has more comprehensive evidence and a novel reusable methodology, suggesting it should score at or above this.** |
| Q2bJ2qgcP1 (CATE Benchmark) | 6.00 | R1 | Comparable contribution level but different domain |
| yuy6cGt3KL (Causal Effect Model Selection) | 7.25 | R1 | Strong empirical analysis paper; the min-p paper is comparable in rigor |
| xI71dsS3o4 (Scaling Laws Survey) | 5.75 | R1 | The min-p paper is stronger — more novel methodology and more consequential findings |
| KbetDM33YG (Online GNN Evaluation) | 8.00 | R1 | Different domain; the min-p paper has comparable rigor but narrower scope |
| **jOmk0uS1hl (Training on Test Task) | 8.00** | R1 | **Most aspirational comparison: also a methodological critique showing evaluation confounds. That paper has broader applicability (general evaluation problem vs. single-paper case study). The min-p paper is slightly below this.** |
| uHLgDEgiS5 (Temporal Data Influence) | 8.00 | R1 | Different focus; the min-p paper is slightly below |
| **PdaPky8MUn (Never Train from Scratch) | 8.00** | R1 | **Also a fair-comparison methodology paper. That paper has broader scope and more general implications. The min-p paper is slightly below this.** |

### Bracket Narrowing

**Round 1 bracket: 6.0–8.0.** The paper is clearly above the rejected memorization critique papers (3.75–4.40) due to its novel methodology and comprehensive evidence. It is comparable to or slightly above the accepted safeguards critique paper (6.50). It falls slightly below the unanimously accepted methodological critique papers at 8.0, which had broader scope and more general applicability.

**Narrowing within bracket:** The paper's strengths (novel hyperparameter equalization methodology, comprehensive 4-line critique, ~6000 A100-hours of compute, concrete verifiable findings including retracted claims) push it above the borderline-accept 6.0 level. However, the single-benchmark limitation for the most novel contribution, the partially incomplete Section 4, and the narrow scope (case study of one paper) prevent it from reaching the 8.0 level of papers like "Training on the Test Task" or "Never Train from Scratch." The paper most naturally sits in the 7.0 range — a solid accept with acknowledged limitations.

**Final score: 7.0**

The paper makes a genuine, well-supported contribution through its novel hyperparameter volume equalization methodology and its comprehensive, rigorous demonstration that a high-profile publication's evidence does not withstand scrutiny. The single major weakness (GSM8K-only benchmark evaluation) is a real limitation on generalizability but does not invalidate the paper's core findings. The paper should be accepted.

MY FINAL SCORE: <score>7.0</score>
MY FINAL DECISION: <decision>Accept</decision>