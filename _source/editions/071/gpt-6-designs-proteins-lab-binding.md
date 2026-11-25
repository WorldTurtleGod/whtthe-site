---
title: A Chatbot Designed Proteins. About One in Nine Actually Stuck to Their Targets.
desk: Tech & AI
dek: OpenAI says its GPT-6 models can sketch new protein shapes and sequences with nothing but reasoning and code, and that 35 of 322 lab-tested designs bound their targets. Specialist tools still did key steps, and some scientists suspect memorization.
author: Publius
slug: gpt-6-designs-proteins-lab-binding
lead: false
sample: false
---

For years, designing a new protein meant using a specialist program like AlphaFold or RFdiffusion. On Tuesday, OpenAI said a general-purpose chatbot model can now do some of that job itself.

In a post published November 24, OpenAI said its GPT-6 family "can design new protein shapes and the sequence of their chemical building blocks using only reasoning and code, without calling specialized biology models to generate those designs." [1] The company said an internal research model "matched or outperformed specialized models on many protein design tasks." [1]

The test that matters is the lab. Working with a company called Onava, OpenAI tested 322 small binding proteins, called minibinders, based on GPT-6.2's designs against five targets. Thirty-five of them, 10.9%, bound their intended target: 5 for PD-L1, a protein some cancers use to hide from the immune system; 3 for IL-7Rα; 1 for TrkA; 8 for VEGF-A; and 18 for IL-17A. [1] Nature's news team reported the same figure, "around 11%." [2]

OpenAI's own fine print is worth reading. The company said specialized tools — Boltz-2, OpenDDE and ESMFold2 — were used to filter candidates, and that its results "do not yet establish that our models can generate de novo minibinders end-to-end" without help from specialized models. [1] It said the original RFdiffusion study reported higher hit rates, though it noted rates depend on how strictly designs are filtered. [1] On predicting a whole protein's structure from its sequence, OpenAI said even its best internal models "remained well behind" specialist tools. [1] And binding, the company said, is "only one step" toward a medicine; specificity, stability, safety and effectiveness are untested. [1]

OpenAI is not alone. Nature reported that researchers Xinming Tu of the AI biology company Phylo and Leo Chen of Harvard Medical School posted results on November 16 showing Anthropic's latest Claude models outperformed other large language models, and specialized protein language models, at predicting the sequences of obscure bacterial proteins. [2] That post "set off a frenzy among computational biologists," Nature wrote. [2]

Not everyone is sold. Nature reported that some researchers suspect part of what the chatbots show is "regurgitating training data." [2] OpenAI itself warned that unusually high accuracy on some sequence tests "may partly reflect memorization." [1] Zurich structural biologist Martin Pačesa told Nature, "In most cases, a specialist will always perform better than a generalist for a given task." [2]

OpenAI researcher Masatoshi Uehara is betting the other way: "I believe the large language model can technically beat every specialized model in even each capability," he told Nature. [2]

**Commentary.** This is genuine progress, and OpenAI deserves credit for publishing its own limits next to its claims. But the same skill that designs a protein to block a cancer signal can be aimed at worse things, and Washington will be tempted to answer with a licensing regime that only the biggest labs can afford. The founders' answer to dangerous power was to check it, not to hand a monopoly to whoever lobbies hardest. Watch who shows up asking Congress to "regulate" this, and whose competitors the rules would shut out.

Sources:
1. GPT-6 models demonstrate intrinsic protein-design capabilities | OpenAI (primary) | https://openai.com/index/gpt-6-models-demonstrate-intrinsic-protein-design-capabilities/ | Claims, 322 designs and 35 hits by target, Onava, limitations, memorization caveat
2. Watch out, AlphaFold: Claude and ChatGPT's new biology skills wow scientists | Nature | https://www.nature.com/articles/d41586-026-03836-z | Independent account of ~11% binding, Tu and Chen Claude results, skeptic and OpenAI researcher quotes

Evidence:
- quote: "do not yet establish that our models can generate de novo minibinders end-to-end in a zero-shot setting without help from specialized models." — OpenAI, Limitations section
