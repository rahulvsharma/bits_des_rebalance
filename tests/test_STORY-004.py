import pytest

class MockAsset:
    def __init__(self, symbol, current, target):
        self.symbol = symbol
        self.current_allocation = current
        self.target_allocation = target

@pytest.fixture
def unbalanced_portfolio():
    return [
        MockAsset("AAPL", 50, 30),
        MockAsset("GOOGL", 20, 40),
        MockAsset("MSFT", 30, 30)
    ]

def test_rebalancing_calculation(unbalanced_portfolio):
    actions = []
    for asset in unbalanced_portfolio:
        diff = asset.target_allocation - asset.current_allocation
        if abs(diff) > 1:
            actions.append({"symbol": asset.symbol, "diff": diff})
    assert len(actions) == 2

def test_rebalancing_totals():
    assets = [
        MockAsset("AAPL", 50, 30),
        MockAsset("GOOGL", 20, 40),
        MockAsset("MSFT", 30, 30)
    ]
    current_sum = sum(a.current_allocation for a in assets)
    target_sum = sum(a.target_allocation for a in assets)
    assert current_sum == 100
    assert target_sum == 100

def test_rebalancing_actions():
    assets = [MockAsset("AAPL", 50, 30)]
    diff = assets[0].target_allocation - assets[0].current_allocation
    assert diff == -20
