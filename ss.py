'''
仅适用于python3.7
其他版本不保证适用
'''
__author__ = "1038761793@qq.com"

import os, time, sys, getopt
# pip install pillow
from PIL import ImageGrab, ImageTk
# pip install pyautogui
import pyautogui as pag
# pip install tkinter
import tkinter as tk
# pip install  pypiwin32
import win32clipboard as wc
import win32con
# pip install pyinstaller
# pyinstaller 可将python程序打包成windows可执行程序, --noconsole 表示无控制台执行
# pyinstaller -F ss.py --noconsole

def get_clipboard():
  wc.OpenClipboard()
  text = wc.GetClipboardData(win32con.CF_UNICODETEXT)
  wc.CloseClipboard()
  return text


def set_clipboard(text):
  wc.OpenClipboard()
  wc.EmptyClipboard()
  wc.SetClipboardData(win32con.CF_UNICODETEXT, text)
  wc.CloseClipboard()


class Sysargs():
  def __init__(self):
    super(Sysargs, self).__init__()
    args = sys.argv[1:]
    try:
      opts, _ = getopt.getopt(args, "hr")
    except getopt.GetoptError:
      print("该应用专用于取色, 打开该应用后, 点击屏幕即可实现取色, 并将色值保存到剪贴板上, 并可以附带命令行参数: ")
      print("-h 表示以16进制输出, 例如 #11fe83")
      print("-r 表示以rgb格式输出, 例如 rgb(11, 122, 255)")
      sys.exit(2)
    self.options = opts

class Event():
  def __init__(self, x=0, y=0):
    super(Event, self).__init__()
    self.x = x
    self.y = y

class App():
  def __init__(self):
    super(App, self).__init__()
    root   = self.root   = tk.Tk()
    root.overrideredirect(True)
    pil_im = self.pil_im = ImageGrab.grab()
    tk_im  = self.tk_im  = ImageTk.PhotoImage(image=pil_im)
    sw, sh = self.sw, self.sh = pil_im.size
    canvas = self.canvas = tk.Canvas(root, width=sw, height=sh)
    self.last_x = 0
    self.last_y = 0
    self.hf_w   = 50
    self.hf_h   = 50
    self.selector = canvas.create_oval((0, 0, 0, 0))
    canvas.pack()
    # 全屏画出截到的屏幕
    canvas.create_image((sw / 2, sh / 2), image=tk_im)
    canvas.bind("<ButtonPress-1>", self.handle_select)
    canvas.bind("<Motion>", self.reset_selector)
    x, y = self.get_mouse_coords()
    e = Event(x, y)
    self.reset_selector(e)

  def handle_select(self, e):
    opts = Sysargs()
    opt = "-h"
    if len(opts.options) > 0:
      opt, _ = opts.options[0]
    if opt == "-r":
      set_clipboard(self.selector_color_rgb)
    else:
      set_clipboard(self.selector_color_hex)
    self.root.quit()

  def get_mouse_coords(self):
    return pag.position()

  def create_mouse_bbox(self, coords):
    x, y = coords
    hf_w, hf_h = self.hf_w, self.hf_h
    if x < self.sw / 2:
      x_1, x_2 = x, x + 2 * hf_w
    else:
      x_1, x_2 = x - 2 * hf_w, x
    if y < self.sh / 2:
      y_1, y_2 = y, y + 2 * hf_h
    else:
      y_1, y_2 = y - 2 * hf_h, y
    return (x_1, y_1, x_2, y_2)
    # return (x - hf_w, y - hf_h, x + hf_w, y + hf_h)
    # return (x, y, x + 2 * hf_w, y + 2 * hf_h)

  def get_select_color(self, coords):
    return self.pil_im.getpixel(coords)

  def rgb2hex_str(self, rgb):
    r, g, b = rgb
    s_r = ("0" if r < 16 else "") + hex(r)[2:]
    s_g = ("0" if g < 16 else "") + hex(g)[2:]
    s_b = ("0" if b < 16 else "") + hex(b)[2:]
    return "#%s%s%s" % (s_r, s_g, s_b)

  def reset_selector(self, e):
    x, y = e.x, e.y
    if not(self.last_x == x and self.last_y == y):
      self.last_x = x
      self.last_y = y
      coords = (x, y)
      bbox = self.create_mouse_bbox(coords)
      color = self.get_select_color(coords)
      fill = self.rgb2hex_str(color)
      self.selector_color_rgb = "rgb" + str(color)
      self.selector_color_hex = fill
      self.canvas.delete(self.selector)
      self.selector = self.canvas.create_oval(bbox, fill=fill)

  # def update(self):
  #   x, y = pag.position()
  #   if not(self.last_x == x and self.last_y == y):
  #     self.last_x = x
  #     self.last_y = y
  #     coords = self.get_mouse_coords()
  #     bbox = self.create_mouse_bbox(coords)
  #     color = self.get_select_color(coords)
  #     self.reset_selector(bbox, color)
  #     time.sleep(0.1)
  #     self.update()

if __name__ == "__main__":
  app = App()
  app.root.mainloop()
