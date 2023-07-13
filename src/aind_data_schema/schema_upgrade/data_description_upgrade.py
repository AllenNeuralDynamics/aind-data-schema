"""Module to contain code to upgrade old data description models"""
from copy import deepcopy
from typing import Any, Optional, Union

from aind_data_schema.data_description import DataDescription, Funding, Institution, Modality


class ModalityUpgrade:
    """Handle upgrades for Modality models."""

    @staticmethod
    def upgrade_modality(old_modality: Union[str, dict, Modality, None]) -> Optional[Modality]:
        """
        Converts old modality models into the current model.
        Parameters
        ----------
        old_modality : Union[str, dict, Modality, None]
          Old models may consist of strings or dictionaries.

        Returns
        -------
        Modality
          Will raise a validation error if unable to parse old modalities.

        """
        if type(old_modality) is str or type(old_modality) is dict:
            return Modality(old_modality)
        elif type(old_modality) is Modality:
            return old_modality
        else:
            return None


class FundingUpgrade:
    """Handle upgrades for Funding models."""

    @staticmethod
    def upgrade_funding(old_funding: Any) -> Optional[Funding]:
        """Map legacy Funding model to current version"""
        if type(old_funding) == Funding:
            return old_funding
        elif type(old_funding) == dict and old_funding.get("funder") is not None and type(old_funding["funder"]) == str:
            old_funder = old_funding.get("funder")
            map_full_name_to_institute = dict(
                [(Institution.__members__[m].value.name, Institution.__members__[m]) for m in Institution.__members__]
            )
            if map_full_name_to_institute.get(old_funder) is not None:
                new_funder = map_full_name_to_institute.get(old_funder)
            else:
                new_funder = Institution(old_funder)
            new_funding = deepcopy(old_funding)
            new_funding["funder"] = new_funder
            return Funding.parse_obj(new_funding)
        elif (
            type(old_funding) == dict and old_funding.get("funder") is not None and type(old_funding["funder"]) == dict
        ):
            return Funding.parse_obj(old_funding)
        else:
            return None


class InstitutionUpgrade:
    """Handle upgrades for Institution class"""

    @staticmethod
    def upgrade_institution(old_institution: Any) -> Optional[Institution]:
        """Map legacy Institution model to current version"""
        if type(old_institution) == str:
            return Institution(old_institution)
        elif type(old_institution) == dict and old_institution.get("abbreviation") is not None:
            return Institution(old_institution.get("abbreviation"))
        else:
            return None


class DataDescriptionUpgrade:
    """Handle upgrades for DataDescription class"""

    def __init__(self, old_data_description_model: DataDescription):
        """
        Handle mapping of old DataDescription models into current models
        Parameters
        ----------
        old_data_description_model : DataDescription
        """
        self.old_data_description_model = old_data_description_model

    @staticmethod
    def _get_or_default(data_description: DataDescription, field_name: str, kwargs: dict) -> Any:
        """
        If field is not explicitly set, will attempt to extract from a model.
        If field is not found in old model, will attempt to set using the default.
        Parameters
        ----------
        data_description : DataDescription
          Old model to extract value
        field_name : str
          Name of the field
        kwargs : dict
          Explicit args that will override everything else

        Returns
        -------
        Any

        """
        if kwargs.get(field_name) is not None:
            return kwargs.get(field_name)
        elif hasattr(data_description, field_name) and getattr(data_description, field_name) is not None:
            return getattr(data_description, field_name)
        else:
            return getattr(DataDescription.__fields__.get(field_name), "default")

    def upgrade_data_description(self, **kwargs) -> DataDescription:
        """Upgrades the old model into the current version"""
        institution = InstitutionUpgrade.upgrade_institution(
            self._get_or_default(self.old_data_description_model, "institution", kwargs)
        )
        funding_source = self._get_or_default(self.old_data_description_model, "funding_source", kwargs)
        funding_source = [FundingUpgrade.upgrade_funding(funding) for funding in funding_source]
        old_modality: Any = self.old_data_description_model.modality
        if kwargs.get("modality") is not None:
            modality = kwargs["modality"]
        elif type(old_modality) == str or type(old_modality) == dict:
            modality = [ModalityUpgrade.upgrade_modality(old_modality)]
        elif type(old_modality) == list:
            modality = [ModalityUpgrade.upgrade_modality(m) for m in old_modality]
        else:
            modality = getattr(DataDescription.__fields__.get("modality"), "default")

        return DataDescription(
            creation_time=self._get_or_default(self.old_data_description_model, "creation_time", kwargs),
            creation_date=self._get_or_default(self.old_data_description_model, "creation_date", kwargs),
            name=self._get_or_default(self.old_data_description_model, "name", kwargs),
            institution=institution,
            funding_source=funding_source,
            data_level=self._get_or_default(self.old_data_description_model, "data_level", kwargs),
            group=self._get_or_default(self.old_data_description_model, "group", kwargs),
            investigators=self._get_or_default(self.old_data_description_model, "investigators", kwargs),
            project_name=self._get_or_default(self.old_data_description_model, "project_name", kwargs),
            project_id=self._get_or_default(self.old_data_description_model, "project_id", kwargs),
            restrictions=self._get_or_default(self.old_data_description_model, "restrictions", kwargs),
            modality=modality,
            experiment_type=self._get_or_default(self.old_data_description_model, "experiment_type", kwargs),
            subject_id=self._get_or_default(self.old_data_description_model, "subject_id", kwargs),
            related_data=self._get_or_default(self.old_data_description_model, "related_data", kwargs),
            data_summary=self._get_or_default(self.old_data_description_model, "data_summary", kwargs),
        )
