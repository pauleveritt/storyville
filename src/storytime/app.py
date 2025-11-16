"""Starlette app."""


import asyncio
from concurrent.futures import ProcessPoolExecutor
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from pathlib import Path
from typing import TYPE_CHECKING, Callable

import watchfiles
from starlette.applications import Starlette
from starlette.responses import PlainTextResponse
from starlette.routing import Mount, WebSocketRoute, Route
from starlette.staticfiles import StaticFiles
from starlette.websockets import WebSocket

from storytime import Site

if TYPE_CHECKING:
    from starlette.types import Receive, Scope, Send


def process_changes():
    print("\n\n ### Callback")


class RebuildServer:
    def __init__(
        self,
        paths: list[Path],
        # ignore_filter: IgnoreFilter,
        change_callback: Callable[[], None],
    ) -> None:
        self.paths = paths
        # self.ignore = ignore_filter
        self.change_callback = change_callback
        self.flag = asyncio.Event()
        self.should_exit = asyncio.Event()

    @asynccontextmanager
    async def lifespan(self, _app) -> AsyncIterator[None]:
        task = asyncio.create_task(self.main())
        yield
        self.should_exit.set()
        await task

    async def main(self) -> None:
        tasks = (
            asyncio.create_task(self.watch()),
            asyncio.create_task(self.should_exit.wait()),
        )
        done, pending = await asyncio.wait(tasks, return_when=asyncio.FIRST_COMPLETED)
        [task.cancel() for task in pending]
        [task.result() for task in done]

    async def watch(self) -> None:
        async for _changes in watchfiles.awatch(
            *self.paths,
            # watch_filter=lambda _, path: not self.ignore(path),
        ):
            with ProcessPoolExecutor() as pool:
                fut = pool.submit(self.change_callback)
                await asyncio.wrap_future(fut)
            self.flag.set()

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        assert scope["type"] == "websocket"
        ws = WebSocket(scope, receive, send)
        await ws.accept()

        tasks = (
            asyncio.create_task(self.watch_reloads(ws)),
            asyncio.create_task(self.wait_client_disconnect(ws)),
        )
        done, pending = await asyncio.wait(tasks, return_when=asyncio.FIRST_COMPLETED)
        [task.cancel() for task in pending]
        [task.result() for task in done]

    async def watch_reloads(self, ws: WebSocket) -> None:
        while True:
            await self.flag.wait()
            self.flag.clear()
            await ws.send_text("refresh")

    @staticmethod
    async def wait_client_disconnect(ws: WebSocket) -> None:
        async for _ in ws.iter_text():
            pass


async def render_node(request):
    full_path = Path(request.path_params.get("full_path"))
    return PlainTextResponse(f"Full path: {full_path}")


def create_app(site: Site) -> Starlette:
    watcher = RebuildServer([Path("/tmp")], change_callback=process_changes)

    return Starlette(
        debug=True,
        routes=[
            Route("/stories/{full_path:path}", endpoint=render_node),
            WebSocketRoute("/websocket-reload", watcher, name="reload"),
            Mount("/static", app=StaticFiles(directory=site.static_dir), name="static"),
        ],
        lifespan=watcher.lifespan,
    )
