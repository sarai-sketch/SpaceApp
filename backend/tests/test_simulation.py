from app.models.schemas import Scenario
from app.simulation.water import simulate

def test_three_days():
    r=simulate(Scenario())
    assert len(r['daily'])==3
    assert r['summary']['rain_total_mm']==21
    assert r['summary']['final_temp_mean_c']==4
    assert 0 <= r['summary']['available_water_mm'] <= r['summary']['taw_mm']

def test_zero_rain():
    r=simulate(Scenario(rain_change_pct=-100))
    assert r['summary']['rain_total_mm']==0

def test_water_conservation_day1():
    s=Scenario()
    r=simulate(s)['daily'][0]
    initial=1000*(s.field_capacity-s.soil_moisture)*s.root_depth_m
    expected=initial-r['rain_mm']+r['runoff_mm']+r['eta_mm']+r['drainage_mm']-s.irrigation_mm_day
    assert abs(r['depletion_mm']-expected)<.01
