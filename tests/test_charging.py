"""
Unit tests for battery simulation and charging logic.
Tests charging stop detection and battery consumption calculations.
"""

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'app')))

from charging import compute_battery_usage, format_battery_level
from data import get_distance


def test_no_charging_needed_short_route():
    """
    Test that no charging is needed for a short route within battery range.
    """
    route = ["Los Angeles", "Bakersfield"]
    battery_range = 200  # More than enough for 110 miles
    
    result = compute_battery_usage(route, battery_range)
    
    assert result['feasible'] is True
    assert len(result['charging_stops']) == 0
    assert len(result['segments']) == 1


def test_charging_stops_detected():
    """
    Test that charging stops are correctly identified when battery range is small.
    
    With 150-mile range, LA to SF should require charging at intermediate cities.
    """
    route = ["Los Angeles", "Bakersfield", "Fresno", "Modesto", "San Francisco"]
    battery_range = 150
    
    result = compute_battery_usage(route, battery_range)
    
    assert result['feasible'] is True
    # Should need charging at Bakersfield and Fresno
    assert len(result['charging_stops']) >= 2
    assert "Bakersfield" in result['charging_stops']
    assert "Fresno" in result['charging_stops']


def test_battery_consumption_calculation():
    """
    Test that battery consumption is calculated correctly.
    """
    route = ["Los Angeles", "Bakersfield"]
    battery_range = 220  # 110 miles uses 50% battery
    
    result = compute_battery_usage(route, battery_range)
    
    assert result['feasible'] is True
    assert len(result['segments']) == 1
    
    segment = result['segments'][0]
    # Distance is 110 miles, range is 220, so consumption should be 50%
    assert segment['battery_consumed'] == 50.0
    assert segment['battery_after'] == 50.0


def test_infeasible_route_no_charging_station():
    """
    Test that route is marked infeasible if battery depletes at city without charging.
    
    San Francisco has no charging station, so if battery runs out there, route fails.
    """
    route = ["Modesto", "San Francisco"]
    battery_range = 50  # Not enough for 80 miles
    
    result = compute_battery_usage(route, battery_range)
    
    # Should be infeasible because SF has no charging station
    assert result['feasible'] is False
    assert result['error_message'] is not None


def test_segment_too_long():
    """
    Test that route is infeasible if a single segment exceeds battery range.
    """
    route = ["Los Angeles", "Fresno"]  # 220 miles direct
    battery_range = 200  # Not enough
    
    result = compute_battery_usage(route, battery_range)
    
    assert result['feasible'] is False
    # The error message indicates battery depletion at the starting city
    assert "Battery depleted before Fresno" in result['error_message']
    assert "Los Angeles has no charging station" in result['error_message']


def test_battery_recharge_to_full():
    """
    Test that battery recharges to 100% at charging stations.
    """
    route = ["Los Angeles", "Bakersfield", "Fresno"]
    battery_range = 150
    
    result = compute_battery_usage(route, battery_range)
    
    assert result['feasible'] is True
    
    # After charging at Bakersfield, battery should be back to 100%
    if "Bakersfield" in result['charging_stops']:
        # Find segment after Bakersfield
        for segment in result['segments']:
            if segment['from'] == "Bakersfield":
                # Battery should be 100% at start of this segment (after charging)
                assert segment['battery_before'] == 100.0


def test_empty_route():
    """
    Test handling of empty route.
    """
    route = []
    battery_range = 200
    
    result = compute_battery_usage(route, battery_range)
    
    assert result['feasible'] is True
    assert len(result['segments']) == 0
    assert len(result['charging_stops']) == 0


def test_single_city_route():
    """
    Test handling of route with single city (no segments).
    """
    route = ["Los Angeles"]
    battery_range = 200
    
    result = compute_battery_usage(route, battery_range)
    
    assert result['feasible'] is True
    assert len(result['segments']) == 0
    assert len(result['charging_stops']) == 0


def test_battery_level_formatting():
    """
    Test battery level visual formatting.
    """
    # Test full battery
    formatted = format_battery_level(100.0)
    assert "100.0%" in formatted
    assert "█" in formatted
    
    # Test half battery
    formatted = format_battery_level(50.0)
    assert "50.0%" in formatted
    
    # Test low battery
    formatted = format_battery_level(10.0)
    assert "10.0%" in formatted


def test_multiple_charging_stops():
    """
    Test route requiring multiple charging stops.
    """
    route = ["Los Angeles", "Bakersfield", "Fresno", "Modesto", "San Francisco"]
    battery_range = 120  # Small range requiring frequent charging
    
    result = compute_battery_usage(route, battery_range)
    
    assert result['feasible'] is True
    # Should need multiple charging stops
    assert len(result['charging_stops']) >= 2


def test_sufficient_range_no_charging():
    """
    Test that with very large battery range, no charging is needed.
    """
    route = ["Los Angeles", "Bakersfield", "Fresno", "Modesto", "San Francisco"]
    battery_range = 500  # Plenty of range
    
    result = compute_battery_usage(route, battery_range)
    
    assert result['feasible'] is True
    assert len(result['charging_stops']) == 0


def test_battery_never_negative():
    """
    Test that battery level never goes negative in feasible routes.
    """
    route = ["Los Angeles", "Bakersfield", "Fresno"]
    battery_range = 150
    
    result = compute_battery_usage(route, battery_range)
    
    if result['feasible']:
        for segment in result['segments']:
            assert segment['battery_after'] >= 0
            assert segment['battery_before'] >= 0
