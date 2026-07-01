## Summary

This paper proposes SPOT, a method for offline preference-based RL that: (1) extracts "subgoals" from high-attention, above-average-reward states in preferred trajectories using a Preference Transformer, (2) trains a CVAE to generate these subgoals conditioned on state-action pairs, and (3) uses cosine-similarity-based reward shaping (r_final = r_model + λ·r_shape) to guide policy optimization. The core idea — using attention-derived subgoals from preference data as structured intermediate targets — is genuinely novel and addresses a real problem (reward model extrapolation in offline PbRL).

## Strengths

1. **Novel and well-motivated conceptual combination.** The idea of leveraging the Preference Transformer's attention weights to identify critical states, then using a CVAE to generate subgoals for reward shaping, is genuinely creative and not, to my knowledge, present in prior work. The pipeline (Figure 1) is clear and the motivation — that subgoals anchored in preferred trajectories constrain the policy toward in-distribution states — is coherent.

2. **Broad evaluation coverage.** The paper evaluates across three benchmark families (D4RL locomotion, Robosuite manipulation, Meta-World) with seven baselines including Oracle, MR, PT, IPL, HPL, CPL, and DTR. This exceeds the coverage of most offline PbRL papers.

3. **Transparent reporting.** The paper reports full result tables with standard deviations across 5 seeds (Table 1) and notes that the Oracle average is computed over 8 tasks excluding Meta-World. The limitations section acknowledges scope constraints (offline setting only, clean preferences assumed).

## Weaknesses

### Fatal
None.

### Major

1. **Two of the most relevant baselines (DTR, CPL) perform at near-random levels, undermining the comparison.** DTR (Tu et al., 2025) — the most closely related work, also targeting extrapolation error in offline PbRL — averages 54.08 across tasks, compared to the simple MR baseline at 73.61. On plate-slide, DTR scores 5.24 ± 5.07 while MR scores 51.5 ± 11.9 — a 10× gap. On lift-mh, DTR scores 22.30 ± 21.96. Similarly, CPL averages 44.98 with scores of 18.79 on lift-mh and 9.15 on can-ph. The paper does not acknowledge or explain these discrepancies. If these implementations are not performing at their published levels, SPOT's "state-of-the-art" claim in Table 1 rests on a comparison against degraded baselines. The authors should either provide evidence that DTR and CPL were tuned to their reported performance or discuss why they underperform in this setting.

2. **The extrapolation error measurement in Figure 2 is ambiguous, making the central quantitative claim unverifiable.** Section 5.3 defines extrapolation error as "the absolute difference between predicted reward and ground truth reward" (line 249) and compares PT vs. SPOT in OOD settings (Figure 2b). However, the paper never specifies whether SPOT's "predicted reward" is the raw model output r_model (Eq. 4) or the final shaped reward r_final = r_model + λ·r_shape (Eq. 13). If it is r_final, comparing against PT's r_model is comparing apples to oranges — the shaping term is designed to compensate, so a lower error is a near-tautology. If it is r_model, the comparison would be legitimate (showing that SPOT's policy visits states where the reward model makes smaller errors), but this must be explicitly stated. Without this clarification, the headline claim of "mitigating extrapolation errors" cannot be properly evaluated.

### Minor

3. **Extreme variance in ablation experiments (Tables 2 and 3) makes the reported rankings unreliable.** In Table 3, numerous entries have standard deviations that exceed 50% of the mean — e.g., cosine similarity on hopper-m at λ=0.5: 63.89 ± 51.95; negative distance at λ=-1.0: 43.09 ± 40.01; potential-based at λ=-0.5: 62.54 ± 41.23. These are computed over only 3 seeds. The paper asserts that "cosine similarity achieves superior performance" (Section 5.2.2), but with overlapping confidence intervals of this magnitude, the comparative ranking of shaping methods is not statistically meaningful. The same issue appears in Table 2 (Bottom 10–20% on hopper-m-e: 69.90 ± 39.12).

4. **The "forward-looking subgoal" claim (Section 5.4) lacks quantitative support.** The paper states that generated subgoals "lead actual execution by approximately one timestep forward" (line 281) and presents this as evidence of predictive quality. The only support is a qualitative visual inspection of four panels in Figure 3. No quantitative metric (temporal offset measurement, error bars, evaluation across multiple trajectories or environments) is provided. This specific claim should either be backed by numbers or softened.

5. **Oracle baseline shows signs of poor tuning on some tasks.** On hop-m-e, the Oracle (ground-truth reward + IQL) scores 62.10 ± 30.42 while SPOT scores 98.73 ± 7.50. The enormous Oracle variance (std 30.42) suggests IQL may be poorly configured for this task with ground-truth rewards, not that SPOT has discovered a generally superior learning paradigm. The paper presents this comparison without commentary, which risks misleading readers about the relative strengths of the methods.

### Trivial

None.

## Nice-to-Haves

- **Clarify the extrapolation error measurement** (this is a core weakness above, listed here as actionable guidance): explicitly state whether SPOT's "predicted reward" in Figure 2 is r_model or r_final.
- **Quantitatively evaluate the forward-looking subgoal claim** by measuring temporal offset between current states and predicted subgoals across trajectories, with distributional statistics.
- **Add a CVAE ablation** that compares CVAE-generated subgoals against directly using ground-truth subgoals from the dataset, to isolate the CVAE's contribution from the subgoal concept itself.
- **Add statistical significance tests or at minimum note overlapping confidence intervals** where the paper makes comparative claims from high-variance data.

## Removed Points

These points were flagged by the harsh reviewer but are removed (with justification) and should be treated with caution:

- **"SPOT's average is inflated by two tasks the Oracle does not compete on"** — **REMOVED (factually wrong).** Computing SPOT's average over only the 8 tasks Oracle competes on gives ~82.18, which is *higher* than its 10-task average of 78.82. The Meta-World tasks pull SPOT's average down, not up.
- **"Central claim does not match the method's mechanism"** — **REMOVED (overstated).** The paper claims SPOT "mitigates extrapolation errors" by constraining the policy to in-distribution states via subgoal guidance. This is a system-level claim about where the learned reward model is queried, not a claim about modifying the reward model's parameters. The mechanism is coherent; the issue is limited to the ambiguous measurement in Section 5.3 (retained as Weakness #2).
- **"Bold formatting hides rankings"** — **REMOVED (presentation nitpick).**
- **"No statistical significance tests"** — **DOWNGRADED to Nice-to-Have.** Single-run evaluation and no significance testing is standard for this benchmark genre.
- **"Missing related work" / imprecise characterization of prior work** — **REMOVED per policy** (do not mention missing related works; the characterization of DTR is reasonable).

## Novel Insights

The most interesting observation from the reviews that goes beyond the paper's own claims is the structural tension revealed between the two ways SPOT could reduce extrapolation error. The paper's mechanism is additive reward shaping (r_final = r_model + λ·r_shape), yet the extrapolation analysis (Figure 2) is framed as though SPOT reduces the reward model's *inherent* prediction error. The ambiguity around whether SPOT's measured "predicted reward" is r_model or r_final exposes a gap between the paper's causal story (subgoals keep the policy in-distribution → reward model makes smaller errors) and the actual experimental protocol (which might simply be comparing r_final against r_model). Resolving this would sharpen the contribution substantially.

## Suggestions

1. **Clarify the extrapolation error measurement.** State explicitly: is the "predicted reward" in Figure 2 r_model (same as PT uses) or r_final (including the shaping term)? If r_model, the claim stands and is interesting — show that SPOT's policy visits states where the *same* reward model makes smaller errors. If r_final, reframe the conclusion as "reward shaping compensates for extrapolation error."

2. **Re-examine DTR and CPL implementations.** Report whether the observed scores match published results for these methods and discuss any differences in experimental setup. If tuning was limited, disclose the search protocol. If the methods genuinely underperform in this setting, explain why.

3. **Add confidence intervals or seed-level scatter plots** for the ablation experiments in Tables 2 and 3, where standard deviations exceed 50% of the mean. Do not make comparative claims about shaping methods whose performance distributions overlap substantially.

4. **Either quantify the forward-looking claim** (measure temporal offset between current state and predicted subgoal across trajectories) or remove the quantitative phrasing ("approximately one timestep forward").

5. **Reconsider the "top 95% performance" bolding convention** — on walk-m-e nearly all methods are bold, making the formatting uninformative. Consider using bold only for the best result(s) within statistical significance.

## Score and Decision

MY FINAL SCORE: <score>5.0</score>
MY FINAL DECISION: <decision>Reject</decision>