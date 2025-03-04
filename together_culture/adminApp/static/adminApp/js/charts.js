// Initialize the Event Type Chart
var eventTypeCtx = document.getElementById('eventTypeChart').getContext('2d');
var eventTypeChart = new Chart(eventTypeCtx, {
    type: 'bar',
    data: {
        labels: [], // Initially empty
        datasets: [{
            label: 'Event Types',
            data: [],  // Initially empty
            backgroundColor: 'rgba(75, 192, 192, 0.2)',
            borderColor: 'rgba(75, 192, 192, 1)',
            borderWidth: 1
        }]
    },
    options: {
        scales: {
            y: {
                beginAtZero: true
            }
        }
    }
});

// Initialize the Event Tag Chart
var eventTagCtx = document.getElementById('eventTagChart').getContext('2d');
var eventTagChart = new Chart(eventTagCtx, {
    type: 'bar',
    data: {
        labels: [], // Initially empty
        datasets: [{
            label: 'Event Tags',
            data: [],  // Initially empty
            backgroundColor: 'rgba(153, 102, 255, 0.2)',
            borderColor: 'rgba(153, 102, 255, 1)',
            borderWidth: 1
        }]
    },
    options: {
        scales: {
            y: {
                beginAtZero: true
            }
        }
    }
});

// Initialize the Event Label Chart
var eventLabelCtx = document.getElementById('eventLabelChart').getContext('2d');
var eventLabelChart = new Chart(eventLabelCtx, {
    type: 'bar',
    data: {
        labels: [], // Initially empty
        datasets: [{
            label: 'Event Labels',
            data: [],  // Initially empty
            backgroundColor: 'rgba(255, 159, 64, 0.2)',
            borderColor: 'rgba(255, 159, 64, 1)',
            borderWidth: 1
        }]
    },
    options: {
        scales: {
            y: {
                beginAtZero: true
            }
        }
    }
});

var eventChartCtx = document.getElementById('eventChart').getContext('2d');
var eventChart = new Chart(eventChartCtx, {
    type: 'bar',
    data: {
        labels: [], // Initially empty
        datasets: [{
            label: 'Events per month',
            data: [],  // Initially empty
            backgroundColor: 'rgba(255, 159, 64, 0.2)',
            borderColor: 'rgb(8, 244, 39)',
            borderWidth: 1
        }]
    },
    options: {
        scales: {
            y: {
                beginAtZero: true
            }
        }
    }
});

// Function to fetch event type data
function updateEventTypeChart() {
    const url = document.getElementById('eventTypeChart').getAttribute('data-url');
    fetch(url)
        .then(response => response.json())
        .then(data => {
            eventTypeChart.data.labels = data.eventTypes;  // Update the labels
            eventTypeChart.data.datasets[0].data = data.eventTypeValues;  // Update the data
            eventTypeChart.update();  // Refresh the chart
        })
        .catch(error => console.error('Error fetching event type data:', error));
}

// Function to fetch event tag data
function updateEventTagChart() {
    const url = document.getElementById('eventTagChart').getAttribute('data-url');
    fetch(url)
        .then(response => response.json())
        .then(data => {
            eventTagChart.data.labels = data.eventTags;  // Update the labels
            eventTagChart.data.datasets[0].data = data.eventTagValues;  // Update the data
            eventTagChart.update();  // Refresh the chart
        })
        .catch(error => console.error('Error fetching event tag data:', error));
}

// Function to fetch event label data
function updateEventLabelChart() {
    const url = document.getElementById('eventLabelChart').getAttribute('data-url');
    fetch(url)
        .then(response => response.json())
        .then(data => {
            eventLabelChart.data.labels = data.eventLabels;  // Update the labels
            eventLabelChart.data.datasets[0].data = data.eventLabelValues;  // Update the data
            eventLabelChart.update();  // Refresh the chart
        })
        .catch(error => console.error('Error fetching event label data:', error));
}

// Function to fetch event per month data
function updateEventsChart() {
    const url = document.getElementById('eventChart').getAttribute('data-url');
    fetch(url)
        .then(response => response.json())
        .then(data => {
            eventChart.data.labels = data.months;  // Update the labels
            eventChart.data.datasets[0].data = data.event_counts;  // Update the data
            eventChart.update();  // Refresh the chart
        })
        .catch(error => console.error('Error fetching event label data:', error));
}

// Call the update functions to load the charts initially
updateEventTypeChart();
updateEventTagChart();
updateEventLabelChart();
updateEventsChart();

// Optionally, you can set an interval to update the charts periodically (e.g., every 30 seconds)
setInterval(() => {
    updateEventTypeChart();
    updateEventTagChart();
    updateEventLabelChart();
    updateEventsChart();
}, 30000);  // 30000ms = 30 seconds