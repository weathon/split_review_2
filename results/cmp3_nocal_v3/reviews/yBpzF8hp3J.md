## Summary

The paper studies differentially private domain discovery problems (set union, top-k, and k-hitting set) and makes several theoretical contributions: (1) first absolute utility guarantees for DP set union, under a Zipfian assumption for ℓ₁ missing mass and distribution-free for ℓ∞ missing mass; (2) a clean meta-algorithm that extends known-domain results to unknown domains via WGM as a precursor; (3) lower bounds showing near-optimality in ε and N for all three problems. Experiments on six datasets evaluate the methods against baselines.

## Strengths

1. **First absolute utility guarantees for DP set union (Section 3, Theorems 3.3, 3.5, 3.6).** Existing work (Desfontaines et al., 2022; Chen et al., 2025) provides only relative guarantees. Theorems 3.3 and 3.6 provide absolute upper bounds on missing mass for WGM, and Theorem 3.5 gives a matching (in ε and N dependence) lower bound — a genuine theoretical advance stated transparently (line 31).

2. **Clean meta-algorithm with distribution-free guarantees (Algorithm 2, Sections 4.1–4.2).** Running WGM to discover a domain then executing a known-domain algorithm is simple and principled. The ℓ∞ missing mass guarantee (Theorem 3.6) is distribution-free, so the top-k and k-hitting set guarantees (Theorems 4.3, 4.5) do not inherit a Zipfian assumption.

3. **Lower bounds for derived problems (Corollaries 4.4, 4.6).** The paper constructs lower bounds showing a linear-in-k/ε loss is unavoidable for top-k and k-hitting set in the unknown-domain setting. This calibrates expectations about achievable performance.

4. **Missing mass framing (Definition 2.2, Equation 1).** The shift from cardinality to missing mass — and the ℓp generalization — is well-motivated by the singleton-dataset hardness argument (lines 77–78). The paper is upfront that cardinality is not informative in this setting.

## Weaknesses

### Fatal
None.

### Major
None that threaten the core theoretical contribution.

### Minor

1. **Within-5% claim vs. figure evidence (line 281).** The text states WGM "obtains MM within 5% of that of the policy mechanisms," but the figure description (parser-generated from the actual plot) suggests larger gaps on Reddit and Movie Reviews — WGM drops to a "low value" while policy mechanisms "remain relatively high." On Amazon Games the gap appears small, but on Reddit (y-axis 0.15–0.40) and Movie Reviews (y-axis 0.00–0.25) the absolute difference seems to exceed 0.05. The authors should reconcile the text and the data, or provide exact numerical values so readers can verify the claim.

2. **No error bars for set union and top-k experiments (Sections 5.1, 5.2).** The paper reports only "average MM across 5 trials" (line 281) for set union and top-k. Standard error is reported only for k-hitting set (line 311). With only 5 trials, variance information is important to assess the reliability of the empirical conclusions.

3. **Only one privacy budget in the main experiments (Section 5).** All main experiments use (ε=1, δ=10⁻⁵). The ε=0.1 results are deferred to the appendix and described as "not significantly qualitatively different" (line 273), but presenting at least one additional budget in the main text would strengthen the empirical validation, given the theory predicts a 1/ε dependence.

### Trivial

- No runtime measurements are provided despite claiming WGM is "simple and scalable" (line 14) and noting the policy mechanisms are "significantly more intensive" (line 281). A brief complexity comparison would substantiate the scalability claim.

## Nice-to-Haves

- A brief discussion (even conjectural) of where the gaps between upper and lower bounds for top-k and k-hitting set are likely tight would enrich the theoretical narrative. The paper acknowledges the gaps in Section 6 but does not discuss which terms (√k, log M) may be artifacts of the proof technique.
- The ℓ∞ missing mass guarantee (Theorem 3.6) depends on maxᵢ|Wᵢ|/(√q*). A brief note on when this factor is benign (e.g., when Δ₀ ≥ maxᵢ|Wᵢ| so q* = maxᵢ|Wᵢ|) would help readers interpret the bound.

## Removed Points

These points were considered but removed from the main weaknesses list with justification:

- **k-hitting set baseline mismatch (Critical Issue 3 from input review).** The critic notes that the auto-generated figure description (lines 319–321, parser artifact) lists "DP-Top-k" / "DP-Top-k with Pay-What-You-Get" while the paper's text (line 309) clearly states the baselines are the non-private greedy algorithm and the private algorithm from Mitrovic et al. (2017). The detailed figure descriptions are parser-generated alt-text from embedded images, not the paper's captions. The paper's own description is unambiguous. **REMOVED** (parser artifact, not a paper error).

- **Gap between upper and lower bounds not precisely acknowledged.** The reviewer raises that the upper bound depends on maxᵢ|Wᵢ|/√q* which doesn't appear in the lower bound, but acknowledges the paper mitigates this via Lemma 3.1 (maxᵢ|Wᵢ| ≤ (CN)^(1/s)). This is a clarity suggestion, not a substantive weakness. **REMOVED** (too minor; subsumed by Nice-to-Haves).

- **ℓ∞ missing mass dependence on maxᵢ|Wᵢ|/(√q*).** The critic observes the bound weakens when maxᵢ|Wᵢ| is large. This is a correct observation about the bound's behavior, not a flaw — the paper correctly presents the bound and notes it is distribution-free. **REMOVED** (technical observation, not a weakness; subsumed by Nice-to-Haves).

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

- Clarify the "within 5%" claim: provide exact numerical values (e.g., a table) alongside the figure, or revise the text to accurately describe the observed gaps.
- Add standard error or confidence intervals to all experimental results, particularly for the 5-trial set union and top-k experiments.
- Consider including a brief complexity comparison (runtime or asymptotic) to substantiate the scalability claim about WGM.

MY FINAL SCORE: <score>7.0</score>
MY FINAL DECISION: <decision>Accept</decision>