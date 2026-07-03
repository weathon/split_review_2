Now let me produce the final review.

---

## Summary

This paper provides a detailed forensic re-analysis of a high-profile ICLR 2025 Oral paper (Nguyen et al., 2024) that introduced min-p sampling for LLMs. The authors examine all four lines of evidence from the original paper — human evaluations, NLP benchmarks, LLM-as-a-Judge evaluations, and community adoption claims — and find that each collapses under proper scrutiny. They contribute a Best-of-N methodology for controlling hyperparameter volume in method comparisons and derive six general lessons for rigorous empirical ML research. The work is well-executed, transparent about its limitations, and the core findings (especially the human evaluation re-analysis and the community-adoption fact-check) are convincing and important.

## Strengths

1. **Rigorous statistical re-analysis with proper multiple-comparison correction (Section 2.2, Table 1):** The paper re-runs 12 one-sided paired t-tests with Bonferroni correction and applies an Intersection-Union Test. Evidence supports min-p's superiority in only 1 of 12 comparisons at α=0.05 and 0 of 12 at α=0.01 — flatly contradicting the original paper's claim that min-p "consistently" outperformed baselines "across all settings." This is a textbook demonstration that correctly applied statistics can overturn a published claim.

2. **Discovery of omitted data and selective reporting (Section 2.1, Section 4.3):** The paper identifies that 1/3 of the human evaluation data (basic sampling scores) was excluded without justification — a finding publicly confirmed with the original authors. It also documents that in the LLM-as-a-Judge results, the higher of two scores was reported for min-p while the lower was reported for top-p (Section 4.3), supported by direct evidence from a Telegram link shared by the original first author. Both findings are specific and independently verifiable.

3. **Novel Best-of-N methodology for controlling hyperparameter volume (Section 3.1, Figures 4–5):** The paper develops a subsampling-based analysis that equalizes the number of hyperparameter configurations considered per method and compares best achievable performance, demonstrating across 9 models and ~6000 A100-hours of computation that min-p's claimed superiority disappears under controlled comparison. Prior work on sampling methods (including the original paper) did not control for differential hyperparameter tuning, making this a genuine methodological contribution.

4. **Fact-checking of retracted community-adoption claims (Section 5):** The paper verifies that the original paper's claims of 54k repositories and 1.1M GitHub stars were unsubstantiated (major LM repositories' combined stars sum to 453k), documents that the authors retracted both claims, and notes that 3 of 4 ICLR reviewers used these retracted numbers as justification for acceptance — a concrete illustration of how unverified claims can distort peer review.

## Weaknesses

### Fatal
None.

### Major

- **NLP benchmark critique is limited to a single benchmark (Section 3).** The original paper evaluated on GSM8K and GPQA; the re-analysis only covers GSM8K CoT (stated reason: compute budget, ~6000 A100-hours). The abstract claims "extensive hyperparameter sweeps on NLP benchmarks show min-p's claimed superiority vanishes," which overstates what was actually tested. While the section heading ("THOROUGH HYPERPARAMETER SWEEP ON GSM8K CONTRADICTS") is precise, the abstract and the blueprint summary generalize beyond the evidence. The paper's central conclusion does not hinge on this section alone — the human evaluation re-analysis (Section 2) independently undermines the original paper's core claims about quality and diversity — but the NLP critique as presented is solid yet narrow.

### Minor

- **The "blueprint" framing modestly overpromises.** The title promises "A Blueprint for More Rigorous Science" but the paper delivers a detailed case study of one paper's failures followed by six correct-but-individually-not-novel lessons (control hyperparameter volume, use multiple-testing corrections, share data, scrutinize qualitative summaries, ensure methodological clarity, watch for selective reporting). These lessons are well-supported by the case study, but they are standard best-practice recommendations that the reproducibility community has articulated before. The paper's real contribution is the careful case study and the Best-of-N methodology; the "blueprint" framing invites unnecessary criticism.

- **The LLM-as-a-Judge critique (Section 4) is the weakest of the four lines of evidence.** The indirect comparison criticism is valid but the paper does not quantify whether the design choice actually distorted results in this specific case. The unequal hyperparameter tuning point is real but largely restates the core insight from the NLP benchmark analysis. Only the selective reporting claim (Section 4.3) brings independently strong evidence; the remaining concerns are less definitive than the evidence in Sections 2 and 3.

- **Best-of-N methodology has an unaddressed limitation:** It controls for the *number* of hyperparameter configurations but not for whether the hyperparameter values span comparably useful regions of each sampler's tuning space. The authors note values were "lightly edited to make them more evenly distributed" (line 133), which mitigates but does not fully address this concern. This does not invalidate the analysis but should be explicitly acknowledged.

- **No explicit code/data repository for the current paper.** Despite the paper's strong emphasis on data transparency (Lesson 3: "Demand and practice full data transparency"), there is no explicit statement or link for where the re-analysis code and data can be found. The paper mentions publicly posting annotations (Section 2.3) and using the original authors' code, but a dedicated reproducibility statement is absent.

- **Limitations section is perfunctory (Section 6, line 210–211).** The "Key Limitation" paragraph states only that "conclusions are based on the evidence we analyzed," which is tautological. A more substantive discussion of the scope boundaries — single NLP benchmark, generalizability from one case study — would strengthen the paper.

### Trivial

- The paper uses Bonferroni correction without noting that other multiple-comparison corrections (e.g., Benjamini-Hochberg) would produce the same qualitative conclusion, which would preempt a predictable objection from informed readers.

## Nice-to-Haves

- Running the Best-of-N analysis on at least one additional benchmark (e.g., MMLU or a coding task) would meaningfully strengthen the NLP critique's generalizability.
- Including the Telegram-link source data (Section 4.3) as a supplementary file would tighten documentation of the selective reporting claim.
- A brief note on alternative multiple-comparison corrections (Benjamini-Hochberg) yielding the same conclusion.

## Removed Points

These points from the reviewer inputs were removed with justification:

1. **"Blueprint lessons are standard/not novel" (Harsh Critic):** The lessons are individually well-known, but the paper's contribution is grounding them in a concrete case study. This is a standard and accepted scientific format. The framing concern is kept as a minor weakness (above) but the stronger claim that the paper contributes nothing new is unwarranted.

2. **"Adversarial tone / score-settling" (Harsh Critic):** Subjective style preference. The paper's catalog of ML scandals (line 13) is factual and contextually appropriate. Removed as a stylistic nitpick.

3. **"Selective reporting claim is circumstantial" (Harsh Critic):** The paper cites a Telegram link publicly shared by the first author of the original paper. Line 193: "the first author publicly shared a Telegram link that showed the higher of two scores was reported for min-p... but the lower of two score was reported for top-p." This is direct evidence from the source, not circumstantial. Removed.

4. **"Pooling claim not directly cited" (Harsh Critic):** The paper describes the original paper's statistical approach based on available code and public discussion with the original authors. The context provided (line 86) is sufficient. Removed.

5. **"Focus on high diversity setting could be contested" (Harsh Critic):** The paper gives three explicit justifications for this focus (line 64), including the original authors' own recommendation. Removed.

6. **"Missing related works" (Harsh Critic):** The paper cites Pineau et al. 2017 (line 13) and Belz et al. 2021 (line 31, full reference on line 228). Factually incorrect. Removed.

7. **"LLM-as-a-Judge indirect comparison criticism not as damning" (Harsh Critic):** The paper raises a valid methodological concern about indirect comparison and non-transitivity. This is noted as part of the section weakness in the main review rather than treated as a fatal flaw.

## Novel Insights

None beyond the paper's own contributions. The paper itself provides the key novel insights: (a) a documented case of how three specific methodological failures (omitted data, incorrect statistics, selective reporting) combined to produce an unsupported scientific claim in a high-profile publication, and (b) the Best-of-N subsampling analysis as a general-purpose tool for detecting cherry-picking via differential hyperparameter tuning.

## Suggestions

1. **Add at least one more NLP benchmark** to the Best-of-N analysis (e.g., a reasoning or coding benchmark) to move the NLP critique from "solid but narrow" to "definitive."
2. **Include an explicit code/data repository link** for the re-analysis. Given the paper's central message about transparency, this omission is particularly noticeable.
3. **Expand the limitations section** to substantively discuss the scope boundaries rather than a single tautological sentence.
4. **Tighten the abstract** to match exactly what was tested ("GSM8K" rather than "NLP benchmarks").
5. **Add a note about alternative multiple-comparison corrections** producing the same qualitative result.

## Score and Decision

**Score: 7.5** — Solidly in the accept range. The paper is above borderline (6) due to the convincing multi-faceted evidence, the novel Best-of-N methodology, and the important scientific correction it provides. It is below a clear 8 due to the single-benchmark limitation in the NLP analysis, the somewhat overclaimed "blueprint" framing, and the thinner LLM-as-a-Judge section. With minor revisions (especially adding a second benchmark and a code repository link), the paper would merit a clear 8.

**Decision: Accept**

MY FINAL SCORE: <score>7.5</score>
MY FINAL DECISION: <decision>Accept</decision>