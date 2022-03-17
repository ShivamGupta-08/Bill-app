from turtle import width
from fpdf import FPDF
from datetime import date
import tkinter 
from tkinter.constants import ANCHOR, NW
import PIL.Image,PIL.ImageTk
import cv2
from functools import partial
import threading
import imutils
title = 'Swarnrekha Infosolutions'
SET_WIDTH = 1366
SET_HEIGHT=768
class PDF(FPDF):
    def __init__(self, **kwargs):
        super(PDF,self).__init__(**kwargs)
        
        self.add_font('Amatic','',
                    r'G:\Python Projects\print\AmaticSC-Regular.ttf',
                    uni=True)
        self.add_font('Amatic','B',
                    r'G:\Python Projects\print\AmaticSC-Bold.ttf',
                    uni=True)
        self.add_font('Blackadder','',
                    r'C:\Windows\Fonts\ITCBLKAD.TTF',
                    uni=True)

    def header(self):
        
        self.set_font('Amatic','B',15)
        title_w = self.get_string_width(title)+6
        doc_w = self.w
        self.set_x((doc_w - title_w)/2)
        self.set_draw_color(0,80,180) #border
        self.set_fill_color(230,230,0) #background
        self.set_text_color(220,50,50) #text
        self.set_line_width(1) #border thickness
        self.cell(title_w,10,title, border=True, ln=True, align='C',fill=True)
        self.ln(10)
    
    def footer(self):
        self.set_y(-15)
        self.set_font('Amatic','',8)
        self.set_text_color(169,169,169)
        self.cell(0, 10, f'Page: {self.page_no()}/nb', 0, 0, 'C')

    def chapter_title(self,ch_num,ch_title,link):
        self.set_link(link)
        self.set_font('helvetica','',12)
        self.set_fill_color(200,220,255)
        chapter_title =f'Chapter {ch_num} : {ch_title}'
        self.cell(0,5,chapter_title,ln=True, fill=True)

    def chapter_body(self,name):
        with open (name,'rb') as fh:
            txt= fh.read().decode('latin-1')
        self.set_font('times','',12)
        self.multi_cell(0,5,txt)
        self.ln()
        self.set_font('times','I',12)
        self.cell(0,5,'END OF CHAPTER')

    def print_chapter(self,ch_num,ch_title,name,link):
        self.add_page()
        self.chapter_title(ch_num,ch_title,link)
        self.chapter_body(name)

def create_table(table_data, title='', data_size = 10, title_size=12, align_data='L', align_header='L', cell_width='even', x_start='x_default',emphasize_data=[], emphasize_style=None, emphasize_color=(0,0,0)):
    """
    table_data: 
                list of lists with first element being list of headers
    title: 
                (Optional) title of table (optional)
    data_size: 
                the font size of table data
    title_size: 
                the font size fo the title of the table
    align_data: 
                align table data
                L = left align
                C = center align
                R = right align
    align_header: 
                align table data
                L = left align
                C = center align
                R = right align
    cell_width: 
                even: evenly distribute cell/column width
                uneven: base cell size on lenght of cell/column items
                int: int value for width of each cell/column
                list of ints: list equal to number of columns with the widht of each cell / column
    x_start: 
                where the left edge of table should start
    emphasize_data:  
                which data elements are to be emphasized - pass as list 
                emphasize_style: the font style you want emphaized data to take
                emphasize_color: emphasize color (if other than black) 
    
    """
    default_style = pdf.font_style
    if emphasize_style == None:
        emphasize_style = default_style
    # default_font = pdf.font_family
    # default_size = pdf.font_size_pt
    # default_style = pdf.font_style
    # default_color = pdf.color # This does not work

    # Get Width of Columns
    def get_col_widths():
        col_width = cell_width
        if col_width == 'even':
            col_width = pdf.epw / len(data[0]) - 1  # distribute content evenly   # epw = effective page width (width of page not including margins)
        elif col_width == 'uneven':
            col_widths = []

            # searching through columns for largest sized cell (not rows but cols)
            for col in range(len(table_data[0])): # for every row
                longest = 0 
                for row in range(len(table_data)):
                    cell_value = str(table_data[row][col])
                    value_length = pdf.get_string_width(cell_value)
                    if value_length > longest:
                        longest = value_length
                col_widths.append(longest + 4) # add 4 for padding
            col_width = col_widths



                    ### compare columns 

        elif isinstance(cell_width, list):
            col_width = cell_width  # TODO: convert all items in list to int        
        else:
            # TODO: Add try catch
            col_width = int(col_width)
        return col_width

    # Convert dict to lol
    # Why? because i built it with lol first and added dict func after
    # Is there performance differences?
    if isinstance(table_data, dict):
        header = [key for key in table_data]
        data = []
        for key in table_data:
            value = table_data[key]
            data.append(value)
        # need to zip so data is in correct format (first, second, third --> not first, first, first)
        data = [list(a) for a in zip(*data)]

    else:
        header = table_data[0]
        data = table_data[1:]

    line_height = pdf.font_size * 2.5

    col_width = get_col_widths()
    pdf.set_font(size=title_size)

    # Get starting position of x
    # Determin width of table to get x starting point for centred table
    if x_start == 'C':
        table_width = 0
        if isinstance(col_width, list):
            for width in col_width:
                table_width += width
        else: # need to multiply cell width by number of cells to get table width 
            table_width = col_width * len(table_data[0])
        # Get x start by subtracting table width from pdf width and divide by 2 (margins)
        margin_width = pdf.w - table_width
        # TODO: Check if table_width is larger than pdf width

        center_table = margin_width / 2 # only want width of left margin not both
        x_start = center_table
        pdf.set_x(x_start)
    elif isinstance(x_start, int):
        pdf.set_x(x_start)
    elif x_start == 'x_default':
        x_start = pdf.set_x(pdf.l_margin)


    # TABLE CREATION #

    # add title
    if title != '':
        pdf.multi_cell(0, line_height, title, border=0, align='j', ln=3, max_line_height=pdf.font_size)
        pdf.ln(line_height) # move cursor back to the left margin

    pdf.set_font(size=data_size)
    # add header
    y1 = pdf.get_y()
    if x_start:
        x_left = x_start
    else:
        x_left = pdf.get_x()
    x_right = pdf.epw + x_left
    if  not isinstance(col_width, list):
        if x_start:
            pdf.set_x(x_start)
        for datum in header:
            pdf.multi_cell(col_width, line_height, datum, border=0, align=align_header, ln=3, max_line_height=pdf.font_size)
            x_right = pdf.get_x()
        pdf.ln(line_height) # move cursor back to the left margin
        y2 = pdf.get_y()
        pdf.line(x_left,y1,x_right,y1)
        pdf.line(x_left,y2,x_right,y2)

        for row in data:
            if x_start: # not sure if I need this
                pdf.set_x(x_start)
            for datum in row:
                if datum in emphasize_data:
                    pdf.set_text_color(*emphasize_color)
                    pdf.set_font(style=emphasize_style)
                    pdf.multi_cell(col_width, line_height, datum, border=0, align=align_data, ln=3, max_line_height=pdf.font_size)
                    pdf.set_text_color(0,0,0)
                    pdf.set_font(style=default_style)
                else:
                    pdf.multi_cell(col_width, line_height, datum, border=0, align=align_data, ln=3, max_line_height=pdf.font_size) # ln = 3 - move cursor to right with same vertical offset # this uses an object named pdf
            pdf.ln(line_height) # move cursor back to the left margin
    
    else:
        if x_start:
            pdf.set_x(x_start)
        for i in range(len(header)):
            datum = header[i]
            pdf.multi_cell(col_width[i], line_height, datum, border=0, align=align_header, ln=3, max_line_height=pdf.font_size)
            x_right = pdf.get_x()
        pdf.ln(line_height) # move cursor back to the left margin
        y2 = pdf.get_y()
        pdf.line(x_left,y1,x_right,y1)
        pdf.line(x_left,y2,x_right,y2)


        for i in range(len(data)):
            if x_start:
                pdf.set_x(x_start)
            row = data[i]
            for i in range(len(row)):
                datum = row[i]
                if not isinstance(datum, str):
                    datum = str(datum)
                adjusted_col_width = col_width[i]
                if datum in emphasize_data:
                    pdf.set_text_color(*emphasize_color)
                    pdf.set_font(style=emphasize_style)
                    pdf.multi_cell(adjusted_col_width, line_height, datum, border=0, align=align_data, ln=3, max_line_height=pdf.font_size)
                    pdf.set_text_color(0,0,0)
                    pdf.set_font(style=default_style)
                else:
                    pdf.multi_cell(adjusted_col_width, line_height, datum, border=0, align=align_data, ln=3, max_line_height=pdf.font_size) # ln = 3 - move cursor to right with same vertical offset # this uses an object named pdf
            pdf.ln(line_height) # move cursor back to the left margin
    y3 = pdf.get_y()
    pdf.line(x_left,y3,x_right,y3)

def no_done_button():
    num_of_items=entry2.get()
    
    num_of_items=int(entry2.get())
    print(type(num_of_items))
    num_of_items

    label_position_x = 100
    label_position_y = 200
    entry3_position_x = 250
    entry3_position_y = 200
    for i in range(1, int(num_of_items) + 1):
        
        label3 = tkinter.Label(window, text=f'Enter the name of product ')
        label3.config(font=('helvetica', 10))
        canvas.create_window(label_position_x, label_position_y, window=label3)
        
        entry3 = tkinter.Entry (window) 
        canvas.create_window(entry3_position_x, entry3_position_y, window=entry3,)
        label_position_y +=50
        entry3_position_y +=50
        # item_name = input(f'Enter name of product {i}\n')
        item_name = entry3.get()
        item_list.append(item_name)

# def quantity_done_button():
#     num_of_items=entry3.get()
#     int(num_of_items)
#     #--------------Qty Products--------------------
#     for i in range(1, int(num_of_items) + 1):
#         product_serial = i-1
#         label4 = tkinter.Label(window, text=f'Enter quantity of \'{item_list[product_serial]}\' \n')
#         label4.config(font=('helvetica', 10))
#         canvas.create_window(100, 250, window=label4)

#         entry4 = tkinter.Entry (window) 
#         entry4.insert(0,1)
#         canvas.create_window(250, 250, window=entry4,)
        
#         Qty = entry4.get()
#         qty_list.append(Qty)







pdf = PDF()
pdf.add_page()
# pdf.header('20,000 Leagues Under the Seas')  
pdf.set_font("Times", size=10)
today = date.today()
d1 = today.strftime("%B %d, %Y")
# num_of_items = int(input('Enter the number of products\n'))
data_as_dict = {}
item_list=[]
qty_list=[]
rate_list=[]
amount_list=[]
data_as_dict["Item name"] = []
data_as_dict["Qty"] = []
data_as_dict["Rate"] = []
data_as_dict["Amount"] = []
window = tkinter.Tk()
window.title("Dhoni Review System")
# cv_img = cv2.cvtColor(cv2.imread("welcome.png"),cv2.COLOR_BGR2RGB)
canvas = tkinter.Canvas(window,width=SET_WIDTH,height=SET_HEIGHT)
# photo = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(cv_img))
# image_on_canavas= canvas.create_image(0,0, anchor=tkinter.NW,image=photo)
canvas.pack()
#--------------Your company--------------------
label = tkinter.Label(window, text='Your Company Name')
label.config(font=('helvetica', 10))
canvas.create_window(100, 50, window=label)

entry = tkinter.Entry (window) 
entry.insert(0,title)
canvas.create_window(250, 50, window=entry,)

#--------------date--------------------
label1 = tkinter.Label(window, text='Date')
label1.config(font=('helvetica', 10))
canvas.create_window(100, 100, window=label1)

entry1 = tkinter.Entry (window) 
entry1.insert(0,d1)
canvas.create_window(250, 100, window=entry1,)

#--------------No. products--------------------
label2 = tkinter.Label(window, text='Enter the number of products')
label2.config(font=('helvetica', 10))
canvas.create_window(100, 150, window=label2)

entry2 = tkinter.Entry (window) 
entry2.insert(0,1)
canvas.create_window(250, 150, window=entry2,)
# num_of_items = entry2.get()

btn = tkinter.Button(window,text="Done",width=10,command=no_done_button)
canvas.create_window(400, 150, window=btn)





# sliced= item_name.split(',')
# for item in num_of_items:
#     data_as_dict.update({"Item name": [sliced[item]]})
# print(data_as_dict)

# def get_number_of_items():
#     for i in range(1, num_of_items + 1):
#             item_name = input(f'Enter name of product {i}\n')
#             item_list.append(item_name)


# for i in range(1, num_of_items + 1):
#         product_serial = i-1
#         rate = input(f'Enter rate of \'{item_list[product_serial]}\' \n')
#         rate_list.append(rate)

# for n in range(num_of_items):
#     amount = int(rate_list[n])*int(qty_list[n])
#     amount_list.append(str(amount))
# data_as_dict = dict({"Item name": item_list,
#                     "Qty":qty_list,
#                     "Rate":rate_list,
#                     "Amount":amount_list})
# print(data_as_dict)


# create_table(table_data = data_as_dict,title='', cell_width='even')
# pdf.ln()


# pdf.output('table_function.pdf')
# window.after(100, no_done_button)
window.attributes('-fullscreen', True)
window.mainloop()
# Need to create obejct as pdf