Now let me read the rest of the paper to verify remaining claims about training setup and specific sections:Now I have thoroughly read the paper. Let me draft the review before calibration.Now let me run Round 1 calibration — bracketing search across score bands:Let me read key anchor papers for calibration:Now let me also read the closely relevant anchor at score 5.0 more carefully to finalize my bracket:Now I have sufficient calibration data. Let me write the final consolidated review.

## Summary
IRIS proposes using Negative Self-Certainty (NSC) — the negated KL divergence between a uniform distribution and the model's output distribution — as an intrinsic reward for RL fine-tuning of autoregressive text-to-image models. The key finding is that, contrary to text-reasoning tasks where self-certainty increases with RL training, image generation quality correlates with *decreased* self-certainty. The method is evaluated on Janus-Pro (1B and 7B) against T2I-R1 (which uses four external reward models) on GenEval, T2I-CompBench, and WISE benchmarks, showing substantial improvement over the base model without any external supervision.

## Strengths
- **Novel and well-documented empirical observation (Fig 2).** The finding that self-certainty behaves oppositely in image generation vs. text reasoning is concrete, falsifiable, and directly demonstrated: external-reward RL training decreases image-token self-certainty while increasing text-token self-certainty. This challenges the "self-certainty is always good" framing of prior work (Zhao et al., 2025b; Zhang et al., 2025a) and could inform future reward design for multimodal models.

- **Thorough ablation design (Sec 4.3, Figs 5–9).** Five ablation dimensions — maximize/minimize image SC, maximize/minimize text SC, forward/backward KL, RL vs. direct optimization, with/without CoT — each isolate a single design choice with clear evidence. The finding that maximizing image self-certainty causes rapid degradation (Fig 6, grey line dropping sharply after 200 steps) is a particularly compelling negative result that directly supports the core claim.

- **Practical value of zero external supervision.** IRIS achieves substantial improvement over the base model (e.g., +9.1% GenEval, +28.8% WISE for 1B) without requiring any external reward model, human labels, or domain-specific verifier. This is genuinely useful for domains where reward models are unavailable or poorly calibrated.

- **Identification of T2I-R1 chat-template bug (Sec 4.1, final paragraph).** The discovery that T2I-R1's official implementation uses the wrong chat template for Janus-Pro is a constructive community contribution that aids reproducibility.

## Weaknesses

### Fatal
None.

### Major
- **Abstract overclaims "competitive with or superior to external rewards."** Table 1 shows T2I-R1 consistently outperforms IRIS on overall scores across all benchmarks and model sizes: GenEval 1B (0.72 vs 0.75), GenEval 7B (0.77 vs 0.78), T2I-CompBench 7B (IRIS trails on all 6 sub-metrics), WISE 1B (0.37 vs 0.38), WISE 7B (0.48 vs 0.50). The body text uses the more measured term "comparable" (Sec 4.2: "achieving results comparable to its counterpart that uses an external reward"), but the abstract's "superior to" is not supported by the best-checkpoint comparison in Table 1. The claim of superiority in specific WISE sub-categories (biology, physics, chemistry) is real but cherry-picked; T2I-R1 wins on more sub-categories overall. The honest framing is that IRIS achieves roughly 60–80% of the improvement of four combined external reward models, using zero external supervision — which is still a meaningful contribution, but a different claim than the abstract makes.

- **No human evaluation despite explicit human-preference claims.** Fig 1 caption asserts images with lower self-certainty are "more preferred by humans," and the abstract references alignment with "human preferences." Yet all evaluation is automated (GenEval uses object detection, T2I-CompBench uses CLIP/BLIP metrics, WISE uses VQA scoring). For a paper whose central narrative ties NSC to human-preferred image quality, even a modest pairwise comparison study (e.g., 100–200 prompts) would be expected. The automated benchmarks are reasonable for measuring compositional correctness, but they do not validate the human-preference claim.

### Minor
- **Mechanistic understanding is shallow.** The paper establishes a robust empirical correlation (Fig 2) and confirms design choices via ablations, but offers no analysis of *why* lower self-certainty produces better images. The narrative that "overly confident models generate uniform and plain figures" (Sec 3.2) is plausible but untested. For instance: does the model use a broader portion of the VQ codebook? Does token-level diversity increase in a measurable way? Without this analysis, the contribution remains "flipping the sign works" rather than "we understand why the sign should be flipped in this modality."

- **Single model family limits generality.** Only Janus-Pro (1B and 7B) is tested. The paper acknowledges this limitation in Sec 4.4, noting the diversity of T2I architectures, but testing even one additional autoregressive T2I model (e.g., Show-o, which appears in the baselines) would substantially strengthen the generality claim.

- **Tension in text-token self-certainty direction.** The paper uses NSC for both text and image tokens, but Fig 2 shows text self-certainty *increases* during math-reasoning RL. The explanation in Sec 3.2 — that T2I text descriptions require "exploration" while math requires "precision" — is speculative. A simple experiment measuring text-token entropy/self-certainty changes during IRIS training and comparing to the math-reasoning case would directly address this.

### Trivial
None.

## Nice-to-Haves
- A mechanistic analysis of how visual token distributions change under NSC training (e.g., VQ codebook usage histograms comparing base, IRIS-trained, and SC-maximized models).
- Human preference study, even small-scale, to support the human-preference claims.
- Testing on at least one additional autoregressive T2I model.
- FID/IS or distributional quality metrics to complement task-specific benchmarks.
- Analysis of where IRIS fails relative to external rewards (spatial/counting tasks) as an informative finding about what different reward signals teach the model.

## Removed Points
*These points were flagged for removal; treat them with caution.*

- **Ablation metrics biased toward T2I-R1.** The reviewer raised a concern that using T2I-R1's training rewards as ablation evaluation metrics could create bias. However, the paper directly addresses this in Sec 4.3: "we never use these reward models in the training objectives, so they can be simple and unbiased metrics to evaluate the performance." This is a reasonable response — the metrics are external to IRIS's training loop. Removed as addressed.

- **Length-bias argument for forward KL doesn't apply to fixed-length image tokens.** While technically correct (image tokens form a fixed grid), the paper provides multiple justifications for forward KL including mode-covering behavior and empirical evidence (Fig 8). The length-bias argument applies to the text (CoT) tokens which do vary in length. Removed as insufficiently impactful.

- **GRPO confound between CoT text diversity and image quality.** The reviewer suggested the advantage signal from 8 text strings × 1 image may mix text and image variation. This is speculative and not clearly demonstrated as a problem — it is a feature of the GRPO design that exploration happens through diverse CoTs. Removed as speculative.

- **Missing FID/IS metrics.** These are nice-to-have but not standard in the evaluation framework used by the paper and its baselines (T2I-R1). Moved to nice-to-haves.

- **Missing training prompt distribution details.** The paper states it follows T2I-R1's protocol (Sec 4.1). This is a reproducibility nitpick. Removed.

- **Percentage improvements potentially misleading.** The paper clearly states these are relative to the base model ("IRIS boosts the performance of the Janus-Pro 1B model by 9.1%..."), not relative to T2I-R1. The reviewer's concern is about potential misreading, not actual misrepresentation. Removed.

## Novel Insights
The paper's genuinely novel insight is the task-dependent directionality of self-certainty: in text reasoning, higher self-certainty correlates with better performance, while in image generation, lower self-certainty correlates with better quality. The ablation showing that maximizing image self-certainty causes rapid performance degradation (Fig 6) provides direct causal evidence for this asymmetry. This observation could serve as a useful guideline for future intrinsic reward design in multimodal generative models, particularly the principle that creative/generative tasks may benefit from uncertainty-maximizing rewards while precision tasks benefit from certainty-maximizing ones.

## Suggestions
1. **Recalibrate the abstract claim** from "competitive with or superior to external rewards" to language that accurately reflects Table 1, e.g., "achieves a large fraction of the improvement of external reward methods, without any external supervision."
2. **Add mechanistic analysis** of how visual token distributions change under NSC training — even a histogram of VQ codebook usage would provide the missing "why."
3. **Add a small-scale human preference study** to validate the human-preference claims that are central to the paper's narrative.
4. **Frame the category-level analysis** (Sec 4.2, where IRIS outperforms T2I-R1 on natural science but underperforms on spatial/counting tasks) as an informative finding about the complementary nature of intrinsic vs. external rewards, rather than downplaying the differences.

## Score and Decision

### Calibration Anchors

| Paper | Path | Avg Score | Round | Comparison to IRIS |
|---|---|---|---|---|
| KL Divergence for Stochastic GFlowNets | Uj0h13lVrR | 1.00 | R1 | Fundamental methodological issues; IRIS is far stronger |
| Clothing-Irrelevant Lifelong Person ReID | 5lUdTogEL3 | 1.00 | R1 | No real contribution; IRIS is far stronger |
| Humanoid Robots Cross-Lingual | gwZ90hFSL2 | 1.00 | R1 | Not a real research paper; IRIS is far stronger |
| GAN with CLIP for T2I | oOa3ZCtMjJ | 3.00 | R1 | Incremental GAN+CLIP work; IRIS has a more novel observation |
| Data Extrapolation for T2I | TJHB4sSVZM | 3.40 | R1 | Poor presentation and limited novelty; IRIS is stronger |
| Knowledge Enhanced Fashion Captioning | ZVOGMy8Sd8 | 3.00 | R1 | Limited scope and novelty; IRIS is stronger |
| Vision-Based Grasping Goal-Conditioned | sXF5P4N7e8 | 3.00 | R1 | Different domain, limited contribution; IRIS is stronger |
| Mitigating Hallucination with Human-Free RL | bO31lfEdos | 5.00 | R1 | **Closest match**: also human-free RL for vision-language, single model, some overclaiming. IRIS has a more novel core observation and better ablations, but similar limitations. IRIS is at or slightly above. |
| Fine-grained T2I with Semantic Refinement | RauUgiw7VX | 4.75 | R1 | Limited novelty in diffusion refinement; IRIS has more novelty |
| Dice-GAN | 5187wrocJq | 4.25 | R1 | GAN-based T2I with limited novelty; IRIS is stronger |
| Lost in Translation: Conceptual Blind Spots | vb3O9jxTLc | 4.00 | R1 | Analysis paper with limited solution; IRIS has a more complete method |
| Test-Time Adaptation with CLIP Reward | kIP0duasBb | 6.67 | R1 | Solid method across tasks, well-supported. IRIS has a more novel observation but weaker evidence-claim alignment. IRIS is below. |
| Confidence-aware Reward for T2I | Let8OMe20n | 6.00 | R1 | **Key comparison**: Also T2I reward optimization, accepted with human evaluation and measured claims. IRIS lacks human evaluation and overclaims. IRIS is at or slightly below. |
| CertainlyUncertain Benchmark | cQ25MQQSNI | 6.00 | R1 | Uncertainty benchmark, different scope. Similar rigor level. |
| SelfEval Generative Models | RcANissyP4 | 5.67 | R1 | Interesting self-evaluation idea, borderline. Comparable to IRIS. |
| Transfusion | SI2hI0frk6 | 7.60 | R1 | Strong multimodal paper with scaling laws and comprehensive evaluation. IRIS is well below. |
| Würstchen | gU58d5QeGv | 8.00 | R1 | Strong architectural contribution with efficiency gains. IRIS is well below. |
| IC-Light | u1cQYxRI1H | 10.00* | R1 | Exceptional paper; IRIS is far below. (*Note: retrieval similarity was low; this paper's actual score of 10 reflects a different caliber.) |

### Scoring Rationale

**Round 1 bracket: 5.0–6.0.** IRIS sits above the score-5.0 "Mitigating Hallucination" paper due to a more novel core observation and more thorough ablations, but below the score-6.0 "Confidence-aware Reward" paper which had human evaluation and more measured claims. The paper's novel observation about self-certainty direction reversal is a genuine contribution, but the overclaimed abstract, absent human evaluation, and single-model-family limitation prevent it from reaching borderline accept.

**Final score: 5.5.** The novel observation and thorough ablations push it above the 5.0 anchor, but the major gap between claims and evidence (abstract says "superior to" while Table 1 shows consistent underperformance) and the missing human evaluation for a paper centered on human preference alignment keep it below the 6.0 threshold. The contribution is real but the execution and framing have notable gaps.

**Decision: Reject.** The paper makes a genuinely interesting observation and proposes a practical method, but the overclaimed framing and lack of human evaluation for a human-preference-centered narrative are significant issues that should be addressed before acceptance.

MY FINAL SCORE: <score>5.5</score>
MY FINAL DECISION: <decision>Reject</decision>