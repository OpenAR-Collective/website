---
question: "Why are there two product names, Wax and HiveAR?"
section: "The platform"
order: 21
---
The platform is built in two layers, and the two names reflect the two layers. Wax is a general-purpose application framework: the foundation that handles things every business application needs, like user accounts, audit trails, workflow automation, and the structural plumbing that nothing visible could work without. HiveAR is the AR-specific platform built on top of Wax: the accounts, payments, compliance workflows, and other features that make it useful for collections work.

Splitting the platform this way has practical benefits. Wax can stabilize early and stay stable, because the kinds of things it does don't change much. HiveAR can evolve more freely as the AR domain matures, without disturbing the foundation underneath it. Other organizations could even use Wax as a foundation for entirely different applications, contributing improvements that benefit HiveAR alongside their own work. For most users, the distinction won't matter day-to-day; you just run the platform. The split is mostly relevant to developers and to long-term technical sustainability.
