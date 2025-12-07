const MAX_RECONNECT_DELAY = 30000; // 30 seconds
const INITIAL_RECONNECT_DELAY = 1000; // 1 second
const RELOAD_DEBOUNCE_DELAY = 100; // 100ms

let ws = null;
let reconnectAttempt = 0;
let reconnectTimeout = null;
let reloadDebounceTimeout = null;

function getWebSocketUrl() {
    const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
    const host = window.location.host;
    return `${protocol}//${host}/ws/reload`;
}

function isModeC() {
    const iframe = document.querySelector('iframe[src="./themed_story.html"]');
    return iframe !== null;
}

/**
 * Detect the current page type.
 * @returns {'story' | 'non_story'} Page type classification
 */
function detectPageType() {
    // Check if this is a story page (has iframe for themed story)
    if (isModeC()) {
        return 'story';
    }

    // Check if URL contains story-N pattern (story container page)
    if (window.location.pathname.includes('story-') &&
        window.location.pathname.endsWith('/index.html')) {
        return 'story';
    }

    // Everything else is non-story (docs, indexes, etc.)
    return 'non_story';
}

/**
 * Extract story identifier from current URL path.
 * Extracts story path from URLs like:
 * - /components/heading/story-0/index.html -> components/heading/story-0
 * - /components/heading/story-0/ -> components/heading/story-0
 *
 * @returns {string | null} Story identifier or null if not a story page
 */
function extractStoryId() {
    const pathname = window.location.pathname;

    // Find "story-N" segment in path
    const parts = pathname.split('/').filter(part => part !== '');

    for (let i = 0; i < parts.length; i++) {
        if (parts[i].startsWith('story-')) {
            // Return path up to and including the story-N segment
            const storyParts = parts.slice(0, i + 1);
            return storyParts.join('/');
        }
    }

    return null;
}

/**
 * Send page metadata to server on WebSocket connection.
 * Sends message: {type: "page_info", page_url, page_type, story_id}
 */
function sendPageInfo() {
    if (!ws || ws.readyState !== WebSocket.OPEN) {
        console.log('[Storyville] Cannot send page info - WebSocket not open');
        return;
    }

    const pageUrl = window.location.pathname;
    const pageType = detectPageType();
    const storyId = pageType === 'story' ? extractStoryId() : null;

    const message = {
        type: 'page_info',
        page_url: pageUrl,
        page_type: pageType,
        story_id: storyId
    };

    console.log('[Storyville] Sending page info:', message);
    ws.send(JSON.stringify(message));
}

function captureIframeScroll(iframe) {
    try {
        const scrollX = iframe.contentWindow.scrollX || 0;
        const scrollY = iframe.contentWindow.scrollY || 0;
        return { scrollX, scrollY };
    } catch (e) {
        console.log('[Storyville] Could not capture iframe scroll position (cross-origin):', e.message);
        return null;
    }
}

function restoreIframeScroll(iframe, scrollState) {
    if (!scrollState) {
        return false;
    }
    try {
        iframe.contentWindow.scrollTo(scrollState.scrollX, scrollState.scrollY);
        console.log('[Storyville] Restored iframe scroll position:', scrollState);
        return true;
    } catch (e) {
        console.log('[Storyville] Could not restore iframe scroll position (cross-origin):', e.message);
        return false;
    }
}

function applyReloadEffect(iframe) {
    iframe.classList.add('iframe-reloading');
    setTimeout(() => {
        iframe.classList.remove('iframe-reloading');
    }, 200);
}

function reloadIframe() {
    const iframe = document.querySelector('iframe[src="./themed_story.html"]');
    if (!iframe) {
        console.log('[Storyville] No iframe found for reload');
        return false;
    }

    console.log('[Storyville] Reloading iframe content');

    // Capture scroll position before reload
    const scrollState = captureIframeScroll(iframe);

    // Apply visual effect
    applyReloadEffect(iframe);

    // Set up error handler for fallback
    iframe.onerror = () => {
        console.error('[Storyville] Iframe failed to load, falling back to full page reload');
        window.location.reload();
    };

    // Set up scroll restoration after load
    iframe.onload = () => {
        console.log('[Storyville] Iframe loaded successfully');
        if (scrollState) {
            restoreIframeScroll(iframe, scrollState);
        }
    };

    // Trigger reload by updating src with timestamp
    const currentSrc = iframe.src.split('?')[0];
    iframe.src = `${currentSrc}?t=${Date.now()}`;

    return true;
}

/**
 * Handle morph_html message (stub for now - will be implemented in Task Group 5).
 * @param {string} html - HTML content to morph
 * @param {string | null} storyId - Story identifier
 */
function morphDOM(html, storyId) {
    console.log('[Storyville] DOM morphing requested for story:', storyId);
    console.log('[Storyville] DOM morphing not yet implemented, falling back to iframe reload');

    // Fallback to iframe reload
    if (!reloadIframe()) {
        // If iframe reload fails, fall back to full page reload
        console.log('[Storyville] Iframe reload failed, falling back to full page reload');
        window.location.reload();
    }
}

/**
 * Handle reload message based on change_type field.
 * Routes to appropriate reload handler:
 * - iframe_reload: reloadIframe()
 * - morph_html: morphDOM() (stub for now)
 * - full_reload: scheduleReload()
 *
 * @param {Object} message - Parsed WebSocket message
 */
function handleReloadMessage(message) {
    const changeType = message.change_type;
    const storyId = message.story_id || null;

    console.log('[Storyville] Processing reload message:', {
        type: message.type,
        change_type: changeType,
        story_id: storyId
    });

    switch (changeType) {
        case 'iframe_reload':
            console.log('[Storyville] Iframe reload requested');
            if (!reloadIframe()) {
                // If iframe reload fails, fall back to full page reload
                console.log('[Storyville] Iframe reload failed, falling back to full page reload');
                window.location.reload();
            }
            break;

        case 'morph_html':
            console.log('[Storyville] DOM morph requested for story:', storyId);
            const html = message.html;
            if (html) {
                morphDOM(html, storyId);
            } else {
                console.error('[Storyville] No HTML payload in morph_html message');
                // Fall back to iframe reload
                if (!reloadIframe()) {
                    window.location.reload();
                }
            }
            break;

        case 'full_reload':
            console.log('[Storyville] Full page reload requested');
            window.location.reload();
            break;

        default:
            console.warn('[Storyville] Unknown change_type:', changeType, '- falling back to full reload');
            window.location.reload();
    }
}

function scheduleReload() {
    console.log(`[Storyville] Scheduling reload in ${RELOAD_DEBOUNCE_DELAY}ms...`);
    // Clear any existing debounce timeout
    if (reloadDebounceTimeout) {
        clearTimeout(reloadDebounceTimeout);
    }

    // Schedule reload after debounce delay
    reloadDebounceTimeout = setTimeout(() => {
        if (isModeC()) {
            console.log('[Storyville] Mode C detected - reloading iframe only');
            reloadIframe();
        } else {
            console.log('[Storyville] Mode A/B detected - reloading full page');
            window.location.reload();
        }
    }, RELOAD_DEBOUNCE_DELAY);
}

function connect() {
    const url = getWebSocketUrl();

    try {
        ws = new WebSocket(url);

        ws.onopen = () => {
            console.log('[Storyville] WebSocket connected');
            // Reset reconnect attempt counter on successful connection
            reconnectAttempt = 0;
            if (reconnectTimeout) {
                clearTimeout(reconnectTimeout);
                reconnectTimeout = null;
            }

            // Send page metadata to server
            sendPageInfo();
        };

        ws.onmessage = (event) => {
            console.log('[Storyville] WebSocket message received:', event.data);
            try {
                const message = JSON.parse(event.data);
                console.log('[Storyville] Parsed message:', message);

                if (message.type === 'reload') {
                    // Check if this is new format (has change_type) or old format
                    if (message.change_type) {
                        handleReloadMessage(message);
                    } else {
                        // Legacy fallback for old format
                        console.log('[Storyville] Legacy reload message received, scheduling reload...');
                        scheduleReload();
                    }
                }
            } catch (e) {
                console.error('[Storyville] Failed to parse WebSocket message:', e);
            }
        };

        ws.onclose = () => {
            ws = null;
            scheduleReconnect();
        };

        ws.onerror = () => {
            // Errors are handled silently
            // Connection will be closed and onclose will trigger reconnect
        };
    } catch (e) {
        // Silently handle connection errors
        scheduleReconnect();
    }
}

function scheduleReconnect() {
    if (reconnectTimeout) {
        return; // Already scheduled
    }

    // Calculate delay with exponential backoff: 1s, 2s, 4s, 8s, 16s, 30s (max)
    const delay = Math.min(
        INITIAL_RECONNECT_DELAY * Math.pow(2, reconnectAttempt),
        MAX_RECONNECT_DELAY
    );

    reconnectAttempt++;

    reconnectTimeout = setTimeout(() => {
        reconnectTimeout = null;
        connect();
    }, delay);
}

// Start connection on page load
connect();
