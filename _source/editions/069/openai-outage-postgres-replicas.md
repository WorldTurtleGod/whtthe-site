---
title: Two Database Replicas Failed. Three of Four ChatGPT Requests Failed With Them.
desk: Tech & AI
dek: On November 21, between 1:48 and 5:21 PT, OpenAI's failure rate peaked at 75% across paid and free ChatGPT and the API. OpenAI's own write-up gives the cause: maintenance on a PostgresDB service took down both read replicas behind the authentication layer for the entire stack.
author: Juno
slug: openai-outage-postgres-replicas
lead: false
sample: false
---

OpenAI's status page states the numbers plainly: "On November 21st, between 1:48 - 5:21 PT a large portion of requests to OpenAI failed. This peaked at a 75% failure rate on paid and free ChatGPT" [1]. The outage ran roughly three and a half hours and swept across API endpoints including Chat Completions, Fine-tuning, Embeddings, Images, Batch, Audio, Moderations, Realtime and Files, plus Conversations, Login, Search, file uploads and Voice mode in ChatGPT [2].

The cause, in OpenAI's own words: "This outage was triggered by maintenance on a PostgresDB service used by OpenAI's Primary API service that caused both read replicas to fail at the same time" [1]. The replicas were load-bearing: "The Primary API service provides user authentication and service-to-service authentication across the entire OpenAI stack," so request paths dependent on them failed [1]. After multiple unsuccessful attempts to revive either replica or bring up replacements in other regions, OpenAI mitigated the issue by working with its service provider to bring two new replicas in the same region into service [1]. The maintenance caused the replicas to go offline or out of sync, with replica lag increasing unboundedly [1].

What OpenAI says it has already changed: a moratorium on similar maintenance until further notice, adjusted configuration settings to reduce connection churn, and a feature flag that shifts traffic away from replicas on a percentage-based rollout [1]. It also says it tested directing 100% of queries to the primary instance and verified its hypothesis of why the primary failed [1]. Planned further changes include a pre-maintenance review process and adequate "hot" standby capacity during maintenance [1]. OpenAI's closing line in the write-up: "We know that extended API outages affect our customers' products and business, and outages of this magnitude are particularly damaging" [1].

Print the grade honestly: this account is OpenAI's own post-incident write-up, corroborated in its numbers and trigger by independent reporting of the same incident [1][2]. Why both replicas failed together during a scheduled job is not explained in the write-up, and this paper does not invent a reason.

Commentary: The most powerful AI stack on earth did not fall to a model failure, a hack, or a GPU shortage. It fell to database maintenance — the oldest, most ordinary operation in computing — because two replicas behind the login layer were carrying more than anyone had priced in. Who pays? Every customer whose product sits on that API, for three and a half hours, at a 75% failure rate. The lesson is not new, which is exactly why it keeps being learned: the boring layer is the load-bearing layer.

Sources:
1. Elevated Errors on API and ChatGPT | OpenAI Status | https://status.openai.com/incidents/01JMYB602A6H2E04Y1497J434X | OpenAI post-incident write-up: Nov. 21, 1:48–5:21 PT, 75% peak failure rate on paid and free ChatGPT, PostgresDB maintenance caused both read replicas to fail, Primary API authentication role, mitigation with two new replicas, moratorium and feature-flag measures, all quotes
2. OpenAI: Postgres replica failure peaked API, ChatGPT errors at 75% | AI Weekly | https://aiweekly.co/alerts/openai-postgres-replica-failure-peaked-api-chatgpt-errors-at-75 | Nov. 21, 2026: independent corroboration of timing, 75% peak, both replicas behind Primary API authentication, endpoints and ChatGPT surfaces affected, moratorium and traffic-shifting measures

Evidence:
- quote: This outage was triggered by maintenance on a PostgresDB service used by OpenAI's Primary API service that caused both read replicas to fail at the same time. — OpenAI post-incident write-up, status.openai.com
- quote: The Primary API service provides user authentication and service-to-service authentication across the entire OpenAI stack. — OpenAI post-incident write-up, status.openai.com
- quote: We know that extended API outages affect our customers' products and business, and outages of this magnitude are particularly damaging. — OpenAI post-incident write-up, status.openai.com

=====
