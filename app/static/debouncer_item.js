function debouncer_item(listId) {
    let debounceTimeout = null;
    const input = document.getElementById('item-input');
    const suggestionsDiv = document.getElementById('suggestions');

    if (!input) return;

    input.addEventListener('input', function() {
        const value = input.value.trim();
        suggestionsDiv.innerHTML = '';
        if (value.length < 3) return;

        if (debounceTimeout) clearTimeout(debounceTimeout);

        debounceTimeout = setTimeout(() => {
            fetch(`/lists/${listId}/suggestions?q=${encodeURIComponent(value)}`)
                .then(response => response.json())
                .then(data => {
                    if (data.suggestions.length > 0) {
                        suggestionsDiv.innerHTML = '<ul style="border:1px solid #ccc; background:#fff; margin-top:2px; padding:5px;">' +
                            data.suggestions.map(s =>
                                `<li style="cursor:pointer;" onclick="document.getElementById('item-input').value='${s.replace(/'/g,"\\'")}';document.getElementById('suggestions').innerHTML=''">${s}</li>`
                            ).join('') +
                            '</ul>';
                    }
                });
        }, 300);
    });
}
