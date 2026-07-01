## Summary

This paper proposes DTERM (Dynamic Task-Embedded Reward Machine), a hypernetwork-driven framework that dynamically generates weights for multiple reward components (syntactic correctness, functional correctness, code style, computational efficiency) based on task embeddings extracted from task descriptions. The goal is to avoid manual reward engineering in RL-for-code-generation by letting the learned weighting scheme adapt per task, including zero-shot transfer to unseen coding tasks. Experiments compare against Uniform, Expert-Tuned, and GradNorm baselines across several code benchmarks, and an ablation study isolates the contribution of each architectural component.

## Strengths

1. **The core idea is well-motivated.** The paper identifies a genuine limitation of current practice: fixed reward weights for diverse coding tasks (translation, repair, completion, competitive programming) cannot capture their differing emphasis on compilation correctness vs. test-passing rate vs. efficiency. Dynamic weighting conditioned on a task embedding is a sensible and clearly stated direction (Section 1, lines 13–22).

2. **The architectural pipeline is modular and coherent.** The design (task embedding → hypernetwork → weighted sub-rewards) is clearly described in Sections 4.1–4.3. The use of FiLM layers for reward-component specialization (Section 4.2) and cross-task prototypes with attention (Section 4.3) are specific, motivated additions that connect to the zero-shot adaptation goal.

3. **The ablation study provides internal validation.** Table 2 isolates each component on HumanEval: removing the hypernetwork (18.1 vs. 22.7), task embeddings (19.3), FiLM modulation (20.8), compiler feedback (21.1), and static prototypes (17.6) all produce the expected degradation, lending some credence to the architectural choices.

## Weaknesses

### Fatal

None.

### Major

1. **Conclusion section is about a completely different paper.** Section 6 (lines 299–303) reads: *"The Dual Selfular-Acting Machine (DSAM.Mouth Rachel) A new method for analyzing the dual selfular acting machine (DSAM), a generative text model architecture akin to one employed by ChatGPT."* This text does not summarize DTERM or its findings; it appears to be unrelated content accidentally included. While this does not invalidate the technical claims, it is a severe quality-control failure. A venue-ready paper must summarize its own results.

2. **No variance or statistical significance reported anywhere.** The paper states "Each experiment runs on 4 NVIDIA V100 GPUs with 3 random seeds" (line 201), yet Table 1, Table 2, Figure 2, and all other results report only point estimates — no standard deviations, confidence intervals, or ranges. Without variance, the reader cannot assess whether the reported improvements (e.g., +12.7% BLEU for translation, +18.4% fix rate for repair) are robust or within noise. Many gains over GradNorm are ~4–5 percentage points; without error bars these could easily be within one standard deviation. This is a basic reporting standard that every experimental paper should meet.

3. **Cross-task generalization experiment (Figure 2) is uninterpretable as reported.** Several problems: (a) The 10 "unseen tasks" are never named, described, or characterized — the reader cannot assess the domain gap. (b) "Normalized reward" is undefined — it could be relative to a per-task maximum, Z-scored, or computed in a way that inflates DTERM's apparent advantage. (c) DTERM starts at 0.70 while Uniform starts at 0.28 on Task 1 — if these are truly unseen, this 2.5× gap suggests task leakage between training and evaluation, a per-method normalization artifact, or a systematic advantage of DTERM unrelated to dynamic weighting. (d) All methods improve over the 10-task sequence (DTERM 0.70→0.93, Uniform 0.28→0.51). This pattern is more consistent with a learning curve on seen tasks or ordering by increasing similarity to training data than with zero-shot evaluation. The experiment as reported does not support the "zero-shot adaptation" claim.

4. **Missing critical baselines.** The paper compares against Uniform, Expert-Tuned, and GradNorm. It does not compare against CodeRL (Le et al., 2022), which is *cited* in the paper and is the most directly relevant RL-for-code-generation baseline. It also does not compare against a simpler learned-weight alternative (e.g., a per-task learned scalar weight per component without a hypernetwork), which would isolate whether the hypernetwork's expressive capacity provides benefit beyond a simpler parameterization. Without these, the paper cannot substantiate that its specific approach is better than available alternatives.

5. **Method describes capabilities that are never evaluated.** Sections 4.4 (Multi-Modal Task Embedding Fusion, with CLIP-based visual input) and 4.6 (Integration with CodeLLMs via RLHF, with a human preference reward component) present extensions that are not tested in any experiment. Section 5 describes experiments only on text-only code benchmarks (CodeXGLUE, APPS, DeepFix, HumanEval). No multi-modal or RLHF experiments appear. Presenting untested capabilities as part of the method inflates the paper's scope and makes it harder to assess what was actually implemented.

### Minor

1. **"visualization" task appears in Figure 3 but is not described in the experimental setup.** Section 5.1 lists only CodeXGLUE, APPS, DeepFix, and HumanEval as datasets. The reward proportion analysis (Figure 3) includes a "visualization" task type with no provenance — where does this data come from? This suggests either an undocumented dataset or a mismatch between the evaluation description and the analysis.

2. **Table 1 row-to-dataset mapping is ambiguous.** The table lists Summarization, Translation, Completion, Repair, and Problems. Section 5.1 names CodeXGLUE, APPS, DeepFix, and HumanEval. The reader cannot reconstruct which metric comes from which dataset. "Problems" with Pass@1 metric could be APPS or HumanEval; the ablation study uses HumanEval, but Table 1's "Problems" is never explicitly linked to a dataset.

3. **"Reward Machines" framing overclaims the connection.** The title and acronym invoke Reward Machines (Icarte et al., 2022), which formalize reward functions as finite state machines with conditional transitions. The paper acknowledges the difference in Section 3.5 ("While our approach differs in implementation"), but the framing still suggests a connection to formal reward machine machinery that is not delivered. The method is better described as dynamic reward *composition* or *weighting*.

4. **Cross-task prototype meta-training protocol is underspecified.** Section 4.3 states prototypes are "learned during meta-training on many different types of tasks" (line 142) but gives no details: how many tasks, how they are sampled, how the prototype mechanism is optimized. This is a central component for the zero-shot claim.

5. **Expert-Tuned baseline cites an inappropriate reference.** The Expert-Tuned baseline cites Rame et al. (2023), which is about Rewarded Soups (interpolating fine-tuned weights), not about manually tuning reward weights. The description of this baseline is inadequate.

6. **Incomplete citations.** Three places use "(?)" as a placeholder citation (lines 39, 47, 197 — the latter for CodeXGLUE). These need to be filled in.

7. **Sub-reward component assignments per task not specified.** The paper states baselines use "identical sub-reward components as DTERM" (line 200) but never specifies what the five reward components are for each specific task (e.g., does "Computational Efficiency" apply to summarization?).

### Trivial

- Garbled phrases: "down-river tasks" (line 43), "Bat var" (line 162), "Word xog" (line 98).
- Reference entries with "Unable to determine the complete publication venue" (lines 313, 357).

## Nice-to-Haves

- Compare against CodeRL and a simpler per-task learned-weight baseline to isolate the hypernetwork's specific benefit.
- Report variance (mean ± std with 3 seeds) for all quantitative results.
- Define the cross-task evaluation protocol clearly: name the 10 tasks, define "normalized reward," and rule out training/evaluation task leakage.
- Remove or clearly mark Sections 4.4 and 4.6 as future work if not implemented.
- Add hyperparameter sensitivity analysis for the hypernetwork (hidden size, number of layers).
- Analyze the learned task embeddings (e.g., which dimensions correlate with weight changes across tasks).

## Removed Points

These points are flagged to be removed, treat them with caution:

- The critic's claim that "the conclusion being garbled makes the paper impossible to evaluate" — the paper's technical content (method, experiments, results) is still present and evaluable despite the garbled conclusion. This is a severe presentation flaw but does not make evaluation impossible.
- The critic's claim about PPOCoder/RLTF/RLEF as missing baselines — these methods are not mentioned in the paper and are not standard references in the way CodeRL is. Only the CodeRL omission is verifiably problematic.
- The critic's note about "no code release" — per instructions, this is a reproducibility nitpick that should be removed. The paper does not promise code release.
- The critic's strength about "the core idea is sensible" — this is generic but I kept it because the specific motivation (fixed weights cannot capture diverse coding-task requirements) is concrete and paper-grounded.

## Novel Insights

None beyond the paper's own contributions. The review process surfaces a consistent pattern: the paper has a reasonable core idea and internally consistent architecture, but its evaluation and presentation quality are substantially below the standard required at a top venue. The gap is not in the soundness of the approach but in the rigor of the evidence — uninterpretable generalization experiments, missing variance, absent baselines, untested method components, and a garbled conclusion.

## Suggestions

1. Replace the garbled conclusion (Section 6) with a proper summary of DTERM's findings. This is non-negotiable.
2. Report means and standard deviations for all experimental results (Tables 1, 2, Figure 2) computed over the 3 seeds already used.
3. Name and describe the 10 tasks in the cross-task generalization experiment, define the "normalized reward" metric, and clearly separate training tasks from held-out tasks.
4. Add CodeRL (Le et al., 2022) and a simple per-task learned-weight baseline to the comparisons.
5. Either remove or explicitly label Sections 4.4 and 4.6 as future/ongoing work, since they are not evaluated.
6. Clarify the dataset-to-task mapping in Table 1 and explain the provenance of the "visualization" task in Figure 3.
7. Fill in the "(?)" placeholder citations.

## Score and Decision

MY FINAL SCORE: <score>3.0</score>
MY FINAL DECISION: <decision>Reject</decision>