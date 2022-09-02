'use strict';
(async () => {
    const dates = [];
    const startDate = new Date();
    let date = new Date();
    while ((date - startDate) / 1000 / 60 / 60 / 24 < 59) {
        if ([0, 3, 5, 6].includes(date.getDay())) { // sun, wed, fri, sat
            const monthStr = String(date.getMonth() + 1).padStart(2, '0');
            const dateStr = String(date.getDate()).padStart(2, '0');
            dates.push(`${date.getFullYear()}-${monthStr}-${dateStr}`);
        }
        date.setDate(date.getDate() + 1);
    }

    const main = document.querySelector('#dates');
    for (const date of dates) {
        const section = document.createElement('section');
        main.appendChild(section);
        loadCapacity(date, section);
    }

    async function loadCapacity(date, section) {
        const r = await fetch('/flight_capacity?date=' + date);
        const cabins = await r.json();
        
        const h2 = document.createElement('h2');
        h2.innerText = date;
        section.appendChild(h2);

        let totalBooked = 0;
        let totalCapacity = 0;
        for (const cabin of cabins) {
            const div = document.createElement('div');
            div.innerText += `${cabin['name']}: ${cabin['booked']}/${cabin['capacity']}`;
            section.appendChild(div);
            totalBooked += cabin['booked'];
            totalCapacity += cabin['capacity'];
        }
        const div = document.createElement('div');
        const percentage = (totalBooked / totalCapacity).toLocaleString(
            undefined, {'style': 'percent', 'minimumFractionDigits': 2});
        div.innerText += `${totalBooked}/${totalCapacity} = ${percentage}`;
        section.appendChild(div);
    }
})();
