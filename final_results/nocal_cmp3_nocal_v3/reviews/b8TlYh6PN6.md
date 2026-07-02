## Summary

This paper characterizes distributional equivalence (observational indistinguishability) in linear non-Gaussian causal models with *both* arbitrary latent structure and cycles — a setting where no such characterization existed. The authors introduce *edge rank* constraints as a new tool dual to the familiar path-rank constraints, derive a local graphical criterion (Theorem 2) that reduces global rank-checking to checking children bases for each singleton observed variable, and prove a transformational characterization (Theorem 3) using cycle reversals and edge additions/deletions, analogous to Meek's conjecture for CPDAGs. An algorithm (glvLiNG) is presented as a proof of concept that the characterization can be used for recovery from data.

---

## Strengths

1. **First equivalence characterization covering both latent variables and cycles in linear non-Gaussian models.** Prior work covered cycles without latents (Lacerda et al., 2008) or latents without cycles (Adams et al., 2021 gave identification conditions but no equivalence). Theorem 2 (children-bases criterion) and Theorem 3 (transformational characterization) genuinely extend the frontier. The paper's claim that this is the first such equivalence result with latent variables in any parametric setting without structural assumptions is credible based on the literature surveyed.

2. **Edge ranks as a new analytical tool with potential beyond this paper.** Theorem 1 (duality between path ranks and edge ranks) elegantly bridges two perspectives. While the duality itself is known in matroid theory (König; Perfect; Ingleton & Piff), the paper's identification of its relevance to causal discovery and its use to derive local criteria (Theorem 2 from Lemma 5) is genuinely insightful and fills a missing piece in the rank-based toolkit. This contribution likely has value for other settings (selection bias, mixtures, etc.).

3. **Clean reduction from global to local constraints.** Theorem 2's reduction — checking bases for all subsets of $X$ reduces to checking bases for $L$ and $L\cup\{X_i\}$ for each singleton $X_i$ — mirrors the value of moving from "all d-separations" to "same adjacencies and v-structures." The paper convincingly explains why this reduction is possible with edge ranks but was not available with path ranks.

4. **Irreducibility framework (Propositions 1, 2).** A clean graphical condition (each latent set must have >1 child outside itself) and a reduction procedure that rule out trivial unidentifiability without introducing structural assumptions. Properly distinguished from the type of assumptions the paper aims to avoid.

---

## Weaknesses

### Fatal

None.

### Major

1. **Tension between strong practical claims and proof-of-concept framing.** The contribution list (point 4) presents glvLiNG as "an efficient algorithm to recover the equivalence class from data" and the abstract calls it "the first structural-assumption-free discovery method." Yet the paper also states that OICA is "known [to be] inefficient in practice" and that glvLiNG "serves more as a proof of concept" (Section 5, Final Remarks). This framing mismatch is significant: the algorithm cannot credibly be called a practical discovery method if its core estimation step (OICA) does not scale reliably, and the strong "first structural-assumption-free discovery method" claim should be qualified or demoted. If the algorithm were reframed as an illustration of the characterization's utility rather than a co-equal contribution, this tension would be resolved.

2. **The linear programming baseline for runtime comparison is not described.** The paper states: "We compare the execution time against a linear programming baseline for constructing digraphs to satisfy ranks of oracle OICA mixing matrices" — with no detail on what the baseline actually is, how it was formulated (e.g., integer programming, constraint satisfaction), or whether it is a reasonable comparator. This makes the runtime claim ("glvLiNG solves cases with n=10 vertices in under 5s, while the baseline takes hours beyond n=5") unverifiable. A minimal description of the baseline formulation is needed.

3. **Oracle comparison against LaHiCaSi and PO-LiNGAM tests them only under assumption violations.** The paper frames this as studying "how existing methods behave under structural misspecification," which is a legitimate question. However, there is no complementary evaluation where the baselines' assumptions *are* satisfied — to check whether glvLiNG loses meaningful performance by being more general. The finite-sample experiments (Appendix D.4) may partially address this, but are deferred entirely to the appendix with only a two-sentence qualitative summary in the main text. Even a single main-text experiment showing glvLiNG's performance relative to baselines under assumption-matched conditions would substantially strengthen the evaluation.

### Minor

1. **Main-text evaluation is thin for a method claimed as a co-equal contribution.** Section 5 describes five experimental aspects but provides only brief qualitative summaries (class sizes, runtime, misspecification effects) with no tables or figures in the main paper. The key numerical claims ("n=10 in under 5s", "783 equivalence classes") are present, but the overall evaluation weight is low relative to the practical ambitions implied by contribution 4. This is mitigated by the paper's own acknowledgment that glvLiNG is a proof of concept, but if the contribution is to be retained at the current strength, more main-text evidence is needed.

2. **Equivalence class enumeration reports counts but not informativeness.** The paper reports that 480,640 irreducible digraphs with 5 vertices and 2 latents form 783 equivalence classes (Table 3), but does not analyze whether most classes are singletons (unique identification) or large multi-graph classes (high uncertainty). This information would help calibrate expectations about the method's output.

3. **Faithfulness robustness is not discussed.** The paper assumes faithfulness and defers its formal statement to Assumption 1 in the appendix, but does not discuss what happens under near-violations (finite-sample rank estimation error, near-cancellations). This is common in rank-based causal discovery and not a fatal gap, but a brief discussion would strengthen the paper.

### Trivial

None.

---

## Nice-to-Haves

- Replace the linear programming baseline in the runtime comparison with the naive brute-force enumeration implied by Lemma 3 (path-rank characterization), which would directly demonstrate the value of Theorem 2's local decomposition.
- Add a small main-text sanity check: run the full glvLiNG pipeline (with practical OICA) on a simple 2-latent, 3-observed simulated model at varying sample sizes, and report whether the estimated equivalence class contains the ground-truth graph.
- Discuss what happens when the equivalence class is very large (many graphs) — does the method's output become practically uninformative, and how would a practitioner interpret it?

---

## Removed Points

These points were raised in the input review but are removed under the filtering rules:

- **"No concrete experimental result survives in the main paper"** — Overstated. The main paper contains concrete claims ("n=10 in under 5s", "783 equivalence classes", "misidentify over half of the edges"). Tables are in the appendix, which is standard for ICLR. The evaluation is thin but not absent. A moderated version is kept as a Minor weakness above.

- **"Missing related works" / "FCI is typically not regarded..."** — This is a minor framing debate, not a substantive weakness. The paper's statement about FCI is reasonable in context.

- **"The oracle comparison is circular/straw targets"** — Moderated. The paper explicitly frames this as a test of structural misspecification, not a head-to-head comparison; this is a valid empirical question. The real weakness (kept above) is the absence of a complementary test under assumption-matched conditions.

- **"Only needs to check each singleton due to Theorem 2" — this already shows the algorithm is fully specified** — Removed as not a valid weakness.

---

## Novel Insights

Beyond the paper's own contributions, the most interesting observation from the reviews is that the edge-rank duality (Theorem 1) could have broader applicability than even this paper claims. The paper uses it to derive local criteria for equivalence, but the duality itself — translating between path-level and edge-level constraints — could be applied to other causal discovery problems where rank constraints arise (e.g., selection bias, mixture models, linear Gaussian models with rank constraints). The paper notes this potential briefly but does not elaborate.

---

## Suggestions

1. Reframe the contribution list to explicitly present the equivalence characterization (Theorems 2 and 3) as the primary contribution, with the algorithm as an illustration of how the characterization enables recovery — not as a co-equal practical method. This resolves the main framing tension.
2. Provide at least a one-paragraph description of what the "linear programming baseline" actually is, or replace it with a more clearly specified comparator.
3. Add one main-text experiment showing glvLiNG's performance on a simple model where ground truth is known, even if limited (e.g., 2 latents, 3 observed, varying sample sizes, reporting whether the equivalence class contains the true graph).

---

## Score and Decision

This paper makes a genuine theoretical advance: it is the first to characterize distributional equivalence in linear non-Gaussian models with both latent variables and cycles. The edge-rank tool, the local decomposition (Theorem 2), and the transformational characterization (Theorem 3) are well-motivated, technically sound, and appropriately situated relative to prior work. The main weaknesses are framing issues (overclaiming practical contribution relative to proof-of-concept evidence) and thin evaluation detail in the main text — both are addressable through revision without undermining the theoretical core.

MY FINAL SCORE: <score>7.5</score>
MY FINAL DECISION: <decision>Accept</decision>