## Summary

DTI-DA is an end-to-end framework for drug-target interaction (DTI) prediction under domain shift. It combines a Graph Attention Network (GAT) compound encoder, a Knowledge-Aware Network (KAN) for injecting relational priors via GCN-style propagation, and dual domain adaptation objectives (MMD + adversarial gradient-reversal). Experiments on BioSNAP and BindingDB compare against classical (SVM, RF) and deep (GraphDTA, MolTrans) baselines under a cluster-based domain-split protocol.

---

## Strengths

- **Well-motivated problem framing.** The paper identifies a real and underexplored concern in DTI prediction—entity-level leakage in domain splits—and constructs cluster-based partitions that prevent compound/target overlap across source and target domains. This is a meaningful methodological contribution to evaluation practice.
- **Two-track reporting policy.** Distinguishing "source-only" from "transductive UDA" evaluation conditions is a sound and transparent decision that deserves wider adoption in the DTI literature.
- **Modular design with clear ablations.** The ablation structure (GAT, KAN, DA individually, and combined) is coherent and addresses the main components.

---

## Weaknesses

### Fatal

- **Corrupted ablation table (Figure 3 / Table in §5.2).** For the BindingDB dataset, the table lists Ours-KAN, Ours-DA, *and* Ours (All) as all having identical values: AUC = 0.7452, ACC = 0.6582. These three ablations are structurally different models and cannot legitimately produce the same numbers. This appears to be a copy-paste error, but it directly undermines the ablation study, which is the primary evidence for each component's contribution. Concurrently, the BindingDB full-model AUC (0.7452) reported in the ablation is higher than the AUC (0.654) cited for BindingDB in the main results (§5.1). These contradictions make it impossible to trust the BindingDB numbers.

### Major

- **Unfair main comparison.** The headline result pits the full DTI-DA model (transductive UDA—uses unlabeled target data) against baselines running in source-only mode. This gives the proposed method a systematic, unacknowledged advantage. The paper acknowledges the distinction in §4/§6 but does not include transductive-UDA versions of the baselines (e.g., MolTrans + MMD, GraphDTA + GRL). Without this, the observed improvement conflates the benefit of transductive access with the architectural choices.

- **Marginal gains with single-run estimates and no significance testing.** The main reported advantage over the strongest baseline (MolTrans) on BioSNAP is +0.0066 AUC absolute (+0.895% relative). The paper itself acknowledges minor run-to-run variation (e.g., 0.744 vs. 0.7452 for the same model). A gap of the same order of magnitude as run variance, measured with a single seed, provides essentially no evidence that DTI-DA outperforms MolTrans.

- **No domain-adaptation-specific baselines.** The paper claims that combining MMD and adversarial DA is a contribution, yet there is no comparison to standard DA baselines applied to DTI (e.g., DANN alone, CORAL, or MolTrans+MMD). Without these, the value of the specific DA design choices cannot be evaluated.

### Minor

- **Naming clash.** "KAN" (Knowledge-Aware Network) collides with the now-prominent Kolmogorov–Arnold Networks literature, which will confuse readers. The module itself is a standard GCN propagation step with a gating mechanism—not novel enough to warrant a new acronym.

- **BindingDB results underperform source-only baselines indirectly.** On BindingDB, the stated AUC of 0.654 (full model) barely exceeds RF (0.569) and is below MolTrans (presumably >0.68 given BioSNAP numbers), yet MolTrans is described only as a baseline without explicit BindingDB numbers being listed in the main table.

### Trivial

- Figure 3 caption references "Ours-GCN" as a typographical issue acknowledged in the text; this is a minor consistency problem.

---

## Nice-to-Haves

- Apply the transductive UDA alignment wrapper (described as available in the artifact) to the strong baselines and include those results in the main table.
- Report mean ± std over at least 3 seeds to support the marginal gains.
- Rename KAN to avoid confusion with Kolmogorov–Arnold Networks.

---

## Novel Insights

None beyond the paper's own contributions. The individual components (GAT, GCN-style relational propagation with gating, MMD, GRL-based adversarial alignment) are well established. The cluster-based leakage-free domain split is a useful evaluation practice but is not introduced here for the first time.

---

## Suggestions

- Fix the BindingDB ablation table—re-run and report distinct values for Ours-KAN, Ours-DA, and Ours (All), and reconcile with the §5.1 full-model BindingDB number.
- Add transductive UDA wrappers around GraphDTA and MolTrans as fair comparators and include them in the main table.
- Report multi-seed statistics given the marginal nature of the gains.

---

## Score and Decision

The corrupted ablation table for BindingDB is a factual error that eliminates the primary evidence for component contributions on one of two datasets. The unfair comparison (transductive vs. source-only baselines) means the headline gains cannot be attributed to the proposed architecture. Together these issues invalidate the central empirical claims of the paper in its current form.

MY FINAL SCORE: <score>3</score>
MY FINAL DECISION: <decision>Reject</decision>