## Summary
# Final Review Report

## Summary

This paper studies Online Inventory Optimization (OIO) under non-stationary demand — a sequential decision-making problem where a learner sets order-up-to levels for multiple items subject to warehouse capacity and carryover stock constraints. The main contribution is a novel algorithm achieving **near-optimal dynamic regret** $\tilde{\mathcal{O}}(\sqrt{L_{\max}T(1+P_T)})$ without prior knowledge of the maximum sell-out period $L_{\max}$ or the comparator path-length $P_T$. The algorithm employs a two-stage projection strategy that decouples the base learner (operating on capacity constraints only) from the carryover stock constraint via projection, thereby connecting OIO to Smoothed Online Convex Optimization (SOCO). A matching $\Omega(\sqrt{L_{\max}T})$ lower bound is also established, improving upon existing static-regret bounds by $\sqrt{L_{\max}}$. The paper is purely theoretical: all results are regret upper/lower bounds with no empirical evaluation.

The paper is technically solid and addresses a well-motivated open problem (dynamic regret for OIO). The two-stage projection idea is clean and the connection to SOCO is insightful. However, the presentation has several areas needing improvement: the abstract and introduction overclaim without sufficient qualification, the key parameter $L_{\max}$ has definitional subtleties that are not fully discussed, and the relationship between the general framework (Theorem 2) and concrete instantiations (Theorems 3-4) is not fully explicit. Novelty assessment is deferred to manual verification due to external paper search unavailability in this run.

## Strengths
**1. Well-motivated and timely problem.** The paper addresses the dynamic regret minimization problem for OIO, which is a natural extension of the static-regret OIO framework established by Hihat et al. (2023). The motivating example (Section 1, fluctuating demand with linear trend) convincingly shows why static regret is inadequate under non-stationary demand, and why $\Omega(T)$ regret can arise even with $\mathcal{O}(\sqrt{T})$ static regret.

**2. Clean algorithmic idea.** The two-stage projection strategy (Alg. 2) is conceptually simple yet effective: a base learner operates independently of carryover stock constraints, and its output is projected onto the feasible set $\mathcal{C}(x_{t+1})$. This decoupling elegantly bypasses the technical difficulty that the comparator $u_t$ and the decision $y_t$ have different feasible regions. The connection to SOCO via Lemma 1 is a technically novel insight that opens the door to leveraging existing SOCO algorithms for OIO.

**3. Tight theoretical guarantees.** The paper provides both upper bounds ($\tilde{\mathcal{O}}(\sqrt{L_{\max}T(1+P_T)})$ dynamic regret, $\mathcal{O}(\sqrt{L_{\max}T})$ static regret) and a matching $\Omega(\sqrt{L_{\max}T})$ lower bound, establishing near-optimality. The lower bound (Theorem 5) is a non-trivial contribution that resolves the open question raised by Hihat et al. (2023). The matching static bound improves prior work by a $\sqrt{L_{\max}}$ factor after reparameterization.

**4. Adaptive algorithm (SOGD version).** The SOGD-based instantiation (Theorem 4, Alg. 5) achieves dynamic regret without requiring a priori knowledge of $P_T$, using a meta-algorithm with Discounted-Normal-Predictor. This makes the algorithm practical in the sense that it does not need advance knowledge of future demand variability.

**5. Transparent limitation discussion.** The conclusion mentions key limitations: lack of lead time handling, fixed-order costs, and the restriction to linear capacity constraints. This transparency is commendable for a theory paper.

## Weaknesses
**W1. [Major] Ambiguity in the "$\sqrt{L_{\max}}$ improvement" claim.** The abstract and Theorem 1 statement claim "an improvement of $\sqrt{L_{\max}}$ for the static regret upper bound in existing studies." While Table 1 diligently reparameterizes prior bounds to use $L_{\max}$, the abstract does not explain that prior works used different demand-characteristic parameters (e.g., $1/\gamma$, $1/\mu$, $D$) that are not directly comparable. A reader may misinterpret this as a direct improvement on the same metric in the identical setting. *Fix:* Qualify the improvement claim by explicitly stating that reparameterization aligns prior bounds to a common scale, and note that direct apples-to-apples comparison is not always possible.

**W2. [Major] Theorem 3 (OGD) requires prior knowledge of $P_T$ despite the "without knowing $P_T$" claim.** The paper's highlight contribution (Theorem 1 informal) states the algorithm works "without knowing $L_{\max}$ and $P_T$ a priori." However, the OGD-based instantiation (Theorem 3) explicitly requires $P_T$ in the learning rate $\eta$. The text acknowledges this but only in one sentence. Since the SOGD-based algorithm (Theorem 4) resolves this, the presentation should more sharply distinguish between algorithms that are fully adaptive and those that require $P_T$. *Fix:* Revise Theorem 3 statement to explicitly note the $P_T$ requirement, and restructure the narrative so the fully adaptive SOGD result is presented as the primary algorithmic contribution.

**W3. [Major] Theorem 2's assumptions are not explicitly verified for the concrete base learners.** Theorem 2 provides a general regret bound assuming the base learner's regret decomposes as $L^\alpha \mathcal{R}(T)$ and its switching cost is $\mathcal{O}(L^{-\beta})$. The paper does not compute $\alpha$ and $\beta$ for either OGD or SOGD. While these can be inferred (e.g., $\alpha=1/2$ for OGD, $\beta$ depends on $\eta$), making the mapping explicit would improve clarity and reproducibility. *Fix:* Add a short table or paragraph showing the parameter mapping for each base learner.

**W4. [Major] The $L_{\max}$ parameter has definitional subtleties that affect practical relevance.** Definition 1 defines $L_{\max}$ as a worst-case minimum over all items and all time intervals such that cumulative demand reaches $D$ within $L$ rounds. This is an extremely strong condition: if even one item experiences low demand for one interval, $L_{\max}$ can approach $T$, making sublinear regret impossible. The paper acknowledges this boundary case ($L_{\max} = \Omega(T)$ implies no sublinear regret) but does not discuss how restrictive this condition is in practice. The probabilistic extension (Remark 3) helps but is not formally integrated into the main results. *Fix:* Provide a more thorough discussion of when $L_{\max}$ is realistically $o(T)$, perhaps with concrete examples of demand patterns that satisfy or violate the condition.

**W5. [Major] Inconsistency in the parameter-doubling logic of Algorithm 2.** Alg. 2 initializes $\mathcal{E}(2L,T)$ with $L=1$ and restarts with $2L$ when $\max\mathcal{L}_t > L$. The resulting sequence of base-learner parameters is $2, 4, 8, \ldots$, but Theorem 2's final bound uses $\mathcal{R}_{2L_{\max},T}$. The factor of 2 is not explained. While standard for doubling tricks, the relationship between the doubling condition ($L < \max\mathcal{L}_t \leq L_{\max}$) and the final parameter $2L_{\max}$ should be explicitly derived. *Fix:* Add a brief analysis showing that when the algorithm terminates, $L \leq L_{\max} < 2L$, so the base learner parameter is $2L \in [L_{\max}, 2L_{\max})$.

**W6. [Moderate] The logical gap in the two-layer structure difficulty argument (Section 1).** The argument explaining why standard two-layer meta-algorithms fail in OIO conflates two different issues (meta-algorithm overriding base-learner decisions vs. carryover stock constraint violation). The specific concern that "$x_{t+1}$ can exceed $y_t^a$" is not clearly connected to the algorithm architecture described later. *Fix:* Clarify that the issue is that base learners in standard OCO assume a fixed feasible set, but in OIO the feasible set depends on the previous decision through $x_{t+1}$, which is incompatible with standard two-layer analysis.

**W7. [Minor] Related Work sections are list-like rather than critically positioned.** The Inventory Management paragraph (Section 2) enumerates many dimensions without stating how they relate to the paper's contribution. The OCO paragraph omits reference to the matching lower bound $\Omega(\sqrt{(1+P_T)T})$ from Zhang et al. (2018b), which is directly relevant to the optimality discussion in Section 5. *Fix:* Restructure Related Work to highlight the gap this paper fills, and add the matching lower bound reference.

**W8. [Minor] Conclusion is too brief and lacks structured summary of validated findings.** The conclusion does not enumerate specific proven results, does not bound the scope of claims, and uses informal language ("we believe"). *Fix:* Restructure as suggested in the annotation — list proven bounds, state limitations explicitly, and use precise language.

**W9. [Minor] Algorithm 1 mixes problem setup with algorithmic decision rule.** The "Algorithm 1" label suggests an algorithmic method, but the content describes the environment's behavior and information structure. *Fix:* Rename to "Setting of OIO (per-round interaction)" to avoid confusion.

**Novelty Assessment (Deferred):** Due to external paper search unavailability in this run, novelty and comparison conclusions are deferred to manual verification. The paper claims the first dynamic regret guarantee for OIO; this should be verified against the most recent OCO-for-inventory literature, particularly works on dynamic regret in related online convex optimization settings with state-dependent constraints.

## Score
Final Score: 6/10

**Rationale:** The paper addresses a well-motivated theoretical problem with a clean algorithmic idea and tight regret bounds. The two-stage projection connecting OIO to SOCO is technically novel, and the matching lower bound resolves an open question. However, the score is constrained by several factors: (1) the presentation overclaims in the abstract without sufficient qualification; (2) the OGD instantiation requires a priori knowledge of $P_T$, undermining the full adaptivity claim; (3) the general framework (Theorem 2) and concrete algorithms are not explicitly connected via parameter mapping; (4) the $L_{\max}$ parameter has definitional restrictiveness that is not adequately discussed; and (5) the paper is purely theoretical with no empirical validation. These weaknesses are fixable through clearer writing and structural revisions, but in their current form they reduce confidence in the claimed contributions. The paper likely has a solid core that would benefit from a major revision focused on precise communication and explicit verification of framework assumptions.

---

### ASCII Diagrams

```text
ASCII Diagram — Paper Structure & Evidence Map

[Problem: Static regret insufficient for OIO under demand fluctuations]
    |
    v
[Gap: No dynamic regret guarantee for OIO (carryover constraint makes
 standard two-layer methods inapplicable)]
    |
    v
[Key Idea: Two-stage projection + connection to SOCO]
    |-- Base learner operates on C(0) (capacity only)
    |-- Projection onto C(x_{t+1}) restores carryover feasibility
    |-- Lemma 1: projection cost bounded by switching cost × cycle length
    v
[Algorithm 2: Doubling trick for unknown L_max]
    |-- Tracks max observed cycle length
    |-- Restarts base learner when L_max estimate doubles
    v
[Theoretical Guarantees]
    |-- OGD base learner: O(sqrt(L_max(1+P_T)T)) but requires P_T knowledge
    |-- SOGD base learner: O~(sqrt(L_max(1+P_T)T)) fully adaptive
    |-- Lower bound: Omega(sqrt(L_max T))
    v
[Limitations / Open Issues]
    |-- No lead time or fixed-order costs
    |-- Linear capacity constraint only
    |-- No empirical validation
    |-- L_max definition restricts applicability
```

```text
ASCII Diagram — Revision Strategy Roadmap

Issue                                    Fix                                              Expected Gain
─────────────────────────────────────────────────────────────────────────────────
W1: sqrt(L_max) improvement claim        Qualify with reparameterization note        Accurate contribution perception
W2: OGD requires P_T                     Separate adaptive/non-adaptive claims       Clearer contribution scope
W3: Theorem 2 assumptions not verified   Add parameter mapping table (alpha, beta)   Reproducibility + clarity
W4: L_max definition restrictiveness     Add practical demand examples + discussion   Better practical relevance
W5: Doubling trick factor of 2           Add analysis of parameter guarantees        Theoretical precision
W6: Two-layer difficulty argument gap    Rewrite problem statement                   Reader comprehension
W7: Related-work list-like               Restructure as gap-focused comparison       Better positioning
W8: Conclusion too brief                 Add structured result summary               Impactful closing
W9: Alg. 1 mislabeled                    Rename to "Setting of OIO"                  No confusion
```

```text
ASCII Diagram — Related-Work Taxonomy Tree (Layered)

Online Inventory Optimization (Root)
├── Branch 1: Demand Assumption
│   ├── Leaf 1.1: Known demand model [Glock et al. 2014, textbooks]
│   └── Leaf 1.2: Unknown demand (OCO-based)
│       ├── Single-item, i.i.d. [Huh&Rusmevichientong 2009; Zhang+ 2018a]
│       ├── Single-item with lead time [+Zhang+ 2020; Agrawal&Jia 2022]
│       ├── Single-item with fixed cost [+Yuan+ 2021]
│       ├── Multi-item, independent [Shi+ 2016]
│       └── Multi-item, convex constraints [Hihat+ 2023]
│           └── THIS WORK: dynamic regret, linear capacity
├── Branch 2: Regret Type
│   ├── Static regret [all prior OIO works]
│   └── Dynamic regret [THIS WORK]
└── Branch 3: Capacity Constraint
    ├── Interval (single-item capacity) [Huh&R; Zhang+; Yuan+; Agrawal&Jia]
    ├── Linear sum (multi-item) [Shi+ 2016; THIS WORK]
    └── General convex [Hihat+ 2023]

Key Insight: This paper is the first to provide dynamic regret guarantees
in any OIO setting, and the first lower bound for OIO. The main novelty
axis is regret type (dynamic vs. static), enabled by the connection to
Smoothed OCO via two-stage projection.
```