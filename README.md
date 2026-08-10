# openarcollective.org

The public website of The Open Accounts Receivable Collective Foundation, operating as The OpenAR Collective.

Static site built with [Astro](https://astro.build), deployed to Cloudflare Pages, served at [openarcollective.org](https://openarcollective.org).

## Status

Holding page live. The full site is in progress.

## Development

```
npm install
npm run dev      # local dev server
npm run build    # static build to dist/
```

Deployment is automatic: pushes to `main` are built and published by Cloudflare Pages.

## Licensing

This repository uses a split licensing model:

- **Code** (components, configuration, styles, scripts): Apache License 2.0. See [LICENSE](LICENSE).
- **Content** (page copy, FAQ entries, files under `src/content`): Creative Commons Attribution 4.0 International. See [LICENSE-CONTENT](LICENSE-CONTENT).
- **Brand assets** (the hex icon, wordmark, favicon set, and other visual identity elements): **not** open licensed. Their use is governed by the Foundation's Trademark Policy. See [public/assets/brand/README.md](public/assets/brand/README.md).

## Contributing

Contributions are accepted under the Developer Certificate of Origin, Version 1.1, with a `Signed-off-by` trailer on every commit. See [CONTRIBUTING.md](CONTRIBUTING.md).
