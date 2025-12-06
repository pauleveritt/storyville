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
 * Find the navigation element that matches the current URL
 * This could be a link (<a>) for Story pages, or a details element for Section/Subject pages
 * @param {string} currentPath - The current URL pathname
 * @returns {HTMLElement|null} The matching element or null
 */
function findMatchingNavElement(currentPath) {
    try {
        const normalizedCurrentPath = normalizePath(currentPath);
        console.log('[Storyville] Looking for navigation match for path:', normalizedCurrentPath);

        // First, try to find exact link match (for Story pages)
        const links = document.querySelectorAll('aside nav a');
        for (const link of links) {
            const href = link.getAttribute('href');
            if (!href) {
                continue;
            }

            const normalizedHref = normalizePath(href);
            if (normalizedHref === normalizedCurrentPath) {
                console.log('[Storyville] Found exact link match:', href);
                return link;
            }
        }

        // If no exact link match, try to find matching details element by path structure
        // Section pages are at /section/index.html
        // Subject pages are at /section/subject/index.html
        const pathParts = normalizedCurrentPath.split('/').filter(p => p.length > 0);

        if (pathParts.length === 0) {
            // Root page - nothing to expand
            console.log('[Storyville] Root page - no expansion needed');
            return null;
        }

        // Find all details elements in navigation
        const allDetails = document.querySelectorAll('aside nav details');

        // Look for details whose summary text matches the path segments
        let matchedDetails = null;

        for (const details of allDetails) {
            const summary = details.querySelector('summary');
            if (!summary) {
                continue;
            }

            const summaryText = summary.textContent.trim().toLowerCase();

            // Check if any path part matches this summary
            for (const pathPart of pathParts) {
                const normalizedPathPart = pathPart.toLowerCase().replace(/-/g, ' ');
                if (summaryText === normalizedPathPart ||
                    summaryText === pathPart.toLowerCase()) {
                    console.log('[Storyville] Found details match:', summaryText, 'for path part:', pathPart);
                    matchedDetails = details;
                    break;
                }
            }
        }

        if (matchedDetails) {
            return matchedDetails;
        }

        // If still no match, try partial match on links (for nested Story pages)
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
            console.log('[Storyville] Found partial link match:', bestMatch.getAttribute('href'));
            return bestMatch;
        }

        console.log('[Storyville] No matching navigation element found for path:', currentPath);
        return null;
    } catch (e) {
        console.error('[Storyville] Error finding matching navigation element:', e);
        return null;
    }
}

/**
 * Expand all ancestor details elements for a given element
 * @param {HTMLElement} element - The navigation element (link or details)
 */
function expandAncestors(element) {
    try {
        // If the element itself is a details element, expand it
        if (element.tagName === 'DETAILS') {
            if (!element.hasAttribute('open')) {
                element.setAttribute('open', 'open');
                console.log('[Storyville] Expanded matched details element');
            }
        }

        // Find and expand all ancestor details
        const ancestors = findAncestorDetails(element);
        console.log('[Storyville] Found', ancestors.length, 'ancestor details elements');

        // Set open attribute on all ancestors
        for (const details of ancestors) {
            if (!details.hasAttribute('open')) {
                details.setAttribute('open', 'open');
                console.log('[Storyville] Expanded ancestor details element');
            }
        }

        if (ancestors.length > 0 || element.tagName === 'DETAILS') {
            const totalExpanded = ancestors.length + (element.tagName === 'DETAILS' ? 1 : 0);
            console.log('[Storyville] Successfully expanded', totalExpanded, 'navigation nodes');
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

        // Find matching navigation element (link or details)
        const matchingElement = findMatchingNavElement(currentPath);
        if (!matchingElement) {
            console.log('[Storyville] No matching navigation element found, skipping tree expansion');
            return;
        }

        // Expand all ancestor details elements (and the element itself if it's a details)
        expandAncestors(matchingElement);
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
