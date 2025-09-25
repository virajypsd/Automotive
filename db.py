# db.py
session.add(car)
session.commit()
session.refresh(car)
return car


def get_all_cars(session):
return session.query(Car).order_by(Car.id).all()


def find_car_by_code(session, car_code):
return session.query(Car).filter(Car.car_code == car_code).first()


def delete_car(session, car_id):
car = session.query(Car).get(car_id)
if car:
session.delete(car)
session.commit()
return True
return False


def add_daily_log(session, car_id, date, distance_km, fuel_liters, notes=None):
mileage = None
if fuel_liters and fuel_liters > 0:
mileage = distance_km / fuel_liters
log = DailyLog(car_id=car_id, date=date, distance_km=distance_km, fuel_liters=fuel_liters, mileage=mileage, notes=notes)
session.add(log)
session.commit()
session.refresh(log)
return log


def get_logs_dataframe(session, start_date=None, end_date=None, car_ids=None):
import pandas as pd
q = session.query(DailyLog).join(Car)
if car_ids:
q = q.filter(DailyLog.car_id.in_(car_ids))
if start_date:
q = q.filter(DailyLog.date >= start_date)
if end_date:
q = q.filter(DailyLog.date <= end_date)
rows = q.order_by(DailyLog.date).all()
data = []
for r in rows:
data.append({
'log_id': r.id,
'car_id': r.car_id,
'car_code': r.car.car_code,
'date': r.date,
'distance_km': r.distance_km,
'fuel_liters': r.fuel_liters,
'mileage': r.mileage,
'notes': r.notes,
})
if data:
df = pd.DataFrame(data)
else:
df = pd.DataFrame(columns=['log_id','car_id','car_code','date','distance_km','fuel_liters','mileage','notes'])
return df
