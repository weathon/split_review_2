## Summary
# Final Review Report

## Summary

This paper introduces **Marginal Flow**, a density estimation framework that approximates a target distribution by marginalizing latent parameters $\mathbf{w}$ sampled from a learnable distribution $q_\theta(\mathbf{w})$. The core idea is to replace the standard approach of optimizing fixed mixture components with a procedure that resamples parameters $\mathbf{w}$ at each iteration from $q_\theta(\mathbf{w})$, which in turn is parameterized by an unconstrained neural network $f_\theta$ applied to a base distribution $p_{\text{base}}(\mathbf{z})$. This yields a model that simultaneously supports exact density evaluation (via Monte Carlo averaging over resampled $\mathbf{w}$) and efficient single-step sampling.

The key claimed advantages over existing density estimation models are: (1) exact density evaluation without requiring bijective architectures or Jacobian determinants; (2) efficient training and inference across dimensionalities; (3) native support for lower-dimensional manifold learning; (4) flexibility in choice of the parametric family $q(\mathbf{x}|\mathbf{w})$; and (5) compatibility with multiple training objectives (forward and reverse KL).

Empirical validation is provided across several settings: 2D synthetic density estimation (log-likelihood and reverse KL), simulation-based inference on the SBI benchmark, Wishart mixture distributions on positive-definite matrices, and conditional manifold learning in VAE latent spaces for MNIST and JAFFE face datasets. The paper reports orders-of-magnitude runtime improvements over Normalizing Flows, Flow Matching, and Free-form Flows for high-dimensional inference, and faster convergence on synthetic benchmarks.

**Overall assessment:** Marginal Flow presents a genuinely novel and conceptually clean approach to density estimation that breaks away from the prevailing bijection-based and diffusion-based paradigms. The core idea — marginalizing resampled latent parameters through a learnable distribution — is elegant and leads to a model with an attractive combination of properties (exact likelihood + efficient sampling + architectural freedom). However, the manuscript in its current form has several significant weaknesses: (a) overclaiming in the abstract and contribution statements that is not fully supported by the evidence; (b) missing discussion of the Monte Carlo variance-quality trade-off that governs the method's practical behavior; (c) evaluation gaps including absent training-time benchmarks beyond 2D synthetic data and unquantified manifold reconstruction metrics; (d) lack of a limitations paragraph; and (e) a related-work section that catalogs rather than analytically compares. With substantial revisions to bound claims, add missing analyses, and improve narrative structure, this work has the potential to be a strong contribution.

## Strengths
**1. Conceptually novel and technically clean framework.**
The core idea behind Marginal Flow — marginalizing over resampled latent parameters $\mathbf{w}$ drawn from a learnable distribution $q_\theta(\mathbf{w})$ — is genuinely different from existing paradigms (bijective flows, diffusion, adversarial training). The formulation is elegant: it converts density estimation into learning a distribution over mixture component parameters, where the Monte Carlo approximation to marginalization allows the model capacity to scale with the neural network $f_\theta$ rather than the number of components $N_c$. This conceptual simplicity is a genuine strength.

**2. Attractive combination of properties.**
Marginal Flow simultaneously achieves exact density evaluation (unlike GANs, VAEs, diffusion models, and EBMs), efficient single-step sampling (unlike diffusion and flow matching), no architectural constraints (unlike Normalizing Flows), and native manifold learning (unlike NF, FM, and diffusion). Table 1 effectively summarizes this unique combination. While each individual property exists in some prior model, bundling all five in a single framework with a unified learning principle is a meaningful advance.

**3. Strong runtime performance at high dimensionality.**
Figure 3 demonstrates orders-of-magnitude speedups for sampling and density evaluation at high dimensions ($d=10^2$ to $10^5$) compared to Normalizing Flows, Flow Matching, and Free-form Flows. This is a practically relevant advantage: many real-world density estimation tasks (in simulation-based inference, computational physics, and Bayesian inverse problems) involve high-dimensional parameter spaces where existing methods become computationally prohibitive.

**4. Flexible parametric family.**
The ability to swap $q(\mathbf{x}|\mathbf{w})$ to match the data domain (Gaussian for Euclidean data, Wishart for positive-definite matrices, Dirichlet for simplex data) without changing the learning framework is an elegant design choice. The Wishart mixture demonstration (Section 4.3) effectively showcases this flexibility on a non-trivial data type.

**5. Training objective versatility.**
Because Marginal Flow is efficient at both sampling and density evaluation, it can be trained with forward KL, reverse KL, or combined objectives. The reverse KL demonstration (Figure 8) is particularly notable because most modern generative models (diffusion, flow matching, GANs) cannot efficiently compute the log-likelihood required for reverse KL training. This opens up applications in scientific settings where the target density is known only up to a normalizing constant.

**6. Promising qualitative results on low-data manifold learning.**
The 1D conditional manifold experiments on MNIST and JAFFE (Section 4.4) produce visually interpretable latent traversals — digits smoothly varying from bold to italic to normal, and faces interpolating identity while preserving emotion. Given the extreme low-data regime of the JAFFE dataset (214 images), the fact that Marginal Flow produces structured manifolds is encouraging and suggests practical utility in data-scarce scientific domains.

## Weaknesses
### W1. Overclaiming in abstract and contribution statements (Severity: Major, Fixable)
The abstract states that Marginal Flow "overcomes these limitations altogether" — an absolute claim that no practical model can satisfy, as every framework has trade-offs in different regimes. Similarly, "orders of magnitude faster than competing models both at training and inference" is asserted in the abstract and contribution list, but the empirical support (Figure 3) only covers inference (sampling and density evaluation) at high dimensions, not training. The training-time evidence is limited to 2D synthetic convergence curves (Figure 7). These overstatements undermine scientific credibility and are likely to attract reviewer criticism.

**Fix:** Replace absolute language with bounded claims. Specify the conditions under which runtime advantages hold (high-dimensional inference). Distinguish training-time evidence (2D synthetic) from inference evidence (high-dimensional scaling). See annotation ID `0704c983` for a full Mentor Revised Version of the abstract.

### W2. Missing analysis of Monte Carlo variance-quality trade-off (Severity: Major, Fixable)
The model definition (Eq. 2) uses a finite-$N_c$ Monte Carlo approximation to the marginal in Eq. 1. The paper states that "modeling capacity is not directly linked to $N_c$ anymore," but this is only true in the $N_c \to \infty$ limit. With finite $N_c$, the density estimate has variance proportional to $\text{Var}_{q_\theta(\mathbf{w})}[q(\mathbf{x}|\mathbf{w})]/N_c$. The paper provides no analysis of how $N_c$ should be chosen, how it interacts with data dimensionality, or what the variance-induced error in the density estimate is. Moreover, no guidance is offered on whether $N_c$ is a fixed hyperparameter or can be adapted during training.

**Impact:** Without this analysis, readers cannot assess whether the reported results depend on a favorable choice of $N_c$, or whether the method degrades gracefully in settings where $N_c$ must be small due to computational constraints.

**Fix:** Add a paragraph in Section 2.1 analyzing the $N_c$ dependence, including a practical heuristic for choosing $N_c$ and the variance-scaling behavior. Report the $N_c$ values used in all experiments. See annotation ID `31c304ad` for detailed guidance.

### W3. Insufficient training-time benchmarking (Severity: Major, Fixable)
The runtime advantage claim ("orders of magnitude faster") is supported primarily by Figure 3, which measures inference (sampling and density evaluation) across dimensions $10^2$-$10^5$. The only training-time comparison is Figure 7, which shows log-likelihood as a function of runtime for 2D synthetic datasets. No training runtime comparison is provided for higher-dimensional settings (Wishart matrices, VAE latent spaces). This means the claim of faster *training* is not empirically supported beyond low-dimensional toy data.

**Fix:** Either (a) add training runtime comparisons for at least one non-synthetic setting (e.g., Wishart $10\times10$ or MNIST VAE training), or (b) explicitly separate the claim into "faster inference (orders of magnitude)" and "competitive or faster training (demonstrated on 2D benchmarks, pending further validation)". See annotation ID `3c27aa26`.

### W4. Related Work is catalog-style rather than analytical (Severity: Major, Fixable)
The Related Work section (Section 3) presents three paragraphs that each summarize a model family (EB/diffusion, VAE/GAN, NF/FM) without analyzing them along decision-relevant axes. It does not explicitly state how Marginal Flow differs from the closest baselines (Free-form Flows for architectural freedom, Normalizing Flows for exact likelihood, Flow Matching for high-dimensional scaling). Table 1 in the Introduction provides a feature matrix, but the Related Work section does not reference or elaborate on it. The section reads as a descriptive survey rather than a positioning argument that clarifies the paper's novelty.

**Fix:** Restructure around 3-4 comparison axes (exact likelihood, sampling efficiency, architectural constraints, manifold support). For each axis, position 2-3 representative models and state where Marginal Flow differs. Reduce the paper-by-paper summary tone. See annotation ID `6c883144` for a rewritten structure.

### W5. Missing limitations paragraph (Severity: Major, Fixable)
The Conclusion (Section 5) recaps achievements without mentioning any limitations, boundary conditions, or failure modes. For a methods paper that claims broad advantages over multiple model families, the absence of critical self-assessment is a serious omission. No discussion appears on: finite-$N_c$ variance, scaling to extremely high-dimensional data spaces, conditions under which the method might underperform, or theoretical guarantees.

**Impact:** This omission reduces the paper's scientific credibility and signals insufficient critical reflection. Reviewers frequently cite lack of limitations as a reason for rejection.

**Fix:** Add a limitations paragraph covering finite-$N_c$ effects, the linear cost scaling with $N_c$, the dependence of manifold quality on $f_\theta$ smoothness, and the absence of theoretical approximation guarantees. See annotation ID `eebe684a` for a complete Mentor Revised Version.

### W6. SBI results claim "state-of-the-art" with only deferred evidence (Severity: Major, Fixable)
Section 4.2 states that "Marginal Flow achieves state-of-the-art results" on the SBI benchmark, but provides no quantitative results in the main text. The claim relies entirely on Appendix Figure 14, which is not included in the provided manuscript. The evaluation metric (C2ST) is mentioned but no numerical values, baseline comparisons, or task definitions are presented in the main body. This makes the claim unverifiable from the main text alone.

**Fix:** Add a compact summary table with C2ST scores for Marginal Flow vs. at least 2-3 SBI baselines across the benchmark tasks. If space is constrained, provide the top-2 most informative comparisons in the main text. Bound the claim to "competitive or superior on several SBI tasks." See annotation ID `7aa46c77`.

### W7. Manifold reconstruction evaluation uses PCA projection without quantitative metrics (Severity: Major, Fixable)
The Wishart experiment (Section 4.3) evaluates manifold recovery purely through PCA projections to 2D. PCA is a linear method: if the true manifold $\mathcal{M}$ is nonlinear in the matrix space, PCA can distort distances and produce a misleading visual impression. No quantitative manifold reconstruction metric (e.g., reconstruction error, Chamfer distance) is reported. The claim that Marginal Flow "perfectly recovers the manifold" is therefore not supported by the presented evidence.

**Fix:** Report at least one quantitative metric for manifold reconstruction in the original space. For the $100\times100$ case where NF cannot be trained, compare against a practical baseline (e.g., PCA-based reconstruction or VAE-based manifold learning). See annotation ID `79fbef7f`.

### W8. VAE latent-space experiments lack quantitative validation (Severity: Minor, Nice-to-have)
The MNIST and JAFFE manifold experiments (Section 4.4) are qualitatively compelling but lack any quantitative evaluation. The "disentanglement" claim is based on visual inspection alone. VAE reconstruction quality is not reported, and no baseline comparison is provided (e.g., linear interpolation in VAE space, or a conditional VAE).

**Fix:** Report VAE reconstruction error, add a simple baseline comparison, and compute a quantitative disentanglement metric. See annotation ID `6ec2d8f4`.

### W9. Introduction narrative structure weakens motivation (Severity: Minor, Fixable)
The first two introductory paragraphs read as a list of application areas (image generation, text-to-audio, protein folding, cosmology, neuroscience) without establishing a clear research gap. The reader must wait until the third paragraph and the Contribution section to understand what problem the paper solves. This reduces narrative engagement.

**Fix:** Restructure the introduction to open with a concise statement of the core trade-off in density estimation, then discuss applications as context for why the trade-off matters. See annotations `068477a2`, `d1dc487e`, and `b2a5f797` for paragraph-level revisions.

### W10. Multi-modal demonstration lacks quantitative evidence (Severity: Minor, Nice-to-have)
Figure 5 convincingly shows Marginal Flow capturing 5 modes where baselines collapse or blur. However, the comparison is purely visual — no negative log-likelihood, KL divergence, or mode-coverage metric is reported. With only 150 training points, it is unclear whether the advantage persists at larger sample sizes.

**Fix:** Add a quantitative metric (e.g., per-mode KL divergence) and test at least one additional sample size. See annotation ID `7685117e`.

## Score
**Final Score: 6/10**

**Rationale:** The score prioritizes novelty and research value as the primary dimensions, as required by the scoring policy. The core idea (marginalizing over resampled latent parameters via a learnable distribution) is conceptually novel and technically clean, representing a genuine departure from existing density estimation paradigms. The framework's combination of exact likelihood, efficient sampling, architectural freedom, and manifold support is practically valuable and not simultaneously achieved by any prior single model to the best of available knowledge.

However, the manuscript in its current form is weakened by significant overclaiming (abstract and contribution statements that outstrip the presented evidence), missing technical analysis (the $N_c$ variance-quality trade-off is unexamined), evaluation gaps (training-time benchmarking is limited to 2D synthetic data; manifold reconstruction quality is unquantified), and the absence of a limitations paragraph. These issues are fixable but reduce confidence in the paper's claims as written.

The novelty verdict cannot be fully verified due to Retrieval-Disabled Mode in this review (external literature search unavailable). Based on internal evidence, the marginalization-resampling principle appears genuinely novel within the density estimation literature, but comparisons against the closest methods (e.g., Free-form Flows, manifold-capable flows) should be strengthened by the authors through explicit mechanism-level differentiation.

A revised version addressing the major weaknesses (overclaim bounding, $N_c$ analysis, training benchmarks, limitations paragraph, restructured related work) would likely merit a score of 7-8/10.