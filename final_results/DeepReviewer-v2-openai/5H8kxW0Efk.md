## Summary
**External literature verification unavailable in this run (Retrieval-Disabled Mode); novelty/comparison conclusions are intentionally deferred to manual verification.**

## Summary

This paper proposes NPIM (Neural-network Parameterized Ising Machine), which applies algorithm unrolling to dynamical Ising machines for the NP-hard Ising/Max-Cut combinatorial optimization problem. The key idea is to replace the handcrafted update rule of an Ising machine with a small MLP whose parameters are trained via zeroth-order evolutionary optimization, bypassing the vanishing-gradient and reward-attribution problems of backpropagation and policy-gradient methods. Two variants are introduced: cNPIM (continuous coupling) and dNPIM (discrete coupling via sign thresholding).

The paper demonstrates that:
- Learned dynamics can emerge from scratch on small SK instances (N=100), including momentum-like behavior that improves escape from local minima.
- On G-set Max-Cut benchmarks, dNPIM achieves lower median time-to-solution than CAC, CFC, and dSBM on 4 of 5 instance groups.
- On neural CO benchmarks (MIS, MaxClique, MaxCut), dNPIM achieves higher objective values than diffusion-based methods on 4 of 5 problem classes, though at higher computation time for large graphs.

The work sits at the intersection of neural combinatorial optimization, algorithm unrolling, and physics-inspired Ising machines. While the combination of these ideas is novel, several methodological and empirical concerns (comparison fairness, bootstrapping limitations, statistical reporting quality) must be addressed before the claimed performance advantages can be fully validated.

```text
ASCII Diagram — Paper Structure & Evidence Map

[Problem: NP-hard Ising/Max-Cut] -> [Gap: Handcrafted Ising machine dynamics require
                                    extensive tuning and lack theoretical understanding]
 -> [Solution: Parameterize update step as MLP, train via zeroth-order ES (NPIM)]
 -> [Evidence: Section 4.1: momentum emergence; Section 4.2-4.3: architecture scaling
     and bootstrapping; Section 5: benchmark comparisons]
 -> [Risks: Comparison fairness (top-30 vs mean), bootstrapping requirement,
     sparse-vs-dense implementation confound, no variance reporting]
 -> [Conclusion: Promising proof-of-concept requiring fairer evaluation and
     broader validation]
```

## Strengths
**1. Novel conceptual integration.** The paper's core idea — applying algorithm unrolling to dynamical Ising machines and training via zeroth-order optimization — is a genuinely novel combination. It bridges the physics-inspired Ising machine literature (CIM, SBM, CAC) with the learning-to-optimize paradigm in a non-trivial way. Unlike most neural CO methods that use GNNs, GFlowNets, or diffusion models, NPIM parameterizes the iterative dynamics themselves, resulting in a very compact model (as few as 10–100 parameters) that can generalize across problem sizes.

**2. Honest and informative failure analysis.** The paper candidly discusses important limitations: (a) cNPIM suffers from instance-level overfitting where some hard instances are never solved; (b) training from scratch on large problems is not possible, requiring bootstrapping from smaller instances; (c) the method underperforms on planar unweighted G-set graphs. This level of transparency is rare and valuable for the community.

**3. Interesting emergent dynamics.** Section 4.1's demonstration that training solely to maximize reward causes the network to learn momentum-like dynamics (positive weights in the temporal filter) is a compelling finding. It suggests that the optimizer discovers a physically meaningful search strategy without any explicit inductive bias for momentum, which speaks to the potential of data-driven algorithm design.

**4. Thorough benchmarking across two communities.** The paper evaluates against both neural CO baselines (DiffUCO, SDDS, Gurobi) and Ising machine baselines (CAC, CFC, dSBM) on problem instances from both literatures (BA graphs, G-set, SK models, WPE). This dual-community benchmarking is a strength that helps position the work clearly.

**5. Computational efficiency per trajectory.** As noted, each NPIM trajectory is computationally lightweight (simple MLP forward pass), making it suitable for parallel multi-trajectory execution. The "top 30" strategy, while methodologically problematic for comparison, does demonstrate practical parallelism potential.

## Weaknesses
The weaknesses are ordered by severity and impact on the paper's validity and conclusions.

### 1. Unfair comparison methodology in neural CO benchmarks (MAJOR)

In Table 1, dNPIM reports "top 30" (maximum over 30 independent trajectories) while baselines (DiffUCO, SDDS) report mean ± std over multiple runs. Taking the maximum over N runs is an order statistic that grows with N and is systematically larger than the mean. This makes the claimed advantage in "four out of five cases" potentially an artifact of evaluation protocol rather than genuine algorithmic superiority. Furthermore, dNPIM results are reported without variance, preventing statistical significance assessment. On large graphs, dNPIM takes 1:20 vs 0:03 for baselines (27× slower), an unresolved confound attributed to "dense PyTorch matrix-matrix product" without controlled verification.

**Fix:** Report dNPIM as mean ± std over ≥3 training seeds using the same evaluation protocol as baselines. Provide significance tests. Run a sparse-implementation ablation to isolate the algorithmic vs implementation component of runtime.

### 2. Claim-evidence mismatch in Conclusion and Abstract (MAJOR)

The conclusion states the method "can achieve state-of-the-art performance on commonly used benchmarks" without caveating: (a) the comparison fairness concern above, (b) the failure on planar G-set graphs (Table 2, P,+ group: dNPIM TTS 4.42e07 vs CAC 1.81e06 — 24× worse), and (c) the bootstrapping requirement that limits practical applicability. The abstract similarly uses "competitive performance" without specifying bounds.

**Fix:** Replace "state-of-the-art" with scoped claims (e.g., "achieves lower TTS than CAC on 4 of 5 G-set groups" and "achieves higher objective than diffusion-based neural CO methods on 4 of 5 benchmarks"). Acknowledge the planar-graph limitation explicitly in the abstract.

### 3. Statistical and variance reporting gap (MAJOR)

Across all experiments, the paper does not report:
- Standard deviations or confidence intervals for dNPIM's main results.
- Number of independent training runs/seeds.
- Statistical significance tests for performance comparisons.
- Instance-level variance analysis (e.g., violin plots or scatter plots with summary statistics beyond median).

Without these, readers cannot assess whether observed gains are reproducible or within noise. This is especially concerning given that the cNPIM overfitting analysis (Section 4.5) shows extreme instance-level variance — some hard instances are never solved.

**Fix:** (Must) Report mean ± std over ≥3 training seeds for all main results. (Must) Add a paired comparison test (e.g., Wilcoxon signed-rank) for dNPIM vs CAC TTS on G-set instances.

### 4. Insufficient novelty positioning and literature comparison (MAJOR)

The novelty claim "algorithm unrolling has not been explored for NP-hard combinatorial optimization with the exception of ILP" (Section 2.3) is a strong statement that requires thorough literature verification. Given that Retrieval-Disabled Mode prevents external paper search in this run, this claim cannot be validated here and is flagged for mandatory manual verification. Additionally, the paper does not clearly distinguish its zeroth-order approach from prior evolutionary methods for CO hyperparameter tuning. The contribution section (2.5) lists an experimental finding (C3: "effective dynamics can be learned from scratch") as a methodological claim, which conflates discovery with invention.

**Fix:** Distinguish methodological contributions from empirical findings. Add "to the best of our knowledge" qualifiers where appropriate. Provide a clear table contrasting NPIM's assumptions and training protocol against the nearest neural CO and Ising machine works.

### 5. Bootstrapping is a practical bottleneck (MODERATE)

Section 4.3 states "training the network from scratch at the larger problem size (N = 500) is not possible." The method requires a pre-existing easy-instance distribution for pretraining. For problem classes where such a natural easy-to-hard curriculum does not exist, the method cannot be applied. This is a significant practical limitation that is under-discussed.

**Fix:** (a) Characterize when bootstrapping succeeds/fails more formally. (b) Ablate whether curriculum learning on instance hardness can replace the separate easy→hard transfer. (c) Discuss implications for problems without clear hardness graduations.

### 6. Notation and formula clarity issues (MODERATE)

Eq. (5) does not explicitly state that the MLP parameters are shared across all N spins (a crucial detail for scalability). The noise term $W^0(t)\eta$ with $W^0 \in \mathbb{R}^{1\times1}$ and scalar $\eta$ is ambiguous — is noise independent per spin or identical across all spins? The paper states "we do not include bias parameters" for odd symmetry but does not verify whether the resulting MLP strictly satisfies $F(-x) = -F(x)$ given the tanh outer activation and no biases.

**Fix:** Add explicit per-spin index to Eq. (5). Clarify noise sampling. Provide a proof or empirical verification of the odd-symmetry property.

### 7. cNPIM/dNPIM overfitting analysis is speculative (MINOR)

The explanation that cNPIM "learns to optimize some relaxed version of the underlying discrete Ising problem" is intuitive but unsupported by quantitative evidence. No correlation is shown between the continuous relaxation gap and instance hardness.

**Fix:** Add a quantitative analysis correlating relaxation gap with TTS ratio per instance, as suggested in the annotation on Section 4.5.

### 8. Writing quality issues (MINOR)

Several grammatical errors and awkward phrasings reduce professional polish: "an recent" (should be "a recent"), "closely related an recent line" (missing preposition), "data-driven matter" (should be "data-driven manner"), "adapted provide" (missing "to"). The Introduction is written as a single dense paragraph exceeding 15 sentences, violating the one-paragraph-one-role principle.

**Fix:** Proofread thoroughly. Split Introduction into 3 paragraphs as suggested in the Introduction annotation.

```text
ASCII Diagram — Revision Strategy Roadmap

[Top Priority: Fix comparison fairness]
 -> [Add variance reporting, use same evaluation protocol]
 -> [Expected: fairer benchmarking, lower but more credible advantage]
 -> [Affected sections: Section 5, Table 1, Conclusion, Abstract]

[High Priority: Tighten novelty claims]
 -> [Distinguish C1/C2 (methodological) from C3 (empirical)]
 -> [Add explicit scope boundaries to each claim]
 -> [Affected: Section 2.5, Abstract, Conclusion]

[Medium Priority: Address bootstrapping limitation]
 -> [Characterize conditions for successful easy→hard transfer]
 -> [Discuss alternative training strategies]
 -> [Affected: Section 4.3, Conclusion]

[Lower Priority: Formula clarifications]
 -> [Fix Eq. (5) indexing, clarify noise/symmetry]
 -> [Affected: Section 3.3]

[Polish: Split Introduction into 3 paragraphs, proofread]
 -> [Affected: Section 1]
```

```text
ASCII Diagram — Related-Work Taxonomy Tree (Layered)

Related Work: Neural Combinatorial Optimization & Ising Machines (Root)
├── Branch 1: Neural CO Methods
│   ├── Leaf 1.1: Autoregressive / RL-based (Pointer Nets, Transformer)
│   ├── Leaf 1.2: GNN-based one-shot prediction (Schuetz et al., 2022)
│   ├── Leaf 1.3: GFlowNet / generative policy (Zhang et al., 2023)
│   └── Leaf 1.4: Diffusion-based samplers (Sanokowski et al., 2024; 2025)
│       └── Key gap: All use backprop/policy-gradient → gradient/reward issues
├── Branch 2: Physics-Inspired Ising Machines
│   ├── Leaf 2.1: Physical-device-based (CIM, AIM, OIM)
│   ├── Leaf 2.2: Simulated dynamics (SBM, CAC)
│   │   └── Key gap: Handcrafted dynamics, hyperparameter tuning per class
│   └── Leaf 2.3: Algorithm-unrolled (ILP unrolling, Chen et al., 2024)
│       └── Key gap: Prior unrolling limited to linear/convex or ILP
└── Branch 3: This Work (NPIM)
    ├── Mechanism: MLP-parameterized Ising machine update
    ├── Training: Zeroth-order evolutionary optimization
    └── Value: Learns dynamics from scratch, compact model,
                competitive on 4/5 G-set groups and neural CO benchmarks
```

## Score
**Final Score: 6/10**

**Rationale:** This score balances the paper's genuine novelty in integrating algorithm unrolling with Ising machines against significant concerns about comparison fairness, statistical rigor, and claim-evidence alignment.

**Supporting the positive side (+):**
- The core idea (MLP-parameterized Ising machine trained via zeroth-order optimization) is original and technically sound.
- The paper demonstrates interesting emergent dynamics (momentum) that suggest the potential of data-driven algorithm design.
- Results on G-set benchmarks are competitive when taken at face value.
- The paper is transparent about several limitations (bootstrapping, planar-graph failure, cNPIM overfitting).

**Constraining the score (-):**
- The unfair comparison methodology (top-30 vs mean for baselines) undermines the headline performance claims and requires substantial revision before the results can be trusted.
- The absence of variance reporting and statistical tests makes it impossible to assess reproducibility.
- The conclusion overclaims SOTA status without the necessary caveats.
- Novelty positioning against related work cannot be fully verified in this run (Retrieval-Disabled Mode), and at least one claim ("algorithm unrolling not explored for NP-hard CO") is a strong statement requiring literature confirmation.
- The bootstrapping requirement limits practical applicability in a way that is under-discussed.

**Verification note (Retrieval-Disabled Mode):** All novelty and comparison conclusions in this review are marked as deferred manual verification because external literature search was unavailable in this run. The scores and judgments above are based solely on internal manuscript evidence and methodological consistency. A manual literature check is strongly recommended before final acceptance decisions.