from tkinter import messagebox, scrolledtext
import customtkinter as ctk
from customtkinter import CTkScrollbar
import time
from rules import rules_list
from google import genai
import re

client = genai.Client()

#def bold(text):
    #response_label.configure(state="normal")
    #response_label.delete("1.0", "end")

    #parts = re.split(r"\*\*(.*?)\*\*", text)
    #for i, part in enumerate(parts):
        #tag = "bold" if i % 2 else ""
        #response_label.insert("end", part, tag)

    #response_label.configure(state="disabled")

def onclick():
    user_promt = promt_entry.get()
    if user_promt == "":
        messagebox.showerror("Помилка","Ти нічого не написав")
        return
    else:
        response_label.configure(state="normal")
        response_label.delete("1.0", "end")
        response_label.insert("1.0", f"Ваш запит: {user_promt}\n\n", "promt")

        window.update()

        promt = (
            f"Виконай запит користувач: {user_promt}. При формуванні відповіді виконуй наступні правила та обмежень.:\n{"\n".join(rules_list)}")
        print(promt)
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=(promt),
        )

        parts = re.split(r"\*\*(.*?)\*\*", response.text)
        for i, part in enumerate(parts):
            if part != "":
                if i % 2 != 0:
                    response_label.insert("end",part,"response")

                else:
                    response_label.insert("end",part,"bold")

        #bold(response.text)
        #response_label._textbox.tag_config("bold", font=("Arial", 13, "bold"))

        #response_label.insert("end", response.text, "response")
        response_label.configure(state="disabled")

window = ctk.CTk()
window.title("Візуальний асистент")
window.geometry("400x500")
window.resizable(False, False)

response_label = ctk.CTkTextbox(master=window, width=350, height=350, wrap="word")
response_label.pack(pady=10)
response_label._textbox.tag_config("promt", foreground="Gray" ,font = ("Arial",17,"bold"))
response_label._textbox.tag_config("response", font=("Arial",13,))
response_label._textbox.tag_config("response", font=("Arial",12,"bold"))

promt_button = ctk.CTkButton(master=window, width = 200,height=50, command= onclick,text= "Відправити", font=("Arial", 25))
promt_button.pack(side="bottom",pady=15)

promt_entry = ctk.CTkEntry(master=window, width= 300,)
promt_entry.bind("<Return>", lambda event: onclick())
promt_entry.pack(side="bottom",)

response_label.configure(state="disabled")

window.mainloop()