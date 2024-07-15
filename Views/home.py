from flet import *
from core import AppStyle
from controls import CategoriesCard, ActiveTasks, UserSearchBar, Chart
from data.dbconfig import User
import datetime as dt


today = dt.datetime.today().strftime('%d')

FG = '#3450a1'
BG = colors.INDIGO_900
GREEN = colors.GREEN_ACCENT_400


class Home(Container):
    def __init__(self, home_page: Page, session, chart):
        super().__init__(expand=True, border_radius=35)
        self.page = home_page

        self.style = AppStyle(self.page.theme_mode)
        self.circle = Container(
            padding=10,
            content=CircleAvatar(
                                   width=80,
                                   height=80,
                                   foreground_image_src='https://picsum.photos/150',
                                   bgcolor=colors.INDIGO_900
                                   )
        )

        self.searchbar = UserSearchBar(func=lambda e: self.filter_tasks(e),
                                       theme_mode=self.page.theme_mode)

        self.user = session.query(User).filter_by(email=self.page.client_storage.get('user_email')).first()

        self.saved_tasks = self.user.tasks
        self.active_tasks = [task for task in self.saved_tasks if task.active]

        self.categories_card = CategoriesCard(self.saved_tasks)

        self.tasks = ActiveTasks(self.active_tasks, session, self.page)

        self.front_page_contents = Container(
            content=Column(
                controls=[
                    Row(
                        controls=[
                            Container(
                                width=40,
                                height=50,
                                on_click=lambda e: self.shrink(),
                                content=Icon(
                                    icons.MENU,
                                    size=35)),
                            self.searchbar,
                            IconButton(icon=icons.NOTIFICATIONS, icon_size=25)
                        ], spacing=0
                        ),
                    Container(height=20),
                    Text(
                        value=f"What's up, {self.page.client_storage.get('first_name')} !",
                    ),
                    Text(
                        value='CATEGORIES'
                    ),
                    Container(
                        padding=padding.only(top=10, bottom=20, ),
                        content=self.categories_card
                    ),

                    # Container(height=20)

                    Stack(
                        controls=[
                            self.tasks]
                    )
                ],
            ),
        )

        self.page_1 = Container(
            expand=True,
            border_radius=35,
            padding=padding.only(left=10, top=20, right=200),
            visible=False,
            bgcolor=colors.BLACK,

            content=Column(
                controls=[
                    Row(alignment=MainAxisAlignment.CENTER,
                        controls=[IconButton(icon=icons.ARROW_CIRCLE_LEFT_ROUNDED,
                                             icon_color=colors.WHITE,
                                             icon_size=40,
                                             on_click=lambda e: self.restore())]
                        ),
                    self.circle,
                    Text(
                        f'{self.page.client_storage.get('first_name')}\n{self.page.client_storage.get('last_name')}',
                        size=25, weight=FontWeight.BOLD),
                    Container(height=25),
                    Row(controls=[
                        Icon(icons.FAVORITE_BORDER_SHARP, color='white60'),
                        Text('Templates', size=15, weight=FontWeight.W_300, color='white', font_family='poppins')
                    ]),
                    Container(height=5),
                    Container(
                        Row(controls=[
                            Icon(icons.CHECK_BOX, color=colors.GREEN_ACCENT_700),
                            Text('Completed', size=15, weight=FontWeight.W_300, color='white', font_family='poppins')
                        ]), on_click=lambda e: self.go_to_completed()
                    ),

                    Container(height=5),
                    Container(
                        Row(controls=[
                            Icon(icons.DELETE, color=colors.RED),
                            Text('Deleted', size=15, weight=FontWeight.W_300, color='white', font_family='poppins')
                        ]), on_click=lambda e: self.go_to_deleted()
                    ),
                    Chart(self.saved_tasks, chart),
                    Text('Good', color=colors.GREEN_ACCENT_700, font_family='poppins', ),
                    Text('Consistency', size=22, )

                ]
            )
        )

        self.page_2 = Row(
            alignment=MainAxisAlignment.END,
            controls=[
                Container(
                    expand=True,
                    border_radius=35,
                    animate=animation.Animation(600, AnimationCurve.DECELERATE),
                    animate_scale=animation.Animation(300, curve=AnimationCurve.DECELERATE),
                    padding=padding.only(
                        top=50, left=20,
                        right=20, bottom=5
                    ),
                    bgcolor=colors.BLACK54,
                    content=Column(
                        controls=[
                            self.front_page_contents,
                            Row([
                                FloatingActionButton(
                                    bgcolor=colors.GREEN_ACCENT_700,
                                    icon=icons.ADD, on_click=lambda _: self.page.go('/create_task')
                                )
                            ], alignment=MainAxisAlignment.END)
                        ]
                    )
                )
            ]
        )

        self.content = Stack(
            controls=[
                self.page_1,
                self.page_2,
            ]
        )

    def shrink(self):
        self.page_2.controls[0].margin = margin.only(left=70) # noqa
        self.page_2.controls[0].scale = transform.Scale(0.75, alignment=alignment.center_right) # noqa
        self.page_2.controls[0].border_radius = border_radius.only(  # noqa
            top_left=35,
            top_right=0,
            bottom_left=35,
            bottom_right=0
        )
        self.page_1.visible = True

        self.page.update()

    def restore(self):

        self.page_2.controls[0].margin = None  # noqa
        self.page_2.controls[0].border_radius = 35  # noqa
        self.page_2.controls[0].scale = transform.Scale(1, alignment=alignment.center_right) # noqa

        self.page_1.visible = False

        self.page.update()

    def filter_tasks(self, e):
        if e.data:
            for task in self.tasks.controls:
                try:
                    task.visible = (
                        True
                        if e.data.lower() in task.label.lower()
                        else False
                    )
                except AttributeError:
                    pass
                else:
                    continue
            self.page.update()
        else:
            for task in self.tasks.controls:
                task.visible = True
            self.page.update()

    def go_to_deleted(self):
        self.page.go('/deleted')

    def go_to_completed(self):
        self.page.go('/completed')
