## Summary
This paper introduces Visuo-Tactile World Models (VT-WM), the first multi-task world model that integrates fingertip tactile sensing with exocentric vision for robot manipulation. By complementing vision with touch, the model aims to ground imagination in contact physics, improving object permanence and causal compliance in autoregressive rollouts. The authors demonstrate that these improvements translate to better zero-shot planning on a real robot (up to 35% higher success on contact-rich tasks) and show data efficiency advantages over behavioral cloning with limited demonstrations.

## Strengths
- The paper identifies a genuine limitation of vision-only world models—hallucinated object interactions due to missing contact information—and provides a well-motivated solution by integrating tactile sensing.
- The architecture is clearly described and technically sound, using pretrained foundation encoders (Cosmos, Sparsh-X) with a transformer predictor employing factorized spatio-temporal attention and action cross-attention.
- The evaluation of imagination quality uses objective metrics (Fréchet distance on CoTracker trajectories) with statistical significance tests, providing quantitative evidence that tactile grounding improves object permanence and causal compliance.
- Real-robot validation across five manipulation tasks demonstrates the practical applicability of the approach, and the data efficiency experiment highlights the potential of pre-trained world models for fast adaptation.

## Weaknesses
### Fatal
None.

### Major
1. **Low statistical power in real-robot planning experiments.** The zero-shot planning results are based on only 5 trials per task with no reported confidence intervals or significance tests. Differences such as 75% vs 83% (Stack Cubes) or 83% vs 92% (Push Fruits) may not be reliable given such small samples, especially under randomized initial conditions. Without error bars or statistical tests, the claimed up-to-35% improvement is not convincingly supported.

2. **The V-WM baseline is inadequately specified.** It is unclear whether the vision-only model is: (a) the same architecture with tactile encoders removed and trained from scratch, (b) the same model with tactile inputs masked during inference, or (c) a differently designed baseline. Without this information, it is impossible to isolate the contribution of tactile sensing from possible confounding factors such as architectural differences, training data, or hyperparameter choices.

3. **Data efficiency comparison is fundamentally unfair.** VT-WM benefits from extensive multi-task pre-training on many demonstrations across multiple tasks, while the behavioral cloning (BC) policy is trained from scratch on only 20 demonstrations of the target task. The 3.5× improvement reflects the value of pre-training, not the data efficiency of the world model framework itself. A proper controlled comparison would include VT-WM *without* pre-training (trained from scratch on 20 demos) or BC with similar pre-training.

### Minor
- Only five manipulation tasks are evaluated, all relatively similar (tabletop pick-and-place, pushing, wiping, stacking). Generalization to more diverse contact-rich tasks (e.g., assembly, deformable objects, in-hand manipulation) is not demonstrated.
- No ablation study examines design choices for tactile encoding: e.g., raw tactile images vs. Sparsh-X embeddings, number of tactile frames, or the effect of the shorter tactile horizon.
- Planning computation time or inference speed is not reported, which is important for assessing practical deployability in real-time robot control.

### Trivial
None.

## Nice-to-Haves
- Include confidence intervals (e.g., bootstrap) and significance tests for the real-robot planning success rates.
- Clarify the V-WM training procedure in the main text, not just in the appendix.
- Add an ablation of VT-WM trained from scratch on the new task to disentangle the benefits of pre-training from the world model structure.
- Evaluate on tasks requiring finer contact discrimination (e.g., peg insertion with variable force, fragile object manipulation).

## Novel Insights
None beyond the paper's own contributions.

## Suggestions
1. Increase the number of real-robot trials per task (e.g., to 20+) and report bootstrapped confidence intervals and p-values for the success rate differences.
2. Clearly specify the V-WM baseline: if it shares the same architecture minus tactile, state this explicitly; if it uses a different design, justify and ablate appropriately.
3. For the data efficiency experiment, include comparisons where VT-WM is trained from scratch on 20 demos (no multi-task pre-training) and where BC is pre-trained on the multi-task dataset, to isolate the effect of the world model approach vs. pre-training.
4. Report planning wall-clock time and the number of CEM iterations, as these affect practical usability.
5. Ablate the tactile encoding: compare using raw Digit 360 images vs. Sparsh-X embeddings, and vary the tactile history length.

## Score and Decision
I find the core idea valuable and the imagination metrics reasonably convincing, but the real-robot planning results are underpowered, the baseline comparison is ambiguous, and the data efficiency claim is overstated. These issues weaken the evidence for the paper's main claims and reduce confidence in the reported improvements. A significantly strengthened experimental section could remedy these concerns.

**Score:** 5

**Decision:** Reject

MY FINAL SCORE: <score>5</score>
MY FINAL DECISION: <decision>Reject</decision>