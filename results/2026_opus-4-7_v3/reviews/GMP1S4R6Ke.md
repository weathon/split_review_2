Now let me read the remaining sections more carefully to verify specific claims:Now I have a thorough understanding of the paper. Let me draft the review before calibration.Now let me do calibration search — Round 1 (Bracketing):Let me read key anchor papers to calibrate the score:Now I have sufficient calibration data. Let me form my bracket and finalize.

**Round 1 Bracket:**
- LoRA-Mixer is clearly above the reject tier (DLP-LoRA at 3.0, MORE at 4.0) given its much broader evaluation and more specific contributions.
- It's comparable to MoLE (5.0, accepted) and PERFT (5.33, rejected) in terms of novelty concerns, but has better evaluation breadth.
- It sits slightly below HMoRA (6.0, accepted) due to the missing placement ablation and no variance reporting — HMoRA had a cleaner novelty story with unanimous 6s.

**Initial bracket: 4.5 – 6.0**

The missing ablation for the paper's core claim (projection-layer vs FFN placement) and the absence of variance reporting are the key differentiators. These pull it below the HMoRA/MeteoRA tier (6.0-6.2). The breadth of evaluation and plug-and-play experiments pull it above clear rejects.

Now let me write the final review:

---

## Summary
LoRA-Mixer proposes a modular MoE framework that routes task-specific LoRA experts into the linear projection layers (Q, K, V, O) of attention/state-space modules rather than FFN blocks, combined with Routing Specialization Loss (RSL)—a negative entropy regularization term added to the standard MoE auxiliary loss to encourage input-aware, peaked routing distributions. The framework supports plug-and-play composition of pre-trained LoRAs from public repositories and is evaluated across 15 benchmarks on three base models (LLaMA3-8B, Mistral-7B, Falcon-Mamba-7B), spanning Transformers and SSMs.

## Strengths

- **Practical plug-and-play LoRA reuse (Table 3, §4.3).** The experiment composing five internet-sourced LoRAs from LoRAHub over Flan-T5 with only 2k routing-training samples is the paper's strongest practical demonstration. LoRA-Mixer achieves improvements on 4 of 5 GLUE tasks (e.g., SST-2: 94.50→95.07, RTE: 83.47→85.31) with frozen expert parameters, directly validating the claimed modularity.

- **Architecture-agnostic evaluation including SSMs (Tables 1–2).** Falcon-Mamba-7B is a full participant across all seven benchmarks, not an afterthought. LoRA-Mixer consistently outperforms all baselines on Falcon-Mamba (e.g., GSM8K: 57.87 vs. MoLE 54.28, HumanEval: 35.37 vs. MoLE 33.57), giving real substance to the architecture-agnostic claim.

- **Cross-model router transfer (Table 5).** Transferring routing parameters trained on Mistral-7B directly to LLaMA3-8B without adaptation yields positive transfer on 4 of 5 settings (e.g., GSM8K 5-shot: 78.64→81.43). This experiment is genuinely informative and rarely attempted in the LoRA-MoE literature.

- **Controlled routing loss comparison (Table 8).** Fixing LoRA parameters and training data (2k) while varying only the routing loss across RSL, GMoE, DS-MoE, and AESL is the right experimental design. The margins are substantial (e.g., ARC-C: 83.24 vs. AESL 79.88; HumanEval: 57.32 vs. AESL 50.46).

## Weaknesses

### Fatal
None.

### Major

- **The core architectural claim—projection-layer placement superiority—is never directly ablated.** The paper's headline thesis (§1, Figure 1, §5) is that routing LoRA experts into projection layers is superior to FFN-layer placement used by MixLoRA, MoLE, etc. However, Table 2 compares methods that differ simultaneously in routing loss, routing architecture, number of experts, training procedure, *and* placement location. Without an experiment applying the same RSL-optimized router to projection layers vs. FFN layers while holding everything else constant, this central claim is a design choice rather than an empirically validated finding. The conclusion in §5 states: "Unlike other methods that indiscriminately insert MoEs or completely replace attention or FFN modules, LoRA-Mixer only adapts the core projection layer"—but this is asserted, not demonstrated.

- **No variance reporting despite small margins on several benchmarks.** The paper states "all experiments are run three times and the average reported" (§4.1), yet no table includes standard deviations or confidence intervals. On LLaMA3-8B (Table 2), many gains over single LoRA are very small: SST2 +0.11 (95.30→95.41), GSM8K +0.39 (65.14→65.53), Medical +0.46 (81.09→81.55). Without spread information, these margins are not distinguishable from run-to-run noise. The three runs already exist; reporting ±σ would either confirm the improvements or honestly reveal which are within noise.

### Minor

- **Abstract improvement claims are not traceable to any table in the main text.** The abstract and §1 headline "+3.79% on GSM8K, +2.90% on CoLA, and +3.95% on ARC-C," but none of these numbers match any comparison in Tables 2, 3, 4, 7, or 8. The baseline for these gains is never specified, making the abstract selectively misleading. Readers will likely assume comparison to single LoRA (where the LLaMA3-8B gains are 0.39, 0.72, and 1.09 respectively).

- **RSL's novelty is overstated relative to its content.** RSL (Eq. 5) adds −λ·H(p(x)) to the standard auxiliary loss—this is entropy regularization of the routing distribution, a well-known technique in MoE and RL literature. The information-bottleneck framing (§3.3) and the gradient derivation (Eqs. 7–9) create an impression of novelty that the underlying modification does not fully sustain. The empirical evidence that this works well in the LoRA-composition setting (Table 8, Table 9) is more convincing than the theoretical dressing; the paper would be strengthened by directly acknowledging the simplicity and focusing on *why* this known technique is particularly effective when experts are pre-trained and frozen.

- **Table 9 shows RSL underperforms at 4k data (78.77 vs. 79.14).** For a method whose central claim includes data efficiency, a performance inversion at a specific data scale deserves discussion in the main text, not deferral to Appendix A.16.

- **Medical-QA evaluation uses an LLM judge (DeepSeek-R1) without validation.** No inter-rater reliability, correlation with human judgment, evaluation prompt, or temperature settings are disclosed (§4.1). For a benchmark where scores are reported to two decimal places, the reproducibility of the evaluation metric itself is a concern specific to the Medical results.

- **Figure 3's near-uniform expert loads create tension with the specialization narrative.** Global expert loads range from ~15.5% to ~17.5% (deviation ≤1pp from uniform 16.67%). While Figure 4 shows meaningful per-task differentiation, the paper does not address the apparent contradiction between the near-uniform global distribution and the claimed specialization benefits. The paper states this shows "balanced expert utilization" (§4.5), but the specialization story depends entirely on the per-task view.

### Trivial
None.

## Nice-to-Haves

- **Placement ablation**: Apply the same RSL-optimized router to (a) projection layers only, (b) FFN layers only, (c) both, across at least two base models. This would transform the central architectural claim from assertion into evidence.
- **More challenging multi-task benchmarks**: The current benchmarks are mostly classification/QA tasks where even naive LoRA composition works reasonably well. Benchmarks with known severe task interference would better showcase routing value.
- The theoretical apparatus (convergence analysis, generalization bounds) in the appendix could be replaced with a more concise empirical analysis of when and why entropy regularization helps in the LoRA-composition setting specifically.

## Removed Points

*These points are flagged to be removed; treat them with caution.*

- **$\mathcal{F}_{\text{route}}$ notation underspecification (Eq. 4)**: The reviewer noted the aggregation function is not made explicit until one infers top-K weighted averaging from context. This is a minor presentation issue, not a substantive weakness—the routing mechanism is standard MoE top-K weighted sum and is clear from Eqs. 1–2.

- **Gradient derivation omits chain rule through softmax (Eqs. 7–9)**: The reviewer noted that the derivation treats $p_i(x)$ as a free variable rather than deriving through the softmax Jacobian. This is formally correct as written and is a pedagogical choice, not an error.

- **LoRA rank not stated in Table 2 caption**: The rank information requires cross-referencing §4.5. This is a trivial presentation issue.

- **"LoRA" baseline may be weaker than it appears (Table 2)**: The reviewer suggested the "LoRA" row might be a single LoRA trained on mixed data rather than per-task upper bounds. However, the paper's stated goal is multi-task composition, so a multi-task LoRA baseline is the appropriate comparison.

## Novel Insights

The cross-model router transfer experiment (Table 5) is the paper's most genuinely novel contribution. It demonstrates that routing parameters trained on one model (Mistral-7B) can transfer to another (LLaMA3-8B) with positive results, suggesting that learned routing captures task-structure information that is portable across models with shared architecture families. This is an underexplored direction in the LoRA-MoE literature and could inspire future work on reusable routing modules.

## Suggestions

1. **Run the placement ablation.** This is the single highest-leverage experiment—same experts, same RSL, same data, but placed in projection layers vs. FFN layers. The result either validates the core claim or reveals it's not the placement but the loss/routing that matters.
2. **Report standard deviations.** The three runs already exist. Adding ±σ to every table would dramatically strengthen the evidential base.
3. **Clarify abstract baselines.** Specify which baseline yields +3.79/+2.90/+3.95, or replace with gains that are traceable to Table 2.
4. **Discuss Table 9's 4k inversion in the main text.** A brief explanation of why RSL underperforms at this data scale belongs in the paper, not the appendix.
5. **Validate the Medical-QA LLM judge.** Disclose the evaluation prompt and report agreement with a secondary evaluator on a sample.

## Score and Decision

### Calibration Anchors

| Paper | Path | Avg Score | Round | Comparison |
|---|---|---|---|---|
| NEMESIS (jailbreaking) | 5kMwiMnUip | 1.40 | R1 | Broken paper; LoRA-Mixer far superior |
| Systematic Review of LLMs | 8QTpYC4smR | 1.00 | R1 | Survey, not research; not comparable |
| Cross-Lingual Humanoid | gwZ90hFSL2 | 1.00 | R1 | Not a methods paper; not comparable |
| KL Divergence GFlowNets | Uj0h13lVrR | 1.00 | R1 | Fundamentally flawed; LoRA-Mixer far superior |
| DLP-LoRA | I1VCj1l1Zn | 3.00 | R1 | Similar topic, weak baselines, limited comparison; LoRA-Mixer substantially better in evaluation breadth and baselines |
| Collective Model Intelligence | XVHXVdoV11 | 3.40 | R1 | Model merging; weaker experimental validation than LoRA-Mixer |
| UnoLoRA | 49ti6LOUw5 | 3.00 | R1 | Single-LoRA multi-task; LoRA-Mixer has stronger MoE contribution and broader evaluation |
| MOEfication by Experts as Masks | 762u1p9dgg | 3.40 | R1 | MoE sparsification; different focus, but similar novelty concerns |
| MoLE (Mixture of LoRA Experts) | uWvKBCYh4S | 5.00 | R1 | Direct predecessor; LoRA-Mixer extends with broader evaluation, SSM support, and RSL, but has unvalidated placement claim |
| MORE | LWvgajBmNH | 4.00 | R1 | Similar topic, limited benchmarks; LoRA-Mixer has better breadth but similar novelty gap |
| MoTE | uHTmx0nRfX | 4.75 | R1 | Task-specific embedding experts; rejected with similar novelty concerns |
| PERFT | PPjpGTPG5K | 5.33 | R1 | MoE PEFT framework; rejected for being vanilla combination; LoRA-Mixer has more specific contributions |
| HMoRA | lTkHiXeuDl | 6.00 | R1 | Closest accepted anchor; HMoRA had cleaner novelty (hierarchical routing, GJS loss) and all reviewers at 6; LoRA-Mixer's missing ablation pulls it below |
| MeteoRA | yOOJwR15xg | 6.20 | R1 | Accepted; had 28 LoRAs, efficient kernel, practical systems contribution; LoRA-Mixer has less systems novelty |
| Soft Merging (SMEAR) | QHzzAU7Qf9 | 6.00 | R1 | Different routing approach; rejected |
| Tight Clusters | Pu3c0209cx | 7.00 | R1 | Stronger theoretical contribution with clustering optimization; LoRA-Mixer below this tier |
| MoE++ | t7P5BUKcYv | 8.00 | R1 | Significantly stronger novelty (zero-computation experts); LoRA-Mixer clearly below |
| HiRA | TwJrTz9cRS | 8.00 | R1 | Strong PEFT contribution; LoRA-Mixer below |

**Round 1 bracket: 4.5 – 6.0**

**Narrowing analysis:** LoRA-Mixer's evaluation breadth (3 models including SSM, 15 benchmarks, plug-and-play, cross-model transfer) is notably stronger than the rejected papers in the 3.0-4.0 range (DLP-LoRA, MORE, UnoLoRA). This breadth pushes it above a 4.0. However, compared to accepted papers at 6.0 (HMoRA, SMEAR), LoRA-Mixer's core architectural claim is unvalidated by ablation, RSL is incremental, and the absence of variance reporting undermines confidence in the small-margin results. The paper reads as competent engineering with good breadth but claims that outrun the evidence. It sits at the boundary between borderline reject and borderline accept, with the missing ablation being the decisive gap.

**Final score: 5.0** — The paper has genuine practical value (plug-and-play, cross-model transfer, SSM support) and above-average evaluation breadth, placing it above the 3.0-4.0 reject tier. However, its core architectural contribution (projection-layer placement) lacks the ablation needed to validate it, RSL is essentially known entropy regularization with disproportionate theoretical framing, and the absence of variance reporting makes many claimed improvements unverifiable. These gaps prevent it from reaching the borderline-accept threshold of 6.0.

MY FINAL SCORE: <score>5.0</score>
MY FINAL DECISION: <decision>Reject</decision>