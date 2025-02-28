// charts.js

// Get the context of the canvas element we want to use
var ctx = document.getElementById('chart').getContext('2d');

// Create a new chart instance
var chart = new Chart(ctx, {
    type: 'bar', // Type of chart (bar, line, etc.)
    data: {
        labels: ['January', 'February', 'March', 'April'],
        datasets: [{
            label: 'Sales',
            data: [12, 19, 3, 5],  // Data points
            backgroundColor: 'rgba(54, 162, 235, 0.2)', // Background color for bars
            borderColor: 'rgba(54, 162, 235, 1)',  // Border color for bars
            borderWidth: 1
        }]
    }
});
