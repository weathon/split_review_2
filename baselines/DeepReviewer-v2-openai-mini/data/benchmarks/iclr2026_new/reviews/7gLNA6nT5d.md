## Summary
This paper proposes integrating n-gram induction heads — a hardcoded attention mechanism that identifies repeating n-gram patterns in sequences — into transformers for in-context reinforcement learning (ICRL). The method builds on Algorithm Distillation (AD) and addresses two key limitations: the large data requirement and training instability of existing ICRL approaches. The authors introduce an N-Gram Layer (NGL) as a drop-in component derived from prior work by Akyürek et al. [2], adapted for RL observation spaces including discrete states and pixel-based images (via Vector Quantization). Experiments on Dark Room, Key-to-Door (grid-world), and Miniworld (3D visual) environments show that the n-gram augmented model requires substantially fewer hyperparameter search trials, achieves better data efficiency (up to 27x reduction in training goals on Key-to-Door), and extends to visual observations through VQ preprocessing. The paper also includes ablation studies showing that n-gram length and layer position have limited impact on performance, and that a permuted n-gram mask does not degrade the baseline.

**Overall assessment:** The paper tackles a relevant problem — making ICRL training more practical — and the core idea (adding n-gram inductive bias to reduce simplicity bias) is well-motivated. However, several significant methodological and evidential concerns limit the current strength of the claims: (1) The 27x data efficiency claim conflates different data dimensions and relies on an apples-to-oranges comparison with AD's original configuration. (2) The evaluation protocol lacks multi-seed variance reporting and statistical significance testing. (3) The VQ-based n-gram matching for visual observations uses an extremely restrictive all-match condition without quality metrics. (4) The data collection procedure (oracle+noise schedule) differs fundamentally from AD's original training-from-scratch approach, creating a potential confound. (5) The n-gram attention formula contains index asymmetry and undefined boundary conditions that affect reproducibility. Due to Retrieval-Disabled Mode, novelty/comparison conclusions are deferred for manual verification.

## Strengths
1. **Well-motivated problem and solution direction.** The paper identifies a genuine bottleneck in ICRL — the data hunger and training instability of methods like AD — and proposes a model-centric intervention (n-gram inductive bias) rather than more complex data augmentation or curation pipelines. This is a sensible direction that targets the root cause (simplicity bias in transformers) rather than symptoms.

2. **Clean integration of existing n-gram layer into ICRL architecture.** The method of hardcoding n-gram attention patterns (from Akyürek et al. [2]) into a transformer-based ICRL model is straightforward and technically sound. The modification is minimally invasive — a single N-Gram Layer inserted among standard transformer layers — which makes the approach easy to adopt and ablate.

3. **Thoughtful evaluation protocol using Expected Maximum Performance (EMP).** Reporting EMP across random hyperparameter searches is a principled way to compare methods on both ease-of-tuning and peak performance simultaneously, avoiding cherry-picking of single best checkpoints. This is an improvement over reporting only best-run results.

4. **Empirical evidence across multiple environment types.** The paper evaluates on three environments covering: (a) discrete grid-world (Dark Room), (b) partially-observed POMDP (Key-to-Door), and (c) pixel-based 3D world (Miniworld). This range provides partial evidence that the benefits of n-gram heads are not limited to a single observation modality.

5. **Helpful ablation studies on n-gram hyperparameters.** Sections 4.4 and 4.5 investigate whether n-gram length and layer position require extensive tuning, and whether a broken n-gram mask degrades performance. These experiments address natural reviewer concerns about the method's overhead and robustness, even though the statistical power is limited.

6. **Honest handling of the 10-goal failure case.** The paper reports (Figure 2 bottom row) that neither method can generalize from only 10 goals. This negative result adds credibility by showing the authors are not selectively reporting only positive outcomes.

## Weaknesses
### W1. Overclaimed and poorly scoped contribution claims (High severity)

The three contribution bullets in the introduction lack necessary scope qualifiers, creating a mismatch between what is claimed and what is actually demonstrated.

- **C1 (27x data reduction):** The 27x figure is derived from a specific comparison where the baseline AD uses 2048 goals + 2048 learning histories [17], while the n-gram method uses 100 training goals with unspecified histories per goal. This conflates "goals" and "transitions" as data dimensions. The paper does not specify the total transition count for either method, making "27x less data" an apples-to-oranges comparison. Furthermore, the 27x factor applies only to the Key-to-Door environment under low task diversity and only to the 'states' matching variant — not to the general method. The paper must provide a side-by-side breakdown of goals, histories per goal, and total transitions for both methods.

- **C2 (hyperparameter sensitivity):** The claim that n-gram heads "help mitigate hyperparameter sensitivity" is supported only by EMP curves showing faster convergence in hyperparameter search. Faster hyperparameter convergence is not the same as reduced sensitivity — sensitivity refers to how much performance varies across different hyperparameter values, which is not directly measured.

- **C3 (visual observations):** The claim about visual observations is supported only on Miniworld (simple 3D grid with 64x64 RGB). The VQ-based matching uses an extremely restrictive all-16-indices-must-match condition, with no quality metrics reported. Generalization to richer visual domains (Atari, DMControl, Habitat) is unvalidated.

### W2. Missing statistical rigor in evaluation protocol (High severity)

- **No multi-seed variance:** The paper does not specify how many independent training seeds are used per hyperparameter configuration. The EMP curves aggregate over random hyperparameter trials, but each trial may use only a single seed. Without multi-seed variance, the observed differences between n-gram and baseline could be driven by seed noise. At minimum, the paper should report: (a) number of seeds per config, (b) whether EMP confidence intervals use bootstrapping, and (c) results of statistical significance tests for headline comparisons (e.g., n-gram vs baseline at the same number of hyperparameter assignments).

- **No parameter count comparison:** The n-gram model adds W1, W2 projection matrices and an MLP to the baseline transformer. The paper does not report total parameter counts for either model. If the n-gram model has substantially more parameters, the improved performance could be partially attributed to increased capacity rather than the n-gram mechanism.

### W3. Data collection confound (High severity)

The data for image-based environments uses an oracle agent with decaying noise schedule (following Zisman et al. [33]), which produces near-optimal trajectories from the start. This fundamentally differs from AD's original approach of training RL algorithms from scratch to generate learning histories. Oracle-generated data may be easier to learn from, potentially inflating the n-gram method's apparent advantage. The paper does not discuss this discrepancy or provide a control experiment with AD-style training-from-scratch data.

### W4. Core n-gram attention formula lacks clarity and completeness (Medium severity)

Equation (1) defining A(n)_ij has an index asymmetry (left side ends at i-1, right side ends at j-2) that is not explained. Boundary conditions for positions i<=n or j<=n+1 are undefined (negative indices x_0, x_{-1}). The mapping from discrete token-level A(n) to embedding-level attention h^l is not specified. These gaps prevent faithful reproduction of the method.

### W5. VQ-based n-gram matching for images is underspecified and brittle (Medium severity)

- The all-16-indices-must-match condition is extremely strict — a single code mismatch breaks the match. No ablation with softer criteria (e.g., match threshold 12/16 or 14/16) is provided.
- VQ reconstruction quality (MSE, perplexity) and codebook usage statistics are not reported.
- The VQ training dataset composition and size are not specified.
- Without these details, readers cannot assess whether the VQ preprocessing preserves state-discriminative information or introduces bottleneck artifacts.

### W6. Underpowered ablation studies (Medium severity)

Sections 4.4 and 4.5 use only 6 random searches total (3 per condition) on a single environment (Miniworld-Dark). Claims of "no significant difference" are unsupported by statistical tests. The permuted mask experiment (Section 4.5) is confounded because the permuted model retains the extra parameters of the N-Gram layer, making it an unfair control for the baseline.

### W7. Related work lacks comparison structure and critical depth (Low-Medium severity)

The Related Work section reads as two independent literature summaries rather than a comparative positioning. The "first to apply" claim at line 117 cannot be verified without external literature search (deferred in this run). The section does not discuss limitations of the n-gram approach or compare the model-centric approach quantitatively with data-centric alternatives.

### W8. Conclusion contains unsupported speculation (Low-Medium severity)

The conclusion introduces a mechanistic speculation about why n-gram heads help (reducing simplicity bias, transitivity of in-context ability) that is not supported by any analysis experiments in the results section. This should be explicitly labeled as hypothesis for future work. The limitations paragraph is too generic and should include experiment-specific boundaries (single-seed protocol, restrictive VQ matching, limited environment scope).

### W9. Writing quality and presentation issues (Low severity)

- Figure descriptions are repeated multiple times (e.g., Figure 1 description appears three times on the same page), likely due to PDF extraction artifacts. Authors should ensure clean figure captions.
- The sentence in Section 4.4 contains a double negative: "no significant difference between neither the n-gram length, nor the position."
- The "transitivity" of in-context ability in Section 6 should read "transience" or "transient nature" to match the cited work [27].

### Novelty & Comparison (Deferred)

Due to Retrieval-Disabled Mode (external paper search unavailable), novelty verification and related-work comparison are deferred for manual verification. The core technical contribution — applying n-gram induction heads from Akyürek et al. [2] to the ICRL setting — is clearly described, but whether concurrent or prior work has already explored this direction cannot be assessed here. The "first to apply in decision-making" claim should be verified against the current literature.

## Score
**Final Score: 5/10**

The paper addresses a relevant problem with a sensible architectural modification, and the experimental results across three environments provide partial support for the claimed benefits. However, the current evidence base has several significant limitations that prevent stronger endorsement: the headline 27x data efficiency claim relies on an incompletely specified comparison; the evaluation protocol lacks multi-seed variance and statistical significance testing; the data collection procedure introduces a potential confound relative to the baseline method; the VQ-based visual extension is underspecified and uses a restrictive matching criterion; and the n-gram attention formula has ambiguities that affect reproducibility. The core idea is promising, but the paper needs substantially stronger empirical validation and more carefully scoped claims before it can be considered publication-ready at a top venue. Novelty must be manually verified against the literature due to the absence of external retrieval in this run.