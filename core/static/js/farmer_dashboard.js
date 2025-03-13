document.addEventListener('DOMContentLoaded', () => {
  const ctx = document.getElementById('diseaseChart').getContext('2d');
  const diseaseChart = new Chart(ctx, {
      type: 'line',
      data: {
          labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun'],
          datasets: [{
              label: 'Disease Trends',
              data: [5, 10, 3, 15, 8, 20],
              borderColor: '#2e7d32',
              backgroundColor: 'rgba(46, 125, 50, 0.2)',
              borderWidth: 2
          }]
      },
      options: {
          responsive: true,
          scales: {
              y: {
                  beginAtZero: true
              }
          }
      }
  });
});
