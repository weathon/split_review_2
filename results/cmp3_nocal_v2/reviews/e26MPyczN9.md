## Summary

This paper re-evaluates the widely-cited claim that programmatic policies generalize better than neural policies in RL. Across three benchmarks (TORCS, KAREL, PARKING), the authors show that much of the reported gap stems from uncontrolled experimental confounds (reward design, observation design, spurious correlations) rather than fundamental representational advantages. The paper introduces an expressivity/discoverability framework to analyze why, and identifies memory-scaling tasks (general pathfinding, nested subproblems) where programmatic representations do provide a genuine advantage that fixed-capacity neural architectures cannot match, with a proof-of-concept using FUNSEARCH to synthesize BFS.

---

## Strengths

1. **Clean KAREL re-evaluation (Table 2).** The finding that a simple feedforward network augmented with the last action ("PPO with a_{t-1}") matches or exceeds LEAPS on 4/5 KAREL tasks at 100×100 scale, evaluated over 30 seeds, is the paper's strongest experimental result. It convincingly shows that the original gap was driven by observation design and partial observability handling rather than representation per se.

2. **Expressivity/Discoverability framework (Section 5, Definitions 2–3).** The conceptual distinction between whether a policy space *contains* a generalizing solution and whether search can *find* it provides a clean vocabulary for discussing what had been a vague "representation comparison." This is a useful methodological contribution for future work in this area.

3. **Intellectually honest handling of PARKING (Section 4.3).** The paper presents both interpretations of the PARKING data—PSM has a smaller train-test gap but DQN has a marginally higher absolute test success rate—without spinning the result. This transparency is commendable even though the ambiguity weakens the paper's overall narrative.

4. **Well-motivated positive thesis.** The argument that programmatic representations are genuinely advantageous when the solution requires instance-growing working memory (general pathfinding needs Ω(log|V|) bits) is theoretically sound and points toward a meaningful research direction, distinct from the confound-driven comparisons in prior work.

---

## Weaknesses

### Fatal
None.

### Major

1. **The TORCS comparison is confounded by two asymmetries that weaken the headline claim.**  
   The paper claims neural policies "can match or exceed" programmatic ones on TORCS, but the comparison is not apples-to-apples.  
   - **Different reward function.** NDPS (programmatic) was evaluated under the original reward (β=1.0). The neural DRL method was evaluated under a modified, cautious reward (β=0.5) because β=1.0 caused all 3 seeds to crash. The paper argues this is an "intrinsic reward" that doesn't change the problem (evaluation is on lap time, not reward) — a defensible but debatable position. The claim "neural policies match programmatic ones" is only valid under a reward function that was not needed by the programmatic policy.  
   - **Selection filtering.** For DRL (β=0.5), only models that successfully learned the training track (13/30 for G-TRACK-1, 4/15 for AALBORG) were evaluated on OOD tracks; their generalization fractions (76%, 69%, 100%) are conditional on this filter. For NDPS, 3/3 seeds succeeded, so no filtering was needed. The paper reports the underlying numbers transparently but does not compute an "overall generalization rate" (proportion of all trained seeds that generalize), which for DRL (β=0.5) would be roughly 33% and 27% — substantially lower than NDPS's 100%. While the paper's transparency partly mitigates this, the asymmetry prevents a clean "neural matches programmatic" conclusion on TORCS.

### Minor

2. **The abstract's "match or exceed" claim is too strong for the PARKING results.**  
   On PARKING, neither representation generalizes reliably: PSM achieves test Successful-on-100 of 0.06 vs. DQN's 0.00; PSM's test Success Rate is 0.16 vs. DQN's 0.18. The paper's own discussion is appropriately balanced, but the abstract and introduction frame this as supporting the "match or exceed" narrative. The honest summary is that on PARKING, both methods struggle and there is no clear winner. The claim should be tempered to reflect this.

3. **The expressivity argument for neural-programmatic equivalence is only concretely supported for TORCS.**  
   Section 5 argues that the DSLs induce policy spaces "similar, if not identical" to neural spaces. A concrete argument is given for TORCS (citing Orfanos & Lelis, 2023, and showing how ReLU networks can subsume the DSL by adding peek/fold as inputs). However, for KAREL and PARKING, no analogous construction or citation is provided. The claim that programmatic and neural spaces are expressively equivalent on these domains is asserted rather than demonstrated. This does not invalidate the paper's thesis, but it means the framework rests on partially unsubstantiated premises for two of the three benchmarks.

4. **The HARVESTER failure on KAREL is not analyzed.**  
   PPO with a_{t-1} achieves 0.59 on Small HARVESTER but only 0.04 at 100×100 — the one task where it clearly fails to generalize. Since the paper's central claim is that neural policies can match or exceed programmatic ones, understanding why this single task resists generalization (is it an expressivity issue? A discoverability issue? Does it require memory scaling even at small sizes?) would sharpen the paper's framework and add depth to the analysis. The paper is silent on this.

### Trivial
None.

---

## Nice-to-Haves

- **The FUNSEARCH proof-of-concept (3 runs, one constructed task) is suggestive but preliminary.** The paper appropriately labels it a "proof-of-concept," but demonstrating the memory-scaling thesis across a parametrically varied range of problem sizes (e.g., grids of increasing size) with more trials would significantly strengthen the positive half of the paper's argument.  
- **NetHack is discussed as a domain where programmatic representations would help due to nested subproblems, but no experiments are run.** An experiment on NetHack (or a similar domain with genuinely nested subproblems) would directly connect the theoretical framework to empirical evidence. Currently the advantage remains theoretical.

---

## Removed Points

- **"FUNSEARCH uses a completely different mechanism than NDPS/LEAPS/PSM"** — Removed. The paper is clear this is a proof-of-concept about programmatic *representations* (outputting code), not about the specific synthesis methods in the re-evaluation. The reviewer's framing conflates method with representation; the paper does not claim NDPS/LEAPS could produce BFS.
- **"Three runs is not a meaningful evaluation"** — Removed as a weakness but retained as a Nice-to-Have. The paper explicitly calls this a proof-of-concept and is transparent about the limited scale; the reviewer demands more evidence than what a proof-of-concept is intended to provide.
- **"The NetHack example is mentioned but not tested"** — Demoted to Nice-to-Have, since the paper's memory-scaling argument is a theoretical contribution, and requiring experiments on all mentioned domains exceeds the paper's stated scope.
- **"Different neural architectures across benchmarks"** — Removed. The paper explains that DDPG, PPO, and DQN were each chosen based on preliminary experiments showing which worked best for each domain. This is standard practice.

---

## Novel Insights

The reviews surface that the paper's main weakness is not in its KAREL experiment (which is strong) or its conceptual framework (which is useful), but in the gap between the strength of its headline claim and the unevenness of the evidence supporting it across the three benchmarks. The TORCS asymmetry and PARKING ambiguity together mean the paper's central empirical result is: on one benchmark (KAREL) the confound hypothesis is convincingly demonstrated; on a second (TORCS) the evidence is suggestive but the comparison is not fully controlled; on a third (PARKING) the data is inconclusive. This pattern suggests the paper would be more accurately framed as *a clear demonstration that at least one major benchmark's reported advantage was confounded* rather than *a uniform debunking across all three benchmarks*. The real contribution—identifying confounds and providing a framework—does not depend on all three benchmarks being equally clean, but the current presentation implies a uniformity that the evidence does not fully support.

---

## Suggestions

1. **TORCS:** Either run NDPS with β=0.5 (so both methods use the same reward) or acknowledge explicitly that the comparison changes two variables at once (reward function and representation). Report the overall generalization rate including seeds that failed training.
2. **PARKING:** Reframe the abstract to say "the gap is narrower than previously reported" or "neither method generalizes reliably" rather than "match or exceed."
3. **KAREL HARVESTER:** Add a brief analysis of why this task resists generalization, connecting it to the expressivity/discoverability framework.
4. **Proof-of-concept:** Expand to multiple maze sizes and more trials to strengthen the memory-scaling thesis.

---

## Score and Decision

This paper makes a meaningful conceptual contribution (expressivity/discoverability framework), presents one convincing re-evaluation (KAREL), and identifies a genuinely useful direction for future work (memory-scaling advantage). However, the headline claim is unevenly supported: the TORCS comparison has uncontrolled asymmetries, and the PARKING results are genuinely ambiguous. The overclaim in the abstract relative to the evidence is a non-trivial presentation issue.

With revisions that address the asymmetric comparison and temper the claims, this would be a solid paper. In its current form, the contribution is above the acceptance threshold but the evidence is not uniformly strong.

**Score:** 6  
**Decision:** Accept

MY FINAL SCORE: <score>6</score>
MY FINAL DECISION: <decision>Accept</decision>