Now let me verify a few more specific claims from the reviewer. Let me check the conclusion section and any remaining content.Now I have a comprehensive understanding of the paper. Let me draft the review before calibration.Now let me run Round 1 calibration — bracketing across score bands:Let me read the most topically relevant anchors to calibrate:Now I have enough calibration data. Let me form my bracket.

**Round 1 Bracket:**
- Score < 1.5: Strong reject papers with fundamental methodology problems or survey-only papers. AdcVSR is clearly far above this.
- Score 1.5–3.5: Papers like Self-distillation for diffusion (3.0) and VideoDiT (2.5), rejected for limited novelty. AdcVSR is clearly stronger.
- Score 3.5–5.5: AddSR (5.0) and DFOSD (4.75) — both rejected image SR papers with similar topics but weaker novelty and evaluation. AdcVSR is stronger: it tackles the harder video problem, has the 2D+1D insight, creative dual-head discriminator, and 10 baselines.
- Score 5.5–7.5: Video inverse problems via image diffusion (6.50, accepted) and adversarial score identity distillation (6.25, accepted). These have clean conceptual contributions. AdcVSR has stronger practical impact but weaker evaluation of its core claim.
- Score 7.5–8.5: Papers with comprehensive evaluation and strong theoretical grounding. AdcVSR's evaluation gaps prevent it from reaching here.

**Initial bracket: 5.5–7.0**

The paper is clearly above the rejected 5.0-level SR papers (AddSR, DFOSD) due to stronger novelty and practical contribution, but the E_warp* reliance and split ablations prevent it from matching the stronger accepted papers at 6.5+.

Now let me write the final consolidated review:

---

## Summary
This paper proposes AdcVSR, a compressed diffusion model for real-world video super-resolution that distills a large 3D DiT teacher (DOVE, 10.55B params) into a compact "2D + 1D" student (0.57B params). The two key contributions are: (1) an architectural decomposition using a pruned 2D Stable Diffusion backbone for detail synthesis augmented with lightweight 1D temporal convolutions for consistency, and (2) a dual-head, dual-discriminator adversarial distillation scheme with five curated data types that disentangles detail richness and temporal consistency objectives. The model achieves 95% parameter reduction and 8× speedup with competitive video quality.

## Strengths

- **Well-motivated and validated "2D + 1D" architectural decomposition (Sec. 3.2, Table 2).** The insight that in conditional video SR the LR input already carries structural and temporal information—making heavy 3D attention largely redundant—is both principled and well-supported. Table 2 shows the 2D+1D design (0.55B params) closes the DISTS gap with a pruned 3D DOVE (8.36B params) to just 0.0014 while achieving better E_warp* (1.67 vs 2.53) at 7% of the parameters. This is a genuinely useful finding for the model compression community.

- **Creative dual-head discriminator design with curated data types (Sec. 3.3, Eqs. 4–5, Table 3).** The five data types—student outputs, real videos, temporally shuffled videos, repeated images, and randomly sampled images—with head-specific labels that isolate detail and consistency dimensions represent thoughtful engineering. Table 3 validates both components: removing dual-head increases E_warp* from 2.22 to 6.32; removing dual-domain reduces CLIPIQA from 0.6861 to 0.6421.

- **Dramatic and well-documented efficiency gains (Table 1, Fig. 4).** The headline numbers—95% parameter reduction, 8× speedup over DOVE, 0.55s inference for 25 frames at 512×512 on a specified GPU (H20)—are substantial, practically meaningful, and reported with sufficient specificity for reproduction.

- **Honest and self-aware reporting.** The paper does not hide that image SR models (PiSA-SR, HYPIR) outperform AdcVSR on several no-reference quality metrics (Table 1), and uses this observation constructively to validate hypothesis (1) about 2D backbones' detail generation capacity (Sec. 4.2, paragraph 3).

## Weaknesses

### Fatal
None

### Major

- **Insufficient investigation of whether low E_warp* reflects genuine temporal coherence vs. temporal smoothing (Table 1).** AdcVSR achieves E_warp* = 1.67 on UDM10, substantially lower than its teacher DOVE (2.22), non-generative RealBasicVSR (3.36), and multi-step STAR (2.37). A distilled student dramatically surpassing its teacher and all other methods on a key metric demands investigation of whether the 1D temporal convolutions impose a smoothing bias that reduces inter-frame variation in a way that flatters E_warp*. The paper's strong no-reference quality scores (CLIPIQA 0.6818, MUSIQ 63.88) partially mitigate this concern—if AdcVSR were heavily over-smoothing, these would be low—but the paper provides no direct analysis (e.g., per-frame texture variance, detail energy comparison with DOVE) to distinguish the favorable from unfavorable explanations. For a paper positioning the detail-consistency tradeoff as its core contribution, this evidential gap matters.

- **Over-reliance on a single proxy metric (E_warp*) for the consistency axis of the paper's central claim.** E_warp* is a flow-warping-based pixel-level metric with known sensitivity to smoothing and dependence on optical flow estimation quality. The DOVER metric captures some video quality aspect but conflates multiple dimensions and is not specifically a temporal consistency metric. There is no user study and no alternative temporal consistency metric. For a paper that claims to "balance" detail richness and temporal consistency as its core contribution, the consistency side rests on thin evidence.

### Minor

- **Ablation studies conducted on three different datasets without justification (Tables 2–4).** Table 2 (architecture) uses UDM10, Table 3 (discriminator) uses YouHQ40, Table 4 (distillation) uses MVSR4x. While the paper notes appendix results exist, this split makes it impossible to assess component interactions or consistency across datasets from the main text alone. This is a presentation issue rather than a structural flaw, but it weakens the ablation narrative.

- **Main paper results cover only 2 of 6 test datasets (Table 1).** For a paper claiming "extensive experiments," showing UDM10 and VideoLQ while deferring SPMCS, YouHQ40, RealVSR, and MVSR4x entirely to the appendix feels thin for the main body, though this is mitigated by the appendix presumably containing complete results.

- **Conclusion mildly overclaims scope.** The conclusion states the work "provides a systematic recipe for building efficient video reconstruction systems" (Sec. 5), but the paper demonstrates one specific compression path (DOVE → AdcVSR) and does not establish general principles applicable to other architectures or tasks.

### Trivial
None

## Nice-to-Haves

- Sensitivity analysis of 1D temporal convolution design choices: kernel size (3 vs. 5 vs. 7), number of inserted layers, and behavior for longer sequences (50+ frames vs. the fixed 25 used throughout).
- Ablation on the y_d=0 labeling choice for real videos (Eq. 5)—what happens if real videos are also labeled "real" for the detail head?
- A user study specifically targeting flicker perception would substantially strengthen the consistency claim.
- Analysis of per-frame detail variance or texture energy alongside E_warp* to demonstrate detail quality is preserved.
- A brief limitations section discussing failure cases and degradation types where the 1D convolutions' limited temporal receptive field may cause problems.

## Removed Points

*These points are flagged to be removed; treat them with caution.*

- **Criticism that the detail-consistency "conflict" is presented as established fact without the paper's own controlled demonstration:** The paper cites multiple prior works (Chu et al., 2020; Sun et al., 2025; Li et al., 2025c; Xu et al., 2025) observing this tradeoff, and Table 3's single-head result (E_warp* 6.32 vs. 2.22 for dual-head) provides direct empirical evidence. Removed as the paper addresses this sufficiently.
- **Criticism about the discriminator learning rate (1e-7 vs 1e-5) lacking justification:** This is a reproducibility detail that the paper does report. Demanding justification for every hyperparameter choice is excessive for an empirical paper.
- **Criticism about the introduction not providing a controlled demonstration that single-head discriminators "necessarily" collapse:** Table 3 provides empirical evidence, which is sufficient for an empirical methods paper. The paper does not claim "necessarily"—it states the discriminator "often tends to prioritize one aspect."

## Novel Insights

The paper's key architectural insight—that in conditional video SR, the LR input already provides sufficient structural and temporal context to make heavy 3D spatio-temporal attention redundant, enabling a "2D + 1D" decomposition—is well-validated and could inform future model compression work beyond this specific setting. The dual-head discriminator design with curated data types that independently vary detail and consistency provides a potentially transferable framework for disentangling competing objectives in adversarial training for video tasks.

## Suggestions

- **Highest priority:** Investigate whether low E_warp* reflects genuine temporal coherence vs. smoothing by computing per-frame texture energy or detail variance and comparing to DOVE. Even a brief analysis in a rebuttal showing that detail statistics are preserved would substantially address the main concern.
- Consolidate ablation studies onto a single dataset (or report all three ablations on all datasets in the main paper) to demonstrate component interactions and cross-dataset consistency.
- Add a brief limitations section discussing failure cases, particularly around the 1D convolutions' limited temporal receptive field for long sequences.
- Tone down the conclusion's claims about "systematic recipes" to match the paper's actual scope.

## Score and Decision

### Calibration Anchors

| Paper | Path | Avg Score | Round | Comparison to AdcVSR |
|-------|------|-----------|-------|---------------------|
| Self-distillation for diffusion models | QKqWnNkwPL | 3.00 | R1 | Rejected for limited novelty; AdcVSR has substantially more novel contributions and stronger validation. |
| VideoDiT | lvgsPjRtLM | 2.50 | R1 | Rejected for weak contribution; AdcVSR is far stronger in both novelty and practical impact. |
| Superposition of Diffusion Models | 2o58Mbqkd2 | 3.25 | R1 | Different topic (model combination); AdcVSR is stronger in experimental validation. |
| Sample what you can't compress | vK8C37eHXM | 3.20 | R1 | Rejected for marginal optimization; AdcVSR has clearer contributions. |
| AddSR (Adversarial Diffusion Distillation for SR) | BpKbKeY0La | 5.00 | R1 | Most similar paper; rejected for sacrificing fidelity and limited novelty. AdcVSR is clearly stronger: addresses harder video problem, more novel dual-head design, 10 baselines. |
| DFOSD (Distillation-Free One-Step SR) | 2ogxyVlHmi | 4.75 | R1 | Similar topic (one-step image SR); rejected for marginal novelty. AdcVSR has more distinct contributions. |
| Arbitrary-scale SR from Diffusion | QO3yH7X8JJ | 5.25 | R1 | Rejected for insufficient novelty; AdcVSR has stronger practical gains. |
| Beyond Transformations (SR augmentation) | JmGEZXkCH3 | 3.67 | R1 | Rejected for weak evaluation; AdcVSR is clearly stronger. |
| Does Diffusion Beat GAN in SR | 46mbA3vu25 | 5.75 | R1 | Rejected comparative study; different paper type. AdcVSR offers more practical value. |
| Adversarial Score Identity Distillation | lS2SGfWizd | 6.25 | R1 | Accepted; stronger theoretical grounding. AdcVSR has comparable practical value but weaker evaluation rigor for core claim. |
| Solving Video Inverse Problems with Image Diffusion | TRWxFUzK9K | 6.50 | R1 | Accepted; clean conceptual contribution for video tasks. AdcVSR has stronger practical results but the E_warp* evaluation gap is a concern. |
| Solving Diffusion ODEs for SR | BtT6o5tfHu | 6.67 | R1 | Accepted; stronger theoretical contribution. Different scope. |
| Flexible Residual Binarization for SR | MEbNz44926 | 8.00 | R1 | Accepted with high scores; more comprehensive evaluation. AdcVSR doesn't reach this level. |
| Progressive Compression with Diffusion | CxXGvKRDnL | 8.00 | R1 | Accepted with strong theory; different scope. |
| IC-Light | u1cQYxRI1H | 0.50 (mislabeled, actual 10.0) | R1 | Not comparable. |
| Clothing-Irrelevant Lifelong ReID | 5lUdTogEL3 | 1.00 | R1 | Strong reject; completely different quality level. |

**Round-1 bracket: 5.5–7.0**

**Narrowing:** AdcVSR is clearly above the rejected 5.0-level SR papers (AddSR, DFOSD) due to more novel architecture and training contributions, a harder problem (video vs. image), and stronger practical impact. However, compared to accepted papers at 6.25–6.50 (SiDA, video inverse problems), AdcVSR's evaluation has a notable gap: its core claim about balancing detail and consistency rests heavily on a single imperfect metric without robustness analysis. The paper's strengths—dramatic efficiency gains, creative architecture, and well-engineered dual-head design—are genuine and practically valuable. But the evidential gap on the consistency axis and split ablations prevent it from being a confident accept.

**Final score: 6.0** — Borderline accept. The engineering contribution is strong and practically meaningful (95% compression with competitive quality), the 2D+1D insight is well-validated, and the dual-head discriminator is creative. The paper is clearly above the rejected SR papers in this space. However, the evaluation of its central claim (detail-consistency balance) is weakened by over-reliance on E_warp* without ruling out smoothing artifacts, and the split ablations and limited main-paper results thin the evidence. These are addressable weaknesses that a rebuttal could potentially resolve.

MY FINAL SCORE: <score>6.0</score>
MY FINAL DECISION: <decision>Accept</decision>