// @ts-check
import { defineConfig } from 'astro/config';
import { satteri } from '@astrojs/markdown-satteri';
import sitemap from '@astrojs/sitemap';

const SITE_HOST = 'openarcollective.org';

// Links written in Markdown never pass through ExternalLink.astro, so this
// gives them the same treatment at build time: a new tab, no referrer, the
// arrow icon, and a name that says where the link goes. Keep the two in step.
// The Foundation's own subdomains, join.openarcollective.org among them, are
// not external and stay in the tab.
function isExternal(href) {
  if (typeof href !== 'string' || !/^https?:\/\//i.test(href)) return false;
  try {
    const host = new URL(href).hostname.toLowerCase();
    return host !== SITE_HOST && !host.endsWith(`.${SITE_HOST}`);
  } catch {
    return false;
  }
}

// Mirrors the markup in ExternalLink.astro; .ext-icon in global.css styles both.
function icon() {
  const path = (d) => ({ type: 'element', tagName: 'path', properties: { d }, children: [] });
  return {
    type: 'element',
    tagName: 'svg',
    properties: {
      class: 'ext-icon',
      viewBox: '0 0 24 24',
      fill: 'none',
      stroke: 'currentColor',
      'stroke-width': '2.5',
      'stroke-linecap': 'round',
      'stroke-linejoin': 'round',
      'aria-hidden': 'true',
      focusable: 'false',
    },
    children: [
      path('M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6'),
      path('M15 3h6v6'),
      path('M10 14 21 3'),
    ],
  };
}

const externalLinks = {
  name: 'openar-external-links',
  element: {
    filter: ['a'],
    visit(node, ctx) {
      if (!isExternal(node.properties?.href)) return;
      const label = ctx.textContent(node).trim();
      ctx.setProperty(node, 'target', '_blank');
      ctx.setProperty(node, 'rel', 'noopener noreferrer');
      ctx.setProperty(node, 'class', 'external');
      if (label) ctx.setProperty(node, 'aria-label', `${label} (opens in a new tab)`);
      ctx.appendChild(node, icon());
    },
  },
};

// https://astro.build/config
export default defineConfig({
  site: `https://${SITE_HOST}`,
  integrations: [sitemap()],
  markdown: {
    processor: satteri({ hastPlugins: [externalLinks] }),
  },
});
