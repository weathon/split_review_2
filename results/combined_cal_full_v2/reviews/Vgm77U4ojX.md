Now I have enough information to calibrate. Let me compile my final analysis.

**Round-1 bracket:** I compared SIGMADOCK against anchors from all bands. Below 3.5, papers have trivial or flawed contributions (CompassDock at 3.0 has a fundamentally broken training procedure). SIGMADOCK is clearly above this. Between 3.5 and 5.5, papers like DiffDock-Pocket (5.0) and the "Are We There Yet?" benchmark (4.38) have useful but incremental contributions. SIGMADOCK's method (fragment-based SE(3)^m diffusion + FR3D) is more novel than these, and its results (79.9% PB-valid) are stronger. Between 5.5 and 7.5, papers like DockGen (6.0), IPDiff (6.25), and GroupBind (6.75) have strong novel methods and clean evaluations. SIGMADOCK's method novelty is on par or ahead, but its evaluation presentation is less clean. **Initial bracket: [5.5, 7.0].**

**Round-2 narrow:** I itemized VFDiff (6.00), IPDiff (6.25), and Frag2Seq (5.75) — the most topically similar papers in the 5.5-7.5 band. SIGMADOCK's strongest-weighted items (strength weights 7.87-10.65) match or exceed these anchors' strongest items. But its most negative-weighted weakness (Vina omission at -1.12) is worse than anything at the 6.0+ level (VFDiff's worst was -2.77 about novelty concerns; IPDiff's worst was -2.36; DockGen's worst was -0.32). The comparison table confusion (0.63) and AF3 mismatch (1.61) are also meaningful drags.

**Final score: 6.0.** This is below GroupBind (6.75) whose evaluation was cleaner, slightly below IPDiff (6.25), on par with DockGen (6.00) and VFDiff (6.00), and above Frag2Seq (5.75) and DiffDock-Pocket (5.00). The method contribution and results support borderline acceptance, but the evaluation presentation requires substantial cleaning.

Now let me write the final review.

## Summary
2-3 sentence summary of the paper's contribution.

## Strengths
- strength 1 with evidence
- strength 2 with evidence

## Weaknesses
### Fatal
None

### Major
- weakness 1
- weakness 2
- weakness 3

### Minor
- weakness 1
- weakness 2
- weakness 3

### Trivial
- weakness 1

## Nice-to-Haves
- suggestion

## Removed Points
...

## Novel Insights
...

## Suggestions
...

## Score and Decision## Summary

This paper introduces SIGMADOCK, an SE(3)^m Riemannian diffusion model that replaces the standard torsional parametrization of ligands with a fragment-based rigid-body representation for molecular docking. By decomposing ligands into torsion-free fragments (using a novel FR3D merging scheme to reduce degrees of freedom) and diffusing/denoising their poses in SE(3)^m, the method avoids several known pathologies of torsional models. Empirically, SIGMADOCK reports 79.9% Top-1 PB-valid on PoseBusters and 90.6% on Astex, trained only on PDBBind(v2020).

## Strengths

- **Well-motivated fragmentation paradigm.** The paper's central idea — replacing torsional diffusion with fragment-based SE(3)^m diffusion — is conceptually compelling. Section 2.2.2 provides the clearest treatment of the limitations of torsional models (non-product induced measures, ambiguous extrinsic gauge, lever effect) seen in the docking literature. Theorem 1 captures a genuine structural weakness of torsional approaches, even if its statement is qualitative.

- **Strong headline results.** The raw numbers are striking: 79.9% Top-1 PB-valid on PoseBusters vs. 38.0% for DiffDock (under the same train-test split). The 90.6% on Astex is also impressive. If these numbers hold under fair comparison, this is a genuine advance over prior deep learning docking methods.

- **Disciplined training setup.** Training only on PDBBind(v2020) and using the correct PB train-test split (Footnote 1, Footnote 8) is good experimental hygiene. The paper explicitly calls out the common unfair practice of training on larger datasets and then comparing on the same held-out set.

- **Informative ablation study.** Table 1 usefully isolates the contributions of triangulation conditioning, fragment merging, protein-ligand interactions, and the scoring heuristic. The 4–12% relative degradations when removing these components confirm that each plays a non-trivial role.

- **Robustness analysis.** The pocket-size sensitivity (Table 3), sequence-similarity stratification (Figure 4, right), and co-factor analysis (Table 2) are exactly the kind of stress tests needed to evaluate whether a deep learning docking model is learning physics rather than memorizing training patterns.

## Weaknesses

### Fatal

None.

### Major

- **Ambiguous comparison conditions in the main results table (Figure 4, left).** Methods are split into "Holo Specified" and "Pocket Specified" without defining either condition or explaining how they differ. SIGMADOCK is listed under "Pocket Specified" despite the paper stating (line 24) that it uses the standard re-docking protocol with the holo-conformation — the same setting presumably used by methods listed under "Holo Specified." The text then directly compares SIGMADOCK (Pocket Specified, 79.9%) to DiffDock (Holo Specified, 38.0%). Additionally, the 6.3× improvement claim (line 192: "6.3× higher PB-validity than DiffDock") is inconsistent with the table values (79.9/38.0 ≈ 2.1), and the abstract's "12.7–32.8%" range for "recent deep learning approaches" is unattributed — the table shows G2G and Vibe2 at 58.1% and DiffDock at 38.0%, none falling in that range. The "Ours" entry appears twice (79.9 and 80.6) without labeling what each value represents.

- **The classical docking baseline is underreported.** The paper claims to be "the first deep learning approach to surpass classical physics-based docking" (abstract, Section 3.2, Conclusion), yet the only classical method in the main comparison table is "PDBBind" at an implausibly low 15.9% Top-1 on PB. Vina, the most widely used physics-based docking tool, achieves 57.2% on the same PB set (mentioned in passing at line 256 in a pocket-sensitivity discussion) but is excluded from the main comparison table. A reader who only looks at Figure 4 would conclude classical docking achieves ~16%, making the "first to surpass" claim self-serving. A proper side-by-side comparison including Vina in the main table is essential.

- **The AF3 comparison uses non-matching per-bin samples (Table 4).** For the [0,30) sequence similarity bin, SIGMADOCK evaluates 109 complexes while AF3 evaluates 38; for [95,100], SIGMADOCK evaluates 123 vs AF3's 187. The paper does not explain this discrepancy. If the two methods are evaluated on different subsets of the PB set, the per-bin percentages (72% vs 87%, etc.) are not directly comparable, and the claim of "AF3-level performance" in the abstract and conclusion is unsupported. The comparison either needs to be performed on exactly matching subsets or de-emphasized from headline claims.

### Minor

- **The scoring heuristic is integral, not auxiliary.** Ablation Config D (removing energy scoring) drops PB Val. from 79.9% to 66.1%, and Config E (removing PB scoring) drops it to 70.8% — drops of ~10–14 absolute percentage points. The paper states (Section 2.5) that "SIGMADOCK does not require the use of a separately trained confidence model," which is technically true but understates that the hand-crafted scoring heuristic is responsible for a large fraction of the reported performance. This should be presented as a core inference component, not a minor post-processing step.

- **No confidence intervals or statistical significance tests.** No error bars, standard errors, or bootstrapped confidence intervals are reported for any Top-1 success rates. The PB set contains 308 complexes, so a 2–3 percentage point difference could be within sampling variability. For a paper making "first to surpass" comparative claims, this is a notable omission.

- **The "simpler to learn" claim for higher-dimensional fragment space lacks empirical support.** The paper acknowledges that FR3D yields ~4(k+1) DoF vs (k+6) for torsional models (approximately 24 vs 11 for a typical drug-like ligand). The claim that this is "simpler to learn" because the fragment space is a product space (Theorem 1 addresses the prior measure, not the learning difficulty) is supported only by intuition. The paper would benefit from training curves, sample efficiency comparisons, or analysis of the score model's effective rank to substantiate this claim.

### Trivial

None.

## Nice-to-Haves

- Provide a histogram of fragment counts (m) and rotatable bond counts (k) across the training/test sets to support the DoF reduction claim.
- Report absolute sampling times and runtime comparisons against deep learning baselines (DiffDock, G2G, Vibe2), not just the 50× speedup vs AF3.
- Analyze whether co-factor failures are systematic (e.g., do all co-factor-dependent ligands fail, or is it stochastic?).
- Show an ablation removing FR3D entirely (naive fragmentation without merging) to isolate the contribution of the merging strategy.

## Removed Points

These points from the input review were filtered:

- **"Comparing across Holo/Pocket conditions is invalid"** — Downgraded from Fatal to Major because the comparison is not fundamentally invalid; the paper just fails to define the conditions clearly. Both settings use the same re-docking protocol.
- **"Section 2.2.3 FR3D details deferred to appendix"** — Standard practice for space-constrained papers; the main text description is at an appropriate level.
- **"Missing runtime comparison against DL baselines"** — Moved to Nice-to-Haves.
- **"The 12.7-32.8% range is inconsistent"** — Merged into the first Major weakness rather than standing as a separate issue.
- **"Ours entry appears twice without explanation"** — Merged into the first Major weakness.
- **"Pure formatting/style nitpicks"** — Removed per hard rules.
- **"Typos/grammar/capitalization"** — These are parser artifacts, not author errors.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. **Fix the comparison table:** Provide a single unified table with all methods (including Vina at 57.2%) under identically labeled conditions, clearly defining what "Holo Specified" and "Pocket Specified" mean or collapsing the distinction.
2. **Correct the 6.3× claim:** Either provide the correct factor or explain what baseline and metric produce this number.
3. **Fix the AF3 comparison:** Evaluate on exactly matching PB subsets, or remove the AF3 comparison from headline claims (abstract, conclusion).
4. **Add confidence intervals:** Report bootstrapped 95% CIs for all Top-1 success rates in the main tables.
5. **Present the scoring heuristic more prominently:** Give it a full main-text description and acknowledge its ~10–14 point contribution.

## Score and Decision

**Anchors used for calibration:**
| Anchor | Score | Round | Itemized | Comparison |
|--------|-------|-------|----------|------------|
| CompassDock (nWO75tVjfp) | 3.00 | R1 | Yes | Less novel method, broken implementation. SIGMADOCK is clearly stronger. |
| DiffDock-Pocket (1IaoWBqB6K) | 5.00 | R1 | Yes | Incremental improvement on DiffDock. SIGMADOCK has more novel method and stronger results. |
| "Are We There Yet?" (ZuU4mZILBB) | 4.38 | R1 | Yes | Benchmark paper, not a new method. SIGMADOCK contributes a new method. |
| VFDiff (5YLsnsjgeC) | 6.00 | R2 | Yes | SE(3) diffusion for SBDG; novelty concerns. SIGMADOCK's method is more novel, results are stronger. |
| IPDiff (qH9nrMNTIW) | 6.25 | R2 | Yes | Novel prior-shifting for SBDG; clean evaluation. Different task, but SIGMADOCK's evaluation is less clean. |
| Frag2Seq (mMhZS7qt0U) | 5.75 | R2 | Yes | Fragment-based tokenization for SBDG. SIGMADOCK's docking results and method novelty are stronger. |
| DockGen (UfBIxpTK10) | 6.00 | R1 | Yes | New benchmark + training method; clean evaluation. SIGMADOCK has more novel method but messier evaluation. |
| GroupBind (zDC3iCBxJb) | 6.75 | R1 | Yes | Group-wise docking paradigm; clean evaluation. SIGMADOCK has comparable method novelty but less clean eval. |

**Weighted-item comparison:** SIGMADOCK's strongest strengths (headline results weight 10.65, ablation weight 9.76, paradigm motivation weight 9.57) match or exceed the top strengths of DockGen (11.88) and IPDiff (10.79, 11.46). However, its most negative-weighted weaknesses (Vina omission at -1.12, table confusion at 0.63) are worse than those at the 6.0+ level — DockGen's worst was -0.32, IPDiff's worst was -2.36 (about a more contained novelty concern), GroupBind's worst was 0.04. The evaluation presentation issues, while fixable, prevent full confidence in the comparative claims as currently written.

**Final score: 6.0.** The method contribution (fragment-based SE(3)^m diffusion + FR3D + triangulation conditioning) is genuinely novel and well-motivated, and the raw results (79.9% PB-valid) are strong. However, the evaluation presentation has meaningful issues that must be addressed: ambiguous comparison conditions, omission of a proper classical baseline (Vina) from the main table, and a non-matching AF3 comparison. A borderline-accept score reflects that the core contribution is real and publishable, but the paper needs revision to cleanly support its comparative claims.

MY FINAL SCORE: <score>6.0</score>
MY FINAL DECISION: <decision>Accept</decision>