## Summary

PELICAN proposes a two-stage adaptive tutoring framework that (1) diagnoses a student's cognitive state via collaborative questioning using a successor-first strategy and an expert-assistant-verifier pipeline, then (2) tutors adaptively by selecting strategies from a pool using fast/slow thinking (dual-system theory). Evaluated on the Gaokao dataset with both simulated and human experiments (169 students, 1,335 tutoring reports).

## Strengths

1. **Well-motivated problem with clear illustration.** Figures 1 and 2 concretely demonstrate why one-size-fits-all LLM responses fail for students at different cognitive levels, making the gap the paper addresses immediately understandable.

2. **Real human-in-the-loop evaluation.** Section 4.6 reports a study with 169 real high school students and 1,335 tutoring reports. This goes well beyond purely simulated evaluation and is a genuine strength for an AI-in-education paper.

3. **Sensible architectural design.** The successor-first diagnostic strategy (prioritizing leaf nodes whose prerequisites are already evaluated) is a clean and efficient way to leverage hierarchical knowledge structures. The expert-assistant-verifier pipeline is a simple but reasonable quality-control mechanism for generated questions. The two-stage design (diagnose-then-tutor) is well-motivated.

## Weaknesses

### Major

- **Numerical inconsistency between Table 2 and Tables 3/4 for the same method.** The PELICAN row in Table 2 (main results) reports R_coverage=72.36 and F_frequency=72.06. The same PELICAN (GPT-4o) in Tables 3 (module ablation) and 4 (backbone ablation) reports R_coverage=54.84 and Frequency=61.47 — gaps of **17.5 and 10.6 points** respectively. The paper offers no explanation. This makes it impossible to know which numbers reflect the method's actual performance and undermines confidence in the quantitative claims. The human evaluation (Table 6, R_coverage=70.04) is closer to Table 2 but computed on a different setup, so it does not resolve the inconsistency.

- **Abstract's headline numbers cannot be traced to any reported result.** The abstract claims "+18.7% improvement in critical thinking stimulation" and "+22.4% improvement in task completion rates." No table reports a metric labeled "critical thinking" or "task completion rate." The closest proxy (Inspiration in Table 2) shows PELICAN at 4.21 vs. best baseline at 3.99 (~5.5% relative gain), far from 18.7%. The closest proxy for task completion (Success rate in Table 6) shows PELICAN at 86.8% vs. best baseline at 86.5% (+0.3pp), far from 22.4%. The paper does not specify which baseline or metric produced these advertised numbers, making the paper's strongest claims unverifiable from the presented data.

### Minor

- **Human evaluation shows only marginal gains on the headline metric.** In Table 6, PELICAN's success rate (86.8%) is nearly identical to Sepwise (86.5%) and only 1.6pp above Free-Prompt (85.2%). The simulated evaluation showed much larger gaps; the paper's claim that the human results "exhibit strong consistency" with Table 2 is overstated. The real-world improvement over simple baselines is modest.

- **Ablation results show removing slow thinking barely hurts overall and even improves Inspiration.** In Table 3, "w/o. slow" achieves Inspiration of 4.46 vs. PELICAN's 4.30 — the ablated version is *better* on this dimension. While other metrics do degrade (R_coverage 49.44 vs. 54.84), the differences are modest. The paper's emphasis that these modules are "key" is not strongly supported by the ablation evidence.

- **Slow-thinking threshold M=1 makes it the default, not an exception.** The paper states slow thinking activates when dialogue rounds on a sub-task exceed M=1. This means after a single unsuccessful round, the system uses the expensive slow-thinking process (~230k tokens, ~40% of total usage). This undercuts the claimed fast/slow dichotomy and has practical cost/latency implications not discussed.

- **Primary metrics (R_coverage, F_frequency) measure process, not learning outcomes.** These metrics capture whether the system *addresses* non-mastered knowledge points, not whether the student actually learns. The paper's core claim about improving learning outcomes is not directly evidenced by these metrics.

- **GPT-based evaluation of GPT-generated outputs is a known confound.** The paper uses GPT-4o to assess outputs from GPT-4o-based systems. This introduces a potential model-preference confound that is not discussed or controlled for.

- **Strategy distribution analysis (Figure 4) contradicts the paper's own textual claims.** Seven of the nine strategies (Suggestion, Confirmation, Correction, Open Question, Closed Question, Simplification, Decomposition) are used at *identical* rates across all three cognitive levels (e.g., Open Question: 5%/5%/5%). Only Explanation (32/33/30) and Analogies (22/18/15) vary. The paper claims "for higher-level students, teachers tend to use questioning strategies," but both Open and Closed Question are fixed at 5% across levels — the data does not support the claim.

- **No ablation isolating the Simulated Teaching Tree from the strategy pool.** The ablation removes all slow thinking at once, so it is unclear whether the benefit comes from the Tree-search simulation or simply from having a curated strategy pool available.

- **Case study (Section 4.5) is illustrative but not evidential.** It asserts PELICAN's response is better than alternatives but provides no empirical basis (e.g., expert ratings of the compared responses).

### Trivial

None.

## Nice-to-Haves

- An explicit description of how the simulated student works in the main text (currently deferred to Appendix G, stripped by the parser).
- A comparison of slow-thinking cost vs. benefit: how many rounds of slow thinking per session, and what is the wall-clock latency?
- A discussion of failure cases: when does the expert-assistant-verifier pipeline fail to reach agreement? What happens when slow thinking selects a suboptimal strategy?
- A validation of the simulated student behavior against real student data.

## Removed Points

- **"Simulated student setup not specified"** — REMOVED. The paper states "Design details of the student role (Appendix G)" on line 278; this was stripped by the parser, not omitted by the authors.
- **"ANOVA analysis not assessable"** — REMOVED. The paper states ANOVA is in Appendix K.1 (line 284) and Appendix I (line 418); stripped by the parser.
- **"No comparison to IRT/NeuralCDM"** — REMOVED. The paper's diagnostic approach is interactive LLM-based questioning in a fundamentally different paradigm from traditional psychometric models; a fair comparison would require aligning entirely different input formats and the paper's evaluation is appropriately scoped.
- **"No comparison to contemporary systems"** — PARTIALLY REMOVED. The paper does compare against Socratic (Liu et al., 2025) and Bridge-Based (Wang et al., 2024b), which are published LLM-based tutoring methods. The claim that no published frameworks are compared is not accurate.
- **"Would benefit from more baselines"** — REMOVED as generic. The existing set covers prompting, stepwise, and strategy-based approaches and is reasonable for a first evaluation.

## Novel Insights

None beyond the paper's own contributions. The most salient observation — the numerical inconsistency between main results and ablation/backbone results — is a factual discrepancy in the paper's reporting rather than a novel scientific insight.

## Suggestions

1. **Resolve the numerical inconsistency** between Table 2 and Tables 3/4. If the tables report results under different experimental conditions (different evaluation splits, different random seeds, different student simulator configurations), state this explicitly and explain why the differences are expected. This is the single most important fix.
2. **Trace the abstract's headline numbers** (+18.7%, +22.4%) to a specific table entry and named baseline so readers can verify the advertised gains.
3. **Discuss why the human evaluation** shows much smaller advantages than the simulated evaluation, and what this implies about the framework's real-world impact versus the simulated setting.
4. **Report the slow-thinking activation threshold as a sensitivity analysis** (e.g., M=1, M=2, M=3) to demonstrate the robustness of the fast/slow design choice.
5. **Add an outcome-focused metric** (e.g., pre/post-test accuracy gain, near-transfer performance) to complement the process metrics (R_coverage, F_frequency).

## Score and Decision

The paper addresses a real and important problem with a sensible architectural design and a genuine human evaluation. However, the evaluation has two major issues that prevent acceptance: (1) an unexplained numerical inconsistency in the main tables that makes the core quantitative claims unreliable, and (2) the abstract's strongest advertised numbers cannot be verified from any reported result. The paper's contributions are real, but the evidence as presented does not meet the standard needed to substantiate the claims.

MY FINAL SCORE: <score>4</score>
MY FINAL DECISION: <decision>Reject</decision>