Now let me write the final consolidated review.

## Summary

This paper introduces LoRA-Mixer, a framework that routes task-specific LoRA experts into the Q/K/V projection layers of LLMs via a learned router, with an emphasis on data-efficient routing and plug-and-play reuse of externally sourced LoRA modules. The authors propose a Routing Specialization Loss (RSL) to balance expert load while promoting input-aware specialization, and demonstrate results across ~15 benchmarks on Transformers and SSMs.

## Strengths

- **Architectural design choice is well-motivated.** Positioning LoRA experts at the Q/K/V projection matrices — rather than replacing entire FFN/attention blocks or using parallel branches — makes the framework architecture-agnostic and compatible with both Transformers and SSMs. This is a genuine differentiator from prior work like MixLoRA (which targets FFN) and parallel-branch schemes (which perform shallow fusion).

- **Cross-model transfer experiment (Table 5).** Transferring routing weights from Mistral-7B to LLaMA3-8B (same architecture) and observing non-degraded performance on 2 of 3 tasks is a non-trivial positive result that supports the claim that RSL-learned routing captures something beyond dataset-specific artifacts.

- **Internet-sourced LoRA reuse (Table 3).** Demonstrating that pretrained LoRAs from public repositories can be composed via routing trained on only 2k held-out data points (with frozen LoRA parameters) is practically appealing and directly addresses the paper's stated motivation of plug-and-play modularity.

## Weaknesses

### Fatal

- **RSL sign error contradicts the paper's central narrative.** Equation (5) defines $\mathcal{L}_{\text{RSL}} = \alpha \cdot \sum_{i=1}^K \bar{p}_i \cdot \bar{f}_i - \lambda \cdot \mathbb{E}_{x \sim \mathcal{D}} [\mathcal{H}(p(x))]$. Since $\mathcal{H}(p(x)) = -\sum_i p_i(x) \log p_i(x) \geq 0$, the term $-\lambda \cdot \mathbb{E}[\mathcal{H}(p)]$ is ≤ 0 and minimizing it makes $\mathcal{H}(p)$ *larger* — pushing the routing distribution toward *uniformity*, not peakedness. Yet the paper repeatedly claims that RSL "suppresses overly flat distributions" (line 86), "minimizes $\mathcal{H}(p(x))$ to promote specialization" (line 94), and "encourages high variance and peaked distributions" (line 110). The gradient in Equation (9) (which is $+\lambda(\log p_i(x) + 1 - \mu)$) confirms the uniformity-promoting direction. This is a direct mathematical contradiction with the paper's entire narrative about what RSL does. If the intended loss was $+\lambda \cdot \mathbb{E}[\mathcal{H}(p(x))]$, the formulation is wrong; if the formulation is correct, the paper's motivation and analysis are invalid. Either way, the core technical contribution is unsound as written.

### Major

- **The "LoRA" baseline in Table 2 is undefined.** It appears as a row alongside LoRAHub, MoLE, and MixLoRA, but the paper never specifies what "LoRA" means — whether it is a single LoRA trained on combined multi-task data, a per-task best single LoRA, or a single LoRA with comparable total parameters to the ensemble. Without this definition the comparison is uninterpretable. If "LoRA" is a single adapter, the near-tie with LoRA-Mixer on several tasks (e.g., LLaMA3-8B: LoRA 81.09 vs. LoRA-Mixer 81.55 on Medical; 65.14 vs. 65.53 on GSM8K) would suggest the routing mechanism itself contributes little beyond having more parameters.

- **The 48% parameter claim is unsubstantiated.** The abstract and introduction prominently claim LoRA-Mixer uses "only 48% of the trainable parameters of existing methods," but no table, derivation, or analysis in the paper explains how this number is computed — which methods it is compared against, at what expert count or rank. This is a central quantitative claim used to position the paper's contribution and it is entirely unsupported.

- **Training data sizes are not specified for the main comparison (Table 2).** The paper emphasizes data efficiency as a key advantage, but Table 2 does not state how much training data each baseline used. The RSL comparison (Table 8) properly controls training data at 2k, but the primary results table does not, making the "data efficiency" claim unverifiable from the main experiments.

### Minor

- **Selective reporting in Table 4 (LoRA-LEGO).** The paper states it "outperforms LoRA-LEGO on three of the four tasks" without acknowledging the RTE result where LoRA-LEGO (71.85) substantially beats LoRA-Mixer (61.47) by over 10 points. The data is displayed but the framing is selectively positive.

- **No variance or confidence intervals.** Many gains in Table 2 are small (<1 percentage point, e.g., +0.46 on Medical, +0.39 on GSM8K for LLaMA3-8B). The paper reports averages over three runs but no variance, making it unclear whether small differences are significant.

- **Missing ablation of the architectural choice.** The paper attributes part of its improvement to applying LoRA at projection layers rather than FFN blocks, but never tests this directly (e.g., LoRA-Mixer with experts at the FFN instead, or at both locations). The architectural contribution is asserted but not demonstrated via controlled comparison.

### Trivial

None.

## Nice-to-Haves

- An ablation comparing projection-layer placement vs. FFN placement of LoRA experts would strengthen the architectural claims.
- Variance or confidence intervals for the main results, especially where gains are <1%, would improve interpretability.
- The paper mentions a fixed top-K routing limitation; future work on dynamic or adaptive K would be a natural extension.

## Removed Points

These points are flagged for removal; treat them with caution:

- *"The convergence analysis and generalization bound are relegated to the appendix…their quality cannot be assessed here."* — **Removed:** The parser strips appendices from all papers; these exist in the original submission.
- *"The claim that entropy regularization reduces assumed complexity is plausible but unsupported in the main text."* — **Removed:** This criticism relies on content deferred to the appendix, which was stripped.
- *"LoRA-LEGO comparison uses a different base model and configuration and the paper does not explain why."* — **Removed:** The paper explicitly states it uses LLaMA2-7B to match the LoRA-LEGO paper's setup.
- *"Cross-model transfer framing obscures the ARC-E degradation."* — **Removed:** The data is fully presented in Table 5; the paper's framing (outperforms on 2 of 3 tasks) is accurate.
- *"Section 4.1 doesn't specify hyperparameters for each baseline."* — **Removed:** The paper references Appendix A.4, A.7, A.11 for model details.

## Novel Insights

None beyond the paper's own contributions. The key finding from review is the RSL sign contradiction, which is a flaw detection rather than a novel insight about the paper's actual contribution.

## Suggestions

1. **Fix the RSL formulation.** Either change Equation (5) to $+\lambda \cdot \mathbb{E}[\mathcal{H}(p(x))]$ (which would penalize high entropy and promote peaked routing, matching the narrative), or if the current sign is intentional, rewrite Section 3.3 entirely to accurately describe what the loss does and why promoting moderate-to-high entropy is beneficial given the auxiliary loss already pushes toward uniformity.
2. **Define the "LoRA" baseline** in Table 2 explicitly — what it is, how it was trained, and how many parameters it uses.
3. **Provide a table or derivation** for the "48% of existing methods' parameters" claim, or remove it.
4. **Report training data sizes** used by each baseline in Table 2.
5. **Add a direct ablation** comparing projection-layer placement vs. FFN placement of LoRA experts.
6. **Report variance/confidence intervals**, especially where gains are <1%.

## Score and Decision

The paper tackles a well-motivated problem with a clean architectural design, and the cross-model transfer and internet-sourced LoRA reuse results are genuinely interesting. However, the paper has a decisive structural flaw: the RSL loss as formulated in Equation (5) mathematically encourages uniform routing, which is the opposite of what the paper claims and builds its entire narrative around. This contradiction between the mathematics and the narrative undermines the core technical contribution. The additional issues (undefined "LoRA" baseline, unsubstantiated 48% parameter claim, uncontrolled training data in the main comparison) compound the evidential problems. The paper cannot be accepted in its current form.

MY FINAL SCORE: <score>3</score>
MY FINAL DECISION: <decision>Reject</decision>