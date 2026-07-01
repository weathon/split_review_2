Now I have read the full paper. Let me draft the review before calibration.Now let me run Round 1 calibration — bracketing across score bands with topically relevant queries:Let me read a few key anchors for comparison:Now let me read one more anchor to sharpen my calibration — the SafeDPO paper's remaining reviews and the "Safety Alignment" paper to compare quality:Now I have sufficient calibration data to finalize the review. Let me synthesize everything.

**Round 1 Bracket Analysis:**
- **Strong reject (< 1.5):** Papers like NEMESIS (1.4), survey papers (1.0) — fundamentally flawed or no contribution. The IPO paper is clearly far above these.
- **Reject (1.5–3.5):** Code-of-thought (3.0), Planning in Strawberry Fields (3.0) — limited novelty, evaluation-only. IPO is clearly better with genuine analytical and methodological contributions.
- **Borderline reject (3.5–5.5):** MODPO (4.25), GenerativeRM (4.5), MOSLIM (4.0) — incremental extensions. IPO has stronger novelty and more comprehensive evaluation.
- **Borderline accept (5.5–7.5):** SafeDPO (6.4, Reject), SCDPO (6.0, Reject), 3D-Properties (6.25, Accept), SuperCorrect (6.5, Accept). IPO is comparable to or better than these — more novel analysis framework, stronger empirical breadth.
- **Accept (7.5–8.5):** Backtracking (8.0, Accept) — similar spirit (safety + intervention during generation), simple and effective. IPO has more detailed analysis but also more issues (over-refusal, narrow analysis base).
- **Strong accept (8.5+):** "Safety Alignment... Few Tokens Deep" (9.5) — comprehensive, multi-attack analysis. Clearly stronger than IPO.

**Initial bracket: 6.5–7.5**

Now let me produce the final review:## Summary
This paper addresses the under-explored problem of unsafe intermediate reasoning in Large Reasoning Models (LRMs), showing that even safety-aligned LRMs produce harmful reasoning traces despite safe final responses. The authors introduce the Continuation Safety Ratio (CSR) metric to analyze safety dynamics during reasoning, identifying "safety triggers" (steps that consolidate safe reasoning) and "compliance cues" (steps that amplify unsafe continuations). Based on these insights, they propose Intervened Preference Optimization (IPO), which replaces compliance cues with safety triggers at the divergence point and trains with partial DPO. Experiments across three LRMs and three safety benchmarks show IPO reduces harmful reasoning by over 30% relative to baselines while preserving reasoning capabilities.

## Strengths

- **Concrete, quantitative evidence for a real problem.** Figure 2 demonstrates that existing aligned LRMs maintain substantial unsafe reasoning despite safe responses — e.g., RealSafe-7B shows 52.2% harmful reasoning vs. 2.4% harmful responses on WildJailbreak. Figure 3 further quantifies that safe reasoning is near-sufficient for safe responses (the "Safe Reasoning + Unsafe Response" category is ≤0.6% for DS-8B and DS-7B), making a precise case for reasoning-level alignment rather than a generic safety argument.

- **CSR analysis is a genuine analytical contribution.** Rather than qualitative observation, the paper defines the CSR metric (Eq. 1), locates turning points (Eq. 2), and connects them to linguistically interpretable structures. The 0.85 Pearson correlation between compliance cue indices and CSR turning points (Figure 5b) is a concrete, reproducible finding. This systematic framework for identifying safety-critical reasoning steps goes meaningfully beyond prior qualitative work (e.g., Zhou et al., 2025b).

- **Analysis-driven method design.** IPO's mechanism — replace compliance cues with safety triggers, train with partial DPO from the divergence point — follows directly from the three empirical insights, giving the method a principled foundation. The reward shaping interpretation (Section 3.4 Remark), connecting CSR to value functions and potential-based shaping, provides additional theoretical grounding.

- **Strong experimental results with good breadth.** Table 2 shows IPO achieves the best average reasoning safety across all three models (15.3%, 18.4%, 13.9%), substantially outperforming both SFT-based and RL-based baselines. Reasoning capabilities are preserved or improved: IPO models achieve the highest or near-highest average scores on AIME, MATH-500, GPQA, and HumanEval across all three model families.

- **Meaningful ablation studies with practical implications.** Table 3 validates robustness to compliance cue detector choice (GPT-4o, DeepSeek-R1, DS-8B all yield strong results) and confirms partial DPO's superiority over full-trajectory alternatives (10.9% vs. 42.3% SFT, 19.0% full DPO). The computational efficiency analysis (Section 4.3: ~14 generations/prompt vs. ≥40 for GRPO; 40 min vs. 2+ hours) is a practical advantage.

## Weaknesses

### Fatal
None

### Major

- **Narrow empirical foundation for core mechanistic claims.** The CSR analysis (Sections 3.1–3.3) — which underpins the entire method — is conducted on only 30 prompts from JailbreakBench using a single model (DS-8B). Section 3.1 states: "we pick 30 prompts from JailbreakBench for which the completions exhibit uncertainty in their safety." JailbreakBench consists of "directly malicious prompts" (Section 2.1), which are relatively simple compared to StrongReject's multi-step attacks or WildJailbreak's diverse jailbreak scenarios. While the paper extends the CSR visualization to Qwen3-8B in the appendix (Figure 10) and reports "consistent" trends, it does not test whether the safety trigger / compliance cue structure holds on harder benchmarks. The method's strong downstream performance provides indirect support, but does not validate the specific mechanistic claims (e.g., that compliance cues are discrete, identifiable turning points in more sophisticated attack settings). This is a bounded but real evidential gap between the specificity of the claims and the breadth of the supporting analysis.

- **Substantial over-refusal addressed with an ad-hoc two-stage fix.** XsTest compliance drops from 98.1% to 71.2% for DS-7B (a ~29% refusal rate on benign prompts) and from 98.4% to 80.0% for DS-8B (Table 2). This is addressed by a second DPO stage using 915 benign prompts (Section 4.1), but this mitigation is not motivated by the same analysis that underpins the safety alignment and is not integrated into the IPO framework. The over-refusal is architecturally predictable: training the model to strongly pivot at compliance cues will over-apply to benign prompts. The sequential patch is a reasonable engineering solution but makes the claimed "simple" method a two-stage pipeline. Note: IPO's over-refusal is still better than some safety-focused baselines (RealSafe: 33.1% for DS-7B, 47.5% for DS-8B), and Qwen3-8B shows only a modest drop (99.3% → 91.0%).

### Minor

- **Limited Qwen3-8B comparison.** For Qwen3-8B, only GRPO serves as a baseline because "the SFT-based methods only release weights for R1 models" (Section 4.1). While this is an understandable practical constraint, comparing IPO against a single baseline on the third model weakens the generalizability claim for non-R1 model families.

- **GPT-4o used for both data construction and evaluation.** GPT-4o serves as the safety judge for all evaluation metrics (Section 2.1), the compliance cue detector during data construction (Section 3.4), and implicitly as the validator of safety triggers. The paper validates compliance cue detection against human annotation at "over 80% consistency" (Section 3.4) — only moderate agreement. No corresponding human validation is reported for the more consequential task of evaluating reasoning safety. The Table 3 ablation with alternative detectors partially mitigates construction-side concerns, but the evaluation-side circularity remains unaddressed.

- **Generic trigger pool.** Only 6 safety triggers are used (Section 4.1), all generic refusal-initiating sentences (e.g., "Wait, maybe I have to refuse because…", "Hmm, that sounds really wrong…"). While downstream results are strong, the paper does not investigate whether prompt-specific triggers would yield more robust or deeper safety alignment. The genericity raises a question about whether the model learns genuine safety deliberation or a surface-level pivot pattern.

### Trivial
None

## Nice-to-Haves
- **Human evaluation of reasoning safety** on a small sample (e.g., 50 examples) to calibrate GPT-4o's judgments and assess whether IPO produces genuine safety reasoning vs. cosmetic refusal phrases.
- **Statistical variance** reporting across multiple seeds, especially for JailbreakBench (100 prompts where a 5-point swing represents only 5 examples).
- **Integrating over-refusal mitigation** into the primary IPO training stage by including benign prompts in the preference dataset from the start, making the safety-utility tradeoff an explicit design parameter.
- **Ablation of generic vs. contextualized triggers** to assess whether prompt-specific safety reasoning outperforms the current generic trigger pool.
- **KL divergence analysis conditioned on harmful vs. benign prompts** (extending Figure 7) to diagnose the over-refusal mechanism.

## Removed Points
*These points are flagged to be removed; treat them with caution.*

- **Equation 4 appears non-standard (reviewer claim).** The reviewer noted that π_θ appears in both numerator and denominator of the first fraction in Eq. 4. This is almost certainly a PDF parsing artifact — the paper describes using DPO and the formulation is consistent with partial-trajectory DPO where subscripts may be garbled. Removed per formatting/parsing rules.
- **Missing robustness against adaptive attacks in main paper.** The paper explicitly references robustness tests in Appendix B.2 including "obfuscation, paraphrasing, and adaptive attack" (Section 4.3). Removed per appendix rule.
- **GRPO baseline may be under-tuned.** The paper states GRPO was "trained until reward convergence with at least twice the sampled trajectories of IPO" (Section 4.1), and GRPO achieves very competitive results on JailbreakBench (0.3% for DS-8B, 3.0% for DS-7B). The concern is speculative without specific evidence of unfair tuning.
- **Small dataset sizes may cause overfitting.** The datasets (1,438 / 1,346 / 520 pairs) are small, but this is also an efficiency advantage and the paper's cross-benchmark generalization suggests overfitting is not a dominant issue.
- **"Safe reasoning implies safe responses" treated as universal.** The reviewer noted model-dependent variation in Figure 3. The paper's finding is explicitly framed as empirical ("we notice that the responses following safe reasoning are highly likely to be safe"), and the claim holds across all three tested models.

## Novel Insights
The CSR framework provides a systematic, quantitative tool for understanding *where* in the reasoning chain safety is determined — moving from qualitative observation to an automatically identifiable structure. The key insight that safety "crystallizes" at discrete early turning points (with 0.85 Pearson correlation to compliance cues) offers both a diagnostic tool and a concrete intervention target. The reward shaping interpretation — connecting CSR to value functions and showing that the shaped reward concentrates at compliance cue / safety trigger transitions — is a clean theoretical framing that explains why step-level intervention is more sample-efficient than sparse outcome-level RL.

## Suggestions
- Extend CSR analysis to ≥100 prompts from multiple benchmarks (especially StrongReject and WildJailbreak) and at least two models to strengthen the empirical foundation of the core claims.
- Ablate generic vs. prompt-specific safety triggers — even a small comparison would address the concern about surface-level pattern learning.
- Integrate over-refusal mitigation into the primary training stage by including benign prompts in the preference dataset, making IPO a single-stage method.
- Report XsTest compliance alongside safety metrics in all comparisons to make safety-utility tradeoffs explicit.
- Add a small-scale human evaluation of reasoning safety to validate the GPT-4o judge.

## Score and Decision

### Calibration Anchors

| Paper | Path | Avg Score | Round | Comparison |
|---|---|---|---|---|
| NEMESIS: Jailbreaking LLMs with CoT | 5kMwiMnUip | 1.40 | R1 | Fundamentally weaker — no method, just attack demos |
| Systematic Review of LLMs | 8QTpYC4smR | 1.00 | R1 | Survey paper, no contribution; completely different tier |
| Cross-Lingual Humanoid Robots | gwZ90hFSL2 | 1.00 | R1 | Off-topic, no ML contribution |
| IC-Light | u1cQYxRI1H | 0.50 (sim artifact) | R1 | Different domain, not comparable |
| Code-of-Thought Prompting | lUyYX9VFgA | 3.00 | R1 | Safety evaluation-only with limited novelty; IPO is clearly stronger |
| Planning in Strawberry Fields | jOuHjFw71C | 3.00 | R1 | Evaluation-only paper on LRM planning; IPO has both analysis and method |
| Supervised Chain of Thought | pXIbcRPxWR | 2.50 | R1 | Incremental CoT training; IPO has deeper contribution |
| Safety Alignment Few Tokens Deep | 6Mxhg9PtDE | 9.50 | R1 | Comprehensive analysis + multiple mitigations; clearly stronger than IPO |
| MODPO | 2BfZMh9td4 | 4.25 | R1 | Multi-objective DPO, incremental; IPO has clearer novelty |
| General Preference Modeling | xS4XOS4NQ5 | 5.00 | R1 | Preference representation learning; different focus, comparable novelty but weaker evaluation |
| Generative Reward Models | MwU2SGLKpS | 4.50 | R1 | Iterative reward model training; incremental compared to IPO's analytical contribution |
| MOSLIM | w0MAu8vjwj | 4.00 | R1 | Multi-objective alignment; IPO has stronger novelty and evaluation |
| SafeDPO | MoJSnVZ59d | 6.40 | R1 | Safety DPO with one extra hyperparameter; criticized as incremental with missing efficiency analysis. IPO is more novel (CSR framework) and better evaluated |
| Step-Controlled DPO | ZRDa2IT1sQ | 6.00 | R1 | Step-level DPO for math; similar spirit but criticized as "minor contribution." IPO has deeper analysis and broader evaluation |
| 3D-Properties of DPO | 9Hxdixed7p | 6.25 | R1 | DPO analysis paper; IPO has stronger practical contribution |
| SuperCorrect | PyjZO7oSw2 | 6.50 | R1 | Teacher-student correction for reasoning; comparable novelty but different domain |
| Backtracking Improves Safety | Bo62NeU6VF | 8.00 | R1 | Very similar spirit (safety + generation intervention), simple and effective with no over-refusal. IPO has more analysis but more issues |
| Rethinking Reward Modeling | rfdblE10qm | 8.00 | R1 | Reward model theory + empirics; different focus, clearly polished |
| MAP: Multi-Value Alignment | NN6QHwgRrQ | 8.00 | R1 | Multi-value alignment; different problem, strong contribution |
| RM-Bench | QEHrmQPBdd | 8.00 | R1 | Reward model benchmarking; different focus |

**Round 1 bracket: 6.5 – 7.5**

The paper is clearly above the borderline reject papers (SafeDPO at 6.4 was Rejected, SCDPO at 6.0 was Rejected) — IPO has a more novel analytical framework (CSR), a more principled method, and broader evaluation. However, it falls somewhat below the Backtracking paper (8.0, Accept), which has a similarly simple and effective intervention mechanism but without the over-refusal issue or narrow analysis base. The CSR analytical contribution is genuine and differentiating, pushing it above the 6.0-6.5 reject-tier methods, but the over-refusal with ad-hoc fix and 30-prompt analysis base prevent it from reaching the polished quality of the 8.0-tier accepts.

**Final calibrated score: 6.5**

The paper makes a genuine contribution — the CSR analytical framework is novel, the method follows principally from the analysis, and results are strong across multiple models and benchmarks. The weaknesses (narrow analysis base, substantial over-refusal with ad-hoc mitigation, limited Qwen3-8B baselines) are real but bounded and addressable. It sits above the rejected SafeDPO (6.4) and SCDPO (6.0) due to stronger novelty and evaluation breadth, but below the accepted Backtracking (8.0) due to the over-refusal issue and analysis scope limitations. This is a solid borderline-accept paper with genuine contributions.

MY FINAL SCORE: <score>6.5</score>
MY FINAL DECISION: <decision>Accept</decision>