Now I have a thorough understanding of the paper. Let me draft the review before calibration.Now let me proceed to Round 1 calibration — bracketing the score range by searching for similar papers across score bands.Let me read the most relevant anchors in detail for calibration.Now I have strong calibration anchors. Let me finalize my assessment.

**Round 1 Bracket:** Based on the anchors:
- x33vSZUg0A (5.33) — most directly comparable: multi-task compression. The paper under review has stronger theoretical contribution (Theorem 1, clean β parameterization) but similar experimental limitation patterns.
- 3n4RY25UWP (6.25) — disentangling shared vs modality-specific information using info theory. Conceptually very similar; paper under review has comparably deep theory in a more specific domain.
- Tv36j85SqR (7.20) — tighter theory-to-practice gap, more thorough experiments. Paper under review is weaker on the experimental side.
- Papers in the 3-4 range (DsMxVELk3K, 6j0GH40mFt) had more fundamental issues; the paper under review is clearly stronger.

**Initial bracket: 5.0–7.0**, most likely 5.5–6.5.

The paper has a genuine theoretical contribution (Theorem 1), a principled and novel framework, and strong synthetic validation, but the CV experiments show non-trivial gaps to Joint and the hard masking is an acknowledged design limitation. This places it firmly in the borderline-accept range, comparable to 3n4RY25UWP (6.25) and stronger than x33vSZUg0A (5.33).

Now let me write the final consolidated review.

---

## Summary
This paper bridges classical information theory — specifically the Gray-Wyner network and associated notions of common information (Wyner's and Gács-Körner) — with modern learnable multi-task compression. It contributes Theorem 1, extending lossy common information bounds via interaction information, derives a Lagrangian optimization objective (Theorem 2, Eq. 12) with a single hyperparameter β controlling the transmit-receive rate tradeoff, and proposes a three-channel neural codec architecture validated on synthetic, colored MNIST, and computer vision benchmarks.

## Strengths

- **Theorem 1 is a genuine theoretical contribution.** Extending Wyner's lossless result to the lossy setting — showing that lossy GK and Wyner's common information are bounded by interaction information over their respective achievable sets (Eqs. 6–7) — provides real insight. The equality conditions connecting to separability of the stochastic matrix (Eq. 8) are not trivial and directly predict practical behavior observed in experiments (Mixture PMF difficulty in Section 4.2).

- **The β parameterization cleanly operationalizes the transmit-receive tradeoff.** The mapping from α₁, α₂ in Eq. 9 to β in Eq. 12 is elegant: β=1 optimizes transmit rate, β=2 optimizes receive rate, β=3/2 balances both. This is empirically validated in Figures 3a, 3c, and 3d, where the common channel rate with β=1 exceeds empirical mutual information and β=2 falls below it — exactly matching theory.

- **The synthetic experiment (Section 4.1, Figure 3) is the paper's strongest empirical evidence.** The theory-practice link is convincingly demonstrated: β controls common channel rate relative to MI, and the comparison between theoretical and empirical rate-distortion curves calibrates the learned codec against optimal. The architecture comparison (Shared outperforming Separated and Combined in Figure 3b) is useful and backed by a compatibility-based justification (Appendix C).

- **Edge-case validation on colored MNIST (Section 4.2) is well-designed.** Testing on Dependent (all info common), Independent (zero MI), and Mixture (partial, non-separable MI) PMFs demonstrates the framework handles degenerate cases correctly and behaves as theoretically predicted.

## Weaknesses

### Fatal
None

### Major

- **The hard masking mechanism (Eq. 14) is a design bottleneck that limits practical performance.** Y₀ requires element-wise exact equality between quantized Y₀⁽¹⁾ and Y₀⁽²⁾, zeroing out non-matching elements. The paper acknowledges the γ tension (Section 3.3: "Small values of γ might result in elements...never matching. A large γ can result in degenerate distributions") but resolves it by fixing γ=1 and adjusting β, which is ad hoc. This mechanism rewards element-wise agreement rather than maximally informative common features — these are different objectives. The resulting gap to the Joint baseline in Figure 5 (23.32% and 13.16% BD-rate on transmit rate for Cityscapes and COCO; 51.97% and 42.70% on receive rate) is substantial and likely partly attributable to this constraint. While some gap is structurally inherent to three-channel decomposition, the magnitude suggests the masking is a significant bottleneck.

- **The CV experiments (Section 4.3) demonstrate the concept but do not establish practical significance.** The proposed method outperforms Independent coding, but the more informative comparison against Joint shows large gaps (above). The paper does not discuss practical scenarios where the three-channel decomposition would be preferred over joint coding — yet this is the key practical question a deployment engineer would ask. Without this discussion, the experimental evaluation reads as a proof-of-concept rather than a case for practical adoption.

### Minor

- **Theorem 2's richness assumption weakens the theory-practice link.** Theorem 2 assumes the function families contain optimizers achieving T(α₁, α₂; D₁, D₂). In practice, finite-capacity neural networks do not satisfy this, and the gap is visible in Figure 3b (acknowledged: "considerably higher than the theoretical values"). While the Lagrangian relaxation provides a reasonable heuristic regardless, the theorem's conclusion does not strictly hold for the actual system.

- **The introduction's motivating scenario is never tested.** The introduction describes sequential transmission (camera sends info for one task, then sends only additional info for the second), but all experiments encode all three channels simultaneously. Testing this scenario would directly validate the paper's practical narrative.

- **The composite performance metric obscures per-task behavior.** In Section 4.3, adding mIoU and scaled inverse depth RMSE (or detection and keypoint mAP) conflates tasks with different scales. A method could improve one task while degrading the other, and the sum hides this.

- **The aggregated BD-rate claim is misleading.** The conclusion's "BD-rate advantage of −81.58% in transmit rate, against single-task codecs" averages across synthetic, MNIST, and CV experiments. The bulk comes from synthetic/MNIST where the gap is naturally larger, making this a misleading summary of practical CV performance.

- **The α₁ = α₂ assumption is not discussed for real experiments.** Section 3.2 assumes equal cost for both private channels. For tasks with very different complexity (e.g., segmentation vs. depth estimation), this may be restrictive, but no analysis or discussion is provided.

### Trivial
None

## Nice-to-Haves
- Replacing the hard masking (Eq. 14) with a softer mechanism (e.g., learned soft-gating or variational formulation encouraging MI capture) is the highest-leverage improvement.
- Comparison against existing multi-task compression methods (Chamain et al., 2021; Feng et al., 2022; Guo et al., 2024) on transmit rate would contextualize performance.
- Computational overhead analysis comparing Shared against Joint/Independent baselines.
- Expanding the synthetic experiment to sweep separability levels would more directly validate Theorem 1's bounds.
- Per-task rate-distortion curves for the CV experiments.

## Removed Points
*These points are flagged to be removed; treat them with caution.*

- **"Dated architectures" concern**: The reviewer noted DeepLabV3+/MobileNet, LRASPP, Faster R-CNN are dated. Removed because the paper is proving a framework concept, not pushing SOTA on specific vision tasks. Architecture modernity is irrelevant to the core contribution.
- **Missing variance/confidence intervals**: Removed per field norms — single-run evaluation is standard for learned compression benchmarks at this scale.
- **"Within an order of magnitude" phrasing**: The reviewer flagged this as underselling the gap to theoretical bounds. The paper contextualizes it appropriately by citing Bajić (2025) as comparable to other codecs. This is a presentation preference, not a substantive weakness.
- **Markov conditions mismatch**: The reviewer noted Theorem 1 may depend on Markov conditions (Eq. 1) that the Shared architecture violates. The paper explicitly addresses this in Section 3.3: "This effectively removes the requirement for the conditions in 1." The architecture is intentionally more flexible than the classical setting.
- **No experiments with low/moderate common information on real data**: The colored MNIST Mixture and Independent PMFs partially address this. Demanding additional real-data experiments with low MI is scope creep for a paper already testing three experimental settings.

## Novel Insights
The paper's key novel insight is that interaction information I(X₁, X₂; Ẑ₁; Ẑ₂) serves as a bridge between lossy Gács-Körner and Wyner's common information, with the separability condition (Eq. 8) determining whether these quantities coincide. This theoretical insight directly predicts practical difficulty: the Mixture PMF in Section 4.2 has non-separable common information, and the method indeed struggles there relative to the Dependent PMF, demonstrating internal coherence between theory and experiment. The β-parameterized tradeoff between transmit and receive rates is a conceptually clean contribution that could inform future multi-task system design.

## Suggestions
- Replace or augment the hard masking with a differentiable mechanism that directly encourages mutual information capture in Y₀ rather than element-wise agreement.
- Show per-task rate-distortion curves for CV experiments to demonstrate the method doesn't trade off one task for another.
- Report BD-rate for CV experiments separately from synthetic/MNIST to provide an honest summary of practical performance.
- Demonstrate the sequential transmission scenario experimentally to close the gap between motivation and evaluation.
- Discuss practical deployment scenarios where the three-channel decomposition is preferred over joint coding, quantifying the tradeoff.

## Score and Decision

### Calibration Anchors

| Paper | Avg Score | Round | Comparison |
|---|---|---|---|
| x33vSZUg0A (Multi-task compression, causal discovery) | 5.33 | R1 | Most directly comparable; paper under review has stronger theoretical contribution (Theorem 1, β parameterization) but similar experimental limitations |
| 3n4RY25UWP (Disentangled SSL, multimodal) | 6.25 | R1 | Conceptually very similar (disentangling shared vs specific info with info theory); paper under review has comparable theoretical depth in a more focused domain |
| Tv36j85SqR (Lattice Transform Coding) | 7.20 | R1 | Tighter theory-practice connection and more thorough experiments; paper under review is weaker on experimental side |
| jznbgiynus (Language Modeling Is Compression) | 6.00 | R1 | Similar "bridging two fields" character; paper under review has more technical depth but narrower scope |
| CxXGvKRDnL (Progressive Compression, Diffusion) | 8.00 | R1 | Much stronger experimental validation and tighter theory-practice gap; clearly above |
| DsMxVELk3K (TextEconomizer) | 3.00 | R1 | Much weaker theoretically and experimentally; clearly below |
| 6j0GH40mFt (Window-Based Dynamic Attention, LIC) | 3.40 | R1 | More fundamental issues in contribution; clearly below |
| aQ7qYnY2nF (Task-Aware Video Compression, RL) | 4.00 | R1 | Less principled approach, weaker theory; below |
| ulIW7Frjpn (LLMs as Entropy Models) | 4.75 | R1 | Different focus; paper under review has stronger novelty in the multi-task decomposition |
| VkWbxFrCC8 (RECOMBINER) | 6.67 | R1 | Stronger experimental results within its scope; comparable contribution level |

**Round 1 bracket: 5.0–7.0**

**Narrowing:** The paper has a genuine standalone theoretical contribution (Theorem 1) that is novel and insightful, a clean operationalization of the transmit-receive tradeoff, and convincing synthetic/MNIST validation. These put it above x33vSZUg0A (5.33). However, the major weaknesses — the hard masking bottleneck causing significant gaps to Joint, and the proof-of-concept character of CV experiments — prevent it from reaching Tv36j85SqR (7.20) or VkWbxFrCC8 (6.67) territory. It is most comparable to 3n4RY25UWP (6.25) and jznbgiynus (6.00): papers that bridge communities with genuine theoretical insight and reasonable but imperfect experimental validation.

**Final score: 6.0** — This is a borderline accept paper. The theoretical contributions (Theorem 1, β-parameterized tradeoff) are genuine and above-average for the venue. The synthetic and MNIST experiments convincingly validate the framework. The practical realization has real limitations (hard masking, gap to Joint), and the CV experiments are more proof-of-concept than practically compelling. Overall, the paper makes a meaningful contribution bridging information theory and learned compression that will interest both communities.

MY FINAL SCORE: <score>6.0</score>
MY FINAL DECISION: <decision>Accept</decision>