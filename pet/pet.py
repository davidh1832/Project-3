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
    
    
    def __init__(self, name="Soobin", smiling_dog="/.pet/vendor/similing_dog.png", walking_dog="./pet/vendor/dog.png", barking_dog="./pet/vendor/barking_dog.png") -> None:
        self.name = name
        self.smiling_dog_image = Image(smiling_dog)
        self.walking_dog_image = Image(walking_dog)
        self.barking_dog_image = Image(barking_dog)
        
        
    def get_name(self) -> str:
        """
        Returns the name of the pet. The default name is Soobin
        """
        return self.name
    
    def get_walking_image(self) -> str:
        """
        Returns a string that looks like the image of a walking dog.
        """
        return self.walking_dog_image.get_image_string()
        
    def get_barking_image(self) -> str:
        """
        Returns a string that looks like the image of a barking dog.
        """
        return self.barking_dog_image.get_image_string()
    
    def get_smiling_image(self) -> str:
        """
        Returns a string that looks like the image of a smiling dog.
        """
        return self.smiling_dog_image.get_image_string()