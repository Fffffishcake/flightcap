'use strict';
(async () => {
    const dates = [
        '2022-07-01',
        '2022-07-02',
        '2022-07-03',
        '2022-07-06',
        '2022-07-08',
        '2022-07-09',
        '2022-07-10',
        '2022-07-13',
        '2022-07-15',
        '2022-07-16',
        '2022-07-17',
        '2022-07-20',
        '2022-07-22',
        '2022-07-23',
        '2022-07-24',
        '2022-07-27',
        '2022-07-29',
        '2022-07-30',
        '2022-07-31',
    ];

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
        div.innerText += `${totalBooked}/${totalCapacity} = ${totalBooked/totalCapacity}`;
        section.appendChild(div);
    }
})();