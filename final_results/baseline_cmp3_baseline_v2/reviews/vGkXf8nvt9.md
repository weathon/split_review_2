## Summary

This paper proposes *Forget-to-Focus* (F2F), a two-stage protocol for domain specialization of LLMs that first performs targeted unlearning on a "forget set" of general-domain data (with an optional retain set for stability) and then fine-tunes on a domain-specific dataset. Through experiments on coding, mathematics, and medical tasks across models from 0.6B to 72B parameters, the authors claim that preparatory unlearning consistently outperforms standard fine-tuning, DAPT, LoRA, and other baselines. They also analyze representational shifts using CKA and SVCCA to support the claim that unlearning reshapes internal geometries toward domain-useful structures.

## Strengths

- **Clear problem motivation**: The paper correctly identifies that negative transfer from pretrained general knowledge can hinder domain-specific fine-tuning, and it proposes an interesting intervention—actively suppressing irrelevant priors via unlearning.
- **Broad empirical scope**: Experiments cover three diverse domains (coding, math, medical), five model families (Qwen, LLaMA, Gemma) ranging from 0.6B to 72B, and multiple unlearning variants (GA+GD, GA, NPO, GA+KL). This breadth lends partial credibility to the main claim.
- **Representation analysis**: The use of centered kernel alignment (CKA) and SVCCA to probe representational drift provides a mechanistic perspective that goes beyond raw performance numbers, helping to understand *why* unlearning might help.

## Weaknesses

### Major

- **Missing evidence for calibration claims**: The abstract and introduction state that F2F "improve[s] calibration on medical QA tasks, reducing overconfidence and mitigating reliability issues," yet no calibration metrics (e.g., expected calibration error, reliability diagrams) appear anywhere in the main paper. This is a claimed core benefit that is entirely unsubstantiated—a significant omission that undermines the contribution.

- **Weak theoretical grounding**: The authors attempt a theoretical analysis with strong-convexity and linear-model assumptions that do not hold for LLMs. The Proposition and Corollary are presented as though they provide guarantees for the actual setting, but the authors themselves note the mismatch ("While LLM training objective is non-convex..."). This analysis adds little rigor and may mislead readers about the true nature of the gains. It would be far more honest to present the theory as an illustrative toy model without claiming it explains the empirical results.

- **Unconvincing forget-set construction and baseline fairness**: The forget set is drawn from BookCorpus, which is fiction/narrative—not representative of the general pretraining data of modern LLMs (which includes web text, code, etc.). Using only 100–1000 samples (versus trillions of pre-training tokens) to "remove irrelevant knowledge" is unlikely to cause a meaningful change; the observed gains may instead stem from regularization effects (e.g., gradient ascent injecting noise). The baselines (SFT, DAPT, LoRA, CurlLoRA) are implemented without extensive tuning, and it is unclear whether they are comparably optimized. The paper does not control for the computational cost or training steps across methods.

- **Inconsistent gains and unexplained failures**: While F2F shows large improvements on Qwen-0.6B (e.g., HumanEval from 19.50 to 42.07), gains on larger models are more moderate (e.g., LLaMA-8B from 33.54 to 60.37, but SFT alone already reaches 56.71). For Gemma-2B, the unlearning step catastrophically degrades performance (HumanEval 0.00) before fine-tuning, and the final improvement over base is small. These patterns are not systematically analyzed; the paper attributes variation to "model capacity" but provides no rigorous explanation, weakening the claim of universal benefit.

- **Missing key experimental details**: The number of unlearning steps/epochs is not reported in the main text. The retain set is described as "a small subset of the fine-tuning data," but it is unclear how this subset is chosen and whether it overlaps with the evaluation data. The fine-tuning datasets (e.g., OpenCoder, PubmedQA) are used as both the downstream task and the source of the retain set, creating a potential leakage issue.

### Minor

- **Overclaiming novelty**: The paper states it is "the first comprehensive study of machine unlearning as a preparatory stage for domain specialization." However, prior work (e.g., Cha et al. 2024 on robust unlearning for LLMs, Chen et al. 2023a on active forgetting during pretraining) touches on related ideas. While the framing is different, the novelty claim could be softened.
- **Representation analysis limited to one model**: CKA and SVCCA are only shown for a single model size/architecture; it is unclear whether the geometric shifts generalize across all tested models.
- **Table layout issues**: Table 3 is large and somewhat difficult to parse; headers for forget-set type and model are not as clear as they could be.

## Nice-to-Haves

- Include calibration results (ECE, reliability diagrams) for the medical QA experiments to substantiate the claim made in the abstract.
- Ablate whether the unlearning step simply adds beneficial stochastic noise by comparing against random-direction gradient ascent or parameter perturbation.
- Provide a direct comparison of training compute (wall-clock time, FLOPs) for F2F vs. standard fine-tuning to assess practical cost.

## Novel Insights

None beyond the paper's own contributions. The core idea—using unlearning to aid fine-tuning—is intuitively appealing, and the CKA/SVCCA analysis offers a plausible visual story. However, the lack of controlled ablations and the missing calibration results prevent the emergence of a genuinely new insight beyond what the authors already claim.

## Suggestions

- Add the calibration experiments and either remove the unsubstantiated claim or report the (possibly negative/null) results.
- Replace the theoretical section with a more honest discussion of why unlearning might help in practice (e.g., as a regularizer or as a way to break symmetry), and remove the strong-convexity analysis.
- Use forget sets from the actual pre-training distribution (e.g., subsets of C4, RedPajama) rather than BookCorpus, or justify why BookCorpus is a valid proxy.
- Report the number of unlearning steps for all models and control for the total training steps across methods.

## Score and Decision

**Score**: 4  
**Decision**: Reject

MY FINAL SCORE: <score>4</score>
MY FINAL DECISION: Reject