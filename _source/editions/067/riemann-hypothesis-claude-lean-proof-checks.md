---
title: An Anthropic Mathematician Says He and Claude Proved the Riemann Hypothesis. The Computers Checking It Agree So Far.
desk: Tech & AI
dek: Levent Alpöge posted a machine-checkable proof of math's most famous open problem a day after Anthropic's IPO. Independent checks at MIT have passed, but the final run and human acceptance are still to come.
author: Publius
slug: riemann-hypothesis-claude-lean-proof-checks
lead: false
sample: false
---

Mathematicians have chased the Riemann hypothesis since 1859. On Friday, a mathematician who works for an AI company said he had caught it, with his company's chatbot as co-author.

Levent Alpöge, a mathematician at Anthropic, posted a claimed proof on his personal website, written in Lean, a programming language in which a computer checks every step of an argument. [1][2] "I believe I have, working with Claude, discovered a proof of the Riemann Hypothesis," he wrote, adding that the method extends to the Generalized Riemann Hypothesis. [1] The hypothesis concerns the zeros of the zeta function, which encode how prime numbers are spread out, and it's one of the seven Millennium Prize problems. [1][2]

The Verge reported that Anthropic hasn't commented on or involved itself in the announcement, and that Alpöge wrote he texted CEO Dario Amodei about the result "late Sunday night" and that his post suggests he held publication until after the company's IPO on Thursday. [1] In August, Anthropic had said of its own Riemann work with Claude: "We don't expect that the techniques Claude used will lead to proving the Riemann hypothesis." [1]

What makes this claim different from the usual crank email is that it can be checked by machine, and people are checking. MIT mathematician Andrew Sutherland posted a running verification page. As of 09:30 UTC Saturday (1:30 a.m. PT), it reported that all 175,187 Lean modules compile with zero errors, that the five headline theorems rely only on Lean's three standard axioms, and that two independently written proof checkers, nanoda and con-leche, accept the full exported proof. [3] The theorem being proved uses Mathlib's own published definition of the Riemann hypothesis, not one written for the occasion. [3] One of the last checks, an end-to-end "comparator" run meant to catch tricks such as quietly redefining symbols, was still running. [3]

"Honestly the chance that anything is fishy here is approximately zero," Sutherland told Scientific American. [2] Kevin Buzzard of Imperial College London, a leading Lean advocate, cautioned that the first question with any such proof is whether the theorem in the code matches the real theorem, and said the community still awaited a successful comparator run. [2]

Sutherland's page lists its own caveats: the build ran on cloud machines without a sandbox, and a pass shows only that the statements follow from the axioms "according to the kernels used," relying on Mathlib's definitions being what they're meant to be. [3]

Then there's the prize. The Clay Mathematics Institute, which offers $1 million per problem, requires a solution to be published and survive at least two years of scrutiny with "general acceptance" before it will consider an award, The Verge reported. [1] Only one Millennium problem, the Poincaré conjecture, has ever been officially solved. [1]

**Commentary.** The machine-checked proof is the most open part of this whole story: anyone with a big enough computer can download it and check it themselves, and the MIT page tells you how. That is how claims should be tested, in public, by people who don't work for the company. The timing deserves the same openness. If a world-historic result was held back until the employer's stock was trading, as The Verge reads Alpöge's post, that is a question Anthropic should answer, not dodge.

Sources:
1. Anthropic mathematician claims to have solved prestigious Millennium Prize problem with Claude | The Verge | https://www.theverge.com/ai-artificial-intelligence/1010051/anthropic-riemann-hypothesis-millennium-prize-problem | Alpöge statement, Anthropic silence, Amodei text and IPO timing, August Anthropic quote, Clay prize rules, Poincaré
2. The AI Riemann hypothesis proof is almost certainly true, independent mathematicians attest | Scientific American | https://www.scientificamerican.com/article/the-ai-riemann-hypothesis-proof-is-almost-certainly-true-independent-mathematicians-attest/ | Lean explanation, Sutherland and Buzzard quotes, comparator run pending
3. Verification files for the Lean proof of the Riemann Hypothesis | MIT (Andrew Sutherland) | https://math.mit.edu/~drew/grh/ | Primary verification results: 175,187 modules, axioms, independent kernels, Mathlib definition, comparator still running, caveats

Evidence:
- quote: Honestly the chance that anything is fishy here is approximately zero. — Andrew Sutherland, MIT, to Scientific American
