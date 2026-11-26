class Body:
    """A physical body that can receive or give off heat."""

    def __init__(self, mass, specific_heat, temperature):
        # Check that all values are valid
        if mass <= 0:
            raise ValueError("mass must be greater than 0")
        if specific_heat <= 0:
            raise ValueError("specific_heat must be greater than 0")
        if temperature < 0:
            raise ValueError("temperature must be 0 or above")

        self.mass = mass                    # kg
        self.specific_heat = specific_heat  # J/(kg*C)
        self.temperature = temperature      # degrees Celsius

    def add_heat(self, heat):
        """Add heat (in Joules) to the body. Negative heat means the body loses heat.
        Returns the new temperature."""
        # Q = m * c * dT  ->  dT = Q / (m * c)
        delta_t = heat / (self.mass * self.specific_heat)
        self.temperature = self.temperature + delta_t
        return self.temperature


if __name__ == "__main__":
    body = Body(100, 0.15, 200)
    print(body.add_heat(20))   # about 201.333
    print(body.add_heat(-40))  # about 198.667
