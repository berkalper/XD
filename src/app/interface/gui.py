from __future__ import annotations

import tkinter as tk
from dataclasses import dataclass
from datetime import datetime
from tkinter import messagebox, ttk

from app.application.use_cases import (
    AddVisitRequest,
    PatientService,
    RegisterPatientRequest,
    ScheduleAppointmentRequest,
)
from app.config import get_credentials_path
from app.infrastructure.credentials_store import CredentialsStore


@dataclass
class GuiAppState:
    selected_patient_id: str | None = None
    logged_in: bool = False


class GuiApp:
    def __init__(self, service: PatientService) -> None:
        self._service = service
        self._state = GuiAppState()
        self._credentials_store = CredentialsStore(get_credentials_path())

        self._root = tk.Tk()
        self._root.title("Hasta Kayıt Sistemi")
        self._root.geometry("900x720")
        self._root.minsize(860, 680)
        self._root.resizable(True, True)

        self._build_layout()
        self._refresh_patient_list()
        self._update_auth_state()

    def run(self) -> None:
        self._root.mainloop()

    def _build_layout(self) -> None:
        header = ttk.Label(self._root, text="Hasta Kayıt Sistemi", font=("Arial", 16, "bold"))
        header.pack(pady=12)

        self._notebook = ttk.Notebook(self._root)
        self._notebook.pack(fill=tk.BOTH, expand=True, padx=12, pady=12)

        self._login_tab = ttk.Frame(self._notebook)
        self._patient_tab = ttk.Frame(self._notebook)
        self._appointment_tab = ttk.Frame(self._notebook)

        self._notebook.add(self._login_tab, text="Giriş")
        self._notebook.add(self._patient_tab, text="Hasta Kayıtları")
        self._notebook.add(self._appointment_tab, text="Randevular")

        self._build_login_tab(self._login_tab)
        self._build_patient_tab(self._patient_tab)
        self._build_appointment_tab(self._appointment_tab)

    def _build_login_tab(self, parent: ttk.Frame) -> None:
        parent.columnconfigure(1, weight=1)

        info_label = ttk.Label(
            parent,
            text=(
                "İlk açılışta kullanıcı adı ve şifre belirleyin. "
                "Daha sonra aynı bilgilerle giriş yapın."
            ),
            wraplength=600,
        )
        info_label.grid(row=0, column=0, columnspan=2, pady=(12, 16), sticky=tk.W)

        ttk.Label(parent, text="Kullanıcı Adı:").grid(row=1, column=0, sticky=tk.W, pady=6)
        ttk.Label(parent, text="Şifre:").grid(row=2, column=0, sticky=tk.W, pady=6)

        self._username_entry = ttk.Entry(parent, width=32)
        self._password_entry = ttk.Entry(parent, width=32, show="*")
        self._username_entry.grid(row=1, column=1, sticky=tk.W, pady=6)
        self._password_entry.grid(row=2, column=1, sticky=tk.W, pady=6)

        self._auth_message = ttk.Label(parent, text="")
        self._auth_message.grid(row=3, column=0, columnspan=2, sticky=tk.W, pady=(6, 12))

        button_frame = ttk.Frame(parent)
        button_frame.grid(row=4, column=0, columnspan=2, sticky=tk.W)

        self._register_button = ttk.Button(button_frame, text="Kayıt Ol", command=self._handle_register_user)
        self._login_button = ttk.Button(button_frame, text="Giriş Yap", command=self._handle_login)
        self._logout_button = ttk.Button(button_frame, text="Çıkış Yap", command=self._handle_logout)

        self._register_button.grid(row=0, column=0, padx=(0, 8))
        self._login_button.grid(row=0, column=1, padx=(0, 8))
        self._logout_button.grid(row=0, column=2)

    def _build_patient_tab(self, parent: ttk.Frame) -> None:
        parent.columnconfigure(0, weight=1)
        parent.columnconfigure(1, weight=2)

        left_frame = ttk.Frame(parent, padding=12)
        left_frame.grid(row=0, column=0, sticky=tk.NSEW)
        right_frame = ttk.Frame(parent, padding=12)
        right_frame.grid(row=0, column=1, sticky=tk.NSEW)

        self._build_register_form(left_frame)
        self._build_patient_list(right_frame)
        self._build_visit_form(right_frame)

    def _build_appointment_tab(self, parent: ttk.Frame) -> None:
        parent.columnconfigure(0, weight=1)
        appointment_frame = ttk.Frame(parent, padding=12)
        appointment_frame.grid(row=0, column=0, sticky=tk.NSEW)
        self._build_appointment_form(appointment_frame)

    def _build_register_form(self, parent: ttk.Frame) -> None:
        section = ttk.LabelFrame(parent, text="Sekreter: Hasta Kaydı", padding=12)
        section.pack(fill=tk.X)

        ttk.Label(section, text="Hasta No:").grid(row=0, column=0, sticky=tk.W, pady=4)
        ttk.Label(section, text="Ad Soyad:").grid(row=1, column=0, sticky=tk.W, pady=4)
        ttk.Label(section, text="Telefon:").grid(row=2, column=0, sticky=tk.W, pady=4)
        ttk.Label(section, text="Yaş:").grid(row=3, column=0, sticky=tk.W, pady=4)
        ttk.Label(section, text="Cinsiyet:").grid(row=4, column=0, sticky=tk.W, pady=4)

        self._patient_id_entry = ttk.Entry(section, width=28)
        self._full_name_entry = ttk.Entry(section, width=28)
        self._phone_entry = ttk.Entry(section, width=28)
        self._age_entry = ttk.Entry(section, width=28)
        self._gender_entry = ttk.Entry(section, width=28)

        self._patient_id_entry.grid(row=0, column=1, pady=4, sticky=tk.W)
        self._full_name_entry.grid(row=1, column=1, pady=4, sticky=tk.W)
        self._phone_entry.grid(row=2, column=1, pady=4, sticky=tk.W)
        self._age_entry.grid(row=3, column=1, pady=4, sticky=tk.W)
        self._gender_entry.grid(row=4, column=1, pady=4, sticky=tk.W)

        submit_button = ttk.Button(section, text="Kaydı Oluştur", command=self._handle_register_patient)
        submit_button.grid(row=5, column=0, columnspan=2, pady=(8, 0))

    def _build_patient_list(self, parent: ttk.Frame) -> None:
        section = ttk.LabelFrame(parent, text="Doktor: Hasta Listesi", padding=12)
        section.pack(fill=tk.BOTH, expand=True)

        filter_frame = ttk.Frame(section)
        filter_frame.pack(fill=tk.X)

        ttk.Label(filter_frame, text="Arama:").pack(side=tk.LEFT)
        self._filter_var = tk.StringVar()
        filter_entry = ttk.Entry(filter_frame, textvariable=self._filter_var)
        filter_entry.pack(side=tk.LEFT, padx=8, fill=tk.X, expand=True)
        filter_entry.bind("<KeyRelease>", self._on_filter_change)

        columns = ("patient_id", "full_name", "age", "gender", "phone", "visit_count")
        self._tree = ttk.Treeview(section, columns=columns, show="headings", height=8)
        self._tree.heading("patient_id", text="Hasta No")
        self._tree.heading("full_name", text="Ad Soyad")
        self._tree.heading("age", text="Yaş")
        self._tree.heading("gender", text="Cinsiyet")
        self._tree.heading("phone", text="Telefon")
        self._tree.heading("visit_count", text="Muayene")

        self._tree.column("patient_id", width=90)
        self._tree.column("full_name", width=200)
        self._tree.column("age", width=50, anchor=tk.CENTER)
        self._tree.column("gender", width=80)
        self._tree.column("phone", width=110)
        self._tree.column("visit_count", width=80, anchor=tk.CENTER)

        self._tree.pack(fill=tk.BOTH, expand=True, pady=(8, 0))
        self._tree.bind("<<TreeviewSelect>>", self._on_patient_select)

    def _build_visit_form(self, parent: ttk.Frame) -> None:
        section = ttk.LabelFrame(parent, text="Doktor: Muayene Notu", padding=12)
        section.pack(fill=tk.X, pady=(12, 0))

        ttk.Label(section, text="Seçili Hasta:").grid(row=0, column=0, sticky=tk.W)
        self._selected_label = ttk.Label(section, text="-")
        self._selected_label.grid(row=0, column=1, sticky=tk.W)

        ttk.Label(section, text="Not:").grid(row=1, column=0, sticky=tk.NW, pady=(8, 0))
        self._note_text = tk.Text(section, width=48, height=4)
        self._note_text.grid(row=1, column=1, pady=(8, 0), sticky=tk.W)

        add_button = ttk.Button(section, text="Notu Ekle", command=self._handle_add_visit)
        add_button.grid(row=2, column=0, columnspan=2, pady=(8, 0))

        ttk.Label(section, text="Notlar:").grid(row=3, column=0, sticky=tk.NW, pady=(8, 0))
        self._visit_list = tk.Listbox(section, width=48, height=6)
        self._visit_list.grid(row=3, column=1, pady=(8, 0), sticky=tk.W)

    def _build_appointment_form(self, parent: ttk.Frame) -> None:
        section = ttk.LabelFrame(parent, text="Sekreter: Randevu", padding=12)
        section.pack(fill=tk.X)

        ttk.Label(section, text="Seçili Hasta:").grid(row=0, column=0, sticky=tk.W)
        self._appointment_selected_label = ttk.Label(section, text="-")
        self._appointment_selected_label.grid(row=0, column=1, sticky=tk.W)

        ttk.Label(section, text="Tarih Saat (YYYY-AA-GG SS:DD):").grid(
            row=1, column=0, sticky=tk.W, pady=(8, 0)
        )
        self._appointment_entry = ttk.Entry(section, width=28)
        self._appointment_entry.grid(row=1, column=1, sticky=tk.W, pady=(8, 0))

        ttk.Label(section, text="Not:").grid(row=2, column=0, sticky=tk.W, pady=(8, 0))
        self._appointment_note_entry = ttk.Entry(section, width=28)
        self._appointment_note_entry.grid(row=2, column=1, pady=(8, 0), sticky=tk.W)

        add_button = ttk.Button(section, text="Randevu Ekle", command=self._handle_add_appointment)
        add_button.grid(row=3, column=0, columnspan=2, pady=(8, 0))

        ttk.Label(section, text="Randevular:").grid(row=4, column=0, sticky=tk.NW, pady=(8, 0))
        self._appointment_list = tk.Listbox(section, width=48, height=8)
        self._appointment_list.grid(row=4, column=1, pady=(8, 0), sticky=tk.W)

    def _update_auth_state(self) -> None:
        credentials = self._credentials_store.load()
        has_credentials = credentials is not None

        if has_credentials:
            self._auth_message.configure(text="Kayıtlı kullanıcı bulundu. Giriş yapın.")
            self._register_button.configure(state=tk.DISABLED)
            self._login_button.configure(state=tk.NORMAL)
        else:
            self._auth_message.configure(text="Kayıt yok. Lütfen kullanıcı oluşturun.")
            self._register_button.configure(state=tk.NORMAL)
            self._login_button.configure(state=tk.DISABLED)

        self._set_protected_tabs_state(self._state.logged_in)

    def _set_protected_tabs_state(self, enabled: bool) -> None:
        state = "normal" if enabled else "disabled"
        self._notebook.tab(1, state=state)
        self._notebook.tab(2, state=state)

    def _handle_register_user(self) -> None:
        username = self._username_entry.get().strip()
        password = self._password_entry.get().strip()

        if not username or not password:
            messagebox.showwarning("Eksik Bilgi", "Kullanıcı adı ve şifre girin.")
            return

        if self._credentials_store.load() is not None:
            messagebox.showwarning("Kayıt Var", "Kayıt zaten mevcut. Giriş yapın.")
            return

        self._credentials_store.save(username, password)
        messagebox.showinfo("Başarılı", "Kullanıcı oluşturuldu. Giriş yapabilirsiniz.")
        self._username_entry.delete(0, tk.END)
        self._password_entry.delete(0, tk.END)
        self._update_auth_state()

    def _handle_login(self) -> None:
        username = self._username_entry.get().strip()
        password = self._password_entry.get().strip()

        if not username or not password:
            messagebox.showwarning("Eksik Bilgi", "Kullanıcı adı ve şifre girin.")
            return

        if self._credentials_store.verify(username, password):
            self._state.logged_in = True
            self._auth_message.configure(text="Giriş başarılı.")
            self._set_protected_tabs_state(True)
            self._notebook.select(self._patient_tab)
        else:
            messagebox.showerror("Hatalı Giriş", "Bilgiler hatalı. Tekrar deneyin.")
            self._password_entry.delete(0, tk.END)

    def _handle_logout(self) -> None:
        self._state.logged_in = False
        self._set_protected_tabs_state(False)
        self._auth_message.configure(text="Çıkış yapıldı.")
        self._notebook.select(self._login_tab)

    def _handle_add_visit(self) -> None:
        patient_id = self._state.selected_patient_id
        note = self._note_text.get("1.0", tk.END).strip()

        if not patient_id:
            messagebox.showwarning("Seçim", "Lütfen bir hasta seçin.")
            return

        if not note:
            messagebox.showwarning("Eksik Bilgi", "Muayene notu girin.")
            return

        try:
            self._service.add_visit(AddVisitRequest(patient_id=patient_id, note=note))
        except ValueError as exc:
            messagebox.showerror("Kayıt Hatası", str(exc))
            return

        self._note_text.delete("1.0", tk.END)
        self._refresh_patient_list(selected_id=patient_id)
        self._refresh_visit_list(patient_id)
        messagebox.showinfo("Başarılı", "Muayene notu eklendi.")

    def _handle_add_appointment(self) -> None:
        patient_id = self._state.selected_patient_id
        scheduled_text = self._appointment_entry.get().strip()
        note = self._appointment_note_entry.get().strip()

        if not patient_id:
            messagebox.showwarning("Seçim", "Lütfen bir hasta seçin.")
            return
        if not scheduled_text:
            messagebox.showwarning("Eksik Bilgi", "Randevu tarihi girin.")
            return

        try:
            scheduled_dt = datetime.strptime(scheduled_text, "%Y-%m-%d %H:%M")
        except ValueError:
            messagebox.showwarning("Eksik Bilgi", "Tarih formatı YYYY-AA-GG SS:DD olmalı.")
            return

        try:
            self._service.schedule_appointment(
                ScheduleAppointmentRequest(
                    patient_id=patient_id,
                    scheduled_at=scheduled_dt,
                    note=note,
                )
            )
        except ValueError as exc:
            messagebox.showerror("Kayıt Hatası", str(exc))
            return

        self._appointment_entry.delete(0, tk.END)
        self._appointment_note_entry.delete(0, tk.END)
        self._refresh_patient_list(selected_id=patient_id)
        self._refresh_appointment_list(patient_id)
        messagebox.showinfo("Başarılı", "Randevu eklendi.")

    def _handle_register_patient(self) -> None:
        if not self._state.logged_in:
            messagebox.showwarning("Giriş", "Lütfen giriş yapın.")
            return
        self._create_patient()

    def _create_patient(self) -> None:
        patient_id = self._patient_id_entry.get().strip()
        full_name = self._full_name_entry.get().strip()
        phone = self._phone_entry.get().strip()
        age_text = self._age_entry.get().strip()
        gender = self._gender_entry.get().strip() or "Belirtilmedi"

        if not patient_id or not full_name or not phone or not age_text:
            messagebox.showwarning("Eksik Bilgi", "Tüm alanları doldurun.")
            return
        if not age_text.isdigit():
            messagebox.showwarning("Eksik Bilgi", "Yaş sayısal olmalı.")
            return

        try:
            self._service.register_patient(
                RegisterPatientRequest(
                    patient_id=patient_id,
                    full_name=full_name,
                    phone=phone,
                    age=int(age_text),
                    gender=gender,
                )
            )
        except ValueError as exc:
            messagebox.showerror("Kayıt Hatası", str(exc))
            return

        self._patient_id_entry.delete(0, tk.END)
        self._full_name_entry.delete(0, tk.END)
        self._phone_entry.delete(0, tk.END)
        self._age_entry.delete(0, tk.END)
        self._gender_entry.delete(0, tk.END)
        self._refresh_patient_list()
        messagebox.showinfo("Başarılı", "Hasta kaydı oluşturuldu.")

    def _refresh_patient_list(self, selected_id: str | None = None) -> None:
        for item in self._tree.get_children():
            self._tree.delete(item)

        query = self._filter_var.get().lower().strip() if hasattr(self, "_filter_var") else ""
        patients = list(self._service.list_patients())
        for patient in patients:
            if query and query not in patient.full_name.lower() and query not in patient.patient_id.lower():
                continue
            values = (
                patient.patient_id,
                patient.full_name,
                str(patient.age),
                patient.gender,
                patient.phone,
                str(len(patient.visits)),
            )
            self._tree.insert("", tk.END, iid=patient.patient_id, values=values)

        if selected_id and self._tree.exists(selected_id):
            self._tree.selection_set(selected_id)
            self._tree.see(selected_id)
            self._state.selected_patient_id = selected_id
            self._selected_label.configure(text=selected_id)
            self._appointment_selected_label.configure(text=selected_id)
            self._refresh_visit_list(selected_id)
            self._refresh_appointment_list(selected_id)
        else:
            self._state.selected_patient_id = None
            self._selected_label.configure(text="-")
            self._appointment_selected_label.configure(text="-")
            self._visit_list.delete(0, tk.END)
            self._appointment_list.delete(0, tk.END)

    def _on_patient_select(self, _event: tk.Event) -> None:
        selected = self._tree.selection()
        if not selected:
            return
        patient_id = selected[0]
        self._state.selected_patient_id = patient_id
        self._selected_label.configure(text=patient_id)
        self._appointment_selected_label.configure(text=patient_id)
        self._refresh_visit_list(patient_id)
        self._refresh_appointment_list(patient_id)

    def _on_filter_change(self, _event: tk.Event) -> None:
        self._refresh_patient_list(selected_id=self._state.selected_patient_id)

    def _refresh_visit_list(self, patient_id: str) -> None:
        self._visit_list.delete(0, tk.END)
        patient = next(
            (item for item in self._service.list_patients() if item.patient_id == patient_id),
            None,
        )
        if not patient:
            return
        for visit in patient.visits:
            timestamp = visit.created_at.strftime("%Y-%m-%d %H:%M")
            self._visit_list.insert(tk.END, f"[{timestamp}] {visit.note}")

    def _refresh_appointment_list(self, patient_id: str) -> None:
        self._appointment_list.delete(0, tk.END)
        patient = next(
            (item for item in self._service.list_patients() if item.patient_id == patient_id),
            None,
        )
        if not patient:
            return
        for appointment in sorted(patient.appointments, key=lambda item: item.scheduled_at):
            timestamp = appointment.scheduled_at.strftime("%Y-%m-%d %H:%M")
            note = appointment.note or "-"
            self._appointment_list.insert(tk.END, f"[{timestamp}] {note}")
