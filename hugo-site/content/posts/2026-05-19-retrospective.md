---
title: "2026-05-19 Retrospective"
date: 2026-05-20T04:41:21.692020
draft: false
tags: ["daily-update"]
---

Hello!  My name is Amitav!  A good summary of today is that I did some work that then was invalidated, so I'm feeling a bit deflated.  I did quite a bit of work for 8090, but wasted quite a bit of time on setting up some infrastructure that was then nullified when my boss and I decided that it would make more sense for the system I'm working with to work with lighter-weight tools that would allow me to iterate faster as the system I'm working on will likely never see absurd levels of traffic.  That's good for future Amitav, however it is somewhat saddening for current Amitav as quite a bit of work will be redone, but it is what it is I suppose.  In addition to that, today I read [this article](https://vladfeinberg.com/2026/05/10/how-to-land-a-job-at-a-frontier-lab.html) which was interesting (it was shared with me yesterday and I did read it yesterday, but did not share it on this blog).  There are a couple of action items there that I will not act on right now due to greater priorities, but that I defer instead to the 28th (the day after final paper submissions are due for qCCL).  In particular, I lack [mathematical maturity](https://en.wikipedia.org/wiki/Mathematical_maturity), which is bad and must be solved.  Another interesting thing I read today was [this slideshow](https://www.slideshare.net/slideshow/event-streaming-a-paradigm-shift-in-enterprise-software-architecture/228574336) by my boss from a few years ago (not recommended to me by him, found it on my own), though I lack a lot of prerequisites in distributed systems and so it's mostly gibberish to me.  One thing I'd like to do eventually is learn more about distributed systems.  Today, I also listened to the podcast by David Senra on [Claude Shannon](https://podcasts.apple.com/bb/podcast/95-claude-shannon/id1141877104?i=1000581808165).  Overall it was interesting, I think my biggest takeaway is that you shouldn't take things too seriously.  Now, back to Amitav, the tasks I set out for myself yesterday are as follows:
- [X] Submit overdue photography assignment
- [ ] Complete project demo for 8090 (URGENT)
- [ ] Start longer running experiments for my QSD paper to allow the models to train to convergence
The tasks I have for tomorrow are:
- [ ] Complete project demo for 8090 (URGENT)
- [ ] Start longer running experiments for my QSD paper to allow the models to train to convergence
	- [ ] Modify hyperparameters to be an unreasonable number of epochs (>10000) with early stopping
	- [ ] Rent out two CPU pods
	- [ ] Generate the 5 qubit and 8 qubit dataset, one on each pod
	- [ ] Rent out four pods on RunPod,
	- [ ] SCP each dataset to two of the pods
	- [ ] SCP over the relevant models to each pod
	- [ ] Begin training the models
That's all from me!  Have a great day :^)	
