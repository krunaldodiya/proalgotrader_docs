import type { SidebarsConfig } from '@docusaurus/plugin-content-docs';

/**
 * ProAlgoTrader Documentation Sidebar
 * Organized structure matching the GitBook navigation
 */
const sidebars: SidebarsConfig = {
  docsSidebar: [
    'intro',
    {
      type: 'category',
      label: 'Getting Started',
      collapsed: false,
      items: [
        'getting-started/installation',
        'getting-started/quick-start',
        'getting-started/project-structure',
      ],
    },
    {
      type: 'category',
      label: 'Core Concepts',
      collapsed: false,
      items: [
        'core-concepts/algorithm-overview',
        'core-concepts/session-management',
        'core-concepts/api-integration',
      ],
    },
    {
      type: 'category',
      label: 'Indicators',
      collapsed: false,
      items: [
        'indicators/built-in-indicators',
        'indicators/custom-indicators-guide',
        'indicators/indicator-quick-reference',
        'indicators/tradingview-indicators',
      ],
    },
    {
      type: 'category',
      label: 'Trading & Strategy',
      collapsed: false,
      items: [
        'trading-and-strategy/order-management',
        'trading-and-strategy/position-management',
        'trading-and-strategy/signal-management',
        'trading-and-strategy/risk-management',
      ],
    },
    {
      type: 'category',
      label: 'Brokers & Integration',
      collapsed: false,
      items: [
        'brokers-and-integration/supported-brokers',
        'brokers-and-integration/fyers-integration',
        'brokers-and-integration/angel-one-integration',
        'brokers-and-integration/shoonya-integration',
      ],
    },
    {
      type: 'category',
      label: 'Development',
      collapsed: false,
      items: [
        'development/development-setup',
        'development/contributing-guidelines',
        'development/testing-guide',
        'development/deployment-guide',
      ],
    },
    {
      type: 'category',
      label: 'API Reference',
      collapsed: false,
      items: [
        'api-reference/algorithm-api',
        'api-reference/core-api-reference',
        'api-reference/indicators-api',
      ],
    },
    {
      type: 'category',
      label: 'Examples',
      link: {
        type: 'doc',
        id: 'examples/README',
      },
      collapsed: false,
      items: [],
    },
    {
      type: 'category',
      label: 'Support',
      collapsed: false,
      items: [
        'support/troubleshooting',
        'support/faq',
        'support/contact',
      ],
    },
  ],
};

export default sidebars;
