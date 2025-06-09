import streamlit as st
from datetime import date
import pandas as pd
import db
import analysis


def main():
    conn = db.get_conn()
    db.init_db(conn)
    st.title("Self-Experiment Tracker")

    with st.form("entry_form", clear_on_submit=True):
        st.subheader("New Entry")
        date_value = st.date_input("Date", value=date.today())
        intervention = st.text_input("Intervention")
        dose = st.text_input("Dose / Intensity")
        mood = st.slider("Mood", 1, 10, 5)
        focus = st.slider("Focus", 1, 10, 5)
        sleep_quality = st.slider("Sleep Quality", 1, 10, 5)
        heart_rate = st.number_input("Heart Rate", step=1.0, format="%0.1f")
        sleep_hours = st.number_input("Sleep Hours", step=0.5)
        notes = st.text_area("Notes")
        tags_text = st.text_input("Tags (comma separated)")
        submitted = st.form_submit_button("Add")
        if submitted:
            tags = [t.strip() for t in tags_text.split(',') if t.strip()]
            db.add_entry(
                intervention=intervention,
                dose=dose,
                date_value=date_value,
                mood=mood,
                focus=focus,
                sleep_quality=sleep_quality,
                heart_rate=heart_rate,
                sleep_hours=sleep_hours,
                notes=notes,
                tags=tags,
                conn=conn,
            )
            st.success("Added entry")

    st.subheader("Entries")
    df = analysis.load_dataframe()
    if not df.empty:
        unique_tags = sorted({t for sub in df['tags'].dropna() for t in str(sub).split(',') if t})
        tag_filter = st.multiselect("Filter by tag", unique_tags)
        intervention_filter = st.text_input("Filter by intervention")
        filtered = df
        if tag_filter:
            filtered = filtered[filtered['tags'].apply(lambda x: any(tag in str(x) for tag in tag_filter))]
        if intervention_filter:
            filtered = filtered[filtered['intervention'].str.contains(intervention_filter, case=False)]
        st.dataframe(filtered.sort_values('date', ascending=False))

        metric = st.selectbox("Plot metric", ['mood', 'focus', 'sleep_quality'])
        fig = analysis.plot_trend(metric, None, None)
        if fig:
            st.pyplot(fig)
    else:
        st.write("No entries yet.")

    if st.button("Export CSV"):
        analysis.export_csv("export.csv")
        with open("export.csv", "rb") as f:
            st.download_button(label="Download", data=f, file_name="entries.csv", mime="text/csv")


if __name__ == "__main__":
    main()
