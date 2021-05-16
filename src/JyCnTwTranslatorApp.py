import glob
import os
import shutil
import tkinter
import tkinter.ttk as ttk
from tkinter import Tk, NO, Scrollbar, RIGHT, Y, TRUE, X, messagebox, simpledialog, filedialog
from tkinter.ttk import Frame, Treeview

from PIL import Image, ImageTk

from JyCnTwTranslator import get_video_texts, set_video_texts, get_video_names, do_single_translate
from JyExportSrt import analyseFile, createSrt
from src.Utils import get_jy_path, get_video_info_filename, get_video_meta_filename, get_cover_image_filename, \
    get_export_srt_filename


def disable_popup_close(event=None):
    pass


def get_video_list():
    """
    Get Jianying video list
    :return: The list of all video path
    """
    result = [folder for folder in glob.glob(os.path.join(get_jy_path(), '*/'))]
    new_list = []
    for path in result:
        if os.path.exists(get_video_info_filename(path)):
            new_list.append(path)

    return new_list


class App(Frame):
    """
    Main App with treeview
    """
    def __init__(self, parent=None, *args, **kwargs):
        Frame.__init__(self, parent)
        self.parent = parent

        # Create scrollbar
        scrollbar = Scrollbar(self)
        scrollbar.pack(side=RIGHT, fill=Y)

        # Create Treeview
        self.tree = Treeview(self, columns=('#0', '#1', '#2'), selectmode="browse",
                             yscrollcommand=scrollbar.set)
        self.tree.pack(expand=TRUE, fill=X)
        scrollbar.config(command=self.tree)

        # Setup column heading
        self.tree.heading('#0', text='Thumbnail', anchor='center')
        self.tree.heading('#1', text='Name', anchor='center')
        self.tree.heading('#2', text='Origin Text', anchor='nw')

        # Setup column
        self.tree.column('#0', stretch=NO)
        self.tree.column('#1', stretch=NO)
        self.tree.column('#2', anchor='nw', minwidth=300)

        # Bind event
        self.tree.bind('<Double-1>', self.show_menu)

        # Variables init
        self.video_path_list = []
        self.video_texts_list = []
        self.video_name_list = []
        self.video_images = []
        self.load_video_info()

    def load_video_info(self):
        """
        Load video text information
        """
        self.video_path_list = get_video_list()
        self.video_texts_list = []
        self.video_name_list = []
        for path in self.video_path_list:
            self.video_texts_list.append(get_video_texts(get_video_info_filename(path)))
            self.video_name_list.append(get_video_names(get_video_meta_filename(path)))

        self.video_images = []
        images = [Image.open(get_cover_image_filename(path)) for path in self.video_path_list]
        for img in images:
            img = img.resize((160, 90), Image.ANTIALIAS)
            self.video_images.append(ImageTk.PhotoImage(img))
        for i in range(0, len(self.video_images)):
            txt = '\n'.join(self.video_texts_list[i][:5])
            self.tree.insert('', 'end', image=self.video_images[i],
                             value=(self.video_name_list[i], txt),
                             tags='video')

    def refresh_treeview(self):
        """
        Reload all treeview items after translate or replace image complete
        """
        self.tree.delete(*self.tree.get_children())
        self.update()
        self.load_video_info()
        self.update()

    def show_menu(self, event):
        """
        Show menu when double click on treeview item
        :param event: Treeview double click event objject
        """
        menu = tkinter.Menu(self, tearoff=0)
        menu.add_command(label='Translate to TW', command=self.do_translate)
        menu.add_command(label='Export SRT', command=self.export_srt)
        menu.add_command(label='Replace cover image', command=self.replace_cover_image)

        try:
            menu.tk_popup(event.x_root, event.y_root)
        finally:
            menu.grab_release()

    def do_translate(self):
        """
        Translate selected video's texts from CN to TW
        """
        index = self.tree.index(self.tree.focus())
        texts = self.video_texts_list[index]
        tw_texts = []

        progress_var = tkinter.DoubleVar()
        progress_step = float(100.0/len(texts))
        progress = 0

        popup = tkinter.Toplevel(self.parent)
        popup.geometry('300x50')
        popup.transient(self.parent)
        popup.grab_set()
        popup.protocol('WM_DELETE_WINDOW', disable_popup_close)

        tkinter.Label(popup, text="Translating...").grid(row=0, column=0)
        progress_bar = ttk.Progressbar(popup, variable=progress_var, maximum=100, length=300)
        progress_bar.grid(row=1, column=0)
        popup.pack_slaves()

        try:
            for i in range(0, len(texts)):
                popup.update()
                tw_texts.append(do_single_translate(texts[i]))
                progress += progress_step
                progress_var.set(progress)

        except:
            messagebox.showerror(title='Error', message='Translate fail! Please try again')

        set_video_texts(tw_texts, get_video_info_filename(self.video_path_list[index]))

        popup.destroy()
        messagebox.showinfo(title='Success', message='Translate success!')
        self.refresh_treeview()

    def export_srt(self):
        """
        Export selected video's subtitle to SRT file
        """
        index = self.tree.index(self.tree.focus())
        filename = simpledialog.askstring("File name", "What is SRT file name?", parent=self)

        f = open(get_video_info_filename(self.video_path_list[index]), encoding='utf-8')
        txt = f.read()
        f.close()

        subtitle_txt = analyseFile(txt)
        subtitle_srt = createSrt(subtitle_txt)

        f = open(get_export_srt_filename(filename), "w", encoding='utf-8')
        f.write(subtitle_srt)
        f.close()

        messagebox.showinfo(title='Export',
                            message='Export srt file success!\nPlease check it on the Desktop.')

    def replace_cover_image(self):
        """
        Replace selected video cover image
        """
        index = self.tree.index(self.tree.focus())
        img_file = filedialog.askopenfilename(parent=self,
                                              initialdir=os.getcwd(),
                                              title="Please select a JPEG file:",
                                              filetypes=[('JPEG', ".jpg")])
        cover_image_filename = get_cover_image_filename(self.video_path_list[index])
        shutil.copy(img_file, cover_image_filename)

        messagebox.showinfo(title='Replace', message='Replace cover image success!')
        self.refresh_treeview()


if __name__ == '__main__':
    root = Tk()
    root.title('Jianying Text CN to TW Translator')
    root.geometry('640x480')
    root.grid_rowconfigure(0, weight=1)
    root.grid_columnconfigure(0, weight=1)

    style = ttk.Style(root)
    style.configure('Treeview', rowheight=100)

    app = App(root)
    app.grid(row=0, column=0, sticky='nsew')

    root.rowconfigure(0, weight=1)
    root.columnconfigure(0, weight=1)
    root.mainloop()
