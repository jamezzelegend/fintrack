const CHART_COLORS = [
  '#4f46e5', '#10b981', '#f59e0b', '#ef4444', '#3b82f6',
  '#8b5cf6', '#ec4899', '#14b8a6', '#f97316', '#6366f1',
];

function formatCurrency(value) {
  return new Intl.NumberFormat('en-US', {
    style: 'currency',
    currency: 'USD',
  }).format(value);
}

document.addEventListener('DOMContentLoaded', async function () {
  try {
    const response = await fetch('/analytics/api/charts');
    const data = await response.json();

    Chart.defaults.font.family = "'Segoe UI', system-ui, sans-serif";
    Chart.defaults.color = '#64748b';

    const rankingsCtx = document.getElementById('categoryRankingsChart');
    if (rankingsCtx && data.category_rankings.labels.length) {
      new Chart(rankingsCtx, {
        type: 'bar',
        data: {
          labels: data.category_rankings.labels,
          datasets: [{
            label: 'Total Spending',
            data: data.category_rankings.values,
            backgroundColor: CHART_COLORS,
            borderRadius: 6,
          }],
        },
        options: {
          indexAxis: 'y',
          responsive: true,
          maintainAspectRatio: false,
          plugins: {
            legend: { display: false },
            tooltip: {
              callbacks: {
                label: (ctx) => ` ${formatCurrency(ctx.raw)}`,
              },
            },
          },
          scales: {
            x: {
              beginAtZero: true,
              ticks: {
                callback: (value) => formatCurrency(value),
              },
            },
          },
        },
      });
    } else if (rankingsCtx) {
      rankingsCtx.parentElement.innerHTML = '<p class="text-muted text-center py-5">No spending data available yet.</p>';
    }

    const trendCtx = document.getElementById('analyticsTrendChart');
    if (trendCtx) {
      new Chart(trendCtx, {
        type: 'line',
        data: {
          labels: data.monthly_trend.labels,
          datasets: [
            {
              label: 'Income',
              data: data.monthly_trend.income,
              borderColor: '#10b981',
              backgroundColor: 'rgba(16, 185, 129, 0.1)',
              fill: false,
              tension: 0.4,
            },
            {
              label: 'Expenses',
              data: data.monthly_trend.expenses,
              borderColor: '#ef4444',
              backgroundColor: 'rgba(239, 68, 68, 0.1)',
              fill: false,
              tension: 0.4,
            },
            {
              label: 'Net',
              data: data.monthly_trend.net,
              borderColor: '#4f46e5',
              backgroundColor: 'rgba(79, 70, 229, 0.1)',
              fill: true,
              tension: 0.4,
            },
          ],
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          plugins: {
            legend: { position: 'top' },
            tooltip: {
              callbacks: {
                label: (ctx) => ` ${ctx.dataset.label}: ${formatCurrency(ctx.raw)}`,
              },
            },
          },
          scales: {
            y: {
              ticks: {
                callback: (value) => formatCurrency(value),
              },
            },
          },
        },
      });
    }

    const budgetCtx = document.getElementById('budgetUtilizationChart');
    const emptyMsg = document.getElementById('budgetUtilizationEmpty');

    if (budgetCtx && data.budget_utilization.labels.length) {
      new Chart(budgetCtx, {
        type: 'bar',
        data: {
          labels: data.budget_utilization.labels,
          datasets: [
            {
              label: 'Spent',
              data: data.budget_utilization.spent,
              backgroundColor: 'rgba(239, 68, 68, 0.8)',
              borderRadius: 6,
            },
            {
              label: 'Budget Limit',
              data: data.budget_utilization.limits,
              backgroundColor: 'rgba(79, 70, 229, 0.5)',
              borderRadius: 6,
            },
          ],
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          plugins: {
            legend: { position: 'top' },
            tooltip: {
              callbacks: {
                label: (ctx) => ` ${ctx.dataset.label}: ${formatCurrency(ctx.raw)}`,
              },
            },
          },
          scales: {
            y: {
              beginAtZero: true,
              ticks: {
                callback: (value) => formatCurrency(value),
              },
            },
          },
        },
      });
    } else if (budgetCtx && emptyMsg) {
      budgetCtx.style.display = 'none';
      emptyMsg.style.display = 'block';
    }
  } catch (error) {
    console.error('Failed to load analytics charts:', error);
  }
});
