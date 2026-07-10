Now I have all the information needed. Let me produce the final consolidated review.

## Summary

This paper proposes the Fast and Slow Effect (FSE) framework to evaluate whether LLM/VLM-generated concept annotations are *sufficient*—self-contained enough that the concepts alone enable accurate class inference. The framework progressively collects concepts across five refinement stages (*Background* → *Superclass* → *Salient Features* → *Detailed Features* → *Auxiliary Features*), transitioning from a *fast mode* (direct visual inference, t=0) to a *slow mode* (concept-only inference, t>0). A new metric, the Class Representation Index (CRI), quantifies annotation sufficiency. The paper evaluates six LLM families across five datasets, finding that slow mode underperforms fast mode by 25%+ on fine-grained datasets, and demonstrates via a fused-mode experiment that the common "utility-as-proxy" evaluation paradigm can mask annotation insufficiency.

## Strengths

- **The motivating example (Figure 1) is strong and concretely grounds the problem.** It shows an AI correctly classifying a bird image but switching to the *wrong* class when forced to reason through only its own textual concepts. This cleanly illustrates a non-trivial failure mode where the model has implicit knowledge it cannot articulate—the paper's central empirical finding.

- **The utility-as-proxy critique is well-supported and is the paper's most impactful contribution.** The fused-mode experiment (Table 4) shows that joint image+concept inference scores ~90% CRI while concepts-alone inference scores ~50% under identical conditions. This cleanly demonstrates that end-to-end downstream performance can remain high even when concept annotations are insufficient—the visual modality dominates fusion, masking annotation quality. This is a meaningful methodological contribution to the XAI community.

- **The multi-model, multi-dataset evaluation is appropriately scoped.** Six model variants across three families (GPT, Llama, Qwen) and five datasets covering both fine-grained (CUB, Cars, Flowers) and general (CIFAR-100, Caltech-101) domains provides a reasonably comprehensive picture. The contrast between fine-grained (slow mode consistently underperforms) and general domains (slow mode catches up and surpasses fast mode on CIFAR-100 and Caltech-101) is a genuinely informative finding.

- **The semantically-related distractor selection is well-motivated.** The preliminary experiment (Table 1) shows that random distractors yield low contradiction rates (14–20%), while semantically related distractors more than double them (34–45%). This clean design choice ensures the evaluation is not trivially easy.

## Weaknesses

### Fatal
None.

### Major
- **The "Slow Mode Superiority" framing overstates what dual-process theory implies.** The paper states that "when both modes are available, the slow mode is expected to consistently achieve performance superior or at least comparable to the fast mode" (Section 4.2), citing Kahneman's dual-process theory. This conflates *reasoning mode* with *input modality*: fast mode (t=0) receives the full image, while slow mode (t>0) receives only textual concept summaries. Even in humans, replacing visual input with a written summary would impair fine-grained visual discrimination—not because the summary is "insufficient" in an absolute sense, but because visual information has higher bandwidth for this task. Dual-process theory describes cognitive styles, not modality transfer. The paper's actual argument—that concepts should be self-contained enough to support class inference (Definition 3.1)—stands on its own without this theoretical framing. The fast-vs-slow comparison is still informative as a measurement of an *articulation gap* (implicit vs. explicit knowledge), but the "Slow Mode Superiority" framing over-claims the theoretical backing for why the gap is surprising. The paper would be stronger by reframing this directly as measuring whether concepts are self-contained, without invoking dual-process theory to establish an expectation that is arguably unreasonable given the modality asymmetry.

### Minor

- **The CRI formula (Equation 2) contains a notational error.** It writes $CRI := 100\% \times \frac{1}{t} \sum_{i=1}^t \mathbb{1}[y_i^t = y_i]$, using $t$ as both the annotation step index and the summation bound. The text correctly describes CRI as "the proportion of correctly predicted labels" over the test set $\mathcal{D}_{\text{test}}$, which contains $l$ test cases (line 113). The summation should be over $i=1,\dots,l$ divided by $l$, not $t$. This is a formal definition error in the paper's central metric.

- **Sample sizes for the main FSE evaluation are not stated.** The preliminary experiment specifies 100 images per dataset (line 183), but the main experiments (Figure 3, Tables 2–4) do not report how many images or test cases were used. For datasets with many classes (CIFAR-100 has 100, CUB has 200), undersampling could affect results, and readers cannot assess the reliability of the key numerical claims.

- **The paper does not report whether Tables 2–4 use the same three-run multi-seed protocol as Figure 3.** Figure 3 mentions three runs with negligible standard deviations (line 211), but Tables 2–4 provide no error estimates or clarification of the experimental protocol used for those numerical results.

- **No ablation study justifies the choice of five annotation stages.** The paper notes prior work uses 1–3 stages and extends to five (lines 117–125), but does not demonstrate that all five stages contribute meaningfully, nor whether a different number of stages would alter the conclusions about annotation sufficiency.

- **The Ethics and Limitations section does not discuss a key limitation: the FSE framework evaluates annotation sufficiency only through the model's own self-consistency.** Definition 3.1 states a sufficient annotation should enable "accurate inference of the corresponding class," but the operationalization measures whether the *same model that generated the concepts* can use them to predict the class. This conflates concept quality with the model's text-to-class mapping ability—a necessary but not sufficient condition for annotation sufficiency.

### Trivial
None.

## Nice-to-Haves

- Clarify the relationship between the preliminary contradiction test (candidate set $\{y_i^{init}, d_i^j\}$) and the main FSE evaluation (candidate set $\{y_i, d_i^j\}$). The paper does not discuss this difference or its implications.
- Adding a control experiment (e.g., feeding human-written gold-standard concepts in slow mode) would help distinguish whether the bottleneck is concept generation quality or text-to-class mapping ability, pinning down which stage of the pipeline fails.

## Removed Points

These points are flagged to be removed; treat them with caution:

1. **Criticism about the contradiction test conflating different types of contradictions (type a vs. type b):** This criticism is partially factually incorrect for the specific setup used. In the contradiction test, the candidate set is $\{y_i^{init}, d_i^j\}$ where distractors exclude the ground-truth class. If the initial prediction is wrong, the ground-truth class is not in the candidate set, so the scenario where "concept prediction is correct" (type b) is impossible by design. The contradiction test is used solely to select a distractor strategy, not to diagnose annotation quality.

2. **Criticism about the code/data link being a placeholder ("here"):** This is a parser artifact. The original submission likely contains a hyperlink stripped during PDF-to-text extraction.

3. **Criticism about FineGrained-Avg not being defined:** The paper explicitly states in Table 3's caption that "FineGrained-Avg denotes the average CRI score computed across the three fine-grained datasets presented in Figure 3."

## Novel Insights

The reviewer insightfully observes that the paper's fast-vs-slow comparison is better understood as measuring an "articulation gap" (what the model knows implicitly vs. what it can express through text) rather than through the lens of dual-process theory. This reframing is more precise and aligns better with what the data actually show. The reviewer also correctly identifies that a control experiment (feeding human-written gold-standard concepts in slow mode) would help pin down whether the bottleneck is concept generation or text-to-class mapping—a useful direction for future work that clarifies the scope of the paper's claims.

## Suggestions

1. **Reframe the fast-vs-slow comparison** as an "articulation gap" measuring whether the model's explicit concept knowledge is self-contained enough for class inference, rather than invoking dual-process theory and "Slow Mode Superiority."

2. **Correct the notational error in Equation (2):** change the summation bound from $t$ to $l$ (the number of test cases) and the divisor from $t$ to $l$.

3. **Report sample sizes** for all main experiments and clarify the experimental protocol (single run vs. multi-run) for each table, including error estimates for numerical claims in Tables 2–4.

4. **Add explicit discussion** of the self-consistency limitation: the FSE framework tests concept sufficiency for the model's *own* inference, which is necessary but not sufficient for external annotation quality.

---

## Score and Decision

### Calibration Anchors

| Path | Avg Score | Round | Itemized | Comparison |
|------|-----------|-------|----------|------------|
| `/home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/kTjEPEy96Q.md` | 3.00 | R1 | Yes | Topically similar (evaluation framework for CBMs). Key weaknesses were limited technical contribution and lacking practical impact—both worse than our paper. |
| `/home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/KLUDshUx2V.md` | 3.40 | R1 | Yes | Topically similar (LLM concept bank generation/evaluation). Key weaknesses were limited novelty and insufficient experiments—our paper has more rigorous experiments and a more novel framework. |
| `/home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/RC5FPYVQaH.md` | 5.75 | R1, R2 | Yes | Different focus (proposing a new CBM architecture). Accepted despite weaknesses about model diversity and concept evaluation. |
| `/home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/tZk3LnvVtK.md` | 5.60 | R1, R2 | No | Different focus (LLM uncertainty with concepts). Rejected. |
| `/home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/9bmTbVaA2A.md` | 5.75 | R2 | Yes | Related (using LLMs/VLMs for interpretable classification). Accepted. |
| `/home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/ARFRZh6pzI.md` | 6.00 | R2 | Yes | Uses metacognitive/dual-process framing. Rejected despite mixed scores (5,6,8,5). |
| `/home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/rp0EdI8X4e.md` | 6.25 | R2 | Yes | Related (faithful vision-language CBMs). Accepted with clear formulation and extensive experiments. |

### Score Determination

The topically most similar anchors (kTjEPEy96Q at 3.00, KLUDshUx2V at 3.40) were both Rejected with severe weaknesses (favorability as low as -2.90 for limited contribution, insufficient experiments). Our paper avoids those pitfalls: it has a clearly motivated framework, concrete empirical findings (the ~25% articulation gap, the utility-as-proxy debunking), and a comprehensive multi-model evaluation. Our draft's weaknesses have favorability ratings of -0.86 to 1.29 (mostly positive/neutral), compared to -2.90 to -2.82 for those rejected anchors' most severe items. Comparatively, accepted anchors at 5.75–6.25 have weaknesses with similarly mild favorability ranges.

The paper sits in the 5.5–7.5 bracket. The primary framing weakness (the "Slow Mode Superiority" dual-process claim) is notable but does not invalidate the core contributions—the FSE framework, CRI metric, and empirical findings stand independently. The other weaknesses (CRI notation, missing sample sizes, no ablation) are all addressable in revision. **Final score: 6.5.**

MY FINAL SCORE: <score>6.5</score>
MY FINAL DECISION: <decision>Accept</decision>