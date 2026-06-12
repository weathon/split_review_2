## Summary

This paper studies online inventory optimization (OIO), where a decision maker sequentially sets order-up-to levels subject to carryover stock and warehouse capacity constraints under adversarial demand. The main contribution is an algorithm achieving near-optimal dynamic regret of $\tilde{\mathcal{O}}(\sqrt{L_{\max}(1+P_T)T})$, where $L_{\max}$ is the maximum sell-out period and $P_T$ is the path-length of the comparator. The algorithm connects OIO to Smoothed OCO via a two-stage projection strategy, and a matching lower bound is provided for the static case, resolving an open question from prior work.

## Strengths

- **Clean theoretical contribution with matching bounds.** The paper establishes $\tilde{\mathcal{O}}(\sqrt{L_{\max}T})$ static regret upper and $\Omega(\sqrt{L_{\max}T})$ lower bounds (Theorems 4 and 5), demonstrating near-optimality. The $\sqrt{L_{\max}}$ improvement over existing $\mathcal{O}(L_{\max}\sqrt{T})$ bounds (Table 1) is significant when $L_{\max}$ is large.

- **Novel structural connection between OIO and SOCO.** Lemma 1, which shows the carryover stock constraint manifests as switching cost proportional to cycle length, is an elegant technical result. This transforms the fundamentally different-feasible-regions problem into a well-understood SOCO framework, making the problem tractable for dynamic regret analysis.

- **Addresses a genuine gap.** The paper clearly demonstrates (with a concrete example in Section 1) why static regret is inadequate for non-stationary inventory environments and why standard two-layer meta-algorithm architectures fail for OIO due to carryover stock constraints. The problem formulation and approach are well-motivated.

- **Generality of the framework.** The algorithm handles multi-item settings with convex losses and linear capacity constraints, subsuming several existing specialized results. The connection to SOCO also yields Corollary 1 (lower bound for SOCO as a byproduct).

## Weaknesses

### Fatal
None.

### Major

- **Complete absence of empirical evaluation.** For a method paper proposing a practical algorithm in an applied domain (inventory management), the lack of any numerical experiments is a significant shortcoming. Even synthetic experiments demonstrating (a) the dynamic regret scaling with $L_{\max}$ and $P_T$, (b) comparison with MaxCOSD on non-stationary instances, and (c) computational overhead of the doubling trick and SOGD meta-algorithm would substantially strengthen the paper. Without experiments, it is difficult to assess whether the constant factors, log terms, and the $O(T\log T)$ per-round computational cost render the algorithm practically viable.

- **Narrower problem setting than prior work.** The paper restricts to linear capacity constraints $\sum_i y_t^i \leq D$, whereas Hihat et al. (2023) handles general convex sets $\mathcal{C}$. The authors acknowledge this (Remark 2, Section 6) but state the linear constraint is "critical to the proof of Lemmas 5 and 6." This limitation is not trivial—it restricts applicability to settings where warehouse capacity is a simple sum constraint rather than more complex geometric or combinatorial constraints.

### Minor

- **The doubling trick introduces an unnecessary dependence on unknown $P_T$ in OGD.** Theorem 3 requires knowing $P_T$ a priori for the optimal learning rate. While SOGD (Theorem 4) removes this requirement, the paper does not discuss whether simpler parameter-free OGD variants (e.g., with adaptive learning rates) could avoid this without the full meta-algorithm machinery of SOGD. This matters for computational practicality.

- **The $L_{\max}\log L_{\max}$ additive term from the doubling trick.** While the authors claim this is subdominant when $T > L_{\max}\log^2 L_{\max}$, this condition could be restrictive for moderate time horizons relative to the sell-out period. A brief discussion of when this overhead matters would be helpful.

### Trivial
None.

## Nice-to-Haves

- Experiments on both synthetic and semi-realistic inventory instances, even simple ones, comparing dynamic regret trajectories of the proposed algorithm against MaxCOSD and OGD baselines under varying demand non-stationarity.
- Discussion of how to estimate $L_{\max}$ in practice or how the doubling trick performs empirically.
- A brief analysis of the implicit constraints on comparator sequences (e.g., when is $P_T$ small in practice).

## Novel Insights

The central novel insight is the identification of a structural equivalence between the carryover stock constraint in OIO and the switching cost in SOCO. Specifically, the two-stage projection of an unconstrained base learner's decision onto the carrystock-feasible set $\mathcal{C}(x_{t+1})$ introduces an $\ell_1$-norm switching cost proportional to the cycle length (Lemma 1). This is not a superficial analogy—the cycle length is itself bounded by $L_{\max}$ (Lemma 2), directly linking the inventory system's demand characteristics to the SOCO switching cost parameter. This connection elegantly resolves the fundamental difficulty that standard meta-algorithm approaches fail for OIO (as explained in Section 1), by instead leveraging SOCO algorithms that naturally handle switching costs. The matching lower bound (Theorem 5) further confirms that this connection captures the inherent structure of the problem rather than being an artifact of the proof technique.

## Suggestions

- Add a section with numerical experiments. At minimum, test on (i) a single-item Newsvendor setting with linearly increasing demand (as in the motivating example), (ii) a multi-item setting with fluctuating demand, and (iii) compare against MaxCOSD, OGD, and SOGD as standalone approaches. Report dynamic regret vs. time, and scaling with $L_{\max}$ and $P_T$.
- Discuss the gap between the linear constraint and general convex constraints, including whether partial extensions (e.g., to intersection of box constraints and a single linear constraint) are feasible.
- Provide a brief practical guideline: under what inventory management scenarios would a practitioner expect $L_{\max}$ to be moderate, and thus expect significant improvement over existing $L_{\max}\sqrt{T}$ bounds?

## Score and Decision

This is a theoretically strong paper that establishes clean, near-optimal regret bounds for a meaningful problem, with a novel structural insight (OIO-SOCO connection) and matching lower bounds. The theoretical contribution is genuine and significant. However, the complete absence of empirical evaluation is a notable weakness for a paper proposing algorithms in an applied domain, and the narrowing from general convex to linear constraints limits the scope relative to prior work. The paper sits comfortably above the median in theoretical quality but falls short of the strongest submissions due to the lack of experimental validation.

MY FINAL SCORE: <score>6.0</score>
MY FINAL DECISION: Accept