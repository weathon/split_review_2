## Summary
This paper addresses the important and timely problem of unsafe chain-of-thought reasoning in Large Reasoning Models (LRMs). The authors identify a critical gap: existing safety alignment methods (SFT on curated datasets, outcome-level RL) focus on final response safety but leave intermediate reasoning steps unaligned, creating information leakage and jailbreak vulnerabilities. 

The core contribution is **Intervened Preference Optimization (IPO)**, a method that enforces safe reasoning through three steps: (1) empirically identifying "safety triggers" (critical reasoning steps where safe continuation probability jumps to ~100%) and "compliance cues" (steps where compliance with harmful requests makes unsafe continuation highly likely); (2) constructing preference pairs by replacing compliance cues with safety triggers to generate safe reasoning trajectories; and (3) applying DPO on these pairs at the divergence point to provide localized, strong supervision signals.

Experiments on DS-8B, DS-7B, and Qwen3-8B across three safety benchmarks (JailbreakBench, StrongReject, WildJailbreak) and four reasoning benchmarks (AIME, MATH, GPQA, HumanEval) show that IPO achieves the lowest reasoning harmfulness among compared methods while maintaining competitive reasoning performance. The paper also provides ablation studies on compliance detector choice, training algorithm variants, and sampling efficiency.

**Novelty assessment (deferred — external literature verification unavailable in this run):** The core idea of process-level supervision via corrective intervention in reasoning appears novel relative to the described prior work (SafeChain, RealSafe, STAR, GRPO), but a thorough literature comparison requires external search that was not available in this run. The contribution should be evaluated against concurrent work on CoT monitoring and process reward models.

## Strengths
**1. Timely and well-motivated problem.** The paper addresses a genuinely underexplored safety issue — unsafe intermediate reasoning in LRMs — that persists even when final responses appear safe. The motivation is clearly established through empirical evaluation of existing aligned LRMs (RealSafe, STAR), showing that reasoning harmfulness is systematically higher than response harmfulness (Figure 2), and that safe reasoning strongly correlates with safe responses (Figure 3). This provides a compelling rationale for process-level supervision.

**2. Clean empirical insights driving method design.** The discovery of safety triggers and compliance cues through the Continuation Safety Ratio (CSR) analysis is one of the paper's strongest contributions. The observation that safety is concentrated in a few critical reasoning steps (Section 3.1), that compliance cues are highly correlated with unsafe turns (Pearson R=0.85, Section 3.2), and that corrective intervention can redirect unsafe trajectories (Section 3.3) provides an elegant, evidence-driven foundation for the IPO method. This is more principled than heuristic-based alignment approaches.

**3. Strong empirical results across multiple models and benchmarks.** IPO achieves substantial reductions in reasoning harmfulness (e.g., DS-8B reasoning harmful ratio from 71.5% base to 15.3% — an improvement of ~78% relative) while maintaining competitive reasoning performance. The gains are consistent across three different LRM families (DeepSeek-R1-Llama-8B, DeepSeek-R1-Qwen-7B, Qwen3-8B) and three safety benchmarks with different attack types. The ablation studies (Table 3) demonstrate robustness to compliance detector choice and confirm the advantage of partial DPO over full-trajectory alternatives.

**4. Sampling efficiency advantage.** IPO's explicit construction of safe trajectories requires fewer model generations than GRPO-based RL (14 vs 40+ per prompt) and shorter training time (40 min vs 2+ hours). While this comparison has caveats (discussed in Weaknesses), the underlying principle — that corrective intervention is more sample-efficient than undirected exploration — is sound and practically important.

**5. Comprehensive empirical methodology.** The paper evaluates not only safety but also reasoning capability preservation across math (AIME, MATH), science (GPQA), and coding (HumanEval) benchmarks, and measures over-refusal rates via XsTest. This multi-dimensional evaluation provides a balanced view of the safety-utility trade-off.

## Weaknesses
### Major Weaknesses

**W1. Causal claim of "safe reasoning → safe responses" is correlational, not proven (Page 3 — Section 2.2).** The paper argues that "safe reasoning is a more reliable path to safe outputs" because Figure 3 shows safe reasoning strongly correlates with safe responses. However, this is a correlational finding — the causal direction could be reverse (models that learn safe responses develop safe reasoning as a byproduct) or both could be driven by a common underlying safety representation. The paper does not present a controlled experiment that isolates whether changing reasoning safety causally changes response safety. While the IPO intervention results in Section 4.2 partially address this by showing that reasoning-level alignment improves both reasoning and response safety, the paper should acknowledge the correlational nature of the Section 2.2 claim and cite forward to the causal evidence provided later. *Impact: Weakens the central motivation if readers doubt the causal chain.* (Annotation IDs: dad6b2ec)

**W2. DPO objective in Eq. (4) deviates from standard DPO without explanation (Page 6 — Section 3.4).** The IPO objective uses π_θ(ẑ)/π_θ(z) as the first ratio instead of the standard DPO form π_θ(ẑ)/π_ref(ẑ). This non-standard formulation means the gradient behavior differs from standard DPO: the preferred trajectory ẑ is not anchored to the reference model, allowing uncontrolled drift. The paper does not discuss or justify this design choice. If this is intentional, the authors should explain the motivation, theoretical convergence properties, and empirical differences from standard DPO. If it is a typographical error, the experiments may need to be re-run with the correct formulation. *Impact: Potential correctness issue in the core training objective.* (Annotation ID: 186a62fb)

**W3. Missing variance and statistical significance reporting (Page 7-8 — Section 4.2, Table 2).** All metrics are reported as single-point percentages without standard deviations, confidence intervals, or significance tests. Many comparisons involve small margins (e.g., DS-8B IPO 68.5% vs GRPO 68.3% on average reasoning accuracy — a 0.2% difference). Given that safety evaluation uses GPT-4o (which has inherent stochasticity) and WildJailbreak uses a 250-instance sample, the reported rankings could be within noise range. The paper should report results over multiple training seeds and include bootstrap confidence intervals for safety metrics. *Impact: Reduces confidence in the reported rankings between methods.* (Annotation ID: d1e3867b)

**W4. Heavy reliance on GPT-4o without adequate specification (Pages 1-8 — multiple sections).** IPO's pipeline depends on GPT-4o for three distinct functions: (1) compliance cue detection during preference dataset construction (Section 3.4), (2) safety evaluation of both reasoning and responses (Section 2.1), and (3) safety trigger identification (Section 3.1). The paper does not specify GPT-4o version, prompt templates, temperature, or decoding parameters for any of these uses. This creates several issues: reproducibility is limited; the safety evaluation may inherit GPT-4o's own safety biases; and the practical deployment cost of relying on a commercial API is not discussed. While the compliance detector ablation (Table 3) partially addresses robustness, the evaluation itself still uses GPT-4o — creating potential circularity. *Impact: Reproducibility concern and potential evaluation bias.* (Annotation ID: 860f6db2)

**W5. Questionable reward function design in GRPO baseline (Page 3 — Section 2.3).** The reward function I[z is safe] - I[y is safe] is unusual: it rewards safe reasoning but penalizes safe responses. This could create perverse incentives where the model learns to produce unsafe responses to maximize reward. The small improvement over the simple I[y is safe] reward (36.3% vs 44.0% on WildJailbreak) suggests the reasoning-specific signal adds limited value under GRPO. The paper should discuss this design choice and its potential for reward misspecification, as it directly affects the fairness of comparison between GRPO and IPO. *Impact: GRPO baseline may be suboptimally designed, unfairly advantaging IPO in comparisons.* (Annotation ID: 42fdda2c)

**W6. Sampling efficiency comparison may be unfair to GRPO (Page 8 — Section 4.3).** The paper claims IPO is more sample-efficient than GRPO (14 vs 40+ generations per prompt), but this comparison uses GRPO with rollout size 8 and 5 epochs without evidence that these hyperparameters are optimal. GRPO for reasoning tasks typically benefits from larger rollout sizes. Furthermore, IPO's "14 generations" excludes the upfront cost of GPT-4o API calls for compliance detection, trigger pool construction, and safety evaluation. A fair comparison would include total end-to-end cost including all preprocessing and external API dependencies. *Impact: Efficiency advantage may be overstated.* (Annotation ID: ecc4e820)

**W7. Compliance cue detection accuracy is only ~80% (Page 5-6 — Sections 3.2, 3.4).** The paper reports >80% agreement between GPT-4o-based compliance cue detection and manual annotation. This means approximately 1 in 5 preference pairs may be constructed from incorrectly identified cues. The paper does not report precision/recall, error type analysis (which kinds of cues are commonly missed or misidentified), or whether data filtering by detection confidence would improve results. While Table 3 shows robustness to detector choice, this does not characterize the impact of detection errors on training signal quality. *Impact: Training data noise from detection errors could limit the effectiveness of IPO.* (Annotation ID: 3d4635a8)

### Minor Weaknesses

**W8. Abstract uses vague "over 30% relative reduction" without anchoring the baseline (Page 0 — Abstract).** The specific reference baseline and metric for this claim are ambiguous. The abstract should explicitly state "average reasoning harmfulness across three safety benchmarks compared to the best prior method." (Annotation ID: 74a3e019)

**W9. CSR notation in Eq. (1) uses ambiguous concatenation notation (Page 4 — Section 3.1).** The indicator I(z_s^{≤i} | z_c is safe) uses "|" for both conditioning and string concatenation (defined in Section 2.1), which could confuse readers. (Annotation ID: 6a023bfc)

**W10. Introduction paragraph 2 does not articulate the precise gap that prior methods leave open (Page 1 — Paragraph 2).** The transition from problem to solution would be strengthened by explicitly stating why SFT approaches fail to correct unsafe reasoning step-by-step. (Annotation ID: d653e403)

**W11. Reward shaping analogy in Section 3.4 is imprecise (Page 6 — Remark).** The potential-based shaping analogy breaks because the CSR-derived potential depends on the policy being optimized, violating the standard optimality-preservation guarantee. The paper should qualify this as an intuitive analogy rather than a formal equivalence. (Annotation ID: 1c116c01)

**W12. Conclusion speculates about multi-turn dialogue and agentic systems without supporting evidence (Page 9 — Section 6).** These extensions introduce fundamentally different safety challenges and are not evaluated anywhere in the paper. The claim should be qualified or removed. (Annotation ID: 1817753d)

**W13. Related Work section is a narrative listing rather than structured comparison (Page 9 — Section 5).** A comparison table organized by alignment target, supervision type, intervention mechanism, and external dependency would more clearly position IPO relative to existing methods. (Annotation ID: 0ee8f2bd)

### Page Coverage Audit

All substantive pages (1-9 in the provided manuscript) were covered with annotations:
- Page 0 (Abstract): 1 annotation
- Page 1 (Introduction through Page 8-9): 15 annotations across Introduction, Method, Experiments, Related Work, Conclusion
- The Appendix is not available in the provided manuscript (stated as "removed")

### Skipped Paragraphs
- Figure captions (Figures 1-7): non-substantive; covered by adjacent text annotations
- Table 2 data rows and Table 3: covered through experiment section annotations

## Score
**Final Score: 7/10**

*This score prioritizes research value and novelty as primary dimensions, consistent with the review policy.*

**Rationale:** The paper tackles a genuinely important and timely problem (unsafe intermediate reasoning in LRMs) with a well-motivated, empirically-grounded approach. The identification of safety triggers and compliance cues through CSR analysis is a solid conceptual contribution, and the IPO method demonstrates strong empirical results across multiple models and benchmarks. The paper is generally well-written, with clear motivation and thorough experimentation.

However, the score is reduced by several significant concerns:
1. **Potential DPO formulation issue (W2):** The non-standard DPO objective in Eq. (4) may contain an error or require justification; this directly affects the core training method.
2. **Missing statistical rigor (W3):** The lack of variance reporting and significance testing makes it difficult to assess the reliability of reported rankings.
3. **GPT-4o dependency and reproducibility (W4):** Heavy reliance on a commercial API without adequate specification limits reproducibility and introduces potential evaluation bias.
4. **Correlational vs causal reasoning claim (W1):** The central motivational claim needs stronger causal evidence.
5. **Baseline and efficiency comparison concerns (W5, W6):** The GRPO baseline and efficiency comparison may be unfair, potentially overstating IPO's advantage.

These concerns are addressable in revision, and the core contribution — process-level supervision through corrective intervention — is valuable enough to warrant publication after major revision addressing the DPO formulation, statistical reporting, and reproducibility.

**Note on novelty:** Due to Retrieval-Disabled Mode (external paper search unavailable), novelty assessment against the full literature is deferred. The paper's contribution relative to the described baselines (SafeChain, RealSafe, STAR, GRPO) appears solid, but a complete novelty evaluation requires manual literature verification.

---

### ASCII Diagrams

**A. ASCII Diagram — Paper Structure & Evidence Map**

```text
[Problem: Unsafe CoT reasoning in LRMs persists even when responses are safe]
    |
    v
[Empirical Motivation (Section 2.2): 
  - Existing aligned LRMs have higher reasoning harmfulness than response harmfulness
  - Safe reasoning correlates with safe responses]
    |
    v
[Limitation of RL (Section 2.3): 
  - GRPO with safety reward suffers from low rollout diversity
  - ~50% of prompts yield 0-1 safe trajectories
  - Sparse reward signals are insufficient]
    |
    v
[Empirical Insights (Sections 3.1-3.3):
  - Safety triggers: critical steps where safe continuation probability → 100%
  - Compliance cues: steps strongly correlated with unsafe turn (R=0.85)
  - Corrective intervention: replacing compliance cues with triggers reduces harm]
    |
    v
[IPO Method (Section 3.4):
  - Detect compliance cues via GPT-4o (80%+ agreement)
  - Replace with safety triggers from pool
  - Construct preference pairs diverging at critical step
  - Apply DPO on divergence segments]
    |
    v
[Evaluation (Section 4):
  - 3 models (DS-8B, DS-7B, Qwen3-8B)
  - 3 safety benchmarks (JBB, SR, WJ)
  - 4 reasoning benchmarks (AIME, MATH, GPQA, HEval)
  - Ablations on detector, training algorithm, efficiency]
    |
    v
[Claim: IPO reduces reasoning harmfulness by >30% relative while preserving reasoning capability]
```

**B. ASCII Diagram — Revision Strategy Roadmap**

```text
Priority 0 (Must fix — publication-critical):
  [W2: DPO Eq. (4) formulation] 
    -> Verify if π_θ(ẑ)/π_θ(z) is intentional or typo 
    -> If typo: correct to standard DPO, re-run experiments
    -> If intentional: add detailed justification + convergence analysis
    -> Expected impact: correct training objective
    
  [W3: Missing statistics]
    -> Add multi-seed results (mean ± std over ≥3 seeds)
    -> Add 95% bootstrap CIs for safety metrics
    -> Significance tests for key comparisons
    -> Expected impact: reliable ranking conclusions

Priority 1 (Major — should fix for acceptance):
  [W4: GPT-4o dependency]
    -> Specify exact GPT-4o version, prompts, temperature
    -> Add evaluation with open-source safety classifier
    -> Ablate detection quality (precision/recall, error analysis)
    -> Expected impact: reproducibility + bias assessment

  [W1: Causal claim]
    -> Add causal caveat in Section 2.2
    -> Cite forward to intervention experiments
    -> Expected impact: honest scope of motivational claim

Priority 2 (Minor — quality improvements):
  [W5: GRPO reward] -> Explain reward design, add ablation with I[z safe] only
  [W6: Efficiency comparison] -> Include end-to-end cost including GPT-4o APIs
  [W7: Detection accuracy] -> Add error analysis + confidence filtering
  [W8-W13] -> Textual revisions per annotations
```

**C. ASCII Diagram — Related-Work Taxonomy Tree (Layered)**

```text
Root: Safety Alignment for LRMs
│
├── Branch 1: Alignment Target
│   ├── Leaf 1.1: Response-only safety
│   │   └── Standard LLM alignment (SFT, DPO, RLHF)
│   ├── Leaf 1.2: Combined reasoning + response
│   │   └── SafeChain, RealSafe, STAR, SafeKey
│   └── Leaf 1.3: Reasoning-level primary (IPO)
│       └── IPO [THIS PAPER]
│
├── Branch 2: Supervision Signal
│   ├── Leaf 2.1: Supervised on curated CoT data
│   │   └── SafeChain, RealSafe, STAR
│   ├── Leaf 2.2: Outcome reward (RL)
│   │   └── GRPO with safety reward
│   └── Leaf 2.3: Process-level preference (IPO)
│       └── IPO: preference pairs at critical steps
│
├── Branch 3: Intervention Mechanism
│   ├── Leaf 3.1: None (passive dataset curation)
│   │   └── SFT-based methods
│   ├── Leaf 3.2: External monitoring/critique
│   │   └── BackTrack, TARS, CoT monitoring
│   └── Leaf 3.3: Corrective substitution (IPO)
│       └── Replace compliance cues with safety triggers
│
└── Branch 4: External Model Dependency
    ├── Leaf 4.1: Self-contained (no external API)
    │   └── SafeChain
    ├── Leaf 4.2: External detector/evaluator
    │   └── IPO (GPT-4o for detection + evaluation)
    └── Leaf 4.3: Larger model distillation
        └── RealSafe, STAR (distilled data)
```

**Value Contribution of IPO (positioning across branches):**
- IPO is unique in targeting reasoning-level safety as the *primary* alignment objective (Branch 1, Leaf 1.3).
- IPO introduces *process-level preference* supervision (Branch 2, Leaf 2.3), distinct from SFT or outcome RL.
- IPO uses *corrective substitution* of compliance cues (Branch 3, Leaf 3.3), which is more targeted than monitoring-based approaches.
- The main limitation is dependency on GPT-4o (Branch 4, Leaf 4.2), which should be addressed in future work.