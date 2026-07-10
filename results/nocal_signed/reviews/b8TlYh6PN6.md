Now I have all the information I need. Let me compose the final review.

## Summary

This paper characterizes distributional equivalence for linear non-Gaussian causal models with arbitrary latent variables and cycles. It introduces edge rank constraints as a new graphical tool, derives a local decomposition (Theorem 2) that reduces equivalence checking from exponential to linear in the number of observed variables, and provides a transformational characterization of the equivalence class (Theorem 3). It also develops glvLiNG, a proof-of-concept algorithm that recovers models up to equivalence using over-complete ICA. The theoretical contribution addresses a genuine gap — no equivalence characterization existed for this setting — and is the paper's primary contribution.

## Strengths

- **Addresses a genuine gap in causal discovery.** Distributional equivalence for linear non-Gaussian models with arbitrary latent variables and cycles was previously uncharacterized. The paper correctly motivates why this gap has blocked structural-assumption-free approaches, drawing an effective analogy to the history of PC/CPDAG and FCI/MAG.

- **Theorem 2 is a genuine algorithmic insight.** It reduces checking all subsets of observed variables to checking only singletons (exponential to linear in |X|), which the paper convincingly argues would not be possible from the path-rank formulation alone. This decomposition is the paper's deepest theoretical result.

- **The duality between path ranks and edge ranks (Theorem 1) is well-motivated.** Adapting known matroid duality (König, Perfect, Ingleton & Piff) to causal discovery is a novel application that enriches the rank-based toolbox for the community. The paper's argument that edge ranks are easier to manipulate locally — and that this localness is what enables Theorem 2 — is clearly articulated.

- **The theoretical architecture is clean and logically motivated.** The progression from mixing matrices → path ranks (Lemma 3) → edge ranks (Lemma 5 via duality) → local decomposition (Theorem 2) is step-by-step, with each step's limitations motivating the next. The paper is transparent about which results are novel and which are attributed to prior work (e.g., Lemma 6's cycle reversals to Lacerda et al. 2008).

- **The paper is appropriately cautious about its own limitations.** It explicitly acknowledges OICA's practical difficulties and frames glvLiNG as a proof of concept, particularly in the conclusion and final remarks.

## Weaknesses

### Fatal

None.

### Major

- **The evaluation section (§5) provides no visible experimental evidence in the main text.** Every empirical claim is presented as a qualitative summary ("glvLiNG solves cases with n=10 vertices in under 5s," "both methods misidentify over half of the edges") with references to tables that reside solely in the (not visible) appendix. No numbers, error bars, tables, or figures appear in the visible portion. While the paper's core contribution is theoretical, the title and abstract foreground the algorithm, and a reader of the main text alone cannot assess whether the empirical claims are substantiated. This is a significant presentation weakness for a conference that values empirical validation.

### Minor

- **Practical significance of glvLiNG is unclear even on the paper's own terms.** The algorithm's correctness guarantee depends on oracle OICA in the over-complete regime (more sources than observed mixtures), which is known to be unstable and sample-inefficient. The paper acknowledges this as a limitation, but the gap between the oracle assumption and practical applicability remains large, and the evaluation (even in the appendix) uses simulated data from known models. This does not diminish the theoretical contribution but does temper the algorithmic claims.

- **The "first structural-assumption-free method" framing could be misleading without more careful qualification.** The paper defines "structural assumptions" narrowly as restrictions on latent interactions, which is internally consistent. However, the method replaces these with strong parametric assumptions (linearity, non-Gaussianity, faithfulness, oracle OICA) — a meaningful trade-off between different kinds of assumptions, not the absence of assumptions. The abstract and introduction do not carry this qualification as clearly as the conclusion does.

- **The algorithm section does not explicitly clarify that OICA is used in its over-complete variant** (mixing matrix of size |X| × (|L|+|X|), where the number of sources exceeds the number of observed mixtures). This is a non-standard usage of ICA and is worth flagging directly in the algorithm description rather than only mentioning "over-complete ICA" once in the introduction.

### Trivial

- Lemma 5 contains a typo: the equivalence is written as `$\mathcal{G} \stackrel{\mathcal{H}}{\sim} \mathcal{H}$` instead of the intended `$\mathcal{G} \stackrel{X}{\sim} \mathcal{H}$`.
- The notation switches from ∼ (Definition 1) to ≈ (Lemma 1 onward) without explanation. While likely intentional to distinguish two formalisms, the shift is confusing to the reader.

## Nice-to-Haves

- Including even a single summary table or figure in the main text (e.g., runtime scaling, a simulation result) would substantially strengthen the paper's credibility on the empirical side without changing its theoretical focus.

## Removed Points

These points from the input review were removed with justification:

- The criticism questioning the "first structural-assumption-free method" claim as "open to reasonable objection" about linearity/non-Gaussianity assumptions was demoted from critical to minor because the paper explicitly defines "structural assumptions" as restrictions on latent interactions (not parametric assumptions) and scopes its claims to the linear non-Gaussian setting. The removed framing was speculative about reader perception rather than a concrete error in the paper.
- The criticism that "practical significance is unclear even on its own terms" was demoted from critical to minor because the paper itself repeatedly calls glvLiNG a "proof of concept" and flags OICA as a limitation — the paper already addresses this concern.
- Formatting nitpicks and style comments were removed per instructions.
- Missing related works criticisms were removed per instructions (cannot be verified from external sources).

## Novel Insights

None beyond the paper's own contributions. The reviews confirm the paper's stated contributions without adding new analytical angles.

## Suggestions

1. Move at least one concrete experimental summary (e.g., runtime vs. baseline scaling, or a main performance figure) into the main text so readers can calibrate the empirical claims directly.
2. In the abstract and introduction, state more explicitly that the main contribution is the theoretical characterization and that the algorithm serves as a proof-of-concept, to avoid conflating theoretical and algorithmic contributions in a way that overpromises.
3. Clarify in the algorithm section that OICA is used in its over-complete variant and briefly discuss the implications of this choice.
4. Fix the Lemma 5 typo and consider using consistent notation for distributional equivalence throughout.

## Score and Decision

The theoretical contribution — the characterization of distributional equivalence for linear non-Gaussian models with arbitrary latent variables and cycles — is significant, novel, and appears technically sound. It addresses a genuine gap, introduces a useful new tool (edge ranks), and obtains a clean local decomposition (Theorem 2) that is a genuine algorithmic insight. The paper is transparent about its limitations.

The primary weakness is the absence of visible experimental evidence in the main text, which is a meaningful presentation gap. However, this does not undermine the theoretical contribution, which stands on its own. The paper should be accepted on the strength of its theoretical characterization, with the expectation that the authors address the presentation gap in the camera-ready version.

MY FINAL SCORE: <score>7.5</score>
MY FINAL DECISION: <decision>Accept</decision>