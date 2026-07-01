## Summary

This paper introduces a formal model of controlled sequential social learning, in which an information-mediating planner (e.g., an LLM-powered system) strategically chooses the precision of private signals for a sequence of agents who also learn socially from predecessors' actions. The authors characterize optimal policies for both altruistic planners (maximizing agent welfare) and biased planners (inducing a specific action), proving convexity of the altruistic value function and revealing qualitatively distinct multi-phase regimes (no investment at extreme beliefs, maximum investment at moderate beliefs, and threshold-based precision in intermediate regions). LLM-based simulations are used to illustrate the framework.

## Strengths

1. **Clean, tractable model that captures a genuinely underexplored dynamic.** The paper formalizes the interplay between an information-controlling planner and sequential social learning — a setting increasingly relevant as LLMs mediate information at scale. The model (Section 3) distills the essential tension (planner-controlled signal precision + Bayesian social learning + information cascades) into a stationary MDP with public belief as state, which is well-specified with clear reward and transition functions (Equations 4–6).

2. **Non-trivial convexity result (Theorem 2).** The proof that the altruistic value function is convex in public belief is technically involved and of independent interest. The reward function involves a `min(b, 1-b, 1-q)` term that is concave in b, making convexity preservation under the Bellman operator non-trivial. This result enables the clean characterization in Theorem 3.

3. **Insightful multi-phase characterization of optimal policies (Theorems 3 and 5).** The three-phase structure for the altruistic planner and the five-phase structure for the biased planner are genuinely informative. The finding that a biased planner may intentionally *decrease* signal precision below baseline (lines 184–186, 199–200) to trap agents in a favorable cascade is a non-obvious and interesting result.

4. **Honest treatment of assumptions.** Remark 2 (line 117) explicitly acknowledges three key limitations and discusses when each is or is not restrictive. This is more transparent than standard practice and helps readers calibrate the scope of the results.

## Weaknesses

### Fatal

None.

### Major

1. **The empirical evaluation lacks essential reporting details.** The LLM-based experiments (Section 6) are presented with insufficient methodological transparency to support the weight placed on them:
   - **No sample sizes, error bars, or statistical tests.** The paper reports that "the deviation is less than 10% for the majority of belief states" (line 242) and that "the biased analytical and LLM planners decreased social welfare by 40 to 50%" (line 252), but provides no indication of variance across runs, number of trials, or statistical significance. The histogram in Figure 2b is described qualitatively with no indication of how many data points it aggregates over.
   - **Parameter values used for figures are not reported.** The paper states that "k, baseline precision p, and discount factor δ" are varied (line 212) but never states which specific values were used to generate any of the figures shown. Without this, the results are not interpretable or reproducible from the main text.
   - **The main text does not identify which LLM model was used.** The paper repeatedly refers to "LLMs" acting as planner, agent, and oracle but does not state which model(s) (GPT-4, Claude, Llama, etc.) were employed. This is a basic omission that prevents assessment or reproducibility.

   The experiments are presented in Contributions as "Empirical Validation" (line 33). At minimum, the main text should specify the model used and report the parameter values, number of runs, and variance measures for the quantitative claims made.

2. **The most interesting empirical claim — that the LLM planner adapts to non-Bayesian agents — is asserted without supporting quantitative evidence.** The paper introduces a "hybrid" setting (optimal policy + LLM agents) which is the necessary counterfactual to support the claim that the LLM planner deviates "in ways which account for the non-Bayesian nature of the LLM agents" (line 218). The paper states that in the hybrid setting the optimal policy is "brittle" and "its performance suffers" (line 254), but no quantitative comparison between the hybrid setting and the LLM planner setting is provided. The most interesting empirical finding in the paper is therefore the least supported.

### Minor

1. **Oracle validation is only referenced in the appendix without any summary in the main text.** The paper states "In Appendix E.3, we validate both the beliefs and the performance of the oracle" (line 212). Given that the Oracle's ability to generate signals of a specified precision is central to whether the experimental setup faithfully instantiates the model, a brief summary of this validation (e.g., correlation between intended and achieved precision) should appear in the main text to allow readers to assess the setup's validity without consulting the appendix.

### Trivial

None.

## Nice-to-Haves

- The cost function β(q) is described differently for the altruistic planner (cost only above baseline p) versus the biased planner (cost for any deviation from p). Being explicit about whether these different cost structures are required by the objectives or are modeling choices would help comparability.
- The paper could usefully note that all agents share the same preference (match the state). This is standard in the literature but worth flagging for readers outside the social learning community.

## Removed Points

These points are flagged to be removed; treat them with caution.

1. **Criticism about the "structural gap" between Bayesian theory and non-Bayesian experiments (Issue 2 from the harsh critic).** The paper explicitly acknowledges that LLM agents are non-Bayesian (Section 6.1) and frames the comparison as testing robustness. This is not a structural flaw but a deliberate research design choice. The specific evidential gap (the hybrid setting claim being unsupported) is retained as Major weakness 2 above — the broader framing as a "structural gap" is removed.

2. **Criticism about the Oracle's role being non-transparent (Issue 3 from the harsh critic).** The paper references Appendix E.3 which validates the oracle. The appendix is stripped by the parser, but it exists in the original submission. The concern about missing summary in the main text is retained as Minor weakness 1.

3. **Criticism about LLM model identity not being identified.** This information is likely in Appendix E (referenced at line 212), which is stripped by the parser. The concern is retained as part of Major weakness 1 but specifically about the main text not including it, not about the paper overall lacking it.

4. **Generic strength: "The problem is timely and well-motivated."** This is not specific enough to the paper's concrete content. It is folded into the evaluation but removed as a standalone strength.

## Novel Insights

None beyond the paper's own contributions. The reviews do not contribute a perspective that the paper itself does not already articulate or imply.

## Suggestions

1. **Substantially expand the experimental reporting.** Specify the LLM model and version in the main text. Report the number of independent runs, variance/error bars for all quantitative claims, and the specific parameter values (k, p, δ) used to generate each figure. This is essential whether the experiments are framed as validation or as illustration.

2. **Quantitatively report the hybrid setting comparison.** The claim that the LLM planner outperforms the analytically optimal policy when facing non-Bayesian LLM agents is the paper's most novel empirical finding. It must be supported with numbers, not just a qualitative assertion.

3. **Include a brief summary of the Oracle validation in the main text** (even one sentence with a correlation measure between intended and achieved precision).

4. **Either reframe Section 6 as "illustrative case study" rather than "empirical validation"** to match the level of rigor currently on offer, or bring the experimental methodology up to the standards implied by "validation."

## Score and Decision

MY FINAL SCORE: <score>6</score>
MY FINAL DECISION: <decision>Accept</decision>