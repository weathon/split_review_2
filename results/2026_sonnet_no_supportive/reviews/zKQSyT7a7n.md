## Summary
VT-WM is the first multi-task visuo-tactile world model for robot manipulation, integrating fingertip tactile sensing (four Digit 360 sensors on an Allegro Hand) with exocentric vision via a transformer predictor that fuses Cosmos visual latents with Sparsh-X tactile embeddings. Evaluated on five contact-rich manipulation tasks with a real robot, VT-WM demonstrates 33% improvement in object permanence and 29% improvement in causal compliance over a vision-only baseline (V-WM), achieves up to 35% higher zero-shot CEM planning success rates, and outperforms ACT behavioral cloning 3.5× in a 20-demonstration data efficiency study.

---

## Strengths
- **Real-robot hardware commitment**: Implementing Digit 360 sensors on all four fingertips of an Allegro Hand on a Franka Panda, collecting multi-task demonstrations, and executing open-loop CEM plans across five contact-rich tasks is a substantial engineering commitment. Most world-model papers at this venue operate only in simulation.
- **Novel, principled imagination-quality metrics**: Using CoTracker keypoint tracking to compute normalized Fréchet distance separately for *moving* objects (object permanence, Fig. 4) and *static* objects (causal compliance, Fig. 6) is a well-motivated evaluation instrument. Paired t-tests are correctly applied (e.g., t=4.38, p<0.001 for place fruits; t=6.06, p<10⁻⁶ for push fruits), and the asymmetry between "should-move" and "should-stay" objects is exactly the right decomposition for testing contact physics.
- **Data efficiency result (Section 4.3)**: VT-WM fine-tuned on 20 demonstrations achieves 77% vs. 22% for ACT on the plate-insertion task — a concrete 3.5× advantage that demonstrates the value of multi-task pretraining over task-specific behavioral cloning.
- **Concrete, grounded failure-mode illustrations**: Fig. 1 (V-WM substituting the wrong cube under occlusion) and Fig. 7 (cloth keypoints spuriously displacing in V-WM when the hand is not in contact) are unambiguous visual demonstrations of the failure modes being addressed.

---

## Weaknesses

### Fatal
None.

### Major

- **Trial-count inconsistency in planning results (Section 4.2)**: The paper states "success rates, averaged over five trials per task from distinct initial conditions," yet Figure 8 (left) reports rates of 69%, 83%, 92%, 93%, 70%, 75% — none of which are representable as fractions with denominator 5 (only multiples of 20% are possible at n=5). The actual denominator appears to differ from the stated five, calling into question the accuracy of the experimental description. Combined with the absence of any statistical significance test for the planning results (in direct contrast to the careful paired t-tests in Section 4.1), the headline claim of "up to 35% higher success rates" rests on an unverified and likely small sample with no accompanying uncertainty estimates. This creates a material evidentiary gap between the paper's strongest finding (imagination quality) and its top-line planning claim.

- **No ablation isolating the tactile signal (Sections 3–4)**: The only comparison in the paper is V-WM vs. VT-WM, which differ jointly in (a) the presence of tactile input, (b) added model parameters to process it, and (c) a richer multi-modal training objective. A "V-WM+" control condition — same architecture as VT-WM but with zeroed or dummy tactile inputs — would isolate whether gains stem from genuine contact grounding versus added model capacity. This matters especially for the causal compliance metric: a higher-capacity model might learn conservative dynamics (less predicted motion in general) rather than physics-specific contact awareness. Without this control, the attribution of improvement to tactile sensing specifically is incomplete.

### Minor

- **Scribble-with-marker degradation unexplained (Figure 6)**: VT-WM is *worse* than V-WM on the scribble-with-marker task for causal compliance (t=−1.22, VT-WM Fréchet ≈0.50 vs. V-WM ≈0.35, non-significant but directionally reversed). The paper acknowledges this without offering any explanation. Since this is the one task where tactile grounding hurts, it has genuine diagnostic value — a potential hypothesis is distributional mismatch in the Sparsh-X embeddings for dry marker-on-paper contact — and its absence limits the reader's understanding of when VT-WM's grounding breaks down.

- **Data efficiency confound (Section 4.3)**: The comparison of VT-WM (fine-tuned) vs. ACT BC conflates "multi-task world model pretraining" with "visuo-tactile grounding." Adding a fine-tuned V-WM (same multi-task pretraining, no tactile input) as a third condition would isolate whether the 3.5× data efficiency advantage comes from multi-task WM pretraining in general or specifically from contact grounding via touch. As structured, the Section 4.3 claim about contact grounding enabling data efficiency is not directly supported.

### Trivial
- The description of the planning setup notes "we do not provide the tactile modality as a goal signal" (Section 3.2.3) without empirical justification. This is a design choice that limits the planning framework but is presented as if it were fully motivated.

---

## Nice-to-Haves
- More planning trials per task (e.g., 15–20) with bootstrap confidence intervals would bring the planning evaluation to the same statistical rigor as the imagination quality results in Section 4.1.
- An ablation on tactile context length (Section 3.2.2 uses only 2 frames per sensor over 0.16s); for slip detection, longer tactile history may be informative, and a brief ablation would validate the design choice.
- Investigation of the scribble-with-marker causal compliance failure: understanding whether the degradation is due to distributional mismatch in Sparsh-X for dry contact, sensor noise, or task-specific properties would productively bound the model's operating regime.
- A V-WM fine-tuned on the same 20 insertion demonstrations as a third condition in Section 4.3 to disentangle multi-task WM pretraining from tactile grounding.

---

## Removed Points
*These points are flagged to be removed; treat them with caution.*

- **Generic strength "addresses an important problem"**: Non-specific; removed.
- **Criticism that tactile goal signal is absent from CEM**: The paper explicitly frames this as a design choice in Section 3.2.3. Framing its absence as a weakness is scope creep; moved to nice-to-have.
- **Tactile context length ablation as a weakness**: Methodological practice beyond the paper's stated scope; moved to nice-to-have.
- **Criticism of the training objective / sampling loss formulation**: The training objective in Equations 1–2 follows established practice (Assran et al., 2025) and is correctly described. No weakness here.

---

## Novel Insights
The decomposition of imagination quality into *object permanence* (tracking objects that should move) vs. *causal compliance* (tracking objects that should remain stationary) is a genuinely useful evaluation framework for contact-aware world models that extends the World Consistency Score. The finding that tactile grounding helps most in multi-step, sustained-contact tasks (pushing, wiping, placing) while providing little benefit for free-space reach — and actually degrading causal compliance on the scribble-with-marker task — suggests that the benefit is tied to the representational coverage of the pretrained tactile encoder (Sparsh-X), not to multimodal fusion universally. This points toward a productive future direction: characterizing what contact distributions a tactile foundation model covers, and predicting when its grounding benefit will transfer.

---

## Suggestions
1. **Fix or clarify the trial count**: Reconcile the stated "five trials per task" with the reported success percentages that cannot be expressed as fractions with denominator 5. If more trials were run, state the correct number; if fewer, recompute percentages.
2. **Add a capacity-matched ablation**: Include a "V-WM+" condition matching VT-WM's parameter count but with zeroed tactile inputs. This single ablation would substantially strengthen the causal attribution to tactile sensing.
3. **Add V-WM fine-tuned on 20 demos in Section 4.3**: This third condition is essential to disentangle the data efficiency benefit of multi-task WM pretraining from visuo-tactile grounding specifically.
4. **Apply statistical tests to planning results**: Use the same paired t-test or bootstrap CI framework from Section 4.1 in Section 4.2 to report whether VT-WM's planning improvements are significant.
5. **Diagnose the scribble-with-marker failure**: Even a brief hypothesis about why VT-WM degrades on this task would sharpen the paper's claims about operating conditions.

---

## Score and Decision

**Anchor papers retrieved:**

| Path | Avg Score | Round | Comparison |
|---|---|---|---|
| FMsmo01TaI (Vision+Touch M3L for RL) | 4.33 | R1 | Vision-touch fusion for manipulation but task-specific, simulation-only; less novel than VT-WM |
| KTtEICH4TO (CORN contact manipulation) | 4.75 | R1 | Real robot contact manipulation but no world model; narrower scope |
| J4D5WVoc5g (ViTaM-D visual-tactile reconstruction) | 4.50 | R1 | Visual-tactile framework but for reconstruction, not WM planning |
| mnwlhvmKMN (4D embodied world models) | 4.25 | R1 | 4D world model for manipulation but limited results |
| 9pKtcJcMP3 (VLP video language planning) | 7.00 | R1 | Multimodal WM for planning, broader scope and stronger evaluation |
| NtQqIcSbqv (visual-tactile signals learning) | 6.00 | R1 | Visual-tactile for object understanding, dataset contribution |
| c0chJTSbci (zero-shot manipulation diffusion) | 6.25 | R1 | Zero-shot robot manipulation, real hardware, comparable novelty |
| hOELrZfg0J (PWM multi-task world models) | 6.00 | R2 | Multi-task world models for robot manipulation, more rigorous evaluation |
| DINO-WM (world models + zero-shot planning) | 5.75 | R2 | Closely analogous (latent WM + CEM planning), but no real hardware |
| VTDexManip (visual-tactile dexterous manipulation) | 5.50 | R2 | Visual-tactile dataset/benchmark, related scope, accepted |
| vJwjWyt4Ed (view-invariant world models) | 5.40 | R2 | World models for manipulation, real data, narrower contribution |
| KsUh8MMFKQ (thin-shell manipulation) | 8.00 | R1 | Strong real-robot manipulation, comprehensive and rigorous; clearly above VT-WM |

**Round 1 bracket**: 5.5–6.5. VT-WM is more novel than the 4.x-range tactile papers (real hardware, multi-task, world model, zero-shot planning). It is weaker than the 7.0+ range (VLP has stronger statistical evaluation, broader scope). Comparable papers cluster around 5.5–6.0 (DINO-WM: 5.75; PWM: 6.0).

**Round 2 narrowing**: The major trial-count inconsistency and missing capacity-controlled ablation pull VT-WM below PWM (6.0) and VLP (7.0). DINO-WM (5.75) is closely analogous but executes on real hardware less than VT-WM; VT-WM's real-hardware scope and novel metrics push it slightly above DINO-WM. Final score: **5.5**.

MY FINAL SCORE: <score>5.5</score>
MY FINAL DECISION: <decision>Reject</decision>