---
title: "How to Use This Blog Efficiently"
date: 2024-02-01T10:00:00-05:00
draft: false
tags: ["meta", "rss"]
---

Hello! This page is on the rules of engagement on this website.

## "I want to get more content from you, but I'm worried I'll forget about your existence"

Has this ever happened to you? We have a revolutionary new technology to ease your woes: [RSS](https://en.wikipedia.org/wiki/RSS).

I use an RSS reader for most of my browsing, and I would highly recommend you do as well! The one I use is [Bubo Reader](https://github.com/georgemandis/bubo-rss), which I use because it's extremely simple, and can be deployed on your own server. You can also deploy it on [Netlify](https://netlify.com), as seen in this [demo](https://bubo-rss-demo.netlify.app).

Netlify's free plan gives us 300 credits. Here's the credit breakdown:

| Feature | Credit Usage | Description |
|---------|--------------|-------------|
| Production deploys | 15 | Deploying to production |
| Bandwidth | 10 credits per GB | Data sent to the internet |
| Web requests | 3 credits per 10,000 | Page views, API calls, etc |

Using some back-of-the-envelope math: assuming under 10,000 requests per month and under 1GB of bandwidth, that leaves us with 20 production deploys. That's enough for a reload every 36 hours. I would recommend using branch deploys instead — unlimited deploys means you can reload your reader as often as you'd like!

**TL;DR:** Use Bubo. If that seems like a hassle, the creator of this blog environment, [Karl Voit](https://karl-voit.at), recommends [NewsBlur](https://play.google.com/store/apps/details?id=com.newsblur&hl=en). The most reliable feed to use would be the links feed in the sidebar.
