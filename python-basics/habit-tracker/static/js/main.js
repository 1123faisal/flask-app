document.addEventListener("DOMContentLoaded", () => {
	document.body.classList.add("page-ready");

	const textarea = document.querySelector("textarea[name='habit']");
	if (textarea) {
		const resize = () => {
			textarea.style.height = "auto";
			textarea.style.height = `${Math.max(textarea.scrollHeight, 120)}px`;
		};

		textarea.addEventListener("input", resize);
		resize();
	}
});
