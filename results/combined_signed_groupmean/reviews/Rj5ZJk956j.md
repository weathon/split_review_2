## Summary

This paper introduces a weight-based method for analyzing gated neurons (SwiGLU/GeGLU) in LLMs by computing cosine similarities between input, gate, and output weight vectors. This yields a taxonomy of "read-write" neuron classes including *strengthening*, *conditional strengthening*, and *weakening* neurons. The key discoveries are: (1) the strengthening-then-weakening pattern across layers is consistent across 12 LLMs (2B–9B parameters); (2) weakening neurons, though few in number, have outsized influence on model behavior when ablated; and (3) this influence is partially driven by negative gate values — a regime typically dismissed as a training-dynamic artifact — which is shown to be functionally meaningful via conditional ablation experiments.

## Strengths

- **Cross-model consistency of the geometric pattern (impact: +10.00).** The paper tests 12 LLMs (Section 5) and finds a strengthening-then-weakening pattern across layers in all of them (Figure 1a). The consistency is a genuine discovery and the paper's strongest empirical result — it transforms what could be a single-model observation into a robust architectural principle.

- **The conditional ablation method (Section 6.2) (impact: +9.83).** Decomposing ablation effects by the sign conditions of $x_{\text{gate}}$ and $x_{\text{in}}$ is a clean, useful methodological tool that could transfer to other neuron analyses. It is the ablation design that enables the negative-gate-value finding, which is the paper's most interesting specific result.

- **The negative gate value finding (impact: +10.00).** The claim that Swish's negative regime (small-valued and often treated as a training-dynamic artifact) actually contributes to model mechanisms in a functionally meaningful way is genuinely surprising and worth publishing. The paper documents this clearly with the conditional ablation data in Figure 3(b).

- **Transparency about limitations (impact: +5.82).** The paper explicitly acknowledges that weakening neurons are hard to interpret (Section 8), that they may work in superposition (Section 6.3), and that conditional strengthening neurons dominate numerically but were not deeply studied. This candor is commendable.

## Weaknesses

### Fatal
None.

### Major
- **Functional claims validated on only one model (impact: -10.00).** The geometric taxonomy (Section 5) is validated across 12 LLMs. However, every experiment testing whether weakening neurons *matter functionally* — the ablation experiments (Section 6), the activation frequency analysis (Section 7), and the case studies (Section 8) — is run on OLMo-7B alone. The paper explicitly says "to save resources, we focus on a single model" (line 188). The central functional claims — that weakening neurons have outsized influence and that negative gate values contribute to this — are presented as general LLM properties (abstract, conclusion) but lack cross-model functional evidence. This creates a disconnect between the scope of the claims and the scope of the evidence. Testing at least one additional model family (e.g., Llama-3.2-3B) on a smaller dataset would substantially strengthen the generality claim.

### Minor
- **"First time" / "mechanism" claim is imprecise (impact: -9.74).** The abstract and introduction state "for the first time, we observe a mechanism involving negative gate values" without the caveat that Section 6.2 adds ("concurrently with Kong et al. (2025)"). More importantly, the conditional ablation experiment shows that negative gate values are *causally relevant*, but does not reveal the underlying *mechanism* — the paper's own attempted explanation (line 229: "the usual neuron behavior gets a minus sign in front") is a post-hoc geometric reinterpretation, not a validated causal mechanism.

- **Key negative result only in appendix (impact: -7.76).** The claim that non-weakening neuron classes are "indistinguishable from the 'clean' line" (line 207) is a key piece of evidence for the paper's main claim that weakening neurons uniquely matter, yet it is only shown in appendix figures 14-16 rather than the main body. A paper making this strong a functional claim should display this negative result prominently.

- **No variance or statistical significance for ablation results (impact: -2.16).** The entropy histograms (Figure 3b) and attribute rate plots (Figure 3a) are presented without confidence intervals, error bars, or multiple seeds. For a finding as striking as weakening neurons having uniquely large effects, this lack of uncertainty quantification weakens the evidence.

- **Key preprocessing step justification deferred to appendix (impact: -0.03).** The preprocessing step (multiplying $\mathbf{w}_{\text{in}}$ and $\mathbf{w}_{\text{out}}$ by $\text{sign}(\cos(\mathbf{w}_{\text{gate}}, \mathbf{w}_{\text{in}}))$) is critical because it changes weight vector signs and directly affects the cosine-similarity classification on which the entire taxonomy is built. The paper defers the justification for why this is valid and does not change model behavior to Appendix C (line 85). A reader who does not inspect the appendix cannot evaluate whether this step is valid or whether it introduces artifacts.

- **Conditional ablation conditions and preprocessing interaction unclear (impact: -0.01).** The four sign-based conditions ($x_{\text{gate}} > 0 / < 0$, $x_{\text{in}} > 0 / < 0$) are defined after the preprocessing step that flips weight vector signs based on $\cos(\mathbf{w}_{\text{gate}}, \mathbf{w}_{\text{in}})$. This means the same condition label may correspond to different actual behaviors across neurons depending on how their weights were flipped. The paper does not clarify this interaction.

- **Activation frequency cross-model results deferred to appendix (impact: -0.00).** The finding of strong negative correlation between $\cos(\mathbf{w}_{\text{in}}, \mathbf{w}_{\text{out}})$ and activation frequency (Section 7) is only shown for OLMo-7B in the main text (Figure 4). Since activation frequency is a behavioral measure (unlike static weight geometry), demonstrating it holds across models in the main text would strengthen the generality claim.

### Trivial
- **Minor inconsistency in model count (impact: -0.02).** The abstract says "nine different LLMs" while Section 5 lists 12 LLMs and Figure 1(a) shows 9 models of 2B–9B. This appears to be because the abstract refers to the 9 larger models shown in the figure, but the phrasing is imprecise.

## Nice-to-Haves
- Testing the ablation experiments on at least one additional model family (e.g., Llama-3.2-3B or Gemma-2-2B) to support the generality of functional claims.
- Reporting ablation results with multiple random seeds or confidence intervals.
- Adding the "concurrently with Kong et al. (2025)" caveat to the abstract and introduction, and reframing "mechanism" to "causal relevance."
- Matching the random ablation baseline on additional statistics beyond layer membership (e.g., weight norm, bias).

## Removed Points (from input, retained for reference — treat with caution)
- *"25% of all neurons seems low"* — This criticism misreads the paper: 25% input manipulators across all layers (with 50% in early-middle layers) is substantial, and the paper is transparent about classification coarseness.
- *"Case study admission undercuts broader framing"* — The paper is being honest about limitations; its main claims are about functional importance (ablation effects), not interpretability.
- *"Random baseline could be stronger"* — A speculative nice-to-have; same-layer random neurons is a standard baseline.
- *"Limited evaluation on only two metrics"* — The paper justifies these choices in the appendix.
- *"Formatting/typographical issues"* — Parser artifacts, not author errors.

## Novel Insights
Beyond the paper's own contributions, the reviews surface the insight that the paper has a built-in evidential asymmetry: the geometric claims are thoroughly cross-validated across 12 models, but the functional claims that make the paper most exciting rest on a single model. This pattern — where a striking functional discovery is under-evidenced relative to its framing — is worth flagging explicitly as it is common in mechanistic interpretability papers.

## Suggestions
1. **Test the ablation experiments on at least one additional model family** (e.g., Llama-3.2-3B on a smaller data subset). This is the single highest-leverage improvement.
2. **Move the key negative result** (non-weakening classes having minimal effect) from the appendix to the main body.
3. **Clarify whether the preprocessing step interacts with the conditional ablation conditions** and how.
4. **Report ablation results with multiple random seeds or confidence intervals.**
5. **Add the "concurrently with Kong et al. (2025)" caveat to the abstract and introduction**, and reframe "mechanism" language to "causal relevance" or "causal importance."

---

### Calibration Anchors

| Path | Avg Human Score | Round | Itemized | Comparison |
|------|---------------|-------|----------|------------|
| EytBpUGB1Z.md (Retrieval Head) | 8.00 | R1 | Yes | Similar structure (sparse important component, cross-model validation, causal tests) but tests functional claims across 4 model families vs. this paper's 1 |
| gI0kPklUKS.md (Bilinear MLPs) | 7.50 | R2 | Yes | Weight-based interpretability of gated architectures; similar scope but essentially no substantive weaknesses |
| cnKhHxN3xj.md (Wasserstein Neurons) | 7.50 | R2 | Yes | Discovers small class of important neurons; has more severe clarity/experimental concerns |
| bVTM2QKYuA.md (Representation Geometry) | 6.75 | R2 | Yes | Strong theoretical + empirical; concerns about limited scope and methodology clarity |
| GdbQyFOUlJ.md (NeurFlow) | 6.50 | R1 | Yes | Neuron analysis framework; similar evidence-scope mismatches in reviewer assessment |
| 2J18i8T0oI.md (Towards Universality) | 6.50 | R2 | Yes | Cross-architecture similarity; concerns about limited model scale and statistical rigor |
| yR47RmND1m.md (Safety Neurons) | 6.20 | R1 | Yes | Discovers sparse neuron class with multi-model validation; originality concerns |
| f6r1mYwM1g.md (Capability Localization) | 5.75 | R1 | Yes | Neuron localization; significant methodological weaknesses |
| nUGFpDCu3W.md (Brackets case study) | 4.00 | R1 | No | MLP analysis on toy task; much narrower scope |

**Bracket (Round 1):** 5.5–7.0. **Narrowing (Round 2):** Compared to Safety Neurons (6.20) and NeurFlow (6.50), this paper has stronger cross-model geometric evidence and greater originality, but the single-model functional validation is a decisive gap. The paper sits below Bilinear MLPs (7.50) and Retrieval Head (8.00) precisely because those papers validate their functional claims more broadly.

**Placement:** The paper's top strengths (+10.00, +10.00, +9.83) rival those of higher-scoring papers, but its decisive weakness (-10.00, single-model functional gap) prevents it from reaching their level. It is most comparable to Safety Neurons (6.20) in overall evidence profile — a genuinely interesting discovery with an actionable evidence gap.

MY FINAL SCORE: <score>6.0</score>
MY FINAL DECISION: <decision>Accept</decision>