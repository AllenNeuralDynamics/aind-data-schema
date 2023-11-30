# """Module to contain code to upgrade old processing models"""
#
# from aind_data_schema.processing import DataProcess, PipelineProcess, Processing
#
# from .base_upgrade import AindModel, BaseModelUpgrade
#
#
# class DataProcessUpgrade(BaseModelUpgrade):
#     """Handle upgrades for DataProcess class"""
#
#     def __init__(self, old_data_process_model: DataProcess):
#         """
#         Handle mapping of old DataProcess models into current models
#
#         Parameters
#         ----------
#         old_data_process_model : DataProcess
#         """
#         super().__init__(old_model=old_data_process_model, model_class=DataProcess)
#
#     def upgrade(self, **kwargs) -> AindModel:
#         """Upgrades the old model into the current version"""
#         version = self._get_or_default(self.old_model, "version", kwargs)
#         software_version = self._get_or_default(self.old_model, "software_version", kwargs)
#         data_process_dict = self.old_model.dict()
#         if version is not None and software_version is None:
#             software_version = version
#             data_process_dict["software_version"] = software_version
#             del data_process_dict["version"]
#         # Empty notes with 'Other' name is not allowed in the new schema
#         name = self._get_or_default(self.old_model, "name", kwargs)
#         notes = self._get_or_default(self.old_model, "notes", kwargs)
#         if name == "Other" and notes is None:
#             data_process_dict["notes"] = "missing notes"
#
#         return DataProcess(**data_process_dict)
#
#
# class ProcessingUpgrade(BaseModelUpgrade):
#     """Handle upgrades for Processing class"""
#
#     def __init__(self, old_processing_model: Processing):
#         """
#         Handle mapping of old Processing models into current models
#
#         Parameters
#         ----------
#         old_processing_model : Processing
#             The old model to upgrade
#         """
#         super().__init__(old_model=old_processing_model, model_class=Processing)
#
#     def upgrade(self, **kwargs) -> AindModel:
#         """Upgrades the old model into the current version"""
#         # old versions of the schema (<0.3.0) had data_processes directly
#         schema_version = self.old_model.schema_version
#         if schema_version is None or schema_version < "0.3.0":
#             data_processes = self._get_or_default(self.old_model, "data_processes", kwargs)
#             pipeline_version = self._get_or_default(self.old_model, "pipeline_version", kwargs)
#             pipeline_url = self._get_or_default(self.old_model, "pipeline_version", kwargs)
#
#             if data_processes is not None:
#                 # upgrade data processes
#                 data_processes_new = [
#                     DataProcessUpgrade(DataProcess.construct(**data_process)).upgrade()
#                     for data_process in data_processes
#                 ]
#                 processor_full_name = kwargs.get("processor_full_name")
#                 processing_pipeline = PipelineProcess(
#                     pipeline_version=pipeline_version,
#                     pipeline_url=pipeline_url,
#                     data_processes=data_processes_new,
#                     processor_full_name=processor_full_name,
#                 )
#         else:
#             processing_pipeline = self._get_or_default(self.old_model, "processing_pipeline", kwargs)
#
#         return Processing(
#             processing_pipeline=processing_pipeline,
#             analyses=self._get_or_default(self.old_model, "analyses", kwargs),
#             notes=self._get_or_default(self.old_model, "notes", kwargs),
#         )
