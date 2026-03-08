import tkinter as tk
from tkinter import scrolledtext,messagebox
from rules import rules_list
from google import genai

client = genai.Client()

def onclick():
    user_promt = promt_entry.get()
    messagebox.showerror("Помилка","Ти нічого не написав")
    promt = (
        f"Виконай запит користувач: {user_promt}. При формуванні відповіді виконуй наступні правила та обмежень.:\n{"\n".join(rules_list)}")
    print(promt)
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=(promt),
    )

    #response_label.config(text=str(response.text))
    response_textbox.insert("end", str(response.text)+ "\n")
    response_textbox.see("end")


window = tk.Tk()
window.title("Візуальний асистент")
window.geometry("400x500")
window.resizable(True, True)
window.maxsize(400, 500)
window.minsize(300, 400)

response_label = tk.Label(text = "Response")
response_label.pack(side="top",fill="x")

response_textbox = scrolledtext.ScrolledText()
response_textbox.pack(side="top",fill="both",expand=True)

promt_button = tk.Button(command= onclick,text= "Відправити")
promt_button.pack(side="bottom",fill="x")

promt_entry = tk.Entry(master=window, width= 300,)
promt_entry.pack(side="bottom",fill="x")

window.mainloop()