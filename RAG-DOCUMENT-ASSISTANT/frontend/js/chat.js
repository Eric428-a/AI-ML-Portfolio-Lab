function appendUserMessage(question) {
    const container =
        document.getElementById(
            "chat-messages"
        );

    removeWelcomeMessage();

    const row =
        document.createElement("div");

    row.className =
        "message-row user";

    row.innerHTML = `
        <div class="message-bubble">
            ${App.escapeHtml(question)}
        </div>
    `;

    container.appendChild(row);

    scrollChatToBottom();
}


function appendAssistantMessage(
    answer,
    sources = []
) {
    const container =
        document.getElementById(
            "chat-messages"
        );

    const row =
        document.createElement("div");

    row.className =
        "message-row assistant";

    const sourceMarkup =
        sources.length
            ? `
                <div class="sources">
                    <div class="sources-title">
                        Sources
                    </div>

                    ${sources
                        .map(
                            (source) => `
                                <div class="source-item">
                                    <div class="source-name">
                                        ${App.escapeHtml(
                                            source.filename
                                        )}
                                    </div>

                                    <div class="source-page">
                                        Chunk ${
                                            source.chunk_index
                                        }${
                                            source.page_number
                                                ? ` · Page ${source.page_number}`
                                                : ""
                                        }
                                    </div>
                                </div>
                            `
                        )
                        .join("")}
                </div>
            `
            : "";

    row.innerHTML = `
        <div>
            <div class="message-bubble">
                ${App.escapeHtml(answer)}
            </div>

            ${sourceMarkup}
        </div>
    `;

    container.appendChild(row);

    scrollChatToBottom();
}


function appendTypingMessage() {
    const container =
        document.getElementById(
            "chat-messages"
        );

    const row =
        document.createElement("div");

    row.id = "typing-message";
    row.className =
        "message-row assistant";

    row.innerHTML = `
        <div class="message-bubble typing">
            Searching documents...
        </div>
    `;

    container.appendChild(row);

    scrollChatToBottom();
}


function removeTypingMessage() {
    document
        .getElementById("typing-message")
        ?.remove();
}


function removeWelcomeMessage() {
    document
        .querySelector(".welcome-message")
        ?.remove();
}


function scrollChatToBottom() {
    const container =
        document.getElementById(
            "chat-messages"
        );

    if (!container) {
        return;
    }

    container.scrollTop =
        container.scrollHeight;
}


async function sendQuestion() {
    const input =
        document.getElementById(
            "question-input"
        );

    const button =
        document.getElementById(
            "send-question"
        );

    const question =
        input.value.trim();

    if (!question) {
        return;
    }

    if (App.state.loading) {
        return;
    }

    App.state.loading = true;

    button.disabled = true;

    appendUserMessage(question);
    appendTypingMessage();

    input.value = "";

    try {
        const response =
            await App.request(
                "/chat",
                {
                    method: "POST",
                    headers: {
                        "Content-Type":
                            "application/json"
                    },
                    body: JSON.stringify({
                        question,
                        document_ids:
                            App.state
                                .selectedDocumentIds,
                        top_k: 5
                    })
                }
            );

        removeTypingMessage();

        appendAssistantMessage(
            response.answer,
            response.sources || []
        );

    } catch (error) {
        removeTypingMessage();

        appendAssistantMessage(
            `Unable to answer the question: ${
                error.message
            }`
        );

    } finally {
        App.state.loading = false;
        button.disabled = false;
        input.focus();
    }
}


function clearChat() {
    const container =
        document.getElementById(
            "chat-messages"
        );

    container.innerHTML = `
        <div class="welcome-message">
            <h3>What would you like to know?</h3>
            <p>
                Upload documents and ask questions
                about their contents.
            </p>
        </div>
    `;
}


document.addEventListener(
    "DOMContentLoaded",
    () => {
        const button =
            document.getElementById(
                "send-question"
            );

        const input =
            document.getElementById(
                "question-input"
            );

        const clearButton =
            document.getElementById(
                "clear-chat"
            );

        button?.addEventListener(
            "click",
            sendQuestion
        );

        clearButton?.addEventListener(
            "click",
            clearChat
        );

        input?.addEventListener(
            "keydown",
            (event) => {
                if (
                    event.key === "Enter" &&
                    !event.shiftKey
                ) {
                    event.preventDefault();
                    sendQuestion();
                }
            }
        );
    }
);