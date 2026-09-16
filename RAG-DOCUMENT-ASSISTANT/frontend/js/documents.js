async function loadDocuments() {
    const list = document.getElementById(
        "documents-list"
    );

    try {
        const data = await App.request(
            "/documents"
        );

        App.state.documents =
            data.documents || [];

        renderDocuments();

    } catch (error) {
        list.innerHTML = `
            <div class="empty-state">
                <h3>Unable to load documents</h3>
                <p>${App.escapeHtml(
                    error.message
                )}</p>
            </div>
        `;
    }
}


function renderDocuments() {
    const list = document.getElementById(
        "documents-list"
    );

    const count = document.getElementById(
        "document-count"
    );

    if (!list || !count) {
        return;
    }

    const documents =
        App.state.documents;

    count.textContent =
        `${documents.length} ${
            documents.length === 1
                ? "document"
                : "documents"
        }`;

    if (!documents.length) {
        list.innerHTML = `
            <div class="empty-state">
                <div class="empty-icon">+</div>
                <h3>No documents yet</h3>
                <p>
                    Upload a PDF, DOCX, or TXT file
                    to start asking questions.
                </p>
            </div>
        `;

        updateSelectedDocumentsLabel();
        return;
    }

    list.innerHTML = documents
        .map((document) => {
            const selected =
                App.state.selectedDocumentIds
                    .includes(document.id);

            const extension =
                App.formatFileType(
                    document.file_type
                );

            return `
                <div
                    class="document-card"
                    data-document-id="${document.id}"
                    title="Click to ${
                        selected
                            ? "deselect"
                            : "select"
                    } this document"
                    style="${
                        selected
                            ? "background: var(--surface-soft);"
                            : ""
                    }"
                >
                    <div class="document-icon">
                        ${App.escapeHtml(extension)}
                    </div>

                    <div class="document-info">
                        <div class="document-name">
                            ${App.escapeHtml(
                                document.filename
                            )}
                        </div>

                        <div class="document-meta">
                            ${
                                document.chunk_count
                            } chunks
                            ${
                                document.created_at
                                    ? ` · ${App.formatDate(
                                        document.created_at
                                    )}`
                                    : ""
                            }
                        </div>

                        <div class="document-status ${
                            document.status
                        }">
                            ${App.escapeHtml(
                                document.status
                            )}
                        </div>
                    </div>
                </div>
            `;
        })
        .join("");

    list
        .querySelectorAll(".document-card")
        .forEach((card) => {
            card.addEventListener(
                "click",
                () => {
                    const id = Number(
                        card.dataset.documentId
                    );

                    toggleDocumentSelection(id);
                }
            );
        });

    updateSelectedDocumentsLabel();
}


function toggleDocumentSelection(id) {
    const selected =
        App.state.selectedDocumentIds;

    const index = selected.indexOf(id);

    if (index >= 0) {
        selected.splice(index, 1);
    } else {
        selected.push(id);
    }

    renderDocuments();
}


function updateSelectedDocumentsLabel() {
    const label = document.getElementById(
        "selected-documents"
    );

    if (!label) {
        return;
    }

    const selected =
        App.state.selectedDocumentIds;

    if (!selected.length) {
        label.textContent =
            "All documents";
        return;
    }

    label.textContent =
        `${selected.length} ${
            selected.length === 1
                ? "document"
                : "documents"
        } selected`;
}


async function uploadDocument(file) {
    if (!file) {
        return;
    }

    const formData = new FormData();

    formData.append(
        "file",
        file
    );

    try {
        App.showMessage(
            "Uploading document...",
            "success"
        );

        const response =
            await App.request(
                "/documents/upload",
                {
                    method: "POST",
                    body: formData
                }
            );

        App.showMessage(
            `${response.filename} uploaded successfully.`,
            "success"
        );

        await loadDocuments();

    } catch (error) {
        App.showMessage(
            error.message,
            "error"
        );
    }
}


document.addEventListener(
    "DOMContentLoaded",
    () => {
        const input =
            document.getElementById(
                "document-input"
            );

        if (!input) {
            return;
        }

        input.addEventListener(
            "change",
            async (event) => {
                const file =
                    event.target.files?.[0];

                await uploadDocument(file);

                event.target.value = "";
            }
        );
    }
);