Good. Line 73 mentions "variable renaming or statement reordering" as contrastive augmentations for pre-training — not as the RL agent's action space. Confirmed: the paper never enumerates the agent's actual refactoring operations.

Here is the final review.

---

## Summary

The paper proposes an RL-based automated code refactoring framework that uses contrastive pre-trained code graph embeddings. The key idea is to learn structural invariant representations of code via a self-supervised contrastive objective on graph-structured code, then combine learned embeddings with traditional code quality metrics in a composite reward function for PPO-based RL training. The paper evaluates on three datasets with five metrics and reports comparisons against rule-based, learning-based, and RL-based baselines, plus a cross-language generalization experiment.

## Strengths

- **The ablation study (Table 2) methodically decomposes four components** (contrastive pre-training, embedding rewards, semantic tests, random exploration) and quantifies each component's contribution. The −7.5% SI drop without contrastive pre-training and −8.6% SP drop without semantic tests are informative diagnostics that help the reader understand which parts of the method matter.

- **The cross-language generalization experiment (Table 3)**, testing a Java-pretrained model on Python and C++ without fine-tuning, goes beyond the standard single-language evaluation common in refactoring work and provides useful evidence about transferability.

## Weaknesses

### Fatal

None.

### Major

- **Action space is never specified.** The paper defines the MDP with $A$ denoting the action space (line 57: *"A denotes the action space (possible refactorings)"*) but never enumerates the actual refactoring operations the agent can perform (e.g., extract method, rename variable, inline function, reorder statements, change access modifiers, etc.). For both an RL paper and a code refactoring paper, this is a basic specification failure: the reader cannot understand what the agent is actually doing, the results cannot be interpreted, and the method is not reproducible from the description provided.

- **The GraphRL baseline is misattributed.** The paper lists *"GraphRL (Darvari et al., 2024): GNN policy with expert demonstrations"* (line 203) and cites Darvari et al. 2024 as *"Graph reinforcement learning for combinatorial optimization: A survey and unifying perspective"* (lines 347–349). The cited work is a survey on combinatorial optimization, not a method paper proposing a code refactoring system. It is unclear where the GraphRL results in Table 1 come from or whether this is a reasonable comparator. This undermines the credibility of the baseline comparison.

- **No variance or statistical significance reported.** All results in Tables 1, 2, and 3 are single numbers with no standard deviations, confidence intervals, or significance tests. The claimed margins over NeuroRefactor are 4–5 percentage points (SI, SP, GS), but without error bars there is no way to assess whether these differences are meaningful gains or noise. This is a significant evidential gap for the paper's central empirical claim.

- **The embedding dynamics reward term lacks principled justification.** Equation (5) includes $+\alpha\tanh(\beta\|\mathbf{h}_t - \mathbf{h}_{t-1}\|_2)$ that positively rewards the agent for making large movements in latent embedding space. The only justification given (line 119: *"The hyperbolic tangent means that the gradients propagate in a stable way during RL training"*) addresses the choice of nonlinearity, not why large $\Delta\mathbf{h}$ should be rewarded. Large embedding changes could correspond to damaging transformations that happen to preserve test coverage. Figure 2 shows a correlation ($r=0.72$) between embedding dynamics and syntactic improvement, but this is a descriptive finding, not a causal justification — SI is already optimized through other reward components, so this correlation does not validate the sign of this term. The ablation (Table 2, "w/o embedding rewards") removes the entire embedding-based reward and does not isolate the marginal effect of this specific term.

- **Cross-language claim is overgeneralized.** The paper states the method *"out-performing language-specific rule-based tools"* in cross-language transfer (line 266). Table 3 shows this is accurate for SI (68.7% vs PyLint's 59.2% for Python; 63.5% vs Cppcheck's 54.3% for C++) but *false* for SP, where the proposed method is lower than rule-based tools (88.9% vs 90.4% for Python; 91.2% vs 93.1% for C++). The paper should accurately characterize this mixed result rather than claiming general outperformance.

### Minor

- **The semantic test mechanism is underspecified.** The paper mentions generating test cases via symbolic execution (line 145) and a parameter $L$ for test case count (line 149), but reports no details on how many test cases are generated per method or what the computational cost of symbolic execution is for arbitrary code. This could be a significant practical bottleneck.

- **Hyperparameter sensitivity is not explored.** Reward weights $w_q = [0.4, 0.3, 0.3], \alpha=0.2, \beta=1.0, \gamma=0.5$ are reported as single values with no sensitivity analysis. The ablation removes entire components but does not vary scaling parameters within components.

- **Computational cost is not reported.** No training time, inference time, or GPU-hour comparisons are provided, even though the pre-training uses 8×V100 GPUs and practical deployment relevance is claimed.

### Trivial

None.

## Nice-to-Haves

- An ablation that removes just the embedding dynamics term $\alpha\tanh(\beta\Delta\mathbf{h}_t)$ while keeping the rest of the embedding-based reward would be more informative than the current "w/o embedding rewards" row.
- Reporting results with standard deviations over multiple seeds (at least 3–5) would substantially strengthen the empirical claims.
- A sensitivity analysis on the reward scaling parameters would help assess robustness.

## Removed Points

These points were raised by the harsh critic but removed for the following reasons:

1. **Writing quality / "garbled prose" criticism (abstract, intro, "lemon deep learning")**: Parser artifacts — the instruction treats garbled text as a formatting issue in the extraction, not author error.
2. **Criticism about 2025 citations (Marvellous et al., Polu) being on researchgate.net/academia.edu with "content cannot be assessed"**: Hard rules prohibit flagging cited references as unverifiable.
3. **LLM polish criticism**: Subjective writing quality complaint; the paper transparently acknowledges LLM use for polishing.
4. **PMD/Checkstyle "inflating apparent performance"**: The paper honestly categorizes these as "Rule-based" and includes multiple learned baselines. Including rule-based tools as a separate category is standard benchmarking practice.
5. **RLRefactor lacking implementation details**: Partially redundant with the already-included Major weakness about the paper's own missing action space; expecting full implementation details for every baseline is not always feasible in a conference paper.
6. **Strength: "problem selection is well-motivated"**: Generic and about whether the problem is important, not a concrete, paper-specific strength.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

- **Specify the action space explicitly**: enumerate every refactoring operation the agent can apply, the granularity (single-operation or composite), and the action selection mechanism.
- **Clarify the GraphRL baseline**: either correct the citation to a specific method paper or describe how the method was implemented from the survey.
- **Add error bars** (standard deviations over at least 3 random seeds) to all quantitative results, especially Table 1.
- **Provide a principled justification** (or remove) the positive sign on the embedding dynamics reward term; at minimum, ablate it in isolation.
- **Correct the cross-language claim** to accurately reflect that SP is lower than rule-based tools, and discuss why.

## Score and Decision

Score: 4

Decision: Reject

MY FINAL SCORE: <score>4</score>
MY FINAL DECISION: <decision>Reject</decision>