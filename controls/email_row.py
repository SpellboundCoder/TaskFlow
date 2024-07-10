from flet import (Stack,
                  TextField,
                  Row,
                  Container,
                  MainAxisAlignment,
                  CrossAxisAlignment,
                  Text,
                  FontWeight,
                  AnimationCurve,
                  Page,
                  alignment,
                  icons,
                  transform,
                  animation)
from core import AppStyle


class EmailRow(Stack):
    def __init__(self, _on_focus, theme_mode: Page.theme_mode):
        super().__init__()
        self.spacing = 0
        self.AppStyle = AppStyle(theme_mode)
        self.controls = [
            TextField(on_change=lambda e: self.get_suffix_emails(e),
                      **self.AppStyle.input_textfield(),
                      label='Email',
                      prefix_icon=icons.EMAIL,
                      on_focus=_on_focus,
                      ),
            self.suffix_email_row(),
        ]

    def suffix_email_row(self) -> Row:
        email_labels = ["@gmail.com", '@yahoo.com']
        label_title = ["GMAIL", "YAHOO"]
        __ = Row(spacing=1, alignment=MainAxisAlignment.END)
        for index, label in enumerate(email_labels):
            __.controls.append(
                Container(
                    width=45,
                    height=30,
                    alignment=alignment.center,
                    data=label,
                    on_click=lambda e: self.return_email_suffix(e),
                    content=Text(
                        label_title[index],
                        size=12,
                        weight=FontWeight.BOLD
                    )
                )
            )
        return Row(
            vertical_alignment=CrossAxisAlignment.CENTER,
            alignment=MainAxisAlignment.END,
            spacing=2,
            opacity=0,
            animate_opacity=200,
            offset=transform.Offset(+0.1, 0),
            animate_offset=animation.Animation(400, curve=AnimationCurve.DECELERATE),
            controls=[__],
        )

    def get_suffix_emails(self, e) -> None:
        email = e.data
        if e.data:
            if "@gmail.com" in email or "@yahoo.com" in email:
                self.controls[1].offset = transform.Offset(+0.1, 0)
                self.controls[1].opacity = 0
                self.page.update()
            else:
                self.controls[1].offset = transform.Offset(-0.02, 0)
                self.controls[1].opacity = 1
                self.page.update()
        else:
            self.controls[1].offset = transform.Offset(+0.1, 0)
            self.controls[1].opacity = 0
            self.page.update()

    def return_email_suffix(self, e) -> None:
        email = self.controls[0].value
        if e.control.data in email:
            pass
        else:
            self.controls[0].value += e.control.data
            self.controls[1].offset = transform.Offset(0.5, 0)
            self.controls[1].opacity = 0
            self.page.update()
