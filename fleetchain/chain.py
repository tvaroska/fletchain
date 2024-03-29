import uuid

import flet as ft
from langchain_core.runnables import Runnable
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.memory import BaseMemory

from fleetchain.user import UserEntry, ChatMessage

SESSION_ID = 'session'

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

        if isinstance(self.chain, RunnableWithMessageHistory):
            self.memory_chain = True
        else:
            self.memory_chain = False


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

    def get_id(self, page):
        if page.session.contains_key(SESSION_ID):
            return page.session.get(SESSION_ID)
        else:
            session_id = str(uuid.uuid4())
            page.session.set(SESSION_ID, session_id)
            return session_id

    async def send_message_click(self, e):
        inputs = {"input": self.user_entry.value}
        if self.memory_chain:
            response = self.chain.invoke(inputs, config={"configurable": {"session_id": self.get_id(self.page)}})
        else:
            response = self.chain.invoke(inputs)
        self.save_context(inputs, response.content)

        self.messages.controls.append(ChatMessage(self.user_initials, self.user_entry.value))
        await self.user_entry.clear()
        self.messages.controls.append(ChatMessage(self.ai_initials, response.content))
        await self.update_async()

    def save_context(self, inputs, outputs):
        if not self.memory_chain and self.memory:
            self.memory.save_context(inputs, {"output": outputs})

    def build(self):
        return ft.Column(
            controls=[
                ft.Container(content=self.messages),
                ft.Container(content=self.user_entry),
            ],
        )
