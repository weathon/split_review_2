## Summary

This paper proposes AtlasKV, a method for augmenting LLMs with knowledge graphs at billion-scale within 20GB VRAM by extending the KBLaM parametric knowledge injection paradigm. Two contributions are introduced: (1) **KG2KV**, which converts KG triples (h, r, t) into diverse Q-K-V training data by masking entities and rewriting relations, achieving substantially higher query diversity than KBLaM's synthetic approach; and (2) **HiKVP**, a hierarchical key-value pruning algorithm that reduces inference-time complexity from linear to sub-linear O(∛M). The method demonstrates strong memory savings (20GB VRAM for 1B triples) and improved OOD generalization over KBLaM on attention-based accuracy and GPT-scored answer relevance.

## Strengths

1. **KG2KV is a clean, principled solution to the data-diversity problem.** Converting KG triples into Q-K-V data by masking entities and rewriting relations into noun phrases is well-motivated and concretely validated. Table 1 shows a striking diversity-ratio improvement over the synthetic method (7.864% vs. 0.003%) with lower token cost (165.7 vs. 349.9). The mechanism is clearly illustrated (Figure 2) and the improvement is attributable to the conversion method itself (using KG relations as attributes vs. fixed schemas).

2. **Memory scaling results (Figure 4) are central to the paper's main claim and are well-supported.** AtlasKV staying under ~20GB VRAM for up to 1B triples while KBLaM exceeds 40GB at 10^5 triples is a meaningful engineering achievement. The sub-linear complexity analysis (Table 2) is correctly derived from the 3-layer hierarchical structure with branching factor S = ∛M, and the memory measurements directly demonstrate the practical benefit of HiKVP.

3. **Consistently strong OOD generalization over KBLaM across three datasets.** Table 3 shows AtlasKV (even with HiKVP) substantially outperforming KBLaM on the harder ATLAS-Pes2o-QKV and ATLAS-CC-QKV datasets (+40–70 points on ACC@1 in many cells). The improvement holds across multiple KG sizes and is particularly notable given that KBLaM's training data contains the same enquiry attributes as the Enron test set while AtlasKV generalizes from different training attributes.

## Weaknesses

### Major

- **Confounded comparison between AtlasKV and KBLaM: data source and architecture are conflated.** AtlasKV is trained on ATLAS-Wiki-QKV (KG2KV-converted from the ATLAS-Wiki KG), while KBLaM is trained on the Synthetic dataset (Q-K-V generated from unformatted documents via fixed schemas). These differ in both the underlying data source and the conversion pipeline. The paper attributes AtlasKV's superior OOD generalization to KG2KV's higher diversity ratio (Table 1), but the comparison mixes two variables. A controlled experiment — training AtlasKV on the Synthetic data, or training KBLaM on ATLAS-Wiki-QKV data — is needed to isolate whether the improvement comes from KG2KV's formatting or simply from using a larger/more diverse source KG. Table 3's results are striking (+60–70 points on ACC@1 in some cells), but without this control we cannot attribute them specifically to KG2KV.

### Minor

- **Answer-quality metric (GPTScore) is not reported for the full AtlasKV system with HiKVP enabled.** Figure 5 — which uses GPT-4o to score answer relevance against ground truth — only evaluates AtlasKV *w/o HiKVP* (the version without the pruning that enables scalability). While Table 3 does report attention-based accuracy for AtlasKV with HiKVP, the more direct measure of generation quality is absent for the scalable variant. This leaves a gap: we cannot confirm that the pruned system produces equivalently good answers, even though the attention-based retrieval accuracy remains high.

- **No accuracy evaluation at large scale.** The title and abstract prominently feature billion-scale capability. Memory scaling is demonstrated up to 1B triples (Figure 4), which is well-supported. However, all accuracy results (Tables 3, 4; Figure 5) cap at 10^3–10^4 triples. While it is reasonable to expect the mechanism to transfer (the complexity analysis is scale-invariant), the absence of accuracy measurements at even 10^5 or 10^6 triples makes the "billion-scale" claim in the title aspirational for accuracy rather than demonstrated.

- **RAG is absent from the accuracy evaluation despite being a central framing point.** The paper motivates AtlasKV against RAG's limitations (expensive retrieval, long-context latency) and claims comparison "to RAG methods" (line 47). Yet the only non-parametric accuracy baseline is ICL with *all* triples in context — which is not how any practical RAG system works (real RAG retrieves R ≪ M triples). A proper RAG baseline (e.g., retrieve top-k relevant triples and use them as context) would provide a fairer comparison and strengthen the paper's positioning. (The paper does include RAG in the complexity comparison of Table 2, but not in accuracy experiments.)

### Trivial

- None.

## Nice-to-Haves

- **Wall-clock time measurements** would strengthen the scalability story. The theoretical sub-linear complexity is clearly derived, but PCIe bandwidth costs from the CPU–GPU offloading/uploading in HiKVP's three-step pipeline are not measured and could be a bottleneck at each decoding step.
- **Additional ablations** such as (a) training AtlasKV's architecture on the Synthetic data, or (b) reporting GPTScore for the full HiKVP system, would directly address the confound and metric-coverage gaps identified above.
- **Details on the sentence encoder's role during inference.** The paper uses all-MiniLM-L6-v2 but does not discuss whether its capacity is sufficient for the diverse relation types that would appear in billion-scale KGs, or whether the frozen encoder could be a bottleneck for novel relation types at inference time.

## Removed Points

These points appeared in the input review but were removed after verification against the paper:

- **"Attention-based ACC@1/ACC@5 is a weak proxy / attention as explanation is fragile"** — Removed. In AtlasKV's rectangular attention architecture, the attention weights between the query and KG keys ARE the retrieval mechanism (not a post-hoc explanation of model behavior). Measuring whether the correct triple receives the highest attention weight directly tests whether the mechanism selects the right knowledge. This is the appropriate intrinsic evaluation for this architecture, not a proxy. (The separate concern about GPTScore coverage is retained above as a Minor weakness.)

- **"KBLaM training steps mismatch"** — Removed. The input review speculated that KBLaM might also improve with KG2KV-style data, which is an untested hypothesis, not a verifiable flaw in the paper.

- **"No comparison against GraphRAG or similar KG-augmented RAG methods"** — Removed. The paper's scope is parametric knowledge injection, and the baselines follow KBLaM's protocol. Including GraphRAG would be an extension, not a required comparison.

- **Table 4 header typo concern** — Removed as a likely parser artifact.

## Novel Insights

None beyond the paper's own contributions. The harsh reviewer offered no observation that reframes or deepens the paper's contribution beyond what the authors already state.

## Suggestions

1. **Run a controlled data-source ablation.** Train AtlasKV's architecture on the Synthetic data (which the paper states it has access to, line 186) to isolate whether KG2KV's formatting or the source KG diversity drives the accuracy gains.
2. **Report GPTScore for the full AtlasKV system with HiKVP.** This would close the main metric-coverage gap and directly support the claim that pruning maintains answer quality.
3. **Include a proper RAG baseline** that retrieves a small subset of relevant triples rather than placing all triples in context, to fairly represent the competing paradigm that motivates the paper.
4. **Add accuracy results at one or two larger scales** (e.g., 10^5 triples) to strengthen the billion-scale claim beyond just memory measurements.

## Score and Decision

<score>6</score>
<decision>Accept</decision>

**Rationale:** AtlasKV makes two well-motivated contributions (KG2KV and HiKVP) with concrete, reproducible engineering value. The memory scaling at 1B triples is credible and impressive. The KG2KV data-diversity improvement is convincingly demonstrated in Table 1. The major weakness — the confounded comparison between AtlasKV and KBLaM — is real but addressable; it weakens the attribution of the accuracy gains to KG2KV specifically, but the gains themselves are large and consistent across three OOD datasets. The minor weaknesses (GPTScore gap, no accuracy at scale, RAG baseline absence) are gaps in the experimental coverage rather than flaws in the method. The paper presents a credible path toward scalable parametric knowledge injection — a direction that merits publication and community discussion. With the controlled ablation and GPTScore extension suggested above, the evidentiary standard would be materially strengthened.