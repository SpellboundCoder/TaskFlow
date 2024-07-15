from flet import *
from core import AppStyle
from controls import ActiveTasks
from data.dbconfig import User, Task
import datetime as dt
from time import sleep

now = dt.datetime.now().strftime('%d-%m-%y')
today = dt.datetime.today().strftime('%d')


class CreateTask(Container):
    def __init__(self, task_page: Page, session, chart): # noqa
        super().__init__(expand=True, border_radius=35, padding=25)

        self.db_session = session
        self.page = task_page
        self.style = AppStyle(self.page.theme_mode)

        self.user = self.db_session.query(User).filter_by(email=self.page.client_storage.get('user_email')).first()

        # Task field
        self.task = TextField(**self.style.task_textfield())
        self.all_tasks = self.user.tasks
        self.today_tasks = [task for task in self.all_tasks[::-1] if
                            task.active and task.date.split('-')[0] == today]

        self.add_button = ElevatedButton(
            **AppStyle.primary_button(),
            text='ADD',
            on_click=lambda e: self.add_task(),
        )
        self.tasks = ActiveTasks(tasks=self.today_tasks, session=self.db_session, home_page=self.page)

        # BACK ARROW
        self.back = IconButton(
            icon=icons.ARROW_CIRCLE_LEFT_ROUNDED,
            icon_size=35,
            offset=(-0.3, -0.3),
            on_click=lambda e: self.go_back()
        )

        # CATEGORY
        self.tag_list = ['Business', 'Family', 'Friends', 'Health', 'Education']
        self.dd_tags = Dropdown(
            **self.style.dropdown(),
            value='Family',
            options=[
                dropdown.Option(f'{self.tag_list[i]}')
                for i in range(len(self.tag_list))
            ],
        )

        # validate error
        self.validate_error = SnackBar(
            Text(color=colors.WHITE),
            bgcolor=colors.RED_ACCENT_700)

        self.content = Column(
            controls=[
                Row([self.back], MainAxisAlignment.START),
                VerticalDivider(width=20),
                Text('Write a new Task below:', size=20, weight=FontWeight.BOLD),
                Row([
                    Container(
                        **self.style.task_container(),
                        expand=True,
                        content=self.task
                    )
                ]),
                Text('Choose a category :', size=20, weight=FontWeight.BOLD),
                Row([self.dd_tags]),
                Row([self.add_button], alignment=MainAxisAlignment.CENTER),
                self.validate_error,
                VerticalDivider(width=20),
                Text("Today's Tasks :", size=20, weight=FontWeight.BOLD),
                self.tasks
            ]
        )

    def add_task(self):
        if self.task.value:
            new_task = Task(
                task=self.task.value,
                tag=self.dd_tags.value,
                completed=False,
                deleted=False,
                active=True,
                date=now
            )
            self.user.tasks.append(new_task)
            self.db_session.commit()
            sleep(0.1)
            self.content.controls.remove(self.tasks)
            self.user = self.db_session.query(User).filter_by(email=self.page.client_storage.get('user_email')).first()
            self.all_tasks = self.user.tasks
            self.today_tasks = [task for task in self.all_tasks[::-1] if
                                task.active and task.date.split('-')[0] == today]
            self.tasks = ActiveTasks(tasks=self.today_tasks, session=self.db_session, home_page=self.page)

            self.content.controls.append(self.tasks)
            self.page.update()

        else:
            self.validate_error.content.value = "The task field is empty please fill it up."
            self.validate_error.open = True
            self.validate_error.update()

    def go_back(self):
        self.page.go('/')
