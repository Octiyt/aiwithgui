from tkinter import messagebox, scrolledtext
import customtkinter as ctk
from PIL import ImageTk, Image
from customtkinter import CTkScrollbar
import time
from rules import rules_list
from google import genai
import re
import json

client = genai.Client()

emotionImages = {}

def load_emotions():
    img = Image.open("normal.png")
    img = img.resize((100, 100), Image.LANCZOS)
    emotionImages["normal"] = ImageTk.PhotoImage(img)

    img = Image.open("thinking.png")
    img = img.resize((100, 100), Image.LANCZOS)
    emotionImages["thinking"] = ImageTk.PhotoImage(img)

    img = Image.open("sad_emoji.png")
    img = img.resize((100, 100), Image.LANCZOS)
    emotionImages["sad"] = ImageTk.PhotoImage(img)

    img = Image.open("angry.png")
    img = img.resize((100, 100), Image.LANCZOS)
    emotionImages["angry"] = ImageTk.PhotoImage(img)

    img = Image.open("Eye Roll Emoji.png")
    img = img.resize((100, 100), Image.LANCZOS)
    emotionImages["eyeroll"] = ImageTk.PhotoImage(img)

    img = Image.open("Smiling Devil Emoji.png")
    img = img.resize((100, 100), Image.LANCZOS)
    emotionImages["devil"] = ImageTk.PhotoImage(img)

    img = Image.open("Sunglasses Emoji [Free Download Cool Emoji].png")
    img = img.resize((100, 100), Image.LANCZOS)
    emotionImages["cool"] = ImageTk.PhotoImage(img)

    img = Image.open("Sparkling Pink Heart Emoji.png")
    img = img.resize((100, 100), Image.LANCZOS)
    emotionImages["heart"] = ImageTk.PhotoImage(img)

    img = Image.open("Wink Emoji.png")
    img = img.resize((100, 100), Image.LANCZOS)
    emotionImages["wink"] = ImageTk.PhotoImage(img)

    img = Image.open("Smiling Cat Emoji [Free Download IOS Emojis].png")
    img = img.resize((100, 100), Image.LANCZOS)
    emotionImages["smile_cat"] = ImageTk.PhotoImage(img)

def change_emotion(emotiom):
    response_emo.configure(image=emotionImages.get(emotiom))

def onclick():
    try:
        user_promt = promt_entry.get()
        if user_promt == "":
            messagebox.showerror("Помилка","Ти нічого не написав")
            return
        else:
            response_label.configure(state="normal")

            response_label.insert("end", f"\n\nВаш запит: {user_promt}\n\n", "promt")

            window.update()

            promt = (
                f"Виконай запит користувач: {user_promt}. При формуванні відповіді виконуй наступні правила та обмежень.:\n{"\n".join(rules_list)}")
            print(promt)
            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=(promt),
            )
            print(response)

            response_text = str(response.text).removeprefix("```json").removesuffix("```")
            response_json = json.loads(response_text)

            response_actual = response_json.get("response",str(response_json.get))

            parts = re.split(r"\*\*(.*?)\*\*", response_actual)
            for i, part in enumerate(parts):
                if part != "":
                    if i % 2 != 0:
                        response_label.insert("end",part,"bold")
                        response_label.configure(state="disabled")

                    else:
                        response_label.insert("end",part,"response")
                        response_label.configure(state="disabled")
            change_emotion(response_json.get("emotion"))
            response_label.configure(state="disabled")
    except Exception as error:
        #print(str(error))
        response_label.configure(state="normal")
        response_label.insert("end", f"Виникла помилка: \n\n {error}", "error")
        response_label.configure(state="disabled")


window = ctk.CTk()
window.title("Візуальний асистент")
window.geometry("400x600")
window.resizable(False, False)
load_emotions()

response_emo = ctk.CTkLabel(master=window, image=emotionImages["normal"],text="")
response_emo.pack(pady=1)


change_emotion("normal")



response_label = ctk.CTkTextbox(master=window, width=350, height=350, wrap="word")
response_label.pack(pady=10)
response_label._textbox.tag_config("promt", foreground="Gray" ,font = ("Arial",17,"bold"))
response_label._textbox.tag_config("response", font=("Arial",13,))
response_label._textbox.tag_config("bold", font=("Arial",12,"bold"))
response_label._textbox.tag_config("error",foreground="Red", font=("Arial",15,"bold"))


promt_button = ctk.CTkButton(master=window, width = 200,height=50, command= onclick,text= "Відправити", font=("Arial", 25))
promt_button.pack(side="bottom",pady=20)

promt_entry = ctk.CTkEntry(master=window, width= 300,)
promt_entry.bind("<Return>", lambda event: onclick())
promt_entry.pack(side="bottom",)

response_label.configure(state="disabled")

window.mainloop()