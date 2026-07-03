## Summary
CaPT introduces an asymmetric-modalities co-training framework that jointly trains an adapter-tuned CLIP model and a fully fine-tuned unimodal network for semi-supervised learning (SSL). The central insight is that existing SSL methods are label-dependent—pseudo-label quality degrades sharply when labeled data is scarce or unprototypical—and that CLIP's zero-shot prior can decouple this dependency. CaPT combines predictions from both branches via entropy-weighted co-pseudo labels, achieving 21.38% and 4.05% improvements over the second-best method on CIFAR-100 and EuroSAT at one label per class, respectively, while adding only 8% memory and 11% training-time overhead over FreeMatch.

---

## Strengths

- **Extraordinary empirical gains in the extreme low-label regime.** Table 3 shows CaPT reaching 82.51% on CIFAR-100 (1 label/class) versus 61.13% (FreeMatch) and 60.49% (RegMixMatch). A 21-point margin is far above incremental improvement; it represents a qualitative change in what SSL can achieve under severe label scarcity. The EuroSAT gain (96.33% vs. 92.28%) over an already-strong baseline further corroborates the trend.

- **Favorable efficiency profile with empirical support.** Table 4 directly measures training time (0.1044 vs. 0.0939 s/iter) and memory (5050 vs. 4676 MiB) against FreeMatch, demonstrating a 6.23-point accuracy gain at a mere 8% memory cost. This is a concrete, verifiable advantage absent in most SSL papers.

- **Well-structured ablations validating each design choice.** Table 6 isolates adapter-tuning (CaPT-Deb: −12.73% on EuroSAT), bidirectionality (CaPT-Uni: −0.88%/−1.49%), feature-augmented regularization, and entropy-based weighting with consistent internal coherence. Figure 5 directly shows adapter-tuning correcting CLIP's class-distribution bias on EuroSAT.

- **Honest reporting of failure modes.** CaPT underperforms FreeMatch on FGVCAircraft (50.12 vs. 51.43 at 5 labels) and RegMixMatch at 10 labels (64.33 vs. 66.21), and these results are included in Table 5 without sanitization.

---

## Weaknesses

### Fatal
None.

### Major

- **CaPT's unimodal network underperforms standalone adapter-tuned CLIP on STL-10, and this is never acknowledged.** Table 1 shows adapter-tuned CLIP alone at 96.86% (4 labels/class) and 97.15% (10 labels/class), while CaPT (unimodal branch) reports 96.07% and 96.34%. The paper explicitly states "The final performance of CaPT is reported using the fully fine-tuned unimodal network." On STL-10, this reporting convention presents a result that is 0.79–0.81 points *below* the CLIP branch that CaPT itself trains. The co-training mechanism was designed to improve both branches; if it suppresses the unimodal network below standalone adapter-tuned CLIP on one of the three main benchmark datasets, this contradicts the mutual-learning claim. The paper does not acknowledge the anomaly, explain the STL-10 dynamics, or discuss whether an ensemble/best-of-two policy would change the conclusion. This is a substantive evidential gap that must be addressed.

- **Ablation study (Table 6) is run only at 2 labels/class, while the headline claim lives at 1 label/class.** The 21.38% headline improvement is the paper's strongest evidence, but Table 6 is run "with 2 labeled samples per class." More critically, the standalone adapter-tuned CLIP baseline — which is reported in Table 1 at 2 labels/class — is absent from Table 3 (the 1-label table). Without it, it is impossible to determine how much of the 21-point gain comes from CaPT's co-training machinery versus simply using CLIP at all in that regime. The paper attributes the headline improvement to its framework, but the evidence required to support that attribution is missing.

### Minor

- **Theorem 1.1 is framed with a prominence that overstates its scope.** The theorem bounds pseudo-label error for a nearest-prototype classifier under a Gaussian mixture model — neither of which applies to the neural-network SSL methods evaluated empirically. It correctly captures the qualitative role of prototype bias $B$ and $n_{\min}$, but it does not constrain or predict any property of CaPT itself. Framing this as Theorem 1.1 in the introduction overstates its reach; it functions as an analytic motivation, not a core theoretical result.

- **FGVCAircraft underperformance receives only a brief in-text note and is deferred to Appendix N.** This is the setting where the CLIP prior is least reliable, and it is the most important failure case for understanding the method's boundaries. A main-body analysis of *whether* co-pseudo labels from a poor CLIP branch hurt the unimodal network (vs. graceful degradation) would sharpen the scope of the contribution.

### Trivial

- The entropy-weighting degeneracy at equal entropy (both models output 0.5 weight) is a minor theoretical loose end; the ablation in Table 6 shows this costs only −0.87%/−1.57%, confirming it is not a practical concern.

---

## Nice-to-Haves

- Run Table 6 ablations at 1 label/class on CIFAR-100 and EuroSAT to validate which design choices drive the headline gains, especially whether entropy weighting and feature-augmented regularization remain relevant when the unimodal network starts from a weaker initialization.
- Include an adapter-tuned CLIP standalone row in Table 3 (1-label setting) so the contribution of the co-training mechanism can be cleanly isolated.
- Add a brief experiment or discussion comparing CaPT against a two-unimodal-ViT co-training baseline (e.g., CLS) with matched parameters to quantify the asymmetric-modalities advantage quantitatively rather than qualitatively (Figure 3).
- For the STL-10 anomaly, report whether best-of-two-branches or ensemble evaluation resolves the underperformance, and characterize in which distribution settings the co-training mechanism improves vs. hurts the unimodal branch.

---

## Removed Points
*These points are flagged to be removed; treat them with caution.*

- **Alternative explanation for Figure 1c** (a better pretrained backbone might fix the same problem): This is scope-creep speculation not verifiable from the paper. Removed.
- **Gains partially entangled with FreeMatch's threshold strategy**: The paper is transparent about adopting FreeMatch's adaptive threshold as a standard building block; this is not a confound. Removed.
- **Entropy-weighting degeneracy as a significant weakness**: Empirically shown to cost ~1% and confirmed minor by ablation. Downgraded to trivial.
- **Asymmetric comparison with baseline methods**: Asymmetry favors baselines (CaPT uses CLIP; baselines do not), so this strengthens rather than weakens the comparison. Removed per hard rule.

---

## Novel Insights

The most genuinely novel structural observation in this paper is that the asymmetric-modalities co-training design—pairing CLIP with a unimodal ViT rather than two unimodal ViTs—provides a natural view-independence argument for co-training: text-grounded CLIP representations diverge from pure-vision ViT representations in attention localization (Figure 3), and this divergence enriches the mutual learning signal in ways that same-architecture co-training (CLS) cannot achieve. The STL-10 anomaly, unintentionally revealed by the paper's own Table 1, also suggests that the co-training mechanism's benefit is not monotone: when CLIP's prior is already dominant (STL-10 is a dataset where CLIP achieves near-ceiling performance even zero-shot), the co-training may not add value to the unimodal branch. Characterizing this "prior dominance" regime—when CLIP is so strong that co-training becomes co-teaching by CLIP—would be a valuable follow-on contribution.

---

## Suggestions

1. **Acknowledge and analyze the STL-10 anomaly in the main body.** Report whether the ensemble of both branches, or selecting the max-confidence branch per sample, recovers performance above the standalone adapter-tuned CLIP baseline on STL-10.
2. **Add the adapter-tuned CLIP standalone to Table 3.** This single row would let readers directly assess the co-training machinery's contribution to the headline 21-point gain.
3. **Run at least the two most impactful ablation variants (CaPT-Deb and only MPM) at the 1-label/class setting.** This would establish whether the co-training mechanism is responsible for the headline claim or whether CLIP-alone would achieve similar results.

---

## Score and Decision

**Anchor papers retrieved:**

| Path | Avg Score | Round | Comparison to CaPT |
|---|---|---|---|
| u1cQYxRI1H.md | 0.50 | R1 | Illumination harmonization — unrelated, strong-reject territory |
| 5lUdTogEL3.md | 1.00 | R1 | Person re-ID lifelong learning — unrelated |
| FwkYeLovHk.md | 3.33 | R1 | Weak-to-strong CLIP generalization — weaker empirical contribution, narrow scope |
| HfJxXbXlYJ.md | 3.00 | R1 | LLM2CLIP — more incremental CLIP extension |
| E0UsEIRBQ8.md | 3.00 | R1 | SSL for underwater OD — narrower scope, weaker contribution |
| 1rgMkDWfYV.md | 4.50 | R1 | CLIP for noisy-label learning — related setting, smaller gains |
| RgWATMmWmz.md | 4.75 | R1 | Weakly supervised + pretrained models — methodologically similar but weaker evidence |
| jjjxp9Wgjp.md | 4.25 | R1 | Pseudo-labels for OOD — different task |
| PD8JVDg8mB.md | 4.25 | R1 | Annotation bootstrapping — related but weaker evidence |
| 97D725GJtQ.md | 5.80 | R1 | SemiCLIP — most similar (CLIP + SSL), smaller gains, fewer benchmarks |
| ptCIlV24YZ.md | 5.80 | R1 | Image clustering with CLIP — different task |
| DjzvJCRsVf.md | 7.00 | R1 | CLIPSelf for dense prediction — stronger theoretical grounding |
| 4JbrdrHxYy.md | 6.00 | R1 | Foundation models + annotation-free segmentation — different task |
| uAFHCZRmXk.md | 8.00 | R1 | CLIP analysis paper — purely analytic, different contribution type |
| 3i13Gev2hV.md | 8.00 | R1 | Hyperbolic VLM — different task |
| 5Ca9sSzuDp.md | 8.00 | R1 | CLIP interpretation — purely analytic |
| WyEdX2R4er.md | 8.00 | R1 | VLM visual data-type understanding — purely analytic |

**Round 1 bracket:** The most comparable paper is SemiCLIP (5.80), which improves CLIP fine-tuning for limited-data settings with 1.7–6.6% gains. CaPT has much larger empirical gains (21 points headline), broader evaluation (9+ datasets), and a cleaner efficiency story. However, CaPT's two major weaknesses — unacknowledged STL-10 anomaly and missing 1-label ablations — are real and would require substantive revision. The paper sits in the **5.5–7.0 range**.

**Narrowing:** Papers at 6.0–6.5 (borderline accept) in the calibration set (SemiCLIP at 5.8, CLIPSelf at 7.0, devil-is-in-boundary at 6.0) reflect solid empirical contributions with some gaps. CaPT is empirically stronger than SemiCLIP (much larger gains, broader scope), but the unacknowledged STL-10 anomaly and missing ablations at the headline setting prevent a confident 7.0. The major weaknesses are fixable in a revision but are real evidentiary gaps. **Score: 6.0.**

**Final score: 6.0 (Borderline Accept).** The paper makes a genuine and substantial contribution — 21-point gains in extreme low-label SSL are noteworthy, the efficiency story is clean, and the ablations are well-designed. Two major issues need resolution before acceptance can be fully recommended: the STL-10 reporting anomaly (where the paper's own CLIP branch outperforms the reported CaPT result) and the missing adapter-tuned CLIP baseline and component ablations at the 1-label/class setting that would establish what mechanism drives the headline claim.

MY FINAL SCORE: <score>6.0</score>
MY FINAL DECISION: <decision>Accept</decision>