// static/transport/js/city_filter.js

function loadCities(countrySelectId, citySelectId) {
    const countrySelect = document.getElementById(countrySelectId);
    const citySelect = document.getElementById(citySelectId);
    const selectedCity = citySelect.getAttribute('data-selected');

    countrySelect.addEventListener('change', function () {
        const countryId = this.value;
        citySelect.innerHTML = '<option value="">Все</option>';
        if (!countryId) return;
        fetch(`/transport/ajax/cities/?country_id=${countryId}`)
            .then(response => response.json())
            .then(data => {
                data.cities.forEach(function (city) {
                    const option = document.createElement('option');
                    option.value = city.id;
                    option.textContent = city.name;
                    citySelect.appendChild(option);
                });
            });
    });

    // При первой загрузке — если страна выбрана, сразу подгружаем города
    if (countrySelect.value) {
        fetch(`/transport/ajax/cities/?country_id=${countrySelect.value}`)
            .then(response => response.json())
            .then(data => {
                citySelect.innerHTML = '<option value="">Все</option>';
                data.cities.forEach(function (city) {
                    const option = document.createElement('option');
                    option.value = city.id;
                    option.textContent = city.name;
                    if (selectedCity && String(city.id) === selectedCity) {
                        option.selected = true;
                    }
                    citySelect.appendChild(option);
                });
            });
    }
}

document.addEventListener('DOMContentLoaded', function () {
    loadCities('departure-country', 'departure-city');
    loadCities('arrival-country', 'arrival-city');
});
