# FsocietyGPT

## Safe educational alternative

This repository now contains a **Windows-friendly Python Tkinter app** that demonstrates key-hold logic in a safe, non-game way.

### What it does
- Always-on-top menu window.
- `Insert` toggles menu visibility.
- **Option A**: while holding `W`, it performs one **simulated** left-click.
- **Option B**: while holding `Shift`, it repeatedly writes `c` in the app test area; on release, it performs one **simulated** left-click.

> The behavior is intentionally limited to this application for educational testing.

## Run

```bash
python safe_input_trainer.py
```

No third-party packages are required (uses Python standard library `tkinter`).
