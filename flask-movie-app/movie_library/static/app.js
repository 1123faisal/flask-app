const root = document.documentElement;
const toggle = document.getElementById("theme-toggle");
const storedTheme = window.localStorage.getItem("watchlist-theme");

if (storedTheme === "light" || storedTheme === "dark") {
    root.setAttribute("data-theme", storedTheme);
}

if (toggle) {
    const syncLabel = () => {
        const mode = root.getAttribute("data-theme") === "light" ? "Dark mode" : "Light mode";
        toggle.textContent = mode;
    };

    syncLabel();

    toggle.addEventListener("click", () => {
        const nextTheme = root.getAttribute("data-theme") === "light" ? "dark" : "light";
        root.setAttribute("data-theme", nextTheme);
        window.localStorage.setItem("watchlist-theme", nextTheme);
        syncLabel();
    });
}