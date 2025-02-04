

"""
Test suite for the summarize_transcripts module.
"""
import os
import unittest
from unittest.mock import patch
from unittest import mock
from dotenv import load_dotenv
from utils.summarize_transcripts import get_ai_extract

load_dotenv()
GEMINI_API_KEY = os.environ.get('GEMINI_API_KEY')


class TestGetAIExtract(unittest.TestCase):
    """
    Test case for the get_ai_extract function.
    """

    def test_prompt_blank(self):
        """
        Test when the prompt is blank.
        """
        with self.assertRaises(ValueError):
            get_ai_extract('', 'hello')

    def test_text_blank(self):
        """
        Test when the text is blank.
        """
        with self.assertRaises(ValueError):
            get_ai_extract('hello','')

    @patch('utils.summarize_transcripts.genai_model.generate_content')
    def test_api_call(self, mock_generate_content):
        """
        Test API call behavior.
        """

        mock_response = mock.Mock(return_value=None)
        mock_response.candidates = [
            mock.Mock(content=mock.Mock(parts=[mock.Mock(text='rocks')])),
            # You can add more mock candidates if needed
        ]

        mock_generate_content.return_value = mock_response

        result = get_ai_extract('What is the last word of the sentence', 'tldw rocks')
        self.assertEqual(result, 'rocks')

    # def test_get_ai_extract_smoke(self):
    #     # Input data
    #     prompt = "What is the second letter of the word"
    #     text = "Seattle"

    #     # Call the function
    #     result = get_ai_extract(prompt, text)

    #     # Assert that the result is not empty
    #     self.assertNotEqual(result, "", "Result should not be empty.")

    @patch('utils.summarize_transcripts.genai_model.generate_content')
    def test_api_health(self, mock_generate_content):
        """
        Test API mock behavior.
        """
        # Set up mock response
        mock_response = mock.Mock()
        mock_response.status_code = 200
        # Return a list of mock candidates
        mock_response.candidates = [
            mock.Mock(content=mock.Mock(parts=[mock.Mock(text='Mock response text')])),
            # Add more mock candidates if needed
        ]

        # Configure the mock to return the mock response
        mock_generate_content.return_value = mock_response

        # Call the function
        prompt = "What is the last word of sentence"
        text = "UW is best"
        result = get_ai_extract(prompt, text)

        # Assert that the result is not empty
        self.assertNotEqual(result, "", "Result should not be empty.")
        # Add more assertions if needed
