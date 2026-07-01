Now I'll produce the final consolidated review.

## Summary

This paper proposes ASPEC, a framework that manages a full lifecycle of stateful specialist agents through two phases: evolutionary **discovery** of specialist archetypes and experiential **cultivation** of their persistent memory. A lightweight "retain-then-escalate" meta-controller learns when to reuse the current agent team versus when to invoke the Architect to redesign it. The core design point — persistent specialists with a learned gating policy that avoids per-query regeneration — is genuinely novel and well-motivated. On GPQA, ASPEC achieves 62.8% at $0.88 inference cost, substantially cheaper than comparable methods (AFlow: $1.58, MaAS: $2.07) while matching or exceeding their accuracy.

## Strengths

1. **Compelling efficiency story.** Table 2 is the strongest result in the paper. ASPEC achieves 62.8% on GPQA with $0.88 inference cost — cheaper than CoT-SC ($0.85 at 57.1%), cheaper than AFlow ($1.58 at 61.3%), and dramatically cheaper than LLM-as-gate ($3.74 at 62.5%). The $1.38 total *offline training* cost is orders of magnitude below AFlow ($20.14) and MaAS ($3.43). These numbers represent a practical contribution if they hold.

2. **Clean, coherent system architecture.** The three-component decomposition — specialist operators (identity + memory), Architect (evolutionary search + redesign), Meta-Controller (lightweight retain/resample policy) — is well-designed and each component has a clearly defined role. The "retain-then-escalate" control policy is a simple but elegant conceptual contribution that cleanly separates *what* to build from *when* to rebuild it.

3. **Well-designed ablation study.** The ablation (Figure 6 / Table 6) is informative and goes beyond box-checking. The finding that removing specialists drops accuracy by 5.4% *and triples cost* cleanly demonstrates that specialists are not just a performance booster but also a cost-saving mechanism. The sensitivity analysis on k and m (Figure 6, right) provides useful calibration insight.

4. **Cross-model transfer results are strong.** The left table in Figure 5 shows ASPEC improves performance across three different model families (Gemini 2.0 Flash, GPT-4o-mini, Llama 3.3 70B Instruct), demonstrating that the benefit is not specific to one model.

## Weaknesses

### Fatal
None.

### Major

1. **Train/test separation for the cultivation corpus is not explicitly stated.** The paper says specialists are cultivated on a "training corpus" (Section 3.2) and deployed to "handle unseen queries" (Section 3), but never explicitly states whether this training corpus is a held-out subset of each benchmark or an entirely separate dataset. GPQA has only ~448 questions total; if even a fraction were used for cultivation (where specialists see questions, attempt answers, receive feedback, and store memory entries as in Figure 4), test results could reflect answer familiarity rather than genuine expertise. The cross-benchmark experiment (Figure 5) implies a clean separation for that analysis, but the main-table results (Table 1) are not accompanied by a comparable statement. This is a first-order experimental design detail that must be clarified before the accuracy numbers can be properly interpreted.

2. **The meta-controller's training protocol is underspecified.** Equation 4 gives a generic discounted-reward RL objective, but the paper never defines the reward function \(R_t(s_t, a_t)\), never states the RL algorithm used, never describes how training data is collected, and never reports training hyperparameters. Without these details, the meta-controller — a core component of the system — cannot be reproduced or meaningfully evaluated. The confusion matrix analysis (Figure 8) further underscores this problem: the meta-controller disagrees with the LLM-as-gate oracle on 45.9% of GPQA queries, and without knowing the reward function, the claim that this reflects "pragmatic economic policy" versus simply an undertrained policy cannot be assessed.

### Minor

3. **No statistical uncertainty reported for main results.** Table 1 reports single numbers without confidence intervals, standard deviations, or significance tests. The margins are small: ASPEC leads on GPQA with 62.8% vs. EvoAgent at 61.5% (1.3% gap) and AFlow at 61.3% (1.5% gap). On HumanEval, ASPEC is second at 91.4%, 0.2% behind MaAS at 91.6%. Given temperature T=0.3 is used, sampling variance alone could shift these numbers. The sensitivity analysis reports "mean over 4 runs" (Figure 6), so the authors have this infrastructure; applying it to the main table would substantially increase confidence in the results.

4. **The central narrative (stateful expertise accumulation) is not well-supported by the paper's own evidence.** Two findings create tension with the framing that specialists accumulate deep domain-specific expertise through memory:
   - **Memory contributes only 1.4%**: "ASPEC w/o specialist memory" achieves 61.4% vs. the full system's 62.8% (Table 6). The *memory* component — the mechanism by which specialists are supposed to accumulate growing competence — accounts for very little of the gain.
   - **Cross-domain transfer works without domain matching**: Figure 5 shows that when specialists trained on a *different* benchmark are used exclusively (ONLYSPEC), they "match or even slightly exceed the performance of the full system." If domain-specific expertise were critical, removing domain-matched generalist operators and forcing cross-domain specialists should hurt performance.
   
   The paper's explanation — that restricting the pool prevents the Architect from defaulting to "safe" generalist operators — is an efficiency/routing argument, not an expertise argument. These results together suggest the primary benefit comes from the specialist *prompt structure* (identities + directives) rather than from accumulated memory. The paper would be stronger if it recalibrated its claims to match this evidence: automated discovery of specialist prompts with efficient routing is still a novel and useful contribution.

5. **Equation 2 introduces a value function \(V_{\pi_\theta}(s_{t+1})\) that is claimed to be "formally defined in Equation 3," but Equation 3 defines only the state \(s_t = (e_q(q_t), e_g(\mathcal{G}_{t-1}))\), not the value function.** The value function is never defined or operationalized anywhere in the paper. Since the Architect is implemented as an in-context learning LLM — not a value-maximizing optimizer — this equation appears decorative rather than functional.

### Trivial
None.

## Nice-to-Haves

- Explicitly define the meta-controller's reward function and specify the RL algorithm, number of episodes, and training procedure. A clear reference to where this lives (even if in the appendix) would suffice.
- Report main results (Table 1) over 3–5 random seeds with standard deviations or confidence intervals.
- Clarify what query subset the confusion matrices (Figure 8) cover and resolve the apparent discrepancy between the stated percentages and raw counts.
- Add a straightforward comparison: same specialist prompt *with* versus *without* its accumulated memory entries to directly isolate what memory contributes beyond the prompt itself.

## Removed Points

These points from the input review are not included in the main evaluation, for the reasons indicated:

- **Confusion matrix percentages appear internally inconsistent (17.8%+45.9%+5.6%+41.9%=111.2%)**: May be a parser-induced formatting artifact. The Hard Rules for this review require removing such artifact-based criticisms. The authors should verify the numbers resolve correctly in the original PDF.
- **Missing comparison to AgentSquare**: The paper already includes 13 baselines covering the relevant categories. Not including every method cited in related work is standard practice.
- **Section-by-section commentary on framing, preliminaries, and discovery details**: These are presentation suggestions and scope observations that do not constitute evidence-grounded weaknesses.
- **Equation 2 "includes a value term that is never used again"** has been kept as Weakness #5 but aligned to the specific, verifiable claim (the value function is claimed to be "formally defined" but isn't).

## Novel Insights

The input review surfaces a genuine tension that goes beyond standard criticism. The paper's framing centers on *stateful expertise accumulation* through memory, but two pieces of evidence — the memory ablation losing only 1.4%, and cross-domain specialists working as well as in-domain ones — converge on a different interpretation: the real value comes from the automated *discovery of effective specialist prompts* (identities + directives) combined with a learned routing policy. The paper's attempted explanation for the ONLYSPEC result (restricting the pool prevents the Architect from defaulting to safe generalists) reads as an *efficiency* argument rather than an *expertise* argument. This suggests the paper's contribution could be reframed productively as "automated prompt specialization with cost-aware gating" without losing novelty or impact. The efficiency numbers (Table 2) are where the paper's strongest evidence lies, and they should be foregrounded more prominently.

## Suggestions

1. **Add a single sentence** to the experimental setup stating whether the cultivation corpus for each benchmark is a held-out subset of that benchmark, and if so, what the split size is. This is the most impactful fix the paper could make.
2. **Reframe the contribution** to align with the evidence: position the memory/cultivation component as a modest additive benefit and the specialist prompt discovery + learned gating as the primary mechanism. Alternatively, add an experiment that isolates what memory contributes beyond the prompt (e.g., same specialist with vs. without its memory entries, or tracking memory quality over cultivation steps).
3. **Specify the meta-controller's reward function** and training protocol, even if briefly. A single paragraph in the main text or a clear appendix reference would resolve this.

## Score and Decision

The paper proposes a genuinely interesting design point and the efficiency results are compelling. However, the evaluation protocol for the cultivation phase needs clarification before the accuracy numbers can be properly interpreted, and the meta-controller's training is underspecified. These are addressable issues that do not undermine the core contribution.

**Score**: 7

**Decision**: Accept

<score>7</score>
<decision>Accept</decision>