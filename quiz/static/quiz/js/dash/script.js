google.charts.load('current', {'packages': ['corechart']});
google.charts.setOnLoadCallback(drawChart);

function drawChart() {

// Set Data
    const data = google.visualization.arrayToDataTable([
        ['', ''],
        ['Italy lorem ipsum dolor sit ammet duoplup dheuyjhbzscasca  e', 34],
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
