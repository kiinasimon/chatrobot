#importing necessary libraries
import tkinter as tk
from langchain_ollama import OllamaLLM
from langdetect import detect
from datetime import datetime
import csv
import os

model = OllamaLLM(model='llama3')
#making a dict to store the time ,user_input,and the response from the chatbot
conversation_dict={"USER_INPUT":"","CHATBOT":"","TIME":datetime.now()}

def track_conversation(user_input):
    #checking the file has already existed or not
    file_exit=os.path.exists("conversation.csv")
    conversation_dict["USER_INPUT"]=user_input

    field_name=["USER_INPUT","CHATBOT","TIME"]
    with open("conversation.csv","a",newline="") as csvfile:
        writer=csv.DictWriter(csvfile,fieldnames=field_name)
        #if the file has not already existed the header will be written
        if not file_exit:
            writer.writeheader()
        writer.writerow(conversation_dict)



def stream_response(user_input):
    try:
        response_stream = model.stream(input=user_input)

        chat_display.insert(tk.END, "Chatbot: ")


        chat_display.see(tk.END)
        
        #seeing the chatbot prompt token by token not to wait unitl it prompts the whole text

        for token in response_stream:
            conversation_dict["CHATBOT"]+=token
            chat_display.insert(tk.END, token)  
            chat_display.update_idletasks()  
            
            chat_display.see(tk.END) 
        track_conversation(user_input)




        chat_display.insert(tk.END, "\n\n")  
        
        chat_display.insert(tk.END,"You :")
        chat_display.see(tk.END)

    except Exception as e:
        chat_display.insert(tk.END, f"Chatbot: Error: {e}\n\n")

        chat_display.see(tk.END)

def send_message():
    
    common_word=['hi','hello','Thanks']
    user_input = user_input_entry.get("1.0", "end-1c").strip()

    user_input_entry.delete("1.0", "end") 

    #checking the input is empty or not
    if not user_input:
        chat_display.insert(tk.END, "You: (Empty message)\nChatbot: Please enter a message.\n\n")

        return
    #checking the user_input langauge is english or is the word in common_word list

    if detect(user_input) != 'en' and not (any(word.lower() in common_word for word in common_word)):
        chat_display.insert(tk.END, f" {user_input}\nChatbot: Only English text is supported.\n\n")

        return
    
    #prompting if the user_input pass the above checking steps
    chat_display.insert(tk.END, f" {user_input}\n")
    chat_display.see(tk.END)  

    root.after(100, lambda: stream_response(user_input))

root = tk.Tk()
root.title("Chatbot")

#the height and width of user interface
root.geometry("1500x1500")

#the font family and size of the chatbot response and the text that user has typed
chat_display = tk.Text(root, font=("Arial", 12), wrap=tk.WORD)

chat_display.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)

#making frame for  user_input and send button
user_input_frame = tk.Frame(root)
user_input_frame.pack(fill=tk.X, padx=10, pady=5)
user_input_entry = tk.Text(user_input_frame, font=("Arial", 18), height=5, bd=5, relief=tk.GROOVE, wrap=tk.WORD)


user_input_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
# Button to send the message
send_button = tk.Button(user_input_frame, text="Send", command=send_message,height=5)

send_button.pack(side=tk.RIGHT, padx=6)

root.mainloop()
