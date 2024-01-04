import flet as ft
from langchain_core.runnables import Runnable
from langchain_core.memory import BaseMemory

from fleetchain.user import UserEntry, ChatMessage

class FletChain(ft.UserControl):
    def __init__(self,
                 chain: Runnable,
                 memory:BaseMemory = None,
                 user_name: str = 'User',
                 user_color: str = ft.colors.WHITE,
                 user_bgcolor: str = ft.colors.BLACK,
                 ai_name: str = 'AI',
                 ai_color: str = ft.colors.BLACK,
                 ai_bgcolor: str = ft.colors.WHITE):
        super().__init__()

        self.chain = chain
        self.memory = memory
        self.user_initials = self.get_initials(user_name)
        self.user_color = user_color
        self.user_bg_color = user_bgcolor
        
        self.ai_initials = self.get_initials(ai_name)
        self.ai_color = ai_color
        self.ai_bgcolor = ai_bgcolor

        self.user_entry = UserEntry(self.user_initials, self.send_message_click)

        self.messages = ft.ListView(
            expand=True,
            spacing=10,
            auto_scroll=True,
        )

    def get_initials(self, name: str) -> str:
        if len(name) <= 2:
            return name
        elif len(name.split()) > 1:
            splits = name.split()
            return splits[0][0] + splits[-1][0]
        else:
            return name[0]

    async def send_message_click(self, e):
        inputs = {"input": self.user_entry.value}
        response = self.chain.invoke(inputs)
        if self.memory:
            self.memory.save_context(inputs, {"output": response.content})

        self.messages.controls.append(ChatMessage(self.user_initials, self.user_entry.value))
        await self.user_entry.clear()
        self.messages.controls.append(ChatMessage(self.ai_initials, response.content))
        await self.update_async()

    def build(self):
        return ft.Column(
            controls=[
                ft.Container(content=self.messages),
                ft.Container(content=self.user_entry),
            ],
        )
