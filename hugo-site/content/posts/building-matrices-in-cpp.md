---
title: "Building Matrices in C++"
date: 2024-01-18T10:00:00-05:00
draft: false
tags: ["cpp", "systems", "math", "linear-algebra", "series"]
---

## What the hell is a matrix, anyways?

When I say matrix, you probably don't have a great idea of what a matrix actually *is*, and that's what I aim to solve.

### What the hell is a vector, really?

*This section draws heavily on the textbook Linear Algebra Done Right by Sheldon Axler*

In the previous issue I didn't go that deeply into the mathematical definition behind a vector. Sadly, before we can truly understand what a matrix is, we must first understand what a vector is.

In grade school, you should have learned about $\\mathbb{Q}$, the rational numbers, $\\mathbb{Z}$, the integers, and most importantly for this discussion, $\\mathbb{R}$, the set of all real numbers. The *set of* the real numbers ($\\mathbb{R}$) include the rational numbers and the *irrational* numbers. It does *not* include what we call *imaginary* numbers: numbers that include an imaginary part, $i$, the *imaginary unit*, which is defined as the $\\sqrt{-1}$. A *complex number* is an ordered pair $(a, b)$, where $a, b \\in \\mathbb{R}$, and written as $a + bi$. We denote the set of all complex numbers with $\\mathbb{C}$. We define $\\mathbb{F}$ as either $\\mathbb{R}$ or $\\mathbb{C}$.

*Note: This post is a work in progress — full matrix implementation coming soon.*
