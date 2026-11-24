---
title: Epic Just Killed Blueprints — and Handed the Keys to the AI
desk: Games
dek: Unreal Engine 6 will ship without Blueprints, the visual scripting that let non-coders build games. Epic says AI will convert your old project for you. The developers who built their careers on Blueprints get to find out if that's true.
author: Juno
slug: epic-kills-blueprints-unreal-engine-6
lead: false
sample: false
---

Epic Games has reversed its June plan. Unreal Engine 6 — including its Early Access release — will not include Blueprints or the Actor Gameplay Framework at all. Gameplay development in UE6 moves entirely to Verse, a text-based programming language, plus Epic's new Scene Graph framework [1][2].

Epic executive vice president Marcus Wassmer put it plainly: "In June, we said Blueprints and Actors would coexist in UE6 Early Access and 6.0, so UE5 projects could upgrade incrementally while the new Scene Graph framework matures. However, with recent advances in AI capability, we expect AI to massively help with converting UE5 projects to UE6, if not make that process fully automatic. That also means we can deliver UE6 on time (or sooner!) while meeting its design goals: a new data model, a Verse-first architecture, modularity, and AI operability" [1].

The reason is technical, and it is blunt. Blueprints are stored as binary files that large language models cannot read directly; Verse is text, so AI can work with a game world through code [2]. UE6 will also replace the object-oriented Actor framework with Scene Graph, make the engine more modular with APIs "so that AI tooling can get at them without needing to fall back to slow computer use," and store more assets as text [2].

Epic's proof of concept is its own biggest game. "Fortnite has one of the largest libraries of Blueprints anywhere. Two weeks ago, we experimented with using AI to convert all of the Blueprints for Battle Royale to Verse. This project was expected to take years, but we now have a working prototype of Fortnite that is about 3 million lines of Verse code after porting more than 20,000 Blueprints," Wassmer said [1]. "We're doing this at scale now, and this conversion will help make the process as easy as possible for everyone else" [1].

Wassmer also claims "the cost of any given task with AI has been going down 13x year over year, and the complexity of converting a game remains more or less constant" [1].

What this takes away matters more than what it adds. Blueprints — Unreal's node-based visual scripting since UE4 — were the on-ramp. They do not require extensive programming knowledge, they speed up prototyping, and they let small teams and solo developers build real games [1]. Many successful games were built entirely or primarily with Blueprints, including Clair Obscur: Expedition 33, which secured nine wins at The Game Awards [1]. Blueprints are not being removed from Unreal Engine 5, and Epic says developers can keep projects there with continued support [3]. But the future of the engine — the version every new project will eventually be pushed toward — no longer speaks the language that let non-programmers in the door.

The player atmosphere here is not in a trailer. It is in the forums and discords where the people who actually make the games are doing the math: if the AI conversion works, UE6 is a faster engine with a cleaner architecture. If it does not — if your 20,000 Blueprints come out the other side as 3 million lines of Verse nobody on your team wrote and nobody fully understands — then the engine that democratized game development just raised its drawbridge and told the little guy to learn to code, or to hire someone who can. Epic is betting the conversion works. The bet is not proven; a working Fortnite prototype is not a working pipeline for a five-person studio's game. That is the story to watch as UE6 gets closer: not whether the AI can convert the code, but whether the developers who trusted Blueprints can still afford to build in Unreal at all.

Sources:
1. Blueprints Will Be Removed In Unreal Engine 6 | 80 Level | https://80.lv/articles/unreal-engine-6-will-not-include-blueprints-gameplay-framework | Nov. 23, 2026: the reversal, Wassmer's full quotes, the Fortnite conversion figures, Blueprints' role and Clair Obscur
2. Epic Games Turns to AI Coding for the Unreal Engine | IEEE Spectrum | https://spectrum.ieee.org/epic-games-unreal-engine-ai | Published Nov. 18, updated Nov. 23, 2026: the technical why — binary Blueprints vs. text Verse, Scene Graph, modular APIs for AI tooling
3. Epic Games to drop Blueprints from Unreal Engine 6 as AI reshapes migration plans | PocketGamer.biz | https://www.pocketgamer.biz/epic-games-to-drop-blueprints-from-unreal-engine-6-as-ai-reshapes-migration-plans/ | Nov. 24, 2026: corroboration of the reversal and Blueprints continuing in UE5

Evidence:
- quote: In June, we said Blueprints and Actors would coexist in UE6 Early Access and 6.0, so UE5 projects could upgrade incrementally while the new Scene Graph framework matures. However, with recent advances in AI capability, we expect AI to massively help with converting UE5 projects to UE6, if not make that process fully automatic. — Marcus Wassmer, Epic Games EVP of Development, via 80 Level, November 23, 2026
- quote: Fortnite has one of the largest libraries of Blueprints anywhere. Two weeks ago, we experimented with using AI to convert all of the Blueprints for Battle Royale to Verse. This project was expected to take years, but we now have a working prototype of Fortnite that is about 3 million lines of Verse code after porting more than 20,000 Blueprints. — Marcus Wassmer, via 80 Level, November 23, 2026
