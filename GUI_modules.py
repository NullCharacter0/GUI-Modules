from collections.abc import Callable
from tkinter import BOTH, BOTTOM, LEFT, N, TOP, X, Y, Frame, Label, LabelFrame, Radiobutton, StringVar, ttk
import tkinter as tk
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg,NavigationToolbar2Tk   # type: ignore

from matplotlib import pyplot as plt

import pandas as pd
import numpy as np

import sys
sys.path.insert(1, "/home/will/Projects/CoinBaseADVtrade_Data")
from Data import Products, Wallet, Candles

def createCanvasFromMatPlt(fig ,master,pack_toolbar: bool = False):
    canvas = FigureCanvasTkAgg(fig, master=master)  # A tk.DrawingArea.
    canvas.draw()
    toolbar = NavigationToolbar2Tk(canvas, master, pack_toolbar=pack_toolbar)  # pack_toolbar=False will make it easier to use a layout manager later on.

    return canvas, toolbar


class FinancialModules:
    
    class PiePerformanceFrame(Frame):
        def __init__(self, master , ):
            size_of_groups=[1,1,1,1,1]
            labels = ["f" for i in size_of_groups]

            super().__init__(master)
                
            pieFig = plt.figure(num=99) 
            pieAxis = pieFig.add_subplot(1,1,1)
                    
            performanceFigure  = plt.figure(num=98,layout='compressed')
            performanceAxis = performanceFigure.add_subplot(1,1,1)
                        
            performanceFigure.set_size_inches(3.4,1, forward=True)
            pieFig.set_size_inches(3.4, 3, forward=True)
            
            pieAxis.pie(size_of_groups,radius=1.2,labels=labels,autopct='%1.1f%%',
                    pctdistance=1.25,wedgeprops=dict(width=.6), labeldistance=.6)
            pieAxis.text(-.55, -.05, 'Open positions', fontsize=10)


            canvas1, asd = createCanvasFromMatPlt(pieFig,self, )
            canvas2, asd = createCanvasFromMatPlt(performanceFigure,self, )
            canvas1.get_tk_widget().pack(side="top")
            canvas2.get_tk_widget().pack(side="top")
            
        
class PremadeMatplotFigures:
    
    twoPanelHeightRatios = [3, 1]
    threePanelHeightRatios = [1, 3, 1]
    fourPanelHeightRatios = [3, 5, 2,3]
    fivePanelHeightRatios = [3, 5, 2,3,2]
    height_profiles = [twoPanelHeightRatios, threePanelHeightRatios, fourPanelHeightRatios, fivePanelHeightRatios]
    
    volumeOverlay = False
    w_pad = .11
    h_pad = -0.81
    hspace = 0
    wspace = 0
    layout = "constrained"
    
    render_preformance_fig:bool = True
    
    def __init__(self,n=4,  w_pad=w_pad, h_pad=h_pad, hspace=hspace, wspace=wspace, layout=layout) -> None:
        
        fig, axes = plt.subplots(n, sharex=True, height_ratios=self.height_profiles[n-2], layout=layout)
        fig.get_layout_engine().set(w_pad=w_pad, h_pad=h_pad, hspace=hspace, wspace=wspace)  # type: ignore
        self.clean_axes(fig)
        self.fig, self.axes = fig,axes 


    
    @staticmethod
    def clean_axes(fig):
        for ax in fig.get_axes():
            ax.label_outer()
            ax.grid(True)

        
    @staticmethod
    def singlePanel( w_pad=w_pad, h_pad=h_pad, hspace=hspace, wspace=wspace, layout=layout):
        fig, ax = plt.subplots(1,layout=layout)
        fig.get_layout_engine().set(w_pad=w_pad, h_pad=h_pad, hspace=hspace, wspace=wspace)  # type: ignore
        PremadeMatplotFigures.clean_axes(fig)
        return fig,ax
    
    @staticmethod
    def doublePanel(height_ratios = twoPanelHeightRatios, w_pad=w_pad, h_pad=h_pad, hspace=hspace, wspace=wspace, layout=layout):
        fig, (main_ax, bot_ax,) = plt.subplots(2, sharex=True, height_ratios=height_ratios, layout=layout)
        fig.get_layout_engine().set(w_pad=w_pad, h_pad=h_pad, hspace=hspace, wspace=wspace)  # type: ignore
        PremadeMatplotFigures.clean_axes(fig)
        return fig,(main_ax, bot_ax,) 


    @staticmethod
    def triplePanel(height_ratios = threePanelHeightRatios, w_pad=w_pad, h_pad=h_pad, hspace=hspace, wspace=wspace, layout=layout):
        fig, (top_ax, main_ax,bot_ax ) = plt.subplots(3, sharex=True, height_ratios=height_ratios, layout=layout)
        fig.get_layout_engine().set(w_pad=w_pad, h_pad=h_pad, hspace=hspace, wspace=wspace)  # type: ignore
        PremadeMatplotFigures.clean_axes(fig)
        return fig,(top_ax, main_ax,bot_ax )

    @staticmethod
    def fourPanel(height_ratios = fourPanelHeightRatios, w_pad=w_pad, h_pad=h_pad, hspace=hspace, wspace=wspace, layout=layout):
        fig, (top_ax, main_ax,vol_ax, bot_ax ) = plt.subplots(4, sharex=True, height_ratios=height_ratios, layout=layout,)
        fig.get_layout_engine().set(w_pad=w_pad, h_pad=h_pad, hspace=hspace, wspace=wspace)  # type: ignore
        PremadeMatplotFigures.clean_axes(fig)
        return fig,(top_ax, main_ax,vol_ax,bot_ax )

    @staticmethod
    def threePanelVolumeOverlay(height_ratios = threePanelHeightRatios, w_pad=w_pad, h_pad=h_pad,hspace=hspace,wspace=wspace,layout=layout):
        fig, axes = plt.subplots(3, sharex=True, height_ratios=height_ratios, layout=layout)
        vol_ax = plt.twinx(axes[1])
        
        fig.get_layout_engine().set(w_pad=w_pad, h_pad=h_pad, hspace=hspace, wspace=wspace)  # type: ignore
        PremadeMatplotFigures.clean_axes(fig)
        return fig,axes




class Simple_IndicatorRadioButtons(LabelFrame):
    def __init__(self,master,name="SMA",height=50) -> None:
        super().__init__(master,text=name,height=height)

        self.int_var = tk.IntVar(value= 0 )
        

        # On/Off buttons for Indicator
        offButton = Radiobutton(self,variable=self.int_var,value=0)
        onButton = Radiobutton(self,variable=self.int_var,value=1)
        InvertedButton = Radiobutton(self,variable=self.int_var,value=2,state='disabled')
        # Labels for said buttons 
        offLabel = Label(self, text="Off")
        onLabel = Label(self, text="On")
        invertedLabel = Label(self, text="Inverted")
        
        # Packing 
        offLabel.pack(side=LEFT,expand=1,)
        offButton.pack(side=LEFT,expand=1,)
        onLabel.pack(side=LEFT,expand=1,)
        onButton.pack(side=LEFT,expand=1,)
        invertedLabel.pack(side=LEFT,expand=1,)
        InvertedButton.pack(side=LEFT,expand=1,)



class Complex_Indicator(LabelFrame):
    def __init__(self,master,name="MACD",height=50) -> None:
        super().__init__(master,text=name,height=height)

        self.int_var = tk.IntVar(value= 0 )
        
        # On/Off buttons for Indicator
        offButton = Radiobutton(self,variable=self.int_var,value=0)
        onButton = Radiobutton(self,variable=self.int_var,value=1)
        invertedButton = Radiobutton(self,variable=self.int_var,value=2)
        # Labels for said buttons 
        offLabel = Label(self, text="Off")
        onLabel = Label(self, text="On")
        invertedLabel = Label(self, text="Inverted")
        
        # Packing 
        offLabel.pack(side=LEFT,expand=1,)
        offButton.pack(side=LEFT,expand=1,)
        onLabel.pack(side=LEFT,expand=1,)
        onButton.pack(side=LEFT,expand=1,)
        invertedLabel.pack(side=LEFT,expand=1,)
        invertedButton.pack(side=LEFT,expand=1,)
        


class DoubleDataFrameViewer(tk.Frame):

    def on_opentree_click(self, event,):
        if self.closedTradesTree.selection():
            self.closedTradesTree.selection_remove(self.closedTradesTree.selection())                
    
    def on_closedtree_click(self, event,):
        if self.openTradesTree.selection():
            self.openTradesTree.selection_remove(self.openTradesTree.selection())                
    
    def __init__(self, master,openTrades,closedTrades ) -> None:
        super().__init__(master)
        self.openTrades_tv = SingleDataFrameViewer(self,openTrades)
        self.openTrades_tv.pack(side=TOP,fill="x",anchor=N,expand=1,)
        closedTrades_tv = SingleDataFrameViewer(self,closedTrades)
        closedTrades_tv.pack(side=TOP,fill="x",anchor=N,expand=1,)
        
        self.openTradesTree =  self.openTrades_tv.tree
        self.closedTradesTree =  closedTrades_tv.tree
        
        self.closedTradesTree.bind("<ButtonPress-1>", self.on_closedtree_click )
        self.openTradesTree.bind("<ButtonPress-1>", self.on_opentree_click )


class SingleDataFrameViewer(tk.Frame):
    

    def __init__(self, master,dataframe:pd.DataFrame) -> None:
        
        super().__init__(master)
        # Create a treeview widget
        self.tree = ttk.Treeview(self)
        
        filterColumnList = [i for i in dataframe.columns if i not in  ['Expected_return', 'Expected_loss', 'Trade_value(wager)', 'Trade_value(Success)', 'Trade_value(Failure)']]
        
        dataframe =  dataframe[filterColumnList]          
        
        # Define columns
        not_quantity = [i for i in dataframe.columns if i != "Quantity"]
        self.tree["columns"] = tuple(dataframe.columns)
        dataframe[not_quantity] = dataframe[not_quantity].round(2)
        dataframe["Quantity"] = dataframe.Quantity.round(4)
        

        
        # Format columns
        self.tree.column("#0", width=0, stretch=tk.NO)
        for col in dataframe.columns:
            self.tree.column(col, anchor=tk.W, width=60)
            self.tree.heading(col, text=col, anchor=tk.W)

        # Insert data into the treeview
        for i, row in dataframe.iterrows():
            self.tree.insert("", i, values=tuple(row),tags="unchecked") # type: ignore 

        # Add scrollbar
        scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        # Bind the click event to the function
        self.tree.bind("<ButtonRelease-1>", self.on_tree_release )

        # Pack the treeview and scrollbar
        scrollbar.pack(side=tk.RIGHT, fill=Y ,anchor="e",)
        self.tree.pack(side=tk.RIGHT,fill=BOTH,anchor="e",expand=1)


    def on_tree_release(self, event,):
        
        selection = self.tree.selection()
        if len(selection) > 0 :
            item = selection[0]
            values = self.tree.item(item, 'values')
            current_state = self.tree.item(item, 'tags')

            col_id = self.tree.identify_column(event.x)
            col = self.tree.column(col_id, 'id')
            print("Clicked Row Data:", values)
            print("Clicked Column:", col)
            print("Clicked State:", current_state)

            return col , values
        # Unhighlight the selected row
        # self.tree.selection_remove(self.tree.selection())


class SingleTreeViewer(tk.Frame):
    """
    Base For all dateframe based treeview widgets
    Requires: 
        pd.DataFrame
    
    """
        
    def test_floatORstr(self, x):
        try: 
            return float(x)
        except ValueError:
            return x 

    def treeview_sort_column(self, col, reverse):
        
        
        l = [(self.tree.set(self.test_floatORstr(k), col), k) for k in self.tree.get_children('')]
        l = [(self.test_floatORstr(tpl[0]), tpl[1]) for tpl in l]
        l.sort(reverse=reverse)

        # rearrange items in sorted positions
        for index, (val, k) in enumerate(l):
            self.tree.move(k, '', index)

        # reverse sort next time
        self.tree.heading(col, command=lambda: \
                self.treeview_sort_column( col, not reverse))

    def setup_heading(self, col):
        self.tree.heading(col, text=col, command=lambda _col=col: self.treeview_sort_column(col, False))

    def full_heading_setup(self):
        for col in self.tree["columns"]:
            self.setup_heading(col)
            
    def treeview_With_VSB(self):
        scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.tree.yview)
        # Add scrollbar
        self.tree.configure(yscrollcommand=scrollbar.set)
        # Bind the click event to the function
        self.tree.bind("<ButtonRelease-1>", self.on_tree_release )

        # Pack the treeview and scrollbar
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    
    def columnAndHeadingsetUp(self):
        if self.column_blackList != [] :
            filterColumnList = [i for i in self.dataframe.columns if i not in  self.column_blackList]
            self.dataframe =  self.dataframe[filterColumnList]
        self.tree["columns"] = tuple(self.dataframe.columns)
        self.full_heading_setup()
        pass

    def populate(self,):
        """
        Replace This with any future population methods you may have """
        idx= 0 
        for i, row in self.dataframe.iterrows():
            
            self.tree.insert("", idx, values=tuple(row),tags="unchecked") # type: ignore 
            idx += 1         

    
    def __init__(self, master,dataframe:pd.DataFrame, column_blackList: list = []) -> None:
        
        
        super().__init__(master)
        # Create a treeview widget
        self.tree = ttk.Treeview(self)
        self.column_blackList = column_blackList
        self.dataframe= dataframe
        
        self.columnAndHeadingsetUp()
        self.populate()
        self.treeview_With_VSB()

    def on_tree_release(self, event,):
        

        selection = self.tree.selection()
        if len(selection) > 0 :
            item = selection[0]
            values = self.tree.item(item, 'values')
            current_state = self.tree.item(item, 'tags')

            col_id = self.tree.identify_column(event.x)
            col = self.tree.column(col_id, 'id')
            print("Clicked Row Data:", values)
            print("Clicked Column:", col)
            print("Clicked State:", current_state)
            return col , values
        # Unhighlight the selected row
        # self.tree.selection_remove(self.tree.selection())


class TickerSelectionBox(ttk.Combobox):
    
    def __init__(self, master, ):
        self.product_variable = StringVar()
        super().__init__(master,textvariable=self.product_variable)
        self['values'] = Products().list_tradable_products()
        self.current(3) 

        self.bind('<<ComboboxSelected>>', self.selection_changed )

        
    def selection_changed(self, event):
        print(f"selected {self.get()}")
        pass
                            
                            
class GranularitySelectionBox(ttk.Combobox):
    
    def __init__(self, master):
        self.granularity_variable = StringVar()
        super().__init__(master,textvariable=self.granularity_variable)
        self['values'] = [
            "ONE_MINUTE",
            "FIVE_MINUTE",
            "FIFTEEN_MINUTE",
            "THIRTY_MINUTE",
            "ONE_HOUR",
            "TWO_HOUR",
            "SIX_HOUR",
            "ONE_DAY"
        ]
        self.current(0)

                            
class ScaleGranularitySelectionBox(ttk.Combobox):
    
    def __init__(self, master):
        self.scale_variable = StringVar()
        super().__init__(master,textvariable=self.scale_variable)
        self['values'] = [
            "Past Day",
            "Past Week",
            "Past Month",
            "Past Year",
            "Past (ALL)",
        ]
        
        self.current(0)

    def getScaledDataFrame(self):
        
        granularity = self.granularity_variable.get()
        scale = self.scale_variable.get()
        
class Indicator_configFrame(tk.Frame):
    def __init__(self,master) -> None:
        super().__init__(master)
                        
        # SMA_var = tk.IntVar(value= 0 )
        # EMA_var = tk.IntVar(value= 0 )
        # MACD_var = tk.IntVar(value= 0 )
        # ADX_var = tk.IntVar(value= 0 )
        # BB_var = tk.IntVar(value= 0 )
        
        
        # self.indicator_vars = {
        #     "SMA":SMA_var,
        #     "EMA":EMA_var,
        #     "MACD":MACD_var,
        #     "ADX":ADX_var,
        #     "BB":BB_var,
        #     # Add more indicators here
        # }
        default_topFrameSide = TOP
        SMA_frame = Simple_IndicatorRadioButtons(self,)
        SMA_frame.pack(side = TOP,expand=1,fill=X)
        
        EMA_frame = Simple_IndicatorRadioButtons(self,"EMA")
        EMA_frame.pack(side = TOP,expand=1,fill=X)


        MACD_frame = Complex_Indicator(self,"MACD")
        MACD_frame.pack(side = TOP,expand=1,fill=X)

        ADX_frame = Complex_Indicator(self,"ADX")
        ADX_frame.pack(side = TOP,expand=1,fill=X)

        BB_frame = Complex_Indicator(self,"Bollinger Bands")
        BB_frame.pack(side = TOP,expand=1,fill=X)
        
        SMA_var = SMA_frame.int_var
        EMA_var = EMA_frame.int_var
        MACD_var = MACD_frame.int_var
        ADX_var = ADX_frame.int_var
        BB_var = BB_frame.int_var
        
        
        
        self.indicator_vars = {
            "SMA":SMA_var,
            "EMA":EMA_var,
            "MACD":MACD_var,
            "ADX":ADX_var,
            "BB":BB_var,
            # Add more indicators here
        }
    
    pass

class SnappingCursor:
    """
    A cross-hair cursor that snaps to the data point of a line, which is
    closest to the *x* position of the cursor.

    For simplicity, this assumes that *x* values of the data are sorted.
    """
    def __init__(self, ax, line):
        self.ax = ax
        ymin, ymax = ax.get_ylim()

        # self.horizontal_line = ax.axhline(color='k',y=ymin, lw=0.8, ls='--')
        self.vertical_line = ax.axvline(color='k', lw=0.8, ls='--')
        self.x0, self.y0, = line.get_xbound()
        self._last_index = None
        # text location in axes coords
        self.text = ax.text(0.72, 0.9, '', transform=ax.transAxes)

    def set_cross_hair_visible(self, visible):
        need_redraw = self.vertical_line.get_visible() != visible
        # self.horizontal_line.set_visible(visible)
        self.vertical_line.set_visible(visible)
        self.text.set_visible(visible)
        return need_redraw

    def on_mouse_move(self, event):
        if not event.inaxes:
            self._last_index = None
            need_redraw = self.set_cross_hair_visible(False)
            if need_redraw:
                self.ax.figure.canvas.draw()
        else:
            self.set_cross_hair_visible(True)
            x, y = event.xdata, event.ydata
            # index = min(np.searchsorted(self.x0, x), len(self.x0) - 1)
            # if index == self._last_index:
            #     return  # still on the same data point. Nothing to do.
            # self._last_index = index
            # x = self.x0[index]
            # y = self.y0[index]
            # # update the line positions
            # self.horizontal_line.set_ydata([y])
            self.vertical_line.set_xdata(x)
            # self.set_message(self._mouse_event_to_message(event))
            self.text.set_text(self._mouse_event_to_message(event))
            self.ax.figure.canvas.draw()


    @staticmethod
    def _mouse_event_to_message(event):
        if event.inaxes and event.inaxes.get_navigate():
            try:
                s = event.inaxes.format_coord(event.xdata, event.ydata)
            except (ValueError, OverflowError):
                pass
            else:
                s = s.rstrip()
                artists = [a for a in event.inaxes._mouseover_set
                        if a.contains(event)[0] and a.get_visible()]
                if artists:
                    a = cbook._topmost_artist(artists)
                    if a is not event.inaxes.patch:
                        data = a.get_cursor_data(event)
                        if data is not None:
                            data_str = a.format_cursor_data(data).rstrip()
                            if data_str:
                                s = s + '\n' + data_str
                return s
        return ""

class DataFrameDetailing(LabelFrame):
    ticker : str
    current_Price : float
    pct_Change : float
    high  : float
    close : float
    low  : float
    bid  : float
    ask  : float
    market  : float
    volume_Base : float
    volume_Quote : float
    market_cap : float
    def __init__(self,master, text="Details:", **kwargs):
        
        
        top_row = 0
        mid_row = 1 
        bot_row = 2 
        first_column = 1 
        mid_column = 3 
        last_column = 5 

        super().__init__(master,text=text,**kwargs )

        self.pct_change_color_var = tk.StringVar(name="PCT Change",value= "green")
        self.pct_24hrchange_color_var = tk.StringVar(name="PCT24hr Change",value= "green")

        price_frame = Label(self, )
        liquiditymetrics = Label(self, )
        change_frame = Label(self, )
        change_frame.grid(row=1, column= 0,padx=5,pady=10, sticky = "NSEW",)
        Label(self, text=f"Symbol:").grid(row = 0, column=0 ,columnspan=5, sticky = "NSEW",)

        for key, value in kwargs.items():
            match key:
                case "vert" | "ver"| "v"| "vertical":
                    if value ==True:
                        price_frame.grid(row = 1, column= 0,padx=10, sticky = "NSEW",)
                        liquiditymetrics.grid(row = 2, column= 0,padx=10, sticky = "NSEW",)        
                case "horiz" | "hor"| "h"| "horizontal ":
                    if value ==True:
                    
                        price_frame.grid(row = 0, column= 1, sticky = "NSEW",)
                        liquiditymetrics.grid(row = 0, column= 2,padx=10, sticky = "NSEW",)  
                case _: 
                    price_frame.grid(row = 1, column= 1,padx=10, sticky = "NSEW",)
                    liquiditymetrics.grid(row = 1, column=2,padx=10, sticky = "NSEW",) 

        Label(change_frame, text="Current Price:").grid(row = 1, column= first_column, sticky = "NSEw")
        Label(change_frame, text= "PCT Change:").grid(row = 2, column= first_column, sticky = "NSEW")
        Label(change_frame, text= "PCT (24hr) Change:").grid(row = 2, column= first_column, sticky = "NSEW")

        Label(price_frame, text="Open :").grid(row = 0, column= 0, sticky = "NSew",)
        Label(price_frame, text="High :").grid(row = 0, column= 1, sticky = "NSEW")
        Label(price_frame, text="Low :").grid(row = 1, column= 1, sticky = "NSEW")
        Label(price_frame, text="Close:").grid(row = 1, column= 0, sticky = "NSEW")
        
        

        Label(liquiditymetrics, text="Bid :",foreground="Green").grid(row = 0, column= 0, sticky = "NSEW")
        Label(liquiditymetrics, text="Mid :",foreground="Black").grid(row = 1, column= 0, sticky = "NSEW")
        Label(liquiditymetrics, text="Ask :",foreground="Red").grid(row = 2, column= 0, sticky = "NSEW") # signifies the lowest price a #seller is willing to accept

        
        # Label(self, text="Market :").grid(row = mid_row, column= mid_column, sticky = "NS")
        # Label(self, text="Volume: (Base Asset)").grid(row = mid_row, column= mid_column, sticky = "NS")
        # Label(self, text="Volume: (Quote Asset)").grid(row = mid_row, column= mid_column, sticky = "NS")
        # Label(self, text="Market Cap:").grid(row = mid_row, column= mid_column, sticky = "NS")
        
        
        
class Framebased_modules:
    SingleDataFrameViewer = SingleDataFrameViewer
    DoubleDataFrameViewer = DoubleDataFrameViewer 
    SingleTreeViewer = SingleTreeViewer
    Indicator_configFrame = Indicator_configFrame 
    DataFrameDetailing = DataFrameDetailing 
    
    


