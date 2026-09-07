import {
    summarizeText,
} from "./api.js";

import {
    countWords,
    countCharacters,
    downloadText,
} from "./utils.js";

import {
    elements,
    setLoading,
    showError,
    clearError,
    showStatus,
    updateInputStats,
    updateSummaryStats,
    renderSummary,
    clearSummary,
    copySummary,
} from "./ui.js";


function getPayload() {
    return {
        text: elements.textInput.value.trim(),

        min_length: Number(
            elements.minLength.value || 30
        ),

        max_length: Number(
            elements.maxLength.value || 150
        ),

        style:
            elements.styleSelect.value ||
            "balanced",
    };
}


function updateInputStatistics() {
    const text =
        elements.textInput?.value || "";

    updateInputStats(
        countWords(text),
        countCharacters(text),
    );
}


async function handleSummarize() {
    clearError();
    showStatus("");

    const payload = getPayload();

    if (!payload.text) {
        showError(
            "Please enter text to summarize."
        );
        return;
    }

    if (payload.text.length < 50) {
        showError(
            "Please enter at least 50 characters."
        );
        return;
    }

    if (payload.max_length < payload.min_length) {
        showError(
            "Maximum length must be greater than or equal to minimum length."
        );
        return;
    }

    setLoading(true);

    try {
        const result =
            await summarizeText(payload);

        renderSummary(result.summary);

        updateSummaryStats(result);

        showStatus(
            "Summary generated successfully."
        );
    } catch (error) {
        showError(
            error.message ||
            "Unable to generate summary."
        );
    } finally {
        setLoading(false);
    }
}


function handleClear() {
    elements.textInput.value = "";

    updateInputStatistics();
    clearSummary();

    clearError();
    showStatus("Cleared.");
}


async function handleCopy() {
    clearError();

    try {
        const copied = await copySummary();

        if (!copied) {
            showError(
                "There is no summary to copy."
            );
        }
    } catch {
        showError(
            "Unable to copy the summary."
        );
    }
}


function handleDownload() {
    const summary =
        elements.summaryOutput?.textContent?.trim();

    if (!summary) {
        showError(
            "There is no summary to download."
        );
        return;
    }

    downloadText(
        "summary.txt",
        summary,
    );

    showStatus(
        "Summary downloaded."
    );
}


function handleKeyboardShortcut(event) {
    if (
        (event.ctrlKey || event.metaKey) &&
        event.key === "Enter"
    ) {
        event.preventDefault();

        handleSummarize();
    }
}


function initialize() {
    if (elements.textInput) {
        elements.textInput.addEventListener(
            "input",
            updateInputStatistics,
        );

        elements.textInput.addEventListener(
            "keydown",
            handleKeyboardShortcut,
        );
    }

    elements.summarizeButton?.addEventListener(
        "click",
        handleSummarize,
    );

    elements.clearButton?.addEventListener(
        "click",
        handleClear,
    );

    elements.copyButton?.addEventListener(
        "click",
        handleCopy,
    );

    elements.downloadButton?.addEventListener(
        "click",
        handleDownload,
    );

    updateInputStatistics();
    clearSummary();
}


document.addEventListener(
    "DOMContentLoaded",
    initialize,
);