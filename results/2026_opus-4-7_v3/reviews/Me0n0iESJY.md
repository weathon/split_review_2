Now let me re-read a few critical sections to verify specific claims about the ablation and "data-free" claim.Now I have a thorough understanding of the paper. Let me draft the review before calibration.Now let me perform Round 1 calibration — bracketing across score bands:Let me read a few key anchor papers to calibrate my scoring:Now I have a good sense of the calibration landscape. Let me form my bracket.

**Round 1 Bracket:** Based on the anchor papers:
- ATM (3.0): Fundamentally flawed framing, misconfigured baselines — OptMerge is clearly stronger.
- SUPERMERGE (4.33): Insufficient baselines, limited scope — OptMerge has broader coverage and stronger benchmark.
- "What Matters for Model Merging at Scale?" (5.33): Empirical study, limited insights, text-only — OptMerge covers MLLMs, modality merging, and provides checkpoints.
- "Realistic Evaluation of Model Merging" (5.33): Benchmark paper, no clear method trends — OptMerge has a more novel setting and a method contribution (even if modest).
- "WIDEN" (5.67): Clearer method but limited experiments — OptMerge has broader experiments but overclaimed method.

**Initial bracket: 5.0–6.5.** The benchmark is genuinely strong and fills a real gap. The method is competitive but overclaimed. The modality merging contribution is novel. The overclaiming of method results is the main concern pulling the paper down.

Now let me write the final review.

---

## Summary
This paper introduces (1) a benchmark for evaluating model merging algorithms on Multimodal LLMs, covering capability merging (VQA, Geometry, Chart, OCR, Grounding) across InternVL2.5-1B and Qwen2-VL-7B with both LoRA and full fine-tuning, plus modality merging (vision, audio, video) on Vicuna-7B; and (2) OptMerge, a method that stabilizes WUDI Merging's optimization-based formulation via low-rank denoising, mean initialization, and SGD. The paper tests 10 merging algorithms across four settings and provides a theoretical result (Theorem 3.1) linking fine-tuning intensity to merging performance.

## Strengths

- **The benchmark fills a genuine gap with concrete deliverables.** Prior MLLM merging work (AdaMMS, UQ-Merge) lacked standardized evaluation with clear task separation. This paper provides checkpoints for two architectures, ≥100K samples per task (Table 1), code, and standardized evaluation via VLMEvalKit/LMMs-Eval. The benchmark covers both LoRA and full fine-tuning, which is practically relevant since merging dynamics differ (e.g., Iso-C's catastrophic failure on LoRA in Table 3, dropping to 26.69 avg).

- **Modality merging is a practically valuable and novel contribution.** The finding that static merging of separately-trained vision-language, audio-language, and video-language models (Table 5) can match or outperform online composition methods (NaiveMC at 66.88, DAMC at 66.79) while using 1/3 the storage (static merging requires only one copy of parameters) is a concrete, useful result. TSV achieves 67.34 and OptMerge 67.00, both exceeding the online methods.

- **The diagnosis of WUDI Merging's instability is well-supported.** The observation that optimizing Eq. (1) on low-rank LoRA task vectors causes the merged vector's norm to blow up (Figure 3 geometric illustration, Figure 4 empirical verification showing WUDI's norm increasing from ~0.00012 to ~0.00027 while OptMerge stays flat) is clearly articulated, geometrically intuitive, and verified empirically.

- **Broad experimental coverage provides a useful reference for the community.** Ten merging algorithms, four evaluation settings (Tables 2, 3, 5, 6), scalability to 32B (Table 9), general benchmarks (Table 10 showing dramatic improvements), and computational comparisons (Table 7: 3.78h vs 24.56h, 21.97GB vs 256GB for Qwen2-VL-7B) collectively make this a thorough study.

- **Table 10 demonstrates strong emergent integrated capabilities.** On general multimodal QA benchmarks requiring multiple abilities, the merged model (OptMerge on InternVL2.5-1B) dramatically outperforms all individual models — e.g., ScienceQA: 91.89 vs best individual 76.54; DocVQA: 84.18 vs best individual 77.67. This is a compelling demonstration of merging value.

## Weaknesses

### Fatal
None.

### Major

- **OptMerge does not consistently outperform baselines, undermining the method's headline claims.** In Table 3 (Qwen2-VL, LoRA — one of two primary capability-merging settings), WUDI Merging achieves 63.65 avg vs OptMerge's 63.30. In Table 5 (modality merging), TSV Merging achieves 67.34 avg vs OptMerge's 67.00. In Table 2 (InternVL2.5, full FT), OptMerge edges WUDI by only 0.44 points (57.44 vs 57.00). The abstract's claim of "an average performance gain of 2.48%" appears to derive from the ablation (Table 4), where WUDI is configured at 58.65 — substantially lower than the 63.65 that fully-tuned WUDI achieves in Table 3. This means the headline improvement is measured against a suboptimally configured baseline rather than the best available WUDI. This is a significant evidential issue: the paper's central method claim is not supported by the main experimental tables.

- **The "data-free method that requires no hyperparameter search" claim (end of Section 2) contradicts the experimental protocol.** Section 5.1 states: "we determine the optimal merging coefficient λ by searching within the range [0.1, 0.3, 0.5, 0.7, 1.0, 1.5]." This search requires a validation set with labeled data to evaluate each λ. While all methods undergo the same search (preserving comparison fairness), the paper cannot simultaneously claim "data-free" and "no hyperparameter search" while requiring validation-based λ selection. This misrepresentation weakens credibility.

### Minor

- **No variance or significance reporting on any result.** Across Tables 2, 3, 5, 6, 8, and 9, no standard deviations, confidence intervals, or significance tests are reported. Given that OptMerge's margins of improvement (when it does win) range from 0.12 to 1.9 points, the absence of variance estimates makes it difficult to assess whether observed differences are meaningful. This is particularly concerning for the 0.44-point win in Table 2 and 0.12-point win in Table 6.

- **Table 9 (Qwen2.5-VL-32B) evaluates only OptMerge; no other merging baselines are shown.** This makes it impossible to assess whether OptMerge's advantage persists at scale or whether simpler methods (e.g., Task Arithmetic, TIES w/ DARE) would also perform well. The scalability claim is therefore unsupported by comparative evidence.

- **The ablation (Table 4) obscures the primary mechanism.** SGD alone hurts performance on Qwen2-VL by −9.77%; the gain comes primarily from mean initialization (+4.43%). Low-rank adds only 0.22% more. The paper would be more informative if it clearly identified mean initialization as the dominant contribution rather than presenting all three techniques as equally important components of an integrated framework.

### Trivial
None.

## Nice-to-Haves
- Investigate why TSV outperforms OptMerge in modality merging — the paper notes TSV's orthogonalization mitigates modal conflicts (Sec 5.2) but does not analyze this further. This would be a distinctive insight.
- Include at least Task Arithmetic and WUDI at 32B scale in Table 9 to support the scalability claim.
- Report the ablation against the best-tuned WUDI configuration (with the same λ search), not the default WUDI.
- Discuss failure modes more systematically — the remark about Qwen2.5-Math/Coder is interesting but unsupported by data.

## Removed Points
*These points are flagged to be removed; treat them with caution.*

- **"Theorem 3.1 has limited practical utility due to unknown constants"**: The theorem's contribution is a theoretical explanation of the fine-tuning–merging relationship. Demanding that the authors estimate $C_i$, $\delta$, $L$, $\mu$ for benchmark models is beyond the theorem's intended scope. The qualitative guidance (control $\eta T$) is sufficient for benchmark design.
- **"No ablation isolating the input subspace substitution ($\Sigma_{1:k}V_{1:k}^\top$ for $x_{i,l}$)"**: This is a detailed architectural choice that is implicitly covered by the overall ablation. Demanding separate ablation of every design decision is excessive.
- **"The paper frames OptMerge as the star of modality merging when TSV wins"**: On re-reading Sec 5.2, the paper actually says "the best merging method even outperforms these online composition methods" without specifying OptMerge — this phrasing correctly refers to TSV. The framing is defensible.
- **"Remark about Qwen2.5-Math/Coder not backed by data"**: It is presented as an illustrative remark, not a core claim. Removing.

## Novel Insights
The most genuinely novel finding is that static merging of modality-specific models (vision, audio, video) sharing a common LLM backbone can match or exceed online composition methods at 1/3 the storage cost. This has immediate practical implications for building omni-modal models without retraining. The diagnosis of WUDI's norm blow-up on low-rank LoRA task vectors is a concrete, reproducible failure mode that extends understanding of optimization-based merging.

## Suggestions
- Recalibrate the abstract and contributions to match the evidence: position OptMerge as a stabilization of optimization-based merging that is competitive across settings, not uniformly dominant. Acknowledge settings where TSV or WUDI outperform.
- Foreground the benchmark as the primary contribution, with OptMerge as a secondary algorithmic contribution.
- Run the ablation against WUDI with the same λ search to get a fair improvement estimate.
- Add at least 2–3 baselines to Table 9 at 32B scale.
- Either adopt a truly data-free λ selection criterion (e.g., norm-based) or drop the "no hyperparameter search" claim.

## Score and Decision

### Anchor Comparison

| Paper | Avg Score | Round | Comparison to OptMerge |
|---|---|---|---|
| 8QTpYC4smR (Systematic Review of LLMs) | 1.00 | R1 | Pure survey, not comparable — OptMerge is far stronger |
| 5kMwiMnUip (NEMESIS Jailbreaking) | 1.40 | R1 | Fundamentally flawed paper — OptMerge is far stronger |
| gwZ90hFSL2 (Cross-Lingual Humanoid) | 1.00 | R1 | Not a real research contribution — OptMerge is far stronger |
| u1cQYxRI1H (IC-Light) | 0.50* | R1 | Mismatch on score extraction; not comparable |
| lNtio1tdbL (ATM: Alternating Tuning) | 3.00 | R1 | Fundamentally flawed framing; OptMerge has much stronger benchmark and clearer contributions |
| HfJxXbXlYJ (LLM2CLIP) | 3.00 | R1 | Different domain; OptMerge has stronger empirical coverage |
| gNoqEdT2wO (Multimodal Class-Incremental) | 2.33 | R1 | Lacking benchmark standardization; OptMerge far more complete |
| cagNCwQEEN (Hybrid State Space Multimodal) | 3.40 | R1 | Different focus; OptMerge benchmark is more impactful |
| fvUVe2gJh0 (What Matters for Merging at Scale) | 5.33 | R1 | Closest comparable: also benchmark-style merging study, text-only, no code/checkpoints released. OptMerge covers MLLMs and modality merging — slightly stronger. |
| Bq3fEAGXUL (Realistic Eval of Merging) | 5.33 | R1 | Benchmark paper with no clear method trends. OptMerge provides more novel setting + method. Comparable but OptMerge somewhat stronger. |
| lIdc5DUplq (SUPERMERGE) | 4.33 | R1 | Gradient-based merging with insufficient baselines. OptMerge has broader coverage. |
| f1uXrAjpOH (Open-vocab Multimodal Emotion) | 5.40 | R1 | Different domain. Comparable contribution level. |
| 2rWbKbmOuM (MEGA-Bench) | 7.00 | R1 | Much larger-scale benchmark (500+ tasks). OptMerge's benchmark is more focused but less ambitious. |
| 2pvMZKGYDR (WIDEN: Extend Merging FT to PT) | 5.67 | R1 | Model merging for LLMs. Clearer method contribution but narrower experiments. Comparable. |
| vJ0axKTh7t (Labyrinth of Links) | 6.25 | R1 | Accepted MLLM benchmark — more novel evaluation angle. OptMerge slightly weaker overall. |
| k5VHHgsRbi (MME-RealWorld) | 6.80 | R1 | Larger-scale MLLM benchmark, accepted. OptMerge's focus is narrower. |
| HnhNRrLPwm (MMIE) | 8.00 | R1 | Major MLLM benchmark, much larger scale. OptMerge doesn't reach this level. |
| SI2hI0frk6 (Transfusion) | 7.60 | R1 | Foundational multimodal architecture. Different class of contribution. |

**Round 1 bracket: 5.0–6.5**

**Narrowing within the bracket:** The paper's benchmark contribution is genuine and fills a real gap in the MLLM merging space, making it stronger than the rejected merging benchmark papers (5.33 range). However, the overclaiming of method results (the "2.48%" headline claim contradicted by Table 3 where WUDI beats OptMerge) and the "data-free" misrepresentation are credibility issues that pull the paper below the accepted benchmark papers (6.25–6.80 range). The benchmark alone is valuable but the method contribution is weaker than claimed.

The paper sits in the 5.5 range: stronger than the 5.33 rejected merging papers due to its MLLM focus, modality merging novelty, and released artifacts, but weaker than accepted benchmark papers due to overclaimed method results and missing statistical rigor.

**Final score: 5.5** — The benchmark is a genuine contribution that the community would benefit from, and the modality merging finding is novel. However, the method's headline claim is not supported by its own tables, and the "data-free" framing is misleading. If the authors recalibrate claims to match evidence, this would be a solid borderline-accept paper. As submitted, the credibility gap between claims and evidence tips the balance toward reject.

MY FINAL SCORE: <score>5.5</score>
MY FINAL DECISION: <decision>Reject</decision>