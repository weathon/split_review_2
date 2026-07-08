Now I have a comprehensive calibration picture. Let me compile the final review.

## Summary

The paper proposes SPOT, a framework for offline preference-based RL that uses attention weights from a Preference Transformer to identify "subgoals" (high-attention states in preferred trajectories), trains a CVAE to generate these subgoals conditioned on state-action pairs, and uses cosine similarity between predicted subgoals and next states as a shaping reward to mitigate reward model extrapolation errors.

## Strengths

- **Creative use of PT attention signals.** Leveraging preference transformer attention weights to identify states that drive human preferences (Section 4.1.1) is an intuitively appealing and resourceful use of existing architectural signals. The dual-criteria filtering (attention + reward, Section 4.1.2) adds a reasonable safeguard against low-quality subgoals.

- **Broad evaluation with multiple benchmarks and baselines.** The paper evaluates across D4RL locomotion, Robosuite, and Meta-World (10 tasks total) with seven baselines including MR, PT, IPL, HPL, CPL, DTR, and an Oracle (Table 1). This breadth of comparison is a genuine effort.

- **Useful ablations.** The Top-K percentile analysis (Table 2), reward shaping method comparison (Table 3), and query efficiency experiments (Table 4) provide meaningful insight into design choices and help isolate what contributes to performance.

## Weaknesses

### Major

**1. The paper's own evidence shows the "subgoal" is actually a one-step next-state prediction, undermining the entire conceptual framing.**

Section 5.4 (line 281) reports that predicted subgoals "consistently lead actual execution by **approximately one timestep forward**." This is not a validation of the method — it is direct evidence that the CVAE learns a one-step forward dynamics model, not temporally distant milestones or "critical decision points." The shaping reward (Equations 11–13) then measures cosine similarity between the actual next state and the predicted next state. This is a dynamics prediction bonus, not a subgoal-achievement signal. The paper's central narrative — "critical decision points," "milestones," "waypoints" — is inconsistent with what the method actually computes. The paper itself frames this one-timestep offset as positive ("empirically validates the quality and effectiveness of our subgoal generation mechanism") without recognizing that it contradicts the claimed role of subgoals.

**2. The empirical results do not support the claimed "consistent superiority."**

The paper claims "consistent superiority" (Section 5.1, line 216), but per-task results are mixed. SPOT underperforms simpler baselines on several tasks: on lift-mh SPOT scores 65.17 vs. MR's 95.62; on drawer-open SPOT scores 66.80 vs. MR's 86.6 and IPL's 87.64; on hop-m-r SPOT (85.08) trails DTR (94.18); on can-ph SPOT (63.82) trails IPL (67.98). The headline average (78.82) mixes D4RL normalized scores with success rates, and the Oracle baseline excludes Meta-World tasks (where SPOT benefits from strong plate-slide results) while SPOT's average includes them (noted transparently in the caption but the comparison is still affected). No statistical significance tests are reported despite high per-task variance (many standard deviations of 10–40 points).

**3. The CVAE generalization argument is unexamined.**

Section 4.1.3 (line 156) claims "the CVAE framework ensures that generated subgoals remain within the training distribution" via the KL divergence term. However, the KL term regularizes the latent space *z*, not the conditioning input *(s_t, a_t)*. The CVAE is conditioned on state-action pairs from the batch dataset that may be OOD relative to its training distribution (which consisted of pairs from preferred trajectories only). The paper provides no theoretical argument or empirical evidence that the CVAE should generalize to OOD conditioning inputs better than the reward model does — yet this generalization is precisely the mechanism by which SPOT is supposed to mitigate extrapolation errors. Without a demonstration that the CVAE produces reliable subgoals on the same OOD inputs that cause the reward model to fail, the core claim is unsupported.

### Minor

**4. Ambiguity in the extrapolation error analysis (Figure 2).** The paper defines extrapolation error as "absolute difference between predicted reward and ground truth reward" but does not specify whether "predicted reward" for SPOT includes the shaping term or only the PT reward model output. If it includes the shaping term, SPOT and PT are evaluated against different reward functions, invalidating the comparison. If it uses only the PT output, the comparison is valid but trivial (showing SPOT's policy stays closer to the training distribution). The paper must clarify this.

**5. Missing ablations.** The paper lacks an ablation comparing dual-criteria filtering vs. attention-only filtering (Section 4.1.2), making the claimed benefit of the reward criterion speculative. The Top-K ablation (Table 2) suggests that simple selection of high-attention states correlates strongly with performance, yet no baseline using nearest-neighbor retrieval from attention-highlighted states (instead of CVAE generation) is included to isolate the source of gains.

**6. Query efficiency claims are insufficiently supported.** The query efficiency experiments (Section 5.5, Table 4) compare SPOT only against PT, not against reward-model-free methods like IPL or CPL that are specifically designed for query efficiency.

## Nice-to-Haves

- Report the average temporal gap between conditioning state-action pairs and subgoals in the training data, to resolve whether subgoals are truly temporally distant milestones or one-step predictions.
- Add statistical significance tests (e.g., paired bootstrap across seeds) for Table 1 comparisons where standard deviations overlap substantially.
- Include an ablation of the dual-criteria filtering mechanism to validate its benefit over attention-only selection.
- Include a nearest-neighbor retrieval baseline to disentangle whether gains come from the CVAE's generalization or simply from proximity to any preferred-trajectory state.

## Removed Points

- Strength about "the problem being well-chosen" — generic, about problem importance rather than paper-specific contribution.
- Criticism about notation in Equation 3 being confusing — not a substantive weakness.
- Criticism about cosine similarity framing being "overwrought" — stylistic nitpick.
- Claim about "PT's high variance coming from can-mh (14.48) and plate-slide (2.8)" — plate-slide's std is 2.8, which is low; this part of the argument is factually incorrect.
- References to missing appendix content or missing references — parser artifacts.

## Novel Insights

The key insight from this review is that the paper's own evidence (one-timestep offset, Section 5.4) directly contradicts its central conceptual framing. The method appears to implement a dynamics prediction bonus in disguise rather than a subgoal-discovery mechanism. This framing mismatch is not a minor presentation issue — it obscures what the method actually does and why it might work, making it difficult to assess the paper's true contribution.

## Suggestions

1. Reframe the method honestly: characterize the CVAE as learning a one-step forward dynamics model and the shaping reward as a dynamics-consistency bonus, not a "subgoal" signal.
2. Clarify the extrapolation error analysis: specify whether "predicted reward" for SPOT includes or excludes the shaping term.
3. Add the missing ablations (dual-criteria vs. attention-only; nearest-neighbor retrieval vs. CVAE) to isolate what drives performance.
4. Temper claims of "consistent superiority" — acknowledge tasks where SPOT underperforms baselines.
5. Validate the CVAE's OOD generalization directly by measuring reconstruction quality on state-action pairs known to cause high reward model error.

## Score and Decision

**Bracket reasoning (Round 1):** The paper sits below well-received PbRL papers like Hindsight PRIORs (6.33) and below borderline-accept papers like OPRIDE (5.00) and HPL (5.20), which have clearer contributions and fewer structural issues. It sits above papers with clearly insufficient evidence like ADLoss (3.75) and HERON (4.00), which had narrower evaluations and weaker results.

**Narrowing (Round 2):** Compared to the most closely related anchors — OPRIDE (5.00, weighted items: novelty ~9.59, evaluation ~10.91, but weaknesses at -3.37 and -4.50) — our paper has less negative weight on its weaknesses (CVAE shift: -0.76, subgoal framing: -1.15, overclaimed results: -1.46) but the *nature* of these weaknesses is more structural. The subgoal-framing mismatch undermines the paper's core claim in a way that OPRIDE's novelty concerns do not. Compared to HPL (5.20), which shared a VAE-based approach but had a clearer motivation and stronger per-task results, our paper's mixed per-task performance and framing issues push it lower. Compared to ADLoss (3.75), our paper has broader evaluation and more ablations, placing it clearly above. The final score of 4.0 reflects a paper with a creative idea and broad evaluation but undermined by a framing mismatch between what it claims and what it actually does, overclaimed results, and an unexamined assumption at the core of its mechanism.

**MY FINAL SCORE:** <score>4.0</score>
**MY FINAL DECISION:** <decision>Reject</decision>