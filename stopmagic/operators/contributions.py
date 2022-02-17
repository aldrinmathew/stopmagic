from __future__ import annotations
from typing import Set
import webbrowser
import bpy


class AddonContributionPayPal(bpy.types.Operator):
    bl_idname = "stopmagic.contribution_paypal"
    bl_label = "Donate via Paypal"
    bl_description = "Support the addon by donating via PayPal"

    @classmethod
    def poll(cls, context: bpy.types.Context) -> bool:
        return True

    def execute(self, context: bpy.types.Context) -> Set[int] | Set[str]:
        webbrowser.open_new_tab("https://paypal.me/aldrinsartfactory")
        return {"FINISHED"}


class AddonContributionKofi(bpy.types.Operator):
    bl_idname = "stopmagic.contribution_kofi"
    bl_label = "Donate via Kofi"
    bl_description = "Support the addon by donating via ko-fi"

    @classmethod
    def poll(cls, context: bpy.types.Context) -> bool:
        return True

    def execute(self, context: bpy.types.Context) -> Set[int] | Set[str]:
        webbrowser.open_new_tab("https://ko-fi.com/aldrinmathew")
        return {"FINISHED"}


class AddonContributionGithub(bpy.types.Operator):
    bl_idname = "stopmagic.contribution_github"
    bl_label = "Contribute via Github"
    bl_description = "Support the addon by making contributions to Github"

    @classmethod
    def poll(cls, context: bpy.types.Context) -> bool:
        return True

    def execute(self, context: bpy.types.Context) -> Set[int] | Set[str]:
        webbrowser.open_new_tab("https://github.com/aldrinsartfactory/stopmagic")
        return {"FINISHED"}


def register() -> None:
    bpy.utils.register_class(AddonContributionPayPal)
    bpy.utils.register_class(AddonContributionKofi)
    bpy.utils.register_class(AddonContributionGithub)


def unregister() -> None:
    bpy.utils.unregister_class(AddonContributionPayPal)
    bpy.utils.unregister_class(AddonContributionKofi)
    bpy.utils.unregister_class(AddonContributionGithub)
