import sys
import sqlite3
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QLineEdit, QPushButton, QListWidget, QListWidgetItem
)

DB_FILE = 'gmao.db'

conn = sqlite3.connect(DB_FILE)
cur = conn.cursor()
cur.execute("""CREATE TABLE IF NOT EXISTS equipment (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    description TEXT
)""")
cur.execute("""CREATE TABLE IF NOT EXISTS task (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    equipment_id INTEGER,
    description TEXT NOT NULL,
    date_created TEXT,
    status TEXT DEFAULT 'pending',
    FOREIGN KEY(equipment_id) REFERENCES equipment(id)
)""")
conn.commit()

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("GMAO")
        self.resize(600, 400)
        layout = QHBoxLayout()
        self.setLayout(layout)

        # Equipment list and add form
        eq_layout = QVBoxLayout()
        eq_layout.addWidget(QLabel("Équipements"))
        self.eq_list = QListWidget()
        self.eq_list.currentItemChanged.connect(self.load_tasks)
        eq_layout.addWidget(self.eq_list)
        self.eq_name = QLineEdit()
        self.eq_name.setPlaceholderText("Nom")
        self.eq_desc = QLineEdit()
        self.eq_desc.setPlaceholderText("Description")
        add_eq_btn = QPushButton("Ajouter équipement")
        add_eq_btn.clicked.connect(self.add_equipment)
        eq_layout.addWidget(self.eq_name)
        eq_layout.addWidget(self.eq_desc)
        eq_layout.addWidget(add_eq_btn)
        layout.addLayout(eq_layout)

        # Task list and add form
        task_layout = QVBoxLayout()
        task_layout.addWidget(QLabel("Tâches"))
        self.task_list = QListWidget()
        task_layout.addWidget(self.task_list)
        self.task_desc = QLineEdit()
        self.task_desc.setPlaceholderText("Nouvelle tâche")
        add_task_btn = QPushButton("Ajouter tâche")
        add_task_btn.clicked.connect(self.add_task)
        done_btn = QPushButton("Marquer comme réalisée")
        done_btn.clicked.connect(self.mark_done)
        task_layout.addWidget(self.task_desc)
        task_layout.addWidget(add_task_btn)
        task_layout.addWidget(done_btn)
        layout.addLayout(task_layout)

        self.load_equipment()

    def load_equipment(self):
        self.eq_list.clear()
        for row in cur.execute("SELECT id, name FROM equipment"):
            item = QListWidgetItem(row[1])
            item.setData(0, row[0])
            self.eq_list.addItem(item)
        if self.eq_list.count():
            self.eq_list.setCurrentRow(0)

    def load_tasks(self):
        self.task_list.clear()
        item = self.eq_list.currentItem()
        if not item:
            return
        eq_id = item.data(0)
        for row in cur.execute("SELECT id, description, status FROM task WHERE equipment_id=?", (eq_id,)):
            t_item = QListWidgetItem(f"{row[1]} - {row[2]}")
            t_item.setData(0, row[0])
            self.task_list.addItem(t_item)

    def add_equipment(self):
        name = self.eq_name.text().strip()
        desc = self.eq_desc.text().strip()
        if not name:
            return
        cur.execute("INSERT INTO equipment(name, description) VALUES (?, ?)", (name, desc))
        conn.commit()
        self.eq_name.clear(); self.eq_desc.clear()
        self.load_equipment()

    def add_task(self):
        item = self.eq_list.currentItem()
        desc = self.task_desc.text().strip()
        if not item or not desc:
            return
        eq_id = item.data(0)
        cur.execute(
            "INSERT INTO task(equipment_id, description, date_created) VALUES (?, ?, datetime('now'))",
            (eq_id, desc)
        )
        conn.commit()
        self.task_desc.clear()
        self.load_tasks()

    def mark_done(self):
        item = self.task_list.currentItem()
        if not item:
            return
        task_id = item.data(0)
        cur.execute("UPDATE task SET status='done' WHERE id=?", (task_id,))
        conn.commit()
        self.load_tasks()

app = QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec_()
conn.close()
