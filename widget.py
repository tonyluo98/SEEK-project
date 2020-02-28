import requests
import json
import string
import getpass
import sys
import io
import ipywidgets as widgets
import functools as ft
# Importing the libraries we need to format the data in a more readable way.
import pandas as pd
from pandas.io.json import json_normalize

from multiprocessing import Pool
from IPython.display import display
from IPython.display import HTML
from IPython.display import clear_output

from json_methods import JSON_methods

class Widget():
    def __init__(self):
        self.layout0 = {'width': '400px'}
        self.layout1 = {'width': '750px'}
        self.layout2 = {'width': '850px'}
        self.layout3 = {'width': '925px'}


        self.button_layout0 = {'width': '455px'}
        self.button_layout1 = {'width': '635px'}
        self.button_layout2 = {'width': '800px'}

        self.toggle_button_layout0 = {'width': '400px'}
        self.toggle_button_layout1 = {'width': '600px'}
        self.toggle_button_layout2 = {'width': '900px'}

        self.toggle_button_style = {'description_width': '180px'}
        self.small_toggle_button_style = {'description_width': '110px'}

    def check_list_content(self,list):
        temp_list =list
        default_value =[]
        number_of_rows = 1
        if list:
            default_value.append(x[0])
            if len(list_of_names) > 4:
                number_of_rows = 4
            else :
                number_of_rows = len(list_of_names)+1
    def dropdown_widget(self,options,value,desc):

        if value == 'default' and len(value) > 0:
            val = options[0]
        else :
            val = value
        widget = widgets.Dropdown(
            options = options,
            value = val,
            description = desc,
        )
        return widget

    def bounded_int_text_widget(self,val,desc,boolean,min,max):
        widget = widgets.BoundedIntText(
            value=val,
            description=desc,
            disabled=boolean,
            min=min,
            max = max
        )
        return widget

    def combobox(self,ph,options,desc,bool_option,bool_active):
        widget = widgets.Combobox(
            # value='',
            placeholder=ph,
            options=options,
            description=desc,
            ensure_option=bool_option,
            disabled=bool_active
        )
        return widget

    def toggle_button(self,desc,val):

        widget = widgets.ToggleButtons(
            options=['True', 'False'],
            description=desc,
            disabled=False,
            button_style='', # 'success', 'info', 'warning', 'danger' or ''
            tooltips=['', ''],
            style =self.toggle_button_style,
            layout=self.toggle_button_layout1,
            value = val

        #     icons=['check'] * 3
        )
        return widget

    def toggle_with_options_button(self,desc,val,options):

        widget = widgets.ToggleButtons(
            options=options,
            description=desc,
            disabled=False,
            button_style='', # 'success', 'info', 'warning', 'danger' or ''
            tooltips=['', ''],
            style =self.small_toggle_button_style,
            layout=self.toggle_button_layout2,
            value = val

        #     icons=['check'] * 3
        )
        return widget

    def text_widget(self,val,desc,increased_width = False):
        if increased_width == 0:
            layout = self.layout0
        elif increased_width == 1:
            layout = self.layout1
        else :
            layout = self.layout2
        widget = widgets.Text(
            value=val,
            placeholder='',
            description=desc,
            disabled=False,
            layout=layout

        )
        return widget

    def text_area_widget(self,val,desc,increased_width=1):
        if increased_width == 0:
            layout = self.layout0
        elif increased_width == 1:
            layout = self.layout1
        else :
            layout = self.layout2
        widget = widgets.Textarea(
            value=val,
            placeholder='',
            description=desc,
            disabled=False,
            layout=layout
        )
        return widget

    def button(self,desc):
        widget = widgets.Button(
            description=desc,
            disabled=False,
            button_style='', # 'success', 'info', 'warning', 'danger' or ''
            tooltip='Click me',
            # style =style_right,
            # layout=layout_right,
            # icon='check'
        )
        return widget

    def button_optional(self,desc,value):

        if len(value) == 0 :
            boolean = True
        else:
            boolean = False
        widget = widgets.Button(
            description=desc,
            disabled=boolean,
            button_style='', # 'success', 'info', 'warning', 'danger' or ''
            tooltip='Click me',
        )
        return widget

    def accordion(self,list,increased_width =1):
        if increased_width == 0:
            layout = self.layout0
        elif increased_width == 1:
            layout = self.layout1
        elif increased_width == 2:
            layout = self.layout2
        else :
            layout = self.layout3
        children = list

        widget = widgets.Accordion(
            children=children,
            layout = layout
            )
        return widget

    def tab(self,children,tab_names):
        widget = widgets.Tab()
        widget.children = children
        for index in range(len(tab_names)):
            widget.set_title(index, tab_names[index])
        return widget

    def select_multiple(self,increased_width,options,default_val,rows,desc):
        if increased_width == 0:
            layout = self.layout0
        elif increased_width == 1:
            layout = self.layout1
        elif increased_width == 2:
            layout = self.layout2
        else :
            layout = self.layout3
        widget =  widgets.SelectMultiple(
            layout = layout,
            options= options,
            value=default_val,
            rows=rows,
            description=desc,
            disabled=False
        )
        return widget
