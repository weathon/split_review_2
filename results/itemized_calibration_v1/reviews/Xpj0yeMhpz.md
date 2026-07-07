Now I have all the information I need. Let me write the final review.

## Summary

This paper identifies a gap in class-wise machine unlearning: prior work assumes the target concept to forget coincides with the class label. The authors introduce three new "mismatch" scenarios (target mismatch, model mismatch, data mismatch) that arise when the label domain of the forgetting data, the model output, and the target concept do not align. They propose TARF (TARget-aware Forgetting), a framework combining annealed gradient ascent on forgetting data with target-aware gradient descent on selected retaining data, guided by a "representation gravity" intuition. Experiments on CIFAR-10/100, ImageNet, TinyImageNet, stable diffusion, and TOFU/LLaMA demonstrate performance across the new settings.

## Strengths

1. **Problem framing is novel and well-motivated.** The observation that practical unlearning requests (privacy, copyright, safety) may not align with the pre-training label taxonomy is important and realistic. The four-way taxonomy (all matched / target mismatch / model mismatch / data mismatch) in Section 3.1 and Figure 1 provides a clear organizational structure that meaningfully expands the class-wise unlearning literature.

2. **CIFAR-10/100 results show dramatic improvements in mismatch settings.** In target mismatch and data mismatch (Table 3), baselines achieve Gap scores of ~20–50 while TARF achieves Gap ≈ 1 on both datasets. In model mismatch, TARF is competitive with or ahead of the best baseline (SCRUB). This is a categorical difference, not marginal.

3. **"Representation gravity" concept (Theorem 3.2 and Definition 3.3)** provides a useful lens for understanding why forgetting dynamics propagate along representation distances. While the theorem is a Lipschitz smoothness bound, connecting it to false-retaining-data identification via accuracy drops during gradient ascent (Phase I) is a clever practical application.

## Weaknesses

### Fatal
None.

### Major

1. **The "known number of target classes" assumption is underexplored and limits practical claims.** Line 61 states: "we assume that the number of classes in D_un belonging to the target concept is known in target mismatch forgetting." Phase I identifies false retaining data by ranking classes by accuracy drop and selecting the top-k, where k is this assumed-known number. In practice, a user might report a few examples without knowing the full semantic extent of the target concept. The paper mentions a β threshold alternative in passing but does not evaluate the method without the k-knowledge. This creates an evidential gap: the most practically realistic variant of the target mismatch setting is not tested. The paper should either provide experiments where k is unknown (using β alone) or clearly delineate this as a limitation.

2. **The TOFU/LLaMA results (Table 5) are concerning and under-discussed in the main text.** In the first block of Table 5, in the target mismatch setting, TARF achieves QA Prob on retaining data of 0.0094 — essentially zero, compared to CL(NPO)'s 0.4481. The main text (Section 4.2) says "we leave more details in Appendices E.3 and F.8" without acknowledging the apparent utility collapse. The table formatting is also garbled (multiple blocks with differing results; TARF(GA) and TARF(NPO) showing identical values across multiple rows), making interpretation difficult. If TARF destroys retaining QA probability in this setting, the qualitative claim that "TARF works" for LLM unlearning is not supported by the numbers as presented.

### Minor

3. **ImageNet-1k results show only marginal advantages over baselines.** On ImageNet (Table 4), TARF's Gap improvements over the best baseline are small: all matched (3.66 vs FT 3.82, Δ=0.16), target mismatch (3.97 vs FT 4.02, Δ=0.05), model mismatch (5.92 vs SCRUB 6.34, Δ=0.42), data mismatch (4.17 vs FT 4.24, Δ=0.07). Without standard deviations in the main table (deferred to Appendix F.7), these tiny margins make it difficult to assess whether TARF is meaningfully better than simpler baselines at scale.

4. **Table 2 (fine-grained superclass evaluation) shows TARF appearing twice with different values.** Lines 267-268 both list "TARF (ours)" with different metric values (UA 81.28 vs 74.70, Gap 2.65 vs 1.36). This appears to be either a reporting error or a formatting artifact that needs clarification.

5. **The β threshold heuristic is underspecified in the main text.** Line 152 says "setting the threshold β as the lowest value of top-10% data with in a descending order" — it is unclear what is being ranked, what "order" refers to, and how "top-10%" interacts with the known-classes assumption. The reference to Appendix E is noted, but the main text should provide a precise protocol for reproducibility.

6. **Theorem 3.2 does not derive TARF's specific design choices.** It establishes that loss dynamics differences between two subsets are bounded by representation distance — a consequence of Lipschitz smoothness (Assumption 3.1). It provides qualitative intuition but does not guide the annealing schedule k(t), the threshold β, or the three-phase structure. The method's components are justified by intuition and empirics, not by the theory.

### Trivial
7. **No standard deviations in main-text tables.** While the paper defers to Appendix F.7, the main results (Tables 3, 4) report single values, making it impossible to assess significance from the main text alone.

## Nice-to-Haves
- Adding standard deviations to the main-text tables would strengthen the empirical claims, especially for the ImageNet results where margins are small.
- Clarifying the TOFU experimental setup in the main text rather than deferring entirely to appendices would improve readability.
- A brief discussion of how TARF compares to the "withhold then fine-tune" heuristic would be useful context for practitioners.

## Removed Points
- **"Method components are standard techniques combined in a heuristic way"** (from Harsh Critic Weakness 4): This reflects a judgment about novelty level rather than a verifiable technical flaw. Combining known components to solve a newly identified problem is a valid contribution, and the problem taxonomy carries most of the weight. [REASON: Opinion about contribution framing, not a verifiable weakness.]

## Novel Insights
The reviews surface an important calibration point: the paper's strongest contribution is the problem taxonomy (identifying and formalizing the mismatch gap in class-wise unlearning), not the algorithmic novelty of TARF. The CIFAR results convincingly demonstrate that prior methods systematically fail on these settings, which is a finding that stands independently of whether TARF is the ultimate solution. This suggests the paper's primary value to the community may lie more in reframing the problem space than in the method itself.

## Suggestions
1. Run experiments for the target mismatch setting where the number of target classes k is unknown (using only the β threshold for selection), and transparently report whether performance degrades.
2. Acknowledge and discuss the TOFU/LLaMA retaining utility results directly in the main text — if the method destroys retention in the LLM setting, state this as a limitation rather than presenting results as unqualified evidence of efficacy.
3. Include standard deviations in the main tables, especially for ImageNet where margins over baselines are small.
4. Clarify the duplicate TARF rows in Table 2 and the garbled formatting in Table 5.
5. Provide a more precise specification of the β threshold in the main text (what is being ranked, how "top-10%" is computed).

---

**Calibration Anchors (all rounds):**

| Anchor | Path | Avg Score | Round | Itemized? | Comparison to this paper |
|--------|------|-----------|-------|-----------|--------------------------|
| PPU (Pseudo-Probability Unlearning) | Xagys9QD3T.md | 3.00 | 1 | No | Much weaker — foundational errors in optimization goal and privacy claims; this paper has no such foundational errors |
| UGradSL | hwXUmwJAq5.md | 3.00 | 1 | Yes | Weaker — flawed evaluation metrics (comparing to retraining incorrectly), incorrect problem statement; this paper correctly frames evaluation |
| MASIMU | BJfIDS5LsS.md | 2.50 | 1 | No | Much weaker — poorly executed multi-agent approach |
| Auditing Data Controller Compliance | 85X9awoVtv.md | 2.50 | 1 | No | Different topic (auditing), much lower quality |
| FIUBench (VLM Benchmark) | 0y3hGn1wOk.md | 5.40 | 1 | Yes | Similar quality — both introduce new problem framing; FIUBench had small dataset concerns, this paper has known-k and TOFU concerns |
| Adversarial Mixup Unlearning | GcbhbZsgiu.md | 5.00 | 1 | Yes | Most comparable — both propose new method + extensive experiments; this paper has more novel problem framing but more serious limitations |
| Forget Vectors at Play | 7tpMhoPXrL.md | 4.80 | 1 | No | Similar tier — novel perspective but limited scope |
| Evaluating Deep Unlearning in LLMs | CIN2VRxPKU.md | 5.33 | 1 | No | Similar tier — novel setting (logical deduction in unlearning) with good experiments |
| Rethinking LLM Unlearning Objectives | huo8MqVH6t.md | 6.00 | 1 | Yes | Stronger — more thorough theoretical framework (G-effect), multiple accepted reviews; this paper has stronger problem novelty but weaker theory |
| The Utility and Complexity of OOD Unlearning | HVFMooKrHX.md | 6.60 | 1 | Yes | Stronger — rigorous theoretical analysis with proofs; this paper is more empirical |
| Oblivious Unlearning by Learning | wAemQcyWqq.md | 5.67 | 1 | No | Stronger in novelty — clever oblivious setting, but limited empirical scope |

**Initial bracket from Round 1:** The paper sits between the 3.0-range papers (foundationally flawed) and the 6.0+ range papers (rigorous theory or comprehensive frameworks). Comparison with itemized anchors shows the paper shares heavy-weight positive items with the 5.0–5.4 range papers (novel problem framing, strong experimental results on primary benchmarks) while sharing heavy-weight negative items with those same papers (limited evaluation at scale, methodological assumptions not fully stress-tested). The TOFU utility concern is a distinguishing negative item that this paper has and the 5.0 anchors do not, preventing a higher score. The paper does not have the foundational errors (incorrect evaluation, flawed objectives) that characterize the 3.0 anchors. The bracket narrows to 4.5–5.5.

MY FINAL SCORE: <score>5.0</score>
MY FINAL DECISION: <decision>Accept</decision>