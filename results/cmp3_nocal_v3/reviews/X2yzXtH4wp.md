## Summary

This paper introduces Ambig-SWE, an underspecified variant of SWE-Bench Verified, and a diagnostic framework that decomposes an agent's ability to handle underspecified instructions into three sub-capacities: (a) detecting that information is missing, (b) asking targeted clarification questions, and (c) integrating the acquired information to complete the task. Through a three-setting experimental design (Full, Hidden, Interaction), the authors evaluate six LLMs and produce several non-obvious findings — notably that Qwen 3 Coder's rigid protocol-following causes its performance to *worsen* when given navigational details, and that Claude Sonnet 4 achieves comparable information gain to Qwen with roughly 50% fewer questions through an exploration-first strategy. The framework provides a valuable diagnostic lens that goes beyond a single accuracy number.

## Strengths

- **Structured three-capacity decomposition (detection, clarification, integration).** The paper cleanly separates "can the model tell it needs more information?" from "can it ask good questions?" from "can it use the answers to solve the task?" This is the paper's most valuable intellectual contribution — it provides a diagnostic framework that future work can target independently, as each capacity exposes a different bottleneck. The three-experiment design (RQ1–RQ3) follows from this decomposition naturally.

- **The Full / Hidden / Interaction three-setting design is well-calibrated.** Each setting isolates a distinct variable (information completeness × interaction availability). Hidden → Interaction measures the value of interaction holding underspecification constant; Interaction → Full measures the residual gap from imperfect integration. This is a cleaner design than most benchmark papers in this area provide, and it enables the "gap recovery" analysis (e.g., recovering 89% of full performance) that is the paper's central quantitative result.

- **The navigational-vs.-informational analysis (Table 1) surfaces genuinely non-obvious findings.** The observation that Qwen 3 Coder's resolve rate *drops* when given file locations (55.43% → 52.38%), because it rigidly re-explores the code despite having the answer, and that Claude Sonnet 3.5 achieves competitive performance even without navigational details (37.94% vs. 24.78% for Haiku), provides concrete failure modes that training could address. These qualitative findings are the paper's strongest actionable insights.

- **The model selection supports controlled inference.** Including Claude Sonnet 3.5 → Sonnet 4 as a capability-scaling comparison within the same family, Haiku as a within-family scale comparison, and Qwen 3 Coder as a comparably-capable open-weight model allows the paper to draw inferences about scaling vs. training methodology that a random model collection would not support.

## Weaknesses

### Fatal

None.

### Major

- **Uneven turn budgets confound comparative model claims across the budget-differentiated groups.** Claude Sonnet 4 and Qwen 3 Coder receive up to **100 turns**; all other models receive **30 turns** (line 106). The paper's justification ("account for their greater reasoning and planning capacity") is circular: these models are allocated more budget *because* they are expected to use it, which means key comparisons — e.g., "proprietary models show stronger evidence of a significant difference" and "proprietary models generally demonstrate greater effectiveness in utilizing interaction" (line 123) — cannot separate the effect of interaction capability from the effect of having 3× the exploration budget. If Llama 3.1 or Deepseek-v2 were given 100 turns, their Interaction resolve rates might improve simply from more exploration steps, not from better interaction. The qualitative observations (Qwen's rigidity, Claude's exploration-first strategy) are **not** budget-dependent and remain valid, but any comparative rank-order claim across the 30-turn vs. 100-turn groups is weakened.

- **Claude Sonnet 4's Hidden (non-interactive) baseline is measured on only 100 out of 500 instances, and the subset selection is not described (footnote 4, line 131).** The headline claim "up to 74% improvement over non-interactive settings" depends on comparing Sonnet 4's Hidden rate (40.0%, from 100 instances) to its Interaction rate (61.4%, from 500 instances). If the 100-instance subset is systematically harder or easier than the full set, this comparison is invalid. The paper asserts the findings "are still statistically significant" and references Table 4 in the appendix, but without knowing how the subset was sampled (random stratified by difficulty? first 100? cheapest 100?), the reader cannot assess the risk of selection bias. This does not invalidate the paper's qualitative findings, but it makes the headline quantitative claim unverifiable from the presented information.

### Minor

- **The "up to 74%" improvement claim is not clearly traceable to the numbers presented in Figure 3.** Computing relative improvements from the table yields: Haiku 100%, Sonnet 3.5 63.6%, Sonnet 4 53.5%, Qwen 18.0%. Gap recovery yields Sonnet 4 at 76.4% — close to but not matching 74%, and the paper does not state which model or calculation produces the 74% figure. Since this number appears in both the abstract and §1 as a headline result, the paper should clarify which model and which definition of "improvement" (absolute percentage gain? relative gain? gap recovery?) produces 74%.

- **The user proxy has access to file locations that need modification (line 92), which is information a real user typically cannot provide.** This makes the Interaction setting artificially easier than any real deployment where a user says "my code has an index error." The proxy design conflates (a) extracting information a user can plausibly provide with (b) extracting information from an omniscient oracle. The paper acknowledges this in the limitations section ("our simulated user proxy may be more cooperative than real users"), but the framing of "interactive agents recover 89% of full performance" does not caveat that this recovery depends on an unrealistically knowledgeable user.

- **No confidence intervals are reported for the resolve rates in Figure 3.** With only 500 issues (and only 100 for Sonnet 4's Hidden setting), binomial confidence intervals are wide enough to affect some comparative claims. For instance, Qwen's Interaction (53.8%) and Hidden (45.6%) rates may overlap at standard confidence levels. The paper reports Wilcoxon signed-rank tests but does not provide interval estimates that would help readers assess the precision of the point estimates.

### Trivial

None.

## Nice-to-Haves

- **Direct measurement of integration capability (sub-capacity c).** The paper currently infers integration ability from the Interaction → Full gap, which conflates integration with question quality. An experiment where all models receive the same oracle-provided answers to standardized clarification questions would isolate integration from question quality, completing the three-capacity decomposition that the paper motivates.
- **Analysis of whether the GPT-4o-generated underspecified issues lead to systematically different resolve rates than naturally-occurring ones.** The distributional analysis compares *features* but does not measure whether the generated issues are easier or harder to resolve. This would strengthen the benchmark's validity argument.
- **Documentation of the 100-instance subset selection method for Sonnet 4's Hidden evaluation.** A brief statement (random stratified, first N, etc.) would resolve the major evidential concern about the headline 74% claim.

## Removed Points

These points were flagged by the harsh critic but are removed in the final review (with justification):

1. "Title uses 'Ambig-SWE' which foregrounds ambiguity, but paper is about underspecificity" — Removed: the paper explicitly defines the relationship between ambiguity and underspecificity in §6. The naming is a reasonable branding choice and does not mislead about the paper's content.
2. "GPT-4o as both generator of underspecified variants and user proxy creates systematic bias" — Removed: this is standard practice, the paper acknowledges it's a simulation not a real user (§2.2), and the reviewer themselves called it "not a fatal flaw." It does not warrant inclusion as a weakness.
3. "No discussion of whether GPT-4o-generated issues are easier/harder than natural ones" — Moved to Nice-to-Haves (not a weakness, a constructive extension).
4. "Detection measured only within first three turns is only mentioned in limitations" — Removed: the paper states this clearly as a scope constraint in §7 (line 281), which is the appropriate place for limitations. No one would expect to find the limitation in the experimental setup section.
5. Several minor comments about presentation and phrasing — Removed per formatting-nitpick filtering rule.

## Novel Insights

Beyond the paper's own contributions, the reviews surface one synthetic observation: the paper is strongest as a *diagnostic framework* and weakest as a *comparative model ranking*. The turn-budget confound and the partial Hidden evaluation for Sonnet 4 mean that the comparative claims (proprietary vs. open-weight, scale effects) are less well supported than the qualitative behavioral findings (Qwen's protocol rigidity, Claude's exploration-first strategy). This suggests the paper would benefit from reframing its contributions around the framework and behavioral diagnostics rather than model rankings.

## Suggestions

1. **Equalize turn budgets, or explicitly drop comparative claims across budget groups.** Run a subset of experiments where all models receive the same larger budget (e.g., 100 turns) on a smaller number of issues to verify that the qualitative patterns hold. Alternatively, explicitly re-scope the paper to avoid claims that compare models across the 30-turn vs. 100-turn groups.
2. **Document the 100-instance subset selection for Sonnet 4's Hidden evaluation** (random stratified by difficulty? first 100?). Even a one-sentence description would resolve the evidential concern.
3. **Clarify the 74% figure.** State which model and which definition of "improvement" produces this number. If it refers to gap recovery for a specific model, say so explicitly.
4. **Add a caveat about the user proxy's access to file locations** when stating the 89% recovery figure in the abstract and introduction, not just in the limitations section.
5. **Add confidence intervals** to Figure 3 (or a brief justification for why they are omitted).

MY FINAL SCORE: <score>7.0</score>
MY FINAL DECISION: <decision>Accept</decision>