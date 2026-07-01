## Summary

This paper proposes GHPO (Guided Hybrid Policy Optimization), a difficulty-aware reinforcement learning framework that detects when a model struggles with a problem (all G responses yield zero reward) and adaptively provides partial ground-truth solution traces as hints in the prompt. This switches between on-policy RL for manageable problems and guided imitation learning for challenging ones. Experiments on six math benchmarks using Qwen2.5-7B variants show ~5% average improvement over GRPO.

---

## Strengths

1. **A well-motivated problem with quantified severity.** The paper identifies a genuine practical bottleneck in RLVR—reward sparsity from capacity-difficulty mismatch—and quantifies it concretely: even Qwen2.5-7B-Instruct fails on 52% of NuminaMath-1.5 problems (§2.3, line 78). This motivates the need for adaptive guidance.

2. **Informative training-dynamics analysis.** Figures 3 and 4 provide non-obvious qualitative insights: GHPO maintains consistently smaller gradient norms than GRPO (suggesting more stable optimization), higher accuracy reward, and longer response lengths throughout training. The persistent ~60% difficult-problem proportion (Figure 3) underscores that reward sparsity is not an initial transient but a structural challenge throughout RL training.

3. **Consistent directional improvement across benchmarks.** GHPO outperforms GRPO on 11 out of 12 benchmark entries across two training datasets (Tables 1 and 2), and outperforms the trace-using baseline GRPO-CL-H(0.5) on 5 out of 6 benchmarks, suggesting the adaptive mechanism adds value beyond simply having access to ground-truth traces.

---

## Weaknesses

### Fatal
None.

### Major

1. **The importance-sampling ratio in Eq. (1)–(2) is formally inconsistent.** The expectation samples responses from $\pi_{\theta,\text{old}}(\cdot|q)$ (the *original* prompt), but the importance ratio $r_{i,t}(\theta) = \pi_\theta(o_{i,t}|q^*, o_{i,<t}) / \pi_{\theta,\text{old}}(o_{i,t}|q^*, o_{i,<t})$ conditions on $q^*$ (the *hinted* prompt) in both numerator and denominator. When $q^* \neq q$, the denominator evaluates the old policy's density under a different conditioning than the actual sampling distribution. The proposal distribution ($\pi_{\theta,\text{old}}(\cdot|q)$) and the distribution used in the ratio ($\pi_{\theta,\text{old}}(\cdot|q^*)$) differ, and the objective contains no correction for this mismatch. As written, this yields a biased gradient estimate. The paper does not state that responses are re-sampled under $q^*$ after prompt refinement. This issue needs to be resolved (either by correcting the ratio or by confirming re-sampling occurs in implementation).

2. **The mechanism by which hints produce a learning signal when all advantages are zero is unexplained.** When all G responses are incorrect (the case that triggers hinting), all rewards are zero, so for every trajectory $\hat{A}_{i,t} = 0$. The PPO clipped-surrogate term $\min(r\hat{A}, \text{clip}(r)\hat{A})$ is therefore zero regardless of the hint, contributing no gradient. The only remaining term is $-\beta D_{\text{KL}}(\pi_\theta\|\pi_{\text{ref}})$, which regularizes toward the reference policy and does not convey task-specific signal. The paper claims that guidance provides "valid learning signals" for difficult problems (line 84, line 99), but the formal objective does not show how this occurs within the same batch. The authors should clarify whether the learning signal operates across training iterations (hints improve future response quality *in subsequent batches*) rather than within the current batch, and adjust the framing accordingly.

3. **The foundational premise (Assumption 1) is claimed to be empirically validated but is not directly tested.** Assumption 1 (§3.1) posits that fine-tuning *with* ground-truth traces on a failing problem improves OOD generalization compared to fine-tuning *without* traces. The paper states "we demonstrate the effectiveness of this Assumption 1 through comprehensive experiment detailed in Section 4" (line 99). However, Section 4 tests the full GHPO system—which includes adaptive difficulty detection, multi-stage ω scheduling, cold-start, KL penalty, and clipping—not the clean comparison stated in the assumption (two models fine-tuned from the same initialization on the same hard problems, one with traces and one without). The isolated effect of trace usage is never measured, so the paper's core premise remains untested by its own evidence.

### Minor

4. **No variance or uncertainty reported for any result.** All metrics in Tables 1 and 2 are single point estimates with no standard deviations, confidence intervals, or mention of multiple seeds. Several improvements are small (Math-500: 0.774→0.776 in Table 2; OlympiadBench: 0.396→0.389 where GHPO is *worse*). Without variance estimates, it is impossible to determine whether differences in the 1–3% range are meaningful given typical RL training variability.

5. **No SFT-on-hard-problems ablation to isolate the RL component.** The paper presents GHPO as an RL method that "combines online RL and imitation learning" (line 39), including GRPO-CL-H(0.5) as a trace-using baseline. However, the simplest baseline that would test whether the RL objective contributes beyond the traces themselves—supervised fine-tuning (SFT) on the same hard problems (identified by the same difficulty detector), or mixing SFT with GRPO—is absent. This leaves open the question of whether the reported gains come from GHPO's adaptive RL mechanism or simply from training on ground-truth traces via any method.

6. **Multi-stage guidance, one of the two core modules, is deferred to the appendix.** The adaptive ω adjustment schedule is described as a core component (§3.2: "GHPO is comprised of two core modules") but only a one-sentence summary appears in the main text (line 143: "details provided in the Appendix B.3"). While the appendix exists in the full submission, the main paper should include at least a sketch of how ω is staged, so that the method description is self-contained.

### Trivial
None.

---

## Nice-to-Haves

- An SFT-on-hard-problems ablation (as noted above) would cleanly isolate whether the RL objective contributes beyond the guidance data itself.
- Reporting results with variance (≥3 seeds) for at least the main comparisons would greatly increase confidence.
- A direct experimental comparison with LUFFY (which also combines imitation and RL, §5) would strengthen positioning against the most closely related approach.
- Extending evaluation to non-mathematical reasoning tasks would broaden the evidence for general applicability, though the paper's scope (math) is acceptable.

---

## Removed Points

These points from the input review were removed with justification:

- **"GHPO underperforms Qwen2.5-Math-7B on AIME24 (0.133 vs. 0.193)"**: This compares GHPO trained from Qwen2.5-Base-7B against Qwen2.5-Math-7B, a model with specialized math pretraining. These are different base models, so the comparison is apples-to-oranges. The relevant comparison (GHPO vs. GRPO from the same Base-7B) shows near-identical AIME24 scores (0.131 vs. 0.133 in Table 1), not a deficit. **Removed** (factually misleading comparison).

- **"DAPO characterization is incomplete"**: The paper's goal is to introduce GHPO, not to provide a comprehensive survey of DAPO's clip-higher, token-level loss, etc. Criticizing incomplete treatment of a related method mentioned only for context is scope creep. **Removed** (scope creep).

- **"Cold-start N=20 is not justified"**: Hyperparameter choices like N=20 are routine in empirical papers. An exhaustive sensitivity analysis for every hyperparameter is not standard. **Removed** (nitpick).

- **"Figure 3's volatile difficulty proportion may indicate unreliable detection"**: The volatility could equally reflect genuine fluctuations in which problems are difficult as the policy evolves. The critic's interpretation is one of several plausible readings, not a verified flaw. **Removed** (speculative).

- **"LUFFY should be experimentally compared"**: Moved to Nice-to-Haves. The paper discusses LUFFY qualitatively; requesting a full experimental comparison is a reasonable suggestion but not a weakness of the current submission.

- **"Non-mathematical tasks not evaluated"**: The paper scopes to mathematics (§4.1: "efficacy is demonstrated here within this domain"), so this is scope-respecting. Moved to Nice-to-Haves.

---

## Novel Insights

None beyond the paper's own contributions. The reviewer's key observations—the importance-sampling mismatch in Eq. (1)–(2) and the lack of a direct test of Assumption 1—are standard technical scrutiny, not novel conceptual insights.

---

## Suggestions

1. **Fix the importance-sampling ratio.** Clarify whether responses are re-sampled under $q^*$ (in which case the expectation notation should condition on $q^*$) or provide a corrected importance weight that accounts for the distribution shift from $q$ to $q^*$.

2. **Clarify how hints produce a learning signal when advantages are zero.** If the signal operates across iterations rather than within a batch, state this explicitly and adjust claims about "providing valid learning signals" for current difficult problems.

3. **Test Assumption 1 directly.** Run the clean ablation: fine-tune two models from the same initialization on hard problems identified by the difficulty detector, one with ground-truth traces and one without, using identical optimization. Report OOD benchmark results.

4. **Add variance information.** Report mean ± std over at least 3 random seeds for the main comparisons in Tables 1 and 2.

5. **Include a brief summary of the multi-stage ω schedule in the main text** so that the method description is self-contained.

---

## Score and Decision

MY FINAL SCORE: <score>5.0</score>
MY FINAL DECISION: <decision>Reject</decision>