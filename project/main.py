from fpdf import FPDF
from datetime import date
import tkinter 

title = 'Bill'
SET_WIDTH = 366
SET_HEIGHT=768
window = tkinter.Tk()
window.title("Bill App")
window.geometry('900x500')
item_list=[]
item_list_main=[]
qty_list=[]
qty_list_main=[]
rate_list=[]
rate_list_main=[]
amount_list=[]
amount_list_main=[]
data_as_dict = {}
no_of_items = {"Number of items" : "" }
data_as_dict["Item name"] = []
data_as_dict["Qty"] = []
data_as_dict["Rate"] = []
data_as_dict["Amount"] = []
widget = []
No_Var=tkinter.IntVar()
Name_Var=tkinter.StringVar()

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
        
        self.set_font('helvetica','B',15)
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
        self.set_font('helvetica','I',10)
        self.set_text_color(169,169,169)
        self.cell(0, 10, f'Page: {self.page_no()}/nb', 0, 0, 'C')
    

    def create_table(self, table_data, title='', data_size = 10, title_size=12, align_data='L', align_header='L', cell_width='even', x_start='x_default',emphasize_data=[], emphasize_style=None,emphasize_color=(0,0,0)): 
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
        default_style = self.font_style
        if emphasize_style == None:
            emphasize_style = default_style
        # default_font = self.font_family
        # default_size = self.font_size_pt
        # default_style = self.font_style
        # default_color = self.color # This does not work

        # Get Width of Columns
        def get_col_widths():
            col_width = cell_width
            if col_width == 'even':
                col_width = self.epw / len(data[0]) - 1  # distribute content evenly   # epw = effective page width (width of page not including margins)
            elif col_width == 'uneven':
                col_widths = []

                # searching through columns for largest sized cell (not rows but cols)
                for col in range(len(table_data[0])): # for every row
                    longest = 0 
                    for row in range(len(table_data)):
                        cell_value = str(table_data[row][col])
                        value_length = self.get_string_width(cell_value)
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

        line_height = self.font_size * 2.5

        col_width = get_col_widths()
        self.set_font(size=title_size)

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
            margin_width = self.w - table_width
            # TODO: Check if table_width is larger than pdf width

            center_table = margin_width / 2 # only want width of left margin not both
            x_start = center_table
            self.set_x(x_start)
        elif isinstance(x_start, int):
            self.set_x(x_start)
        elif x_start == 'x_default':
            x_start = self.set_x(self.l_margin)


        # TABLE CREATION #

        # add title
        if title != '':
            self.multi_cell(0, line_height, title, border=0, align='j', ln=3, max_line_height=self.font_size)
            self.ln(line_height) # move cursor back to the left margin

        self.set_font(size=data_size)
        # add header
        y1 = self.get_y()
        if x_start:
            x_left = x_start
        else:
            x_left = self.get_x()
        x_right = self.epw + x_left
        if  not isinstance(col_width, list):
            if x_start:
                self.set_x(x_start)
            for datum in header:
                self.multi_cell(col_width, line_height, datum, border=0, align=align_header, ln=3, max_line_height=self.font_size)
                x_right = self.get_x()
            self.ln(line_height) # move cursor back to the left margin
            y2 = self.get_y()
            self.line(x_left,y1,x_right,y1)
            self.line(x_left,y2,x_right,y2)

            for row in data:
                if x_start: # not sure if I need this
                    self.set_x(x_start)
                for datum in row:
                    if datum in emphasize_data:
                        self.set_text_color(*emphasize_color)
                        self.set_font(style=emphasize_style)
                        self.multi_cell(col_width, line_height, datum, border=0, align=align_data, ln=3, max_line_height=self.font_size)
                        self.set_text_color(0,0,0)
                        self.set_font(style=default_style)
                    else:
                        self.multi_cell(col_width, line_height, datum, border=0, align=align_data, ln=3, max_line_height=self.font_size) # ln = 3 - move cursor to right with same vertical offset # this uses an object named self
                self.ln(line_height) # move cursor back to the left margin
        
        else:
            if x_start:
                self.set_x(x_start)
            for i in range(len(header)):
                datum = header[i]
                self.multi_cell(col_width[i], line_height, datum, border=0, align=align_header, ln=3, max_line_height=self.font_size)
                x_right = self.get_x()
            self.ln(line_height) # move cursor back to the left margin
            y2 = self.get_y()
            self.line(x_left,y1,x_right,y1)
            self.line(x_left,y2,x_right,y2)


            for i in range(len(data)):
                if x_start:
                    self.set_x(x_start)
                row = data[i]
                for i in range(len(row)):
                    datum = row[i]
                    if not isinstance(datum, str):
                        datum = str(datum)
                    adjusted_col_width = col_width[i]
                    if datum in emphasize_data:
                        self.set_text_color(*emphasize_color)
                        self.set_font(style=emphasize_style)
                        self.multi_cell(adjusted_col_width, line_height, datum, border=0, align=align_data, ln=3, max_line_height=self.font_size)
                        self.set_text_color(0,0,0)
                        self.set_font(style=default_style)
                    else:
                        self.multi_cell(adjusted_col_width, line_height, datum, border=0, align=align_data, ln=3, max_line_height=self.font_size) # ln = 3 - move cursor to right with same vertical offset # this uses an object named self
                self.ln(line_height) # move cursor back to the left margin
        y3 = self.get_y()
        self.line(x_left,y3,x_right,y3)

def output_pdf():
    num_of_items=No_Var.get()
    
    for items in item_list:
        items_for_list = (str(items.get()))
        item_list_main.append(items_for_list)
    for qty in qty_list:
        qty_for_list = (str(qty.get()))
        qty_list_main.append(qty_for_list)
    for rate in rate_list:
        rate_for_list = (str(rate.get()))
        rate_list_main.append(rate_for_list)
    #--------------------Amount-------------------
    label6 = tkinter.Label(window, text=f'Amount')
    label6.config(font=('helvetica', 10))
    label6.grid(row=3,column=3,pady=20,padx=5)

    for i in range(num_of_items):   
        name_position = i+4
        amount = int(rate_list_main[i])*int(qty_list_main[i])
        amount_list.append(str(amount))
        entry5 = tkinter.Entry (window) 
        entry5.insert(0,amount)
        entry5.config(state= "disabled")
        entry5.grid(row=name_position,column=3,pady=20,padx=5)

    for amount in amount_list:
        amount_for_list = (str(amount))
        print(amount_for_list)
        amount_list_main.append(amount_for_list)
    data_as_dict = dict({"Item name": item_list_main,
                     "Qty":qty_list_main,
                     "Rate":rate_list_main,
                     "Amount":amount_list_main})
    print(data_as_dict)
    pdf.create_table(table_data = data_as_dict,title=entry.get(), cell_width='even')
    pdf.ln()
    pdf.output('project/pdfs/Bill.pdf')


def clear():
    pass

def name_take():
    num_of_items=No_Var.get()
    
    for i in range(num_of_items):
        
        name_position = i+4
        label3 = tkinter.Label(window, text=f'Name')
        label3.config(font=('helvetica', 10))
        label3.grid(row=3,column=0,pady=20,padx=5)
            
        entry3 = tkinter.Entry (window) 
        entry3.grid(row=name_position,column=0,pady=20,padx=5)
        item_list.append(entry3)
    
        #--------------Qty--------------------

        label4 = tkinter.Label(window, text=f'Qty')
        label4.config(font=('helvetica', 10))
        label4.grid(row=3,column=1,pady=20,padx=5)

        entry6 = tkinter.Entry (window) 
        entry6.insert(0,1)
        entry6.grid(row=name_position,column=1,pady=20,padx=5)
        qty_list.append(entry6)

        #--------------------Rate--------------------
        label5 = tkinter.Label(window, text=f'Rate')
        label5.config(font=('helvetica', 10))
        label5.grid(row=3,column=2,pady=20,padx=5)

        entry4 = tkinter.Entry (window) 
        entry4.insert(0,1)      
        entry4.grid(row=name_position,column=2,pady=20,padx=5)
        rate_list.append(entry4)

    
    btn1 = tkinter.Button(window,text="Done",width=10,command=output_pdf)
    btn1.grid(row=name_position,column=5,pady=20,padx=5)

    
pdf = PDF(orientation='P',unit='mm',format='A4')
pdf.add_page()
pdf.set_title(title)
pdf.set_author("Bill App")
today = date.today()
d1 = today.strftime("%B %d, %Y")
pdf.cell(330,0,d1,0,0, 'C')

#--------------Your company--------------------
label = tkinter.Label(window, text='Your Company Name')
label.config(font=('helvetica', 10))
label.grid(row=0,column=0,pady=20,padx=5)

entry = tkinter.Entry (window) 
entry.insert(0,'Your Company Name')
entry.grid(row=0,column=1,pady=20,padx=5)  
pdf.set_font("Times", size=10)

#--------------date--------------------
label1 = tkinter.Label(window, text='Date')
label1.config(font=('helvetica', 10))
label1.grid(row=1,column=0,pady=20,padx=5)

entry1 = tkinter.Entry (window) 
entry1.insert(0,d1)
entry1.grid(row=1,column=1,pady=20,padx=5)

#--------------No. products--------------------
label2 = tkinter.Label(window, text='Enter the number of products')
label2.config(font=('helvetica', 10))
label2.grid(row=2,column=0,pady=20,padx=5)

entry2 = tkinter.Entry (window,textvariable = No_Var) 
entry2.grid(row=2,column=1,pady=20,padx=5)

btn=tkinter.Button(window,text = 'Done', width = 10,command = name_take)
btn.grid(row=2,column=2,pady=20,padx=5)

btn2=tkinter.Button(window,text = 'Clear',width = 10)
btn2.grid(row=2,column=3,pady=20,padx=5) 


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


# pdf.output('Bill.pdf')

# window.after(100,print_name_of_items(name_take()))
# window.attributes('-fullscreen', True)
window.mainloop()
# Need to create obejct as pdf