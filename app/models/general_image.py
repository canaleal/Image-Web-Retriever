class GeneralImage:

    def __init__(self, name, container_link, image_link):
        self.name = name
        self.container_link = container_link
        self.image_link = image_link
    
    def __sizeof__(self) -> int:
        return len(self.__str__())
    
    def __str__(self) -> str:
        return f'{self.name} {self.container_link} {self.image_link}'