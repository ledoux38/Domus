function debouncer_tag() {
    const tagInput = document.querySelector('input[name="tag"]');
    const tagSuggestionsDiv = document.getElementById('tag-suggestions');
    let tagDebounceTimeout = null;

    if (tagInput) {
        tagInput.addEventListener('input', function () {
            const value = tagInput.value.trim();
            tagSuggestionsDiv.innerHTML = '';
            if (value.length < 3) return;

            if (tagDebounceTimeout) clearTimeout(tagDebounceTimeout);

            tagDebounceTimeout = setTimeout(() => {
                fetch(`/tags/suggestions?q=${encodeURIComponent(value)}`)
                    .then(response => response.json())
                    .then(data => {
                        if (data.suggestions.length > 0) {
                            tagSuggestionsDiv.innerHTML =
                                '<ul style="border:1px solid #ccc; background:#fff; margin-top:2px; padding:5px;">' +
                                data.suggestions.map(s =>
                                    `<li style="cursor:pointer;" onclick="document.querySelector('input[name=tag]').value='${s.replace(/'/g,"\\'")}';document.getElementById('tag-suggestions').innerHTML=''">${s}</li>`
                                ).join('') +
                                '</ul>';
                        }
                    });
            }, 300);
        });
    }
};