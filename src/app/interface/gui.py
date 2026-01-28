from __future__ import annotations

import tkinter as tk
from dataclasses import dataclass
from tkinter import messagebox, ttk

from app.application.use_cases import (
    AddVisitRequest,
    PatientService,
    RegisterPatientRequest,
)


@dataclass
class GuiAppState:
    selected_patient_id: str | None = None


class GuiApp:
    def __init__(self, service: PatientService) -> None:
        self._service = service
        self._state = GuiAppState()

        self._root = tk.Tk()
        self._root.title("Hasta Kayıt Sistemi")
        self._root.geometry("720x520")
        self._root.resizable(False, False)

        self._build_layout()
        self._refresh_patient_list()

    def run(self) -> None:
        self._root.mainloop()

    def _build_layout(self) -> None:
        header = ttk.Label(self._root, text="Hasta Kayıt Sistemi", font=("Arial", 16, "bold"))
        header.pack(pady=12)

        main_frame = ttk.Frame(self._root, padding=12)
        main_frame.pack(fill=tk.BOTH, expand=True)

        left_frame = ttk.Frame(main_frame)
        left_frame.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 12))

        right_frame = ttk.Frame(main_frame)
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        self._build_register_form(left_frame)
        self._build_patient_list(right_frame)
        self._build_visit_form(right_frame)

    def _build_register_form(self, parent: ttk.Frame) -> None:
        section = ttk.LabelFrame(parent, text="Sekreter: Hasta Kaydı", padding=12)
        section.pack(fill=tk.X)

        ttk.Label(section, text="Hasta No:").grid(row=0, column=0, sticky=tk.W, pady=4)
        ttk.Label(section, text="Ad Soyad:").grid(row=1, column=0, sticky=tk.W, pady=4)
        ttk.Label(section, text="Telefon:").grid(row=2, column=0, sticky=tk.W, pady=4)

        self._patient_id_entry = ttk.Entry(section, width=28)
        self._full_name_entry = ttk.Entry(section, width=28)
        self._phone_entry = ttk.Entry(section, width=28)

        self._patient_id_entry.grid(row=0, column=1, pady=4, sticky=tk.W)
        self._full_name_entry.grid(row=1, column=1, pady=4, sticky=tk.W)
        self._phone_entry.grid(row=2, column=1, pady=4, sticky=tk.W)

        submit_button = ttk.Button(section, text="Kaydı Oluştur", command=self._handle_register)
        submit_button.grid(row=3, column=0, columnspan=2, pady=(8, 0))

    def _build_patient_list(self, parent: ttk.Frame) -> None:
        section = ttk.LabelFrame(parent, text="Doktor: Hasta Listesi", padding=12)
        section.pack(fill=tk.BOTH, expand=True)

        columns = ("patient_id", "full_name", "phone", "visit_count")
        self._tree = ttk.Treeview(section, columns=columns, show="headings", height=8)
        self._tree.heading("patient_id", text="Hasta No")
        self._tree.heading("full_name", text="Ad Soyad")
        self._tree.heading("phone", text="Telefon")
        self._tree.heading("visit_count", text="Muayene")

        self._tree.column("patient_id", width=90)
        self._tree.column("full_name", width=220)
        self._tree.column("phone", width=120)
        self._tree.column("visit_count", width=80, anchor=tk.CENTER)

        self._tree.pack(fill=tk.BOTH, expand=True)
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

    def _handle_register(self) -> None:
        patient_id = self._patient_id_entry.get().strip()
        full_name = self._full_name_entry.get().strip()
        phone = self._phone_entry.get().strip()

        if not patient_id or not full_name or not phone:
            messagebox.showwarning("Eksik Bilgi", "Tüm alanları doldurun.")
            return

        try:
            self._service.register_patient(
                RegisterPatientRequest(
                    patient_id=patient_id,
                    full_name=full_name,
                    phone=phone,
                )
            )
        except ValueError as exc:
            messagebox.showerror("Kayıt Hatası", str(exc))
            return

        self._patient_id_entry.delete(0, tk.END)
        self._full_name_entry.delete(0, tk.END)
        self._phone_entry.delete(0, tk.END)
        self._refresh_patient_list()
        messagebox.showinfo("Başarılı", "Hasta kaydı oluşturuldu.")

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
        messagebox.showinfo("Başarılı", "Muayene notu eklendi.")

    def _refresh_patient_list(self, selected_id: str | None = None) -> None:
        for item in self._tree.get_children():
            self._tree.delete(item)

        patients = list(self._service.list_patients())
        for patient in patients:
            values = (
                patient.patient_id,
                patient.full_name,
                patient.phone,
                str(len(patient.visits)),
            )
            self._tree.insert("", tk.END, iid=patient.patient_id, values=values)

        if selected_id and self._tree.exists(selected_id):
            self._tree.selection_set(selected_id)
            self._tree.see(selected_id)
            self._state.selected_patient_id = selected_id
            self._selected_label.configure(text=selected_id)
        else:
            self._state.selected_patient_id = None
            self._selected_label.configure(text="-")

    def _on_patient_select(self, _event: tk.Event) -> None:
        selected = self._tree.selection()
        if not selected:
            return
        patient_id = selected[0]
        self._state.selected_patient_id = patient_id
        self._selected_label.configure(text=patient_id)
