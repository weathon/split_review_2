Now let me write the final consolidated review.

---

## Summary

This paper introduces Ambig-SWE, an underspecified variant of SWE-Bench Verified designed to study how LLM agents handle missing information in multi-step software engineering tasks. The key contribution is a three-stage decomposition of the interaction problem—detecting underspecification, asking targeted clarification questions, and leveraging interaction to improve performance—along with systematic evaluation of 6 proprietary and open-weight models across these capacities. The paper finds that interaction can substantially improve resolve rates, but most models default to non-interactive behavior and struggle to distinguish well-specified from underspecified inputs.

## Strengths

- **Well-motivated three-stage decomposition of the interaction problem.** Breaking "handling underspecification" into (i) detection, (ii) questioning, and (iii) leveraging interaction is both natural and actionable. It lets the community diagnose which specific capacity a model fails at, rather than just measuring end-to-end resolve rates. The paper correctly identifies that real agentic tasks involve multiple, dynamically arising gaps rather than a single missing detail. [Impact: +9.95]

- **The user proxy design is principled and reproducible.** The proxy responds only using information present in the fully specified issue, says "I don't have that information" for missing details, and cannot hallucinate. This conservative design isolates agent behavior from confounds introduced by a more generous simulator. [Impact: +10.00]

- **Several findings are genuinely surprising and non-obvious.** Qwen 3 Coder achieving 100% FNR in detection (complete non-responsiveness to any interaction prompt), Qwen's performance worsening when navigational information is provided (Table 1: 55.43% resolve without vs. 52.38% with), and Claude Sonnet 4 achieving comparable information gain to Qwen with 50% fewer questions via an exploration-first strategy are all concrete, actionable insights. [Impact: +10.00]

- **The navigational vs. informational distinction (Section 3.3) is a useful analytical lens.** Table 1 reveals real variation across models, and the finding that Deepseek-v2 performs worse than its Hidden baseline when file locations are absent is a non-trivial dependency. [Impact: +2.05]

- **The dataset construction is well-reasoned with transparent limitations.** The paper acknowledges that generated underspecification differs from natural underspecification and explains why natural examples cannot be used (lack of paired ground truth). The distributional difference analysis provides transparency about how the synthetic issues compare to real ones. [Impact: +9.14]

## Weaknesses

### Major

- **The headline "74% improvement" figure is not verifiable from the presented data and conflates compulsory interaction with genuine detection-driven interaction.** The 74% figure appears twice (abstract and introduction) but cannot be reproduced from Figure 3's resolve rates. Computing relative improvement (Interaction−Hidden)/Hidden for each model yields: Llama 3.1=50%, Deepseek-v2=32.1%, Haiku=100%, Sonnet 3.5=63.6%, Qwen 3 Coder=18.0%, Sonnet 4=53.5% — none equals 74%. Gap recovery (Interaction−Hidden)/(Full−Hidden) is 76.4% for Sonnet 4, close but not 74%, and the paper never states which quantity is being reported. Furthermore, RQ1 makes interaction compulsory via prompt modification (Section 3.1: "we modify the prompt to make interaction with the user compulsory"). The 74% figure therefore comes from forced interaction with a perfectly informed user, not from models autonomously detecting underspecification — a significantly narrower phenomenon than the natural framing suggests. [Impact: -9.99]

- **Uneven turn budgets (100 vs. 30 turns across models) confound cross-model comparisons.** Claude Sonnet 4 and Qwen 3 Coder receive up to 100 interaction turns while all other models receive 30 (Section 3.1). The justification — "greater reasoning and planning capacity" — is circular: the capacity being evaluated is the very thing used to allocate more budget. Claims like "Claude Sonnet 4 attains the highest relative performance (89%)" are weakened by this asymmetry (3.3× the budget of the next-best model). Within-model comparisons (Hidden vs. Interaction for the same model) remain valid, but cross-model comparisons are uncontrolled for compute budget. [Impact: -9.85]

- **Claude Sonnet 4's Hidden setting evaluation uses only 100/500 instances (footnote 4).** This introduces two validity concerns: (a) the Hidden→Interaction improvement for Sonnet 4 is computed across potentially non-comparable instance sets (100 for Hidden, presumably 500 for Interaction), and (b) cross-model comparisons of Hidden rates (e.g., Sonnet 4's 40.0% vs. Qwen's 45.6%) compare different instance sets. If the 100 instances happen to be harder than average, Sonnet 4's Hidden rate is artificially depressed, inflating its apparent interaction improvement. The paper asserts findings are "still statistically significant" but defers details to the appendix. [Impact: -10.00]

### Minor

- **Data leakage from SWE-Bench Verified is acknowledged but not substantively addressed.** The paper notes in one sentence that higher Hidden-setting resolve rates may be due to "data leakage" and that Qwen 3 Coder's "correct assumptions about missing information" may inflate performance. For a benchmark whose core purpose is measuring how models handle missing information, this is a first-order validity threat. A contamination analysis or at minimum a discussion of which models' training data includes SWE-Bench would substantially strengthen the paper. [Impact: -9.38]

- **The detection experiment (RQ2) measures interaction as a binary choice, but detection in practice involves confidence calibration.** A model might be uncertain whether the issue is underspecified and could ask one low-cost question to check. The current framing treats "interact" vs. "don't interact" as the decision, missing the more nuanced question of what the model asks and whether it asks proportionally to its uncertainty. [Impact: -0.00]

- **The synthetic underspecification uses more aggressive information removal than natural underspecification (acknowledged in Section 2.1).** While the paper explains why natural issues cannot be used, the consequence is that models are tested on cleaner, artificially stripped descriptions rather than the messier underspecification occurring in practice. The conclusions should be correspondingly scoped. [Impact: -1.19]

### Trivial

None.

## Nice-to-Haves

- Add binomial confidence intervals to Figure 3's bar chart to help readers assess whether differences between models are meaningful.
- Include a single summary figure mapping the three RQs to the three decomposed capacities.
- The turn-budget asymmetry could be partially addressed by evaluating a subset of models at both 30 and 100 turns as a sensitivity analysis.

## Removed Points

These points are flagged to be removed; treat them with caution.

- **Criticism about missing related works**: Removed per policy — I cannot verify the existence of works not cited.
- **Criticism about missing appendix content (distributional difference quantitative metrics, Wilcoxon test details)**: Removed. These are in the appendix which the parser strips; they exist in the original submission.
- **"No hypotheses grounded in training methodology" (about RQ2 patterns)**: Removed — the paper is an empirical/descriptive study and this is scope creep.
- **"Error bars missing from Figure 3"**: Moved to Nice-to-Haves; bar charts without error bars are standard for SWE agent evaluation.
- **Generic criticisms about user proxy realism**: Removed — the paper already acknowledges this limitation.
- **"Paper would benefit from summary figure mapping RQs to capacities"**: Moved to Nice-to-Haves; not a weakness.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. **Fix the headline 74% figure.** Make it directly computable from the presented data: specify which quantity (relative improvement, gap recovery, or other) and which model(s), or replace with a range/qualitative statement.
2. **Address the turn-budget asymmetry.** Present a sensitivity analysis (e.g., evaluate a subset of models at both 30 and 100 turns) or explicitly label all cross-model comparisons as uncontrolled for budget.
3. **For Claude Sonnet 4's Hidden subset**, report how the 100 instances were selected (random? stratified?), provide confidence intervals, and clarify exactly which comparisons use which instance sets.
4. **Add a contamination analysis** for SWE-Bench Verified, or at minimum discuss which models' training data likely include this benchmark, to calibrate the data leakage concern.
5. **Frame RQ1 more explicitly** around what it actually measures (forced interaction with a perfectly informed user) and scope the quantitative claims to match.

## Score and Decision

MY FINAL SCORE: <score>4.5</score>
MY FINAL DECISION: <decision>Reject</decision>