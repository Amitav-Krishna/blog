---
title: "Emergent Ventures Application: Neural Networks for Quantum Denoising"
date: 2026-05-21T04:30:00
draft: false
tags: ["quantum", "machine-learning", "research", "grant"]
---

I recently applied to [Emergent Ventures](https://mercatuscenter.org/emergentventures) for funding to continue my research on using neural networks to fix broken quantum measurements. Below is my full application.

---

## Describe your proposal in a tweet

I'm using neural networks to fix broken quantum measurements. My work scaled prior results from 5 to 8 qubits, but I want to attack a bottleneck when scaling up the size of the models themselves with new representations.

## About me

Quantum computers could transform drug discovery, materials science, epilepsy treatment, and many other fields that require high-fidelity simulations of the physical world. Their outputs are currently destroyed by noise, so I'm training neural networks to mend them. I'm Amitav, I'm 14, and I build things before I know how to build them. I'm also the youngest engineer at 8090 Solutions, Chamath's company, where I make their software development platform more autonomous.

In seventh grade, I started a tutoring business, going door to door to sell it, with a blog about STEM topics as a promotional tool. I would go to the Wikipedia page for a topic, skip to the sources, and get to work, trying to find any interesting bits and then doing more research to verify those claims. I would post them on Reddit, and while the comments weren't always nice, they were almost always helpful. I had a really good teacher, but the Redditors were much more honest and had much higher standards for me, which led to me having higher standards for myself. As the semester was starting to wrap up, I started working on another project, a stock email automation. My dad does trading, and I had helped him in the past with spreadsheets and whatnot, but because he had a dayjob he couldn't check every day to see which stocks were up, which were down, which were sideways, etc. So, I built my first real Python project, that would pull a stock's price against its 52-week high or low, generated buy/sell signals based on that, doing that for every stock on my dad's watchlist, and then send him an email with the signals. I ended up posting it on Reddit, which got some traction, around 70 signups, and one person who DMed me thanking me because my service had made them a bunch of money! I ran it until around October of grade 9 before shutting it down due to the server costs. I skipped eighth grade and joined TKS in ninth grade, a program focused on emerging technology, which is where I started going deeper into programming and where I later began my quantum denoising research.

Last summer I started an unpaid internship at a company, but after a few weeks they stopped replying to my emails. My brother and I both did swimming, and one thing he used to drill into me was that the clock doesn't care. The clock doesn't care if you're younger or if you're unsure about the requirements or if you were trying your best, the clock only cares about the value you provide. So, I started trying to build an LLM in C++, the hardest project I could think of at the time, to become more valuable. Every morning I would bike 10 kilometres to a library in the town over that had longer hours, I would work there from 10.00 until 18.00 (with lunch in between), bike back home, and then work from 19.00 to 23.00. When I would look at reference material, I would often not even be able to parse the notation, let alone understand the content, but after many hours and days of tutoring from ChatGPT, I had enough mathematical knowledge to understand the mechanisms by which the neural network would learn. After weeks of this, I had still not built a full LLM, which was my original goal. I'd only built a neural network.

I wrote up the project as a blog series on my personal site. My brother shared it with his CTO at 8090, who asked "why isn't this guy working for us yet?" I interviewed and got hired. This January, to decompress from spending all of winter break staying up supervising my experiments, I reimplemented my neural network in Verilog, a hardware description language, to learn more about the functioning of a neural network at each timestep.

## What's a mainstream view you absolutely agree with?

I agree that, in general, science should be publicly funded. Most fields that now receive significant amounts of private funding like semiconductors and AI were at one point funded primarily by the public. Eventually, if a field has potential, the industry will swoop in to fund it, but for that cold start period public funding is necessary. It's tempting to envision a model in which the private sector takes these kinds of bets, but one thing that I've taken away from having a few conversations with researchers in the industry is that to justify their funding they need to demonstrate how they're making money for the business. For deep learning, the time from the field getting started to it making money for people was undoubtedly at least a few decades. This sort of thing would not be sustainable in the industry, because often times whole industries will grow and die within that time. Academic institutions are quite unique in that way, in that I'm confident that the University of Toronto will be there when I die.

## About my idea

My research started as a group project for TKS where we were tasked to use quantum for real world impact. Our initial idea was to find a way to use quantum sensors for detecting cancer, however this was impractical due to quantum noise, which would creep into the sensors and make their measurements gibberish. After doing some research, I came across an interesting piece by Karan Kendre about using machine learning for quantum noise reduction of 5-qubit quantum computers (arXiv 2509.16242). After reading it though, I was left with many questions: is there anything special about CNNs for this task, could we scale up this work to larger qubit counts, could we train individual models for each noise type and do some sort of dynamic routing. Sadly, after a relatively extensive lit review, I had still come across very little. As far as I can tell, the only other paper tackling this specific task of mapping density matrix to density matrix was by Morgillo et al. (arXiv 2309.11949) on 2 and 3 qubit states. If I wanted these questions to be answered, I would have to answer them. So, I got to work.

In the remainder of the challenge, I implemented a first attempt of a transformer on this task, got some promising results, and then continued the research independently. I then began experimenting with different sizes and architectures, trying to improve performance. Eventually over winter break I tried scaling up to 8 qubits, but I encountered model collapse, where the models began outputting results that were worse than the input. After doing some diagnostics on the input data, the conclusion I came to was that they were scaled down due to the noise, which suppressed the network's learning. By reversing this squeezing effect, I was able to get much better results.

In my research, I also came across two promising representations that I did not have time nor compute to pursue. They were the Pauli basis and the Cholesky decomposed versions of the states. The way I represented them during my main experiments was with density matrices. At a high level, the diagonal terms of a density matrix tell you the probability of the circuit being in that state, while the off-diagonals tell you the relationships between the different states.

The Pauli basis is an alternative way of representing a quantum state. It consists of four operators: I, X, Y, Z. At a high level, X and Y are used to measure the way in which the different components of the state interfere and evolve over time, while Z tells you whether it will be 0 or 1. I is the identity operator, and it does nothing. You can basically compose these operators to entirely represent the state. We tried using the pauli basis, and it worked well, for unknown reasons. Our idea is to use this representation to break through the wall we hit for performance.

We also experimented with cholesky decomposition, where we basically just chop off ~half of the matrix since the matrix is symmetrical, so we don't lose any info. Theoretically you lose no information, so in an ideal case we would get the same or better performance with less memory usage, but in practice we observed that non-linearities in the evaluation made it hard for the models to learn. I believe there is low-hanging fruit in the tokenization that could allow this technique to work well.

Morgillo et al. demonstrated that feed-forward neural networks can classify states by noise type, which suggests a mixture-of-experts approach: train a classifier to identify the noise channel, then route to a specialist model for that channel, so each expert can focus on one type of noise rather than all of them. I would also like to explore scaling to 10 qubits. This is where costs become serious. At 10 qubits, 100,000 circuits would produce roughly 1.6 TiB of data. The compute is also expensive, my rough estimate is 5-7 days per experiment on the hardware I've been using, which comes to $200-400 per experiment. I'm actively researching ways to reduce this: train-time dataset generation instead of storing everything to disk, exploiting hermiticity to cut storage in half, and rethinking the tokenization.

My research plan:

- 3 weeks on the Pauli basis representation (10-15 experiments, ~$300-400)
- 4 weeks on Cholesky decomposed inputs (15-20 experiments, ~$700-800)
- 2 weeks on the mixture-of-experts approach (5-10 experiments, ~$200-350)
- 1 week on standardized evaluations comparing my approaches against prior work (~$30-40)
- Exploratory 10-qubit experiments, budget dependent on optimization progress (~$2,000-3,000)
- If accepted to IEEE qCCL in Aalborg, Denmark, conference travel (~$1,700)

Total ask: ~$7,000-8,000. If the conference doesn't happen, those funds go to additional compute.

---

**Note:** This was my application to [Emergent Ventures](https://mercatuscenter.org/emergentventures), a grant program run by Tyler Cowen at George Mason University. I applied on March 21, 2026.
