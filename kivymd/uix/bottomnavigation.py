"""
Components/Bottom Navigation
============================

.. seealso::

   `Material Design spec, Bottom navigation <https://material.io/components/bottom-navigation>`_

.. rubric:: Bottom navigation bars allow movement between primary destinations in an app:

.. image:: https://github.com/HeaTTheatR/KivyMD-data/raw/master/gallery/kivymddoc/bottom-navigation.png
    :align: center

Usage
=====

.. code-block:: kv

    <Root>>:

        MDBottomNavigation:

            MDBottomNavigationItem:
                name: "screen 1"

                YourContent:

            MDBottomNavigationItem:
                name: "screen 2"

                YourContent:

            MDBottomNavigationItem:
                name: "screen 3"

                YourContent:

For ease of understanding, this code works like this:

.. code-block:: kv

    <Root>>:

        ScreenManager:

            Screen:
                name: "screen 1"

                YourContent:

            Screen:
                name: "screen 2"

                YourContent:

            Screen:
                name: "screen 3"

                YourContent:

Example
=======

.. code-block:: python

    from kivymd.app import MDApp
    from kivy.lang import Builder


    class Test(MDApp):

        def build(self):
            self.theme_cls.primary_palette = "Gray"
            return Builder.load_string(
                '''
    BoxLayout:
        orientation:'vertical'

        MDToolbar:
            title: 'Bottom navigation'
            md_bg_color: .2, .2, .2, 1
            specific_text_color: 1, 1, 1, 1

        MDBottomNavigation:
            panel_color: .2, .2, .2, 1

            MDBottomNavigationItem:
                name: 'screen 1'
                text: 'Python'
                icon: 'language-python'

                MDLabel:
                    text: 'Python'
                    halign: 'center'

            MDBottomNavigationItem:
                name: 'screen 2'
                text: 'C++'
                icon: 'language-cpp'

                MDLabel:
                    text: 'I programming of C++'
                    halign: 'center'

            MDBottomNavigationItem:
                name: 'screen 3'
                text: 'JS'
                icon: 'language-javascript'

                MDLabel:
                    text: 'JS'
                    halign: 'center'
    '''
            )


    Test().run()

.. image:: https://github.com/HeaTTheatR/KivyMD-data/raw/master/gallery/kivymddoc/bottom-navigation.gif
    :align: center

.. rubric:: :class:`~MDBottomNavigationItem` provides the following events for use:

.. code-block:: python

    __events__ = (
        "on_tab_touch_down",
        "on_tab_touch_move",
        "on_tab_touch_up",
        "on_tab_press",
        "on_tab_release",
    )

.. Note:: See :class:`~MDTab.__events__`

.. code-block:: kv

    Root:

        MDBottomNavigation:

            MDBottomNavigationItem:
                on_tab_touch_down: print("on_tab_touch_down")
                on_tab_touch_move: print("on_tab_touch_move")
                on_tab_touch_up: print("on_tab_touch_up")
                on_tab_press: print("on_tab_press")
                on_tab_release: print("on_tab_release")

                YourContent:


.. Note:: `See full example <https://github.com/HeaTTheatR/KivyMD/wiki/Components-Bottom-Navigation>`_
"""

__all__ = (
    "TabbedPanelBase",
    "MDBottomNavigationItem",
    "MDBottomNavigation",
    "MDTab",
)

from kivy.animation import Animation
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.lang import Builder

from kivy.metrics import dp, sp
from kivy.properties import (
    StringProperty,
    ListProperty,
    ObjectProperty,
    BoundedNumericProperty,
    NumericProperty,
    BooleanProperty,
)
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.screenmanager import Screen

from kivymd.uix.behaviors.backgroundcolorbehavior import (
    BackgroundColorBehavior,
    SpecificBackgroundColorBehavior,
)
from kivymd.uix.behaviors import RectangularElevationBehavior
from kivymd.uix.button import BaseFlatButton, BasePressedButton
from kivymd.theming import ThemableBehavior

Builder.load_string(
    """
#:import sm kivy.uix.screenmanager
#:import Window kivy.core.window.Window


<MDBottomNavigation>
    id: panel
    orientation: 'vertical'
    height: dp(56)  # Spec

    ScreenManager:
        id: tab_manager
        transition: sm.FadeTransition(duration=.2)
        current: root.current
        screens: root.tabs

    MDBottomNavigationBar:
        id: bottom_panel
        size_hint_y: None
        height: dp(56)
        md_bg_color: root.theme_cls.bg_dark if not root.panel_color else root.panel_color

        BoxLayout:
            id: tab_bar
            pos_hint: {'center_x': .5, 'center_y': .5}
            height: dp(56)
            size_hint: None, None


<MDBottomNavigationHeader>
    canvas:
        Color:
            rgba: root.panel_color
            #rgba: self.panel.theme_cls.bg_dark if not root.panel_color else root.panel_color
        Rectangle:
            size: self.size
            pos: self.pos

    width:
        root.panel.width / len(root.panel.ids.tab_manager.screens)\
        if len(root.panel.ids.tab_manager.screens) != 0 else root.panel.width
    padding: (dp(12), dp(12))
    on_press:
        self.tab.dispatch('on_tab_press')
    on_release: self.tab.dispatch('on_tab_release')
    on_touch_down: self.tab.dispatch('on_tab_touch_down',*args)
    on_touch_move: self.tab.dispatch('on_tab_touch_move',*args)
    on_touch_up: self.tab.dispatch('on_tab_touch_up',*args)

    FloatLayout:
        id: item_container

        MDIcon:
            id: _label_icon
            icon: root.tab.icon
            size_hint_x: None
            text_size: (None, root.height)
            height: self.texture_size[1]
            theme_text_color: 'Custom'
            text_color: root._current_color
            valign: 'middle'
            halign: 'center'
            opposite_colors: root.opposite_colors
            pos: [self.pos[0], self.pos[1]]
            font_size: dp(24)
            pos_hint: {'center_x': .5, 'center_y': .7}

        MDLabel:
            id: _label
            text: root.tab.text
            font_style: 'Button'
            size_hint_x: None
            text_size: (None, root.height)
            height: self.texture_size[1]
            theme_text_color: 'Custom'
            text_color: root._current_color
            valign: 'bottom'
            halign: 'center'
            opposite_colors: root.opposite_colors
            font_size: root._label_font_size
            pos_hint: {'center_x': .5, 'center_y': .6}


<MDTab>
    canvas:
        Color:
            rgba: root.theme_cls.bg_normal
        Rectangle:
            size: root.size
"""
)


class MDBottomNavigationHeader(BaseFlatButton, BasePressedButton):
    panel_color = ListProperty([1, 1, 1, 0])
    """Panel color of bottom navigation.

    :attr:`panel_color` is an :class:`~kivy.properties.ListProperty`
    and defaults to `[1, 1, 1, 0]`.
    """

    width = BoundedNumericProperty(
        0, min=80, max=168, errorhandler=lambda x: small_error_warn(x)
    )
    tab = ObjectProperty()
    """
    :attr:`tab` is an :class:`~MDBottomNavigationItem`
    and defaults to `Nome`.
    """

    panel = ObjectProperty()
    """
    :attr:`panel` is an :class:`~MDBottomNavigation`
    and defaults to `Nome`.
    """

    active = BooleanProperty(False)

    text = StringProperty()
    """
    :attr:`text` is an :class:`~MDTab.text`
    and defaults to `''`.
    """

    _label = ObjectProperty()
    _label_font_size = NumericProperty("12sp")
    _current_color = ListProperty([0.0, 0.0, 0.0, 0.0])
    _capitalized_text = StringProperty()

    def on_text(self, instance, value):
        self._capitalized_text = value.upper()

    def __init__(self, panel, height, tab):
        self.panel = panel
        self.height = height
        self.tab = tab
        super().__init__()
        self._current_color = self.theme_cls.disabled_hint_text_color
        self._label = self.ids._label
        self._label_font_size = sp(12)
        self.theme_cls.bind(
            primary_color=self._update_theme_color,
            disabled_hint_text_color=self._update_theme_style,
        )
        self.active = False

    def on_press(self):
        Animation(_label_font_size=sp(14), d=0.1).start(self)
        Animation(_current_color=self.theme_cls.primary_color, d=0.1).start(
            self
        )

    def _update_theme_color(self, instance, color):
        if self.active:
            self._current_color = self.theme_cls.primary_color

    def _update_theme_style(self, instance, color):
        if not self.active:
            self._current_color = self.theme_cls.disabled_hint_text_color


class MDTab(Screen, ThemableBehavior):
    """A tab is simply a screen with meta information
    that defines the content that goes in the tab header.
    """

    __events__ = (
        "on_tab_touch_down",
        "on_tab_touch_move",
        "on_tab_touch_up",
        "on_tab_press",
        "on_tab_release",
    )
    """Events provided."""

    text = StringProperty()
    """Tab header text.

    :attr:`text` is an :class:`~kivy.properties.StringProperty`
    and defaults to `''`.
    """

    icon = StringProperty("checkbox-blank-circle")
    """Tab header icon.

    :attr:`icon` is an :class:`~kivy.properties.StringProperty`
    and defaults to `'checkbox-blank-circle'`.
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.index = 0
        self.parent_widget = None
        self.register_event_type("on_tab_touch_down")
        self.register_event_type("on_tab_touch_move")
        self.register_event_type("on_tab_touch_up")
        self.register_event_type("on_tab_press")
        self.register_event_type("on_tab_release")

    def on_tab_touch_down(self, *args):
        pass

    def on_tab_touch_move(self, *args):
        pass

    def on_tab_touch_up(self, *args):
        pass

    def on_tab_press(self, *args):
        par = self.parent_widget
        if par.previous_tab is not self:
            if par.previous_tab.index > self.index:
                par.ids.tab_manager.transition.direction = "right"
            elif par.previous_tab.index < self.index:
                par.ids.tab_manager.transition.direction = "left"
            par.ids.tab_manager.current = self.name
            par.previous_tab = self

    def on_tab_release(self, *args):
        pass

    def __repr__(self):
        return f"<MDTab name='{self.name}', text='{self.text}'>"


class MDBottomNavigationItem(MDTab):
    header = ObjectProperty()
    """
    :attr:`header` is an :class:`~MDBottomNavigationHeader`
    and defaults to `Nome`.
    """

    def on_tab_press(self, *args):
        par = self.parent_widget
        par.ids.tab_manager.current = self.name
        if par.previous_tab is not self:
            Animation(_label_font_size=sp(12), d=0.1).start(
                par.previous_tab.header
            )
            Animation(
                _current_color=par.previous_tab.header.theme_cls.disabled_hint_text_color,
                d=0.1,
            ).start(par.previous_tab.header)
            par.previous_tab.header.active = False
            self.header.active = True
        par.previous_tab = self

    def on_leave(self, *args):
        pass


class TabbedPanelBase(
    ThemableBehavior, SpecificBackgroundColorBehavior, BoxLayout
):
    """A class that contains all variables a :class:`~kivy.properties.TabPannel`
    must have. It is here so I (zingballyhoo) don't get mad about
    the :class:`~kivy.properties.TabbedPannels` not being DRY.

    """

    current = StringProperty(None)
    """Current tab name.
    
    :attr:`current` is an :class:`~kivy.properties.StringProperty`
    and defaults to `None`.
    """

    previous_tab = ObjectProperty()
    """
    :attr:`previous_tab` is an :class:`~MDTab` and defaults to `None`.
    """

    panel_color = ListProperty()
    """Panel color of bottom navigation.

    :attr:`panel_color` is an :class:`~kivy.properties.ListProperty`
    and defaults to `[]`.
    """

    tabs = ListProperty()


class MDBottomNavigation(TabbedPanelBase):
    """A bottom navigation that is implemented by delegating
    all items to a ScreenManager."""

    first_widget = ObjectProperty()
    """
    :attr:`first_widget` is an :class:`~MDBottomNavigationItem`
    and defaults to `Nome`.
    """

    tab_header = ObjectProperty()
    """
    :attr:`tab_header` is an :class:`~MDBottomNavigationHeader`
    and defaults to `Nome`.
    """

    def on_panel_color(self, instance, value):
        self.tab_header.panel_color = value

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.previous_tab = None
        self.widget_index = 0
        self._refresh_tabs()

        Window.bind(on_resize=self.on_resize)
        Clock.schedule_once(lambda x: self.on_resize(), 2)

    def _refresh_tabs(self):
        """Refresh all tabs."""

        if not self.ids:
            return
        tab_bar = self.ids.tab_bar
        tab_bar.clear_widgets()
        tab_manager = self.ids.tab_manager
        for tab in tab_manager.screens:
            self.tab_header = MDBottomNavigationHeader(
                tab=tab, panel=self, height=tab_bar.height
            )
            tab.header = self.tab_header
            tab_bar.add_widget(self.tab_header)
            if tab is self.first_widget:
                self.tab_header._current_color = self.theme_cls.primary_color
                self.tab_header._label_font_size = sp(14)
                self.tab_header.active = True
            else:
                self.tab_header._label_font_size = sp(12)
        self.on_resize()

    def on_resize(self, instance=None, width=None, do_again=True):
        full_width = 0
        for tab in self.ids.tab_manager.screens:
            full_width += tab.header.width
        self.ids.tab_bar.width = full_width
        if do_again:
            Clock.schedule_once(lambda x: self.on_resize(do_again=False), 0.1)

    def add_widget(self, widget, **kwargs):
        """Add tabs to the screen or the layout.

        :param widget: The widget to add.
        """

        if isinstance(widget, MDBottomNavigationItem):
            self.widget_index += 1
            widget.index = self.widget_index
            widget.parent_widget = self
            tab_header = MDBottomNavigationHeader(
                tab=widget, panel=self, height=widget.height
            )
            self.ids.tab_bar.add_widget(tab_header)
            widget.header = tab_header
            self.ids.tab_manager.add_widget(widget)
            if self.widget_index == 1:
                self.previous_tab = widget
                tab_header._current_color = self.theme_cls.primary_color
                tab_header._label_font_size = sp(14)
                tab_header.active = True
                self.first_widget = widget
            else:
                tab_header._label_font_size = sp(12)
            self._refresh_tabs()
        else:
            super().add_widget(widget)

    def remove_widget(self, widget):
        """Remove tabs from the screen or the layout.

        :param widget: The widget to remove.
        """

        if isinstance(widget, MDBottomNavigationItem):
            self.ids.tab_manager.remove_widget(widget)
            self._refresh_tabs()
        else:
            super().remove_widget(widget)


class MDBottomNavigationBar(
    ThemableBehavior,
    BackgroundColorBehavior,
    FloatLayout,
    RectangularElevationBehavior,
):
    pass


class MDBottomNavigationErrorCache:
    last_size_warning = 0


def small_error_warn(x):
    if dp(x) <= dp(80):
        if MDBottomNavigationErrorCache.last_size_warning != x:
            MDBottomNavigationErrorCache.last_size_warning = x
            # Logger.warning(
            #    f"MDBottomNavigation: {x}dp is less than the minimum size "
            #    f"of 80dp for a MDBottomNavigationItem. "
            #    f"We must now expand to 168dp."
            # )
            # Did you come here to find out what the bug is?
            # The bug is that on startup, this function returning dp(80)
            # breaks the way it displays until you resize
            # I don't know why, this may or may not get fixed in the future
    return dp(168)
