import webview


def main():
    webview.create_window("Hello world", "https://pywebview.flowrl.com/")
    webview.start()


if __name__ == "__main__":
    main()
