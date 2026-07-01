Now let me verify a few specific claims more carefully.Now I have a thorough understanding of the paper. Let me submit my draft review before calibration.Now let me run Round 1 calibration — bracketing across score bands:Let me read some of the most relevant anchor papers for calibration:Now let me read one more anchor to refine my bracket:Now I have enough calibration data. Let me form my bracket and write the final review.

**Round 1 Bracket:** Based on anchors, the paper sits between **4.0 and 5.5**. It's clearly above the 2.5-3.0 rejected papers (which have weaker methods and evaluations), comparable to the 4.25-4.75 range (papers with interesting ideas but evaluation gaps), and falls short of the 5.5+ accepted range (which have more thorough evaluations).

---

## Summary
WASI (Weight-Activation Subspace Iteration) introduces a method for jointly compressing weight matrices and activation maps into low-rank subspaces during transformer fine-tuning, enabling on-device training with reduced memory and computation. The method leverages the empirical observation that the essential subspace of model parameters remains stable during fine-tuning, performing a one-time SVD to determine the subspace and using cheaper subspace iteration thereafter. Both weights and activations are compressed under a unified explained-variance threshold ε.

## Strengths
- **Unified weight-activation compression is a genuine design contribution.** Prior work ASI compressed only activations and SVD-LLM compressed only weights; WASI unifies both under a single ε threshold. Algorithm 1 is clearly specified and the decomposition strategy is well-motivated. The paper explicitly identifies the gap in prior work (Sec. 2) and fills it with a coherent mechanism.

- **Empirical validation of the subspace stability premise (Fig. 3).** Figure 3a shows singular values of ViT weight matrices remain stable across 40 epochs, and Figure 3b demonstrates WSI matches full SVD accuracy at 1.36× fewer FLOPs. The paper builds its method on a testable assumption and tests it—good scientific practice.

- **Real hardware wall-clock measurements on Raspberry Pi 5 (Sec. 4.4, Fig. 8).** The paper reports actual per-iteration training and inference times showing ~1.4× speedup at ε=0.9. Many efficiency papers rely solely on theoretical FLOPs; this paper grounds its claims in reality.

- **Closed-form complexity analysis (Sec. 3.4, Fig. 2)** provides practitioners with a tool to predict memory and speedup before running experiments, showing how savings scale with rank K_i and layer dimensions.

## Weaknesses

### Fatal
None

### Major

- **Missing LoRA baseline.** LoRA is the dominant parameter-efficient fine-tuning method and is extensively discussed in Sec. 2, where the paper argues theoretically that LoRA doesn't compress activations (Sec. 1) and doesn't help at inference (Sec. 2). However, no empirical comparison is provided. The paper's framing targets the same practical problem as LoRA—fine-tuning under resource constraints—so practitioners need to see their accuracy-memory-FLOPs tradeoffs side by side. SVD-LLM (which incorporates LoRA adapters) is compared but is not a substitute for a direct LoRA baseline. This gap is especially significant because the paper explicitly acknowledges LoRA's relevance to its problem setting.

- **MLP-only evaluation with unqualified headline numbers.** Sec. 4.1 states: "focusing on linear layers within multi-perceptron blocks for fair comparison with previous methods." Attention layers—roughly half the parameters and computation in a transformer—are excluded. However, the abstract claims "reducing memory usage by up to 62×" and "up to 2× FLOPs reduction" without this qualification. This creates a misleading impression of whole-model savings. The actual end-to-end memory and speedup for a full transformer training run are likely substantially lower than the per-MLP-layer numbers reported.

- **TinyLlama experiment is inconclusive for LLM applicability.** Sec. 4.3 uses ε=0.1 (retaining only 10% of explained variance), fine-tunes only the last 5 layers, on BoolQ with accuracy in the 64–66% range. The paper itself frames this as an extension ("To test its generality"), but the extreme settings make the dramatic compression numbers (953.86× activation memory) hard to interpret. These numbers likely reflect that the last 5 MLP layers at ε=0.1 contribute minimally, rather than demonstrating that WASI works well on LLMs. A more informative experiment would use a moderate ε, more layers, and a more demanding task.

### Minor

- **No numerical accuracy tables in the main text.** All main results (Figs. 5–7) are presented as Pareto curves without specific accuracy values. The claim "maintains accuracy comparable to vanilla training" (abstract) and "matches vanilla accuracy" (Sec. 4.3) cannot be precisely verified from figures alone. Tab. 2 is referenced (line 223) but deferred to the appendix; key quantitative results should appear in the main paper.

- **Subspace stability validated too narrowly.** The foundational hypothesis—that the essential subspace remains stable during fine-tuning—is tested only on one layer (W_6) of one model (ViT) on one dataset (Pets) in Fig. 3a. This is the theoretical pillar of the entire method and deserves validation across multiple layers, models, and datasets.

- **Full baseline comparison only for ViT/CIFAR-10.** In the main text, the full four-way comparison (WASI vs. ASI vs. SVD-LLM vs. vanilla) appears only for ViT on CIFAR-10 (Fig. 5). For SwinT (Fig. 6), only WASI vs. vanilla is shown, with ASI and SVD-LLM baselines deferred to Appendix B.3. This weakens the main paper's narrative about WASI's superiority across settings.

- **Weight factorization maintenance during training needs clarification.** Algorithm 1 (lines 6–7) requires the full weight matrix W at each iteration for subspace iteration, but Eq. 11 updates the product L_i R_i with the gradient. How the factored form is maintained after the gradient update—and whether this requires reconstructing the full O_i × I_i matrix transiently—needs explicit discussion, as it affects the actual memory savings during training.

### Trivial
None

## Nice-to-Haves
- Report end-to-end whole-model memory and latency (including attention layers) alongside per-MLP-layer numbers
- Provide variance/error bars across random seeds, particularly for the narrow accuracy ranges in the TinyLlama experiment (64–66%)
- Extend the subspace stability analysis (Fig. 3a) to multiple layers and models as a compact summary figure
- On-device latency measurements for SwinT, not just ViT

## Removed Points
*These points are flagged to be removed; treat them with caution.*

- **"Same hyperparameters may disadvantage SVD-LLM"** — The reviewer speculated that shared hyperparameters across methods might be unfair. This is speculative and depends on appendix details. Moreover, using identical hyperparameters is a common and defensible experimental choice that arguably strengthens reproducibility. Removed as speculative.

- **"Introduction framing mismatch with GPT/Gemini/LLaMA/DeepSeek"** — The reviewer noted the introduction references large models that are far beyond the experimental scope. While the gap is real, motivating with prominent examples before scoping down to feasible experiments is standard practice. The paper's actual experimental scope (ViT, SwinT, TinyLlama) is clearly stated in Sec. 4.1. Removed as minor scope framing, not a substantive flaw.

- **"Missing variance reporting across seeds"** — While valuable, this is not standard in all on-device learning evaluations and the accuracy differences are directionally consistent across settings. Moved to nice-to-have rather than weakness.

## Novel Insights
The core insight that weight subspace stability during fine-tuning can be exploited to replace expensive per-iteration SVD with cheap subspace iteration—and that this can be unified with activation map compression under a single explained-variance threshold—is genuinely novel in the on-device training literature. The empirical confirmation in Fig. 3 that singular values remain stable across 40 epochs of fine-tuning provides a clean, testable foundation. The resulting method elegantly addresses both training memory (via activation compression) and inference efficiency (via weight compression) simultaneously, which is a meaningful step beyond prior methods that handle these separately.

## Suggestions
- Add a comprehensive table in the main text with exact accuracy, memory, and FLOPs at each ε for all model-dataset-baseline combinations—this would make the paper's claims precisely verifiable
- Include LoRA as an empirical baseline even if the comparison is asymmetric (LoRA doesn't compress activations); practitioners need this comparison
- Clearly qualify headline compression numbers in the abstract/introduction as applying to MLP linear layers only, or extend the evaluation to whole-model savings
- Strengthen the TinyLlama experiment with a moderate ε (e.g., 0.5–0.9), more layers, and a task with a wider accuracy range (e.g., a multi-class NLU task)
- Expand subspace stability validation to at least 3–4 layers across both ViT and SwinT

## Score and Decision

### Calibration Anchors

| Paper | Path | Avg Score | Round | Comparison |
|---|---|---|---|---|
| Robotics Chinese NLP | gwZ90hFSL2 | 1.00 | R1 | Clearly below WASI; pseudoscientific |
| Financial Markets NN | nSDOkm0SKo | 1.00 | R1 | Clearly below WASI; toy scenario |
| IC-Light | u1cQYxRI1H | 10.00 | R1 | Misclassified in low band; irrelevant |
| NEMESIS Jailbreaking | 5kMwiMnUip | 1.40 | R1 | Clearly below WASI; limited contribution |
| NanoMoE | 04RLVxDvig | 3.00 | R1 | Weaker experiments and narrower contribution than WASI |
| On-Device TL Mixed Precision | eqKHuxIpp5 | 2.50 | R1 | Same domain but much weaker method; no real device eval; WASI clearly better |
| HoLoRA | igGeaxOiFM | 3.00 | R1 | Limited novelty (LoRA variant); comparable evaluation issues but less unique contribution than WASI |
| FeDeRA | GtlRN48XYA | 3.00 | R1 | Federated LoRA; narrower than WASI's unified approach |
| Activations Aren't Cheap in LoRA | 3ylNuZXtMg | 4.25 | R1 | Similar domain (activation memory in fine-tuning); limited novelty (reformulation). WASI has more novelty but comparable eval gaps |
| EVA (Explained Variance Adaptation) | DM6Q45HWSk | 4.75 | R1 | Uses SVD/explained variance like WASI; marginal improvements and missing baselines. Comparable overall quality |
| Memory-Efficient Fine-Tuning via Pruning | JMgxtZqkvO | 4.50 | R1 | Similar efficiency focus; comparable evaluation thoroughness |
| Low-Rank Correction for Quantized LLMs | FA3iYp1y6z | 5.00 | R1 | More thorough evaluation; WASI falls slightly short |
| Sine-Activated Low-Rank Matrices | cWGCkd7mCp | 7.00 | R1 | Stronger theoretical framework and broader evaluation; WASI clearly below |
| Differentiable Structured Matrices | pAVJKp3Dvn | 5.67 | R1 | More general framework with stronger eval; above WASI |
| Structural Integrity PEFT | OALIb8oNfl | 5.75 | R1 | Better-developed framework; above WASI |
| OATS | DLDuVbxORA | 6.25 | R1 | Stronger method and evaluation; above WASI |

**Round 1 bracket: 4.0–5.5**

The paper's genuine novelty (unified weight-activation compression), real hardware evaluation, and sound methodology place it above the 3.0-range papers, which typically have weaker methods or toy-only experiments. However, the significant evaluation gaps—missing LoRA baseline, MLP-only scope with misleading headline numbers, inconclusive TinyLlama experiment, and no numerical tables—prevent it from reaching the borderline-accept (5.5+) range. The paper is most comparable to papers in the 4.25–4.75 range that have interesting ideas but insufficiently thorough evaluations.

**Final assessment:** The core idea is sound and has practical value, but the experimental evaluation does not convincingly support the claims as currently framed. The issues are primarily evidential rather than structural—the method itself is reasonable—but they are collectively substantial enough to place the paper below the acceptance threshold. The paper would benefit significantly from a more comprehensive and honestly-scoped evaluation.

**Score: 4.5**

MY FINAL SCORE: <score>4.5</score>
MY FINAL DECISION: <decision>Reject</decision>