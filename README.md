# ClipGPT

The ClipGPT is a Python tool that allows users to easily process text from their clipboard using the ChatGPT language model. Simply copy the desired text, run your clipboard content through chatGPT with customisable commands, and the processed output will be put back into your clipboard.

## Installation

### Prerequisites

- Git
- Python 3 (tested with 3.11.)
- Following modules has to be installed alongside python:
  - pyperclip
  - pynput
  - chatgpt_wrapper

### Instruction

Clone the repository:

```
git clone https://github.com/iamolihe/ClipGPT.git
```

Follow the installation instruction from chatgpt_wrapper.

Done.

## Usage

### 1. Define your shortcuts

Open the file `config.json` and add your desired shortcuts. The keys  definement must be aligned with the pynput python library. Here are a few examples:

- Alt: `<alt>
- CMD: `<cmd>

### 2. Start the application

You can start the application by running the launcher file in the terminal.

> ./launcher.sh

### 3. Login into ChatGPT

After launching an explorer will open with the chatGPT website. Log in with your credentials and close the window.
Then type into the terminal application `exit`.

### 4. Transform your Text with ChatGPT

Copy the text you want to transform into the clipboard (`<cmd>+c`) and press your defined shortcut. You will receive a notification when your text is transformed and put back into your clipboard. Simply past the text with `<cmd>+v` to the desired location. Done.

### 5. Terminate the application

The shortcut `<ctrl>+<alt>+<cmd>+e`is predefined so terminate the running application.


## WIP
More Infos will follow soon...
