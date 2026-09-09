const API_BASE_URL = window.APP_CONFIG?.API_BASE_URL || "/api/v1";

async function parseResponse(response) {
    const contentType = response.headers.get("content-type") || "";

    if (contentType.includes("application/json")) {
        return response.json();
    }

    return {
        detail: await response.text(),
    };
}

async function request(url, options = {}) {
    let response;

    try {
        response = await fetch(url, {
            ...options,
            headers: {
                Accept: "application/json",
                ...(options.headers || {}),
            },
        });
    } catch (error) {
        throw new Error(
            "Unable to connect to the server."
        );
    }

    const payload = await parseResponse(response);

    if (!response.ok) {
        const message =
            payload?.detail ||
            payload?.message ||
            "The request failed.";

        throw new Error(message);
    }

    return payload;
}

export async function checkHealth() {
    return request(
        `${API_BASE_URL}/health`
    );
}

export async function getDocuments() {
    return request(
        `${API_BASE_URL}/documents`
    );
}

export async function getDocument(documentId) {
    return request(
        `${API_BASE_URL}/documents/${encodeURIComponent(documentId)}`
    );
}

export async function uploadDocument(
    file,
    onProgress = null
) {
    const formData = new FormData();
    formData.append("file", file);

    if (typeof onProgress !== "function") {
        return request(
            `${API_BASE_URL}/documents/upload`,
            {
                method: "POST",
                body: formData,
            }
        );
    }

    return new Promise((resolve, reject) => {
        const xhr = new XMLHttpRequest();

        xhr.open(
            "POST",
            `${API_BASE_URL}/documents/upload`
        );

        xhr.setRequestHeader(
            "Accept",
            "application/json"
        );

        xhr.upload.addEventListener(
            "progress",
            (event) => {
                if (!event.lengthComputable) {
                    return;
                }

                const percentage =
                    Math.round(
                        (event.loaded / event.total) * 100
                    );

                onProgress(percentage);
            }
        );

        xhr.addEventListener(
            "load",
            () => {
                let payload;

                try {
                    payload = JSON.parse(
                        xhr.responseText
                    );
                } catch {
                    payload = {
                        detail: xhr.responseText,
                    };
                }

                if (
                    xhr.status >= 200 &&
                    xhr.status < 300
                ) {
                    resolve(payload);
                    return;
                }

                reject(
                    new Error(
                        payload?.detail ||
                        "PDF upload failed."
                    )
                );
            }
        );

        xhr.addEventListener(
            "error",
            () => {
                reject(
                    new Error(
                        "Unable to upload the PDF."
                    )
                );
            }
        );

        xhr.addEventListener(
            "abort",
            () => {
                reject(
                    new Error(
                        "PDF upload was cancelled."
                    )
                );
            }
        );

        xhr.send(formData);
    });
}

export async function deleteDocument(
    documentId
) {
    return request(
        `${API_BASE_URL}/documents/${encodeURIComponent(documentId)}`,
        {
            method: "DELETE",
        }
    );
}

export async function askQuestion({
    question,
    documentId = null,
    topK = 5,
}) {
    return request(
        `${API_BASE_URL}/questions/ask`,
        {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({
                question,
                document_id: documentId,
                top_k: topK,
            }),
        }
    );
}