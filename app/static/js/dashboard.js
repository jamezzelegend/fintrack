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
    const response = await fetch('/api/dashboard/charts');
    const data = await response.json();

    Chart.defaults.font.family = "'Segoe UI', system-ui, sans-serif";
    Chart.defaults.color = '#64748b';

    const pieCtx = document.getElementById('expensePieChart');
    if (pieCtx && data.expense_breakdown.labels.length) {
      new Chart(pieCtx, {
        type: 'doughnut',
        data: {
          labels: data.expense_breakdown.labels,
          datasets: [{
            data: data.expense_breakdown.values,
            backgroundColor: CHART_COLORS,
            borderWidth: 2,
            borderColor: '#ffffff',
          }],
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          plugins: {
            legend: { position: 'bottom' },
            tooltip: {
              callbacks: {
                label: (ctx) => ` ${ctx.label}: ${formatCurrency(ctx.raw)}`,
              },
            },
          },
        },
      });
    } else if (pieCtx) {
      pieCtx.parentElement.innerHTML = '<p class="text-muted text-center py-5">No expense data available yet.</p>';
    }

    const trendCtx = document.getElementById('monthlyTrendChart');
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
              fill: true,
              tension: 0.4,
            },
            {
              label: 'Expenses',
              data: data.monthly_trend.expenses,
              borderColor: '#ef4444',
              backgroundColor: 'rgba(239, 68, 68, 0.1)',
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
              beginAtZero: true,
              ticks: {
                callback: (value) => formatCurrency(value),
              },
            },
          },
        },
      });
    }

    const barCtx = document.getElementById('incomeExpenseChart');
    if (barCtx) {
      new Chart(barCtx, {
        type: 'bar',
        data: {
          labels: data.income_vs_expense.labels,
          datasets: [
            {
              label: 'Income',
              data: data.income_vs_expense.income,
              backgroundColor: 'rgba(16, 185, 129, 0.8)',
              borderRadius: 6,
            },
            {
              label: 'Expenses',
              data: data.income_vs_expense.expenses,
              backgroundColor: 'rgba(239, 68, 68, 0.8)',
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
    }
  } catch (error) {
    console.error('Failed to load dashboard charts:', error);
  }
});
