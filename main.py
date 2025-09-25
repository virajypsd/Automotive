# main.py
else:
add_car(session, car_code, model, reg_no, driver)
st.success('Car added successfully')
session.close()


# --- Manage Cars ---
elif page == 'Manage Cars':
st.title('Manage Cars')
session = get_session()
cars = get_all_cars(session)
if cars:
df = pd.DataFrame([{'id':c.id,'car_code':c.car_code,'model':c.model,'reg_no':c.reg_no,'driver':c.driver} for c in cars])
st.dataframe(df)
car_to_delete = st.selectbox('Select car to delete', options=[(c.id, c.car_code) for c in cars], format_func=lambda x: x[1])
if st.button('Delete selected car'):
car_id = car_to_delete[0]
delete_car(session, car_id)
st.success('Car deleted')
st.experimental_rerun()
else:
st.info('No cars in database yet. Add one from Add Car page.')
session.close()


# --- Add Daily Log ---
elif page == 'Add Daily Log':
st.title('Add Daily Log')
session = get_session()
cars = get_all_cars(session)
if not cars:
st.info('No cars available. Add a car first.')
else:
with st.form('add_log'):
car_choice = st.selectbox('Select car', options=[(c.id, c.car_code) for c in cars], format_func=lambda x: x[1])
date = st.date_input('Date', value=datetime.date.today())
distance_km = st.number_input('Distance (km)', min_value=0.0, format='%f')
fuel_liters = st.number_input('Fuel used (L)', min_value=0.0, format='%f')
notes = st.text_area('Notes (optional)')
submit = st.form_submit_button('Add log')
if submit:
car_id = car_choice[0]
add_daily_log(session, car_id, date, distance_km, fuel_liters, notes)
st.success('Log added')
session.close()


# --- Logs ---
elif page == 'Logs':
st.title('Logs & Filters')
session = get_session()
cars = get_all_cars(session)
car_options = [c.id for c in cars]
car_filter = st.multiselect('Filter by car', options=car_options, format_func=lambda id: next((c.car_code for c in cars if c.id==id),'Unknown'))
start_date = st.date_input('Start date', value=datetime.date.today() - datetime.timedelta(days=30))
