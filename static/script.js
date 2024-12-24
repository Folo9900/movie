let page = 1;
let loading = false;
let currentFilters = {};

// Загрузка фильмов
async function loadMovies(reset = false) {
    if (loading) return;
    if (reset) {
        page = 1;
        document.getElementById('movieFeed').innerHTML = '';
    }
    
    loading = true;
    
    const queryParams = new URLSearchParams({
        page: page,
        ...currentFilters
    });
    
    try {
        const response = await fetch(`/api/movies?${queryParams}`);
        const data = await response.json();
        
        renderMovies(data.movies);
        
        if (data.has_next) {
            page++;
        }
    } catch (error) {
        console.error('Error loading movies:', error);
    } finally {
        loading = false;
    }
}

// Рендеринг карточек фильмов
function renderMovies(movies) {
    const feed = document.getElementById('movieFeed');
    
    movies.forEach(movie => {
        const card = document.createElement('div');
        card.className = 'movie-card';
        card.innerHTML = `
            <img src="${movie.poster_url}" alt="${movie.title}">
            <div class="movie-info">
                <h3>${movie.title} (${movie.year})</h3>
                <p>${movie.description}</p>
                <div class="ratings">
                    <span class="rating-badge imdb">IMDb: ${movie.imdb_rating}</span>
                    <span class="rating-badge kinopoisk">КП: ${movie.kinopoisk_rating}</span>
                </div>
                <div class="mt-2">
                    <small>Жанр: ${movie.genre}</small><br>
                    <small>Страна: ${movie.country}</small>
                </div>
            </div>
        `;
        feed.appendChild(card);
    });
}

// Бесконечная прокрутка
window.addEventListener('scroll', () => {
    if (window.innerHeight + window.scrollY >= document.body.offsetHeight - 1000) {
        loadMovies();
    }
});

// Обработка фильтров
document.getElementById('applyFilters').addEventListener('click', () => {
    const form = document.getElementById('filterForm');
    const formData = new FormData(form);
    
    currentFilters = {};
    for (let [key, value] of formData.entries()) {
        if (value) {
            currentFilters[key] = value;
        }
    }
    
    loadMovies(true);
    
    const modal = bootstrap.Modal.getInstance(document.getElementById('filterModal'));
    modal.hide();
});

// Кнопка "Мне повезёт"
document.getElementById('luckyBtn').addEventListener('click', async () => {
    try {
        const response = await fetch('/api/random');
        const movie = await response.json();
        
        document.getElementById('movieFeed').innerHTML = '';
        renderMovies([movie]);
    } catch (error) {
        console.error('Error getting random movie:', error);
    }
});

// Начальная загрузка фильмов
loadMovies();
