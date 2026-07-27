def test_package_can_be_imported() -> None:
    import retail_demand

    assert retail_demand.__version__ == "0.1.0"
