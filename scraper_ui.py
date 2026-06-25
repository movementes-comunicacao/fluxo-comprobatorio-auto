"""
scraper_ui.py — Interface gráfica para o fluxo comprobatório de scraping social.
Executa: python scraper_ui.py
"""

import ctypes
import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import subprocess
import threading
import queue
import sys
import os
import time
import json
import shutil
from datetime import datetime
from pathlib import Path

import ctypes
import sys


def checar_e_forcar_admin():
    try:
        # Verifica se o script atual já tem privilégios de Admin
        is_admin = ctypes.windll.shell32.IsUserAnAdmin()
    except:
        is_admin = False

    if not is_admin:
        print("Solicitando privilégios de Administrador...")
        # Reabre o próprio script Python, mas pedindo permissão de Admin ao Windows
        ctypes.windll.shell32.ShellExecuteW(
            None, "runas", sys.executable, " ".join(sys.argv), None, 1
        )
        sys.exit()  # Fecha a instância atual sem privilégios


# Executa a função assim que o script inicia
checar_e_forcar_admin()

# --- DAQUI PARA BAIXO SEGUE O SEU CÓDIGO NORMAL DA INTERFACE TKINTER ---

# ─────────────────────────────────────────────
#  CONSTANTES DE ESTILO
# ─────────────────────────────────────────────
BG          = "#0d0f14"
SURFACE     = "#141720"
SURFACE2    = "#1c2030"
BORDER      = "#252a3a"
ACCENT      = "#4f8ef7"
ACCENT2     = "#7c5ef7"
SUCCESS     = "#34d399"
ERROR       = "#f87171"
WARNING     = "#fbbf24"
TEXT        = "#e2e8f0"
TEXT_DIM    = "#64748b"
FONT_MONO   = ("Consolas", 10)
FONT_UI     = ("Segoe UI", 10)
FONT_TITLE  = ("Segoe UI Semibold", 13)
FONT_LABEL  = ("Segoe UI", 9)

PLATFORMS = {
    "TikTok":    {"icon": "🎵", "env": "TIKTOK_ACC",   "needs_vpn": True},
    "Facebook":  {"icon": "📘", "env": "FACEBOOK_ACC",  "needs_vpn": False},
    "Instagram": {"icon": "📸", "env": "INSTAGRAM_ACC", "needs_vpn": False},
    "Threads":   {"icon": "🧵", "env": "THREADS_ACC",   "needs_vpn": False},
    "YouTube":   {"icon": "▶️",  "env": "YOUTUBE_ACC",   "needs_vpn": False},
    "Twitter":   {"icon": "🐦", "env": "TWITTER_ACC",   "needs_vpn": False},
}

VPN_CONFIG_DEFAULT = "vpn/config.ovpn"


# ─────────────────────────────────────────────
#  HELPERS
# ─────────────────────────────────────────────

def ts():
    return datetime.now().strftime("%H:%M:%S")


def find_openvpn():
    """Tenta localizar o binário do OpenVPN."""
    candidates = [
        r"C:\Program Files\OpenVPN Connect\ovpnconnector.exe",
        r"C:\Program Files (x86)\OpenVPN\bin\openvpn.exe",
        shutil.which("openvpn"),
    ]
    for c in candidates:
        if c and Path(c).exists():
            return c
    return None


# ─────────────────────────────────────────────
#  APLICAÇÃO PRINCIPAL
# ─────────────────────────────────────────────

class ScraperApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Fluxo Comprobatório · Social Scraper")
        self.configure(bg=BG)
        self.resizable(True, True)
        self.minsize(860, 620)
        self.geometry("980x720")

        # Estado interno
        self._proc: subprocess.Popen | None = None
        self._vpn_proc: subprocess.Popen | None = None
        self._log_queue: queue.Queue = queue.Queue()
        self._running = False
        self._vpn_connected = False
        self._platform_vars: dict[str, tk.BooleanVar] = {}
        self._status_labels: dict[str, tk.Label] = {}

        self._build_ui()
        self._poll_queue()
        self.protocol("WM_DELETE_WINDOW", self._on_close)

    # ── UI BUILD ──────────────────────────────

    def _build_ui(self):
        # Título / header
        header = tk.Frame(self, bg=BG)
        header.pack(fill="x", padx=20, pady=(18, 0))

        tk.Label(
            header, text="⬡  FLUXO COMPROBATÓRIO",
            font=("Segoe UI Semibold", 15), fg=ACCENT, bg=BG
        ).pack(side="left")

        self._clock_lbl = tk.Label(header, text="", font=FONT_LABEL, fg=TEXT_DIM, bg=BG)
        self._clock_lbl.pack(side="right")
        self._tick_clock()

        sep = tk.Frame(self, bg=BORDER, height=1)
        sep.pack(fill="x", padx=20, pady=(10, 0))

        # Corpo principal (esquerda + direita)
        body = tk.Frame(self, bg=BG)
        body.pack(fill="both", expand=True, padx=20, pady=12)

        left = tk.Frame(body, bg=BG, width=280)
        left.pack(side="left", fill="y", padx=(0, 12))
        left.pack_propagate(False)

        right = tk.Frame(body, bg=BG)
        right.pack(side="left", fill="both", expand=True)

        self._build_left(left)
        self._build_right(right)

        # Barra de status inferior
        self._build_statusbar()

    def _build_left(self, parent):
        # ── Plataformas ──
        self._section_label(parent, "PLATAFORMAS")

        plat_frame = tk.Frame(parent, bg=SURFACE, bd=0, relief="flat",
                              highlightbackground=BORDER, highlightthickness=1)
        plat_frame.pack(fill="x", pady=(4, 12))

        tk.Label(plat_frame, text="Prefixo da Unidade:", font=FONT_LABEL, fg=TEXT_DIM, bg=SURFACE).pack(anchor="w")
        self._prefix_var = tk.StringVar(value="nit")
        prefix_combo = ttk.Combobox(plat_frame, textvariable=self._prefix_var, values=["nit", "marica"], state="readonly")
        prefix_combo.pack(fill="x", pady=(2, 5))

        for name, meta in PLATFORMS.items():
            var = tk.BooleanVar(value=True)
            self._platform_vars[name] = var
            row = tk.Frame(plat_frame, bg=SURFACE)
            row.pack(fill="x", padx=10, pady=3)

            cb = tk.Checkbutton(
                row, text=f"{meta['icon']}  {name}",
                variable=var, bg=SURFACE, fg=TEXT, selectcolor=SURFACE2,
                activebackground=SURFACE, activeforeground=TEXT,
                font=FONT_UI, anchor="w", cursor="hand2",
                highlightthickness=0,
            )
            cb.pack(side="left", fill="x", expand=True)

            dot = tk.Label(row, text="●", fg=TEXT_DIM, bg=SURFACE, font=("Segoe UI", 8))
            dot.pack(side="right", padx=(0, 4))
            self._status_labels[name] = dot

            if meta["needs_vpn"]:
                tk.Label(row, text="VPN", fg=WARNING, bg=SURFACE,
                         font=("Segoe UI", 7)).pack(side="right", padx=2)

        # ── VPN ──
        self._section_label(parent, "VPN  (TikTok BR)")

        vpn_frame = tk.Frame(parent, bg=SURFACE,
                             highlightbackground=BORDER, highlightthickness=1)
        vpn_frame.pack(fill="x", pady=(4, 12))

        vpn_inner = tk.Frame(vpn_frame, bg=SURFACE, padx=10, pady=8)
        vpn_inner.pack(fill="x")

        self._vpn_var = tk.BooleanVar(value=False)
        vpn_cb = tk.Checkbutton(
            vpn_inner, text="Ativar OpenVPN antes do scraping",
            variable=self._vpn_var, bg=SURFACE, fg=TEXT, selectcolor=SURFACE2,
            activebackground=SURFACE, activeforeground=TEXT,
            font=FONT_UI, cursor="hand2", highlightthickness=0,
            command=self._on_vpn_toggle_ui,
        )
        vpn_cb.grid(row=0, column=0, columnspan=2, sticky="w")

        tk.Label(vpn_inner, text="Config .ovpn:", font=FONT_LABEL, fg=TEXT_DIM, bg=SURFACE
                 ).grid(row=1, column=0, sticky="w", pady=(6, 0))

        self._vpn_path_var = tk.StringVar(value=VPN_CONFIG_DEFAULT)
        vpn_entry = tk.Entry(
            vpn_inner, textvariable=self._vpn_path_var,
            bg=SURFACE2, fg=TEXT, insertbackground=TEXT,
            relief="flat", font=FONT_MONO, width=22,
        )
        vpn_entry.grid(row=2, column=0, columnspan=2, sticky="ew", pady=2)

        self._vpn_status_dot = tk.Label(vpn_inner, text="● Desconectado",
                                        fg=TEXT_DIM, bg=SURFACE, font=FONT_LABEL)
        self._vpn_status_dot.grid(row=3, column=0, sticky="w", pady=(4, 0))

        self._vpn_btn = tk.Button(
            vpn_inner, text="Conectar VPN",
            command=self._manual_vpn_toggle,
            bg=SURFACE2, fg=TEXT, relief="flat", font=FONT_LABEL,
            activebackground=BORDER, activeforeground=TEXT, cursor="hand2",
            padx=8, pady=3,
        )
        self._vpn_btn.grid(row=3, column=1, sticky="e", pady=(4, 0))
        vpn_inner.columnconfigure(0, weight=1)

        # ── Período ──
        self._section_label(parent, "PERÍODO")

        period_frame = tk.Frame(parent, bg=SURFACE,
                                highlightbackground=BORDER, highlightthickness=1)
        period_frame.pack(fill="x", pady=(4, 12))

        pf = tk.Frame(period_frame, bg=SURFACE, padx=10, pady=8)
        pf.pack(fill="x")

        self._period_var = tk.StringVar(value="auto")
        for val, lbl in [("auto", "Automático (sheets)"), ("manual", "Escolher datas")]:
            tk.Radiobutton(
                pf, text=lbl, variable=self._period_var, value=val,
                bg=SURFACE, fg=TEXT, selectcolor=SURFACE2,
                activebackground=SURFACE, activeforeground=TEXT,
                font=FONT_UI, cursor="hand2", highlightthickness=0,
                command=self._on_period_change,
            ).pack(anchor="w")

        date_row = tk.Frame(pf, bg=SURFACE)
        date_row.pack(fill="x", pady=(6, 0))

        tk.Label(date_row, text="De:", font=FONT_LABEL, fg=TEXT_DIM, bg=SURFACE).grid(row=0, column=0, sticky="w")
        self._since_var = tk.StringVar(value=datetime.now().strftime("%d/%m/%Y"))
        self._since_entry = tk.Entry(date_row, textvariable=self._since_var,
                                     bg=SURFACE2, fg=TEXT, insertbackground=TEXT,
                                     relief="flat", font=FONT_MONO, width=11, state="disabled")
        self._since_entry.grid(row=0, column=1, padx=(4, 0), sticky="w")

        tk.Label(date_row, text="Até:", font=FONT_LABEL, fg=TEXT_DIM, bg=SURFACE).grid(row=1, column=0, sticky="w", pady=(4, 0))
        self._until_var = tk.StringVar(value=datetime.now().strftime("%d/%m/%Y"))
        self._until_entry = tk.Entry(date_row, textvariable=self._until_var,
                                     bg=SURFACE2, fg=TEXT, insertbackground=TEXT,
                                     relief="flat", font=FONT_MONO, width=11, state="disabled")
        self._until_entry.grid(row=1, column=1, padx=(4, 0), pady=(4, 0), sticky="w")

        # ── Botão principal ──
        self._run_btn = tk.Button(
            parent, text="▶  INICIAR SCRAPING",
            command=self._on_run,
            bg=ACCENT, fg="#ffffff", relief="flat",
            font=("Segoe UI Semibold", 11),
            activebackground="#3a72e0", activeforeground="#ffffff",
            cursor="hand2", pady=10,
        )
        self._run_btn.pack(fill="x", pady=(8, 4))

        self._stop_btn = tk.Button(
            parent, text="■  PARAR",
            command=self._on_stop,
            bg=SURFACE2, fg=ERROR, relief="flat",
            font=("Segoe UI Semibold", 11),
            activebackground=BORDER, activeforeground=ERROR,
            cursor="hand2", pady=10, state="disabled",
        )
        self._stop_btn.pack(fill="x", pady=4)

    def _build_right(self, parent):
        # ── Cards de status por plataforma ──
        cards_frame = tk.Frame(parent, bg=BG)
        cards_frame.pack(fill="x", pady=(0, 10))

        self._platform_cards: dict[str, dict] = {}
        cols = 3
        for i, (name, meta) in enumerate(PLATFORMS.items()):
            card = tk.Frame(cards_frame, bg=SURFACE,
                            highlightbackground=BORDER, highlightthickness=1)
            card.grid(row=i // cols, column=i % cols, padx=4, pady=4, sticky="nsew")
            cards_frame.columnconfigure(i % cols, weight=1)

            tk.Label(card, text=meta["icon"], font=("Segoe UI", 16), bg=SURFACE
                     ).pack(pady=(8, 0))
            tk.Label(card, text=name, font=("Segoe UI Semibold", 9), fg=TEXT, bg=SURFACE
                     ).pack()
            status = tk.Label(card, text="aguardando", font=FONT_LABEL, fg=TEXT_DIM, bg=SURFACE)
            status.pack(pady=(2, 8))
            bar_bg = tk.Frame(card, bg=BORDER, height=3)
            bar_bg.pack(fill="x", padx=8, pady=(0, 8))
            bar = tk.Frame(bar_bg, bg=TEXT_DIM, height=3, width=0)
            bar.place(x=0, y=0, relheight=1)
            self._platform_cards[name] = {"status": status, "bar": bar, "bar_bg": bar_bg}

        # ── Log ──
        log_header = tk.Frame(parent, bg=BG)
        log_header.pack(fill="x")
        tk.Label(log_header, text="LOG DE EXECUÇÃO", font=("Segoe UI Semibold", 9),
                 fg=TEXT_DIM, bg=BG).pack(side="left")

        clr_btn = tk.Button(log_header, text="Limpar", command=self._clear_log,
                            bg=BG, fg=TEXT_DIM, relief="flat", font=FONT_LABEL,
                            activebackground=BG, cursor="hand2")
        clr_btn.pack(side="right")

        self._log = scrolledtext.ScrolledText(
            parent, bg=SURFACE, fg=TEXT, insertbackground=TEXT,
            font=FONT_MONO, relief="flat", wrap="word",
            highlightbackground=BORDER, highlightthickness=1,
            state="disabled",
        )
        self._log.pack(fill="both", expand=True, pady=(4, 0))

        # Tags de cor no log
        self._log.tag_config("info",    foreground=TEXT)
        self._log.tag_config("success", foreground=SUCCESS)
        self._log.tag_config("error",   foreground=ERROR)
        self._log.tag_config("warning", foreground=WARNING)
        self._log.tag_config("dim",     foreground=TEXT_DIM)
        self._log.tag_config("accent",  foreground=ACCENT)

    def _build_statusbar(self):
        bar = tk.Frame(self, bg=SURFACE2, height=28)
        bar.pack(fill="x", side="bottom")
        bar.pack_propagate(False)

        self._status_bar_lbl = tk.Label(
            bar, text="Pronto.", font=FONT_LABEL, fg=TEXT_DIM, bg=SURFACE2, anchor="w"
        )
        self._status_bar_lbl.pack(side="left", padx=12, fill="y")

        self._progress = ttk.Progressbar(bar, mode="indeterminate", length=120)
        self._progress.pack(side="right", padx=12, pady=5)

        style = ttk.Style()
        style.theme_use("clam")
        style.configure("TProgressbar", troughcolor=BORDER, background=ACCENT,
                        bordercolor=SURFACE2, lightcolor=ACCENT, darkcolor=ACCENT)

    # ── HELPERS DE UI ──────────────────────────

    def _section_label(self, parent, text):
        tk.Label(parent, text=text, font=("Segoe UI Semibold", 8),
                 fg=TEXT_DIM, bg=BG).pack(anchor="w", pady=(8, 0))

    def _tick_clock(self):
        self._clock_lbl.config(text=datetime.now().strftime("%d/%m/%Y  %H:%M:%S"))
        self.after(1000, self._tick_clock)

    def _on_period_change(self):
        state = "normal" if self._period_var.get() == "manual" else "disabled"
        self._since_entry.config(state=state)
        self._until_entry.config(state=state)

    def _on_vpn_toggle_ui(self):
        # apenas habilita/desabilita o botão manual de VPN
        pass

    # ── LOGGING ───────────────────────────────

    def _log_write(self, msg: str, tag: str = "info"):
        self._log.config(state="normal")
        self._log.insert("end", f"[{ts()}] {msg}\n", tag)
        self._log.see("end")
        self._log.config(state="disabled")

    def _clear_log(self):
        self._log.config(state="normal")
        self._log.delete("1.0", "end")
        self._log.config(state="disabled")

    def _set_status(self, msg: str):
        self._status_bar_lbl.config(text=msg)

    # ── CARDS ─────────────────────────────────

    def _set_card(self, name: str, status: str, color: str, progress: float = 0.0):
        """Atualiza card de plataforma (0.0–1.0 para a barra)."""
        card = self._platform_cards.get(name)
        if not card:
            return
        card["status"].config(text=status, fg=color)
        bar_bg = card["bar_bg"]
        bar_bg.update_idletasks()
        w = int(bar_bg.winfo_width() * progress)
        card["bar"].config(bg=color, width=max(w, 0))
        card["bar"].place(x=0, y=0, relheight=1, width=max(w, 0))

    def _reset_cards(self):
        for name in PLATFORMS:
            self._set_card(name, "aguardando", TEXT_DIM, 0.0)
            self._status_labels[name].config(fg=TEXT_DIM)

    # ── VPN ───────────────────────────────────

    def _manual_vpn_toggle(self):
        if self._vpn_connected:
            self._disconnect_vpn()
        else:
            self._connect_vpn()

    def _connect_vpn(self):
        ovpn_bin = find_openvpn()  # Deve retornar o caminho para o ovpnconnector.exe
        if not ovpn_bin:
            self._log_write("OpenVPN Connect (ovpnconnector) não encontrado.", "error")
            messagebox.showerror("VPN", "ovpnconnector.exe não encontrado no sistema.")
            return

        config = self._vpn_path_var.get().strip()
        if not Path(config).exists():
            self._log_write(f"Arquivo de config VPN não encontrado: {config}", "error")
            messagebox.showerror("VPN", f"Arquivo não encontrado:\n{config}")
            return

        self._log_write(f"Configurando e conectando VPN → {config}", "warning")
        self._vpn_status_dot.config(text="● Conectando…", fg=WARNING)
        self._vpn_btn.config(state="disabled")

        def _run():
            try:
                # 1. Aplica o perfil no conector
                self._log_queue.put(("log", "Registrando perfil .ovpn...", "dim"))
                proc_set = subprocess.run(
                    [ovpn_bin, "set-config", "profile", config],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.STDOUT,
                    text=True,
                    creationflags=subprocess.CREATE_NO_WINDOW # Evita piscar tela preta de CMD
                )
                self._log_queue.put(("log", proc_set.stdout.strip(), "dim"))

                # 2. Garante que o serviço está instalado
                subprocess.run([ovpn_bin, "install"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

                # 3. Inicia o serviço da VPN
                self._log_queue.put(("log", "Disparando o serviço OpenVPN Connect...", "dim"))
                proc_start = subprocess.run(
                    [ovpn_bin, "start"],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.STDOUT,
                    text=True,
                    creationflags=subprocess.CREATE_NO_WINDOW
                )
                
                log_output = proc_start.stdout.strip()
                self._log_queue.put(("log", log_output, "dim"))

                # Como o ovpnconnector inicia como serviço, checamos se ele não acusou erro imediato
                if "error" in log_output.lower() or "failed" in log_output.lower():
                    self._log_queue.put(("vpn_fail", log_output, None))
                else:
                    # Dá 2 segundinhos para o Windows fechar o aperto de mão com o servidor
                    time.sleep(2) 
                    self._log_queue.put(("vpn_ok", None, None))

            except Exception as e:
                self._log_queue.put(("vpn_fail", str(e), None))

        threading.Thread(target=_run, daemon=True).start()

    def _disconnect_vpn(self):
        if self._vpn_proc:
            try:
                self._vpn_proc.terminate()
            except Exception:
                pass
        self._vpn_proc = None
        self._vpn_connected = False
        self._vpn_status_dot.config(text="● Desconectado", fg=TEXT_DIM)
        self._vpn_btn.config(text="Conectar VPN", state="normal")
        self._log_write("VPN desconectada.", "warning")

    # ── PROCESSO PRINCIPAL ────────────────────

    def _build_env(self) -> dict:
        """Monta variáveis de ambiente desativando plataformas desmarcadas."""
        env = os.environ.copy()
        
        # 1. FORÇA O LOG EM TEMPO REAL (Evita que a UI fique sem atualizar)
        env["PYTHONUNBUFFERED"] = "1" 
        
        # 2. ENVIA O PREFIXO DA UNIDADE
        env["SCRAPER_PREFIX"] = self._prefix_var.get()

        for name, meta in PLATFORMS.items():
            if not self._platform_vars[name].get():
                env[meta["env"]] = ""  # força None no código
                
        if self._period_var.get() == "manual":
            env["SCRAPER_SINCE"] = self._since_var.get()
            env["SCRAPER_UNTIL"] = self._until_var.get()
            
        return env

    def _on_run(self):
        if self._running:
            return

        # Garante VPN se TikTok selecionado e toggle ativo
        if self._platform_vars.get("TikTok", tk.BooleanVar(value=False)).get() \
                and self._vpn_var.get() and not self._vpn_connected:
            self._log_write("TikTok selecionado com VPN habilitada — conectando VPN primeiro.", "warning")
            self._connect_vpn()
            # Aguarda até conectar (máx 30s) em thread separada
            def _wait_vpn_then_run():
                for _ in range(60):
                    if self._vpn_connected:
                        self.after(0, self._start_scraping)
                        return
                    time.sleep(0.5)
                self._log_queue.put(("log", "Timeout aguardando VPN. Abortando.", "error"))
            threading.Thread(target=_wait_vpn_then_run, daemon=True).start()
            return

        self._start_scraping()

    def _start_scraping(self):
        self._running = True
        self._reset_cards()
        self._clear_log()
        self._run_btn.config(state="disabled")
        self._stop_btn.config(state="normal")
        self._progress.start(12)
        self._set_status("Executando scraping…")
        self._log_write("═" * 50, "dim")
        self._log_write("INICIANDO FLUXO COMPROBATÓRIO", "accent")
        self._log_write("═" * 50, "dim")

        # Mapeia plataformas ativas para cards
        for name in PLATFORMS:
            if self._platform_vars[name].get():
                self._set_card(name, "em fila", TEXT_DIM, 0.05)

        env = self._build_env()
        cmd = [sys.executable, "outer_data.py"]
        if self._period_var.get() == "manual":
            cmd.append("dtchoose")

        def _run():
            try:
                self._proc = subprocess.Popen(
                    cmd,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.STDOUT,
                    text=True,
                    env=env,
                    cwd=Path(__file__).parent,
                )
                for raw_line in self._proc.stdout:
                    line = raw_line.rstrip()
                    if not line:
                        continue
                    tag, parsed = self._classify_line(line)
                    self._log_queue.put(("log", parsed, tag))
                    plat, action = self._detect_platform_event(line)
                    if plat:
                        self._log_queue.put(("card", plat, action))

                self._proc.wait()
                rc = self._proc.returncode
                if rc == 0:
                    self._log_queue.put(("done_ok", None, None))
                else:
                    self._log_queue.put(("done_err", f"Processo encerrou com código {rc}", None))
            except FileNotFoundError:
                self._log_queue.put(("done_err", "outer_data.py não encontrado.", None))
            except Exception as e:
                self._log_queue.put(("done_err", str(e), None))

        threading.Thread(target=_run, daemon=True).start()

    def _on_stop(self):
        if self._proc:
            try:
                self._proc.terminate()
            except Exception:
                pass
        self._log_write("Processo interrompido pelo usuário.", "warning")
        self._finalize(success=False)

    def _finalize(self, success: bool):
        self._running = False
        self._run_btn.config(state="normal")
        self._stop_btn.config(state="disabled")
        self._progress.stop()
        if success:
            self._set_status("✔ Concluído com sucesso.")
            self._log_write("═" * 50, "dim")
            self._log_write("SCRAPING CONCLUÍDO COM SUCESSO ✔", "success")
            self._log_write("═" * 50, "dim")
            for name in PLATFORMS:
                if self._platform_vars[name].get():
                    self._set_card(name, "concluído", SUCCESS, 1.0)
                    self._status_labels[name].config(fg=SUCCESS)
        else:
            self._set_status("✘ Processo encerrado com erros.")

    # ── CLASSIFICAÇÃO DE LINHAS ───────────────

    def _classify_line(self, line: str) -> tuple[str, str]:
        lower = line.lower()
        if any(k in lower for k in ("error", "erro", "exception", "traceback", "failed")):
            return "error", line
        if any(k in lower for k in ("warning", "warn", "aviso")):
            return "warning", line
        if any(k in lower for k in ("success", "sucesso", "concluído", "gerado", "✔")):
            return "success", line
        if any(k in lower for k in ("info", "iniciando", "coletando", "buscando")):
            return "info", line
        return "dim", line

    def _detect_platform_event(self, line: str) -> tuple[str | None, str]:
        lower = line.lower()
        platform_keywords = {
            "TikTok":    ["tiktok"],
            "Facebook":  ["facebook", "face"],
            "Instagram": ["instagram", "insta"],
            "Threads":   ["threads", "thread"],
            "YouTube":   ["youtube", "ytb"],
            "Twitter":   ["twitter", "twt"],
        }
        for plat, keys in platform_keywords.items():
            if any(k in lower for k in keys):
                if any(k in lower for k in ("error", "erro", "fail")):
                    return plat, "error"
                if any(k in lower for k in ("concluído", "done", "success", "gerado")):
                    return plat, "done"
                return plat, "running"
        return None, ""

    # ── FILA DE MENSAGENS (thread-safe) ───────

    def _poll_queue(self):
        try:
            while True:
                item = self._log_queue.get_nowait()
                kind, a, b = item
                if kind == "log":
                    self._log_write(a, b or "info")
                elif kind == "card":
                    self._update_card_from_event(a, b)
                elif kind == "done_ok":
                    self._finalize(success=True)
                elif kind == "done_err":
                    self._log_write(a or "Erro desconhecido.", "error")
                    self._finalize(success=False)
                elif kind == "vpn_ok":
                    self._vpn_connected = True
                    self._vpn_status_dot.config(text="● Conectado", fg=SUCCESS)
                    self._vpn_btn.config(text="Desconectar", state="normal")
                    self._log_write("VPN conectada com sucesso.", "success")
                elif kind == "vpn_fail":
                    self._vpn_connected = False
                    self._vpn_status_dot.config(text="● Falha", fg=ERROR)
                    self._vpn_btn.config(text="Conectar VPN", state="normal")
                    self._log_write(f"Falha na VPN: {a}", "error")
        except queue.Empty:
            pass
        finally:
            self.after(100, self._poll_queue)

    def _update_card_from_event(self, name: str, action: str):
        if not self._platform_vars.get(name, tk.BooleanVar(value=False)).get():
            return
        if action == "running":
            self._set_card(name, "coletando…", ACCENT, 0.5)
            self._status_labels[name].config(fg=ACCENT)
        elif action == "done":
            self._set_card(name, "concluído", SUCCESS, 1.0)
            self._status_labels[name].config(fg=SUCCESS)
        elif action == "error":
            self._set_card(name, "erro", ERROR, 1.0)
            self._status_labels[name].config(fg=ERROR)

    # ── FECHAR ────────────────────────────────

    def _on_close(self):
        if self._running:
            if not messagebox.askyesno("Sair", "Scraping em andamento. Deseja encerrar mesmo assim?"):
                return
        if self._proc:
            try:
                self._proc.terminate()
            except Exception:
                pass
        if self._vpn_proc:
            try:
                self._vpn_proc.terminate()
            except Exception:
                pass
        self.destroy()


# ─────────────────────────────────────────────
#  ENTRY POINT
# ─────────────────────────────────────────────

if __name__ == "__main__":
    app = ScraperApp()
    app.mainloop()