

class LoggerMixin:

    def log(self, text):
        self.app.after(
            0,
            lambda: (
                self.log_box.insert("end", text + "\n"),
                self.log_box.see("end")
            )
        )
        
        