google.charts.load('current', {'packages': ['corechart']});
google.charts.setOnLoadCallback(drawChart);


var options = {
    method: 'GET',
    mode: 'same-origin',
    headers: {
        "Content-Type": "application/json",
    }
}

fetch(url, options)
    .then(response => response.json())
    .then(data => {
        console.log(data.organizations)

    })


function drawChart() {

// Set Data
    const data = google.visualization.arrayToDataTable([
        ['', ''],
        ['Italy', 34],
        ['France', 49],
        ['Spain', 44],
        ['USA', 24],
        ['Argentina', 15]
    ]);

// Set Options
    const options = {
        title: 'World Wide Wine Production'
    };

// Draw
    const chart = new google.visualization.BarChart(document.getElementById('myChart'));
    chart.draw(data, options);

}
