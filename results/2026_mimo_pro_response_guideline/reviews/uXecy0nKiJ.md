Now I have sufficient data to calibrate. Let me finalize.

**Calibration Summary:**

| Anchor Paper | Score | Round | Comparison |
|---|---|---|---|
| NEMESIS Jailbreaking (5kMwiMnUip) | 1.40 | 1 | Off-topic or poorly executed; our paper is far stronger |
| Systematic Review of LLMs (8QTpYC4smR) | 1.00 | 1 | Generic survey; irrelevant comparison |
| Advancing Cross-Lingual (gwZ90hFSL2) | 1.00 | 1 | Off-topic |
| Financial Markets NN (nSDOkm0SKo) | 1.00 | 1 | Off-topic |
| Playing Language Game (BeOEmnmyFu) | 2.50 | 1 | Novelty-limited jailbreak; our paper has more depth |
| Measuring Steered Representations (z1yI8uoVU3) | 3.00 | 1 | Same topic but limited novelty, slim contribution; our paper is clearly stronger |
| Multi-round Conversational Jailbreaking (KyKTjRtyNG) | 3.00 | 1 | Standard jailbreak method; our paper more impactful |
| BlackDAN (kT6oc5CpEi) | 3.00 | 1 | Black-box multi-objective attack; our paper has broader scope |
| Understanding Jailbreak Success (HuNoNfiQqH) | 4.75 | 1 | Related latent space analysis but less impactful |
| Quack (1zt8GWZ9sc) | 3.67 | 1 | Role-playing jailbreak; our paper more substantial |
| AttnGCG (k9GfyX1eqM) | 4.00 | 1 | GCG enhancement; limited novelty |
| Steering Language Models with Activation Engineering (2XBPdPIcFK) | 5.00 | 1 | Foundational steering work; rejected with polarized (8,3,6,3) |
| Scaling Laws for Adversarial Attacks (YzxMu1asQi) | 6.50 | 1 | Activation attacks with scaling laws; comparable quality, theoretical angle |
| Jailbreaking with Simple Adaptive Attacks (hXA8wqRdyV) | 6.14 | 1 | Achieves 100% success; comparable practical impact, less novel method |
| Injecting Universal Jailbreak Backdoors (aSy2nYwiZ2) | 6.67 | 1 | Novel backdoor injection; comparable contribution |
| One Model Transfer to All (sULAwlAWc1) | 7.00 | 1 | Robust jailbreak against defenses; more polished methodology |
| Catastrophic Jailbreak via Exploiting Generation (r42tSSCHPh) | 7.00 | 2 | Simple generation exploitation attack; comparable |
| Principled Evaluations of SAEs (1Njl73JKjB) | 7.00 | 2 | SAE evaluation framework; more theoretical rigor |
| SAEs Do Not Find Canonical Units (9ca9eHNrdH) | 7.00 | 2 | SAE theoretical analysis; different sub-area, more polished |
| Residual Stream Analysis with MLSAEs (XAjfjizaKs) | 6.50 | 2 | Multi-layer SAE; different focus, comparable quality |
| Not All Features Are Linear (d63a4AM4hb) | 7.00 | 2 | SAE theory paper; different focus, more theoretical depth |

**Round 1 bracket: between 6.0 and 7.0**

The paper is clearly stronger than the 3-5 range reject papers (which have limited novelty, slim contributions, or limited scope). It is comparable to the 6.14-6.67 accepted papers with its novel universal attack and broad experimental scope. It sits slightly below the 7.0 papers, which tend to have more methodological polish (e.g., uncertainty reporting, more careful experimental controls). The absence of uncertainty quantification is the primary differentiator from the 7.0 tier.

**Narrowed to: 6.5**

The paper's universal attack construction is genuinely novel and practically impactful—arguably more novel than the "Simple Adaptive Attacks" paper (6.14) and comparable to "Injecting Universal Jailbreak Backdoors" (6.67). However, the complete absence of variance/confidence interval reporting across 300K responses, and the cross-model confounding in Fig. 3, prevent it from reaching the 7.0 tier.

---

## Summary
This paper demonstrates that activation steering—a popular interpretability technique for controlling LLM behavior—systematically compromises safety mechanisms. Through experiments across 4 model families, 8 scales, and 300,000 responses, the authors show that even random steering vectors increase harmful compliance from 0% to 2–27%, SAE-based features are comparably dangerous, and averaging just 20 prompt-specific jailbreak vectors creates a zero-shot universal attack achieving up to 63.4% compliance on unseen prompts with only black-box access.

## Strengths
- **Novel universal attack construction with clear security implications**: Averaging 20 randomly-sampled vectors that each jailbreak a single prompt creates a universal attack achieving up to 63.4% compliance on Falcon3-7B (~10× improvement over random steering) and generalizing zero-shot to unseen prompts, requiring only black-box access (Sec. 4.4, Fig. 6). This is the paper's strongest and most novel contribution.
- **Broad experimental scope**: 4 model families (Llama3, Qwen2.5, Falcon3, FalconH1), 8 model scales (3B–70B), 3 layer depths, 6 scaling coefficients, 2 vector types, and 300,000 total responses (Sec. 4.1–4.4, Figs. 2, 3, 6). This breadth makes it difficult to dismiss the findings as isolated artifacts.
- **Random steering baseline establishes a fundamental vulnerability**: Testing random Gaussian vectors demonstrates safety bypass is not contingent on semantic alignment, showing the latent space harbors directional vulnerabilities regardless of vector interpretability (Sec. 3.2, Fig. 2).
- **Practical validation via production API**: Section 4.3 demonstrates steering a benign "brand identity" SAE feature through the public Goodfire API successfully jailbreaks Llama3.1-8B, revealing "disclaimer-then-compliance" and "justification via fictional framing" failure modes (Fig. 5). This confirms real-world risk in deployed systems.
- **Cross-category analysis reveals monitoring infeasibility**: 668/1000 SAE features jailbreak ≥5 prompts, the most dangerous features represent benign concepts like "brand identity" (Fig. 4a), and cross-category generalization is poor (Fig. 4b), making exhaustive safety monitoring practically infeasible.
- **Careful evaluation design**: Incoherent or nonsensical responses are classified as SAFE even if they mention harmful content (Sec. 3.4), using a reasoning-mode judge model (Qwen3-8B) with justification output, which prevents inflated compliance rates from nonsensical text.

## Weaknesses

### Fatal
None

### Major
- **No uncertainty quantification on any reported number**: The paper averages compliance rates over 1,000 vectors per condition (100 prompts × 1,000 vectors for scaled evaluation) but never reports variance, confidence intervals, standard errors, or error bars anywhere in the paper. This is particularly problematic for the core SAE-vs-random comparison, where the claimed "2–4% higher Compliance Rate" (Fig. 2c) difference cannot be assessed for statistical significance by the reader. For the universal attack results (Fig. 6), the large effect sizes (e.g., 63.4% vs 5.7%) make this less critical, but for fine-grained comparisons in Figs. 2c and 4, the absence substantially undermines confidence. The paper already has all the data needed to compute these.

- **Scaled evaluation lacks a same-model SAE-vs-random comparison**: Fig. 3, the main scaled-up result, compares random vectors on Llama3-8B (17%) and Qwen2.5-7B (11%) against SAE features on Llama3.1-8B (10%)—three different models with different layer depths and scaling coefficients. The 17% vs 10% comparison cannot be attributed to vector type without controlling for model differences. While the paper does have a same-model comparison in Fig. 2c (Llama3.1-8B, random vs SAE), this is only on a single prompt. Extending the random vector evaluation to Llama3.1-8B across the full 100-prompt JailbreakBench dataset would directly support the central "SAE features are no safer than random" claim from the scaled evaluation.

### Minor
- **Hyperparameter selection procedure not fully transparent**: Sec. 4.1 sweeps layers and scaling coefficients on a single prompt. Sec. 4.2 uses specific configurations (Llama3-8B at 1/3 depth with c=2.0, Llama3.1-8B at 2/3 depth with c=2.0) that appear selected from this sweep. The paper doesn't state whether these were pre-specified or selected from the single-prompt results, which constitutes a mild form of optimization on one JailbreakBench prompt before evaluating on the full dataset.

- **No sensitivity analysis for number of averaged vectors in universal attack**: The choice of 20 vectors is described as balancing "attack potency and sampling efficiency" but no analysis shows how performance varies with 5, 10, 20, or 50 vectors. A brief ablation would strengthen the claim that 20 is sufficient.

### Trivial
None

## Nice-to-Haves
- Brief mechanistic discussion of *why* random steering breaks alignment in the main text rather than only in App. E.
- Brief discussion of feasible defense strategies beyond the one-sentence mention in the conclusion.
- Sampling-based generation (vs. greedy decoding) may interact differently with steering effects; a brief note acknowledging this would be useful.

## Removed Points
These points are flagged to be removed, treat them with caution:
- None needed; all reviewer points were either substantively valid or were already filtered during merger.

## Novel Insights
The paper's most genuinely novel insight is that localized, prompt-specific activation steering vulnerabilities can be systematically aggregated into a universal attack vector with black-box access alone. The demonstration that averaging just 20 vectors from single-prompt jailbreaks produces a zero-shot universal attack (up to 63.4% compliance, ~10× improvement over random) reveals that the linearity of activation steering creates a fundamental security asymmetry: it is far easier to weaponize these vulnerabilities than to defend against them. The finding that the most dangerous SAE features correspond to benign concepts (e.g., "brand identity") is also an important contribution to understanding the safety implications of interpretability tools.

## Suggestions
- Add error bars / confidence intervals to all figures and tables; the data already exists in the 1,000-vector samples.
- Extend random vector evaluation on Llama3.1-8B across the full 100-prompt JailbreakBench dataset for a direct same-model comparison with SAE features.
- Clarify whether layer/coefficient configurations for Sec. 4.2 were pre-specified or selected from the Sec. 4.1 sweep.
- Add an ablation on the number of averaged vectors (5, 10, 20, 50) for the universal attack construction.

MY FINAL SCORE: <score>6.5</score>
MY FINAL DECISION: <decision>Accept</decision>