## Summary

This paper investigates the strategic decision-making of LLMs in three canonical game-theoretic settings—Rock-Paper-Scissors (RPS), the Centipede Game (CG), and the Traveler's Dilemma (TD)—where empirical human behavior systematically departs from Nash Equilibrium (NE) predictions. Using historical human-subject data as benchmarks, the authors compare 8 LLMs (3B–671B parameters) and find that LLMs generally lean toward GT rationality, show limited sensitivity to payoff-related hyperparameters, and underperform compared to both NE benchmarks and human players in several settings.

---

## Strengths

- **Well-chosen game selection with documented human baselines.** The three games (RPS, CG, TD) each represent a distinct structural class (evolutionary, sequential, one-shot) and each has well-documented human behavioral anomalies. Using published human experimental protocols (Wang et al. 2014; McKelvey & Palfrey 1992; Capra et al. 1999) provides a credible external reference for comparison without needing new human experiments.

- **Verbalization controls.** Randomizing action label letters across sessions is a meaningful methodological precaution against semantic anchoring effects, and the observation that high variance persists even across abstract labels is itself a useful finding about prompt sensitivity.

- **Consistent cross-game finding with internal nuance.** The general trend that LLMs are more GT-rational than humans holds across all three games, but the paper highlights important model-level variation (e.g., Gemma-27B exhibiting altruistic/pass-heavy CG behavior; DeepSeek tracking NE in TD while others move toward Pareto-efficient outcomes), which adds specificity beyond a single blanket conclusion.

- **Broad model coverage.** Eight models from diverse families (Llama, OLMo, Gemma, DeepSeek) spanning a wide parameter range lend reasonable generality to the empirical findings.

---

## Weaknesses

### Fatal
None.

### Major

- **Informal comparison to human data.** The paper's central contribution is comparing LLM behavior to human behavior, but the comparison is almost entirely visual/descriptive rather than statistical. Human experiments differ in sample sizes, incentive structures, cultural contexts, and era from the LLM experiments. No formal tests are used to measure the "distance" between LLM distributions and human distributions, nor is there any attempt to quantify alignment rigorously. Without this, claims such as "Gemma-27B aligns more with human behavior in CG" remain anecdotal.

- **Shallow mechanistic understanding.** The paper observes that LLMs behave more rationally than humans but does not probe why. Do models explicitly reason through backward induction? Are results from game theory textbooks in training data driving the behavior? Is it context-length/memory effects? A simple prompt-ablation (e.g., with vs. without history, with vs. without explicit payoff tables) would have clarified whether models are reasoning strategically or pattern-matching, which is important for interpreting the findings.

- **Surprising self-contradiction in RPS analysis.** The paper concludes LLMs "imitate rational (NE) behavior" in RPS, yet also reports that W₀ < 1/3 for most models, meaning models switch strategies more often than NE prescribes, *and* that all LLM models underperform relative to NE expected payoff. These results together suggest LLMs are not actually approximating NE in RPS—they are neither matching the mixed strategy nor exploiting conditional patterns like humans. The paper does not reconcile this tension clearly.

### Minor

- Only 10 independent sessions are run per game configuration. For models with high verbalization variance, this is a thin basis for per-model statistical conclusions, and the wide confidence intervals visible in figures underscore this limitation.

- The asymmetric Traveler's Dilemma results (Section 3.3) are reported briefly with conclusions largely hedged. This setting is potentially the most interesting (no previous human benchmark), but the analysis is underdeveloped relative to the setup it receives.

### Trivial

- The "Design principles" section in the introduction restates methodology that is covered again in Section 3, creating redundancy.

---

## Nice-to-Haves

- A formal distance metric (e.g., KL divergence or Wasserstein distance) between LLM choice distributions and human choice distributions would strengthen every comparison.
- An ablation removing game history from prompts would test whether models' learning curves in CG and TD arise from strategic adaptation or simply recency bias.
- Adding a human-like "framing" condition (with game titles and monetary stakes) alongside the abstract condition would reveal whether LLM behavior is genuinely derived from structural reasoning or from semantic priors about game names.

---

## Novel Insights

The paper's most interesting, underexplored finding is that LLMs display high variance across verbalization conditions even when only abstract strategy labels are randomized—meaning that label semantics alone, independently of game context, introduce substantial behavioral noise. This suggests a fundamental fragility of LLM strategic reasoning that is orthogonal to whether the model "knows" game theory: even strategically capable models are anchored by surface features of symbol choice in ways that have practical implications for deploying LLMs as decision-making agents. This observation sits across the three games and is more mechanistically informative than the main GT-vs-human comparison.

---

## Suggestions

- Provide a quantitative measure of LLM–human alignment (e.g., distributional distance) to substantiate the central comparison claim.
- Reconcile the RPS contradiction explicitly: if LLMs switch too often and underperform NE, what strategy are they actually playing?
- Expand the asymmetric TD analysis—it is the one setting with no human baseline and the richest potential for novel findings.
- Run at least 20–25 verbalization sessions to reduce confidence interval width in per-model comparisons.

---

## Score and Decision

The paper addresses a well-motivated research question, uses appropriate game-theoretic methodology, and produces a consistent empirical picture across three structurally different games. However, the central comparison to human data is descriptive rather than rigorous, a core analytical inconsistency (RPS rationality claim vs. suboptimal performance) is left unresolved, and the work does not advance mechanistic understanding of *why* LLMs deviate from human patterns. The contribution is solid empirical documentation but falls short of the analytical depth expected for a strong ICLR contribution.

MY FINAL SCORE: <score>4</score>
MY FINAL DECISION: <decision>Reject</decision>