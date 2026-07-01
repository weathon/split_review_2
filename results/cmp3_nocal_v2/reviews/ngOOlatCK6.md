Now I have all the information needed. Let me write the final consolidated review.

---

## Summary

This paper studies causal bandits where arms are *conditional interventions* on a single node (the value of the intervened variable depends on observed context). It provides a graphical characterization — the LSCA closure of Pa(Y) — of the minimal set of nodes guaranteed to contain the optimal intervention, and presents C4, a linear-time O(|V|+|E|) algorithm to compute this set. The main theoretical result (Theorem 13) is proven; experiments on random and real-world graphs show substantial pruning, especially in sparse graphs. A bandit regret experiment demonstrates faster convergence when using the pruned search space.

## Strengths

- **Proposition 4 is a genuinely clever reduction.** Showing that conditional-intervention superiority (over all policies, in probabilistic SCMs) is equivalent to deterministic atomic-intervention superiority (over values, in a fixed-unit deterministic SCM) is non-trivial and makes the subsequent graphical characterization tractable. This is the paper's sharpest conceptual insight. (Section 3, Proposition 4.)

- **The LSCA closure characterization (Theorem 13) is novel and elegant.** The Λ-structure reformulation (Theorem 12) turns a recursive closure into a simple, visually intuitive condition. The paper motivates the failure of standard LCA and builds up to LSCA with concrete examples (Figures 1a–1d), making the need for the stricter definition clear. The result is the kind that feels natural once stated. (Section 4, Definitions 7–11, Theorem 13.)

- **The C4 algorithm is a clean technical contribution.** Running in O(|V|+|E|) time, it uses a connector-based backward pass through the DAG. The connector concept (Definition 14, Lemma 15) is well explained and maps intuitively to the Λ-structure characterization. This is linear-time graph theory applied to a bandit pre-processing problem at exactly the right level of simplicity. (Section 5, Algorithm 1, Theorem 16.)

- **The paper is transparent about its assumptions and limitations.** It explicitly states: no latent confounders, single-node interventions only, the "observable conditioning set" nesting property, conditioning sets obeying An(X)\{X} ⊆ Z_X ⊆ V\De(X). It distinguishes its setting from Lee & Bareinboim (2018) (multi-node hard interventions with confounding) and clearly flags latent confounding and optimal conditioning set selection as future work. (Sections 2, 7.)

## Weaknesses

### Fatal

None. The core theoretical claims are proven and self-contained; the experiments serve as demonstrations, not as the foundation of the contribution.

### Major

- **The regret experiment (CondIntUCB comparison) does not provide independent evidence for the theory and has a definitional weakness.** The comparison shows that using mGISS nodes yields lower cumulative regret than using all ancestor nodes. Since Theorem 13 already guarantees the mGISS contains at least one optimal node, and bandit regret scales with the number of arms, the observed improvement is a *necessary consequence* of a correct pruning rule — it would be surprising if it did *not* hold. The experiment does not verify that the mGISS actually contains the optimal node in these specific instances (which would require known ground-truth SCMs or a simulation-based design). Furthermore, the "estimated best arm" is defined as "the arm that most runs concluded to be the best at the end of training" (line 291), making the regret benchmark relative to the algorithm's own convergence rather than an external ground truth. The paper would be stronger with a simulation-based verification under known SCMs (as suggested in the "Strengthening" section of this review) or with a control baseline of *random* node subsets of the same size to isolate the effect of mGISS selection from the trivial effect of arm-count reduction. This does not undermine the theoretical contribution (which stands independently), but it means the empirical claims about "substantially accelerating convergence" should be moderated to reflect what the experiment actually shows: that a smaller node set converges faster, which is definitionally true of any correct pruning.

### Minor

- **The worst-case nature of the guarantee is underexplored.** The superiority relation is defined "for all SCMs with causal graph G" — a worst-case guarantee. The paper is consistent about this, but it never discusses how conservative the mGISS might be in practice (i.e., the gap between worst-case minimality and what a specific SCM would actually require). A brief analysis or discussion of when/why the mGISS might be larger than the instance-optimal set (and by how much, in expectation) would give practitioners better intuition about the method's behavior. (Definition 1, Theorem 13.)

- **The "observable conditioning set" nesting assumption (Z_W ⊆ Z_X when W ∈ An(X)) is restrictive, and its scope is undiscussed.** The paper motivates this with temporal examples (trains, clinical timeline), which have a natural ordering. In a general DAG without a temporal interpretation (e.g., a static gene regulatory network), there may be no reason to assume such nesting. The paper does not analyze how sensitive the mGISS characterization is to violations of this assumption, nor does it characterize what happens when Z_W ⊈ Z_X. (Section 2, page 86.)

- **The regret experiment lacks a baseline controlling for arm-count reduction.** Without comparing against random subsets of nodes of the same size as the mGISS, the reader cannot distinguish between "mGISS contains the right nodes" and "any small subset would also improve regret." (Section 6, Figure 3.)

- **The paper does not discuss the degenerate case where Y has no parents.** In that setting, no single-node intervention can affect Y. The mGISS would be empty. The paper requires Y to have at least one parent (Proposition 6, Theorem 13), which is fine, but the degenerate case merits a brief mention for completeness.

### Trivial

- **The mGISS size vs. full ancestor set size is not reported for the 4 CondIntUCB datasets.** Knowing, e.g., that pathfinder went from X ancestors to Y mGISS nodes would make the regret curves more interpretable directly in the main text rather than only in the appendix.

## Nice-to-Haves

- Simulate SCMs with known ground-truth structural equations and noise distributions for the bnlearn graphs used in the regret experiment, and verify that the mGISS indeed contains the optimal node. This would directly confirm Theorem 13 experimentally while also allowing quantification of the gap between worst-case mGISS and instance-optimal set.
- Analyze sensitivity of the mGISS characterization to violations of the conditioning-set nesting assumption, or provide a concrete counterexample showing when it fails.
- Add a baseline of random or heuristic node subsets of the same size in the regret experiment to control for the arm-count confound.

## Removed Points

- **Criticism that the regret experiment "validates a trivial consequence" and that "the framing in the abstract overstates"** is partially retained (the experiment does not provide independent validation) but the tone is softened: the paper's abstract says "empirically demonstrate that our algorithm... substantially accelerates convergence," which is supported by the regret curves as a demonstration of *downstream benefit* — the theory itself is proven and does not need experimental validation. The criticism is kept as a Major weakness but framed more precisely around the experimental design limitations rather than overstatement.
- **Claim that "the paper's language sometimes implies [the mGISS] is tight"** — removed after checking the text. The paper consistently says "guaranteed" and "regardless of the SCM" (lines 145, 147), which clearly signals a worst-case guarantee. No language implying instance-level tightness was found.
- **Request for discussion of worst-case mGISS size** — the paper implicitly addresses this through the empirical results (mGISS can be large in dense graphs). The empirical framing is sufficient; no additional discussion is required.
- **"No discussion of the case where Y has no parents"** — demoted to Minor (it is a degenerate edge case explicitly excluded from the paper's scope).

## Novel Insights

None beyond the paper's own contributions. The reviewer correctly identifies the key strengths (Proposition 4, LSCA characterization, C4 algorithm) and the main experimental limitation, but does not raise a genuinely novel observation that the paper itself does not already make.

## Suggestions

- Add a control baseline of random node subsets of the same size as the mGISS to the regret experiment (Section 6, Figure 3) to isolate the effect of mGISS selection beyond arm-count reduction.
- Report the actual mGISS size vs. ancestor set size for each of the 4 CondIntUCB datasets in the main text (even parenthetically in the figure caption).
- Include a brief discussion of the gap between worst-case (all SCMs) and instance-specific optimal sets, perhaps noting that the mGISS is the *set-inclusion minimal* set for the worst case, which may be conservative in practice.
- Mention the degenerate case of Y with no parents (mGISS empty) for completeness.

## Score and Decision

The paper makes a clean, non-trivial theoretical contribution (LSCA closure characterization of the mGISS, with a linear-time algorithm) that is well-motivated, correctly proven, and clearly communicated. The experimental evaluation adequately demonstrates search-space pruning on random and real-world graphs. The regret experiment is the weakest component — it shows a downstream benefit that is a necessary consequence of correct pruning, but does not independently validate the theory or control for the trivial arm-count effect. This is a real limitation in the empirical framing but does not threaten the core theoretical contribution.

The paper meets the bar for a solid acceptance at ICLR: it contributes new, provably correct knowledge to a well-defined problem, and the theoretical machinery (Proposition 4, LSCA closure, C4) is genuinely useful.

MY FINAL SCORE: <score>7</score>
MY FINAL DECISION: <decision>Accept</decision>