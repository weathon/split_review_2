## Summary
# Final Review Report

## Summary

This paper proposes Agentic Reinforced Policy Optimization (ARPO), a reinforcement learning algorithm for training multi-turn LLM-based agents that use external tools (search engine, web browser, code interpreter). The key idea is to move beyond trajectory-level RL rollouts by using token entropy as a signal for adaptive branching: when entropy spikes after a tool-call step, ARPO triggers additional partial rollouts to explore alternative tool-use behaviors. The method is evaluated across 13 benchmarks spanning mathematical reasoning, knowledge-intensive QA, and deep search tasks, using Qwen2.5/3 and Llama3.1 backbones.

**Strengths:** The entropy-based adaptive rollout is a well-motivated extension of GRPO that addresses a genuine limitation of trajectory-level RL for multi-turn agent training. The empirical evaluation is broad (13 datasets, multiple backbones) and the tool-call efficiency analysis shows meaningful computational savings. The paper is generally well-written and the method is clearly described with helpful figures.

**Core weaknesses:** (1) No statistical significance or variance reporting for any result, making claimed improvements hard to verify. (2) The "half the tool-call budget" claim is overstated (actual reduction is ~30-40% in the reported experiment). (3) The GPG "Theorem" is a reformulation of the standard policy gradient, not a new theoretical result. (4) Entropy normalization is underspecified, hindering reproducibility. (5) The complexity analysis (O(n²) vs O(n log n)) is unsubstantiated. (6) No limitations section or failure case analysis.

**Novelty assessment (deferred):** Retrieval-Disabled Mode is active for this run; external literature verification could not be performed. Claims of "pioneering" entropy quantification and theoretical novelty should be verified against prior work (particularly Wang et al. 2025b,c; Cheng et al. 2025; segment-level RL objectives cited in the paper itself) in a follow-up review.

## Strengths
1. **Well-motivated algorithmic extension.** The paper identifies a genuine limitation of trajectory-level RL for multi-turn tool-use agents: the inability to explore at fine-grained tool-call steps where uncertainty is highest. Using token entropy as a branching signal is a practical and intuitive heuristic that connects observable model behavior (entropy spikes after tool calls) to an algorithmic intervention (adaptive partial rollouts).

2. **Comprehensive evaluation scope.** The method is tested across 13 datasets covering three distinct reasoning categories (mathematical, knowledge-intensive, deep search) with two model families (Qwen and Llama). The deep search evaluation (Table 2) is particularly thorough, comparing against multiple single-enhanced methods (RAG, Search-o1, WebThinker, ReAct) and trajectory-level RL algorithms (GRPO, DAPO, REINFORCE++). The inclusion of closed-source models (GPT-4o, DeepSeek-R1, o1-preview) as reference points helps contextualize performance.

3. **Tool-call efficiency analysis.** The analysis in Section 5.2 showing reduced tool-call usage during training (Figure 7a) is practically relevant for deployment scenarios where API costs or latency matter. The rollout diversity analysis (Figure 7b) using PCA + DBSCAN clustering provides additional evidence that ARPO achieves broader exploration of the solution space.

4. **Open-source release.** The authors release code at https://github.com/RUC-NLP/ARPO, which supports reproducibility and follow-up research.

5. **Clear ablation of advantage estimation.** The comparison between hard and soft advantage estimation (Figure 5) provides useful insight into design choices for advantage attribution in branched rollout structures, showing that the soft approach (via GRPO's natural importance sampling) yields more stable training dynamics.

## Weaknesses
### W1. No Statistical Significance or Variance Reporting (Critical)
**Evidence:** Tables 1 and 2 report single-pass accuracy numbers without any variance, confidence intervals, or significance tests. The improvements over baselines are small (2-5 percentage points average). On specific sub-tasks, ARPO underperforms individual baselines (e.g., Qwen2.5-7B on MATH500: DAPO 80.4 vs ARPO 78.8).

**Impact:** Without multi-seed variance or statistical tests, the claimed "consistent outperformance" cannot be reliably assessed. RL training is known to have high variance across seeds, and single-run results may reflect favorable random initialization rather than genuine algorithmic advantage.

**Required action:** Report all main results as mean ± std over ≥3 seeds. Add a paired significance test (e.g., bootstrap or Wilcoxon signed-rank) comparing ARPO against the strongest baseline on each dataset. Identify and discuss cases where ARPO does not outperform baselines.

### W2. Overstated "Half the Tool-Call Budget" Claim (Major)
**Evidence:** Page 2 (contribution list) and Page 9 state ARPO requires "only half the tool-call budget" compared to other methods. Figure 7a shows ARPO uses ~250-350 calls vs GRPO ~400-450 — a 30-40% reduction, not 50%. The comparison is only against GRPO, not DAPO or Reinforce++.

**Impact:** This overstatement may mislead readers and can trigger reviewer skepticism, potentially undermining otherwise solid empirical results.

**Required action:** Replace "half" with precise numbers (~30-40% fewer tool calls vs GRPO on Qwen2.5-7B). Compare tool-call efficiency against at least one additional trajectory-level RL method. Provide wall-clock time per training step for a complete efficiency picture.

### W3. Underspecified Entropy Normalization (Major)
**Evidence:** Section 3.1 (Step 2) defines ΔH_t = Normalize(H_t - H_initial), explaining normalization as "summing all the values of ΔH and dividing by the vocab size V." This is ambiguous: ΔH_t is introduced as a vector (ℝ^{1×k}) but the normalization description treats it as a scalar. Dividing by V (~128k) would produce very small values, making P_t = α + β·ΔH_t dominated by α unless β is tuned to compensate.

**Impact:** This ambiguity prevents exact reproduction of the method. The branching behavior is highly sensitive to the scale of ΔH_t, and incorrect implementation could produce qualitatively different results.

**Required action:** Provide the exact mathematical form of the normalization. Specify whether ΔH_t is a scalar or vector, how the k token positions are aggregated, and report typical ranges of ΔH_t in practice together with chosen α, β, τ values.

### W4. Unsubstantiated Computational Complexity Analysis (Major)
**Evidence:** Section 3.1 claims "ARPO reduces the computational complexity of each rollout from the trajectory-level RL's O(n²) to between O(n log n) and O(n²)." The variable n simultaneously represents "global expansion size and the number of tokens per trajectory" — conflating two independent quantities. No derivation or reference supports the O(n log n) claim. The entropy computation overhead O(V) per token is dismissed as "minor" but V~128k makes it non-negligible for long rollouts.

**Impact:** Unsubstantiated complexity claims can mislead readers about scalability and may weaken the paper's credibility during technical review.

**Required action:** Remove the O(·) claims or provide a rigorous derivation. Replace with empirical runtime comparison (wall-clock time, total tokens generated, total training time) between ARPO and baselines.

### W5. Overclaimed Theoretical Contribution (Major)
**Evidence:** Section 3.3 presents the "Generalized Policy Gradient (GPG) Theorem" as a novel theoretical foundation. However, Eq. (6) is a direct application of the standard policy gradient theorem with temporally extended actions (macro actions). The theorem does not use any Transformer-specific property despite claiming applicability to "all Transformer-based policies." The proof (in Appendix F.3) likely follows the same steps as the standard PG proof.

**Impact:** Presenting a standard result as a new theorem may be seen as novelty inflation and can damage the paper's reception. The GPG framing is a useful perspective but should not be claimed as a novel theoretical contribution.

**Required action:** Rephrase Section 3.3 as "Macro-Action Policy Gradient Perspective" rather than a new theorem. Acknowledge that this follows from the standard PG theorem. Remove the claim of Transformer-specific novelty unless a non-trivial Transformer-dependent property is proven.

### W6. Missing Limitations and Failure Case Analysis (Major)
**Evidence:** The paper has no Limitations section. The Conclusion (Section 7) merely restates the abstract without discussing any scenarios where ARPO might underperform, hyperparameter sensitivity, computational overhead of entropy monitoring, or comparison to simpler baselines.

**Impact:** Omitting limitations reduces scientific rigor and completeness. Reviewers and readers cannot assess the boundary conditions of the method's effectiveness.

**Required action:** Add a dedicated Limitations subsection in the Conclusion or as a separate section. Discuss: (a) hyperparameter sensitivity (α, β, τ), (b) settings where trajectory-level methods may be sufficient, (c) additional computational cost of entropy monitoring, (d) limited tool diversity in evaluation.

### W7. Missing Hyperparameter Reporting (Minor)
**Evidence:** The core adaptive rollout mechanism depends on hyperparameters α (base sampling probability), β (entropy coefficient), τ (branching threshold), Z (branch width), M (total rollout size), and N (initial trajectories). None of these values are reported in the main text or experimental setup.

**Impact:** The method cannot be reproduced without these values. If performance is sensitive to these parameters, the generalization claims are weakened.

**Required action:** Report all hyperparameter values in a table in Section 4 (Experimental Setup). Add a sensitivity analysis showing the effect of varying τ and the branching budget on final performance.

### W8. Writing and Presentation Issues (Minor)
**Evidence:** (a) The symbol τ is used for both decoding temperature (Eq. 1) and branching threshold (Eq. 2). (b) The abstract sentence ends abruptly in the extraction. (c) The phrase "pioneeringly quantify" (contribution list) is promotional. (d) The introduction contains dense citation blocks (up to 10 citations per sentence) that obscure the narrative.

**Impact:** These issues reduce readability and may create an impression of carelessness.

**Required action:** (a) Rename branching threshold to γ or θ. (b) Remove promotional language. (c) Reduce citation density by grouping related work. (d) Proofread for sentence completeness.

## Score
**Final Score: 6.5/10**

**Rationale:** The paper presents a practically motivated and well-evaluated algorithm for multi-turn tool-use agent training. The entropy-based adaptive rollout is a genuine extension of GRPO with demonstrated empirical benefits. However, the score is constrained by several methodological weaknesses: the absence of statistical significance testing and variance reporting (W1) limits confidence in the claimed improvements; the overstated efficiency and novelty claims (W2, W5) reduce the paper's scientific credibility; and underspecified algorithmic details (W3, W4, W7) hinder reproducibility. The missing limitations discussion (W6) further reduces completeness. The paper is above the acceptance threshold in most venues with major revisions, but the current form requires substantial strengthening of the empirical methodology and more measured claim framing.

**Scoring breakdown (priority: research value + novelty):**
- Research value: 7/10 — Practical problem (multi-turn agent alignment) with a sensible algorithmic contribution
- Novelty: 6/10 — Incremental over GRPO; entropy-based branching is a novel combination but GPG theory is not a new result
- Validity/Soundness: 5/10 — Undermined by missing variance, overclaims, and underspecified normalization
- Reproducibility: 5/10 — Missing hyperparameters and ambiguous normalization hinder exact reproduction
- Presentation: 7/10 — Generally clear writing with helpful figures; some promotional language and citation density issues

```text
ASCII Diagram — Paper Structure & Evidence Map

[Problem: trajectory-level RL ignores tool-use step uncertainty]
    ↓
[Observation: entropy spikes after tool calls (Fig 1, Fig 2)]
    ↓ Evidence strength: Level 1 (descriptive correlation)
    ↓
[ARPO Solution: entropy-based adaptive rollout + advantage attribution]
    ↓
    ├── Adaptive Rollout: P_t = α + β·ΔH_t, branch if > τ
    │       Evidence: underspecified normalization (W3)
    │       Missing: hyperparameter values α,β,τ (W7)
    ├── Advantage Estimation: Hard vs Soft (GRPO-based)
    │       Evidence: Fig 5 comparison (adequate)
    └── GPG Theorem: macro-action policy gradient (Eq. 6)
            Evidence: standard PG reframing (W5)
    ↓
[Experiments: 13 benchmarks, 2 model families]
    ↓
    ├── Table 1: Math + Knowledge Reasoning
    │       Missing: variance, significance tests (W1)
    ├── Table 2: Deep Search
    │       Missing: variance, significance tests (W1)
    ├── Tool-call efficiency (Fig 7a)
    │       Issue: "half" overstated by 20% (W2)
    └── Rollout diversity (Fig 7b)
            Evidence: 54 vs 48 clusters (adequate)
    ↓
[Conclusion: lacks limitations, failure cases (W6)]
```

```text
ASCII Diagram — Revision Strategy Roadmap

Priority 0 (Must, before resubmission)
├── W1: Add 3-seed variance + significance tests to Tables 1/2
├── W2: Correct "half" to "30-40%" throughout manuscript
├── W3: Clarify entropy normalization with exact formula
└── W7: Report all hyperparameters (α, β, τ, Z, M, N) in a table

Priority 1 (Should, strongly recommended)
├── W4: Replace O(·) claims with empirical runtime comparison
├── W5: Rephrase GPG as "macro-action perspective" not "new theorem"
└── W6: Add dedicated Limitations section (3-5 concrete points)

Priority 2 (Nice-to-have)
├── W8: Fix τ symbol conflict, reduce promotion, group citations
├── Add entropy-based vs random branching ablation
└── Compare tool-call efficiency against DAPO and Reinforce++
```

```text
ASCII Diagram — Related-Work Taxonomy Tree (Layered)

Agentic RL for LLMs (Root)
├── Branch 1: Trajectory-Level RL Methods
│   ├── Leaf 1.1: GRPO-based agent training (Shao et al., Dong et al.)
│   ├── Leaf 1.2: DAPO / REINFORCE++ for tool-use (Yu et al., Hu)
│   └── Limitation: coarse credit assignment for multi-turn steps
│       → ARPO addresses this via step-level branching
├── Branch 2: Credit Assignment & Reward Design
│   ├── Leaf 2.1: Refined reward functions (Wang et al., Bai et al.)
│   ├── Leaf 2.2: Segment-level RL objectives (Guo et al., Zheng et al.)
│   └── Leaf 2.3: Multi-tool coordination rewards (Tool-Star)
│       → ARPO complements with step-level advantage attribution
├── Branch 3: Entropy & Uncertainty in RL
│   ├── Leaf 3.1: Token entropy analysis (Wang et al. 2025b,c; Cheng et al.)
│   └── Leaf 3.2: Exploration via uncertainty (Ruan et al., Li et al.)
│       → ARPO extends entropy-based exploration to agentic RL
└── Branch 4: Tool-Augmented Agent Frameworks
    ├── Leaf 4.1: Search-based agents (WebThinker, Search-o1)
    ├── Leaf 4.2: ReAct-style reasoning (Yao et al.)
    └── Leaf 4.3: Web browsing agents (WebWalker, HIRA)
        → ARPO provides RL training methodology for any tool-use agent
```

**Novelty & Retrieval Note:** External literature verification is unavailable in this run (Retrieval-Disabled Mode active due to missing API token). The "pioneering" claim for entropy quantification during agentic reasoning (C1) should be verified against the entropy-based RL studies already cited by the authors (Wang et al., 2025b,c; Cheng et al., 2025; Zheng et al., 2025b) and other concurrent work. The GPG Theorem novelty (C3) is judged as a reframing from internal evidence alone, but prior art on macro-action policy gradients should be checked. Manual follow-up verification is recommended before final acceptance decisions.