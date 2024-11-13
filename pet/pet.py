from typing import List
from pet.imageToAscii import Image
import sys 

class Pet:
    """
    The pet is capable of returning strings that are ASCII images. To use them simply print the returned string to the console.
    Eg.
    ```python
    my_pet = Pet("Charlie")
    print(my_pet.get_walking_image())
    ```
    """
    
    
    def __init__(self, name: str, dog_images: List[str]) -> None:
        self.name = name
        self.dog_images = dog_images
        
        
    def get_name(self) -> str:
        """
        Returns the name of the pet. The default name is Soobin
        """
        return self.name
    
    def get_image(self, index: int) -> str:
        """
        Returns a string that looks like the image of a walking dog.
        """
        return Image(self.dog_images[index]).get_image_string()