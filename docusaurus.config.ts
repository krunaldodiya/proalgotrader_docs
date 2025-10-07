import { themes as prismThemes } from 'prism-react-renderer';
import type { Config } from '@docusaurus/types';
import type * as Preset from '@docusaurus/preset-classic';

// This runs in Node.js - Don't use client-side code here (browser APIs, JSX...)

const config: Config = {
  title: 'ProAlgoTrader',
  tagline: 'Build profitable algorithmic trading strategies with ease',
  favicon: 'img/favicon.ico',

  // Future flags, see https://docusaurus.io/docs/api/docusaurus-config#future
  future: {
    v4: true, // Improve compatibility with the upcoming Docusaurus v4
  },

  // Set the production url of your site here
  url: 'https://docs.proalgotrader.com',
  // Set the /<baseUrl>/ pathname under which your site is served
  // For GitHub pages deployment, it is often '/<projectName>/'
  baseUrl: '/',

  // GitHub pages deployment config.
  // If you aren't using GitHub pages, you don't need these.
  organizationName: 'krunaldodiya', // Usually your GitHub org/user name.
  projectName: 'proalgotrader_docs', // Usually your repo name.

  onBrokenLinks: 'warn', // Changed from 'throw' to allow build with warnings

  // Even if you don't use internationalization, you can use this field to set
  // useful metadata like html lang. For example, if your site is Chinese, you
  // may want to replace "en" with "zh-Hans".
  i18n: {
    defaultLocale: 'en',
    locales: ['en'],
  },

  presets: [
    [
      'classic',
      {
        docs: {
          routeBasePath: '/', // Serve docs at the site's root
          sidebarPath: './sidebars.ts',
          // Please change this to your repo.
          // Remove this to remove the "edit this page" links.
          editUrl:
            'https://github.com/krunaldodiya/proalgotrader_docs/tree/main/',
        },
        blog: false,
        theme: {
          customCss: './src/css/custom.css',
        },
      } satisfies Preset.Options,
    ],
  ],

  themes: [
    [
      '@easyops-cn/docusaurus-search-local',
      {
        hashed: true,
        language: ['en'],
        highlightSearchTermsOnTargetPage: true,
        explicitSearchResultPath: true,
        indexDocs: true,
        indexBlog: false,
        indexPages: false,
        docsRouteBasePath: '/',
        searchBarShortcutHint: true,
        searchBarPosition: 'right',
      },
    ],
  ],

  themeConfig: {
    // Replace with your project's social card
    image: 'img/docusaurus-social-card.jpg',
    colorMode: {
      respectPrefersColorScheme: true,
    },
    navbar: {
      title: 'ProAlgoTrader',
      logo: {
        alt: 'ProAlgoTrader Logo',
        src: 'img/logo.svg',
        href: 'https://www.proalgotrader.com',
        target: '_blank',
      },
      items: [
        {
          type: 'docSidebar',
          sidebarId: 'docsSidebar',
          position: 'left',
          label: 'Documentation',
        },
        {
          href: 'https://www.proalgotrader.com',
          label: 'Main Website',
          position: 'right',
        },
        {
          href: 'https://github.com/krunaldodiya/proalgotrader_docs',
          label: 'GitHub',
          position: 'right',
        },
      ],
    },
    footer: {
      style: 'dark',
      links: [
        {
          title: 'Documentation',
          items: [
            {
              label: 'Getting Started',
              to: '/getting-started/installation',
            },
            {
              label: 'Core Concepts',
              to: '/core-concepts/algorithm-overview',
            },
            {
              label: 'API Reference',
              to: '/api-reference/algorithm-api',
            },
          ],
        },
        {
          title: 'Community',
          items: [
            {
              label: 'Main Website',
              href: 'https://www.proalgotrader.com',
            },
            {
              label: 'GitHub',
              href: 'https://github.com/krunaldodiya/proalgotrader_docs',
            },
            {
              label: 'Support',
              to: '/support/contact',
            },
          ],
        },
        {
          title: 'Resources',
          items: [
            {
              label: 'Examples',
              to: '/examples/README',
            },
            {
              label: 'Troubleshooting',
              to: '/support/troubleshooting',
            },
          ],
        },
      ],
      copyright: `Copyright © ${new Date().getFullYear()} ProAlgoTrader. Built with Docusaurus.`,
    },
    prism: {
      theme: prismThemes.github,
      darkTheme: prismThemes.dracula,
      additionalLanguages: ['python', 'bash', 'json', 'yaml'],
    },
  } satisfies Preset.ThemeConfig,
};

export default config;
