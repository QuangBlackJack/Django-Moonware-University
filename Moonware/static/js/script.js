
sortDay();    

var chart = document.getElementById("chart");
var rank = document.getElementById("rank");
var myChart = document.getElementById("myChart");

window.addEventListener('load', function () {
    chart.style.width = '100%';
    chart.style.height = rank.clientHeight - 50 + "px";
    myChart.style.height = "80%";
});
// change on resize
window.addEventListener("resize", function () {
    chart.style.width = '100%';
    chart.style.height = rank.clientHeight - 50 + "px";
    myChart.style.height = "80%";
});

// days
function sortDay() {    
    var dropdownMenuButton = document.getElementById("dropdownMenuButton");
    dropdownMenuButton.innerHTML = "Day";
    var xValues = [1, 2, 3, 4, 5, 6, 7];
    var yValues = {{ valueYDay | safe }};
    

    new Chart("myChart", {
        type: "line",
        data: {
            labels: xValues,
            datasets: [{
                fill: false,
                lineTension: 0,
                backgroundColor: "#38C68B",
                borderColor: "#38c68b6b",
                data: yValues
            }]
        },
        options: {
            legend: { display: false },
            scales: {
                yAxes: [{ ticks: { min: 0, max: 16, fontColor: '#38C68B' } }],
                xAxes: [{ ticks: { fontColor: '#38C68B' } }]
            }
        }
    });
}

// weeks
function sortWeek() {
    var dropdownMenuButton = document.getElementById("dropdownMenuButton");
    dropdownMenuButton.innerHTML = `Week`;
    var xValues = [1, 2, 3, 4];
    var yValues = {{ valueYWeek | safe }};        

    new Chart("myChart", {
        type: "line",
        data: {
            labels: xValues,
            datasets: [{
                fill: false,
                lineTension: 0,
                backgroundColor: "#38C68B",
                borderColor: "#38c68b6b",
                data: yValues
            }]
        },
        options: {
            legend: { display: false },
            scales: {
                yAxes: [{ ticks: { min: 0, max: 16, fontColor: '#38C68B' } }],
                xAxes: [{ ticks: { fontColor: '#38C68B' } }]
            }
        }
    });
}

// months
function sortMonth() {
    var dropdownMenuButton = document.getElementById("dropdownMenuButton");
    dropdownMenuButton.innerHTML = `Month`;
    var xValues = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12];
    var yValues = {{ valueYMonth | safe }};        

    new Chart("myChart", {
        type: "line",
        data: {
            labels: xValues,
            datasets: [{
                fill: false,
                lineTension: 0,
                backgroundColor: "#38C68B",
                borderColor: "#38c68b6b",
                data: yValues
            }]
        },
        options: {
            legend: { display: false },
            scales: {
                yAxes: [{ ticks: { min: 0, max: 16, fontColor: '#38C68B' } }],
                xAxes: [{ ticks: { fontColor: '#38C68B' } }]
            }
        }
    });
}

