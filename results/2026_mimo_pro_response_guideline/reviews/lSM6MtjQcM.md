## Summary
AetherCode is a competitive programming benchmark for LLMs that sources 456 problems from premier competitions (IOI, ICPC, NOI, USACO, CCPC) spanning 2024–2025, and introduces a hybrid automated-expert test case construction methodology validated using a novel TPR/TNR framework against 30,000+ human submissions. The evaluation of 17 LLMs demonstrates meaningful performance discrimination (Pass@1 from 4.4% to 35.5%) with fine-grained per-category diagnostics, supporting the paper's argument that current benchmarks overstate LLM coding proficiency.

## Strengths
- **Novel TPR/TNR framework for test case quality**: The paper formalizes test suite quality as a binary classifier (Equations 1-2) evaluated against 30,000+ human submissions, departing from quantity-based proxies. The G-V Agent alone achieves 89.9% TNR, and after expert annotation reaches 100% TPR and 100% TNR on the collected solution corpus (Section 2.3.1-2.3.2). This is a genuine methodological contribution to benchmark construction.
- **Premier competition sourcing with recency advantage**: AetherCode systematically collects problems from IOI, ICPC, NOI, USACO, and CCPC spanning January 2024 to May 2025 (Table 2), significantly more recent than prior benchmarks like USACO (2011–2023), OJBench (2016–2023), or LLM-Pros (2011–2024), reducing data contamination risk.
- **Meaningful model discrimination with actionable diagnostics**: Table 3 shows clear tier separation across 17 models, with per-category breakdowns across 10 algorithmic domains (Table 4) enabling diagnosis of model-specific weaknesses (e.g., Claude models' TLE tendency at ~50% of errors vs. ~20% for others, GPT-4.1's weak math performance at 4.2%).
- **Human-grounded difficulty classification**: Difficulty is assigned from human contestant solve rates and expert judgment (Section 2.2), with "Extreme" problems defined as those unsolved by any human contestant. This avoids the circular problem of LLM-based difficulty classification.
- **Substantial expert involvement**: 67 competitive programming experts (majority Codeforces 2000+) constructed targeted test cases, and an additional elite team of ICPC gold medalists performed final audits (Section 2.3.3). The handling of special judges for multi-output problems is also well-addressed.

## Weaknesses

### Fatal
None.

### Major
- **Table 1 difficulty rating contradicts the paper's central thesis**: The paper's core argument is that existing benchmarks are insufficiently difficult and that AetherCode provides a harder test. Yet Table 1 (line 51) rates AetherCode at ★★★ while CodeContests, USACO, CodeELO, and LiveCodeBench Pro all receive ★★★★ (lines 46-50). The empirical data in Table 3 supports AetherCode being harder — top models reach only ~35% Pass@1, vs. >80% on LiveCodeBench as cited in the introduction (line 13) — so the table is either using an inconsistent methodology or is simply wrong. A reader encountering Table 1 would conclude the authors consider their own benchmark less challenging than several alternatives they critique, which directly undermines the paper's framing. This is an easy fix with high credibility impact.

- **Headline 100% TPR/TNR is measured on the construction set, overstating what it guarantees**: Section 2.3.3 (line 136) explicitly states experts were "tasked with constructing targeted test cases specifically designed to fail the various incorrect solutions we had collected," and Section 2.3.1 (line 124) reports 100% metrics "on our collected solution set." Test cases were optimized against the specific failure modes in the corpus. The elite audit (ICPC gold medalists supplementing corner cases) partially mitigates this, but the paper does not disentangle the contributions: what is the TNR on solutions not used during construction? Without held-out validation, the "100%/100%" headline is technically correct but misleading about generalizability to novel LLM submissions.

### Minor
- **No rank correlation analysis against existing benchmarks**: The evaluation reports absolute performance but does not compare model rankings on AetherCode versus other benchmarks. If AetherCode produces the same ordinal ranking as LiveCodeBench, its contribution is "harder benchmark with better test cases" — still valuable but less transformative than implied by "a more faithful measure of LLM capabilities" (line 9). A Spearman rank correlation with at least one overlapping benchmark would directly substantiate or nuance this claim.

- **Selection criteria for the 456 problems not specified**: The paper says problems were sourced from premier competitions but does not clarify whether these represent all problems from targeted 2024–2025 competitions or a curated subset. If a subset, selection criteria matter for assessing potential bias toward certain difficulty levels or problem types.

- **Statistical noise at Extreme difficulty level**: With only 20 "Extreme" problems and models showing 0–3.8% pass rates (0–0.76 problems solved per model on average), conclusions about that tier have essentially zero statistical power. The paper should explicitly acknowledge this limitation.

- **Pass@1 vs Pass@4 exploration analysis potentially confounded**: The claim that "top-tier models exhibit great exploration potential" (line 206) based on Pass@1-to-Pass@4 gaps could be confounded by problem difficulty — models near the solving threshold on more problems naturally benefit more from additional samples. The analysis would benefit from controlling for problem-level solve probability.

### Trivial
None.

## Nice-to-Haves
- Discussion of how ICPC's team-based format (3 people, 1 computer) maps to individual LLM evaluation and whether this creates systematic differences from OI problems (individual competition).
- Ablation separating the G-V Agent's contribution to TNR from the expert annotation layer's contribution.
- Plans for benchmark maintenance and expansion beyond the current 2024–2025 window.

## Removed Points
These points are flagged to be removed, treat them with caution:
- **Missing Appendix A (prompt format details)**: The harsh critic flagged that prompt format and evaluation setup are only in Appendix A. Per the rules, the appendix is stripped from all papers but exists in the original submission. Not a real weakness.
- **"Ssed-1.6-Thinking" typo in Table 3**: This is a parser formatting artifact, not a paper problem.
- **Missing related works**: Per rules, cannot verify existence of uncited works.
- **ICPC team format concern**: Moved to Nice-to-Haves rather than retained as a weakness — the paper's scope is benchmarking LLMs on competition problems, not analyzing competition format psychology. This is outside the paper's stated scope.

## Novel Insights
The TPR/TNR formalization of test case quality — treating a test suite as a binary classifier evaluated against a large corpus of correct and incorrect solutions — is a genuinely novel methodological contribution that could become a standard for benchmark construction. The finding that Claude models tend to produce correct-but-inefficient solutions (TLE ~50% of errors vs. ~20% for other models) is an interesting and actionable diagnostic. The demonstration that even Pass@4 on non-reasoning models cannot match Pass@1 on reasoning models provides meaningful evidence about the current capability frontier.

## Suggestions
- **Fix Table 1**: Either increase AetherCode's difficulty rating to ★★★★ or ★★★★★ to match the empirical evidence, or explain the rating methodology so it doesn't appear self-contradictory.
- **Report held-out TNR**: Split the collected solutions into construction and held-out subsets; report TNR separately. If close to 100%, this powerfully validates the framework.
- **Add rank correlation**: Compute Spearman rank correlation between AetherCode model rankings and at least one overlapping benchmark (e.g., LiveCodeBench) using commonly evaluated models.
- **Acknowledge Extreme-level statistical limitations**: Note explicitly that n=20 Extreme problems provides insufficient statistical power for meaningful conclusions at that tier.

## Score and Decision

**Calibration anchors retrieved across both rounds (22 papers total):**

| Paper | Avg Score | Round | Comparison |
|-------|-----------|-------|------------|
| Nemesis (jailbreaking) | 1.40 | 1 | Irrelevant topic |
| Minimax path implementation | 1.00 | 1 | Very weak paper |
| Systematic review of LLMs | 1.00 | 1 | No original contribution |
| Cross-lingual humanoid robots | 1.00 | 1 | Irrelevant |
| Improving AI via computational models | 2.00 | 1 | Weak, irrelevant |
| Improve Code Generation with Feedback | 3.00 | 1 | Weaker methodology |
| RACE benchmark | 3.60 | 1 | Similar concept, weaker validation; AetherCode clearly stronger |
| Code Reasoning (CES) | 3.75 | 1 | Narrower focus |
| LLM search problems | 3.67 | 1 | Narrower benchmark |
| Tests as Instructions | 4.00 | 1 | Narrower TDD benchmark |
| BigCodeBench | 9.00 | 1 | Gold standard; AetherCode less polished |
| ENAMEL (efficiency benchmark) | 5.75 | 1 | AetherCode broader, novel TPR/TNR |
| LiveCodeBench | 6.25 | 1 | Closest comparable; AetherCode has stronger test methodology but self-inflicted issues |
| H-CAT (hardness characterization) | 6.20 | 1 | Different domain, comparable methodology rigor |
| Contamination analysis | 6.75 | 1 | Different focus (contamination) |
| CS-Bench | 6.75 | 1 | Broader CS benchmark, comparable rigor |
| TestGenEval | 6.25 | 2 | Similar scale benchmark effort |
| Automatic Dataset Construction | 6.00 | 2 | AetherCode stronger |
| AIMS.au dataset | 6.33 | 2 | Different domain, comparable effort |
| Commit0 | 6.67 | 2 | Different focus (library generation) |
| LiveBench | 7.33 | 2 | More polished, fewer self-inflicted issues |
| WildBench | 7.33 | 2 | More polished evaluation framework |

**Round 1 bracket: 5.5–7.5.** AetherCode is clearly stronger than ENAMEL (5.75, Accept) and comparable to LiveCodeBench (6.25, Accept) but with more self-inflicted credibility issues. It sits below CS-Bench (6.75) and LiveBench (7.33).

**Round 2 narrowing: 6.0–7.0**, anchored at **6.5**. The paper has genuinely strong and unique contributions (TPR/TNR framework, premier competition sourcing, comprehensive 17-model evaluation), but the Table 1 self-contradiction and headline metric circularity are substantive issues that prevent a stronger score. These are fixable — addressing them would likely move the paper to 7.0+.

MY FINAL SCORE: <score>6.5</score>
MY FINAL DECISION: <decision>Accept</decision>