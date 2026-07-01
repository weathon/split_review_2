## Summary

This paper proposes OML, a brain-inspired hierarchical modular neural network for online multimodal learning that adds three capabilities beyond prior work (ART, AEN): (1) a reference extraction algorithm that identifies which specific feature dimensions a word refers to (e.g., color vs. shape), (2) a conflict-detection mechanism that compares current input against learned knowledge, and (3) human-in-the-loop interaction where the system asks questions and updates based on user answers. Experiments on fruit and home-object datasets show consistent accuracy improvements over existing online baselines.

## Strengths

- **Reference extraction via variance stabilization is a genuinely novel and well-motivated contribution.** Section 3.4 identifies a real gap—existing online multimodal methods treat name words and attribute words identically, unable to distinguish that "apple" refers to shape+color while "red" refers only to color. The approach of tracking which feature dimensions stabilize across repeated exposures (via coefficient of variation) to infer the referent is intuitive and directly addresses this gap.

- **Conflict detection with user querying introduces a capability absent from prior work.** The four-case taxonomy of visual/auditory recognition states (Section 3.5, cases 1–4) provides a principled structure for when and how to query the user, producing context-specific questions (e.g., "The object I recalled does not look like the current visual input, are you sure?"). This contrasts with ART and AEN, which simply bind input pairs without any check for inconsistency.

- **Consistent empirical advantage over the two existing online baselines (ART and AEN).** In Table 1 (baseline), OML outperforms ART and AEN across all 8 rows (close/open, V→A, A→V). In Table 2 (precise referring), OML leads across all 8 rows. In Table 3 (modal extension), OML outperforms AEN across all 12 rows. The margins are modest (2–6 pp) but consistent.

## Weaknesses

### Fatal

None.

### Major

1. **The human-in-the-loop mechanism—a core claimed contribution appearing in the paper's title—is not actually evaluated with human interaction.**  
   Line 240 states: *"if the question posed to the user by OLM remains unanswered for a certain period of time, we set the answer to be positive."* This means every question is automatically answered "yes." The paper does not report: how many questions were asked, the distribution of positive vs. negative answers, any experiment with real human users (even a small-scale study), or how the system behaves with noisy/wrong user answers. The only direct result (line 250) is a single sentence: *"when we randomly add 10% of word-image or word-taste data pairs with incorrect matches, OML is able to detect all conflicts and raise appropriate questions"* — with no detail on how detection accuracy is measured or what "all conflicts" means. A contribution that hinges on interactive learning must demonstrate the interaction works.

2. **No statistical significance or variance is reported for any experimental result.**  
   All tables (1–3) report single accuracy numbers. Given that online learning with dynamic neuron creation and hard thresholds can be path-dependent, single-run results are insufficient to establish reliability. It is impossible to assess whether OML's margins over ART/AEN are robust or within noise, or whether the "close environment" gap between OML and offline methods is meaningful. Multiple runs with different random seeds and reporting of mean ± std are standard and necessary here.

3. **No ablation or component analysis is provided.**  
   The paper proposes three claimed innovations: (a) the hierarchical modular architecture with ascending/descending/lateral pathways, (b) the reference extraction algorithm, and (c) the conflict detection/interaction mechanism. None is ablated. Without removing components (e.g., replacing reference extraction with a uniform treatment of all word types, disabling conflict detection, removing lateral connections), we cannot attribute the results to the claimed mechanisms rather than to other architectural choices (threshold rules, Fourier transform signaling, or the dynamic neuron growth strategy).

### Minor

1. **The open-environment comparison against offline methods is not informative for establishing OML's value.**  
   Lines 246–247 report that offline methods (DAE, DBM, DJSRH, NRCH, FUME) drop in accuracy when classes appear sequentially across partitions. These methods were never designed for online/continual learning—they use multiple passes over a single static partition. Showing that a method built for online learning handles online learning better than methods not built for it does not strengthen the paper's case. This comparison should have been presented as context (the expected behavior of offline methods), not as evidence of OML's superiority.

2. **Baselines are scored under different, more lenient criteria than OML, conflating the accuracy metric.**  
   The paper states (line 248) that when querying a baseline with "hóng sè" (red), the baseline returns all features (shape and color) of red objects and *"we count this as a correct result for them in Table 2."* The same concession is applied to AEN in Table 3 (line 250). While the paper is transparent about this and the direction of the bias favors baselines (making OML's margins conservative), the metric is not applied consistently. The results should also be reported with a consistent metric so that the reader can compare fairly.

3. **The reference extraction uses a coefficient of variation (\(r = \sigma \oslash \mu\)) without addressing the case where \(\mu \approx 0\).**  
   In Section 3.4 (Eq. 7 and surrounding text), dimensions with small \(r\) are flagged as "referred to." If a feature dimension has mean activation near zero (common with normalized or sparse features), the coefficient becomes numerically unstable or undefined. The paper does not discuss this edge case or any stabilizing mechanism.

4. **Existing feature neuron weights do not adapt after initialization; the method is more accurately described as a memory-augmented architecture than a learned representation system.**  
   The paper describes how new FNs and UANs are added with weights set to current input features (Section 3.5), but there is no learning rule that updates existing neuron weights. Only the statistics \(\mu\) and \(\sigma\) of word neurons are updated incrementally (Eq. 8). This design choice is workable (and common in ART-like systems), but the paper's framing (online "learning") should be precise about the extent of adaptation.

5. **Evaluation is limited to small, hand-crafted feature domains.**  
   The datasets (Fruits, HomeF) are small-scale and limited to fruits/object-color attributes. Features are hand-crafted (Fourier descriptors for shape, mean color, MFCCs). The paper has not demonstrated that the method works with modern learned feature extractors or on broader multimodal domains (video+text, image+audio beyond speech). Generalizability claims are therefore unsupported.

### Trivial

- The threshold \(r = 0.5\) for reference extraction (Eq. 7) and \(\theta\) set to a quarter of the weight norm (Eq. 1) are fixed with no sensitivity analysis.
- The purpose of the frequency-parameter encoding in Eq. (1) is stated but not justified—why a cosine-basis expansion is preferable to a simpler similarity metric is not explained.

## Nice-to-Haves

- Report the number of questions asked during conflict detection and the distribution of positive/negative answers under the simulated setting.
- Add a small-scale real user study (5–10 participants) to validate the interaction mechanism, or candidly acknowledge that this claim is only simulated.
- Discuss the memory/parameter footprint of OML after training (how many neurons are created) compared to baselines.
- Conduct a sensitivity analysis on the threshold \(r\) used in reference extraction.

## Removed Points

These points were flagged by the harsh critic but are removed from the main review for the reasons given:

- **"Comparison against continual learning baselines (EWC, experience replay) is missing."** — Removed per the instruction not to mention missing related works; the meta-reviewer cannot independently verify what baselines exist or are appropriate for this setting.
- **"The Fourier transform applied to an already frequency-encoded signal is conceptually odd."** — Removed. The cosine basis expansion in Eq. (1) produces a time-domain signal; applying a Fourier transform to it in Eq. (6) is standard signal processing, not conceptually odd. The criticism misunderstands the method.
- **"Brain-inspired language is not substantiated by neuroscience."** — Removed as a superficial stylistic criticism that does not affect the paper's technical validity.
- **"Computational cost is not discussed."** — Demoted from the critic's "Missing Parts" to Nice-to-Haves; it is a reasonable request but not a core weakness.
- **"No comparison against continual learning baselines adapted for multimodal settings."** — Removed for the same reason as above; the meta-reviewer cannot confirm the existence of such adapted baselines.
- **"The paper leans heavily on brain-inspired language."** — Removed as a style nitpick that does not affect the evaluation of the method or results.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. Run all experiments with at least 5 random seeds and report mean ± std.
2. Conduct an ablation study that removes reference extraction, conflict detection, and lateral connections individually to isolate each component's contribution to accuracy.
3. Conduct at least a small-scale real human interaction study (even 5–10 participants) or, if infeasible, reframe the paper's claims to accurately reflect that the human-in-the-loop mechanism was only simulated with positive-only automatic answers.
4. Report results with a consistent metric for all methods (not scoring baselines more leniently) in addition to the current generous scoring.
5. Address the numerical stability of the coefficient of variation when \(\mu \approx 0\).
6. Clarify in the method description whether and how existing neuron weights are updated after initialization.

## Score and Decision

MY FINAL SCORE: <score>5.0</score>
MY FINAL DECISION: <decision>Reject</decision>