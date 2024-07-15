from flet import (
    Page,
    Column,
    ScrollMode,
    Container,
    Row,
    Text,
    Icon,
    icons,
    colors
    )
from core import AppStyle
from controls import CustomCheckBox
from typing import Iterable
import datetime as dt

today = dt.datetime.today().strftime('%d')
now = dt.datetime.now().strftime('%d-%m-%y')


class ActiveTasks(Column):
    def __init__(self, tasks: Iterable, session, home_page: Page):
        super().__init__(height=400, scroll=ScrollMode.AUTO)

        self.page = home_page
        self.style = AppStyle(None)
        self.db_session = session

        self.today_tasks = [task for task in tasks if task.date.split('-')[0] == today]
        self.older_tasks = [task for task in tasks if task.date.split('-')[0] != today]

        if len(self.today_tasks) != 0:
            self.controls.append(
                Text("TODAY'S TASKS:")
            )
            for task in self.today_tasks:
                self.controls.append(
                    CustomCheckBox(
                        label=f'{task.task}',
                        data=task,
                        delete_func=lambda e: self.delete_task(e),
                        session=session,
                        date=now,
                        home_page=self.page))

        if len(self.older_tasks) != 0:
            self.controls.append(
                Text("TASKS:")
            )
            for task in self.older_tasks:
                self.controls.append(
                    CustomCheckBox(
                        label=f'{task.task}',
                        data=task,
                        delete_func=lambda e: self.delete_task(e),
                        session=session,
                        date=now,
                        home_page=self.page))

    def delete_task(self, e):
        website_to_delete = e.control.data
        website_to_delete.deleted = True
        website_to_delete.active = False
        # self.db_session.delete(website_to_delete)
        self.db_session.commit()
        self.controls.remove(e.control.data)
        self.page.update()


class DeletedTasks(Column):
    def __init__(self, tasks: Iterable):
        super().__init__(height=400, scroll=ScrollMode.AUTO)

        self.style = AppStyle(None)

        for task in tasks:
            self.controls.append(
                Container(
                    **AppStyle.task_container(),
                    data=task,
                    content=Row([
                        Icon(name=icons.DELETE, color=colors.RED),
                        Text(f'{task.task}')
                    ])
                )
            )


class CompletedTasks(Column):
    def __init__(self, tasks: Iterable):
        super().__init__(height=600, scroll=ScrollMode.AUTO)

        self.style = AppStyle(None)

        for task in tasks:
            self.controls.append(
                Container(
                    **AppStyle.task_container(),
                    content=Row([
                        Icon(name=icons.CHECK_BOX, color=colors.GREEN),
                        Text(f'{task.task}')
                    ])
                )
            )
