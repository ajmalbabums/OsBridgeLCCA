from abc import ABC, abstractmethod

class CostComponent(ABC):
    """Abstract Base Class for different cost components in Life Cycle Cost Analysis."""

    def __init__(self, amount, category, is_initial, is_recurring, pwf):
        """
        Initialize a generic cost component.

        :param amount: Cost amount in INR
        :param category: Economic, Environmental, or Social
        :param is_initial: True if an initial cost, False if future cost
        :param is_recurring: True if recurring, False if one-time
        :param pwf: Discounting factor for future costs
        """
        self.amount = None
        self.category = category
        self.is_initial = None
        self.is_recurring = None
        self.pwf = None

    @abstractmethod
    def calculate_cost(self):
        """Abstract method to be implemented by subclasses for cost calculation."""
        pass


def calculate_pwf(discount_rate, design_life, is_initial=False, is_recurring=True, interval=1, future_year=None):
    """
    Calculates the Present Worth Factor (PWF) based on cost type.

    :param discount_rate: Discount rate (decimal form, e.g., 0.05 for 5%).
    :param design_life: Total design life in years.
    :param is_initial: True for initial cost (PWF = 1).
    :param is_recurring: True for recurring costs.
    :param interval: Interval in years for recurring costs (default is 1).
    :param future_year: Year when a non-recurring future cost occurs.
    :return: Present Worth Factor (PWF).
    """
    if is_initial:
        return 1.0  # Initial cost has no discounting

    elif not is_recurring:
        if future_year is None:
            raise ValueError("future_year must be provided for non-recurring future costs")
        return 1 / ((1 + discount_rate) ** future_year)

    else:
        if interval is None:
            raise ValueError("interval must be provided for recurring costs")
        return sum(1 / ((1 + discount_rate) ** (i * interval)) for i in range(1, int(design_life / interval) + 1))


class InitialConstructionCost(CostComponent):
    def __init__(self, quantity, rate):
        super().__init__(amount=quantity * rate, category="Economic", is_initial=True, is_recurring=False, pwf=1.00)
        self.quantity = quantity
        self.rate = rate

    def calculate_cost(self):
        return self.quantity * self.rate * self.pwf


class InitialCarbonEmissionCost(CostComponent):
    def __init__(self, material_quantity, carbon_emission_factor, carbon_cost):
        super().__init__(amount=(material_quantity * carbon_emission_factor) * carbon_cost, category="Environmental", is_initial=True, is_recurring=False, pwf=1.00)

    def calculate_cost(self):
        return self.amount


class TimeCost(CostComponent):
    def __init__(self, construction_cost, interest_rate, time, investment_ratio):
        cost = construction_cost * interest_rate * time * investment_ratio
        super().__init__(amount=cost, category="Economic", is_initial=True, is_recurring=False, pwf=1.00)

    def calculate_cost(self):
        return self.amount


class RoadUserCost(CostComponent):
    def __init__(self, vehicles_affected, vehicle_operation_cost, construction_time):
        cost = vehicles_affected * vehicle_operation_cost * construction_time
        super().__init__(amount=cost, category="Economic", is_initial=True, is_recurring=False, pwf=1.00)

    def calculate_cost(self):
        return self.amount


class AdditionalCarbonEmissionCost(CostComponent):
    def __init__(self, vehicles_affected, reroute_distance, co2_emission_per_km, carbon_cost):
        cost = vehicles_affected * reroute_distance * co2_emission_per_km * carbon_cost
        super().__init__(amount=cost, category="Environmental", is_initial=True, is_recurring=False, pwf=1.00)

    def calculate_cost(self):
        return self.amount


class PeriodicMaintenanceCost(CostComponent):
    def __init__(self, maintenance_cost_rate, construction_cost, discount_rate, period, design_life):
        pwf = calculate_pwf(discount_rate, period, design_life)
        cost = maintenance_cost_rate * construction_cost * pwf
        super().__init__(amount=cost, category="Economic", is_initial=False, is_recurring=True, pwf=pwf)

    def calculate_cost(self):
        return self.amount


class PeriodicMaintenanceCarbonCost(CostComponent):
    def __init__(self, material_quantity, carbon_emission_factor, carbon_cost, discount_rate, period, design_life):
        pwf = calculate_pwf(discount_rate, period, design_life)
        cost = material_quantity * carbon_emission_factor * carbon_cost * pwf
        super().__init__(amount=cost, category="Environmental", is_initial=False, is_recurring=True, pwf=pwf)

    def calculate_cost(self):
        return self.amount


class RoutineInspectionCost(CostComponent):
    def __init__(self, quantity, rate, discount_rate, design_life):
        pwf = calculate_pwf(discount_rate, 1, design_life)
        cost = quantity * rate * pwf
        super().__init__(amount=cost, category="Economic", is_initial=False, is_recurring=True, pwf=pwf)

    def calculate_cost(self):
        return self.amount


class RepairAndRehabilitationCost(CostComponent):
    def __init__(self, repair_cost_rate, construction_cost, discount_rate, period, design_life):
        pwf = calculate_pwf(discount_rate, period, design_life)
        cost = repair_cost_rate * construction_cost * pwf
        super().__init__(amount=cost, category="Economic", is_initial=False, is_recurring=True, pwf=pwf)

    def calculate_cost(self):
        return self.amount


class DemolitionCost(CostComponent):
    def __init__(self, demolition_rate, construction_cost, discount_rate, design_life):
        pwf = 1 / ((1 + discount_rate) ** design_life)
        cost = demolition_rate * construction_cost * pwf
        super().__init__(amount=cost, category="Economic", is_initial=False, is_recurring=False, pwf=pwf)

    def calculate_cost(self):
        return self.amount


class RecyclingCost(CostComponent):
    def __init__(self, scrap_value, quantity, discount_rate, design_life):
        pwf = 1 / ((1 + discount_rate) ** design_life)
        cost = scrap_value * quantity * pwf
        super().__init__(amount=cost, category="Economic", is_initial=False, is_recurring=False, pwf=pwf)

    def calculate_cost(self):
        return self.amount
