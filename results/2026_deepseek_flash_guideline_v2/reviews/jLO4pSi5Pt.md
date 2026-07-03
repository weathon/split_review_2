Now I have all the information I need. Let me write the final consolidated review.

## Summary

This paper introduces L-TTA, a method for test-time adaptation (TTA) of vision-language models under long-tailed test distributions. It identifies two failure modes (text-induced tail erosion and modality-bias amplification) and proposes three co-designed components: Synergistic Prototypes (dual prototype banks with different update strategies), Rebalancing Shortcuts (learnable cross-attention vectors with a class re-allocation loss), and Balanced Entropy Minimization (a modified entropy loss with confidence-gated penalty). Experiments span 15 datasets across three benchmarks at imbalance ratios of 10, 20, and 50, showing consistent improvements over prior TTA methods. This is the first systematic study of long-tailed TTA for VLMs.

## Strengths

- **First systematic study of LT-TTA for VLMs with identified failure modes (§1, lines 37–41).** The paper formalizes two failure modes (Text-induced Tail Erosion and Modality-bias Amplification) that go beyond what generic long-tailed learning or unimodal TTA methods address. This problem analysis is a clear contribution that directly motivates the bi-modal design of L-TTA.

- **Exclusionary Prototypes are a genuinely novel mechanism that solves the tail-class prototype update problem (§3.2, Eq. 5, lines 106–110).** Unlike TDA's "negative cache" which only updates the predicted class, EPs update prototypes for *all* classes using every view, weighted by a prediction-derived coefficient. This means tail-class prototypes can be updated even when tail-class samples are rare. The design is explicitly contrasted with TDA and the mechanism is correctly grounded — when a class is improbable (\(\phi_c\) large), the new sample contributes more to its EP update, which is the opposite of what the Harsh Critic claimed.

- **Consistent empirical gains across 15 datasets, three imbalance ratios, and multiple backbones (Tables 1, 2, 3, 5).** L-TTA achieves the best averaged accuracy and macro-F1 in nearly every setting (e.g., Table 1 OOD Average Acc. 65.97 vs. next-best DPE at 64.50; Table 2 averaged Mac. 63.44 vs. next-best DPE at 61.24). Gains extend to ViT-L/14, ViT-H/14, SigLIP-L/16, and MetaCLIP-BigG (Table 5). The macro-F1 advantage (e.g., +2.20% averaged in Table 2) directly confirms the claimed class-balancing capability.

- **Theoretical grounding of why standard EM harms tail classes (Propositions 1–2, lines 132–142).** Proposition 1 formalizes that standard EM pushes head-class logits up and tail-class logits down. Proposition 2 states that BEM reduces this gradient gap. While the statements are informal, they provide useful theoretical motivation that prior TTA methods lack in long-tailed settings.

- **Efficiency analysis with clear comparison (Table 4).** L-TTA (1.45h) is over an order of magnitude faster than RLCF (18.30h) and WATT (27.70h), while achieving the highest harmonic mean on both benchmarks.

- **Component ablation confirms synergy (Table 6).** Removing either DP or EP degrades macro-F1 by 2–4%, removing RS causes further degradation, and SyP+RS+BEM gives the best result. All three components contribute as claimed.

- **Robustness to dynamic class ordering (Table 7, lines 356–358).** L-TTA maintains stable accuracy and macro-F1 as the sampling probability \(\epsilon\) for tail-class samples varies from 0 to 2/3, on both ImageNet and Flowers. This partially addresses streaming-order concerns.

## Weaknesses

### Fatal
None.

### Major

- **TTA streaming order is underspecified in the main experiments (§4, Tables 1–3).** The paper constructs long-tailed test sets by subsampling originally balanced datasets into an exponential decay curve, but never states the *order* in which samples are presented to the model during sequential TTA. This is critical: if head samples are concentrated early, the model may over-adapt to head classes before tail samples appear; if the order is random, tail samples are uniformly sparse throughout. The only discussion of ordering is the "dynamic head/tail-class shifts" ablation (Table 7), but the main protocol's ordering is entirely unspecified. Without this detail, the evaluation is not fully reproducible, and the baseline comparisons could be confounded if baselines were run with a different ordering assumption. The Table 7 ablation partially mitigates this concern (showing L-TTA is stable across ordering conditions), but does not specify what ordering was used to produce the main results.

- **BEM's class-prior estimation from pseudo-labels creates a potential confirmation-bias loop (§3.2, Eq. 9, line 138).** BEM modifies logits with a penalty term involving the class prior \(\pi\), which "is continually updated based on the current predicted pseudo-labels" (line 138). This creates a loop: biased predictions → biased prior → biased penalty → more biased predictions. The paper claims this differs from standard logit adjustment (which uses true class frequencies), but never tests the simpler baseline of combining an existing TTA method with *true* (known) class frequencies via logit adjustment. The confidence-gating term \((1-\tilde{\mathbb{P}})^\beta\) partially mitigates this concern by down-weighting confident (likely head) classes, but the issue remains unaddressed empirically.

### Minor

- **No standard deviations reported despite 5 runs (Tables 1–3).** The paper states "5 runs for each experiment" but reports only point estimates across all main tables. TTA methods can exhibit variance due to sensitivity to sample order and prototype initialization. Without variance information, the reader cannot assess whether reported improvements are statistically reliable.

- **Notation ambiguity in Eq. 9 (line 136).** \(\tilde{\mathbb{P}}\) is used in the definition of \(z'\) and as the argument to \(\mathbb{H}'\), but it is not explicitly defined before its first use. From context it likely refers to the model's original softmax predictions (i.e., \(\sigma(z)\)), but this should be clarified. The notation is inferable but technically incomplete.

- **Inconsistency in hyper-class vector count \(K\) (line 208 vs. line 334).** Implementation details state \(K = 0.3\) (line 208), but the ablation study finds that "setting \(K = 0.2\) yields the best performance" (line 334). Since \(K\) represents a fraction of the number of classes (the values 0.2–1.0 in Fig. 4c are clearly proportions), this discrepancy means the main experiments may not have used the optimal setting, or the two numbers refer to different things. This should be clarified.

- **Proposition statements are informal (lines 132, 140).** The propositions state we "split \(C\) into \(C_{\text{head}}\) and \(C_{\text{tail}}\) with certain measurements" without specifying the measurement or split criterion. While full proofs are deferred to the appendix (removed), the main-text statements are too vague to evaluate as formal claims.

### Trivial
- Minor formatting issues in Eq. 4 (norm bracket placement is mangled by the PDF parser — this is not an author error).
- The paper could clarify the intuition for the affinity function \(\mathcal{A}(x) = \lambda_1 \exp(-\lambda_2(1-x))\) in Eq. 8.

## Nice-to-Haves
- Test the combination of existing TTA methods with logit adjustment using the *true* (known) test-set class frequencies. This would help isolate whether BEM's advantage comes from its confidence-gating mechanism or simply from any form of logit adjustment.
- Track the estimated class prior \(\pi\) vs. the ground-truth \(\pi\) over the course of the stream to empirically verify that the pseudo-label-based estimation does not drift.
- Clarify the streaming order used in main experiments and ideally test sensitivity to order as a controlled variable (head-first, tail-first, alternating, random) for both L-TTA and a strong baseline.
- Report standard deviations for the main results (Tables 1–3).

## Removed Points
*These points were raised by the reviewers but are removed after verification against the paper.*

- **"EP naming is misleading; EPs store high-probability features, not improbable ones."** This is factually wrong. In Eq. 5, when a class is improbable (\(\mathbb{P}(y_c|\tilde{x})\) is low), \(\phi_c\) is large, and the new sample contributes *more* to the EP update (since \((N - \phi_c)\) is smaller, reducing the weight of the old prototype). EPs correctly store improbable features. REMOVED — reviewer misread the equation.
- **"The HM metric is non-standard."** The harmonic mean of accuracy and macro-F1 is a reasonable design choice that penalizes imbalance; this is a methodological preference, not a weakness. REMOVED.
- **"The RS/MoE connection is not sufficiently justified."** The paper explicitly draws the inspiration and explains the reasoning (lines 116–120). Whether the connection is convincing is a design judgment, not a flaw. REMOVED.
- **"Preliminaries notation is overly complex (Eq. 1)."** While Eq. 1 shows intermediate features across layers that are not all used later, this is a minor stylistic observation. REMOVED as a formatting/style nitpick.
- **"Figure 2 is only qualitative."** Figure 2 includes macro-F1 values — a quantitative metric — alongside t-SNE visualizations. The main quantitative results are in Tables 1–3, not Figure 2. REMOVED — not a substantive weakness.
- **"Proposition 2 only shows gradient gap reduction, not guaranteed LT generalization."** This is true of essentially all theoretical results in deep learning (which provide motivation, not guarantees). Holding the paper to a higher standard than the field uses is unreasonable. WEAKENED to note in Minor section.

## Novel Insights
None beyond the paper's own contributions. The Harsh Critic identified the streaming-order underspecification, which is a genuine gap, but this is a methodological oversight rather than a novel insight about the paper's strengths.

## Suggestions

1. **Specify the streaming order in the main experiments** (is it random? head-first? fixed seed?) and add an experiment that systematically varies order (head-first, tail-first, alternating, random) for L-TTA and a leading baseline. This would either validate robustness (strengthening the contribution) or reveal a confound (requiring caveats).
2. **Add an experiment combining TPT or DPE with ground-truth logit adjustment** using the known class frequencies (which are available from the subsampling procedure). This directly tests whether BEM's advantage comes from its confidence-gating mechanism or merely from any form of logit modification.
3. **Report standard deviations** for the main results (by default from the 5 runs already conducted).
4. **Clarify Eq. 9**: define \(\tilde{\mathbb{P}}\) explicitly (as \(\sigma(z)\), the softmax of the original logits) before using it. Resolve the \(K\) discrepancy (0.3 vs. 0.2) and explain whether \(K\) is a count or a fraction.
5. **Track the estimated class prior \(\pi\) vs. ground-truth \(\pi\)** over the stream to verify that pseudo-label-based estimation does not drift toward head-class bias.

## Score and Decision

I calibrate this paper as follows. The paper tackles a genuinely new and well-motivated problem (first to study LT-TTA for VLMs), proposes a method with three co-designed components that are individually and collectively ablated, and evaluates broadly across 15 datasets, 3 imbalance ratios, and multiple backbones with consistent improvements. This is a substantial and solid contribution.

The weaknesses are real but addressable: the streaming-order omission weakens reproducibility but does not invalidate the results (especially given the ordering-robustness test in Table 7); the BEM prior-estimation concern is partially mitigated by the confidence-gating mechanism but would benefit from an explicit comparison with ground-truth logit adjustment. No weaknesses are fatal — the core contribution (problem identification + method design + comprehensive evaluation) stands.

This paper sits solidly in the **borderline-accept / accept** range. The contribution is meaningful and the evaluation is thorough, but the methodological gaps (especially streaming-order specification and BEM prior estimation) warrant caution and should be addressed before final acceptance.

**MY FINAL SCORE: <score>7</score>**
**MY FINAL DECISION: <decision>Accept</decision>**