import { askQuestion } from "./api.js";

import {
    addAssistantMessage,
    addLoadingMessage,
    addUserMessage,
    elements,
    hideError,
    removeLoadingMessage,
    setLoading,
} from "./ui.js";

export function bindChatEvents(
    getSelectedDocumentId,
    onError
) {
    elements.questionForm.addEventListener(
        "submit",
        async (event) => {
            event.preventDefault();

            await submitQuestion(
                getSelectedDocumentId,
                onError
            );
        }
    );

    elements.questionInput.addEventListener(
        "keydown",
        async (event) => {
            if (
                (event.ctrlKey ||
                    event.metaKey) &&
                event.key === "Enter"
            ) {
                event.preventDefault();

                await submitQuestion(
                    getSelectedDocumentId,
                    onError
                );
            }
        }
    );

    document.addEventListener(
        "click",
        (event) => {
            const suggestion =
                event.target.closest(
                    "[data-question]"
                );

            if (!suggestion) {
                return;
            }

            elements.questionInput.value =
                suggestion.dataset.question ||
                "";

            elements.questionInput.focus();

            elements.questionInput.dispatchEvent(
                new Event("input")
            );
        }
    );
}

async function submitQuestion(
    getSelectedDocumentId,
    onError
) {
    const question =
        elements.questionInput.value.trim();

    hideError();

    if (!question) {
        onError(
            "Please enter a question."
        );

        return;
    }

    if (question.length < 2) {
        onError(
            "Your question is too short."
        );

        return;
    }

    const documentId =
        getSelectedDocumentId();

    addUserMessage(question);

    elements.questionInput.value = "";

    elements.questionInput.dispatchEvent(
        new Event("input")
    );

    setLoading(true);
    addLoadingMessage();

    try {
        const response =
            await askQuestion({
                question,
                documentId,
                topK: 5,
            });

        removeLoadingMessage();

        addAssistantMessage(
            response
        );
    } catch (error) {
        removeLoadingMessage();

        onError(
            error.message ||
            "Unable to answer the question."
        );
    } finally {
        setLoading(false);
        elements.questionInput.focus();
    }
}