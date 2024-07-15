from flet import *
from data.dbconfig import User
from controls import CompletedTasks


class Completed(Container):
    def __init__(self, complete_page: Page, session, chart): # noqa
        super().__init__(expand=True, padding=padding.all(25))

        self.db_session = session
        self.page = complete_page

        # BACK ARROW
        self.back = IconButton(
            icon=icons.ARROW_CIRCLE_LEFT_ROUNDED,
            icon_size=35,
            offset=(-0.3, -0.3),
            on_click=lambda e: self.go_back()
        )

        # COMPLETED TASKS
        self.user = self.db_session.query(User).filter_by(email=self.page.client_storage.get('user_email')).first()
        self.all_tasks = self.user.tasks
        self.completed_tasks = [task for task in self.all_tasks if task.completed][::-1]

        self.tasks = CompletedTasks(self.completed_tasks)

        # DIALOG
        self.dlg_modal = AlertDialog(
            modal=True,
            title=Text("Please confirm"),
            content=Text("Are you sure you wanna clear info ?"),
            actions=[
                TextButton("Yes", on_click=lambda e: self.clear_completed_tasks()),
                TextButton("No", on_click=lambda e: self.close_dlg()),
            ],
            actions_alignment=MainAxisAlignment.END,
            on_dismiss=lambda e: print("Modal dialog dismissed!"),
        )

        self.content = Column(
            controls=[
                self.back,
                Row([
                    Text("Completed Tasks:", size=26),
                    Text('',
                         spans=[
                            TextSpan(
                                     text='Clear ALL Tasks.',
                                     on_click=lambda s: self.open_dlg_modal(),
                                     style=TextStyle(
                                         italic=True,
                                         decoration=TextDecoration.UNDERLINE
                                     )
                                 )]
                         )
                ], alignment=MainAxisAlignment.SPACE_BETWEEN),
                Container(height=20),
                self.tasks if len(self.completed_tasks) != 0 else Text('There are no completed Tasks yet.'),
                Container(height=50),
                Container(expand=True)
            ]
        )

    def go_back(self):
        self.page.go('/')

    def clear_completed_tasks(self):
        for task in self.completed_tasks:
            self.db_session.delete(task)
            self.db_session.commit()
        self.content.controls.remove(self.tasks)
        self.page.update()

    def open_dlg_modal(self):
        self.page.dialog = self.dlg_modal
        self.dlg_modal.open = True
        self.page.update()

    def close_dlg(self):
        self.dlg_modal.open = False
        self.page.update()
