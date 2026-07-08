Now I have all the information I need. Let me compile my final review.

## Round 1 Bracket

Based on my comparison with calibration anchors, I bracket DiSTAR between **4.5 and 5.5**. 

Reasoning:
- Above rejected papers like VALL-E 2 (5.00) and Codec-LM Co-design (5.00) which had weaker novelty or more fundamental issues
- Below accepted papers like CLaM-TTS (6.40) and DiTTo-TTS (6.25) which had more thorough experimental validation
- Comparable to MaskGCT (5.25, Accept) which also had masked generative modeling but stronger ablations

## Round 2 — Narrowing

Within the 4.5–5.5 bracket, let me compare weighted items:

**DiSTAR's strongest positive weights (strengths):** Architecture (10.43), Heuristics (10.38), WER results (10.64), Subjective quality (9.91)

**DiSTAR's strongest negative weights (weaknesses):** 
- Missing component ablation: 0.67 (severe drag)
- SIM overclaiming: 0.73 (severe drag)
- Unsupported compute claims: 0.75 (severe drag)
- WER-below-resynthesis: 2.40 (moderate drag)

Comparing to VALL-E 2 (5.00, Reject): VALL-E 2 had highly negative weights on novelty (-4.40, -2.59) and weak baselines (-5.76). DiSTAR's novelty is stronger, but DiSTAR has more severe experimental gaps. DiSTAR edges slightly above VALL-E 2.

Comparing to MaskGCT (5.25, Accept): MaskGCT had novelty concerns (weight -2.30, -4.29) but strong demos and thorough experiments. DiSTAR has better novelty but weaker validation. 

Comparing to Codec-LM Co-design (5.00, Reject): That paper had weak novelty (-3.58, -3.69) and insufficient validation. DiSTAR has stronger novelty.

**Final score: 5.0.** The paper has genuine architectural novelty and strong results, but the experimental validation is too incomplete (no component ablation, unaddressed WER confound, unsupported compute claims, overstated SOTA claims) to fully support its contributions.

Now let me write the final review.

---

Actually, I should think more about the decision. A score of 5.0 with Reject feels right. The paper has important contributions but the experimental gaps prevent it from being acceptable in its current form.

Let me finalize everything and write the review.Now I have all the data needed. Let me compile the final review.

---

## Summary
DiSTAR presents a zero-shot TTS framework that couples an autoregressive language model (AR drafter) with a discrete masked diffusion model (MDM refiner) entirely in the RVQ code space, adapting the next-patch paradigm from continuous to discrete domains. The method is well-motivated, technically clean, and achieves strong WER and competitive subjective quality against leading baselines.

## Strengths
- **Sensible architectural synthesis (Sections 3.1–3.3):** The core idea — using a causal AR LM to draft a compact hidden sketch for the next patch, then completing the patch via discrete masked diffusion — is a natural and well-motivated adaptation of the next-patch paradigm (DiTAR) from the continuous to the discrete RVQ domain. The discrete setting avoids the optimization fragilities of high-dimensional continuous latents, preserves the [EOS] token for clean termination, and lets both the AR drafter and the diffusion refiner share the same code space, sidestepping inter-module mismatch.
- **RVQ-aware inference heuristics (Section 3.4):** The identification of a "tail-first" bias in patch-level masked decoding and the three mitigation strategies (layer-wise temperature shaping, position-wise temperature shaping, hybrid sampling) show thoughtful engineering that addresses a real failure mode specific to the RVQ+masked-diffusion setting.
- **Strong WER results (Table 1):** On LibriSpeech-PC, DiSTAR-medium (0.3B) achieves 1.66% WER vs. DiTAR (0.6B) at 2.39% and F5TTS at 2.02%. On SeedTTS test-en, it achieves 1.32% WER vs. DiTAR's 1.78% and F5TTS's 1.35%. These are robust improvements, especially given the smaller parameter budget.
- **Competitive subjective quality (Table 2):** DiSTAR achieves the best CMOS (0.22) and competitive SMOS (3.31) on SeedTTS test-en, suggesting genuine perceptual advantages in naturalness/robustness over strong baselines like CosyVoice 2, E2TTS, and F5TTS.

## Weaknesses

### Fatal
None.

### Major
1. **WER below the resynthesis ceiling is unexplained (Table 1).** DiSTAR-medium achieves 1.66% WER on LibriSpeech-PC when the RVQ resynthesis of original audio achieves only 1.83%, and human speech achieves 1.80%. On SeedTTS test-en, DiSTAR-medium achieves 1.32% WER vs. RVQ resynthesis at 1.71% and human at 1.47%. Since the RVQ codec reconstructs the *original* audio, its WER should bound what any generation system operating in that code space can achieve for faithful content reproduction. DiSTAR beating both resynthesis and human speech on the same metric means the metric (Whisper-large-v3) is likely measuring something other than pure content accuracy — clean synthetic speech may be transcribed more accurately than natural or codec-degraded speech. The paper provides no explanation or analysis of this phenomenon, which significantly weakens the headline robustness claim.

2. **Speaker similarity (SIM) is not state-of-the-art, contrary to the paper's framing.** The abstract (line 9: "surpasses state-of-the-art ... speaker/style consistency"), contributions list (line 37: "state-of-the-art ... speaker similarity"), and conclusion (line 263: "yield SOTA ... speaker similarity") all claim SOTA speaker similarity. However, objective SIM scores show DiSTAR-medium trailing E2TTS on both datasets (0.67 vs. 0.70 on LibriSpeech-PC; 0.66 vs. 0.71 on SeedTTS test-en). While subjective SMOS is competitive (3.31 vs. E2TTS's 3.29, with overlapping confidence intervals), the blanket SOTA claim for speaker similarity in the abstract and contributions is misleading. The paper's own text (line 209: "SIM on par with the best alternatives") is more measured, but this tension should be resolved by adjusting the high-level claims.

3. **Core architectural contribution is not ablated (Section 4.3).** The paper's central thesis is that combining an AR drafter with a masked diffusion refiner in the discrete RVQ space is beneficial. Yet the ablation study (Table 3) only varies decoding strategies (greedy vs. sampling, temperature parameters) on a single model — it does not isolate the contribution of either component. There is no experiment testing an AR-only variant (no masked diffusion, using an AR decoder for within-patch tokens) or a diffusion-only variant (no AR drafter, conditioning MDM directly on text and a sliding window of past codes). The paper frames its motivation around "the central question: Can we architect a generator that natively models RVQ's joint time-depth structure" (line 23), but the experiments do not test whether the proposed architecture answers that question better than simpler alternatives. This is a structural gap that prevents the reader from knowing whether the two-module complexity is justified.

4. **Inference cost claims are unsupported by evidence.** The paper states DiSTAR has "inference cost close to its continuous counterpart DiTAR" (line 31) and "comparable or lower computational cost" (line 37). The only quantitative evidence offered is parameter count (0.3B vs. 0.6B for DiTAR). However, DiSTAR uses NFE=24 diffusion steps vs. DiTAR's NFE=10, and runs both an AR LM forward pass and multiple MDM forward passes per patch. No latency, real-time factor (RTF), total FLOPs per utterance, or throughput numbers are reported. Parameter count alone is insufficient to substantiate computational cost claims.

### Minor
None.

### Trivial
None.

## Nice-to-Haves
- Add component-level ablations (AR-only without MDM, diffusion-only without AR drafter) to validate whether the two-module design is necessary. This is the single highest-leverage improvement.
- Provide actual latency/RTF/throughput numbers to ground the inference cost claims.
- Address the WER-below-resynthesis phenomenon: analyze whether Whisper systematically favors clean synthetic speech, or use a complementary metric (e.g., phoneme error rate on forced-aligned transcripts).
- Reframe the speaker similarity claims in the abstract and contributions to match the objective evidence (e.g., "competitive speaker similarity" rather than "SOTA speaker similarity").
- Add confidence intervals or error bars to objective metrics in Table 1.
- Include subjective evaluations on LibriSpeech-PC for completeness.

## Removed Points
These points from the input review were removed after verification against the paper:
1. *"DiTAR not re-run in same evaluation pipeline"* — REMOVED: The paper honestly marks DiTAR scores with ♦ and cites the original paper. The concern is speculation about potential pipeline differences, not an identified problem in the paper.
2. *"Subjective evaluation protocol underspecified (number of listeners, controlled conditions)"* — REMOVED: The appendix (which is stripped) may contain these details, and this level of specification is often omitted from the main paper.
3. *"DiSTAR-base vs. DiSTAR-medium scaling trajectory too narrow"* — REMOVED: Generic criticism that would apply to virtually any paper with two model sizes; the paper is not primarily a scaling study.
4. *Strengths about "addressing an important problem" and generic praise* — REMOVED: Too generic to retain as specific evidence.
5. *Speculation about WER confound being "the likely explanation"* — RETAINED but framed as a verifiable observation of the data (WER below resynthesis ceiling) rather than speculation about Whisper's internal behavior.

## Novel Insights
The review highlights an interesting tension: the discrete code space (RVQ) that makes DiSTAR's architecture tractable and clean also introduces a subtle evaluation confound — the same clean-synthetic-speech property that helps WER may partially decouple the metric from "faithful content reproduction" in the usual sense. This suggests that TTS papers reporting WER should routinely check against the resynthesis ceiling of their codec as a sanity check on the metric. The second insight is that the paper's architectural claim (AR + MDM) is its most distinctive contribution, yet it lacks the most basic form of support: a component ablation. This gap is more significant than any individual missing baseline or experiment because it connects directly to the paper's stated research question.

## Suggestions
- **Validate the architecture:** Add component ablations: (a) an AR-only decoder that predicts all RVQ layers within a patch autoregressively (e.g., via flattening or delay-pattern scheme), and (b) a diffusion-only model that conditions MDM directly on text + sliding window of past codes, skipping the AR drafter. If DiSTAR outperforms both, the two-module design is justified. If not, identify the regime where it helps.
- **Address the WER confound:** Report WER on a held-out set where resynthesis and human baselines are measured under identical conditions, or provide an analysis (e.g., per-utterance WER breakdown) showing the gap is consistent with known properties of Whisper on synthetic vs. natural speech.
- **Substantiate compute claims:** Report wall-clock generation time per utterance or RTF for DiSTAR vs. DiTAR vs. F5TTS at comparable settings.
- **Calibrate claims:** Adjust the abstract and contributions to say "competitive speaker similarity" unless stronger evidence (e.g., statistical significance over E2TTS on SIM) is provided.

## Score and Decision
**Calibration report:**

| Anchor | Path | Avg Score | Round | Itemized | Comparison |
|--------|------|-----------|-------|----------|------------|
| (low) | /home/.../gwZ90hFSL2.md | 1.00 | R1 | No | Unrelated paper; far below DiSTAR |
| Simple-TTS | /home/.../m4mwbPjOwb.md | 3.00 | R1 | No | Weaker novelty and results; DiSTAR is stronger |
| Fox-TTS | /home/.../pWdkM9NNCA.md | 3.00 | R1 | No | Weaker results; DiSTAR is stronger |
| VALL-E 2 | /home/.../0bcRCD7YUx.md | 5.00 | R2 | Yes | Similar score band; DiSTAR has stronger novelty but weaker validation |
| Codec-LM Co-design | /home/.../KCVv3tICvp.md | 5.00 | R2 | Yes | Similar; DiSTAR has better novelty |
| ControlSpeech | /home/.../zAogQOIphH.md | 5.20 | R1 | Yes | Similar; DiSTAR has cleaner architecture |
| MaskGCT | /home/.../ExuBFYtCQU.md | 5.25 | R2 | Yes | Similar masked-gen approach; MaskGCT had better ablations |
| DiTTo-TTS | /home/.../hQvX9MBowC.md | 6.25 | R1 | Yes | Stronger validation; DiSTAR has comparable novelty |
| HALL-E | /home/.../868masI331.md | 6.40 | R1 | Yes | Stronger empirical work; DiSTAR has better novelty |
| CLaM-TTS | /home/.../ofzeypWosV.md | 6.40 | R1 | Yes | Stronger validation overall |

**Weighted-item comparison:** DiSTAR's strength weights (10.43, 10.38, 10.64, 9.91) are comparable to accepted anchors like CLaM-TTS and MaskGCT. However, DiSTAR has three weaknesses with very low weights (0.67, 0.73, 0.75) indicating severe score drag — missing component ablation, SIM overclaiming, and unsupported compute claims — plus a moderate-drag weakness (2.40) for the unexplained WER confound. Accepted anchors at 5.25+ (MaskGCT, CLaM-TTS) had at most one or two such severe-drag items, and their most severe weaknesses were at higher weights (less drag) than DiSTAR's. This differential puts DiSTAR below those accepted papers but above clearly rejected papers like VALL-E 2 (5.00) which had severe novelty concerns.

**Round 1 bracket:** 4.5–5.5  
**Round 2 narrowing:** Below CLaM-TTS (6.40), MaskGCT (5.25), and DiTTo-TTS (6.25) due to larger experimental gaps; above VALL-E 2 (5.00) and Codec-LM Co-design (5.00) due to stronger architectural novelty.

**Final score: 5.0**

MY FINAL SCORE: <score>5.0</score>
MY FINAL DECISION: <decision>Reject</decision>