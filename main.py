from PIL import Image, ImageTk
import re
from customtkinter import *
from tkinter import filedialog, Text
from tkinter import messagebox


def b_to_decimal(b):
    """takes single binary number and returns decimal number(int)"""
    n, dec = 128, 0
    for i in str(b):
        if int(i):
            dec += n
            n /= 2
        else:
            n /= 2
    return int(dec)


def b_to_string(b):
    """Takes 0,1 and return convert string"""
    txt = ''.join(chr(b_to_decimal(b[i:i + 8])) for i in range(0, len(b), 8))
    return txt


def s_to_binary(s):
    """Takes string and converts to binary(str)"""
    res = ''.join(format(ord(i), '08b') for i in str(s))
    return res


class ImageStego:
    def __init__(self):
        self.decode_btn = None
        self.encode_btn = None
        self.bg_color = 'black'
        self.img_path = ''

    def browse_file(self):
        self.text_box.delete('0.0', 'end')
        self.image_box.configure(text='Image Displaying Area', image='')

        self.img_path = filedialog.askopenfilename(initialdir="/",
                                                   title="Select a File",
                                                   filetypes=(("Image",
                                                               ".jpg .jpeg .png"),
                                                              ))
        if self.img_path:
            self.encode_btn.configure(state='normal')
            self.decode_btn.configure(state='normal')

            img1 = ImageTk.PhotoImage(Image.open(self.img_path).resize((350, 250)))
            self.image_box.configure(image=img1)
            self.image_box.image = img1

    def save_file(self, img):
        f = filedialog.asksaveasfile(initialdir='.', filetypes=[('Image', '.png')], initialfile='encoded.png')
        img.save(f.name)
        messagebox.showinfo(title='Success', message=f'Image saved as {f.name}')
        self.encode_btn.configure(text='Encode', command=lambda: self.encode(self.text_box.get('1.0', END)))

    def encode(self, message):
        if len(message) < 2:
            messagebox.showerror(title='Error', message='Message can\'t be empty')
        else:
            image = Image.open(self.img_path, 'r')
            w = image.size[0]
            (x, y) = (0, 0)

            binaries = s_to_binary(message) + '0010010100100100'

            for pixel, n in zip(image.getdata(), binaries):
                pb = format(int(pixel[0]), '08b')
                pb = pb[:-1] + n
                p = list(pixel)
                p[0] = b_to_decimal(pb)
                image.putpixel((x, y), tuple(p))
                if x == w - 1:
                    x = 0
                    y += 1
                else:
                    x += 1

            self.encode_btn.configure(text='Save Image', command=lambda: self.save_file(image))

    def decode(self):
        image = Image.open(self.img_path, 'r')
        s, txt = '', ''
        for i in image.getdata():
            s += str(s_to_binary(i[0])[-1])

            if len(s) % 8 == 0:
                txt += b_to_string(s[-8:])
                if not bool(re.match("[a-zA-Z\s\d!@#$%^&*()_+\-=|;':/?.>,<]+$", txt)):
                    break
                if len(txt) > 2:
                    if txt[-2] + txt[-1] == '%$':
                        break
        if len(txt) > 2:
            self.text_box.delete('0.0', 'end')
            self.text_box.insert('0.0', txt[:-2])
        else:
            messagebox.showerror(title='Empty', message='No message found')

    def inter(self):
        win = CTk()
        win.title('Image Stego')
        win.config(bg=self.bg_color)
        win.minsize(width=760, height=400)
        win.resizable(False, False)

        select_image_btn = CTkButton(text='Select Image', command=self.browse_file, corner_radius=20, fg_color='#c2fbd7', text_color='#008000', hover_color='#86e386',
                                     text_font=('Helvetica', '-16', 'bold'))
        select_image_btn.pack(pady=(20, 0))

        f1 = CTkFrame(fg_color=self.bg_color)
        f1.pack(anchor='center', pady=20)
        self.image_box = CTkLabel(f1, width=350, height=250, bg_color='white', text='Image Displaying Area', text_font=('default_theme', 20))
        self.image_box.pack(side='left', padx=(0, 20))
        self.text_box = Text(f1, width=25, height=10, wrap=WORD, font='Verdana 15')
        self.text_box.pack(side='left')

        f2 = CTkFrame(fg_color=self.bg_color)
        f2.pack(anchor='center')
        self.encode_btn = CTkButton(f2, text='Encode', state='disabled', command=lambda: self.encode(self.text_box.get('1.0', END)), corner_radius=20, hover_color='#86e386',
                                    text_font=('Helvetica', '-16', 'bold'), fg_color='#c2fbd7', text_color='#008000')
        self.decode_btn = CTkButton(f2, text='Decode', state='disabled', command=lambda: self.decode(), corner_radius=20, fg_color='#c2fbd7', hover_color='#86e386',
                                    text_font=('Helvetica', '-16', 'bold'), text_color='#008000')
        self.encode_btn.pack(side='left', padx=(0, 20))
        self.decode_btn.pack()

        win.mainloop()


if __name__ == '__main__':
    ImageStego().inter()
