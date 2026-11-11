---
title: AI Proved Signal's Encryption — In Four Weeks, Not Years
desk: Tech & AI
dek: Google DeepMind's new AlphaProof Code used AI agents to mathematically verify the actual compiled code behind the Signal protocol — a job DeepMind says historically took expert teams years — and found no new flaws in the parts it checked.
author: Juno
slug: alphaproof-code-verifies-signal
lead: false
sample: false
---

On November 10, Google DeepMind unveiled AlphaProof Code, a multi-LLM agentic framework for formal verification, and used it to formally verify key security properties of the actual code underlying the Signal protocol. Agents powered by Gemini Carbon generated about 6.5 million lines of machine-checked Lean proof code. The verification took just four weeks — "a task that historically takes expert teams years," according to DeepMind. [1][3]

The scope is what makes this different from a paper review. The proofs cover Signal's post-quantum PQXDH handshake and its Triple Ratchet, validating forward secrecy, authentication, post-compromise security, and handshake secrecy — down to compiled AArch64 machine code, not just the protocol design on paper. [1][3]

The human role was limited but real. Human experts worked with the AI models to turn Signal's security goals into formal mathematical specifications and reviewed every one; the agents' audit pass flagged just 1% of the codebase for a second human look, with Lean automatically checking the rest. [1]

It can also spot real bugs. As a sanity check, researchers reintroduced two real, previously fixed bugs into an isolated version of Signal's code. In both cases, the system produced a machine-checked proof that the buggy version was insecure. [1]

Now the limits, kept where they belong. WIRED reported the analysis found no new vulnerabilities in the portions examined. It did not verify the entire Signal mobile app, and the low-level cryptographic building blocks were treated as assumed-secure rather than proven from scratch. This is not proof that Signal is unhackable. It is proof that the core protocol code, as specified, does what it claims to do. [2][3]

DeepMind is open-sourcing its formal-verification artifacts for community use, and says the method could next be applied to medical-device firmware and power-grid software. Signal's chief technology officer, Ehren Kret, called it "a major breakthrough": "Using AI agents to translate live code into valid Lean theorems is a major breakthrough. As AI-driven security threats grow, rigorously verifying the Signal protocol implementation gives us even greater confidence in our code's privacy guarantees." [1]

The honest shape of this news is a speed story, not a safety blanket. A job that took expert teams years now takes an AI system four weeks — and the first thing it proved was the code that millions of people already trust with their private messages.

Sources:
1. Formal Verification of Signal's Protocol with Gemini | Google DeepMind | https://deepmind.google/blog/introducing-alphaproof-code/ | Primary announcement, Nov. 10, 2026: AlphaProof Code, Gemini Carbon agents, over six million lines of Lean, four weeks, 1% human-review flag, two reintroduced bugs caught, open-sourced artifacts, and the Ehren Kret quote
2. A New AI Tool From Google DeepMind Proved the Signal Protocol Is Secure | WIRED (via Cybernoz syndicated reproduction) | https://cybernoz.com/a-new-ai-tool-from-google-deepmind-proved-the-signal-protocol-is-secure/ | Independent WIRED reporting, Nov. 10, 2026: four-week proof of concept, no new vulnerabilities in the parts examined, known bugs correctly identified in older versions, scope limited to the protocol not the whole app, and the Swarat Chaudhuri quote
3. AlphaProof Code Verifies Signal Encryption at Machine Level | ShiftDelete | https://shiftdelete.net/en/alphaproof-code | Independent corroboration: ~6.5 million lines of Lean, ~26,000 lines of trusted specifications, PQXDH and Triple Ratchet scope, AArch64 machine-code level, and the limits (not the whole app, primitives assumed secure)

Evidence:
- quote: "Using AI agents to translate live code into valid Lean theorems is a major breakthrough. As AI-driven security threats grow, rigorously verifying the Signal protocol implementation gives us even greater confidence in our code's privacy guarantees." — Ehren Kret, Chief Technology Officer of Signal, quoted in DeepMind's announcement
- quote: "We are very excited by this result, but there is a long distance to go before we are able to scale this to all the software of the world, and we want to do that," — Swarat Chaudhuri, DeepMind research scientist, to WIRED
- quote: "Our work marks the first time AI has been used to formally verify a widely deployed cryptographic protocol at this depth. It's also the first time the implementation of a widely deployed protocol like this has been formally verified by any method, with or without AI." — Google DeepMind, announcement, Nov. 10, 2026
