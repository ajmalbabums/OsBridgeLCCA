from core.bridge_lcc import BridgeLCC
from core.visualization import Visualization


class Controller:
    """Handles UI logic and backend integration."""

    def run_calculations(self):
        """Run LCCA calculations and display results."""
        inputs = {
            "bill_of_quantity": {"steel": 10000, "concrete": 5000},
            "maintenance_cost": 2000,
            "vehicle_operating_cost": 5000,
            "discount_rate": 0.05
        }
        lcc = BridgeLCC("Sample Project", inputs)
        results = lcc.calculate_lcc()

        fig = Visualization.plot_lcc_distribution(lcc.get_outputs())
        fig.show()
