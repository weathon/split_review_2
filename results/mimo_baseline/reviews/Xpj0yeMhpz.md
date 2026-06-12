## Summary

This paper introduces a new problem formulation for machine unlearning by decoupling the class label from the target concept to forget. It systematically identifies three unexplored settings beyond conventional class-wise unlearning—target mismatch, model mismatch, and data mismatch—and proposes TARF, a three-phase framework combining annealed gradient ascent with target-aware retaining to handle these scenarios. The method is validated across CIFAR-10/100, TinyImageNet, ImageNet, and applied to diffusion model concept removal and LLM unlearning.

## Strengths

- **Genuinely important problem formulation.** The paper clearly articulates a real gap: previous class-wise unlearning assumes class labels coincide with target concepts, but practical requests (privacy, fairness, copyright) often don't. The four-task taxonomy (all-matched, target mismatch, model mismatch, data mismatch) is well-motivated with concrete examples and Figure 1 illustrations. This reframing is the paper's strongest conceptual contribution.

- **Rigorous empirical evaluation across diverse settings.** The experiments span CIFAR-10, CIFAR-100, TinyImageNet, and ImageNet-1k (Table 3, 4), plus real-world applications on Stable Diffusion concept removal (Figure 6) and LLM unlearning on TOFU (Table 5). The consistent advantage of TARF across mismatch settings is compelling: in target mismatch on CIFAR-100, TARF achieves Gap=0.21 versus the next-best GA at 8.86, and in data mismatch it achieves Gap=0.96 versus the next-best IU at 0.44 on CIFAR-10. The method also performs competitively in the conventional all-matched setting (Gap=1.01 on CIFAR-10), demonstrating it doesn't sacrifice standard performance.

- **Well-integrated framework design.** The three phases (target identification, target separation, retraining approximation) are organically connected through the unified objective in Eq. 3, rather than being an ad-hoc pipeline. The annealing schedule $k(t)$ and the dynamic indicator $\tau(x,y,t)$ cleanly control the transitions. Figure 4 provides a clear conceptual overview of how these phases address the identified challenges.

- **Useful representation-level analysis.** Theorem 3.2 and the "representation gravity" concept (Definition 3.3) provide meaningful intuition about why mismatched settings are hard: when representations are under-entangled (target/data mismatch), forgetting data cannot govern the whole concept; when over-entangled (model mismatch), forgetting spills over to other data. The empirical verification in Figure 3 effectively supports this analysis.

## Weaknesses

### Fatal

None.

### Major

- **Limited theoretical depth.** Theorem 3.2 provides a useful intuition about representation distance and forgetting dynamics, but the formal contribution is relatively thin. The proof (deferred to Appendix) bounds a loss difference term under Lipschitz smoothness, which is a standard technique. The paper relies more on the empirical observations (Figures 2, 3, 9) than on rigorous theoretical guarantees about when and why TARF succeeds. A stronger theoretical characterization—e.g., conditions under which target identification succeeds or fails, convergence guarantees for the three-phase process—would significantly strengthen the paper.

- **Hyperparameter sensitivity and selection process.** The method requires several hand-tuned parameters: forgetting strength $k$, threshold $\beta$, start/end times $t_1$ and $t_0$, and the annealing schedule. While Appendix E discusses guidelines, the main paper doesn't provide clear practical guidance for choosing these in novel settings. The threshold $\beta$ selection (top-10% in a descending order) is particularly ad hoc and may not transfer across domains or concept types. For a method targeting practical unlearning, this sensitivity is a meaningful limitation.

### Minor

- **Superclass labels as proxy for concepts.** The paper uses CIFAR-10/100 superclass groupings (Tables 13-15 in appendix) to instantiate the mismatch scenarios. While this is a reasonable first step, these superclass labels are themselves somewhat subjective and may not fully capture the complexity of real-world concept hierarchies. The paper partially addresses this with ImageNet and LLM experiments, but the core analysis relies heavily on the CIFAR superclass structure.

- **Some experimental results appear less decisive.** In the model mismatch setting on CIFAR-100, TARF achieves Gap=1.21 which is strong, but the fine-grained Table 2 shows the "Retrained" reference achieving Gap=3.42 in the CIFAR-100 model mismatch case, while TARF achieves 1.36—this is better but the comparison structure in Table 2 is somewhat confusing as it mixes different unlearning configurations.

- **The gravity-based identification assumes structured data.** The target identification phase relies on class-level accuracy drops, requiring class label availability and that the target concept spans identifiable class boundaries. In truly fine-grained or continuous concept settings, this class-level granularity may be insufficient.

### Trivial

None.

## Nice-to-Haves

- A discussion of failure modes: when would TARF's representation gravity approach fail (e.g., adversarial data distributions, concept distributions that are genuinely entangled at the representation level)?
- Comparison with concept erasure methods from the generative model literature (e.g., Erased Stable Diffusion, concept editing methods) in the diffusion model experiments for more complete positioning.
- Analysis of how TARF scales with the number of target classes and the granularity of the concept hierarchy.

## Novel Insights

The paper's key novel insight is the "representation gravity" effect in unlearning dynamics: when performing gradient ascent to forget data, the degree of collateral damage (or collateral forgetting) on nearby data is proportional to their representation distance. This insight directly motivates the method design—the gravity effect can be exploited to *identify* false retaining data (data that belong to the target concept but weren't explicitly provided) and to *separate* entangled features through simultaneous gradient ascent and descent. This is a genuine contribution to understanding unlearning dynamics beyond the conventional matched setting.

## Suggestions

- Provide a more principled procedure for selecting $\beta$ and the timing parameters $t_0, t_1$, ideally with theoretical or empirical justification for specific ranges.
- Consider adding a small validation study where users annotate concepts differently from class labels (even if on a small scale) to validate that the superclass proxy is reasonable.
- Include a sensitivity analysis figure showing TARF's performance as a function of each hyperparameter across multiple settings, which would greatly aid practitioners.

## Score and Decision

The paper makes a genuine contribution by identifying and formalizing an important gap in machine unlearning research—the mismatch between class labels and target concepts. The problem formulation is novel and practically motivated, the representation gravity analysis provides useful insights, and TARF performs convincingly across multiple benchmarks and applications. However, the theoretical contribution is limited, and the method, while effective, is built from relatively straightforward components (annealed gradient descent, threshold-based selection). The overall contribution is solid but falls in the moderate novelty range—stronger than incremental but not transformative. Given the ICLR 2026 distribution (14.9% at score 6), this paper's quality aligns well with a borderline-accept score.

MY FINAL SCORE: <score>6.0</score>
MY FINAL DECISION: <decision>Accept</decision>