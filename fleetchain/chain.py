import flet as ft
from langchain_core.messages import ChatMessage

from fleetchain.user import UserEntry


class FletChain(ft.UserControl):
    def __init__(self, chain, memory=None):
        super().__init__()

        self.chain = chain
        self.memory = memory
        self.user_entry = UserEntry("B", self.send_message_click)

        self.messages = ft.ListView(
            expand=True,
            spacing=10,
            auto_scroll=True,
        )

    async def send_message_click(self, e):
        inputs = {"input": self.user_entry.value}
        response = self.chain.invoke(inputs)
        if self.memory:
            self.memory.save_context(inputs, {"output": response.content})

        self.messages.controls.append(ChatMessage("B", self.user_entry.value))
        await self.user_entry.clear()
        self.messages.controls.append(ChatMessage("P", response.content))
        await self.update_async()

    def build(self):
        return ft.Column(
            controls=[
                ft.Container(content=self.messages),
                ft.Container(content=self.user_entry),
            ],
        )
