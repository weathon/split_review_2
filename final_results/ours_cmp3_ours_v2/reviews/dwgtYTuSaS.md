Now I have all the information I need. Let me produce the final consolidated review.

Here is the scoring calibration summary before I write the final review:

**Round 1 bracket:** After comparing to calibration anchors, I form an initial bracket of **5.0–6.5** for this paper.

**Key anchors used for calibration:**

| Anchor | Score | Decision | Comparison to this paper |
|--------|-------|----------|------------------------|
| VidEgoThink (Z5nqeTH24j) | 4.40 | Reject | Benchmark-only paper with limited novelty. This paper has a stronger contribution (new task formulation + benchmark + method). |
| PrAViC (jawV7vhGHw) | 4.25 | Reject | Real-time video classification framework with weak baselines. Similar evaluation weaknesses but paper under review has stronger core contributions. |
| EgoHOIBench (M8gXSFGkn2) | 7.00 | Accept | Benchmark + method with stronger evaluation. More polished but similar structure. Paper under review has weaker evaluation. |
| Test-Time Adaptation (1L52bHEL5d) | 6.00 | Accept | Egocentric adaptation paper with solid evaluation. Comparable contribution level. |
| CLDyB (RnxwxGXxex) | 5.67 | Accept | Continual learning benchmark paper. Similar "new benchmark" contribution, accepted despite some concerns. |
| Anomalies are Streaming (Y7jJN0VQ4y) | 5.71 | Reject | Continual learning for video anomaly detection. Despite higher avg score, rejected (wide score spread). |

**Narrowing:** Compared to accepted papers at 6.0 (Test-Time Adaptation, MMEgo), those papers had stronger experimental rigor (multiple seeds, comprehensive baselines). Compared to CLDyB (5.67, accepted), that paper had a more thorough evaluation with multiple analyses. The COAD paper's core contributions (task formulation + dataset) are at least as strong, but the evaluation is notably weaker. This places it at **5.5** — borderline accept.

Here is the final review:

## Summary
This paper introduces Continuous Online Action Detection (COAD), a new task formulation where models not only detect actions online but also continuously learn and adapt from streaming video in a single pass without storing data. It also curates Ego-OAD, a large-scale egocentric OAD benchmark from Ego4D (263h, 87 classes, 22,991 instances), which is the largest egocentric OAD benchmark to date. The paper proposes three training strategies adapted from existing work (state continuity, orthogonal gradient projection, non-uniform loss) and evaluates them on Ego-OAD and EPIC-KITCHENS.

## Strengths
1. **The COAD task formulation is genuinely novel and well-motivated.** The paper correctly identifies a gap: existing OAD models are trained offline and deployed statically, but wearable devices operate in personalized, dynamic environments where adaptation after deployment matters. Section 4 cleanly formalizes the causality, memory, and compute constraints of the COAD setting, and the contrast with standard OAD (Sections 4.3 vs. 4.5) is clearly drawn.

2. **Ego-OAD fills a genuine gap in available benchmarks.** Existing OAD datasets are predominantly exocentric (THUMOS14, TVSeries), and egocentric options (EPIC-KITCHENS) are domain-restricted. Repurposing the Ego4D MQ split yields 263 hours of diverse egocentric video with 87 action classes and 22,991 labeled instances — the largest egocentric OAD benchmark by a significant margin. The multi-label nature (36% instance overlap) reflects real-world ambiguity that prior datasets sidestep. This is a reusable community asset.

3. **The ablation study (Table 3) is informative and correctly executed.** The paper systematically ablates each proposed component and reports both in-stream and out-of-stream metrics. For example, orthogonal gradient projection primarily helps out-of-stream recall (+4.5%) but not in-stream mAP, and state continuity alone provides a small but consistent gain. This diagnostic detail is valuable and goes beyond what is typical.

## Weaknesses

### Fatal
None.

### Major
1. **No comparison to established continual learning baselines.** The paper compares COAD against only two baselines: Pretrained Only (no adaptation) and w/o COAD (the same architecture trained on in-stream data without any of the proposed strategies). Neither is a competitive baseline for assessing whether the orthogonal gradient approach offers advantages over standard forgetting-mitigation methods. No comparison is made against Elastic Weight Consolidation (EWC), Synaptic Intelligence, or other continual learning methods, even though the orthogonal gradient component (taken from Han et al., 2025) is the main mechanism for preventing catastrophic forgetting and the COAD setting is fundamentally a continual learning problem. The headline claims ("up to 20% improvement") are computed against the non-adaptive Pretrained Only baseline; the improvement over w/o COAD is substantially smaller (e.g., 76.0 vs 71.6 Top-5 on out-of-stream Ego). Without a continual learning baseline, the reader cannot determine whether the proposed approach is meaningfully better than existing alternatives or merely "better than doing nothing."

2. **EPIC-KITCHENS results show inconsistent performance that is not adequately analyzed.** On EPIC-KITCHENS (Table 2), COAD's in-stream Action mAP (7.9) and Top-5 Recall (20.5) are *worse* than the Pretrained Only baseline (9.6 and 22.9, respectively). The paper attributes this to "the fine-grained nature of the actions and annotations" in a single sentence without any supporting analysis — no per-class breakdown, confusion matrix, or analysis linking degradation to action granularity, label frequency, or action duration. Since COAD underperforms the non-adaptive baseline on one of the two tested datasets under several metrics, the claim that it is a general-purpose solution for egocentric OAD is weakened.

### Minor
1. **No statistical significance or variance reported.** Single-pass online training is inherently stochastic — the data order, random seeds, and initializations all affect results. None of the tables report standard deviations or multiple-seed averages. Given that several reported differences are small (e.g., 26.0 vs 25.5 mAP on out-of-stream Ego), the reader cannot assess whether these are stable improvements or within the noise.

2. **No existing OAD methods benchmarked on Ego-OAD in the standard protocol.** The paper introduces Ego-OAD as a new benchmark but only evaluates its own architecture (GRU-based, following An et al., 2023). Even in the standard non-continuous OAD protocol, the paper does not establish what a reasonable baseline on Ego-OAD looks like. Results from other architectures (e.g., LSTR, TeSTra, GateHub) would help calibrate the dataset for the community.

3. **No direct measurement of catastrophic forgetting.** The orthogonal gradient method is motivated as preventing interference between consecutive updates, but the paper never directly measures forgetting (e.g., by tracking performance on earlier portions of the in-stream data as new portions arrive). This is a standard analysis in continual learning and would directly support the paper's claims about the method's effectiveness.

4. **Related works section omits the continual learning literature.** Despite the method's reliance on orthogonal gradient projection from the continual learning literature (Han et al., 2025) and the COAD setting being fundamentally a continual learning problem, the related works section covers only OAD models and datasets. The connection to continual learning is unexplored, which limits the paper's positioning within the broader literature it draws from.

### Trivial
None.

## Nice-to-Haves
- Add at least one standard continual learning baseline (e.g., EWC or an online variant) to contextualize the orthogonal gradient method's effectiveness.
- Benchmark 2–3 existing OAD methods on Ego-OAD in the standard (non-continuous) protocol to establish reasonable baselines.
- Diagnose the EPIC-KITCHENS in-stream degradation with per-class analysis or confusion matrices.
- Report results with multiple random seeds (mean and std over 3–5 runs).
- Analyze the choice of projecting gradients against only the immediately preceding gradient (rather than a buffer or moving average) and ablate the number of past gradients used.
- Report computational/memory overhead of the orthogonal gradient projection relative to baselines, given the paper's motivation from resource-constrained devices.

## Removed Points
These points from the input review are excluded:
- **Typos ("Countinuous", "CODA"):** Removed per formatting rules (parser artifacts do not carry weight).
- **"No comparison to existing OAD methods" characterized as Critical Issue 2:** Downgraded to Minor — the dataset is primarily for the COAD task, and the Pretrained Only baseline already serves as a standard OAD benchmark. Benchmarking additional methods would strengthen the contribution but is not a critical omission.
- **"The orthogonal gradient projects against only one previous gradient" (insufficient ablation):** Removed — the paper does not claim to ablate this; it's a methodological choice that could be explored in future work but is not a weakness per se.
- **"Pretraining split too small inflates relative gains":** The paper explicitly states this provides "a weak initialization under limited supervision" (line 146), which is a deliberate experimental design choice rather than a flaw.
- **"The 'w/o COAD' baseline is essentially no regularization" — already subsumed into Major weakness #1** (lack of continual learning baselines).
- **"Claims about 7% improvement are computed relative to Pretrained Only" — already subsumed into Major weakness #1** (baseline inflation).
- **"Method novelty overstated" framing:** The paper acknowledges the sources of each component (An et al., 2023; Han et al., 2025). The critic's characterization is noted but the novelty of the task formulation and dataset stands independently.
- **"IID Training upper bound underspecified":** The specific hyperparameter details asked for are implementation details not critical to understanding the upper bound's role.

## Novel Insights
None beyond the paper's own contributions.

## Suggestions
1. **Add continual learning baselines** (at minimum EWC or an online variant) to Table 1 to position the orthogonal gradient method relative to established forgetting-mitigation approaches.
2. **Include variance** over 3–5 seeds in all tables, given the inherent stochasticity of single-pass training.
3. **Analyze the EPIC-KITCHENS failure** with per-class results or confusion matrices rather than a post-hoc attribution to "fine-grained actions."
4. **Benchmark at least one existing OAD method** on Ego-OAD in the standard protocol to establish the dataset's baseline performance for the community.
5. **Add a section on continual learning** to the related works and discuss how COAD relates to that literature.
6. **Frame headline claims** relative to the w/o COAD baseline (which disentangles the effect of any adaptation from the effect of the proposed strategies) rather than the non-adaptive Pretrained Only baseline.

MY FINAL SCORE: <score>5.5</score>
MY FINAL DECISION: <decision>Accept</decision>