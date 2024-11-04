
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
        
        self.image = cv2.imread(file_path)
        
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
    
    def get_colorful_image_string(self, terminal_character_width: float=(os.get_terminal_size()[0] * 0.6)) -> str:
        """
        Get the colorful string representing the image in with ASCII character.
        Optionally pass the terminal width (in characters) to adjust the size of the image.
        By default it uses the 60% of the width of the terminal as the width of the ASCII image.
        """
        if self.image is None:
            return "Could not read the image."
                
        
        width_of_resclaed_image = int(terminal_character_width)
        height_of_rescaled_image = int(terminal_character_width * 0.45)
        
        
        rescaled_image_size = width_of_resclaed_image, height_of_rescaled_image
        
        rescaled_image = cv2.resize(self.image, rescaled_image_size)
        
        image_string = ""
        
        for row_of_image in rescaled_image:
            for rgb_value in row_of_image:
                character = self.get_character_for_rgb_value(rgb_value)
                image_string += character
            image_string += "\033[39m\033[49m\n"
        
        return image_string
    
    def get_gery_scale_image_string(self, terminal_character_width: float=(os.get_terminal_size()[0] * 0.3)) -> str:
        """
        Get the string representing the image in with ASCII character.
        Optionally pass the terminal size (in characters) to adjust the size of the image.
        By default it uses the 60% of the width of the terminal as the width of the ASCII image.
        """
        
        if self.image is None:
            return "Could not read the image."
        
        width_of_resclaed_image = int(terminal_character_width)
        height_of_rescaled_image = width_of_resclaed_image // 3
        
        
        rescaled_image_size = width_of_resclaed_image, height_of_rescaled_image
        
        rescaled_image = cv2.resize(self.image, rescaled_image_size)
        
        image_string = ""
        
        for row_of_image in cv2.cvtColor(rescaled_image, cv2.COLOR_BGR2GRAY):
            for grey_scale_value in row_of_image:
                character = self.get_character_for_gery_scale_value(grey_scale_value)
                image_string += character
            image_string += "\n"
        
        return image_string
        
    
    def get_character_for_gery_scale_value(self, grey_scale_value: int) -> str:
        normalized_grey_scale_value = grey_scale_value / 256.0
        index_of_ascii_character = int(len(self.CHARACTERS) * normalized_grey_scale_value)
        corresponding_ascii_character = self.CHARACTERS[index_of_ascii_character]
        
        return corresponding_ascii_character
        
    
    def get_character_for_rgb_value(self, rgb_value) -> str:
        blue, green, red = rgb_value
        if blue == green == red == 0: return "\033[39m\033[49m"+' '
        return f"\033[38;2;{red};{green};{blue}m" + self.get_character_for_gery_scale_value(self.rgb_to_grey_scale(red, green, blue))
        # return f"\033[38;2;{red};{green};{blue};48;2;{red};{green};{blue}m#"
        
    def rgb_to_grey_scale(self, red, green, blue) -> int:
        return int(0.299 * red + 0.587 * green + 0.114 * blue)