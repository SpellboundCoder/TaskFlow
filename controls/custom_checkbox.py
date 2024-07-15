from flet import (
    Page,
    Container,
    Icon,
    Row,
    Text,
    FontWeight,
    IconButton,
    icons,
    border,
    colors
    )
from core import AppStyle


class CustomCheckBox(Container):
    def __init__(self, home_page: Page, data, delete_func, session, date, label='', animation_=None,
                 checked=False, pressed=None):
        super().__init__(**AppStyle.task_container())

        self.page = home_page
        self.today = date
        self.selection_fill = colors.GREEN_ACCENT_700
        self.color = colors.BLUE_ACCENT_700
        self.data = data
        self.label = label
        self.size = 25
        self.stroke_width = 2
        self.animation = animation_
        self.checked = checked
        self.font_size = 17
        self.pressed = pressed
        self.CHECKED = colors.GREEN_ACCENT_700
        self.delete_func = delete_func
        self.check_box = self._checked() if self.checked else self._unchecked()
        self.db_session = session

        self.content = Row([
            self.check_box,
            Text(
                self.label,
                font_family='poppins',
                size=self.font_size,
                weight=FontWeight.W_300),
            Container(expand=True),
            IconButton(icon=icons.DELETE,
                       icon_color=colors.RED,
                       data=self.data,
                       on_click=lambda e: self.delete_func(e))
        ])

    def _checked(self):
        return Container(
            on_click=lambda e: self.checked_check(e),
            animate=self.animation,
            width=self.size, height=self.size,
            border_radius=(self.size/2)+5,
            bgcolor=self.CHECKED,
            content=Icon(icons.CHECK_ROUNDED, size=15),
        )
  
    def _unchecked(self):
        return Container(
            on_click=lambda e: self.checked_check(e),
            animate=self.animation,
            width=self.size,
            height=self.size,
            border_radius=(self.size/2)+5,
            bgcolor=None,
            border=border.all(color=self.color, width=self.stroke_width),
          )

    def checked_check(self, e):  # noqa
        print(self.checked)
        if not self.checked:
            self.checked = True
            self.check_box.border = None
            self.check_box.bgcolor = self.CHECKED
            self.check_box.content = Icon(icons.CHECK_ROUNDED, size=15)

            self.data.completed = True
            self.data.active = False
            self.data.date = self.today
            self.db_session.commit()
            # self.page.go('/home')
            self.page.update()

        elif self.checked:
            self.checked = False
            self.check_box.bgcolor = None
            self.check_box.border = border.all(color=self.color, width=self.stroke_width)
            self.check_box.content.visible = False

            self.data.completed = False
            self.data.active = True
            self.data.date = self.today

            self.db_session.commit()
            # self.page.go('/home')
            self.page.update()

        if self.pressed:
            self.run()

    # def is_checked(self):
    #     return self.checked

    def run(self, *args):
        self.pressed(args)
