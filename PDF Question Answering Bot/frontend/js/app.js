import {
    checkHealth,
} from "./api.js";

import {
    bindDocumentEvents,
    getSelectedDocumentId,
    loadDocuments,
} from "./documents.js";

import {
    bindChatEvents,
} from "./chat.js";

import {
    clearChat,
    elements,
    hideError,
    setSystemStatus,
    updateCharacterCounter,
} from "./ui.js";

function showApplicationError(
    message
) {
    const error =
        elements.questionError;

    error.textContent =
        message;

    error.classList.remove(
        "hidden"
    );

    window.setTimeout(
        hideError,
        6000
    );
}

async function initializeHealth() {
    try {
        await checkHealth();

        setSystemStatus(
            true,
            "System online"
        );
    } catch {
        setSystemStatus(
            false,
            "System offline"
        );
    }
}

async function initializeDocuments() {
    try {
        await loadDocuments();
    } catch (error) {
        showApplicationError(
            error.message
        );
    }
}

function initializeInput() {
    elements.questionInput.addEventListener(
        "input",
        updateCharacterCounter
    );

    updateCharacterCounter();
}

function initializeClearChat() {
    elements.clearChat.addEventListener(
        "click",
        clearChat
    );
}

function initialize() {
    initializeHealth();

    initializeDocuments();

    initializeInput();

    initializeClearChat();

    bindDocumentEvents({
        onError: showApplicationError,
    });

    bindChatEvents(
        getSelectedDocumentId,
        showApplicationError
    );
}

if (
    document.readyState ===
    "loading"
) {
    document.addEventListener(
        "DOMContentLoaded",
        initialize,
        {
            once: true,
        }
    );
} else {
    initialize();
}