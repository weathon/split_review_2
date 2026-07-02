---
job_id: 7a50f73d-b339-48f2-81aa-320786eb51f7
agent_id: ICLR_main_2026_2
status: COMPLETED
filename: OPFE1zPYbU.pdf
paper: Rethinking Diffusion Model in High Dimension
main_score_norm: 0.2
desk_reject: false
---
# Desk Rejection Assessment:
## Paper Length
Pass ✅.

## Topic Compatibility
Pass ✅. The paper is clearly about generative models, probabilistic methods, and representation learning, all of which are within ICLR scope.

## Minimum Quality
Pass ✅. The paper has the essential structure and enough technical and empirical content to merit full review, although there are substantial concerns about correctness, evidential support, and positioning that affect the final recommendation rather than triggering desk rejection.

## Prompt Injection and Hidden Manipulation Detection
Pass ✅. I did not find hidden prompts, manipulative instructions to automated reviewers, or other signs of prompt injection in the provided paper content.

# Expected Review Outcome:
## Summary
This paper argues that in high-dimensional sparse settings, the effective target of diffusion-model training collapses from a weighted average over many possible clean samples to a single nearest sample, a phenomenon the authors call "weighted sum degradation." Building on this claim, the paper proposes a reinterpretation of diffusion training as predicting \(x_0\) via frequency-dependent completion, and introduces a "Natural Inference" framework that rewrites a broad family of samplers, including DDPM, DDIM, Euler, DPM-Solver, DPM-Solver++, DEIS, and flow-matching solvers, as iterative combinations of predicted \(x_0\) terms and noise terms.

## Strengths
1. The paper tackles an important and genuinely interesting question, namely why diffusion models work well in very high-dimensional spaces despite the usual intuition about sparsity and the curse of dimensionality. Even though I am not convinced by the paper's strongest conclusions, the central question is relevant to the ICLR community.

2. The observation in Section 3 that the posterior over training examples can become highly concentrated at low noise levels is intuitively meaningful, and the paper makes this concrete through a simple empirical statistic. In particular, **Tables 1 and 2 on Page 5** do show a clear pattern that posterior mass concentration is much stronger at smaller \(t\), and that the effect is more pronounced for flow matching than VP under the paper's chosen criterion. That part is useful as a descriptive phenomenon, even if the paper overinterprets it.

3. The paper does a decent job of exposing a common algebraic structure across many samplers. The recursive form in **Equations (17)-(18) on Page 8** is a helpful abstraction: many practical samplers can indeed be written as repeated affine updates using the current state, a model prediction, and sometimes fresh Gaussian noise. This re-expression may be pedagogically useful.

4. Some figures help communicate intuition. For example, **Figure 1 on Page 5** makes the concentration story visually accessible by showing how a small-noise neighborhood around \(\mu\) can isolate a single nearby training point in a sparse space. Likewise, **Figure 5 on Page 7** gives a compact schematic of the proposed Natural Inference framework, and is one of the clearer parts of the paper conceptually.

5. The frequency-domain discussion in **Figures 2-4 on Pages 5-6** is intuitive and may resonate with how many practitioners already think about denoising, namely coarse structure appearing early and details later. I do not think this rises to a scientific explanation of diffusion, but it is at least a plausible informal picture.

## Weaknesses
1. **The paper's main conceptual leap is not justified: posterior concentration does not imply that diffusion models "do not learn statistical quantities."**  
   The strongest claims in the abstract, introduction, and conclusion are much broader than what the analysis actually establishes. The paper shows, at best, that for an empirical distribution over finitely many training samples and for sufficiently small noise, the posterior over those samples may be sharply concentrated. But from this it concludes that the model therefore "cannot effectively learn" posterior, score, or velocity field, and that diffusion models "operate via a different mechanism." That is a very large jump. A concentrated posterior is still a posterior. A score field induced by an empirical or smoothed empirical distribution is still a score field. In fact, diffusion training is explicitly defined on noisy marginals, not on exact recovery of a complicated multimodal posterior at every point. So the paper repeatedly conflates a numerical concentration phenomenon with a conceptual failure of the probabilistic formulation. This issue affects the core claim of the paper and is not a minor wording problem.

2. **The central analysis depends on replacing the data distribution \(p(x_0)\) by an empirical Dirac mixture over dataset samples, which changes the object being analyzed in a way the paper does not adequately discuss.**  
   In **Section 3.1, Equations (13)-(15) on Page 4**, the paper writes \(p(x_0)=\frac{1}{N}\sum_i \delta(x_0-X_0^i)\). Under this model, the posterior over \(x_0\) given \(x_t\) is necessarily a discrete distribution over training examples. Of course this can become concentrated on one atom when noise is low and dimension is high. But diffusion models are usually interpreted as learning a smoothed population distribution, or at minimum a continuous noised distribution \(p_t\), not as literally inferring one of finitely many training examples from a catalog. If the authors want this empirical-distribution substitution to support claims about how diffusion models fundamentally work, they need to explain why it is not merely an artifact of analyzing the finite empirical measure. As written, the analysis feels closer to nearest-neighbor behavior in a finite database than to a refutation of diffusion's statistical interpretation.

3. **The argument that all diffusion objectives reduce to "predicting the mean of \(p(x_0|x_t)\)" is incomplete and in places mathematically loose.**  
   The derivations in **Section 2, Equations (3)-(12), Pages 2-3** are not all equally clean. For DDPM-like models, the relationship between posterior mean parameterization and \(x_0\)-prediction is standard and mostly fine. For score matching, **Equations (7)-(9)** do express the score as a posterior average of conditional scores, but the subsequent claim that the objective "can also be considered as learning the mean of \(p(x_0|x_t)\)" elides the scaling and parameterization details. For flow matching, **Equation (12)** is particularly troubling: \(u(x_t)=\varepsilon - \int p(x_0|x_t)x_0\,dx_0\) treats \(\varepsilon\) as though it were a well-defined function of \(x_t\) independent of the conditioning subtleties. But under the coupling \(x_t=(1-\sigma_t)x_0+\sigma_t\varepsilon\), once conditioning on \(x_t\), the residual noise is not just a free constant sitting outside the posterior integral in the way written. This matters because the paper repeatedly uses these equations to justify the claim that all formulations are really just \(x_0\)-prediction in disguise.

4. **Several mathematical statements are presented as stronger than warranted, and the exposition around them is too casual for a theory-heavy paper.**  
   A concrete example is **Equation (13) on Page 4**, which writes
   \[
   p(x_0|x_t)=\mathrm{Normalize}\left(\exp\left(-\frac{(x_0-\mu)^2}{2\sigma^2}\right)p(x_0)\right).
   \]
   In high dimension, this should be expressed with vector norms, e.g.
   \[
   p(x_0|x_t)\propto \exp\left(-\frac{\|x_0-\mu\|_2^2}{2\sigma^2}\right)p(x_0),
   \]
   together with a clear statement of the isotropic Gaussian assumption and ambient dimension. As written, the notation oscillates between scalar and vector interpretations throughout the paper, which is not harmless because the entire argument is explicitly about high-dimensional geometry. Similarly, the threshold-based degradation definition in Section 3.2 uses \(p(x_0=X_0' \mid x_t=X_t)>0.9\), but the exact computation procedure, candidate set, and dependence on dataset size are underspecified in the main paper. Since the headline empirical claim hinges on this statistic, the mathematical object needs to be defined much more carefully.

5. **The empirical evidence in Section 3 is too narrow to support the paper's sweeping claims.**  
   The only quantitative evidence in the main paper is the degradation statistic on latent ImageNet-256 and ImageNet-512 in **Tables 1 and 2 on Page 5**. This does not test whether diffusion models fail to learn score fields, posterior means, or velocity fields; it only tests concentration of posterior mass under the authors' empirical-mixture formulation. There is no analysis of actual trained model predictions versus true posterior means on synthetic distributions where the truth is known, no controlled low-dimensional or manifold-based counterexamples, no measurement of approximation error induced by replacing a weighted sum by a single sample, and no evidence that this alleged degradation is causally related to sample quality. The paper asks a major scientific question, but the experiments are not designed to answer it.

6. **The "Natural Inference" framework is largely a reparameterization of existing samplers, and the paper does not demonstrate scientific or practical value beyond this algebraic rewriting.**  
   Section 4 shows that many samplers can be expanded into linear combinations of previous \(x_0\)-predictions and Gaussian noise terms. Fine, but that is not yet a new inference principle. **Figure 5 on Page 7** visualizes this decomposition nicely, and **Figures 7-14 in the appendix pages 16-19** show that the equivalent signal/noise coefficients approximately match marginal coefficients for various methods. However, this mostly confirms that these samplers preserve the intended signal-noise schedule, which is already built into their design. The paper does not show that Natural Inference yields a new algorithm, a better sampler, improved debugging, improved interpretability, or any new theorem. Without such evidence, the contribution feels descriptive rather than scientific.

7. **The "self guidance" notion is too broad to be meaningful as presented.**  
   In **Section 4.1, Equations (16), (44)-(51), Pages 6-7 and 14**, the paper defines Self Guidance as essentially any affine combination of two outputs, and then further states that any linear combination of multiple outputs can be viewed as compositions of Self Guidance. This is mathematically true in a trivial sense, but scientifically weak: if any linear combination qualifies, then the concept risks becoming a relabeling device rather than a mechanism. The qualitative examples in **Figure 6 on Page 14** show that different interpolation/extrapolation choices produce sharper or worse images, but that does not establish that self-guidance is a principled explanation of actual diffusion samplers.

8. **The frequency-spectrum explanation is plausible as intuition, but it is not validated and is overstated as an explanation of the training objective.**  
   **Figures 2, 3, and 4 on Pages 5-6** are visually intuitive, especially the contrast between natural-image spectra and white noise spectra. But the step from "natural images have low-frequency-heavy spectra" to "therefore the diffusion objective should be understood as filtering and then completing frequencies" is not actually established. There is no quantitative experiment measuring frequency-wise prediction error over time, no comparison across datasets with different spectral structure, and no demonstration that this view predicts anything nontrivial about model behavior. This section reads more like an informal blog-style interpretation than evidence for the paper's core thesis.

9. **The paper is insufficiently positioned relative to recent theory on diffusion in high dimensions and on low-dimensional structure.**  
   For a paper whose main message is that the standard probabilistic interpretation breaks down in high dimension, the literature discussion is surprisingly thin. The introduction cites classic diffusion and flow-matching papers, but the paper does not seriously engage with recent theoretical work arguing that diffusion can avoid ambient-dimensional curse-of-dimensionality effects under manifold, low-rank, or other structured assumptions. This omission matters because the paper frames its result as a fundamental contradiction with "conventional understandings," when in fact the modern theory landscape is more nuanced. The lack of careful positioning makes the claims appear broader than they are.

10. **Presentation is uneven, and some parts are much less precise than they need to be.**  
   The paper has a bold narrative, but clarity suffers in several places. Some terminology is introduced informally and then treated as if formal, such as "degradation," "information enhancement operator," and "natural inference." Section transitions often state conclusions before proving them. The paper also tends to overclaim, for example "first rigorous analysis" in the contributions on **Page 2**, while the actual analysis is neither comprehensive nor fully rigorous. This overstatement interacts badly with the already limited evidence.

11. **There is no direct evaluation of whether the proposed perspective improves anything.**  
   If the paper wants to sell Natural Inference as more than a pedagogical rewrite, it should provide at least one concrete downstream payoff: a better sampler, a better schedule, an improved guidance mechanism, a debugging case study, or even a diagnostic that correlates with sample quality. The paper's own **Section 4.4 on Pages 8-9** lists potential advantages, but these remain speculative. As it stands, the work asks the community to adopt a new conceptual framework without demonstrating clear gains.

## Questions
1. The paper's strongest claim is that weighted-sum degradation prevents the model from learning score, posterior, or velocity-field quantities. Can the authors provide a controlled synthetic experiment where the true posterior mean or score is analytically available, and then directly measure whether trained diffusion models track that true quantity poorly precisely in the regime where degradation is high? This would substantially strengthen the core argument.

2. In **Equation (12)**, what is the exact conditioning structure under which
   \[
   u(x_t)=\varepsilon-\int p(x_0|x_t)x_0\,dx_0
   \]
   is valid? Please rewrite this derivation carefully, because as written it appears to treat \(\varepsilon\) as independent of the posterior over \(x_0\) after conditioning on \(x_t\), which is not obvious.

3. The main empirical statistic uses the criterion \(p(x_0=X_0' \mid x_t=X_t)>0.9\). How exactly is this posterior computed in the main paper experiments? Over the full dataset, over a minibatch, or over a subsample? Since the posterior mass over an empirical mixture is sensitive to the support size, this choice matters a lot.

4. The analysis relies on treating \(p(x_0)\) as an empirical mixture of deltas on dataset points. Can the authors explain why the resulting conclusions should transfer to the continuous population distribution that diffusion models are usually interpreted as approximating? A rebuttal that carefully distinguishes "finite dataset posterior concentration" from "failure of probabilistic learning" would be useful.

5. Can the authors provide one concrete result, qualitative or quantitative, showing that the Natural Inference perspective leads to a better design choice than existing formulations? For example, does it suggest a new coefficient pattern, guidance policy, or schedule that improves FID or sample efficiency?

6. Regarding **Tables 1 and 2**, could the authors report sensitivity to the degradation threshold (e.g., 0.7, 0.8, 0.95), the latent dimensionality, and dataset size? Right now it is hard to know whether the reported effect is robust or partly an artifact of the chosen cutoff.

7. The paper repeatedly interprets the objective through frequency filtering. Can the authors add a quantitative plot of frequency-wise reconstruction error as a function of \(t\), to validate the story behind **Figures 2-4**?

## Flag For Ethics Review
- No ethics review needed.

## Details Of Ethics Concerns
No specific ethics concerns arise from the main paper. The work is a conceptual and methodological critique of diffusion-model training and sampling rather than a dataset or deployment paper.

## Soundness Rating
2: fair. The paper raises an interesting phenomenon and contains some correct algebraic reformulations, but the central scientific claims are not adequately supported and some mathematical steps are too loose for the strength of the conclusions.

## Presentation Rating
2: fair. The paper is readable and has helpful diagrams, but the exposition is imprecise in important places, terminology is informal, and the narrative substantially overstates what the evidence shows.

## Contribution Rating
1: poor. The descriptive posterior-concentration observation is interesting, but the paper does not convincingly establish its claimed implications, and the proposed inference framework is mostly a reformulation without demonstrated new capability or insight of sufficient scientific depth.

## Overall Rating
2: Reject, not good enough. The paper asks an important question and contains a potentially useful descriptive observation about posterior concentration in high-dimensional empirical datasets, but the main claims are significantly overstated, the theoretical argument is not rigorous enough to support the proposed reinterpretation of diffusion models, and the empirical evidence is too limited to justify such broad conclusions.

## Reviewer Confidence
4: confident. I am confident in the overall negative assessment, though some appendical derivations and implementation details could still be clarified in rebuttal.