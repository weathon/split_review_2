Now I will produce the final consolidated review.

## Summary

This paper proposes a compositional meta-learning framework that casts task learning as inference in a learned probabilistic generative model. A gating RNN captures between-module transition statistics while module RNNs capture within-module dynamics; training maximizes marginal likelihood via particle filtering, and test-time inference finds module sequences without any parameter updates. The method is demonstrated on synthetic rule-learning (6D vector shifts) and motor-learning (2D trajectory generation) tasks, with ablations isolating the contribution of each architectural component.

## Strengths

1. **Clean and well-motivated formulation (Section 2.1, Equations 1–4).** Framing compositional meta-learning as an RNN-augmented HMM — where the transition matrix becomes a gating RNN that captures non-Markovian dependencies and the emission matrix becomes module RNNs — is conceptually elegant and provides a clear bridge between probabilistic models and learned neural components.

2. **Strong diagnostic verification of module/gating recovery (Figures 2b–c, 4b–c).** The paper goes beyond task-performance reporting by directly verifying that learned module RNNs implement the correct operations and the gating RNN reproduces the history-dependent transition structure. This is a genuinely rigorous test of whether the model has learned the intended decomposition.

3. **Compelling sparse-feedback results (Figures 2e, 3c–d, 4e).** The demonstration that the gating RNN constrains the hypothesis space during periods without feedback — with posterior collapsing for exactly the learned number of repetitions before going uniform — provides the clearest illustration of why the architecture matters. This is a specific, non-trivial behavioral signature of correct counting and sequencing.

4. **Well-designed ablation controls (Figures 3a–d).** The four-panel comparison (RNN without task ID → fails; RNN with task ID → can't zero-shot transfer; full model without gating network → fails on sparse feedback; full model → succeeds) cleanly isolates the contribution of each architectural choice.

5. **Generalization to longer test tasks (Figures 2f, 3f).** The model infers solutions for tasks 4× longer than any training task, without retraining, while gradient-based methods with frozen recurrent weights suffer. This advantage follows directly from the compositional inference mechanism.

## Weaknesses

### Fatal

None.

### Major

1. **Missing empirical comparison against the most closely related prior work.** The paper identifies Alet et al. (2019) as "most similar in spirit" (line 157) and claims to "greatly improve sample efficiency" by replacing simulated annealing with probabilistic inference (lines 158–160). Hummos et al. (2024) is described as "particularly closely related" (line 165). Yet neither method is included in any experiment. The comparisons that *are* provided (Figure 3e–f: MAML, MLDG, standard RNN retraining) establish differences from gradient-based meta-learning but do not distinguish the paper from the most relevant modular, inference-based alternatives. A claim of superiority over the closest prior work requires evidence.

2. **Evaluation scope is narrow relative to the paper's framing.** Both domains share the same underlying combinatorial grammar: select 3 of N operations/skills, each with fixed durations (3/4/5 steps), concatenated in sequence. The output modality differs (6D vector shifts vs. 2D trajectories) and the motor task requires some architectural adaptations, but the structural template is identical. The paper candidly describes its tasks as "proof-of-principle" (lines 180, 194), which is appropriate, but the gap between the claimed generality and the demonstrated scope is substantial. Tasks with genuinely different structural forms — e.g., input-dependent module selection, variable module durations, or content-dependent gating — would significantly strengthen the contribution.

### Minor

1. **Fixed number of modules matched to ground truth.** The main-text results use N = 6 modules for 6 operations, the favorable case. The paper acknowledges this limitation (line 181) and includes module-count mismatch experiments in the appendix (Figure A1). However, the main text should summarize this analysis, since a reader needs to know whether the model degrades gracefully or catastrophically when N is misspecified.

2. **"Correlation" metric unspecified for module/gating recovery.** Figure 2a's caption reports "module and gating accuracy (correlation with ground truth operations and transitions)" without stating which correlation metric (Pearson? Spearman?) is used. For discrete operations, the choice of correlation measure and its interpretation should be explained.

3. **"One-shot" terminology could be clarified.** The model infers solutions from a "single episode," which is a full multi-timestep trajectory (e.g., 12 timesteps for a 3-operation task). This differs from standard few-shot usage where "one-shot" means one example per class. Not a flaw, but the paper should distinguish its usage to avoid confusion.

4. **Motor learning model includes several domain-specific modifications.** The paper lists: removing the input \(x_t\), resetting module hidden state after switches, module-specific weights, and a different proposal distribution for the particle filter (line 127). The paper is transparent about these changes, but it does not discuss which are essential to the framework versus merely convenient. This makes it somewhat unclear what counts as the "core" model versus a domain-adapted variant.

### Trivial

None.

## Nice-to-Haves

- **Demonstrate on a task with more complex or variable structure.** A synthetic domain with variable module durations, input-dependent gating, or hierarchical structure would substantially strengthen the "proof-of-principle" without requiring a real-world application.
- **Add an empirical comparison against Alet et al. (2019)** on a shared experimental setup to substantiate the claimed sample-efficiency improvement.
- **Summarize the module-count mismatch analysis (Figure A1) in the main text** rather than deferring it entirely to the appendix.

## Removed Points

These points from the input review are removed with brief justification:

- **"Thinking vs. learning" framing criticism** — Removed. The paper clearly describes its training phase as learning (line 145: "first learning the common components"). The rhetorical contrast is not misleading in context; this is a presentation judgment call rather than a substantive weakness.
- **Missing hyperparameters from main text** — Removed per hard rules. The paper states parameters are described in the appendix (line 217), which was stripped by the parser.
- **Training stability / initialization sensitivity speculation** — Removed. The reviewer speculates that success "likely depends on careful initialization and training," but the paper shows convergence across five seeds (Figure 2a). There is no evidence of instability in the presented results.
- **Thalamic gating connection as speculative** — Removed. This is an observation about a discussion section point, not a weakness of the paper's claims.
- **Section-by-section notes that are observations rather than criticisms** — Individual observations that do not identify a concrete problem (e.g., noting the discussion is well-structured, or that equations are clearly presented) are not retained as weaknesses.

## Novel Insights

The reviews surface one genuinely novel insight beyond the paper's own contributions: the sparse-feedback behavior (posterior collapsing for exactly the learned repetition count, then going uniform) is identified as the paper's most distinctive and compelling result because it provides a non-trivial behavioral signature that the gating RNN has learned correct counting statistics. This specific diagnostic goes well beyond typical accuracy reporting and is the paper's strongest evidence for the value of learned non-Markovian transition structure. The reviews do not uncover additional novel insights beyond what the paper itself demonstrates.

## Suggestions

1. Add an experiment comparing against the closest prior work (Alet et al., 2019) on the same tasks, with shared metrics.
2. Include at least one task with a different structural template (e.g., input-dependent module durations, variable number of modules per task) to substantiate the claim of generality.
3. Move the module-count mismatch analysis (or at least its conclusions) from the appendix into the main text.
4. Specify the correlation metric used for module/gating accuracy in Figure 2a and justify its use for discrete comparisons.

MY FINAL SCORE: <score>6</score>
MY FINAL DECISION: <decision>Borderline Accept</decision>