"""For making rig controls.

Reference:
https://app.pluralsight.com/library/courses/procedural-rigging-python-maya-2283
"""

import maya.cmds as cmds


class Control:
    """For building rig controls."""

    def __init__(
                self,
                prefix="new",
                scale=1.0,
                translateTo="",
                rotateTo="",
                parent="",
                lockChannels=['s', 'v']
                ):
        """For building rig controls.

        Args:
            prefix (str): Name prefex for generated objects and groups
            scale (float): Scale control to control its size
            rotateTo (str): Name of object to match control rotation to
            parent (str): Name of parent object
            lockChannels (list): List of characters indicating which channels
                of control to lock.
                Options:
                    t = translation
                    s = scale
                    r = rotation
                    v = visibility
        """
        ctrlObject, ctrlOffset = self.__makeCircleCtrl(prefix)

        if cmds.objExists(translateTo):
            self.__snapTrans(translateTo, ctrlOffset)

        if cmds.objExists(rotateTo):
            self.__snapOrient(rotateTo, ctrlOffset)

        if cmds.objExists(parent):
            cmds.parent(ctrlOffset, parent)

        self.__lockByChannel(ctrlObject, lockChannels)
        self.__lockByChannel(ctrlOffset, ['t', 'r', 's', 'v'])

    def __makeCircleCtrl(self, prefix):
        ctrlObject = cmds.circle(name=prefix + "_ctl", ch=False)[0]
        ctrlOffset = cmds.group(name=prefix + "_grp", empty=1)
        cmds.parent(ctrlObject, ctrlOffset)

        return (ctrlObject, ctrlOffset)

    def __snapTrans(self, target, subject):
        cmds.delete(cmds.pointConstraint(target, subject))

    def __snapOrient(self, target, subject):
        cmds.delete(cmds.pointConstraint(target, subject))

    def __lockByChannel(self, subject, lockChannels):

        # convert t, r, s to individual channels for each axis
        singleChannels = []

        for channel in lockChannels:
            if channel in ['t', 'r', 's']:
                singleChannels.append(channel + 'x')
                singleChannels.append(channel + 'y')
                singleChannels.append(channel + 'z')
            else:
                singleChannels.append(channel)

        # Lock channels
        for channel in singleChannels:
            cmds.setAttr(subject + "." + channel, lock=True)
