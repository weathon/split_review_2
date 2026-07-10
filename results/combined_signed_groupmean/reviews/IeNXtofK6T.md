Now I have all the information I need. Let me compose the final review.

**Round 1 bracket:** [5.5, 7.0] — the two decisive weaknesses (-8.66, -10.00) pull the paper down from the 7+ range, while the very strong decisive strengths (+10.00, +9.96, +9.22) push it above the 5.5 range.

**Round 2 narrowing:** Compared against Rapid Response (5.75, reject), JudgeRail (5.75, reject), GuardAgent (6.00, reject), Agent Security Bench (6.25, accept), Robust LLM Safeguarding (5.75, accept). My paper has a cleaner, more impactful core contribution than Rapid Response and JudgeRail. It is slightly stronger than GuardAgent (6.00) whose weaknesses were about fundamental generalizability (task-dependence) while my paper's weaknesses are fixable (missing experiment, framing). The two major weaknesses do not invalidate the core empirical finding. I place the paper at **6.0**.

Here is the final review:

## Summary

This paper revisits the idea of using an off-the-shelf LLM as a guardrail to detect and remove prompt injection attacks against LLM agents. The core finding is that with modern LLMs (GPT-4o, GPT-4.1), a simple prompting-based approach achieves near-perfect detection (FPR < 1%, FNR < 1% on AgentDojo) and reduces attack success rate from 54.53% to 0.00% (GPT-4.1), overturning the earlier finding from 2023–2024 that this approach was ineffective. Experiments span three benchmarks, include useful ablations (model size vs. reasoning, prompt strategies, open-source Qwen3 models), and address data contamination and adaptive attacks.

## Strengths

- **Clear empirical finding with practical importance (Tables 1, 2).** The paper demonstrates that prompting GPT-4o or GPT-4.1 as a guardrail achieves genuinely strong detection (FPR < 1%, FNR < 1% on AgentDojo; both below 5% on Open Prompt Injection and TensorTrust) and reduces ASR from 54.53% to 0.00% (GPT-4.1). This directly revises the established finding from Liu et al. (2024) that prompting-based defenses were ineffective. The evidence for this core result is strong and directly actionable.

- **Thorough ablation on model capacity vs. reasoning (Section 4.4, Figure 3).** The controlled experiment using Qwen3 models at three sizes (0.6B, 8B, 32B) in both reasoning and non-reasoning modes cleanly separates the effects of model scale and reasoning capability. The finding that 0.6B models cannot simultaneously achieve low FPR and FNR regardless of reasoning mode, while 32B models approach GPT-4.1's performance, is informative for practitioners managing cost-effectiveness tradeoffs.

- **Memorization test (Section 4.5).** The paper directly addresses the plausible alternative explanation that strong benchmark performance is due to data contamination, running a standard memorization test (Carlini et al.; Staab et al.) on GPT-4.1 and reporting average similarity 0.34 with only 3.5% of samples exceeding the 0.6 threshold. This strengthens the credibility of the results.

- **Adaptive attack evaluation (Section 4.6, Table 4).** The paper goes beyond static benchmark evaluation by using AgentVigil to generate attacks optimized specifically against PromptArmor, achieving ASR of only 0.16% even under this adaptive setting.

## Weaknesses

### Major

- **Unsupported empirical assertion about prompt strategy robustness (Section 4.3).** The paper states that "newer models like GPT-4o and GPT-4.1 perform equally well across different prompting strategies" but presents data only for GPT-3.5, not for GPT-4o or GPT-4.1. The reader therefore cannot verify whether the headline 0% ASR result is robust to sloppy prompts or depends on careful prompt engineering. This is a directly testable claim the paper should have included.

- **Framing vs. practical accessibility tension.** The paper titles itself "An Essential Baseline" and all headline results (0.00% ASR, 72.02% UA) use GPT-4.1, a costly proprietary API model. Every tool call an agent processes requires a separate GPT-4.1 or GPT-4o call, multiplying both latency and cost. The Qwen3-32B results (0.99% FPR, 0.33% FNR, 0.15% ASR) partially address this, but the paper provides no cost or latency quantification to help practitioners evaluate deployability, and the "Computational efficiency" rationale (Section 3.2) discusses only training cost, ignoring inference cost. The paper's claim to be a "standard baseline" is undercut if the best configuration requires expensive proprietary access.

### Minor

- **Removal pipeline under-analyzed.** The paper claims removal (vs. discarding the entire input) as a key differentiator from prior work, but the mechanism is described in a single paragraph (Section 3.1) with no analysis of failure modes. On false positives, the fuzzy matcher could remove benign content, degrading utility in ways not captured by aggregate FPR. This is a methodological gap for a claimed differentiator.

- **No cost or latency data.** Given that PromptArmor calls a frontier LLM on every data sample (and a single AgentDojo task involves many tool calls), practical deployability depends heavily on these factors, which are unquantified.

- **Unexplained UA discrepancy.** The Figure 3 caption includes "No defense: 94.27" for UA while Table 2 reports "No defense" UA as 64.27%. These differ by 30 percentage points without explanation.

- **Asymmetric baseline comparison (Table 2).** PromptArmor-GPT-4.1 is compared against Deberta, Llama Prompt Guard 2, and DataSentinel (fine-tuned Mistral-7B)—models orders of magnitude smaller. While approach-level comparison is valid, the experiment conflates method choice with model capacity. A controlled comparison using the same underlying model would strengthen the claim.

- **No error analysis.** The paper reports aggregate FPR/FNR but does not characterize the types of prompts that trigger false positives or false negatives. Understanding failure modes would help practitioners assess risk.

### Trivial

None.

## Nice-to-Haves

- Provide a reproducible baseline configuration (e.g., Qwen3-32B with a fixed prompt) and explicitly nominate it as the recommended baseline, with full cost estimates.
- Show data for GPT-4o and GPT-4.1 in the prompting-strategies experiment (Section 4.3) to actually support the claim about their insensitivity to prompt formulation.
- Analyze the removal pipeline on false positives: what happens to benign data that is incorrectly flagged?
- Report the number of guardrail LLM calls per task and approximate API cost per 1,000 tasks.

## Removed Points

These points are flagged to be removed, treat them with caution:

- **Detection prompt adjustments (Critical Issue 2 from the harsh critic).** Removed because the paper states the prompts are in Appendix C (line 322), which was stripped by the parser. The rules require removing weaknesses about missing appendix content.
- **Abstract claim "below 5%" is slightly misleading.** Removed because the numbers are numerically correct (GPT-4o FNR 2.38% on Open Prompt Injection, 4.61% on TensorTrust; GPT-4.1 FNR 4.24% on Open Prompt Injection). This is a nitpick without substance.
- **Section 3.2 "Computational efficiency" ignores inference cost.** Removed because the paper's claim is specifically about avoiding *training* costs ("avoids the significant costs associated with developing and training custom security models"), which is correct. The paper also acknowledges that smaller models can work.
- **Strength: "Clear empirical finding with practical importance."** The impact model scored this at +10.00. This is a genuine strength, retained above.

## Novel Insights

None beyond the paper's own contributions. The review's observations largely recapitulate what is visible from the paper: the core finding is strong and well-supported, but the "essential baseline" framing outruns the evidence for accessible configurations, and one empirical claim about prompt robustness is unsupported.

## Suggestions

1. Run the Section 4.3 prompting-strategies experiment on GPT-4o and GPT-4.1 and report the results. If the claim is correct, this will strengthen the paper; if not, it will reveal a genuine limitation.
2. Nominate Qwen3-32B (already evaluated) as a recommended reproducible baseline configuration, and provide cost/latency estimates.
3. Resolve the UA discrepancy between Figure 3 and Table 2.
4. Add an error analysis section characterizing false positive and false negative cases.
5. Analyze the removal pipeline's behavior on false positives.

## Score and Decision

All anchor papers retrieved across rounds:

| Path | Avg Score | Round | Itemized? | Comparison |
|------|-----------|-------|-----------|------------|
| 5kMwiMnUip.md (NEMESIS) | 1.40 | R1 | No | Much weaker; trivial jailbreaking exploration |
| 8QTpYC4smR.md (Systematic Review) | 1.00 | R1 | No | Survey paper, no empirical contribution |
| 3MDmM0rMPQ.md (Inverse Prompt Engineering) | 3.00 | R1 | No | Interesting idea but weaker evaluation |
| MV5j4Qpq7N.md (System-Prompt Attention) | 2.33 | R1 | No | Limited empirical support |
| 0VZP2Dr9KX.md (Baseline Defenses) | 5.25 | R1 | Yes | Similar theme of establishing baselines, but had fatal methodological flaws (single attack, trivial defenses) |
| V4y0CpX4hK.md (Agent Security Bench) | 6.25 | R1 | Yes | Different category (benchmark paper), stronger in scope |
| YixNDE12wm.md (GuardAgent) | 6.00 | R1 | Yes | Similar guardrail concept, rejected due to task-dependent generalizability concerns |
| MsRdq0ePTR.md (Prompt Injection Benchmark) | 5.25 | R1 | Yes | Limited novelty, reproducibility issues |
| V892sBHUbN.md (Rapid Response) | 5.75 | R2 | Yes | Weaker contribution; had incorrect reporting and insufficient adaptivity |
| CEvGuwMum0.md (JudgeRail) | 5.75 | R2 | Yes | Weaker; limited novelty in core concept |
| s5orchdb33.md (Robust LLM Safeguarding) | 5.75 | R2 | No | Accept; different approach (adversarial training) |

**Round 1 bracket:** [5.5, 7.0] — the two decisive weaknesses (-8.66, -10.00) pull the paper down from the 7+ range, while the very strong decisive strengths (+10.00, +9.96, +9.22) push it above the 5.5 range.

**Round 2 narrowing:** Compared against anchors in the bracket, my paper has stronger decisive strengths (+10.00, +9.96) than Rapid Response and JudgeRail (both 5.75, rejected), whose fatal weaknesses were more fundamental (incorrect reporting methodology, missing comparisons, lack of novelty). Compared to GuardAgent (6.00, rejected), my paper has a similar strength profile but the two major weaknesses (unsupported claim, framing) are fixable rather than fundamental (GuardAgent's weaknesses were about task-dependent generalizability). The -10.00 weakness (unsupported claim in Section 4.3) is about a missing experiment the authors could easily run; it does not invalidate the paper's core finding, which is well-supported across Tables 1, 2, 4, Figure 3, and the memorization test.

**Final score:** 6.0 — borderline accept. The paper makes a clear, empirically sound contribution that revises an established finding, but the unsupported assertion about GPT-4o/4.1 prompt robustness and the tension between "essential baseline" framing and proprietary API dependence are notable weaknesses that the authors should address.

MY FINAL SCORE: <score>6.0</score>
MY FINAL DECISION: <decision>Accept</decision>