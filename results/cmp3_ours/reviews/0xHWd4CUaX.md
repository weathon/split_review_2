## Summary

This paper proposes a reinforcement learning framework for automated code refactoring that combines contrastive pre-training on code graphs with a composite reward function and a graph attention policy network. The approach is evaluated on refactoring benchmarks against rule-based, learning-based, and RL-based baselines, with ablation studies and a cross-language transfer experiment.

## Strengths

1. **Well-structured method with clear components.** The contrastive encoder (Section 4.1), composite reward (Section 4.2), and graph attention policy (Section 4.4) are cleanly separated, and each component serves a plausible role within the overall framework.

2. **Ablation study (Table 2).** The paper systematically removes each major component and reports directional impacts on Syntactic Improvement (SI), Semantic Preservation (SP), and Maintainability Gain (MG). This is the appropriate analytical approach for a multi-component method.

3. **Cross-language transfer experiment (Table 3).** Testing on Python and C++ after training only on Java is a meaningful test of generalization, even if the evaluation design has significant shortcomings (noted below).

## Weaknesses

### Major

1. **Action space is never defined (Sections 3.1, 4).** The paper defines the MDP tuple `(S, A, P, R, γ)` and states that `A` denotes "possible refactorings" (line 57), but it never specifies what concrete actions the agent can take. Are these discrete operations (extract method, rename variable, inline method, pull up field, etc.)? Token-level edits? Parameterized by AST node location? The policy network (Equation 7, line 133) processes `[h_t; q_t]` but provides no description of how actions are parameterized or decoded from this representation. Without the action space, the method as presented is incomplete — it cannot be reproduced or even understood operationally. This is a fundamental method specification gap.

2. **No variance or statistical significance reported (Tables 1, 2, 3).** Every result is a single point estimate with no standard deviation, confidence interval, or number of runs. For RL-based methods, variance across random seeds is typically substantial. The claimed 4.3pp SI advantage over NeuroRefactor (83.7% vs. 79.4%) and the ablation drops (e.g., −7.5% SI without contrastive pre-training, −8.6% SP without semantic tests) are all uninterpretable without error bars. This undermines every quantitative claim in the paper.

3. **Missing key baselines that would directly test the core claim.** The paper's central technical innovation is contrastive pre-training on code graphs. Yet SyncoBERT (Wang et al., 2021) and GraphCodeBERT (Guo et al., 2020) — both cited in the related work (lines 41-43) as relevant contrastive code models — are **not** used as baselines (e.g., by plugging their embeddings into the same RL pipeline). This means the reported advantage could be driven by other design choices (composite reward, GAT policy, exploration strategy) rather than the contrastive encoder specifically. The ablation study partially addresses this, but does not substitute for comparison against existing contrastive code representation models.

4. **Cross-language evaluation compares only against rule-based linters (Table 3).** The method is compared only against PyLint and Cppcheck — not against any learning-based method. Furthermore, the method's Semantic Preservation is *worse* than the rule-based tools in both cases (88.9% vs. PyLint's 90.4% for Python; 91.2% vs. Cppcheck's 93.1% for C++). Comparing against the learning-based baselines from Table 1 re-run on the target languages would be the necessary experiment to demonstrate cross-language generalization.

### Minor

1. **Symbolic execution feasibility unaddressed (Section 4.5).** The method proposes using symbolic execution for test case generation and execution trace comparison at each environment step (lines 144-149). Symbolic execution is known to suffer from path explosion and high computational cost. The paper provides no runtime analysis, wall-clock time comparison, or discussion of what approximations are used. If a cheaper heuristic is substituted in practice, the description as written is misleading.

2. **Freezing vs. fine-tuning the encoder is not ablated (Section 4.6).** The contrastive encoder `f_θ` is fixed during RL fine-tuning (line 156), meaning the reward signal cannot reshape the representations for the refactoring task. The paper neither justifies nor ablates this design choice.

3. **"w/o contrastive pre-training" ablation is ambiguous (Table 2).** Removing contrastive pre-training — but what replaces the encoder? A randomly initialized GAT may not converge in 1M environment steps, so the observed drop could reflect insufficient training rather than the value of contrastive learning per se. The replacement is not specified.

4. **Embedding-guided exploration bootstrapping not discussed (Section 4.3).** The exploration strategy (Equation 6) uses Mahalanobis distance to a running average of "high-reward states." Early in training before any high-reward states are identified, the mechanism reduces to random exploration. This bootstrapping issue is unaddressed.

5. **Claim about reducing expert demonstrations is not evaluated.** The Introduction states the method reduces "the necessity of expert demonstration based learning" (line 21), but no experiment compares sample efficiency or data requirements against expert-demonstration-based approaches.

6. **GCN background is inconsistent with GAT method.** Equation 3 (line 81) describes a standard GCN update, while the method (Section 4.1) uses graph attention. This is a minor disconnect between the background section and the actual method.

### Trivial

None.

## Nice-to-Haves

- Adding hyperparameter sensitivity analysis for reward weights (`w_q`, `α`, `β`, `γ`, listed on line 226) would strengthen the empirical evaluation.
- A wall-clock training time and inference latency comparison, particularly for the symbolic execution component, would help assess practical feasibility.

## Removed Points

These points were flagged in the input review but removed per filtering rules. Treat them with caution — they may reflect genuine issues but were excluded for procedural reasons.

- **Grammar/writing quality criticisms (abstract, "lemon deep learning technologies," etc.):** Removed per hard rule — parser-extracted text may contain artifacts, and grammar/style nitpicks are excluded by instruction.
- **LLM-use writing quality criticism:** Removed — same rule as above applies.
- **Related work venue credibility:** The critic noted that references are weighted toward unreviewed tech reports. Removed per hard rule — the existence and availability of cited references must not be questioned.
- **LLM-based baselines as a required comparison:** Removed as scope creep. The paper is about RL-based refactoring; LLM-based code transformation is a different paradigm and demanding it as a required baseline overextends the paper's stated scope.
- **Abstract clarity complaint:** Removed per grammar/style rule.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. **Define the action space explicitly and concretely.** List the discrete refactoring operations available to the agent, how they are parameterized (e.g., by AST node type and location), and how the policy network decodes them from the `[h_t; q_t]` representation.

2. **Report means with standard deviations over multiple random seeds** for all main experimental results (Tables 1, 2, 3). This is the single highest-leverage change for making the results interpretable.

3. **Add baselines using embeddings from existing contrastive code models** (SyncoBERT, GraphCodeBERT) in the same RL pipeline. This directly tests whether the paper's contrastive pre-training approach provides benefits beyond existing alternatives.

4. **Redesign the cross-language experiment** to compare against learning-based baselines on the target languages, not just against rule-based linters.

5. **Add an ablation comparing frozen vs. fine-tuned encoder** during RL training to justify the design choice of fixing `f_θ`.

## Score and Decision

### Calibration Summary

I performed iterative calibration against the available review corpus. Anchors used:

| Path | Avg Score | Round | Comparison |
|---|---|---|---|
| `N18Z2MkMEa` (FALCON) | 3.00 | Round 1 | Both papers apply RL to code with underspecified components. FALCON had unclear method motivation; this paper has a clearer architecture but a more severe method gap (undefined action space). |
| `vLqkCvjHRD` (Coarse-Tuning) | 4.75 | Round 1 | Clearer method specification and evaluation than this paper. Rejected despite stronger rigor. |
| `zPPy79qKWe` (RLEF) | 4.50 | Round 1 | Clear RL-for-code method with standard evaluation. This paper is notably weaker in both method completeness and evaluation. |
| `4MWUdp6deL` (CodeFavor) | 5.50 | Round 1 | Well-motivated with benchmark contribution. Accepted-range paper. This paper does not reach this quality level. |
| `vfzRRjumpX` (Code Repr. Learning at Scale) | 5.75 | Round 1 | Thorough experiments, clear contributions. Accepted. Far stronger than this paper. |
| `hZztyfmr8n` (COSTAR) | 3.00 | Round 2 | Contrastive + RL with evaluability issues. Comparable quality tier. |
| `dsALpkd1OU` (D2Coder) | 1.67 | Round 2 | Extreme issues. This paper is not at this level — it has a coherent framing. |
| `OXIIFZqiiN` (Dual-Modal) | 1.50 | Round 2 | Incoherent method. This paper is substantially better. |

**Round 1 bracket (initial):** 3.0 – 4.5 — the paper sits between FALCON (3.0) and Coarse-Tuning (4.75), closer to the reject end.

**Narrowing rationale:** The paper's method has a clear three-component structure and the problem framing is coherent, which prevents it from falling into the 1-2 range. However, the undefined action space, complete absence of variance reporting, missing contrastive baselines, and weak cross-language evaluation are each individually serious. Collectively they mean the paper's central claims cannot be evaluated from the presented evidence. This places it below Coarse-Tuning (4.75) and RLEF (4.5), in the 3.0-4.0 range.

MY FINAL SCORE: <score>3.5</score>
MY FINAL DECISION: <decision>Reject</decision>