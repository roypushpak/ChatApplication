import socket
import threading
import queue
import tkinter as tk
from tkinter import messagebox, scrolledtext


class ServerApp:
    def __init__(self, root):
        self.root = root
        self.root.title('TCP Chat Server')
        self.root.geometry('760x520')
        self.server_socket = None
        self.clients = {}
        self.running = False
        self.log_queue = queue.Queue()
        self.host_var = tk.StringVar(value='127.0.0.1')
        self.port_var = tk.StringVar(value='60001')
        self.status_var = tk.StringVar(value='Stopped')
        self._build_ui()
        self.root.protocol('WM_DELETE_WINDOW', self.on_close)
        self.root.after(100, self.process_log_queue)

    def _build_ui(self):
        top = tk.Frame(self.root, padx=12, pady=12)
        top.pack(fill='x')

        tk.Label(top, text='Host').grid(row=0, column=0, sticky='w')
        tk.Entry(top, textvariable=self.host_var, width=18).grid(row=0, column=1, padx=(6, 16))
        tk.Label(top, text='Port').grid(row=0, column=2, sticky='w')
        tk.Entry(top, textvariable=self.port_var, width=10).grid(row=0, column=3, padx=(6, 16))

        self.start_button = tk.Button(top, text='Start Server', width=14, command=self.start_server)
        self.start_button.grid(row=0, column=4, padx=(0, 8))

        self.stop_button = tk.Button(top, text='Stop Server', width=14, command=self.stop_server, state='disabled')
        self.stop_button.grid(row=0, column=5)

        status_frame = tk.Frame(self.root, padx=12)
        status_frame.pack(fill='x')
        tk.Label(status_frame, text='Status:').pack(side='left')
        tk.Label(status_frame, textvariable=self.status_var, fg='blue').pack(side='left', padx=(6, 0))

        main = tk.Frame(self.root, padx=12, pady=12)
        main.pack(fill='both', expand=True)

        left = tk.Frame(main)
        left.pack(side='left', fill='both', expand=True)
        tk.Label(left, text='Server Log').pack(anchor='w')
        self.log_area = scrolledtext.ScrolledText(left, wrap='word', state='disabled', font=('Consolas', 11))
        self.log_area.pack(fill='both', expand=True, pady=(6, 0))

        right = tk.Frame(main, width=220)
        right.pack(side='right', fill='y', padx=(12, 0))
        right.pack_propagate(False)
        tk.Label(right, text='Connected Clients').pack(anchor='w')
        self.client_list = tk.Listbox(right, font=('Consolas', 10))
        self.client_list.pack(fill='both', expand=True, pady=(6, 0))

    def log(self, message):
        self.log_queue.put(message)

    def process_log_queue(self):
        while not self.log_queue.empty():
            message = self.log_queue.get()
            self.log_area.configure(state='normal')
            self.log_area.insert('end', message + '\n')
            self.log_area.see('end')
            self.log_area.configure(state='disabled')
        self.root.after(100, self.process_log_queue)

    def refresh_clients(self):
        self.client_list.delete(0, 'end')
        for addr in sorted(self.clients):
            self.client_list.insert('end', addr)

    def start_server(self):
        if self.running:
            return
        host = self.host_var.get().strip()
        try:
            port = int(self.port_var.get().strip())
        except ValueError:
            messagebox.showerror('Invalid Port', 'Please enter a valid port number.')
            return

        try:
            self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.server_socket.bind((host, port))
            self.server_socket.listen(10)
            self.running = True
            self.status_var.set(f'Running on {host}:{port}')
            self.start_button.configure(state='disabled')
            self.stop_button.configure(state='normal')
            threading.Thread(target=self.accept_loop, daemon=True).start()
            self.log(f'Server started on {host}:{port}')
        except OSError as e:
            self.server_socket = None
            messagebox.showerror('Server Error', str(e))

    def accept_loop(self):
        while self.running:
            try:
                client_socket, client_address = self.server_socket.accept()
            except OSError:
                break
            addr_text = f'{client_address[0]}:{client_address[1]}'
            self.clients[addr_text] = client_socket
            self.root.after(0, self.refresh_clients)
            self.log(f'Connected: {addr_text}')
            threading.Thread(target=self.handle_client, args=(client_socket, addr_text), daemon=True).start()

    def handle_client(self, client_socket, addr_text):
        try:
            while self.running:
                data = client_socket.recv(1024)
                if not data:
                    break
                message = data.decode().strip()
                if not message:
                    continue
                self.log(f'From {addr_text}: {message}')
                if message.lower() == 'exit':
                    break
                reply = f'{message} ACK'
                client_socket.sendall(reply.encode())
                self.log(f'To {addr_text}: {reply}')
        except OSError:
            pass
        finally:
            try:
                client_socket.close()
            except OSError:
                pass
            if addr_text in self.clients:
                self.clients.pop(addr_text, None)
                self.root.after(0, self.refresh_clients)
            self.log(f'Disconnected: {addr_text}')

    def stop_server(self):
        if not self.running:
            return
        self.running = False
        for addr_text, client_socket in list(self.clients.items()):
            try:
                client_socket.shutdown(socket.SHUT_RDWR)
            except OSError:
                pass
            try:
                client_socket.close()
            except OSError:
                pass
            self.log(f'Closed client: {addr_text}')
        self.clients.clear()
        self.refresh_clients()
        try:
            self.server_socket.close()
        except OSError:
            pass
        self.server_socket = None
        self.status_var.set('Stopped')
        self.start_button.configure(state='normal')
        self.stop_button.configure(state='disabled')
        self.log('Server stopped')

    def on_close(self):
        self.stop_server()
        self.root.destroy()


if __name__ == '__main__':
    root = tk.Tk()
    app = ServerApp(root)
    root.mainloop()
