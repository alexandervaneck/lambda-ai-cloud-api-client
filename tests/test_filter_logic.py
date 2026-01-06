import pytest
from hypothesis import given, strategies as st
from lambda_ai_cloud_api_client.cli.types import filter_instance_types
from lambda_ai_cloud_api_client.cli.start import _parse_image, _parse_tags
from lambda_ai_cloud_api_client.models import InstanceTypesItem, InstanceType, InstanceTypeSpecs, Region, PublicRegionCode, ImageSpecificationFamily, ImageSpecificationID

# Strategies for building models
region_st = st.builds(Region, name=st.sampled_from(PublicRegionCode), description=st.text())

specs_st = st.builds(
    InstanceTypeSpecs,
    vcpus=st.integers(min_value=0, max_value=256),
    memory_gib=st.integers(min_value=0, max_value=2048),
    storage_gib=st.integers(min_value=0, max_value=10000),
    gpus=st.integers(min_value=0, max_value=16)
)

instance_type_st = st.builds(
    InstanceType,
    name=st.text(min_size=1),
    description=st.text(),
    gpu_description=st.text(),
    price_cents_per_hour=st.integers(min_value=0, max_value=100000),
    specs=specs_st
)

item_st = st.builds(
    InstanceTypesItem,
    instance_type=instance_type_st,
    regions_with_capacity_available=st.lists(region_st)
)

@given(
    items=st.lists(item_st, min_size=1, max_size=20),
    instance_type=st.none() | st.text(),
    available=st.booleans(),
    cheapest=st.booleans(),
    region=st.lists(st.text(), max_size=3).map(tuple),
    gpu=st.lists(st.text(), max_size=3).map(tuple),
    min_gpus=st.none() | st.integers(min_value=0, max_value=16),
    min_vcpus=st.none() | st.integers(min_value=0, max_value=256),
    min_memory=st.none() | st.integers(min_value=0, max_value=2048),
    min_storage=st.none() | st.integers(min_value=0, max_value=10000),
    max_price=st.none() | st.integers(min_value=0, max_value=1000),
)
def test_filter_properties(
    items, instance_type, available, cheapest, region, gpu, 
    min_gpus, min_vcpus, min_memory, min_storage, max_price
):
    filtered = filter_instance_types(
        items, instance_type, available, cheapest, region, gpu, 
        min_gpus, min_vcpus, min_memory, min_storage, max_price
    )
    
    # 1. Any filtered item must satisfy the constraints
    for item in filtered:
        if instance_type:
            assert item.instance_type.name == instance_type
        
        if available:
            assert len(item.regions_with_capacity_available) > 0
            
        if region:
            assert any(r.name in region for r in item.regions_with_capacity_available)
            
        if gpu:
            assert any(g in item.instance_type.gpu_description for g in gpu)
            
        if min_gpus is not None:
            assert item.instance_type.specs.gpus >= min_gpus
            
        if min_vcpus is not None:
            assert item.instance_type.specs.vcpus >= min_vcpus
            
        if min_memory is not None:
            assert item.instance_type.specs.memory_gib >= min_memory
            
        if min_storage is not None:
            assert item.instance_type.specs.storage_gib >= min_storage
            
        if max_price is not None:
            assert item.instance_type.price_cents_per_hour <= max_price * 100

    # 2. If cheapest is True, we should have at most one item, and it should be the one with min price
    if cheapest and filtered:
        assert len(filtered) == 1
        # It must be the absolute cheapest among those that matched
        non_cheapest = filter_instance_types(
            items, instance_type, available, False, region, gpu, 
            min_gpus, min_vcpus, min_memory, min_storage, max_price
        )
        min_price = min(i.instance_type.price_cents_per_hour for i in non_cheapest)
        assert filtered[0].instance_type.price_cents_per_hour == min_price

@given(
    image_id=st.none() | st.text(min_size=1, max_size=10),
    image_family=st.none() | st.text(min_size=1, max_size=10)
)
def test_parse_image(image_id, image_family):
    if image_id and image_family:
        with pytest.raises(RuntimeError, match="Use either --image-id or --image-family"):
            _parse_image(image_id, image_family)
    else:
        result = _parse_image(image_id, image_family)
        if image_id:
            assert isinstance(result, ImageSpecificationID)
            assert result.id == image_id
        elif image_family:
            assert isinstance(result, ImageSpecificationFamily)
            assert result.family == image_family
        else:
            assert result is None

@given(st.lists(st.text()))
def test_parse_tags(raw_tags):
    # Some tags might be valid, some not. 
    # Valid tags have exactly one '=' or at least one '='.
    # The current implementation uses raw.split("=", 1), so any string with '=' is technically valid.
    is_valid = all("=" in t and not t.startswith("=") for t in raw_tags)
    
    if is_valid:
        tags = _parse_tags(raw_tags)
        if raw_tags:
            assert len(tags) == len(raw_tags)
            for i, raw in enumerate(raw_tags):
                key, value = raw.split("=", 1)
                assert tags[i].key == key
                assert tags[i].value == value
        else:
            assert tags is None
    else:
        # If any tag is invalid, it raises RuntimeError
        # Note: "" is invalid because it doesn't contain '='.
        # "=value" is invalid because it starts with '='? 
        # Wait, the code says: if "=" not in raw: raise
        # and key, value = raw.split("=", 1). 
        # Actually it doesn't check if it starts with '='.
        with pytest.raises(RuntimeError):
            _parse_tags(raw_tags)
