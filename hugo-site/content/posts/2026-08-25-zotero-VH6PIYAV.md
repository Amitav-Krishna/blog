---
title: "Reinforcement learning: an introduction"
date: 2026-08-25T03:40:42.416540
draft: false
tags: ["literature-note"]
---

*Meta: I am reading [the free online copy](http://www.incompleteideas.net/book/RLbook2020trimmed.pdf) of this textbook published by one of the authors, the legendary Richard Sutton.  I have written my Anki notes below, and provided a link through which you can download the decks as APKGs for easy import into Anki.  If you notice any errors in my notes or have any advice for how I should write these notes, email me at [krishna@amitav.net](mailto:krishna@amitav.net).  This post is very likely to change over time as I read more and more of the textbook.  No spoiler warnings because this is a technical text.*

# Chapter 0: Preface
## Anki Notes
### Components of the expected approximate action value function (Cloze)
```
[latex]$\overline{V}_{t}(s) \doteq$[/latex] {{c1::[latex]$\sum_{a} \pi(a|s) Q_{t}(s, a)$[/latex]}}
where a is {{c2::the action}}, s is {{c2::the current state}}, [latex]$\pi$[/latex] is {{c2::the current policy}}, and [latex]$Q_{t}(s, a)$[/latex] is {{c2::the action-value of action a given state s}}.
```

[Basic]
Front: The following function is the expected approximate action value at time [latex]$t$[/latex] and given state [latex]$s$[/latex] and policy [latex]$\pi$[/latex]:
[latex]$\overline{V}_{t}(S) \doteq \sum_{a} \pi(a|s) Q_{t}(s, a)$[/latex]

Explain what the function of the terms [latex]$\sum_{a}$[/latex], [latex]$\pi(a|s)$[/latex], and [latex]$Q_{t}(s, a)$[/latex] are.
Back: Firstly, [latex]$\sum_{a}$[/latex] is used to execute the terms within the summation for every possible action in state s, therefore taking the action-value of every possible action.  [latex]$\pi(a|s)$[/latex] gives the probability of action [latex]$a$[/latex], and is used to weight the action-value of the action ([latex]$Q_{t}(s, a)$[/latex]) by how probable that action is to be taken.
[/Basic]

[Basic]
Front: What is dynamic programming in the context of reinforcement learning?
Back: Dynamic programming is the family of algorithms that compute optimal value functions and policies given a perfect model of the environment.
[/Basic]

[Cloze]
An agent's policy is simultaneously {{c1::a decision-making rule}} and {{c2::a mapping from perceived states of the environment to actions to be taken when in those states}}.  
[/Cloze]

[Cloze]
A reinforcement learning system is a system that {{c1::wants something}}.
[/Cloze]



[Direct download of the preface Anki deck.](/files/Sutton_et_al._Chapter_0__Preface.apkg)
# Chapter 1: Introduction
## Anki Notes
[Basic]
Front: What does an agent's value function do?
Back: It gives the approximate total expected accumulated reward over the future, starting from the present state. 
[/Basic]

[Basic]
Front: Why doesn't the exploration-exploitation issue appear in supervised learning?
Back: In reinforcement learning, the exploitation-exploration trade-off exists because at each timestep, the agent must choose between learning about the reward of an unknown action via performing it or earning a predictable amount of reward via performing a known action. On the other hand, in supervised learning the model is explicitly told the correct label after each example, so unlike the reinforcement learning agent it needn't discover the most effective choice, it must merely remember it.
[/Basic]

[Basic]
Front: Which of the four subelements of a reinforcment learning system (policy, reward signal, model of the environment, value function) is optional?
Back: A model of the environment. 
[/Basic]

[Basic]
Front: What does an agent's reward signal do?
Back: It determines the agent's goal. 
[/Basic]

[Basic]
Front: What does an agent's policy do?
Back: It determines how an agent behaves.
[/Basic]

[Basic]
Front: The four subelements of a reinforcement learning system:
Back: 1. Policy
2. Reward signal
3. Value function
4. Model of the environment
[/Basic]

[Basic]
Front: How does the exploration-exploitation dilemma become more difficult when the task is stochastic? 
Back: When the task is stochastic, the agent must attempt an action multiple times to build a good estimate of that action's reward and a previously high-reward action may occasionally produce low reward.  This results in exploration being more expensive and exploitation being more uncertain. 
[/Basic]

[Basic]
Front: What is the exploitation-exploration trade-off in reinforcement learning?
Back: To obtain a high reward, the agent must prefer actions it has found effective at producing reward (i.e. exploiting the good actions), but in order to discover which actions produce high reward, the agent must explore many different actions, of which only a few might produce high reward while the others produce low reward.  Therefore, there is an inherent trade-off within reinforcement learning between maximizing near-term reward via exploitation of known high-reward actions and maximizing long-term value via exploration of the action space in search of the highest-value actions.  
[/Basic]

[Basic]
Front: A reinforcement learning agent has 3 aspects: 
Back: 1. Sensation
2. Action
3. Goal
[/Basic]

[Cloze]
The 2 most important distinguishing features of reinforcement learning are:
- {{c1::trial-and-error search}},
- {{c1::delayed reward}}
[/Cloze]

[Cloze]
Reinforcement learning is learning {{c1::what to do}} in order to {{c1::maximize a numerical reward signal}}.
[/Cloze]



[Direct download of the chapter 1 Anki deck.](/files/Sutton_et_al._Chapter_1__Introduction.apkg)

*[Zotero item: VH6PIYAV](/zotero/VH6PIYAV)*
