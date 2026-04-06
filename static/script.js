const context = document.getElementById('studyHoursOverTime').getContext('2d')

new Chart(context, {
    type: 'line',
    data: {
        labels: studyLabel,
        datasets: [{
            label: 'Hours Studied',
            data: studyData,
            borderWidth: 2,
            fill: true,
            tension: 0.4,
            borderColor: '#575799',
            backgroundColor: 'rgba(87, 87, 153, 0.20)',
            pointRadius: 4,
            pointBackgroundColor: '#575799',
            pointBorderColor: '#575799'
        }]
    },
    options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
            legend: {
                labels: {
                    color: '#575799'
                }
            }
        },
        scales: {
            x: {
                ticks: {
                    color: '#575799'
                }
            },
            y: {
                beginAtZero: true,
                ticks: {
                    color: '#575799'
                }
            }
        }
    }
});

const context1 = document.getElementById('productivityOverTime').getContext('2d')

new Chart(context1, {
    type: 'line',
    data: {
        labels: productivityLabel,
        datasets: [{
            label: 'Productivity',
            data: productivityData,
            borderWidth: 2,
            fill: true,
            tension: 0.4,
            borderColor: '#575799',
            backgroundColor: 'rgba(87, 87, 153, 0.20)',
            pointRadius: 4,
            pointBackgroundColor: '#575799',
            pointBorderColor: '#575799'
        }]
    },
    options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
            legend: {
                labels: {
                    color: '#575799'
                }
            }
        },
        scales: {
            x: {
                ticks: {
                    color: '#575799'
                }
            },
            y: {
                beginAtZero: true,
                min: 1,
                max: 5,
                ticks: {
                    stepSize: 1,
                    color: '#575799'
                }
            }
        }
    }
});

const context2 = document.getElementById('timeOnCourse').getContext('2d')

new Chart(context2, {
    type: 'bar',
    data: {
        labels: courseLabel,
        datasets: [{
            label: 'Hours Spent',
            data: courseData,
            backgroundColor: '#575799',
            barPercentage: 0.7,
            categoryPercentage: 0.6,
        }]
    },
    options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
            legend: {
                labels: {
                    color: '#575799'
                }
            }
        },
        scales: {
            x: {
                ticks: {
                    color: '#575799'
                }
            },
            y: {
                beginAtZero: true,
                ticks: {
                    color: '#575799'
                }
            }
        }
    }
});

const context3 = document.getElementById('productivityByMethod').getContext('2d')

new Chart(context3, {
    type: 'bar',
    data: {
        labels: methodLabel,
        datasets: [{
            label: 'Average Productivity',
            data: methodData,
            backgroundColor: '#575799',
            barPercentage: 0.7,
            categoryPercentage: 0.6,
        }]
    },
    options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
            legend: {
                labels: {
                    color: '#575799'
                }
            }
        },
        scales: {
            y: {
                beginAtZero: true,
                min: 1,
                max: 5,
                ticks: {
                    stepSize: 1,
                    color: '#575799'
                }
            }
        }
    }
});