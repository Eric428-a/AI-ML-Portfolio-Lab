const API_BASE = "/api/v1";

const App = {
    state: {
        documents: [],
        selectedDocumentIds: [],
        loading: false
    },

    async request(endpoint, options = {}) {
        const response = await fetch(
            `${API_BASE}${endpoint}`,
            options
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
                "The server returned an error.";

            throw new Error(message);
        }

        return data;
    },

    setStatus(online, text) {
        const dot = document.querySelector(
            ".status-dot"
        );

        const status = document.getElementById(
            "system-status"
        );

        if (!dot || !status) {
            return;
        }

        dot.classList.toggle(
            "online",
            Boolean(online)
        );

        dot.classList.toggle(
            "offline",
            online === false
        );

        status.textContent = text;
    },

    escapeHtml(value) {
        const element = document.createElement("div");
        element.textContent = value ?? "";
        return element.innerHTML;
    },

    formatFileType(type) {
        return String(type || "")
            .toUpperCase()
            .replace("DOCX", "DOCX");
    },

    formatDate(value) {
        if (!value) {
            return "";
        }

        const date = new Date(value);

        if (Number.isNaN(date.getTime())) {
            return "";
        }

        return date.toLocaleDateString();
    },

    showMessage(message, type = "success") {
        const element = document.getElementById(
            "upload-message"
        );

        if (!element) {
            return;
        }

        element.textContent = message;
        element.className = `message ${type}`;

        window.clearTimeout(
            this._messageTimeout
        );

        this._messageTimeout = window.setTimeout(
            () => {
                element.className = "message hidden";
                element.textContent = "";
            },
            5000
        );
    }
};


document.addEventListener(
    "DOMContentLoaded",
    async () => {
        try {
            await App.request("/health");

            App.setStatus(
                true,
                "System online"
            );
        } catch {
            App.setStatus(
                false,
                "System unavailable"
            );
        }

        if (
            typeof loadDocuments === "function"
        ) {
            await loadDocuments();
        }
    }
);