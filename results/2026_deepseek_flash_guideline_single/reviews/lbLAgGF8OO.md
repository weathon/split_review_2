Now let me write the final review.

## Summary

This paper introduces Dig-DEC, a model-free Decision-Estimation Coefficient that replaces the optimism principle of prior work [FGQ+23] with KL regularization driven purely by information gain. The core idea is conceptually sound: by augmenting the AIR objective with an additional KL information-gain term, the framework removes the need for optimism, enabling it to handle adversarial environments (hybrid MDPs with stochastic transitions and adversarial rewards) without explicit reward estimators. The paper provides a general algorithmic framework (Algorithm 1) with a mirror-descent analysis, bounds on the Dig-DEC for several canonical settings (bilinear classes, Bellman-Eluder dimension, coverable MDPs), and a comparison showing that Dig-DEC ≤ optimistic DEC + η (Theorem 13) with a strict improvement example (Theorem 14).

## Strengths

1. **Conceptual advance (Section 4, Eq. 7–8):** Replacing optimism with KL regularization + information gain is a principled improvement over the optimistic DEC of [FGQ+23]. The mirror-descent analysis (line 153) provides a cleaner and more flexible proof technique than the "constructive minimax theorem" of prior work, and it naturally generalizes the AIR framework of [XZ23, LWZ25].

2. **Theorem 13 + Theorem 14 (Section 6):** Together these show Dig-DEC ≤ o-dec + η (so it is never substantially larger than optimistic DEC) and give an explicit 3-armed bandit example where optimistic DEC incurs Ω(√T) regret while Dig-DEC achieves constant regret. This cleanly demonstrates strict improvement in a concrete setting.

3. **Scope of the framework:** The paper covers bilinear classes, MDPs with bounded Bellman-Eluder dimension, and coverable MDPs under a single umbrella, and claims the first model-free regret bounds for hybrid MDPs with bandit feedback. The breadth is impressive, and the unified treatment is a genuine contribution.

## Weaknesses

### Fatal
None.

### Major

1. **Rate inconsistencies between the stated formula and the tables, and across the abstract/introduction/tables.** The paper states (line 251) that regret ≤ T·dig-dec + Est/η, provides dig-dec bounds and Est bounds (Theorem 7: Est ≲ N·log|Φ|·T^{1/2}; Theorem 11: Est ≲ log²|Φ|), and then reports regret exponents in Tables 1–2. The arithmetic from the stated formula does not match the table entries:

   - **Table 1, average-error rows (rows 1–4):** For bilinear on-policy (dig-dec = H² d η, N=1), the formula gives optimal T-exponent T^{3/4}, but the table states T^{2/3}. For bilinear off-policy (dig-dec ∝ √η), the formula gives T^{5/6}, but the table states T^{2/3}.
   - **Table 2, all rows:** Bilinear on-policy with D̄_av (dig-dec ∝ √η, Est ∝ d·T^{1/2}) gives T^{5/6} from the formula, but the table states T^{3/2}. Several entries exceed T (the trivial per-round bound), making them impossible if taken as asymptotic rates. The squared-error rows (D̄_sq, Est constant) give T^{2/3} from the formula, but the table states T^{3/2} or T^{1/2}.

   These are not formatting artifacts — the fractions (3/2, 13/8, 2/3, 1/2) are clearly typeset and differ from what the formula supports. The squared-error rows of Table 1 are consistent, confirming the problem is localized to specific entries, but the affected entries are numerous and include the headline hybrid results.

2. **Abstract/Introduction rate claims are mutually inconsistent and include impossible "improvements."**  
   - Abstract (line 13): on-policy improves from T^{3/4} to T^{3/5}; off-policy from T^{5/6} to T^{7/8}.  
   - Introduction (line 33): on-policy goes from T^{3/2} to T^{3/2} (no change); off-policy from T^{5/8} to T^{5/6}.  
   - Neither matches Table 1, which states T^{2/3} for all average-error rows.  
   - The off-policy "improvement" of T^{5/6} → T^{7/8} (0.833 → 0.875) in the abstract is actually a degradation. The introduction's T^{5/8} → T^{5/6} (0.625 → 0.833) is also worse. These appear to be errors in the advertised comparisons.

   The paper's contribution is partly quantified by these regret exponents. With multiple conflicting sets of numbers, a reviewer cannot verify which claims are correct.

### Minor

3. **Est "improvement" from √T to T^{1/2} is tautological (line 213).** The paper states that the estimator "improves their rate of Est from √T to T^{1/2}." These are the same rate. The actual contribution — constructing an unbiased estimator instead of a biased one, improving constants — is real and should be presented clearly without implying a T-exponent change. This is primarily a presentation issue.

4. **No discussion of computational tractability.** Algorithm 1 requires solving a minimax optimization over distributions on Π and Ψ (Eq. 3) at each round. The paper acknowledges (line 37) that "model-free" does not imply computational efficiency, but it offers no guidance on when the optimization is tractable (e.g., convex-concave structure, finite action spaces). For a paper presenting a general algorithmic framework, some discussion of computational considerations would be helpful.

### Trivial

None.

## Nice-to-Haves

- The paper notes (line 272) that high-probability bounds are possible but gives no details. Sketching the additional overhead would be useful for readers wanting to deploy such bounds.
- The honest limitations paragraph (line 115) about Assumption 3 not covering low-rank MDPs with unknown reward features is commendable but could be expanded to more clearly delineate the scope of the contribution.
- Theorem 14's strict improvement is demonstrated on a 3-armed bandit; discussion of whether the gap extends to non-trivial MDPs would strengthen the paper.

## Removed Points

These points from the harsh critic input are removed with justification:

- **"The paper claims improved rates for average estimation error but the improvement is only in constants."** This is kept as Minor weakness #3.
- **"Computational tractability is a methodological gap."** Kept as Minor weakness #4 but weakened from the original framing (the paper explicitly scopes this out).
- **Claims about missing appendix content, deferred proofs, or absent references.** The parser strips these sections; they exist in the original submission. Removed per policy.
- **"Bilinear classes marked with ★" caveats in tables.** These are qualifications the paper already includes; not a weakness.
- **"The on-policy/off-policy distinction is confusingly named."** This is a domain convention, not an author error.
- **Generic framing like "the evaluation lacks rigor" or "baselines may not be fair."** These lack concrete anchors in the paper and are removed.
- **Strength claims about the problem being "important" or "well-motivated."** These are generic and removed per policy; only concrete, evidence-backed strengths are retained.
- **Duplicate framings of the same rate inconsistency issue.** Merged into Major weakness #1 and #2 above.

## Novel Insights

None beyond the paper's own contributions. The reviews confirm the conceptual advance but surface real problems with the quantitative claims that the paper itself does not resolve.

## Suggestions

1. **Reconcile all stated rates.** Re-derive the regret exponents for every entry in Tables 1–2 from the actual analysis (not the loose bound of T·dig-dec + Est/η, but the actual per-round bound). Ensure that the abstract, introduction, and tables all report the same numbers. If the appendix contains a tighter bound, state it explicitly in the main text. Fix the impossible superlinear entries in Table 2.

2. **Fix the "improvement" language in the abstract and introduction.** Ensure that every claimed improvement is actually an improvement and that the direction (from → to) is correct. Harmonize the notation between abstract and introduction — the slash notation (T^{3/2}/T^{5/8}) is not explained and causes confusion.

3. **Clarify the Est improvement.** Replace "from √T to T^{1/2}" with accurate language about the nature of the improvement (constant factors via unbiased estimation).

**Calibration details:**

Round 1 bracket: [4.0, 5.5]

Anchors consulted (all from deepreview_13k_calibration):
- *Horizon-free RL in Adversarial Linear Mixture MDPs* (aPNwsJgnZJ, avg 6.0): Clean theory paper with no identified weaknesses, accepted. Our paper has more conceptual novelty but significant quantitative inconsistencies that this anchor lacks.
- *Stochastic Bandits Robust to Adversarial Attacks* (vOFx8HDcvF, avg 6.5): Tight bounds, clean results, accepted. Our paper has messier presentation by comparison.
- *RL Algorithms are Information-State Policies in BAMDP* (ByW9j60mvV, avg 5.25): Interesting conceptual framework but insufficient concrete results, rejected. Similar to our paper in having a conceptual contribution weighed down by presentation issues.
- *Model-based RL as a Minimalist Approach* (txD9llAYn9, avg 7.0): Clean, solid results, accepted. Not comparable due to cleanliness of presentation.
- *RLHF with Inconsistent Multi-Agent Feedback* (GqGoa44obw, avg 4.5): Novel algorithm + setting but poor presentation, rejected. Most comparable anchor — both papers have genuine contributions undermined by presentation/consistency issues.
- *Value-Biased MLE for Model-based RL* (2h3m61LFWL, avg 4.25): Theoretical work with mixed reviews, rejected.

The paper's conceptual contribution is real and interesting, which prevents a low score. However, the quantitative inconsistencies (conflicting rates between abstract, introduction, and tables; impossible superlinear entries) are too numerous and central to overlook. The presentation issues go beyond formatting — they affect the verifiability of the paper's core quantitative claims. Score 4.5 reflects a paper with genuine ideas that needs substantial revision before its claims can be trusted.

MY FINAL SCORE: <score>4.5</score>
MY FINAL DECISION: <decision>Reject</decision>