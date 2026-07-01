Now let me verify some specific claims from the reviewer more carefully, particularly around the budget mechanism and the ITS claims.Now I have a thorough understanding of the paper. Let me draft the review before calibration.Now let me proceed with calibration. Round 1 — Bracketing:Let me read the most relevant anchor papers for calibration.Now let me read the MINT review more closely (the remaining portion) as it's the most comparable anchor:Now I have sufficient calibration data. Let me form my bracket and finalize the review.

**Round 1 Bracket: 6.5–8.0**

Key comparisons:
- Clearly above rejected benchmarks (DB-GPT-Hub 3.75, TrustSQL 4.0)
- Comparable to or slightly above MINT (6.75) — similar multi-turn benchmark concept but BIRD-INTERACT has a more sophisticated simulator with stronger empirical validation
- Below Spider 2.0 (8.0) — Spider 2.0 received no major weaknesses, while BIRD-INTERACT has the budget leakage concern

The paper has one major but easily fixable issue (budget leakage) and several minor concerns. Its contributions are substantial and genuine. I'll place it at **7.0**.

---

## Summary
BIRD-INTERACT introduces a benchmark for evaluating LLMs on interactive, multi-turn text-to-SQL tasks. Its core contributions are: (1) a function-driven user simulator that mitigates ground-truth leakage via constrained symbolic actions; (2) dual evaluation settings—conversational (*c*-Interact) and agentic (*a*-Interact)—that reveal non-trivial differences in model behavior; and (3) a task suite covering full CRUD operations with systematically injected ambiguities and state-dependent follow-up sub-tasks. Results show even GPT-5 achieves only 8.67–17% end-to-end task completion, highlighting the difficulty of dynamic interactive text-to-SQL.

## Strengths
- **Function-driven user simulator addresses a real and important problem.** The two-stage design (semantic parsing into `AMB`/`LOC`/`UNA` → controlled response generation) measurably solves ground-truth leakage. Figure 6 shows baseline simulators fail on UNA questions at rates up to 67.4%, reduced to 2.7% with the proposed approach. This is a substantial and well-validated engineering contribution.
- **Dual evaluation modes surface genuinely informative model behavior differences.** GPT-5 achieves 14.50% priority-task SR in *c*-Interact (worst among all models) but 29.17% in *a*-Interact (best) (Table 2). This ranking inversion is a substantive finding that could not emerge from a single-mode benchmark and is well-supported by the data.
- **Knowledge-chain-breaking ambiguity injection is a well-designed mechanism.** By masking intermediate DAG nodes in the hierarchical knowledge base (Section 3.2, Figure 2), the benchmark creates ambiguities requiring multi-hop reasoning to detect and resolve—a principled approach grounded in the structure of the knowledge base.
- **Memory grafting experiment (Section 5.2, Figure 5) provides a novel diagnostic insight.** Demonstrating that GPT-5's poor *c*-Interact performance stems from interaction deficiencies rather than SQL generation capability (performance improves from 13.8% to 20.5% with O3-Mini's interaction history) is a finding with direct implications for model development.
- **Human-alignment study (Table 3) provides non-trivial validation.** Function-driven simulators achieve 0.84 Pearson correlation (p=0.02) with human-driven outcomes vs. 0.61 (p=0.14) for baselines, supporting the simulator's fidelity beyond self-evaluation metrics alone.

## Weaknesses

### Fatal
None

### Major
- **Budget formula leaks task-level information about the number of annotated ambiguities.** In *c*-Interact, τ_clar = m_amb + λ_pat (Section 4.1); in *a*-Interact, B = B_base + 2·m_amb + 2·λ_pat (Section 4.2). Since λ_pat (default 3) and B_base (6) are fixed constants and "systems are informed of the remaining budget" (Section 4), a model can trivially back-solve for m_amb. For example, in *c*-Interact, m_amb = τ_clar − 3. This provides a meta-signal about task difficulty that would not exist in real deployment. While knowing the *count* of ambiguities doesn't reveal their *content*, it allows models to allocate interaction turns strategically. The fix is straightforward (fixed or randomly perturbed budgets), and the paper should acknowledge this design artifact and analyze whether models exploit it.

### Minor
- **Human-alignment correlation is computed over only 7 data points (Table 3).** The correlations (0.84 vs. 0.61) are directionally informative but statistically fragile at n=7; a single outlier model could substantially shift the result. Bootstrapped confidence intervals or Spearman rank correlation would strengthen the analysis.
- **The "Interaction Test-Time Scaling Law" (Section 5.2) is overframed.** The paper defines: "A model satisfies this law if, given enough interactive turns, its performance can match or even surpass that of the idealized single-turn task." Figure 4 shows monotonic improvement in *c*-Interact for multiple models, but reaching/surpassing idealized performance appears model-dependent (convincingly demonstrated only for Claude-3.7-Sonnet). In *a*-Interact, curves are flat or decreasing. Calling this a "law" overstates the generality; "empirical observation" would be more accurate.
- **All results are single runs with no variance reporting.** Section 5 acknowledges "conducting single runs due to cost." For performance differences as small as 14.50% vs. 18.00% (Table 2), it is unclear whether these gaps exceed noise from sampling and simulator stochasticity. Even with single runs, bootstrapped confidence intervals over the task set could partially address this.
- **The two evaluation modes confound multiple design dimensions.** *c*-Interact and *a*-Interact differ simultaneously in protocol structure, budget formulation, action space, and debugging opportunities. The paper's attribution of the GPT-5 ranking inversion to "training data distributions and architectural inductive biases" (Section 5.1) is speculative; it could stem from any combination of these confounded factors.

### Trivial
None

## Nice-to-Haves
- A taxonomy of interaction strategies (e.g., asking about ambiguities early vs. late, exploring schema before vs. after querying the user) with quantitative evidence for which correlate with success would make findings more actionable. The paper mentions this analysis exists in Appendix P but it deserves main-text prominence.
- Failure analysis identifying which task types or ambiguity categories remain consistently unsolved by all models.
- Analysis of simulator failure modes for AMB and LOC categories (not just UNA), including how incorrect simulator responses affect downstream task success.
- A controlled ITS experiment varying budget per-task based on required clarifications, to distinguish "more turns help" from "better interaction strategy helps."

## Removed Points
*These points are flagged to be removed; treat them with caution.*

- **"Abstract GPT-5 numbers are misleading"**: REMOVED — The abstract says GPT-5 "completes only 8.67% of tasks," which refers to end-to-end task completion (follow-up SR). This is the natural meaning of completing a full task and is not misleading.
- **"Fixed n=2 sub-tasks limits generalizability"**: REMOVED — This is an explicit design choice (Table 1: "# sub-tasks / Task: 2"), and evaluating variable-length task sequences is outside the paper's stated scope. It would be a different benchmark.
- **"Inter-annotator agreement metric unspecified in main text"**: REMOVED — Details are likely in the appendix (stripped by parser), and the 93.33% agreement number is reported.
- **"Simulator may introduce biases in LOC responses"**: REMOVED — This is speculative; the paper does not claim perfection for LOC and the concern is not anchored to a specific observed failure.

## Novel Insights
The memory grafting experiment (Figure 5) is a genuinely novel diagnostic technique that decomposes interactive text-to-SQL performance into interaction quality and SQL generation capability. The finding that GPT-5 benefits substantially from other models' interaction histories suggests that interaction strategy and SQL generation are separable competencies that may require distinct training approaches. Additionally, the ranking inversion between *c*-Interact and *a*-Interact challenges the assumption that model capabilities transfer uniformly across interaction paradigms—a finding with implications for how interactive systems should be deployed and matched to specific use cases.

## Suggestions
- Use a fixed or randomly perturbed budget to prevent models from inferring m_amb from the communicated budget.
- Report Spearman rank correlations alongside Pearson for the human-alignment study, and consider expanding the model set in future iterations.
- Reframe "ITS Law" as an "ITS hypothesis" or "empirical observation" to match the evidence.
- Provide bootstrapped confidence intervals over the task set even with single runs—this is cheap to compute and would clarify which model ranking differences are meaningful.
- Consider an ablation isolating individual design differences between *c*-Interact and *a*-Interact (e.g., giving *c*-Interact models the same action space as *a*-Interact but keeping the protocol structure).

## Score and Decision

**Anchor papers retrieved:**

| Paper | Avg Score | Round | Comparison |
|---|---|---|---|
| Spider 2.0 (XmProj9cPs) | 8.0 | R1 | Accepted text-to-SQL benchmark; similar ambition but received no major weaknesses; BIRD-INTERACT has budget leakage concern |
| MMQA (GGlpykXDCa) | 8.0 | R1 | Accepted benchmark; well-received but had synthetic data concerns; BIRD-INTERACT has more novel engineering contributions |
| MINT (jp3gWrMuIZ) | 6.75 | R1 | Most comparable: multi-turn interaction benchmark with user simulation; BIRD-INTERACT has stronger simulator design and validation |
| CHASE-SQL (CvGqMD5OtX) | 6.25 | R1 | Accepted text-to-SQL method paper; narrower in scope than BIRD-INTERACT's benchmark contribution |
| ROUTE (BAglD6NGy0) | 6.25 | R1 | Accepted text-to-SQL method paper; less relevant as a comparison |
| SQL-GEN (RaSLSUCKz0) | 5.67 | R1 | Rejected text-to-SQL method; narrower scope |
| LAIA-SQL (WYdpjwKQma) | 5.0 | R1 | Rejected NL2SQL benchmark; weaker contribution than BIRD-INTERACT |
| EvoSchema (NfUHBaZdLw) | 4.25 | R1 | Rejected text-to-SQL robustness benchmark; less novel than BIRD-INTERACT |
| TrustSQL (7ZeoPg3eTA) | 4.0 | R1 | Rejected text-to-SQL benchmark; less innovative |
| DB-GPT-Hub (NmILZXKcOi) | 3.75 | R1 | Rejected text-to-SQL benchmark; limited innovation; clearly below BIRD-INTERACT |
| MMIE (HnhNRrLPwm) | 8.0 | R1 | Accepted multimodal benchmark; high quality but different domain |
| CABINET (SQrHpTllXa) | 8.0 | R1 | Accepted table QA paper; different focus |
| NEMESIS (5kMwiMnUip) | 1.4 | R1 | Strong reject; not comparable |
| Others in 1.0-3.0 range | 1.0-3.4 | R1 | Strong/clear rejects; not comparable to this paper |

**Round 1 bracket: 6.5–8.0**

BIRD-INTERACT is clearly above rejected benchmarks (DB-GPT-Hub 3.75, TrustSQL 4.0, EvoSchema 4.25) and above borderline papers (LAIA-SQL 5.0, SQL-GEN 5.67). It fills a genuine gap with a well-engineered contribution. Compared to MINT (6.75), the closest analog, BIRD-INTERACT offers a more sophisticated simulator with stronger empirical validation (USERSIM-GUARD + human alignment study), more interesting findings (ranking inversion, memory grafting), and a more comprehensive task suite (CRUD operations, state-dependent follow-ups). This suggests it sits above MINT. However, compared to Spider 2.0 (8.0), which received essentially no major weaknesses, BIRD-INTERACT has the budget leakage concern and some evidential limitations. This places it in the 7.0–7.5 range.

**Final score: 7.0**

The paper makes a solid, genuine contribution to the text-to-SQL evaluation landscape. The function-driven user simulator is a well-validated engineering innovation, the dual evaluation modes surface genuinely novel findings, and the benchmark fills an important gap. The major weakness (budget information leakage) is real but easily fixable and does not invalidate the benchmark's core design. The minor issues (statistical fragility of human-alignment study, ITS overframing, no variance reporting) are standard evidential limitations. This paper merits acceptance.

MY FINAL SCORE: <score>7.0</score>
MY FINAL DECISION: <decision>Accept</decision>