## Summary

InnoGym proposes a benchmark and framework for evaluating AI agents along two dimensions: **performance gain** (improvement over known best solutions) and **novelty** (methodological dissimilarity from prior approaches). The paper contributes (1) a formal quadruple framework $(P, S, V, D)$ for defining innovation, (2) a curated set of 18 *Improvable Tasks* drawn from real competitions, (3) a unified execution environment (iGym), and (4) an empirical evaluation showing that current agents produce novel approaches but lack the robustness to translate them into performance gains.

---

## Strengths

1. **Principled formalization of an underevaluated dimension.** The decomposition of innovation into Performance Gain (G) and Novelty (N) is clean and well-motivated. The quadruple formalism $(P, S, V, D)$ provides a generalizable language for describing tasks in terms beyond correctness, and the taxonomy of Solved/Improvable/Exploratory problems (Section 2.3) usefully scopes where the benchmark applies.

2. **Rigorous task curation.** The two-stage filtering (197 → 72 → 18 tasks) with attention to resource availability, evaluator correctness, domain balance, and standardization (evaluator normalization, validator construction, data partitioning) reflects serious engineering effort. The tasks span diverse domains (OR, ML, systems, science) and are genuinely "improvable" — the right design choice for an innovation benchmark.

3. **Honest reporting of uniformly negative results.** Table 2 candidly reports that no agent achieves positive performance gain on any task, and none surpass human baselines. The finding that agents can achieve moderate-to-high novelty while performing worse than near-baseline solutions (e.g., RCIC: Novelty=83.33, Gain=−99.67) is an honest diagnosis of the creativity–robustness gap.

4. **Insightful controlled analysis on Circle Packing.** Section 4.3 is the paper's strongest experimental contribution: the complex-plane representation (Fig. 5b) elegantly visualizes the G/N trade-off, and the temporal dynamics (G increasing, N decreasing over time) and temperature analysis (sweet spot at 0.5–0.75) demonstrate the metrics' ability to produce nontrivial insight beyond what correctness-only benchmarks provide.

---

## Weaknesses

### Fatal
None.

### Major

1. **Novelty metric rests on an unvalidated LLM-as-judge procedure, with no validation summary in the main text.** The distance function $D$ — the linchpin of the novelty dimension — is instantiated via a pipeline: Codex extracts a structured representation, then GPT-5 rates dissimilarity along six rubric dimensions (0–4 each), which are averaged, min-aggregated over known solutions, and rescaled to $[0, 100]$. The main text provides **no evidence** that this procedure yields meaningful or reliable measurements. Specifically: (a) the six rubric dimensions are not described in the main text (deferred to Appendix H.2), (b) no correlation with human judgments is reported, (c) no inter-annotator or inter-prompt agreement is given, and (d) no analysis of sensitivity to surface-level vs. genuinely different strategies is provided. The paper states "We provide a more detailed analysis of the behavior and reliability of D in Appx. F" (line 186), but for a benchmark whose distinguishing contribution *is* measuring novelty, a summary of that validation belongs in the main text. *Severity: Major — this does not invalidate the paper (the performance dimension and task curation stand independently), but it means the paper's primary novel claim is unsubstantiated in the presented text.*

2. **Misleading cross-framework comparison via averages over different task sets.** In Table 2, "/" entries (no valid submission) are excluded from each framework's average. Because MLAB produced valid submissions on 7/10 tasks, CodeAct on 5/10, and AIDE on 5/10, the averages in the final row are computed over **different task subsets** for each framework. The paper then claims "MLab leads in both Performance Gain and Novelty" without qualifying that this comparison is over non-identical task sets. This is methodologically problematic: a framework that succeeds only on easy tasks could appear to outperform one that attempts harder tasks.

3. **"Best of 3" reporting without run-level statistics.** Each configuration is run three times, and only the best score is reported (line 209). This conflates one success out of three with three successes out of three, making it impossible to assess the robustness that the paper itself emphasizes as "the foremost challenge." On tasks where frameworks produce valid submissions in only some runs (the "/" entries), the run-level failure rate would be highly informative. The paper's central finding — that agents lack robustness — is undercut by a reporting protocol that cannot measure robustness.

### Minor

1. **Inconsistent treatment of GPT-5.** Section 4.1 cites "GPT-5 (OpenAI, 2025a)" as a real model alongside DeepSeek-v3.1 and Gemini-2.5-Pro, while Section 4.3 (line 257) refers to "a hypothetical GPT-5." If GPT-5 is a real model the results are empirical; if hypothetical they are projections. This must be resolved for the results in Fig. 6(b) to be interpretable.

2. **Innovation taxonomy introduced but never applied.** Section 2.2 defines three innovation categories (breakthrough, performance, conceptual) but no solution in the experiments is classified into any of them. This is a missed opportunity to demonstrate the framework's descriptive power.

3. **"First benchmark" claim needs qualification.** The paper states "the first benchmark specifically designed to evaluate the innovation potential of AI agents" (line 9, line 26) but cites related work (Ruan et al. 2025, Qiu et al. 2025) that evaluates idea generation. The distinction (on-task execution vs. speculative ideation) is legitimate but should be stated explicitly in the claim to avoid an easily raised objection.

4. **iGym contribution under-articulated in the main text.** Section 3.5 (6 lines plus a figure caption) describes iGym's capabilities but does not explain how it differs from OpenHands, AutoGen, or LangGraph in concrete design terms, deferring entirely to Appendix C. As a claimed contribution (item 3), this is too thin for the main text.

5. **"MLab leads" claim unqualified.** The statement "MLab leads in both Performance Gain and Novelty" (line 217) is based on averages computed over different task sets (see Major #2), and no statistical test is provided to assess whether the observed differences are meaningful.

### Trivial
- The paper lacks an explicit limitations section; the reliance on LLM-as-judge, the selection of 10/18 tasks, and the scope (only Improvable Tasks) all merit one.
- It is unclear which 8 of the 18 tasks are excluded from the main evaluation and why.

---

## Nice-to-Haves

- Report run-level statistics (e.g., number of successful submissions out of 3 for each configuration) or mean/variance across runs.
- Include a summary of novelty metric validation in the main text: correlation with human expert judgments, ablation of pipeline components (e.g., Codex extraction vs. direct rating), and sensitivity to surface-level vs. strategic differences.
- Apply the innovation taxonomy from Section 2.2 to classify specific solutions in the experimental section.
- List the 8 tasks not evaluated and clarify the selection criteria.

---

## Removed Points

These points were raised in the input review but are removed per filtering rules; treat them with caution as they may be irrelevant or incorrect:

- **"V(s) hard threshold" observation** (Section 2.1): This is a design choice observation, not a weakness. The paper notes $C(s) \in \{0,1\}$ as standard. Removed because it is an observation rather than a concrete problem.
- **"Discarded tasks (72→18)" question**: The critic asks what the 54 removed tasks looked like. This is a reasonable question but does not identify a flaw in the paper; the paper honestly reports the attrition rate. Removed as speculation rather than a verifiable weakness.
- **Strengths about "addressing an important problem" / "filling a real gap"**: These are generic and lack specific evidentiary grounding in the paper's execution. Only strengths backed by concrete content are retained.
- **"Strongest part of the experimental section" (Circle Packing)**: Retained in Strengths as "insightful controlled analysis" with specific evidence.
- **Section-by-section notes that are stylistic or editorial** (e.g., "this section is too thin," "this feels like a missed opportunity," "this is standard but worth noting"): These are observations rather than verifiable weaknesses. Where substantive (iGym thinness, unused taxonomy), they are included as Minor weaknesses with specific anchors.

---

## Novel Insights

None beyond the paper's own contributions. The reviews offer no alternative interpretation or novel observation that the paper does not already articulate.

---

## Suggestions

1. Move a one-paragraph summary of Appendix F's novelty metric validation (correlation with human judges, ablation results) into the main text — ideally into Section 3.4 or 4.1.
2. Report per-framework averages only over the intersection of tasks where all frameworks produced valid submissions, or explicitly note that averages are over different task sets.
3. Include run-level success rates (e.g., "X/3 runs produced valid submissions") to support the robustness claims.
4. Resolve the GPT-5 inconsistency: either consistently treat it as a real, tested model or explicitly label Fig. 6(b) results as projections.
5. Add a brief limitations paragraph discussing the LLM-as-judge dependency, the 10/18 task selection, and the exclusion of Solved and Exploratory problems.

---

## Score and Decision

The paper addresses a genuine gap in agent evaluation with a well-motivated framework and carefully curated tasks. The honest reporting of negative results and the insightful Circle Packing analysis demonstrate the benchmark's value. However, the paper's central distinguishing contribution — measuring novelty — depends on an LLM-as-judge distance function whose validation is deferred entirely to the appendix, with no summary in the main text. Additionally, the cross-framework comparison in Table 2 is weakened by averages computed over different task sets, and the "best of 3" protocol undercuts the robustness claims. These issues are addressable but require non-trivial clarification and supplementation. On balance, the paper represents a solid contribution with significant but fixable weaknesses.

**Score: 6** — borderline accept. The framework and task curation have value, but the novelty metric validation must be convincingly demonstrated (not merely referenced) and the evaluation methodology needs tightening.

MY FINAL SCORE: <score>6</score>
MY FINAL DECISION: <decision>Accept</decision>