from typing import Any, Type

from aind_data_schema.base import AindModel


class BaseModelUpgrade:
    """Base class for handling upgrades for models"""

    def __init__(self, old_model: AindModel, model_class: Type[AindModel]):
        """
        Handle mapping of old AindModel model versions into current models

        Parameters
        ----------
        old_data_description_model : DataDescription
        """
        self.old_model = old_model
        self.model_class = model_class

    def _get_or_default(self, model: AindModel, field_name: str, kwargs: dict) -> Any:
        """
        If field is not explicitly set, will attempt to extract from a model.
        If field is not found in old model, will attempt to set using the default.

        Parameters
        ----------
        model : AindModel
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
        elif hasattr(model, field_name) and getattr(model, field_name) is not None:
            return getattr(model, field_name)
        else:
            try:
                return getattr(self.model_class.__fields__.get(field_name), "default")
            except AttributeError:
                return None

    def upgrade(self, **kwargs) -> AindModel:
        """Upgrades the old model into the current version"""
        raise NotImplementedError