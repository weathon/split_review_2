## Summary

This paper investigates whether activation steering — a technique for controlling LLM behavior by adding vectors to hidden states — systematically undermines safety refusal mechanisms. Across Llama-3, Qwen2.5, Falcon-3, and Falcon-H1 (3B–70B parameters), the authors show that even **random** Gaussian steering vectors induce non-zero harmful compliance (0% → 2–27%). SAE features (a standard source of interpretable steering vectors) show comparable effects, and averaging just 20 prompt-specific jailbreaking vectors produces a universal attack that generalizes to unseen harmful prompts. A case study using the production Goodfire API confirms the practical risk.

## Strengths

- **Novel core finding.** The observation that even *random* activation directions can routinely induce harmful compliance (0% → 2–27%) is genuinely surprising and practically significant. Prior work focused on *optimized* adversarial steering vectors; showing that arbitrary perturbations systematically compromise refusal is a distinct result with clear security implications (Sec. 4.1, Fig. 2).

- **Broad and systematic evaluation.** The paper tests four model families (Llama-3, Qwen2.5, Falcon-3, Falcon-H1) at scales from 3B to 70B, spanning multiple architectural lineages. This breadth rules out the concern that the vulnerability is specific to one training recipe. The universal attack results across eight model variants (Fig. 6) are particularly informative.

- **Clever universal attack construction.** Averaging 20 prompt-specific jailbreak vectors produces a vector that achieves up to 64% compliance on unseen harmful prompts (Falcon3-3B) without requiring model weights, gradients, or output logits — a realistic and concerning threat model (Sec. 4.4, Fig. 6).

- **Concrete case study via a production API.** The demonstration that a benign "brand identity" SAE feature, deployed through the public Goodfire API, can elicit scam emails and detailed cannibalism instructions is compelling and hard to dismiss. The two identified failure modes (disclaimer-then-compliance, justification via fictional framing) are empirically useful characterizations (Sec. 4.3, Fig. 5).

- **Well-designed single-prompt sweep.** The sweep over layers (early/middle/late), scaling coefficients, and vector types in Sec. 4.1 is methodologically sound. The finding that middle layers are most vulnerable and that the steering strength vs. compliance relationship is non-monotonic are valuable observations for future work.

## Weaknesses

### Major

- **No variance or uncertainty reported on any averaged result.** Every quantitative result in the paper (e.g., 17% CR for Llama3-8B, 11% for Qwen2.5-7B, 4× improvement for the universal attack) is a point estimate without standard deviation, confidence interval, or any distributional information. The paper averages 1,000 random vectors per condition — but do most vectors produce 0% compliance and a few produce 100%, or is the effect relatively uniform? These are very different scenarios with different implications. For the universal attack, 20 distinct universal vectors are created per model but only their average CR is reported. This limits the reader's ability to assess the stability and practical risk level of the reported effects. (Spans Secs. 4.1, 4.2, 4.4.)

### Minor

- **Confounded comparison in the scaled evaluation (Sec. 4.2).** The scaled experiment compares random steering (Llama3-8B at 1/3 depth, coefficient 2.0; Qwen2.5-7B at 1/3 depth, coefficient 1.5) against SAE feature steering (Llama3.1-8B at 2/3 depth, coefficient 2.0). Three variables differ simultaneously (model variant, layer depth, coefficient), so any observed differences cannot be attributed to SAE vs. random vectors alone. The clean comparison was already done in Sec. 4.1 (Fig. 2c) under controlled conditions. The scaled experiment should either match those conditions or be explicitly framed as a separate demonstration that SAE features at their native layer also produce the phenomenon — not as a controlled comparison.

- **Overclaimed "zero-shot" label for the universal attack (Sec. 4.4).** The attack is described as "completely zero-shot," but constructing it requires 100–500 query-response trials on the target model to identify successful jailbreaking vectors, followed by output-dependent selection. This involves substantial interaction with the model. The substantive contribution (no weights, gradients, or harmful training data needed) stands without this label, which invites unnecessary terminological debate.

- **Baseline 0% compliance is stated but not empirically demonstrated.** The paper asserts "For all models and prompts, the baseline compliance rate without any steering is 0%" (Sec. 3.4) without showing this verification in the main text. While the claim is plausible for aligned instruction-tuned models, a brief verification table would strengthen credibility.

### Trivial

None.

## Nice-to-Haves

- Including variance/uncertainty metrics for all averaged results would be the single most impactful improvement the authors could make.
- If the SAE scaled comparison cannot use the same model/layer as the random baselines (due to SAE availability constraints — the paper notes it is limited to Llama3.1-8B layer 19 in Sec. 3.3), clearly stating this limitation and framing the two sets of results as independent demonstrations rather than a comparison would improve clarity.
- A brief analysis of what distinguishes high-compliance random vectors from low-compliance ones (e.g., cosine similarity to known refusal directions) could deepen the mechanistic investigation.

## Removed Points

The following points from the input review are removed under the filtering rules:

- **LLM-as-judge not validated in the main text:** The paper states that quality assessment against human annotations is in Appx. B. The complaint that validation is not in the main paper and that the appendix is unavailable during review is a weakness about missing appendix content, which per policy is a parser artifact and not a valid criticism.
- **Request to evaluate on HarmBench:** This is scope creep beyond the paper's stated evaluation framework using JailbreakBench.
- **"No discussion of practical access requirements for the universal attack":** The paper does discuss access requirements (line 239: "needs no model weights, gradients, or logits, only the ability to perform activation steering and observe model outputs").
- **"No analysis of whether compliance is real or superficial":** The Sec. 4.3 case study directly provides this analysis with concrete harmful outputs and identified failure modes.
- **Evaluation on 99 vs. 100 prompts:** The universal attack uses one prompt as the seed and evaluates on the remaining 99 — this is a reasonable and standard experimental design.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. **Add variance information.** Report standard deviation, confidence intervals, or distribution histograms for every averaged CR result. Even a brief statement like "across 1,000 random vectors, mean CR = 17% (SD = 5.2%)" would resolve the most significant evidential gap.
2. **Clarify Sec. 4.2 framing.** Either run SAE features at the 1/3 depth layer to match random baselines (if feasible), or explicitly state that the comparison is limited by SAE availability and present the two sets of results as independent demonstrations of the phenomenon.
3. **Replace "zero-shot"** with a more precise description such as "black-box" or "query-efficient" for the universal attack (Sec. 4.4).
4. **Verify the 0% baseline** with a brief sentence or one-line table for each model.

MY FINAL SCORE: <score>6</score>
MY FINAL DECISION: <decision>Accept</decision>