Now I have all the information needed. Let me write the final consolidated review.

## Summary

This paper introduces Ambig-SWE, an underspecified variant of SWE-Bench Verified (500 issues with GPT-4o-generated stripped-down versions), and a three-stage evaluation framework (detect → ask → leverage) for studying how LLM-based code agents handle missing information through interaction. The paper evaluates six proprietary and open-weight models and produces several non-obvious findings: models rarely detect underspecification unprompted, Qwen 3 Coder catastrophically fails to interact at all (100% FNR), and there is a meaningful disconnect between how much information models extract through questions and how well they integrate it.

## Strengths

1. **Well-motivated problem, cleanly decomposed.** The paper correctly identifies that prior work on ambiguity studied single missing details, whereas real agentic tasks involve multiple interdependent gaps. The three-stage decomposition (detecting underspecification → asking targeted questions → leveraging answers) is the paper's most valuable analytical contribution—it produces distinct and sometimes uncorrelated model rankings (e.g., Qwen 3 Coder is strong on coding ability but catastrophic on detection), validating the decomposition's utility.

2. **Non-obvious empirical findings.** Several results are genuinely informative: (a) Qwen 3 Coder's 100% FNR in detection (Table 2) is a striking finding about a widely-used open-weight model; (b) the disconnect between information extraction volume and integration (Qwen extracts the most information via cosine distance but performs *worse* with navigational information) is non-obvious (Table 1, §5.2); (c) the exploration-first strategy of Claude models vs. ask-first of Deepseek and Qwen (§5.3) is a meaningful qualitative finding that could guide training.

3. **Responsible dataset construction and transparency.** Creating synthetic underspecified variants from well-specified SWE-Bench Verified issues preserves paired ground truth for causal measurement. The distributional analysis (§2.1) comparing generated vs. natural underspecification is a transparency measure that many benchmark papers omit. The explicit acknowledgment that synthetic underspecification is "more aggressive" in removing technical detail than natural underspecification is honest and allows readers to calibrate.

## Weaknesses

### Fatal
None.

### Major

1. **Headline quantitative claims are measured against an idealized oracle without adequate calibration.** The user proxy (GPT-4o with the full issue specification) has three properties real users lack: perfect knowledge, perfect cooperativity, and perfect recall. The paper acknowledges this briefly in §7 ("may be more cooperative than real users") and states in §2.2 that "[t]he goal is not to simulate real users but provide the information injection." However, the abstract and introduction present the 74% improvement and 89% recovery figures without caveats—the abstract states "up to 74% over the non-interactive settings, underscoring the value of effective interaction" and §3.2 claims "interactive systems are essential for ensuring alignment and reducing safety risks." These are claims about the *value of interaction in general*, benchmarked against an environment where the user is maximally helpful. The 74% figure is an upper bound under ideal conditions, not an estimate of real-world gains. The within-study model comparisons remain valid, but the paper should consistently frame its absolute quantitative results as upper bounds, or provide a human calibration study (even small-scale) to ground them.

2. **Unequal turn budgets confound cross-model comparisons in RQ1.** Section 3.1 states that Claude Sonnet 4 and Qwen 3 Coder are allocated up to 100 interaction turns, while all other models are limited to 30, justified as "to account for their greater reasoning and planning capacity." This justification is circular—the capacity difference is what the evaluation aims to measure. Claude Sonnet 4's 89% recovery rate (vs. Sonnet 3.5's 80%) could partially reflect the 3× turn budget rather than genuinely superior interaction capability. This primarily affects cross-model comparisons in the Interaction setting; within-model Hidden-vs-Interaction comparisons are less affected since the budget is constant per model. The paper should either (a) equalize budgets, (b) run a budget-ablation (e.g., Sonnet 4 at 30 turns), or (c) explicitly discuss this confound's potential impact on specific comparisons.

3. **Claude Sonnet 4's Hidden-setting results use only 100/500 instances without clear selection criteria.** Footnote 4 states Claude Sonnet 4 is evaluated on "a subset of 100/500 instances in the Hidden setting" due to cost. The 40.00% Hidden resolve rate for Sonnet 4 therefore may not be a reliable estimate of its performance on the full 500-instance set. The paper asserts the findings are "still statistically significant" (citing Table 4 in the appendix), but the claim that a paired Wilcoxon test is valid requires that the 100 instances are a proper subset of the 500 used in the Interaction setting and that the same instances are paired—this needs explicit confirmation. Without knowing whether the subset was randomly selected, the comparison of Sonnet 4's Hidden (40.00% on 100) vs. Interaction (61.40% on 500) rates is uncertain.

### Minor

4. **The cosine distance metric for information gain (§5.1) likely confounds conversation length with meaningful information gain.** The metric computes cosine distance between embeddings of the task description *before* and *after* interaction, where the "after" embedding includes the full conversation history. Higher distance could largely reflect longer conversations rather than more useful information—consistent with the observed pattern that Qwen 3 Coder asks the most questions (6.02 avg) and has the highest distance (0.179). The paper acknowledges in §7 that this measure "weigh[s] all information equally," but does not address the length confound specifically. The LLM-as-judge scores and the qualitative analysis (§5.3) provide complementary evidence, but the cosine distance metric on its own has low face validity for measuring information gain.

5. **Construct validity of synthetic underspecification affects ecological validity.** The paper's own distributional analysis (§2.1) shows that naturally underspecified issues retain concrete technical details (code snippets, error messages, file/line references) that the GPT-4o-generated issues aggressively strip. The paper correctly notes the methodological necessity (paired ground truth), but the evaluation thus measures performance on an artificially clean form of underspecification. A "realistic" underspecification condition that retains some technical details while removing others would strengthen the claims about generalization to real-world scenarios.

### Trivial
None.

## Nice-to-Haves

- **Cost/efficiency analysis:** Reporting token costs or wall-clock time would make the practical trade-off between interaction and compute budget concrete.
- **Proxy quality characterization:** How often does the proxy respond "I don't have that information"? This would help characterize how much information models can actually extract.
- **Per-instance error analysis:** Which issues are most/least helped by interaction? Understanding the conditions under which interaction fails would strengthen the paper's diagnostic contribution.

## Removed Points

These points from the original review were removed (with justification):
- **"Hidden setting conflates underspecified input with disabled interaction prompt":** The paper's design is deliberate—RQ1 measures the combined effect, while RQ2 (detection) separately studies voluntary interaction under different prompt conditions. The paper already addresses this through its multi-experiment structure.
- **"Interaction is forced, so results are upper bounds":** The paper acknowledges this in footnote 3, and RQ2 separately studies voluntary interaction. This is an intentional design choice that the paper is transparent about.
- **"Section-by-section presentation notes" and "cost analysis," "I don't know rate," "error analysis":** These are minor suggestions or nice-to-haves, not weaknesses.
- **"The LLM-as-judge scores converge around 4/5, providing little discriminating signal":** The paper uses this metric alongside cosine distance and qualitative analysis; convergence among strong models is itself informative and consistent with the paper's main finding that most capable models can elicit relevant information when prompted.

## Novel Insights

The original review's most valuable synthesis is recognizing that the three-stage decomposition is the paper's core methodological contribution rather than a secondary feature. The fact that model rankings differ across the three stages (detection, question quality, integration) justifies the decomposition and explains why aggregate "resolve rate" metrics conceal important failure modes. The review also correctly identifies that the paper's most interesting finding is the *disconnect* between information extraction and integration—a pattern that would be invisible in a standard benchmark. This synthesis is implicit in the paper but the review helpfully makes it explicit.

## Suggestions

1. **Reframe quantitative claims as upper bounds under ideal interaction conditions.** Replace "interactivity can boost performance by up to 74%" (abstract) with language that consistently caveats the oracle nature of the user proxy. The within-study comparisons and qualitative findings do not need this caveat, but the absolute percentages do.
2. **Run a budget-ablation for at least one model** to separate the effect of interaction capability from the effect of having more turns. If Claude Sonnet 4 with 30 turns still achieves similar recovery rates, the claims are substantially stronger.
3. **Clarify the 100-instance subset selection** for Claude Sonnet 4's Hidden setting and confirm that the paired Wilcoxon test is computed on the same-instance subset.
4. **Validate or replace the cosine distance metric** for information gain by showing correlation with human judgments or downstream task performance.

## Score and Decision

**Score:** 6.0  
**Decision:** Accept

The paper makes a genuine contribution: a well-motivated dataset, a clean three-stage evaluation framework, and several non-obvious empirical findings. The limitations (oracle proxy, unequal budgets, subset evaluation) are real but primarily affect the *absolute* quantitative claims rather than the relative model comparisons or qualitative insights. With revision to reframe the headline numbers as upper bounds and address the methodological concerns, the contribution is clearly publishable at a top venue.

MY FINAL SCORE: <score>6.0</score>
MY FINAL DECISION: <decision>Accept</decision>