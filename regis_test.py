import unittest
import requests
import datetime

HOST = "https://wcg-apis.herokuapp.com"
DATABASE_URL = HOST + "/citizen"
URL = HOST + "/registration"


class RegistrationTest(unittest.TestCase):
    """Unit tests for WCG API Registration"""

    def setUp(self):
        requests.delete(DATABASE_URL, data=self.citizen_setup("1103703174274", "Sirapop", "Kunjiak", "11 Jan 1993"
                                                              , "Office worker", "115/22 mock_village, mock_road, "
                                                                                 "Bangkok 10210"))
        self.user = self.citizen_setup("1103703174274", "Sirapop", "Kunjiak", "11 Jan 1993"
                                       , "Office worker", "115/22 mock_village, mock_road, "
                                                          "Bangkok 10210")

    def citizen_setup(self, citizen_id, firstname, lastname, birthdate,
                      occupation, address):
        """The setup to create citizen"""
        return {
            'citizen_id': citizen_id,
            'name': firstname,
            'surname': lastname,
            'birth_date': birthdate,
            'occupation': occupation,
            'address': address
        }

    def get_response_feedback(self, response):
        """Return the feedback from response"""
        return response.json()['feedback']

    def test_basic_registration(self):
        """Test if the registration success"""
        feedback = requests.post(URL, data=self.user)
        self.assertEqual(feedback.status_code, 200)
        self.assertEqual(self.get_response_feedback(feedback), "registration success!")

    def test_duplicate_registered(self):
        """Test registration with a already registered account"""
        feedback = requests.post(URL, data=self.user)
        feedback1 = requests.post(URL, data=self.user)
        self.assertEqual(self.get_response_feedback(feedback), "registration success!")
        self.assertEqual(self.get_response_feedback(feedback1), "registration failed: this person already registered")

    def test_missing_attribute_registration(self):
        """Test when the registration missing a attribute"""
        citizen = self.citizen_setup("1103703174274", "Sirapop", "Kunjiak", "11 Jan 1993"
                                     , "Office worker", "")
        feedback = requests.post(URL, data=citizen)
        self.assertEqual(self.get_response_feedback(feedback), "registration failed: missing some attribute")

    def test_wrong_format_birthday(self):
        """Test registration with the wrong birth format"""
        citizen = self.citizen_setup("1103703174275", "Sirapop1", "Kunjiak1", "1993 11 01", "Office worker",
                                     "115/22 mock_village, mock_road, "
                                     "Bangkok 10210")
        feedback = requests.post(URL, data=citizen)
        self.assertEqual(self.get_response_feedback(feedback), "registration failed: invalid birth date format")

    def test_wrong_citizen_id(self):
        """Test registration with the invalid citizen id"""
        citizen = self.citizen_setup("110370", "Sirapop1", "Kunjiak1", "11 Feb 1993", "Office worker",
                                     "115/22 mock_village, mock_road, "
                                     "Bangkok 10210")
        citizen1 = self.citizen_setup("ๅ/ตๅ/ค-คๅ/-", "Sirapop2", "Kunjiak2", "1 Dec 1999",
                                      "Student", "115/263 mocc_village, mocc_road, "
                                                 "Bangkok 102102")
        feedback = requests.post(URL, data=citizen)
        feedback1 = requests.post(URL, data=citizen1)
        self.assertEqual(self.get_response_feedback(feedback), "registration failed: invalid citizen ID")
        self.assertEqual(self.get_response_feedback(feedback1), "registration failed: invalid citizen ID")


if __name__ == '__main__':
    unittest.main()
