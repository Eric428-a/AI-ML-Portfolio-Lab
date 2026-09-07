const API_BASE_URL =
    window.APP_CONFIG?.API_BASE_URL ||
    "http://localhost:8000/api/v1";

async function request(endpoint, options = {}) {
    const response = await fetch(
        `${API_BASE_URL}${endpoint}`,
        {
            headers: {
                "Content-Type": "application/json",
                ...(options.headers || {}),
            },
            ...options,
        }
    );

    let data = null;

    try {
        data = await response.json();
    } catch {
        data = null;
    }

    if (!response.ok) {
        const message =
            data?.detail ||
            data?.message ||
            `Request failed with status ${response.status}`;

        throw new Error(message);
    }

    return data;
}

export async function summarizeText(payload) {
    return request("/summarizer/summarize", {
        method: "POST",
        body: JSON.stringify(payload),
    });
}

export async function getHealth() {
    return request("/summarizer/health", {
        method: "GET",
    });
}

export { API_BASE_URL };