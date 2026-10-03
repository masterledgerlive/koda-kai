"""Drop overlay — Koda Kai lives on the Shadow PC desktop.

A transparent, always-on-top buddy: bobs, blinks, looks around, waves, points
with his OWN cursor (bluey-style), and speaks. A real helper, not a screensaver.

Remote control channel (Kodakai writes these over SSH):
  C:\\Users\\Public\\Muse\\drop-say.txt  -> Drop speaks the line, then clears it
  C:\\Users\\Public\\Muse\\drop-cmd.txt  -> one command per line:
      wave | point X Y | hide | show | bounce

Click Drop: he waves and says something. Drag him to move him.
Launch detached: WMI Win32_Process.Create (survives SSH disconnect).
"""
import tkinter as tk
import os, random, time, json, subprocess

BASE = os.path.dirname(os.path.abspath(__file__))
SAY = r"C:\Users\Public\Muse\drop-say.txt"
CMD = r"C:\Users\Public\Muse\drop-cmd.txt"
PROG = r"C:\Users\Public\Muse\align-progress.json"

IDLE_LINES = [
    "Hey David! I'm here if you need me.",
    "The captions are cooking. I'll keep watch.",
    "Psst… drink some water. Hydration is magic.",
    "I can point at things now. Try me.",
    "Floating's hard work. Good thing I'm great at it.",
    "Kai and Koda would love this screen. Just saying.",
]


class Drop:
    def __init__(self):
        self.root = tk.Tk()
        self.root.overrideredirect(True)
        self.root.attributes('-topmost', True)
        self.root.attributes('-transparentcolor', 'magenta')
        self.root.configure(bg='magenta')
        self.W, self.H = 240, 320
        sw = self.root.winfo_screenwidth()
        sh = self.root.winfo_screenheight()
        self.bx, self.by = sw - self.W - 24, sh - self.H - 70
        self.root.geometry("%dx%d+%d+%d" % (self.W, self.H, self.bx, self.by))
        self.cv = tk.Canvas(self.root, width=self.W, height=self.H, bg='magenta',
                            highlightthickness=0, bd=0)
        self.cv.pack()
        self.imgs = {}
        for k in ('idle', 'wave', 'point'):
            self.imgs[k] = tk.PhotoImage(file=os.path.join(BASE, 'drop-%s.png' % k))
        # blink frame: vertical squash of idle (integer subsample)
        self.imgs['blink'] = self.imgs['idle'].subsample(1, 4)
        self.cx, self.cy = self.W // 2, self.H // 2 - 10
        self.sprite = self.cv.create_image(self.cx, self.cy, image=self.imgs['idle'])
        # bluey-style OWN cursor (drawn, independent of the real pointer)
        self.cursor = self.cv.create_text(-50, -50, text="\u27a4",
                                          font=("Segoe UI", 30), fill="#ffd166",
                                          state='hidden')
        # speech bubble
        self.bub = self.cv.create_rectangle(0, 0, 0, 0, fill="white",
                                            outline="#0a2233", width=2, state='hidden')
        self.bubtxt = self.cv.create_text(0, 0, text="", font=("Segoe UI", 11, "bold"),
                                          fill="#0a2233", width=190, justify='center',
                                          state='hidden')
        self.drag = None
        self.cv.bind('<ButtonPress-1>', self._press)
        self.cv.bind('<B1-Motion>', self._drag)
        self.cv.bind('<ButtonRelease-1>', self._release)
        self.t0 = time.time()
        self.busy_until = 0
        self.root.after(60, self.tick)
        self.root.after(2500, self.blink_loop)
        self.root.after(6000, self.look_loop)
        self.root.after(4000, self.poll)
        self.waved_at_start = False

    # ---------- life ----------
    def tick(self):
        # gentle float bob
        bob = int(7 * __import__('math').sin((time.time() - self.t0) * 2.1))
        self.cv.coords(self.sprite, self.cx, self.cy + bob)
        self.root.after(60, self.tick)
        if not self.waved_at_start and time.time() - self.t0 > 2:
            self.waved_at_start = True
            self.do_wave()
            hr = time.localtime().tm_hour
            if 5 <= hr < 12:
                self.say("Good morning, David! I'm here.")
            elif 12 <= hr < 18:
                self.say("Good afternoon, David! I'm here.")
            else:
                self.say("I'm live on your desktop, David!")

    def blink_loop(self):
        if time.time() > self.busy_until:
            self.cv.itemconfig(self.sprite, image=self.imgs['blink'])
            self.root.after(130, lambda: self.cv.itemconfig(
                self.sprite, image=self.imgs.get('cur', self.imgs['idle'])))
        self.root.after(random.randint(2600, 5600), self.blink_loop)

    def look_loop(self):
        if time.time() > self.busy_until:
            dx = random.choice((-16, 16))
            self.busy_until = time.time() + 1.4
            self.cv.coords(self.sprite, self.cx + dx, self.cy)
            self.root.after(1200, lambda: self.cv.coords(self.sprite, self.cx, self.cy))
        self.root.after(random.randint(9000, 16000), self.look_loop)

    # ---------- actions ----------
    def say(self, text, ms=4500):
        self.cv.itemconfig(self.bubtxt, text=text, state='normal')
        self.cv.update_idletasks()
        bx = self.cv.bbox(self.bubtxt)
        pad = 14
        self.cv.coords(self.bub, bx[0] - pad, bx[1] - pad, bx[2] + pad, bx[3] + pad)
        self.cv.itemconfig(self.bub, state='normal')
        self.cv.tag_raise(self.bubtxt)
        self.root.after(ms, lambda: (self.cv.itemconfig(self.bub, state='hidden'),
                                     self.cv.itemconfig(self.bubtxt, state='hidden')))

    def do_wave(self):
        self.imgs['cur'] = self.imgs['wave']
        self.cv.itemconfig(self.sprite, image=self.imgs['wave'])
        self.busy_until = time.time() + 1.6
        for i in range(3):
            self.root.after(i * 320, lambda: self.cv.move(self.sprite, 0, -14))
            self.root.after(i * 320 + 160, lambda: self.cv.move(self.sprite, 0, 14))
        self.root.after(1100, lambda: (self.cv.itemconfig(self.sprite, image=self.imgs['idle']),
                                       self.imgs.__setitem__('cur', self.imgs['idle'])))

    def do_point(self, x, y):
        """Glide the OWN cursor from Drop to a screen point, hold, return."""
        self.imgs['cur'] = self.imgs['point']
        self.cv.itemconfig(self.sprite, image=self.imgs['point'])
        self.busy_until = time.time() + 4
        # canvas coords of drop center on screen
        wx = self.root.winfo_x() + self.cx
        wy = self.root.winfo_y() + self.cy
        # target relative to canvas
        tx, ty = x - self.root.winfo_x(), y - self.root.winfo_y()
        self.cv.itemconfig(self.cursor, state='normal')
        steps, i = 24, [0]

        def glide():
            i[0] += 1
            t = i[0] / steps
            cx = wx - self.root.winfo_x() + (tx - (wx - self.root.winfo_x())) * t
            cy = wy - self.root.winfo_y() + (ty - (wy - self.root.winfo_y())) * t - 40 * (1 - abs(2 * t - 1))
            self.cv.coords(self.cursor, cx, cy)
            if i[0] < steps:
                self.root.after(28, glide)
            else:
                self.root.after(1800, self._point_done)
        glide()

    def _point_done(self):
        self.cv.itemconfig(self.cursor, state='hidden')
        self.cv.itemconfig(self.sprite, image=self.imgs['idle'])
        self.imgs['cur'] = self.imgs['idle']

    # ---------- remote channel ----------
    def poll(self):
        # heartbeat so HQ can verify I'm alive on the interactive desktop
        try:
            if int(time.time()) - getattr(self, '_hbt', 0) > 30:
                self._hbt = int(time.time())
                open(os.path.join(BASE, 'drop-status.txt'), 'w').write(
                    'alive %d frame=%s' % (self._hbt, 'idle'))
        except Exception:
            pass
        try:
            if os.path.exists(SAY):
                txt = open(SAY, encoding='utf-8').read().strip()
                if txt:
                    self.say(txt[:140])
                    open(SAY, 'w').close()
        except Exception:
            pass
        try:
            if os.path.exists(CMD):
                lines = open(CMD, encoding='utf-8').read().strip().splitlines()
                open(CMD, 'w').close()
                for ln in lines:
                    self.run_cmd(ln.strip())
        except Exception:
            pass
        # milestone announcements from the caption batch
        try:
            if os.path.exists(PROG):
                d = json.load(open(PROG))
                n = int(d.get('done', 0))
                if n != getattr(self, '_lastn', -1):
                    if getattr(self, '_lastn', -1) != -1 and n % 25 == 0 and n > 0:
                        self.say("Caption checkpoint: %d videos done!" % n)
                    self._lastn = n
        except Exception:
            pass
        self.root.after(2000, self.poll)

    def run_cmd(self, ln):
        if not ln:
            return
        p = ln.split()
        if p[0] == 'wave':
            self.do_wave()
        elif p[0] == 'bounce':
            for i in range(2):
                self.root.after(i * 300, lambda: self.cv.move(self.sprite, 0, -22))
                self.root.after(i * 300 + 150, lambda: self.cv.move(self.sprite, 0, 22))
        elif p[0] == 'point' and len(p) == 3:
            try:
                self.do_point(int(p[1]), int(p[2]))
            except ValueError:
                pass
        elif p[0] == 'say':
            self.say(ln[4:140])
        elif p[0] == 'open':
            target = ln[5:].strip().strip('"')
            if target and os.path.exists(target):
                self.say("On it — opening that for you.")
                self.do_wave()
                try:
                    subprocess.Popen(['explorer.exe', target])
                except Exception:
                    pass
        elif p[0] == 'hide':
            self.root.withdraw()
        elif p[0] == 'show':
            self.root.deiconify()

    # ---------- mouse ----------
    def _press(self, e):
        self.drag = (e.x_root, e.y_root, self.root.winfo_x(), self.root.winfo_y(), False)

    def _drag(self, e):
        if not self.drag:
            return
        x0, y0, wx, wy, moved = self.drag
        if abs(e.x_root - x0) + abs(e.y_root - y0) > 6:
            moved = True
        self.drag = (x0, y0, wx, wy, moved)
        if moved:
            self.root.geometry("+%d+%d" % (wx + e.x_root - x0, wy + e.y_root - y0))

    def _release(self, e):
        if self.drag and not self.drag[4]:
            self.do_wave()
            self.say(random.choice(IDLE_LINES))
        self.drag = None


if __name__ == '__main__':
    Drop().root.mainloop()
