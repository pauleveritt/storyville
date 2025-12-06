(function () {
    'use strict';

    var STORAGE_KEY = 'storyville.sidebar.collapsed';
    var COLLAPSED_CLASS = 'sidebar-collapsed';

    /**
     * Get the sidebar toggle button element
     * @returns {HTMLElement|null} The toggle button or null if not found
     */
    function getToggleButton() {
        return document.querySelector('#sidebar-toggle');
    }

    /**
     * Get the current collapsed state from localStorage
     * @returns {boolean} True if sidebar should be collapsed, false otherwise
     */
    function getStoredState() {
        try {
            var stored = localStorage.getItem(STORAGE_KEY);
            return stored === 'true';
        } catch (e) {
            console.log('[Storyville] localStorage not available:', e.message);
            return false;
        }
    }

    /**
     * Save the collapsed state to localStorage
     * @param {boolean} isCollapsed - Whether the sidebar is collapsed
     */
    function saveState(isCollapsed) {
        try {
            localStorage.setItem(STORAGE_KEY, String(isCollapsed));
        } catch (e) {
            console.log('[Storyville] Could not save to localStorage:', e.message);
        }
    }

    /**
     * Apply the collapsed state to the body element
     * @param {boolean} isCollapsed - Whether the sidebar should be collapsed
     */
    function applyCollapsedState(isCollapsed) {
        if (isCollapsed) {
            document.body.classList.add(COLLAPSED_CLASS);
        } else {
            document.body.classList.remove(COLLAPSED_CLASS);
        }
    }

    /**
     * Update the aria-expanded attribute on the toggle button
     * @param {HTMLElement} button - The toggle button element
     * @param {boolean} isExpanded - Whether the sidebar is expanded
     */
    function updateAriaExpanded(button, isExpanded) {
        button.setAttribute('aria-expanded', String(isExpanded));
    }

    /**
     * Toggle the sidebar collapsed state
     */
    function toggleSidebar() {
        var button = getToggleButton();
        if (!button) {
            console.log('[Storyville] Toggle button not found');
            return;
        }

        var isCurrentlyCollapsed = document.body.classList.contains(COLLAPSED_CLASS);
        var newCollapsedState = !isCurrentlyCollapsed;

        // Apply the new state
        applyCollapsedState(newCollapsedState);
        updateAriaExpanded(button, !newCollapsedState);
        saveState(newCollapsedState);

        console.log('[Storyville] Sidebar toggled:', newCollapsedState ? 'collapsed' : 'expanded');
    }

    /**
     * Initialize the sidebar toggle functionality
     */
    function init() {
        var button = getToggleButton();
        if (!button) {
            console.log('[Storyville] Toggle button not found, skipping sidebar initialization');
            return;
        }

        // Restore saved state
        var isCollapsed = getStoredState();
        applyCollapsedState(isCollapsed);
        updateAriaExpanded(button, !isCollapsed);

        console.log('[Storyville] Sidebar initialized, collapsed:', isCollapsed);

        // Add click event listener
        button.addEventListener('click', toggleSidebar);
    }

    // Initialize on page load
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', init);
    } else {
        init();
    }
})();
