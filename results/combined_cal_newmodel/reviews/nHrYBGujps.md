Now I have all the information needed. Let me produce the final consolidated review.

---

## Summary

BIRD-INTERACT introduces a benchmark for evaluating text-to-SQL systems in dynamic, multi-turn settings—addressing limitations of prior benchmarks that rely on static transcripts and narrow SELECT-only evaluation. The benchmark features a function-driven user simulator (two-stage AMB/LOC/UNA action classification), two evaluation settings (c-Interact for conversational and a-Interact for agentic), and 900 tasks spanning the full CRUD spectrum with state-dependent follow-ups. Empirical results show that even the strongest models (GPT-5, Gemini-2.5-Pro) achieve only 8–25% success rates, highlighting a significant gap between single-turn SQL generation and the strategic interaction skills needed for real-world deployment.

## Strengths

- **Well-motivated benchmark design that addresses a genuine gap.** The paper correctly identifies limitations in existing multi-turn benchmarks: (a) reliance on static conversation transcripts that evaluate every system against the same predetermined trajectory, and (b) narrow SELECT-only scope ignoring the full CRUD spectrum and state-dependent follow-ups. The two evaluation settings (c-Interact and a-Interact) cleanly isolate different aspects of the interaction challenge.

- **Function-driven user simulator with compelling reliability evidence.** The two-stage approach (semantic parsing into AMB/LOC/UNA actions, then generating responses from ground-truth SQL via clarification sources) is a technically sound solution to the well-known problem of LLM-based simulators leaking ground-truth or generating inconsistent responses. The evidence in Figure 6—reducing UNA failure rates from 67.4% to 2.7%—is compelling and represents a meaningful engineering contribution that could benefit other interactive benchmarks beyond text-to-SQL.

- **The memory grafting experiment (Figure 5) is genuinely informative.** Providing GPT-5 with interaction histories from O3-Mini raises GPT-5's performance (20.5%) above O3-Mini's own performance (18.5%). This cleanly demonstrates that GPT-5's SQL generation capability is not the bottleneck—the bottleneck is its interaction strategy. This is the strongest evidence in the paper for the claim that communication effectiveness determines success in c-Interact.

- **CRUD coverage with state-dependent sub-tasks.** The inclusion of INSERT/UPDATE/DELETE and DDL operations, combined with sub-tasks where the follow-up depends on intermediate database state from the first query, extends beyond existing interactive benchmarks and is directly relevant to production database assistant scenarios.

## Weaknesses

### Fatal
None.

### Major

- **Single-run evaluations with no variance estimates undermine quantitative claims for a benchmark paper.** The paper states it conducts single runs with temperature=0 "due to cost" (Section 5). While temperature=0 reduces model-side variance, the user simulator itself uses an LLM-based semantic parser. More importantly, with no confidence intervals or multiple trials, it is impossible to assess whether observed differences between models (e.g., the 4 percentage point gap between the strongest and weakest model in c-Interact) are meaningful. For a benchmark paper that aims to define how the community evaluates interactive text-to-SQL, the absence of any variance estimate is a significant methodological weakness. Comparable benchmarks like τ-bench address this by proposing metrics like pass^k that explicitly measure reliability across trials.

- **The human alignment study (Table 3) is critically underspecified.** The paper reports correlations between human and simulator success rates across 7 models on 100 tasks but does not state how many human judges participated, their qualifications, how tasks were distributed, or inter-rater reliability—these details are deferred to Appendix O. The p-values themselves are concerning: the baseline GPT-4o simulator achieves p=0.14 (not significant), and the baseline Gemini simulator achieves p=0.21. The conclusion that the function-driven simulator "demonstrates significantly stronger alignment" rests on p=0.02 and p=0.03 from what is likely a small effective sample size per model (~14 tasks each). This is thin evidence for the claim that the simulator reflects "actual human-AI interaction patterns."

### Minor

- **The "ITS Law" claim is overstated relative to the evidence.** The paper defines "ITS Law" as: "A model satisfies this law if, given enough interactive turns, its performance can match or even surpass that of the idealized single-turn task" (line 207). Figure 4 shows that only Claude-3.7-Sonnet exhibits clear scaling behavior in c-Interact, while several models show flat or decreasing performance in a-Interact mode. If most models cannot approach the idealized single-turn baseline even with 7 interaction turns (patience=7), the "ITS Law" is not a general law—it is an observation about specific models in a specific setting.

- **The ambiguity injection methodology, while a reasonable design choice, is framed too ambitiously.** The benchmark creates ambiguities by removing knowledge nodes and making queries vague, pairing each with a clarification source derived from ground-truth SQL. This evaluates whether models can ask about pre-specified ambiguities, not whether they can identify genuinely unforeseen ambiguities. The paper's language of "restoring missing realism" and "high-fidelity interactive environment" overstates what is actually being measured. This is a useful controlled evaluation, but the framing should be more carefully qualified.

- **No breakdown by ambiguity type.** The paper defines three categories of ambiguity (superficial, knowledge, environmental) with two knowledge subtypes but does not report how many ambiguities of each type exist or per-category success rates. This makes it impossible to assess which categories drive performance and reduces the benchmark's diagnostic utility.

- **The claim that "ambiguous queries are unsolvable without clarification" (line 72) is asserted without empirical verification.** Running the best-performing model without allowing any interaction (forcing it to guess) would directly validate this claim. If success rates under this condition are near zero, the ambiguity injection is working as intended.

### Trivial
None.

## Nice-to-Haves

- Provide a breakdown of *why* models fail (failure to ask the right clarification vs. failure to interpret the clarification vs. failure to generate correct SQL vs. SQL that fails test cases). This would dramatically increase the benchmark's diagnostic value.
- Report the distribution of AMB/LOC/UNA actions triggered during evaluation and the rate at which the semantic parser misclassifies requests.
- Run a no-interaction baseline to empirically validate the claim that ambiguous queries are unsolvable without clarification.
- Provide per-ambiguity-type success rates to reveal which interaction skills matter most.

## Removed Points

These points are flagged to be removed; treat them with caution.

- The original reviewer's claim that the ambiguity injection methodology is a "fundamental" or "structural" concern was downgraded to Minor. Constructing controlled tasks with known ambiguities is standard benchmark practice, and the paper is transparent about its methodology. The overclaiming about "realism" is a framing issue, not a fatal methodological flaw.
- The original reviewer's section-by-section notes about budget comparability between c-Interact and a-Interact were removed. The paper explicitly acknowledges the different budget designs, and the two settings are intentionally different because they test different interaction paradigms (conversational vs. agentic). Different budget mechanisms are appropriate for different paradigms.
- The comment about the LLM-as-Judge confound in USERSIM-GUARD was removed because the paper's main evidence (Figure 6) is a clear quantitative comparison of failure rates that does not depend on the LLM judge's absolute validity for the headline claim (the dramatic reduction from 67.4% to 2.7% is a large enough effect to be credible regardless of any judge bias).
- The point about user simulator action distribution transparency was moved to Nice-to-Haves.
- The point about "no analysis of why models fail" was moved to Nice-to-Haves because it would strengthen the paper but is not a core flaw given the paper's primary contribution is the benchmark itself.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. **Add confidence intervals** to the main results (Table 2) via bootstrap over tasks. Even a simple approach (resampling tasks with replacement, computing SR for each resample, reporting 95% CI) would significantly strengthen the quantitative claims.
2. **Report full human alignment study details** in the main text: number of judges, qualifications, task distribution, inter-rater reliability, and the effective sample size for each correlation. The benchmark's validation depends on this evidence.
3. **Either substantiate the "ITS Law" claim** with evidence across more models and settings, or reframe it as an observation about specific models showing marginal improvement with additional interaction turns. The term "law" sets an expectation the current evidence does not support.
4. **Provide per-ambiguity-type breakdowns** of success rates to increase the benchmark's diagnostic utility and help the community understand which interaction skills matter most.

## Score and Decision

### Calibration Anchors

All anchors retrieved across rounds:

| Path | Avg Score | Round | Itemized? | Comparison |
|------|-----------|-------|-----------|------------|
| `/home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/roNSXZpUDN.md` (τ-bench) | 6.50 | R2 | Yes | Most directly comparable: interactive benchmark with LLM-simulated user, two domains, similar scope. Slightly stronger on statistical methodology (pass^k metric), slightly weaker on simulator design. |
| `/home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/XmProj9cPs.md` (Spider 2.0) | 8.00 | R1 | Yes | Higher-quality benchmark with real-world enterprise workflows, no major methodological weaknesses flagged. |
| `/home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/GGlpykXDCa.md` (MMQA) | 8.00 | R1 | Yes | Multi-table QA benchmark with thorough evaluation; minor synthetic data concerns but strong overall. |
| `/home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/7ZeoPg3eTA.md` (TrustSQL) | 4.00 | R1 | Yes | Lower-rated text-to-SQL reliability benchmark with significant methodological issues. |
| `/home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/CvGqMD5OtX.md` (CHASE-SQL) | 6.25 | R1 | No | Method paper, not directly comparable to benchmark contribution. |
| `/home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/BAglD6NGy0.md` (ROUTE) | 6.25 | R1 | No | Method paper, not directly comparable. |

**Round 1 bracket**: 5.5–7.0. The paper is clearly stronger than TrustSQL (4.0) but has more methodological weaknesses than Spider 2.0 (8.0). The closest comparable is τ-bench (6.50).

**Round 2 narrowing**: Compared to τ-bench (6.50), BIRD-INTERACT has a stronger simulator design (the function-driven approach is a real improvement over standard LLM simulators, which τ-bench's own reviewers flagged as a weakness). However, BIRD-INTERACT is weaker on evaluation methodology (single runs with no variance vs. τ-bench's pass^k) and has an underspecified human alignment study. The τ-bench reviewers raised concerns about simulated user realism (favorability ~1.5–2.8), which BIRD-INTERACT's function-driven approach partially addresses. BIRD-INTERACT's two major weaknesses have favorability ratings of +0.60 (single-run) and −0.09 (human alignment) from the scoring model, while τ-bench's main weaknesses cluster around −2.32 to +2.5. The shared pattern (simulated-user concerns + evaluation methodological concerns) places BIRD-INTERACT slightly below τ-bench due to the variance issue being more acute for a benchmark paper. Final score: **6.0**.

**MY FINAL SCORE: <score>6.0</score>**
**MY FINAL DECISION: <decision>Accept</decision>**