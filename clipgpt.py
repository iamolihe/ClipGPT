import json
import threading
import queue
import os
import pyperclip
from pynput import keyboard
from chatgpt_wrapper import ChatGPT

NOTIFICATION_SEND_TITLE = '"Text send..."'
NOTIFICATION_SEND_BODY = '"Waiting for answer..."'
NOTIFICATION_RECEIVED_TITLE = '"Text is Ready"'
NOTIFICATION_RECEIVED_BODY = '"Your command was processed."'
NOTIFICATION_EXIT_TITLE = '"Exiting ClipGPT..."'
NOTIFICATION_EXIT_BODY = '"Program is closing down"'

def chatgpt_thread(input_queue, output_queue, stop_event):
    gpt = ChatGPT()
    prompt = None
    last_prompt = None
    reply = None
    while True:
        try:
            prompt = input_queue.get(timeout=1)
        except queue.Empty:
            if stop_event.is_set():
                return
            continue # don't run the last part, if queue was empty
        # if prompt didn't changed, return the same reply again (simple cashing)
        # useful if you press the hotkey by accident
        if prompt and prompt != last_prompt:
            last_prompt = prompt
            reply = gpt.ask(prompt)
        output_queue.put(reply)

def notify(title, body):
    os.system(f"terminal-notifier -title {title} -message {body}")

class ClipGPT:
    def __init__(self, config_file):
        self._init_chatGPT()
        self._init_hotkey_listener(config_file)

    def _init_chatGPT(self):
        self.input_q = queue.Queue()
        self.output_q = queue.Queue()
        self.stop_event = threading.Event()
        self.chatgpt = threading.Thread(target=chatgpt_thread, args=(self.input_q, self.output_q, self.stop_event))

    def _init_hotkey_listener(self, config_file):
        def exit_program(self):
            self.stop()
        def on_activate(phrase):
            notify(NOTIFICATION_SEND_TITLE, NOTIFICATION_SEND_BODY)
            content = pyperclip.paste()
            reply = self.chat(phrase, content)
            pyperclip.copy(reply.replace('"', ''))
            notify(NOTIFICATION_RECEIVED_TITLE, NOTIFICATION_RECEIVED_BODY)
        def fun_definer(p):
            return lambda: on_activate(p)
        # provide a shortcut to quit the application
        hot_key_config = {"<ctrl>+<alt>+<cmd>+e": exit_program}
        # add other shortcut of the config file
        with open(config_file) as f:
            config = json.load(f)
            for hk in config["hot_keys"]:
                hot_key_config[hk["hot_key"]] = fun_definer(hk["phrase"])
        self.key_listener = keyboard.GlobalHotKeys(hot_key_config)

    def chat(self, phrase, content):
        question = phrase + content
        self.input_q.put(question)
        return self.output_q.get()

    def run(self):
        self.chatgpt.start()
        self.key_listener.start()
        try:
            self.key_listener.join()
        finally:
            self.stop()
    
    def stop(self):
        notify(NOTIFICATION_EXIT_TITLE, NOTIFICATION_EXIT_BODY)
        self.key_listener.stop()
        self.stop_event.set()
        self.chatgpt.join()

def main():
    clip = ClipGPT('config.json')
    clip.run()

if __name__ == '__main__':
    main()
