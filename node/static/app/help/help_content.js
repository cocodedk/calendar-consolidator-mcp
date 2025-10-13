/**
 * Content registry mapping page IDs to guide content.
 */

import { dashboardGuide } from './guides/dashboard_guide.js';
import { sourcesGuide } from './guides/sources_guide.js';
import { targetGuide } from './guides/target_guide.js';
import { syncGuide } from './guides/sync_guide.js';
import { logsGuide } from './guides/logs_guide.js';
import { settingsGuide } from './guides/settings_guide.js';
import { addSourceGuide } from './guides/add_source_guide.js';

const guideRegistry = {
    'dashboard': dashboardGuide,
    'sources': sourcesGuide,
    'target': targetGuide,
    'sync': syncGuide,
    'logs': logsGuide,
    'settings': settingsGuide,
    'add-source': addSourceGuide
};

export function getGuideContent(pageId) {
    return guideRegistry[pageId] || null;
}
