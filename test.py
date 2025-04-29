from aind_data_schema.base import DataModel
from aind_data_schema.components.wrappers import AssetPath

class TestAssetPath(DataModel):
    """Test class for AssetPath"""

    asset_path: AssetPath

model = TestAssetPath(
    asset_path=AssetPath("path/to/file.txt")
)

model2 = TestAssetPath.model_validate(model.model_dump())
model3 = TestAssetPath.model_validate_json(model.model_dump_json())

print(model.asset_path)  # Output: path/to/file.txt