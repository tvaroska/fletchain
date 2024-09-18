# requires: langchain google-cloud-aiplatform

from operator import itemgetter

import flet as ft

from fleetchain import FletChain

from langchain_core.runnables import RunnablePassthrough, RunnableLambda
from langchain_google_vertexai import ChatVertexAI
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.memory import ConversationBufferMemory

async def main(page: ft.Page):

    model = ChatVertexAI()
    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", "You are a helpful chatbot"),
            MessagesPlaceholder(variable_name="history"),
            ("human", "{input}"),
        ]
    )
    memory = ConversationBufferMemory(return_messages=True)
    chain = (
        RunnablePassthrough.assign(
            history=RunnableLambda(memory.load_memory_variables) | itemgetter("history")
        )
        | prompt
        | model
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


    page.add(FletChain(chain, memory))

ft.app(target= main) #, view = ft.AppView.WEB_BROWSER)
