/**
 * Normalize URL path for comparison
 * Handles variations like trailing slashes and index.html
 * @param {string} path - The URL path to normalize
 * @returns {string} Normalized path
 */
function normalizePath(path) {
    // Remove leading/trailing slashes
    let normalized = path.replace(/^\/+|\/+$/g, '');
    // Remove index.html if present
    normalized = normalized.replace(/\/index\.html$/, '');
    // Remove trailing /index.html if present without leading slash
    normalized = normalized.replace(/index\.html$/, '');
    return normalized;
}

/**
 * Find all ancestor details elements of a given element
 * @param {HTMLElement} element - The starting element
 * @returns {Array<HTMLDetailsElement>} Array of ancestor details elements
 */
function findAncestorDetails(element) {
    const ancestors = [];
    let current = element.parentElement;

    while (current) {
        if (current.tagName === 'DETAILS') {
            ancestors.push(current);
        }
        current = current.parentElement;
    }

    return ancestors;
}

/**
 * Find the navigation link that matches the current URL
 * @param {string} currentPath - The current URL pathname
 * @returns {HTMLAnchorElement|null} The matching link or null
 */
function findMatchingNavLink(currentPath) {
    try {
        // Query all navigation links in the aside
        const links = document.querySelectorAll('aside nav a');
        if (!links || links.length === 0) {
            console.log('[Storyville] No navigation links found');
            return null;
        }

        const normalizedCurrentPath = normalizePath(currentPath);
        console.log('[Storyville] Looking for navigation match for path:', normalizedCurrentPath);

        // Try to find exact match first
        for (const link of links) {
            const href = link.getAttribute('href');
            if (!href) {
                continue;
            }

            const normalizedHref = normalizePath(href);
            if (normalizedHref === normalizedCurrentPath) {
                console.log('[Storyville] Found exact match:', href);
                return link;
            }
        }

        // If no exact match, try partial match (closest ancestor)
        let bestMatch = null;
        let bestMatchLength = 0;

        for (const link of links) {
            const href = link.getAttribute('href');
            if (!href) {
                continue;
            }

            const normalizedHref = normalizePath(href);
            // Check if current path starts with this href (partial match)
            if (normalizedCurrentPath.startsWith(normalizedHref)) {
                if (normalizedHref.length > bestMatchLength) {
                    bestMatch = link;
                    bestMatchLength = normalizedHref.length;
                }
            }
        }

        if (bestMatch) {
            console.log('[Storyville] Found partial match:', bestMatch.getAttribute('href'));
            return bestMatch;
        }

        console.log('[Storyville] No matching navigation link found for path:', currentPath);
        return null;
    } catch (e) {
        console.error('[Storyville] Error finding matching navigation link:', e);
        return null;
    }
}

/**
 * Expand all ancestor details elements for a given link
 * @param {HTMLAnchorElement} link - The navigation link
 */
function expandAncestors(link) {
    try {
        const ancestors = findAncestorDetails(link);
        console.log('[Storyville] Found', ancestors.length, 'ancestor details elements');

        // Set open attribute on all ancestors
        for (const details of ancestors) {
            if (!details.hasAttribute('open')) {
                details.setAttribute('open', 'open');
                console.log('[Storyville] Expanded ancestor details element');
            }
        }

        if (ancestors.length > 0) {
            console.log('[Storyville] Successfully expanded', ancestors.length, 'navigation nodes');
        }
    } catch (e) {
        console.error('[Storyville] Error expanding ancestor details:', e);
    }
}

/**
 * Initialize tree expansion based on current URL
 */
function init() {
    try {
        const currentPath = window.location.pathname;
        console.log('[Storyville] Initializing tree expansion for path:', currentPath);

        // Find matching navigation link
        const matchingLink = findMatchingNavLink(currentPath);
        if (!matchingLink) {
            console.log('[Storyville] No matching navigation link found, skipping tree expansion');
            return;
        }

        // Expand all ancestor details elements
        expandAncestors(matchingLink);
    } catch (e) {
        console.error('[Storyville] Error initializing tree expansion:', e);
    }
}

// Initialize on page load
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
} else {
    init();
}
