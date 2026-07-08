I now have a clear picture. Let me compile the final review.

**Round 1 bracket (from calibration_search results):** The most topically similar anchors are:
- kTjEPEy96Q (3.00, REJECT) — evaluation framework for unsupervised CBMs with a more severe conceptual fallacy
- KLUDshUx2V (3.40, REJECT) — LLM concept bank generation with limited novelty
- 0qrTH5AZVt (4.67, REJECT) — concept-based explanations with concept quality validation issues
- todLTYB1I7 (5.00, REJECT) — evaluation framework for neuron explanations with claim-evidence mismatch
- tZk3LnvVtK (5.60, REJECT) — LLM uncertainty with concepts (different topic)
- RC5FPYVQaH (5.75, ACCEPT) — CB-LLM method paper (different category)
- ncCuiD3KJQ (6.75, ACCEPT) — Fast/slow thinking method paper (different category)

**Initial bracket:** 4.0–5.5

**Narrowing:** Our paper is meaningfully stronger than the 3.0–3.4 papers (avoids their fatal flaws, broader experiments, more novel framework) but shares with them the core challenges of evaluation-framework papers at ICLR. Weighted-item comparison with todLTYB1I7 (5.00) shows our strengths are more strongly weighted (10.77, 9.22, 8.19 vs their 8.56, 8.54, 8.02) but our major weaknesses (0.98, -1.24) are less severe than that paper's mismatch issue (3.19). The confound weakness weight (0.98, near-neutral) suggests it is seen as addressable rather than fatal.

**Final bracket:** 4.5–5.5, placing at 5.0.

Here is the final review:

---

## Summary

This paper proposes the Fast and Slow Effect (FSE) framework and the Class Representation Index (CRI) metric for automatically evaluating whether LLM/VLM-generated concept annotations provide sufficient semantic coverage for reliable concept-based XAI. Across 6 models, 2 annotation paradigms, and 5 datasets, the paper finds a systematic gap: LLMs classify accurately from visual input (fast mode, ~90% CRI) but perform substantially worse when forced to use their own textual concept annotations (slow mode, ~50–60% CRI on fine-grained datasets). The contrast is especially stark because the slow mode faces an easier 5-way classification task while the fast mode handles a 200-way task. The paper also demonstrates that high multimodal fusion accuracy does not imply good concept annotations, undermining the utility-as-proxy assumption.

## Strengths

- **Timely and well-motivated problem.** Whether LLM-generated concept annotations are sufficient for reliable XAI is a question that directly impacts the practical deployment of concept-based models. The motivating example in Figure 1—where the model correctly identifies a Red-faced Cormorant visually but misclassifies it when forced to use its own textual concepts—is genuinely compelling. (Section 1, Figure 1)

- **Broad and systematic experimental design.** The evaluation spans 6 models (GPT-4o, GPT-4o-mini, Llama-3.2-vision-90b/11b, QwenVL2-72b/7b), 2 annotation paradigms (post-hoc and visual-grounded), and 5 datasets covering both fine-grained (CUB-200, Cars-196, Flowers-102) and general domains (CIFAR-100, Caltech-101). This breadth makes the empirical patterns more convincing than a narrower study. (Sections 5.1–5.2, Figure 3)

- **Informative boundary condition.** The finding that CRI exceeds 90% on general datasets but drops below 60% on fine-grained datasets (Table 3) provides a useful delineation: LLM-generated concept annotations may suffice for coarse-grained tasks but fail for fine-grained discrimination. This helps practitioners calibrate expectations. (Table 3)

- **Utility-as-proxy critique.** The demonstration that fused (visual + concept) mode achieves ~90% CRI while slow mode alone scores only ~50% (Table 4) provides concrete evidence that high downstream task accuracy does not imply adequate concept annotations—validating the paper's motivation for a more direct evaluation framework. (Table 4)

## Weaknesses

### Major

- **Confound between concept quality and text-based reasoning ability.** The paper's central interpretive claim—that "current annotation methods fail to provide sufficient semantic coverage" (abstract)—rests on low CRI scores. But CRI measures classification accuracy from textual concepts, which conflates two factors: (a) whether the generated concepts are genuinely discriminative, and (b) whether the LLM is capable of reasoning from any set of textual concepts. The paper provides no control to separate these. The missing experiment is a human-written gold-standard concept set: if CRI were to remain low with expert human concepts, the problem would be text-based reasoning rather than annotation insufficiency. This confound is not acknowledged in the limitations section (Section 8). The paper's robust finding is that there is a systematic **gap** between visual and concept-based reasoning; attributing this gap specifically to annotation insufficiency goes beyond what the evidence supports without further controls.

- **CRI is not validated against any external standard.** CRI is presented as a measure of "annotation sufficiency" (Definition 3.1, Equation 2) but receives zero validation against any independent signal of annotation quality. There is no human evaluation comparing CRI scores against expert judgments, no comparison with ground-truth concept sets from existing CBM datasets as a positive control, and no content-based analysis linking CRI to concept specificity or discriminativeness. The paper critiques human evaluation as costly (Section 3), but a proposed metric requires some form of validation to establish what it actually measures.

### Minor

- **Abstract language imprecision.** The abstract states "the CRI dropping by over 25% on average in slow mode" without clarifying whether this means 25 percentage points or 25% relative. Table 2 shows absolute percentage-point drops of −25 to −27 (e.g., from ~88% to ~57%), so "25 percentage points" is the intended reading. The wording could mislead casual readers.

- **Distractor selection label imprecision.** The paper labels distractors as "semantically related" but selects them using ResNet-18 prediction confusions (Section 5.3, line 197), which capture visual similarity rather than conceptual/semantic relatedness. Two bird species that are visually confusable may not share conceptual features relevant to textual annotation. This does not invalidate the results but the terminology is imprecise.

- **Scale of main experiments unspecified.** The preliminary experiment (Table 1) states it uses 100 samples per dataset. The main experiments (Figure 3, Tables 2–4) do not specify how many images or classes were evaluated. While the text mentions covering "all K classes" for post-hoc and "all N samples" for visual-grounded (line 117), the actual numbers are absent, making it difficult to assess reliability and statistical power.

### Trivial

- **CRI formula notation error.** Equation (2) writes `(1/t) Σ_{i=1}^t` where the summation should run over test instances l (as defined in `𝒟_test`) rather than annotation steps t. This appears to be a notation error or parser artifact that should be corrected.

- **Inconsistent dataset naming in tables.** Tables 1 and 4 use abbreviated names (e.g., "Car", "Flower", "CUB-Bird") while the standard names are Cars-196, Flowers-102, CUB-200.

## Nice-to-Haves

- **Content analysis of generated concepts.** The paper treats concept sets as a black box, measuring only whether they suffice for classification. An analysis of what kinds of concepts are generated at each stage (e.g., are they overly generic? do they miss key discriminative features?) would substantially strengthen diagnostic value.
- **Alternative prompting strategies.** The paper uses a single 5-stage hierarchical prompt. Testing one or two alternatives (e.g., asking for the top-5 most distinctive features in one shot) would address whether results are prompt-dependent or reflect a more inherent limitation.
- **Statistical significance testing.** The paper reports three runs and states standard deviations are "negligible" (line 211), but no formal significance tests are performed for the key CRI-gap results.

## Removed Points

These points from the input review were removed as not genuine weaknesses, speculative, or grounded in misunderstandings:

- **"Fast-mode superiority framing is backward"** (Critic Weakness 3): The observation that slow mode is 5-way while fast mode is 200-way makes the paper's results *more* striking, not less. This is a valid observation about framing emphasis, not a weakness. Removed on Hard Rule grounds (the criticism is not a genuine weakness).
- **"Utility-as-proxy experiment does not test what it claims"** (Critic Weakness 4): The critic argues the experiment is circular. However, the paper correctly demonstrates that high fused accuracy (≈90%) combined with low concept-only accuracy (≈50%) shows that downstream utility is a poor proxy for annotation quality. The experiment validly tests what it claims. Removed as a misunderstanding of the paper's argument.
- **"Ethics section is generic"**: All ethics sections are necessarily broad; this is not a specific weakness.
- **"Definition 3.1 makes CRI tautological"**: The paper defines sufficiency as "concepts alone enable accurate inference" and operationalizes it via classification accuracy from concepts alone. This is a reasonable operationalization, not a tautology.
- **"Missing related works"**: Cannot be verified without external sources per Hard Rules.
- **"No positive control for CRI"**: Already subsumed by the CRI-validation weakness above.

## Novel Insights

Beyond the paper's own contributions, the review analysis highlights that the paper's strongest finding is not "annotations are insufficient" as a blanket claim, but rather that there is a **systematic and large gap** between LLMs' visual classification ability and their ability to produce and reason from textual concept descriptions. This gap is especially notable because the slow mode operates on an easier 5-way classification while the fast mode operates on a 200-way classification—making the gap even more severe than the paper's framing suggests. Reframing the contribution around this specific diagnostic finding (rather than a categorical claim about annotation quality) would make the paper both more precise and more actionable for the community.

## Suggestions

1. **Add a human-concept control.** Source or generate gold-standard concept annotations (e.g., from existing CBM datasets or domain experts) and measure CRI when the LLM reasons from these. This would disentangle whether the fast-slow gap is driven by annotation quality or text-based reasoning ability.
2. **Validate CRI against at least one external signal.** Even a small-scale human study where experts rate concept quality, compared against CRI scores, would significantly strengthen confidence in the metric.
3. **Specify the evaluation scale.** Clarify the number of images/classes used in the main experiments and include variance estimates for the key CRI-gap results.
4. **Reframe the central contribution.** Acknowledge the confound explicitly and characterize the paper's contribution as diagnosing the fast-slow gap and demonstrating the failure of the utility-as-proxy assumption, rather than a categorical claim that annotations are insufficient.

## Score and Decision

**Score: 5.0**
**Decision: Borderline**

**Calibration Report:**

All anchors retrieved across rounds:

| Path | Avg Score | Round | Itemized? | Comparison |
|------|-----------|-------|-----------|------------|
| kTjEPEy96Q | 3.00 | Brkt | Yes | Evaluation framework for unsupervised CBMs with a conceptual fallacy (metrics didn't measure what they claimed). Our paper avoids this but has a different interpretive confound. |
| KLUDshUx2V | 3.40 | Brkt | Yes | LLM concept bank generation with limited novelty over prior work. Our paper's FSE framework is more novel and experiments are broader. |
| 0qrTH5AZVt | 4.67 | Brkt | Yes | Concept-based local explanations with validation issues. Comparable to our paper in concept-quality concerns. |
| todLTYB1I7 | 5.00 | Brkt/Narrow | Yes | Evaluation framework for neuron explanations with claim-evidence mismatch. Our strengths are more strongly weighted (10.77 vs 8.56, 9.22 vs 8.54) but share similar evaluative concerns. |
| tZk3LnvVtK | 5.60 | Narrow | No | LLM uncertainty with concepts — different topic, not directly comparable. |
| RC5FPYVQaH | 5.75 | Brkt | Yes | CB-LLM method paper — different category (method vs. evaluation framework). |
| ncCuiD3KJQ | 6.75 | Brkt | Yes | Fast/slow thinking method paper — different category (method with strong results vs. evaluation framework). |

**Reasoning:** Weighted-item comparison shows this paper's strengths are strongly positive (10.77, 9.22, 8.19, 6.29) and its major weaknesses carry near-neutral to mildly negative weight (0.98, -1.24). The paper is meaningfully stronger than kTjEPEy96Q (3.00) and KLUDshUx2V (3.40), which had either fatal conceptual issues or insufficient novelty. It is on par with todLTYB1I7 (5.00) and ConLUX (4.67) in terms of overall contribution-vs-limitation balance. The confound issue is the primary factor preventing a higher score—while addressable, the paper's central interpretive claim goes beyond what the evidence strictly supports without a human-concept control. The paper contributes a genuinely useful evaluation framework and informative empirical findings, but the over-interpretation of those findings and the lack of CRI validation place it at the borderline.

MY FINAL SCORE: <score>5.0</score>
MY FINAL DECISION: <decision>Borderline</decision>