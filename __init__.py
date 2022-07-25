# ====================== BEGIN GPL LICENSE BLOCK ======================
#
#  This program is free software; you can redistribute it and/or
#  modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation, version 3.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software Foundation,
#  Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
#
# ======================= END GPL LICENSE BLOCK ========================


bl_info = {
    "name": "2 Battiti",
    "author": "Betti",
    "version": (1, 2, 4),
    "blender": (3, 0, 0),
    "location": "View3D > 2B",
    "description": """Addons for the 2B production""",
    "warning": "",
    "doc_url": "",
    "category": "production-specific",
}


import bpy
from importlib import reload

from . import timeline_operators
from . import twoB_ui
from . import update_comp_node_tree
from . import ExtraSettingComp
from . import make_anm_files_from_lay
from . import enable_render_nodes
from . import misc_operators
from . import bind_unbind

reload(timeline_operators)
reload(twoB_ui)
reload(update_comp_node_tree)
reload(ExtraSettingComp)
reload(make_anm_files_from_lay)
reload(enable_render_nodes)
reload(misc_operators)
reload(bind_unbind)

from .twoB_ui import *
from .update_comp_node_tree import *




def register():
    twoB_ui_register()
    


def unregister():
    twoB_ui_unregister()

if __name__ == "__main__":
    twoB_ui_register()