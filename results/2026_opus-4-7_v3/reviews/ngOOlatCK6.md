Now let me read the experimental section more carefully to check the footnote claims and methodology:I've now carefully read the entire paper and verified the reviewer's claims. Let me produce my draft review.Now let me proceed with calibration. Round 1 — Bracketing:Let me read a few key anchors for calibration:Now I have sufficient calibration data. Let me construct my final review.

**Round 1 Bracket Analysis:**

- **Score ≤1.5**: Clearly much weaker papers (incomplete, fundamentally flawed). The mGISS paper is far above this.
- **Score 3.0-3.5**: Causal modeling papers with significant methodological issues. The mGISS paper is substantially stronger.
- **Score 5.0** (IPayPEGwdE, "Learning Good Interventions in Causal Contextual Bandits"): Directly comparable causal bandits paper, rejected with uniform 5s. Had binary restrictions, limited experiments, weaker theory. The mGISS paper is clearly stronger with more elegant theoretical results.
- **Score 6.0** (YcW8i9VCf5, "Adversarial CBO"): Accepted with uniform 6s. Has regret bounds but naming/framing issues. The mGISS paper's theoretical contribution is at least as clean.
- **Score 7.0** (u63OVngeSp, "Deriving Causal Order from Single-Variable Interventions"): Accepted with scores 5,8,8,6,8. Strong theory+algorithm paper with some reviewer disagreement. Comparable in theoretical quality to the mGISS paper.
- **Score 8.0** (xByvdb3DCm, "When Selection meets Intervention"): Unanimous 8s. More broadly impactful graphical framework. The mGISS paper is probably slightly below this level.

**Initial bracket: 6.0 to 7.5**

---

## Summary
This paper characterizes the minimal set of nodes (mGISS) guaranteed to contain the optimal single-node conditional intervention in a causal bandit setting without latent confounders. The key contributions are: (1) an equivalence between conditional-intervention superiority in probabilistic SCMs and atomic-intervention superiority in deterministic SCMs (Proposition 4); (2) a graphical characterization of the mGISS via Λ-structures (Theorems 12–13); and (3) a linear-time C4 algorithm to compute the mGISS. Experiments on random and real-world graphs demonstrate significant search-space reduction and improved bandit convergence.

## Strengths

- **The equivalence result (Proposition 4) is elegant and non-obvious.** Showing that conditional-intervention superiority in a probabilistic SCM is equivalent to atomic-intervention superiority in a deterministic SCM is a genuinely surprising structural reduction. It collapses optimization over arbitrary policy functions $g$ into pointwise optimization, and this insight is cleanly exploited throughout the paper's proofs. This is the kind of structural insight that elevates a theoretical contribution.

- **The Λ-structure characterization (Theorem 12) provides a simple, non-recursive graph-theoretic criterion.** Rather than leaving the mGISS defined only through the iterative LSCA closure (Definition 9), the paper shows it equals the set of nodes forming a Λ-structure over (Pa(Y), Pa(Y)) — a single, checkable condition. This is illustrated well in Figure 2a and represents a meaningful simplification over the recursive definition.

- **The C4 algorithm (Algorithm 1) is genuinely efficient and well-designed.** Running in O(|V|+|E|) time via a single reverse-topological-order pass using the connector concept (Definition 14), the algorithm is concise (11 lines), its correctness argument via Lemma 15 is well-structured, and the connector concept itself is a clean graph-theoretic idea that a node belongs to the mGISS iff its children have multiple distinct connectors.

- **The paper is carefully positioned relative to prior work.** The distinction from Lee & Bareinboim (2018) is precisely articulated: the single-node conditional-intervention setting is non-comparable to the multi-node hard-intervention setting. The argument that single-node interventions make the search-space characterization *harder* (since one cannot simply intervene on all parents of Y) is convincingly illustrated in Section 2.

- **Intuition-building in Section 4 is effective.** The progression through Figures 1a–1d, showing why successive refinements of the heuristic fail and motivating the LSCA closure, is well-paced and makes the non-trivial Λ-structure characterization accessible.

## Weaknesses

### Fatal
None

### Major
None

### Minor

- **Regret computed against an estimated, not true, optimal arm (Section 6, footnote 11).** The paper states: "For the computation of regret, we use the estimated best arm, defined as the arm that most runs concluded to be the best at the end of training." Since the full SCMs for the bnlearn datasets are known, the true optimal node and policy *can* be computed (at least for discrete, small-domain variables). Using a mode estimate across runs introduces potential bias: if the estimate is wrong, regret is systematically underestimated, and if brute-force and mGISS conditions converge to different "estimated best" arms, regret curves are computed against different references and become incomparable. This is a real methodological issue in the experimental evaluation, though it does not affect the paper's primary theoretical contributions.

- **Experiments do not disentangle mGISS-specific benefit from generic arm-count reduction (Section 6).** Any bandit algorithm over $k$ arms converges faster than the same algorithm over $k' > k$ arms, provided the optimal arm is retained. The experiments compare only brute-force (all ancestors) vs. mGISS, without a control condition such as a random subset of nodes of the same size as the mGISS. Such a control would demonstrate that the *identity* of retained nodes, not just the *count*, drives the improvement — which is the paper's substantive claim.

- **Sensitivity to target node choice is not explored.** All experiments set Y as the node with the most ancestors. While this is reasonable for demonstrating maximum pruning potential, reporting mGISS sizes across multiple target nodes (or across all possible targets) would give a more complete picture of the method's practical utility.

### Trivial
None

## Nice-to-Haves

- **Discussion of the gap between worst-case mGISS and instance-specific optimal.** The mGISS is defined as the minimal set that works for *all* SCMs with graph $G$ (Definition 5). For any specific SCM, the set of nodes worth testing could be much smaller. A brief analysis or example quantifying this gap would help practitioners calibrate expectations.

- **Testing with additional bandit algorithms** (e.g., Thompson Sampling) would strengthen empirical generality, though the paper honestly acknowledges (Section 7) that no specialized conditional causal bandit algorithm currently exists.

- **Brief discussion of computational feasibility of CondIntUCB with large conditioning sets** would better scope the practical claims. Footnote 10 uses $\mathbf{Z}_X = \text{An}(X) \setminus \{X\}$, and running a separate UCB instance per realization of $\mathbf{Z}_X$ is tractable only for small, discrete-domain conditioning sets.

## Removed Points

*These points are flagged to be removed, treat them with caution.*

- **"The conditioning set assumption may be restrictive"** — The paper explicitly discusses this assumption in Section 2 (lines on $\text{An}(X) \setminus \{X\} \subseteq \mathbf{Z}_X$), footnote 3 clarifies they are not claiming all ancestors *need* to be in $\mathbf{Z}_X$ but that they *can* be, and the paper explicitly scopes to no-latent-confounders. The computational scalability of CondIntUCB is a downstream algorithm concern, not a weakness of the mGISS characterization itself. Moved to nice-to-have.

- **"The improvement from mGISS pruning is expected"** — The reviewer's framing that the benefit is "to a first approximation, expected" conflates the *guarantee* (that the optimal arm is retained) with the *trivial observation* that fewer arms converge faster. The paper's contribution is proving the guarantee, and the bandit improvement is a natural consequence of a correct theoretical result. This is a strength, not a weakness.

- **"The claim that single-node interventions make the problem more challenging is stated somewhat imprecisely"** — The reviewer suggests the paper claims universal difficulty, but in fact Section 2 specifically states "restricting to single-node interventions in fact makes the problem more challenging" in the context of characterizing the minimal search space, which is precisely what the paper studies. The distinction between the search-space characterization and the bandit problem itself is implicit but clear from context.

## Novel Insights

The core novel insight is the equivalence between conditional-intervention superiority in probabilistic SCMs and atomic-intervention superiority in deterministic SCMs (Proposition 4). This structural reduction is genuinely surprising — it shows that the complexity of optimizing over arbitrary policy functions collapses to pointwise optimization over values, allowing the entire characterization to be carried out through deterministic reasoning. The Λ-structure characterization (Theorem 12) as a non-recursive equivalent of the LSCA closure is a clean graph-theoretic contribution, and the connector concept (Definition 14) underlying the C4 algorithm is an elegant algorithmic idea.

## Suggestions

- Compute true optimal arm regret from the known bnlearn SCMs to make regret curves fully interpretable.
- Add a random-subset control of equal size to mGISS in bandit experiments to disentangle arm-count reduction from node-identity benefit.
- Report mGISS sizes across multiple (or all) possible target nodes per graph, not just the node with most ancestors.
- Add a brief remark about how much larger mGISS can be than the instance-specific optimal set, perhaps with one worked example.

## Score and Decision

**Anchor comparison (all rounds):**

| Anchor | Path | Avg Score | Round | Comparison to paper under review |
|--------|------|-----------|-------|----------------------------------|
| KL Divergence GFlowNets | Uj0h13lVrR | 1.0 | R1 | Far weaker: incomplete, fundamentally flawed |
| All Pairs Minimax Path | bEgDEyy2Yk | 1.0 | R1 | Far weaker: trivial contribution, no novelty |
| Financial Markets NN | nSDOkm0SKo | 1.0 | R1 | Far weaker: hypothetical scenario, pseudoscience |
| Clothing-Irrelevant ReID | 5lUdTogEL3 | 1.0 | R1 | Far weaker: unrelated, low contribution |
| Causal BO Unknown Graphs | MVpvyeVeyI | 3.4 | R1 | Weaker: less rigorous theoretical foundation |
| Sparse Causal Model | fSxiromxAq | 3.0 | R1 | Weaker: less focused, less rigorous |
| Best of Both Worlds Causal | AvXrppAS2o | 3.0 | R1 | Weaker: restrictive assumptions, weaker theory |
| LLM-Supervised CSL | JzFLBOFMZ2 | 3.2 | R1 | Weaker: unreliable constraints, less rigorous |
| Causal Contextual Bandits Adaptive | IPayPEGwdE | 5.0 | R1 | Directly comparable, weaker: binary restrictions, less elegant theory, limited experiments |
| Root Cause Analysis | 2pEqXce0um | 4.5 | R1 | Different problem, weaker contribution |
| Causal Graph via Distributional Invariance | Lxst78Rrwj | 5.0 | R1 | Different problem, comparable rigor but less novel insight |
| Fast Conditional Intervention RL | oVVLBxVmbZ | 5.25 | R1 | Different problem (recourse), less focused theory |
| Adversarial CBO | YcW8i9VCf5 | 6.0 | R1 | Comparable: solid theory+algorithm, but naming/framing issues; mGISS paper has cleaner core results |
| Deriving Causal Order | u63OVngeSp | 7.0 | R1 | Comparable: strong theory+algorithm, mixed reviews; mGISS paper has comparable theoretical elegance but narrower scope |
| Robust Agents Causal Models | pOoKI3ouv1 | 5.75 | R1 | Different problem, broader but more contested (scores 8,1,6,8) |
| Causal Information Bottleneck | qac43AwuL9 | 6.0 | R1 | Different problem, comparable rigor |
| Selection meets Intervention | xByvdb3DCm | 8.0 | R1 | Stronger: broader impact, novel framework, unanimous high scores; mGISS is below this |
| Intervention Extrapolation | 3cuJwmPxXj | 8.0 | R1 | Stronger: broader scope, unanimous 8s |
| Hidden Cost of Waiting | A3YUPeJTNR | 8.0 | R1 | Different problem, broader societal implications |
| Root Cause Granger | k38Th3x4d9 | 8.0 | R1 | Different problem, broader applicability |
| Efficient Causal Discovery Latent | BZYIEw4mcY | 6.0 | R1 | Comparable: theory+algorithm, handles latent variables (broader scope) |
| Constraint-Free Structure Learning | KWO8LSUC5W | 5.6 | R1 | Weaker: constraint-free DAG learning, less novel theoretical insight |
| Causal Graph Latent Homologous | fGhr39bqZa | 6.0 | R1 | Comparable: clean theoretical contribution with graph-theoretic insight |

**Round 1 bracket: 6.0 to 7.5**

The paper under review is clearly stronger than the score-5.0 causal contextual bandits paper (IPayPEGwdE), which had binary restrictions, weaker theory, and limited experiments. It is comparable to or slightly stronger than the score-6.0 adversarial CBO paper (YcW8i9VCf5), which had comparable algorithmic sophistication but naming/framing issues. It is comparable to the score-7.0 causal order paper (u63OVngeSp), which had strong theory but mixed reviewer reception. It falls below the score-8.0 papers, which had broader impact and near-unanimous acclaim.

The paper's theoretical contribution — particularly the surprising equivalence result (Proposition 4), the clean Λ-structure characterization (Theorem 12), and the linear-time algorithm — is elegant, correct, and well-presented. The experimental weaknesses (estimated regret, no random-subset control) are real but minor, affecting only the supplementary empirical validation, not the core claims. The scope is narrow (single-node, no latent confounders) but honestly stated and justified as a necessary stepping stone.

Balancing the strong theoretical contribution against the narrow scope and minor experimental issues, the paper sits solidly in the 6.5–7.0 range. The elegance and correctness of the theory, combined with good presentation and honest scoping, place it at the upper end.

**Score: 7.0**
**Decision: Accept**

MY FINAL SCORE: <score>7.0</score>
MY FINAL DECISION: <decision>Accept</decision>