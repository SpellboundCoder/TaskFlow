from flet import (
    Container,
    IconButton,
    Icon,
    Column,
    Row,
    TextField,
    Text,
    MainAxisAlignment,
    Page,
    padding,
    icons)
from core import AppStyle


class UserSearchBar(Container):
    def __init__(self, func, theme_mode: Page.theme_mode):
        super().__init__(**AppStyle.search_bar())

        self.content = Column([
            Row([
                IconButton(icon=icons.ARROW_BACK_ROUNDED,
                           on_click=lambda e: self.view_search_close(),
                           icon_size=18,
                           offset=(-0.3, 0.05)
                           ),
                TextField(
                    **AppStyle(None).search_bar_textfield(),
                    on_change=func,
                    offset=(-0.05, 0),
                    content_padding=padding.only(bottom=5)
                ),
                IconButton(icon=icons.CLOSE,
                           icon_size=16,
                           on_click=lambda e: self.clear_search_field(e, func)),
            ], spacing=0, visible=False, alignment=MainAxisAlignment.SPACE_BETWEEN, height=40
            ),
            Row(
                height=40,
                controls=[
                    Container(
                        content=Row([
                            Text('Search...', size=18),
                            Icon(name=icons.SEARCH),
                        ], spacing=10,
                            alignment=MainAxisAlignment.SPACE_BETWEEN),
                        expand=True,
                        on_click=lambda e: self.view_search()
                    )
                ]),

        ], alignment=MainAxisAlignment.CENTER)

    def view_search(self):
        self.content.controls[0].visible = True
        self.content.controls[1].visible = False
        self.update()

    def view_search_close(self):
        self.content.controls[1].visible = True
        self.content.controls[0].visible = False
        self.update()

    def clear_search_field(self, e, func):
        self.content.controls[0].controls[1].value = ''
        self.content.controls[0].controls[1].focus()
        self.content.controls[0].controls[1].update()
        func(e)

