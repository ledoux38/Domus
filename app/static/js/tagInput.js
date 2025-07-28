// static/js/tagInput.js
function tagInput() {
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
                fetch(`/tags/suggestions?q=${encodeURIComponent(this.input)}`)
                    .then(response => response.json())
                    .then(data => {
                        this.suggestions = data.suggestions;
                    });
            }, 300);
        },

        select(suggestion) {
            this.input = suggestion;
            this.suggestions = [];
        }
    };
}

window.tagInput = tagInput;
