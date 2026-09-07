export function debounce(callback, delay = 300) {
    let timeoutId;

    return (...args) => {
        clearTimeout(timeoutId);

        timeoutId = setTimeout(() => {
            callback(...args);
        }, delay);
    };
}


export function countWords(text) {
    if (!text?.trim()) {
        return 0;
    }

    return text
        .trim()
        .split(/\s+/)
        .filter(Boolean)
        .length;
}


export function countCharacters(text) {
    return text?.length || 0;
}


export function formatNumber(value) {
    return Number(value || 0).toLocaleString();
}


export function downloadText(
    filename,
    content,
) {
    const blob = new Blob(
        [content],
        {
            type: "text/plain;charset=utf-8",
        },
    );

    const url = URL.createObjectURL(blob);

    const anchor = document.createElement("a");

    anchor.href = url;
    anchor.download = filename;

    document.body.appendChild(anchor);
    anchor.click();
    anchor.remove();

    URL.revokeObjectURL(url);
}


export function debounceInput(
    callback,
    delay = 250,
) {
    return debounce(callback, delay);
}