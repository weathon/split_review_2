Now I have all the calibration information I need. Let me compile the final review.

## Summary

This paper presents a meta-science case study re-examining the evidence from "Turning Up the Heat: MIN-P Sampling for Creative and Coherent LLM Outputs" (Nguyen et al., 2024, ICLR 2025 Oral). Through careful re-analysis across all four lines of evidence in the original paper — human evaluations, NLP benchmarks, LLM-as-a-Judge evaluations, and community adoption claims — the authors identify systematic flaws including omitted data, incorrect statistical testing, selective reporting, and unsubstantiated claims. They also contribute a novel "Best-of-N" methodology for fairly comparing methods by controlling for hyperparameter tuning volume. The paper derives six general lessons for rigorous empirical ML research.

## Strengths

- **Concrete identification of omitted data (Sec. 2.1):** The paper demonstrates that the original authors excluded 1/3 of their human evaluation data (scores for the "basic" sampler) without justification, confirmed by the original authors themselves — a clear, falsifiable finding.

- **Correct statistical re-analysis with multiple-comparison correction (Sec. 2.2, Table 1):** The paper correctly shows that the original authors pooled data across conditions and failed to correct for multiple comparisons. The re-analysis using 12 one-sided paired t-tests with Bonferroni correction, plus the Intersection-Union Test, is appropriate and well-explained. Table 1 crisply demonstrates that the original claim of "consistent" superiority collapses under proper testing.

- **Novel "Best-of-N" methodology for controlling hyperparameter tuning volume (Sec. 3.1):** The subsampling-based analysis that equalizes the number of hyperparameter configurations tested per sampler is a genuinely useful methodological contribution that extends beyond this case study. The analysis across 9 models × 2 stages × 3 seeds × 31 temperatures × 6 hyperparameters (~6000 A100-hours) is substantial.

- **Selective reporting in LLM-as-a-Judge evaluations (Sec. 4.3):** The paper provides specific evidence (a publicly shared Telegram link) that the higher of two scores was reported for min-p (52.01 vs 50.14) while the lower of two was reported for top-p (50.07 vs 50.43) — direct evidence of reporting bias.

- **Community adoption claims retraction (Sec. 5):** The paper documents that the 54k GitHub repositories / 1.1M stars claim was retracted by the original authors after basic sanity-checking, and that 3 of 4 reviewers and the Area Chair cited it as the main justification for acceptance — a striking data point about how unverified claims influence peer review.

## Weaknesses

### Major

- **The NLP benchmark re-analysis covers only GSM8K, not GPQA.** Section 3 explicitly states "Due to our compute budget, we only evaluated GSM8K CoT" (line 150). The original paper used both GSM8K and GPQA, so the claim that "min-p does not outperform other samplers when controlling for hyperparameter volume" (line 165) is strictly limited to GSM8K. While the GSM8K analysis is thorough and convincing on its own terms, the GPQA gap limits the scope of the negative claim about NLP benchmarks.

- **The claimed data-entry error in Table 15 (Sec. 2.4) is asserted but not demonstrated.** The paper states "we believe the correct numerical value should be 5.80" instead of 7.80 (a difference of +2.00 on a 2–10 scale), but does not show the specific calculation or raw data row. For a paper that holds others to high standards of transparency, this claim needs a clear walk-through or explicit acknowledgment that it is an estimate rather than a verified error.

### Minor

- **The LLM-as-a-Judge analysis in Sec. 4.2 partly relies on data described as "(ongoing work to publish)"** (line 189). While Figure 6's caption mentions a public GitHub repository, the phrase is ambiguous about whether the underlying analysis data is fully public. This creates a transparency gap that the paper itself criticizes in the original authors. The paper should clarify what data is public vs. not yet public.

- **The conclusion language occasionally overstates.** The abstract says "min-p sampling improves neither quality, nor diversity, nor the trade-off" and the conclusion says "min-p offers no apparent advantage." These are claims about the method itself rather than about the evidence. The paper convincingly shows the original case is invalid; it does not prove the null across all settings. Tightening this to "the original evidence does not support min-p's claimed advantage" would be more precise.

- **The qualitative annotation in Sec. 2.3 does not report inter-annotator reliability.** The paper says "we manually annotated" without specifying whether multiple annotators were used or whether annotations were performed blindly. For a section that critiques qualitative analysis, this should be transparent.

- **The Best-of-N subsampling controls for number of randomly sampled configurations, but this is not identical to controlling for actual tuning effort** (systematic validation-set tuning). The paper could be more upfront about this distinction, although the analysis is still informative.

### Trivial

None.

## Nice-to-Haves

- Run the Best-of-N sweep on GPQA with a smaller model or fewer configurations, or explicitly scope the NLP benchmark claim to GSM8K.
- Demonstrate the Table 15 error with the specific raw data row that produces 5.80.
- Report inter-annotator reliability for the qualitative annotation.
- A brief discussion of any settings (if any exist) where min-p genuinely provides value would strengthen credibility.

## Removed Points

These points are flagged to be removed, treat them with caution:
- "The list of 20+ cited scandals is somewhat performative (many are blog posts and non-peer-reviewed critiques)" — style opinion, not a substantive weakness. Removed.
- "The paucired t-tests assume normality; with df=52 this is likely fine, but a non-parametric alternative would be more conservative" — speculative, not an identified flaw. Removed.
- Section-by-section presentation notes from the harsh critic that don't rise to the level of weaknesses. Removed.

## Novel Insights

None beyond the paper's own contributions. The harsh critic's review does not surface a novel analytical lens that the paper itself does not already provide.

## Suggestions

1. Explicitly scope the NLP benchmark claim to GSM8K or extend the analysis to GPQA.
2. Clarify the public availability status of the LLM-as-a-Judge data (Sec. 4.2).
3. Demonstrate the Table 15 error with a transparent calculation from the raw data.
4. Tighten conclusion language to reflect claims about evidence rather than about the method itself.
5. Report inter-annotator reliability for the qualitative annotation in Sec. 2.3.

## Score and Decision

**Calibration anchors retrieved (across all rounds):**

| Path | Avg Score | Round | Itemized? | Comparison |
|------|-----------|-------|-----------|------------|
| P49gSPmrvN.md | 1.00 | R1 | No | Unrelated low-quality paper |
| nSDOkm0SKo.md | 1.00 | R1 | No | Unrelated low-quality paper |
| bEgDEyy2Yk.md | 1.00 | R1 | No | Unrelated low-quality paper |
| Uj0h13lVrR.md | 1.00 | R1 | No | Unrelated low-quality paper |
| CpiOUOaqh3.md | 2.00 | R1 | No | Unrelated |
| FYvZCwdb6F.md | 3.00 | R1 | No | Unrelated |
| w2C7gJqaai.md | 2.33 | R1 | No | Unrelated |
| fM1ETm3ssl.md | 3.00 | R1 | No | Unrelated |
| GbEmJmnQCz.md | 4.40 | R1 | Yes | Most structurally similar — a re-analysis of "Is Memorization Actually Necessary for Generalization?" finding methodological errors. My paper has stronger concrete contributions (Best-of-N methodology, specific documented flaws) and milder weaknesses. |
| lf8QQ2KMgv.md | 3.75 | R1 | Yes | Same paper, second version. My paper is clearly stronger on execution and contribution clarity. |
| 5cPEkoHHyG.md | 3.67 | R1 | No | Unrelated |
| py54X6mAEy.md | 4.00 | R1 | No | Unrelated |
| m2NVG4Htxs.md | 6.75 | R1 | Yes | Meta-science about LLM data contamination. Stronger paper overall with broader findings. My paper's scope is narrower but its findings are more concretely verified. |
| 3lDxKQepvn.md | 5.75 | R1 | No | Unrelated |
| g16vmAtJ8x.md | 6.00 | R1 | Yes | Critique of privacy metrics + novel attack. Comparable quality: my paper has slightly weaker top strengths (+5.48 vs +6.82) but much milder weaknesses (-4.20 vs -10.29). |
| QGGNvKaoIU.md | 7.00 | R1 | No | Unrelated |
| EUSkm2sVJ6.md | 7.60 | R1 | No | Unrelated |
| A3YUPeJTNR.md | 8.00 | R1 | No | Unrelated |
| jOmk0uS1hl.md | 8.00 | R1 | Yes | Strong meta-science paper on evaluation methodology. My paper is not at this level of breadth or novelty. |
| PdaPky8MUn.md | 8.00 | R1 | No | Unrelated |
| bwZ9xh178a.md | 6.00 | R2 | No | Unrelated |
| upALuXjdxc.md | 6.00 | R2 | No | Unrelated |
| kz5igjl04W.md | 5.50 | R2 | No | Unrelated |
| RW37MMrNAi.md | 5.60 | R2 | No | Unrelated |
| jdynlBj3b0.md | 6.25 | R2 | No | Unrelated |

**Bracket reasoning:** Round 1 established that the most structurally similar anchors (re-analysis of prior published work) cluster in the 3.75–6.00 range. The "Is Memorization Actually Necessary for Generalization?" papers (4.40, 3.75) share the re-analysis structure but have weaker contribution clarity and more severe over-claiming issues. My paper has clear novel contributions (Best-of-N at +5.48 weight) and the weaknesses are bounded (max -4.20 for GPQA gap, vs -8.99 and -7.74 in those anchors). The privacy metrics critique (6.00) provides a useful upper anchor — my paper has comparable strength in its critique but a less severe fatal flaw (-4.20 vs -10.29). Round 2 confirmed that no re-analysis paper of similar style received above 6.00 from human reviewers. The round-1 bracket was (4.40, 6.00), and the weighted-item comparison places this paper above the 4.40 anchor (stronger strengths, much milder weaknesses) but below the 8.00 anchors in breadth and novelty. The final score of **6.0** reflects a paper with genuine, well-supported contributions and bounded, addressable weaknesses.

MY FINAL SCORE: <score>6.0</score>
MY FINAL DECISION: <decision>Accept</decision>