Based on my calibration, AetherCode sits in the same bracket as LiveCodeBench (avg 6.25). Both are competitive programming evaluation benchmarks with contamination controls and multi-model evaluations. AetherCode has a stronger test-case quality framework and novel source coverage, but is weaker on the human baseline gap and has a smaller problem set. I place it slightly below LiveCodeBench.

**Round 1 bracket: 5.5 – 6.5**
**Final score: 6.0**

---

## Summary
AetherCode is a competitive programming benchmark that draws 456 problems from premier offline competitions (IOI, ICPC, NOI, USACO) rather than online judge platforms (LeetCode, CodeForces), addressing a genuine coverage gap. Test cases are constructed via a Generator-Validator Agent system plus 67 competitive programming experts, validated against 30,000+ human submissions using a TPR/TNR framework. An evaluation of 17 models across difficulty tiers, algorithm categories, and failure modes is presented.

## Strengths
- **Novel source coverage with genuine differentiation**: AetherCode is the first benchmark to systematically collect problems from premier offline competitions (IOI/ICPC World Finals, NOI). Section 1 and Table 1 credibly argue that online-judge sources have structural limitations (LeetCode's easier/single-function design, CodeForces' constrained 2–3 hour problem set), and the paper distinguishes itself from USACO Bench, ICPCEval, and OJBench by breadth and recency.
- **Principled test-case quality framework**: The TPR/TNR binary-classifier framing (Section 2.3.1) is a substantive methodological improvement over quantity-based proxies or naive mutation. Validated against 30,000+ human submissions, with the G-V Agent achieving 100% TPR and 89.9% TNR before expert supplementation, the framework is clearly described and reproducible in principle.
- **Broad, fine-grained evaluation**: Table 3 covers 17 models (12 reasoning, 6 non-reasoning) with Pass@1/2/4 breakdowns across difficulty, year, and 10 algorithm categories (Table 4). The failure mode analysis in Section 3.3 — that Claude-series models produce correct-but-slow algorithms (roughly equal WA/TLE split vs. 70–80% WA for other models) and that GLM-4.5 suffers language-following failures — is a concrete and actionable diagnostic.

## Weaknesses

### Fatal
None.

### Major
- **No human performance baseline despite it being the paper's central claim**: The abstract, Sections 1 and 5 all assert "a significant gap still exists between the performance of LLMs and top-tier human competitors." However, Table 3 contains no human row, and the paper never reports what fraction of AetherCode problems a gold medalist or ICPC world finalist would solve. Contest leaderboard metadata is collected for difficulty annotation (Section 2.2) but is not converted into a benchmark-level human figure. The conclusion that "there remains a significant gap compared to top human experts" (Section 5) is therefore unsubstantiated. Model scores below 36% Pass@1 are suggestive but not proof without a human anchor.

- **100% TPR/TNR claim is presented as an unconditional guarantee rather than a corpus-bounded one**: The paper explicitly acknowledges in Section 2.3.3 that "for problems with fewer than 50 incorrect solutions, achieving a 100% TNR might not sufficiently guarantee the robustness of the test cases." Yet the abstract and Section 5 conclude by "guaranteeing exceptional accuracy and reliability in evaluation." Because the expert annotation process literally adds cases until all *collected* incorrect solutions fail, the 100% TNR is partly tautological relative to that corpus and may not cover novel LLM-generated failure modes absent from the 30,000 human submissions.

### Minor
- **Contamination analysis (2024/2025 split) is reported but not discussed**: Table 3 shows a sizable and consistent performance drop on 2025 problems (e.g., Seed-1.6-Thinking: 28.3% → 14.7%; Gemini-2.5-Flash: 22.0% → 8.0%), but Section 3.1 does not interpret this. The data is present to support a meaningful contamination discussion; leaving it as a raw table column is an underexploitation of a genuine contribution.

- **OI/ICPC imbalance not analyzed in results**: Table 2 shows only 76 OI problems versus 380 ICPC. Since OI problems are specifically cited as the differentiating source (Section 1), and the benchmark is named in part for olympiad coverage, the minority OI share is notable. Table 4 breaks down results by algorithm category but not by competition type (OI vs. ICPC), so it is impossible to verify whether OI-style challenges are actually captured in the model results.

- **Extreme difficulty tier is too small for reliable conclusions**: The Extreme tier contains only 20 problems. Claims like "o4-mini-high and Gemini-2.5-Pro are notably two of the three models capable of tackling Extremely Difficult problems" (Section 3.1) rest on single-digit pass counts; variance is too high to support firm conclusions.

### Trivial
- **Table 1 difficulty self-rating is inconsistent with reported results**: AetherCode is rated ★★★, the same as APPS and LiveCodeBench and lower than CodeELO (★★★★) and LiveCodeBench Pro (★★★★). Yet Table 3 shows o4-mini-high solving only 35.5% at Pass@1, comparable to the hardest four-star benchmarks. No explanation is given.

## Nice-to-Haves
- A cross-benchmark comparison showing where AetherCode rankings diverge from LiveCodeBench Pro / CodeELO under identical evaluation conditions would directly validate the claim that AetherCode measures distinct capabilities.
- A more careful contamination analysis — controlling for problem difficulty within each year cohort — would elevate the 2024/2025 split from a table note to a genuine scientific result.
- A token-budget analysis checking how often models hit the 32,768-token cap would clarify whether TLE failures reflect reasoning limits or evaluation artifacts (Time Limit Exceeded is the second-largest failure mode; Section 3.3).

## Removed Points
*These points are flagged to be removed; treat them with caution.*

- **Harsh Critic suggestion for held-out/prospective TPR/TNR validation**: A valid methodological suggestion but beyond what benchmark papers typically provide; demoted to Nice-to-Have.
- **Harsh Critic prescription for specific human baseline methodology**: The core concern (no human baseline) is retained as Major; the prescription for how to implement it is removed as over-specified reviewer guidance.

## Novel Insights
The most genuinely novel observation is the binary-classifier TPR/TNR framework applied to test-case quality assessment, validated against a large corpus of both correct and incorrect human submissions — a conceptual shift from quantity to discrimination power. The finding that Claude-series models diverge sharply from all other evaluated models in their WA/TLE split (roughly equal vs. 70–80% WA elsewhere) suggests a systematic architectural or RLHF-driven tendency to favor correctness of logic over time-complexity planning, which is a concrete, field-relevant diagnostic not previously reported.

## Suggestions
1. Add a proxy human baseline: the fraction of problems solved by at least one human contestant in the original competition can be derived from existing contest metadata without recruiting volunteers. This would directly substantiate the paper's central "significant gap" claim.
2. Explicitly scope the 100% TPR/TNR claim to the collected human solution space, and note that expert audit provides additional coverage assurance beyond the measured corpus.
3. Expand the contamination section to interpret the 2024 vs. 2025 performance split, ideally with difficulty-controlled comparisons.
4. Report per-competition-type results (OI vs. ICPC) to validate that olympiad-style problems provide distinctive challenges beyond the ICPC majority.

## Score and Decision

**Anchor papers retrieved:**

| Path | Avg Score | Round | Comparison |
|---|---|---|---|
| chfJJYC3iL (LiveCodeBench) | 6.25 | R1 | Most direct analog — also a competitive programming evaluation benchmark; AetherCode has stronger test-case quality framework but weaker contamination analysis and missing human baseline |
| suz4utPr9Y (ENAMEL code efficiency benchmark) | 5.75 | R1 | Code benchmark with novel metric design; similar in scope but narrower in coverage |
| m2NVG4Htxs (LLM data contamination longitudinal) | 6.75 | R1 | Strong empirical study with novel analysis; AetherCode's contamination analysis is shallower |
| fjEZ2LPceZ (CS-Bench) | 6.75 | R1 | Comprehensive evaluation benchmark; broader scope but less rigorous test-case validation |
| XmProj9cPs (Spider 2.0) | 8.00 | R1 | High-quality benchmark with real-world complexity; more novel evaluation context than AetherCode |
| NlY3XppPt3 (novel programming challenges) | 2.00 | R1 | Weak benchmark paper; AetherCode clearly above this tier |
| DZBFchnM3b (search problems benchmark) | 3.67 | R2 | Weaker benchmark paper; AetherCode's curation rigor exceeds this |
| u6jbcaCHqO (SciBench) | 5.60 | R2 | College-level scientific benchmark; similar structure; AetherCode's test-case framework is stronger |
| jw2fC6REUB (CURIE) | 6.40 | R2 | Scientific long-context benchmark accepted at ~6.4; AetherCode comparable in contribution scope |
| WrBqgoseGL (Putnam-AXIOM) | 5.80 | R2 | Hard math benchmark with contamination control; similar tier |

**Round 1 bracket**: 5.5 – 7.0. AetherCode is above reject-tier benchmarks (3.5–5) given genuine source novelty and the substantive test-case quality framework. It does not reach 7+ because the central claim ("significant gap vs. human experts") lacks direct evidence, and the 100% TPR/TNR claim is overstated.

**Round 2 narrowing**: LiveCodeBench (6.25) is the closest analog and scored borderline-accept. AetherCode has a stronger test-case quality contribution but a weaker central motivation (no human baseline). Placing it at **6.0** — marginally below LiveCodeBench, which also benefits from a broader problem set and live updating mechanism.

MY FINAL SCORE: <score>6.0</score>
MY FINAL DECISION: <decision>Accept</decision>