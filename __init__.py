from .openpose_editor_nodes import LoadOpenposeJSONNode
from .openpose_editor import DIST_DIR, update_app

WEB_DIRECTORY = "js"

NODE_CLASS_MAPPINGS = {
    "huchenlei.LoadOpenposeJSON": LoadOpenposeJSONNode,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "huchenlei.LoadOpenposeJSON": "Load Openpose JSON",
}

__all__ = ["NODE_CLASS_MAPPINGS", "NODE_DISPLAY_NAME_MAPPINGS"]

update_app()
from aiohttp import web
from server import PromptServer

PromptServer.instance.app.add_routes([web.static("/openpose_editor", DIST_DIR)])