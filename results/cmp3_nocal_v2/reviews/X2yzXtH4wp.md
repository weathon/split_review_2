## Summary

This paper introduces Ambig-SWE, a benchmark derived from SWE-Bench Verified that creates underspecified variants of GitHub issues alongside their fully-specified counterparts. The authors decompose the problem of handling underspecification into three capacities—detecting missing information, asking targeted clarification questions, and integrating the answers—and evaluate six LLM-based agents (proprietary and open-weight) across these dimensions using a GPT-4o simulated user. The central empirical finding is that interaction can improve performance on underspecified inputs by up to 74% over non-interactive baselines, but most models default to non-interactive behavior and struggle at reliable detection. Notable findings include Qwen 3 Coder's complete non-responsiveness to interaction prompts despite strong standalone performance, and Claude models' exploration-first questioning strategy that achieves comparable information gain with ~50% fewer questions.

## Strengths

- **Structured decomposition of the interaction problem.** The paper breaks "handling underspecification" into three distinct capacities (detection, questioning, integration) and designs targeted evaluations for each. This is a genuine methodological advance—most prior work treats underspecification monolithically—and gives practitioners concrete axes for improvement.

- **Clean experimental design with paired ground truth.** Ambig-SWE creates underspecified variants of SWE-Bench Verified issues that have verified fully-specified counterparts, enabling causal measurement of interaction value (the same issue can be compared with and without interaction). The authors also provide a distributional analysis comparing their synthetic underspecification to natural underspecified issues and are transparent about differences. This is good practice for a benchmark paper.

- **Non-obvious empirical findings.** Several results provide concrete guidance for agent design: (a) Qwen 3 Coder's 100% FNR across all interaction prompts despite strong SWE-Bench performance is a striking and actionable failure mode; (b) the disconnect between information extraction volume and task performance (Qwen extracts the most information but doesn't use it effectively); (c) Claude models' exploration-first strategy extracting comparable information with substantially fewer questions. These findings make the paper worth publishing beyond the benchmark contribution.

## Weaknesses

### Fatal
None.

### Major

- **RQ2 measures "interaction decisions," not "detection ability."** The RQ2 experiment (§4) frames its metric as measuring whether models "detect" underspecification, but the operationalization conflates detection with the decision to act. Non-interaction on an underspecified input could reflect (a) failure to detect missing information *or* (b) detection combined with a strategic choice not to ask (e.g., reliance on parametric knowledge). Qwen 3 Coder illustrates the problem: its 100% FNR is presented as a detection failure, but the paper's own §3.2 shows Qwen achieves the highest Hidden resolve rate (45.6%) by relying on internal knowledge. The paper mentions this behavior in §3.2 but never connects it back to the RQ2 framing. The FPR/FNR analysis should be described as measuring "interaction decisions" rather than "detection accuracy." This does not invalidate the experiment—the data are still informative—but the conclusions are broader than the evidence supports.

### Minor

- **The "74% improvement" headline is an ideal-conditions upper bound not foregrounded as such.** The interaction setting uses GPT-4o as a simulated user proxy that never misunderstands the agent, never gets impatient, and always has the right answer. This measures improvement achievable with a *perfectly cooperative* user, not a realistic one. The paper acknowledges this in §7 ("our simulated user proxy may be more cooperative than real users") and §2.2 ("The goal is not to simulate real users"), but the abstract and introduction present the 74% figure as "underscoring the value of effective interaction" without caveat. The results are valid as an upper bound; calibrating the headline language to reflect this would substantially improve the paper.

- **LLM-as-judge metric in RQ3 has a circular dependency.** GPT-4o serves as both the simulated user proxy (generating answers) and the judge scoring those answers for "specificity and novelty" (§5.1). This means GPT-4o evaluates its own responses. The cosine distance metric (§5.1) provides an independent signal that partially mitigates this, but the paper's qualitative claims about question quality rely in part on the LLM-as-judge scores (Figure 6). A model that asks questions GPT-4o finds easy to answer will naturally receive higher scores from GPT-4o-as-judge.

- **Hidden vs. Interaction comparison conflates prompt addition with actual interaction.** The Hidden setting gives no interaction-related instructions; the Interaction setting adds an explicit prompt to interact (footnote 3). The "improvement" from Hidden to Interaction therefore reflects two changes: (a) adding an interaction prompt and (b) actual interaction. A cleaner baseline would give the Interaction prompt but disable the user proxy, isolating the effect of prompting from the effect of interaction.

- **Data leakage mentioned without discussion (§3.2).** The paper states "Some models achieve higher resolve rates in the Hidden setting likely due to their superior programming acumen, or data leakage." If data leakage is a real concern, this warrants discussion about which models might be affected and how it impacts the comparison. If not, the phrase should be removed or clarified. As written it introduces ambiguity about a core result.

- **Distributional analysis dismisses conversational fragments too quickly (§2.1).** The paper notes that natural underspecified issues have more conversational fragments and stream-of-consciousness phrasing, then claims these "may not directly impact agent performance since agents cannot access external information." But conversational fragments are cues about user uncertainty, not external information—their absence in Ambig-SWE could make detection *harder* than in natural settings, which would affect RQ2 findings. This deserves acknowledgment.

- **Claude Sonnet 4's 100/500 Hidden subset noted only in a footnote (§3.1).** The model is evaluated on 100 of 500 Hidden instances due to cost. The authors report the findings remain statistically significant (Table 4 in the appendix), which is reasonable, but the reduced sample size and its implications for the 40% Hidden resolve rate should be noted in the main text, not just footnote 4.

### Trivial

- Statistical significance details (Wilcoxon p-values) are deferred to the appendix (Table 4). The key significance test supporting the 74% improvement claim should be summarized in the main text.

## Nice-to-Haves

- **Analysis of which information dimensions matter most.** The paper distinguishes "navigational" vs. "informational" information (§3.3) but does not systematically analyze which specific dimensions of missing information (file paths, error descriptions, behavioral constraints, etc.) are most and least recoverable through interaction. Given the structured evaluation framework, this is a natural extension.

- **Separate detection from action policy experimentally.** For RQ2, prompting models to output a detection judgment *before* deciding whether to interact (e.g., "First, state whether the instructions contain sufficient information. Then proceed.") would give a cleaner measure of detection ability separate from action policy.

## Removed Points

These points were raised in the input review but are removed after cross-checking against the paper:

- **"Multiple interdependent gaps" claim not empirically characterized:** This is used as motivation for the multi-step evaluation framework (§1 introduction), not as an empirical claim about the dataset. Criticizing it as uncharacterized is outside the paper's stated scope for RQ1-RQ3.
- **Cherry-picked examples in Figure 4:** The qualitative analysis in §5.3 uses illustrative examples from one issue while supporting its broader claims with quantitative data (Table 6, Figure 5). This is standard practice, not a weakness.
- **Missing analysis of information types:** This is a nice-to-have extension, not a weakness. The paper is well-positioned to do this but is not deficient for not including it.

## Novel Insights

The harsh review surfaces a genuinely insightful critique that goes beyond what the paper authors claim: the disconnect between RQ2's "detection" framing and what the experiment actually measures (interaction decisions) is not merely a labeling issue—it interacts with the paper's most striking finding. Qwen 3 Coder's 100% FNR is presented as a detection failure, but the paper's own §3.2 evidence (highest Hidden resolve rate, reliance on internal knowledge) suggests it may instead be a *policy failure* (choosing not to ask despite detecting the gap). This reframing changes the interpretation: Qwen's problem is not that it can't detect underspecification, but that it has been trained to over-rely on parametric knowledge rather than engage in dialogue. This distinction matters because the remediation strategies differ (detection training vs. dialogue-policy training). The review also correctly identifies that the "interaction improves performance" headline conflates two variables (prompt presence + actual interaction), again separating what the authors treat as a single behavioral finding into distinct components that future work should isolate.

## Suggestions

1. Reframe the RQ2 findings as measuring "interaction decisions" rather than "detection accuracy," and explicitly discuss the Qwen 3 Coder case where detection and action policy diverge.
2. Calibrate the 74% headline claim to reflect that it measures improvement under ideal simulated-user conditions (e.g., "Under ideal interaction conditions with a perfectly responsive simulated user...").
3. Add a brief main-text summary of the Wilcoxon significance tests supporting the Hidden-vs-Interaction comparisons.
4. Clarify or remove the "data leakage" speculation in §3.2.
5. Acknowledge in §2.1 that the absence of conversational fragments in Ambig-SWE may affect detection difficulty relative to natural settings.

## Score and Decision

MY FINAL SCORE: <score>7</score>
MY FINAL DECISION: <decision>Accept</decision>