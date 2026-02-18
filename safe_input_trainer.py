"""Educational input trainer (safe alternative to game macros).

This app demonstrates key-hold logic and toggles without targeting any game.
It only performs actions inside this app's own widgets.
"""

from __future__ import annotations

import tkinter as tk
from tkinter import ttk


class SafeInputTrainer:
    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self.root.title("Educational Input Trainer")
        self.root.geometry("560x420")
        self.root.attributes("-topmost", True)

        self.enable_w_click = tk.BooleanVar(value=False)
        self.enable_shift_c = tk.BooleanVar(value=False)

        self._w_held = False
        self._shift_held = False
        self._c_spam_job: str | None = None
        self._click_counter = 0
        self._menu_visible = True

        self._build_ui()
        self._bind_events()

    def _build_ui(self) -> None:
        frame = ttk.Frame(self.root, padding=12)
        frame.pack(fill="both", expand=True)

        title = ttk.Label(
            frame,
            text="Safe Educational Key-Hold Demo",
            font=("Segoe UI", 14, "bold"),
        )
        title.pack(anchor="w")

        note = ttk.Label(
            frame,
            text=(
                "This tool is intentionally limited to this app for educational use.\n"
                "Use Insert to show/hide this menu while it stays always-on-top."
            ),
        )
        note.pack(anchor="w", pady=(6, 12))

        controls = ttk.LabelFrame(frame, text="Options", padding=10)
        controls.pack(fill="x")

        ttk.Checkbutton(
            controls,
            text="Option A: While holding W, perform one simulated left-click",
            variable=self.enable_w_click,
        ).pack(anchor="w", pady=4)

        ttk.Checkbutton(
            controls,
            text=(
                "Option B: While holding Shift, spam 'C' in test box. "
                "On release, do one simulated left-click"
            ),
            variable=self.enable_shift_c,
        ).pack(anchor="w", pady=4)

        self.status_var = tk.StringVar(value="Idle")
        ttk.Label(frame, textvariable=self.status_var).pack(anchor="w", pady=(10, 6))

        ttk.Label(frame, text="Test area (actions happen here only):").pack(anchor="w")
        self.test_box = tk.Text(frame, height=10)
        self.test_box.pack(fill="both", expand=True)
        self.test_box.insert("end", "Focus this app and hold W / Shift to test.\n")

        info = ttk.Frame(frame)
        info.pack(fill="x", pady=(8, 0))
        self.clicks_var = tk.StringVar(value="Simulated clicks: 0")
        ttk.Label(info, textvariable=self.clicks_var).pack(side="left")

    def _bind_events(self) -> None:
        self.root.bind_all("<Insert>", self._toggle_menu)
        self.root.bind_all("<KeyPress-w>", self._on_w_press)
        self.root.bind_all("<KeyRelease-w>", self._on_w_release)
        self.root.bind_all("<KeyPress-Shift_L>", self._on_shift_press)
        self.root.bind_all("<KeyPress-Shift_R>", self._on_shift_press)
        self.root.bind_all("<KeyRelease-Shift_L>", self._on_shift_release)
        self.root.bind_all("<KeyRelease-Shift_R>", self._on_shift_release)

    def _toggle_menu(self, _event: tk.Event) -> None:
        self._menu_visible = not self._menu_visible
        self.root.attributes("-alpha", 1.0 if self._menu_visible else 0.0)
        self.status_var.set("Menu visible" if self._menu_visible else "Menu hidden (press Insert)")

    def _on_w_press(self, _event: tk.Event) -> None:
        if self._w_held:
            return
        self._w_held = True

        if self.enable_w_click.get():
            self._simulate_left_click("W hold triggered one click")

    def _on_w_release(self, _event: tk.Event) -> None:
        self._w_held = False

    def _on_shift_press(self, _event: tk.Event) -> None:
        if self._shift_held:
            return
        self._shift_held = True

        if self.enable_shift_c.get():
            self.status_var.set("Shift held: spamming C in test area")
            self._start_c_spam()

    def _on_shift_release(self, _event: tk.Event) -> None:
        if not self._shift_held:
            return
        self._shift_held = False

        if self._c_spam_job is not None:
            self.root.after_cancel(self._c_spam_job)
            self._c_spam_job = None

        if self.enable_shift_c.get():
            self._simulate_left_click("Shift released: one click")
        else:
            self.status_var.set("Idle")

    def _start_c_spam(self) -> None:
        if not self._shift_held or not self.enable_shift_c.get():
            return

        self.test_box.insert("end", "c")
        self.test_box.see("end")
        self._c_spam_job = self.root.after(60, self._start_c_spam)

    def _simulate_left_click(self, reason: str) -> None:
        self._click_counter += 1
        self.clicks_var.set(f"Simulated clicks: {self._click_counter}")
        self.status_var.set(reason)
        self.test_box.insert("end", "\n[simulated left click]\n")
        self.test_box.see("end")


def main() -> None:
    root = tk.Tk()
    SafeInputTrainer(root)
    root.mainloop()


if __name__ == "__main__":
    main()
