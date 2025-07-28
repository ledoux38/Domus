let activeTagIds = [...document.querySelectorAll('.tag-btn.active')].map(btn => btn.dataset.tagId);

function refreshQuickSuggestions() {
    fetch(`/lists/${listId}/quick_suggestions?` + activeTagIds.map(id => `tag_ids=${id}`).join('&'))
        .then(res => res.json())
        .then(data => {
            const ul = document.querySelector('#suggestions-quick-add ul');
            ul.innerHTML = '';
            data.suggestions.forEach(s => {
                const presentItem = items.find(item => item.suggestion.text === s.text);
                let form = document.createElement('form');
                form.method = "POST";
                form.action = `/lists/${listId}/add_item`;
                form.style.display = "inline";
                form.innerHTML = `
                    <input type="hidden" name="text" value="${s.text}">
                    <button type="submit">
                        ${presentItem ? `+ (x${presentItem.quantity})` : `+`}
                    </button>
                `;
                let li = document.createElement('li');
                li.innerHTML = s.text + " ";
                li.appendChild(form);
                ul.appendChild(li);
            });

                // Ajout du comportement pour activer/désactiver les tags dynamiquement
    document.querySelectorAll('.tag-btn').forEach(btn => {
        btn.addEventListener('click', function() {
            this.classList.toggle('active');
            // Reconstruit la liste des tags actifs
            activeTagIds = [...document.querySelectorAll('.tag-btn.active')].map(b => b.dataset.tagId);
            refreshQuickSuggestions();
        });