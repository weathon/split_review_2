## Summary

This paper addresses Online Inventory Optimization (OIO) in non-stationary environments. It proposes algorithms achieving $\tilde{\mathcal{O}}(\sqrt{L_{\max}T(1+P_T)})$ dynamic regret for OIO — the first dynamic regret guarantee for this problem — by drawing a clean connection between OIO and Smoothed Online Convex Optimization (SOCO) via a two-stage projection strategy. It also improves the static regret bound from prior $\mathcal{O}(L_{\max}\sqrt{T})$ to $\tilde{\mathcal{O}}(\sqrt{L_{\max}T})$ and provides a matching $\Omega(\sqrt{L_{\max}T})$ static lower bound.

## Strengths

1. **Novel conceptual connection between OIO and SOCO.** Lemma 1 and Remark 4 show that the carryover stock constraint introduces a switching cost in the base learner's decisions, transforming the OIO dynamic regret problem into a SOCO problem. The two-stage projection that enables this is simple, clean, and technically non-trivial.

2. **First dynamic regret guarantee for OIO.** Prior OIO work focused exclusively on static regret. The paper correctly motivates the insufficiency of static regret under demand fluctuations (Section 1, linear demand example) and provides the first sublinear dynamic regret bound for this setting.

3. **Improved static regret bound.** The paper achieves $\tilde{\mathcal{O}}(\sqrt{L_{\max}T})$ vs. prior $\mathcal{O}(L_{\max}\sqrt{T})$, an improvement of a $\sqrt{L_{\max}}$ factor. This is a genuine quantitative advance over a line of work.

4. **Matching lower bound for the static case.** Theorem 5 gives $\Omega(\sqrt{L_{\max}T})$, showing the static regret bound is tight up to log factors. The lower-bound argument also yields a new lower bound for SOCO (Corollary 1), providing an interesting cross-connection.

## Weaknesses

### Major

1. **The "near-optimal dynamic regret" claim is not fully supported by the provided lower bounds.** The paper claims "near-optimal dynamic regret" (abstract, line 33, line 349) and Theorem 1 gives $\tilde{\mathcal{O}}(\sqrt{L_{\max}T(1+P_T)})$. However, the lower bound (Theorem 5) is $\Omega(\sqrt{L_{\max}T})$ for the *static* case (fixed comparator $u$), not for the dynamic case with path-length $P_T$. The paper references the standard OCO dynamic lower bound $\Omega(\sqrt{(1+P_T)T})$ from Zhang et al. (2018b) (line 331), but this does not incorporate $L_{\max}$. The best known combined lower bound is $\Omega(\max\{\sqrt{L_{\max}T}, \sqrt{(1+P_T)T}\})$, while the upper bound is $\tilde{\mathcal{O}}(\sqrt{L_{\max}(1+P_T)T})$, which can be $\sqrt{L_{\max}}$ or $\sqrt{1+P_T}$ times larger than the max lower bound depending on the regime. The paper does not address this gap, making the "near-optimal" claim for dynamic regret overstated. The optimality is well-supported only for the static component.

### Minor

2. **The "adversarial environment" framing (line 124) would benefit from immediate qualification about $L_{\max}$.** The paper defines $L_{\max}$ (Definition 1) as the minimum length such that *for every item $i$ and every starting time $t$*, the cumulative demand over $[t, t+L_{\max}-1]$ reaches at least $D$. This is a strong uniform condition on the demand process. The paper is transparent about its necessity (line 144: sublinear regret is impossible when $L_{\max}=\Omega(T)$), and the condition is common in the inventory literature. However, stating the setting as "adversarial" without immediately noting that the adversary is constrained by $L_{\max}=o(T)$ could lead readers to overestimate the algorithm's applicability to environments with prolonged demand droughts, seasonality, or product lifecycles with slow periods.

3. **The $\sqrt{L_{\max}}$ improvement over prior static regret is partly enabled by the different (more restrictive) capacity constraint.** The paper improves the static regret from $\mathcal{O}(L_{\max}\sqrt{T})$ (Hihat et al., 2023) to $\tilde{\mathcal{O}}(\sqrt{L_{\max}T})$. However, prior work used a general convex capacity constraint, while this paper uses a linear-sum constraint (Eq. 3). As the paper acknowledges (Remark 2, Section 6), the linear constraint is a special case of the convex constraint. The abstract and contributions (lines 9, 41) present the improvement without immediate caveat that the constraint differs, so the improvement cannot be attributed solely to algorithmic innovation. The paper's honest discussion in Remark 2 and the limitations section partially mitigates this, but the framing could still mislead a casual reader.

### Trivial

None.

## Nice-to-Haves

- A synthetic simulation verifying the regret bounds (e.g., on the linear demand example from the introduction) would increase confidence that the bounds are tight and the algorithm works as claimed. This is not required for a theory paper but would strengthen it.
- A discussion of what $P_T$ looks like in realistic demand scenarios would help practitioners gauge the bound's practical significance.
- A concrete numerical example contrasting the prior $\mathcal{O}(L_{\max}\sqrt{T})$ with the new $\tilde{\mathcal{O}}(\sqrt{L_{\max}T})$ for specific values of $L_{\max}$ and $T$ would help illustrate the practical significance of the improvement.

## Removed Points

- **"Theorem 2 relies on assumptions about the base learner that are not verified in the main text"**: The paper states at line 213 ("All omitted proofs are given in the appendix"). Deferring verification of technical conditions to the appendix is standard practice for conference papers, and the appendix content was stripped by the parser. Following the filtering rules, this is removed as it concerns missing appendix content.
- **"Section-by-section notes" about missing experiments, missing discussion of $P_T$ estimation, etc.**: Moved to Nice-to-Haves where appropriate. The paper's contribution is theoretical; lack of experiments is not a weakness in a theory paper.
- **Generic criticisms about comparison fairness in Table 1**: The paper clearly annotates the differences in setting (capacity constraint type, item count, loss function, demand model). No misleading claims were found beyond those already captured in Weakness 3.

## Novel Insights

The harsh reviewer's most incisive observation is that the paper's "near-optimal dynamic regret" claim rests on two separate lower bounds (one static-OIO-specific, one OCO-dynamic) that do not jointly account for both $L_{\max}$ and $P_T$ simultaneously. This gap between the upper bound $\tilde{\mathcal{O}}(\sqrt{L_{\max}(1+P_T)T})$ and the best known lower bound $\Omega(\max\{\sqrt{L_{\max}T}, \sqrt{(1+P_T)T}\})$ is a specific, well-defined open question that the paper does not acknowledge. Aside from this, the review's insights largely follow from careful reading of the paper's own framing and do not reveal deep issues beyond the paper's stated limitations.

## Suggestions

1. **Temper the "near-optimal" claim for dynamic regret** to reflect that optimality is established only for the static case and that the tightness of the dynamic regret bound remains an open question. Alternatively, provide a dynamic-regret lower bound that depends on both $L_{\max}$ and $P_T$, or explain why such a bound is difficult to obtain.

2. **Qualify the adversarial framing** at line 124 by stating: "We consider an adversarial environment subject to the minimum-demand condition that $L_{\max}=o(T)$ (Definition 1), without which sublinear regret is impossible." This aligns the presentation with the mathematics.

3. **When presenting the $\sqrt{L_{\max}}$ improvement**, add a brief parenthetical caveat noting the difference in capacity constraints: "improvement of $\sqrt{L_{\max}}$ over existing works (which considered general convex capacity constraints; we assume the linear constraint in Eq. 3)."

MY FINAL SCORE: <score>7</score>
MY FINAL DECISION: <decision>Accept</decision>