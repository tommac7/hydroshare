import json
import jsonschema

from django import forms


class ModelProgramMetadataValidationForm(forms.Form):
    version = forms.CharField(required=False, max_length=250)
    release_date = forms.DateField(required=False)
    website = forms.URLField(required=False, max_length=255)
    code_repository = forms.URLField(required=False, max_length=255)
    programming_languages = forms.CharField(required=False)
    operating_systems = forms.CharField(required=False)
    mi_json_schema = forms.CharField(max_length=5000, required=False)

    def clean_version(self):
        version = self.cleaned_data['version'].strip()
        return version

    def clean_programming_languages(self):
        langauge_string = self.cleaned_data['programming_languages']
        if langauge_string:
            # generate a list of strings
            languages = langauge_string.split(',')
            languages = [lang.strip() for lang in languages]
            return languages
        return langauge_string

    def clean_operating_systems(self):
        os_string = self.cleaned_data['operating_systems']
        if os_string:
            # generate a list of strings
            op_systems = os_string.split(',')
            op_systems = [op.strip() for op in op_systems]
            return op_systems
        return []

    def clean_mi_json_schema(self):
        # TODO: more validation of json schema needs to be implemented once we define the requirements of the schema
        json_schema_string = self.cleaned_data['mi_json_schema'].strip()
        json_schema = dict()
        if json_schema_string:
            try:
                json_schema = json.loads(json_schema_string)
            except ValueError as exp:
                self.add_error('mi_json_schema', "Not valid json data")

            if json_schema:
                try:
                    jsonschema.Draft4Validator.check_schema(json_schema)
                except jsonschema.SchemaError as ex:
                    self.add_error('mi_json_schema', "Not a valid json schema.{}".format(ex.message))

        return json_schema

    def update_metadata(self, metadata):
        metadata.version = self.cleaned_data['version']
        metadata.website = self.cleaned_data['website']
        metadata.code_repository = self.cleaned_data['code_repository']
        metadata.release_date = self.cleaned_data['release_date']
        metadata.operating_systems = self.cleaned_data['operating_systems']
        metadata.programming_languages = self.cleaned_data['programming_languages']
        metadata.save()
        logical_file = metadata.logical_file
        logical_file.mi_schema_json = self.cleaned_data['mi_json_schema']
        logical_file.save()
