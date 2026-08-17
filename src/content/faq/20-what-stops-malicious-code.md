---
question: "Is this even safe? What stops someone malicious from sneaking bad code in?"
group: "The software"
section: "Building and running it"
order: 20
---
Open-source projects use formal change-control processes that, in many ways, offer better security than closed commercial software. Every proposed change to the platform is submitted as a public "pull request" that other contributors review before it can be accepted. Nothing makes it into the released software without passing review. The review history is public and permanent, so anyone can audit what changed, who proposed it, and who approved it.

This is the opposite of how proprietary software works, where you have no idea what is in the code you are running and no ability to verify that it does what the vendor claims. Closed-source platforms have a long, well-documented history of containing hidden problems their vendors did not disclose, including hardcoded administrator accounts with static passwords known internally to the vendor's staff, undocumented "support" backdoors that bypass normal authentication, and similar shortcuts that would be caught immediately in a public code review. With proprietary software you find out about these things only when a researcher reverse-engineers the product or when a breach forces disclosure. Open-source software gets reviewed by far more eyes than any single commercial vendor's internal team, and major vulnerabilities are caught and fixed publicly, often within hours of discovery. The Collective will follow established open-source security practices, including signed releases, dependency scanning, and a published process for reporting and addressing security issues responsibly.
