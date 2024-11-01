import os
import unittest


import sys

sys.path.append('.')
from pet.pet import Image


class TestImages(unittest.TestCase):
    def test_get_file_path(self) -> None:
        file_path: str = "./pet/vendor/rose.png"
        image: Image = Image(file_path)
        
        self.assertEqual(image.get_file_path(), file_path)
    
    def tes_show_image(self) -> None:
        file_path: str = "./pet/vendor/rose.png"
        image: Image = Image(file_path)
        
        self.assertEqual(image.show_image(), "success")
        
        print(image.image.shape)
    
    
    def test_get_character_for_gery_scale_value(self) -> None:
        CHARACTERS: str = " `.-':_,^=;><+!rc*/z?sLTv)J7(|Fi{C}fI31tlu[neoZ5Yxjya]2ESwqkP6h9d4VpOGbUAKXHm8RD#$Bg0MNWQ%&@"
        length_of_characters = len(CHARACTERS)
        
        file_path: str = "./pet/vendor/rose.png"
        image: Image = Image(file_path)
        
        self.assertEqual(' ', image.get_character_for_gery_scale_value(0))
        self.assertEqual('@', image.get_character_for_gery_scale_value(255))
        # self.assertEqual(CHARACTERS[length_of_characters // 2], image.get_character_for_gery_scale_value(127))
        # 
    
    def test_image_string(self) -> None:
        file_path: str = "./pet/vendor/rose.png"
        image: Image = Image(file_path)
        
        print(image.get_colorful_image_string())
    
    # def test_image_string_invalid(self) -> None:
    #     file_path: str = "./pet/vendor/doesnotexist.png"
    #     image: Image = Image(file_path)
        
    #     self.assertEqual(image.get_image_string(), "Could not read the image.")


if __name__ == "__main__":
    unittest.main()