Based on my reading of the paper and calibration anchors, I can now form a bracket. The most topically similar paper is "Autoregressive Action Sequence Learning for Robotic Manipulation" (avg 4.0 — rejected), which is much narrower in scope than FASTer. "Latent Action Pretraining from Videos" (LAPA, 5.83) also uses VQ-based action tokenization for VLAs, but is considerably less comprehensive in evaluation. "HAMSTER" (6.0) and "Video Language Planning" (7.0) are comparable in scope. FASTer goes beyond all of these in evaluation breadth, technical novelty (RVQ + patchifier), and the strength of its WBC results.

**Round 1 bracket: 6.5–7.5**

The paper has solid real contributions (FASTerVQ, WBC results, cross-backbone generalization) with two fixable major weaknesses (BAR framing, baseline initialization clarity) and a few minor ones. No fatal flaws. I'll place this at **7.0**.

---

## Summary
FASTer is a unified framework for efficient autoregressive VLA modeling comprising FASTerVQ—a neural action tokenizer that applies a semantic action patchifier followed by residual vector quantization (RVQ)—and FASTerVLA, which builds on FASTerVQ with block-wise autoregressive (BAR) decoding and a lightweight action expert. The system is evaluated across nine benchmarks spanning five embodiments in simulated and real-world settings, achieving state-of-the-art performance on LIBERO (97.9%), Simpler-Bridge (87.9%), and dramatically outperforming prior methods on high-DoF whole-body control (~80% vs. ~10% for FAST).

## Strengths

- **FASTerVQ architecture is well-motivated and technically coherent (Section 3.1).** The two-stage design—non-uniform patchification by physical semantics (grouping end-effector position, orientation, gripper state separately) followed by transformer-based RVQ—directly addresses the mismatch between temporal redundancy and cross-dimensional independence in robot action sequences. This is a principled, data-structural design, not a generic retrofit of an image tokenizer.

- **Decisive WBC result (Figure 4).** FASTer achieves ~80% success vs. ~10% for FAST on the R1Lite WBC task. This large gap validates the core claim that variable-length token sequences (150–200 tokens for 2-second motions) are a first-order obstacle for autoregressive VLAs in high-DoF settings, not merely a performance disadvantage.

- **Cross-backbone generalization (Figure 7).** FASTer raises InternVL3.5-2B from 79.35% (worst backbone under FAST) to 96.65% (+17.3%), turning it into the strongest backbone under FASTerVLA. This suggests FASTerVQ's fixed-length, regularized representation reduces the difficulty of adapting diverse VLM backbones to action prediction—a specific, verifiable claim.

- **Breadth of evaluation.** Nine benchmarks, five embodiments, real-world and simulation, in-distribution and OOD settings. The 87.9% on Simpler-Bridge (+12.9% over the next-best method) and consistent advantage across all VLABench generalization dimensions (Figure 9) provide convergent evidence for generalization.

## Weaknesses

### Fatal
None.

### Major

- **BAR is framed as a co-equal contribution but evidence consistently shows it is secondary.** Table 1 shows FASTer w/o BAR at 95.4% (LIBERO avg.) vs. FASTer at 97.9%, and Figure 7 shows FASTerVQ alone captures nearly all cross-backbone improvement. BAR even hurts on one sub-task (Spatial: 99.4% w/o BAR vs. 98.0% with). The paper itself acknowledges in Section 4.3: *"FASTer's improvement is driven primarily by its neural VQ tokenizer: swapping FAST for FASTerVQ yields most of the gain, with BAR adding only a smaller incremental boost."* Additionally, Table 2 shows the observation encoding bottleneck (88–105ms) dwarfs the savings from BAR in the single-arm case (~35ms saved). BAR is most valuable in WBC (12 forward passes, where FAST incurs 1,100–3,000ms). Framing BAR as co-equal in the abstract and introduction misrepresents where the value comes from.

- **Baseline initialization protocol in Table 1 is underspecified.** Section 4.1 states: *"all baselines and FASTerVLA models in our experiments are initialized from checkpoints pretrained on large-scale robotics data (e.g., from π₀-FAST)."* The phrase "e.g., from π₀-FAST" does not confirm that all listed baselines (OpenVLA-OFT, SpatialVLA, UniVLA, VQ-VLA) receive the same pretrained initialization. If FASTerVLA starts from a richer pretrained checkpoint while some baselines start from VLM-only weights, the LIBERO and Simpler-Bridge comparisons are not apples-to-apples. This needs to be stated explicitly in the main text.

### Minor

- **Real-world results lack statistical reporting.** Results in Figures 4, 9, and 10 are read from bar charts without exact values, trial counts, or confidence intervals. Narrow margins (5–10% gaps between FASTer and baselines in Figures 9 and 10) may not be statistically significant. The WBC gap is large enough to be robust regardless, but narrower margins in other settings deserve error bars and explicit trial counts.

- **VRR threshold σ=10⁻² is asserted without empirical grounding.** Section 4.2 states "a reconstruction error on the order of 10⁻² is sufficient to cause a noticeable degradation in task execution accuracy" without citing any experiment linking this threshold to actual task failure rates. This threshold drives the primary tokenizer comparison metric; its empirical basis should be established.

### Trivial

- The claim that "many action codes are only weakly coupled across dimensions" (Section 3.2) is asserted to justify BAR but not demonstrated. The fact that BAR occasionally hurts performance (Table 1, Spatial sub-task) is consistent with this assumption breaking down; the conditions under which BAR helps vs. hurts are not analyzed.

## Nice-to-Haves

- A single clean ablation table that holds the VLA architecture fixed and swaps only the tokenizer (FASTerVQ vs. FAST vs. naive binning) would sharpen the causal claim about tokenizer quality → downstream performance. Table 1's FASTer-w/o-BAR rows partially achieve this but a unified comparison would be cleaner.
- The WBC result (Figure 4) is the paper's most dramatic finding. A qualitative analysis of *why* FAST fails (gradual degradation vs. catastrophic failure) and how many rollouts underlie each bar would make this finding considerably more compelling.
- Connecting codebook utilization (Table 8) to reconstruction quality per task—showing high-utilization codes correlate with high VRR—would make the code distribution analysis mechanistic rather than correlational.

## Removed Points

*These points are flagged to be removed; treat them with caution.*

- **FASTerVQ training data scale not verifiable (critic claims comparison relies on appendix Table 3):** Removed per hard rule against criticizing missing appendix material. The main text (Section 4.2) states "equal or smaller data budgets" explicitly, so the claim is present in the accessible paper.
- **Embodiment-specific patchification groupings absent from main body:** Removed as a reproducibility nitpick about appendix-deferred details.
- **Controlled ablation on codebook size absent:** Removed; this is a nice-to-have suggestion rather than a substantive flaw. The normalized-entropy comparison in Table 8 partially addresses the concern.
- **"Preliminary experimental results in Figure 1 not accessible":** Removed per hard rule about parser-stripped figures; the figure exists in the original submission.

## Novel Insights

The WBC result (Figure 4) implicitly demonstrates something not fully articulated in the paper: there may be a *phase transition* in autoregressive VLA performance as token sequence length grows, not just gradual degradation. FAST's near-total failure (~10%) on WBC while performing competitively on single-arm tasks—despite being a reasonable tokenizer in both settings—suggests that the effect of token length on multi-step autoregressive accuracy is nonlinear. Making this phase-transition framing explicit would substantially strengthen the theoretical motivation for fixed-length, compressed tokenization as a design principle.

## Suggestions

- Reframe BAR as a complementary efficiency module especially valuable for high-DoF/WBC settings, rather than a co-equal contribution. The evidence supports this, and honest framing strengthens rather than weakens the paper.
- Explicitly state in Section 4.1 and Table 1's caption whether all baselines share the same pretrained checkpoint initialization as FASTerVLA, or clearly disclose any asymmetry.
- Add trial counts and, where feasible, confidence intervals to all real-robot result figures.
- Provide an empirical calibration (even one or two data points) linking the σ=10⁻² VRR threshold to task outcome changes.

## Score and Decision

**Calibration anchors:**

| Path | Avg Human Score | Round | Comparison to FASTer |
|------|----------------|-------|----------------------|
| Lr8IIc1rB8.md (Autoregressive Action Sequence Learning) | 4.00 | R1 | Narrower scope, less evaluation breadth, no real-world WBC; FASTer is substantially stronger |
| VYOe2eBQeh.md (LAPA) | 5.83 | R1 | Uses VQ for action pretraining; FASTer has richer tokenizer design and far more comprehensive evaluation |
| lFYj0oibGR.md (VLM as Robot Imitators) | 6.50 | R1 | Simpler approach, limited task variety; FASTer is comparable or stronger |
| h7aQxzKbq6.md (HAMSTER) | 6.00 | R1 | Hierarchical VLA with broader generalization motivation; comparable in scope |
| 9pKtcJcMP3.md (Video Language Planning) | 7.00 | R1 | Broader multimodal scope; FASTer is more focused but more rigorous empirically |
| KBSHR4h8XV.md (Early Fusion VLA) | 3.33 | R1 | Weaker contribution, limited evaluation; FASTer is much stronger |
| OI3RoHoWAN.md (GenSim) | 8.00 | R1 | Different domain (task generation); strong paper; FASTer is comparable in rigor |
| tyEyYT267x.md (SAR Diffusion) | 8.00 | R1 | Different modality (language); clean theoretical + empirical; comparable tier |

**Round 1 bracket:** 6.5–7.5. FASTer exceeds the 6.0–6.5 range papers (HAMSTER, Robot Imitators) in evaluation breadth and result strength, and is roughly comparable to Video Language Planning (7.0). Its major weaknesses (BAR framing, initialization disclosure) are presentation-level issues addressable in rebuttal, not technical flaws. I see no reason to move above 7.5 (where papers have cleaner, fully-resolved contributions). **Final score: 7.0.**

MY FINAL SCORE: <score>7.0</score>
MY FINAL DECISION: <decision>Accept</decision>