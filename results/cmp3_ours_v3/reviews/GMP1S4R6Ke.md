Here is the final consolidated review:

## Summary

LoRA-Mixer proposes a framework for composing LoRA experts by placing them at the attention projection (Q/K/V) layers with top-k routing, rather than at FFN layers or as external parallel branches. It also introduces Routing Specialization Loss (RSL), an entropy-regularized auxiliary loss designed to balance expert load and specialization. Experiments span 15 benchmarks across Transformer and SSM architectures (LLaMA3-8B, Mistral-7B, Falcon-Mamba-7B), with additional cross-model transfer experiments.

## Strengths

1. **Architecturally distinctive intervention point.** Placing LoRA experts at the Q/K/V projections (Eq. 4, Figure 1) means expert outputs flow through the core attention computation, unlike prior work targeting FFN blocks (MixLoRA) or attaching external parallel branches (MoLE). This is a well-motivated design choice grounded in the observation that projection layers are "the most expressive point of the model" (Section 3.2).

2. **Cross-model transfer experiment (Table 5).** Training a router on Mistral-7B and transferring it to LLaMA3-8B — improving GSM8K (59.13 vs 57.92) and ARC-C (79.14 vs 78.65) with zero fine-tuning — is a non-trivial demonstration that RSL-learned routing patterns capture transferable knowledge across models of the same architecture family.

3. **RSL formulation is clean and the gradient analysis is instructive.** The observation that standard auxiliary losses (Eq. 3) push toward uniform routing is correct. Adding a negative entropy term to counteract this (Eq. 5) is a well-motivated solution, and the gradient derivation (Eq. 7-9) showing how this introduces token-level signal via log p_i(x) is clearly presented.

4. **Data efficiency of RSL is a practical strength.** Table 9 shows RSL achieving comparable or superior performance with ~50% less training data (e.g., 79.26 at 2K vs 77.29 w/o RSL), which is a tangible advantage for low-resource deployment.

## Weaknesses

### Fatal
None.

### Major

1. **Abstract's headline numerical claims are unverifiable from presented results.** The abstract states gains of +3.79% (GSM8K), +2.90% (CoLA), and +3.95% (ARC-C). These specific percentages cannot be matched against any comparison in Tables 1-9 — whether computed as absolute differences or relative percentages versus base models, LoRA, MixLoRA, or any other baseline. For the LLaMA3-8B setting most likely referenced, the actual gains over LoRA on these tasks are +0.39 (GSM8K), +0.72 (CoLA), and +1.09 (ARC-C) — all far from the abstract's numbers. The paper's central quantitative claim is stated three times (abstract, introduction) but cannot be traced to any reported experimental result. This is a serious integrity issue that must be corrected.

2. **No variance or significance reporting despite small margins.** The paper reports only point averages (three runs, no standard deviations). On LLaMA3-8B (Table 2), the gains over LoRA across seven tasks have a median of ~+0.39 (range: 0.11–1.71). Gains below 1% cannot be assessed as meaningful without variance estimates. Moreover, LoRA-Mixer underperforms plain LoRA on Mistral-7B GSM8K (46.48 vs 46.67). The paper's language ("perform significantly," "significantly improves") is not supported by statistical evidence.

### Minor

3. **The "serial attention routing" framing overstates architectural novelty.** Equation (4) shows **y = Wx + F_route({α_e(x)·ΔW^(e) x})**, which is a parallel addition — the same mechanism the paper criticizes in prior parallel-branch methods (Fig. 1, methods 3-4). The genuine distinction is *where* experts attach (projection layers) rather than a serial routing mechanism. The title's "Serial Attention Routing" is therefore misleading.

4. **RSL's novelty is incremental.** RSL (Eq. 5) = standard auxiliary loss (Eq. 3) + negative entropy regularizer (−λ·ℍ[p(x)]). Entropy regularization in MoE routing has been explored previously. The paper does not adequately discuss prior entropy-based approaches to routing regularization.

5. **"Token-level specialization" is claimed but not demonstrated.** The abstract asserts "fine-grained token-level specialization," but every experiment reports aggregate task-level accuracy. The expert load analysis (Figures 3, 4) shows task-level averages, not per-token routing patterns. No within-task routing visualization or token-level case study is provided.

6. **"48% of their trainable parameters" claim is unsubstantiated.** The abstract and introduction state LoRA-Mixer uses "48% of their trainable parameters" compared to existing methods, but no parameter count comparison table appears in the main paper to verify this against specific baselines.

7. **Key hyperparameters undisclosed for main experiments.** The number of experts E and the top-k value are never specified for the main experiments (Table 2). The "LoRA" baseline in Table 2 is also underspecified — is it a single adapter per task, or something else?

8. **Selective reporting of negative results.** (a) In Table 4, LoRA-Mixer loses to LoRA-LEGO on RTE by a large margin (61.47 vs 71.85) without discussion. (b) In Table 5, the cross-model transfer degrades ARC-E (88.45 → 85.89), described only as "outperform on two of three tasks." (c) In Table 9, RSL underperforms without RSL at 4K data (78.77 vs 79.14), explained only via a deferred appendix reference.

9. **SSM extension is underexplored.** Only a single table (Falcon-Mamba in Table 2) with no architectural details on how LoRA-Mixer integrates with Mamba's recurrence rather than attention.

### Trivial
None.

## Nice-to-Haves

- Reporting FLOPs, inference latency, or memory usage to complement the parameter efficiency claims.
- Per-task routing analysis or a case study showing routing decisions for individual tokens to support the "token-level specialization" claim.
- Standard deviations or confidence intervals for all main results.
- A parameter count comparison table substantiating the "48%" claim.

## Removed Points

These points from the input review were removed or demoted for the following reasons:

- The critique about "LoRA-Mixer uses parallel-add like prior methods" was demoted to Minor (Weakness 3) because the genuine architectural difference (where experts attach) is acknowledged; the criticism is primarily about framing, not a technical failure.
- References to missing appendix content were removed per the hard rule that the parser strips appendices from all papers.
- "Missing related works" was removed per the hard rule that the merger cannot verify the existence of uncited work.
- Formatting and style nitpicks were removed per the hard rule that parser artifacts are not the authors' errors.
- The criticism that gains are "marginal" on Falcon-Mamba was narrowed because LoRA-Mixer does show clear improvements there.
- The criticism that RSL lacks theoretical support was removed because the paper does provide convergence and generalization proofs (deferred to appendix, which was stripped).

## Novel Insights

Beyond the paper's own contributions, the most notable observation from the reviews is that RSL's data efficiency (Table 9: comparable performance with ~50% less data) is a stronger and more practically compelling contribution than the raw accuracy gains, which are modest. The cross-model transfer experiment (Table 5) is also underexploited — the fact that a router trained on one model family transfers to another with zero adaptation is noteworthy, yet the paper treats it as a minor side result. Both of these angles could be developed into more compelling evidence for the method's value.

## Suggestions

1. **Fix the abstract.** Align the headline numbers precisely with a specific comparison in the paper, or remove them in favor of prose describing the range of improvements. This is non-negotiable.
2. **Report variance.** Provide standard deviations across the three runs. For gains below 1%, note whether they are within the noise margin.
3. **Disclose E and k.** State the number of experts and top-k values used in the main experiments.
4. **Add a parameter count table.** Compare total trainable parameters against each baseline at matching ranks to substantiate the "48%" claim.
5. **Discuss negative results explicitly.** Address the RTE loss (Table 4), the ARC-E degradation (Table 5), and the 4K anomaly (Table 9) in the main text rather than deferring to the appendix.
6. **Rephrase "serial attention routing"** to something more descriptively accurate (e.g., "projection-layer routing") unless a genuinely serial mechanism is present.

---

## Calibration Report

The score was calibrated against papers retrieved from the deepreview_13k_calibration dataset using topical similarity queries.

**Round 1 — Bracketing:** Searched six score bands with the query "LoRA mixture of experts routing fine-tuning LLM" (n=4 per band).

**Round 2 — Narrowing:** Searched the 3.5–5.5 band with the more specific query "LoRA-MoE routing attention projection layers multi-task adaptation" (n=3).

**Anchors used:**

| Paper | Avg Score | Decision | Round | Comparison |
|---|---|---|---|---|
| 8QTpYC4smR (systematic review) | 1.00 | Reject | R1 | Not comparable; pure survey |
| XVHXVdoV11 (model merging) | 3.40 | Reject | R1 | More principled but different setting |
| I1VCj1l1Zn (DLP-LoRA) | 3.00 | Reject | R1 | Similar LoRA fusion topic; LoRA-Mixer has more extensive experiments |
| LWvgajBmNH (MoRE) | 4.00 | Reject | R2 | Closest related paper; LoRA-Mixer has more distinctive architectural contribution and broader eval, but also has the unverifiable abstract claim that MoRE doesn't |
| PPjpGTPG5K (PERFT) | 5.33 | Reject | R1 | Called "A+B" work; LoRA-Mixer is more architecturally distinctive |
| uWvKBCYh4S (MoLE) | 5.00 | Accept | R1 | Direct baseline; MoLE accepted despite marginal improvement concerns; LoRA-Mixer has broader eval but also has the abstract claim problem |
| lTkHiXeuDl (HMoRA) | 6.00 | Accept | R1 | Cleaner presentation, clearer results, fewer presentation issues |

**Bracket:** Round 1 placed the paper in [3.5, 5.5].

**Final score:** 4.0. The paper's architectural contribution (projection-layer routing) and cross-model transfer experiment are genuine assets, placing it above DLP-LoRA (3.00) and comparable to MoRE (4.00). However, the unverifiable abstract claims, absence of variance reporting despite sub-1% gains, and overstated framing prevent it from reaching the acceptance bar set by MoLE (5.00) or HMoRA (6.00).

MY FINAL SCORE: <score>4.0</score>
MY FINAL DECISION: <decision>Reject</decision>