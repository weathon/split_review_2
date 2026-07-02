## Summary
# Final Review Report

## Summary

This paper addresses the problem of plasticity loss in deep reinforcement learning — the gradual degradation of a neural network's ability to learn from new data during training. The authors develop a theoretical analysis attributing plasticity loss to two mechanisms: (1) rank collapse of the Neural Tangent Kernel (NTK) Gram matrix, and (2) $\Theta(1/k)$ decay of gradient magnitude caused by the non-stationarity of data distributions and bootstrapped targets in RL. Based on the gradient decay analysis (Theorem 3), they propose Sample Weight Decay (SWD), a method that assigns higher sampling probability to recent experiences in the replay buffer, aiming to counteract the $\frac{1}{k}$ attenuation of gradient contributions from new data.

Experiments across MuJoCo (TD3), ALE (Double DQN), and DeepMind Control Suite (SAC with SimBa architecture) show consistent improvements over base algorithms, with IQM gains of 13.7%–30.1%. The paper includes ablation studies with a reverse variant (SWA), plasticity quantification via GraMa metric, UTD robustness tests, and comparison with existing plasticity methods (ReGraMa, S&P, Plasticity Injection).

The paper makes a genuine contribution by providing a formal theoretical perspective on plasticity loss — an area that has been predominantly empirical. The gradient attenuation result is novel and the SWD method is simple yet effective. However, several weaknesses limit the current version: the NTK analysis remains conceptual rather than rigorous, the theoretical link between SWD and gradient compensation is asserted without formal derivation, the GraMa metric interpretation is contradictory as written, experimental comparisons lack statistical rigor, and the SOTA claims are not adequately bounded.

## Strengths
**1. Novel theoretical framing of plasticity loss.** The paper provides one of the first formal treatments connecting plasticity loss in RL to specific optimization-theoretic quantities — NTK Gram matrix rank and gradient magnitude decay rate. While the NTK discussion is high-level, the gradient attenuation analysis (Theorem 3) offers a concrete, falsifiable prediction ($\Theta(1/k)$ decay) that goes beyond the purely empirical observations prevalent in the literature. This theoretical framing is a meaningful step toward bridging the gap between empirical findings and principled understanding.

**2. Clean, practical algorithm design.** SWD is elegantly simple: age-based linear decay weighting of replay buffer samples. Unlike prior plasticity interventions that modify network architectures (ReDo, S&P, Plasticity Injection), SWD operates purely at the data level, making it algorithm-agnostic and easy to integrate into existing deep RL codebases. The method has only two hyperparameters ($T$ and $w_{\min}$), and the authors show low sensitivity to their values.

**3. Comprehensive empirical evaluation across diverse settings.** The experiments cover three algorithm families (TD3, Double DQN, SAC), three benchmark suites (MuJoCo, ALE, DMC), both continuous and discrete control, and multiple network architectures (MLP, CNN-MLP, SimBa). The consistent improvements across this varied landscape provide reasonable evidence that SWD is broadly applicable rather than narrowly tuned to a specific setting.

**4. Thoughtful ablation and analysis.** The reverse validation with SWA (assigning higher weights to older samples) is a clever experimental design that strengthens the causal narrative: if recency weighting is the mechanism, then anti-recency weighting should hurt performance, which is confirmed. The GraMa analysis further connects SWD to the plasticity loss mechanism directly, and the UTD robustness test addresses an important practical consideration about the method's behavior under frequent gradient updates.

**5. Orthogonality demonstration.** The SWD+S&P combination outperforming either method alone suggests genuine complementarity between data-level and architecture-level plasticity interventions. This opens a promising direction for composing plasticity-preserving techniques, even though the current validation is limited to one combination.

## Weaknesses
**1. [Major] NTK analysis is conceptual rather than rigorous (Page 1 - Section 4.1).** Section 4.1 consists of only two high-level paragraphs citing prior NTK convergence results and stating that "random initialization is violated in RL." No formal theorem, rank-degeneracy bound, or spectral analysis is provided for the NTK Gram matrix under the FQI update scheme. The paper claims a "unified theory" (Contribution C1) but the NTK mechanism — which constitutes half of the claimed theoretical contribution — lacks the technical depth needed to be considered a rigorous theoretical result. The overparameterization assumption required for NTK analysis is also unlikely to hold in the practical networks used in experiments. This limits the theoretical contribution to the gradient attenuation analysis (Theorem 3) alone.

**2. [Major] Theorem 3's gradient decomposition has notational and logical issues (Page 1 - Section 4.2).** 
- The term $\nabla f^2$ in the target-drift component is ambiguous: standard gradient of the squared Bellman residual is $2(f - \mathcal{T}\hat{f})\nabla f$, not $\nabla f^2$.
- The claim that setting $\hat{f}_{H+1}\equiv 0$ "eliminates the target-drift term entirely" is valid only at the terminal step $h=H$. For all intermediate layers $h<H$, the target $\mathcal{T}_h\hat{f}_{h+1}^k$ changes with $k$ because $\hat{f}_{h+1}^k$ is learned, so the drift term does not vanish. The paper overstates the generality of this cancellation.
- The derivation of the $\frac{1}{k}$ factor from the recursive buffer update (Proposition 1) is not shown in the main text — the gradient decomposition is presented as a theorem without a proof sketch, making it difficult to assess the reasoning.

**3. [Major] SWD's theoretical grounding is asserted rather than derived (Page 1 - Section 5).** The paper positions SWD as a "theoretically grounded" method (Contribution C2) that "neutralizes the $\frac{1}{k}$ attenuation," but no formal link is established between Theorem 3 and the SWD weighting scheme. Theorem 3 characterizes the gradient *at the initialization point* of each iteration, while SWD modifies the *sampling distribution* over the replay buffer. The paper does not prove that recency-weighted sampling actually compensates for the $\frac{1}{k}$ factor in the gradient expression. The connection is intuitive and plausible, but it remains a heuristic inspired by theory rather than a direct theoretical implication.

**4. [Major] Contradictory GraMa metric interpretation (Page 1 - Section 6.3).** Section 6.3 states "a larger GraMa value indicates a weaker learning capability of the neural network," yet the paper claims SWD is effective because it "maintains a higher GraMa value than SAC" (Figure 6). If higher GraMa = worse plasticity, then maintaining higher GraMa would be detrimental, not beneficial. This is either a critical error in the metric definition or a typographical error in the text. Either way, it fundamentally undermines the plasticity analysis in Section 6.3 and the GraMa-related conclusions. The same issue affects the ablation study results in Section 6.2 where GraMa is also referenced.

**5. [Major] Incomplete experimental rigor (Page 1 - Section 6.1).**
- Statistical significance is not formally tested. Improvements in several environments (Walker2d, Hopper) are within one standard deviation and could arise from random seed variation. The paper uses 95% stratified bootstrap CIs in aggregate plots but does not report them per-environment.
- PER comparison lacks wall-clock time data. The claim that PER "demands nearly several times more training time" is unquantified and unverifiable.
- The FQI-based theory is tested on TD3, SAC, and Double DQN, which differ substantially from FQI (policy gradients, entropy regularization, target networks). The transfer assumptions are not discussed in the main text.

**6. [Moderate] The strong SOTA claim is unsupported (Page 1 - Introduction).** The abstract and contribution list claim "achieving SOTA performance on challenging DMC Humanoid tasks." However, comparisons are limited to base algorithms (SAC, TD3, DDQN) and a few plasticity-specific methods (ReGraMa, S&P, Plasticity Injection). The paper does not compare against recent high-performing methods on DMC benchmarks (e.g., DrQ-v2, DMC-Alpha, model-based approaches). The performance improvements shown are consistent and meaningful, but the SOTA label is not justified by the comparison scope.

**7. [Moderate] Orthogonality claim lacks sufficient validation (Page 1 - Related Work).** The paper claims SWD is "orthogonal to existing methods" and "ensuring compatibility with existing plasticity-preserving techniques." However, only one combination (SWD+S&P) is tested. Compatibility with ReDo, Plasticity Injection, and other methods is asserted without evidence. The orthogonality claim is a hypothesis, not a validated finding.

**8. [Minor] Introduction overclaims and has tangential content (Page 1 - Introduction).** The opening paragraph mentions LLM post-training "for breaking the Turing test" — a hyperbolic and largely irrelevant framing for a paper about plasticity loss in RL. The introduction should directly motivate plasticity loss as a barrier to continual learning in RL, not invoke trending topics.

**9. [Minor] Conclusion and limitations are insufficiently specific (Page 1 - Section 7).** The limitations section mentions "computational constraints" and being the "tip of the iceberg," but does not acknowledge specific theoretical gaps: (a) NTK analysis is conceptual, (b) Theorem 3's clean result only holds at terminal layer, (c) SWD's theoretical link is asserted, (d) orthogonality was only tested for S&P. Acknowledging these would strengthen the paper's credibility.

**10. [Minor] Experimental design confound in SWA ablation (Page 1 - Section 6.2).** SWA (weighting older samples higher) simultaneously reduces gradient magnitude *and* shifts the training distribution toward outdated policies. The paper attributes poorer performance entirely to gradient attenuation, but distribution mismatch is a plausible alternative explanation. This confound is not acknowledged.

## Score
**Final Score: 6/10**

**Rationale:** The paper makes a genuine contribution by providing a formal theoretical perspective (gradient attenuation) on plasticity loss in RL and proposing a simple, empirically effective method (SWD). However, the overall score is moderated by several factors:

- **Research value and novelty (primary dimension):** The gradient attenuation analysis (Theorem 3) is novel and provides a testable prediction about plasticity loss. However, half of the claimed theoretical contribution (NTK rank collapse) is presented at a conceptual level without rigorous formalism, and the SWD method's theoretical grounding is asserted rather than formally derived. The overall novelty is genuine but more limited than the paper claims. **(6/10)**

- **Validity and soundness:** The experimental results consistently show improvement, which supports the empirical claims. However, the GraMa metric interpretation contradiction is a significant concern that needs resolution. Statistical rigor is incomplete (no significance tests, limited per-environment CIs). Several theoretical claims have logical gaps (Theorem 3 terminal-condition scope, NTK analysis depth). **(5/10)**

- **Reproducibility:** The SWD algorithm is clearly described, code is provided, and the method has only two hyperparameters with demonstrated low sensitivity. This is a strength. **(7/10)**

The paper has the potential to be a solid contribution to the RL community after addressing the identified weaknesses, particularly the GraMa contradiction, statistical rigor gaps, claim bounding, and theoretical overstatements.

```text
ASCII Diagram — Paper Structure & Evidence Map
================================================
[Problem: Plasticity loss in deep RL]
     |
     v
[Theoretical Analysis (Section 4)]
     |
     +--[NTK Degeneration (4.1)] -- conceptual only, no formal proof
     |      Evidence: references to Du et al. 2019, Allen-Zhu et al. 2019
     |      Gap: no rank-evolution analysis under FQI
     |
     +--[Gradient Attenuation (4.2)] -- Theorem 3, Θ(1/k) decay
            Evidence: gradient decomposition from recursive buffer
            Gap: terminal-condition scope, notation ambiguity ∇f²
     |
     v
[SWD Algorithm (Section 5)]
     |  Claim: neutralizes 1/k attenuation via recency weighting
     |  Gap: no formal proof linking weighting to gradient compensation
     v
[Experiments (Section 6)]
     |
     +-- Performance: consistent gains across TD3/DDQN/SAC
     |     Gap: no significance tests, PER timing unquantified
     |
     +-- Ablation: SWA confirms directionality
     |     Gap: distribution-mismatch confound unaddressed
     |
     +-- GraMa analysis: supports plasticity mechanism
     |     Issue: contradictory definition (higher=worse vs higher=better)
     |
     +-- UTD robustness: gains increase with UTD
     |     Gap: single environment, mechanism explanation heuristic
     |
     +-- Method comparison: SWD+S&P best on Humanoid Run
            Gap: single environment, limited combination scope
     |
     v
[Conclusion (Section 7)]
     Validated: gradient decay exists, SWD improves performance
     Limitations: generic, missing specific theoretical gaps
```

```text
ASCII Diagram — Related-Work Taxonomy Tree (Deferred)
======================================================
NOTE: External literature verification unavailable in this run
(paper_search not started due to missing API token).
Novelty/comparison conclusions are deferred for manual verification.

Expected taxonomy structure (to be validated):
Root: Plasticity Loss in Deep RL
├── Branch A: Architecture-Level Interventions
│   ├── Leaf A1: Neuron Recycling / ReDo [Sokar et al. 2023]
│   ├── Leaf A2: Network Reset [Nikishin et al. 2022]
│   ├── Leaf A3: Shrink & Perturb [Ash & Adams 2020]
│   └── Leaf A4: Plasticity Injection [Nikishin et al. 2023a]
├── Branch B: Gradient/Activation-Based Methods
│   ├── Leaf B1: ReGraMa / GraMa [Liu et al. 2025]
│   └── Leaf B2: Gradient-based Reset
├── Branch C: Data-Level Interventions ← THIS PAPER (SWD)
│   └── Leaf C1: Recency-weighted replay sampling [SWD]
└── Branch D: Empirical Studies
    └── Leaf D1: Plasticity loss characterization [Dohare et al. 2024,
                 Elsayed & Mahmood 2024, Nikishin et al. 2022]
```

**Novelty/Comparison Note:** Due to Retrieval-Disabled Mode (external paper search unavailable), all novelty and comparison conclusions in this review are based solely on manuscript evidence. A comprehensive literature verification is required before final publication decisions.

```text
ASCII Diagram — Revision Strategy Roadmap
==========================================
Priority 0 (Must fix before acceptance):
├── [GraMa contradiction] Clarify metric definition
│   → Check original GraMa paper (Liu et al. 2025)
│   → Correct Section 6.3: if higher GraMa = better, fix text; otherwise fix Figure 6 interpretation
│   → Expected impact: resolves an invalid conclusion
│
├── [Theorem 3 issues] Fix notation and scope
│   → Replace ∇f² with correct gradient expression
│   → Clarify that terminal-condition cancellation only applies at h=H
│   → Expected impact: restores theoretical credibility
│
├── [Statistical rigor] Add significance tests
│   → Report 95% CIs per environment (already done at aggregate level)
│   → Add multi-seed paired comparisons
│   → Expected impact: confirms improvement reliability
│
└── [SOTA/overclaiming] Bound all claims
    → Remove unqualified "SOTA" and "unified theory"
    → Replace with bounded claims scoped to evaluated settings
    → Expected impact: eliminates reviewer trust issues

Priority 1 (Major improvement):
├── [Theory-practice gap] Discuss transfer assumptions
│   → Clarify how FQI-derived results apply to TD3/SAC/DDQN
│   → Expected impact: strengthens theory-experiment alignment
│
├── [SWD theoretical link] Add formal connection
│   → Show how recency-weighted expectation compensates 1/k factor
│   → Or explicitly acknowledge heuristic status
│   → Expected impact: strengthens contribution C2
│
├── [PER comparison] Add wall-clock timing
│   → Report training time overhead for all methods
│   → Expected impact: substantiates efficiency claim
│
└── [Limitations] Add specific theoretical gaps
    → Acknowledge NTK conceptual nature, theorem scope, confound
    → Expected impact: demonstrates author awareness of boundaries

Priority 2 (Nice to have):
├── [Orthogonality] Test SWD+ReDo combination
├── [Method comparison] Add 2+ environments to Section 6.5
├── [SWA confound] Add distribution-matched control experiment
├── [NTK analysis] Provide spectral bound under FQI (if feasible)
└── [UTD mechanism] Formalize expected improvement scaling with R
```