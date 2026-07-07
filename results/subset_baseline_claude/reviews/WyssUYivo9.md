## Summary
XPro-Design is an iterative protein optimization framework that combines inverse folding models (ProteinMPNN/HyperMPNN) with Integrated Gradients (IG)-based attribution scores to update a Position-Specific Scoring Matrix (PSSM), biasing sampling toward thermostable sequence space. The method uses temperature tempering and annealing for exploration-exploitation balance and claims to generate protein variants with nearly 2× wild-type melting temperatures while preserving structural integrity, as assessed entirely through computational predictors and simulations.

---

## Strengths
- **No fine-tuning required**: XPro-Design operates directly on frozen inverse folding models and updates only a PSSM matrix, avoiding catastrophic forgetting and preserving structural fidelity. This is an elegant design choice.
- **Broad comparison**: Seven baselines (ProteinMPNN, HyperMPNN, ADFLIP, MapDIFF, PiFold, and XPro-Design variants) are compared across predicted Tm, sequence recovery, diversity, structure metrics, and free energy, providing a fairly comprehensive computational benchmark.
- **Mechanistic interpretability**: The IG-derived attribution maps and pairwise epistasis matrix (Eq. 4) provide a direct readout of which residues drive predictions, offering useful XAI tooling for practitioners even if the epistasis claim is imprecise.
- **Multi-layer stability validation**: The work goes beyond simple Tm predictions to include MM/GBSA energetics, packing entropy (PACKMAN), inter-residue interaction counting, and BioEmu/MD sampling, yielding a richer picture than single-metric studies.

---

## Weaknesses

### Fatal
**Circular evaluation**: The core evaluation loop is substantially circular. TemBERTure (specifically, variants of it) is used both as the oracle inside the optimization (its gradients drive PSSM updates via IG, Eq. 8) and as the primary metric reported in Table 1 and Figure 2. Sequences that score well on TemBERTure will by construction be those the PSSM has been steered toward. The paper uses DeepSTABp as a "cross-model" check, but it is the same class of sequence-level ML predictor trained on similar datasets; it cannot serve as an independent ground-truth validator. No wet-lab melting-temperature measurements are provided for any designed variant. All headline claims—"nearly 2× Tm", "up to 38% lower ΔΔG"—are thus claims about ML predictor outputs, not about actual protein biophysics.

### Major
**Physically implausible energy values**: The ΔΔG values in Table 3 range from −2962 to +650 kcal/mol. Physical ΔΔG for protein stabilization is typically 1–10 kcal/mol. The paper briefly notes these are MM/GBSA energies used as "relative stability proxies," yet the abstract states "38% lower folding free energy relative to wild-type" without this caveat. Total MM/GBSA internal energies (which scale with protein size and include all bonded/non-bonded terms) are not valid folding free-energy proxies and cannot support thermostability claims directly. The ΔG values of −7000 to −10,000 kcal/mol also appear to be total MM/GBSA interaction energies rather than anything physically interpretable as folding energy. This significantly undermines the quantitative stability claims.

**Very narrow experimental scope**: The framework is tested on two proteins (CaLB for results, SOR briefly as a control). Both share structural features amenable to inverse folding. The paper claims generalizability to "altered substrate selectivity, enhanced cofactor binding, hinge dynamics, reduced immunogenic epitopes," but provides no evidence for any of these scenarios.

### Minor
**Epistasis claim is imprecise**: The pairwise epistasis matrix (Eq. 4) computes the product of individual IG scores averaged over sequences. This captures correlated attribution—sites that jointly point the same direction—but not true epistasis (non-additive effects). True epistasis requires measuring the deviation of the double-mutant effect from the sum of single-mutant effects.

**Low-rank matrix description**: The abstract says the method "trains a low-rank matrix," but the PSSM update in Section 2.3 (Eq. 9) is a full L × 20 matrix with no rank constraint discussed anywhere in the methods. This inconsistency between the abstract description and the actual methodology is confusing.

**SOR control is underreported**: SOR is mentioned as a hyperthermophile "control scaffold" but there is no SOR results table comparable to Table 1–3 for CaLB. The control experiment that would most rigorously validate the method (showing XPro-Design doesn't falsely destabilize an already-thermostable protein, or confirms baselines) is absent from the main text.

### Trivial
The figure captions for Figure 3 describe ProteinMPNN and HyperMPNN as showing distributions shifted toward more negative values, which is inconsistent with Table 3 showing XPro-Design achieving substantially more negative ΔΔG. Likely a caption-generation artifact.

---

## Nice-to-Haves
- Even one or two experimental Tm measurements (DSF/DSC) on top-ranked designs would transform this from a computational study to a validated engineering result.
- An ablation experiment isolating the individual contributions of (a) tempering/annealing, (b) PSSM biasing alone without IG, and (c) full XPro-Design, would clarify which component drives improvement.
- The SOR benchmark should be fully reported with the same tables as CaLB.

---

## Novel Insights
The core insight—that Integrated Gradients computed over frozen ML predictors can provide residue-level attribution signals that are informative enough to update an external biasing matrix and steer a pretrained generative model without weight modification—is a legitimate and interesting contribution. The separation between the generative model (structural prior) and the PSSM update (functional guidance) avoids the catastrophic forgetting typical of fine-tuning on small datasets. If experimentally validated, this approach could offer a practical, lightweight alternative to RL-based or direct fine-tuning protein optimization pipelines.

---

## Suggestions
- Replace or augment TemBERTure-based Tm reporting with an independent predictor (e.g., ProTstab2 or ThermoMPNN, neither used in optimization) or, ideally, experimental Tm values for 5–10 top candidates.
- Reframe or remove the "folding free energy" language in the abstract and main text; use "MM/GBSA interaction energy proxy" consistently and acknowledge that these values cannot be compared to physical ΔΔG estimates.
- Add a proper ablation table showing performance of: (1) ProteinMPNN + PSSM bias without IG (random or evolutionary PSSM), (2) ProteinMPNN + IG attributions without annealing, (3) full XPro-Design.
- Either add rank constraints to the PSSM update to match the "low-rank matrix" claim or remove that description from the abstract.

---

MY FINAL SCORE: <score>3</score>
MY FINAL DECISION: <decision>Reject</decision>