document.addEventListener("DOMContentLoaded", () => {
    const daysContainer = document.querySelector(".days");
    const monthLabel = document.querySelector(".month");
    const prevBtn = document.querySelectorAll(".nav-btn")[0];
    const nextBtn = document.querySelectorAll(".nav-btn")[1];

    let currentDate = new Date();

    const renderCalendar = (date) => {
        daysContainer.innerHTML = "";
        const year = date.getFullYear();
        const month = date.getMonth();

        const monthNames = [
            "January", "February", "March", "April", "May", "June",
            "July", "August", "September", "October", "November", "December"
        ];
        monthLabel.textContent = monthNames[month];

        const firstDay = new Date(year, month, 1).getDay(); // день недели
        const daysInMonth = new Date(year, month + 1, 0).getDate(); // кол-во дней

        const offset = (firstDay + 6) % 7; // делаем так, чтобы неделя начиналась с понедельника

        for (let i = 0; i < offset; i++) {
            const span = document.createElement("span");
            span.textContent = "";
            daysContainer.appendChild(span);
        }

        for (let d = 1; d <= daysInMonth; d++) {
            const span = document.createElement("span");
            span.textContent = d < 10 ? "0" + d : d;
            const isToday =
                d === new Date().getDate() &&
                month === new Date().getMonth() &&
                year === new Date().getFullYear();

            if (isToday) {
                span.classList.add("active");
            }

            // здесь можно будет отмечать даты с бронями
            daysContainer.appendChild(span);
        }
    };

    prevBtn.addEventListener("click", () => {
        currentDate.setMonth(currentDate.getMonth() - 1);
        renderCalendar(currentDate);
    });

    nextBtn.addEventListener("click", () => {
        currentDate.setMonth(currentDate.getMonth() + 1);
        renderCalendar(currentDate);
    });

    renderCalendar(currentDate);
});
