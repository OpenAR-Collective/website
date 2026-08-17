---
title: "Open Source Policy"
description: "License selection for Foundation software and documentation, and the Developer Certificate of Origin contribution model."
category: "Programs, community, and intellectual property"
order: 11
adopted: 2026-08-13
---

## ARTICLE I: PURPOSE

This Open Source Policy (the "Policy") governs the licensing of software produced under the umbrella of The Open Accounts Receivable Collective Foundation (the "Foundation") and the terms on which contributions to that software are accepted. The Foundation's exempt purpose includes the development and stewardship of open source software, educational resources, and compliance information for the public benefit. The licensing and contribution choices recorded in this Policy are the structural means by which that software serves the public.

This Policy supplements the Foundation's Trademark Policy but does not modify it. License terms govern rights to use, modify, and distribute the Foundation's software. The Trademark Policy governs use of the Foundation's name and visual identity.

## ARTICLE II: SOFTWARE COVERED

This Policy covers all software produced under the Foundation's umbrella, including:

- The Wax application framework, the Foundation's domain-agnostic event sourcing framework.

- The HiveAR accounts receivable platform, the Foundation's flagship platform built on Wax.

- Foundation-published modules, including Locale Modules, region packs, Business Class Modules, Treatment Modules, debt-type modules, and other modules distributed by the Foundation.

- Other software outputs of the Foundation, including but not limited to tooling, sample implementations, integration adapters, and educational software produced as part of the Foundation's programs.

Third-party software is not covered by this Policy. Modules and integrations produced by external contributors and not distributed by the Foundation remain under the licenses selected by their respective authors.

## ARTICLE III: LICENSE SELECTION

### Section 3.1. Flagship Software

The Foundation's flagship software, comprising the Wax application framework and the HiveAR accounts receivable platform, is licensed under the Apache License, Version 2.0. Each Foundation-maintained repository containing flagship software must include the full text of the Apache License, Version 2.0, in a LICENSE file at the repository root, and a NOTICE file as Apache 2.0 contemplates.

The Apache License, Version 2.0, was selected for the flagship software because of its express patent grant and patent termination provisions, which protect both contributors and downstream users from patent litigation; its broad permission for commercial and non-commercial use, modification, and redistribution, which maximizes adoption; and its established standing in the open source community, which reduces uncertainty for agencies and vendors who evaluate the platform.

### Section 3.2. Other Foundation Software

The Foundation's Board of Directors retains authority to select different open source licenses for other software outputs of the Foundation where doing so better serves the Foundation's mission. License selection for non-flagship software will be made by the Board on the recommendation of the maintainers of the relevant project, and recorded in the LICENSE file of the corresponding repository.

Permitted licenses for non-flagship Foundation software include Apache License, Version 2.0; the MIT License; the BSD 2-Clause and 3-Clause licenses; and copyleft licenses including the GNU General Public License, the GNU Affero General Public License, and the Mozilla Public License, where the Board determines that copyleft terms better serve the mission. The list is not exhaustive; the Board may approve any OSI-approved open source license consistent with the Foundation's Certificate of Incorporation. For modules intended to compose with the flagship software, the Board will consider license compatibility with the flagship license, and any copyleft selection will record the effect of the selected license on combined deployments.

### Section 3.3. Documentation, Educational Content, and Brand Assets

Documentation, educational resources, and other written or audiovisual content published by the Foundation will be released under Creative Commons licenses appropriate to the content, with Creative Commons Attribution 4.0 International (CC BY 4.0) as the default for general-purpose documentation and educational material. Brand assets, including logos and visual identity elements, are governed by the Foundation's Trademark Policy and are not released under an open source or Creative Commons license.

## ARTICLE IV: CONTRIBUTOR INTELLECTUAL PROPERTY MODEL

### Section 4.1. Developer Certificate of Origin

Contributions to the Foundation's codebases are accepted under the Developer Certificate of Origin (DCO), Version 1.1, as published by the Linux Foundation. Each contributor attests, on a per-commit basis, that the contribution is the contributor's own work or is contributed under a compatible open source license, and that the contributor has the right to submit the contribution under the applicable repository's license. Attestation is made by including a Signed-off-by trailer in the commit message, in the form: "Signed-off-by: Name \<email\>." Each contribution is licensed to the Foundation and to all recipients of Foundation software under the license of the repository to which it is submitted; contributions are accepted on these inbound-equals-outbound terms, and the license's patent provisions apply to each contribution accordingly.

The Foundation does not require contributors to execute a separate Contributor License Agreement (CLA). The DCO model was selected to minimize friction for first-time contributors, to align with the practice of major community-governed open source projects including the Linux kernel and the Cloud Native Computing Foundation projects, and to reflect the Foundation's commitment to a participation model accessible to individual practitioners and hobbyist contributors.

### Section 4.2. Copyright Ownership

Each contributor retains copyright in the contributor's own contributions. The Foundation does not require copyright assignment. The collective attribution in source file headers, in the form "Copyright (c) \[year\] The OpenAR Collective and contributors," is a convention indicating that the Foundation and its contributors collectively hold rights in the codebase under the applicable license. The Git commit history is the authoritative record of individual authorship.

### Section 4.3. Enforcement

Repository maintainers will configure continuous integration to verify the presence of the Signed-off-by trailer on each commit submitted for merge. Contributions missing the trailer will be returned to the contributor for sign-off before merge. Maintainers may, in their discretion, accept a sign-off retroactively from the contributor in a comment or amended commit, where the contributor confirms the DCO attestation.

## ARTICLE V: REPOSITORY PRACTICES

### Section 5.1. License Identification in Source Files

Source files in Foundation-maintained repositories will carry SPDX-License-Identifier headers identifying the file's license. The standard form is a two-line header at the top of each source file containing the SPDX-License-Identifier comment and the collective copyright notice. The full Apache License header text is not required in each source file when SPDX identifiers are used; the LICENSE file at the repository root carries the full license text. Repository maintainers will configure continuous integration to verify SPDX header presence.

### Section 5.2. Third-Party Attribution

Each Foundation-maintained repository will publish and maintain a THIRD-PARTY-NOTICES file enumerating the licenses of incorporated third-party dependencies and any attribution required by those licenses. The file may be auto-generated from the repository's dependency manifests and refreshed as part of the release process. The obligation applies to dependencies whose licenses require attribution; dependencies under licenses that do not require attribution may be omitted.

### Section 5.3. Modification Notices

The Apache License, Version 2.0, requires that modified files carry prominent notice of modification. The Foundation interprets the Git commit history of its repositories as satisfying this requirement, because each modification is recorded with author, date, and content of change. Contributors are not required to add per-file modification comments. Downstream redistributors are responsible for satisfying the modification notice requirement in their own distributions. Release artifacts distributed without version control history will identify the source repository and the release tag or commit from which they were built.

### Section 5.4. Repository Governance Documentation

Each Foundation-maintained repository will publish a CONTRIBUTING.md file describing the contribution process, code review practices, sign-off expectations, and maintainer responsibilities, and a GOVERNANCE.md file describing the maintainer model, decision-making process, conflict resolution, and release authority for the repository. Repository maintainers are authorized to update these documents consistent with this Policy and the Foundation's other governance policies.

## ARTICLE VI: AI-ASSISTED CONTRIBUTIONS

AI-assisted contributions are permitted in the Foundation's codebases. A contributor who uses an AI tool to draft, refactor, or otherwise assist in producing a contribution remains the contributor of record. The contributor's Signed-off-by attestation applies to the contribution as submitted, regardless of the tools used to produce it. The contributor is responsible for reviewing AI-generated output for correctness, license compatibility, and adherence to the project's standards before submission.

Contributors are encouraged to disclose substantial AI assistance in the pull request description, including the tool used and the nature of the assistance. Repository maintainers may require disclosure for specific categories of contribution where the use of AI assistance is material to review.

## ARTICLE VII: FOUNDATION-AFFILIATED CONTRIBUTORS

This Policy applies equally to all contributors, including the Foundation's founder, directors, officers, employees, and contractors, and entities affiliated with any of the foregoing. No Foundation-affiliated contributor receives preferential treatment in contribution review, maintainer access, or repository governance. Contributions from Foundation-affiliated contributors follow the same DCO sign-off, review, and merge process as contributions from any other party. Conflicts of interest arising from Foundation-affiliated contribution are governed by the Foundation's Conflicts of Interest Policy.

## ARTICLE VIII: POLICY ADMINISTRATION AND REVIEW

### Section 8.1. Administration and Updates

This Policy may be updated by the Foundation's Board of Directors. A change to the license selected for flagship software, or to the contributor intellectual property model, requires a recorded Board resolution. Other changes may be approved by the Board by ordinary motion. Substantive changes will be announced through the Foundation's official channels and reflected in the dated version of this Policy. The current version of this Policy supersedes any prior version.

### Section 8.2. Contact

Questions about this Policy may be directed to:

The Open Accounts Receivable Collective Foundation

3000 S Hulen Street, Suite 124-735

Fort Worth, TX 76109

opensource@openarcollective.org
