## Summary
The paper proposes **MoRE (Mixture of Remapping Experts)**, a training‑free framework for feature‑level machine unlearning. MoRE introduces prototype‑orthogonal projection to decorrelate forget and remain prototypes before erasure, then uses a mixture of “remapping experts” to scatter forget features into the remain distribution, making them indistinguishable at the feature level. The method is efficient (single forward pass, linear time, constant memory w.r.t. number of classes) and demonstrates strong empirical results on CIFAR‑10/100, Tiny‑ImageNet, ImageNet, and even concept unlearning in diffusion models.

## Strengths
- **Novel approach to feature‑level unlearning.** The idea of using prototype‑orthogonal projection followed by remapping with multiple experts is creative and addresses a clear limitation of existing erasure‑based methods (ESC), which leave forget features cohesive and separable.
- **Impressive empirical performance.** MoRE consistently achieves near‑perfect HM and KR scores across multiple datasets and architectures, often outperforming training‑based baselines while being orders of magnitude cheaper. The diffusion model results are also competitive.
- **Scalability and efficiency.** The method is training‑free, requires only a single forward pass and lightweight linear algebra, and shows very low GPU memory and time consumption. This makes it practical for large models and datasets.
- **Clear motivation and ablation studies.** The paper motivates the need for orthogonal projection with concrete cosine‑similarity evidence (Fig. 3) and provides ablations that separately demonstrate the effects of PO projection, erasing, remapping, and multiple experts.

## Weaknesses
### Fatal
- **The base feature extractor is never modified.** MoRE adds a projection/remapping layer on top of the unchanged original feature extractor. The paper claims “irreversible feature‑level unlearning,” but an adversary who has white‑box access to the unlearned model can simply discard the MoRE layer and use the original feature extractor directly (together with the original classification head or a new head) to recover full forget performance. The paper never tests this “layer‑removal” attack, nor does it discuss the threat model under which such an attack is possible. Without modifying the underlying model weights, the unlearning is not truly irreversible – it is a post‑processing filter that can be bypassed. This undermines the core claim of the paper.

### Major
- **Overclaim on “irreversibility.”** Even within the deployed model (with MoRE attached), the paper shows that fine‑tuning does not recover forget accuracy, but this is only tested under a specific setting. The possibility of more sophisticated recovery (e.g., meta‑learning, adversarial probing, or simply training a new head on the remapped features to invert the mapping) is not explored. The term “irreversible” is used too strongly.
- **Lack of clarity on threat model.** The paper does not specify whether the adversary has black‑box or white‑box access to the model, whether the base model weights are considered publicly known, or whether the MoRE layer is considered part of the released model. These distinctions are essential for evaluating the security guarantees.
- **Diffusion model experiments are preliminary.** The adaptation to cross‑attention layers is described only briefly, the prototype construction from tokenized prompts is not detailed, and no architecture‑specific tuning or ablation is provided. While the results are good, the treatment is too shallow to be fully convincing as a general method for generative models.

### Minor
- **KR metric may favor the proposed method.** The KR metric uses linear probing to measure feature‑level retention. MoRE is specifically designed to make linear probing fail, so its advantage on KR is partly by construction. The paper would benefit from additional metrics that measure information theoretic leakage (e.g., mutual information estimation) or more adaptive recovery attacks.
- **Random data forgetting experiment is limited.** Only one table is shown, and the baseline set excludes several recent methods. The adaptation (remapping forget prototypes to remain prototypes) is ad‑hoc and not clearly justified.
- **Some results are not statistically significant.** The paper reports mean and std for many experiments, but the standard deviations are sometimes large relative to the claimed improvements (e.g., Table 6 for CIFAR‑10). More careful statistical testing would strengthen the claims.

### Trivial
- In Table 7, the method is sometimes abbreviated as “MoUE” instead of “MoRE” (likely a typo). Several table captions are inconsistent or contain garbled formatting.

## Nice-to‑Haves
- A discussion of how to defend against a “layer‑stripping” attack, or an experiment where the adversary is allowed to remove the MoRE layer and fine‑tune the base model only.
- An analysis of the computational cost of prototype construction for very large forget sets (e.g., ImageNet‑scale).
- A more thorough investigation of the sensitivity to the choice of which layer to apply MoRE to, with recommendations.

## Novel Insights
None beyond the paper’s own contributions. The central insight (using orthogonal projection to enable precise expert‑based remapping of forget features) is genuinely novel, but the paper does not offer a broader theoretical or empirical insight that extends beyond its specific method.

## Suggestions
1. **Address the fatal weakness.** Either modify the framework so that the base feature extractor is also updated (e.g., by backpropagating the projection loss into the backbone), or clearly revise the claims: define the threat model appropriately (e.g., black‑box access to the full deployed model) and acknowledge that white‑box access that allows layer removal would trivially bypass the unlearning. Provide experiments that show whether the method remains robust if an adversary can inspect and modify the MoRE layer.
2. **Soften the “irreversibility” claim.** Replace “irreversible” with “strong resistance to recovery via linear probing and fine‑tuning” or similar, and discuss the limitations.
3. **Provide more details on diffusion model adaptation.** Include the exact construction of prototypes from tokenized prompts, the layer(s) to which MoRE is applied, and an ablation that compares different design choices.
4. **Add more diverse recovery attacks.** Test whether an adversary can train a small network to invert the remapping, or use nearest‑neighbor search in the original feature space to cluster forget samples.
5. **Improve statistical reporting.** Use confidence intervals or paired tests when comparing to baselines, especially in settings with high variance.

## Score and Decision
Score: 4

MY FINAL SCORE: <score>4</score>
MY FINAL DECISION: <decision>Reject</decision>