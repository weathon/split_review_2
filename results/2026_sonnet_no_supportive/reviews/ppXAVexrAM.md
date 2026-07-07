Now let me draft the review and then calibrate.Now I have enough to write the final review. My bracketing puts this paper at **4–6** based on the anchors:
- CCM-DiT (avg 3.0, rejected): simpler camera-control fine-tuning
- AR-1-to-3 (avg 5.0, rejected): closest analog — AR NVS from single image, also borderline
- NuHYh4YKNe (avg 6.25, accepted): AR model for spatial localization + view prediction, more novel

ARSS is more comprehensive than AR-1-to-3 (scene-level, full ablation suite, zero-shot eval) but has meaningful weaknesses: SEVA missing from Figure 6, mixed margins vs. SEVA confounded by training scale, Table 1 vs. Table 2 inconsistency. I'll narrow to **5.0**.

---

## Summary
ARSS introduces a GPT-style decoder-only autoregressive transformer for camera-conditioned novel view synthesis from a single image, claiming to be the first such framework. The method combines a video tokenizer (VidTok/FSQ) for temporally consistent discrete tokens, a camera autoencoder mapping Plücker raymaps to positional guidance tokens, and a hybrid spatial-only permutation strategy that randomizes token order within frames while preserving temporal order across frames. Results on RE10K, ACID, and zero-shot DL3DV are presented against several diffusion-based and transformer baselines.

## Strengths
- **Per-frame error accumulation analysis (Figure 6)**: Per-frame PSNR/SSIM/LPIPS across 17 frames with ARSS exhibiting flatter degradation slopes than LVSM, MotionCtrl, RayZer, and ViewCrafter — a concrete, specific result that directly motivates the causal AR design.
- **Ablation on tokenization strategy (Table 3)**: VQ image tokenizer vs. VidTok comparison is decisive: ~62% FVD improvement and ~3.5 dB PSNR gap clearly establish that video tokenization is load-bearing for temporal consistency.
- **Ablation on permutation strategy (Table 2)**: The three-way raster/full-perm/spatial-only comparison cleanly illustrates why the hybrid design is necessary; Figure 7 shows visible geometry degradation modes for each alternative.
- **Principled camera conditioning**: Plücker raymap with a geometry loss (Eq. 5) enforcing unit-length rays and ray-moment orthogonality is a principled, interpretable camera representation; pairing camera tokens with each visual token as positional instruction is architecturally elegant.

## Weaknesses

### Fatal
None.

### Major
- **SEVA absent from Figure 6 — the paper's central evidential gap**: SEVA is the closest competitor in Table 1 (matching or exceeding ARSS on SSIM and FID). Yet Figure 6, which is the paper's most direct justification for the causal AR approach, omits SEVA entirely and includes only weaker baselines (LVSM, MotionCtrl, RayZer, ViewCrafter). The claim in Section 4.2 that "our model maintains consistently highest or near-highest PSNR/SSIM at every timestep" cannot be substantiated without SEVA in that figure. Whether SEVA's per-frame quality degrades faster along the trajectory is precisely the question the paper needs to answer to validate its core thesis.

- **Inconsistent ARSS numbers between Table 1 and Tables 2/3**: Table 1 reports ARSS PSNR=19.02, SSIM=0.624 on RE10K; Table 2 (ablation, "ours" row) reports PSNR=19.22, SSIM=0.565 — PSNR is higher and SSIM is lower with no explanation provided. This discrepancy likely reflects different evaluation subsets or settings, but readers cannot determine which figures reflect the final system or whether the two comparisons are on an equal footing.

- **Mixed quantitative margins vs. SEVA with selective framing and confounded training scale**: On RE10K, ARSS achieves +0.29 dB PSNR but −6.6% SSIM and +1.3% higher FID compared to SEVA. On ACID, PSNR is marginally better (+0.16 dB) while SSIM and FID again favor SEVA. The paper (Section 4.2) characterizes only the favorable metrics ("higher-fidelity novel views (+1.1% PSNR, -21% LPIPS)") while labeling SSIM and FID disadvantages "minor geometric inconsistencies" — SSIM and FID are not minor metrics. Furthermore, the paper itself acknowledges SEVA "benefits from large-scale, high-resolution training data" while ARSS is "trained from scratch using limited public datasets," conflating architecture benefit with training scale advantage.

### Minor
- **No ablation on the camera autoencoder**: The paper ablates tokenization (Table 3) and permutation (Table 2) but never isolates the camera autoencoder's contribution. It is unclear how much of the camera-control quality stems from the Plücker raymap representation vs. the learned bottleneck vs. simply injecting per-token positional guidance. This is a notable gap given the camera autoencoder is presented as a key novel component (Section 3.2.2).

- **Resolution limitation inadequately contextualized**: All experiments run at 256×256. The paper does not clarify whether baselines were evaluated at their native resolution or at 256×256, which could systematically distort metric comparisons. This is acknowledged in a single sentence in the Discussion but deserves explicit treatment in the experimental setup.

- **Overclaimed conclusion in Discussion**: The Discussion states ARSS "outperforms state-of-the-art methods leveraging diffusion models and transformers," while the Abstract more accurately says "overall comparable." The stronger framing is not supported by Table 1 given SEVA's SSIM and FID advantages.

### Trivial
- None.

## Nice-to-Haves
- Add SEVA to Figure 6. If SEVA's per-frame quality degrades faster than ARSS, this single result provides the clearest possible justification for the AR approach and would substantially strengthen the paper.
- Provide a controlled comparison at matched training scale (e.g., fine-tuning SEVA on RE10K + ACID alone) to disentangle architecture benefit from data-scale benefit.
- The Introduction describes incremental extension of a generated trajectory (appending new views without regeneration) as a key advantage of AR over diffusion, but no experiment demonstrates this. A simple demo would be a strong, distinctive contribution.

## Removed Points
*These points are flagged to be removed; treat them with caution.*

- **Hyperparameters λ₁–λ₄ not reported**: Removed per rule against reproducibility nitpicks about undisclosed hyperparameters/trivial implementation details.
- **Eq. 7 appears cut off**: Removed per rule about parser artifacts not reflecting actual submission problems.
- **Contribution is "component assembly"**: Removed as a standalone weakness. Combining VidTok, LlamaGen, and Plücker rays into the first AR NVS framework is a legitimate first-mover contribution even if components are from prior work. The integration design (camera tokens as positional instruction tokens) is novel.

## Novel Insights
The most genuinely elegant insight in ARSS is that camera tokens — which encode 3D position via Plücker coordinates — naturally serve as the positional instruction tokens that prior AR image generation works (Pang et al., 2025; Yu et al., 2024a) introduced to enable random spatial permutation. This dual-purpose design is not merely convenient: it means the spatial shuffling trick that helps uni-directional models handle bi-directional image data is simultaneously providing the 3D geometric conditioning needed for view synthesis. The ablation in Table 2 and Figure 7 that shows why spatial-only (not temporal) permutation is correct — because temporal ordering ensures later views are generated after near views, preserving causal knowledge accumulation — is the paper's clearest conceptual contribution.

## Suggestions
1. **Include SEVA in Figure 6** — this is the single highest-leverage change the authors could make.
2. **Reconcile Table 1 and Table 2 ARSS scores** with an explicit note on evaluation subset or configuration differences.
3. **Clarify baseline evaluation resolution** in the experimental setup section.
4. **Revise the Discussion claim** to match the Abstract's more accurate "overall comparable" characterization, or add the experiments needed to support the stronger claim.

---

## Score and Decision

**Anchor comparison across rounds:**

| Path | Avg Score | Round | Comparison |
|---|---|---|---|
| `pOcGFvfgjS.md` (AR-1-to-3) | 5.00 | R1 | Closest analog: AR NVS from single image, object-centric, also borderline; ARSS has more complete evaluation but weaker thesis support |
| `15lk4nBXYb.md` (CCM-DiT) | 3.00 | R1 | Camera-control LoRA fine-tuning for video; simpler, lower contribution than ARSS |
| `NuHYh4YKNe.md` (GST) | 6.25 | R1 | Joint AR localization + view prediction; more novel joint task formulation, similarly mixed reviews |
| `wkbx7BRAsM.md` (AR Video Imitators) | 7.00 | R1 | Strong zero-shot AR video capability; deeper contribution than ARSS |
| `QQBPWtvtcn.md` (LVSM) | 7.67 | R1 | LVSM is a baseline in ARSS; clearly higher contribution, scalable architecture |
| `zDJf7fvdid.md` (Zero-shot NVS via video diffusion) | 6.00 | R1 | Training-free NVS via diffusion modulation; competitive contribution level |
| `VLuJL8cnGk.md` (3D-free meets 3D priors) | 5.00 | R1 | Single-image NVS combining 3D-free and 3D-based; similarly borderline |
| `hWlCc7Iksi.md` (ARVideo) | 3.40 | R1 | Autoregressive video representation pretraining; weaker contribution than ARSS |
| `CFOQd4tqn1.md` (Ctrl123) | 4.00 | R1 | Closed-loop diffusion NVS; below ARSS in novelty |

**Round 1 bracket**: 4 – 6. ARSS is clearly above the 3.0–3.5 band (more principled than CCM-DiT or ARVideo) and clearly below the 7.0+ band (LVSM, AR Video Imitators). AR-1-to-3 at 5.0 (rejected) is the closest analog — ARSS has a better evaluation suite and stronger ablations, but its central thesis remains insufficiently supported (SEVA absent from Figure 6, Table 1 vs. Table 2 inconsistency, mixed metrics vs. SEVA). This pushes ARSS slightly above a pure 5.0 borderline-reject toward 5.0–5.5.

**Round 2 narrowing**: The SEVA-absent-from-Figure-6 issue is a major evidential gap, not a fatal flaw. The ablations are stronger than AR-1-to-3's. The zero-shot DL3DV evaluation adds breadth. Final score: **5.0** — borderline reject.

MY FINAL SCORE: <score>5.0</score>
MY FINAL DECISION: <decision>Reject</decision>