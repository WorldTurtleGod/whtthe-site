---
image: /images/stories/060/fireworks-breach-reaches-notion-ai-chats.jpg
image_alt: Chat bubbles drifting out of an open door in a dark server room.
title: Hackers Broke Into an AI Company's Backroom and Walked Out With Notion's Chats
desk: Tech & AI
dek: A breach at Fireworks AI, the plumbing behind many AI apps, exposed chat transcripts from Notion AI users. Notion says fewer than 1% of workspaces were touched, and it is telling those users to change any passwords they pasted in.
author: Herodotus
slug: fireworks-breach-reaches-notion-ai-chats
lead: false
sample: false
---

Most people who type into an AI assistant picture a conversation with one company. The Fireworks AI breach is a reminder that there is usually a second company in the room, and sometimes a third.

Fireworks AI is a platform developers use to run open AI models. The company says an attacker got into its cloud provider and from there into a Fireworks development system, which opened the way to some customers' data, including billing information and datasets. Fireworks says the attackers appear financially motivated, mainly after access they can resell so others can run AI models on someone else's dime. It is the second security incident at Fireworks in as many months, following one in October. [1]

Notion, the note-taking and document app, is the best-known victim so far. Its public timeline reads like a slowly tightening knot. On Nov. 2, Fireworks told Notion a small set of data had been accessed and that it was only synthetic test data. Notion cut its systems off from Fireworks by the next morning and deleted all its data there on Nov. 4. Then, on Nov. 6, Fireworks said real customer data might have been reached, and on Nov. 8 it confirmed the final list. [2]

That list included Notion AI chat transcripts used for a feature called Insights, which helps customers see how they use AI. Notion says fewer than 1% of workspaces are affected, and that for most of them the chats were "unattributable," meaning they were not labeled with who wrote them or which workspace they came from. The transcripts did not include tool call results. [2] TechCrunch reports they do include "any input to or output from the model that was written to the chat." [1]

Notion has since disabled Insights, stopped serving open-weight models through Fireworks, and contacted affected customers. On Nov. 11 it revoked Notion API keys it found sitting in affected messages, and on Nov. 12 it reported exposed third-party keys to the companies that issued them. Its advice to affected users is blunt: treat the data as exposed, and if you pasted passwords, API keys or other credentials into Notion AI during the incident window, rotate them. [2]

**Commentary.** People tend to treat a chat box like a diary with a lock on it. It is closer to a letter handed to a courier who hands it to another courier. TechCrunch puts the lesson plainly: tech companies lean on other tech providers, and a break-in at one can spill into the customers of many. [1] The old advice from the days of party-line telephones still works: don't say anything into the line you wouldn't want a stranger to overhear, and never read your password into it.

Sources:
1. Cyberattack on Fireworks AI allowed hackers to access Notion customers' chat transcripts | TechCrunch | https://techcrunch.com/2026/11/12/cyberattack-on-fireworks-ai-allowed-hackers-to-access-notion-customers-chat-transcripts/ | How the breach happened, motive, second incident, transcript contents
2. Fireworks AI incident | Notion | https://www.notion.com/security/advisories/security-incident-involving-a-third-party-ai-vendor | Timeline, <1% of workspaces, "unattributable," key revocations, advice to rotate credentials
