---
title: "2026-07-09 Retrospective"
date: 2026-07-10T03:56:56.280668
draft: false
tags: ["daily-update"]
---

Today I woke up quite late, around 11.00 EDT, because yesterday I slept relatively late (~03.00 EDT).  I scrolled (x, email, whatsapp, reddit, etc.) for a few hours, until ~18.00 EDT, until I joined a coworking call with {{REDACTED}} and {{REDACTED}}.  I created a plan with claude on how I'm going to review [Ch121a-DFT](https://github.com/ppt-2/Ch121a-DFT), and then did some review.  I learned that:
- the energy of a substance can be (lossily) modelled as a function of all of the positions of all of the nuclei within that substance,
- density functional theory is a tool for finding the function that gives the energy,
- geometry optimization is finding the positions of the nuclei (R) that minimizes the energy, i.e. finds the stable state,
$$F_i = - \frac{\partial E}{\partial R_i}$$
Where $F_i$ is the force on the *i*-th nucleus.  It's negative because we're minimizing the energy.  In general, within an atom or molecule, the force of gravity is negligible w.r.t. to the force between electrons.  Electrons are harder to model.  Let's assume a toy system, where there are three dimension x, y, and z, and 10 points on each axis.  Now, let there be 60 electrons.  For 10 points on each axis and three dimensions, that means that there are a total of $10^3 = 1000$ possible points.  Then, we have to compute the amplitude of each electron at each point, which is $1000^{60}$ possible configurations!!  Naively one would think that we can represent this as just 1000 different wave functions, but sadly we cannot, because the amplitudes of electrons are correlated.  This is very bad, because even for this relatively simple system it's intractable to store.
Now, the solution here is to commoditize (non-technical language) the electrons: instead of computing the chance of finding each electron at each point, we compute the chance of finding an electron at each point (density).  It should be noted that the chance of finding an electron at a point can be greater than 1, because we can have multiple electrons on a points (subject to the Pauli exclusion princple etc. etc.).  The storage scales *constantly* w.r.t. the electron count, only scaling as we add more points per axis, which one can intuit as being because we just give a point in our space (e.g. $[-2, 1, 3]), and then our magical functional gives us the density at that point.  This is good and tractable!

Now, finally, what you've all been waiting for, the energy as a functional of the electron density (Kohn-Sham decomposition):
$$E[n] = T_{s[n]} + E_{ext[n]} + E_{H[n]} + E_{xc[n]}$$
Where $T_{s}$ is the kinetic energy of a fictitious system with our same densities, $E_{ext[n]}$ is the external potential energy, $E_{H[n]}$ is the self-repulsion of the charge cloud, and $E_{xc[n]}$ is the exchange-correlation, aka everything not covered in the other terms, and with no *known* exact form.  
After this I goofed around a bit with [PySCF](https://pyscf.org/), scrolled some twitter, ate a turkey sandwich, went on a run for under 2 minutes, then wrote this up.  

Tomorrow is going to be gym -> library working on this chemistry stuff.  I would rate today 7/10, I did some work.  
