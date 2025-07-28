function itemInput(listId) {
    return {
        input: '',
        suggestions: [],
        timeout: null,

        debounceFetch() {
            clearTimeout(this.timeout);
            if (this.input.length < 3) {
                this.suggestions = [];
                return;
            }
            this.timeout = setTimeout(() => {
                fetch(`/lists/${listId}/suggestions?q=${encodeURIComponent(this.input)}`)
                    .then(res => res.json())
                    .then(data => this.suggestions = data.suggestions);
            }, 300);
        },

        selectSuggestion(text) {
            this.input = text;
            this.suggestions = [];
        }
    };
}
