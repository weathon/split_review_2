Now let me write the final consolidated review.

## Summary
This paper introduces L-TTA, the first test-time adaptation (TTA) method for Vision-Language Models (VLMs) under long-tailed test distributions. It proposes three co-designed components: Synergistic Prototypes (SyPs) with deterministic and exclusionary prototypes, Rebalancing Shortcuts (RSs) with a class re-allocation loss, and Balanced Entropy Minimization (BEM) to counter head-class bias. The method is evaluated extensively on 15 datasets across OOD, cross-domain, and corruption benchmarks with multiple imbalance ratios and backbones.

## Strengths
1. **Well-motivated problem framing.** The paper identifies a genuine gap — existing VLM TTA methods assume balanced test distributions while real test streams are often long-tailed. The two identified failure modes (text-induced tail erosion and modality-bias amplification) are concretely motivated with specific illustrative observations (Figure 1).

2. **Comprehensive evaluation.** 15 datasets across three benchmarks (OOD, cross-domain, corruption), three imbalance ratios (10, 20, 50), multiple backbones (ViT-B/16, ViT-L/14, ViT-H/14, SigLIP-L/16, MetaCLIP-BigG, ResNet-50), and 11 baselines. Results consistently show L-TTA at or near the top, with notable gains in macro-F1 — the metric that directly measures class-balancing capability. For example, on the OOD benchmark at imb=10 (Table 1), L-TTA's macro-F1 of 61.18% surpasses the next-best method (MTA at 59.65%) by 1.53 points.

3. **Favorable efficiency-accuracy trade-off (Table 4).** L-TTA achieves its results with 1.45h runtime and 1.89GB memory on ImageNet, substantially cheaper than methods like RLCF (18.30h) or WATT (27.70h), while outperforming them on harmonic mean metrics.

4. **Ablation studies confirm component contributions (Table 6, Figure 4).** Each component (DP, EP, RS, BEM) contributes incrementally, with the full system outperforming any subset. Sensitivity analyses show the method is not brittle within a reasonable range.

## Weaknesses

### Fatal
None.

### Major
1. **Missing empirical comparison against TTA methods augmented with standard LT techniques (Section 3.2).** The paper asserts that combining existing TTA with classic LT approaches like logit adjustment (Menon et al., 2020) or balanced softmax (Ren et al., 2020) would "further exacerbate the model's bias toward the head classes and damage the decision boundaries." This is a central motivation for the paper's co-designed approach. However, none of the 11 baselines in Tables 1–3 includes a combination of an existing TTA method (e.g., TPT, TDA, DPE) with a standard LT technique applied at test time (logit-adjusted softmax, class-balanced re-weighting, post-hoc logit scaling). Without these comparisons, the claim that L-TTA's specific co-design is **necessary** (rather than merely sufficient) is not fully supported — a simpler hypothesis that adding a logit-adjustment term to TPT's entropy minimization would recover most gains is not ruled out. Given that this is the central thesis motivating the paper's design, this is the most significant gap.

2. **EP update formulation (Eq. 5) is under-specified with unclear counter semantics.** The EMA update for Exclusionary Prototypes uses a counter N_{c,s}^{EP} that "increases by 1 at each step" for all classes c simultaneously (since the update applies ∀c ∈ C at each step). This means N_{c,s}^{EP} is the same for every class (equal to the global step s), so the effective EMA momentum is identical regardless of how many actual samples of a given class have been observed. Additionally, subtracting φ_c (a value in [0,1]) from the integer counter N_{c,s}^{EP} is an unconventional EMA formulation whose effect is not discussed. Since the same visual embedding f(x̃_i) is added to every class's EP, differentiated only by the φ_c weights, it is unclear whether EPs produce class-discriminative features or converge toward a shared centroid. No analysis (qualitative or quantitative) is provided to verify the EP behavior.

### Minor
1. **Proposition 1 is stated without explicit assumptions.** The proposition asserts E_{i~C_head} ∇_{z_i} H < 0 < E_{i~C_tail} ∇_{z_i} H for long-tailed TTA tasks. Whether this holds depends on specific conditions (e.g., that most head-class samples are correctly predicted with high confidence while most tail-class samples are misclassified). The main text states the inequality without caveats about these assumptions; the proof is deferred to the appendix. A brief statement of the conditions under which the inequality holds would improve clarity.

2. **DELTA is mentioned in related work but not evaluated.** The paper identifies DELTA (Zhao et al., 2023a) as a TTA method that "uses batch-renormalization and online re-weighting to reduce class bias" — a directly relevant baseline for class-imbalance-aware TTA. Despite this, DELTA is not included in any comparison. The paper argues that unimodal methods amplify modality mismatch when applied to VLMs, but including DELTA (or explicitly explaining why it is not comparable) would strengthen the evaluation.

3. **Test stream ordering protocol not specified.** TTA is inherently sequential, and sample arrival order can significantly affect prototype-based methods. The paper creates long-tailed test sets by subsampling but does not state the ordering protocol (e.g., random, decreasing class frequency). Table 7 partially addresses this by varying when tail samples appear, but the default protocol should be stated for reproducibility.

### Trivial
None.

## Nice-to-Haves
- Add an explicit mapping between the two identified failure modes (text-induced tail erosion, modality-bias amplification) and the specific design components that address each.
- Include a brief limitations discussion (e.g., reliance on known class priors, assumption that all test classes are known a priori).
- Clarify whether the EMA update for the entropy threshold θ uses a fixed momentum (unlike the counter-based prototype updates).

## Removed Points
These points are flagged to be removed, treat them with caution:
- **"Code: ." placeholder reference**: This is a parser artifact — the appendix (where the link would be) was stripped during PDF extraction.
- **Table 4 and Table 7 formatting concerns**: Issues like "1.54<×n" and garbled Flowers columns are parser artifacts from PDF extraction, not author errors.
- **Eq. 8 prediction logic concern**: The reviewer questioned whether subtracting EP affinity was correct. Reading the paper: EPs store "the most improbable features of each class" — high similarity to an EP means the sample has features improbable for that class, so subtracting reduces the logit, which is the intended behavior. The critique reflects a misunderstanding.
- **EP vs DP EMA asymmetry**: The noted asymmetry (counter-based vs. fixed momentum) is a minor implementation detail, not unusual in prototype systems.
- **Conclusion lacks limitations discussion**: Moved to Nice-to-Haves.
- **Proposition 1 caveats**: Handled as a Minor weakness above.
- **General speculation about EP collapse without evidence**: The concern about EP convergence toward a centroid is reasonable in the Major weakness about under-specification; the removed version is the purely speculative framing without anchoring to the paper's text.

## Novel Insights
Beyond the paper's own contributions, the key insight from the reviews is that the EP update counter N_{c,s}^{EP} — which advances identically for all classes at every step — serves as a global time step rather than a per-class sample count. This means φ_c is the sole mechanism differentiating per-class EMA rates. Whether this design reliably produces class-discriminative "exclusionary" prototypes or inadvertently smooths all EPs toward a shared representation is a question the paper does not address. This dynamic is genuinely novel and not present in prior prototype-based TTA methods like TDA.

## Suggestions
1. **Add combined baselines**: Augment at least 2–3 existing TTA methods (e.g., TPT, TDA, DPE) with standard LT modifications (logit-adjusted softmax, class-balanced re-weighting, or post-hoc logit scaling). If L-TTA still outperforms these, the "necessity of co-design" claim is strongly supported. Either outcome would be informative.
2. **Clarify EP update dynamics**: Provide even a brief qualitative analysis (e.g., nearest-neighbor visualizations of DP vs. EP features per class) to verify that EPs of different classes diverge meaningfully. Clarify whether N_{c,s}^{EP} is a per-class counter or a global step counter.
3. **State test stream ordering**: Specify the default sample ordering protocol and ideally evaluate under multiple orderings.

## Score and Decision

Let me calibrate by comparing with retrieved anchors. The key anchors are:

- **BLG (avg 4.67, Reject)**: CLIP + long-tailed recognition. Less comprehensive evaluation, weaker technical novelty. Current paper is substantially stronger.
- **ROSITA (avg 4.67, Reject)**: VLM open-world TTA. Similar scope to the current paper but with weaker evaluation, fewer baselines, and more severe methodological gaps. Current paper is substantially stronger.
- **DOTA (avg 6.00, Reject)**: VLM distributional TTA. Had fundamental ambiguities about distribution estimation with single samples and unrealistic human-in-the-loop requirements. Current paper has no fatal methodological flaw and broader evaluation.
- **Multi-Label TTA with BEM (avg 6.25, Accept)**: Novel TTA setting with good evaluation but presentation clarity issues. Comparable severity of weaknesses to current paper.

**Round 1 bracket**: Based on anchors, the plausible range is [5.5, 7.0]. The paper is clearly stronger than the 4.67-level papers but has a significant enough evidential gap (missing combined baselines) that keeps it from the 7+ range.

**Final calibration**: The paper's strengths (clear problem motivation, 15 datasets, 11 baselines, multiple backbones, strong ablations, efficiency analysis) and weaknesses (missing combined baselines, EP under-specification) place it similarly to the Multi-Label TTA paper (6.25, accepted). However, the missing combined baselines gap is somewhat larger in significance than the clarity issues of that paper, offset by the broader evaluation. A score at the boundary between borderline accept and borderline reject is appropriate.

MY FINAL SCORE: <score>6.0</score>
MY FINAL DECISION: <decision>Reject</decision>