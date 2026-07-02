## Summary

This paper investigates whether compositional generalization (necessary for data-efficient perception) favors generative (decoder-based) or non-generative (encoder-based) approaches. It formalizes the problem through identifiability: guaranteeing OOD generalization requires constraining a model to the function class ℱ_int (generators) or 𝒢_int (inverse generators). Theorem 3.2 proves that when d_x ≥ d_z³, the derivatives of inverse generators can be arbitrarily complex, making it infeasible to constrain an encoder to 𝒢_int via practical means. Conversely, constraining a decoder to ℱ_int is straightforward via architecture or regularization. Empirically, on PUG datasets, non-generative methods often fail OOD unless large-scale pretrained, while generative methods (autoencoder + replay + search) improve OOD performance without additional data.

## Strengths

- **Clean formal framework for compositional generalization (Section 2).** Equations (2.5)–(2.6) precisely capture what identifiability requires for OOD generalization, and the distinction between generative (Eq. 2.2) and non-generative (Eq. 2.3) approaches in terms of what must be identified (f vs. g) is well-drawn. This gives the field a precise language for a previously fuzzy concept.

- **Theorem 3.2 is a genuine theoretical result.** The proof that, when d_x ≥ d_z³, the Jacobian and Hessian of inverse generators in 𝒢_int can be essentially arbitrary (up to measure zero) is non-trivial. It establishes an inherent asymmetry between generators and their inverses that is not obvious a priori and has implications beyond this paper's specific experiments.

- **Appropriate empirical testbed.** The PUG datasets (Bordes et al., 2023) provide controlled compositional generalization tests with photorealistic images and explicit control over in-domain vs. out-of-domain concept combinations. The three splits (Background, Texture, Object) span a meaningful range of compositional difficulty, and the PUG-Object result (all methods succeed when concepts do not interact, n=0) provides a nice sanity check consistent with the theory.

## Weaknesses

### Fatal
None.

### Major

1. **The experimental comparison does not isolate whether the gains attributed to "generation" come from the decoder structure, from replay (data augmentation), or from test-time search.** The "generative" methods (Fig. 6) differ from the "non-generative" baselines (Fig. 5) in multiple conflated ways: (a) use of a decoder, (b) replay training on synthetic OOD data, (c) test-time optimization via search. The paper provides partial disentanglement — replay cannot be applied on PUG-Texture, yet search still helps (Fig. 6B) — which isolates search as independently beneficial. However, a critical missing control is: train a *non-generative* encoder on the replay-generated OOD data (without test-time search). If that encoder alone matches the "with replay" condition in Fig. 6, the advantage is attributable to having OOD training data (data augmentation), not to the generative inference procedure. If it does not match, the test-time search is the active ingredient. Either result would clarify the mechanism, but the paper's framing attributes the gains to "generation" without this ablation.

2. **The latent dimension d_z used in experiments is not reported, making it impossible to verify whether Theorem 3.2's condition d_x ≥ d_z³ holds.** For 224×224×3 images (d_x = 150,528), the condition requires d_z ≤ ~53. If the actual latent dimension is larger (e.g., 128 or 256), the condition fails and the theorem does not directly apply to the experimental setting. The paper needs to (a) report d_z, (b) verify whether the condition holds, and (c) discuss what the theory predicts when it does not.

### Minor

3. **The data-efficiency claim is asserted rather than directly tested.** The paper argues that non-generative methods require large-scale pretraining (data-inefficient) while generative methods improve without additional data. However, the experiments compare models at different pretraining scales (from scratch → ImageNet → web-scale) rather than systematically varying training set size for a fixed method. The "data efficiency" is inferred from the scale of pretraining data used by different models, not measured directly. A controlled experiment varying data volume for the same architecture would substantiate this claim more rigorously.

4. **No confidence intervals, error bars, or multiple-run statistics are reported.** Fig. 5 and Fig. 6 report point estimates only. With ~20,000 images per split, variance across random seeds or data subsets is non-negligible, especially for methods near chance or at intermediate accuracy levels. Multiple runs would clarify which differences are reliable.

5. **The "best-performing combination" reporting reduces comparability.** For each base encoder, the paper reports the OOD accuracy of the best-performing slot encoder (Transformer vs. Slot Attention) and fine-tuning choice (frozen vs. LoRA). Since these choices are optimized independently per model, cross-model comparisons conflate base encoder differences with slot encoder / fine-tuning differences.

6. **Title overclaims relative to the evidence.** The title "Generation Is Required for Data-Efficient Perception" implies categorical necessity. Yet the paper's own results show SigLIP2 (a non-generative method) achieves ~80% OOD accuracy on PUG-Background and ~85% on PUG-Texture. Non-generative methods *can* work — they just require more pretraining data. The paper's actual contribution is better captured by a claim like "non-generative methods face fundamental obstacles to *guaranteeing* compositional generalization, though they can work in practice with sufficient data." The gap between "cannot be guaranteed" and "is required" is significant.

### Trivial
None.

## Nice-to-Haves

- **Analyze search convergence behavior.** The gradient-based search (Sec. 4.1) involves test-time optimization. Reporting how many gradient steps are needed, whether convergence is reliable, and how initialization quality affects results would strengthen practical applicability claims.

- **Report the condition d_x ≥ d_z³ explicitly.** Beyond reporting d_z, a direct check of whether the condition holds for the experimental setup would tighten the theory-experiment connection.

## Removed Points

These points were raised in the input review but are removed per filtering rules. Treat with caution; they may be partially valid but fail verification against the paper.

1. **"The theoretical and empirical claims operate at different levels and the paper does not connect them."** — Removed. The paper does not assert that experiments *prove* the mechanism in Theorem 3.2. The narrative is: theory shows guarantees are infeasible for encoders → empirically, encoders often fail. These are complementary arguments, not a causal chain. The paper never claims the specific derivative property causes the observed failures; it claims the theory explains *why* encoders cannot guarantee generalization, and the experiments show they empirically do fail.

2. **"The n > 1 case is not covered by the theory."** — Removed. The paper explicitly states (line 117): "We emphasize that this result applies to ℱ_int with arbitrary interaction degree n ≥ 1 and any slot dimensions." Theorem 3.2 covers the experimental regime.

3. **"Theorem 3.2 only proves difficulty at a single point."** — Removed. The theorem states "for any x₀," meaning the result holds at every point individually. This is sufficient to argue that local regularization cannot enforce the constraint globally, since a counterexample function exists at any given OOD point.

4. **Various formatting, style, and reproducibility nitpicks.** — Removed per hard rules (parser artifacts, missing appendix content, trivial implementation details).

## Novel Insights

None beyond the paper's own contributions. The reviews largely reinforced the paper's narrative rather than exposing contradictions or alternative interpretations. The most valuable critical observation is the lack of a control experiment separating data augmentation from generative inference (Weakness 1), which points to a concrete way to strengthen the work on its own terms.

## Suggestions

1. **Run the missing control experiment.** Train a non-generative encoder (no decoder, no test-time search) on replay-generated OOD data and evaluate its OOD accuracy. If it matches "with replay" in Fig. 6, reframe the contribution around the utility of synthetic OOD data; if it does not, the contribution is about test-time search.
2. **Report d_z and check d_x ≥ d_z³.** Add a line to the experimental setup stating the latent dimension(s) used and whether the theorem condition holds. If it does not hold, add a discussion of what the theory predicts in that regime.
3. **Add error bars.** Report means and standard deviations over at least 3 random seeds for the main results.
4. **Tone down the title.** Replace the categorical "Generation Is Required" with something that reflects the actual finding, e.g., "Theoretical Obstacles to Guaranteeing Compositional Generalization with Non-Generative Methods."

## Score and Decision

MY FINAL SCORE: <score>6.5</score>
MY FINAL DECISION: <decision>Accept</decision>