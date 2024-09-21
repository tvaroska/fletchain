import uuid
import logging

import flet as ft
from langchain_core.runnables import Runnable
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.memory import BaseMemory

from fleetchain.user import UserEntry, ChatMessage

SESSION_ID = 'session_id'

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class FletChain(ft.Column):
    def __init__(self,
                 chain: Runnable,
                 memory: BaseMemory = None,
                 user_name: str = 'User',
                 user_color: str = ft.colors.WHITE,
                 user_bgcolor: str = ft.colors.BLACK,
                 ai_name: str = 'AI',
                 ai_color: str = ft.colors.BLACK,
                 ai_bgcolor: str = ft.colors.WHITE):
        super().__init__()
        self.chain = chain
        self.memory = memory
        self.memory_chain = isinstance(self.chain, RunnableWithMessageHistory)

        self.user_initials = self.get_initials(user_name)
        self.user_color = user_color
        self.user_bg_color = user_bgcolor
        self.ai_initials = self.get_initials(ai_name)
        self.ai_color = ai_color
        self.ai_bgcolor = ai_bgcolor

        self.user_entry = UserEntry(self.user_initials, self.send_message_click)

        self.progress_ring = ft.ProgressRing(width=20, height=20, value=1, visible=False)
        self.progress_text = ft.Text('')
        self.progress_row = ft.Row(controls=[self.progress_ring, self.progress_text], expand=True)

        self.messages = ft.ListView(expand=True, spacing=10, auto_scroll=True)
        self.history = ft.Container(
            content=self.messages,
            expand=True,
            # border=ft.border.all(1, ft.colors.OUTLINE),
            # border_radius=5,
            padding=10,
        )

        self.controls = [
            ft.Column([
                self.history,
                ft.Container(content=self.progress_row, height=30),
                ft.Container(content=self.user_entry, height=50),
            ], expand=True, spacing=10)
        ]

        self.expand = True

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
        self.progress_ring.visible = True
        self.progress_text.visible = True
        self.progress_text.value = 'Thinking...'
        self.progress_row.update()
        inputs = {'input': e.control.value}
        if self.memory_chain:
            response = self.chain.invoke(inputs, config={'configurable': {'session_id': self.get_id(self.page)}})
        else:
            response = self.chain.invoke(inputs)
        self.save_context(inputs, response.content)
        self.messages.controls.insert(0, ChatMessage(self.ai_initials, response.content))
        self.messages.controls.insert(0, ChatMessage(self.user_initials, self.user_entry.value))
        await self.user_entry.clear()
        self.progress_ring.visible = False
        self.progress_text.visible = False
        e.page.update()

    def save_context(self, inputs, outputs):
        if not self.memory_chain and self.memory:
            self.memory.save_context(inputs, {'output': outputs})

    def resize(self, e):
        self.height = e.page.height
        self.history.height = max(0, e.page.height - 100)  # Subtract height for progress row and user entry
        self.update()
