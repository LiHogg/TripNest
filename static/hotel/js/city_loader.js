document.addEventListener("DOMContentLoaded", function() {
  const countrySelect = document.getElementById("country-select");
  const citySelect = document.getElementById("city-select");

  if (!countrySelect || !citySelect) return;

  countrySelect.addEventListener("change", function() {
    const countryId = this.value;

    if (countryId) {
      fetch(`/hotels/get-cities/?country_id=${countryId}`)
        .then(response => response.json())
        .then(data => {
          citySelect.innerHTML = '<option value="">Выберите город</option>';
          data.forEach(city => {
            const option = document.createElement("option");
            option.value = city.id;
            option.textContent = city.name;
            citySelect.appendChild(option);
          });
          citySelect.disabled = false;
        });
    } else {
      citySelect.innerHTML = '<option value="">Сначала выберите страну</option>';
      citySelect.disabled = true;
    }
  });
});
