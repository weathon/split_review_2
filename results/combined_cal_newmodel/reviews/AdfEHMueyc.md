## Summary

This paper addresses the problem of co-designing morphology and control in soft robots, where evolutionary changes to body structure break the fixed-dimensional input/output assumptions of standard MLP policies. The authors propose representing voxelized soft robots as graphs and using Graph Attention Network (GAT)-based controllers that naturally handle varying graph sizes. A MAPWEIGHTS inheritance procedure transfers knowledge from parent to offspring morphologies by reusing shared GAT layers and mapping actuator heads via spatial correspondence. Experiments on four EvoGym tasks show that GAT-with-inheritance outperforms MLP baselines (with and without inheritance).

## Strengths

- **Problem framing is well-motivated (Section 1, lines 13-16).** The paper identifies a genuine obstacle: when morphology changes through evolution, the controller's input/output topology changes too, breaking fixed-dimensional MLP policies. This is a real issue, and addressing it with graph-structured policies is a worthwhile contribution.

- **Graph representation is a natural fit (Section 3, lines 71-72, 108-109).** Modeling voxelized soft robots as graphs (nodes = sensors/actuators, edges = spatial adjacency) and using GATs to handle varying graph sizes natively is a clean, sensible solution to the fixed-input problem.

- **MAPWEIGHTS procedure (Algorithm 2) is clearly specified.** The weight-mapping rules — reuse shared GAT layers, transfer matched actuator heads, randomly initialize new ones, discard removed ones — are straightforward and well-described. This clarity aids reproducibility and adoption.

## Weaknesses

### Fatal
None.

### Major

- **Missing critical ablation: No GAT-without-inheritance condition.** The paper compares GAT-with-inheritance (two variants), MLP-with-inheritance, and MLP-from-scratch, but never evaluates GAT-from-scratch. Without this condition, we cannot tell whether performance gains come from the GAT architecture itself (which naturally handles varying graph sizes) or from the specific MAPWEIGHTS inheritance scheme. The abstract (line 31) explicitly claims the paper includes "ablations isolating the effects of graph policies and inheritance," but no such ablation exists in the experiments. This is a factual inaccuracy in the paper's own claims about its contributions.

- **Insufficient statistical evidence.** All results are based on only 3 independent runs (Figure 3 caption and Section 5.1, line 170). No statistical tests (t-test, bootstrap, Mann-Whitney) are reported. In a domain where both evolutionary optimization and PPO exhibit high variance, 3 runs is too few to confidently assert differences in "higher final fitness," "stronger adaptability," or "lower variance." The standard-deviation shading in Figure 3 cannot substitute for formal hypothesis testing — some generation-by-generation overlap in shaded regions (visible in Carrier-v1 and Catcher-v0 as described) suggests claimed advantages may not be reliable.

- **No comparison to other structure-aware controllers.** The Related Work (Section 6.2, lines 219-224) correctly identifies NerveNet (Wang et al. 2018) and the Transformer controller from Kurin et al. (2021) as relevant graph- or structure-aware alternatives, but never compares against them experimentally. The paper's core claim is that GATs enable effective co-design; without comparison to other structure-aware controllers, the evidence only shows "GAT > MLP" — a much more modest result than the title and abstract suggest.

- **Architecture details critically underspecified (Section 3).** The GAT implementation is described only as "a GAT layer, which aggregates information through one attention-based message passing round, followed by averaging over nodes" (line 140). Missing specifications include: number of attention heads, hidden dimensionality, activation functions, MLP head depth and width, learning rate, PPO clip parameter, entropy bonus, and all other PPO hyperparameters. The paper states these are "adopted from Harada & Iba (2024)" and uses Kostrikov's PPO implementation (line 160), but does not list a single numerical value. This is below the reproducibility standard for a methods paper.

- **MAPWEIGHTS node correspondence is unspecified (Algorithm 2).** Algorithm 2 (line 117) says "Compute node correspondence C by spatial matching" but never describes *how* this spatial matching is computed, what distance metric is used, or what happens when morphology changes drastically — e.g., a new appendage appears at a location with no spatially corresponding old node. This is a critical gap in the inheritance mechanism specification.

### Minor

- **Internal tension on convergence speed.** Section 5.1 (line 176) states: "In Thrower-v0, convergence is also faster in the early generations." Section 7 (line 230) states: "GAT controllers often achieve higher final performance than MLP baselines, they do not always converge as quickly." These claims pull in opposite directions on the same dimension (convergence speed), and the paper never systematically quantifies or resolves this ambiguity.

- **Qualitative claim not quantified (Section 5.2).** The paper states GAT robots "make use of two actuators instead of the single actuator typically used in baseline designs" (line 188), but this is based on visual inspection of a single seed. The paper should quantify how often across runs and conditions GAT-based designs evolve multi-actuator strategies.

- **Algorithm 1 typo (line 83).** Line 2 reads "for g = 1 … p do" — using population size p as the loop bound for generations — but should read "for g = 1 … n do" to match the declared parameter "max generations n" (line 81). The variable p is used both for population size (line 81) and the generation loop bound (line 83), which is a bug in the algorithm specification.

- **Carrier-v1 task-dependence not examined.** All methods reach similar high fitness on Carrier-v1 (Figure 3). The paper frames this positively ("GAT variants rapidly attain near-optimal performance"), but the more natural reading is that Carrier-v1 is easy enough that even MLP-from-scratch does well. The paper does not examine why the GAT advantage disappears for this task or what this implies about generality.

### Trivial
None.

## Nice-to-Haves

- Report training time / total wall-clock cost to help readers assess the cost-benefit trade-off of the more expensive GAT architecture.
- Provide a justification for using mutation-only evolution (no crossover), since it differs from the standard EvoGym protocol.
- Quantify the multi-actuator strategy claim (Section 5.2) across multiple runs.
- Report convergence speed quantitatively (generations to reach a given fitness threshold with confidence intervals).

## Removed Points

- **"Abstract claims ablations that don't exist"** — Already covered under the missing GAT-no-inheritance ablation weakness above (Merged).
- **"Mutation-only evolution not justified"** — The paper states this choice explicitly (Section 4). It is a valid design choice, not a weakness.
- **"No crossover is a departure from EvoGym protocols"** — The paper is free to make design choices differing from prior work. Not a weakness.
- **"Carrier-v1 weakens the paper's case"** — This is an interpretive opinion, not a verifiable flaw. Kept as a minor weakness (task-dependence not examined) but the stronger framing was removed.
- **"Morphology evolution analysis undercuts claims"** — The paper explicitly acknowledges this finding (Section 5.3, line 204): "task requirements strongly shape the space of feasible morphologies, whereas the controller architecture mainly influences learning speed and adaptability." This is an honest discussion, not a contradiction.
- **"Missing runtime/compute cost"** — Moved to Nice-to-Haves.
- **"Missing related works"** — Cannot verify; removed per hard rules.
- **Reproducibility nitpicks about format/style** — Removed per hard rules.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. **Add a GAT-PPO-no-inheritance baseline.** This is the single highest-leverage experiment. It would directly test whether the contribution is in the GAT representation or the inheritance mechanism, and it would correct the factual inaccuracy in the abstract claim about "ablations isolating the effects of graph policies and inheritance."

2. **Run at least 10 seeds and report effect sizes** (Cohen's d or bootstrapped confidence intervals on the difference in final fitness). Three runs is not sufficient to draw reliable conclusions in this high-variance setting.

3. **Compare against at least one additional structure-aware controller** — e.g., NerveNet (Wang et al. 2018), which the paper already cites and discusses.

4. **Add a hyperparameter table** specifying GAT architecture (attention heads, hidden dimensions, layers, activations), MLP head structure, PPO hyperparameters (learning rate, clip parameter, entropy bonus, GAE λ), and GA parameters (mutation rate, elite count).

5. **Describe the spatial matching procedure in MAPWEIGHTS**, including the distance metric and a protocol for handling unmatched nodes.

6. **Resolve the convergence-speed contradiction** by systematically measuring and reporting generations to reach a threshold across all tasks and runs.

---

### Calibration Anchors

| Paper | Path | Avg Score | Round | Itemized | Comparison |
|-------|------|-----------|-------|----------|------------|
| MeMo | VZTFUtldbC | 4.75 | 2, bracket | Yes | Similar domain (modular robot controller transfer). MeMo compared against NerveNet; this paper lacks even that baseline. Both share missing-baseline and insufficient-generalization weaknesses. |
| Subequivariant MB Co-Evolution | MueN6LyTmS | 5.20 | 2, bracket | Yes | Closest topical match (co-evolution of morphology and behavior with GNNs). Shared weaknesses: missing SOTA baselines, claims not fully supported by evidence, underspecified architecture. Current paper has more severe experimental gap (missing ablation). |
| Cross-Embodiment Grasping | twIPSx9qHn | 5.00 | 2, bracket | Yes | Cross-embodiment policy transfer. Had real-world validation and comprehensive benchmarks despite missing baselines criticism. Current paper is weaker experimentally. |
| Meta-Evolve | RthOl4jHw5 | 6.00 | 1 | Yes | Policy transfer across morphologies. Had 5 seeds (more than this paper), clear baselines, and ablation studies. Stronger experimental footing than current paper. |
| EvIL | KXNLvfCxEr | 3.75 | 2, bracket | No | Lower-quality paper with imitation learning focus. Not directly comparable but anchors the bottom of the bracket. |

**Round 1 bracket:** 4.0–5.5. The paper's well-motivated problem framing and clean approach place it above EvIL (3.75). However, the experimental gaps (missing ablation, 3 runs, no statistical tests, no structure-aware baselines) are more severe than those of MeMo (4.75) or the Subequivariant paper (5.20), both of which were rejected.

**Narrowing:** Comparing itemized favorability: MeMo's most negative weaknesses (e.g., "baselines insufficient" at -0.16, "vague claims" at -1.15) are less severe than this paper's most negative weakness ("qualitative claim not quantified" at -2.35, "Carrier-v1 not examined" at -1.50). The Subequivariant paper's weakness about missing baselines ("experiments do not compare with previously introduced algorithms") maps directly to this paper's missing GAT-no-inheritance ablation and missing structure-aware baseline comparisons. The Subequivariant paper scored 5.20 but had a reviewer giving 1 (low confidence no. 1); removing that outlier gives ≈4.75. This paper's experimental gaps are larger (the missing ablation contradicts a stated contribution claim in the abstract), placing it slightly below MeMo at **4.5**.

## Score and Decision

MY FINAL SCORE: <score>4.5</score>
MY FINAL DECISION: <decision>Reject</decision>