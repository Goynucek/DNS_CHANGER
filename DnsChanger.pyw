import os
import sys
import tkinter as tk
from tkinter import messagebox

class DnsChangerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("DNS Chanfer")
        self.root.geometry("400x200")
        
        tk.Label(root, text="Input New DNS:").pack(pady=10)
        self.dns_entry = tk.Entry(root)
        self.dns_entry.pack(pady=5)
        self.dns_entry.insert(0, "8.8.8.8")
        
        tk.Button(root, text="Change DNS", command=self.change_dns_wrapper).pack(pady=20)

    def check_admin(self):
        if os.name == 'nt':
            import ctypes
            return ctypes.windll.shell32.IsUserAnAdmin()
        return False

    def change_dns_wrapper(self):
        if not self.check_admin():
            messagebox.showerror("Error", "Administrator rights are required for this operation!")
            return

        new_dns = self.dns_entry.get()
        
        if not all(part.isdigit() and 0 <= int(part) <= 255 for part in new_dns.split('.')):
            messagebox.showerror("Error", "Invalid DNS format!")
            return
            
        try:
            if os.name == 'nt':
                interface = "Ethernet"
                os.system(f'netsh interface ip set dns "{interface}" static {new_dns}')
                messagebox.showinfo("Succes", f"DNS has been successfully changed to {new_dns}")
        except Exception as e:
            messagebox.showerror("Error", f"Error occurred: {str(e)}")

def main():
    root = tk.Tk()
    app = DnsChangerApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()