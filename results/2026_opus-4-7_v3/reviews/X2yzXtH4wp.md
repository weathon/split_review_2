Now let me read the remaining sections to verify specific claims.Now I have thoroughly verified the reviewer's claims against the paper. Let me compile my draft review.Now let me do Round 1 calibration — bracketing pass:Let me read a few key anchor papers to calibrate scoring:Now let me read the MINT paper's lower-scoring review (the one that gave 5) to better understand the borderline for benchmark papers:Now I have sufficient calibration data. Let me synthesize my final review.

**Round 1 Bracket Summary:**
- Strong reject (1.0): Fundamentally broken papers — Ambig-SWE is far above this
- Reject (3.0-3.2): DataSciBench — quality issues, unclear motivation. Ambig-SWE significantly better
- Borderline reject (4.0-4.5): Codev-Bench, Tests as Instructions — some contribution but missing details and unsurprising findings. Ambig-SWE has more insightful findings
- Borderline accept (5.75-6.75): MINT, AgentBench, ScienceAgentBench, ML-Bench — solid benchmarks with clear contributions. MINT is broader (20 models, 8 datasets) but had similar user simulation concerns. Ambig-SWE is narrower but deeper.
- Accept (8.0): PhysBench, Spider 2.0 — comprehensive, well-validated benchmarks

**Initial bracket: 5.0–6.5**

The confound issue and headline imprecision are real but not fatal. The three-part decomposition and non-obvious findings are genuine contributions. The paper is stronger than the rejected benchmarks but narrower in scope than accepted benchmarks like MINT. Let me finalize the review.

---

## Summary
Ambig-SWE introduces an underspecified variant of SWE-Bench Verified to evaluate LLM agents' ability to handle underspecification in software engineering. The paper decomposes interactive problem-solving into three distinct capabilities—detection of underspecification, quality of clarifying questions, and leveraging interaction to improve task completion—and evaluates six proprietary and open-weight models across these dimensions, finding that interaction substantially improves resolve rates but models struggle with detection and vary widely in question strategies.

## Strengths

- **Useful three-part decomposition reveals capability independence.** The paper's breakdown into detection, question quality, and integration reveals that high performance on one axis does not imply high performance on another. Concretely, Qwen 3 Coder extracts the most information (0.179 cosine distance, Figure 5) but completely fails at detection (100% FNR across all prompts, Table 2), while Claude Haiku 3.5 achieves similar relative recovery (~80% of Full) as Claude Sonnet 3.5 despite substantially weaker coding ability (Section 3.2). This demonstrates that interaction capability is partially independent of raw coding skill, a non-obvious finding.

- **Concrete, actionable model-comparison findings.** The observation that Qwen 3 Coder's resolve rate *worsens* when given navigational information (55.43% → 52.38%, Table 1) due to rigid protocol-following is a specific, well-evidenced finding. The analysis of question strategies (Section 5.3) revealing that Claude Sonnet 4 achieves comparable information gain to Qwen with 50% fewer questions (4.03 vs 6.02) through exploration-first strategies provides concrete guidance for agent design.

- **Appropriate statistical methodology.** Wilcoxon signed-rank tests for paired binary outcomes (Section 3.1) provide appropriate statistical grounding for the core comparisons between settings, going beyond raw percentage differences.

## Weaknesses

### Fatal
None.

### Major

- **System prompt confound in the central Hidden vs. Interaction comparison.** The Hidden setting uses no interaction-related instructions while the Interaction setting makes interaction "compulsory" (Section 3.1, footnote 3: "Without compulsory interaction, the model defaults to non-interactive behavior"). This means the improvement from Hidden to Interaction conflates two effects: (a) the actual informational benefit of user answers and (b) the behavioral effect of a substantially different system prompt that instructs the model to pause and assess completeness before coding. The missing control is straightforward: run models with the Interaction prompt but with the user proxy always responding "I don't have that information." The pattern of results (e.g., differential effects of navigational vs. informational details in Table 1, models extracting more information not always performing better) provides indirect evidence that actual information matters, but without this control, the *magnitude* of the interaction benefit is not cleanly identified. This weakens the precision of the paper's central quantitative claim.

- **Headline "up to 74% improvement" claim is not clearly derivable from presented results.** Computing relative improvement (Hidden→Interaction)/Hidden from Figure 3 yields: Claude Haiku 100%, Claude Sonnet 3.5 63.6%, Claude Sonnet 4 53.5%, Llama 50%, Deepseek 32.1%, Qwen 18.0%. Computing gap recovery (Hidden→Interaction)/(Hidden→Full) yields: Claude Sonnet 4 76.4%, Claude Haiku 65.7%, Claude Sonnet 3.5 61.1%, Qwen 43.2%. No computation exactly matches "74%." The paper's central quantitative claim should be precisely traceable to its data.

### Minor

- **Claude Sonnet 4 evaluated on only 100/500 instances in the Hidden setting** (footnote 4) without describing the selection method (random, stratified, first 100?). Since statistical tests compare Hidden (100 instances) to Interaction (500 instances), this asymmetry introduces potential selection bias that is not addressed.

- **Synthetic underspecification creates uniform information removal.** The paper's own distributional analysis (Section 2.1) reveals their approach uses "more aggressive information removal, specifically targeting code snippets and error messages" while natural underspecified issues have heterogeneous gaps (some missing file locations but including error traces, etc.). The authors justifiably explain they cannot use natural examples without paired ground truth, but this means Ambig-SWE tests one specific type of underspecification. Validation on even a small set of naturally occurring underspecified issues would improve generalizability confidence.

- **Detection metric's binary framing may conflate detection failure with strategic compensation.** An agent might correctly identify missing information but choose to compensate through codebase exploration rather than user interaction—this registers as a false negative (FNR) despite being a potentially reasonable strategy. Qwen 3 Coder appears to adopt exactly this approach (Section 3.2: "relies on its internal knowledge for key insights about missing information"), yet the paper treats its 100% FNR as a pure detection failure.

- **"Cumulative knowledge after interaction" in the cosine distance metric (Section 5.1) is not precisely defined.** It is unclear whether this is the concatenation of the summarized issue and all user responses, the agent's questions plus responses, or some other construction. The metric's sensitivity and interpretability depend on this specification.

### Trivial
None.

## Nice-to-Haves

- **Per-instance analysis** of when interaction helps vs. hurts (by repository, issue complexity, or type of underspecification) would reveal heterogeneity masked by aggregate resolve rates.
- **Deeper investigation** of the disconnect between information extraction and task performance (Section 5.2) — categorizing what types of information gained distinguish resolved from unresolved instances would make this interesting finding actionable.
- **Enriched detection evaluation** that measures whether agents that choose not to interact on underspecified inputs compensate through other strategies (e.g., more exploratory codebase reads), connecting detection behavior to downstream performance.

## Removed Points

*These points are flagged to be removed; treat them with caution.*

- **WEAKNESS (removed — speculative):** "SWE-Bench Verified annotation rubric might have false negatives, with some verified issues still partially underspecified." This is speculative—there is no evidence in the results that this is actually causing problems.
- **WEAKNESS (removed — paper acknowledges):** "User proxy provides strictly more information than the Full setting by including file modification locations." The paper explicitly acknowledges this design choice in Section 2.2 and partially addresses its implications through the navigational vs. informational analysis in Table 1 and Section 3.3.
- **WEAKNESS (removed — paper acknowledges):** "Cosine distance treats all information as equally valuable." Already acknowledged in Section 7 as a limitation.
- **WEAKNESS (removed — scope creep):** "Variance or confidence intervals on resolve rates not reported." The Wilcoxon tests provide statistical grounding for the key comparisons; demanding additional uncertainty quantification on all point estimates is beyond standard practice for this type of benchmark evaluation.
- **STRENGTH (removed — generic):** "Practical relevance of the problem" — this applies to any paper on underspecification and is not specific enough to count as a concrete strength of this particular paper.

## Novel Insights

The disconnect between information extraction and task performance is a genuinely novel empirical finding: Qwen 3 Coder extracts the most information through interaction (highest cosine distance) but achieves similar resolve rates to Claude Sonnet 4, while Claude Sonnet 3.5 and Haiku extract nearly identical information (0.136 vs 0.135) despite vastly different task performance (39.6% vs 26.8%). This suggests that information *integration* capability is a distinct axis from information *extraction* capability — a finding that has implications beyond software engineering for any interactive agent system.

## Suggestions

1. **Add the missing control condition:** Run models with the Interaction-encouraging prompt but with the user proxy always responding "I don't have that information." This isolates the prompt effect from the interaction effect with minimal additional infrastructure.
2. **Derive and specify the "74%" headline number** with an explicit formula, model reference, and computation — or replace it with a precisely traceable statistic.
3. **Report the sampling procedure** for Claude Sonnet 4's 100-instance Hidden subset and verify that these 100 instances are a proper subset of the 500 Interaction instances.
4. **Precisely define the embedding construction** for "cumulative knowledge after interaction" in Section 5.1.
5. **Consider enriching the detection evaluation** to distinguish between detection failure (agent doesn't recognize missing information) and strategic compensation (agent recognizes the gap but chooses exploration over interaction).

## Score and Decision

**Calibration Anchors (all from Round 1):**

| Paper | Path | Avg Score | Round | Comparison to Ambig-SWE |
|-------|------|-----------|-------|------------------------|
| NEMESIS (jailbreaking) | 5kMwiMnUip | 1.40 | R1 | Far weaker — no real contribution |
| Systematic LLM Review | 8QTpYC4smR | 1.00 | R1 | Far weaker — survey with no novelty |
| Cross-Lingual Robots | gwZ90hFSL2 | 1.00 | R1 | Far weaker — questionable contribution |
| Financial Markets NN | nSDOkm0SKo | 1.00 | R1 | Far weaker — hypothetical scenario |
| DataSciBench | BltaWJZMeR | 3.20 | R1 | Weaker — quality issues, unclear motivation. Ambig-SWE has clearer design and more insightful findings |
| D2Coder | dsALpkd1OU | 1.67 | R1 | Far weaker — excessive reliance on LLM reasoning |
| Improve Code Gen w/ Feedback | CscKx97jBi | 3.00 | R1 | Weaker — limited novelty. Ambig-SWE has more structured evaluation |
| SOP-Agent | oWm80iR1m9 | 3.00 | R1 | Weaker — more procedural, less insightful findings |
| Codev-Bench | c2C2NQKjZw | 4.25 | R1 | Somewhat weaker — missing details, unsurprising findings. Ambig-SWE has non-obvious findings |
| FEABench | hDkLpu1E64 | 4.50 | R1 | Similar tier — reasonable benchmark but limited scope |
| MLE-Bench | 6s5uXNWGIh | 4.60 (human avg) | R1 | Similar scope but MLE-Bench was actually accepted (8.0 avg); listed avg seems wrong. Different case. |
| Tests as Instructions | sqciWyTm70 | 4.00 | R1 | Weaker — limited insights, highly variable reviews |
| AgentBench | zAdUB0aCTQ | 6.20 | R1 | Stronger — broader (8 environments, 27 models) but criticized for limited novelty. Ambig-SWE has deeper analysis but narrower scope |
| ScienceAgentBench | 6z4YKr0GK6 | 6.00 | R1 | Similar strength — expert-validated benchmark. Ambig-SWE has a confound issue but also has more targeted insights |
| ML-Bench | sf1u3vTRjm | 5.75 | R1 | Similar — repository-level ML benchmark. Ambig-SWE has more structured evaluation |
| MINT | jp3gWrMuIZ | 6.75 | R1 | Stronger — broader (20 models, 8 datasets), similar user simulation concern. Ambig-SWE is narrower but deeper in analysis |
| PhysBench | Q6a9W6kzv5 | 8.00 | R1 | Stronger — comprehensive, well-validated |
| MMQA | GGlpykXDCa | 8.00 | R1 | Stronger — comprehensive multi-table benchmark |
| Spider 2.0 | XmProj9cPs | 8.00 | R1 | Stronger — real-world enterprise benchmark |

**Round 1 bracket: 5.0–6.5**

The paper sits between rejected benchmarks with quality issues (DataSciBench 3.2, Codev-Bench 4.25) and accepted benchmarks with broader scope (MINT 6.75, AgentBench 6.2). The confound in the central experiment and the imprecise headline claim are real issues that prevent clean acceptance, but the three-part decomposition and genuinely non-obvious findings (capability independence, Qwen rigidity, information extraction ≠ integration) represent solid contributions. The paper is stronger than the 4.x-range rejected benchmarks but narrower and methodologically less clean than the 6.x-range accepted benchmarks.

Compared to MINT (6.75), Ambig-SWE is narrower in scope (6 models vs 20, 1 dataset vs 8) and has a more notable confound issue. Compared to ScienceAgentBench (6.0) and ML-Bench (5.75), Ambig-SWE offers comparable depth of analysis but the confound issue is a differentiator. The paper's insights are genuine and the decomposition framework is useful, but the methodological gap in its central experiment — which could be resolved with one additional control condition — prevents confident acceptance.

**Final score: 5.5** — Borderline paper with genuine contributions (useful benchmark, insightful decomposition, non-obvious findings) held back by a notable experimental confound in the central comparison and imprecise headline claims. With the missing control condition addressed, this would likely score in the 6.0–6.5 range.

MY FINAL SCORE: <score>5.5</score>
MY FINAL DECISION: <decision>Reject</decision>