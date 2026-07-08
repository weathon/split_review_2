Now I have all the calibration data I need. Let me construct the final review.

**Round 1 bracket reasoning:** The closest anchors are the "Is Memorization Actually Necessary for Generalization?" papers (avg 3.75 and 4.40), which are re-analysis critiques of published work — directly analogous to this paper. However, this paper is more comprehensive (4 evidence lines vs 3 methodological errors), includes a novel methodological contribution (Best-of-N), and has irrefutable factual findings (data omission, community adoption retraction). It also has less severe weaknesses (weakest weights: -0.43, -1.14 vs -2.74, -3.99, -2.40 for the memorization papers). These comparisons suggest this paper should score above 4.40.

**Round 2 bracket reasoning:** I examined the Knowledge Localization paper (avg 7.50) as a higher-scoring critique+contribution paper. That paper proposes a new assumption and method alongside its critique, whereas this paper's novel contribution (Best-of-N) is more of a methodological tool. Combined with the weak LLM-as-a-Judge section and single-benchmark analysis, this paper sits below 7.50.

**Final score placement:** The paper is clearly stronger than the memorization re-analysis anchors (3.75-4.40) — its positive item weights are higher (max 11.09 vs 10.79) and its negative weights are milder (-1.14 vs -3.99). It falls short of the Knowledge Localization paper (7.50) because that paper proposes a new substantive scientific assumption alongside its critique, while this paper's novel component (Best-of-N) is a methodological tool, and it has a structurally weak section (LLM-as-a-Judge). Score of **6.5** — between borderline accept and accept.

## Summary

This paper re-examines all four lines of evidence from Nguyen et al. (2024)'s ICLR 2025 Oral paper on min-p sampling, which claimed that min-p achieves superior quality and diversity over existing samplers. Through re-analysis of the original human evaluation data, extensive NLP hyperparameter sweeps (~6000 A100-hours), investigation of LLM-as-a-Judge evaluations, and verification of community-adoption claims, the paper demonstrates that the original paper's conclusions are not supported by its own data. The paper also introduces the Best-of-N methodology for fairly comparing methods with different hyperparameter search spaces.

## Strengths

- **Irrefutable documentation of data omission (Section 2.1):** The paper establishes that scores for one of three baseline samplers (basic sampling) — comprising one-third of the total human evaluation data — were excluded without justification, publicly confirmed with the original authors. The Camera Ready version added the data back without updating conclusions. This is a clean, independently verifiable factual finding.

- **Correct statistical re-analysis with proper multiple-comparisons correction (Section 2.2, Table 1):** Twelve one-sided paired t-tests with Bonferroni correction show only 1 of 12 comparisons survives correction at α=0.05 (0 of 12 at α=0.01). The Intersection-Union Test framing is a useful additional lens. This constitutes clean evidence that the original claim of "consistent" superiority is unsupported by the paper's own data.

- **Extensive hyperparameter sweep with novel Best-of-N methodology (Section 3):** ~40,000 individual evaluations across 9 models × 2 stages × 4 samplers × 31 temperatures × 6 hyperparameters × 3 seeds, requiring ~6000 A100-hours. The Best-of-N hyperparameter-volume equalization technique is a practical methodological contribution that could be adopted broadly for fair comparison of methods with different search-space sizes.

- **Documentation of retracted community-adoption claims (Section 5):** The paper verifiably shows that claims of 54,000 GitHub repositories and 1.1M stars were false and were retracted after the current authors raised the issue. The observation that 3 of 4 ICLR 2025 reviewers and the Area Chair cited these retracted numbers as their main justification for acceptance is a striking finding about the review process.

## Weaknesses

### Fatal
None.

### Major
- **LLM-as-a-Judge section has an evidentiary gap for the most serious claim (Section 4.3):** The selective-reporting allegation — that the higher of two scores was reported for min-p while the lower was reported for top-p — rests entirely on a single Telegram link described as "publicly shared" by the first author. The paper provides no details about how this link was obtained, whether it was archived, whether it can be independently verified, or whether there is any written correspondence corroborating the claimed score selection. For an accusation of selective reporting (potentially bordering on scientific misconduct), this evidence is thin. Additionally, the section is described as "ongoing work to publish" (line 189), signaling the analysis is incomplete. This is the weakest pillar in an otherwise strong four-part argument.

### Minor
- **NLP benchmark analysis covers only one task type (Section 3):** The extensive sweep covers GSM8K (CoT) only, citing compute budget (~6000 A100-hours), but the original paper also evaluated on GPQA (5-shot). The central negative result — that min-p does not outperform when hyperparameter volume is controlled — is only established for a single benchmark in mathematical reasoning. The paper acknowledges this limitation but does not argue why GSM8K alone is sufficient to draw conclusions about the original paper's broader NLP benchmark claims.

- **Human evaluation re-analysis focuses on the high-diversity setting only (Section 2.2):** The paper restricts analysis to the "high" diversity setting, excluding "low diversity." While the paper provides three reasonable justifications (min-p's claimed advantage is in high quality+diversity, original authors recommended it, top-p's p was poorly chosen in low diversity), this means the critique covers a subset of the original experimental conditions while inferring that min-p does not outperform in "any" condition. Would be stronger if all conditions were analyzed (with appropriate adjustments for the disadvantageous top-p hyperparameter).

- **The "blueprint" framing overstates the novelty of the general lessons (Sections 1, 6):** The paper's title and framing promise a "Blueprint for More Rigorous Science," but the six general lessons listed (control hyperparameter volume, use correct statistical testing, practice data transparency, scrutinize qualitative summaries, ensure methodological clarity, avoid selective reporting) are well-established best practices. The paper's real contribution is the rigorous demonstration of failures in a high-profile case, not the discovery of new methodological principles. The one genuinely novel methodological contribution is the Best-of-N technique.

- **Partially verified data-error claim without sufficient documentation (Section 2.4):** The paper states "we believe one value is incorrectly reported... we believe the correct numerical value should be 5.80." The hedging language ("we believe") and lack of detailed reconciliation with the original data make this a weak claim. Either the value is wrong or it is not; presenting it as an unverified belief undercuts the paper's own evidentiary standards.

### Trivial
None.

## Nice-to-Haves

- The selective-reporting claim in Section 4.3 should be either fully substantiated (archival screenshots, written correspondence, independent verification) or downgraded from a finding to a suspicion.
- Expanding the NLP benchmark analysis to GPQA, or clearly arguing why GSM8K is sufficient, would strengthen the conclusions.
- An explicit disclosure statement about the authors' relationship to the original work or its review process would strengthen credibility given the adversarial framing.
- The Best-of-N subsampling sensitivity to the specific set of hyperparameter values could be discussed; the 6 values per sampler were "lightly edited" from the original paper (line 133).

## Removed Points

- *Adversarial tone/self-referential citations*: REMOVED — style/presentation nitpick, not substantive.
- *Missing disclosure of relationship to original work*: MOVED to Nice-to-Haves — not a core flaw.
- *Bonferroni vs Benjamini-Hochberg discussion*: REMOVED — even without correction, only 5/12 tests are significant, so choice of correction method does not change conclusions.
- *Paper does not comment on whether min-p has any value*: REMOVED — the paper does comment on this (Section 6: "While min-p is useful as another method to try"). Claim is factually incorrect.
- *General lessons could be sharpened/reduced overlap*: REMOVED — presentation preference, not a weakness.
- *Best-of-N subsampling sensitivity*: MOVED to Nice-to-Haves — reasonable technical question, not a demonstrated flaw.

## Novel Insights

The most incisive observation emerging from the review is the structural asymmetry in evidence quality across the paper's four lines of argument. Sections 2 (human evaluations) and 5 (community adoption) are factually airtight with independently verifiable claims from published data. Section 3 (NLP benchmarks) is thorough and introduces a novel methodology. But Section 4 (LLM-as-a-Judge) is substantially weaker — it is the section the paper itself labels as "ongoing work," and it is also the section making the most serious allegation (selective reporting of scores) on the thinnest evidence (a single unarchived Telegram link). This creates an uneven foundation where the weakest evidence supports the most damaging claim, which the authors should address before publication.

## Suggestions

1. **Strengthen the LLM-as-a-Judge section:** Either substantiate the selective-reporting claim with archived evidence (screenshots, correspondence, independent verification) or explicitly downgrade Section 4.3 from a finding to a suspicion/concern. The current treatment is disproportionate to the evidence.
2. **Acknowledge the single-benchmark limitation more explicitly in the conclusions:** Reframe "min-p does not outperform" to "min-p does not outperform on GSM8K when hyperparameter volume is controlled" and discuss whether GPQA might differ.
3. **Either substantiate or remove the "5.80" data-error claim in Section 2.4:** Presenting unverified beliefs undercuts the paper's otherwise rigorous evidentiary standards.
4. **Tone down the "blueprint" framing:** The paper's contribution is a thorough case study demonstrating common methodological failures, not a novel set of scientific principles. The title and abstract should reflect this.

## Score and Decision

Round 1 bracket (based on comparison with memorization re-analysis anchors scoring 3.75-4.40): This paper is more comprehensive, includes a novel method, and has less severe weaknesses — **above 4.40**.

Round 2 bracket (narrowed by comparison with Knowledge Localization anchor at 7.50): That paper proposes a new scientific assumption alongside its critique, while this paper's novel component is narrower (Best-of-N methodology) and has a structurally weak section (LLM-as-a-Judge). This paper also addresses meta-science/rigor, a topic that traditionally scores lower than core technical contributions. — **below 7.50**.

Final score **6.5**: The paper's strongest items (NLP sweep + Best-of-N at weight 11.09, correct statistics at 9.31, selective reporting documentation at 9.14, community adoption at 8.81) exceed those of the 3.75-4.40 memorization anchors (max 10.79, 9.16), while its weakest items (-0.43, -1.14) are milder than the memorization anchors' most negative items (-2.13, -2.74, -3.99, -2.40). However, the paper falls short of the 7.50 Knowledge Localization paper because: (a) that paper proposes a new substantive scientific assumption alongside its critique, (b) this paper has a structural weakness in the LLM-as-a-Judge section, and (c) meta-science/rigor papers tend to score lower than core technical contributions at comparable quality. Score 6.5 — borderline accept with revisions.

**Anchors consulted:**
| Path | Avg Score | Round | Itemized? | Comparison |
|------|-----------|-------|-----------|------------|
| lf8QQ2KMgv.md | 3.75 | 1 | Yes | Memorization re-analysis — weaker strengths, more severe negative weights |
| GbEmJmnQCz.md | 4.40 | 1 | Yes | Memorization re-analysis (alt. version) — weaker strengths, more severe negative weights |
| Ok7ZH2Cyd7.md | 4.20 | 1 | Yes | RL methodology analysis — less directly comparable, similar critique nature |
| kiwyQsZIGP.md | 5.00 | 1 | Yes | FSL benchmark evaluation — meta-evaluation, different structure |
| bwZ9xh178a.md | 6.00 | 2 | No | Healthcare analytics — less comparable topic |
| zpBamnxyPm.md | 5.75 | 2 | No | Scaling law critique — less directly comparable |
| xI71dsS3o4.md | 5.75 | 2 | No | Scaling law fitting survey — meta-analysis, different structure |
| bmrYu2Ekdz.md | 6.50 | 2 | No | Pre-training stability study — not a critique paper |
| tfyHbvFZ0K.md | 7.50 | 2 | Yes | Knowledge Localization critique + new assumption — combines critique with substantive new scientific contribution |
| RW37MMrNAi.md | 5.60 | 2 | No | Classification difficulty analysis — not a critique paper |

MY FINAL SCORE: <score>6.5</score>
MY FINAL DECISION: <decision>Accept</decision>