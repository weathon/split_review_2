Now let me write the final review.

## Summary

This paper proposes a compositional meta-learning framework where a generative model over tasks (consisting of reusable module RNNs and a gating RNN) is learned during training, and new tasks are solved via probabilistic inference (particle filtering) without any parameter updates at test time. The approach cleanly separates learning "task syllables" (module dynamics) from learning the "task grammar" (gating transitions). Experiments on synthetic rule learning and motor learning tasks demonstrate ground-truth recovery of modular structure, one-shot task inference from a single episode, graceful handling of sparse feedback through constrained hypothesis testing, and generalization to much longer horizons than seen during training.

## Strengths

- **A genuinely different approach to meta-learning.** Instead of learning an initialization for fine-tuning (MAML-style), the paper frames meta-learning as learning a generative model over tasks and solving new tasks via probabilistic inference — no parameter updates at test time. The separation between gating RNN (task grammar) and module RNNs (task syllables) is a compelling organizing principle and is well articulated.

- **Strong demonstration of sparse feedback handling (Figures 2e, 4e).** When y_t is available at only a few timesteps, the particle filter tracks multiple hypotheses about which module is active, constrained by learned gating dynamics. The posterior collapses when feedback arrives, confirming the correct branch. This is a direct and elegant consequence of the probabilistic inference formulation that standard gradient-based meta-learning methods cannot naturally replicate.

- **Generalization to longer horizons without retraining (Figures 2f, 3f).** The model solves test tasks 4× longer than any training task and handles double-length tasks better than retraining baselines. This directly demonstrates compositional generalization: the model has learned durations and transition rules, so extending the sequence does not require new learning.

- **Clean control experiments (Figures 3a–f).** The four-way comparison (standard RNN, RNN+task ID, flat transitions, full model) cleanly isolates what each architectural component contributes. The comparison against MAML, MLDG, and pre-trained/frozen-weight baselines appropriately shows that the proposed method achieves good performance in a single episode where all gradient-based methods require hundreds.

- **Ground-truth verification in two domains (Figures 2b–c, 4b–c).** Recovery of known shift operations and known motor skills provides direct evidence that the model has learned the intended compositional structure, not just memorized training tasks.

## Weaknesses

### Major

- **Limited evaluation scope relative to the claims.** The experimental validation is restricted to simple synthetic tasks: 6D vector shifts with deterministic stay-switch patterns and 2D translation chunks. These tasks are constructed to have the exact modular structure the model assumes. The paper's broader claims — that the framework "joins the expressivity of neural networks with the data-efficiency of probabilistic inference" (abstract) — are not supported by commensurate evidence. It remains unclear whether the model can discover modular structure in tasks with non-linear functions, stochastic transitions, higher-dimensional outputs, or naturalistic data, or whether the particle filter scales to more modules or longer sequences. The paper acknowledges these are "proof-of-principle" tasks (Discussion), but the abstract and introduction do not reflect this caveat. This gap is the single most important limitation of the paper.

- **Missing quantitative comparison against the most closely related inference-based compositional methods.** The paper discusses Alet et al. (2019) and Hummos et al. (2024) qualitatively — both propose compositional meta-learning without parameter updates on test tasks — but provides no quantitative comparison. For Alet et al. (2019), the paper claims "We effectively replace this search by probabilistic inference on learned structure, greatly improving sample efficiency" without evidence. For Hummos et al. (2024), a conceptual difference (sequencing modules along learned transition statistics) is noted without demonstrating measurable benefit. The only quantitative baselines are gradient-based methods (MAML, MLDG) that fundamentally require parameter updates at test time, making the comparison asymmetric. Without quantitative comparison against the most similar methods, the reader cannot assess whether the specific innovations in this paper improve over existing inference-based compositional approaches.

### Minor

- **Domain-specific architectural modifications for motor learning (Section 2.4).** Applying the model to motor learning requires removing the x_t input, resetting module hidden states after switches, adding module-specific parameters, and changing the particle filter proposal distribution. While each change is individually reasonable, the net effect is that the "same" model requires multiple task-specific adjustments, which somewhat undermines the claim of a unified framework.

- **Particle filter training procedure is summarized but not fully detailed in the main text.** The paper reports using the Gumbel-Softmax trick for the module selection (Equation 2) but does not explicitly address how gradients flow through the stratified resampling step (Equation 6). The main text mentions backpropagating through the particle filter and refers to Appendix A.2 for details. While implementation details are legitimately deferred to the appendix, the resampling differentiability is central enough to the method's training procedure that at least naming the technique in the main text would help the reader.

### Trivial

- **Minor inconsistency in the parameter set notation.** Line 45 defines Λ = {σ, θ, φ, W_G, W_M}, but line 67 restates it as Λ = {σ, φ, W_G, W_M}, omitting θ.

## Nice-to-Haves

- Report wall-clock inference time per episode for the particle filter (K copies of both RNNs) vs. gradient-based methods. The comparison in Figure 3e counts episodes, not compute. A method requiring 500 episodes but running 100× faster per episode could be more practical for some applications.
- State the value of K (number of particles) and Gumbel-Softmax temperature in the main text for reproducibility.
- Clarify in the abstract/introduction that the current evaluation is on proof-of-principle synthetic tasks, to better align the claims with the evidence.

## Removed Points

These points were raised in the input review but are removed after cross-checking against the paper:

- **"One-shot" terminology concern:** The reviewer noted that "one-shot" in this paper means "one episode" (multiple timesteps) rather than "one labeled example per class." The paper uses the term consistently with its own definition; this is a terminology preference, not a substantive weakness. REMOVED.
- **Figure caption/equation discrepancy about gating RNN inputs:** The simpler OCR'd figure caption mentions m_{t-1} while Equation (1) uses z_{t-1}. The detailed caption (line 77) correctly uses z_{t-1}, matching the equation. The simpler caption inconsistency is a parser artifact from the image description. REMOVED.
- **Missing hyperparameters (optimizer, learning rate, hidden dimensions, K, temperature):** These are standard implementation details that the reproducibility statement places in the appendix and code. REMOVED per Hard Rules.
- **No statistical tests/confidence intervals:** The paper shows individual seeds and means. For a proof-of-concept study on synthetic tasks, this level of reporting is sufficient and standard. REMOVED.
- **Flat transitions control narrows contribution:** The reviewer framed this as limiting the contribution of the gating RNN. The paper itself acknowledges this — the flat transitions model achieves one-shot inference with full feedback, and the gating network is specifically needed for sparse feedback. The paper's claims are consistent with this finding. The observation is valid but already present in the paper's own analysis; included as a minor point above in weakened form. REMOVED as a standalone weakness since the paper already addresses it.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. **Add at least one experiment on a task where modular structure is not hand-crafted to match the model's assumptions** — for instance, a higher-dimensional synthetic task with compositional structure, or a standard benchmark where modules must be discovered rather than matched to known operations. Even if the method does not reach state-of-the-art, demonstrating discovery of compositional structure in a less contrived setting would substantially strengthen the core claim.

2. **Include a quantitative comparison against Alet et al. (2019) or Hummos et al. (2024)** on the existing synthetic tasks. The paper already has the control infrastructure set up; adding one more baseline that is an "inference-based compositional meta-learning" method (rather than gradient-based) would close the most important gap in the evaluation.

3. **State the number of particles (K) and the Gumbel-Softmax temperature in the main text** for easier reproducibility assessment.

## Score and Decision

### Calibration Anchors

| Path | Avg Score | Round | Itemized | Comparison to this paper |
|------|-----------|-------|----------|--------------------------|
| `EHmjRIA4l2.md` (Compositional World Models) | 3.00 | R1 | Yes | Much weaker; lacks baselines, unclear experiments. Our paper is clearly stronger. |
| `8khcyTc4Di.md` (Meta-Learning Neural Procedural Biases) | 4.00 | R1 | No | Synthetic-only experiments, gradient-based meta-learning. Less novel approach. |
| `6r0BOIb771.md` (Sequential Bayesian Continual Learning) | 5.33 | R1 | Yes | Broader experiments but less conceptual novelty in the approach. Comparable quality. |
| `5Qxx5KpFms.md` (Breaking Scaling Laws with Modularity) | 6.00 | R2 | Yes | Has theory; experiments include CIFAR-10. Our paper has cleaner controls and more novel approach. |
| `H98CVcX1eh.md` (Discovering modular solutions) | 6.50 | R1 | Yes | Most topically similar. Has theory but limited synthetic experiments. Our paper has stronger empirical validation but no theory. |
| `7VPTUWkiDQ.md` (Provable Compositional Generalization) | 7.33 | R2 | Yes | Strong theory, but experiments only on 2-object synthetic images. Our paper has more thorough experiments. |

### Bracket and Calibration

**Round 1 bracket:** 5.5–7.5. The paper is clearly stronger than the 1.5–3.5 and 3.5–5.5 bands (rejected papers with major structural issues). It is not as strong as 7.5–8.5 papers, which typically combine strong theory with broader validation.

**Round 2 narrowing:** The closest anchor is "Discovering modular solutions that generalize compositionally" (6.5, accepted). Both use synthetic tasks with known ground-truth modular structure. That paper is accepted despite narrow scope because it provides theoretical guarantees; our paper has no theory but stronger empirical demonstration (sparse feedback, length generalization, clean controls). Comparing impact scores: our paper's strengths rate comparably (+8 to +10 vs. +9.95 to +10 for that anchor). Both papers have -10 weaknesses. Our two major weaknesses (limited scope, missing comparison) are evidential gaps rather than structural flaws, which is why the paper sits toward the upper end of the bracket. However, without the quantitative comparison against the closest inference-based methods, the contribution is less precisely contextualized than it should be, placing it at the lower end of the 5.5–7.5 bracket rather than at the 6.5 anchor level.

MY FINAL SCORE: 6.0
MY FINAL DECISION: Accept