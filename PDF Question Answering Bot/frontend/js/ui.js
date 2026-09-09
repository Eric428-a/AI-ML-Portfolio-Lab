import {
    escapeHtml,
    formatDate,
    formatFileSize,
    scrollToBottom,
    truncateText,
} from "./utils.js";

export const elements = {
    systemStatus: document.getElementById(
        "systemStatus"
    ),

    pdfInput: document.getElementById(
        "pdfInput"
    ),

    dropZone: document.getElementById(
        "dropZone"
    ),

    documentCount: document.getElementById(
        "documentCount"
    ),

    documentList: document.getElementById(
        "documentList"
    ),

    refreshDocuments: document.getElementById(
        "refreshDocuments"
    ),

    uploadProgressContainer:
        document.getElementById(
            "uploadProgressContainer"
        ),

    uploadStatus: document.getElementById(
        "uploadStatus"
    ),

    uploadPercentage:
        document.getElementById(
            "uploadPercentage"
        ),

    uploadProgress:
        document.getElementById(
            "uploadProgress"
        ),

    activeDocumentTitle:
        document.getElementById(
            "activeDocumentTitle"
        ),

    chatMessages:
        document.getElementById(
            "chatMessages"
        ),

    clearChat:
        document.getElementById(
            "clearChat"
        ),

    questionForm:
        document.getElementById(
            "questionForm"
        ),

    questionInput:
        document.getElementById(
            "questionInput"
        ),

    questionError:
        document.getElementById(
            "questionError"
        ),

    askButton:
        document.getElementById(
            "askButton"
        ),

    askButtonText:
        document.getElementById(
            "askButtonText"
        ),

    askButtonLoader:
        document.getElementById(
            "askButtonLoader"
        ),

    characterCounter:
        document.getElementById(
            "characterCounter"
        ),
};

export function setSystemStatus(
    online,
    message = null
) {
    const element =
        elements.systemStatus;

    element.classList.remove(
        "status-online",
        "status-offline"
    );

    element.classList.add(
        online
            ? "status-online"
            : "status-offline"
    );

    element.textContent =
        message ||
        (online
            ? "System online"
            : "System offline");
}

export function setLoading(
    loading
) {
    elements.askButton.disabled = loading;

    elements.askButtonLoader.classList.toggle(
        "hidden",
        !loading
    );

    elements.askButtonText.textContent =
        loading ? "Thinking..." : "Ask";
}

export function showError(
    message
) {
    elements.questionError.textContent =
        message;

    elements.questionError.classList.remove(
        "hidden"
    );
}

export function hideError() {
    elements.questionError.textContent = "";

    elements.questionError.classList.add(
        "hidden"
    );
}

export function updateCharacterCounter() {
    const length =
        elements.questionInput.value.length;

    elements.characterCounter.textContent =
        `${length} / 2000`;
}

export function renderDocuments(
    documents,
    selectedDocumentId = null
) {
    elements.documentCount.textContent =
        String(documents.length);

    if (!documents.length) {
        elements.documentList.innerHTML = `
            <div class="empty-state">
                <div class="empty-icon">▱</div>
                <p>No documents uploaded yet.</p>
            </div>
        `;

        return;
    }

    elements.documentList.innerHTML =
        documents.map(
            (document) => {
                const selected =
                    document.id ===
                    selectedDocumentId;

                const statusClass =
                    document.status === "ready"
                        ? "document-ready"
                        : document.status === "failed"
                            ? "document-failed"
                            : "document-processing";

                return `
                    <article
                        class="document-card ${
                            selected
                                ? "document-selected"
                                : ""
                        }"
                        data-document-id="${escapeHtml(
                            document.id
                        )}"
                    >
                        <button
                            class="document-select"
                            type="button"
                            data-action="select"
                            data-document-id="${escapeHtml(
                                document.id
                            )}"
                        >
                            <span class="pdf-icon">
                                PDF
                            </span>

                            <span class="document-info">
                                <strong
                                    title="${escapeHtml(
                                        document.filename
                                    )}"
                                >
                                    ${escapeHtml(
                                        truncateText(
                                            document.filename,
                                            32
                                        )
                                    )}
                                </strong>

                                <span>
                                    ${formatFileSize(
                                        document.size_bytes
                                    )}
                                    ·
                                    ${
                                        document.page_count
                                    } pages
                                </span>

                                <span
                                    class="document-status ${statusClass}"
                                >
                                    ${escapeHtml(
                                        document.status
                                    )}
                                </span>
                            </span>
                        </button>

                        <button
                            class="delete-document"
                            type="button"
                            title="Delete document"
                            data-action="delete"
                            data-document-id="${escapeHtml(
                                document.id
                            )}"
                        >
                            ×
                        </button>
                    </article>
                `;
            }
        ).join("");
}

export function setActiveDocument(
    document
) {
    elements.activeDocumentTitle.textContent =
        document
            ? document.filename
            : "All documents";
}

export function addUserMessage(
    question
) {
    const message =
        document.createElement("div");

    message.className =
        "chat-message user-message";

    message.innerHTML = `
        <div class="message-avatar">
            You
        </div>

        <div class="message-content">
            <div class="message-role">
                You
            </div>

            <div class="message-text">
                ${escapeHtml(question)}
            </div>
        </div>
    `;

    elements.chatMessages.appendChild(
        message
    );

    scrollToBottom(
        elements.chatMessages
    );
}

export function addAssistantMessage(
    response
) {
    const message =
        document.createElement("div");

    message.className =
        "chat-message assistant-message";

    message.innerHTML = `
        <div class="message-avatar assistant-avatar">
            AI
        </div>

        <div class="message-content">
            <div class="message-role">
                Assistant
            </div>

            <div class="message-text">
                ${escapeHtml(
                    response.answer
                ).replace(/\n/g, "<br>")}
            </div>

            ${renderSources(
                response.sources || []
            )}
        </div>
    `;

    elements.chatMessages.appendChild(
        message
    );

    scrollToBottom(
        elements.chatMessages
    );
}

function renderSources(
    sources
) {
    if (!sources.length) {
        return "";
    }

    return `
        <div class="sources-section">
            <div class="sources-title">
                Sources
            </div>

            <div class="sources-list">
                ${sources.map(
                    (source, index) => `
                        <div class="source-card">
                            <div class="source-number">
                                ${index + 1}
                            </div>

                            <div class="source-content">
                                <strong>
                                    ${escapeHtml(
                                        source.filename
                                    )}
                                </strong>

                                <span>
                                    Page ${
                                        source.page_number
                                    }
                                    · relevance ${
                                        Math.round(
                                            source.relevance_score *
                                            100
                                        )
                                    }%
                                </span>

                                <p>
                                    ${escapeHtml(
                                        truncateText(
                                            source.excerpt,
                                            300
                                        )
                                    )}
                                </p>
                            </div>
                        </div>
                    `
                ).join("")}
            </div>
        </div>
    `;
}

export function addLoadingMessage() {
    const message =
        document.createElement("div");

    message.id =
        "temporaryAssistantMessage";

    message.className =
        "chat-message assistant-message";

    message.innerHTML = `
        <div class="message-avatar assistant-avatar">
            AI
        </div>

        <div class="message-content">
            <div class="message-role">
                Assistant
            </div>

            <div class="typing-indicator">
                <span></span>
                <span></span>
                <span></span>
            </div>
        </div>
    `;

    elements.chatMessages.appendChild(
        message
    );

    scrollToBottom(
        elements.chatMessages
    );
}

export function removeLoadingMessage() {
    document
        .getElementById(
            "temporaryAssistantMessage"
        )
        ?.remove();
}

export function clearChat() {
    elements.chatMessages.innerHTML = `
        <div class="welcome-message">
            <div class="welcome-icon">
                ✦
            </div>

            <h3>
                Your PDF assistant is ready.
            </h3>

            <p>
                Ask another question about your
                indexed documents.
            </p>
        </div>
    `;
}

export function resetUploadProgress() {
    elements.uploadProgressContainer.classList.add(
        "hidden"
    );

    elements.uploadProgress.style.width =
        "0%";

    elements.uploadPercentage.textContent =
        "0%";

    elements.uploadStatus.textContent =
        "Processing...";
}