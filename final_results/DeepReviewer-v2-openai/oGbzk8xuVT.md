## Summary
# Final Review Report

## Summary

This paper introduces **BuilderBench**, a block-building benchmark designed to accelerate research on open-ended exploration and generalization in reinforcement learning agents. The benchmark consists of a hardware-accelerated physics simulator (built on MuJoCo + JAX) where a robotic hand interacts with cube-shaped blocks, and a curated task suite of 42 target structures that test physics understanding, mathematical reasoning, and long-horizon planning. The paper defines two evaluation protocols: a multi-task self-supervised protocol (agents explore without task supervision, then are evaluated on unseen structures) and a single-task supervised protocol (for debugging and architecture validation). Benchmarking results on 10+ RL algorithms show that current methods solve only the simplest tasks (1-2 cubes) and fail on more complex structures. The paper also evaluates LLMs (ChatGPT-5, Gemini 2.5 Pro) on high-level planning for five tasks, finding that they cannot produce correct construction plans.

**Core strengths:** The benchmark addresses a genuine gap—most existing RL benchmarks do not require open-ended exploration and cross-task generalization in a physically grounded environment. The simulator's hardware acceleration (10-100x speedup over CPU-based alternatives) lowers the barrier to entry. The hand-curated task suite with explicitly designed reasoning requirements is more principled than purely procedural generation.

**Core weaknesses:** The paper lacks sufficient detail on environment parameters, task specification encoding, and reward functions for full reproducibility. Several narrative claims go beyond the evidence (e.g., "inherent difficulty" framing of results, speculative ease of extension). Novelty cannot be assessed due to retrieval unavailability. The introduction conflates multiple motivations and would benefit from a clearer problem-gap-solution chain. The Minecraft comparison is too brief given its relevance as the closest existing benchmark.

**Recommendation:** The benchmark infrastructure is valuable and the task suite is well-designed. However, the paper needs significant revisions in methodological documentation, claim calibration, and narrative clarity before it meets the standard for publication. I recommend major revisions focusing on: (1) completing missing environment specifications, (2) restructuring the introduction to follow a clear problem-gap-solution narrative, (3) calibrating the strength of claims to match available evidence, and (4) adding statistical rigor to experimental reporting.

## Strengths
1. **Addresses a genuine gap in RL benchmarking.** Most existing RL benchmarks evaluate agents on a small number of similar tasks and do not require systematic cross-task generalization in an open-ended setting. BuilderBench's focus on self-supervised exploration followed by zero-shot evaluation on diverse unseen structures targets an important underexplored problem.

2. **Hardware-accelerated simulator reduces iteration time.** By building on MuJoCo + JAX, the simulator achieves 10-100x speedup over CPU-based open-ended environments (Crafter, Minecraft, NetHack). This is a practical engineering contribution that lowers the barrier to entry for RL research on exploration and generalization.

3. **Principled task suite design.** The 42 tasks are hand-curated rather than procedurally generated, with each structure designed to test specific reasoning abilities (geometry, packing, counterweights, scaffolding, stability). The five case studies (T-Block, Four Cube Packing, Hexagonal Portal, Leaning Tower, Maximum Overhang) convincingly demonstrate that block-building can generate tasks requiring diverse high-level skills.

4. **Two evaluation protocols provide flexibility.** The multi-task self-supervised protocol tests open-ended exploration and generalization, while the single-task supervised protocol enables researchers to debug architectures and study representation learning in isolation. This dual-protocol design supports both fundamental and applied research.

5. **Open-source release with reference implementations.** Providing single-file implementations of seven algorithms (PPO, SAC, CRL, RND, BRO, GNN-ATT, SFL, MEGA, UDRL) in an open-source framework makes the benchmark immediately usable and reduces the setup overhead for new users.

6. **Honest limitation acknowledgment.** The paper explicitly acknowledges that current algorithms fail on most tasks (particularly 3+ cube structures), which sets realistic expectations and provides clear headroom for future progress. The "training wheels" protocol is a practical concession to current limitations.

## Weaknesses
### Major Weaknesses

**W1. Insufficient environment specification for reproducibility.** The paper omits critical details needed to reproduce the experimental setup. Action scales, control frequency, physics timestep, observation noise, termination conditions, and the 34-dimensional task specification encoding are either undefined or underspecified. The task specification uses a fixed-size $\mathbb{R}^{34}$ vector, but the mapping from target cube positions to this encoding is never explained. Without these details, independent researchers cannot replicate the benchmark configuration, which undermines one of the paper's core goals (accelerating research). *Impact: high — directly affects reproducibility and usability.*

**W2. Introduction lacks a clear problem-gap-solution narrative.** The first section ("The Need for a New Benchmark") contains four paragraphs that mix motivational arguments, benchmark surveys, and aspirational vision without a logical progression. The opening conflates two distinct motivations (limits of data-driven AI and need for open-ended exploration) without establishing a clear causal link between them. The paragraph on existing benchmarks is a dense citation list without grouping by comparison axes. The "Why block-building?" argument relies on child-development analogies rather than direct evidence for why blocks are uniquely suited for open-ended agent exploration. *Impact: high — the paper's facade does not effectively communicate its research contribution.*

**W3. Claim-evidence misalignment in experimental interpretation.** The paper states that "both algorithms achieve trivial performance on tasks with three cubes" and that this "primarily underscores the inherent difficulty of the task setup itself." This framing equates poor algorithm performance with benchmark difficulty without analysis. The same results could be explained by poor algorithm selection, uninformative reward design, or inappropriate architecture choices. No ablation studies, failure analysis, or diagnostic experiments are provided to distinguish these hypotheses. The paper should offer concrete directions for why algorithms fail rather than attributing failure to "inherent difficulty." *Impact: high — weakens the scientific value of the experimental feedback.*

**W4. Missing comparative analysis with Minecraft.** The Related Work section acknowledges Minecraft as the closest existing benchmark (block-building, physics, exploration) but dismisses it in a single sentence with the claim that BuilderBench is "better suited for academic research due to the much faster speed of its simulator and an extensive carefully curated task-suite." This comparison does not address Minecraft's advantages (larger community, more diverse tasks, extensive research infrastructure, proven platform for generalist agent research like Voyager, Dreamer, etc.). A more substantive comparison with explicit trade-offs would strengthen the paper's positioning. *Impact: moderate — weakens the novelty positioning.*

**W5. LLM evaluation protocol is too narrow to support broad conclusions.** The paper concludes that LLM failures show "solving our tasks requires non-obvious steps of reasoning that are beyond what current models can achieve through scaling alone." However, the evaluation only tests open-loop text-based planning. This design does not rule out LLM effectiveness in closed-loop settings (with visual feedback, replanning, or subgoal proposal) or with more structured prompting. Binary success/failure reporting (X marks) without granular error analysis limits the informativeness of the results. *Impact: moderate — the conclusion overreaches the evidence.*

### Minor Weaknesses

**W6. Abstract uses informal language and lacks compact structure.** The opening "mimicry and sharpening" is undefined terminology. The rhetorical closing question ("Can AI models build a world...") is stylistically unusual and adds no factual content. The prior-work gap is not stated as a discrete sentence.

**W7. Contribution bullet list mixes conceptual and engineering claims.** The four bullets combine benchmark design, simulator speed, open-source release, and reference implementations without distinguishing scientific contributions from engineering deliverables.

**W8. Speed claim (10-100x) lacks comparative benchmark details.** The claim that BuilderBench runs 10-100x faster than Crafter, Minecraft, and NetHack needs specification of hardware, measurement methodology, and task configurations used for comparison.

**W9. Conclusion makes unsupported claims about future extensibility.** The statement "we expect extending BuilderBench to incorporate these settings [stochasticity, partial observability, multi-agent] should be easy" is speculative and unsubstantiated. *Impact: minor — reduces credibility of forward-looking statements.*

**W10. Citation typo.** "Kaeling, 1993" should be corrected (likely "Kaelbling, 1993" or a different reference).

### Novelty and Comparison (Deferred)

Due to Retrieval-Disabled Mode (external paper search unavailable), novelty verification and related-work comparison cannot be completed in this review. The following questions should be addressed in a follow-up manual literature check:
- How does BuilderBench compare to Minecraft-based benchmarks (e.g., MineDojo, CraftEnv) in terms of task diversity, exploration requirements, and generalization measurement?
- Are there existing block-building simulators in robotics research (e.g., Nvidia Isaac Gym, Bullet blocks-world environments) that offer similar capabilities?
- How does the self-supervised evaluation protocol compare to prior unsupervised RL benchmarks (e.g., DMC, URLB, XLand)?

```text
ASCII Diagram — Paper Structure & Evidence Map

[Abstract]
   ├─ Problem: AI models struggle beyond data limits (weak: no clear gap statement)
   ├─ Solution: BuilderBench benchmark (stated)
   └─ Result: Current algorithms only solve simplest tasks (stated)

[Introduction: The Need for a New Benchmark]
   ├─ P1: Big picture (conflates two motivations) ── [ANNOTATION W2]
   ├─ P2: Survey of existing benchmarks (citation list) ── [ANNOTATION W2]
   ├─ P3: Vision for open-ended benchmark (aspirational) ── [ANNOTATION W2]
   ├─ P4: Why block-building? (child development analogy) ── [ANNOTATION W2]
   └─ Contribution bullets (mixed conceptual/engineering) ── [ANNOTATION W7]

[Related Work]
   ├─ RL benchmarks (standard, unsupervised, meta-learning)
   └─ Closest benchmarks (Kinetix, XLand, Minecraft) ── [ANNOTATION W4]

[Method: Environment]
   ├─ MDP formulation, state/action spaces ── [ANNOTATION MISSING: reproducibility]
   └─ Task specification (R^34 undefined) ── [ANNOTATION W1]

[Experiments]
   ├─ Self-supervised protocol (4 algorithms, 12 tasks) ── [ANNOTATION W3]
   ├─ Supervised protocol (6 algorithms, 17 tasks)
   └─ LLM evaluation (open-loop only) ── [ANNOTATION W5]

[Conclusion]
   ├─ Limitations (speculative "should be easy") ── [ANNOTATION W9]
   └─ Closing vision (generic aspiration)
```

```text
ASCII Diagram — Revision Strategy Roadmap

[W1: Missing environment specs]
   -> Add action scale, physics dt, termination, task encoding
   -> Expected gain: reproducibility + usability

[W2: Weak introduction narrative]
   -> Restructure: Big Picture -> Gap -> Solution -> Evidence -> Contributions
   -> Expected gain: clearer research contribution

[W3: Claim-evidence mismatch in results]
   -> Add failure analysis, ablation studies, specific hypotheses
   -> Expected gain: stronger scientific feedback

[W4: Minecraft comparison too brief]
   -> Expand with explicit trade-offs, not dismissal
   -> Expected gain: stronger benchmark positioning

[W5: LLM eval too narrow]
   -> Add granular error analysis, discuss closed-loop potential
   -> Expected gain: fairer conclusions

[W6-W10: Minor issues]
   -> Fix abstract, speed claim, citation typo, conclusion claims
   -> Expected gain: higher paper polish
```

```text
ASCII Diagram — Related-Work Taxonomy Tree (Layered)
(Note: external literature verification not available in this run)

Related Exploration & Generalization Benchmarks
├── Branch 1: Single-task RL benchmarks
│   ├── Leaf 1.1: Atari/Gym (narrow task range, no cross-task eval)
│   ├── Leaf 1.2: DM Control Suite (continuous control, limited diversity)
│   └── Leaf 1.3: Procgen/NetHack (procedural, but task-specific rewards)
├── Branch 2: Unsupervised/self-supervised RL benchmarks
│   ├── Leaf 2.1: URLB (unsupervised pre-training, limited downstream tasks)
│   ├── Leaf 2.2: DMC/Kitchen (few tasks, limited generalization)
│   └── Leaf 2.3: XLand (multi-agent video-game, closed-source)
├── Branch 3: Block-building / construction environments
│   ├── Leaf 3.1: Minecraft/MineDojo (most similar; slower, less curated)
│   ├── Leaf 3.2: Kinetix (2D rigid-body, procedural, less reasoning diversity)
│   └── Leaf 3.3: AI planning blocks-world (classical, no physics/exploration)
└── Branch 4: Open-ended exploration benchmarks
    ├── Leaf 4.1: Crafter (2D survival, limited task diversity)
    ├── Leaf 4.2: ARC-AGI (discrete puzzles, no physical interaction)
    └── Leaf 4.3: BuilderBench (THIS PAPER: 3D blocks, physics, curated tasks)

Key distinction: BuilderBench sits at the intersection of physical block-building,
curated reasoning tasks, and hardware-accelerated simulation — a combination
not fully covered by any single existing benchmark.
```

## Score
**Final Score: 6/10**

**Rationale:** The score of 6/10 reflects the following assessment:

- **Research value & contribution (primary dimension):** The benchmark infrastructure and task suite represent a genuine contribution to the RL benchmarking ecosystem. The hardware-accelerated simulator, curated reasoning tasks, and dual-protocol evaluation are valuable tools for the community. Score contribution: +2.5/4.

- **Novelty & positioning:** The idea of using block-building for open-ended exploration is not entirely new (Minecraft, Kinetix, classical blocks-world), but the specific combination of physics simulation, curated reasoning tasks, and hardware acceleration has incremental novelty. However, novelty verification is deferred due to retrieval unavailability, and the Minecraft comparison is insufficiently developed. Score contribution: +1.5/3.

- **Soundness & validity:** The experimental methodology has several issues that reduce confidence. The interpretation of algorithm failures as "inherent difficulty" is not well-supported. Missing environment specifications hinder reproducibility. The LLM evaluation protocol is too narrow for the conclusions drawn. Score contribution: +1.5/5 (weight adjusted for severity).

- **Clarity & presentation:** The introduction lacks a clear narrative arc. The abstract uses informal language. Several figures (Figure 6, 7) show results that are difficult to parse in the text extraction. The paper is generally well-written but would benefit from structural revision. Score contribution: +0.5/2.

- **Reproducibility:** The paper provides open-source code and reference implementations, which is commendable. However, missing environment specifications and undefined task encoding reduce the standalone reproducibility of the results section. Score contribution: +1.5/3.

**Summary of critical issues affecting score:**
1. W1 (missing environment specs): directly harms reproducibility
2. W2 (weak introduction narrative): reduces communication effectiveness
3. W3 (claim-evidence mismatch): weakens scientific rigor of experimental feedback
4. W4 (Minecraft comparison): insufficient positioning relative to closest benchmark
5. Novelty cannot be fully assessed (retrieval unavailable)

**The paper has solid infrastructure contributions but needs significant revisions in methodological documentation, narrative clarity, and claim calibration before it can be considered for acceptance.**