## Summary

This paper proposes Visuo-Tactile World Models (VT-WM), a multi-task world model that integrates fingertip tactile sensing (Digit 360 sensors) with exocentric vision to improve physical fidelity in imagined rollouts for contact-rich manipulation. The model encodes visual and tactile inputs via Cosmos and Sparsh-X tokenizers, fuses them through a transformer predictor with factorized attention, and uses a cross-entropy method for planning. Experiments compare VT-WM against a vision-only counterpart (V-WM) on five manipulation tasks, reporting 33% and 29% average improvements in object permanence and causal compliance metrics respectively, along with real-robot planning gains and a data efficiency demonstration against behavioral cloning.

## Strengths

- **Well-motivated problem with a natural modality pairing.** The paper makes a clear and compelling case (Sec. 1, Sec. 3.1) that vision-only world models hallucinate under occlusion because they lack contact information, and that tactile sensing is a natural complementary modality. This motivation is specific, grounded in concrete failure modes (object disappearance, teleportation, physically implausible motion), and directly motivates the architecture.

- **Clean experimental design for the core comparison.** The main experiment (Sec. 4.1) conditions VT-WM and V-WM rollouts on *identical action sequences drawn from real successful demonstrations*, using ground-truth video as reference. This design isolates the effect of the additional tactile modality: both models receive the same actions and visual context, so differences in rollout quality are attributable (modulo architectural differences — see Weaknesses) to the tactile input.

- **Quantitative metrics with per-task statistical tests.** The paper uses normalized Fréchet distance via CoTracker keypoint trajectories for object permanence and causal compliance, and backs the offline comparisons with paired t-tests reporting exact p-values per task (Sec. 4.1). This level of statistical detail is above what many robotics papers provide.

- **Real-robot zero-shot transfer across five tasks.** The planning experiments (Sec. 4.2) test whether improved imagination actually translates to better real-world plans across tasks of varying difficulty, from simple reaching to multi-step contact-rich stacking. The directional trend is consistent: VT-WM matches V-WM on free-space reaching and outperforms it on all four contact-rich tasks.

- **Data efficiency demonstration.** The comparison against a task-specific BC policy (Sec. 4.3) on 20 demonstrations of a plate-insertion task shows VT-WM achieving ~3.5× higher success rate, demonstrating a practical advantage beyond improved imagination quality.

## Weaknesses

### Fatal

None.

### Major

- **No ablation studies.** The paper proposes a new architecture (vision encoder + tactile encoder + 12-layer transformer with factorized attention and action cross-attention, specific fusion via concatenation, specific loss weighting, specific sampling horizon \(H\)) but provides zero ablations to isolate which design choices drive the reported gains. In particular, there is no ablation of the tactile input itself — e.g., training VT-WM with random/noise tactile inputs, or with tactile inputs masked to zero — that would attribute improvements to informative touch rather than to having a larger model with more parameters and a larger input sequence. Without such controls, the reader cannot tell whether the improvements come from tactile information as such or from any of the other architectural differences between VT-WM and the V-WM baseline. This limits the scientific contribution to "some configuration of a visuo-tactile model outperforms some configuration of a vision-only model."

- **Real-robot planning results are underpowered.** The zero-shot planning experiments (Sec. 4.2) report binary success rates averaged over only **5 trials per task**. With N=5, a single trial swing changes the success rate by 20 percentage points. Several of the reported gains are within this noise floor (e.g., Push Fruits: 83% → 92% is ~0.5 trials; Stack Cubes: 75% → 83% is ~0.4 trials). No confidence intervals, standard errors, or significance tests are reported for these results. The data efficiency experiment (Sec. 4.3) uses 9 trials — better, but still modest. While the directional pattern across tasks is consistent, individual comparisons are too underpowered to support the reported percentages at face value.

- **The V-WM baseline is underspecified.** The paper never states whether V-WM uses the exact same architecture as VT-WM with the tactile stream removed, or whether it is a different architecture trained with different hyperparameters. If V-WM has strictly fewer parameters (no tactile encoder, no fusion mechanism, smaller transformer input), the comparison conflates "adding touch" with "adding model capacity." Reporting parameter counts and clarifying whether the architectures are matched would directly address this concern.

### Minor

- **Headline improvements (33%, 29%) average across non-significant and even negative-direction results.** For object permanence, 2 of 5 tasks are not statistically significant (*wipe with cloth*, *scribble with marker*); for causal compliance, 2 of 5 are not significant (*cube stacking* p=0.09, *scribble with marker* p=0.23 and directionally worse with t=-1.22). The paper is transparent about per-task p-values, but the headline framing of "33% average reduction" across all tasks (including the non-significant ones) overstates the reliability of the claimed improvement. The data is honest; the framing should match its granularity.

- **Data efficiency experiment conflates multi-task pre-training with tactile sensing.** The comparison (Sec. 4.3) pits VT-WM (multi-task pre-trained + fine-tuned on 20 demos) against a BC policy trained from scratch. This conflates two variables: multi-task pre-training and the specific visuo-tactile architecture. A V-WM with the same multi-task pre-training regime would be the proper control to isolate the benefit of tactile sensing for data efficiency.

- **No systematic failure analysis or limitations discussion.** The paper mentions one failure mode in passing (VT-WM "mostly places the plate beside the rack" for the data efficiency task, Sec. 4.3) but does not systematically characterize where VT-WM still fails in the contact perception or planning experiments. The conclusion (Sec. 5) includes no limitations section, which is a notable omission for a real-robotics paper presenting a new method.

### Trivial

None.

## Nice-to-Haves

- **Controlled ablation of the tactile signal.** The single highest-leverage addition would be training VT-WM with noise/zero tactile inputs (or a matched-parameter V-WM with the same total capacity) to confirm that gains come from task-relevant tactile information rather than added model capacity.
- **Larger-N planning experiments with binomial confidence intervals.** Increasing trials to ≥20 per condition and reporting CIs or Fisher's exact tests would substantially strengthen the real-robot claims.
- **Reporting tactile prediction accuracy.** Since VT-WM predicts both visual (\(s_{k+1}\)) and tactile (\(t_{k+1}\)) latents, evaluating the quality of tactile predictions would directly test whether the model actually learns contact dynamics rather than using tactile input as a latent regularizer.
- **Reporting computational cost.** Inference speed, CEM planning time, and parameter counts for both models would help assess practical deployability.

## Removed Points

- **CoTracker metric validity concern (confound speculation).** The critic hypothesized that CoTracker "may produce different quality tracks" on V-WM vs. VT-WM outputs for reasons unrelated to object permanence. This is speculative — no evidence is provided that CoTracker is systematically biased by output quality — and removed because it is an unsubstantiated concern about a standard evaluation tool, not a specific identified problem in the paper.
- **"First multi-task" claim concern.** Removed because the paper carefully qualifies this claim (Sec. 2 explicitly notes that prior visuo-tactile dynamics models are task-specific), and the "multi-task" qualifier is the operative distinction.
- **Action controllability deferred to appendix.** Removed per policy: the appendix is stripped by the parser and existed in the original submission.
- **Temporally misaligned modalities question (method section).** Removed because this is a minor implementation detail that does not affect the core claims; the paper explains the input rates (6 fps vision, 6 Hz tactile with two recent frames) which pragmatically addresses alignment at the frame level.
- **Missing parameter counts and compute comparison between V-WM and VT-WM.** Partially subsumed by the baseline specification weakness above; the specific demand for inference speed/CEM planning time is moved to Nice-to-Haves.

## Novel Insights

None beyond the paper's own contributions. The reviews identified evidential gaps (no ablations, underpowered real-robot results, underspecified baseline) but did not surface insights about the method or problem beyond what the paper itself presents.

## Suggestions

1. Add a controlled ablation that isolates tactile information from model capacity (e.g., train VT-WM with noise tactile inputs, or train a parameter-matched V-WM with a second visual stream). This is the single most important improvement to support the paper's core claim.
2. Increase real-robot planning trials to ≥20 per condition and report binomial confidence intervals or per-task significance tests.
3. Explicitly specify the V-WM architecture (same model minus tactile stream? same total parameter count?) and report parameter counts for both models.
4. Add a limitations section that systematically characterizes where VT-WM still fails.
5. Report accuracy of tactile predictions (\(t_{k+1}\)) to directly test whether the model learns contact dynamics.

## Score and Decision

<score>6</score>
<decision>Borderline Accept</decision>