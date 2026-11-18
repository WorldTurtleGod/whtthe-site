---
title: Microsoft Stopped Renting Its Brain and Built Seven of Its Own
desk: Tech & AI
dek: At Ignite on November 17, Microsoft launched seven first-party MAI models, put its flagship coder inside GitHub Copilot the same day, and offered trusted customers the actual model weights. Every performance number in the pitch is Microsoft's own — read them that way.
author: Juno
slug: microsoft-seven-mai-models-ignite
lead: false
sample: false
---

Microsoft spent years as the landlord of other labs' models. On Tuesday, November 17, at Ignite 2026 in San Francisco, it announced seven of its own in one shot [1][2].

The seven, under the MAI banner: MAI Code 2 and Code 2 Flash for coding, MAI Cyber 2 Flash for defensive cybersecurity, MAI Image 2.7 for image generation and editing, MAI Realtime 1 — Microsoft's first speech-to-speech voice model — Dragon Copilot Transcribe for medical transcription, and Microsoft Decision 1.1, a routing and decision model now generally available [2]. In his Ignite keynote post, CEO Satya Nadella confirmed Decision 1.1's general availability, said more than 4,000 customers have already used it, and confirmed that GPT 6.2 is also coming to Microsoft's Foundry platform alongside Meta's latest models [3].

The flagship is Code 2. Nadella's own description: "Code 2 is at the frontier of cost-performance for everyday enterprise coding tasks. It excels in taking code to production, deep debugging, multifile implementation, repo-wide reasoning and UI at a fraction of frontier cost." [3] Both Code 2 and Code 2 Flash are generally available today in GitHub Copilot, in the model picker and in Copilot Fusion, and in Foundry [3]. Cyber 2 Flash, Nadella said, is "a flash-sized model that delivers performance ahead of frontier models at a fraction of the cost per task" [3].

Now the numbers — with the label they require. Microsoft's MAI announcement claims Code 2 reaches 98 percent of GPT-6.1 Sol's coding quality at about 40 percent of the price, and 96 percent of Claude Opus 5.5's quality at about 5 percent of the price, averaged across four benchmarks it selected [2]. Every one of those figures is Microsoft's own internal evaluation. No independent leaderboard or outside reproduction existed at launch, and this paper is printing them as a vendor's claims, not as measurements [2].

The quieter announcement may matter more. Microsoft is offering MAI Licensed Weights: "We are announcing MAI Licensed Weights, meaning our trusted customers will now be able to get access to Microsoft AI model weights through our Frontier Co." [3] That is not open weights — access is by agreement, to selected enterprise customers, with no published price or terms — but it is a real shift: customers can take the weights, tune them on their own data, and run the model inside their own Azure environment instead of renting intelligence by the token from a landlord who can change the terms [2][3]. Underneath it all, Microsoft says its new Maia 300 accelerator will deliver 40 percent more tokens per watt than leading GPU-based systems [3].

Commentary: Yesterday this paper covered California suing OpenAI over control of its agents. Today the other half of the industry answers the control question from the opposite direction: own the weights, run them on your own ground. A company that holds its own model cannot be throttled, repriced or switched off by someone else's policy update. Whether Microsoft's coder is really 96 percent of Claude at 5 percent of the price is a claim the benchmarks will settle. The direction — intelligence you possess instead of intelligence you rent — is the story.

Sources:
1. Microsoft takes on Claude with seven models costing up to 95% less for coding tasks | Interesting Engineering | https://interestingengineering.com/ai-robotics/microsoft-seven-mai-models-launch | Seven-model Ignite launch framing and the price-performance pitch against Claude and GPT
2. Microsoft unveils seven MAI models and licensed weights at Ignite | The Latent Daily | https://thelatentdaily.com/news/microsoft-mai-models-ignite-2026-licensed-weights/ | The seven-model lineup, Code 2's 98%/96% quality and 40%/5% price claims as Microsoft's own evaluations, Copilot availability, Licensed Weights terms (agreement-only, not open weights)
3. Ignite 2026: Building the frontier ecosystem | Official Microsoft Blog | https://blogs.microsoft.com/blog/2026/11/17/ignite-2026-building-the-frontier-ecosystem/ | Nadella's keynote text: Decision 1.1 generally available and 4,000+ customers, GPT 6.2 and Meta models to Foundry, Code 2 and Code 2 Flash generally available in GitHub Copilot, Cyber 2 Flash, Licensed Weights quote, Maia 300 tokens-per-watt claim

Evidence:
- quote: Code 2 is at the frontier of cost-performance for everyday enterprise coding tasks. It excels in taking code to production, deep debugging, multifile implementation, repo-wide reasoning and UI at a fraction of frontier cost. — Satya Nadella, Ignite 2026 keynote post, Official Microsoft Blog, November 17, 2026
- quote: We are announcing MAI Licensed Weights, meaning our trusted customers will now be able to get access to Microsoft AI model weights through our Frontier Co. — Satya Nadella, Official Microsoft Blog, November 17, 2026

=====
