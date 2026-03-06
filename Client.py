import socket
import threading
import queue
import tkinter as tk
from tkinter import messagebox, scrolledtext


class ClientApp:
    def __init__(self, root):
        self.root = root
        self.root.title('TCP Chat Client')
        self.root.geometry('760x560')
        self.client_socket = None
        self.connected = False
        self.receive_queue = queue.Queue()
        self.host_var = tk.StringVar(value='127.0.0.1')
        self.port_var = tk.StringVar(value='60001')
        self.status_var = tk.StringVar(value='Disconnected')
        self._build_ui()
        self.root.protocol('WM_DELETE_WINDOW', self.on_close)
        self.root.after(100, self.process_receive_queue)

    def _build_ui(self):
        top = tk.Frame(self.root, padx=12, pady=12)
        top.pack(fill='x')

        tk.Label(top, text='Server IP').grid(row=0, column=0, sticky='w')
        tk.Entry(top, textvariable=self.host_var, width=18).grid(row=0, column=1, padx=(6, 16))
        tk.Label(top, text='Port').grid(row=0, column=2, sticky='w')
        tk.Entry(top, textvariable=self.port_var, width=10).grid(row=0, column=3, padx=(6, 16))

        self.connect_button = tk.Button(top, text='Connect', width=12, command=self.connect_to_server)
        self.connect_button.grid(row=0, column=4, padx=(0, 8))

        self.disconnect_button = tk.Button(top, text='Disconnect', width=12, command=self.disconnect_from_server, state='disabled')
        self.disconnect_button.grid(row=0, column=5)

        status_frame = tk.Frame(self.root, padx=12)
        status_frame.pack(fill='x')
        tk.Label(status_frame, text='Status:').pack(side='left')
        tk.Label(status_frame, textvariable=self.status_var, fg='blue').pack(side='left', padx=(6, 0))

        chat_frame = tk.Frame(self.root, padx=12, pady=12)
        chat_frame.pack(fill='both', expand=True)
        tk.Label(chat_frame, text='Chat').pack(anchor='w')
        self.chat_area = scrolledtext.ScrolledText(chat_frame, wrap='word', state='disabled', font=('Consolas', 11))
        self.chat_area.pack(fill='both', expand=True, pady=(6, 0))

        bottom = tk.Frame(self.root, padx=12, pady=12)
        bottom.pack(fill='x')
        self.message_entry = tk.Entry(bottom, font=('Consolas', 11))
        self.message_entry.pack(side='left', fill='x', expand=True)
        self.message_entry.bind('<Return>', self.send_message)
        self.send_button = tk.Button(bottom, text='Send', width=12, command=self.send_message, state='disabled')
        self.send_button.pack(side='left', padx=(8, 0))

        hint = tk.Frame(self.root, padx=12)
        hint.pack(fill='x', pady=(0, 12))
        tk.Label(hint, text="Type any message and the server will reply with 'ACK'. Type 'exit' to end the connection.").pack(anchor='w')

    def append_chat(self, text):
        self.chat_area.configure(state='normal')
        self.chat_area.insert('end', text + '\n')
        self.chat_area.see('end')
        self.chat_area.configure(state='disabled')

    def process_receive_queue(self):
        while not self.receive_queue.empty():
            kind, message = self.receive_queue.get()
            if kind == 'message':
                self.append_chat(message)
            elif kind == 'disconnect':
                self.finish_disconnect(message)
        self.root.after(100, self.process_receive_queue)

    def connect_to_server(self):
        if self.connected:
            return
        host = self.host_var.get().strip()
        try:
            port = int(self.port_var.get().strip())
        except ValueError:
            messagebox.showerror('Invalid Port', 'Please enter a valid port number.')
            return

        try:
            self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.client_socket.connect((host, port))
            self.connected = True
            self.status_var.set(f'Connected to {host}:{port}')
            self.connect_button.configure(state='disabled')
            self.disconnect_button.configure(state='normal')
            self.send_button.configure(state='normal')
            self.append_chat(f'System: Connected to {host}:{port}')
            threading.Thread(target=self.receive_loop, daemon=True).start()
            self.message_entry.focus_set()
        except OSError as e:
            self.client_socket = None
            messagebox.showerror('Connection Error', str(e))

    def receive_loop(self):
        try:
            while self.connected:
                data = self.client_socket.recv(1024)
                if not data:
                    break
                reply = data.decode().strip()
                if reply:
                    self.receive_queue.put(('message', f'Server: {reply}'))
        except OSError:
            pass
        finally:
            if self.connected:
                self.receive_queue.put(('disconnect', 'System: Server disconnected.'))

    def send_message(self, event=None):
        if not self.connected:
            return
        message = self.message_entry.get().strip()
        if not message:
            return
        try:
            self.client_socket.sendall(message.encode())
            self.append_chat(f'You: {message}')
            self.message_entry.delete(0, 'end')
            if message.lower() == 'exit':
                self.finish_disconnect('System: Connection closed.')
        except OSError as e:
            self.finish_disconnect(f'System: {e}')

    def disconnect_from_server(self):
        if not self.connected:
            return
        try:
            self.client_socket.sendall(b'exit')
        except OSError:
            pass
        self.finish_disconnect('System: Connection closed.')

    def finish_disconnect(self, message):
        if self.client_socket:
            try:
                self.client_socket.shutdown(socket.SHUT_RDWR)
            except OSError:
                pass
            try:
                self.client_socket.close()
            except OSError:
                pass
        self.client_socket = None
        self.connected = False
        self.status_var.set('Disconnected')
        self.connect_button.configure(state='normal')
        self.disconnect_button.configure(state='disabled')
        self.send_button.configure(state='disabled')
        self.append_chat(message)

    def on_close(self):
        if self.connected:
            self.disconnect_from_server()
        self.root.destroy()


if __name__ == '__main__':
    root = tk.Tk()
    app = ClientApp(root)
    root.mainloop()
