(function () {
    'use strict';

    let ws = null;
    let reconnectAttempt = 0;
    let reconnectTimeout = null;
    let reloadDebounceTimeout = null;

    const MAX_RECONNECT_DELAY = 30000; // 30 seconds
    const INITIAL_RECONNECT_DELAY = 1000; // 1 second
    const RELOAD_DEBOUNCE_DELAY = 300; // 300ms

    function getWebSocketUrl() {
        const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
        const host = window.location.host;
        return protocol + '//' + host + '/ws/reload';
    }

    function scheduleReload() {
        console.log('[Storytime] Scheduling page reload in ' + RELOAD_DEBOUNCE_DELAY + 'ms...');
        // Clear any existing debounce timeout
        if (reloadDebounceTimeout) {
            clearTimeout(reloadDebounceTimeout);
        }

        // Schedule reload after debounce delay
        reloadDebounceTimeout = setTimeout(function () {
            console.log('[Storytime] Reloading page now!');
            window.location.reload();
        }, RELOAD_DEBOUNCE_DELAY);
    }

    function connect() {
        const url = getWebSocketUrl();

        try {
            ws = new WebSocket(url);

            ws.onopen = function () {
                console.debug('[Storytime] WebSocket connected');
                // Reset reconnect attempt counter on successful connection
                reconnectAttempt = 0;
                if (reconnectTimeout) {
                    clearTimeout(reconnectTimeout);
                    reconnectTimeout = null;
                }
            };

            ws.onmessage = function (event) {
                console.debug('[Storytime] WebSocket message received:', event.data);
                try {
                    const message = JSON.parse(event.data);
                    console.debug('[Storytime] Parsed message:', message);
                    if (message.type === 'reload') {
                        console.debug('[Storytime] Reload message received, scheduling reload...');
                        scheduleReload();
                    }
                } catch (e) {
                    console.error('[Storytime] Failed to parse WebSocket message:', e);
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
        const delay = Math.min(
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
