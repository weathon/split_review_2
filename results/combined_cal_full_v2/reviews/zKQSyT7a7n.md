Now I have all the calibration data. Let me produce the final review.

## Summary

This paper introduces VT-WM, a multi-task visuo-tactile world model that combines exocentric vision (Cosmos encoder) with fingertip tactile sensing (Sparsh-X on Digit 360 sensors) through a 12-layer transformer predictor with factorized spatio-temporal attention and action cross-attention. The core idea — that tactile sensing can ground world model rollouts in contact physics, preventing object disappearance, teleportation, and physically implausible motion that plague vision-only models — is well-motivated and important. The paper evaluates across three axes: imagination quality (object permanence, causal compliance with paired t-tests), zero-shot CEM planning on a real robot across five tasks, and data efficiency via fine-tuning on 20 demonstrations of a plate-insertion task.

## Strengths

- **Well-motivated problem with clear articulation.** Sections 1 and 3.1 make a compelling case for why vision-only world models fail at contact reasoning (occlusion, visual aliasing, invisible forces) and why tactile sensing is a natural complement. This framing is specific, grounded, and correctly identifies a genuine limitation in the field.

- **Real-robot validation across multiple tasks.** The paper goes beyond simulated rollouts, demonstrating zero-shot CEM planning transfer to a real Franka/Allegro platform across five tasks (reaching, pushing, wiping, stacking, button-pressing) plus a held-out plate-insertion task (Section 4.2–4.3). This is substantially more convincing than simulation-only evaluations.

- **Statistically-grounded imagination metrics.** The object permanence and causal compliance evaluations (Section 4.1) use paired t-tests with reported p-values, achieving significance on 3/5 tasks for each metric. This goes beyond reporting point estimates and gives the reader a meaningful signal about reliability.

- **Sound architectural design.** Using frozen pretrained encoders (Cosmos for vision, Sparsh-X for tactile) with a trainable transformer predictor is pragmatic and follows current best practices. The factorized spatio-temporal attention and action-conditioning via cross-attention (Section 3.2.1) are sensible choices clearly described.

## Weaknesses

### Major

- **The V-WM baseline is underspecified, making the central comparison difficult to interpret.** The paper's core claim — that adding touch improves world models — rests entirely on the VT-WM vs. V-WM comparison. Yet it is never stated whether V-WM uses the same 12-layer transformer architecture with tactile inputs removed (which would control for capacity), a different architecture, or a published baseline. The paper mentions V-JEPA-2AC (Assran et al., 2025) only as a reference point ("consistent with prior visual world models… such as V-JEPA-2AC"), not as the definition of V-WM. This is not a detail relegated to an appendix; it is a fundamental experimental design choice that must be explained in the main text. Without knowing whether the architectures are matched, the improvement attributed to tactile sensing could partially reflect differences in model capacity or architecture.

- **The data efficiency experiment (Section 4.3) does not isolate the role of tactile sensing from multi-task pre-training.** VT-WM is pre-trained on a multi-task dataset, then fine-tuned on 20 demos of a new task, and compared against a BC policy (ACT) trained from scratch on the same 20 demos. The 3.5× improvement is attributed to VT-WM in the abstract and conclusion, but this conflates two factors: multi-task pre-training and tactile sensing. A V-WM baseline, pre-trained on the same multi-task data and fine-tuned on 20 demos, is the necessary control. Without it, the result could be driven entirely by multi-task pre-training having nothing to do with touch. The paper's framing of this as a VT-WM data-efficiency result is not supported by the evidence presented.

- **The zero-shot planning results (Section 4.2) are based on n=5 trials per task without confidence intervals.** With n=5, a single trial flip changes the reported percentage by 20 points. The headline claim of "up to 35% higher success" (69% → 93% on Reach&Push) corresponds to roughly 1.2 trials of difference. No confidence intervals, standard errors, or statistical tests are reported for any planning result. While n=5 is not uncommon in robotics, the paper uses these numbers to make strong comparative claims without quantifying uncertainty, and the observed differences are within the range that could arise by chance under a null hypothesis.

### Minor

- **The Fréchet distance metric for object permanence (Section 4.1) may conflate visual generation quality with physical reasoning accuracy.** CoTracker extracts keypoint trajectories from *generated* images. If V-WM produces lower-quality or blurrier images than VT-WM (which is plausible since VT-WM has more information to constrain generation), CoTracker may track less reliably on V-WM's outputs, inflating its Fréchet distance even if the underlying physics is comparable. The paper does not address this confound or report separate tracking success rates per model's outputs.

- **No ablation experiments are included.** The paper does not ablate: the temporal window of tactile inputs (why 2 frames? why 9 visual frames?), the fusion method (concatenation vs. cross-attention vs. alternatives), the number of tactile sensors, or whether tactile information is needed at every timestep. Without ablations, it is unclear which design choices drive the observed improvements, limiting the paper's scientific contribution beyond demonstrating that "touch helps overall."

- **Open-loop execution is used for planning without acknowledging its limitations.** The best CEM action sequence is executed on the real robot without replanning (Section 3.2.3). For contact-rich tasks where the robot needs to adjust to unexpected interactions (e.g., a cube that shifts during grasping), this is a significant limitation that is not discussed.

### Trivial

None.

## Nice-to-Haves

- Report CoTracker tracking success rates separately for each model's outputs to address the metric confound.
- Specify CEM planning hyperparameters (population size, horizon, iterations, elite fraction) in the main text.
- Add V-WM as a control in the data efficiency experiment to isolate touch's contribution from multi-task pre-training.
- Include a discussion of the asymmetric temporal sampling choice (6 fps vision vs. higher-frequency tactile) as an ablation.

## Removed Points

These points are flagged to be removed, treat them with caution:

- **Simplified action space (Issue 5 from harsh critic):** The action space of ℝ⁷ (3D translation, 3D orientation, binary hand open/close) is standard for CEM-based manipulation planning. Binary hand control with open/close presets is common practice for the Allegro Hand in planning contexts. The paper's goal is demonstrating that touch improves world models, not demonstrating full dexterous manipulation — this criticism is scope creep.
- **Asymmetric temporal sampling unjustified:** The harsh critic claimed no justification was given, but the paper explicitly states (line 103–104): "This shorter horizon reflects the higher temporal frequency and local nature of contact information." The justification is present.
- **Missing architectural details (hidden dimensions, heads):** The paper states these are in Appendix A, which was stripped by the parser. Per the review guidelines, missing appendix content is not a valid criticism.
- **Missing CEM parameters:** Likely detailed in Appendix C (stripped by parser). Not a valid criticism per guidelines.
- **Cherry-picked qualitative examples:** Standard practice for papers showing visualizations; not a specific methodological flaw without evidence of systematic cherry-picking.
- **Generic strengths from the input:** The strength "Sensible architectural choices" was rephrased to be more specific and grounded. The removed generic framing ("well-motivated problem" as a strength) was instead made concrete by referencing specific sections.
- **Delusional/superficial strengths from input:** Not present in this case.

## Novel Insights

None beyond the paper's own contributions. The merged review confirms the paper's core thesis — tactile sensing improves world model fidelity for contact-rich manipulation — while identifying specific evidential gaps in the experimental validation. The most noteworthy observation from the review process is that the paper's strongest evidence (statistically significant gains in imagination metrics) supports a different claim (touch improves rollout quality) from the one with the weakest evidence (zero-shot planning with n=5, data efficiency without V-WM control), creating an asymmetric evidence structure that the paper's narrative does not fully acknowledge.

## Suggestions

1. **Specify V-WM's architecture explicitly.** State whether it uses the same transformer with tactile inputs removed (controlling for parameter count) or a different architecture, and discuss any architectural differences.
2. **Add a V-WM condition to the data efficiency experiment** (Section 4.3) to isolate the contribution of tactile sensing from multi-task pre-training.
3. **Increase planning trials to at least n=20 per task** and report confidence intervals or bootstrap-based uncertainty estimates. At minimum, acknowledge the small-n limitation when making comparative claims.
4. **Add ablation experiments** for key design choices: tactile temporal window, fusion method, and sensor count. This would substantially strengthen the paper's scientific contribution.
5. **Report CoTracker tracking success rates** separately for V-WM and VT-WM outputs to address the metric confound.
6. **Acknowledge the open-loop limitation** and discuss whether closed-loop replanning would likely amplify or reduce the observed VT-WM advantage.

## Score and Decision

**Round 1 bracket: (4.5, 6.0)** — below DINO-WM (5.75) due to baseline underspecification and missing V-WM control in the data efficiency experiment, but above Mani-WM (4.67) due to more extensive real-robot validation and statistical grounding of the imagination metrics.

**Round 2 narrowing:** Compared against all 8 itemized anchors. VT-WM's strengths (real-robot validation, statistical tests) give it higher weight positives than The Power of the Senses (4.33, sim-only) and Mani-WM (4.67, thin real-robot eval). However, the V-WM baseline gap and missing data-efficiency control are more serious methodological omissions than the weaknesses of DINO-WM (5.75, simulation-only but clean experiments) or RCWM (5.50, simulation-only). The weighted-item comparison confirms that VT-WM's strongest positives (real-robot results: 8.95, statistical grounding: 8.15) are shared with strong anchors, but its most negatively-weighted items (V-WM baseline: 1.53, data efficiency confound: 1.67) are structural experimental gaps that the higher-scoring anchors do not have.

**Final score:** 5.0

**All calibration anchors:**

| Path | Avg Score | Round | Itemized | Comparison |
|------|-----------|-------|----------|------------|
| gwZ90hFSL2 | 1.00 | R1 | No | Irrelevant (cross-lingual NLP) |
| u1cQYxRI1H | 0.50 | R1 | No | Irrelevant (illumination) |
| Uj0h13lVrR | 1.00 | R1 | No | Irrelevant (GFlowNets) |
| 5kMwiMnUip | 1.40 | R1 | No | Irrelevant (jailbreaking) |
| xcHIiZr3DT | 2.50 | R1 | No | Pseudo-tactile grasping; weaker than VT-WM |
| wl1Kup6oES | 3.00 | R1 | No | Visual pre-training; no tactile |
| B7cZvTQsUN | 3.00 | R1 | No | Structured world models; sim-only |
| I0To0G5J7g | 3.20 | R1 | No | Embodied foundation models; different method |
| J4D5WVoc5g | 4.50 | R1 | No | ViTaM-D (visuo-tactile reconstruction); similar domain but different task |
| **FMsmo01TaI** | **4.33** | **R1** | **Yes** | **The Power of the Senses (visuo-tactile RL, sim-only); VT-WM stronger due to real-robot** |
| **mnwlhvmKMN** | **4.25** | **R1** | **Yes** | **4D Embodied World Models; VT-WM has stronger real-robot validation** |
| KTtEICH4TO | 4.75 | R1 | No | CORN; contact-based representation, different approach |
| eJHnSg783t | 6.50 | R1 | No | DIFFTACTILE; tactile simulation infrastructure |
| UmhC7fuhzs | 6.50 | R1 | No | Multisensory simulation; different focus |
| KsUh8MMFKQ | 8.00 | R1 | No | Thin-shell manipulation; stronger overall |
| 7BLXhmWvwF | 8.00 | R1 | No | Geometry-aware RL; stronger overall |
| pISLZG7ktL | 8.00 | R1 | No | Data scaling laws; different contribution type |
| OI3RoHoWAN | 8.00 | R1 | No | GenSim; different contribution type |
| c0chJTSbci | 6.25 | R2 | No | Zero-shot manipulation with diffusion; VT-WM weaker on experimental rigor |
| **GARbxyCV13** | **5.75** | **R2** | **Yes** | **DINO-WM (world models for planning); cleaner experiments, sim-only; VT-WM has real-robot but weaker baselines** |
| **aVyJwS1fqQ** | **4.67** | **R2** | **Yes** | **Mani-WM (real-robot world model); thinner real-robot eval than VT-WM** |
| NxoFmGgWC9 | 5.50 | R2 | No | Video pre-training for manipulation; different method |
| **DJw1JBTmuk** | **5.50** | **R3** | **Yes** | **RCWM (world model pre-training); sim-only, attribution issues; VT-WM has real-robot but baseline gap** |
| **jf7C7EGw21** | **5.50** | **R3** | **Yes** | **VTDexManip (visuo-tactile dataset+benchmark); stronger evaluation but dataset contribution type** |

MY FINAL SCORE: <score>5.0</score>
MY FINAL DECISION: <decision>Reject</decision>