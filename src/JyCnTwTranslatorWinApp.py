import glob
import os
import shutil
import tkinter
import tkinter.ttk as ttk
from tkinter import Tk, NO, Scrollbar, RIGHT, Y, TRUE, X, messagebox, simpledialog, filedialog
from tkinter.ttk import Frame, Treeview

from PIL import Image, ImageTk

from JyCnTwTranslator import get_video_texts, set_video_texts, do_translate
from JyExportSrt import analyseFile, createSrt

JY_PATH = os.path.expanduser('~') + '\\AppData\\Local\\JianyingPro\\User Data\\Projects\\com.lveditor.draft'


def get_video_list():
    """
    Get Jianying video list
    :return: The list of all video path
    """
    result = [folder for folder in glob.glob(os.path.join(JY_PATH, '*/'))]
    new_list = []
    for path in result:
        if os.path.exists(path + '\\template.json'):
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
        self.tree = Treeview(self, column='#1', selectmode="browse",
                             yscrollcommand=scrollbar.set)
        self.tree.pack(expand=TRUE, fill=X)
        scrollbar.config(command=self.tree)

        # Setup column heading
        self.tree.heading('#0', text='Video', anchor='center')
        self.tree.heading('#1', text='Origin Text', anchor='nw')

        # Setup column
        self.tree.column('#0', stretch=NO)
        self.tree.column('#1', anchor='nw', minwidth=400)

        # Bind event
        self.tree.bind('<Double-1>', self.show_menu)

        # Variables init
        self.video_path_list = []
        self.video_texts_list = []
        self.video_images = []
        self.load_video_info()

    def load_video_info(self):
        """
        Load video text information
        """
        self.video_path_list = get_video_list()
        self.video_texts_list = []
        for path in self.video_path_list:
            self.video_texts_list.append(get_video_texts(path + '\\template.json'))

        self.video_images = []
        images = [Image.open(path + '\\cover.png') for path in self.video_path_list]
        for img in images:
            img = img.resize((160, 90), Image.ANTIALIAS)
            self.video_images.append(ImageTk.PhotoImage(img))
        for i in range(0, len(self.video_images)):
            txt = '\n'.join(self.video_texts_list[i][:5])
            self.tree.insert('', 'end', image=self.video_images[i], value=(txt, ''), tags='video')

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
        try:
            tw_texts = do_translate(texts)
            set_video_texts(tw_texts, self.video_path_list[index] + '\\template.json')

            messagebox.showinfo(title='Success', message='Translate success!')
            self.refresh_treeview()
        except:
            messagebox.showerror(title='Error', message='Translate fail! Please try again')

    def export_srt(self):
        """
        Export selected video's subtitle to SRT file
        """
        index = self.tree.index(self.tree.focus())
        filename = simpledialog.askstring("File name", "What is SRT file name?", parent=self)

        f = open(self.video_path_list[index] + '\\template.json', encoding='utf-8')
        txt = f.read()
        f.close()

        subtitle_txt = analyseFile(txt)
        subtitle_srt = createSrt(subtitle_txt)

        f = open(os.path.expanduser('~') + '\\Desktop\\' + filename + '.srt', "w", encoding='utf-8')
        f.write(subtitle_srt)
        f.close()

        messagebox.showinfo(title='Export',
                            message='Export srt file success!\nPlease check it on the Desktop.')

    def replace_cover_image(self):
        """
        Replace selected video cover image
        """
        index = self.tree.index(self.tree.focus())
        png_file = filedialog.askopenfilename(parent=self,
                                              initialdir=os.getcwd(),
                                              title="Please select a PNG file:",
                                              filetypes=[('PNG', ".png")])
        shutil.copy(png_file, self.video_path_list[index] + '\\cover.png')

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
