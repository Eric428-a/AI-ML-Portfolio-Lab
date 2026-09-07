export const elements = {
    textInput: document.querySelector("#text-input"),
    summaryOutput: document.querySelector("#summary-output"),

    summarizeButton: document.querySelector("#summarize-button"),
    copyButton: document.querySelector("#copy-button"),
    downloadButton: document.querySelector("#download-button"),
    clearButton: document.querySelector("#clear-button"),

    styleSelect: document.querySelector("#style-select"),
    minLength: document.querySelector("#min-length"),
    maxLength: document.querySelector("#max-length"),

    inputWords: document.querySelector("#input-words"),
    inputCharacters: document.querySelector("#input-characters"),

    summaryWords: document.querySelector("#summary-words"),
    summaryCharacters: document.querySelector("#summary-characters"),

    compressionRatio: document.querySelector("#compression-ratio"),

    loadingIndicator: document.querySelector("#loading-indicator"),
    errorMessage: document.querySelector("#error-message"),
    statusMessage: document.querySelector("#status-message"),
};


export function setLoading(isLoading) {
    if (!elements.summarizeButton) {
        return;
    }

    elements.summarizeButton.disabled = isLoading;

    if (elements.loadingIndicator) {
        elements.loadingIndicator.hidden = !isLoading;
    }

    elements.summarizeButton.textContent =
        isLoading
            ? "Summarizing..."
            : "Generate Summary";
}


export function showError(message) {
    if (!elements.errorMessage) {
        return;
    }

    elements.errorMessage.textContent = message;
    elements.errorMessage.hidden = false;
}


export function clearError() {
    if (!elements.errorMessage) {
        return;
    }

    elements.errorMessage.textContent = "";
    elements.errorMessage.hidden = true;
}


export function showStatus(message) {
    if (!elements.statusMessage) {
        return;
    }

    elements.statusMessage.textContent = message;
    elements.statusMessage.hidden = !message;
}


export function updateInputStats(
    words,
    characters,
) {
    if (elements.inputWords) {
        elements.inputWords.textContent =
            words.toLocaleString();
    }

    if (elements.inputCharacters) {
        elements.inputCharacters.textContent =
            characters.toLocaleString();
    }
}


export function updateSummaryStats(data) {
    if (elements.summaryWords) {
        elements.summaryWords.textContent =
            data.summary_word_count.toLocaleString();
    }

    if (elements.summaryCharacters) {
        elements.summaryCharacters.textContent =
            data.summary_character_count.toLocaleString();
    }

    if (elements.compressionRatio) {
        elements.compressionRatio.textContent =
            `${Math.round(
                data.compression_ratio * 100
            )}%`;
    }
}


export function renderSummary(summary) {
    if (!elements.summaryOutput) {
        return;
    }

    elements.summaryOutput.textContent = summary;
}


export function clearSummary() {
    renderSummary("");

    updateSummaryStats({
        summary_word_count: 0,
        summary_character_count: 0,
        compression_ratio: 0,
    });
}


export async function copySummary() {
    const summary =
        elements.summaryOutput?.textContent?.trim();

    if (!summary) {
        return false;
    }

    await navigator.clipboard.writeText(summary);

    showStatus("Summary copied to clipboard.");

    return true;
}