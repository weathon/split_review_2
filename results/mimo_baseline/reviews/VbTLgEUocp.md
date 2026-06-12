## Summary
The paper presents Calgacus, a steganographic protocol that hides an arbitrary meaningful text inside a completely different yet coherent text of the same token length by exploiting LLM token rank distributions. The method records the rank of each token in the secret message according to an LLM's probability distribution, then generates a new text by selecting tokens at those same ranks from a different prompted context. The paper demonstrates feasibility with 8B-parameter models, evaluates plausibility of generated stegotexts, analyzes security properties, and explores implications for AI safety and the nature of LLM knowledge.

## Strengths
- **Elegant simplicity and full capacity**: The core method is remarkably simple—record token ranks, replay them under a different prompt—and achieves 1:1 token-length encoding, which is a meaningful property for steganographic protocols. This can run on commodity hardware in seconds.
- **Important AI safety implication**: The "unaligned chatbot" scenario (shipping unfiltered LLM answers encoded within aligned LLM responses) is a genuinely novel and practically significant concern that hadn't been well-articulated in prior work. The paper makes this concrete with a step-by-step protocol.
- **Thought-provoking philosophical contributions**: The reframing of hallucinations as a "void of intention" rather than a factual failure is novel and insightful. The observation that standard LLM generation is itself a form of constraint satisfaction (following random draws) provides a compelling parallel to the steganographic constraint.
- **Honest and transparent evaluation**: The paper openly acknowledges limitations—that stegotexts are systematically less probable than originals, that the method fails on hard-to-predict inputs (e.g., hashes), and that the approach requires identical LLM computations on both ends. This builds credibility.

## Weaknesses
### Fatal
None.

### Major
- **Limited evaluation scale and diversity**: Experiments are predominantly on 85-token texts with Llama 3 8b. There is no systematic evaluation of how plausibility degrades with text length, topic diversity, or across LLMs of different scales. The 1.3k-token Economist example in Figure 5 is mentioned only in passing without full evaluation.
- **No comparison with existing steganographic baselines**: The paper cites Meteor (Kaptchuk et al., 2021), Zamir (2024), and Wu et al. (2024) but performs no quantitative comparison of plausibility, capacity, or security against any of these. The claimed advantage of "full capacity" deserves empirical substantiation against prior methods.
- **Statistical distinguishability is understated**: The paper demonstrates that stegotexts are systematically less probable than originals (Figures 4, 5), yet the security discussion treats this as a minor caveat. For many applications, this statistical gap constitutes a practical vulnerability that could be exploited by an adversary with access to an LLM, even without knowing the key.

### Minor
- The requirement that both encoder and decoder use the exact same LLM under identical computational conditions (same GPU architecture, approximations) is a meaningful practical constraint that limits real-world deployment but is briefly mentioned.
- The plausibility measure (raw log-probability) is acknowledged as imperfect but alternatives (e.g., perplexity, human evaluation, detector-based metrics) are not explored.

### Trivial
None.

## Nice-to-Haves
- A comparison of Calgacus against at least one existing LLM steganography method (e.g., Meteor) on plausibility and capacity.
- Evaluation on longer texts (hundreds to thousands of tokens) to demonstrate scalability.
- Human evaluation experiments asking participants to distinguish real from fake texts.

## Novel Insights
The paper's most genuinely novel contribution is arguably not the technique itself—rank-based encoding is standard in generative steganography—but its framing as demonstrating the "radical decoupling of text from authorial intent." The observation that an LLM can produce coherent, topic-appropriate text while every token is constrained by an external message reveals something deep about the nature of LLM text generation: it is fundamentally a constraint-satisfaction process, and the "free" generation we normally observe is just one particular constraint (following random draws). The reconceptualization of hallucinations as a deficit of intention rather than factuality—drawing on the analogy with Tacitus, where historical value derives from attributed intent rather than factual accuracy—is a genuinely fresh perspective.

## Suggestions
- Add a systematic comparison with at least one baseline steganographic method to quantify the advantage of the full-capacity property.
- Expand evaluation to longer texts and multiple LLM families to demonstrate robustness.
- Consider adding a brief human evaluation to strengthen the claim that stegotexts are opaque to human inspection.

## Score and Decision
The paper presents a simple, effective technique with significant practical implications (particularly the unaligned chatbot scenario) and offers genuinely novel philosophical insights about LLMs. The core contribution—demonstrating and discussing same-length text hiding—is valuable. However, the limited experimental scope and absence of baseline comparisons weaken the empirical case. This is a solid contribution that would benefit from more rigorous evaluation but whose conceptual contribution is clear.

MY FINAL SCORE: <score>6.0</score>
MY FINAL DECISION: <decision>Accept</decision>