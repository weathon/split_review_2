## Summary

This paper addresses real-time pursuit-evasion under partial observability on graphs. It proves that a standard DP algorithm for Markov PEGs maintains optimality under asynchronous evader moves (Theorem 2), then proposes a belief preservation mechanism to extend DP policies to partial observability. These components are embedded into the EPG reinforcement learning framework to train GNN-based pursuit policies that generalize zero-shot to unseen graphs. Empirical results show sub-0.01s inference times on large graphs and consistent outperformance over PSRO.

## Strengths

1. **Genuine theoretical extension of DP to asynchronous moves.** Theorem 2/Corollary 1 prove optimality of the DP distance table when the evader sees the pursuer's move and best-responds (Stackelberg framing). This is a sound and non-trivial theoretical result (Section 3.1, lines 117–129).

2. **Clear zero-shot outperformance over PSRO.** Table 2 shows consistent superiority across 10 real-world graphs against DP_async opponents (e.g., 0.95 vs. 0.04 on Times Square, 0.82 vs. 0.24 on Big Ben). The comparison favors the baseline — PSRO is trained directly on each test graph while the proposed method is zero-shot — making the outperformance stronger (lines 244–268).

3. **Real-time inference convincingly demonstrated at scale.** Table 3 reports RL inference of ~0.008–0.01s vs. DP computation of 6–139s on large graphs (n=744–2065). This directly supports the core practical claim (lines 272–288).

4. **Belief mechanism validated through ablation.** Table 4 shows monotonic degradation when belief update frequency decreases (every step → every 2/3 steps) and improvement when the true opponent policy is known. This provides concrete evidence the mechanism is doing useful work (lines 292–308).

5. **Clean complexity analysis.** The O(n²m) inference bound vs. Õ(n^{m+1}) for DP recomputation under changing graph structures formally grounds the real-time claim (Section 4.2, lines 197–201).

## Weaknesses

### Major

None.

### Minor

1. **Missing EPG as a direct baseline.** The paper presents R2PS as extending EPG to partial observability, but never compares against EPG (even adapted to partial observability by feeding it partial information). Since the PSRO baseline is from a different method family, it is hard to isolate how much of the gain comes from the belief mechanism vs. the EPG cross-graph framework vs. the GNN+SAC architecture. Adding an EPG-adapted baseline would directly isolate the contribution of the belief mechanism.

2. **PSRO implementation is underspecified.** The paper states PSRO is trained on each test graph for 10 iterations × 10000 episodes (lines 240–261), but does not describe PSRO's policy representation (tabular? neural? same GNN architecture?), inner RL algorithm, observation model during training, or whether convergence was checked. This makes the comparison difficult to assess fully.

3. **"Worst-case robust" used without a precise definition.** The paper uses this phrase to cover robustness to graph structures, opponent policies, and partial observability, without a single precise definition. The strongest test (BR_async in Table 2) shows success rates as low as 0.10–0.20 on some graphs (Hollywood, Sagrada Familia), which is honestly reported but makes "worst-case robust" somewhat imprecise as a framing.

4. **Theoretical guarantee for partial observability is limited.** Lemma 2 only covers the degenerate case (Pos always singleton). The paper acknowledges D(·) becomes "optimistic" under partial observability (line 234). The contribution statements in the introduction could more cleanly separate what is proved (asynchronous-move optimality) from what is empirical (partial observability extension).

### Trivial

- Results in Tables 1–4 are reported as point estimates without variance or confidence intervals. With 500 tests per condition this does not threaten conclusions, but error bars would improve presentation.

## Nice-to-Haves

- Investigating whether learning the evader's policy (rather than assuming uniform in Eq. 7) during RL training improves performance, since Table 4's "known opponent" column suggests it would.
- Testing on graphs with more diverse characteristics (higher average degree, larger diameter) to better scope the generalization claim.
- Clarifying the "continual partial observability" distinction introduced around Eq. 5–6 (lines 147–148), as the current definition is informal.

## Removed Points

These points from the input review are removed or downgraded with justification:

- **"Missing EPG baseline is a critical omission"** — Downgraded from critical to minor. EPG is a perfect-information method; the paper's core contribution is the partial observability extension. Comparing against PSRO (a standard game RL method) is a reasonable baseline choice. The EPG baseline would be informative but its absence is not fatal.

- **"Admission that D(·) is optimistic undermines contribution claims"** — Removed. The paper is appropriately transparent about what is proved vs. empirical. The contribution list in Section 1 (lines 27–31) accurately separates "prove" (asynchronous optimality) from "design" and "verify" (partial observability).

- **"Belief update uses uniform evader policy despite training against DP-optimal evader"** — Removed. The paper explicitly acknowledges this design choice (lines 157–158: "since the pursuer side cannot obtain the evader's policy ν when no prior knowledge is available, ν(v) is set to be a uniform distribution").

- **"Capture condition (adjacency) is non-standard"** — Removed. The paper is free to define its termination condition and does so clearly (line 230).

- **"Section-by-section notes"** (Algorithm 1 line 78, "continual" definition, etc.) — Removed. These are line-level observations appropriate for discussion but not substantive weaknesses.

## Novel Insights

The harsh critic's observation that the paper's theoretical contribution (asynchronous-move optimality) and its practical contribution (partial observability heuristic) sit at different levels of rigor, and should be cleaned separated in the contribution framing, is a genuinely useful insight that could improve the paper. The specific suggestion of using EPG as a baseline to isolate the belief mechanism's value is also well-targeted.

## Suggestions

1. Add EPG as a baseline (adapted to partial observability by feeding it the belief state or null observations for unobserved nodes) to directly isolate the contribution of the belief mechanism.
2. Provide details on the PSRO implementation: policy architecture, inner RL algorithm, observation model, and convergence criteria.
3. Add a precise definition of "worst-case robust" as scoped to the paper's experimental setup.
4. Add confidence intervals or error bars to the experimental results.
5. Cleanly separate the theoretical claim (Theorem 2: asynchronous-move optimality under full observability) from the heuristic extension to partial observability in the contribution framing.

---

**Calibration Anchors (all rounds)**

| Path | Avg Score | Round | Comparison |
|------|-----------|-------|------------|
| bEgDEyy2Yk.md (minimax path) | 1.00 | R1 | Pure implementation paper; our paper is far more substantive |
| 5kMwiMnUip.md (LLM jailbreaking) | 1.40 | R1 | Unrelated topic, low quality; not comparable |
| VRRuYBaq9u.md (GPO POMDP) | 3.25 | R1 | Weaker framing and experiments than our paper |
| iGHPVbttMs.md (PSRO cyclical chaos) | 3.40 | R1 | PSRO analysis paper; less substantive contribution |
| mxkm1Pr2PM.md (GNN as mean field game) | 5.33 | R1 | Comparable rigor but different domain; our paper has stronger empirical validation |
| voLFfrWzFI.md (decision-focused learning) | 4.75 | R1 | Less complete contribution than our paper |
| 99tKiMVJhY.md (Dec-POMFC) | 6.33 | R1 | Similar tier: theory + MARL under partial observability. Our paper has better real-time demonstration |
| Q00CO1Tm6M.md (POMDP hardness) | 5.75 | R1 | Theory-only; our paper is more applied |
| Kd5nJUgeW4.md (DRDA, POSG solver) | 7.00 | R1, R2 | Stronger theory but similar paper structure. Our paper's practical real-time claims are a distinguishing strength |
| TyZhiK6fDf.md (Dyna-PSRO) | 5.60 | R1 | PSRO variant with world models. Broader weaknesses than our paper |
| WfxPVtYRlL.md (GNNs Hogwild) | 6.25 | R2 | GNN asynchrony theory + experiments. Similar contribution depth |
| 7YKV7zkNpX.md (ACCES games) | 6.50 | R2 | New game class with theory + experiments. Comparable in scope and execution |
| zwU9scoU4A.md (MFG on sparse graphs) | 6.67 | R2 | Graph-based game theory + learning. Similar tier |
| C371MUzjBl.md (DAG column generation) | 6.25 | R2 | Team game algorithm. Mixed reviews, similar to our paper |
| PPTE1DL4Li.md (MF optimal stopping) | 6.00 | R2 | Theory + deep learning. Comparable mixed-quality profile |

**Round 1 bracket**: The paper fits in the 5.5–7.5 band. Papers below 5.5 have substantially weaker contributions; papers above 7.5 are stronger accept-level work.

**Round 2 narrowing**: Among the 5.5–7.5 anchors, our paper aligns most closely with the 6.00–6.67 range (GNNs Hogwild at 6.25, ACCES at 6.50, MFG on sparse graphs at 6.67). The paper has a genuine theoretical result, clear empirical validation, and a practical real-time demonstration — but the missing EPG baseline and underspecified PSRO implementation keep it below the DRDA-level 7.00 threshold.

## Score and Decision

MY FINAL SCORE: <score>6.5</score>
MY FINAL DECISION: <decision>Accept</decision>