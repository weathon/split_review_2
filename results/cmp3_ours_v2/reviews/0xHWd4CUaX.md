I've completed my calibration analysis. Let me write the final review.

**Calibration Summary:**

| Anchor | Path | Avg Score | Round | Comparison to this paper |
|--------|------|-----------|-------|------------------------|
| KL Divergence Optimization for GFlowNets | Uj0h13lVrR.md | 1.00 | R1 | Much less coherent; our paper at least has equations and tables |
| Advancing Cross-Lingual Capabilities | gwZ90hFSL2.md | 1.00 | R1 | Pseudo-scientific framing; our paper has a genuine method skeleton |
| D2Coder | dsALpkd1OU.md | 1.67 | R2 | Coherent abstract but other fatal flaws; our paper has worse writing but more method structure |
| Hierarchical Self-Supervised Graph Contrastive Learning | pL8ws91RW2.md | 2.60 | R1 | Clear writing but limited novelty; our paper has far worse writing quality |
| COSTAR Safe RL | hZztyfmr8n.md | 3.00 | R1 | Clear method description with some novelty; our paper is significantly less coherent |
| Graph RL for Combinatorial Optimization | d1zLRzhalF.md | 2.50 | R2 | Clear writing, limited novelty; our paper is less clear |
| Structured Predictive Representations in RL | sEv6vHIUnu.md | 4.80 | R1 | Well-written with clear contributions; our paper does not approach this quality |

**Bracket (Round 1):** 1.5–3.0

The paper sits above the 1.0–1.5 band (it has a complete methodological pipeline with equations, tables, ablations) but below the 2.5–3.0 band (papers like COSTAR and the hierarchical GCL paper at least have clear writing and coherently described methods). The combination of an underspecified action space, writing that is genuinely incomprehensible in key passages, and an internal reference inconsistency makes this a clear reject at **2.0**.

## Summary

This paper proposes a framework that combines contrastive pre-training of code graph embeddings with reinforcement learning for automated code refactoring. The approach uses a contrastively pre-trained GNN encoder, a composite reward function, a GNN-based policy network trained via PPO, and differential testing for semantic preservation. Evaluations are reported on Java, Python, and C++ codebases against several baselines.

## Strengths

- **The ablation study (Table 2) follows a clean logic.** Removing contrastive pre-training, embedding rewards, and semantic tests produces monotonic degradation across SI, SP, and MG. The direction of effects is consistent with what the paper's claims would predict, and this is the most solid empirical element in the paper.
- **The cross-language evaluation (Table 3)** tests on Python and C++ after training on Java without fine-tuning. While limited, this goes beyond standard in-distribution evaluation and is a reasonable experimental contribution.
- **The paper attempts a non-trivial integration** of several components (contrastive code graph pre-training, composite reward with embedding dynamics, embedding-guided exploration, differential testing) into a single RL refactoring pipeline, which indicates a thoughtfully scoped research direction.

## Weaknesses

### Fatal
None.

### Major

1. **The action space is never concretely specified.** The MDP definition (Section 3.1) lists *A* as "action space (possible refactorings)" and then never says what the actions are. Section 4.4 describes the policy network processing concatenated features through attention and producing "correct refactoring actions," but what those actions are — whether categorical choices among predefined refactoring types (extract method, rename variable, etc.), token-level edits, or region-level transformations — is never stated. The qualitative analysis (Section 5.5) lists three outcomes ("Pattern Consolidation," "Dataflow Optimization," "Architectural Hint") but these are high-level descriptions of results, not action definitions. For an RL method paper whose central claim is learning a refactoring policy, this omission is a **structural gap**: the state transitions, policy output layer, and environment dynamics are all uninterpretable without knowing what decisions the agent makes.

2. **The writing is severely below publication standard in multiple key passages, obscuring core claims.** The abstract contains a sentence that cannot be parsed: *"The key challenge is balancing the implementation of syntactic improvements - while maintaining the semantics of the code being refactored - something that necessarily requires the existing RL approaches to accomplish and that most often do last year because of the handcrafted nature of their metrics."* The main body contains "Recent lemon deep learning technologies" (Section 2.2) and "objecting to code quality" (Section 1, where the intended meaning is clearly "improving"). Section 8 states "We use LLM polish writing based on our original paper." A paper whose abstract and introduction fail to convey their technical content in plain, unambiguous language cannot be accepted for peer review, regardless of the underlying technical quality.

3. **The Darvari et al. (2024) baseline is cited in a way that raises concern about internal consistency.** The paper describes "GraphRL (Darvari et al., 2024): GNN policy with expert demonstrations" (Section 5.1). The reference entry reads *"Graph reinforcement learning for combinatorial optimization: A survey and unifying perspective"* — a survey paper on combinatorial optimization, not a code refactoring method with expert demonstrations. This is an internal inconsistency: the cited reference does not match the claimed method. The paper also provides no description of how any baseline was configured (hyperparameters, whether re-implemented or taken from published code), making it difficult to assess whether the comparisons are informative.

### Minor

4. **No variance, error bars, or statistical significance is reported for any result.** Every value in Tables 1, 2, and 3 is a single point estimate. There is no indication of how many runs were performed, whether results are stable across random seeds, or whether differences between methods are statistically reliable. Some margins are modest (e.g., SI: 77.8→79.4→83.7 across GraphRL, NeuroRefactor, and Ours).

5. **The cross-language evaluation claim is partially contradicted by the paper's own data.** Section 5.4 states the method "out-performing language-specific rule-based tools." Table 3 shows SI is indeed higher for Ours (68.7 vs 59.2 for Python; 63.5 vs 54.3 for C++) but SP is lower than both PyLint (88.9 vs 90.4) and Cppcheck (91.2 vs 93.1). The claim as stated is broader than the evidence supports.

6. **The embedding dynamics reward (Eq. 5) has a perverse incentive that is not discussed.** The term α tanh(β Δh_t) where Δh_t = ||h_t - h_{t-1}||_2 rewards the agent for producing large changes in embedding space, which by construction incentivizes code changes that are maximally distant from the original regardless of quality improvement. The ablation (Table 2) shows removal drops SI from 83.7 to 79.5 but does not clarify reward weight redistribution. Figure 2's positive correlation (r=0.72) between Δh and SI is consistent with both being driven by successful refactoring and does not establish that this specific incentive structure is beneficial.

7. **The learning curve (Figure 1) compares only against GraphRL**, not against any of the other six baselines. The cross-language evaluation (Table 3) compares only against rule-based tools, not against the learning-based or RL-based baselines from Table 1. If those methods cannot be applied cross-language, the paper should state this explicitly.

### Trivial

- The qualitative analysis (Section 5.5) lists three refactoring patterns without showing actual code examples, making the analysis unverifiable.

## Nice-to-Haves

- **Specify the action space:** enumerate the concrete refactoring operations the agent can choose from and how they map to code transformations.
- **Add variance reporting:** run at least 5 seeds and report means with standard deviations or confidence intervals.
- **Include learning-based baselines in the cross-language evaluation** or explain clearly why they cannot be applied.
- **Discuss the reward-hacking incentive** in the embedding dynamics term and provide an ablation with controlled weight redistribution.
- **Qualify the cross-language claims** to acknowledge the SP gap.

## Removed Points

The following points from the input review are removed with justification:

- **Marvellous et al. (2025) plausibility / Polu (2025) academia.edu**: These sub-points question the existence of references, which per hard rules is removed. The reference inconsistency about Darvari et al. (2024) being a survey paper is **kept** because it is about internal inconsistency (the paper's description of the method does not match the reference's content), not about existence.
- **Missing related works**: Removed per hard rule (no external sources to confirm).
- **Background section being "textbook material"**: Generic, no specific anchor in the paper.
- **"Does not establish a clear technical gap"**: Generic, no specific anchor.
- **Missing appendix content or proofs**: Removed per hard rule about PDF extraction stripping appendices.
- **Formatting/style nitpicks**: Removed per hard rules about parser artifacts.
- **"The high-level idea is sensible" strength**: Generic and not specific to the paper's execution.

## Novel Insights

None beyond the paper's own contributions. The identified weaknesses are structural (underspecified action space, poor writing, reference inconsistency) rather than nuanced methodological insights.

## Suggestions

1. **Concretely define the action space.** Without this, the paper is not reproducible and the experimental results are uninterpretable — the reader cannot know what decisions the agent is making.
2. **Revise the writing** so the abstract, introduction, and method sections convey their technical claims in plain, unambiguous language. Have a native English speaker review the manuscript before resubmission.
3. **Resolve the Darvari et al. (2024) inconsistency** — either correct the reference or replace it with an actual code-refactoring RL baseline with appropriate citation.
4. **Report results with variance** across multiple random seeds and perform basic statistical tests for the main comparisons in Table 1.
5. **Qualify the cross-language claims** to accurately reflect that SP is lower than rule-based tools even as SI is higher.
6. **Add a discussion** of the perverse incentive in the embedding dynamics reward, with controlled weight-redistribution ablation.

## Score and Decision

**Round 1 bracket:** 1.5–3.0, based on comparison with 16 calibration anchors.

The paper sits above the 1.0–1.5 band (papers with no coherent method skeleton) and below the 2.5–3.0 band (papers like COSTAR and the hierarchical GCL paper that have clear writing and coherent methods but limited novelty). The combination of a fundamentally underspecified action space, severely poor writing in critical passages, and an internal reference inconsistency make this a clear reject.

MY FINAL SCORE: <score>2.0</score>
MY FINAL DECISION: <decision>Reject</decision>