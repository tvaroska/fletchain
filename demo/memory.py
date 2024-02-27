# requires: langchain google-cloud-aiplatform

import flet as ft

from fleetchain import FletChain

from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_google_vertexai  import ChatVertexAI
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder

async def main(page: ft.Page):

    model = ChatVertexAI()
    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", "You are a helpful chatbot"),
            MessagesPlaceholder(variable_name="history"),
            ("human", "{input}"),
        ]
    )
    chain = prompt | model

    store = {}


    def get_session_history(session_id: str) -> BaseChatMessageHistory:
        if session_id not in store:
            store[session_id] = ChatMessageHistory()
        return store[session_id]


    memory_chain = RunnableWithMessageHistory(
        chain,
        get_session_history,
        input_messages_key="input",
        history_messages_key="history",
    )    

    appbar_items = [
        ft.PopupMenuItem(text="Login"),
        ft.PopupMenuItem(),  # divider
        ft.PopupMenuItem(text="Settings")
    ]
    appbar = ft.AppBar(
        leading=ft.Icon(ft.icons.GRID_GOLDENRATIO_ROUNDED),
        leading_width=40,
        title=ft.Text("FletChain", text_align="start"),
        center_title=False,
        bgcolor=ft.colors.SURFACE_VARIANT,
        actions=[
            ft.Container(
                content=ft.PopupMenuButton(
                    items=appbar_items
                ),
                margin=ft.margin.only(left=50, right=25)
            )
        ],
    )
    page.appbar = appbar
    page.vertical_alignment = ft.MainAxisAlignment.END

    await page.add_async(FletChain(memory_chain))

ft.app(target= main, view = ft.AppView.WEB_BROWSER)
