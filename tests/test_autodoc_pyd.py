

class AudtodocTests(unittest.TestCase):

    def test_autodoc_pydantic_model_summary_list_order_alphabetical(autodocument):

        # explict global
        actual = autodocument(
            documenter='pydantic_model',
            object_path='target.configuration.ModelSummaryListOrder',
            options_app={
                "autodoc_pydantic_model_show_validator_summary": True,
                "autodoc_pydantic_model_show_field_summary": True,
                "autodoc_pydantic_model_summary_list_order": "alphabetical"},
            deactivate_all=True)
        assert result == actual