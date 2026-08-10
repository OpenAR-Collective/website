---
question: "Is my data safe in software whose source code anyone can read?"
section: "The platform"
order: 24
---
Yes, and arguably safer than in proprietary software. This is a common misconception worth addressing directly. Publishing source code does not expose your data; it exposes the rules the software follows. Your actual data, the consumer information, the account history, the financial records, lives in a database that you control, on infrastructure that you control, behind security measures that you implement. Nothing about the source code being public changes that.

What public source code does is allow security researchers, contributors, and your own technical staff to inspect how the software protects data. They can verify that encryption is correctly implemented, that access controls work as documented, that audit trails cannot be tampered with, and that no hidden behaviors exist. This is the opposite of proprietary software, where you have to trust the vendor's claims because you cannot inspect the code yourself. Decades of experience across the broader software industry have shown that security through transparency produces more trustworthy software than security through obscurity. Banks, hospitals, governments, and the entire backbone of the internet run on open-source software for exactly this reason.
