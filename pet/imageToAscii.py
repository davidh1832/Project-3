
# from typing_extensions import Optional
import cv2

import os
### This module should be able to convert a given image into ascii art 
### Input:
### 1 .Need to know the number of characters that can be printed on the screen
### 2. Need to know what image to print


class Image:
    
    """
    The image class converts an image into ASCII art which can be printed in the console.
    In order to get an ascii art, initialize the class with the correct file path and use the method `get_image_string()` to get the ascii string.
    """
    
    CHARACTERS: str = " `.-':_,^=;><+!rc*/z?sLTv)J7(|Fi{C}fI31tlu[neoZ5Yxjya]2ESwqkP6h9d4VpOGbUAKXHm8RD#$Bg0MNWQ%&@"
    
    def __init__(self, file_path: str) -> None:
        self.file_path: str = file_path
        
        self.image = cv2.imread(file_path, cv2.IMREAD_GRAYSCALE)
        
        # print(type(self.image))
        
        # if self.image is not None: print("Success in loading image")
        
    def get_file_path(self) -> str:
        return self.file_path
        
        
    def show_image(self) -> str:
        # Display the image
        cv2.imshow("Image", self.image)
        
        # Wait for the user to press a key
        cv2.waitKey(0)
        
        # Close all windows
        cv2.destroyAllWindows()
        
        return "success"
    
    def get_image_string(self, terminal_character_size=os.get_terminal_size()) -> str:
        """
        Get the string representing the image in with ASCII character.
        Optionally pass the terminal size (in characters) to adjust the size of the image.
        By default it uses the 60% of the width of the terminal as the width of the ASCII image.
        """
        
        if self.image is None:
            return "Could not read the image."
                    
        size_of_image_in_terminal  = 0.6
        
        width_of_resclaed_image = int(os.get_terminal_size()[0] * size_of_image_in_terminal)
        height_of_rescaled_image = width_of_resclaed_image // 3
        
        
        rescaled_image_size = width_of_resclaed_image, height_of_rescaled_image
        
        rescaled_image = cv2.resize(self.image, rescaled_image_size)
        
        image_string = ""
        
        for i, row_of_image in enumerate(rescaled_image):
            for j, grey_scale_value in enumerate(row_of_image):
                character = self.get_character_for_gery_scale_value(grey_scale_value)
                image_string += character
            image_string += '\n'
        
        return image_string
        
    
    def get_character_for_gery_scale_value(self, grey_scale_value: int) -> str:
        normalized_grey_scale_value = grey_scale_value / 256.0
        index_of_ascii_character = int(len(self.CHARACTERS) * normalized_grey_scale_value)
        corresponding_ascii_character = self.CHARACTERS[index_of_ascii_character]
        
        return corresponding_ascii_character
