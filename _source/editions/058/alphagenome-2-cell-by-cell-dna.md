---
title: DeepMind's AlphaGenome 2 Reads DNA Cell by Cell
desk: Tech & AI
dek: The new model predicts how a DNA variant behaves in one specific cell type instead of a tissue average — and it finds nearly twice as many real effects as its predecessor.
author: Juno
slug: alphagenome-2-cell-by-cell-dna
lead: false
sample: false
---

Google DeepMind announced AlphaGenome 2 on Wednesday, Nov. 11, a next-generation AI model that predicts how DNA sequences and their variants affect gene activity in specific human cell types and states — not tissue averages, the way its predecessor did. [1]

The scale is the story. The model was trained on more than 107 million individual cell profiles across 68 tissues, from human and mouse bulk and single-cell data. Give it a DNA sequence of up to a million letters plus a chosen tissue, cell type, and cell state, and it predicts gene expression, chromatin accessibility, histone marks, and DNA methylation for that condition. [1]

On DeepMind's own benchmark, the improvement is stark. On TenK10K, a single-cell immune dataset spanning 28 cell types, AlphaGenome 2 recovered 30 percent of putatively causal expression-linked variants at 90 percent precision, versus 16 percent for AlphaGenome 1 fine-tuned on single-cell data — nearly twice as many. It also called 43 percent of gene-effect directions correctly, versus 23 percent for the predecessor. [1][2] Those are DeepMind's reported figures, from a preprint paper, so treat the exact numbers as the lab's own claim — but the direction is unambiguous, and the gap is large.

The model is available now for non-commercial research via the AlphaGenome API, free; commercial research is in private preview. DeepMind is blunt about the limits: this is research only, "not validated or approved for clinical or diagnostic purposes." [1] It is not open weights. DeepMind also plans AlphaGenome 2 Skills for Google Antigravity, its agentic development platform, and the Wellcome Sanger Institute is named as an ongoing collaborator. Genomics Ltd CEO Peter Donnelly said he looked forward to incorporating it into the company's Mystra platform. [1]

Why this matters: most of the DNA variants linked to disease sit outside genes, in the regulatory dark matter that tells genes when to switch on and off — and that switching is different in every cell type. A model that can say "this variant matters in this immune cell, in this state, and not in the liver cell next door" is the difference between a genetic clue and a genetic explanation. That is the road from genome-wide association studies, which hand researchers a list of suspects, to actual mechanisms, which hand them a target.

The caveat, as always with a lab's own benchmark: the preprint has not yet been through peer review, and the 30-versus-16 comparison is DeepMind measuring its own model against its own earlier model. Independent replication will tell us how much of the gain holds up in other labs' hands. But the architecture — cell-state conditioning at this scale — is a genuine step, and the fact that it is free for non-commercial research means the replication will come fast.

Sources:
1. AlphaGenome 2: Deciphering how cells read DNA to better understand disease | Google DeepMind | https://deepmind.google/blog/alphagenome-2-deciphering-how-cells-read-dna-to-better-understand-disease/ | Backs up the announcement, training scale, availability, and research-only status
2. Google DeepMind's AlphaGenome 2 Predicts Cell-State Variant Effects | Unite.AI | https://www.unite.ai/google-deepminds-alphagenome-2-predicts-cell-state-variant-effects/ | Independent write-up; backs up the 30%-vs-16% TenK10K benchmark and the API/private-preview access terms
3. AI News Nov 12, 2026: AlphaGenome 2, Runway Praxis-1, Qwen4-Max | SXF Brief | https://sxf.si/brief/ | Corroborates Nov 11 timing and places it as the day's top AI story

Evidence:
- quote: "AlphaGenome 2 identifies nearly twice as many variants that change gene expression in cells, compared to our previous state-of-the-art model." — Google DeepMind, AlphaGenome 2 announcement, Nov. 11, 2026
- quote: "Please note that AlphaGenome and AlphaGenome 2 are intended for research use only and have not been validated or approved for clinical or diagnostic purposes." — Google DeepMind, AlphaGenome 2 announcement, Nov. 11, 2026
