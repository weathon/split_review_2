## Summary

This paper proposes RADAR, a neural framework for asymmetric vehicle routing problems (VRPs). It introduces two architectural components: (1) an SVD-based node initialization that encodes static directional asymmetry from the distance matrix, and (2) Sinkhorn normalization replacing softmax in attention to model dynamic asymmetry during encoding. The method is evaluated on 17 synthetic VRP variants and 3 real-world benchmarks, consistently outperforming neural baselines and often matching or beating classical solvers.

---

## Strengths

1. **Principled SVD-based initialization with clean theoretical grounding.** Definition 1 formalizes asymmetry-aware embeddings, and the derivation showing that SVD singular vectors encode outbound/inbound roles (Eqs. 3–5) is elegant and non-trivial. The construction $XW_1(XW_2)^\top \approx D$ connects naturally to the bilinear form used in attention.

2. **Unusually broad experimental evaluation.** The paper tests on ATSP + 16 asymmetric VRP variants (adapted from RouteFinder) plus 3 real-world datasets from RRNCO, covering in-distribution and out-of-distribution generalization up to 10× training size (100 → 1000 nodes). Most neural VRP papers evaluate on 1–3 variants.

3. **Clean ablation isolating both contributions.** Table 6 shows the additive effect of SVD alone (reducing gap from 2.08%→1.19% on ATSP100) and SVD+Sinkhorn together (further to 0.72%), confirming the two components target distinct aspects of asymmetry.

4. **Insightful analysis of coordinates under asymmetry (Section 5.4).** The finding that RADAR without coordinates outperforms RRNCO *with* coordinate augmentation is empirically grounded and practically useful for deployments where coordinates are unavailable or unreliable.

---

## Weaknesses

### Fatal
None.

### Major

1. **Overclaiming in Section 5.3.** The prose states "RADAR consistently achieves lower costs and smaller optimality gaps across all tasks and distribution settings" (line 206–207). In Table 3, on ACVRPTW, OR-Tools achieves a gap of 1.38% (in-distribution) while RADAR achieves 2.71%. The footnote restricts boldface to learning-based methods, but the prose makes an unqualified absolute claim that is false for this setting. This is a clear framing error that should be corrected by adding the qualifier "among learning-based methods."

### Minor

1. **Missing strong baseline in multi-task comparison (Section 5.2).** The multi-task evaluation compares RADAR only against RF and RF-NN (RouteFramework variants). RRNCO, the strongest asymmetric-specific neural baseline evaluated in the synthetic and real-world experiments, is not included. While adapting RRNCO to multi-task is non-trivial, the absence means the "strong generalizability" claim in the multi-task setting is only supported against weak baselines. (The paper's overall evidence for effectiveness does not depend on this experiment alone, but it weakens this particular claim.)

2. **k=10 truncation choice not analyzed across problem sizes.** The paper reports that k=10 captures ~85% of matrix information (line 91) but does not specify the problem size at which this measurement was taken, nor does it analyze how reconstruction quality ($\|U_k\Sigma_k V_k^\top - D\|_F$) degrades as n grows to 200, 500, 1000 with fixed k=10. The strong empirical generalization results mitigate this concern, but the design choice would benefit from explicit validation across sizes.

3. **Minor theoretical imprecision between standardization and SVD derivation.** Algorithm 1 standardizes $D$ before SVD ($D \leftarrow (D-\mu)/\sigma$), but the theoretical derivation in Section 4.1 (Definition 1, Eq. 5) assumes SVD is applied to the unstandardized $D$, yielding $XW_1(XW_2)^\top \approx D$. When SVD is applied to the standardized matrix, the reconstruction is $XW_1(XW_2)^\top \approx (D-\mu)/\sigma$, not $D$ directly. The learnable linear layer (Algorithm 1, line 7) can compensate, but the gap between theory and implementation should be acknowledged.

4. **Missing training time comparison.** RADAR's training time is reported (39h for ATSP, 55h for ACVRP) but not compared to baselines. This is useful practical information that readers would expect.

### Trivial

1. **HGS negative gaps with infeasible solutions (Table 1).** HGS-Short and HGS-Long are marked as yielding infeasible solutions, yet their negative gaps (e.g., -8.83%) are still displayed. The footnote explains this, but presenting objective values for infeasible solutions alongside gaps computed against an optimal baseline is potentially misleading.

---

## Nice-to-Haves

- **Attention pattern analysis for Sinkhorn.** The paper claims Sinkhorn captures "dynamic asymmetry" by making attention scores aware of both $i$'s and $j$'s neighborhoods. A visualization or quantitative analysis of how Sinkhorn attention matrices differ from softmax attention in asymmetric settings would strengthen this mechanistic claim.
- **Failure mode analysis.** The paper could discuss conditions where RADAR might struggle (e.g., extreme triangle inequality violations, pathological matrix structures), which would be useful for practitioners.
- **Reconstruction quality across problem sizes with fixed k=10** (see Weakness 2 above).

---

## Removed Points

These points from the input review were removed or downgraded for the reasons given:

- **"Dynamic asymmetry is a semantic nitpick about naming."** Not a substantive weakness.
- **"SVD implementation details not in Algorithm 1."** Addressed in Section 6.1 ("GPU-accelerated, randomized, truncated SVD"). Minor presentation issue, not a reproducibility concern.
- **"LKH performance unexplained on ACVRP."** The critic acknowledged mid-argument that larger instances having higher objective values is expected. No weakness.
- **"Real-world comparison set is limited."** Reusing reported numbers from RRNCO is standard practice and does not constitute a flaw.
- **"Related works section is perfunctory."** The assessment is subjective and the section adequately covers the relevant literature.
- **"No analysis of attention patterns."** Moved to Nice-to-Haves.

---

## Novel Insights

None beyond the paper's own contributions.

---

## Suggestions

1. Qualify the claim in Section 5.3 to "RADAR consistently achieves lower costs and smaller optimality gaps among learning-based methods across all tasks" (or similar).
2. Either add RRNCO to the multi-task comparison (even as a single-task adaptation) or explicitly state why it was omitted.
3. Report reconstruction quality ($\|U_k\Sigma_k V_k^\top - D\|_F$) for n=100, 200, 500, 1000 with k=10 to validate the fixed-k choice at larger scales.
4. Clarify the relationship between the theoretical derivation (unstandardized D) and Algorithm 1 (standardized D) in Section 4.1.

---

## Score and Decision

The paper addresses a genuine, under-explored problem with a principled approach. The SVD-based initialization is theoretically grounded and empirically effective. The experimental evaluation is unusually thorough. The weaknesses are bounded and fixable: one overclaiming issue in the prose, one missing baseline in a supplementary experiment, and a few minor presentation concerns. None of these threaten the core contribution.

MY FINAL SCORE: <score>8</score>
MY FINAL DECISION: <decision>Accept</decision>