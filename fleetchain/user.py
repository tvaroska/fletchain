from typing import Callable

import flet as ft


class UserEntry(ft.Row):
    def __init__(self, 
                 initials: str,
                 send_message: Callable,
                 text_color: str = ft.colors.WHITE,
                 bg_color: str = ft.colors.BLACK):
        super().__init__()

        self.send_message = send_message
        self.initials = initials
        self.vertical_alignment = "start"

        self.controls = [
            # Avatar for Self
            ft.CircleAvatar(
                content=ft.Text(self.initials),
                color=text_color,
                bgcolor=bg_color,
            ),
            # A new message entry form
            ft.TextField(
                hint_text="Write a message...",
                autofocus=True,
                min_lines=1,
                max_lines=5,
                filled=True,
                expand=True,
                # Enter = send message, CTRL-Enter = new line
                shift_enter=True,
                on_submit=self.send_message_click,
            ),
            # Send button for mouse users
            ft.IconButton(
                icon=ft.icons.SEND_ROUNDED,
                tooltip="Send message",
                on_click=self.send_message_click,
            ),
        ]

    @property
    def value(self):
        return self.controls[1].value

    async def clear(self):
        self.controls[1].value = ""
        await self.update_async()

    async def send_message_click(self, e):
        await self.send_message(e)


class ChatMessage(ft.Row):
    def __init__(self, 
                 initials: str,
                 message: str,
                 text_color: str = ft.colors.WHITE,
                 bg_color: str = ft.colors.BLACK):
        super().__init__()

        self.initials = initials
        self.vertical_alignment = "start"

        self.controls = [
            # Avatar for Self
            ft.CircleAvatar(
                content=ft.Text(self.initials),
                color=text_color,
                bgcolor=bg_color
            ),
            ft.Text(message),
        ]
