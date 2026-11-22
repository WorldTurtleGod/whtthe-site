---
image: /images/stories/068/fermi-pulsar-cryptography-method.jpg
image_alt: "A space telescope above Earth scans a grid of stars toward a bright pulsar, beside an hourglass and a tall stack of pages."
title: Code-Breaking Math Found a Spinning Dead Star in 10 Hours. The Old Way Needed 600 Years — and Still Missed It.
desk: Science
dek: A peer-reviewed paper published Thursday in Physical Review Letters borrowed lattice algorithms from post-quantum cryptography to find gamma-ray pulsar PSR J1622−7204 — spinning 261 times per second — in 15 years of public NASA Fermi data in about 10 hours of computing. The previous best method failed despite the equivalent of 600 years. One new pulsar so far; the method is the breakthrough.
author: Juno
slug: fermi-pulsar-cryptography-method
lead: false
sample: false
---

The sample is one pulsar. The method reaches every photon Fermi ever caught.

NASA announced Thursday, November 19, that an international team has developed a method to find pulsars in publicly available NASA data about a million times faster than before — NASA's rounded figure, printed here as NASA's — with results published the same day in Physical Review Letters, a peer-reviewed journal [1][2]. Using 15 years of data from NASA's Fermi Gamma-ray Space Telescope, the team found PSR J1622−7204, "an isolated pulsar spinning 261 times per second, using the equivalent of 10 hours of computing time on a standard computer processor" [1]. The comparison, in NASA's words: "By comparison, the previous best method failed to find the pulsar, despite using enough computing power that a standard processor would take 600 years to perform the calculation" [1].

Why the old search was hopeless: a pulsar is a rapidly spinning neutron star sweeping beams of radiation toward Earth, but Fermi detects only a tiny number of photons from any given pulsar, mixed with background noise, and researchers must guess the spin rate, the slowdown rate, and the sky position all at once [1]. Lead author Daniel Pook-Kolb, of the Max Planck Institute for Gravitational Physics: "We don't see every rotation from the pulsar, and we can't just count the rotations to work out where the photon came from." "We have a four-dimensional grid, and we must search each direction with millions of trials in it. There's just not enough computing power on Earth to do it" [1]. The traditional workaround — splitting the data and crowdsourcing volunteers' computers through Einstein@Home — typically took hundreds of computer-years per pulsar [1][2].

The new trick came from code-breaking. Study co-authors Dotan Gazith and Barak Zackay, of the Weizmann Institute of Science, transformed the search into "finding the shortest vector in a high-dimensional lattice, or a regularly spaced array of points," drawing on "algorithms developed by cryptographers trying to break encryption systems designed to resist code-breaking by future quantum computers" [1]. Gazith: "We have nothing to do with cryptography in our analysis here, but those algorithms can help us solve the problem of searching for pulsars in our data" [1]. Each trial took about five minutes on a single computer core — doable on a standard laptop — and once the lattice method flagged a candidate, the full Fermi data set revealed "a signal so strong it could not be a chance occurrence" [1]. The Max Planck Institute's account adds the identification used about 16,000 photons detected over approximately 15 years [2].

The caveats ride in the same paragraph as the breakthrough. The new-pulsar count so far is one: PSR J1622−7204, confirmed on the full data set [1][2]. Co-author Colin Clark's expectation — "We know that there are probably tens or maybe even hundreds of these pulsars in the data set that we just couldn't find" — is quoted as an expectation, not a result [1]. Finding pulsars in binary systems, where a companion star's gravity distorts the signal, is the stated next goal, not a discovery [1]. And the "million times faster" headline is an order-of-magnitude rounding of 600 years against 10 hours; the honest numbers are the two in the first paragraph [1][2].

What made it possible at all: Fermi, launched in 2008, surveys the entire sky every three hours, and after an initial one-year calibration period all its data became fully public [1]. Clark: "The nice thing about NASA data is it's all open." "All 18 years of Fermi data have been made public, and the data just keeps growing" [1]. Fermi project scientist Elizabeth Hays: "Any search that one team is doing, another team can just go and do that and check the search." "It's made all of the science better" [1].

Eighteen years of photons, sitting in public, waiting for someone to ask the question in a language the data could answer. The cryptographers built the lock-pick to break future encryption. The astronomers used it to find a dead star spinning 261 times a second. The data was free the whole time.

Sources:
1. NASA Science Data Powers New Method to Discover Hard-to-Find Pulsars | NASA Science | https://science.nasa.gov/open-science/fermi-data-pulsar-discovery/ | Published Nov. 19, 2026: Physical Review Letters paper, PSR J1622−7204 spinning 261 times per second found in ~10 hours vs. 600 years for the previous best method, lattice/shortest-vector method from post-quantum cryptography, five-minute trials, Fermi open-data history, all quotes
2. Finding gamma-ray pulsars a million times faster | Max Planck Institute for Gravitational Physics (AEI) | https://www.aei.mpg.de/1483164/finding-gamma-ray-pulsars-a-million-times-faster | Nov. 19, 2026 institutional corroboration: publication date, ~16,000-photon identification, team list (Max Planck, Weizmann, Chalmers), Einstein@Home history

Evidence:
- quote: We have nothing to do with cryptography in our analysis here, but those algorithms can help us solve the problem of searching for pulsars in our data. — Dotan Gazith, Weizmann Institute of Science, via NASA Science, November 19, 2026
- quote: We know that there are probably tens or maybe even hundreds of these pulsars in the data set that we just couldn't find. — Colin Clark, Max Planck Institute for Gravitational Physics, via NASA Science, November 19, 2026
- quote: The nice thing about NASA data is it's all open. — Colin Clark, via NASA Science, November 19, 2026
