import unittest

from pet.pet import Pet

class PetTesting(unittest.TestCase):

    def test_get_image(self):

        my_dog = Pet("Soobing", ["../pet/vendor/smiling_dog.png"])
        print(my_dog.get_image(0))


if __name__ == "__main__":
    unittest.main()
