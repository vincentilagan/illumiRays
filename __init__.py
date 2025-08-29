bl_info = {
    "name": "IllumiRays",
    "author": "Vincent Ilagan",
    "version": (1, 0, 0),
    "blender": (3, 6, 0),
    "location": "3D View > Sidebar > IllumiRays",
    "description": "Quick render style & lighting controller",
    "warning": "",
    "doc_url": "",
    "category": "Render",
}

from . import illumiRays

def register():
    illumiRays.register()

def unregister():
    illumiRays.unregister()
