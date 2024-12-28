import tkinter as tk
from tkinter import ttk
from datetime import datetime, timedelta
import calendar
from functools import partial
from tkinter import *
from tkinter import messagebox
import os.path
from Date_Month_Year import *
def click_date(date,month,year):
    
    # just copy upsde and viewing there     
    result_window = Toplevel()
    result_window.title("Search Results")
    result_window.geometry("600x300")
    
    columns = ["Organizer", "Title", "Description", "Invitees", "Date", "Month", "Year"]
    tree = ttk.Treeview(result_window, columns=columns, show="headings")
    
    style = ttk.Style()
    style.configure("Treeview", font=("Consolas", 12))
    style.configure("Treeview.Heading", font=("Consolas", 12, "bold"))

    for col in columns:
        tree.heading(col, text=col, anchor="w")
        tree.column(col, width=100, anchor="w")
    
    try:
        found_events = False
        with open("record.txt", "r") as f:
            for line in f:
                data = line.strip().split('|')
        
                if len(data) == len(columns):
                    # check is the date is match
                    if (int(data[4].strip()) == int(date) and int(data[5].strip()) == int(month) and int(data[6].strip()) == int(year)):
                        tree.insert("", "end", values=[item.strip() for item in data])
                        found_events = True
        # add scroll bar
        scrollbar = tk.Scrollbar(result_window, orient=tk.VERTICAL, command=tree.yview)
        tree.configure(yscroll=scrollbar.set)
        
        # if valid make the treeview
        if found_events:
            tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
            scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        else:
            tk.Label(result_window, text="No events found for the specified date.", 
                        font=("Arial", 12)).pack(expand=True)

    except Exception as e:
        messagebox.showerror("Error", str(e))
########################################################################################################################################################################


def creating():
    global creating_window, user_entry, title_entry, desc_text, email_entry
    global date_entry, month_entry, year_entry


    # start for creating function
    global creating_window
    creating_window = Toplevel() # make a sub-window
    creating_window.title("Create event")
    creating_window.geometry("400x350")
    creating_window.resizable(width=False, height=False) # not allow user resize
    
    # make a frame for place the input date month year
    date_month_year_frame = Frame(creating_window,width=300,height=100, bg = "black")
    date_month_year_frame.grid(row=4, column=0, columnspan=2, pady=10)
    # the imformation tolet user know what need to enter at the column
    Label(creating_window, text="Organizer     :",font=("Arial",10)).grid(row=0, column=0)
    # make insert place for user input
    user_entry = Entry(creating_window, width=42, justify="left", borderwidth=2, font=("Arial",9))
    user_entry.grid(row=0 ,column=1)
    
    # the imformation tolet user know what need to enter at the column
    Label(creating_window, text="Title             :",font=("Arial",10)).grid(row=1, column=0)
    # make insert place for user input
    title_entry = Entry(creating_window, width=42, justify="left", borderwidth=2, font=("Arial",9))
    title_entry.grid(row=1, column=1, pady=10) 
  
    # the imformation tolet user know what need to enter at the column
    Label(creating_window, text="Description :", font=("Arial",10)).grid(row=2, column=0, pady=10)
    # make insert place for user input
    desc_text = Text(creating_window, width=42, height=10, wrap=tk.WORD, borderwidth=2, font=("Arial",9))
    desc_text.grid(row=2, column=1)

    # the imformation tolet user know what need to enter at the column
    Label(creating_window, text="Invitees :", font=("Arial",10)).grid(row=3, column=0, pady=10)
    # make insert place for user input 
    email_entry = Entry(creating_window, width=42, justify="left", borderwidth=2, font=("Arial",9))
    email_entry.insert(2,"The preson you want to invite(if valid)")
    email_entry.grid(row=3, column=1, pady=10)


    # let place the date month year in frame 
    Label(date_month_year_frame, text="Date : ").grid(row=0, column=0)
    date_entry = Entry(date_month_year_frame, width = 4, borderwidth = 2, font=("Arial",9))
    date_entry.grid(row=0, column=1)
    
    Label(date_month_year_frame, text="Month:").grid(row=0, column=2)
    month_entry = Entry(date_month_year_frame, width = 4, borderwidth = 2, font=("Arial",9))
    month_entry.grid(row=0, column=3)
    
    Label(date_month_year_frame, text="Year :").grid(row=0, column=4)
    year_entry = Entry(date_month_year_frame, width = 4, borderwidth = 2, font=("Arial",9))
    year_entry.grid(row=0, column=5)

    Button(creating_window, text="Submit",width=7 , height=1, bg="chartreuse1", command=submit_creating_button).grid(sticky="e", row=6,column=1, padx=90)
    Button(creating_window, text="Cancel", bg="brown1", width=7 , height=1, command=creating_window.destroy).grid(sticky="e", row=6, column=1)
    

def submit_creating_button():
    # pass the continue variable value to this function   
    global creating_window, user_entry, title_entry, desc_text, email_entry, date_entry, month_entry, year_entry 

    get_file = open("record.txt", "a")

    # get the user input and strip the extra space
    user = user_entry.get().strip()
    title = title_entry.get().strip()
    desc = desc_text.get("1.0", tk.END).strip() # get the position start(1.0) to the end 
    email = email_entry.get().strip()
    date = date_entry.get().strip()
    month = month_entry.get().strip()
    year = year_entry.get().strip()

    # data valindation and type check
    if len(user) == 0:
        messagebox.showerror("Error", "Organizer field can't be empty!")
        return

    if not validate_date(year, month, date):
        messagebox.showerror("Error", "Invalid date!")
        return 
    if not desc_check(desc):
        messagebox.showerror("Error", "Description is more than 20 cahracter")
        return
    else:
        messagebox.showinfo("INFO", "Create success")
    
        creating_window.destroy() # and destroy the creating window for beautiful window
        
        # save into the file
        get_file.writelines("\n")
        get_file.writelines(f"{user:<20s}|{title:<20s}|{desc:<20s}|{email:<20s}|{date:<20s}|{month:<20s}|{year:<20s}")

        
    get_file.close()

def validate_date(year, month, day):
    try:
        from datetime import datetime
        datetime(year=int(year), month=int(month), day=int(day))
        return True
    except ValueError:
        return False

def desc_check(desc):
    if len(desc)<0 or len(desc)>20:
        return False
    else:
        return True
        
#############################################################################################################################################
def viewing():
    
    viewing_window = Toplevel()
    viewing_window.title("View Event")
    
    # get the size of the screen for continue step outut fullscreen
    screen_width = viewing_window.winfo_screenwidth()
    screen_height = viewing_window.winfo_screenheight()
    viewing_window.geometry(f"{screen_width}x{screen_height}")  # Full screen
    # exception to check is the file any problem
    try:
        read_record = open("record.txt", "r")
    except (AttributeError, FileNotFoundError, PermissionError, IsADirectoryError, FileExistsError, IOError):
        viewing_window.destroy()
        messagebox.showerror("Error", "Record file reading error")
        return
    else:
        # use to modify intterface of the treeview
        style = ttk.Style()
        style.configure("Treeview", font=("Consolas", 12))
        style.configure("Treeview.Heading", font=("Consolas", 12, "bold"))
        # frame for the scrollbar and the table
        frame = Frame(viewing_window)
        frame.pack(fill=BOTH, expand=True) # fill all and if more can expand

        y_scrollbar = Scrollbar(frame, orient="vertical") # whare bar
        y_scrollbar.pack(side="right", fill="y")

        x_scrollbar = Scrollbar(frame, orient="horizontal")
        x_scrollbar.pack(side="bottom", fill="x")

        columns = ["Organizer", "Title", "Description", "Invitees", "Date", "Month", "Year"]
        # the head word and make the bar with the treeview
        tree = ttk.Treeview(frame,columns=columns,show="headings",
            yscrollcommand=y_scrollbar.set,
            xscrollcommand=x_scrollbar.set
        )
        tree.pack(fill=BOTH, expand=True)
        # make the bar can be use
        y_scrollbar.config(command=tree.yview)
        x_scrollbar.config(command=tree.xview)
        # the word place
        for column in columns:
            tree.heading(column, text=column, anchor="w")
            tree.column(column, anchor="w", width=150)
        # the data put into the data field
        for line in read_record:
            data = line.strip().split('|')
            if len(data) > 1:
                tree.insert("", "end", values=[item.strip() for item in data])

        def save_changes():
            # save current data back to the file
            with open("record.txt", "w") as write_record:
                for child in tree.get_children():
                    values = tree.item(child, "values")
                    write_record.write('|'.join(values[:]) + '\n')  # exclude action column
            viewing_window.destroy()
            
        def delete_item(item_id):
            # delete a row from the treeview and update the file
            if messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this record?"):
                tree.delete(item_id)  # remove the row from treeview
                save_changes()  # save the remaining data back to the file
                

        def edit_item(item_id):
            # edit a row in the treeview
            values = tree.item(item_id, "values")

            edit_window = Toplevel(viewing_window)
            edit_window.title("Edit Record")
            
            entries = []
            # display for user input
            for i, column in enumerate(columns):
                Label(edit_window, text=column, font=("Consolas", 12)).grid(row=i, column=0, padx=10, pady=5)
                entry = Entry(edit_window, font=("Consolas", 12), width=30)
                entry.insert(0, values[i])
                entry.grid(row=i, column=1, padx=10, pady=5)
                entries.append(entry)

            # save data
            def save_edit():
                updated_values = [entry.get() for entry in entries]
                user, title, desc, invitees, date, month, year = updated_values

                # validation checks
                if len(user) == 0:
                    messagebox.showerror("Error", "Organizer field can't be empty!")
                    return

                if not validate_date(year, month, date):
                    messagebox.showerror("Error", "Invalid date!")
                    return

                if not desc_check(desc):
                    messagebox.showerror("Error", "Description must be between 1 and 20 characters!")
                    return

                tree.item(item_id, values=updated_values)
                save_changes()
                messagebox.showinfo("Info", "Record updated successfully!")
                edit_window.destroy()

            Button(edit_window, text="Save", font=("Arial", 12), 
                command=save_edit, bg="chartreuse1").grid(row=len(columns), column=0, padx=50, pady=30, sticky='w')
            Button(edit_window, text="Delete", font=("Arial", 12), bg="brown1",
             command=lambda:(edit_window.destroy(), delete_item(item_id))).grid(row=len(columns), column=1, padx=50, pady=30, sticky='e')

        def on_tree_select(event):
            # handle user clicking on the Action column.
            item_id = tree.identify_row(event.y)
            if not item_id:
                return
            else:
                 edit_item(item_id)


        tree.bind("<Double-Button-1>",on_tree_select)

    finally:
        read_record.close()
        
#############################################################################################################################################
class calendar_app(Date_Month_Year):
    def __init__(self):
        # set the year and the month as constant
        NOW = datetime.now() # get the current month and week
        YEAR = int(NOW.strftime("%Y")) 
        MONTH = int(NOW.strftime("%m"))
        current_date = NOW.strftime("%d")
        
        # set a global variabe for change the date
        global month
        month = MONTH # global month in integer 
        
        global year
        year = int(YEAR)  # global year in integer
        
        calendar_month = datetime(year,month,1)
        calendar_month = calendar_month.strftime("%B")  # global calendar_month in english word
        
        # variable that hold the date
        calendar_date = calendar.monthcalendar(YEAR, MONTH)
        

        self.window = Tk() # make a window
        self.window.title("Calendar") # the window of the title name set as calendar
        self.window.geometry("800x600") # set the window size(800 width and 600 height)
        self.window.resizable(width=False, height=False)
        
        # make a operation bar
        abar= Menu(self.window)
        self.window.config(menu = abar)
        
        pull_down_bar = Menu(abar, tearoff=0)
        abar.add_cascade(label="Exit", menu = pull_down_bar)
        pull_down_bar.add_command(label="Exit", command= self.window.destroy)
        
        week_date_month_year = NOW.strftime("%A, %d %B %Y") # the week, date month year
        super().__init__(calendar_date,month,year,calendar_month)


        # now let we make a frame to let the window look better and easy work
        
        self.FRAME_WEEK_DATE_MONTH_YEAR = Frame(self.window, width=250, height=50)
        self.FRAME_WEEK_DATE_MONTH_YEAR.grid(row=0, column=0)

        self.FRAME_CALENDAR_MONTH_YEAR = Frame(self.window, width=250, height=50)
        self.FRAME_CALENDAR_MONTH_YEAR.grid(row=1, column=1)

        self.FRAME_WEEK_CALENDAR = Frame(self.window, width=400, height=300)
        self.FRAME_WEEK_CALENDAR.grid(row=2, column=1, sticky="news")

        self.FRAME_DATE_CALENDAR = Frame(self.window, width=420, height=250)
        self.FRAME_DATE_CALENDAR.grid(row=3, column=1, sticky="news")
        self.FRAME_DATE_CALENDAR.grid_propagate(False)
        
        
        # this frame for the arrow button
        self.FRAME_ARROW = Frame(self.window, width=300, height=50)
        self.FRAME_ARROW.grid(row=4, column=1, pady = 10)
        
        
        # now the frame for the function 
        self.FRAME_FUNCTION = Frame(self.window, width=500, height=50)
        self.FRAME_FUNCTION.grid(row=5, column=1)
        
        # now let we display the week date month year in the frame
        display_week_date_month_year = Label(self.FRAME_WEEK_DATE_MONTH_YEAR,
                                             text=week_date_month_year, font=("Times New Roman",15)) # type of the word times new roman and size 15
        display_week_date_month_year.grid(padx=10,pady=10)
        
        
        # call the function
        calendar_app.display_calendar(self)
           
        # here display the arrow for go to next or previous calendar
        Button(self.FRAME_ARROW, text="<", width=5, height=1, 
                                    command=lambda : calendar_app.click_left_arrow(self)).grid(row=0, column=0, padx=20, pady=10, sticky="w")
        Button(self.FRAME_ARROW, text =">", width=5, height=1,
                                     command = lambda :calendar_app.click_right_arrow(self)).grid(row=0, column=1, padx=20, pady=10, sticky="e")
        
        # button of the function(type, create, and view)
        display_search = Button(self.FRAME_FUNCTION, text = "search", font=("Arial",10), bg = "blue", fg = "white", width = 5,
                              command= lambda : calendar_app.confirm_click(self,"search"))
        display_search.grid(row=0, column=0,padx=30, pady=10)
        
        display_create = Button(self.FRAME_FUNCTION, text = "create", font=("Arial",10), bg = "blue", fg = "white", width = 5,
                                command= lambda : calendar_app.confirm_click(self,"create"))
        display_create.grid(row=0, column=1,padx=30, pady=10)
        
        display_view = Button(self.FRAME_FUNCTION, text = "view", font=("Arial",10), bg = "blue", fg = "white",
                              width = 5, command= lambda : calendar_app.confirm_click(self,"view"))
        display_view.grid(row=0, column=2,padx=30, pady=10)
        
        self.window.mainloop()


    def display_calendar(self):
        global search_date
        # here display the calendar month(in engilsh word) and year
        display_calendar_month_year = Label(self.FRAME_CALENDAR_MONTH_YEAR, text=f"{self.calendar_month} {self.year}", font=("Arial", 15))
        display_calendar_month_year.grid(padx=5, pady=10)
        # the enumerate function can help we get the index of the list and the word["mon","tue"] the col hold index 0 and week hold the value mon
        for col,week in enumerate(calendar_week):
            # now let we display the week of the calendar in the frame
            Label(self.FRAME_WEEK_CALENDAR, text=week, font=("Courier", 12), width=4).grid(row=0, column=col, padx=7, pady=10)

        # now display the date as a button 
        for row,week_date in enumerate(self.calendar_date): # frist for loop get the date in a week list 
            for col,date in enumerate(week_date):   # second loop get the date inside the list
                if date != 0:  # print only when calendar not zero
                    btn_color = "SystemButtonFace"
                    # check is it specify date
                    if date == search_date and self.year == self.year and self.month == self.month:
                        btn_color = "lightskyblue"
                        search_date = 100
                    elif date == int(current_date) and self.month == MONTH and self.year == YEAR:
                        btn_color = "aqua"
                    
                    # build the button
                    Button(
                    self.FRAME_DATE_CALENDAR, text=date, font=("Arial", 10), width=5, bg=btn_color,
                    command=lambda date=date, month=self.month, year=self.year: click_date(date,month,year)
                    ).grid(row=row, column=col, padx=5, pady=5)


    def click_left_arrow(self):
        # loop get the widget in the frame_data_calendar
        for widget in self.FRAME_DATE_CALENDAR.winfo_children():
            # broke the widget
            widget.destroy()
        for widget in self.FRAME_CALENDAR_MONTH_YEAR.winfo_children():
            widget.destroy()
        # minus one to get the previous month
        
        self.month -= 1
        # if the month less than 1 mean is the previous year than year -1 and the month change to 12
        if 1 > self.month:
            
            
            self.year -= 1
            self.month = 12      
        # get the change previous date
        self.calendar_date = calendar.monthcalendar(self.year, self.month)
        
        # get the change previous month in engilsh word
        self.calendar_month = datetime(self.year, self.month, 1)
        self.calendar_month = self.calendar_month.strftime("%B")

        calendar_app.display_calendar(self)
    
    def click_right_arrow(self):
        # same as the left  click 
        for widget in self.FRAME_DATE_CALENDAR.winfo_children():
            widget.destroy()
        for widget in self.FRAME_CALENDAR_MONTH_YEAR.winfo_children():
            widget.destroy()
        # reverse of the left click mean change to +
        self.month += 1
        # if the month more than 12 mean is the next year than year +1 and the month change to 1
        if  self.month > 12:

            self.year += 1
        
            self.month = 1

        if self.year > 9999:
            out = Toplevel()
            out.title("Beautiful things are around you, feel them with your heart")
            out.geometry("600x100")
            out.resizable(width=False, height=False)
            Label(out,text="10,000 years is too long and too far, seize the moment and cherish what is in front of you", font=("Times New Roman", 12)).pack()
            self.year = 9999
            
        # get the date 
        self.calendar_date = calendar.monthcalendar(self.year, self.month)

        self.calendar_month = datetime(self.year,self.month,1)
        self.calendar_month = self.calendar_month.strftime("%B")

        calendar_app.display_calendar(self)
    #####################################################################################################################################################################
    # a har this is my most clever moduler it can identify which button and go to that function
    def confirm_click(self,text):
        
        confirm_window = Toplevel()
        confirm_window.title("Friendly confirm")
        confirm_window.geometry("400x100")
        confirm_window.resizable(width=False, height=False)
    
        if text == "search":
            a = lambda: (calendar_app.searching(self), confirm_window.destroy())
        elif text == "create":
            a = lambda: (creating(), confirm_window.destroy())
        elif text == "view":
            a = lambda: (viewing(), confirm_window.destroy())

        # the text inform user
        Label(confirm_window, text = f"Confirm to use {text}", font=("Times New Roman",13)).pack(anchor="n",pady=5)
        # selection yes button
        Button(confirm_window, text = "YES", font=("Arial",10),width=7 , height=1, bg="chartreuse1", command=  a).pack(side="left", padx=50)
        # selection cancel button it will be destory during user click cancel
        Button(confirm_window, text = "CANCEL", font=("Arial",10), bg="brown1", width=7 , height=1,
                command=confirm_window.destroy).pack(side="right", padx=50)
####################################################################################################################################################

    def searching(self):

        global date_entry, month_entry, year_entry, search_date_window, calendar_date, month, year, calendar_month, search_date
        
        search_date_window = Toplevel()
        search_date_window.title("Search engine")
        search_date_window.geometry("400x100")
        search_date_window.resizable(height=False,width=False)

        
        Label(search_date_window, text="Date :").grid(row=0, column=0, padx=5, pady=5)
        date_entry = Entry(search_date_window, width = 4, borderwidth = 2, font=("Arial",9))
        date_entry.grid(row=0, column=1, padx=5, pady=5)

        Label(search_date_window, text="Month :").grid(row=0, column=2, padx=5, pady=5)
        month_entry= Entry(search_date_window, width = 4, borderwidth = 2, font=("Arial",9))
        month_entry.grid(row=0, column=3, padx=5, pady=5)

        Label(search_date_window, text="Year :").grid(row=0, column=4, padx=5, pady=5)
        year_entry = Entry(search_date_window, width = 4, borderwidth = 2, font=("Arial",9))
        year_entry.grid(row=0, column=5, padx=5, pady=5)

        Button(search_date_window, text="Submit",width=7 , height=1, bg="chartreuse1",
        command=lambda:  calendar_app.submit_search_button(self)).grid(row=1,column=1, pady=20)
        Button(search_date_window, text="Cancel", bg="brown1", width=7 , height=1, command=search_date_window.destroy).grid(row=1, column=4, pady=20)

    def submit_search_button(self):
        global date_entry, month_entry, year_entry, search_date_window, calendar_date, month, year, calendar_month, search_date

        search_date = date_entry.get().strip()
        self.month = month_entry.get().strip()
        self.year = year_entry.get().strip()
        search_date_window.destroy() 
        self.date = search_date

        if not validate_date(self.year , self.month, self.date):
            messagebox.showerror("Error", "Invalid date!")
            return

        else:
            search_date = int(self.date)
            self.month = int(self.month)
            self.year = int(self.year)

        

            for widget in self.FRAME_DATE_CALENDAR.winfo_children():
                widget.destroy()

            for widget in self.FRAME_CALENDAR_MONTH_YEAR.winfo_children():
                widget.destroy()

            self.calendar_date = calendar.monthcalendar(self.year, self.month)
        
            # get the search month in engilsh word
            self.calendar_month = datetime(self.year, self.month,1)
            self.calendar_month = self.calendar_month.strftime("%B")
            # call display calendar
            calendar_app.display_calendar(self)
     
    def run_program(__name__):
        if __name__ == '__main__':  
            Calendar_app = calendar_app()
                
##################################################################################################################################################
    global search_date
    search_date = 100
    
calendar_app.run_program('__main__')
# this program 95% done with myself, all learn for online, rubbish course 6 week assignment but only at week 5 teach GUI pui




