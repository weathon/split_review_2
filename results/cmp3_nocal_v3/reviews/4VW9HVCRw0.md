Here is the final consolidated review.

---

## Summary

This paper introduces the task of free-form HOI generation (beyond grasp-centric interactions like pushing, poking, tipping), constructs a new 3D dataset called WildO2 (4.4k samples, 92 intents, 610 object categories) from in-the-wild video via an O2HOI frame-pairing pipeline, and proposes a three-stage method called TOUCH (contact map prediction CVAE → multi-level conditioned diffusion → physical constraints refinement). The core technical contributions—a pragmatic dataset construction strategy and a well-designed multi-level conditioning architecture—are meaningful and address a genuine gap in the literature.

## Strengths

1. **Well-motivated and concretely scoped task.** The paper convincingly argues that existing HOI generation is confined to grasping patterns, even when language control is used. The examples of non-grasping interactions (pushing, poking, tipping, rotating) make the gap concrete and the contribution clear (Section 1).

2. **The O2HOI frame-pairing strategy for dataset construction is clever and practical.** By pairing an object-only frame with an interaction frame from the same video and transferring masks via dense matching, the pipeline avoids the geometric inconsistencies of diffusion-based inpainting and the cost of manual completion. This is a scalable solution to the occlusion problem that has blocked in-the-wild 3D HOI dataset construction (Section 3.1, Fig. 2).

3. **WildO2 fills a genuine data gap.** At 4.4k samples across 92 intents and 610 object categories, it is larger and more diverse than lab-based datasets (GRAB, OakInk, HOI4D). The multi-level annotation system (SSCs, DSCs, 17-part hand segmentation, contact maps) is comprehensive (Section 3.3).

4. **The multi-level conditioning design is well-reasoned and ablated.** Separating coarse-grained (SSC + global geometry) and fine-grained (DSC + local contact) conditions into early vs. late transformer blocks is a clean architectural choice. The ablation in Table 2 confirms both levels contribute, and the within-method ablations (removing contact prediction, removing multi-level structure) isolate the value of each component convincingly.

5. **The cycle-consistency loss for contact refinement is conceptually elegant.** Enforcing bidirectional mapping consistency between hand and object contact surfaces via L_cycle is a self-supervised way to regularize contact without requiring additional annotations (Section 4.3).

## Weaknesses

### Fatal

None.

### Major

1. **The baseline comparison is weakened by underspecified adaptation of prior methods.** The paper compares against ContactGen (CVAE for grasp generation) and Text2HOI (temporal diffusion model stripped of its temporal axis), both adapted for the new task. The paper says both are augmented with "an optimization-based post-processing module to correct hand poses" (Section 5.2), but this module is never specified—what it optimizes, how it is tuned, or whether the optimization budget is comparable across methods. It is also unclear whether the baselines were fine-tuned on WildO2 training data or simply run as-is from pre-trained weights with the post-processing module tacked on. Since the method is purpose-built and the baselines are not, the headline superiority claim is less informative than it should be. (*The within-family ablations in Tab. 2 do partially address the critic's call for simpler comparisons; the core concern is the lack of transparency about baseline adaptation.*)

2. **The contact accuracy metrics (P-IoU, P-F1) evaluate against algorithmically derived "ground truth" contact maps, not human-annotated or physically validated contact.** The paper states (Section 3.3) that contact maps are computed via "relative and absolute distance thresholds with bidirectional nearest-neighbor filtering." The evaluation therefore measures agreement with a heuristic, not necessarily genuine physical contact. Since the model's contact prediction CVAE is trained on these same heuristic-derived maps, there is a risk that high metric scores reflect fidelity to the heuristic rather than true contact quality. The qualitative visualizations (Figs. 5, 7, 8) provide some independent reassurance, but the quantitative contact accuracy results would be strengthened by validation against human-annotated contact on a held-out subset.

### Minor

3. **Failure-case bias in the dataset pipeline is unanalyzed.** The reconstruction pipeline succeeds on only 55% of clips, with 31% attributed to "Pore Estimation Failure" (Fig. 3a). The paper does not analyze whether the 45% failure rate introduces systematic biases—e.g., does the pipeline preferentially succeed on interactions with larger objects, simpler backgrounds, or more frontal camera views? Since WildO2's claims of diversity rest on its in-the-wild origin, understanding what the pipeline systematically discards is important for assessing dataset representativeness.

4. **Key metrics lack confidence intervals or statistical significance tests.** With a test set of 677 samples, the standard errors on P-IoU, P-F1, and MPVPE are non-negligible. In Table 2, the differences between text encoders (Qwen-7B: 0.728 vs. CLIP: 0.713 vs. BERT: 0.705) are small—about 0.01–0.02. Without confidence intervals or statistical tests, the claim that Qwen-7B "offers better performance in capturing fine-grained semantic details" is not well supported. Similarly, the force-expression claim ("22–25% larger average contact area for firm/tight interactions," Section 5.4.3) is stated without variance or a significance test.

5. **Some implementation details are underspecified.** (a) The text-to-hand-part-mask mechanism in Section 4.1 ("hand-part mask initialized from the fine-grained text") is not explained—is this rule-based parsing or learned? (b) The manual inspection step (Section 3.2, "final stage of manual inspection and refinement") is mentioned only in passing without details on what it involves, how many samples were rejected or modified, or how many person-hours it required. (c) The number of test-time adaptation iterations ($N_{tta}$) in Section 4.3 is not reported.

6. **The Text2HOI baseline's P-FID score (15.72) is anomalously high** compared to ContactGen (6.08) and TOUCH (4.13), suggesting either a severe task mismatch or an implementation/adaptation issue. The paper should explain this discrepancy (Section 5.2, Table 1).

### Trivial

7. The claim in the introduction that even methods using "detailed natural language (via LLMs)" are still fundamentally grasp-centric (Section 1) is asserted without specific counterexample citations beyond Zhang et al. 2025a,b. Naming specific methods would sharpen the argument.

8. The Something-Something V2 source bias (scripted, goal-directed actions by crowdworkers) is not discussed in the limitations section (Section 6).

## Nice-to-Haves

- An analysis of failure cases (e.g., interpenetration the refinement misses, implausible wrist orientations, incorrect contact regions) would help the community build on this work.
- A cross-dataset evaluation (e.g., TOUCH trained on WildO2 evaluated on GRAB or OakInk test samples) would strengthen the generalization claim beyond qualitative Objaverse examples.
- The direct x0 prediction choice in the DDPM (Section 4.2) is stated without justification; a brief rationale would be helpful given standard practice.

## Removed Points

These points are flagged to be removed; treat them with caution.

- **"The evaluation metrics disadvantage diversity"** — This criticism is partially addressed by the paper's inclusion of diversity metrics (Entropy, Cluster Size) and a distributional metric (P-FID). The paper does present these alongside pointwise metrics, and the tension between pointwise accuracy and diversity is a known challenge in generative modeling evaluation. While a more nuanced reconciliation would improve the paper, the criticism overstates the problem.
- **"The 4.4k sample dataset with 1000 epochs raises memorization concerns"** — This is speculative given that the paper demonstrates generalization to novel Objaverse objects (Fig. 7). There is no evidence provided that the model is memorizing.
- **"Missing analysis of failure cases" and "Missing cross-dataset evaluation" and "direct x0 prediction justification"** — These are suggestions for improvement, not indicators of a flaw. Moved to Nice-to-Haves.
- **Formatting/style nitpicks and parser artifact complaints** — These reflect PDF parsing issues, not author errors.

## Novel Insights

None beyond the paper's own contributions. The reviews did not surface any insight about the paper that the paper itself does not already articulate about its contributions or limitations.

## Suggestions

1. **Specify the baseline post-processing module in detail** and, ideally, fine-tune ContactGen and Text2HOI on WildO2 training data for a fairer comparison.
2. **Validate a subset of contact maps through human annotation** (50–100 samples) and report how well both the algorithmic ground-truth maps and TOUCH's predicted maps agree with human judgment.
3. **Report bootstrapped confidence intervals** (95%) on all key metrics in Tables 1 and 2 to enable readers to assess whether reported differences are meaningful.
4. **Analyze the systematic bias** from the 45% pipeline failure rate by comparing failure vs. success cases along dimensions like object size, hand pose complexity, background clutter, and camera viewpoint.
5. **Disambiguate the text-to-hand-part-mask conversion** (Section 4.1) and report $N_{tta}$.

## Score and Decision

This paper makes three solid contributions—a new task formulation, a practical dataset with a clever construction pipeline, and a well-designed method with clean ablations. None of the identified weaknesses are fatal. The most significant concern (weakness #1, baseline adaptation transparency) is methodological and fixable. The paper's evaluation is adequate but would benefit from confidence intervals and human validation of contact maps. The core contributions warrant acceptance.

**MY FINAL SCORE:** <score>7</score>
**MY FINAL DECISION:** <decision>Accept</decision>