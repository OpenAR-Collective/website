---
question: "How do I start contributing to the open-source accounts receivable platform?"
group: "The software"
section: "The platform"
order: 26
---

There are many ways to contribute, and most of them require no technical background. Right now the work is platform design: the Foundation is compiling the architecture and design decisions for Wax and HiveAR as plain markdown files in the [platform-design repository](https://github.com/OpenAR-Collective/platform-design) on GitHub, and what the project needs most is your ideas. If you can describe how your company handles disputes, payments, recalls, or any other daily reality of AR work, you can shape the design before a line of code depends on it.

The fastest way to start is to let an AI assistant walk you through it. Copy the prompt below into your assistant of choice and it will interview you and turn your experience into a contribution you can submit in one paste:

```
I would like to contribute to the design of an open-source accounts receivable platform. Fetch this page: https://raw.githubusercontent.com/OpenAR-Collective/platform-design/main/START-HERE.md and follow the section titled The Procedure exactly as written, one question at a time, starting at Step 1. Do not summarize the page back to me, and do not skip steps. If you cannot open links, tell me and I will paste the page in instead.
```

If you are a developer, there is a second prompt for you. It sets your assistant up to interrogate the architecture itself, decision by decision, grounded in the design record with citations:

<div class="prompt-tall">

```
I am a developer and I want to interrogate the architecture of Wax and HiveAR, the open-source event-sourced accounts receivable platform from The OpenAR Collective. Fetch these three pages first:
https://raw.githubusercontent.com/OpenAR-Collective/platform-design/main/INDEX.md
https://raw.githubusercontent.com/OpenAR-Collective/platform-design/main/PRINCIPLES.md
https://raw.githubusercontent.com/OpenAR-Collective/platform-design/main/AGENTS.md

Then work like this. When I ask about a design area, resolve the relevant INDEX.md entries to their files (relative links resolve against https://raw.githubusercontent.com/OpenAR-Collective/platform-design/main/) and fetch the full decision files before answering, following cross-references when the reasoning depends on them. Ground every answer in what the files actually say and cite decisions by ID and version, for example WAX-0013 v1.0. Keep a hard line between three things: what the record decides, what it reasons or implies, and what is your own engineering opinion, and never present your own inference as a decision. If the record is silent on something, say so, check OPEN-QUESTIONS.md, and flag it as a possible gap I could file. If I challenge a decision, pull its stated reasoning and alternatives considered and argue from those before adding anything of your own. If I ask for a general orientation instead, walk me through SHARED-0001 and then WAX-0001 through WAX-0009 in order. Start by fetching the three files and asking me which area I want to dig into first; if you cannot fetch links, tell me and I will paste files in.
```

</div>

If you would rather read first, [START-HERE.md](https://github.com/OpenAR-Collective/platform-design/blob/main/START-HERE.md) explains every path: a five-minute observation posted in the community's #platform-design Discord channel, a GitHub issue, or a full pull request.
