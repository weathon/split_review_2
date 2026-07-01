## Summary

This paper proposes Automatic Complementary Separation Pruning (ACSP), a structured pruning method with two core ideas: (i) selecting components to retain based on *complementary* separation capabilities (enforced by clustering in a "graph space" of JM distances and picking the highest-weight component from each cluster), and (ii) automatically determining the per-layer pruning extent via the Kneedle algorithm on a Mean Simplified Silhouette (MSS) curve. The method is evaluated on VGG, ResNet, DenseNet, and MobileNet architectures across CIFAR-10/100 and ImageNet.

## Strengths

1. **Complementary selection is a genuinely different pruning principle.** Rather than ranking components independently by importance (which preserves redundancy when similar components both rank high), ACSP explicitly enforces diversity by selecting from different clusters in a separability space. The intuitive example in Section 3.3.2 (three components, two similar, one different) clearly motivates why this could be beneficial. This is a novel angle on the pruning problem.

2. **Automated pruning extent via knee-finding is practical and clean.** Determining layer-wise pruning ratios by finding the "knee" in an MSS-vs.-k curve (Section 3.4.1) removes a manual tuning step that many pruning methods still require. The approach is data-driven and requires no additional supervision or search, making it genuinely automatic for the pruning extent.

3. **Wall-clock latency is reported alongside FLOPs.** Table 2 provides actual inference timing measurements (batch and single-input, averaged over 100 runs). Many pruning papers report only FLOP reduction; ACSP at least provides real timing data so readers can assess actual inference behavior, even if the speed-ups are modest.

## Weaknesses

### Major

1. **No ablation study — the core claims are untested.** ACSP rests on two claimed innovations: (i) complementary selection via clustering in a separability space, and (ii) automatic pruning extent via Kneedle on MSS. The paper contains no experiments isolating either mechanism. Without comparing ACSP against simpler alternatives — e.g., (a) picking the top-k components by weight alone (no clustering), (b) uniform random selection of k components, or (c) fixed pruning ratios per layer instead of Kneedle — the reader cannot attribute the results to the proposed mechanisms rather than to the iterative fine-tuning protocol. The comparison of JM vs. other distance metrics (line 127) does not fill this gap, as it tests a different design choice. This is a significant evidential gap for a paper whose claimed novelty *is* those mechanisms.

2. **Headline speed-up numbers are FLOP-based and substantially overstate real inference acceleration.** The abstract and introduction lead with "significant speed-ups (e.g., 2.25× on ResNet-50)" (lines 33, abstract). However, the "Speed Up" column in Table 1 is defined as the ratio of FLOPs before and after pruning (line 174), not wall-clock time. Table 2 shows that the actual wall-clock speed-up for ResNet-50 on ImageNet is 1.07× (batch) and 1.09× (single) — a 2.25× FLOP reduction producing roughly 1.08× real speed-up. Across all models, average latency reduction is 8.78% (batch) and 5.56% (single). The paper acknowledges this gap briefly in Section 4.5 ("hardware utilization is not perfectly linear with FLOP count"), but the central framing in the abstract, introduction, and contributions list is built around FLOP ratios as though they represent inference acceleration. Since the paper's stated goal is "accelerating inference time," presenting FLOP reduction as "Speed Up" without qualification in the main results table is misleading.

3. **Baseline comparisons are not controlled for fine-tuning protocol.** ACSP uses iterative layer-by-layer pruning with 2–3 epochs of fine-tuning on 25% of the data after each layer (Section 4.1). The baseline results in Table 1 are taken from their original papers, which used varying and often more extensive fine-tuning or retraining schedules. Because ACSP gets multiple rounds of fine-tuning (one per pruned layer), any accuracy advantage could stem from the iterative protocol rather than the selection method. A proper comparison would re-run baselines under ACSP's fine-tuning protocol (or run ACSP under each baseline's protocol). Without this, the numerical comparisons in Table 1 do not constitute valid evidence of ACSP's superiority.

### Minor

4. **No variance or statistical significance reported.** Every accuracy in Table 1 is a single value with no standard deviation, confidence interval, or seed count. Fine-tuning is stochastic, and some accuracy differences between methods are tiny (e.g., ACSP +0.50 vs. SANP +0.45 on MobileNet-V2 CIFAR-10 — a 0.05% gap). Without variance estimates, it is impossible to assess whether any claimed advantage is meaningful.

5. **Greedy layer-by-layer pruning and cross-layer dependencies are not discussed.** Algorithm 1 prunes layers sequentially from first to last, fine-tuning after each layer. After pruning layer *i*, the activations flowing into layer *i+1* come from a partially pruned model whose distribution has shifted. This is a known source of compounding errors in layer-wise pruning, yet the paper does not discuss it or provide analysis to show that it is not a concern here.

6. **Table formatting errors.** Line 193 shows the ACSP row for MobileNet-V2 on CIFAR-10 incorrectly attributed to "(Gao et al., 2023)" (the SANP citation). In lines 216–217, both NS and ACSP show the same Δ accuracy value (-0.36) in **bold**, though the caption states that only the best result is bolded. These are minor but sloppy.

### Trivial

- The term "graph space" is used extensively (≈15 times) to describe what is actually a vector space of JM-distance vectors clustered with k-Medoids. The method is clearly described regardless, so this is purely a naming choice that does not affect correctness.

## Nice-to-Haves

- The paper would benefit from a discussion of when FLOP reduction *does* and *does not* translate to wall-clock speed-up, to help readers understand the practical applicability of the method.
- Comparing the iterative layer-by-layer procedure against a single-shot version (prune all layers at once using pre-pruning activations) would help quantify the benefit of the iterative fine-tuning schedule.

## Removed Points

The following points from the input review were removed:

- **"Graph space is terminological inflation" removed to Trivial** — The construction is clearly described; calling it "graph space" is a naming choice, not a substantive flaw.
- **"Automation claim oversells because it requires labeled data and forward pass"** — Every activation-based pruning method requires data. The automation claim is about pruning extent, not eliminating dataset requirements. This criticism is scope creep.
- **"Does not compare against DepGraph"** — Factually incorrect; DepGraph is cited in related work (line 40) and directly compared in Table 1 (ResNet-56, CIFAR-10, line 204).
- **"Component selection partially undermines complementary principle"** — The paper explicitly discusses this design choice (Section 3.4.2) and presents it as a deliberate balance between diversity and weight importance. This is not a weakness.
- **Generic/superficial strength claims** about "addressing an important problem" — removed. The three retained strengths are concrete and specific to the paper's contributions.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. **Run ablation studies.** Compare ACSP against (i) top-k by weight only, (ii) random selection, (iii) fixed pruning ratios — to isolate the effect of complementary selection and automated pruning extent.
2. **Reframe speed-up claims.** Lead with wall-clock latency numbers (Table 2), not FLOP ratios. If FLOP reduction is presented, clearly qualify that it does not directly equal inference speed.
3. **Re-run baselines under a consistent fine-tuning protocol** or thoroughly discuss how protocol differences affect comparability.
4. **Report variance** (multiple seeds, standard deviations) for at least the main settings.
5. **Fix the table errors:** remove the "(Gao et al., 2023)" attribution from the ACSP row and fix the double-bold on the DenseNet-40 row.

## Score and Decision

<score>4.5</score>
<decision>Reject</decision>