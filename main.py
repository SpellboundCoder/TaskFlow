from flet import (
    Page,
    View,
    ThemeMode,
    app
    )
import matplotlib
import matplotlib.pyplot as plt

from Views import Welcome, CreateTask, Home, Completed, Deleted
from data.dbconfig import engine
from sqlalchemy.orm import sessionmaker

Session = sessionmaker(bind=engine)
session = Session()

matplotlib.use("svg")
plt.figure(figsize=(10, 6), facecolor='none')


def main(page_: Page):
    # page_.client_storage.clear()
    page_.theme_mode = ThemeMode.DARK
    page_.window.width = 500
    page_.window.height = 900

    def chart():
        fig, ax = plt.subplots(figsize=(10, 6), facecolor='none')

        ax.set_facecolor('none')
        ax.spines['top'].set_visible(False)
        ax.spines['bottom'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['left'].set_visible(False)

        ax.xaxis.set_ticks([])
        ax.yaxis.set_ticks([])
        return fig, ax

    def route_change(route):
        route_page = {
            '/': Home,
            '/welcome': Welcome,
            '/create_task': CreateTask,
            '/completed': Completed,
            '/deleted': Deleted
        }[page_.route](page_, session, chart())
        page_.views.clear()
        page_.views.append(
            View(
                route=route,
                controls=[route_page]
            )
        )
        page_.update()

    page_.on_route_change = route_change

    if page_.client_storage.contains_key('first_name'):
        page_.go('/')
    else:
        page_.go('/welcome')


app(target=main, assets_dir='/assets')  # view=WEB_BROWSER, port=8000
