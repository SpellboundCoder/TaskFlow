from math import pi
from flet import (Page,
                  Container,
                  LinearGradient,
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
                  Offset,
                  icons,
                  colors,
                  ScrollMode,
                  padding)
from controls import EmailRow
from core import AppStyle
from data.dbconfig import User
from time import sleep
from func import compare_hashes, hash_password


class Login(Container):

    def __init__(self, login_page: Page, session):
        super().__init__(expand=True, padding=15)
        self.page = login_page
        self.session = session

        self.AppStyle = AppStyle(self.page.theme_mode)

        # LOGIN Form
        self.login_email = EmailRow(lambda e: self.activate_lock(), self.page.theme_mode)

        self.login_password = TextField(
            **self.AppStyle.input_textfield(),
            label='Password',
            prefix_icon=icons.LOCK,
            password=True,
            can_reveal_password=True,
            on_focus=lambda e: self.activate_lock()
        )
        self.login_button = ElevatedButton(
            **self.AppStyle.primary_button(),
            text='Log In',
            on_click=lambda e: self.login_auth(),
        )
        self.login_error = SnackBar(
            Text('Username or Password is incorrect!',
                 color=colors.WHITE),
            bgcolor=colors.RED
        )

        # PAGE CONTENT
        self.content = Container(
            content=Column(
                controls=[
                    Container(
                        # content=self.lock,
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
                                            value='Welcome to PrivatePassSafe',
                                            size=24,
                                            weight=FontWeight.BOLD)]
                                ),
                                self.login_email,
                                Row(
                                    controls=[self.login_password]
                                ),
                                Row(
                                    height=20,
                                    alignment=MainAxisAlignment.END,
                                    controls=[
                                        Text('Forget password?',
                                             offset=Offset(0, -0.4))
                                    ]),
                                Row(
                                    alignment=MainAxisAlignment.CENTER,
                                    controls=[self.login_button]
                                ),
                                Row(height=40),
                                Row(
                                    alignment=MainAxisAlignment.CENTER,
                                    controls=[
                                        Text("Don't have an account yet? Sign up ",
                                             spans=[
                                                 TextSpan(
                                                     text='here.',
                                                     on_click=lambda s: self.to_register(),
                                                     style=TextStyle(
                                                         italic=True,
                                                         decoration=TextDecoration.UNDERLINE)
                                                 )
                                             ]
                                             )
                                    ],
                                )
                            ],
                        ),
                        padding=padding.only(left=15, right=15)
                    ),
                    self.login_error,
                ]
            )
        )

    def login_auth(self):
        email = self.login_email.controls[0].value
        hashed_password = hash_password(self.login_password.value)
        user = self.session.query(User).filter_by(email=email).one_or_none()
        if user:
            if compare_hashes(user.password, hashed_password):
                self.page.session.set(key="username", value=user.username)
                self.page.session.set(key="email", value=user.email)
                self.page.session.set(key="pass", value=self.login_password.value)
                self.page.client_storage.set(key="username", value=user.username)
                self.page.client_storage.set(key="email", value=user.email)
                self.lock.stop_animation()
                sleep(0.2)
                self.page.go('/home')
            else:
                self.login_error.open = True
                self.login_error.update()
        else:
            self.login_error.open = True
            self.login_error.update()

    def activate_lock(self):
        if not self.activated_lock:
            self.activated_lock = True
            self.lock.animate_lock()

    def to_register(self):
        self.page.go('/register')
