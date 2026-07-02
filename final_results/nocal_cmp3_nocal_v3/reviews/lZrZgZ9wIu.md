I've verified all claims against the paper. Now writing the consolidated review.

## Summary

This paper investigates, for the first time, the combination of dynamic sparse training (DST) via Cannistraci-Hebb Training (CHT) with ANN-to-SNN conversion. Across three architectures (MLP, VGG-16, ViT-B), three datasets (CIFAR-10/100, ImageNet), and four conversion methods, it shows that sparse SNNs converted from CHT-trained ANNs achieve accuracy comparable to (and sometimes exceeding) dense SNN baselines while yielding large theoretical energy reductions (up to ~99%). It additionally reports a novel empirical finding: that firing-rate saturation systematically precedes accuracy saturation in SNNs, with a statistically significant difference in this time lag between sparse and dense networks.

## Strengths

- **First study of DST + ANN2SNN conversion.** The paper identifies and fills a genuine gap — prior ANN2SNN conversion work has focused on dense networks, and the intersection with dynamic sparse training was unexplored. This is a well-motivated combination of structural sparsity (from DST) and temporal sparsity (from SNNs) (Section 1, lines 33–41).

- **Broad experimental coverage.** The evaluation spans three architectures (MLP, VGG-16, ViT-B), three datasets (CIFAR-10, CIFAR-100, ImageNet-1K), and four ANN2SNN conversion methods (CS-QCFS, SNM, AEC, SpikeZIP-TF). The consistent pattern — sparse SNNs roughly matching dense SNNs across this diverse set — is genuinely informative.

- **Novel time-lag finding.** The quantitative analysis showing that firing-rate saturation systematically precedes accuracy saturation, and that this lag differs between sparse and dense networks (Section 3.3, Figure 3), is a genuinely empirical discovery. The extremely small p-values suggest the effect is robust across the hyperparameter variations examined. This goes beyond a simple "look, we can do sparse conversion" paper.

- **Honest limitation disclosure.** The paper explicitly acknowledges that energy measurements are theoretical (not measured on hardware), that hardware supporting both sparse and event-driven computation does not yet exist, and that AEC introduces additional latency (Discussion, Section 4, lines 263–268).

## Weaknesses

### Major

- **Sparse-vs-dense comparison may conflate CHT training with sparsity (Section 2.4, lines 152).** The paper trains sparse ANNs using CHT but never specifies whether dense ANNs are also trained with CHT (at 0% sparsity) or with standard training. The only description is: "During sparse/dense ANN training and ANN2SNN conversion, grid-search is performed" (line 152), with grid-search spaces deferred to the (stripped) Appendix B. This matters because for MLP on CIFAR-10, the sparse ANN achieves **66.54%** while the dense ANN achieves **63.89%** — a 2.65% gap that persists after conversion. If dense baselines received standard training (not CHT at 0% sparsity), the comparison is "CHT-trained (sparse) vs. standard-trained (dense)," and the accuracy advantage attributed to sparsity could be driven by CHT's training dynamics rather than by having fewer connections. The authors should either clarify the dense training protocol or add a CHT-trained dense (0% sparsity) condition to isolate the sparsity effect. This does not invalidate the paper's core feasibility demonstration (DST+ANN2SNN works) but substantially weakens the claim that "sparsity itself" drives the accuracy advantage.

- **MLP SNN accuracy substantially exceeding ANN accuracy is unexplained (Table 1, Figure 2).** In several MLP experiments the Max Dense SNN accuracy far exceeds the Dense ANN accuracy: e.g., MLP CIFAR-100 shows Dense ANN = 31.26% vs. Max Dense SNN = 41.31% (+10.05% absolute); MLP CIFAR-10 shows Dense ANN = 63.89% vs. Max Dense SNN = 69.18% (+5.29%). In standard ANN2SNN conversion, the SNN typically achieves accuracy close to or slightly below the ANN. A 10% absolute improvement after conversion is highly unusual and demands explanation. Possible causes include: (a) the reported ANN accuracy may not be the best attainable for that architecture (grid-search may have favored sparse models), (b) the SNN's "max accuracy over 64 time steps" is not directly comparable to the ANN's single-pass evaluation, or (c) the conversion method itself can yield SNN accuracy exceeding ANN accuracy in this specific setting. Regardless, the paper does not address this, and it undermines confidence in whether sparsity or weak dense ANN baselines drive the observed SNN improvements.

### Minor

- **The headline "99% energy reduction" is largely a mechanical consequence of the chosen sparsity level (Section 3.2, Table 1).** Equation (1) defines energy as total_spikes × E_s, where total spike events scale with the number of connections. With 99% fewer connections, energy is mechanically ~1% of the dense case even holding firing rates constant. The reported energy reductions in Table 1 closely mirror the nominal sparsity levels (99% sparsity → ~99% reduction; 50% sparsity → ~31–47% reduction; 70% sparsity → ~59% reduction). The paper acknowledges this mechanism in passing ("because sparse SNNs benefit from structure connection sparsity that reduces active links," lines 223–224) but still presents the reduction as a headline empirical result. The non-trivial component — whether firing rates differ between sparse and dense SNNs — is not analyzed. The paper would be strengthened by isolating the firing-rate contribution to energy differences.

- **Statistical tests in the time-lag analysis pool non-independent data points (Section 3.3, lines 231).** The analysis pools data from "all grid-search experiments involving methods 1,2 across four architecture-dataset combinations." Multiple data points from the same architecture-dataset pair (each from a different hyperparameter configuration) are not independent. The Wilcoxon signed-rank and Mann-Whitney tests assume independent observations. The astronomical p-values (down to 10⁻⁴³) are suggestive of a real effect, but the reported strength of evidence is overstated. A proper analysis would either average within each architecture-dataset combination or use a model that accounts for the grouping structure.

### Trivial

- **Vague explanatory claim in Discussion (line 259).** The statement that "sparsity in networks adds more non-linearity in learning, thus enabling the model to learn a better representation of features" is unsupported hand-waving. This is in the Discussion section and does not affect the paper's core claims, but the paper would be stronger by either providing a mechanistic citation or removing this claim.

## Nice-to-Haves

- **Add a CHT-trained dense baseline (0% sparsity).** This is the single highest-leverage addition. It would isolate whether sparsity or CHT's training dynamics drives the accuracy results. For ViT-B a pre-trained dense model is already used; a CHT-finetuned dense version would be similarly informative.

- **Analyze firing-rate differences between sparse and dense SNNs.** Instead of presenting the absolute energy reduction (which is mechanically determined by sparsity), analyzing whether firing rates differ between sparse and dense SNNs would reveal the genuinely non-trivial dynamic.

- **Sparsity-level ablation.** A sweep over sparsity levels (e.g., 0%, 50%, 75%, 90%, 99% for MLP) would show the accuracy-energy Pareto frontier and is the most informative single experiment the paper could add.

- **Per-architecture time-lag statistics.** Showing per-architecture time-lag results alongside the pooled analysis would address the non-independence concern and strengthen the time-lag claim.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

- For the conference version, add a CHT-trained dense baseline (CHT at 0% sparsity) for at least one architecture-dataset combination to disentangle sparsity effects from CHT training effects.
- Explain or caveat the MLP SNN > ANN accuracy anomaly more explicitly.
- Reframe the energy analysis to separate the mechanical sparsity contribution from the dynamic firing-rate contribution.
- In the time-lag analysis, either report per-architecture statistics alongside pooled results or use a statistical method that accounts for within-group dependencies.
- Clarify the dense ANN training protocol (optimizer, epochs, learning rate schedule) in the main text.

## Score and Decision

<score>6</score>
<decision>Accept</decision>