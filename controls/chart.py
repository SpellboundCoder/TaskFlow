from flet.matplotlib_chart import MatplotlibChart
import numpy as np
from scipy.interpolate import make_interp_spline
from flet import Container


class Chart(Container):
    def __init__(self, tasks, charts):
        super().__init__(padding=0,
                         height=150,
                         width=150)

        fig, ax = charts
        all_dates = sorted(set(task.date for task in tasks))

        completed_tasks_by_date = {date: 0 for date in all_dates}

        for task in tasks:
            if task.completed:
                completed_tasks_by_date[task.date] += 1

        completed_count = [completed_tasks_by_date[date] for date in all_dates]

        # creating smooth curve
        x = np.arange(len(all_dates))
        y = completed_count

        x_smooth = np.linspace(x.min(), x.max(), 300)
        spl = make_interp_spline(x, y, k=1)
        y_smooth = spl(x_smooth)

        ax.plot(x_smooth, y_smooth, marker='o', linestyle='-', color='lightgreen')

        self.content = MatplotlibChart(fig, expand=True)

