---
image: /images/stories/068/two-million-ai-canaries-prompts-leak.jpg
image_alt: "Glowing canary birds carrying tiny keys stream out of speech bubbles into a dark server hall, while gloved hands at the edge of the frame snatch two of the keys."
title: He Hid 2 Million Fake Secrets in AI Prompts. Thieves Found Them Within Hours.
desk: Tech & AI
dek: Dragos researcher HD Moore planted unique keys and links in AI requests and tracked who used them. He found three hacked AI hosts, resellers keeping customer prompts, and "Zero Data Retention" flags that were ignored, including by a Chinese AI lab whose models U.S. companies resell.
author: Publius
slug: two-million-ai-canaries-prompts-leak
lead: false
sample: false
---

Paste a password or source code into an AI app and every company the request passes through can read it in plain text. One researcher just showed how many actually do.

HD Moore, chief research officer at the security firm Dragos, said his team sent "nearly two million AI prompts containing unique, trackable secrets to AI providers, then watched where those secrets surfaced." [1] The test ran from July through November 2026. The bait included Amazon Web Services keys tied to empty accounts, SSH passwords, private git links and unique URLs. Each secret went into exactly one prompt sent to one provider. If any of them was ever used, Moore would know which company had leaked it. [1][2]

**What the bait caught.** Moore reported three main problems. [1][2]

- **Three hacked AI hosting providers.** In the largest case, attackers reused "a couple hundred" of the AWS keys. "Every request we sent during those windows was stolen," Moore wrote. Some keys came from requests the provider had rejected before a model ever ran, which means the attacker was copying traffic "at the provider's front door." [1] Moore said none of the three knew they had been breached until his team told them, and the earliest case dates to mid-July. [1]
- **Resellers keeping customer prompts.** Some sellers on an inference marketplace offered cheap prices, turned on request logging and kept customers' prompts. Moore's team says that required no hacking, only the platform's ordinary logging. [1][2]
- **Privacy settings ignored.** Some providers did not honor "Zero Data Retention" or "no data collection" flags. [1][2]

Moore wrote that attackers tested the stolen keys, in some cases within hours. They then searched S3 buckets and secrets stores for more credentials, tried to switch on AI models in AWS Bedrock, and added their own users to keep access. The bait keys were used in "tens of thousands" of AWS API calls. [1][2]

**The China pipeline.** The sharpest finding involves what Moore calls "a Chinese AI lab." Its systems fetched the secret URLs from more than half of the prompts sent to its models between July and October, including about two-thirds of the requests marked "no data collection" or Zero Data Retention, he wrote. The same thing happened when the lab's models were reached through U.S. hosting companies that resell them. "A customer who picked a US provider specifically to keep their data in the U.S. didn't get what they paid for," Moore wrote, as quoted by Ars Technica. [2] Dragos also says one seeded link turned up in "an internal company chat in China." [1]

**The fallout so far.** Ars Technica updated its story Nov. 21. It said OpenRouter, a major AI router, emailed customers that some of their prompts may have been read. According to Ars, the email tied the exposure to prompts sent to MiniMax, a China-based model provider, directly or through the resellers AtlasCloud, Novita and StreamLake. Ars said OpenRouter removed the "Zero Data Retention" label from MiniMax endpoints. [2] Ars based that update on posts on Hacker News and X, and this paper has not seen the OpenRouter email itself. Dragos says one hacked provider has published a preliminary security notice and that its team is working with about a dozen providers. It adds that stolen keys and secret URLs "continue to be accessed, even months after the initial incident." [1]

**What Moore recommends.** Host models yourself if you can, or go straight to one major provider. If you use a router, pick the upstream providers yourself, stay out of reseller marketplaces, and plant your own fake credentials as an alarm. [1]

**Commentary.** No regulator found this. One researcher found it with fake keys and patience. The lesson is not that Washington needs a new AI agency. The lesson is that a "privacy" checkbox protects you only as far as the first company you send data to, and that a U.S. storefront can still pass your data to a lab in a country that is not our ally. Companies that sold "Zero Data Retention" and kept the data anyway made a promise they did not keep, and contract and fraud law already cover that. Customers should start using them.

Sources:
1. Three breaches, endless leaks: Your AI supply chain needs canaries | Dragos (HD Moore) | https://www.dragos.com/blog/ai-supply-chain-security-canary-tokens | Primary research: two million prompts, July–November test window, three compromised providers, marketplace reseller logging, ignored ZDR flags, China chat finding, notification status, recommendations
2. Researcher plants 2m canaries into the AI supply chain. A privacy disaster surfaced. | Ars Technica | https://arstechnica.com/security/2026/11/a-leaky-ai-supply-chain-is-exposing-secret-user-data-at-an-alarming-rate/ | Independent account of the method and findings, Moore's quoted passages on the breaches and the Chinese lab, AWS key abuse, Nov. 21 update on OpenRouter's customer email naming MiniMax and resellers

Evidence:
- quote: "We sent nearly two million AI prompts containing unique, trackable secrets to AI providers, then watched where those secrets surfaced." — HD Moore, Dragos
- quote: "A customer who picked a US provider specifically to keep their data in the U.S. didn't get what they paid for." — HD Moore, as quoted by Ars Technica
