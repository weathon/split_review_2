Here is the final consolidated review.

---

## Summary

This paper addresses Online Inventory Optimization (OIO), proposing algorithms that achieve near-optimal dynamic regret guarantees of $\tilde{\mathcal{O}}(\sqrt{L_{\max}(1+P_T)T})$ — the first such guarantee for the OIO setting. The key technical contribution is a two-stage projection strategy that connects OIO to Smoothed Online Convex Optimization (SOCO), transforming the carryover stock constraint into a switching cost. The paper also provides a matching $\Omega(\sqrt{L_{\max}T})$ lower bound that resolves an open question from prior work.

## Strengths

- **First dynamic regret guarantee for OIO**: Theorem 4 provides a near-optimal $\tilde{\mathcal{O}}(\sqrt{L_{\max}(1+P_T)T})$ dynamic regret bound. The paper motivates this contribution with a concrete example (Section 1, lines 19–25) showing that static-regret algorithms incur $\Omega(T)$ regret under fluctuating demand while a dynamic comparator achieves zero — making clear why the extension matters.

- **Matching lower bound resolving an open question**: Theorem 5 proves a $\Omega(GD\sqrt{L_{\max}T})$ lower bound matching the upper bound up to logarithmic factors, directly addressing the open question raised by Hihat et al. (2023). Corollary 1 provides an interesting cross-domain implication for SOCO.

- **Novel reduction from OIO to SOCO**: Lemma 1 bounds the gap between the projected decisions $y_t$ and the base learner's decisions $\hat{y}_t$ by a switching-cost term proportional to $L_{\max}$. Remark 4 correctly identifies that this eliminates the dynamic carryover-stock difficulty that previously prevented two-layer meta-algorithms for OIO. This is a genuinely new technical idea.

- **Clear exposition of the core difficulty**: Section 1 provides a well-reasoned explanation of why a standard two-layer meta-algorithm fails in OIO (carryover stock violates the base learner's assumption), making the contribution easy to follow.

## Weaknesses

### Major

- **The $L_{\max}$ condition sits uneasily with the adversarial framing**: The paper states it considers an "adversarial environment" (line 124), but $L_{\max}$ (Definition 1) is a deterministic condition on the demand sequence: every item must collectively sell at least $D$ units within every window of $L_{\max}$ rounds. A fully adversarial environment can make $L_{\max} = \Omega(T)$ by setting demands to zero for long stretches, rendering the sublinear regret guarantee vacuous. The paper is honest that "sublinear regret cannot be achieved when $L_{\max} = \Omega(T)$" (line 144), but describes requiring $L_{\max}=o(T)$ as "mildly constraining" periods of small demand (line 144) — this understates the condition, which rules out any item with extended low-demand periods. The probabilistic extension (Remark 3) partially mitigates this for stochastic settings, but the main text is framed as adversarial. Readers should have a clearer understanding of when the guarantee is practically meaningful.

- **The $\sqrt{L_{\max}}$ static regret improvement is a cross-setting comparison, not a direct improvement within the same setting**: The abstract claims "an improvement of $\sqrt{L_{\max}}$ for the static regret upper bound in existing studies" without qualifying that nearly every prior work in Table 1 operates under a different setting — i.i.d./independent demand (vs. adversarial), single-item (vs. multi-item), or interval/convex capacity constraints (vs. linear). The most directly comparable prior work (Hihat et al. 2023, [7]) uses a more general convex constraint, so the improvement partly reflects the paper's more restrictive linear constraint rather than algorithmic technique alone. The paper acknowledges this distinction in Remark 2 but the framing in the abstract and introduction does not carry this qualification, risking misleading readers about the nature of the improvement.

### Minor

- **Linear capacity constraint is a genuine restriction relative to the closest prior work**: The paper assumes a linear capacity constraint (Eq. 3), a special case of the convex constraint used by Hihat et al. (2023). The paper acknowledges this (Remark 2, Section 6) but does not explain what technical difficulty prevents extension — stating only that the linear assumption "is critical to the proof of Lemmas 5 and 6." A brief explanation of the barrier would help readers assess the scope for future extension.

- **No discussion of when $L_{\max}$ is small enough for practical relevance**: The guarantee depends critically on $L_{\max}$ being $o(T)$, yet there is no discussion of what real-world demand patterns satisfy this, or how $L_{\max}$ relates to practical inventory metrics like turnover rates. Such a discussion would significantly strengthen the paper.

### Trivial

None.

## Nice-to-Haves

- A synthetic experiment confirming the $\sqrt{L_{\max}T}$ scaling of the dynamic regret would strengthen the paper, though it is not required for a purely theoretical contribution.
- The presentation of SOGD (Algorithms 4–5) is dense; since it is inherited from prior work (Zhang et al. 2022a), the algorithmic details could be streamlined with the guarantee cited and the details moved to the appendix.

## Removed Points

The following points from the reviewers were removed after cross-checking against the paper:

- **"No discussion of the relationship between $L_{\max}$ and $D$ in the lower bound"** — The informal Theorem 1 statement omits constant factors $G$ and $D$, which is standard practice for informal statements. The formal theorems include these factors.
- **"The $T \geq \dots$ assumptions in Theorems 3 and 4 are not discussed"** — These are mild technical conditions that hold for nontrivial horizons. The paper discusses the condition for the overhead term at line 325.
- **"The overhead term $L_{\max}\log L_{\max}$ could dominate for large $L_{\max}$"** — The paper explicitly addresses this condition at line 325 ("subdominant for a broad range of horizons, e.g., $T > L_{\max}\log^2 L_{\max}$").
- **"No experiments"** — Not a requirement for a theoretical paper. Moved to nice-to-have.
- **Criticism that the $\sqrt{L_{\max}}$ improvement claim is "not an apples-to-apples comparison" is retained** in the Major weaknesses section above, but the harsh critic's framing of this as a "methodological gap" is softened: the paper provides sufficient context (Table 1, Remark 2) for an informed reader to evaluate the comparison, so the issue is one of framing rather than substance.

## Novel Insights

Beyond the paper's own contributions, the review process surfaces one notable observation: the connection between OIO and SOCO via the projection analysis (Lemma 1) reveals that the carryover stock constraint in inventory systems is structurally equivalent to a switching cost on the base learner's decisions. This insight — that a stateful inventory constraint maps to a dynamical penalty on the underlying OCO decisions — could potentially apply to other stateful online optimization problems beyond inventory management, such as queueing systems, battery storage, or bandwidth allocation. This cross-domain connection is worth highlighting as it suggests broader applicability of the SOCO framework.

## Suggestions

1. In the abstract and introduction, qualify the $\sqrt{L_{\max}}$ improvement claim to clarify that the comparison spans different settings (capacity constraint type, demand model). A phrase like "under a linear capacity constraint, our static regret improves the dependence on $L_{\max}$ from $L_{\max}$ to $\sqrt{L_{\max}}$ relative to analogous existing results" would be more precise.
2. Add a paragraph discussing when $L_{\max}$ is small enough for the bound to be meaningful, connecting it to practical inventory metrics (e.g., minimum guaranteed turnover rate). This would sharpen the practical relevance.
3. Explain briefly what technical barrier prevents extending the linear capacity constraint to general convex constraints — even a paragraph in the conclusions would help.
4. Reframe the description of $L_{\max} = o(T)$: rather than "mildly constrains" periods of small demand, be more precise about what demand patterns it rules out (every item must sell at least $D$ units within every window of $L_{\max}$ rounds).

## Score and Decision

The paper makes a genuine theoretical contribution: first near-optimal dynamic regret for OIO, a clever OIO-to-SOCO reduction, and a matching lower bound that resolves an open question. None of the weaknesses are fatal — they concern framing and scope rather than technical correctness. However, the $L_{\max}$ condition fundamentally restricts the adversarial framing, and the static regret improvement claim would benefit from more precise qualification. These issues are addressable in revision and do not undermine the core contribution. The paper is a solid borderline accept.

MY FINAL SCORE: <score>6</score>
MY FINAL DECISION: <decision>Accept</decision>