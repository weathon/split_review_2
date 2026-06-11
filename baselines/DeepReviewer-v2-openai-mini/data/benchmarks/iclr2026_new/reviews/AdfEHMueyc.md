## Summary
# Final Review Report

## Summary

This paper presents a co-design algorithm for soft robots that integrates Graph Attention Network (GAT)-based policies with deep reinforcement learning (PPO) to enable morphology-aware controller inheritance across generations. The key idea is to represent each robot as a graph, use a GAT to encode node features into a pooled representation, and pass it through a lightweight MLP head for actuator control. When morphology changes (via GA-based mutation), a topology-consistent weight mapping procedure (MAPWEIGHTS) transfers shared GAT layers intact, copies matched actuator weights, and randomly initializes new ones. Experiments on four EvoGym tasks (Pusher-v1, Thrower-v0, Carrier-v1, Catcher-v0) show that the GAT-based variants generally achieve higher final fitness and lower variance than MLP-only baselines (with and without inheritance). The paper addresses a genuine challenge in embodied intelligence—controller reuse under morphological change—and the GAT-based approach is methodologically sound. However, the work has several limitations: missing reproducibility-critical hyperparameters, no statistical significance testing, a pseudocode error in Algorithm 1, and limited novelty differentiation from prior graph-based policy work. The paper would benefit from tightened claims, a fully reproducible experimental appendix, and a more structured related-work positioning.

## Strengths
1. **Addresses a well-motivated, important problem.** The core challenge—controller inheritance under morphological change—is a genuine bottleneck in evolutionary robotics and embodied intelligence. The paper clearly articulates why fixed-architecture MLP policies break when sensor/actuator layouts change, and why a graph-based representation is a natural solution.

2. **Clean technical approach.** The GAT-based policy with MAPWEIGHTS inheritance (Algorithm 2) is intuitive and well-designed. Representing robots as graphs, sharing GAT layers across generations, and handling actuator additions/removals via correspondence mapping is a principled way to achieve morphology-aware policy transfer.

3. **Standardized benchmark (EvoGym).** Using the EvoGym platform with four tasks of varying difficulty (Pusher, Thrower, Carrier, Catcher) provides a fair and reproducible evaluation setting. This is a significant improvement over custom simulation setups used in earlier co-design work.

4. **Thoughtful comparison of global vs. local node features.** Investigating two GAT variants (global mean representation vs. individualized local features) adds insight into when each design is beneficial—local for fine-grained coordination tasks, global for whole-body synchronization tasks. This analysis goes beyond a simple GAT-vs-MLP comparison.

5. **Honest limitation disclosure.** The Conclusion acknowledges that GAT controllers converge more slowly than MLPs and that newly added nodes cause temporary instability. This self-critical reflection increases confidence in the authors' understanding of their method's boundaries.

6. **Ablation by comparison.** Although the paper does not run component-level ablations, the four-way comparison (GAT-global-transfer, GAT-local-transfer, MLP-transfer, MLP-scratch) provides a clear picture of additive benefits from both graph architecture and inheritance, even though these factors are not fully disentangled.

## Weaknesses
### W1. Reproducibility: Critical hyperparameters are missing (Major)
The paper does not self-report PPO and GA hyperparameters (learning rate, discount factor, GAE lambda, clip epsilon, PPO epochs, mini-batch size, population size p, elite count m, mutation operators/rates). Instead, it references external papers (Kostrikov, 2018; Harada & Iba, 2024; Bhatia et al., 2021) for these settings. This forces readers to consult three separate publications to understand the experimental configuration. A self-contained hyperparameter table is essential for reproducibility.

**Required action:** Add a dedicated hyperparameter table (main text or appendix) listing all PPO and GA parameters, as well as compute hardware and runtime.

### W2. Algorithm 1 contains a pseudocode error and missing details (Major)
Line 2 of Algorithm 1 reads "for g = 1 ... p" but the specification requires max generations n (p is population size). This is a variable-name inconsistency that would confuse implementers. Additionally, the algorithm omits: (a) how the elite count m is determined, (b) how parents are selected among elites (uniform? fitness-proportional?), (c) the mutation operator details (add/remove voxel, rates), and (d) the PPO training budget per newborn morphology.

**Required action:** Fix line 2 to use n. Add a paragraph specifying elite selection mechanism, mutation operators and rates, and per-morphology training horizon.

### W3. Statistical significance is not established (Major)
All comparisons are based on mean fitness over 3 seeds with standard deviation shading. No statistical tests (t-test, Mann-Whitney, bootstrap) are reported. Given that only 3 trials are used, the observed differences could be influenced by random seed variation. On Carrier-v1, "all methods reach similar high fitness" — the paper treats this as a robustness advantage rather than discussing the possibility of task saturation, which would weaken generalizability claims.

**Required action:** Add significance tests comparing best GAT variant vs. best MLP baseline per task. Report effect sizes. For Carrier-v1, discuss whether task saturation explains the null result.

### W4. GAT architecture is underspecified (Major)
The method description mentions "a GAT layer" (singular) but does not specify: number of attention heads, hidden dimensions per head, activation functions, number of MLP hidden layers and their sizes, dropout, normalization, or the exact node feature vector composition. The paper states node features combine "global properties (e.g., orientation)" with "local information (e.g., coordinates, voxel type, and velocity)" without giving exact dimensionality or encoding scheme. This makes the method impossible to reproduce independently.

**Required action:** Provide a complete architecture specification: GAT layers, heads, hidden sizes, activations, feature vector definition with dimensions, and MLP head architecture in a dedicated table or subsection.

### W5. Contribution claims overstate ablation evidence (Moderate)
The third bullet contribution states "with ablations isolating the effects of graph policies and inheritance." However, the paper does not run dedicated ablation experiments. The four-way comparison (GAT-global-transfer, GAT-local-transfer, MLP-transfer, MLP-scratch) compares holistic methods, not isolated factors. The GAT advantage could come from any combination of: graph inductive bias, attention mechanism, increased parameter count, or the specific inheritance mapping. Without matched-capacity MLP baselines or an MLP+GAT-hybrid control, readers cannot attribute gains to specific factors.

**Required action:** Either: (a) add a matched-parameter MLP baseline with the same number of parameters as the GAT, or (b) rephrase the contribution to accurately reflect the holistic comparison design.

### W6. Anthropomorphic language without evidence (Minor)
The claim that GAT-co-designed robots display "motion patterns that resemble human-like throwing mechanics" (Section 5.2) is subjective and unsupported. No biomechanical analysis or human motion data is provided. This wording may mislead readers about the nature of the learned behavior.

**Required action:** Replace with a concrete, measurable statement about actuator recruitment (e.g., "the GAT-based methods recruit two actuators instead of one, producing stronger propulsion").

### W7. Morphology convergence claim needs quantitative backing (Minor)
Section 5.3 states that "evolved robots tend to converge toward broadly similar morphologies" across methods, based on visual inspection of Figure 5. Without a quantitative morphology similarity metric (e.g., voxel-wise overlap, graph edit distance), this claim remains qualitative and potentially biased by cherry-picked examples.

**Required action:** Compute a pairwise morphology similarity metric across methods and runs, or soften the claim to acknowledge the qualitative nature of the evidence.

### W8. Related work is list-like rather than structured by comparison axes (Minor)
Section 6 presents a chronological literature summary rather than organizing prior work around decision-relevant categories (graph-based vs. MLP policies, inheritance vs. no-inheritance, soft vs. rigid). This makes it harder for readers to quickly assess the paper's novelty positioning.

**Required action:** Reorganize related work into 2-3 thematic categories with explicit comparison to this paper's approach for each category.

### W9. Abstract grammar and missing quantitative anchor (Minor)
The abstract contains a grammatical error ("by develop") and lacks any numerical performance anchor, reducing its impact as a standalone summary.

**Required action:** Fix grammar and include a representative quantitative result (e.g., "up to 6.26 vs 3.35 fitness on Thrower-v0").

### W10. Novelty verification deferred (Systemic)
Due to Retrieval-Disabled Mode (paper_search unavailable), the novelty of the GAT-based co-design approach relative to existing graph-policy methods (e.g., NerveNet, Kurin et al. "My Body Is a Cage") cannot be independently verified. The paper's differentiation claims—voxelized soft robots in EvoGym and topology-consistent actuator mapping—appear plausible but require manual literature verification before acceptance decisions.

**Required action:** Authors should explicitly compare with NerveNet-style graph policies and Kurin et al.'s Transformer-based approach on the same EvoGym benchmark to substantiate differentiation claims.

## Score
**Final Score: 5.5/10**

**Rationale:** The paper addresses a well-motivated and timely problem (morphology-aware controller inheritance in soft-robot co-design) with a technically sound approach (GAT-based policies with topology-consistent weight mapping). The core ideas are clearly communicated and the EvoGym benchmark provides a fair evaluation platform. However, the paper is significantly limited by reproducibility deficits (missing hyperparameters, underspecified architecture, pseudocode error), lack of statistical rigor (no significance tests, only 3 seeds), and overclaimed contributions that promise ablation evidence not delivered in the experiments. The novelty relative to existing graph-structured policy methods (NerveNet, Kurin et al.) cannot be verified without external literature access, which is deferred. These issues are fixable with moderate effort: adding hyperparameter tables, significance tests, architecture details, and tightening claims would substantially strengthen the paper. In its current form, the paper provides a useful proof-of-concept but does not yet meet the evidence standard required for strong conclusions about GAT superiority in co-design.