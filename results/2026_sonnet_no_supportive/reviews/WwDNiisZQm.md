**Calibration Analysis:**

**Round 1 — Bracketing:**
- Score < 1.5 band: Unrelated papers (diffusion/GFlowNets) — not comparable
- Score 1.5–3.5 band: GroupMamba (3.0), MambaIC-adjacent (3.4) — these are simpler Mamba adaptations with lower novelty
- Score 3.5–5.5 band: **MambaVC (4.8)** — most relevant anchor. MambaVC is one of CMIC's baseline comparisons; it simply applied Mamba to LIC without tailored design. CMIC substantially outperforms it and has far stronger ablation and mechanistic evidence.
- Score 5.5–7.5 band: **Spatial-Mamba (7.0)** — highly relevant. Also addresses Mamba's 2D limitations via a structural fix, achieves SOTA results. Similar innovation level to CMIC.
- Score 7.5–8.5 band: Progressive diffusion compression (8.0) — different approach (diffusion-based), stronger theoretical contribution.
- Score > 8.5 band: No results

**Bracket: 6.5–7.5**

CMIC is clearly stronger than MambaVC (4.8): two novel mechanisms vs. simple application, significantly better RD results, rigorous ablation, ERF mechanistic evidence. It is comparable to Spatial-Mamba (7.0) in quality: both address Mamba's inherent 2D limitations with a specific architectural solution, achieve SOTA-class results in their domain, and have clean ablations. CMIC's ERF-level ablation (Fig. 9) is arguably better evidence than Spatial-Mamba's. One major weakness (overclaiming SOTA on Kodak, where MLICv2 is 0.25% better) keeps it from a higher score, but this is presentational, not structural.

**Final score: 7.0**

---

## Summary
Content-Aware Mamba for Image Compression (CMIC) addresses two identified failure modes of vanilla Mamba for LIC: content-agnostic raster scanning and strict causality. It introduces Content-Adaptive Token Permutation (CTP) — a codebook-based EMA-updated clustering scheme that reorders latent tokens by feature similarity before the SSM scan — and Global-Prior Prompting (GPP), which injects cluster-derived prompt vectors into Mamba's output projection matrix C to relax causal constraints without multi-directional scanning. The resulting model achieves leading RD performance on Tecnick and CLIC while substantially reducing parameters, FLOPs, and memory vs. prior Mamba-based LIC methods.

## Strengths

- **Tightly coupled problem-solution design.** Two mechanistically distinct failure modes of Mamba for LIC are identified (content-agnostic scan order; strict causality) and addressed with two separate, non-redundant components (CTP for scan, GPP for causality). This coherence avoids the ad hoc patchwork common in LIC architecture papers.
- **Clean, diagnostic ablation (Table 2).** The 2×2 component ablation isolates CTP (1.8–2.4% BD-rate) and GPP (0.5–1.4% BD-rate) with independent, additive gains that compound to 2.7–3.6% total. Both components deliver consistent improvements across all three benchmark datasets.
- **ERF visualizations directly validate the claimed mechanisms (Fig. 9).** Computing the ERF of a single Mamba layer under four configurations (±CTP, ±GPP) shows the causality boundary of baseline Mamba disappearing with GPP, and the raster-scan pattern replaced by semantic spread with CTP. This per-layer mechanistic evidence is unusually rigorous for the LIC literature.
- **Favorable efficiency profile (Table 1).** CMIC achieves best BD-rate on Tecnick (−21.34%) and CLIC (−17.58%) while reducing parameters by 56%, FLOPs by 57%, and GPU memory by 78% vs. MambaIC. The single-scan design mechanistically explains the memory reduction.
- **Stable EMA codebook design.** Replacing per-sample online K-Means with a shared EMA-updated codebook avoids centroid re-initialization instability and yields deterministic inference. Cluster visualizations (Fig. 10) confirm semantically coherent centroids (edges, textures, color regions) that generalize across images.

## Weaknesses

### Fatal
None.

### Major
- **Overclaimed SOTA on Kodak.** Table 1 shows MLICv2 at −16.16% BD-rate on Kodak vs. CMIC at −15.91% (a 0.25% gap). Despite this, Section 4.3 states "CMIC model achieves superior performance" across all datasets, and the conclusion claims "SOTA RD performance" unconditionally. The abstract also asserts SOTA without qualification. This is a factual inaccuracy in the performance narrative, even though CMIC leads on 2/3 benchmarks. The omission of any discussion of the Kodak gap vs. MLICv2 reads as selective reporting. The paper should acknowledge the gap explicitly and qualify its SOTA claim: CMIC leads on Tecnick and CLIC (high-resolution datasets that better exercise global content modeling) but trails MLICv2 on Kodak.

### Minor
- **"Sample-specific" framing of GPP overstates what the math delivers.** The prompt P = ΓU, where U is derived from shared EMA-updated centroids (dataset-level statistics projected via a learnable A) and Γ is the per-image one-hot assignment (Section 3.4). What genuinely varies per image is the cluster membership matrix Γ, not the underlying prompt vectors in U. The mechanism is valid and effective — confirmed by Fig. 9c — and the projection A is trained end-to-end on the RD objective. But labeling these as "sample-specific global priors" (abstract, Section 3.4) is stronger than warranted; the dictionary itself is dataset-level, with per-sample adaptation only in which entries are selected.

### Trivial
- **"MambaC" vs. "MambaIC" naming inconsistency.** Table 1 lists "MambaC (Zeng et al., 2025)" while Section 4.3 refers to "MambaIC (Zeng et al., 2025)" from the same citation. Should be reconciled.

## Nice-to-Haves
- A rate-distortion theoretic framing of why content-aware token reordering helps: if semantically similar tokens are adjacent in the scan, the SSM's hidden state retains more relevant context per token, reducing conditional entropy that the entropy model must encode. Even a heuristic argument would connect the empirical gains to compression theory.
- Fig. 10 cluster visualization is shown only at Stage 2. Showing Stage 4 (the highest-compression bottleneck) would reveal whether clustering captures semantic abstractions or low-level texture patterns at the final representation layer, strengthening the claim that the mechanism benefits compression specifically.
- MS-SSIM comparison against Mamba baselines is explicitly omitted (Section 4.3) because MambaVC/MambaIC are "only optimized for MSE." Noting MS-SSIM results for CMIC alone vs. non-Mamba baselines would round out the metric coverage.
- Complexity metrics (FLOPs, latency, memory) are measured at 2K resolution only. Since Kodak operates at 768×512, relative efficiency figures could differ at that scale; a note on this would be helpful.

## Removed Points
*These points are flagged as removed; treat with caution.*

- **Table 2 parsing artifact concern (harsh critic).** The PDF parser garbles the check-mark columns. Per hard rules, formatting/parser artifacts are not paper flaws and this criticism is removed.
- **Equation dimension ambiguity for C + P (harsh critic).** The paper explicitly cites MambaIRv2 for this formulation ("following the Attentive State-Space equation in MambaIRv2"). Questioning dimension handling on a borrowed, published formulation is a speculative-reproducibility concern; removed per hard rules.
- **Rate-distortion theoretic framing as a weakness.** This is an enhancement suggestion rather than an identified problem; moved to Nice-to-Haves.
- **Complexity metrics only at 2K as a weakness.** The paper's design rationale targets high-resolution compression; measuring at 2K is the relevant operating point. Moved to Nice-to-Haves.

## Novel Insights
The paper's use of per-layer ERF under component-ablation conditions (Fig. 9) as a mechanistic diagnostic tool — rather than reporting only end-to-end BD-rate differences — is a notably rigorous approach to ablation in the LIC literature. Observing that the causality boundary at (H/2, W/2) precisely disappears with GPP, and that the raster-scan activation pattern dissolves with CTP, provides empirical evidence that maps directly onto the theoretical failure modes the paper identifies. This methodology (per-layer ERF as a controlled ablation diagnostic) could serve as a template for other architecture-design papers in LIC and related domains.

## Suggestions
- Revise the SOTA claim to be accurate: "CMIC achieves SOTA RD performance on Tecnick and CLIC, and is competitive on Kodak (second to MLICv2 by 0.25% BD-rate while using significantly fewer parameters and memory)." This actually strengthens the paper's narrative by being honest about where content-aware global modeling matters most (high-resolution content-rich images).
- Clarify GPP framing: the prompt dictionary U is shared across images (dataset-level centroids), while the per-sample element is the assignment Γ. Rephrase as "instance-conditioned prompts from a shared redundancy-aware dictionary" to be precise.
- Consider adding cluster visualization at Stage 4 to complement Stage 2; the contrast would strengthen the claim about compression-specific representation quality.

## Score and Decision

**Anchor papers retrieved:**

| Path | Avg Score | Round | Comparison |
|------|-----------|-------|------------|
| KgJwbsfN7G.md (MambaVC) | 4.80 | Round 1 | Baseline CMIC outperforms; simpler contribution (Mamba applied to LIC without tailored design) |
| cagNCwQEEN.md (Multimodal SSM) | 3.40 | Round 1 | Weaker, different domain |
| RmmrHEH6Nx.md (GroupMamba) | 3.00 | Round 1 | Weaker, classification task, less LIC-specific |
| gIrVoQEDQv.md (NCA compression) | 3.40 | Round 1 | Very different approach, weaker results |
| iDe1mtxqK5.md (Spatial-Mamba) | 7.00 | Round 1 | Most comparable: addresses Mamba 2D limitations for vision tasks, similar innovation quality; CMIC has stronger per-component evidence |
| AL1fq05o7H.md (Mamba paper) | 6.25 | Round 1 | Original Mamba paper; different contribution type |
| PQpvhUrA1C.md (Mamba pretraining) | 5.75 | Round 1 | Less relevant — pretraining study |
| MvEkN2ejZ1.md (MamBEV) | 6.60 | Round 1 | SSM for BEV perception; different task |
| CxXGvKRDnL.md (Progressive diffusion compression) | 8.00 | Round 1 | Strong LIC paper; different approach (diffusion-based), stronger theory |
| GRMfXcAAFh.md (LinOSS) | 8.00 | Round 1 | SSM theory paper; different type of contribution |

**Bracket after Round 1: 6.5–7.5**

CMIC clearly surpasses MambaVC (4.8) through two novel mechanisms, rigorous ERF-based ablation, and SOTA efficiency profile. It is most comparable to Spatial-Mamba (7.0), which also addresses Mamba's structural 2D limitations with a specific architectural fix and achieves SOTA results on vision benchmarks. CMIC's ERF-level ablation (Fig. 9) is arguably stronger evidence than Spatial-Mamba provides. The one Major weakness (Kodak SOTA overclaim) is presentational and easily corrected without new experiments — it does not undermine the core contribution. This anchors the score at **7.0**.

MY FINAL SCORE: <score>7.0</score>
MY FINAL DECISION: <decision>Accept</decision>