def add_settings(title, geomety = '400x200+200+100', icon_path = "data/test_axe.ico"):
    def class_decorator(class_to_decorate):
        class DecoratedClass(class_to_decorate):
            def __init__(self, *args, **kwargs):
                super().__init__(*args, **kwargs)
                self.title(title)
                self.iconbitmap(icon_path)
                self.geometry(geomety)

        return DecoratedClass
    return class_decorator