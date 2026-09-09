import {
    deleteDocument,
    getDocuments,
    uploadDocument,
} from "./api.js";

import {
    elements,
    renderDocuments,
    resetUploadProgress,
    setActiveDocument,
} from "./ui.js";

import {
    formatFileSize,
    isPdfFile,
} from "./utils.js";

let documents = [];
let selectedDocumentId = null;

export function getSelectedDocumentId() {
    return selectedDocumentId;
}

export function getDocumentsState() {
    return [...documents];
}

export async function loadDocuments() {
    const response =
        await getDocuments();

    documents =
        response.documents || [];

    renderDocuments(
        documents,
        selectedDocumentId
    );

    const selected =
        documents.find(
            (document) =>
                document.id ===
                selectedDocumentId
        );

    if (selected) {
        setActiveDocument(selected);
    } else {
        setActiveDocument(null);
    }

    return documents;
}

export function selectDocument(
    documentId
) {
    if (
        selectedDocumentId ===
        documentId
    ) {
        selectedDocumentId = null;
        setActiveDocument(null);
    } else {
        selectedDocumentId =
            documentId;

        const document =
            documents.find(
                (item) =>
                    item.id ===
                    documentId
            );

        setActiveDocument(
            document || null
        );
    }

    renderDocuments(
        documents,
        selectedDocumentId
    );
}

export async function handleUpload(
    file
) {
    if (!file) {
        return;
    }

    if (!isPdfFile(file)) {
        throw new Error(
            "Please select a valid PDF file."
        );
    }

    const maxSize =
        (
            window.APP_CONFIG
                ?.MAX_FILE_SIZE_MB ||
            25
        ) *
        1024 *
        1024;

    if (file.size > maxSize) {
        throw new Error(
            `The PDF must be smaller than ${
                window.APP_CONFIG
                    ?.MAX_FILE_SIZE_MB || 25
            } MB.`
        );
    }

    elements.uploadProgressContainer.classList.remove(
        "hidden"
    );

    elements.uploadStatus.textContent =
        `Uploading ${file.name}...`;

    try {
        const response =
            await uploadDocument(
                file,
                (percentage) => {
                    elements.uploadProgress.style.width =
                        `${percentage}%`;

                    elements.uploadPercentage.textContent =
                        `${percentage}%`;

                    if (
                        percentage >= 100
                    ) {
                        elements.uploadStatus.textContent =
                            "Processing PDF...";
                    }
                }
            );

        elements.uploadProgress.style.width =
            "100%";

        elements.uploadPercentage.textContent =
            "100%";

        elements.uploadStatus.textContent =
            `Ready: ${formatFileSize(
                response.size_bytes
            )}`;

        await loadDocuments();

        selectedDocumentId =
            response.id;

        renderDocuments(
            documents,
            selectedDocumentId
        );

        setActiveDocument(
            response
        );

        return response;
    } finally {
        setTimeout(
            resetUploadProgress,
            1800
        );
    }
}

export async function removeDocument(
    documentId
) {
    await deleteDocument(
        documentId
    );

    if (
        selectedDocumentId ===
        documentId
    ) {
        selectedDocumentId = null;
        setActiveDocument(null);
    }

    await loadDocuments();
}

export function bindDocumentEvents({
    onError,
}) {
    elements.pdfInput.addEventListener(
        "change",
        async (event) => {
            const file =
                event.target.files?.[0];

            try {
                await handleUpload(file);
            } catch (error) {
                onError(
                    error.message
                );
            } finally {
                event.target.value = "";
            }
        }
    );

    elements.refreshDocuments.addEventListener(
        "click",
        async () => {
            try {
                await loadDocuments();
            } catch (error) {
                onError(
                    error.message
                );
            }
        }
    );

    elements.documentList.addEventListener(
        "click",
        async (event) => {
            const action =
                event.target.closest(
                    "[data-action]"
                );

            if (!action) {
                return;
            }

            const documentId =
                action.dataset.documentId;

            if (!documentId) {
                return;
            }

            if (
                action.dataset.action ===
                "select"
            ) {
                selectDocument(
                    documentId
                );

                return;
            }

            if (
                action.dataset.action ===
                "delete"
            ) {
                const document =
                    documents.find(
                        (item) =>
                            item.id ===
                            documentId
                    );

                const confirmed =
                    window.confirm(
                        `Delete "${
                            document?.filename ||
                            "this document"
                        }"?`
                    );

                if (!confirmed) {
                    return;
                }

                try {
                    await removeDocument(
                        documentId
                    );
                } catch (error) {
                    onError(
                        error.message
                    );
                }
            }
        }
    );

    const dropZone =
        elements.dropZone;

    dropZone.addEventListener(
        "dragover",
        (event) => {
            event.preventDefault();

            dropZone.classList.add(
                "drag-active"
            );
        }
    );

    dropZone.addEventListener(
        "dragleave",
        () => {
            dropZone.classList.remove(
                "drag-active"
            );
        }
    );

    dropZone.addEventListener(
        "drop",
        async (event) => {
            event.preventDefault();

            dropZone.classList.remove(
                "drag-active"
            );

            const file =
                event.dataTransfer
                    ?.files?.[0];

            try {
                await handleUpload(file);
            } catch (error) {
                onError(
                    error.message
                );
            }
        }
    );
}