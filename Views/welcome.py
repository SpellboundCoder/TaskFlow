from flet import (
    Page,
    Container,
    Row,
    Column,
    ElevatedButton,
    SnackBar,
    Text,
    FontWeight,
    alignment,
    MainAxisAlignment,
    TextField,
    TextSpan,
    TextStyle,
    TextDecoration,
    Image,
    icons,
    colors,
    ScrollMode,
    padding)
from controls import EmailRow
from core import AppStyle
from data.dbconfig import User


class Welcome(Container):

    def __init__(self, login_page: Page, session, chart): # noqa
        super().__init__(expand=True, padding=15)
        self.page = login_page
        self.AppStyle = AppStyle(self.page.theme_mode)
        self._session = session

        # LOGIN Form
        self.login_email = EmailRow(lambda e: self.activate_lock(), self.page.theme_mode)

        self.first_name = TextField(
            **self.AppStyle.input_textfield(),
            label='First Name',
            prefix_icon=icons.ACCOUNT_BOX,
        )
        self.last_name = TextField(
            **self.AppStyle.input_textfield(),
            label='Last Name',
            prefix_icon=icons.ACCOUNT_BOX,
        )
        self.login_button = ElevatedButton(
            **self.AppStyle.primary_button(),
            text='Enter',
            on_click=lambda e: self.validate(),
        )
        self.login_error = SnackBar(
            Text('Please fill in all lines!',
                 color=colors.WHITE),
            bgcolor=colors.RED
        )

        # PAGE CONTENT
        self.content = Container(
            content=Column(
                controls=[
                    Container(
                        content=Image(src='todo.png'),
                        alignment=alignment.center,
                    ),
                    Container(
                        content=Column(
                            scroll=ScrollMode.HIDDEN,
                            spacing=20,
                            controls=[
                                Row(
                                    alignment=MainAxisAlignment.CENTER,
                                    controls=[
                                        Text(
                                            value='Welcome to ',
                                            size=24,
                                            weight=FontWeight.BOLD,
                                            spans=[
                                                TextSpan(
                                                    text='TaskFlow',
                                                    style=TextStyle(
                                                        decoration=TextDecoration.UNDERLINE,
                                                        color=colors.BLUE_ACCENT_700)
                                                )
                                            ]
                                        )]
                                ),
                                Row(
                                    alignment=MainAxisAlignment.CENTER,
                                    controls=[
                                        Text(
                                            value='Please fill up the lines below',
                                            size=20,
                                            weight=FontWeight.BOLD)]
                                ),
                                Row(
                                    controls=[self.first_name]
                                ),
                                Row(
                                    controls=[self.last_name]
                                ),
                                self.login_email,
                                Row(
                                    alignment=MainAxisAlignment.CENTER,
                                    controls=[self.login_button]
                                ),
                                Row(height=40),
                            ],
                        ),
                        padding=padding.only(left=15, right=15)
                    ),
                    self.login_error,
                ]
            )
        )

    def validate(self):
        email = self.login_email.controls[0].value
        first_name = self.first_name.value
        last_name = self.last_name.value
        if email and first_name and last_name:
            self.page.client_storage.set(key="user_email", value=email)
            self.page.client_storage.set(key="first_name", value=first_name)
            self.page.client_storage.set(key="last_name", value=last_name)
            new_user = User(first_name=self.first_name.value,
                            last_name=self.last_name.value,
                            email=self.login_email.controls[0].value
                            )
            self._session.add(new_user)
            self._session.commit()
            self.page.go('/')

        else:
            self.login_error.open = True
            self.login_error.update()

    def activate_lock(self):
        pass
