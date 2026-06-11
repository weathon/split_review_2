## Summary
This paper presents EGG-SR, a unified framework that integrates symbolic equivalence into symbolic regression via equality graphs (e-graphs). The core idea is to leverage e-graphs to compactly represent equivalent syntactic variants of mathematical expressions and use these equivalence classes to improve the learning efficiency of three modern SR paradigms: Monte Carlo Tree Search (EGG-MCTS), Deep Reinforcement Learning (EGG-DRL), and Large Language Models (EGG-LLM). The authors provide theoretical analysis showing a tighter regret bound for EGG-MCTS and reduced gradient variance for EGG-DRL, and present experiments on trigonometric benchmarks and scientific datasets.

**Strengths:** The paper addresses a genuine and underexplored problem — redundancy in SR search spaces due to symbolic equivalence. The unified interface across MCTS, DRL, and LLM is well-motivated. The e-graph integration for backpropagation sharing in MCTS (via equivalence-aware transposition tables) is technically sound, and the space-efficiency analysis (Figure 4) convincingly demonstrates the scalability advantage of e-graphs over naive enumeration.

**Key Weaknesses:** (1) The abstract and introduction overclaim consistency of improvement — Table 1 shows cases where EGG variants underperform baselines (e.g., EGG-DRL noisy (4,4,6): 5.09 vs DRL 2.46), yet these failures are not discussed. (2) The theoretical contribution is heavily dependent on the existing Laurent & Maillard (2020) framework, with the novel component being the observation that EGG-MCTS fits their graph-merging analysis — this should be stated transparently. (3) The LLM experiments compare against previously published numbers without reproducing the baseline under identical conditions, introducing uncontrolled variance. (4) The EGG-DRL gradient estimator (Eq. 4) raises unresolved technical questions about unbiasedness of the log-sum gradient and the choice of baseline b'. (5) Several writing quality issues (vague assumptions, grammatical errors, self-promotional tone in conclusion) reduce scholarly polish.

**Conclusion:** EGG-SR represents a principled contribution to equivalence-aware symbolic regression. The core idea of sharing statistics across equivalent expressions is intuitive and the e-graph implementation is practical. However, the empirical claims need tighter bounding to match the actual experimental evidence, and several technical details require clarification or correction. With revisions addressing the overclaiming, experimental methodology, and theoretical exposition, this work could make a solid contribution to the SR community.

## Strengths
**S1. Well-motivated problem and intuitive solution.** The paper identifies a genuine inefficiency in modern symbolic regression: algorithms treat syntactically different but mathematically equivalent expressions as independent candidates, wasting computational resources. The solution — using e-graphs to compactly represent equivalence classes and sharing statistics across equivalent expressions — is conceptually clean and well-justified.

**S2. Unified framework across multiple SR paradigms.** Rather than focusing on a single algorithm class, EGG-SR provides a modular integration for MCTS (via equivalence-aware backpropagation), DRL (via modified policy gradient), and LLM (via enriched feedback prompts). This breadth strengthens the paper's practical relevance and demonstrates that the equivalence-aware learning idea is general, not tied to one specific algorithmic choice.

**S3. Space-efficiency demonstration (Figure 4).** The memory consumption benchmarks for log-product and sine-sum identities convincingly show that e-graphs achieve exponential space savings over naive array-based enumeration. This directly addresses the scalability challenge stated in the motivation and validates a key practical claim.

**S4. Theoretical grounding for MCTS and DRL.** The paper provides formal regret-bound and variance-reduction theorems, which are rare in the symbolic regression literature. Even though the MCTS result heavily builds on Laurent & Maillard (2020), the framing in terms of symbolic equivalence is novel and the variance-reduction result for DRL offers a testable prediction.

**S5. Time efficiency evidence (Figure 5).** The runtime breakdown in Figure 5 shows that EGG construction overhead is negligible compared to coefficient fitting and neural network updates, addressing a natural concern about the practicality of adding e-graph computations to the training loop.

## Weaknesses
### W1. Empirical claims are inconsistent with Table 1 data (Major)

**Evidence:** Page 8 - Table 1 (Trigonometric benchmarks). The abstract claims EGG-SR "consistently enhances" SR methods. The introduction states "EGG consistently improves performance across diverse frameworks." However, Table 1 shows clear counterexamples:

- **EGG-DRL, noisy (4,4,6):** NMSE 5.09 vs DRL 2.46. EGG-DRL is 2.07x worse.
- **EGG-MCTS, noisy (3,2,2):** NMSE 0.012 vs MCTS 0.007. EGG-MCTS is 1.71x worse.
- **EGG-DRL, noiseless (4,4,6):** NMSE 2.381 vs DRL 2.990. EGG-DRL is better, but only marginally (~20% relative).
- **EGG-LLM (Mistral), Bacterial growth IID:** 0.0101 vs LLM-SR (Mistral) 0.0026. EGG-LLM is 3.88x worse.

**Root cause:** The paper's framing relies on the assumption that equivalent expressions produce identical rewards. In noisy settings, coefficient fitting via BFGS converges to different local optima for different syntactic forms, breaking this assumption. When rewards differ across equivalent forms, EGG's backpropagation in MCTS may propagate incorrect statistics, and the DRL gradient estimator may be based on mismatched reward-probability groupings. The paper does not analyze these failure modes.

**Required action (Must):** (a) Replace "consistently enhances" with bounded language throughout the paper. (b) Add a dedicated paragraph analyzing cases where EGG underperforms. (c) Discuss the assumption that equivalent expressions must have identical rewards and how noise violates it. (d) Report per-instance results (not just median) to show variability. (e) Consider a noise-sensitivity experiment to determine the noise level at which EGG becomes detrimental.

### W2. LLM experiment compares against published numbers without baseline reproduction (Major)

**Evidence:** Page 8 - Table 2 and text: "The result of LLM-SR directly uses the reported result in Shojaee et al. (2025)." The EGG-LLM numbers are from the authors' own runs, but the baseline is copied from a prior paper without re-execution.

**Root cause:** LLM outputs depend on API version, prompt details (which differ between the original paper and EGG-LLM due to equivalence-enriched prompts), temperature, random seed, and sampling parameters. The observed improvements are often tiny (e.g., 0.0004 vs 0.0005 for Oscillation I OOD). Without running both methods under identical conditions, the claimed improvement cannot be attributed to the EGG module rather than random variation or API drift.

**Required action (Must):** Re-run the LLM-SR baseline under exactly the same conditions as EGG-LLM (same API version, temperature=0 or identical seeds, same prompt structure except for equivalence augmentation). Report results over at least 3-5 independent trials with mean and standard deviation. If re-running is not feasible, downgrade claims to "preliminary evidence" with explicit caveats.

### W3. Theoretical contribution: Theorem 3.1 heavily relies on prior framework; novelty is the mapping, not the bound itself (Major)

**Evidence:** Page 6 - Section 3.4. Proof sketch states: "Laurent & Maillard (2020) analyze MCTS on a graph obtained by merging identical tree nodes... Our final results follow their regret analysis on the unrolled tree." The paper's contribution is essentially observing that EGG-MCTS instantiates the graph merging assumptions of Laurent & Maillard.

**Root cause:** The paper does not clearly demarcate which parts of the theoretical analysis are inherited and which are novel. The key quantity kappa_infty (effective branching factor) is stated to satisfy kappa_infty <= kappa, but no proof or even intuitive justification is given in the main text — it depends on appendix definitions that are not summarized.

**Required action (Must):** Clearly state what is novel: (a) the mapping of e-graph-based equivalence detection onto the Laurent & Maillard graph-merging framework, and (b) the specific form of the effective branching factor reduction under symbolic equivalence. Provide an intuitive explanation of when kappa_infty < kappa holds and when it does not (operator sets with few identities). Ensure the appendix proof is complete and self-contained.

### W4. EGG-DRL gradient estimator (Eq. 4) has unresolved technical issues (Verification needed)

**Evidence:** Page 5 - Equations (3)-(4). The EGG-DRL estimator replaces `nabla_theta log p_theta(tau_i)` with `nabla_theta log [sum_k p_theta(tau_i^(k))]`. 

**Root cause issues:** 
(a) The gradient of log-sum is not equal to the average of per-sequence gradients: `grad log(sum p_k) = (sum grad p_k) / (sum p_k)`, which differs from `(1/K) sum grad log p_k`. The unbiasedness claim relative to the standard estimator needs careful proof not provided in the sketch.
(b) The baseline b' in Eq. (4) is not defined. It presumably differs from the standard baseline b in Eq. (3) because the gradient structure is different, but no guidance is given on estimation.
(c) The reward-sharing assumption (all K sequences have identical reward) may fail in practice due to coefficient fitting variance, as noted in W1.

**Required action (Must):** (a) Provide a step-by-step unbiasedness derivation showing E[g_egg(theta)] = E[g(theta)]. (b) Define b' explicitly and explain its estimation procedure. (c) Qualify the assumption that equivalent sequences share identical rewards and discuss practical violations.

### W5. Missing experimental details and statistical rigor (Major)

**Evidence:** Page 7-8 - Experiments section. (a) No standard deviations or confidence intervals reported for Table 1 — only median NMSE. (b) No information on number of independent trials/seeds per experiment. (c) No description of baseline hyperparameter tuning or whether baselines received the same compute budget as EGG-enhanced versions. (d) The MCTS search tree size plot (Figure 3 left) shows EGG-MCTS explores larger trees, but is larger always better? The paper does not discuss this.

**Required action (Must):** (a) Report mean +/- std over at least 3 seeds for all experiments. (b) Clearly state the compute budget (wall time, iterations, or expression evaluations) for each method. (c) Add a paragraph discussing whether larger search trees in EGG-MCTS correspond to more effective exploration or just slower convergence per-iteration due to overhead. (d) Include noise-level sensitivity analysis.

### W6. Overclaiming and writing quality issues (Minor-Major)

**Evidence:** 
- Page 0 - Abstract: "consistently enhances across several benchmarks" contradicts Table 1.
- Page 1 - Introduction: "Under mild theoretical assumptions" — assumptions not stated in main text.
- Page 1 - Contribution paragraph: "using EGG than without" — grammatical error.
- Page 9 - Conclusion: "more sophisticated solver" — unnecessary self-promotional phrasing.
- Page 1 - Related Work: "orthogonal to existing approaches" — asserted without justification.

**Required action (Must for overclaims, Nice-to-have for wording):** Fix the grammatical error. Replace "mild theoretical assumptions" with explicit statements. Revise the abstract and conclusion to accurately reflect the empirical scope. Explain the "orthogonal" claim or replace with a precise description of complementarity.

### W7. Grammar specification is underspecified for reproducibility (Minor)

**Evidence:** Page 1 - Section 2 Preliminaries. The context-free grammar uses a single non-terminal V = {A}, but the production rule set R is not listed in the main text. The coefficient indexing mechanism is described only informally.

**Required action (Nice-to-have):** List the production rule set in the main text (or a representative subset). Clarify coefficient indexing rules and maximum number of coefficients.

### W8. Novelty assessment deferred due to external retrieval unavailability (Deferred)

External paper search was not functional in this run (missing API token). A complete novelty evaluation requires manual literature verification against prior work on e-graphs in symbolic regression (de França & Kronberger 2023, 2025), transposition tables in MCTS (Childs et al. 2008, Leurent & Maillard 2020), and equivalence-aware learning in DRL and LLMs. The paper's contribution appears to be the unified framework and the specific integration patterns, but a definitive novelty verdict cannot be rendered without external evidence. **This is flagged for manual verification by the program chairs or meta-reviewer.**

## Score
**Final Score: 5/10**

**Rationale:** The paper proposes a well-motivated idea (equivalence-aware learning via e-graphs) with a unified framework across three SR paradigms. However, the score is constrained by the following factors that materially affect research value and validity:

1. **Overclaiming vs. evidence mismatch (Score cap: -2.0).** The abstract and introduction claim "consistently enhances" performance, but Table 1 contains counterexamples where EGG variants underperform baselines (noisy (3,2,2), (4,4,6)). This reduces confidence in the authors' objectivity and requires major revisions to claim boundaries.

2. **Theoretical contribution partly inherited (Score cap: -1.0).** Theorem 3.1 is essentially an application of Laurent & Maillard (2020)'s existing framework, with the novelty being the mapping observation. While this mapping is non-trivial, the paper's framing overstates the theoretical novelty. The EGG-DRL estimator (Theorem 3.2) has unresolved technical issues regarding unbiasedness.

3. **LLM experimental methodology (Score cap: -1.0).** Comparing against published numbers without re-running the baseline is not reproducible and does not support the claimed improvements.

4. **Missing statistical rigor (-1.0).** No variance reporting, unclear number of trials, and no discussion of when EGG helps vs. hurts.

5. **Novelty cannot be fully assessed (-0.5).** External literature verification was not available in this run. A manual check against prior e-graph + SR work (de França & Kronberger line) is needed.

The core idea has merit and with revisions addressing these weaknesses — particularly bounding the empirical claims, re-running the LLM baseline, clarifying the theoretical contributions, and adding failure-case analysis — the paper could be improved to the 7/10 range.

---

### ASCII Diagrams

**ASCII Diagram A — Paper Structure & Evidence Map**

```text
[Claim: Symbolic equivalence accelerates SR learning]
    ├── [C1: Unified EGG framework for MCTS/DRL/LLM]
    │       └── Evidence: Table 1 (mixed, some improvements, some regressions)
    ├── [C2: EGG-MCTS has tighter regret bound]
    │       └── Evidence: Theorem 3.1 (inherited from Laurent & Maillard 2020)
    │       └── Gap: kappa_infty <= kappa not proven in main text
    ├── [C3: EGG-DRL has lower-variance gradient]
    │       └── Evidence: Theorem 3.2 (unbiasedness claim needs verification)
    │       └── Gap: b' undefined, log-sum gradient equality unproven
    ├── [C4: EGG is space/time efficient]
    │       └── Evidence: Figure 4 (space), Figure 5 (time) — strong
    └── [C5: EGG improves LLM-based SR]
            └── Evidence: Table 2 (baseline not reproduced — weak)
```

**ASCII Diagram B — Revision Strategy Roadmap**

```text
Priority  | Revision Action                     | Expected Impact
P0 (Must) | Bound claims per Table 1 evidence    | Restores credibility
P0 (Must) | Re-run LLM baseline + add variance   | Validates LLM claims
P0 (Must) | Fix Eq (4) derivation + define b'    | Establishes theory
P1 (Must) | Add failure analysis (noise cases)   | Completes empirical picture
P1 (Must) | State kappa_infty bound intuition    | Clarifies theory contribution
P2 (Nice) | Production rule listing in main text | Improves reproducibility
P2 (Nice) | Remove "more sophisticated" wording  | Scholarly tone
P2 (Nice) | Add noise sensitivity experiment     | Strengthens robustness
```

**ASCII Diagram C — Related-Work Taxonomy Tree (Layered)**

```text
Symbolic Regression (Root)
├── Branch 1: Search Paradigm
│   ├── Leaf 1.1: Genetic Programming (GP) [de França & Kronberger 2023, 2025]
│   ├── Leaf 1.2: MCTS-based [Sun et al. 2023; Ruan et al. 2025]
│   └── Leaf 1.3: DRL-based [Petersen et al. 2021; Landajuela et al. 2022]
│   └── Leaf 1.4: LLM-based [Shojaee et al. 2025; Zhang et al. 2025]
├── Branch 2: Knowledge-Guided Discovery
│   ├── Leaf 2.1: Physical knowledge [AI-Feynman: Udrescu & Tegmark 2020]
│   ├── Leaf 2.2: Unit constraints [Tenachi et al. 2023]
│   └── Leaf 2.3: User-specified prior [Bendinelli et al. 2023]
├── Branch 3: Equivalence-Aware Methods
│   ├── Leaf 3.1: E-graph for GP simplification [de França & Kronberger 2023]
│   ├── Leaf 3.2: E-graph for GP duplicate detection [de França & Kronberger 2025]
│   ├── Leaf 3.3: Transposition tables in MCTS [Childs et al. 2008; Leurent & Maillard 2020]
│   └── Leaf 3.4: EGG-SR (This paper) — unified framework for MCTS/DRL/LLM
├── Branch 4: Alternative Representations
│   ├── Leaf 4.1: SymNet layer-wise networks [Sahoo et al. 2018; Li et al. 2024]
│   └── Leaf 4.2: Transformer end-to-end [Kamienny et al. 2022; Shojaee et al. 2023]
```

**Note on Novelty:** The paper positions itself in Branch 3, Leaf 3.4. The primary differentiator from Leaves 3.1-3.2 (de França & Kronberger) is the focus on embedding equivalence into the *learning loop* of non-GP SR algorithms, rather than post-hoc simplification or duplicate detection. The theoretical analysis connects to Leaf 3.3 (transposition tables) by generalizing node identity to symbolic equivalence. A thorough novelty verdict requires external literature verification (deferred).

---

**Post-Revision Target: [6, 8]/10** — achievable if the Must actions (W1, W2, W3, W4, W5) are completed, the claims are properly bounded, and external novelty verification confirms the differentiation from prior e-graph + SR work.