import json
import numpy as np
from scipy.interpolate import interp1d
from scipy.integrate import trapezoid


def main(temperature_sets_json, heating_sets_json, rules_json, current_temperature):
    try:
        temperature_sets = json.loads(temperature_sets_json)
        heating_sets = json.loads(heating_sets_json)
        rules = json.loads(rules_json)
    except json.JSONDecodeError:
        return "Ошибка: Неверный формат JSON-строки."

    def build_membership(points):
        xs = np.array([p[0] for p in points])
        ys = np.array([p[1] for p in points])

        unique_x, idx, counts = np.unique(xs, return_index=True, return_counts=True)
        avg_y = np.array([np.mean(ys[i:i + c]) for i, c in zip(idx, counts)])

        return interp1d(unique_x, avg_y, kind="linear", fill_value="extrapolate")

    temperature_functions = {
        term["id"]: build_membership(term["points"])
        for term in temperature_sets["температура"]
    }

    heating_functions = {
        term["id"]: build_membership(term["points"])
        for term in heating_sets["температура"]
    }

    temperature_membership = {
        term_id: float(func(current_temperature))
        for term_id, func in temperature_functions.items()
    }

    heating_membership = {}
    for temp_term, heating_term in rules:
        activation = min(temperature_membership.get(temp_term, 0.0), 1.0)
        if heating_term in heating_membership:
            heating_membership[heating_term] = max(
                heating_membership[heating_term], activation
            )
        else:
            heating_membership[heating_term] = activation

    numerator = 0.0
    denominator = 0.0

    x = np.linspace(0, 26, 100)

    for term_id, degree in heating_membership.items():
        y = heating_functions[term_id](x)
        area = trapezoid(y, x)
        if area == 0:
            continue
        centroid = trapezoid(x * y, x) / area
        numerator += centroid * degree
        denominator += degree

    if denominator == 0:
        return 0

    return round(numerator / denominator, 2)


if __name__ == "__main__":
    temperature_sets_json = open('temp_json.json', 'r', encoding='utf-8').read()
    heating_sets_json = open('heat_json.json', 'r', encoding='utf-8').read()
    rules_json = open('rules_json.json', 'r', encoding='utf-8').read()

    current_temp = -14.00
    optimal_heating = main(temperature_sets_json, heating_sets_json, rules_json, current_temp)
    print(f"Оптимальный уровень нагрева при температуре {current_temp}°C: {optimal_heating}")

    current_temp = 12
    optimal_heating = main(temperature_sets_json, heating_sets_json, rules_json, current_temp)
    print(f"Оптимальный уровень нагрева при температуре {current_temp}°C: {optimal_heating}")
