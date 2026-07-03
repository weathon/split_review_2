Here is my final consolidated review:

---

## Summary

This paper argues that compositional generalization (CG) requires a generative approach — inverting a learned decoder — rather than a purely non-generative encoder-based approach. The authors formalize perception as inverting a generator, define the function classes $\mathcal{F}_{\text{int}}$ (generators with slot-wise structure) and $\mathcal{G}_{\text{int}}$ (their inverses), and prove (Theorem 3.2) that constraining an encoder to $\mathcal{G}_{\text{int}}$ is infeasible for high-dimensional data because the constraints depend on the unknown geometry of the data manifold. In contrast, decoder constraints for $\mathcal{F}_{\text{int}}$ are coordinate-axis-aligned and directly enforceable. Empirically, on OOD splits of the PUG photorealistic dataset, non-generative methods fail unless trained at massive scale, while adding a constitutionally constrained decoder with gradient-based search or generative replay yields consistent OOD accuracy gains.

---

## Strengths

1. **Theorem 3.2 — the unconstrained geometry of encoder derivatives.** The paper proves that when $d_x \geq d_z^3$, the Jacobian and Hessian of any inverse generator $g \in \mathcal{G}_{\text{int}}$ can be arbitrary matrices at a point (up to measure zero). The derivative constraints that make the decoder case tractable vanish entirely for encoders; the remaining structure depends on the unknown tangent space of the data manifold. This is a clean mathematical argument that enforcing $\mathcal{G}_{\text{enc}} = \mathcal{G}_{\text{int}}$ via practical regularization is infeasible for image data.

2. **Empirical evidence across many encoder architectures.** Fig. 5 shows that non-generative methods trained from scratch or with modest pretraining fail on OOD splits, while Fig. 6 shows that adding decoder-based inversion (search/replay) to the *same* base encoders yields consistent OOD accuracy improvements across all 6 tested architectures (from scratch ViT-S/36 to SigLIP2 Gauß-Adm/14). The generative benefit is not architecture-specific.

3. **PUG-Object split confirms a special-case prediction of the theory.** The $n=0$ (non-interacting concepts) case is identified in Sec. 3.1 as one where $\mathcal{G}_{\text{int}}$ has additional sparsity structure. Sec. 5.2 then shows that on PUG-Object (animals never occlude, $n=0$ applies), *all* non-generative methods achieve near-perfect OOD accuracy (Fig. 5C). This direct theory-to-experiment link is a strong point: the theory predicts which setting is easy, and the experiment confirms it.

4. **Principled formalization of the generative/non-generative distinction.** The paper frames perception as inverting a ground-truth generator (Eq. 2.1) and precisely defines generative approaches (learning a decoder and inverting it, Eq. 2.2) versus non-generative approaches (learning an encoder directly, Eq. 2.3). This enables precise identifiability conditions (Eqs. 2.5, 2.6) that ground the analysis, going beyond vague "generative vs. discriminative" dichotomies in prior work.

5. **Controlled photorealistic benchmark for compositional generalization.** The paper constructs PUG-Background, PUG-Texture, and PUG-Object splits from the photorealistic PUG dataset, providing explicit control over in-domain vs. out-of-domain concept combinations — a rigor absent from web-scale benchmarks.

---

## Weaknesses

### Fatal
None.

### Major

1. **Theoretical results are proven only for $n=1$ but claimed for arbitrary $n \geq 1$.**
   Lemma 3.1 and the supporting analysis are presented for $n=m=1$. The paper states (line 95) "similar statements can in principle be derived for higher order derivatives for the case $n > 1$" and later (line 117) asserts Theorem 3.2 "applies to $\mathcal{F}_{\text{int}}$ with arbitrary interaction degree $n \geq 1$." This claimed extension is not actually proven. Since the central theoretical argument — that encoder constraints are infeasible — depends on the structure of $\mathcal{G}_{\text{int}}$, the formal contribution is narrower than claimed. *The result likely extends because $\mathcal{F}_{\text{int}}$ for $n>1$ is a superset of the $n=1$ case, but this is not established in the paper.*

2. **No statistical reporting in the experiments.**
   The paper reports OOD accuracy with no error bars, standard deviations, confidence intervals, or mention of random seeds. The selection of "the best-performing combination of slot encoder and fine-tuning choice" (line 213) without reporting the distribution of outcomes across configurations inflates apparent performance and makes quantitative comparisons unreliable. Given the small dataset size (~20,000 images) and known sensitivity of slot-attention/Transformer slot encoders to initialization, the reported differences between methods could be within the noise of the selection procedure.

### Minor

1. **Title and framing overstate what the evidence supports.** The title "GENERATION IS REQUIRED FOR DATA-EFFICIENT PERCEPTION" makes a categorical claim. The theory shows that generation is required for *guaranteeing* compositional generalization, while the experiments show non-generative methods *can* achieve reasonable OOD performance with sufficient pretraining (e.g., SigLIP2 reaches ~80% on PUG-Background). The contribution list (lines 29-31) correctly describes the theoretical result as about *infeasibility of enforcement* rather than *impossibility of success*, but the title and abstract do not maintain this distinction.

2. **Experimental comparison is structurally asymmetric.** Non-generative methods (Fig. 5) are evaluated encoder-only, while generative methods (Fig. 6) add a decoder with search/replay — strictly more parameters and inference-time computation. A matched-capacity or matched-compute baseline (e.g., an encoder with the decoder's parameters converted to additional encoder capacity) would strengthen the claim that the generative *approach itself*, not just extra model capacity, drives the improvement.

3. **Limited control for concept leakage in pretrained models.** The paper states that PUG images were not in the pretraining set (line 205), but the *concepts* (animals, backgrounds, textures) are certainly present in ImageNet/LAION pretraining. This is not data contamination but means pretrained models may have encountered similar OOD concept combinations. The from-scratch ViT-Small baseline partially addresses this but is not a strong representative of modern non-generative methods.

### Trivial
None.

---

## Nice-to-Haves

- Provide error bars / variance estimates for all experimental results.
- Formalize the extension to $n > 1$ in the theory, or explicitly restrict the theoretical claims to $n = 1$.
- Include matched-compute baselines (encoder with comparable total capacity to the encoder+decoder setup).
- Discuss why large-scale pretraining helps non-generative methods (e.g., do they implicitly learn decoder-like structure through exposure to diverse concept combinations?).
- Report the distribution of OOD accuracy across slot encoder and fine-tuning configurations rather than only the best-performing combination.

---

## Removed Points

These points were raised by reviewers but removed after verification against the paper:

- **Harsh critic: "supervised vs. unsupervised distinction is confusing."** The paper clearly explains this (line 209): supervised methods use cross-entropy loss on category labels; unsupervised VAE methods use reconstruction loss. Both are non-generative because the encoder is not constructed to invert the decoder on OOD data.
- **Harsh critic: "missing unstructured decoder baseline in main paper / missing search hyperparameters."** The paper explicitly defers these to Appendices B and C (line 207, line 183). The parser strips these sections; they exist in the original submission. Per hard rules, appendix-related criticisms are removed.
- **Harsh critic: "missing compute and cost analysis."** Implementation details (gradient steps, learning rates, replay data amounts) are in the stripped appendix. Per hard rules, these criticisms are removed.
- **Harsh critic: "SigLIP2 ~80% OOD shows non-generative success — this undermines the paper."** The paper's claim is about *guaranteeing* CG (theoretical) and about *data efficiency* (empirical). SigLIP2's success at the cost of web-scale pretraining is consistent with the paper's argument that non-generative methods need massive data while generative methods improve without additional data. Moved to Minor weakness #1 (framing issue) rather than a fatal contradiction.

---

## Novel Insights

None beyond the paper's own contributions. The reviews surface no insight that the paper itself does not already articulate.

---

## Suggestions

1. **Restrict the formal claim** about Theorem 3.2's scope to $n=1$, or provide the proof for $n>1$ in the main text.
2. **Add statistical reporting** — error bars, variance across configurations and seeds.
3. **Soften the title and abstract** to match the actual contribution: e.g., "Generation Provides Principled Guarantees for Compositional Generalization" rather than "Generation Is Required."
4. **Show the distribution** of OOD accuracy across slot encoder and fine-tuning configurations, not just the best.
5. **Include a matched-capacity baseline** to disentangle the effect of the generative approach from the effect of added parameters/compute.

---

## Score and Decision

This paper contains a genuinely novel theoretical result (Theorem 3.2) about the asymmetry between enforcing compositional structure on decoders vs. encoders, a clean formalization of the perception-as-inversion framework, and controlled experiments that corroborate the theory — including an elegant special-case confirmation (PUG-Object / $n=0$). The core contribution is solid and of interest to the ICLR community.

However, the paper suffers from two significant weaknesses: (a) the theoretical results are proven only for $n=1$ but claimed for arbitrary $n$, and (b) the experimental results lack any statistical reporting, making quantitative comparisons unreliable. Additionally, the title and framing overstate what the evidence supports.

These weaknesses are fixable in revision (providing the $n>1$ proof extension, adding error bars, softening claims). The paper should not be rejected — the theoretical insight is valuable — but it needs revision to be fully convincing. I calibrate this to a score of **6 — borderline accept**, reflecting a solid contribution with fixable issues that should be addressed in the camera-ready version.

MY FINAL SCORE: <score>6.0</score>
MY FINAL DECISION: <decision>Accept</decision>