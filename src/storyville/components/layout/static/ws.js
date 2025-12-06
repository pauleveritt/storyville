(function () {
    'use strict';

    var ws = null;
    var reconnectAttempt = 0;
    var reconnectTimeout = null;
    var reloadDebounceTimeout = null;

    var MAX_RECONNECT_DELAY = 30000; // 30 seconds
    var INITIAL_RECONNECT_DELAY = 1000; // 1 second
    var RELOAD_DEBOUNCE_DELAY = 100; // 100ms

    function getWebSocketUrl() {
        var protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
        var host = window.location.host;
        return protocol + '//' + host + '/ws/reload';
    }

    function isModeC() {
        var iframe = document.querySelector('iframe[src="./themed_story.html"]');
        return iframe !== null;
    }

    function captureIframeScroll(iframe) {
        try {
            var scrollX = iframe.contentWindow.scrollX || 0;
            var scrollY = iframe.contentWindow.scrollY || 0;
            return { scrollX: scrollX, scrollY: scrollY };
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
        setTimeout(function () {
            iframe.classList.remove('iframe-reloading');
        }, 200);
    }

    function reloadIframe() {
        var iframe = document.querySelector('iframe[src="./themed_story.html"]');
        if (!iframe) {
            console.log('[Storyville] No iframe found for reload');
            return false;
        }

        console.log('[Storyville] Reloading iframe content');

        // Capture scroll position before reload
        var scrollState = captureIframeScroll(iframe);

        // Apply visual effect
        applyReloadEffect(iframe);

        // Set up error handler for fallback
        iframe.onerror = function () {
            console.error('[Storyville] Iframe failed to load, falling back to full page reload');
            window.location.reload();
        };

        // Set up scroll restoration after load
        iframe.onload = function () {
            console.log('[Storyville] Iframe loaded successfully');
            if (scrollState) {
                restoreIframeScroll(iframe, scrollState);
            }
        };

        // Trigger reload by updating src with timestamp
        var currentSrc = iframe.src.split('?')[0];
        iframe.src = currentSrc + '?t=' + Date.now();

        return true;
    }

    function scheduleReload() {
        console.log('[Storyville] Scheduling reload in ' + RELOAD_DEBOUNCE_DELAY + 'ms...');
        // Clear any existing debounce timeout
        if (reloadDebounceTimeout) {
            clearTimeout(reloadDebounceTimeout);
        }

        // Schedule reload after debounce delay
        reloadDebounceTimeout = setTimeout(function () {
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
        var url = getWebSocketUrl();

        try {
            ws = new WebSocket(url);

            ws.onopen = function () {
                console.log('[Storyville] WebSocket connected');
                // Reset reconnect attempt counter on successful connection
                reconnectAttempt = 0;
                if (reconnectTimeout) {
                    clearTimeout(reconnectTimeout);
                    reconnectTimeout = null;
                }
            };

            ws.onmessage = function (event) {
                console.log('[Storyville] WebSocket message received:', event.data);
                try {
                    var message = JSON.parse(event.data);
                    console.log('[Storyville] Parsed message:', message);
                    if (message.type === 'reload') {
                        console.log('[Storyville] Reload message received, scheduling reload...');
                        scheduleReload();
                    }
                } catch (e) {
                    console.error('[Storyville] Failed to parse WebSocket message:', e);
                }
            };

            ws.onclose = function () {
                ws = null;
                scheduleReconnect();
            };

            ws.onerror = function () {
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
        var delay = Math.min(
            INITIAL_RECONNECT_DELAY * Math.pow(2, reconnectAttempt),
            MAX_RECONNECT_DELAY
        );

        reconnectAttempt++;

        reconnectTimeout = setTimeout(function () {
            reconnectTimeout = null;
            connect();
        }, delay);
    }

    // Start connection on page load
    connect();
})();
