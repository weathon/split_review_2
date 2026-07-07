Now let me draft the review and run calibration.**Round 1 bracket: 4–6.**

- MMRole (similar RPA framework + dataset paper): avg 6.5 — larger dataset (85 chars, 14K dialogues), multimodal, clearer ablation.
- "Tell Me What You Don't Know" (RPA benchmark + method): avg 5.2.
- PersonaEval (RPA eval benchmark): avg 4.0.

AMADEUS sits below MMRole due to the missing component ablation, marginal Table 4 results, and Korean-only dataset scope. Above clear rejects (score 3 papers) because it has real empirical findings, rigorous human eval, and a novel dataset. I'll narrow to **4.5**.

---

## Summary
AMADEUS is a training-free RAG framework for role-playing agents comprising three components—ACTS (adaptive hierarchical text splitter), GS (LLM-guided chunk selection), and AE (attribute extractor)—layered over a RAG backbone. The paper also introduces CharacterRAG, a manually curated Korean-language persona dataset for 15 anime/manga characters with 976K written characters and 450 QA pairs. Evaluation covers in-knowledge QA accuracy across three LLMs and three embedding models, as well as out-of-knowledge personality matching (MBTI/BFI).

## Strengths
- **Table 1 MBTI/BFI results**: AMADEUS reduces Σ|d| from 19–21 (baselines) to 9, achieving 85% per-question MBTI accuracy versus 65–68% for Naive RAG and CRAG. This is a large, concrete margin on the paper's primary claim about out-of-knowledge persona consistency, and it directly operationalizes the motivating problem.
- **Human validation of GS+AE (Table 3)**: 14 evaluators using a 5-point Likert scale with Cronbach's α of 0.81–0.83 provide independent evidence that the attribute extraction pipeline produces trustworthy outputs — a step many RPA papers skip entirely.
- **Multi-model sweep**: Consistent rankings across 3 LLMs (GPT-4.1, Gemma3-27B, Qwen3-32B) × 3 embedding models, plus LightRAG and CRAG baselines, provides cross-setting robustness evidence and the finding that graph-based and web-search RAG are unsuitable for persona-consistent role-playing.

## Weaknesses

### Fatal
None.

### Major
- **Missing component ablation**: The three components (ACTS, GS, AE) are individually never ablated against the primary task metrics (Σ|d|, MBTI/BFI accuracy). Table 2 ablates chunking strategies for ACTS in retrieval similarity only, but there is no condition with GS disabled or AE disabled. Since both GS and AE invoke GPT-4.1 as a reasoning engine, it is impossible to determine whether the 21→9 Σ|d| reduction in Table 1 derives from improved chunking (ACTS), guided retrieval (GS), attribute extraction (AE), or simply GPT-4.1's general intelligence being called on each query. The three-component architecture is thus asserted but not validated as a design.
- **Marginal in-knowledge gains vs. headline "significantly enhance" claim**: In Table 4 (CharacterRAG, in-knowledge setting), ACC improvements over Naive RAG are 1.3–1.6 percentage points (92.67% vs. 91.33% for GPT-4.1; 88.00% vs. 86.44% for Gemma3; 78.89% vs. 78.44% for Qwen3). No statistical significance test is reported. The abstract's claim that AMADEUS "significantly enhances persona consistency" is supported for the out-of-knowledge setting but not for the in-knowledge setting. The paper should restrict the "significantly" qualifier or acknowledge that in-knowledge improvements are modest.

### Minor
- **Korean-language scope buried in a footnote**: CharacterRAG is sourced from Namuwiki (Korean), disclosed only in footnote 2 on page 3. All 15 characters are from Japanese anime/manga, and all persona documents are in Korean. The paper does not discuss whether ACTS's chunk length calibration, GS's LLM-based inference steps, or the overall framework generalizes to English or other languages. This limitation should be surfaced in Section 2.1 or in a Limitations section, not a footnote, since it constrains the scope of all generalization claims.
- **LLM-as-judge self-consistency risk**: Section 5.1 states GS and AE use GPT-4.1, and one of the three evaluated generators is also GPT-4.1. It is not stated which model serves as judge for ACC, ACC_L, and HS. If GPT-4.1 generates and evaluates its own responses in Table 4, there is a potential self-consistency inflation in that row.
- **GS computational cost unreported**: GS iterates up to N=30 chunks with one LLM call per chunk, potentially incurring 30× the cost of a single RAG step. Section 1 explicitly motivates RAG over full-context LLMs on cost grounds. No latency or API-cost comparison is provided to justify the tradeoff.
- **MBTI ground-truth validity from crowd votes**: GT personality types come from personality-database.com ("thousands of participants' votes"). For fictional characters, popular vote may reflect fan perception rather than a stable psychological profile (notably, Mikoto Misaka's GT=ENTJ received 0 correct MBTI votes from any method). This should be acknowledged as a limitation of the evaluation rather than left implicit.

### Trivial
- **Figure 1 panel labels**: CDF panels are labeled with MBTI types rather than character names, causing ambiguity (15 characters, but label implies the character's MBTI type is the grouping variable). Panels should use character names.
- **Figure 4 / α insensitivity**: Figure 4 shows log sim of 5.916 for α=5, 10, and 15 (identical), with α=2 marginally better at 5.92. The "optimal overlap coefficient" framing overstates the method's precision; the method is not sensitive to α across a wide range, which is actually a favorable robustness finding and should be framed as such.

## Nice-to-Haves
- Add ablation rows (ACTS only; ACTS+GS; ACTS+GS+AE) in the Table 1 setting to decompose what drives the Σ|d|=9 result.
- Brief latency/API-cost report for GS (N=30 LLM calls per query) versus Naive RAG.
- Pilot experiment or explicit discussion on cross-lingual applicability (e.g., one English persona document) to bound the generalization claim.
- Report which LLM serves as judge for ACC/ACC_L/HS, and consider using a fixed third-party judge model to avoid self-evaluation.

## Removed Points
*These points are flagged to be removed; treat them with caution.*

- **"Korean-only dataset is a fatal/structural flaw"** (Harsh Critic): The critic called this a "scoping failure" on par with the missing ablation. Verified in footnote 2: it is disclosed, and the framework is internally coherent within the Korean-language domain. Demoted to Minor — a real limitation that needs surfacing, but not a fatal flaw.
- **Table 5 missing from extracted body** (Harsh Critic): Likely an appendix table stripped by the parser. Removed per hard rule on missing appendix references.
- **"AMADEUS not acceptable without addressing all three" as rejection criterion** (Harsh Critic framing): The first concern (Korean scope) is real but minor. The third concern (ablation) is a genuine Major. The second concern (marginal Table 4 gains) is a calibration issue on the abstract's framing. Together these are Major weaknesses, not individually fatal.
- **α=2 framing as "post-hoc rationalization"** (Harsh Critic): The data in Figure 4 does support α=2 as marginally better (5.92 vs. 5.916); the insensitivity finding is real but is more of a Trivial precision issue than a methodological concern. Demoted to Trivial.

## Novel Insights
The paper surfaces a concrete and practically useful finding: graph-based RAG (LightRAG) and web-search RAG (CRAG) are actively harmful for persona-consistent role-playing due to entity ambiguity and persona contamination from external retrieval, respectively. This is demonstrated empirically across three LLMs and is more informative than the AMADEUS-vs-Naive-RAG comparison. The use of MBTI/BFI interview assessment as a proxy for evaluating out-of-knowledge persona consistency is a methodologically creative adaptation that sidesteps the infeasibility of constructing QA pairs for knowledge the character does not possess.

## Suggestions
- Add a component ablation table (ACTS-only / +GS / +GS+AE) in the Table 1 (MBTI/BFI) setting. This is the single highest-impact revision.
- Rephrase the abstract claim to "significantly enhances persona consistency, particularly for out-of-knowledge queries" to match the evidence.
- Move Korean-language scope disclosure from footnote 2 to Section 2.1 and add a Limitations subsection in the conclusion.
- State the judge LLM identity explicitly in Section 5.1; consider using a separate model for evaluation.
- Report GS inference overhead (average LLM calls per query, wall-clock time vs. Naive RAG baseline).

## Score and Decision

**Anchor papers (all rounds):**

| Path | Avg Score | Round | Comparison |
|------|-----------|-------|------------|
| FGSgsefE0Y (MMRole) | 6.50 | 1 | Most comparable: RPA framework + dataset; larger scale (85 chars, 14K dialogues), multimodal, clearer ablation — stronger paper than AMADEUS |
| 87DtYFaH2d (RPA refusal method+benchmark) | 5.20 | 1 | Similar domain (RPA evaluation), comparable size; AMADEUS has stronger empirical margin on its main metric |
| wZbkQStAXj (PersonaEval) | 4.00 | 1 | Benchmark-only paper, no method; AMADEUS has a stronger contribution footprint |
| BCP5nAHXqs (Human Simulacra) | 5.60 | 1 | Persona simulation framework, similar spirit; stronger ablation than AMADEUS |
| rKMQhP6iAv (Personas + Truthfulness) | 4.25 | 1 | Theoretical persona paper, weaker experiments |
| dePB45VMFx (Travel planning agents) | 5.00 | 1 | Agentic framework, different domain |
| Iyrtb9EJBp (RAG trustworthiness) | 8.00 | 1 | Strong RAG paper with training-based alignment; much more rigorous evaluation |
| oqRe1KvD17 (Reward-RAG) | 3.00 | 1 | Incomplete empirical grounding, weaker than AMADEUS |
| acDwoHrwZ8 (LLM multi-agent) | 3.00 | 1 | Different task, similar tier of empirical rigor |

**Round 1 bracket: 4–6.**
AMADEUS is above 4 (genuine contributions: strong Table 1 results, human eval, multi-model sweep, novel dataset) and below 6 (missing component ablation is a substantive methodological gap; small dataset of 15 chars; monolingual scope; marginal in-knowledge gains misrepresented as "significant"). The closest anchor is MMRole (6.5), which is a clearly better-executed paper of the same type. The next closest is Human Simulacra (5.6) and the RPA refusal paper (5.2), which have comparable contribution size. AMADEUS's ablation gap is more severe than those papers' weaknesses, placing it slightly below them.

**Final score: 4.5** — borderline reject. The paper has a clear and interesting contribution, with one strong empirical result (Table 1), but the absence of any component ablation leaves the core architectural claim unvalidated, and the headline "significantly enhances" claim is unsupported for in-knowledge queries.

MY FINAL SCORE: <score>4.5</score>
MY FINAL DECISION: <decision>Reject</decision>