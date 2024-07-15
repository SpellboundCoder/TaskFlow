from flet import (
    Container,
    Row,
    Column,
    Text,
    ScrollMode,
    ProgressBar,
    colors
    )
from core import AppStyle
from typing import Iterable


class CategoriesCard(Row):
    def __init__(self, all_tasks: Iterable):
        super().__init__(scroll=ScrollMode.AUTO)

        self.tasks = [task for task in all_tasks if not task.deleted]

        categories = ['All', 'Family', 'Business', 'Friends', 'Health', 'Education']

        for i, category in enumerate(categories):

            a = len(self.tasks)
            completed_from_all = [task for task in self.tasks if task.completed]
            b = len(completed_from_all)
            task_by_category = [task for task in self.tasks if task.tag == category]
            x = len(task_by_category)
            completed_by_category = [task for task in self.tasks if task.tag == category and task.completed]
            y = len(completed_by_category)
            self.controls.append(
                Container(
                    **AppStyle.category_container(),
                    content=Column(
                        controls=[
                            Text(value=f'{x} Tasks'),
                            Text(category),
                            Container(height=10),
                            ProgressBar(value=y / x if x != 0 else 0,
                                        bar_height=5, color=colors.GREEN_ACCENT_700),
                        ]
                    ) if category != 'All' else
                    Column(
                        controls=[
                            Text(value=f'{a} Tasks'),
                            Text(category),
                            Container(height=10),
                            ProgressBar(value=b / a if a != 0 else 0,
                                        bar_height=5, color=colors.GREEN_ACCENT_700),
                        ]
                            )
                )
            )
