## Summary

This paper analyzes the role of pooled CLIP text embeddings in modulation layers of diffusion transformers, finding they contribute little in conventional usage. The authors then propose "modulation guidance" — extrapolating between positive and negative prompt modulation vectors (Equation 3) — to repurpose the pooled embedding for quality improvement. A dynamic layer-wise variant further improves the quality-fidelity trade-off. The method is evaluated across text-to-image (FLUX, SD3.5, HiDream, COSMOS), text-to-video (Hunyuan, CausVid), and image editing (FLUX Kontext) tasks.

## Strengths

1. **A clean, informative diagnostic of CLIP's role in modulation layers (Section 4, Table 1, Figure 1).** The paper asks a precise question — does the pooled CLIP embedding actually do anything? — and answers it with a straightforward ablation: zeroing out the pooled embedding and measuring the effect. The results (CLIP is near-inactive for long prompts in FLUX and entirely inactive in HiDream-Fast) are concrete and informative, clarifying a design choice the community has been making implicitly.

2. **A simple, cheap, practically useful intervention (Equation 3, dynamic variant in Figure 3).** Modulation guidance is a vector extrapolation in modulation space that requires no training (for models with CLIP), adds negligible compute, and works across models. The dynamic variant (applying guidance only to later layers) is a sensible refinement that demonstrably improves the quality-fidelity trade-off (Figure 3a). These are the kinds of techniques likely to see real adoption.

3. **Broad empirical validation across diverse models and tasks.** The paper tests on FLUX schnell/dev, SD3.5 Large, HiDream, and COSMOS (T2I); Hunyuan 13B and CausVid (T2V); and FLUX Kontext (image editing). Results show consistent improvements in human preference and automatic metrics across multiple model families and modalities.

## Weaknesses

### Fatal
None.

### Major

- **The evaluation of specific changes (counting, hands, color, position) is limited to a single model.** Table 3 reports improvements in object counting, color, and position only for FLUX schnell. The paper claims the approach "can be applied to various diffusion models," but the most practically compelling improvements — object counting (+22% SbS win rate) and hands correction (+18%) — are demonstrated on only one model. Without evidence on SD3.5, HiDream, or COSMOS, the generalizability of the specific-changes results is unsubstantiated, and this is the most practically impactful part of the evaluation.

### Minor

- **The "training-free" framing in the abstract is imprecise.** The abstract and Section 5 state the approach is "training-free," which is accurate for the guidance formula itself (Equation 3). However, applying this technique to CLIP-free models (COSMOS, CausVid) requires fine-tuning a small MLP (4K and 1K iterations, 500K synthetic samples) with a distillation objective. This is described in the paper but not qualified in the abstract-level claims. The paper would be more precise by distinguishing models with and without native CLIP support.

- **The novelty is incremental relative to prior work.** The core guidance formula (Equation 3: y → y + w·(y₊ − y₋)) is a direct adaptation of Garibi et al. (2025), who used the same mechanism for image editing. The paper credits this work but does not sharply delineate what is new: (i) the diagnosis of CLIP inactivity, (ii) the application to quality improvement rather than editing, (iii) the dynamic layer-wise variant, and (iv) the CLIP-integration technique for CLIP-free models. These are real contributions, but the framing implies a larger methodological novelty than is present.

- **The constant vs. dynamic guidance comparison (Figure 3a) is shown for only one model family (FLUX).** The trade-off curves demonstrate a clear advantage for the dynamic variant, but similar curves for SD3.5 or HiDream would strengthen the claim that the benefit generalizes. As is, it is unclear whether the dynamic advantage is model-specific.

### Trivial
- The color and position gains in Table 3 (+7 and +5 GenEval points) are reported without any discussion or interpretation in the text.
- COSMOS training hyperparameters (learning rate, batch size, MLP architecture) are not reported in the main text (these may be in the stripped appendix).

## Nice-to-Haves
- Extend the specific-changes evaluation (counting, hands, color, position) to at least one additional model beyond FLUX schnell.
- Include a brief summary of the human evaluation protocol (number of annotators, blinding, statistical test) in the main text, even if full details are in the appendix.
- Add a brief limitations paragraph to the main text (currently only in the stripped Appendix H).

## Removed Points
These points were flagged by the reviewer but are removed for the following reasons:

- *Baseline comparison tables relegated to appendix*: The paper states the headline results (34% improvement over Normalized Attention Guidance, 16% over Concept Sliders) in the main text. Placement of full comparison tables in the appendix is standard practice. Additionally, the appendix was stripped by the parser.
- *CLIP inactivity analysis has a confound*: The reviewer argued that zeroing CLIP only shows current-parameter inactivity, not structural incapability. This is addressed by the paper's own experiments — adding CLIP alone to COSMOS does nothing, but CLIP + modulation guidance improves, confirming the paper's thesis. The concern is preempted by the paper's full experimental design.
- *Missing limitations / human evaluation details*: The paper explicitly references Appendix H (limitations) and Appendix J (evaluation details). These sections exist in the original submission but were removed by the parser.
- *Trade-offs not discussed*: The paper acknowledges "slight drops in text relevance for FLUX dev and in defects for COSMOS" (Section 6.1). The CausVid aesthetic quality change (57.85→57.65) and overall consistency change (19.01→19.02) are at noise level and do not require substantive discussion.

## Novel Insights
None beyond the paper's own contributions.

## Suggestions
1. Qualify the "training-free" claim in the abstract (e.g., "training-free for models with CLIP modulation; we also describe a lightweight adaptation for CLIP-free models").
2. Extend the specific-changes evaluation to at least one additional model (e.g., SD3.5 Large or HiDream), or explicitly scope the specific-changes claim to FLUX schnell.
3. Include the dynamic vs. constant guidance trade-off curves for at least one additional model family.
4. Briefly interpret the color and position GenEval gains in the main text.

MY FINAL SCORE: <score>7.0</score>
MY FINAL DECISION: <decision>Accept</decision>