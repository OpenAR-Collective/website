# Contributing

Thank you for your interest in contributing to the OpenAR Collective website.

## Developer Certificate of Origin

Contributions are accepted under the [Developer Certificate of Origin, Version 1.1](https://developercertificate.org/), per Article IV of the Foundation's Open Source Policy. By signing off on a commit, you attest that the contribution is your own work, or that you have the right to submit it under the applicable license.

Every commit must carry a `Signed-off-by` trailer with your real name and email address:

```
Signed-off-by: Jane Developer <jane@example.com>
```

Git adds this for you when you commit with the `-s` flag:

```
git commit -s -m "Describe your change"
```

Pull requests with unsigned commits will be asked to rebase before merge. The Foundation does not require a Contributor License Agreement; you retain copyright in your contributions.

## Licensing of contributions

- Code contributions are accepted under the Apache License, Version 2.0 (see `LICENSE`).
- Content contributions (page copy, FAQ entries, files under `src/content`) are accepted under Creative Commons Attribution 4.0 International (see `LICENSE-CONTENT`).
- Brand assets are not open for contribution; they are governed by the Foundation's Trademark Policy.

## Practical notes

- The site is static Astro with no client-side JavaScript unless a page genuinely needs it. Please do not introduce SSR, server functions, third-party embeds, analytics, or anything that would require a cookie banner.
- Run `npm run build` before opening a pull request and confirm it completes cleanly.

Questions about this process can be directed to opensource@openarcollective.org.
