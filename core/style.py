from flet import (
    Page,
    SweepGradient,
    ThemeMode,
    TextStyle,
    ButtonStyle,
    InputBorder,
    colors, padding, alignment, margin)
from typing import Union


BG = colors.INDIGO_900
GREEN = colors.GREEN_ACCENT_700


class AppStyle:
    def __init__(self, theme_mode: Union[Page.theme_mode, None]):
        super().__init__()
        self.mode = theme_mode
        self.sign_up_bgcolor = colors.DEEP_PURPLE_ACCENT_700 \
            if self.mode == ThemeMode.DARK else colors.INDIGO_ACCENT_700

    @staticmethod
    def avatar_background_container() -> dict:
        return {
            "gradient": SweepGradient(
                    center=alignment.center,
                    start_angle=0.0,
                    end_angle=3,
                    stops=[0.5, 0.5],
                    colors=['#00000000', GREEN],
                ),
            "width": 100,
            "height": 100,
            "border_radius": 50
        }

    @staticmethod
    def avatar_foreground_container() -> dict:
        return {
            "padding": padding.all(5),
            "bgcolor": BG,
            "width": 90,
            "height": 90,
            "border_radius": 50,
        }

    @staticmethod
    def circle_main_container() -> dict:
        return {
            "width": 100,
            "height": 100,
            "border_radius": 50,
            "bgcolor": 'white12'
        }

    @staticmethod
    def task_container() -> dict:
        return {
            "height": 70,
            # "width": 400,
            # "expand": True,
            "bgcolor": BG,
            "border_radius": 25,
            "padding": padding.all(10),
        }

    @staticmethod
    def input_textfield() -> dict:
        return {
            "height": 50,
            "expand": True,
            "bgcolor": BG,
            "border_radius": 25,
        }

    @staticmethod
    def primary_button() -> dict:
        return {
            'height': 45,
            'width': 300,
            'style': ButtonStyle(
                color=colors.WHITE,
                bgcolor=GREEN,
            )
        }

    @staticmethod
    def category_container() -> dict:
        return {
            "border_radius": 20,
            "bgcolor": BG,
            "width": 170,
            "height": 110,
            "padding": 15,

        }

    @staticmethod
    def search_bar_textfield() -> dict:
        return {
            'bgcolor': colors.TRANSPARENT,
            'border': InputBorder.NONE,
            'hover_color': colors.TRANSPARENT,
            'expand': True,
            'autofocus': True,
        }

    @staticmethod
    def search_bar() -> dict:
        return {
            'bgcolor': colors.INDIGO_900,
            'padding': padding.only(left=15, right=10),
            'margin': margin.only(left=5, right=10),
            'border_radius': 35,
            'expand': True
        }

    @staticmethod
    def check_box() -> dict:
        return {
            "height": 25,
            "width": 25

        }

    # DROPDOWN /
    def dropdown(self) -> dict:
        return {
            'bgcolor': BG,
            'border_color': colors.BLACK87,
            'border': 2,
            'border_radius': 10,
            'color': colors.WHITE if self.mode == ThemeMode.DARK else colors.BLACK87,
            'height': 50,
            'expand': True,
            'content_padding': padding.only(bottom=5, left=10),
            'text_style': TextStyle(size=20)
        }

    @staticmethod
    def task_textfield() -> dict:
        return {
            'multiline': True,
            'max_lines': 3,
            'bgcolor': colors.TRANSPARENT,
            'border': InputBorder.NONE,
            'hover_color': colors.TRANSPARENT,
            'cursor_height': 20
        }
