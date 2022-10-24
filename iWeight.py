import datetime
from ttkthemes import ThemedStyle
from tkinter import *
from functools import partial
from tkinter import Label
from iWeightdb import WeightDb
import iWeightGraph
import sys
import os
from os import path

global input_validation
global record_deleted_msg
global no_graph_msg


def create_app_window():
    app = Tk()
    app.title('iWeight')
    app.geometry("400x600")
    style = ThemedStyle(app)
    style.set_theme("vista")
    return app


def create_app_content(app, weight_database):
    headline_label = Label(app, text="Welcome to iWeight!", font=("Helvetica", 20, "bold italic"))
    headline_label.place(x=60, y=20)

    weight_label = Label(app, text="How Much iWeight?", font=("Helvetica", 15, "bold italic"))
    weight_label.place(x=100, y=80)

    text_box = Entry(app, width=10)
    text_box.place(x=130, y=120)

    input_validation = Label(app, text="")
    input_validation.place(x=80, y=150)
    check_weight_input_func = partial(check_weight_input, weight_database, text_box, input_validation)
    submit_btn = Button(app, text="Enter", command=check_weight_input_func)
    submit_btn.place(x=200, y=120)

    delete_record_label = Label(app, text="Oops..Got Confused?", font=("Helvetica", 15, "bold italic"))
    delete_record_label.place(x=90, y=180)

    record_deleted_msg = Label(app, text="")
    record_deleted_msg.place(x=20, y=250)
    delete_today_record_func = partial(delete_today_record, weight_database, record_deleted_msg)
    delete_record_btn = Button(app, text="Delete today's record", command=delete_today_record_func)
    delete_record_btn.place(x=140, y=220)

    graph_label = Label(app, text="Graph Of myWeight By Date?", font=("Helvetica", 15, "bold italic"))
    graph_label.place(x=70, y=280)

    no_graph_msg = Label(app, text="")
    no_graph_msg.place(x=20, y=350)
    build_graph_func = partial(build_graph, weight_database, no_graph_msg)
    graph_btn = Button(app, text="Check Out!", command=build_graph_func)
    graph_btn.place(x=160, y=320)

    exit_label = Label(app, text="See You Next Time, Take Care!", font=("Helvetica", 15, "bold italic"))
    exit_label.place(x=60, y=380)
    exit_app_func = partial(exit_app, app)
    exit_btn = Button(app, text="Exit", command=exit_app_func)
    exit_btn.place(x=180, y=420)

    app.mainloop()


def handle_args(weight, weight_database):
    today_date = datetime.date.today()
    date = today_date.strftime("%d/%m/%Y")
    weight_database.insert_info(weight, date)
    weight_database.show_db()


def is_today_record_created(weight_database):
    today_date = datetime.date.today()
    date = today_date.strftime("%d/%m/%Y")
    weight_database.db_cursor.execute("SELECT weight from weight WHERE date=?", (date,))
    is_created = weight_database.db_cursor.fetchall()
    if not is_created:
        return False
    else:
        return True


def check_weight_input(weight_database, text_box, input_validation):
    if not is_today_record_created(weight_database):
        try:
            weight = int(text_box.get())
            if 0 <= weight <= 400:
                weight = str(weight)
                handle_args(weight, weight_database)
                input_validation["text"] = "Got it!"
                input_validation.place(x=170, y=150)
            else:
                raise ValueError('Invalid input.')
        except ValueError:
            input_validation["text"] = "Invalid input. Try to enter a value between 0-400"
            input_validation.place(x=80, y=150)
            text_box.delete('0', END)
    else:
        input_validation["text"] = "You've already entered today's record."
        input_validation.place(x=100, y=150)
        text_box.delete('0', END)


def delete_today_record(weight_database, record_deleted_msg):
    if is_today_record_created(weight_database):
        today_date = datetime.date.today()
        date = today_date.strftime("%d/%m/%Y")
        weight_database.delete_last_record(date)
        record_deleted_msg["text"] = "Today's record has been deleted."
        record_deleted_msg.place(x=110, y=250)
    else:
        record_deleted_msg["text"] = "There is no today's record."
        record_deleted_msg.place(x=130, y=250)


def build_graph(weight_database, no_graph_msg):
    date_axe, weight_axe = weight_database.get_coord_data()
    if date_axe is False and weight_axe is False:
        no_graph_msg["text"] = "There are no values to present."
        no_graph_msg.place(x=120, y=350)
    else:
        iWeightGraph.build_graph(date_axe, weight_axe)


def exit_app(app):
    app.destroy()


def py_to_exe():
    config_name = 'iWeight.cfg'

    # determine if application is a script file or frozen exe
    if getattr(sys, 'frozen', False):
        application_path = os.path.dirname(sys.executable)
    elif __file__:
        application_path = os.path.dirname(__file__)
    config_path = os.path.join(application_path, config_name)


def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)


def main():
    # py_to_exe()
    sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))
    # os.path.dirname(sys.argv[0])
    # resource_path()
    weight_database = WeightDb()
    app = create_app_window()
    create_app_content(app, weight_database)


if __name__ == "__main__":
    main()
