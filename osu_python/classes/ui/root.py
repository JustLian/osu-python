import typing as t
import pygame as pg


class AnimationManager:
    def __init__(self, width, height, x, y):
        self.animation = {
            'size': {
                'goal': (width, height)
            }
        }


class UiElement:
    def __init__(self, enabled: bool = True, shown: bool = True):
        """
        Base class for any UI elements.

        Parameters
        ----------
        enabled : bool
            Should object be clickable? (if True, UiElement.click method is required)
        shown : bool
            Should object be rendered? (this param can be changed using UiElement.toggle_show method)
        """

        assert hasattr(self, 'draw'), "Class {} doesn't have `draw` method (required)".format(self.__class__)
        if not hasattr(self, 'is_colliding'):
            self.is_colliding = lambda *args: False

        self.enabled = enabled

        if enabled:
            assert hasattr(self, 'click'), "Class {} doesn't have `click` method".format(self.__class__)

        self.shown = shown
        self.hover = False
    
    def toggle_show(self, force_value: bool = None) -> bool:
        """
        Toggle/set visibility of object.

        Parameters
        ----------
        force_value : bool
            Sets visibility of object to passed value
            If None, toggles visibility
        
        Returns
        -------
        True if visibility changed, False otherwise
        """

        if force_value is None:
            self.shown = not self.shown
            return True
        
        r = self.shown != force_value
        self.shown = force_value

        return r
    
    def toggle_click(self, force_value: bool = None) -> bool:
        """
        Toggle/set is object should be enabled.

        Parameters
        ----------
        force_value : bool
            Enables object if passed arg is True, disables otherwise
        
        Returns
        -------
        True if object enabled/disabled, False if nothing changed
        """

        if force_value is None:
            self.enabled = not self.enabled
            return True
        
        r = self.enabled != force_value
        self.enabled = force_value

        return r

    def toggle_hover(self):
            """
            Toggles hover effects. Don't call this method manually
            """

            self.hover = not self.hover


class UiManager:
    def __init__(
        self, objects: t.Sequence[UiElement]
    ):
        """
        Class for managing UIs
        This class will handle drawing objects, calling
        special methods and other. Just run `UiManager.update`
        and `UiManager.draw` every frame

        Parameters
        ----------
        objects : t.Sequence[UiElements]
            Objects that should be drawn on screen
        """

        self.objects = objects
    
    def draw(self, screen: pg.Surface):
        """Draws all UI elements os `screen`"""

        for obj in self.objects:
            if obj.shown:
                obj.draw(screen)
        

    def update(self, events):
        """Updates UI"""

        # detecting collision and changing obj.hover state
        mouse = pg.mouse.get_pos()
        hovering_object = None
        for obj in self.objects:
            hovering = obj.is_colliding(mouse)
            if (not obj.hover and hovering) or (obj.hover and not hovering):
                obj.toggle_hover()
                if hovering and obj.enabled:
                    hovering_object = obj
        
        for event in events:
            if event.type == pg.MOUSEBUTTONUP and hovering_object != None:
                hovering_object.click()