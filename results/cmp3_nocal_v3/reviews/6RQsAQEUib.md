## Summary

This paper proposes Guided Hybrid Policy Optimization (GHPO), a framework that augments on-policy RLVR (specifically GRPO) with adaptive prompting that incorporates ground-truth solution traces. GHPO detects when a query yields zero correct responses (all rewards zero) and, for such "difficult" queries, augments the prompt with partial solution traces as hints. The method is evaluated on six math reasoning benchmarks using Qwen2.5-7B and Qwen2.5-Math-7B, reporting consistent improvements over GRPO and curriculum-learning baselines.

## Strengths

1. **Well-motivated problem with concrete evidence.** The paper identifies capacity-difficulty mismatch as a bottleneck in RLVR and provides empirical grounding — e.g., Qwen2.5-7B-Instruct fails on 52% of NuminaMath-1.5 problems (line 78). This clearly illustrates the reward-sparsity issue the method targets.

2. **Intuitive core idea with practical appeal.** Using ground-truth solution traces as adaptive hints is natural, and the adaptive switching mechanism is a sensible way to avoid the pitfalls of static guidance (over-guiding on easy problems, missing hard ones). The cold-start strategy (N=20 steps of pure GRPO) is a practical addition.

3. **Consistent empirical gains across settings.** Tables 1–2 show GHPO outperforming GRPO and curriculum-learning baselines across most benchmarks and both base models. Notable improvements include GPQA-Diamond (30.8% → 39.4% on Math dataset) and AMC23 (47.5% → 57.5%). The trend holds for both the general-purpose Qwen2.5-Base-7B and the math-specialized Qwen2.5-Math-7B.

## Weaknesses

### Major

1. **Incomplete specification of the advantage computation (methodological gap).** This is the most significant issue. The paper states that "Unlike GRPO, these group rewards are not directly used for advantage estimation" (line 123), but Eq. (1) uses the variable Â_{i,t} **without ever defining it for GHPO**. The only definition of Â_{i,t} in the paper is the GRPO formula (Section 2.2), which the paper explicitly says does NOT apply. For the core scenario GHPO is designed to handle — queries where all G responses are wrong — a reader cannot determine from the main text what Â_{i,t} evaluates to or what produces a non-zero gradient. Furthermore, the responses are sampled from π_θ_old(·|q) but the probability ratio in Eq. (2) conditions on q* (which may be q + ω·h). No importance sampling correction for this distribution mismatch is discussed. This is not necessarily a fatal flaw — a reasonable alternative advantage computation may exist — but the main paper does not present it, leaving the mechanism incompletely specified.

2. **Absence of directly relevant baselines.** The paper discusses DAPO, Dr. GRPO, and LUFFY in Sections 1 and 5 as methods addressing related problems (reward sparsity, exploration-imitation balance), yet none appears in the experimental comparisons (Tables 1–2). The headline claim that GHPO "outperforms state-of-the-art RL methods" (line 45) cannot be properly assessed when the most directly comparable SOTA methods from the same zero-RL training family are discussed but not compared against. Including at least DAPO and Dr. GRPO would substantially strengthen the evaluation.

3. **Assumption 1 has a scope mismatch with the actual method.** Assumption 1 (lines 86–98) is framed around fine-tuning on a *single* problem q (with vs. without its trace) and testing OOD generalization. But GHPO operates on full-dataset training with adaptive hints per query. The connection between the assumption's per-problem framing and GHPO's actual multi-problem, adaptive training procedure is not established. Moreover, the assumption is stated about J_GRPO but GHPO uses a different objective.

### Minor

4. **No error bars or multiple-seed results.** All results in Tables 1–2 are point estimates from what appears to be a single training run per configuration. Given the well-known variance of on-policy RL for LLMs, the reported margins (e.g., 0.409 → 0.442 on the Mixed dataset for Qwen2.5-7B) may fall within run-to-run noise.

5. **Privileged information not fully disentangled.** GHPO conditions on ground-truth solution traces that standard RLVR methods do not use. The paper acknowledges this (line 84) and includes a GRPO-CL-H(0.5) baseline that also uses fixed 50% hints, which GHPO outperforms (0.422 vs. 0.442). This partially addresses the concern. However, an ablation where *all* queries receive a hint (ω=1, no difficulty detection) would cleanly isolate the contribution of the adaptive switching mechanism from the contribution of simply having access to extra supervision, and is not reported.

6. **Cold-start sensitivity unexplored.** The cold-start strategy uses N=20 steps as a fixed choice, but no analysis of sensitivity to this hyperparameter is provided.

### Trivial

7. **Abstract's "~5% average gain" is imprecise.** The actual gains are ~4.4% (Table 1), ~3.3% (Table 2, Qwen2.5-7B), and ~3.5% (Table 2, Qwen2.5-Math-7B). The abstract and conclusion's "approximately 5%" slightly overshoots the reported numbers.

## Nice-to-Haves

- An ablation where difficulty detection is disabled (all queries always receive a fixed-level hint) to isolate the contribution of the adaptive switching mechanism.
- Reporting results from at least 3 random seeds with mean and std.
- A brief discussion in the main text of how the training hyperparameters (learning rate, group size G, batch size, KL penalty β, clipping ε) were chosen, even if full details remain in the appendix.
- Investigation of sensitivity to the cold-start step count N.

## Removed Points

- **"GHPO cannot produce non-zero gradients (fatal flaw)"** — This is downgraded from fatal to Major (see #1 above). The paper explicitly states that group rewards are "not directly used for advantage estimation" (line 123), indicating the authors intend a different computation. The weakness that remains is that this computation is never specified in the main text, not that it is known to be impossible. The "fatal" framing assumes the GRPO formula still applies when the paper says it does not. Also, the distribution-mismatch concern (responses from q, ratio from q*) is real but its severity depends on how advantages are actually computed — which brings it back to the main specification gap.

- **"Training dynamics (Figure 3) undercuts the narrative"** — Removed. The paper's narrative is that reward sparsity is persistent (~60% of problems remain "difficult" throughout training) and GHPO handles this by providing guidance. Figure 3 reinforces, not undercuts, this narrative. The method does not claim to eliminate the detection of difficult problems; it claims to provide learning signal for them.

- **"Missing hyperparameters / group size G in main text"** — Removed per rule about stripped appendix content.

- **Criticisms about missing proofs or details in the appendix** — Removed per rule; the parser strips these sections.

## Novel Insights

None beyond the paper's own contributions. The reviews surface two useful observations that are not in the paper: (1) the methodological gap created by using Â_{i,t} without redefining it for GHPO, and (2) the tension between Assumption 1's per-problem framing and GHPO's full-dataset training. Neither observation invalidates the core approach, but both point to specific places where the paper's argumentation is incomplete.

## Suggestions

1. **Clarify the advantage computation.** Define Â_{i,t} explicitly for GHPO in the main text. If advantages are computed differently for "easy" and "difficult" queries, specify both cases. If responses are re-sampled from q* after difficulty detection, state this and adjust the equations accordingly. Address the distribution mismatch between q and q*.

2. **Add the most directly relevant baselines** — DAPO and Dr. GRPO are discussed in the paper and operate in the same zero-RL setting. Including them would substantially strengthen the evaluation.

3. **Add an ablation that always provides hints** (no difficulty detection, all queries get some fixed ω) to isolate the contribution of the adaptive switching mechanism.

## Score and Decision

The paper identifies a real problem and shows consistent empirical gains. However, the main paper leaves a core component of its method — the advantage computation for the "difficult" query case — incompletely specified. Combined with missing SOTA baselines and the absence of statistical uncertainty estimates, the paper cannot be accepted in its current form. The underlying idea is promising and the empirical results are consistent, so a substantially revised version addressing these issues could be reconsidered.

MY FINAL SCORE: <score>4.0</score>
MY FINAL DECISION: <decision>Reject</decision>